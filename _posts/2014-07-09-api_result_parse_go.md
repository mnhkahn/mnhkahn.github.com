---
layout: post
title: "Go语言接口开发——不确定JSON数据结构的解析"
description: "今天开发的小总结"
category: "golang"
tags: ["Golang", "json"]
---

在公司主要做接口的开发，会经常遇到接口对接的情况。有的时候，同一个请求返回的JSON数据格式并不一样。如果是正常，则可能只返回一个`status`字段，说明正常；如果中间出错，除了在`status`字段里面说明错误类型，还会通过`error_message`附带错误详细信息。比如要给用户加积分，如果加分失败，还会附带用户id等信息。那么，请求一个接口可能的返回值就是不确定的。

我最初就是定义两个结构体，我处理的数据都共有一个字段`status`，如果能够解析并且`status`表示操作成功，那么用封装成功内容的结构体解析；否则，用封装失败的结构体解析。这就是传说中的**DIRTY HACK**。。。

后来，偶然发现封装正确的结构体也会解析错误的字符串，当然，只会解析共有字段。那么，这个问题就好解决多了。把两个结构体放到一起即可，如果没有该字段，就不会被解析放入值。也就是说，未被解析的变量放的是默认值。

	package main

	import (
		"encoding/json"
		"fmt"
	)
	
	type Result struct {
		Status       int    `json:"status"`
		Message      string `json:"message"`
		ErrorCode    int    `json:"error_code"`
		ErrorMessage string `json:"error_message"`
	}
	
	func main() {
		json_str0 := `{"status":0,"message":"success"}`
		json_str1 := `{"status":1,"error_code":5,"error_message":"error"}`
	
		res0 := Result{}
		res1 := Result{}
	
		err0 := json.Unmarshal([]byte(json_str0), &res0)
		err1 := json.Unmarshal([]byte(json_str1), &res1)
	
		fmt.Println(res0, err0)
		fmt.Println(res1, err1)
	
	}

这么简单的东西，Go语言的基本语法，但是看书的时候没有注意过，关键是做的时候没有认真分析，就直接DIRTY HACK了，我都不能忍自己了。。。

最后，还有一点，Go支持未知JSON数据结构的解析。创建一个interface，把它的地址传进去解析就行了，会解析出`map[string]interface`类型的数据。

---

######*参考文献*
+ 【1】Go语言编程

{% include JB/setup %}
