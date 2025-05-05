---
layout: post
title: "MCP Resource学习，用Go搭建一个Demo"
description: "基于官方提供的Inspector学习 Resource 相关内容，并用 Go 在服务端搭一个 Demo。"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1746441901/8addd27e-4e07-4d59-a5b3-d5dd8a25f065.png"
category: "AI"
tags: ["AI","MCP", "Golang"]
---

* 目录
{:toc}
---

## 概述
MCP 协议提供了标准协议来让服务端向客户端暴露资源内容，例如文件、数据库，每个资源使用唯一标识`URI`来区分。

## 协议消息

- Listing Resources

客户端发送`resources/list`请求查询可用的资源，该操作支持分页。

- Reading Resources

发送`resources/read`请求检索资源内容。

- Resource Templates

`resources/templates/list`允许向客户端暴露参数化资源。

- List Changed Notification

当资源发生变更时，服务器会发送`notifications/resources/list_changed`通知。

- Subscriptions

协议支持订阅资源变更，可以支持订阅指定资源当发生变更时会收到通知。

## 数据流

![IMG-THUMBNAIL](https://res.cloudinary.com/cyeam/image/upload/v1746441901/8addd27e-4e07-4d59-a5b3-d5dd8a25f065.png)

## 资源类型

### 资源定义

- uri: 资源的唯一标识符
- name: 资源的名称
- description: 【可选】资源描述
- mimeType: 【可选】资源的MIME类型，常见的有：`text/plain`、`text/html`、`image/jpeg`、`image/png`、`application/json`、`application/pdf`、`application/octet-stream`等
- size: 【可选】资源大小，单位为字节

### URI Scheme

- https://
- file://
- git://

### 错误码

- 资源不存在: `-32002`
- 内部错误：`-32603`

## Go 实现

```go
func registerAllGoResources(mcpServer *server.Server) {
	for _, item := range items {
		mcpServer.RegisterResource(&protocol.Resource{
			URI:      item.Link,
			Name:     item.Title,
			MimeType: "text/html",
		}, resourceHandler)
	}
}

func resourceHandler(ctx context.Context, r *protocol.ReadResourceRequest) (*protocol.ReadResourceResult, error) {
	for _, item := range items {
		if item.Link == r.URI {
			res := protocol.NewReadResourceResult([]protocol.ResourceContents{
				protocol.TextResourceContents{
					URI:      item.Link,
					Text:     item.Description,
					MimeType: "text/html",
				},
			})
			return res, nil
		}
	}
	return nil, fmt.Errorf("resource not found")
}
```

![IMG-THUMBNAIL](https://res.cloudinary.com/cyeam/image/upload/v1746452045/5d7de112-db70-44b6-8803-e11fe5fff54c.png)


{% include JB/setup %}
