---
layout: post
title: "如何离线完成go get——安装Apache Thrift有感"
figure: "https://thrift.apache.org/static/images/favicon.ico"
description: "由于一些原因（你懂的），如果golang代码存放在Google Code上面，想通过go get下载编译就是在骗自己。今天就通过一些方法解决了。做天朝的程序员不易，且行且珍惜吧。"
category: "Kaleidoscope"
tags: ["GFW", "Golang"]
---

今天公司事情不多，我手上的项目还需要等其他同事才能继续，有一段时间比较闲。之前有 3 个月不在公司回学校了，我们部门用了一个新的开发工具——Apache Thrift，就趁这个时间了解一下。

准备把 Thrift 安装到阿里云上面。这个东西大概了解了一下，是 Facebook 开源的一套远程调用的框架，比目前流行的基于 REST 传输 JSON 性能好，更优于基于 SOAP 的 XML。关键是它支持多种语言，当然包括我们 Team 使用的 Golang。

从官网下载压缩包安装有问题，没有官网上面描述的`bootstrap.sh`文件，还会会报错误。

    libtool: link: ar cru .libs/libtestgencpp.a .libs/ThriftTest_constants.o
    .libs/ThriftTest_types.o
    ar: .libs/ThriftTest_constants.o: No such file or directory

在 Ubuntu 安装需要安装依赖。后来观察安装输出，发现还需要 Ant 和 Maven。

    sudo apt-get install libboost-dev libboost-test-dev libboost-program-options-dev libevent-dev automake libtool flex bison pkg-config g++ libssl-dev

Thrift 会自动检查当前机子的环境变量里面存在的开发语言进行编译。它帮我自动支持了 Java、Python 和 Golang。

重点来了。在安装 Golang 的时候，出错了，日志说`go get code.google.com/p/gomock/gomock`连接超时。以我多年的经验来看，被拦截了。我在本机遇到这种情况的时候，都是使用 Goagent，直接`export http_proxy="http://127.0.0.1:8087`和`export https_proxy="http://127.0.0.1:8087`就设置好代理了。但是这次是阿里云，那边没办法代理。后来在本机试了试，能够下载。看来 GFW 是分区域拦的。通过 FTP 上传到`gopath`目录下，进入该目录，通过`go install`进行编译即可。可以再输入`go get code.google.com/p/gomock/gomock`，检测是否安装成功。

准备下个月发工资之后咬咬牙去买 Linode 的$10 的业务，希望今后能愉快的上网。

---

###### _参考文献_

-   【1】[脆弱的 Go 远程包 - qinhui99](http://my.oschina.net/qinhui99/blog/66560)
-   【2】[ubuntu 12.04 中安装 thrift-0.9.1 - iAm333 的专栏](http://blog.csdn.net/iam333/article/details/18771945)
-   【3】[Debian or Ubuntu setup](http://thrift.apache.org/docs/install/debian)

{% include JB/setup %}
