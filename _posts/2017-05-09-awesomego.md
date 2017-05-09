---
layout: post
title: "Awesome Go"
description: "Go 相关推荐。都是亲测过的。"
category: "golang"
tags: ["awesome","golang","tool"]
---

* 目录
{:toc}

---

### Go 包

+ [beego](https://github.com/astaxie/beego)。算起来用了三年beego了。当初选择用它的理由很简单，文档是中文的，开发者是中国的，交流方便。优点就是用得人较多，框架集成度高，工具比较多。不过从1.6开始兼容性大大降低开始对它无感。现在越来越觉得beego框架设计的太重，Golang的设计特点就是轻便，把各个功能包组装起来用。比如配置它的config包，不用又不行，因为框架启动就会调用。最近大家都在推荐[gin](https://github.com/gin-gonic/gin)，有兴趣可以试试。

+ [beego/logs](https://github.com/astaxie/beego/tree/master/logs)。日志包一直在用beego内置的logs包。它有一个特点就是支持日志自动分割，可以按行数分割或者按日期分割。目前还没有发现支持此功能别的日志包，有的话大家给我推荐一下。

+ [beego/orm](https://github.com/astaxie/beego/tree/master/orm)。我的服务对数据库操作很少，orm只是简单用用。之前还用过[grop](https://github.com/go-gorp/gorp)和[xorm](https://github.com/go-xorm/xorm)。Golang主要是用来做接口，对于数据库操作都比较简单，orm高级操作基本用不到。所以对我来说这些orm功能都差不多。。。

+ [redigo](https://github.com/garyburd/redigo)。连Redis必备。功能很完善。

+ [goquery](https://github.com/PuerkitoBio/goquery)。用来解析HTML。开发爬虫都会用到它。

+ [goreq](https://github.com/franela/goreq)。一个HTTP请求包。之前会用它是因为它支持Gzip压缩。

+ [viper](https://github.com/spf13/viper)。一个配置包。支持解析各种格式的配置文件，最让我惊喜的是它支持etcd。

+ [gods](https://github.com/emirpasic/gods)。各种数据结构的Golang实现。这些代码生产环境没有直接用到过，不过自己写的时候可以借鉴一下。

+ [ffjson](https://github.com/pquerna/ffjson)。根据Golang的结构体自动生成`MarshalJSON`方法从而避免原生包通过反射编码引起的垃圾回收的问题。

+ [godep](https://github.com/tools/godep)。说实话Golang对包管理不太友好。有一个项目用了godep来做版本管理，每次都要执行好多命令真是麻烦。Golang新版内置包管理了，这个可以放弃使用了。

+ [bitset](https://github.com/willf/bitset)。这个包已经在生产环境使用了，它是Bitmap的Golang实现。底层用`uint64`切片保存数据。性能是内置`map`的40倍。

+ [jobrunner](https://github.com/bamzi/jobrunner)。一个Crontab包。beego内置的Crontab包之前有bug，只能找个新的。我关注这个的包的时候才100个Star，不过好在好用。

### Go 工具

+ [Cleaner Go](https://gsquire.github.io/static/post/cleaner-go/)。代码检测相关不错的文章。
	+ 静态代码检测 `staticcheck.exe $(glide.exe nv)`
	+ 无用代码检测 `unused.exe $(glide.exe nv)`
	+ 代码简化建议 `gosimple.exe $(glide.exe nv)`
	+ 原生检测 `go vet`
	
+ [gojson](https://github.com/ChimeraCoder/gojson)。一个工具，可以通过Json格式的文本生成Golang结构体代码。


---

会持续更新。


{% include JB/setup %}
