---
layout: post
title: "Go语言的堆排序实现"
description: "Golang源码sort包。"
category: "Golang"
tags: ["Golang", "Sort"]
---

关于堆排序的算法，可以参考我去年的文章[《堆排序(HEAP SORT)》](http://blog.cyeam.com/computer%20science/2013/04/06/heapsort/)。那篇文章讲的是建立小顶堆进行的排序，这里说的是建立大顶堆建立的排序，差不多。

在Golang源码的sort包里，自带了排序函数。该函数可以对各种类型进行排序，只不过该类型需要实现三个函数，使得该类能够实现`Interface`接口。

	type Interface interface {
		// Len is the number of elements in the collection.
		Len() int
		// Less reports whether the element with
		// index i should sort before the element with index j.
		Less(i, j int) bool
		// Swap swaps the elements with indexes i and j.
		Swap(i, j int)
	}

这三个函数分别是，获取排序队列长度、队列任意两个元素比较大小和交换任意两个元素。

	func (a BySortIndex) Len() int      { return len(a) }
	func (a BySortIndex) Swap(i, j int) { a[i], a[j] = a[j], a[i] }
	func (a BySortIndex) Less(i, j int) bool {
		return a[i] < a[j]
	}

如果是整形数组，可以像上面这样实现。Golang支持多值赋值，所以交换值很简单。自带的`len`也使得长度遍历很简单。比较大小，可以根据实际情况自己定义。

堆排序的核心就是建立大顶堆和交换值，它是本地排序，不需要新分配空间。Golang的源码我已经加了注释，也不难，大家直接阅读即可。

	func heapSort(data Interface, a, b int) {
		first := a
		lo := 0
		hi := b - a
	
		// Build heap with greatest element at top.
		for i := (hi - 1) / 2; i >= 0; i-- {
			siftDown(data, i, hi, first)
		}
	
		// Pop elements, largest first, into end of data.
		// 二叉树结构当中最后一个有子结点的结点
		for i := hi - 1; i >= 0; i-- {
			data.Swap(first, first+i)
			siftDown(data, lo, i, first)
		}
	}
	
	// 建立树函数
	// 父节点root的左孩子2*root + 1
	func siftDown(data Interface, lo, hi, first int) {
		root := lo
		for {
			child := 2*root + 1
			if child >= hi { // child 超出了数组长度，也就是该结点无孩子结点，返回
				break
			}
			if child+1 < hi && data.Less(first+child, first+child+1) { // 右孩子结点存在
				child++
			}
			// 以上是为了在孩子结点当中找到较大的结点，用child表示
			if !data.Less(first+root, first+child) {
				return
			}
			// 如果根结点小于较大的孩子结点，则进行交换；该孩子结点的堆结构可能会被影响，继续去处理孩子结点
			data.Swap(first+root, first+child)
			root = child
		}
	}

本文所涉及到的完整源码请[参考](https://github.com/mnhkahn/go_code/blob/master/heapsort.go)。

---

######*参考文献*
+ 【1】[堆排序(HEAP SORT) - Cyeam](http://blog.cyeam.com/computer%20science/2013/04/06/heapsort/)

{% include JB/setup %}