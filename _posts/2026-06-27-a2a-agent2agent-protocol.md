---
layout: post
title: "A2A 协议：开启 AI 智能体互联互通新时代"
description: "Agent2Agent (A2A) 协议是由 Google 联合 50+ 合作伙伴共同推出的开放标准协议，旨在为 AI 智能体之间提供安全、标准化的通信与协作框架，实现不同框架、不同平台构建的智能体之间的互联互通。"
category: "AI"
tags: ["AI", "A2A", "智能体", "多智能体", "协议"]
---
{% include JB/setup %}

## 什么是 A2A，它解决了什么问题

**Agent2Agent (A2A) 协议**是由 Google 联合 50+ 合作伙伴共同推出的**开放标准协议**，旨在为 AI 智能体之间提供安全、标准化的通信与协作框架，实现不同框架、不同平台构建的智能体之间的互联互通。

### 背景与问题

随着 AI 技术的快速发展，企业和开发者构建了大量基于不同框架（如 LangGraph、CrewAI、ADK 等）的智能体，但这些智能体普遍存在以下问题：

1. **孤岛效应**：不同框架开发的智能体无法直接通信，形成技术孤岛
2. **协作困难**：复杂任务需要多个专业智能体分工协作，但缺乏标准协作机制
3. **发现困难**：没有统一的能力描述和服务发现机制
4. **长任务支持不足**：企业场景中常见的长时间运行任务缺乏标准化生命周期管理
5. **安全考量缺失**：跨系统智能体协作缺乏企业级的身份认证和授权机制

A2A 协议的出现在于解决这些痛点，它定义了一套**开放、简单、健壮且具备企业级特性**的标准，作为 AI Agent 之间进行通信与协作的"通用语言"。

## 核心特性

根据官方文档，A2A 协议具备以下核心特性：

### 1. **智能体发现机制**
通过 **AgentCard** 机制自动发现和识别智能体能力，支持自动化服务发现与协作。每个智能体通过标准的 JSON 格式描述自身名称、功能、能力和接入点信息，其他智能体可以自动发现并调用。

### 2. **标准化接口**
采用 JSON-RPC over HTTP/SSE 标准化接口，同时支持同步、异步和流式通信模式，满足不同场景需求。

### 3. **完整的任务生命周期管理**
支持从任务创建、执行到结果返回的完整生命周期管理，特别适合长时间运行任务，提供实时状态更新和结果同步。

### 4. **企业级安全能力**
- 支持强大的身份认证（如 W3C DID 标准）
- 端到端加密通信
- 企业级授权机制

### 5. **多模态支持**
原生支持多种内容类型，包括文本、表单、文件，以及音视频流处理能力，适应复杂业务场景。

### 6. **开放生态系统**
由社区驱动的开放生态系统，已支持主流开发框架如 LangGraph、CrewAI、Google ADK 等，并提供丰富的工具和示例。

## 主要用途和适用场景

A2A 协议主要用于实现智能体之间的互联互通和协作，典型场景包括：

### 1. **分布式多智能体系统**
在微服务架构中，将不同专业领域的智能体部署为独立服务，通过 A2A 实现跨服务调用和协作。例如：
- 订单处理智能体调用物流查询智能体获取配送信息
- 客户服务智能体调用知识库智能体解答专业问题

### 2. **跨框架智能体协作**
不同团队使用不同框架开发的智能体可以通过 A2A 协议无缝协作：
- 团队 A 使用 LangGraph 开发规划智能体
- 团队 B 使用 CrewAI 开发执行智能体
- 通过 A2A 协议实现规划-执行协作流程

### 3. **企业级业务流程编排**
在企业复杂业务流程中，编排多个专业化智能体：
```
用户请求 → 意图识别智能体 → 领域专业智能体 → 合规检查智能体 → 结果整合 → 返回用户
```
每个环节都可以由独立的智能体通过 A2A 协作完成。

### 4. **混合本地-云端部署**
敏感数据处理在本地智能体完成，计算密集型任务交给云端智能体，通过 A2A 安全通信。

### 5. **智能体市场与生态构建**
第三方开发者可以将自己开发的智能体发布为 A2A 服务，供生态系统中其他开发者调用，形成智能体复用和市场生态。

## 核心接口和概念

### 核心概念

| 概念 | 说明 |
|------|------|
| **AgentCard** | 智能体的能力描述卡片，包含名称、描述、URL、能力声明（是否支持流式）和技能列表 |
| **Task (任务)** | A2A 协作的基本单位，包含完整的生命周期：提交 → 执行中 → 完成/失败 |
| **Artifact (工件)** | 任务产生的结果数据，可以是文本、文件或其他格式，支持增量更新 |
| **Message (消息)** | 智能体之间传递的消息，包含角色（用户/助手等）和内容片段 |
| **Part (片段)** | 消息的内容部分，支持文本、文件、表单等多种类型 |

### 核心工作流程

1. **服务发现**：通过标准路径 `/.well-known/agent-card.json` 获取 AgentCard，了解智能体能力
2. **任务创建**：客户端创建新任务，发送初始消息
3. **任务执行**：服务端智能体执行任务，通过流式更新实时返回状态和部分结果
4. **任务完成**：最终结果以 Artifact 形式返回，任务进入终止状态

### 核心 API 接口（HTTP JSON-RPC）

A2A 定义了以下核心 JSON-RPC 方法：

| 方法 | 功能 |
|------|------|
| `agents/getCard` | 获取智能体卡片信息 |
| `tasks/send` | 发送新消息到任务（创建新任务或继续已有任务） |
| `tasks/cancel` | 取消正在执行的任务 |
| `tasks/get` | 获取任务当前状态 |
| `tasks/subscribe` | 订阅任务状态和结果的流式更新 |

### 传输协议

- **同步请求响应**：HTTP POST + JSON-RPC
- **流式更新**：Server-Sent Events (SSE)
- 支持长时间运行任务的异步通知机制

## Go 语言集成使用示例

tRPC-Agent-Go 框架提供了完整的 A2A 协议实现，包含服务端（A2AServer）和客户端（A2AAgent）两个核心组件。以下是基础集成示例：

### 1. 安装依赖

```go
go get trpc.group/trpc-go/trpc-agent-go
go get trpc.group/trpc-go/trpc-a2a-go
```

### 2. 服务端：将本地 Agent 暴露为 A2A 服务

以下示例展示如何快速将一个 LLM Agent 转换为 A2A 服务：

```go
package main

import (
    "trpc.group/trpc-go/trpc-agent-go/agent/llmagent"
    "trpc.group/trpc-go/trpc-agent-go/model/openai"
    a2aserver "trpc.group/trpc-go/trpc-agent-go/server/a2a"
)

func main() {
    // 1. 创建一个普通的 LLM Agent
    model := openai.New("gpt-4o-mini")
    agent := llmagent.New(
        "MyAgent",
        llmagent.WithModel(model),
        llmagent.WithDescription("一个通用智能助手"),
    )

    // 2. 一键转换为 A2A 服务，开启流式支持
    server, err := a2aserver.New(
        a2aserver.WithHost("localhost:8080"),
        a2aserver.WithAgent(agent, true), // 第二个参数表示开启流式
    )
    if err != nil {
        panic(err)
    }

    // 3. 启动服务，接受 A2A 请求
    server.Start(":8080")
}
```

启动后，你的 Agent 就以 A2A 协议对外提供服务了，服务发现地址为：
```
http://localhost:8080/.well-known/agent-card.json
```

### 3. 在同一个端口暴露多个 A2A Agent

你可以通过 base path 路由在同一个端口暴露多个 Agent：

```go
package main

import (
    "net/http"
    "trpc.group/trpc-go/trpc-agent-go/agent/llmagent"
    "trpc.group/trpc-go/trpc-agent-go/model/openai"
    a2a "trpc.group/trpc-go/trpc-agent-go/server/a2a"
)

func main() {
    // 创建数学计算 Agent
    mathAgent := llmagent.New("MathAgent", ...)
    mathServer, _ := a2a.New(
        a2a.WithHost("http://localhost:8888/agents/math"),
        a2a.WithAgent(mathAgent, false),
    )

    // 创建天气查询 Agent
    weatherAgent := llmagent.New("WeatherAgent", ...)
    weatherServer, _ := a2a.New(
        a2a.WithHost("http://localhost:8888/agents/weather"),
        a2a.WithAgent(weatherAgent, false),
    )

    // 在同一个端口挂载两个 Agent
    mux := http.NewServeMux()
    mux.Handle("/agents/math/", mathServer.Handler())
    mux.Handle("/agents/weather/", weatherServer.Handler())
    
    http.ListenAndServe(":8888", mux)
}
```

每个 Agent 有独立的发现地址：
- `http://localhost:8888/agents/math/.well-known/agent-card.json`
- `http://localhost:8888/agents/weather/.well-known/agent-card.json`

### 4. 客户端：通过 A2AAgent 调用远程服务

A2AAgent 让你像使用本地 Agent 一样调用远程 A2A 服务：

```go
package main

import (
    "context"
    "fmt"
    "trpc.group/trpc-go/trpc-agent-go/agent/a2aagent"
    "trpc.group/trpc-go/trpc-agent-go/model"
    "trpc.group/trpc-go/trpc-agent-go/runner"
    "trpc.group/trpc-go/trpc-agent-go/session/inmemory"
)

func main() {
    // 1. 创建 A2AAgent，自动发现远程 Agent
    a2aAgent, err := a2aagent.New(
        a2aagent.WithAgentCardURL("http://localhost:8888/agents/math"),
    )
    if err != nil {
        panic(err)
    }

    // 2. 像使用本地 Agent 一样使用远程 Agent
    sessionService := inmemory.NewSessionService()
    runner := runner.NewRunner("test", a2aAgent, 
        runner.WithSessionService(sessionService))

    // 3. 发送请求并处理响应
    events, err := runner.Run(
        context.Background(), 
        "user1", 
        "session1", 
        model.NewUserMessage("计算 (3 + 5) * 7 = ?"),
    )
    if err != nil {
        panic(err)
    }

    // 4. 处理流式响应
    for event := range events {
        if event.Response != nil && len(event.Response.Choices) > 0 {
            content := event.Response.Choices[0].Message.Content
            if content == "" {
                content = event.Response.Choices[0].Delta.Content
            }
            if content != "" {
                fmt.Print(content)
            }
        }
    }
    fmt.Println()
}
```

### 5. 自定义消息处理钩子（链路追踪示例）

你可以通过钩子机制在消息处理流程中注入自定义逻辑，例如分布式追踪：

**服务端处理钩子：**
```go
import (
    "context"
    "fmt"
    "trpc.group/trpc-go/trpc-a2a-go/taskmanager"
    a2aserver "trpc.group/trpc-go/trpc-agent-go/server/a2a"
)

type traceHook struct {
    next taskmanager.MessageProcessor
}

func (h *traceHook) ProcessMessage(
    ctx context.Context, 
    msg protocol.Message, 
    options taskmanager.ProcessOptions, 
    handler taskmanager.TaskHandler,
) (*taskmanager.MessageProcessingResult, error) {
    if traceID, ok := msg.Metadata["trace_id"]; ok {
        fmt.Printf("received trace_id: %v\n", traceID)
    }
    return h.next.ProcessMessage(ctx, msg, options, handler)
}

// 在创建服务器时注册钩子
server, _ := a2aserver.New(
    a2aserver.WithHost("localhost:8080"),
    a2aserver.WithAgent(agent, true),
    a2aserver.WithProcessMessageHook(func(next taskmanager.MessageProcessor) taskmanager.MessageProcessor {
        return &traceHook{next: next}
    }),
)
```

**客户端构建钩子：**
```go
import "trpc.group/trpc-go/trpc-agent-go/agent/a2aagent"

a2aAgent, _ := a2aagent.New(
    a2aagent.WithAgentCardURL("http://remote-agent:8888"),
    a2aagent.WithBuildMessageHook(func(next a2aagent.ConvertToA2AMessageFunc) a2aagent.ConvertToA2AMessageFunc {
        return func(isStream bool, agentName string, inv *agent.Invocation) (*protocol.Message, error) {
            msg, err := next(isStream, agentName, inv)
            if err != nil {
                return nil, err
            }
            if msg.Metadata == nil {
                msg.Metadata = make(map[string]any)
            }
            msg.Metadata["trace_id"] = "my-trace-123"
            return msg, nil
        }
    }),
)
```

### 6. 完整示例：服务端 + 客户端综合演示

```go
package main

import (
    "context"
    "fmt"
    "time"
    "trpc.group/trpc-go/trpc-agent-go/agent/a2aagent"
    "trpc.group/trpc-go/trpc-agent-go/agent/llmagent"
    "trpc.group/trpc-go/trpc-agent-go/model"
    "trpc.group/trpc-go/trpc-agent-go/model/openai"
    "trpc.group/trpc-go/trpc-agent-go/runner"
    "trpc.group/trpc-go/trpc-agent-go/server/a2a"
    "trpc.group/trpc-go/trpc-agent-go/session/inmemory"
)

func main() {
    // 1. 创建并启动远程 Agent 服务
    remoteAgent := createJokeAgent()
    startA2AServer(remoteAgent, "localhost:8888")
    time.Sleep(1 * time.Second) // 等待服务启动

    // 2. 创建 A2AAgent 连接到远程服务
    a2aAgent, err := a2aagent.New(
        a2aagent.WithAgentCardURL("http://localhost:8888"),
        a2aagent.WithTransferStateKey("user_context"),
    )
    if err != nil {
        panic(err)
    }

    // 3. 调用远程 Agent
    sessionService := inmemory.NewSessionService()
    runner := runner.NewRunner("remote", a2aAgent, 
        runner.WithSessionService(sessionService))
    
    fmt.Println("=== 远程 A2A Agent 响应 ===")
    events, err := runner.Run(
        context.Background(), 
        "user1", 
        "session1", 
        model.NewUserMessage("请帮我讲一个关于程序员的笑话"),
    )
    if err != nil {
        panic(err)
    }

    for event := range events {
        if event.Response != nil && len(event.Response.Choices) > 0 {
            content := event.Response.Choices[0].Message.Content
            if content == "" {
                content = event.Response.Choices[0].Delta.Content
            }
            if content != "" {
                fmt.Print(content)
            }
        }
    }
    fmt.Println()
}

func createJokeAgent() agent.Agent {
    model := openai.New("gpt-4o-mini")
    return llmagent.New(
        "JokeAgent",
        llmagent.WithModel(model),
        llmagent.WithDescription("我是一个专门讲笑话的智能体"),
        llmagent.WithInstruction("总是用有趣的笑话回答，并且要和程序员相关"),
    )
}

func startA2AServer(agent agent.Agent, host string) {
    server, err := a2a.New(
        a2a.WithHost(host),
        a2a.WithAgent(agent, true), // 启用流式
    )
    if err != nil {
        panic(err)
    }
    go func() {
        server.Start(host)
    }()
}
```

以上完整示例代码可在 [tRPC-Agent-Go 官方文档](https://trpc-group.github.io/trpc-agent-go/zh/a2a/)中获取更多细节。

## 总结和发展前景

### 总结

A2A 协议作为 AI 智能体互联互通的开放标准，解决了当前多智能体开发中的核心痛点：

- ✅ **打破框架壁垒**：不同框架开发的智能体可以无缝协作
- ✅ **标准化协作**：统一的任务生命周期和消息格式
- ✅ **企业就绪**：内置安全性和可扩展性，满足企业需求
- ✅ **生态开放**：谷歌牵头，50+ 合作伙伴参与，社区驱动发展
- ✅ **开发友好**：多语言 SDK 支持，快速集成，降低开发门槛

与 Anthropic 提出的 MCP（Model Context Protocol）互补：MCP 侧重智能体与工具/上下文之间的交互，而 A2A 侧重智能体之间的对等通信协作，二者可以结合使用构建更完整的智能体系统架构。

### 发展前景

1. **多智能体协作成为主流**：随着 AI 应用复杂度提升，单一智能体难以满足所有需求，专业化分工协作成为趋势，A2A 将成为多智能体生态的基础协议。

2. **智能体即服务（Agent-as-a-Service）**：开发者可以将专业化智能体封装为 A2A 服务，在企业内部或公开市场复用，催生新的开发模式和商业模式。

3. **跨组织智能体协作**：不同企业/部门的智能体可以通过 A2A 协议安全地协作，数据不用出域就能完成联合计算和业务流程。

4. **云边端协同**：端侧智能体与云端智能体通过 A2A 分工协作，兼顾隐私和能力。

目前 A2A 协议已进入 v1.0.0-rc 版本，生态快速发展中，Go、Python、JavaScript 生态都已有实现，是构建现代多智能体系统值得关注的开放标准。

---

**参考资料**：
- [A2A 官方网站](https://agent2agent.info/zh-cn/)
- [tRPC-Agent-Go A2A 集成文档](https://trpc-group.github.io/trpc-agent-go/zh/a2a/)
- [A2A 协议规范](https://agent2agent.info/zh-cn/specification/)
- [腾讯云：tRPC智能体生态又升级：发布A2A协议的实现trpc-a2a-go](https://cloud.tencent.com/developer/article/2514993)
