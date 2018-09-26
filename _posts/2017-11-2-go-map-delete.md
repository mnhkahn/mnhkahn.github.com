---
layout: post
title: "Golang map 如何进行删除操作？"
description: "map 删除某个key，内存是否会跟着删除？"
category: "Json"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeam/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20171102091325.jpg"
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

### 验证

下面来验证一下上面说的原理。我们申请一个全局`map`来保证内存被分配到堆上面。初始化这个`map`，分配比较大的空间，方便对比。每完成一次操作，进行一个垃圾回收，并且打印当前内存堆的情况。

	var intMap map[int]int
	var cnt = 8192

	func main() {
		printMemStats()

		initMap()
		runtime.GC()
		printMemStats()

		log.Println(len(intMap))
		for i := 0; i < cnt; i++ {
			delete(intMap, i)
		}
		log.Println(len(intMap))

		runtime.GC()
		printMemStats()

		intMap = nil
		runtime.GC()
		printMemStats()
	}

	func initMap() {
		intMap = make(map[int]int, cnt)

		for i := 0; i < cnt; i++ {
			intMap[i] = i
		}
	}

	func printMemStats() {
		var m runtime.MemStats
		runtime.ReadMemStats(&m)
		log.Printf("Alloc = %v TotalAlloc = %v Sys = %v NumGC = %v\n", m.Alloc/1024, m.TotalAlloc/1024, m.Sys/1024, m.NumGC)
	}

结果如下：

	2018/05/31 10:54:25 Alloc = 100 TotalAlloc = 100 Sys = 1700 NumGC = 0
	2018/05/31 10:54:25 Alloc = 422 TotalAlloc = 426 Sys = 3076 NumGC = 1
	2018/05/31 10:54:25 8192
	2018/05/31 10:54:25 0
	2018/05/31 10:54:25 Alloc = 424 TotalAlloc = 429 Sys = 3140 NumGC = 2
	2018/05/31 10:54:25 Alloc = 112 TotalAlloc = 431 Sys = 3140 NumGC = 3

结论很明显：

+ NumGC 是垃圾回收次数；Alloc 是对对象大小，单位是 KB；Sys 是从 OS 获取的内存大小，单位是 KB；
+ 第一行，没有进行过 GC，默认真用了 100 KB 的内存；
+ `map`初始化完成之后进行一次 GC，此时内存占了 422 KB；
+ 接下来就是执行`delete`操作，可以看到`map`已经被清空了，也执行了一次 GC，但是内存没有被释放；
+ 最后把`map`置为空，内存才被释放。
+ 我使用的版本`go version go1.10.1 darwin/amd64`。

### 为什么这么设计？

这么设计看起来不是那么完美，为什么要这么做呢？

	query := map[string]string{}

	query["test0"] = "0"
	query["test1"] = "1"
	query["test2"] = "2"

	i := 0
	for k, v := range query {
		delete(query, "test2")
		fmt.Println(query, k, v)
		i++
	}

我们可以在遍历`map`的时候删除里面的元素，而且可以删除没有遍历到的元素，为了保证删除了之后遍历不发生异常，才这么设计的吧。

### 这样是内存泄漏么？

我觉得这样不算是内存泄漏。如果继续给这个`map`写入值，如果这个值命中了之前被删除的bucket，那么会覆盖之前的empty数据。

---

{% include JB/setup %}