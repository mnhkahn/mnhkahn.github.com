---
layout: post
title: "Claude Code 的会话历史与记忆系统"
description: "深入解析 Claude Code 的两套数据持久化机制——会话历史（Session History）和记忆（Memory），以及 Archivist、Dream 等核心组件如何协同工作。"
category: "AI"
tags: ["AI", "Claude Code", "Memory", "Session", "Architect"]
figure: "https://res.cloudinary.com/cyeam/raw/upload/v1780407465/session-history-memory-architecture.svg"
---

* 目录
{:toc}

---

Claude Code 有两套独立的数据持久化机制：**会话历史（Session History）** 和 **记忆（Memory）**。它们维度不同、用途不同、生命周期不同，但通过"提取"和"整理"两条管线连接在一起。

---

## 一、核心区别

| 维度 | 会话历史 | 记忆 |
|---|---|---|
| **维度** | 会话（Session） | 项目（Project） |
| **存储内容** | 完整对话记录（用户消息、助手回复、工具调用、系统消息） | 提炼后的决策摘要、用户偏好、项目事实 |
| **存储格式** | JSONL（每行一条 Entry） | Markdown（带 frontmatter） |
| **存储路径** | `~/.claude/projects/<cwd-hash>/<sessionId>.jsonl` | `~/.claude/projects/<git-root>/memory/` |
| **生命周期** | 随会话创建，会话结束后不变 | 跨会话累积，定期整理压缩 |
| **用途** | 会话恢复、统计、记忆提取的原始素材 | 新会话的上下文注入，避免从零开始 |
| **能否直接注入上下文** | 否（太大，需压缩后才能用） | 是（MEMORY.md 自动加载 + 按需检索） |

关键点：**会话历史是会话维度的**——每个 JSONL 文件对应一次会话；**记忆是项目维度的**——同一个 git 仓库的所有会话共享同一份 memory 目录。路径中的 `<cwd-hash>` 是工作目录的哈希，而 memory 路径中的 `<git-root>` 是 git 仓库的规范路径（`findCanonicalGitRoot`），同一仓库的所有 worktree 共享一份记忆。

---

## 二、会话历史

### 2.1 存储结构

```
~/.claude/projects/
├── -Users-bytedance-code-myapp/     ← <cwd-hash>
│   ├── a1b2c3d4.jsonl              ← 会话 1
│   ├── e5f6g7h8.jsonl              ← 会话 2
│   └── e5f6g7h8/
│       └── subagents/
│           └── agent-x9y8.jsonl    ← 子代理记录
└── -Users-bytedance-code-other/
    └── ...
```

### 2.2 JSONL Entry 类型

每行是一个 JSON 对象，`type` 字段区分种类：

| type | 说明 |
|---|---|
| `user` | 用户消息 |
| `assistant` | 助手回复（含 tool_use 块和 usage 信息） |
| `system` | 系统消息 |
| `attachment` | 附件消息 |
| `progress` | 进度消息 |
| `mode` | 模式切换 |
| `speculation-accept` | 推测接受（含 timeSavedMs） |
| `file-history-snapshot` | 文件历史快照 |
| `attribution-snapshot` | 归因快照 |

### 2.3 /insights 命令详解

`/insights` 是会话历史最强大的消费方式。它扫描所有会话 JSONL，提取结构化数据，调用 Opus 模型生成洞察，最终输出一个可交互的 HTML 报告。

#### 数据采集

从每个会话的 JSONL 中提取以下维度（`SessionMeta`）：

| 维度 | 说明 |
|---|---|
| 基础信息 | 会话 ID、项目路径、开始时间、持续时长 |
| 消息统计 | 用户消息数、助手消息数 |
| 工具使用 | 各工具调用次数（Bash、Edit、Read 等） |
| 语言分布 | 按文件扩展名统计操作的语言（TS、Go、Python 等） |
| Git 活动 | 提交次数、推送次数 |
| Token 消耗 | input_tokens、output_tokens |
| 代码变更 | 新增行数、删除行数、修改文件数 |
| 交互质量 | 用户中断次数、工具错误次数及分类、用户响应时间 |
| 高级特性 | 是否使用 Task Agent、MCP、Web Search、Web Fetch |
| 多会话并行 | 检测 multi-clauding（多会话重叠使用） |

#### AI 洞察生成

采集完成后，系统并行调用 Opus 模型生成 6-8 个洞察章节：

| 章节 | 内容 |
|---|---|
| **At a Glance** | 一句话总结：什么有效、什么阻碍、快速改进、进阶方向 |
| **What You Work On** | 项目领域分类（4-5 个），每个领域的会话数和描述 |
| **How You Use Claude Code** | 交互风格分析（迭代式 vs 规划式、中断频率等） |
| **Impressive Things You Did** | 3 个高效工作流亮点 |
| **Where Things Go Wrong** | 3 个摩擦类别，每类 2 个具体案例 |
| **Features to Try** | CLAUDE.md 建议添加项 + 推荐尝试的 CC 特性 |
| **On the Horizon** | 3 个进阶自动化机会（并行代理、自主工作流等） |
| **Fun Ending** | 会话中有趣/令人印象深刻的瞬间 |

#### HTML 报告

所有洞察渲染为一个自包含的 HTML 文件，包含概览卡片、四象限快速摘要、按工作领域分类的会话统计、交互风格分析，以及每日活动热力图、语言分布、工具使用分布、每日 Token 消耗、一天中活跃时段等图表。

#### 实现架构

```
/insights 触发
  │
  ├─ 1. 数据采集
  │     扫描 ~/.claude/projects/ 下所有 JSONL
  │     → 提取 SessionMeta（工具计数、语言、Token、代码行变更等）
  │     → 提取 SessionFacets（Opus 分析每个会话的目标/结果/满意度）
  │
  ├─ 2. 数据聚合
  │     aggregateData() → AggregatedData
  │     汇总所有会话的统计 + 检测 multi-clauding
  │
  ├─ 3. 并行洞察生成
  │     6-8 个 Opus 调用并行执行
  │     每个调用传入聚合数据 + 会话摘要列表
  │     → 返回结构化 JSON（project_areas / interaction_style / what_works / ...）
  │
  ├─ 4. HTML 渲染
  │     generateHtmlReport(data, insights)
  │     → 自包含 HTML（内联 CSS + 图表）
  │     → 保存到临时文件
  │
  └─ 5. 输出
        本地用户：file:// URL
        Ant 内部：上传 S3 → 返回 HTTPS URL
```

### 2.4 /cost 命令详解

`/cost` 显示**当前会话**的模型调用详情和费用。`/insights` 是跨会话的宏观分析，但缺少按模型拆分的调用细节；`/cost` 正好补上这个缺口。

#### 输出示例

```
Total cost:            $1.2345
Total duration (API):  5m 30s
Total duration (wall): 12m 15s
Total code changes:    150 lines added, 30 lines removed
Usage by model:
        claude-sonnet-4:  50,000 input, 8,000 output, 30,000 cache read, 5,000 cache write ($0.45)
     claude-opus-4:  20,000 input, 3,000 output, 10,000 cache read, 2,000 cache write ($0.78)
```

#### 数据来源

`/cost` 的数据来自内存中的实时累计（`cost-tracker.ts`），不是从 JSONL 重新解析。每次 API 调用返回后，`addToTotalModelUsage()` 即时更新计数器。因此 `/cost` 只反映当前会话，不含历史会话。

#### 与 /insights 的互补

| | /insights | /cost |
|---|---|---|
| 范围 | 跨会话（全部历史） | 当前会话 |
| 模型拆分 | 仅 input/output tokens 总量 | 按模型拆分 Token + 费用 |
| 代码行变更 | 总新增/删除行数 | 总新增/删除行数 |
| API 耗时 | 无 | 有（API 时间 + 墙钟时间） |
| 输出格式 | HTML 报告 | 终端文本 |

### 2.5 如何查询当前项目的会话

| 命令 | 作用 |
|---|---|
| `/resume` | 列出当前项目（及 git worktree）的历史会话，可选择恢复 |
| `/resume <关键词>` | 按自定义标题或会话 ID 搜索匹配的会话 |

会话列表不需要完整解析 JSONL。系统采用轻量读取策略：先 `stat()` 获取 mtime 按时间排序，然后对候选文件只读头部 64KB + 尾部 64KB（`readSessionLite`），从中提取 `customTitle`、`aiTitle`、`lastPrompt`、`summary`、`gitBranch`、`tag` 等字段。

---

## 三、记忆（Memory）

### 3.1 存储结构

```
~/.claude/projects/<git-root>/memory/
├── MEMORY.md              ← 入口索引（≤200行/25KB，自动加载到 system prompt）
├── user_role.md           ← 用户记忆
├── feedback_testing.md    ← 反馈记忆
├── project_goals.md       ← 项目记忆
├── reference_links.md     ← 引用记忆
├── team/                  ← Team Memory（需 feature flag）
│   ├── MEMORY.md
│   └── coding_std.md
└── logs/                  ← 助手模式日志（KAIROS feature flag）
    └── 2026/
        └── 06/
            └── 2026-06-01.md
```

### 3.2 记忆类型

四种类型，每种有明确的保存时机和使用方式：

| 类型 | 作用域 | 保存什么 | 示例 |
|---|---|---|---|
| `user` | 始终私有 | 用户角色、偏好、知识背景 | "用户是数据科学家，关注可观测性" |
| `feedback` | 默认私有 | 用户对工作方式的纠正和确认 | "不要 mock 数据库，之前出过事故" |
| `project` | 偏向团队 | 项目目标、决策、进度 | "合并冻结从 2026-03-05 开始" |
| `reference` | 通常团队 | 外部系统指针 | "pipeline bug 在 Linear 项目 INGEST 中" |

### 3.3 记忆文件格式

```markdown
---
name: 用户偏好
description: 用户的工作偏好和纠正
type: feedback
---

不要 mock 数据库——上次 mock 通过但生产迁移失败了。

**Why:** 2026 Q1 事故，mock/prod 不一致掩盖了迁移 bug
**How to apply:** 集成测试必须连真实数据库
```

### 3.4 什么不该存为记忆

- 代码模式、架构、文件结构——可以从代码推导
- Git 历史——`git log` 是权威来源
- 调试方案——修复已在代码中，上下文在 commit message
- CLAUDE.md 已有的内容
- 临时任务细节、当前对话上下文

### 3.5 记忆的检索

新会话启动时，记忆通过两条路径注入上下文：

1. **自动加载**：`MEMORY.md` 作为 system prompt 的一部分始终注入（≤200行/25KB）
2. **按需检索**：`findRelevantMemories()` → 扫描所有记忆文件的 frontmatter → Sonnet 模型做相关性选择（最多 5 个）→ 作为 Attachment 注入

---

## 四、记忆是怎么被生成的

记忆有**两条生成路径**，互斥运行：

### 路径一：主代理直接写入

主代理的 system prompt 中包含完整的记忆保存指令。当对话中出现值得记忆的信息时，主代理直接调用 Write/Edit 工具写入 memory 目录。

**特点**：
- 实时性强——信息出现时立即保存
- 无额外 token 消耗——在主对话中完成
- 写入后，后台提取代理会跳过该轮（`hasMemoryWritesSince` 检测）

### 路径二：Archivist 后台提取代理

当主代理**没有**主动写入记忆时，系统在每轮对话结束后自动 fork 一个后台代理（Archivist）来提取记忆。

#### 触发条件

```
每轮对话结束（handleStopHooks）
  → 检查：是否主代理？是
  → 检查：feature flag tengu_passport_quail 是否开启？是
  → 检查：autoMemory 是否启用？是
  → 检查：是否远程模式？否
  → 检查：主代理本轮是否已写入记忆？否
  → 检查：节流门控（tengu_bramble_lintel，默认每 1 轮触发一次）
  → 全部通过 → 启动 Archivist
```

#### 执行流程

Archivist 在后台 2-4 轮完成提取：先 Read 所有可能更新的记忆文件（并行），然后 Write/Edit 写入新记忆并更新 MEMORY.md。它通过游标机制（`lastMemoryMessageUuid`）确保每条消息只被处理一次。

#### 权限隔离

Archivist 的工具权限被严格限制：Read/Grep/Glob 无限制（只读），Bash 仅只读命令，Edit/Write 仅 memory 目录内的路径，其他所有工具拒绝。

#### 并发控制

通过互斥锁（`inProgress` 标志）防止重叠运行；如果提取进行中又有新消息，stash 上下文，当前提取完成后自动运行一次尾随提取。

#### 与主代理的缓存共享

Archivist 通过 `createCacheSafeParams()` 与主代理共享 prompt cache——相同的 system prompt、相同的 tools、相同的消息前缀。这意味着 Archivist 的 API 调用大部分 token 命中缓存，成本远低于全新请求。

---

## 五、记忆的整理：Dream

记忆会随时间积累、过时、重复。`autoDream` 服务定期整理记忆，保持记忆库的精炼和准确。

### 5.1 触发条件

每轮对话结束时检查：距上次整理 ≥ 24 小时，上次整理后有 ≥ 5 个新会话，无其他进程正在整理——全部通过则启动 Dream。

### 5.2 整理流程（4 阶段）

| 阶段 | 动作 |
|---|---|
| Phase 1 — Orient | 浏览 memory 目录，了解当前记忆结构 |
| Phase 2 — Gather | 收集日志信号、与代码现状矛盾的记忆、必要时 grep 会话 JSONL |
| Phase 3 — Consolidate | 合并新信号到现有主题文件，相对日期转绝对日期，删除已被推翻的事实 |
| Phase 4 — Prune & Index | 更新 MEMORY.md（≤200行/25KB），删除过时指针，解决矛盾 |

### 5.3 Dream 的权限

与 Archivist 相同的权限隔离——只读 Bash + 仅 memory 目录内可写。

### 5.4 Dream 与 Archivist 的关系

| | Archivist | Dream |
|---|---|---|
| **做什么** | 从对话中提取新记忆 | 整理、合并、修剪已有记忆 |
| **触发频率** | 每轮对话（节流后） | 每 24h + 5 个新会话 |
| **输入** | 当前对话的消息 | memory 目录 + 会话 JSONL |
| **输出** | 新的记忆文件 | 更新/合并/删除记忆文件 |

---

## 六、全链路：从对话到记忆到检索

```
用户与 Claude 对话
  │
  ├─ 主代理直接写入记忆？──── 是 ──→ 写入 memory/ 目录
  │                                      │
  │                                      ▼
  │                                 推进游标，跳过 Archivist
  │
  └─ 主代理未写入 ──→ Archivist 后台提取
                        │
                        ▼
                   写入 memory/ 目录
                        │
                        ▼
              ┌──── 积累 ────┐
              │               │
              ▼               ▼
         24h + 5会话      用户手动 /dream
              │               │
              ▼               ▼
           autoDream 整理（合并、去重、修剪、更新索引）
              │
              ▼
         精炼的记忆库
              │
              ▼
    ┌── 新会话启动 ──┐
    │                 │
    ▼                 ▼
  MEMORY.md        findRelevantMemories()
  自动加载          Sonnet 选最多 5 条
  (≤200行)         按需注入
    │                 │
    └────┬────────────┘
         ▼
    代理基于历史知识工作
```
