---
layout: post
title: "Golang 优化之路——Cantor pair"
description: "某一种对象是通过两个ID唯一确定的，如何处理这种数据结构以便快速查找以及节约内存？今天讲一种优化算法——Cantor pairing function。"
category: "golang"
tags: ["Golang","optimize","tool"]
---

### 写在前面

某一种对象是通过两个ID唯一确定的，如何处理这种数据结构以便快速查找以及节约内存？先说一种笨方法——用字符串来处理。这是比较容易想到的（我觉得一般最容易想到的也是最简单粗暴的方法都是用字符串来搞搞搞）。

	fmt.Sprintf("%d_%d", id1, id2)

这样就成了。存储的时候用字符串来保存，查询比较的时候用字符串的方法来计算。当然，把数字当作字符串来保存和计算本身就是极其浪费内存和CPU的。

### Cantor pairing function 简介

[康托尔配对 - Cantor pairing function](https://en.wikipedia.org/wiki/Pairing_function)，是一种将两个自然数转成唯一一个自然数的方法。具体原理我就不说了，我也看不懂。。。简单地说：

+ 只支持自然数。自然数是整数（自然数包括正整数和零）；
+ 支持反解；
+ `f(k1, k2)`和`f(k2, k1)`得到的结果是不同的。当然，如果你想得到相同的也是可以的，计算支持把两个数字排个序；
+ 计算结果有可能比`k1`和`k2`都大很多，需要注意溢出的问题。

### Example

这个算法只有一个公式，实现起来很容易。我索性自己造了一个轮子，[pairing](https://github.com/mnhkahn/pairing)。公式的推导请移步[维基百科](https://en.wikipedia.org/wiki/Pairing_function)。

	import "github.com/mnhkahn/pairing"
	
	pair := pairing.Encode(k1, k2)

	k3, k4 := pairing.Decode(pair2)
	
支持正向编码以及反向解码。

### 实现

![IMG-THUMBNAIL](https://wikimedia.org/api/rest_v1/media/math/render/svg/deecd5b1f0f921ae95f5df9521b1846f8f9e2ee3)

	import "math"
	
	func Encode(k1, k2 uint64) uint64 {
		pair := k1 + k2
		pair = pair * (pair + 1)
		pair = pair / 2
		pair = pair + k2
	
		return pair
	}
	
![IMG-THUMBNAIL](https://wikimedia.org/api/rest_v1/media/math/render/svg/daa8d22b2942b099d4be50c2991eebdaaf700487)
![IMG-THUMBNAIL](https://wikimedia.org/api/rest_v1/media/math/render/svg/a5ea840fb429ed04261f8ab3a3b095a6ae1b66a9)
![IMG-THUMBNAIL](https://wikimedia.org/api/rest_v1/media/math/render/svg/e3827ff2a4b59fa136c4076bd81eca3b9e7f3313)
![IMG-THUMBNAIL](https://wikimedia.org/api/rest_v1/media/math/render/svg/6373c7017075ef6a24a68995c10b564a2e5eccf6)

	func Decode(pair uint64) (uint64, uint64) {
		w := math.Floor((math.Sqrt(float64(8*pair+1)) - 1) / 2)
		t := (w*w + w) / 2
	
		k2 := pair - uint64(t)
		k1 := uint64(w) - k2
		return k1, k2
	}

### 与其它数据结构的对比

其中一个要对比的就是和前面说的字符串的比较。还有一种代替方案：两个整数`int32`，这64位数字拼接一个`int64`里面，第一个数字占前32位，后一个数字占后32位，也是一个可行的方案。我们可以把这个方法叫做bit方法。
	
	func EncodeBit(k1, k2 uint32) uint64 {
		pair := uint64(k1)<<32 | uint64(k2)
		return pair
	}
	
	func DecodeBit(pair uint64) (uint32, uint32) {
		k1 := uint32(pair >> 32)
		k2 := uint32(pair) & 0xFFFFFFFF
		return k1, k2
	}

实现起来更简单。那和Cantor pair相比性能怎么样呢？


	import (
		"fmt"
		"testing"
	)
	
	var TEST_PAIRS = [][]uint64{
		[]uint64{0, 0},
		[]uint64{0, 1},
		[]uint64{1, 0},
	}
	
	var TEST_RESs = []uint64{
		0,
		2,
		1,
	}
	
	var TEST_RESBits = []uint64{
		0,
		1,
		4294967296,
	}
	
	func TestPair(t *testing.T) {
		for i, p := range TEST_PAIRS {
			a, b := p[0], p[1]
			if pair := Encode(a, b); pair != TEST_RESs[i] {
				t.Error(a, b, pair)
			}
		}
	
		for i, p := range TEST_PAIRS {
			a, b := p[0], p[1]
			pair := TEST_RESs[i]
			if x, y := Decode(pair); x != a || y != b {
				t.Error(a, b, pair)
			}
		}
	
		fmt.Println(Encode(559, 83792))
	
		for i, p := range TEST_PAIRS {
			a, b := uint32(p[0]), uint32(p[1])
			if pair := EncodeBit(a, b); pair != TEST_RESBits[i] {
				t.Error(a, b, pair)
			}
		}
	
		for i, p := range TEST_PAIRS {
			a, b := uint32(p[0]), uint32(p[1])
			pair := TEST_RESBits[i]
			if x, y := DecodeBit(pair); x != a || y != b {
				t.Error(a, b, pair)
			}
		}
	
		fmt.Println(EncodeBit(559, 83792))
	}
	
	func BenchmarkEncode(b *testing.B) {
		for i := 0; i < b.N; i++ {
			Encode(559, 83792)
		}
	}
	
	func BenchmarkDecode(b *testing.B) {
		for i := 0; i < b.N; i++ {
			Decode(3557671568)
		}
	}
	
	func BenchmarkEncodeBit(b *testing.B) {
		for i := 0; i < b.N; i++ {
			EncodeBit(559, 83792)
		}
	}
	
	func BenchmarkDecodeBit(b *testing.B) {
		for i := 0; i < b.N; i++ {
			DecodeBit(2400886802256)
		}
	}
	
	func BenchmarkEncodeStr(b *testing.B) {
		for i := 0; i < b.N; i++ {
			_ = fmt.Sprintf("%d_%d", 559, 83792)
		}
	}
	
	/*
	go test -bench=. -benchmem
	BenchmarkEncode-2       2000000000               0.37 ns/op            0 B/op          0 allocs/op
	BenchmarkDecode-2       50000000                26.9 ns/op             0 B/op          0 allocs/op
	BenchmarkEncodeBit-2    2000000000               0.37 ns/op            0 B/op          0 allocs/op
	BenchmarkDecodeBit-2    2000000000               0.37 ns/op            0 B/op          0 allocs/op
	BenchmarkEncodeStr-2     5000000               271 ns/op              32 B/op          3 allocs/op
	*/

	
### 结论

+ 用字符串保存的性能最差，剩余两个是这个性能的400倍；
+ Cantor pair和bit方法的性能相当，反解的时候性能还查一些；
+ 既然性能相当，虽然本文着重介绍的是Cantor pair算法，但我还是建议，如果bit方法能满足你的需求，尤其是数字范围较小的时候，还是用这个比较好。简单的方法在维护方面会让你更加得心应手，即使你懂那些复杂的公式是如何推导出来的^ ^。

本文所涉及到的完整源码请[参考](https://github.com/mnhkahn/pairing)。


---

{% include JB/setup %}
