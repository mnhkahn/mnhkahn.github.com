---
layout: post
title: "狗日的slice"
description: "虽然知道slice的实现，虽然也帮别人看过这个问题，但还是要被坑。"
category: "golang"
tags: ["Golang"]
---

首先推荐一下雨痕大神的新书：[《Golang源码剖析（第五版）》](https://github.com/qyuhen/book)。

进入正题。Golang和其它语言不通的是，他增加了一个`slice`，这不同于传统的数组，但是我们使用它又要按照数组的用法来，容易混淆。

先说一下我理解的传统数组，数组的名称就是数组在内存里面的首地址，访问每个子元素就是首地址加子元素长度访问。所以这应该是一个引用对象类型。

而Golang的`slice`，引用一下雨痕大神的文章说明：

> runtime.h


	struct Slice
	{
		byte* array;
		uintgo len;
		uintgo cap;
	}




`slice`底层是通过`struct`实现的，所以传递的时候是值拷贝传递，但是，`slice`的内容是通过数组指针实现的。就会发生这种现象：***通过值传递，`len`和`cap`都不会变，所以使用的时候不会感觉到内容有变化，但是实际上`byte`数组是发生变化的。

上代码：

	package main
	
	import "fmt"
	
	func main() {
		testMap := make(map[int64]int64)
		fmt.Println(testMap)
		FuckMap(testMap)
		fmt.Println(testMap)
		FuckMap2(testMap)
		fmt.Println(testMap)
	
		testSlice := []int64{}
		fmt.Println(testSlice)
		FuckSlice(testSlice)
		fmt.Println(testSlice)
		
		FuckSlice2(&testSlice)
		fmt.Println(testSlice)
	}
	
	func FuckMap(t map[int64]int64) map[int64]int64 {
		t[1] = 1
		return t
	}
	
	func FuckMap2(t map[int64]int64) map[int64]int64 {
		t[1] = 2
		return t
	}
	
	func FuckSlice(a []int64) []int64 {
		a = append(a, 1)
		return a
	}
	
	func FuckSlice2(a *[]int64) *[]int64 {
		*a = append(*a, 1)
		return a
	}
	
直接看后半部分。`FuckSlice`函数对于`slice`的修改是不起作用的，因为`slice`是按值传递的；然后我们强行改成按引用传递，就是传递`slice`的地址作为参数，这时的修改就是起作用的。所以，***对于修改`slice`的操作要注意，有可能会修改失败。***


---


---

{% include JB/setup %}
