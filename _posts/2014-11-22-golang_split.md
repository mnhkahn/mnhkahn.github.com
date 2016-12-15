---
layout: post
title: "Golang字符串切割函数Split"
description: "升级beego 1.4.2之后，根据发现的不兼容的地方顺藤摸瓜。"
category: "Golang"
tags: ["字符串"]
---

先说结论：大Golang里面，如果一个空字符串通过`strings`包的`Split`函数进行切割，那么结果是一个长度为1的数组，里面的内容是一个空字符串。

为了验证，分别在1.0.1、1.1、1.2.2、1.3.3、1.4rc上面进行了测试，验证了上面的结论是正确的。

	func main() {
		a := strings.Split("", ";")
		fmt.Printf("%d****%s****\n", len(a), a[0])
	}

这个也很好理解。切割一个空字符串，肯定是没办法切的，那么结果就是没切开，把原字符串直接加入结果数组里面而已。只不过一开始有点难理解，因为我们都会认为如果是空字符串去切，结果数组里应该是空的。

---

最近升级了beego1.4.2，谢大把beego控制器获取请求参数函数`Controller.GetInt`函数的返回值，由之前的`int64`改成了`int`，本来最早用的时候就别扭，如果想取到`int64`，那直接再加个函数`Controller.GetInt64`就可以了，结果这么一搞，还得自己惦记着。结果这次谢大果断把`Controller.GetInt`返回值改了，项目直接编译不过了。

当然，这不算什么，编译不过最起码知道问题出在哪里了。还有一个坑，`beego.AppConfig.Strings`函数，之前是可以将配置里的字符串通过分号自动切割成数组。结果更新之后，之前的代码返回是空的了（也就是里面是长度是1的空字符串）。这个可害苦了我。看了下源码，发现config包解析配置文件的方法进行了大幅度更新，但是我经过分析，认为并不是这里的错误，反而是另一个地方`beego/config.go`第111行

	func (b *beegoAppConfig) Strings(key string) []string {
		v := b.innerConfig.Strings(RunMode + "::" + key)
		if len(v) == 0 {
			return b.innerConfig.Strings(key)
		}
		return v
	}

从`runmode`里获取配置的值，如果没有取到，去取默认值。这里说一下，beego的配置文件支持`dev`、`prod`和`default`三种模式。如果配置了`runmode`，根据其在配置文件内查找相应的配置，否则去取默认值。上面的代码大体是这个含义。但是如果没有找到`runmode`下的配置，此时`if`的判断是`len(v) == 0`，而之前从配置文件的实现`ini.go`里取值的函数如下：

	func (c *IniConfigContainer) Strings(key string) []string {
		return strings.Split(c.String(key), ";")
	}

它会把取到的字符串进行切割，结合我们上面提到的，无论怎么切割，长度最少是1,所以`if`判断永远是`false`，取默认值的逻辑永远不会被执行。修改的方法也很简单，判断语言改成`if v[0] == ""`即可。完成的beego/config包介绍可以看我之前的[文章](http://blog.cyeam.com/beego/2014/11/12/beego_config)。我已经给谢大提了Merge Request，但是他一直没有理我。。。

---

24号谢大合并了我的代码，开心开心开心。


本文所涉及到的完整源码请[参考](https://github.com/mnhkahn/go_code/blob/master/test_split.go)。

---


{% include JB/setup %}
