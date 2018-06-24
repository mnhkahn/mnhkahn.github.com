---
layout: post
title: "如何离线完成go get——安装Apache Thrift有感"
figure: "http://thrift.apache.org/static/images/favicon.ico"
description: "由于一些原因（你懂的），如果golang代码存放在Google Code上面，想通过go get下载编译就是在骗自己。今天就通过一些方法解决了。做天朝的程序员不易，且行且珍惜吧。"
category: "Kaleidoscope"
tags: ["GFW", "Golang"]
---

今天公司事情不多，我手上的项目还需要等其他同事才能继续，有一段时间比较闲。之前有3个月不在公司回学校了，我们部门用了一个新的开发工具——Apache Thrift，就趁这个时间了解一下。

准备把Thrift安装到阿里云上面。这个东西大概了解了一下，是Facebook开源的一套远程调用的框架，比目前流行的基于REST传输JSON性能好，更优于基于SOAP的XML。关键是它支持多种语言，当然包括我们Team使用的Golang。

从官网下载压缩包安装有问题，没有官网上面描述的`bootstrap.sh`文件，还会会报错误。

	libtool: link: ar cru .libs/libtestgencpp.a .libs/ThriftTest_constants.o   
	.libs/ThriftTest_types.o  
	ar: .libs/ThriftTest_constants.o: No such file or directory  

在Ubuntu安装需要安装依赖。后来观察安装输出，发现还需要Ant和Maven。

	sudo apt-get install libboost-dev libboost-test-dev libboost-program-options-dev libevent-dev automake libtool flex bison pkg-config g++ libssl-dev

Thrift会自动检查当前机子的环境变量里面存在的开发语言进行编译。它帮我自动支持了Java、Python和Golang。

重点来了。在安装Golang的时候，出错了，日志说`go get code.google.com/p/gomock/gomock`连接超时。以我多年的经验来看，被拦截了。我在本机遇到这种情况的时候，都是使用Goagent，直接`export http_proxy="http://127.0.0.1:8087`和`export https_proxy="http://127.0.0.1:8087`就设置好代理了。但是这次是阿里云，那边没办法代理。后来在本机试了试，能够下载。看来GFW是分区域拦的。通过FTP上传到`gopath`目录下，进入该目录，通过`go install`进行编译即可。可以再输入`go get code.google.com/p/gomock/gomock`，检测是否安装成功。

准备下个月发工资之后咬咬牙去买Linode的$10的业务，希望今后能愉快的上网。

---

###### *参考文献*
+ 【1】[脆弱的Go远程包 - qinhui99](http://my.oschina.net/qinhui99/blog/66560)
+ 【2】[ubuntu 12.04中安装thrift-0.9.1 - iAm333的专栏](http://blog.csdn.net/iam333/article/details/18771945)
+ 【3】[Debian or Ubuntu setup](http://thrift.apache.org/docs/install/debian)

{% include JB/setup %}
