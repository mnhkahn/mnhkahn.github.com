---
layout: post
title: 'Superpowers 如何“插装”进 Claude Code：注入机制与双环执法架构'
description: '拆解 Superpowers 如何通过 Claude Code 原生 Plugin + Hooks 注入强制性 Meta-Skill，以及它「离线 eval 执法 + 运行时行为塑形」的双环架构——运行时几乎不执行代码，真正的强制力来自离线评估闭环。'
category: "AI"
tags: ["AI", "Claude Code", "Superpowers", "Hook", "Eval"]
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

# 注入只是上半场：运行时几乎不执行代码

到这里讲的全是「怎么把强制令注入进去」。但注入只是把话说出口——**模型听不听是另一回事**。Superpowers 凭什么相信模型真会遵守那些纯文本铁律？答案不在运行时。

直觉上，一个号称能强制 agent「先写测试再写实现」「违规就删掉重来」的框架，应该有一堆拦截逻辑。实际拆开看，运行时空得惊人。

## 14 个 Skill，98% 是纯 Markdown

Superpowers 的 Skill 目录里，绝大多数文件是 `SKILL.md`——铁律横幅、红旗表、合理化反制表、流程图、正反例、子代理模板，全是**给模型读的文字**。它们不被任何解析器消费，不触发任何代码路径。

唯一称得上「代码」的，是 subagent-driven-development（SDD）里的三个 bash helper，而且**需要模型主动调用**才会跑——模型不调，它们就是磁盘上的死文件。

## 运行时没有任何看门狗

把常见的「强制」手段逐一对照，会发现 Superpowers 一个都没在运行时落地：

| 你以为有的强制手段 | Superpowers 实际有没有 |
|---|---|
| 工具调用拦截（PreToolUse 拦危险命令） | ❌ 没有 |
| 文件写入看门（写非测试文件前先检查有没有测试） | ❌ 没有 |
| Git Hook（commit 前跑校验） | ❌ 没有 |
| 「删除违规代码重来」的执行器 | ❌ 没有，纯文字要求 |

所以像 TDD skill 里「如果你先写了实现，删掉它，重新从测试开始」这种话，**没有任何机制保证它发生**。它能不能生效，取决于模型读到这句话时愿不愿意照做。这是**心理约束力**，不是系统约束力。

如果运行时这么空，Superpowers 又确实能改变 agent 行为，强制力必然来自别处——它来自两个地方：一是上面讲的注入时机（保证铁律一直在窗口里），二是离线把 prompt 调到模型肯遵守的程度。后者才是真正的「执法机关」。

---

# 真正的执法：离线 Quorum Eval 闭环

这套机制不在你的 session 里，而在作者开发 Skill 时跑的离线评估管线里。

## 为什么纯 prompt 约束必须配 eval

纯 prompt 约束有个致命问题：**你怎么知道这段措辞真的管用？** 把「YOU MUST USE THE SKILL」改成「Please consider using the skill」，遵从率会掉多少？把红旗表删掉，模型会不会开始找借口跳过流程？这些问题没法靠读 prompt 拍脑袋回答，只能**测**。Quorum Eval 就是这套测量工具。

## 双 LLM 分离评审

核心是把「跑场景」和「评判结果」拆给两个独立的 LLM：

- 一个 LLM 扮演 agent，在某个场景里实际执行任务（比如「修个 bug」，看它有没有先调 systematic-debugging）；
- 另一个 LLM 当评审，读这条执行轨迹，判断 Skill 遵从率。

分离的意义在于**避免「自己批改自己作业」的偏袒**——执行者和评审者不是同一次推理，评审更客观。

## 确定性时序检查可以推翻 LLM 判决

光靠 LLM 评审还不够，因为 LLM 评审本身也会出错、会被说服。所以 Quorum Eval 叠了一层**确定性检查**：

- 一组**轨迹动词**（trajectory verbs）——针对执行轨迹做时序断言，比如「写测试这个动作必须出现在写实现之前」；
- 一组**文件系统动词**（filesystem verbs）——针对落盘结果做断言，比如「测试文件必须存在」。

这些检查是**确定性**的（不是 LLM 主观判断），所以当它们和 LLM 评审冲突时，**确定性检查可以推翻 LLM 判决**。比如 LLM 评审说「这条轨迹遵守了 TDD」，但时序检查发现实现文件的写入时间早于测试文件，那就直接判定违规——不管 LLM 怎么说。这是整套架构里少有的「硬」逻辑：**用确定性时序断言给主观的 LLM 评审兜底。**

## eval 数据驱动的 prompt 调优闭环

把上面的拼起来，就是 Superpowers 真正的开发循环：

```
写/改某条 Skill 的 prompt 措辞
        ↓
拿几十个场景跑 Quorum Eval
（双 LLM 分离评审 + 确定性时序/文件系统检查）
        ↓
得到这条 Skill 的遵从率
        ↓
遵从率不达标 → 回头改 prompt 措辞
（加强铁律横幅 / 补红旗表 / 加反合理化条目）
        ↓
再跑 eval → 直到遵从率达标
```

**运行时的强制力，是离线这个闭环「调」出来的。** 铁律横幅为什么写成全大写、为什么要列「你可能会这样想……（错）」的反合理化表、为什么流程图画成状态机——这些不是作者的文学偏好，是 eval 数据反复验证后留下的、能把遵从率顶上去的措辞。

---

# 「想起」从哪来：模型为什么会在发命令前改主意

理解了「注入 + eval」双环，就能解释一个常见现象：模型本来打算「马上 git commit」，结果在真正发出工具调用之前，自己改了主意先去跑测试或审查。这个「想起」从哪来？

## 三层上下文一直在窗口里

```
                  ┌─ "想起"的来源：三层上下文一直在窗口里
                  │   ① using-superpowers 强制令（session 注入，compact 重注）
                  │   ② 之前读过的 TDD skill（还在窗口）
                  │   ③ verification skill 的 description（被工具元数据检索到）
                  │
"马上 git commit"  ─┤
                  │   推理是原子的：在工具调用发出去之前，模型自己改主意了
                  │   └─> 没有"撤回"，只是同一轮推理里修正了最终输出
                  │
                  ├─ 一旦真的发出去了且通过了：
                  │   Inline → 看运气（约 50% 自己 git reset）
                  │   SDD    → 3 个外循环兜底：Task Reviewer / Final Reviewer /
                  │                          finishing Step 1 真跑 pytest
                  │
                  └─ 全部都是模型内循环？
                      Inline：是，单点失败
                      SDD：大部分是，但审查/测试被外置到独立的子代理和硬性步骤上，
                           是流程结构保证了"被检查"这件事一定会发生，
                           不依赖某个模型某个瞬间的记忆力。
```

关键在于：**模型不是发出命令后被拦下来，而是在同一轮推理里、命令还没出口时就修正了。** 没有「撤回」这个动作，因为根本没发出去。这正是接入层的价值——它保证那三层文本一直在窗口里，模型每次推理都能「看见」，于是有机会在最后一刻改主意。而这张图的下半段已经预告了后文要展开的对比：同样发生了「想起」，Inline 和 SDD 的兜底强度完全不同。

## 但内循环是单点失败

问题是：这个「改主意」发生在模型的内循环里，**全凭那一刻的记忆力和自觉**。如果模型这次就是没想起来，命令照发不误。一旦真的发出去且通过了，在 **Inline 模式**（在主会话里直接干活）下就只能看运气——大约一半情况模型自己会 `git reset` 补救，另一半就这么过去了。单点失败的根源就在这：**约束力是心理的，没有结构兜底。**

---

# Inline vs SDD：把「被检查」从运气变成结构保证

Superpowers 真正解决单点失败的，是 subagent-driven-development（SDD）这条 Skill。它和 Inline 的差别不在「规则更严」，而在**把检查动作外置成独立的流程步骤**。

| 维度 | Inline | SDD |
|---|---|---|
| 干活在哪 | 主会话内循环 | 派独立子代理执行 |
| 检查靠什么 | 模型那一刻自觉 | 外置的独立步骤 |
| 失败模式 | 单点失败 | 结构兜底 |

- **Inline**：单点失败。干活、检查、补救全在同一个模型的同一条推理链上，哪一环掉了就掉了。
- **SDD**：大部分干活仍是模型内循环，但**审查和测试被外置到独立的子代理和硬性步骤上**。

## SDD 的三道外循环兜底

SDD 不指望某个模型某个瞬间记得要自检，而是用流程结构保证「被检查」这件事**一定会发生**：

1. **Task Reviewer**——每个子任务完成后，派一个独立的审查子代理去看结果。审查者和执行者不是同一次推理，绕开了「自己批改自己」。
2. **Final Reviewer**——整个分支完成后，再来一轮总审查。
3. **finishing 流程的 Step 1 真跑 pytest**——不是「请记得跑测试」，而是流程里写死的一步，真的执行测试命令。

这三道兜底的共同点：**它们是流程结构的一部分，不依赖某个模型某个瞬间的记忆力。** 执行者就算忘了自检，审查子代理也会被流程拉起来；就算审查者放水，finishing Step 1 的 pytest 还会硬跑一遍。

## 这其实是 eval 思路在运行时的投影

注意 SDD 的「双代理分离审查 + 硬性测试步骤」，和离线 Quorum Eval 的「双 LLM 分离评审 + 确定性检查」是**同一个设计哲学**：

> 不信任单次推理的自觉，用「分离的评审 + 确定性的检查」来兜底。

外环用它来离线打磨 prompt，SDD 用它来在运行时保证质量。**Superpowers 把同一套「分离 + 确定性兜底」的思想，同时用在了开发期和运行期。**

---

# 对我们自己的启示

如果想给 opencode / Claude Code / Codex 等编码 agent 增强行为约束，可以直接复用这套双环模式：

| 需求 | 复用 Superpowers 的哪一层 |
|---|---|
| 注册自定义 skill | `plugin.json` + `skills/` 目录 |
| 让 agent 想起某流程 | SessionStart Hook + 注入流程图（接入层） |
| 抗上下文压缩 | matcher 加 `compact` |
| 堵住 agent 偷懒 | 注入反合理化清单 |
| 跨平台兼容 | polyglot Hook 脚本 |
| 让那段文本真的管用 | 离线 eval：测遵从率，数据驱动改措辞 |
| 给 LLM 评审兜底 | 加一层确定性时序/状态断言，允许推翻 LLM 判决 |
| 让「被检查」可靠发生 | 把审查外置成独立子代理 + 硬性测试步骤，别靠模型自觉 |

**核心洞察**：Superpowers 看起来是一堆 Markdown 铁律，但它真正的架构是**「离线 eval 执法 + 运行时行为塑形」双环**——接入层解决「Skill 能不能被发现、会不会被触发」的一致性问题，eval 层解决「触发了之后模型到底遵不遵守」的质量问题，而运行时本身几乎不执行任何代码。把 LLM 从不可靠的"自由 agent"变成"流程合规 agent"，不需要 hack 宿主：只需要在**正确的时机**注入**正确的协议文本**，再用**离线评估闭环**把这段文本反复校准到模型肯就范，最后用 **SDD 的结构兜底**把"被检查"从运气变成必然。
