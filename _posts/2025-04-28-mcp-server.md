---
layout: post
title: "如何用自己的http server搭建一个线上MCP服务？"
description: "使用cyeam.com远程部署MCP服务器"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1745842606/209e5e58-c425-45d4-aa36-b0f5d3e1cd90.jpg"
category: "AI"
tags: ["AI","MCP", "Golang"]
---

* 目录
{:toc}
---

前文讲解了MCP协议并使用Go搭建了一个简单的Demo，本文将介绍如何将其部署到线上。

## MCP Server 初始化

和前面的Demo一样，需要初始化MCP Server，因为要集成到现有 HTTP 服务中，不能直接启动 Server 而是要把Handler注册到 app 中。

```go
app.Handle("/sse", newSseHandler.HandleSSE())
app.Handle("/sse/message", newSseHandler.HandleMessage())
```

app 包是我自研的框架，完整内容可以移步[这里](http://github.com/mnhkahn/gogogo)。

完整代码：
```go

func InitMCPServer() error {
	// Create SSE transport server
	transportServer, newSseHandler, err := transport.NewSSEServerTransportAndHandler("/sse/message", transport.WithSSEServerTransportAndHandlerOptionLogger(pkg.DebugLogger))
	if err != nil {
		return err
	}

	// Initialize MCP server
	mcpServer, err := server.NewServer(transportServer)
	if err != nil {
		return err
	}

	// Register time query tool
	tool, err := protocol.NewTool("current_time", "Get current time for specified timezone", TimeRequest{})
	if err != nil {
		log.Fatalf("Failed to create tool: %v", err)
		return err
	}
	mcpServer.RegisterTool(tool, handleTimeRequest)

	app.Handle("/sse", newSseHandler.HandleSSE())
	app.Handle("/sse/message", newSseHandler.HandleMessage())

	return nil
}
```

## 超时设置

由于是 SSE 协议，需要放开超时时间，否则会报错：`context deadline exceeded`。

需要使用没有超时时间的方式启动：`app.ServeDefault(l)`。不能设置`ReadTimeout`和`WriteTimeout`。

## 代码调用

实际测试的时候AI不一定靠谱，问多了就不真正请求了，所以用代码请求调试靠谱些。

```go
package main

import (
    "context"
    "log"

    "github.com/ThinkInAIXYZ/go-mcp/client"
    "github.com/ThinkInAIXYZ/go-mcp/protocol"
    "github.com/ThinkInAIXYZ/go-mcp/transport"
)

func main() {
    // Create SSE transport client
    transportClient, err := transport.NewSSEClientTransport("https://www.cyeam.com/sse")
    if err != nil {
        log.Fatalf("Failed to create transport client: %v", err)
    }

    // Initialize MCP client
    mcpClient, err := client.NewClient(transportClient)
    if err != nil {
        log.Fatalf("Failed to create MCP client: %v", err)
    }
    defer mcpClient.Close()

    // Get available tools
    ctx := context.Background()
    tools, err := mcpClient.ListTools(ctx)
    if err != nil {
        log.Fatalf("Failed to list tools: %v", err)
    }
    for _, tool := range tools.Tools {
        log.Printf("Tool Name: %+v, Description: %s, Required: %+v", tool.Name, tool.Description, tool.InputSchema.Required)
        if tool.Name == "current_time" {
            req := &protocol.CallToolRequest{
                Name: tool.Name,
                Arguments: map[string]interface{}{
                    "timezone": "Asia/Shanghai",
                },
            }
            resp, err := mcpClient.CallTool(context.Background(), req)
            if err != nil {
                log.Fatalf("Failed to call tool: %v", err)
            } else {
                log.Printf("Tool Response: %+v", resp)
            }
        }
    }
}
```

## 用 Trae 调试

配置：

```json
{
  "mcpServers": {
    "current_time": {
      "url": "https://www.cyeam.com/sse"
    }
  }
}
```

命令：`使用mcp服务告诉我北京时间`。

结果：
![](https://res.cloudinary.com/cyeam/image/upload/v1745852839/1753e5c1-0453-47e4-8202-85d51d05d8e5.png)

{% include JB/setup %}
