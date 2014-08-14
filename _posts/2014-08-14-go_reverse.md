---
layout: post
title: "字符串反转"
description: "Golang的实现。"
category: "Golang"
tags: ["Golang"]
---

字符串反转的Golang实现，应该是最简单的了。废话不多说，代码如下：

	package main

	func Reverse(s string) string {
		r := []rune(s)
		for i, j := 0, len(r)-1; i < j; i, j = i+1, j-1 {
			r[i], r[j] = r[j], r[i]
		}
		return string(r)
	}
	func main() {
		a := "Hello, 世界"
		println(a)
		println(Reverse(a))
	}

Golang本身支持计算字符串长度，并且由于支持多值赋值，交换值也是格外的简单。其他语言无非要单独处理一下这两个部分，通过遍历计算出字符串长度，再通过异或或者加法交换值。为了能够处理字符串里面包含中文的情况，这里使用`rune`进行处理。

本文所涉及到的完整源码请[参考](https://github.com/mnhkahn/go_code/blob/master/reverse.go)。

---


{% include JB/setup %}