---
layout: post
title: "ACP 协议详解（Agent Client Protocol）"
description: "介绍 Agent Client Protocol 的通信模型、核心接口、会话流程、生态采用及模型选择机制，并对比 ACP、MCP、A2A 与 LSP 的分工。"
image: "https://res.cloudinary.com/cyeam/image/upload/v1792080175/blog-images/2026-10-15-acp-cover.webp"
category: "AI"
tags: ["AI", "ACP", "Agent", "协议"]
---

* 目录
{:toc}

> 整理时间：2026-10-15 ｜ 内容基于官方协议文档与各厂商公开资料，来源见文末「参考资料」。

---

## 1. 什么是 ACP

**ACP（Agent Client Protocol，代理客户端协议）** 是标准化 **代码编辑器/IDE 与 AI 编码代理之间通信** 的开放协议，适用于本地与远程场景。

- **一句话定位**：AI 编码时代的「LSP」——LSP 当年统一了「编辑器 × 语言服务器」，ACP 想统一「编辑器 × 编码代理」。
- **要解决的问题**：
  - 集成开销：每个「编辑器 × 代理」组合都要做定制集成；
  - 兼容性差：代理只能服务少数编辑器；
  - 厂商锁定：选了一个代理，往往被锁死在其官方界面里。
- **效果**：任何 ACP 兼容的编辑器可以驱动任何 ACP 兼容的代理，两边各自创新、任意组合。
- **历史**：由 **Zed Industries** 于 2025 年 8 月首先发布，目前由 **JetBrains 与 Zed 联合开放开发**（2025 年 10 月官宣合作），Apache 2.0 许可。
- **参与生态**：JetBrains Junie、Google Gemini CLI、GitHub Copilot、OpenAI Codex、Cursor、Devin Desktop、Docker Agent、Kimi CLI、Qwen Code 等。

---

## 2. 通信模型与传输

- **消息格式**：JSON-RPC 2.0，只有两类消息：
  - **方法（Methods）**：请求-响应，期待 `result` 或 `error`；
  - **通知（Notifications）**：单向消息，不期待响应。
- **传输**：
  - 本地代理：作为编辑器子进程运行，走 **stdio**（行分隔 JSON）；
  - 远程代理：走 **HTTP / WebSocket**（远程场景支持仍在推进中）。
- **数据表示**：尽量复用 MCP 的 JSON 类型，另加代理编码场景特有类型（如 diff 补丁）；面向用户的可读文本默认用 **Markdown**。
- **约定**：
  - 文件路径必须为绝对路径，行号从 1 开始；
  - 错误遵循 JSON-RPC 2.0（`code` + `message`）；
  - JSON 对象键用 `camelCase`，判别字段值用 `snake_case`；
  - 扩展机制：`_meta` 自定义数据、`_` 前缀自定义方法、初始化时声明自定义能力。

---

## 3. 接口清单（v1，共 18 个方法/通知）

### 3.1 Agent 侧暴露 7 个（由 Client 调用）

| 方法 | 类型 | 作用 |
|---|---|---|
| `initialize` | 方法 · 必选 | 协商协议版本、交换能力集 |
| `authenticate` | 方法 · 可选 | 认证（代理要求时才需要） |
| `session/new` | 方法 · 必选 | 新建会话，返回 sessionId |
| `session/load` | 方法 · 可选 | 恢复历史会话（需声明 loadSession 能力） |
| `logout` | 方法 · 可选 | 结束认证态 |
| `session/set_mode` | 方法 · 可选 | 切换代理运行模式 |
| `session/cancel` | 通知 | 中断进行中的操作（无响应） |

### 3.2 Client 侧暴露 11 个（由 Agent 调用）

| 方法 | 类型 | 作用 |
|---|---|---|
| `session/request_permission` | 方法 · 必选 | 工具调用前请求用户授权 |
| `fs/read_text_file` | 方法 · 可选 | 读文件内容 |
| `fs/write_text_file` | 方法 · 可选 | 写文件内容 |
| `terminal/create` | 方法 · 可选 | 创建终端 |
| `terminal/output` | 方法 · 可选 | 取终端输出与退出码 |
| `terminal/release` | 方法 · 可选 | 释放终端 |
| `terminal/wait_for_exit` | 方法 · 可选 | 等待命令退出 |
| `terminal/kill` | 方法 · 可选 | 强杀命令 |
| `elicitation/create` | 方法 · 可选 | 向用户请求结构化信息（表单） |
| `elicitation/complete` | 通知 | 报告带外 URL 交互完成 |
| `session/update` | 通知 | 流式推送：消息块 / 工具调用 / 计划 / 命令 / 模式变更 |

### 3.3 设计要点

- **必选接口极少**：两端真正必须实现的只有 5 个（Agent 的 `initialize`、`session/new`、`session/prompt`；Client 的 `session/request_permission`；通知 `session/update`），其余全按能力协商后启用。
- **能力由声明驱动**：`initialize` 握手时双方互相声明能力（如 `loadSession`、`fs.readTextFile`、`terminal`、`elicitation`），可选方法只有对方声明后才可调用。
- **权限设计**：代理不能直接动文件/终端，只能调 `session/request_permission` 问用户，授权后走客户端代执行——安全边界始终握在编辑器手里。

---

## 4. 核心流程（3 个阶段）

```
Client（编辑器）                        Agent（编码代理）
────────────────────────────────────────────────────────
阶段 1 · 初始化（连接一次）
  initialize ──────────────────────►   版本/能力协商
  authenticate（如需）─────────────►

阶段 2 · 会话建立（每任务一次）
  session/new（或 session/load）───►
  ◄── 返回 sessionId（可带 MCP 服务器接入）

阶段 3 · Prompt 回合（可多轮循环）
  session/prompt ─────────────────►
  ◄── session/update（通知·流式）消息块/工具调用/计划
  ◄── session/request_permission（要授权）
  用户授权结果 ───────────────────►
  ◄── fs/…、terminal/…（可选·由客户端代执行）
  session/cancel（通知·中断）─────►
  ◄── 回合结束：返回 stop reason（完成/出错/取消）
```

---

## 5. 生态采用现状（截至 2026-10）

### 5.1 编辑器 / IDE（ACP 客户端）

| 编辑器 | 支持方式 |
|---|---|
| Zed | 原生（协议发起者） |
| JetBrains 全家桶（IntelliJ、PyCharm、GoLand、WebStorm…） | 原生（2025.10 官宣联合开发，2025.3.2+） |
| VS Code | 官方 ACP 编辑器列表内，主要通过扩展接入（Marketplace 上 ACP 客户端扩展已有很多） |
| Neovim / Emacs | 社区插件（Avante.nvim、CodeCompanion.nvim 等） |

### 5.2 编码代理（ACP agent）

**原生支持（直接说 ACP）**：Google Gemini CLI（首个外部验证方）、GitHub Copilot CLI（公测）、Goose、Cline、OpenHands、Mistral Vibe、OpenCode、Auggie、Blackbox AI、Raven、Hermes Agent、**Kimi CLI、Qwen Code（中文生态）** 等。

**适配器桥接（产品早于 ACP，靠转换层接入）**：

- **Anthropic Claude Code**（Zed SDK adapter）
- **OpenAI Codex CLI**（adapter）

**尚未接入**：各种只走私有协议、绑定自家 IDE/云的 agent，以及云托管 agent（ACP 的 HTTP/WebSocket 远程规范仍在推进，属空白区）。

### 5.3 分发机制：ACP Agent Registry

- 2026 年 1 月上线，由 **Zed + JetBrains 共建**；
- 代理注册一次，即可在所有 ACP 编辑器中一键安装；
- 已收录：Claude Code、Codex CLI、Copilot CLI、OpenCode、Gemini CLI、Cursor、Factory Droid、Kimi CLI 等。

### 5.4 为什么没有全覆盖

1. **历史原因**：Claude Code、Codex 这类先发产品不愿重写核心 CLI，先做兼容层；
2. **商业原因**：绑定自家 IDE 的厂商没有动力开放；
3. **协议年轻**：v1 稳定才一年多，v2 还是草案，远程场景未定型。

**现状总结**：标准已成、生态过半——头部 agent 基本都能在任意主流编辑器里用上，但「所有 agent 都支持」还远谈不上。

---

## 6. ACP 与「指定模型」

**结论**：支持，但分版本、有边界——客户端只能从代理「广告」出来的模型列表里选，不能指定任意模型。

### 6.1 v1（当前稳定版）：模型选择不在协议层

- 初始化时可声明 `modelSelector` 能力（仅能力协商，无统一方法）；
- legacy 适配器可用 `session/set_model`（需广告 `models` 元数据）；
- 主流做法：走代理自己的 CLI 参数——`claude --model`、`codex --model`、`gemini --model`，或配置文件。

### 6.2 v2（草案）：Session Config Options 标准化

- **`session/new`** 返回 `configOptions[]`，其中 `category: "model"` 的项就是模型选择器（`type: select`，必须带默认值）；
- **客户端** 按代理给定顺序渲染下拉选择器（可分组）；
- **用户选择后** 调 `session/set_config_option`（configId + `type:"id"` + value）；
- **Agent 响应**：返回完整配置状态（模型变了可能连带可用选项变化）；
- **Agent 也可主动切换**（如限流自动降级换模型）→ 发 `config_option_update` 通知。

**配置选项类别**：`mode`（会话模式）、`model`（模型选择器）、`model_config`（模型相关参数，如上下文大小/速度质量权衡）、`thought_level`（思考档位）。类别仅供 UX 语义，客户端须优雅处理缺失/未知类别。

**边界提醒**：

- 模型 value 是不透明的 id（如 `model-1`），真实模型名由代理自己映射，协议不承诺拿到具体模型名；
- 只能从代理广告的列表里选，协议不决定「你能用哪些模型」；
- 切模型可能重置会话上下文（部分实现里切换引擎/模型会重启底层会话）。

---

## 7. 具体案例：Kimi 与 OpenCode 的 ACP 选模型

两家均为**原生 ACP 实现**（非适配器），都支持通过会话配置选项选模型，细节不同：

### 7.1 Kimi Code CLI（`kimi acp`）

- **原生 ACP**：`kimi acp` 子命令切换 ACP 模式，`initialize` 完整返回能力矩阵；
- **会话建立**：`session/new` 返回 `sessionId` + `configOptions[]` + `modes`；
- **切换模型**：`session/set_config_option`（`configId:"model"`）——官方称为「统一的 model / thinking / mode picker 分发」；
- **额外兼容**：保留 `session/set_model` 扩展方法（从 ACP 0.23 早期不稳定面延续），等价于设置 model 配置项；
- **变更通知**：`session/update` 流式推送 `config_option_update`；
- **终端侧**：`--model <别名>`、会话内 `/model`、config.toml 的 `default_model`（可选模型如 kimi-for-coding / k3 / k3-256k，与会员档位挂钩）。

### 7.2 OpenCode（`opencode acp`）

- **原生 ACP**：`opencode acp` 启动 ACP server，被 ACP Registry、Zed、JetBrains、HAPI、Mastra 等收录/接入；
- **模型选择**：走 ACP 配置选项；Mastra 的 ACP 客户端实现提供 `getAvailableModels()` / `setModel()` 运行时管理；
- **模型校验**：v1.1.54 起，无效模型选择会触发 `session error` 事件（不再静默失败）；
- **ACP 完整性**：官方声明通过 ACP 使用与终端效果一致，全部功能可用；
- **终端侧**：`--model <provider>/<model>`、`/models` 命令、opencode.json 的 `model` 字段，还可给不同 subagent 配不同模型。

### 7.3 实操提示

1. 在 Zed / JetBrains 配好 `kimi acp` / `opencode acp` 后，**模型下拉是否出现取决于编辑器版本是否渲染 config options**（v2 特性，v1 客户端可能不渲染，此时用代理默认模型）；
2. 不想依赖编辑器 UI，提前在代理配置里定默认模型：Kimi `config.toml` 的 `default_model`；OpenCode `opencode.json` 的 `model`；
3. 模型列表跟着账号/配置走：Kimi 按会员档位，OpenCode 按配置的 provider。

---

## 8. 与其他协议的分工

| 协议 | 关系 | 作用 |
|---|---|---|
| **LSP** | 编辑器 ⇄ 语言服务器 | 补全、跳转等语言功能（与 AI 无关） |
| **ACP** | 编辑器 ⇄ 编码代理 | 前端的交互与任务层（本次主题） |
| **MCP** | 代理 ⇄ 工具 / 数据源 | 让模型调用外部能力（后端的工具层） |
| **A2A** | 代理 ⇄ 代理 | 跨代理协作，走 HTTP |

**互补关系**：一个编码代理在编辑器里干活时，往往同时用 ACP 和编辑器对话、用 MCP 调外部工具。微软基于 ACP 还做了 AHP（Agent Host Protocol），解决「多个客户端共享同一个代理会话」的协调问题——ACP 本身是点对点的。

---

## 9. 版本现状

- **v1**：当前稳定线，接口见第 3 节；
- **v2（草案，2026-07 发布）**：
  - 重设计 prompt 生命周期；
  - 统一流式与非流式更新；
  - schema 默认前向兼容；
  - 统一 `capabilities` 字段（替换 v1 的 `clientCapabilities` / `agentCapabilities`）；
  - 移除客户端直连文件系统/终端的旧方法（改为「用客户端提供的 MCP 服务器」）；
  - `session/load` 移除（用 `session/resume` + `replayFrom`）。
- 各语言官方 SDK：TypeScript（npm `@agentclientprotocol/sdk`）、Python（PyPI `agent-client-protocol`）、Rust（crates.io）、Kotlin/Java 等。

---

## 参考资料

- Agent Client Protocol 官方站（Introduction / Architecture / Overview / Schema / Updates）：https://agentclientprotocol.com
- ACP v2 Session Config Options：https://agentclientprotocol.com/protocol/v2/session-config-options
- ACP v2 草案说明：https://agentclientprotocol.com/rfds/v2/overview
- Session Config Options RFD：https://agentclientprotocol.com/rfds/session-config-options
- Model Config Option Category RFD：https://agentclientprotocol.com/rfds/model-config-category
- Zed ACP 页面：https://zed.dev/acp ｜ ACP Registry 上线博客：https://zed.dev/blog/acp-registry
- JetBrains ACP 页面（含支持代理列表）：https://www.jetbrains.com/acp/
- JetBrains ACP Registry 博客：https://blog.jetbrains.com/ai/2026/01/acp-agent-registry/
- ACP 与 AHP（微软）：http://microsoft.github.io/agent-host-protocol/guide/ahp-and-acp.html
- ACP vs A2A vs MCP（Docker）：https://docs.docker.com/ai/docker-agent/features/acp/
- Agentic AI 知识库（生态采用）：https://agentic-ai.readthedocs.io/en/latest/Standards/agent-client-protocol/
- Kimi Code CLI：`kimi acp` 子命令文档：https://moonshotai.github.io/kimi-code/zh/reference/kimi-acp.html
- Kimi Code CLI：在 IDE 中使用（ACP 配置）：https://moonshotai.github.io/kimi-code/zh/guides/ides.html
- OpenCode ACP 支持：https://opencode.ai/docs/acp/
- Mastra ACP 连接（模型选择 API）：https://mastra.ai/docs/connections/acp/llms.txt
