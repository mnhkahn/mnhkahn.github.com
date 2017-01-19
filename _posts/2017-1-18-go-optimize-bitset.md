---
layout: post
title: "Golang 优化之路——bitset"
description: "开发过程中会经常处理集合这种数据结构，简单点的处理方法都是使用内置的map实现。今天讲一种优化方式——bitset。"
category: "golang"
tags: ["Golang","optimize","tool"]
---

### 写在前面

开发过程中会经常处理集合这种数据结构，简单点的处理方法都是使用内置的map实现。但是如果要应对大量数据，使用map占用内存大的问题就会凸显出来。内存占用高又会带来一些列的问题，这里就不展开说了。还有就是，大量数据存放于map，查找的哈希算法消耗也会很高。这时就该考虑对数据结构进行优化。之前浏览[awesome-go](http://awesome-go.com/)时发现了一种叫bitset的数据结构，今天就介绍一下它。

### bitset 简介

首先这是一个数据结构。从名字set不难发现，这是一个集合的数据结构。bit的含义也比较好懂，通过set是通过bit实现的。如果你需要一个集合，正好集合内的元素都是正整数，那么用这个就没错了。

### Example

	import "github.com/willf/bitset"
	
	var b bitset.BitSet // 定义一个BitSet对象
	b.Set(10).Set(11) // 给这个set新增两个值10和11
	if b.Test(1000) { // 查看set中是否有1000这个值（我觉得Test这个名字起得是真差劲，为啥不叫Exist）
		b.Clear(1000) // 情况set
	}
	for i,e := v.NextSet(0); e; i,e = v.NextSet(i + 1) { // 遍历整个Set
	   fmt.Println("The following bit is set:",i);
	}
	if B.Intersection(bitset.New(100).Set(10)).Count() > 1 { // set求交集
		fmt.Println("Intersection works.")
	}
	
这个包功能已经非常完善了，完整的文档可以参考它的[godoc](https://godoc.org/github.com/willf/bitset)。我使用这些包，除了看重基础功能（对于集合，就是增删改查这些），还有就是得方便调试。bitset内部保存数字都是按位存的，如果调试的时候是把bitset的内部数据给我看，我也是看不懂的，还好这个包提供了`String()`方法，可以把我设置的数据已字符串的形式返回，棒棒哒。

### 实现原理

研究一下实现原理才是我的Style。大概说一下原理。正整数集合可以都放到一个大的整数里面，用位来表示数字。比如`1001`就可以表示0和2这两个数字。用一个bit代替了一个`int`，可以大大降低内存的占用。但是一个整数最大也就64位，也就是说最大表示的数字就是64了，所以可以通过多个`int`拼接的形式来表示大整数。

bitset的内部数据结构，很亲切有木有：

	type BitSet struct {
		length uint // set的大小
		set    []uint64 // 这个就会被用来表示一个大整数
	}
	
通过下面的测试代码对于内部实现一探究竟：

	var b bitset.BitSet // 定义一个BitSet对象
	fmt.Println(b.Bytes())
    b.Set(0)
    fmt.Println(b.Bytes(),0)
	b.Set(10) // 给这个set新增两个值10
    fmt.Println(b.Bytes(),0,10)
    b.Set(64)
	fmt.Println(b.Bytes(),0,10,64)
	if b.Test(1000) { // 查看set中是否有1000这个值（我觉得Test这个名字起得是真差劲，为啥不叫Exist）
		b.Clear(1000) // 情况set
	}
	
输出：
	[]
	[1] 0
	[1025] 0 10
	[1025 1] 0 10 64
	
+ 新建的bitset，set是空`[]`
+ 放入了一个0，用第一位表示，也就是`0x00000001`
+ 放入了10，内部结构`0x00000041`
+ 放入了64，这个时候一个整数已经存不下了，内部结构是`0x00000041`和`0x00000001`。set这个数组里面，从前往后表示的数据依次增加，但是在`uint64`内部，是从低位开始，低位表示小的数。

### 与其它数据结构的对比

表示正整数的集合，Golang有很多种方式，自带的`map`就可以，当然这是最差的一种选择，首先就是内存的浪费，其次是每次查找还涉及到hash计算，虽然理论上hashmap的复杂度是O(1)，实际上跟bitset比完全就是渣渣。此外，bitset都得升级版[roaring](github.com/RoaringBitmap/roaring)也是不错的选择。如果你要保存的数据是10000000000这种级别的，那么用bitset就会存在低位浪费内存的情况，roaring可以用来压缩空间。

	import (
		"testing"

		"github.com/RoaringBitmap/roaring"
		"github.com/willf/bitset"
	)

	func BenchmarkMap(b *testing.B) {
		var B = make(map[int]int8, 3)
		B[10] = 1
		B[11] = 1
		for i := 0; i < b.N; i++ {
			if _, exists := B[1]; exists {

			}
			if _, exists := B[11]; exists {

			}
			if _, exists := B[1000000]; exists {

			}
		}
	}

	func BenchmarkBitset(b *testing.B) {
		var B bitset.BitSet
		B.Set(10).Set(11)
		for i := 0; i < b.N; i++ {
			if B.Test(1) {

			}
			if B.Test(11) {

			}
			if B.Test(1000000) {

			}
		}
	}

	func BenchmarkRoaring(b *testing.B) {
		for i := 0; i < b.N; i++ {
			B := roaring.BitmapOf(10, 11)
			if B.ContainsInt(1) {

			}
			if B.ContainsInt(11) {
			}
			if B.ContainsInt(1000000) {

			}

		}
	}
	
	$ go test -bench=.* -benchmem 
	
	BenchmarkMap-2          50000000                28.4 ns/op             0 B/op          0 allocs/op
	BenchmarkBitset-2       2000000000               1.86 ns/op            0 B/op          0 allocs/op
	BenchmarkRoaring-2       3000000               492 ns/op             152 B/op          6 allocs/op
	
### 结论

如果是比较连续的非负整数，推荐用bitset解决集合的问题。当然具体问题具体分析。

本文所涉及到的完整源码请[参考](https://github.com/mnhkahn/go_code/tree/master/bitset)。


---

{% include JB/setup %}
