---
layout: post
title: "Claude Code 内置 Agent 对比：工具、权限与适用场景"
description: "梳理 Claude Code 6 个内置 Agent 的核心属性、工具权限、模型和使用场景，并解释多 Agent 协作、Agent 核心概念，以及如何选择合适的 Agent。"
category: "AI"
tags: ["AI", "Agent", "Claude Code", "开发工具"]
---

* 目录
{:toc}

---

# Claude Code 内置 Agent 对比表

## 1. 概述

Claude Code 提供了 6 个功能各异的内置 Agent，每个 Agent 都是专门为处理特定类型任务而设计的智能助手。它们拥有不同的工具配置、权限模式和行为特征，能够高效地帮助用户完成各种开发工作。

## 2. 所有 Agent 共有的核心属性

| 属性名            | 类型     | 描述                            |
| ----------------- | -------- | ------------------------------- |
| `agentType`       | string   | Agent 类型标识符                |
| `whenToUse`       | string   | Agent 适用场景描述              |
| `getSystemPrompt` | function | 返回该 Agent 的系统提示         |
| `source`          | string   | Agent 来源（固定为 'built-in'） |
| `baseDir`         | string   | 基础目录（固定为 'built-in'）   |

## 3. 各 Agent 详细对比

| 属性               | GENERAL_PURPOSE_AGENT    | CLAUDE_CODE_GUIDE_AGENT                           | EXPLORE_AGENT                                                              | PLAN_AGENT                                                                 | VERIFICATION_AGENT                                                         | STATUSLINE_SETUP_AGENT |
| ------------------ | ------------------------ | ------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ---------------------- |
| **agentType**      | general-purpose          | claude-code-guide                                 | Explore                                                                    | Plan                                                                       | verification                                                               | statusline-setup       |
| **工具配置**       | `['*']` (允许所有工具)   | Bash、FileRead、WebFetch、WebSearch（含搜索工具） | 禁止编辑工具                                                               | 禁止编辑工具                                                               | 禁止编辑工具                                                               | 未指定                 |
| **禁止工具**       | -                        | -                                                 | AgentTool、ExitPlanModeTool、FileEditTool、FileWriteTool、NotebookEditTool | AgentTool、ExitPlanModeTool、FileEditTool、FileWriteTool、NotebookEditTool | AgentTool、ExitPlanModeTool、FileEditTool、FileWriteTool、NotebookEditTool | -                      |
| **颜色**           | -                        | -                                                 | -                                                                          | -                                                                          | red                                                                        | -                      |
| **模型**           | 未指定 (使用默认)        | haiku                                             | 继承 (Ant) / haiku (外部)                                                  | inherit                                                                    | inherit                                                                    | 未指定                 |
| **权限模式**       | 未指定                   | dontAsk                                           | 未指定                                                                     | 未指定                                                                     | 未指定                                                                     | 未指定                 |
| **记忆功能**       | -                        | -                                                 | -                                                                          | -                                                                          | -                                                                          | -                      |
| **隔离模式**       | -                        | -                                                 | -                                                                          | -                                                                          | -                                                                          | -                      |
| **后台任务**       | -                        | -                                                 | -                                                                          | -                                                                          | true                                                                       | -                      |
| **省略 CLAUDE.md** | -                        | -                                                 | true                                                                       | true                                                                       | -                                                                          | -                      |
| **关键系统提醒**   | -                        | -                                                 | -                                                                          | -                                                                          | 有 (实验功能)                                                              | -                      |
| **功能定位**       | 通用任务处理             | Claude Code 使用指南                              | 快速代码搜索分析                                                           | 架构设计规划                                                               | 实现验证检查                                                               | 状态栏设置             |
| **使用场景**       | 复杂多步骤任务、研究搜索 | 回答 Claude Code 相关问题                         | 查找文件、搜索代码模式                                                     | 规划任务实现策略                                                           | 验证任务完成情况                                                           | 配置状态栏             |

## 4. 详细工具配置说明

表格中的"工具配置"列提供了简化的描述，以下是详细说明：

### GENERAL_PURPOSE_AGENT
- **工具配置**: 允许所有工具
- **具体包括**: 所有可用的 Claude Code 工具，无限制

### CLAUDE_CODE_GUIDE_AGENT
- **工具配置**: 仅允许特定工具
- **允许的工具**: Bash、FileRead、WebFetch、WebSearch（根据环境动态选择搜索工具）
- **工具选择逻辑**: 
  - 有嵌入式搜索工具时：使用 Bash 工具和 `find`/`grep` 命令
  - 无嵌入式搜索工具时：使用 Glob 和 Grep 工具

### EXPLORE_AGENT
- **工具配置**: 禁止编辑工具（只读模式）
- **允许的工具**: 除编辑工具外的所有工具（如搜索、读取、Bash 等）
- **禁止的工具**: AgentTool、ExitPlanModeTool、FileEditTool、FileWriteTool、NotebookEditTool

### PLAN_AGENT
- **工具配置**: 禁止编辑工具（只读模式）
- **允许的工具**: 除编辑工具外的所有工具（如搜索、读取、Bash 等）
- **禁止的工具**: AgentTool、ExitPlanModeTool、FileEditTool、FileWriteTool、NotebookEditTool

### VERIFICATION_AGENT
- **工具配置**: 禁止修改项目（验证模式）
- **允许的工具**: 除编辑工具外的所有工具（如搜索、读取、Bash 等）
- **禁止的工具**: AgentTool、ExitPlanModeTool、FileEditTool、FileWriteTool、NotebookEditTool

### STATUSLINE_SETUP_AGENT
- **工具配置**: 未明确指定
- **说明**: 该 Agent 专门用于配置状态栏，工具使用可能根据具体任务动态调整

## 5. 权限模式说明

- **未指定**: 使用默认权限模式（通常为 'acceptEdits'）
- **dontAsk**: 不询问用户权限，直接执行
- **其他模式**: 如 'plan'（需要计划模式批准）、'auto'（自动判断）

## 6. 使用建议

| 任务类型     | 推荐 Agent        |
| ------------ | ----------------- |
| 快速搜索代码 | Explore           |
| 规划架构设计 | Plan              |
| 代码问题解答 | Claude Code Guide |
| 验证实现     | Verification      |
| 通用任务处理 | General Purpose   |
| 配置状态栏   | Statusline Setup  |

## 7. 何时会使用多个Agent

在Claude Code中，会在以下情况下使用多个Agent协作完成任务：

### 1. 复杂任务分解
将大型任务分解为多个子任务，每个子任务由不同的Agent处理。例如：
- 需求分析 → 使用Explore Agent搜索相关代码
- 架构设计 → 使用Plan Agent制定实现计划
- 代码实现 → 使用General Purpose Agent编写代码
- 验证测试 → 使用Verification Agent验证实现

### 2. 专业任务处理
使用特定类型的Agent处理专业任务：
- 代码搜索分析 → Explore Agent
- 架构设计规划 → Plan Agent
- 代码问题解答 → Claude Code Guide Agent
- 实现验证检查 → Verification Agent

### 3. 异步任务处理
长时间运行的任务会在后台创建新的Agent：
- 持续集成测试
- 代码扫描分析
- 大型文件处理

### 4. 多Agent协作
通过Teams功能创建多个Agent协作完成任务：
- 团队成员间的任务分配
- 并行处理不同任务
- 任务结果的合并与汇总

## 8. Agent 核心概念

### 8.1 什么是 Agent？

在Claude Code中，**Agent是具有特定行为准则、工具权限和性能特征的智能助手**，专门用于处理特定类型任务。它是一个独立的工作实体，可以：

1. **自主执行任务**：根据用户输入和系统提示，决定使用哪些工具完成任务
2. **具有特定专长**：每个Agent都有明确的功能定位和行为准则
3. **权限受限**：只能使用配置允许的工具，防止不必要的风险
4. **可配置**：支持自定义模型、努力程度、权限模式等属性

从代码定义来看，Agent具有以下核心属性（`BaseAgentDefinition`）：

```typescript
export type BaseAgentDefinition = {
  agentType: string;                // Agent类型标识符
  whenToUse: string;                // 使用场景描述
  tools?: string[];                 // 允许使用的工具列表
  disallowedTools?: string[];       // 禁止使用的工具列表
  getSystemPrompt: () => string;    // 返回Agent的行为准则
  model?: string;                   // 使用的模型
  permissionMode?: PermissionMode;  // 权限模式
  memory?: AgentMemoryScope;        // 持久化内存范围
  // ... 其他属性
}
```

### 8.2 Claude Code 是 AI Agent 吗？

简单来说，**Claude Code不是单一的AI Agent，而是一个包含多个AI Agent的系统**。

- **Claude Code**：是一个完整的CLI工具和交互式开发环境，提供运行Agent的基础设施
- **Agent是系统组件**：Claude Code包含多个内置Agent（如General Purpose、Explore、Plan等），每个Agent都是专门设计用于特定任务的智能助手

### 8.3 AI Agent 定义

根据行业标准定义，**AI Agent是一个能够自主感知环境、做出决策并执行行动以实现特定目标的人工智能系统**。AI Agent具有以下核心特征：

1. **自主性（Autonomy）**：能够在没有持续人类干预的情况下执行任务
2. **感知能力（Perception）**：能够获取和理解环境信息
3. **决策能力（Reasoning）**：能够基于信息做出判断和决策
4. **行动能力（Action）**：能够执行操作以改变环境或完成任务
5. **目标导向（Goal-oriented）**：有明确的目标或任务要完成

Claude Code中的每个内置Agent都符合AI Agent的定义，它们可以独立执行特定任务，感知代码库信息，做出决策，并执行相应的操作来完成任务。
