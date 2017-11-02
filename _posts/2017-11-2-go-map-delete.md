---
layout: post
title: "Golang map 如何进行删除操作？"
description: "map 删除某个key，内存是否会跟着删除？"
category: "Json"
figure: "http://cyeam.qiniudn.com/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20171102091325.jpg"
tags: ["hashmap"]
---

* 目录
{:toc}

---

### map 的删除操作

Golang 内置了哈希表，总体上是使用哈希链表实现的，如果出现哈希冲突，就把冲突的内容都放到一个链表里面。

Golang 还内置了`delete`函数，如果作用于哈希表，就是把 map 里面的 key 删除。

	delete(intMap, 1)
	
### map 的删除原理

可以直接看[源码](https://github.com/golang/go/blob/master/src/runtime/hashmap.go#L607)。

我简单摘几行：

	func mapdelete(t *maptype, h *hmap, key unsafe.Pointer) {
		for ; b != nil; b = b.overflow(t) {
			for i := uintptr(0); i < bucketCnt; i++ {
				b.tophash[i] = empty
				h.count--
			}
		}
	}
	
外层的循环就是在遍历整个 map，删除的核心就在那个`empty`。它修改了当前 key 的标记，而不是直接删除了内存里面的数据。

	empty          = 0 // cell is empty
	
### 如何清空整个 map

看了我上面的分析，那么这段代码可以清空 map 么？

	for k, _ := range m {
		delete(m, k)
	}

1. map 被清空。执行完之后调用`len`函数，结果肯定是0；
2. 内存没有释放。清空只是修改了一个标记，底层内存还是被占用了；
3. 循环遍历了`len(m)`次。上面的代码每一次遍历都会删除一个元素，而遍历的次数并不会因为之前每次删一个元素导致减少。

### 如何真正释放内存？

	map = nil

这之后坐等垃圾回收器回收就好了。

***如果你用 map 做缓存，而每次更新只是部分更新，更新的 key 如果偏差比较大，有可能会有内存逐渐增长而不释放的问题***。要注意。
	


---

{% include JB/setup %}