---
layout: post
title: "beego/config包源码分析"
description: "基于beego 1.4.2版本。"
category: "beego"
tags: ["beego"]
---

从去年12月底开始接触golang，用过revel和beego框架。最后选择了beego，用beego的原因也很简单，因为beego是中国人开发的，有中文文档。

golang起源于C语言，虽然不支持面向对象编程，但还是提供了接口interface、匿名字段等方式。虽然进行面向对象编程还是有点别扭，但是好歹都能实现。这里借花献佛，介绍一下beego的config包，顺便提一下golang的面向对象编程。

config包的`config.go`文件定义了两个接口，`ConfigContainer`和`Config`，ConfigContainer定义了如何从原始数据里面获取配置信息的方法。Config接口是一个适配器，定义了把原始数据解析到ConfigContainer的方法。

config包里的其它文件是这两个接口的实现。xml文件夹实现了解析XML数据格式的方法，yaml文件夹实现了解析YAML格式的方法，ini和json分别解析INI格式和JSON格式。这里主要说一下INI格式的实现。

`ini.go`文件定义了两个结构体`IniConfigContainer`和`IniConfig`，分别实现了上面的两个接口。golang接口的实现语法可以参考之前的文章[《Golang 接口实现》](http://blog.cyeam.com/golang/2014/07/20/go_inte/)。其中，IniConfigContainer不光实现了接口，还定义了内部变量来辅助实现。

	filename       string
	data           map[string]map[string]string // section=> key:val
	sectionComment map[string]string            // section : comment
	keyComment     map[string]string            // id: []{comment, key...}; id 1 is for main comment.
	sync.RWMutex

`data`是用map实现的，用来保存配置文件的键值对。IniConfigContainer还有一个匿名对象`sync.RWMutex`，这是golang继承的语法，说明IniConfigContainer继承了同步锁，在这里用于互斥修改配置文件的值。config包和INI格式的实现可以参考下图。

![IMG-THUMBNAIL](https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeam/beego_config.png)

---


{% include JB/setup %}