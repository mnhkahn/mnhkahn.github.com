---
layout: post
title: "安全URL的Base64编码"
description: "今天又见识了一种新的Base64编码方式。"
category: "web"
tags: ["Golang", "Base64"]
---
 
之前在[《网址压缩的调研分析（续）》](http://blog.cyeam.com/web/2014/07/25/short_url2/)介绍过Base62算法，他是一种类似于Base64的哈希算法。今天发现了另一种优化的Base64算法，又参考了下Golang的源码，在`encoding/base64/base64.go`里面。

	const encodeStd = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

传统的Base64用的是A-Z、a-z、0-9，还有+和/，一个64个编码串。

> 然而，标准的Base64并不适合直接放在URL里传输，因为URL编码器会把标准Base64中的“/”和“+”字符变为形如“%XX”的形式，而这些“%”号在存入数据库时还需要再进行转换，因为ANSI SQL中已将“%”号用作通配符。

> 为解决此问题，可采用一种用于URL的改进Base64编码，它不在末尾填充'='号，并将标准Base64中的“+”和“/”分别改成了“-”和“_”，这样就免去了在URL编解码和数据库存储时所要作的转换，避免了编码信息长度在此过程中的增加，并统一了数据库、表单等处对象标识符的格式。

base64.go文件里还定义了专用于URL里传输的URL安全的Base64算法。

	const encodeURL = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"

把之前的加号换成了减号，斜线换成了下划线。

---

就是因为这个原因，我发现我的一个编码结果和应该得到的只相差一位，一个是加号，一个是减号。因为如果是编码串不同的原因，哪怕就是差一位，结果也是完全不同的，差一位肯定不是因为这个。原来是这样，懂得还是太少了。。。

---

###### *参考文献*
+ [Base64 - 维基百科](http://zh.wikipedia.org/wiki/Base64)

 
{% include JB/setup %}