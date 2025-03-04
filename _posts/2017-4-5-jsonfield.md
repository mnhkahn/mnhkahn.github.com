---
layout: post
title: "jsonfield——动态输出 Json 内容"
description: "算是一个工具类包，不追求性能调试的时候会比较爽，推荐给大家。"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeam/logo-json.png"
category: "golang"
tags: ["tool"]
---

* 目录
{:toc}

---

<iframe src="http://ghbtns.com/github-btn.html?user=mnhkahn&repo=jsonfield&type=watch&count=true&size=large"
  allowtransparency="true" frameborder="0" scrolling="0" width="170" height="30"></iframe>

<iframe src="http://ghbtns.com/github-btn.html?user=mnhkahn&repo=jsonfield&type=fork&count=true&size=large"
  allowtransparency="true" frameborder="0" scrolling="0" width="170" height="30"></iframe>

<iframe src="http://ghbtns.com/github-btn.html?user=mnhkahn&type=follow&count=true&size=large"
  allowtransparency="true" frameborder="0" scrolling="0" width="185" height="30"></iframe>


### jsonfield

它能够动态输出指定字段，开发简单。我将它用于通过接口调试数据时使用。

### 安装

	go get -v github.com/mnhkahn/jsonfield
	
### 使用

	type A struct {
		A int
		B int
	}

	jj := new(A)
	jj.A, jj.B = 111, 222
	
	byts, err := Marshal(jj) // {"A":111,"B":222}
	
	byts, err := Marshal(jj, "A") // {"A":111}
	
	byts, err := Marshal(jj, "B") // {"B":222}
	
### 反馈

如果有疑问或者建议，可以通过微信联系我或者在 Github 里面提 [Issue](https://github.com/mnhkahn/jsonfield/issues)。




---

{% include JB/setup %}
