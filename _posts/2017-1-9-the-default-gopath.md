---
layout: post
title: "【译】GOPATH的默认值"
description: "翻译自Go语言作者的博客。这只是设置了GOPATH默认值，GOROOT还是得自己设置。"
category: "Golang"
tags: ["Golang"]
---

从Go 1.8开始，如果GOPATH的环境变量为空，Go将会设置一个默认的GOPATH环境变量。

Go初学者第一次安装完Go之后，他们往往会因为忘记设置GOPATH环境变量而得到*you have to set a GOPATH*这样的错误。这个需求的优先级逐渐变高。对于Go的新用户来说，解释GOPATH的作用、指导他们如何设置GOPATH将会使它们不能专注使用Go。尤其是有些时候，这些人并不是要去使用Go语言去开发，而是使用`go get`去下载一些必要的命令。

Go 1.8将会设置[默认的GOPATH](https://github.com/golang/go/issues/17262)。如果你自己没有设置GOPATH，Go将会使用默认值。默认GOPATH是：

<ins class="adsbygoogle"
     style="display:block; text-align:center;"
     data-ad-layout="in-article"
     data-ad-format="fluid"
     data-ad-client="ca-pub-1651120361108148"
     data-ad-slot="4918476613"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>

+ 在Unix-like系统上是在`$HOME/go`目录下
+ 在Windows系统下是`%USERPROFILE%\go`

虽然已经有了默认的GOPATH，但是它并不能解决所有问题：

+ 我们还是得自己把`$GOPATH/bin`添加到`PATH`里面，这样通过`go get`和go install`安装的二进制程序才能够被直接运行。（译者注：当然，通过绝对路径运行这些程序也是可以的，只不过比较麻烦）。
+ Go语言的开发者依然需要了解GOPATH的作用和它的目录结构。
+ 如果你的`GOROOT`路径（就是你让Go源码的位置）和默认的GOPATH是一样的，并且你并没有设置一个默认的GOPATH，Go也并不为为你设置默认GOPATH，因为这样会把GOROOT里面的内容搞乱。

当你有疑问的时候，可以运行命令`go env GOPATH`来检查GOPATH的路径。如果有问题，比如上面说的情况，Go并没有自动生成GOPATH，这个命令将会打印空。

阅读原文[The default GOPATH](https://rakyll.org/default-gopath/)

---



---

{% include JB/setup %}
