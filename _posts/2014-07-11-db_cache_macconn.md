---
layout: post
title: "数据库访问的缓存与最大连接数"
description: "之前有人提点，现在自己写，就忘记加了。弱爆了。。。"
category: "golang"
tags: ["Golang", "hole", "MySQL Cache", "MySQL Max Conn", "xorm"]
---

今天查看我写的错误日志，里面报出了`Too many connections`这个错误。没见过啊，果断去问我大哥，他说是连接数的问题。我又去看之前已经上线的我的代码，才想起来数据库连接需要设置最大连接数的。当连接数超过范围之后，就是报这个错误。

我用的是xorm作为ORM工具，直接使用`engine.SetMaxConns(dbMaxConns)`就能设置最大连接数。

后来，又优化了一下缓存。一般ORM还是支持缓存机制的。如果缓存命中，就不会去数据库查找数据了，而是会直接返回。添加缓存需要增加缓存时间和最大缓存数。

	cacher := xorm.NewLRUCacher2(xorm.NewMemoryStore(), time.Duration(interval)*time.Second, max)
	engine.SetDefaultCacher(cacher)

很简单的问题，但是老是忘记加。今天用`wrk`对项目做了简单的压力测试，就出了这个问题。以前一直觉得压力测试就是用来测性能的，今天有了新的认识。


{% include JB/setup %}
