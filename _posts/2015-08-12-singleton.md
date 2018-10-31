---
layout: post
title: "单件模式——Golang实现"
description: "很常见的一个模式，之前的文章也写过，这次完整描述一下。"
category: "designpattern"
tags: ["Design Pattern", "Golang"]
---
 
单件模式比较常见，算是创建型的设计模式，和工厂模式不同，他只能创建一个实例。他的应用场景很多，比如MySQL只能有一个实例这种都算。

单件模式能简单分成支持并发和不支持并发两种。不过并发这个很简单，满大街Golang实现的单件模式都是这样的。

#### 普通的单件模式

	package singleton

	import (
		"fmt"
	)

	var _self *Singleton

	type Singleton struct {
		Name string
	}

	func Instance() *Singleton {
		if _self == nil {
			_self = new(Singleton)
			return _self
		}
		return _self
	}

	func (o *Singleton) SetName(s string) {
		_self.Name = s
	}

	func (o *Singleton) GetName() {
		fmt.Println("Name:", _self.Name)
	}
	
支持并发的单件模式也不算难，在这个基础上增加一个叫做`Double Check`的处理。当年在去哪儿网面试被虐的时候被问到过这个，所以这个东西一直也都记着。

<ins class="adsbygoogle"
     style="display:block; text-align:center;"
     data-ad-layout="in-article"
     data-ad-format="fluid"
     data-ad-client="ca-pub-1651120361108148"
     data-ad-slot="4918476613"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>

单件模式在并发情况下，上面的代码就有问题了，有可能会被创建多次，上面的例子加个日志：

	var _self *Singleton

	type Singleton struct {
		Name string
	}

	func NewInstance(name string) *Singleton {
		fmt.Println("Create instance", name)
		time.Sleep(4 * time.Second)
		_self.Name = name
		return _self
	}

	func Instance(name string) *Singleton {
		if _self.Name == "" {
			return NewInstance(name)
		}
		return _self
	}

	func main() {
		_self = new(Singleton)
		go Instance("cyeam")
		go Instance("bryce")
		time.Sleep(10 * time.Second)
		fmt.Println(_self.Name)
	}

结果如下。例子里面给实例化函数加了参数，方便判断实例化的次数和结果。从下面的结果看来，无锁的单件模式创建过两次实例，第二次创建的实例覆盖了第一个创建的实例。

	Create instance cyeam
	Create instance bryce
	bryce
	
#### 支持并发的单件模式

为了保证在并行调用的情况下只创建一个实例，就需要加锁来保证串行创建。简单粗暴的方法就是`Instance()`方法直接全部上锁。

	var _self *Singleton

	type Singleton struct {
		Name string
		sync.Mutex
	}

	func NewInstance(name string) *Singleton {
		fmt.Println("Create instance", name)
		time.Sleep(4 * time.Second)
		_self.Name = name
		return _self
	}

	func Instance(name string) *Singleton {
		_self.Mutex.Lock()
		defer _self.Mutex.Unlock()
		if _self.Name == "" {
			return NewInstance(name)
		}
		return _self
	}

	func main() {
		_self = new(Singleton)
		_self.Mutex = sync.Mutex{}
		go Instance("cyeam")
		go Instance("bryce")
		time.Sleep(10 * time.Second)
		fmt.Println(_self.Name)
	}
	
简单粗暴的加锁，可以发现能够解决并发多次创建的问题。但是如此一来，整个创建流程就变成串行调用了。比如有1000次创建请求，只要创建一个实例就好，剩下999次完全没有必要加锁，直接将之前第一个创建的实例返回就好。而这样的写法会导致每一次都是带锁访问，影响速度。

	Create instance cyeam
	cyeam
	
接着上面的思路，我们可以不为这个函数整体加锁，在创建的时候加锁即可。

	func Instance(name string) *Singleton {
		if _self.Name == "" {
			_self.Mutex.Lock()
			defer _self.Mutex.Unlock()
			return NewInstance(name)
		}
		return _self
	}

在判断确认对象为空后，开始创建对象，结果如下：

	Create instance cyeam
	Create instance bryce
	bryce
	
虽然已经加上了锁，但是可以看到，依然创建了两次对象。如果两个并行的创建调用，此时`if _self.Name == ""`这个调用也同时执行，自然也都是`true`，接着，虽然有锁，但是也就是串行得去创建对象，外面的`if`在无锁的情况是失效了。

这时就需要牛逼的**Double Check**了，在锁里面再加一次判空检查。

	func Instance(name string) *Singleton {
		if _self.Name == "" {
			_self.Mutex.Lock()
			defer _self.Mutex.Unlock()
			if _self.Name == "" {
				return NewInstance(name)
			}
		}
		return _self
	}
	
结果如下。如此一来，既兼顾了效率，又能够很好的支持并发。

	Create instance cyeam
	cyeam
	
上面写的这些都是传统的写法，对于一般语言使用的，对于我大Golang，还有一个更简单的实现。

	import (
		"fmt"
		"sync"
		"time"
	)

	var _self *Singleton

	type Singleton struct {
		Name string
		sync.Once
	}

	func NewInstance(name string) *Singleton {
		fmt.Println("Create instance", name)
		time.Sleep(4 * time.Second)
		_self.Name = name
		return _self
	}

	func Instance(name string) *Singleton {
		if _self.Name == "" {
			_self.Once.Do(func() { NewInstance(name) })
		}
		return _self
	}

	func main() {
		_self = new(Singleton)
		_self.Once = sync.Once{}
		go Instance("cyeam")
		go Instance("bryce")
		time.Sleep(10 * time.Second)
		fmt.Println(_self.Name)
	}

本文所涉及到的完整源码请[参考](https://github.com/mnhkahn/go_code/tree/master/singleton)。

---

###### *参考文献*
1. [设计模式(2) - Singleton单件模式 - shltsh](http://blog.csdn.net/shltsh/article/details/17429363)

{% include JB/setup %}