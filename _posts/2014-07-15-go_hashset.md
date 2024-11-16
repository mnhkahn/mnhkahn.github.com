---
layout: post
title: "Go 语言简单实现HashSet"
description: "公司有个需求，就是能够对列表去重。本屌原本想直接用for循环实现，后来去查了查Java的实现方式，大开眼界。"
category: "Golang"
tags: ["Golang", "HashSet"]
---

公司有个需求，就是能够对列表去重。本屌原本想直接用`for`循环实现，后来去查了查Java的实现方式，大开眼界。

Set，是指数学里的集合。集合当中不能有重复的元素。判断是否有重复，可以使用哈希的方法。Java容器当中有基于哈希实现的`HashSet`。把元素都放入HashSet当中，如果有重复，则会插入失败。这样就能判断出来是否重复了。

而Golang并没有这种高级的容器。只是找了一个大神实现的，稍微改了一下，能够支持字符串检测。

> http://play.golang.org/p/_FvECoFvhq

	type HashSet struct {
		set map[string]bool
	}
	
	func NewHashSet() *HashSet {
		return &HashSet{make(map[string]bool)}
	}
	
	func (set *HashSet) Add(i string) bool {
		_, found := set.set[i]
		set.set[i] = true
		return !found //False if it existed already
	}
	
	func (set *HashSet) Get(i string) bool {
		_, found := set.set[i]
		return found //true if it existed already
	}
	
	func (set *HashSet) Remove(i string) {
		delete(set.set, i)
	}

内部使用map来保存哈希结果。而哈希函数直接就是使用字符串作为哈希结果。

---

还可以看我之后的文章[Golang 优化之路——空结构](https://blog.cyeam.com/golang/2017/04/11/go-empty-struct)，这个方案更好一些。


---

###### *参考文献*

+ 【1】[判断int数组中的元素是否重复 - 百度知道](https://zhidao.baidu.com/question/172011519.html)
+ 【2】[Sets Data Structure in Golang - StackExchange](https://programmers.stackexchange.com/questions/177428/sets-data-structure-in-golang)
+ 【3】[java里有没有专门判断List里有重复的数据？最好能知道是第几行重复. - CSDN论坛](https://bbs.csdn.net/topics/120025156)


{% include JB/setup %}
