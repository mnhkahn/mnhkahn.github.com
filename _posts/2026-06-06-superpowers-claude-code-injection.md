---
layout: post
title: 'Superpowers 如何“插装”进 Claude Code：插件、Hooks 与协议注入'
description: '拆解 Superpowers 如何通过 Claude Code 原生 Plugin + Hooks 机制注入强制性 Meta-Skill，把“用不用 skill”从 agent 自由裁量变成必须执行的工作流协议。'
category: "AI"
tags: ["AI", "Claude Code", "Superpowers", "Hook", "Plugin"]
---

* 目录
{:toc}

---

Superpowers（`github.com/obra/superpowers`，219k stars）是当前最火的"AI 编码方法论框架"。它声称"装上后 Claude 就有了 Superpowers"，但**没有魔改 Claude Code 任何一行源码**。所有"插装"都走的是 Claude Code 官方的 Plugin + Hooks 扩展点。本文拆解它的注入机制、与原生 Skill 机制的差异，以及它在上下文压缩场景下的精妙设计。

---

# TL;DR

**Superpowers = Claude Code 原生 Plugin 机制 + SessionStart Hook 注入一段强制性 Meta-Skill。**

技术上零外部依赖、零二进制劫持、不改 Claude Code 源码。杠杆点只有一个：把“用不用 skill”从 agent 的**自由裁量**变成**必须执行的工作流协议**。

---

# 三层结构

## 插件清单（.claude-plugin/plugin.json）

```json
{
  "name": "superpowers",
  "description": "Core skills library for Claude Code: TDD, debugging, ...",
  "version": "5.1.0",
  ...
}
```

这只是声明"我是一个叫 superpowers 的插件"，让 Claude Code 在 `/plugin install` 时认识它。配套的 `.claude-plugin/marketplace.json` 把它登记到 marketplace，本质都是元数据。

## Hook 注册（hooks/hooks.json）

这是**真正的插装点**：

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}/hooks/run-hook.cmd\" session-start",
            "async": false
          }
        ]
      }
    ]
  }
}
```

`async: false` 意味着 Claude Code **同步执行**这个命令，并把它 stdout 输出的 JSON 解析为 `additionalContext`，**拼接到新会话的 system prompt 里**。

`run-hook.cmd` 是个 polyglot 脚本：Windows 上是 cmd 块（找 Git Bash 调用），Unix 上是 bash 块（直接 exec）。这样同一个 `session-start` 脚本跨平台。

## 注入内容（hooks/session-start）

bash 脚本核心逻辑：

1. 读 `skills/using-superpowers/SKILL.md` 全文；
2. bash 参数替换做 JSON 转义（`${s//\\/\\\\}` 这种，避开 bash 5.3 heredoc hang 的 bug）；
3. 套上 `<EXTREMELY_IMPORTANT>` 标签；
4. 按当前宿主输出对应字段名（Claude Code / Cursor / Copilot CLI 各家协议不同）；
5. 退出 0。

最终注入到 system prompt 的内容长这样（简化）：

```xml
<EXTREMELY_IMPORTANT>
You have superpowers.

**Below is the full content of your 'superpowers:using-superpowers' skill...**

[skills/using-superpowers/SKILL.md 全文]

</EXTREMELY_IMPORTANT>
```

## 注入机制：stdout JSON 契约

上一节留了一个关键问题没说透：**hook 子进程退出后，它的输出是怎么变成 system prompt 的？** 没有常驻连接、没有共享内存、没有回调函数——hook 只是一次同步子进程调用。

完整机制：

```
SessionStart 事件触发
  ↓
Claude Code fork 子进程执行 hooks.json 里配置的 command
  ↓
子进程把 JSON 写到 stdout 后退出（exit 0）
  ↓
Claude Code 读取 stdout，按 JSON schema 解析
  ↓
识别 hookSpecificOutput.additionalContext 字段
  ↓
把这个字符串拼接到新会话的 system prompt（harness 内部决定拼头部/尾部）
  ↓
会话开始
```

**真正干"插入"动作的是 Claude Code 自己，不是 hook 脚本。** Hook 只是个信使，stdout 就是信的内容。Superpowers 写的 `session-start` bash 脚本本质是：**按 SessionStart 事件的 JSON schema 严格格式化一段字符串，输出到 stdout。** 之后的事 harness 处理。

### additionalContext 永远追加，不挑食

对 SessionStart 这个事件，**`additionalContext` 永远会被追加进 system prompt**——harness 不会判断"这段值不值得注入"，看到字段就拼。具体行为：

- **每个事件匹配都注入一次**：`startup|clear|compact` 命中一次，脚本跑一次，stdout 拼一次
- **多 hook 都注入**：同一事件注册多个 hook，每个 hook 输出的 `additionalContext` **都会被追加**，harness 不做去重也不做排序，简单拼接
- **不可撤回**：进了 system prompt 就是 prompt 的一部分，agent 自己不能删除或修改。`<EXTREMELY_IMPORTANT>` 标签只是给 LLM 看的"权重提示"，不是真系统级保护——但 LLM 会当真

整套机制能成立就建立在这个"机械式契约"上：Claude Code 不挑食、不判断、看到字段就拼。

### 关键陷阱：harness 不做字段去重

这是 `session-start` 脚本注释里专门警告的坑：

```bash
# Claude Code reads BOTH additional_context and hookSpecificOutput without
# deduplication, so we must emit only the field the current platform consumes.
```

意思是 Claude Code 同时识别**两种** schema：

| 字段 | 谁用 |
|---|---|
| `additional_context`（snake_case） | Cursor |
| `hookSpecificOutput.additionalContext`（嵌套） | Claude Code |
| `additionalContext`（顶层） | Copilot CLI / SDK 标准 |

**两个字段它都读、都拼、不去重。** 如果脚本同时输出 `additional_context` 和 `hookSpecificOutput.additionalContext`，agent 会看到**两遍** `<EXTREMELY_IMPORTANT>You have superpowers...`，不仅冗余还可能让 LLM 困惑。

所以脚本里必须有 if/else 分支，严格只输出当前宿主该用的字段名：

```bash
if [ -n "${CURSOR_PLUGIN_ROOT:-}" ]; then
  # Cursor → additional_context
  printf '{\n  "additional_context": "%s"\n}\n' "$session_context"
elif [ -n "${CLAUDE_PLUGIN_ROOT:-}" ] && [ -z "${COPILOT_CLI:-}" ]; then
  # Claude Code → hookSpecificOutput.additionalContext
  printf '{\n  "hookSpecificOutput": { ... } }\n' "$session_context"
else
  # Copilot CLI → additionalContext（SDK 标准）
  printf '{\n  "additionalContext": "%s"\n}\n' "$session_context"
fi
```

**字段去重是 hook 写作者的活，harness 不帮你擦屁股。**

### 跨平台 polyglot 的同款机制

`run-hook.cmd` 是同一个模式的递归应用——

```bash
# Unix 分支
exec bash "${SCRIPT_DIR}/${SCRIPT_NAME}" "$@"
```

父进程 `run-hook.cmd` 收到 `session-start` 参数，调子 bash 执行真正的脚本，把子 bash 的 stdout 透传回自己的 stdout。整条链路是**单向 IPC 管道**：

```
Claude Code → run-hook.cmd stdout → bash session-start stdout → Claude Code
```

`run-hook.cmd` 自己不产生 JSON，它只做"找到 bash 并把子进程的 stdout 透传"。这种 polyglot 设计保证了 Windows / Unix 走的是同一份 `session-start` 脚本，行为一致。

### 其他 hook 事件的契约

Claude Code 的 hook 体系是一套**多事件多 schema** 的设计，不止 SessionStart 一招。每种事件有自己专属的 JSON schema，harness 按字段执行对应动作：

| Hook 事件 | 触发时机 | stdout JSON 能干什么 |
|---|---|---|
| `SessionStart` | 会话启动/清空/压缩 | `additionalContext` 注入 system prompt |
| `UserPromptSubmit` | 用户消息发送前 | 可注入上下文、追加信息 |
| `PreToolUse` | 工具调用前 | `permissionDecision: deny` 拦截、修改工具参数 |
| `PostToolUse` | 工具返回后 | 往工具结果里塞额外上下文 |
| `Stop` | agent 尝试停下时 | `decision: block` 阻止停止（强制继续） |
| `SubagentStop` | 子 agent 结束时 | 同 Stop |
| `Notification` | 通知发出时 | 拦截/修改通知 |

**这套契约就是"在不修改 Claude Code 源码的前提下扩展其行为"的完整接口。** Superpowers 只用了 SessionStart 一个事件；其他事件留出了大量未被开发的扩展空间——比如用 PreToolUse 拦截危险命令、用 Stop 强制 agent 完成自检流程。

### 为什么必须包 JSON：每种事件的返回字段不同

上表的"能干什么"看起来很泛，落到 JSON 上每个事件有**专属字段名**，harness 按字段决定动作：

| 事件 | 返回字段 | 字段作用 |
|---|---|---|
| `SessionStart` | `hookSpecificOutput.additionalContext` | 字符串注入到 system prompt |
| `UserPromptSubmit` | `hookSpecificOutput.additionalContext` | 字符串拼到用户消息上下文 |
| `PreToolUse` | `hookSpecificOutput.permissionDecision` | `"allow"` / `"deny"` / `"ask"` 控制工具调用 |
| `PreToolUse` | `hookSpecificOutput.updatedInput` | 对象，改写即将传入工具的参数 |
| `PostToolUse` | `hookSpecificOutput.additionalContext` | 字符串塞到工具返回值后面 |
| `Stop` | `hookSpecificOutput.decision` | `"block"` 阻止 agent 停止（强制继续） |
| `SubagentStop` | `hookSpecificOutput.decision` | 同 Stop，作用域为子 agent |
| `Notification` | （拦截/改写通知内容） | 修改发给用户的通知 |

可见：

- **同一字段名在不同事件里有不同语义**——`additionalContext` 在 SessionStart 进 system prompt，在 PostToolUse 进工具结果。所以 `hookEventName` 这个标签**必须带**，harness 不能只看字段值。
- **PreToolUse 一个事件能返回多个字段**——`permissionDecision` 和 `updatedInput` 都在 `hookSpecificOutput` 下面共存，可以同时拒绝 + 改写。
- **JSON 是"带类型标签的 IPC 信封"**——`hookEventName` 是类型，`hookSpecificOutput.*` 是 payload。即使 SessionStart 现在只用一个字段，外壳也必须是 JSON，因为所有事件共用同一套解析器，且 PreToolUse 这种需要返回**多个结构化字段**的事件必须靠 JSON 表达。

如果 hook 只回 raw text，harness 拿到 `"deny"` 该当权限拦截还是当文本注入？拿到 `"block"` 该当阻止停止还是当字符串？**没有结构就没有语义边界**。

### 动手验证：自己跑一遍这条管道

上面全是原理，把整套链路在 Mac 上**自己执行**一遍最快。Claude Code 实际 spawn 的就是 `run-hook.cmd session-start` 这一个命令：

```bash
cd ~/.cache/opencode/packages/superpowers@git+https:/github.com/obra/superpowers.git/node_modules/superpowers/hooks && \
CLAUDE_PLUGIN_ROOT="$(cd .. && pwd)" bash run-hook.cmd session-start
```

`run-hook.cmd` 是 polyglot：前 40 行是 bash 的 `: << 'CMDBLOCK'` no-op heredoc，Unix 上被当空操作跳过，从第 42 行起才是真 Unix 分支 `exec bash session-start`。所以 Mac/Linux 上必须**显式用 bash 解释执行**（文件没 shebang，裸跑 `execve` 会拒绝）。

抽出 `additionalContext` 字段（去掉 JSON 信封）：

```bash
cd ~/.cache/opencode/packages/superpowers@git+https:/github.com/obra/superpowers.git/node_modules/superpowers/hooks && \
CLAUDE_PLUGIN_ROOT="$(cd .. && pwd)" bash run-hook.cmd session-start \
  | jq -r '.hookSpecificOutput.additionalContext' | head -40
```

输出就是真正被 Claude Code 拼到 system prompt 的内容——开头是 session-start 脚本自己套的 `<EXTREMELY_IMPORTANT>You have superpowers.</EXTREMELY_IMPORTANT>` 外壳，里面嵌一层 using-superpowers skill 自带的 `<EXTREMELY_IMPORTANT>` 强约束声明。**两层标签嵌套**：外层是 hook 注入的元协议，内层是 skill 自己的"1% 相关就必须用 skill"。

看 JSON 信封结构（验证 `hookEventName` 标签 + `\n` 转义）：

```bash
cd ~/.cache/opencode/packages/superpowers@git+https:/github.com/obra/superpowers.git/node_modules/superpowers/hooks && \
CLAUDE_PLUGIN_ROOT="$(cd .. && pwd)" bash run-hook.cmd session-start | jq 'keys, .hookSpecificOutput | keys'
```

输出：

```json
[
  "hookSpecificOutput"
]
[
  "additionalContext",
  "hookEventName"
]
```

三行命令就能把整篇第一节讲的"Claude Code 怎么把 stdout 变成 system prompt"在本地复现一遍。

---

# 与默认 Skill 加载的本质差异

Claude Code 原生就有 Skill 机制：把 `SKILL.md` 放到 `~/.claude/skills/` 或 `.claude/skills/`，自动注册到 `Skill` 工具的可用列表。那 Superpowers 到底改了什么？

## 默认是"能力暴露"，Superpowers 是"行为约束"

| 维度 | Claude Code 原生 | Superpowers |
|---|---|---|
| Skill 注册 | 工具列表中可见 | 工具列表中可见 |
| 加载决策方 | **Agent 自主判断** | **强制**：1% 相关就加载 |
| 元规则加载 | 无（无法加载，因为没人告诉 agent 必须加载） | SessionStart 注入，绕开 agent 决策 |
| 对抗偷懒 | 无 | 显式反合理化清单 |
| 流程定义 | 自由 | 状态机式流程图 |
| 优先级 | 默认行为为最高 | 显式压过默认系统 prompt |

## 元规则免疫的精妙设计

`using-superpowers` 这条 skill 自己**不是通过 Skill 工具加载的**——如果它走 Skill 工具，就会陷入"agent 觉得不需要就不加载"的死结。

它走的是 `SessionStart` Hook → `additionalContext` → 直接进 system prompt。所以"强制检查并加载 skill"这条规则本身**是被强制注入的**，免疫于它自己所对抗的"agent 自由裁量"问题。

## 反合理化（Anti-Rationalization）武器

`using-superpowers` skill 里的核心话术：

> **IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.**
>
> This is not negotiable. This is not optional. You cannot rationalize your way out of this.

并附带流程图：

```
用户消息 → "有没有 skill 可能相关？" → 是（哪怕 1%）→ 必须先调 Skill 工具 → 才能回复
```

以及 Red Flags 清单，明确把以下念头标记为**正在合理化 = 必须停下来**：

- "这任务简单，跳过流程"
- "用户赶时间"
- "我直接写代码更快"
- "这个 skill 不完全适用"

这是从 CBT（认知行为疗法）借来的行为干预技术，针对 LLM "急于产出答案"的默认倾向。**不是告诉 agent 怎么做，而是堵死它逃避的借口。**

## 优先级覆盖

skill 文本里有一句关键声明：

> Superpowers skills override default system prompt behavior, but user instructions always take precedence

意思是：当 Superpowers 与 Claude Code 默认的"快速帮用户"倾向冲突时，**Superpowers 赢**。这等于在 system prompt 内部立了一个"宪法层"。

---

# 最精妙的一招：抗上下文压缩

`hooks.json` 的 matcher 是 `startup|clear|compact`，**包括 `compact`**。

这意味着：

## 默认行为下的脆弱性

默认机制里，Skill 工具的返回值（skill 全文）会变成**普通对话内容**进入上下文。当上下文撑爆触发自动 compact 时，这些 skill 文本**会一起被压缩掉**——时间一长，agent 就"忘了还有 TDD 这回事"。

## Superpowers 的解法

SessionStart Hook 在每次 compact 之后**重新跑一次**，把 `using-superpowers` 全文连同反合理化清单**重新注入到 system prompt**。

```
compact 触发
   ↓
Hook 重跑
   ↓
"你必须用 skill" 协议重新进入 system prompt
   ↓
Agent 重新获得"先检查 skill"的约束
   ↓
Agent 通过 Skill 工具按需重新加载具体的 TDD / brainstorming 等
```

效果是**"协议持久 + 内容按需重拉"**：

- **元规则**（"1% 相关就用 skill"）→ durable，compact 后自动恢复
- **单个技能**（TDD / brainstorming）→ 仍然按需加载，但被元规则保护，会被自动重新调出来

简单说：默认是"skill 内容活在对话历史里、随压缩蒸发"；Superpowers 是"提醒器活在系统提示里、每次压缩后自动刷新"。

---

# 抽象出来的设计模式

Superpowers 展示了一套可复用的"在不修改 LLM 宿主的前提下改变 agent 行为"的设计模式：

## 三层插装模型

```
┌──────────────────────────────────────────────┐
│ 1. 插件清单（plugin.json）                      │
│    → 让宿主认识你                              │
├──────────────────────────────────────────────┤
│ 2. 生命周期 Hook（hooks.json）                 │
│    → 选择在哪个时机插装（startup/compact/...）  │
├──────────────────────────────────────────────┤
│ 3. 协议注入（session-start 脚本）               │
│    → 注入的文本里包含：                         │
│       - 强制规则（"必须 X"）                    │
│       - 状态机流程图（"先 A 再 B"）              │
│       - 反合理化清单（"这些念头都是借口"）       │
│       - 优先级声明（"我覆盖默认行为"）            │
└──────────────────────────────────────────────┘
```

## 关键设计原则

1. **元规则不能依赖自己**——bootstrap 规则必须由系统级机制（Hook）直接注入，不能走 agent 自主决策的路径，否则陷入递归。

2. **抗压缩是必修课**——任何"agent 行为约束"如果不能扛住上下文压缩，撑不过一个长 session 就失效。匹配 `compact` matcher 是必备。

3. **协议比工具有效**——光给 agent 工具（Skill 工具）不够，必须配套硬性协议（"必须调"）和反合理化（"不许找借口不调"）。

4. **跨平台 polyglot**——Hook 脚本是 polyglot（`run-hook.cmd` 同一个文件 Windows cmd 块 + Unix bash 块），保证 Claude Code / Cursor / Copilot CLI 等不同宿主都能跑。

5. **行为杠杆在文本里**——Superpowers 90% 的代码是 Markdown 文本。"插装"本质是 prompt engineering 在系统提示层面的工程化版本。

---

# 对我们自己的启示

如果想给 opencode / Claude Code / Codex 等编码 agent 增强行为约束，可以直接复用这个模式：

| 需求 | 复用 Superpowers 的哪一层 |
|---|---|
| 注册自定义 skill | `plugin.json` + `skills/` 目录 |
| 强制 agent 走某流程 | SessionStart Hook + 注入流程图 |
| 抗上下文压缩 | matcher 加 `compact` |
| 堵住 agent 偷懒 | 注入反合理化清单 |
| 跨平台兼容 | polyglot Hook 脚本 |

**核心洞察**：LLM 是不可靠的"自由 agent"，把它变成"流程合规 agent"不需要 hack 宿主，只需要在**正确的时机**向 system prompt 注入**正确的协议文本**。Superpowers 把这件事做到了极致。
