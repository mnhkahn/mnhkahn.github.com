---
layout: post
title: "Agent Harness 五源语：从不可靠的 LLM 到可靠的工程系统"
description: "解析 AI 编码代理 Harness 的五个核心源语——Skill、Rule、Hook、Memory、Eval，如何通过递进防御将概率性模型转化为可靠的工程系统。"
category: "AI"
tags: ["AI", "Agent", "Harness Engineering", "LLM", "工程实践"]
figure: "https://res.cloudinary.com/cyeam/image/upload/v1780324344/agent-harness-five-primitives_d6kmbc.svg"
---

* 目录
{:toc}

---

一个 AI 编码代理的核心难题是：**模型是无状态的、概率性的、不可靠的**。Harness 的本质就是用工程手段把一个不可靠的模型变成一个可靠的工程系统。五个源语各自解决这个大问题的一个侧面。

## 五源语总览

| 维度 | Skill | Rule | Hook | Memory | Eval |
|---|---|---|---|---|---|
| **保证什么** | 一致性 | 对齐性 | 安全性 | 连续性 | 正确性 |
| **一句话定义** | 同类任务每次执行方式相同、质量稳定 | 模型行为始终符合项目/团队的工程规范 | 危险操作在运行时被拦截，不可绕过 | 历史决策和知识跨会话保留，不遗忘 | 独立验证工作成果，"完成"必须可证明 |
| **解决什么问题** | 模型每次面对同类任务从零推理，既浪费 token 又不可控 | 模型默认行为是通用的，与特定项目要求脱节 | 仅靠 prompt 约束不够，关键路径需要程序化强制 | 模型每次会话都是白纸，无法积累项目经验 | 代理的"完成"声明不可信，模型有自我合理化倾向 |
| **没有它的风险** | 低效——每次重新推理，输出质量波动大 | 混乱——行为与项目规范脱节，需要反复纠正 | 危险——关键约束可被绕过，安全事故迟早发生 | 健忘——每次从零开始，无法积累项目经验 | 自欺——"完成"不可信，bug 流入生产环境 |
| **在 Harness 中的角色** | 能力层——"怎么做" | 规范层——"应该做" | 执行层——"必须做" | 状态层——"上次做" | 验证层——"做对了" |

## 协作链路与防御关系

五层保证是**递进防御**关系，不是并列关系。每层解决上一层无法覆盖的盲区：

```
用户需求
  │
  ▼
┌─────────────────────────────────────────────────────────┐
│ Skill 保证一致性                                         │
│ "按标准流程做" —— 模型不自由发挥，走验证过的工作流          │
└──────────────────────┬──────────────────────────────────┘
                       │ 一致 ≠ 正确 → 需要 Rule
  ▼
┌─────────────────────────────────────────────────────────┐
│ Rule 保证对齐性                                          │
│ "按项目规范做" —— 即使 Skill 没覆盖的场景，行为也符合约定   │
└──────────────────────┬──────────────────────────────────┘
                       │ 对齐 ≠ 执行 → 需要 Hook
  ▼
┌─────────────────────────────────────────────────────────┐
│ Hook 保证安全性                                          │
│ "危险操作拦得住" —— 即使 Rule 被忽略，运行时仍然安全        │
└──────────────────────┬──────────────────────────────────┘
                       │ 安全 ≠ 高效 → 需要 Memory
  ▼
┌─────────────────────────────────────────────────────────┐
│ Memory 保证连续性                                        │
│ "上次的经验这次用得上" —— 不重复踩坑，在历史基础上前进       │
└──────────────────────┬──────────────────────────────────┘
                       │ 连续 ≠ 正确 → 需要 Eval
  ▼
┌─────────────────────────────────────────────────────────┐
│ Eval 保证正确性                                          │
│ "做完了 = 做对了" —— 独立验证闭环，完成声明必须可证明       │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
                  可信的交付物
```

| 缺失层 | 系统症状 | 典型事故 |
|---|---|---|
| 无 Skill | 每次重新推理，输出质量波动 | 同类 code review 每次标准不同，漏检率不稳定 |
| 无 Rule | 行为与项目规范脱节 | 模型用 npm install 而项目用 bun，破坏锁文件 |
| 无 Hook | 关键约束可被绕过 | 模型执行 `git push --force` 覆盖远程分支 |
| 无 Memory | 每次从零开始 | 上次发现的数据库连接池问题下次又踩 |
| 无 Eval | "完成"不可信 | 模型声称修复了 bug 但实际未验证，bug 流入生产 |

## Skill — 保证一致性

**问题**：模型每次面对同类任务（如 code review、写单测、部署）都要从零推理，既浪费 token 又不可控。不同项目、不同会话重复造轮子。

**Skill 解决什么**：把**经过验证的工作流**打包成可复用的单元。一个 Skill 就是一个"配方"——规定了触发条件、可用工具、执行步骤和完成标准。模型不需要自己想怎么做，只需要判断"该用哪个 Skill"，然后按配方执行。

**在 Harness 中的角色**：Skill 是 Harness 的**能力层**，相当于给代理安装"技能包"。没有 Skill，代理是通用但浅薄的；有了 Skill，代理在特定领域是专业且可靠的。

**没有保证的风险**：

| 风险 | Skill 如何消除 |
|---|---|
| 每次写单测的方式不同，质量参差不齐 | 打包成标准工作流，按配方执行 |
| 新手不知道怎么做 code review，老手做法也不统一 | Skill 定义触发条件+工具+完成标准 |
| 复杂任务遗漏关键步骤 | Skill 模板化强制走完流程 |

**实现要点**：

- **核心类型**：`PromptCommand`（`src/types/command.ts`）
- **存储位置**：`.claude/skills/<name>/SKILL.md`
- **加载来源（6种，按优先级合并）**：bundledSkills → builtinPluginSkills → skillDirCommands → workflowCommands → pluginCommands → COMMANDS()
- **SKILL.md 格式**：

```yaml
---
description: 技能描述
when_to_use: 何时使用
allowed-tools: Bash,Read,Write
context: fork        # inline(默认) 或 fork(子代理)
paths: "src/**/*.ts" # 条件激活 glob
---
技能指令内容（支持 $ARGUMENTS, ${CLAUDE_SKILL_DIR}, !`shell` 注入）
```

- **触发方式**：模型通过 SkillTool 主动调用（技能清单通过 `system-reminder` 增量注入，token 预算 ≤ 上下文窗口 1%）
- **执行模式**：inline（直接注入 prompt）/ fork（独立子代理隔离执行）
- **条件激活**：`paths` frontmatter 让技能只在操作特定文件时才出现，避免上下文污染
- **模型能否绕过**：能（模型可以选择不调用 Skill）
- **安全机制**：fork 模式隔离执行，MCP skill 禁止 shell 注入

> 关键文件：`src/skills/loadSkillsDir.ts`、`src/tools/SkillTool/SkillTool.ts`、`src/commands.ts`

## Rule — 保证对齐性

**问题**：模型默认行为是通用的，但每个团队/项目有自己的工程规范（测试标准、安全要求、Git 约定、代码风格）。如果每次都要在对话中重复说明，既浪费上下文又容易遗漏。

**Rule 解决什么**：把**持久化的工程默认配置**注入到每一次对话中。Rule 不需要触发——它始终在场，像引力一样约束模型的行为。无论用户是否提及，模型都必须遵守。

**在 Harness 中的角色**：Rule 是 Harness 的**规范层**，相当于代理的"行为宪法"。它解决的是"模型应该怎样做"的问题——不是教模型怎么做（那是 Skill），而是规定模型必须怎么做。

**没有保证的风险**：

| 风险 | Rule 如何消除 |
|---|---|
| 模型用 npm 而项目用 bun | CLAUDE.md 声明包管理器，每次自动遵守 |
| 模型不知道项目禁止直接操作数据库 | Rule 写入安全规范，模型无法忽略 |
| 不同开发者对模型说不同的话，行为不一致 | Rule 是单一事实来源，所有人共享同一份规范 |

**实现要点**：

- **核心类型**：`MemoryFileInfo`（`src/utils/claudemd.ts`）
- **文件发现（从低到高优先级）**：Managed(/etc/claude-code/) → User(~/.claude/) → Project(root→CWD) → Local(CLADE.local.md)
- **目录结构**：

```
project/
├── CLAUDE.md              ← 项目共享（可提交）
├── CLAUDE.local.md        ← 项目私有（gitignored）
├── .claude/
│   ├── CLAUDE.md
│   └── rules/
│       ├── typescript.md  ← 无条件规则（始终加载）
│       └── api.md         ← 条件规则（有 paths frontmatter）
~/.claude/
├── CLAUDE.md              ← 用户全局
└── rules/                 ← 用户全局规则
```

- **注入方式**：
  - 预加载：会话启动时全部 Rule 作为 `<system-reminder>` 注入，模型无法绕过
  - 懒加载：模型操作文件时 `getNestedMemoryAttachmentsForFile()` → 嵌套目录遍历 + 条件规则匹配 → 作为 Attachment 注入
- **条件规则**：frontmatter 中的 `paths` 字段指定 glob 模式，仅在模型操作匹配路径的文件时懒加载注入
- **@include 机制**：支持 `@./path`、`@~/path`、`@/path` 引用外部文件，最大嵌套 5 层，循环引用检测
- **模型能否绕过**：能（模型可能忽略 Rule）
- **排除机制**：`claudeMdExcludes` 设置项允许排除特定路径（Managed 不可排除）

> 关键文件：`src/utils/claudemd.ts`、`src/context.ts`、`src/utils/attachments.ts`

## Hook — 保证安全性

**问题**：Rule 是"建议"——模型可能忽略或误解。在关键路径上（如安全检查、权限控制、质量门控），仅靠 prompt 约束是不够的。你需要**程序化的、不可绕过的**强制执行。

**Hook 解决什么**：在 Harness 的运行时管道中插入**可编程的拦截点**。Hook 不是给模型看的指令，而是 Harness 框架自身执行的代码。模型无法跳过 Hook，因为 Hook 在工具调用前后、会话启停时由框架自动触发。

**在 Harness 中的角色**：Hook 是 Harness 的**执行层**，相当于代理的"免疫系统"。Rule 说"应该这样做"，Hook 确保"必须这样做"。这是从 prompt engineering 到 software engineering 的关键跨越。

**没有保证的风险**：

| 风险 | Hook 如何消除 |
|---|---|
| 模型执行 `rm -rf` 或 `git push --force` | PreToolUse Hook 拦截危险命令，exit code 2 阻止执行 |
| 模型绕过安全审查直接部署 | PreToolUse Hook 强制执行安全检查脚本 |
| 模型在未信任的仓库中执行恶意 Hook | 工作区信任检查，未信任则跳过所有 Hook |
| 模型向外部服务泄露敏感数据 | HTTP Hook SSRF 防护 + 环境变量白名单 |
| 模型声称完成但实际未通过测试 | Stop Hook 在代理结束前强制运行验证，可阻止结束 |

**Rule vs Hook 的本质区别**：

| | Rule | Hook |
|---|---|---|
| 执行者 | 模型（自主遵守） | 框架（强制执行） |
| 可绕过 | 是（模型可能忽略） | 否（框架拦截） |
| 代价 | 低（纯文本） | 高（进程/LLM调用） |
| 适用场景 | 风格、偏好、约定 | 安全、合规、质量门控 |

**实现要点**：

- **核心类型**：`HookCommand`（`src/schemas/hooks.ts`），4种持久化类型：

| 类型 | 执行方式 |
|---|---|
| `command` | spawn shell 进程 |
| `prompt` | 调用 LLM（默认 Haiku），返回 `{ok, reason}` |
| `agent` | 多轮 Agent 验证（最多 50 轮） |
| `http` | HTTP POST（SSRF 防护 + URL 白名单） |

- **25种事件类型**：PreToolUse、PostToolUse、Stop、UserPromptSubmit、SessionStart、SubagentStart 等
- **配置结构**：

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [{ "type": "command", "command": "check.sh" }] }
    ],
    "Stop": [
      { "hooks": [{ "type": "agent", "prompt": "Verify tests passed" }] }
    ]
  }
}
```

- **配置来源层级**：policySettings > userSettings > projectSettings > localSettings > SDK注册 > sessionHooks
- **匹配器机制**：`matcher` 字段（精确匹配/管道分隔/正则）+ `if` 字段（权限规则语法，如 `"Bash(git *)"`）
- **执行流程**：`executeHooks()` → `getMatchingHooks()`（匹配+过滤+去重）→ 并行执行 → 聚合结果（权限决策 deny>ask>allow / 阻塞错误 / 输入修改）
- **模型能否绕过**：**不能**（框架拦截）
- **安全机制**：工作区信任检查、SSRF 防护、CRLF 注入防护、环境变量白名单、退出码语义（0=成功，2=阻塞）

> 关键文件：`src/utils/hooks.ts`、`src/schemas/hooks.ts`、`src/utils/hooks/hooksConfigSnapshot.ts`

## Memory — 保证连续性

**问题**：模型每次会话都是白纸一张。上次对话中达成的决策、发现的坑、用户的偏好，下次全忘了。用户不得不每次重复说明，代理也无法积累项目经验。

**Memory 解决什么**：在会话之间建立**持久化的知识通道**。Memory 不是 Rule（规定应该怎么做），而是记录**已经做了什么决定、发现了什么、偏好什么**。新会话不需要从零开始，而是站在历史决策的基础上继续。

**在 Harness 中的角色**：Memory 是 Harness 的**状态层**，相当于代理的"长期记忆"。Skill 解决"怎么做"，Rule 解决"必须怎么做"，Memory 解决"上次怎么做的"。

**没有保证的风险**：

| 风险 | Memory 如何消除 |
|---|---|
| 每次新会话用户重复解释项目架构 | project 类型记忆自动加载，代理直接理解 |
| 上次发现的坑下次又踩 | feedback 类型记忆记录纠正，避免重犯 |
| 团队成员各自对代理说不同的话 | Team Memory 共享团队决策，所有人同一认知 |
| 过时的记忆误导当前决策 | 新鲜度标注（>1天附警告），模型被指导验证后使用 |

**Rule vs Memory 的本质区别**：

| | Rule | Memory |
|---|---|---|
| 性质 | 规范（应该） | 事实（已经） |
| 变化频率 | 低（规范稳定） | 高（随项目演进） |
| 来源 | 人工编写 | 代理自动提取 + 人工编辑 |
| 作用 | 约束行为 | 提供上下文 |

**实现要点**：

- **核心类型**：`MemoryType` = user/feedback/project/reference（`src/memdir/memoryTypes.ts`）

| 类型 | 作用域 | 用途 |
|---|---|---|
| `user` | 始终私有 | 用户角色、偏好 |
| `feedback` | 默认私有 | 用户对工作方式的纠正 |
| `project` | 偏向团队 | 项目目标、决策 |
| `reference` | 通常团队 | 外部系统指针 |

- **存储路径**：`~/.claude/projects/<sanitized-git-root>/memory/`
- **目录结构**：

```
memory/
├── MEMORY.md           ← 入口索引（≤200行/25KB）
├── user_role.md        ← 用户记忆
├── project_goals.md    ← 项目记忆
└── team/               ← Team Memory（需 feature flag）
    ├── MEMORY.md
    └── coding_std.md
```

- **写入方式**：
  - 主代理直接写：Write 工具写入文件 + Edit 更新 MEMORY.md 索引
  - 后台提取代理：每轮对话结束后，若主代理未写入，自动 fork 子代理提取记忆（限制：只能读写 memory 目录）
- **检索机制**：`findRelevantMemories()` → `scanMemoryFiles()` 扫描 → Sonnet 模型做相关性选择（最多 5 个）
- **Team Memory 同步**：Pull（服务端覆盖本地）+ Push（仅上传 delta，带 ETag 乐观锁）+ gitleaks 凭据扫描
- **新鲜度**：>1 天的记忆自动附加过期警告，系统提示指导"推荐前验证"
- **模型能否绕过**：能（模型可能不读取 Memory）

> 关键文件：`src/memdir/memdir.ts`、`src/memdir/findRelevantMemories.ts`、`src/services/extractMemories/extractMemories.ts`、`src/services/teamMemorySync/index.ts`

## Eval — 保证正确性

**问题**：代理说"我做完了"，但真的做完了吗？代码能跑吗？测试通过吗？边界情况处理了吗？没有独立验证，代理的"完成"声明不可信——模型有自我合理化的倾向，倾向于报喜不报忧。

**Eval 解决什么**：引入**独立的对抗性验证**，让"完成"不是一个声明，而是一个**可证明的结论**。验证代理与实现代理隔离，只读、只测、只破不立。只有通过独立验证的工作才算完成。

**在 Harness 中的角色**：Eval 是 Harness 的**验证层**，相当于代理的"质检员"。前四个源语让代理能做事、守规矩、有记忆；Eval 确保代理做的事是真正正确的。没有 Eval，整个系统是开环的；有了 Eval，系统变成闭环。

**没有保证的风险**：

| 风险 | Eval 如何消除 |
|---|---|
| 模型说"修好了"但实际没修 | 验证代理独立复现 bug → 确认修复 → 回归测试 |
| 代码能跑但边界情况未处理 | 对抗性验证：专门找边界值、并发、幂等性问题 |
| 模型只测了 happy path | "Reading code is not verification"——必须有实际执行的命令和输出 |
| 模型自我合理化，对明显问题视而不见 | 验证代理与实现代理隔离，只读不写，职责是"破"不是"立" |

**Eval 到底是什么**：Eval **就是一个 Agent**——一个内置的、只读的、对抗性的子代理。它没有自己的存储格式、没有自己的配置文件、没有独立的数据结构。整个 Eval 的实现链条就三步：

```
1. 主代理做了非平凡修改（3+ 文件编辑）
2. 主代理调用 AgentTool(subagent_type="verification") 启动验证代理
3. 验证代理独立运行，输出 VERDICT: PASS/FAIL/PARTIAL
```

没有独立的 Eval 框架、没有独立的测试引擎、没有独立的检查清单——**"验证"这件事完全交给另一个 LLM 代理去做**。它用 Bash 跑命令、用 Read 读代码、用 curl 测接口、用 Playwright 测 UI，然后自己判断通过还是失败。具体跑什么命令、测什么边界、怎么构造对抗性输入——全部由验证代理这个 LLM 自己决定。

**实现要点**：

- **核心实体**：`VERIFICATION_AGENT`（定义在 `src/tools/AgentTool/built-in/verificationAgent.ts`），复用 AgentTool 的全部基础设施，唯一独特的是 130 行的验证 prompt 和 `disallowedTools` 限制
- **触发机制一：System Prompt 契约**（写在 `src/constants/prompts.ts:394`，注入到每次对话的 system prompt 中）：

> The contract: when non-trivial implementation happens on your turn, independent adversarial verification must happen before you report completion — regardless of who did the implementing. Non-trivial means: 3+ file edits, backend/API changes, or infrastructure changes. Spawn the Agent tool with subagent_type="verification".

这不是代码逻辑——是写给模型的指令。模型读到这段话后，自己判断"我做了非平凡修改"，然后主动调用 AgentTool 启动验证代理。

- **触发机制二：结构性 Nudge**（代码逻辑，写在 `src/tools/TodoWriteTool/TodoWriteTool.ts:76-86`）：

```typescript
// 当主线程代理关闭 3+ 个 todo 且没有包含 "verif" 关键词的步骤时
if (
  feature('VERIFICATION_AGENT') &&
  getFeatureValue_CACHED_MAY_BE_STALE('tengu_hive_evidence', false) &&
  !context.agentId &&           // 仅主线程
  allDone &&                     // 全部完成
  todos.length >= 3 &&          // 3+ 任务
  !todos.some(t => /verif/i.test(t.content))  // 无验证步骤
) {
  verificationNudgeNeeded = true;  // 工具返回结果中附加提醒
}
```

这是程序化的兜底。如果模型忘了调验证代理（违反了 prompt 契约），TodoWriteTool 在返回结果时自动追加提醒文本。TaskUpdateTool（V2 任务系统）有完全相同的逻辑。

- **触发机制三**：`/verify` 技能（Ant 内部用户直接调用）
- **验证代理安全隔离**：

```typescript
disallowedTools: [AGENT, FILE_EDIT, FILE_WRITE, NOTEBOOK_EDIT]  // 只读
background: true       // 默认后台运行
criticalSystemReminder: "You CANNOT edit, write, or create files"
```

- **对抗性验证哲学**：
  - "Your job is not to confirm — it's to try to break it"
  - 列出常见逃避借口并要求做相反的事
  - PASS 报告必须包含至少一个对抗性探测
  - "Reading code is not verification"——没有 Command run 块的 PASS 会被拒绝
- **Verdict 格式**：`VERDICT: PASS / FAIL / PARTIAL`，FAIL 必须含精确错误输出和复现步骤
- **验证循环（prompt-driven）**：FAIL → 修复 → 再验证 → PASS → spot-check 2-3 个命令
- **验证策略按变更类型适配**：Frontend(浏览器自动化)、Backend(curl+错误处理)、CLI(边界输入)、Bug fix(复现→修复→回归)、DB migration(可逆性)
- **自定义验证器**：`/init-verifiers` 创建 `verifier-playwright`、`verifier-cli`、`verifier-api` 技能，验证代理通过文件夹名含 "verifier" 自动发现
- **Feature Flag 双重门控**：`VERIFICATION_AGENT`（编译时）+ `tengu_hive_evidence`（GrowthBook 运行时）
- **模型能否绕过**：不能（系统契约强制 + Nudge 提醒）

> 关键文件：`src/tools/AgentTool/built-in/verificationAgent.ts`、`src/constants/prompts.ts`、`src/tools/TodoWriteTool/TodoWriteTool.ts`

## 五源语实现方式对比

Eval 与其他四源语有本质区别——其他四个是**基础设施**（可扩展、可配置的框架能力），Eval 是**策略**（一段 prompt + 一个内置代理 + 两个触发点）：

| | Skill | Rule | Hook | Memory | Eval |
|---|---|---|---|---|---|
| **实现方式** | 文件格式（SKILL.md）+ 加载器 + SkillTool | 文件格式（CLAUDE.md）+ 加载器 + prompt 注入 | 配置格式（settings.json）+ 执行引擎（shell/LLM/HTTP） | 文件格式（memory/*.md）+ 检索器 + 后台提取代理 | **就是一个 Agent**（`subagent_type="verification"`） |
| **有自己的存储格式吗？** | 有（SKILL.md） | 有（CLAUDE.md / rules/*.md） | 有（settings.json hooks 字段） | 有（memory/*.md） | **没有** |
| **有自己的配置文件吗？** | 有 | 有 | 有 | 有 | **没有** |
| **有独立的数据结构吗？** | 有（PromptCommand） | 有（MemoryFileInfo） | 有（HookCommand） | 有（MemoryType） | **没有**——复用 AgentTool 的 BuiltInAgentDefinition |
| **用户能自定义吗？** | 能（写 SKILL.md） | 能（写 CLAUDE.md） | 能（配 settings.json） | 能（写 memory 文件） | **基本不能**（只有 `/init-verifiers` 创建验证器技能） |
| **本质** | 基础设施 | 基础设施 | 基础设施 | 基础设施 | **最佳实践封装**（prompt + 内置代理 + 触发点） |

## 实现细节对照表

| 维度 | Skill | Rule | Hook | Memory | Eval |
|---|---|---|---|---|---|
| **核心类型** | `PromptCommand` | `MemoryFileInfo` | `HookCommand` | `MemoryType` | `VERIFICATION_AGENT` |
| **类型定义文件** | `src/types/command.ts` | `src/utils/claudemd.ts` | `src/schemas/hooks.ts` | `src/memdir/memoryTypes.ts` | `src/tools/AgentTool/built-in/verificationAgent.ts` |
| **存储位置** | `.claude/skills/<name>/SKILL.md` | `CLAUDE.md` + `.claude/rules/*.md` | `settings.json` 的 `hooks` 字段 | `~/.claude/projects/<repo>/memory/` | 编译进二进制 + `.claude/skills/verifier-*/` |
| **加载时机** | 会话启动 + 文件操作时动态发现 | 会话启动预加载 + 文件操作时懒加载条件规则 | 会话启动捕获快照 + 运行时注册 | 会话启动注入 system prompt + 每轮后台提取 | 非平凡实现后由系统提示词契约触发 |
| **触发方式** | 模型 SkillTool 主动调用 / 用户 `/name` | 无需触发，始终在场 | 框架自动触发（25种事件） | 主代理直接写 / 后台提取代理自动提取 | 主代理调用验证代理 / TodoWrite Nudge 提醒 |
| **模型能否绕过** | 能（模型可以选择不调用） | 能（模型可能忽略） | **不能**（框架拦截） | 能（模型可能不读取） | 不能（系统契约强制 + Nudge 提醒） |
| **执行代价** | 低（prompt 注入） | 低（文本注入） | 高（进程/LLM/HTTP 调用） | 中（后台子代理提取） | 高（独立代理多轮验证） |
| **关键实现机制** | 参数替换 + shell 注入 + inline/fork 执行 | @include 引用 + 条件规则 paths glob + 优先级合并 | matcher 匹配 + if 条件过滤 + 4种执行类型 | Sonnet 相关性检索 + Team Memory ETag 同步 + gitleaks 扫描 | 对抗性验证 + disallowedTools 隔离 + Verdict 格式 |
| **优先级/合并逻辑** | bundled → plugin → skillDir → workflow，先到先得 | Managed → User → Project(root→CWD) → Local，后加载优先级高 | policy > user > project > local > SDK > session | 四类型分类法，检索时 Sonnet 选最多5条 | 验证代理与实现代理完全隔离，只读不写 |
| **安全机制** | fork 模式隔离执行，MCP skill 禁止 shell 注入 | claudeMdExcludes 排除，Managed 不可排除 | 工作区信任检查、SSRF 防护、CRLF 注入防护、环境变量白名单 | Team Memory 凭据扫描、路径遍历防护、ETag 乐观锁 | disallowedTools 禁止写操作、criticalSystemReminder 每轮提醒 |
| **与上下文窗口的关系** | 技能清单 ≤ 上下文窗口 1%，增量发送 | 无条件规则预加载，条件规则按需懒加载 | 不占上下文（框架执行） | MEMORY.md ≤ 200行/25KB，检索最多5条 | 验证代理在独立子代理中运行，不占主上下文 |
| **典型场景** | code review、写单测、部署、API 测试 | 包管理器选择、安全规范、Git 约定、代码风格 | 阻止 force push、安全检查、自动授权、质量门控 | 项目架构记忆、用户偏好、团队决策、踩坑记录 | 3+ 文件编辑后验证、bug 修复验证、部署前验证 |
