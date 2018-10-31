---
layout: post
title: "Golang 优化之路——空结构"
description: "Golang 内置了 hashmap 类型。编码的过程中 hashset 也是很常用的一种数据结构。我们如何使用内置的 hashmap 来封装一个高效的 hashset？"
category: "golang"
tags: ["Golang","optimize","tool"]
---

* 目录
{:toc}

---

### 写在前面

开发 hashset 常用的套路：

	map[int]int8
	map[int]bool

我们一般只用 map 的键来保存数据，值是没有用的。所以来缓存集合数据会造成内存浪费。

### 空对象

空对象是个神奇的东西。它指的是没有字段的结构类型。

	type Q struct{}

<ins class="adsbygoogle"
     style="display:block; text-align:center;"
     data-ad-layout="in-article"
     data-ad-format="fluid"
     data-ad-client="ca-pub-1651120361108148"
     data-ad-slot="4918476613"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
	
它牛逼的地方在于：

+ 可以和普通结构一样操作

		var a = []struct{}{struct{}{}}
		fmt.Println(len(a)) // prints 1

+ 不占用空间

		var s struct{}
		fmt.Println(unsafe.Sizeof(s)) // prints 0

+ 声明两个空对象，它们指向同一个地址

		type A struct{}
		a := A{}
		b := A{}
		fmt.Println(&a == &b) // prints true
	
造成这个结果的原因是 Golang 的编译器会把这种空对象都当成`runtime.zerobase`处理。

	var zerobase uintptr


### hashset

有了上面的介绍，就可以利用空结构来优化 hashset 了。

	var itemExists = struct{}{}

	type Set struct {
		items map[interface{}]struct{}
	}
	
	func New() *Set {
		return &Set{items: make(map[interface{}]struct{})}
	}

	func (set *Set) Add(item interface{}) {
		set.items[item] = itemExists
	}
	
	func (set *Set) Remove(item interface{}) {
		delete(set.items, item)
	}

	func (set *Set) Contains(item interface{}) bool {
		if _, contains := set.items[item]; !contains {
			return false
		}
		return true
	}
	
一个简易的 hashset 实现就完成了。

### 性能比较

	func BenchmarkIntSet(b *testing.B) {
		var B = NewIntSet(3)
		B.Set(10).Set(11)
		for i := 0; i < b.N; i++ {
			if B.Exists(1) {

			}
			if B.Exists(11) {

			}
			if B.Exists(1000000) {

			}
		}
	}

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
	
	BenchmarkIntSet-2       50000000                35.3 ns/op             0 B/op          0 allocs/op
	BenchmarkMap-2          30000000                41.2 ns/op             0 B/op          0 allocs/op
	
### 结论

+ 性能，有些提升，但不是特别明显。尤其是线上压力不大的情况性能应该不会有明显变化；
+ 内存占用。我们的服务缓存较多、占用内存较大，通过这个优化实测可以减少 1.6 GB 的空间。不过这个优化的空间取决于数据量。

### 后续

前面有个例子：

	var a, b struct{}
	fmt.Println(&a == &b) // true

从 Go1.6 开始输出的结果有了变化，之前是`true`，现在是`false`。

[官方](https://golang.org/ref/spec#Comparison_operators)的解释：

> Pointer values are comparable. Two pointer values are equal if they point to the same variable or if both have value nil. **Pointers to distinct zero-size variables may or may not be equal**.

不过这个处理并不影响对于空结构体的使用。官方对于空指针相等的判断进行了修改，至于原因并没有给出详细的解释。


---

### *参考文献*
+ 【1】[The empty struct - Dave Cheney](https://dave.cheney.net/2014/03/25/the-empty-struct)
+ 【2】[gods - emirpasic](https://github.com/emirpasic/gods/blob/master/sets/hashset/hashset.go)
+ 【3】 《Go 语言学习笔记》 - 雨痕。5.5 结构。

{% include JB/setup %}
