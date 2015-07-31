---
layout: post
title: "Thrift数据传输序列化"
description: "有时间写博客，不光是因为有时间，还因为出过线上bug。不懂序列化的我们，必须记录一下。"
category: "Thrift"
tags: ["Golang", "Thrift"]
---
 
Thrift的序列化是比Json更好用的结构（具体哪里好了我还没研究）。但是它有一个非常严重的问题：兼容性差。常年使用Json的我们已经被惯坏了，潜意识里就觉得数据默认是能保持兼容的。

先说一下那个线上问题。我与公司其它部门用Thrift对接，先上了一版，我是调用方。接着，二次升级的时候，合作的部门改了一下Idl，在函数返回结果结构体的最前面，插入了一个结构，是一个结构体，原本第一版第一个位置是整形。然后他们上线了，我还在排队上线。突然监控就报我接口返回了404(一般错误都转成404)。然后去排查，发现返回了一堆负数，负数导致后面的逻辑出问题了，哪怕返回了整数，也是非常不正常。

这个关键的时刻，我们组长（永远是他）给解释了bug的原因，是Thrift不兼容导致的。

	struct Pair {
		1: required string key
		2: required string value
	}

上面这个结构体，如果解析成Json，是按照键值对的形式展示，字段变量的名称是有意义的。而在Thrift里面，依然是键值对的形式，但是没有用变量名的名字作为键，而是通过***序号和类型***作为键，序号决定位置，类型决定解析方式。

> Versioning in Thrift is implemented via ﬁeld identiﬁers. The ﬁeld header for every member of a struct in Thrift is encoded with a unique ﬁeld identiﬁer. The combination of this ﬁeld identiﬁer and its type speciﬁer is used to uniquely identify the ﬁeld. The Thrift deﬁnition language supports automatic assignment of ﬁeld identiﬁers, but it is good programming practice to always explicitly specify ﬁeld identiﬁers.

之前写过一篇[《Golang开发Thrift接口》](http://blog.cyeam.com/golang/2014/07/22/go_thrift/)，这次接着以这个为基础修改进行实验。新增一个测试函数，返回我们要实验的这个结构体。

	Pair helloPair()

通过Idl生成Golang包：

	thrift -v --gen go:package_prefix=go_code/test_thrift Hello1.thrift

在`helloimpl.go`实现这个新增的方法：

	func (h *HelloHandler) HelloPair() (*hello.Pair, error) {
		p := new(hello.Pair)
		p.Key = "rowkey"
		p.Value = "column-family"
		return p, nil
	}

启动服务端：

	go run helloserver.go helloimpl.go

在`helloclient.go`增加调用：

	res, err := client.HelloPair()
	fmt.Println(res.String())

结果如下：

	$ go run helloclient.go
	Pair({Key:rowkey Value:column-family})

结果正确，下面来模拟错误的情况。这个模拟很简单，修改Idl顺序：

	struct Pair {
		2: required string key
		1: required string value
	}

重新生成一遍Idl，为了对比，我把这个Idl命名为`Hello1.thrift`。然后复制原文件并重命名为`helloimpl1.go`和`helloserver1.go`。把引用的包名改成`hello "go_code/test_thrift/hello1"`。再启动服务端：

	hello "go_code/test_thrift/hello1"

客户端不做任何修改：

	$ go run helloclient.go
	Pair({Key:column-family Value:rowkey})

结果正好相反，Amazing有没有。。。

本文所涉及到的完整源码请[参考](https://github.com/mnhkahn/go_code/tree/master/test_thrift)。

---

######*参考文献*
1. [Thrift 个人实战--Thrift 的序列化机制 - mumuxinfei](http://www.cnblogs.com/mumuxinfei/p/3876075.html)

{% include JB/setup %}