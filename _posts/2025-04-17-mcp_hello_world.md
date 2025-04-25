---
layout: post
title: "MCP 模型上下文协议初探，用Go快速构建一个 hello world"
description: "市面上模型非常多，不可能对每个模型都做插件开发。MCP协议能解决多种模型统一接入模型的问题。本文初步介绍了MCP协议、场景、用CLINE搭一个例子。"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1744897150/%E6%88%AA%E5%B1%8F2025-04-17_21.37.49_zysdtr.png"
category: "AI"
tags: ["AI","MCP", "Golang"]
---

* 目录
{:toc}
---

Model Context Protocol (MCP)是一个开源协议，正如 USB-C 为将你的设备连接到各种外围设备和配件提供了一种标准化的方式一样，MCP 也为将人工智能模型连接到不同的数据源和工具提供了一种标准化的方式。大语言模型常常需要与数据和工具集成，而 MCP 能够提供：
1. 一份不断扩充的预构建集成列表，你的大语言模型可直接接入这些集成；
2. 在不同大语言模型提供商和供应商之间切换的灵活性；
3. 在你的基础设施内保障数据安全。

## 整体架构

- MCP Hosts：诸如 Claude 桌面应用程序、集成开发环境（IDE）或希望通过 MCP 访问数据的人工智能工具等程序。本文使用的是VSCode里面的插件Cline。
- MCP Clients: 与服务器保持一对一连接的协议客户端。
- MCP Servers：通过MCP协议提供的轻量级服务。
- Local Data Sources：你的计算机上 MCP 服务器能够安全访问的文件、数据库和服务。
- Remote Services：MCP 服务器可以连接的通过互联网可用的外部系统（例如，通过应用程序编程接口（API））。

## 通信方式

MCP协议支持两种数据通信方式：

![](https://res.cloudinary.com/cyeam/image/upload/v1744897827/640.webp_az9ha1.png)

1. 本地通信
	- 对于本地进程，使用stdio传输方式，就是常见的进程输入输出；
	- 对于同一机器上的通信而言效率较高；
	- 进程管理简单
2. 远程通信
	- 对于需要 HTTP 兼容性的场景，使用服务器发送事件（SSE）技术；
	- 需考虑包括身份验证和授权等方面的安全问题；

## 编码方式

为了灵活支持复杂命令，MCP协议使用JSON-RPC数据格式。

### Request

```
{
  jsonrpc: "2.0";
  id: string | number;
  method: string;
  params?: {
    [key: string]: unknown;
  };
}
```

- 请求必须包含一个字符串或整数类型的标识符（ID）。
- 与基础的 JSON-RPC 不同，该标识符不能为 null。
- 在同一会话中，请求者此前一定不能使用过该请求标识符。

### Response

```
{
  jsonrpc: "2.0";
  id: string | number;
  result?: {
    [key: string]: unknown;
  }
  error?: {
    code: number;
    message: string;
    data?: unknown;
  }
}
```

- 响应必须包含与所对应请求相同的标识符（ID）。
- 响应进一步细分为成功结果或错误两类。必须设置结果或错误其中之一，响应绝不能同时设置两者。
- 结果可以遵循任何 JSON 对象结构，而错误至少必须包含一个错误代码和一条错误消息。
- 错误代码必须是整数。

### Notifications

```
{
  jsonrpc: "2.0";
  method: string;
  params?: {
    [key: string]: unknown;
  };
}
```

通知是从客户端发送到服务器，或者从服务器发送到客户端的一种单向消息。接收方不能发送响应。

## Go语言实现

### Server

代码类似于 HTTP 服务，也需要写Handler。例子里是在本地启动，日志等级为Debug方便观察响应流程。

```go
package main

import (
	"fmt"
	"log"
	"time"

	"github.com/ThinkInAIXYZ/go-mcp/pkg"
	"github.com/ThinkInAIXYZ/go-mcp/protocol"
	"github.com/ThinkInAIXYZ/go-mcp/server"
	"github.com/ThinkInAIXYZ/go-mcp/transport"
)

type TimeRequest struct {
	Timezone string `json:"timezone" description:"timezone" required:"true"` // Use field tag to describe input schema
}

func main() {
	// Create SSE transport server
	transportServer, err := transport.NewSSEServerTransport("127.0.0.1:8080", transport.WithSSEServerTransportOptionLogger(pkg.DebugLogger))
	if err != nil {
		log.Fatalf("Failed to create transport server: %v", err)
	}

	// Initialize MCP server
	mcpServer, err := server.NewServer(transportServer)
	if err != nil {
		log.Fatalf("Failed to create MCP server: %v", err)
	}

	// Register time query tool
	tool, err := protocol.NewTool("current_time", "Get current time for specified timezone", TimeRequest{})
	if err != nil {
		log.Fatalf("Failed to create tool: %v", err)
		return
	}
	mcpServer.RegisterTool(tool, handleTimeRequest)

	// Start server
	if err = mcpServer.Run(); err != nil {
		log.Fatalf("Server failed to start: %v", err)
	}
}

func handleTimeRequest(req *protocol.CallToolRequest) (*protocol.CallToolResult, error) {
	var timeReq TimeRequest
	if err := protocol.VerifyAndUnmarshal(req.RawArguments, &timeReq); err != nil {
		return nil, err
	}

	loc, err := time.LoadLocation(timeReq.Timezone)
	if err != nil {
		return nil, fmt.Errorf("invalid timezone: %v", err)
	}

	return &protocol.CallToolResult{
		Content: []protocol.Content{
			protocol.TextContent{
				Type: "text",
				Text: time.Now().In(loc).String(),
			},
		},
	}, nil
}
```

### 客户端

VSCode安装插件Cline，登录，配置MCP服务器。Trae也支持了，在AI对话框的设置添加下面的配置即可。

```json
{
  "mcpServers": {
    "current_time": {
      "timeout": 60,
      "url": "http://127.0.0.1:8080/sse",
      "transportType": "sse",
      "disabled": false
    }
  }
}
```

输入问题：「告诉我北京时间」，等待即可。

![](https://res.cloudinary.com/cyeam/image/upload/v1744899675/%E6%88%AA%E5%B1%8F2025-04-17_22.20.39_s2frsr.png)

## 最后

MCP协议最大的应用场景在于AI编程，本地文件、数据库资源都可以作为Local Data Sources引入进来支持高效开发，Trae要赶紧跟上了。

---


{% include JB/setup %}
