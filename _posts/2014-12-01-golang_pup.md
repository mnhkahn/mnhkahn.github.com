---
layout: post
title: "Golang通过pup实现HTML解析"
description: "在GitHub上面找了一个能解析HTML的包。"
category: "web"
tags: ["Golang"]
---
 
上一周给我的网站加了一个搜索功能，能自动抓取我的博客和别人的CSDN博客。通过RSS抓取。这样数据格式规范，容易解析。问题是信息较少。后来发现在HTML源代码里面，会有为了方便搜索引擎索引的`meta`字段，能指出作者和详情。以我的博客[《Golang实现HTTP发送gzip请求》](http://blog.cyeam.com/golang/2014/11/29/golang_gzip/)为例。里面的`meta`信息如下：

	<meta charset="utf-8">
	<meta name="description" content="beego的httplib不支持发送gzip请求，自己研究了一下。">
	<meta name="author" content="Bryce">
	<meta name="google-translate-customization" content="a4136e955b3e09f2-45a74b56dc13e741-gf616ffda6e6360e0-11">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">

查了查，一般大家通过`xpath`进行解析。有一个现成的包`https://github.com/go-xmlpath/xmlpath`，按照说明做了一下，不行。看了一下源码，这个包内部是通过`encoding/xml`实现的，如果HTML的代码有问题，标签不是严格按照规范编写的，就会有解析问题。同理，如果把HTML当作XHTML处理，也是不行的。

后来发现一个神奇的工具`https://github.com/EricChiang/pup`，通过命令`go get github.com/ericchiang/pup`安装。它可以通过管道调用：

	curl -s http://blog.cyeam.com | pup 'div div div div h2 a' 

直接抓取作者和简介可以用如下命令：

	curl -s http://blog.cyeam.com/golang/2014/11/29/golang_gzip/ | pup 'head meta[name="author"] attr{content}'
	curl -s http://blog.cyeam.com/golang/2014/11/29/golang_gzip/ | pup 'head meta[name="description"] attr{content}' 

这个包能完美解决我的问题，进去看了一下源码，发现包名是`main`，再一个是因为它用来解析HTML不是那么方便，想了想，我囧的还是用`cmd`的方式通过管道执行。

	req := httplib.Get("http://blog.cyeam.com/golang/2014/11/29/golang_gzip/")
	res, err := req.Bytes()
	if err != nil {
		panic(err)
	}

	cmd := exec.Command("pup", `head meta`)
	stdin, err := cmd.StdinPipe()
	if err != nil {
		panic(err)
	}
	// defer stdin.Close()
	var output bytes.Buffer
	cmd.Stdout = &output

	if err = cmd.Start(); err != nil { //Use start, not run
		fmt.Println("An error occured: ", err) //replace with logger, or anything you want
	}
	stdin.Write(res)
	stdin.Close()

	if err := cmd.Wait(); err != nil {
		panic(err)
	}
	fmt.Println(string(output.Bytes())) //for debug

通过`shell`命令行管道是通过`|`实现，而通过Golang代码，需要通过`exec`包提供的`Stdin`实现。把内容写入标准输入流，就相当于管道输入了。写完了要关闭输入流`stdin.Close()`，如果不关闭，输入流不会被写入。。。
 
本文所涉及到的完整源码请[参考](https://github.com/mnhkahn/go_code/blob/master/test_pup.go)。
 
---

######*参考文献*
+ 【1】[Package exec - The Go Programming Language](http://golang.org/pkg/os/exec/)
+ 【2】[golang讲解（go语言）标准库分析之os/exec - widuu](http://www.widuu.com/archives/01/927.html)
 
{% include JB/setup %}