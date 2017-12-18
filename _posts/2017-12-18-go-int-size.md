---
layout: post
title: "Golang int 和 uint 天天用，那么问题来了，它多大？"
description: "这么基础的问题可能很多人都不知道"
category: "Json"
figure: "http://cyeam.qiniudn.com/blog/171218/E9lK3HAC6g.jpg?imageslim"
tags: ["int"]
---

* 目录
{:toc}

---

### 写在前面

今天调试一个问题，发现一个我无法理解的情况：

	package main

	import (
		"fmt"
		"math"
		"runtime"
	)

	func main() {
		var a uint = math.MaxUint64
		fmt.Println("Hello, playground", a, runtime.Version())
	}
	
把64位的数字赋值给`uint`，我理解`uint`是32位的，为啥可以编译通过？但是我接着又在 playground 上试了一把，结果是编译不过了：

> constant 18446744073709551615 overflows uint

### int 和 uint 到底占多大空间？

其实我一直理解是32位的。因为别的语言是这样，惯性思维了。

直接看一下官方文档：

> int is a signed integer type that is at least 32 bits in size. It is a distinct type, however, and not an alias for, say, int32.

`uint`和`int`情况差不多。翻译一下，就是说这个整形最少占32位，`int`和`int32`是两码事。

再看一下 davecheney 大神的回复（大神半夜回复 GitHub 真是敬业啊）：

> uint is a variable sized type, on your 64 bit computer uint is 64 bits wide.

我的理解`uint`类型长度取决于 CPU，如果是32位CPU就是4个字节，如果是64位就是8个字节。我的电脑是64位的，而 playground 是32位的，问题就出在这里。

### More

这里就会出现一个情况，`int`和`uint`是根据 CPU 变化的，如何知道当前系统的情况？

+ CPU 型号：`runtime.GOARCH`
+ `int`的长度：`strconv.IntSize`

写了这么多年 Golang，`int`天天用，一直被我当32位处理，说来惭愧。。。

---

题图：孜然牛肉。

{% include JB/setup %}