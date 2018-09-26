---
layout: post
title: "介绍一下Json的Number(二)"
description: "单独介绍一下 json 包的 Number 类型。"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeamjson160.gif"
category: "Golang"
tags: ["Golang","json"]
---

* 目录
{:toc}
---

### 如何将JSON中的数字和字符串都解析为数字？

接着[《介绍一下Json的Number》
](http://blog.cyeam.com/golang/2016/05/02/jsonnumber)继续写，可以两篇文章一起读。

有一些情况下，JSON 解码需要适配多种类型，比如一串数字会被存成整数或者字符串两种格式，类型是不确定的，这个时候如何解析？

通用一点的方法我们可以自定义类型，自己实现`MarshalJSON`方法来实现负责逻辑的解析，具体方法可以参考[《Golang——json数据处理》](http://blog.cyeam.com/json/2014/08/04/go_json)，但是对于数字，就不用这么复杂了，Go 已经提供了一`Number`来帮助我们。

```
var raw = []byte(`{"a":1}`)
var raw_string = []byte(`{"a":"2"}`)
```

定义了两个 JSON 串，一个是整形，一个是字符串。如何将这两个数据解析到同一种类型中呢？

```
type S3 struct {
	A json.Number `json:"a"`
}

s3 := new(S3)
err = json.Unmarshal(raw, s3)
log.Println(err, s3.A)

s31 := new(S3)
err = json.Unmarshal(raw_string, s31)
log.Println(err, s31.A)
```

将对象`a`的类型定义成`json.Number`就可以实现对两种数据类型的解析。

### 原理

我们知道，解析 JSON 的时候其实是对 JSON 串的遍历，其实所有遍历出来的值都是`[]byte`类型，然后根据识别目标解析对象字段类型，或者识别`[]byte`数据的内容转换格式。比如，如果数据被解析到`int`上，把`[]byte`转换为`int`；如果被解析到`interface{}`上，就只能通过`[]byte`的类型来转换了，数字会被统一处理能`float64`，这个有个问题，就是会丢精度。而通过`Number`解析时，值会被直接保存为字符串类型。

```
// A Number represents a JSON number literal.
type Number string

// String returns the literal text of the number.
func (n Number) String() string { return string(n) }

// Float64 returns the number as a float64.
func (n Number) Float64() (float64, error) {
	return strconv.ParseFloat(string(n), 64)
}

// Int64 returns the number as an int64.
func (n Number) Int64() (int64, error) {
	return strconv.ParseInt(string(n), 10, 64)
}
```

使用`Int64`还是`float64`就可以通过用户自己的情况选择了。

本文涉及的代码可以从[这里](https://github.com/mnhkahn/go_code/blob/master/jsonnumber/main.go)下载。

### UseNumber

有时候我们想偷懒，并不想自己定义结构体，还是想使用`map[string]interface{}`来解析 JSON，可以使用`UseNumber`方法：

```
decoder := json.NewDecoder(bytes.NewBufferString(`{"10000000000":10000000000,"111":1}`))
decoder.UseNumber()
var obj map[string]interface{}
decoder1.Decode(&obj)
```

---





{% include JB/setup %}
