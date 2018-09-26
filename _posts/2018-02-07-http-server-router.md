---
layout: post
title: "Golang HTTP 服务路由查询"
description: "通过黑科技扩展原生包的功能。"
category: "HTTP"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeamblog/180207/khi6gCIb7k.jpg?imageslim"
tags: ["Golang","HTTP","Router"]
---

* 目录
{:toc}

---

### Golang HTTP 原始包

Golang 的框架用过不少，越来越发现还是原生的好。我们一般只做接口，对于项目服务没有那么高的灵活性要求，原生的 HTTP 包已经够用。而且原生包通过接口的形式提供了扩展的方式，自己简单扩展一下就方便很多。Golang 的设计思想就是简单，还是用简单的方式比较好。

### 路由

原生包的路由非常简单，就用了一个哈希表来报存路由。

	type ServeMux struct {
		mu    sync.RWMutex
		m     map[string]muxEntry
		hosts bool // whether any patterns contain hostnames
	}

每次请求进来都要在`m`里查询路由。但是这个路由有个问题，它是局部变量，而且没有对应的`getter`函数，我们没法知道路由的内容。

### 黑科技获取变量内部变量

获取内部变量`m`的方法也不难，通过反射的方式。路由变量`ServeMux`可以拿到，通过反射是可以拿到它的局部变量的。反射也提供了操作哈希表的对于方法。直接上代码：

	v := reflect.ValueOf(mux)
	m := v.Elem().FieldByName("m")

	keys := m.MapKeys()

	routers := make([]string, 0, len(keys))
	for _, key := range keys {
		routers = append(routers, key.String())
	}

	sort.Strings(routers)
	
---

题图：天津瓷房子。

最近半年更新少了很多，太忙了，`Go`代码写得也少了很多，实在惭愧。又要到新年了，希望明年更好。

{% include JB/setup %}