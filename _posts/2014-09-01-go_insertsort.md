---
layout: post
title: "Go语言的插入排序实现"
description: "Golang源码sort包。"
category: "Golang"
tags: ["Golang", "Sort"]
---

这个算法还是我考研的时候看懂的。插入排序大体有两种，头插法和尾插法。区别就是插入的位置是头部还是尾部。

简单说一下插入排序的思路：

+ 从第二个元素开始遍历，第一个元素认为是有序的；
+ 将要插入的元素依次与已有序队列比较，插入到合适的位置；
+ 循环执行，直到遍历结束。

Golang包里的实现和我上面说的严奶奶的有点区别。将遍历得到的元素倒着与有序队列依次比较。如果比有序队列的小，交换这两个元素。

这样的方法和传统的相比，插入步骤同样都是通过从后向前依次移动实现的插入。而这个方法更加简单一点，不需要声明临时变量。

	package main
	
	import "fmt"
	
	func insertionSort(data Interface, a, b int) {
		for i := a + 1; i < b; i++ {
			for j := i; j > a && data.Less(j, j-1); j-- {
				data.Swap(j, j-1)
			}
		}
	}
	
	type BySortIndex []int
	
	func (a BySortIndex) Len() int      { return len(a) }
	func (a BySortIndex) Swap(i, j int) { a[i], a[j] = a[j], a[i] }
	func (a BySortIndex) Less(i, j int) bool {
		return a[i] < a[j]
	}
	
	func main() {
		test0 := []int{49, 38, 65, 97, 76, 13, 27, 49}
		insertionSort(BySortIndex(test0), 0, len(test0))
		fmt.Println(test0)
	}
	
	type Interface interface {
		// Len is the number of elements in the collection.
		Len() int
		// Less reports whether the element with
		// index i should sort before the element with index j.
		Less(i, j int) bool
		// Swap swaps the elements with indexes i and j.
		Swap(i, j int)
	}

本文所涉及到的完整源码请[参考](https://github.com/mnhkahn/go_code/blob/master/insertsort.go)。

---
+ 【1】数据结构 - 严蔚敏

{% include JB/setup %}