---
layout: post
title: "Swiftype的Golang API 发布！"
description: "为了给我的网站接入Swiftype，开发了Golang的API。"
category: "golang"
tags: ["Golang","swiftype","tool"]
---

### 写在前面

我是一个Golang程序员，基本上我所有的东西都是用Go开发的。前不久想给我的[个人网站](http://cyeam.com)接入搜索功能，使用了Swiftype这个工具。然而我发现它并没有Golang的API工具包。在GitHub上面找了一个包，却发现有bug不能用，遂自己fork了代码搞一套。

源码地址：[https://github.com/mnhkahn/swiftype](https://github.com/mnhkahn/swiftype)

### 安装

	go get -v gopkg.in/mnhkahn/swiftype.v1

### 文档

文档可以在[godoc](https://godoc.org/github.com/mnhkahn/swiftype)上面查看。目前只支持搜索方法，因为我这边也只用这个，如果未来我这边有别的API需求，会考虑更新。

[type Client](https://godoc.org/github.com/mnhkahn/swiftype#Client)

+ [func NewClientWithApiKey(api_key string, host string) *Client](https://godoc.org/github.com/mnhkahn/swiftype#NewClientWithApiKey)
+ [func NewClientWithUsernamePassword(username string, password string, host string) *Client](https://godoc.org/github.com/mnhkahn/swiftype#NewClientWithUsernamePassword)
+ [func (c *Client) Engine(engine string) ([]byte, error)](https://godoc.org/github.com/mnhkahn/swiftype#Client.Engine)
+ [func (c *Client) Engines() ([]byte, error)](https://godoc.org/github.com/mnhkahn/swiftype#Client.Engines)
+ [func (c *Client) Search(engine string, query string) (*SwiftypeResult, error)](https://godoc.org/github.com/mnhkahn/swiftype#Client.Search)

[type SwiftypeResult](https://godoc.org/github.com/mnhkahn/swiftype#SwiftypeResult)


### 例子

	SWIFTYPE := *swiftype.Client
	SWIFTYPE_APIKEY := "YOUR OWN API KEY"
	SWIFTYPE_HOST := "api.swiftype.com"
	SWIFTYPE_ENGINE := "YOUR OWN ENGINE"
	
	SWIFTYPE := swiftype.NewClientWithApiKey(SWIFTYPE_APIKEY, SWIFTYPE_HOST)
	
	data, err := SWIFTYPE.Search(SWIFTYPE_ENGINE, q)
	if err != nil {
	    panic(err)
	}
	_ = data




---

{% include JB/setup %}
