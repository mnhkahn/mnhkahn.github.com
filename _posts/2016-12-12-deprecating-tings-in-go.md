---
layout: post
title: "【译】Golang中使用『弃用(Deprecate)』"
description: "rakyll是一位Golang语言开发工程师。这哥们长得很秀气（有可能人家是姑娘），博客更是犀利。"
category: "golang"
tags: ["Golang","tool"]
---

Go语言很长时间都没有一套标记弃用API的定义规范。这几年，出现了个规范可以在文档当中添加弃用注释。

现在，标准库开始使用这个格式了。

举个例子，Go 1.8的包中`sql/driver.Execer`被弃用，这里增加了一套注释，它可以被`godoc`识别。

	// Execer is an optional interface that may be implemented by a Conn.
	//
	// If a Conn does not implement Execer, the sql package's DB.Exec will
	// first prepare a query, execute the statement, and then close the
	// statement.
	//
	// Exec may return ErrSkip.
	//
	// Deprecated: Drivers should implement ExecerContext instead (or additionally).
	type Execer interface {
		Exec(query string, args []Value) (Result, error)
	}

弃用的通知会出现在godoc里面，注释需要以`Deprecated`开头，后面再写上代替此API的提示。

	// Deprecated: Use strings.HasPrefix instead.

使用API的用户就可以根据这个提示使用新的API了。

Additional to the notices, there is an effort going on to discourage users to keep depending on the deprecated APIs.
除了注释通知之外，还可以有一些方法来阻止用户一直使用被弃用的API。

可以参考下面的文章:

+ [《默认隐藏弃用API的方法》](https://github.com/golang/go/issues/17056)
+ [《在godoc.org上面隐藏弃用的API》](https://github.com/golang/gddo/issues/456)
+ [《通过golint通知弃用的API》](https://github.com/golang/lint/issues/238)

总之，可以使用这个注释格式来支持弃用通知。不要用`DEPRECATED`或者`This type is deprecated`。将来，你可以用一些工具来通知用户停止使用弃用的API。

阅读原文[Deprecating things in Go](http://golang.rakyll.org/deprecated/)

---



---

{% include JB/setup %}
