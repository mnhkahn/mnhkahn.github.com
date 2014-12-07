---
layout: post
title: "百度云推送——Go语言实现类库"
figure: "http://blog.cyeam.com/assets/images/logo.jpg"
description: "把之前写好的百度云推送封装成了Go包。只是实现了最简单的消息推送。。"
category: "golang"
tags: ["Golang", "android", "notification"]
---

<iframe src="http://ghbtns.com/github-btn.html?user=mnhkahn&repo=BaiduYunPush&type=watch&count=true&size=large"
  allowtransparency="true" frameborder="0" scrolling="0" width="170" height="30"></iframe>

<iframe src="http://ghbtns.com/github-btn.html?user=mnhkahn&repo=BaiduYunPush&type=fork&count=true&size=large"
  allowtransparency="true" frameborder="0" scrolling="0" width="170" height="30"></iframe>

<iframe src="http://ghbtns.com/github-btn.html?user=mnhkahn&type=follow&count=true&size=large"
  allowtransparency="true" frameborder="0" scrolling="0" width="185" height="30"></iframe>

#快速开始

###下载安装

    go get github.com/mnhkahn/BaiduYunPush

###创建文件pushtest.go

    package main

    import (
        "fmt"
        "github.com/mnhkahn/BaiduYunPush"
    )

    var apikey = "**************************"
    var seckey = "******************************"
    var method = "POST"
    var url_base1 = "channel.api.duapp.com/rest/2.0/channel/channel"

    func main() {
        push := BaiduYunPush.New(apikey, seckey)
        s, err := push.Push("推送成功", "这是我的个人博客blog.cyeam.com")
        fmt.Println(s, err)
    }


###编译运行

    go run pushtest.go

当控制台显示`true`之后，推送成功。这时，通过SDK绑定的设备就会展示推送消息。

![IMG-THUMBNAIL](http://cyeam.qiniudn.com/baiduyunpush.jpg)

---

######*参考文献*
+ 【1】[百度开放云文档](http://developer.baidu.com/wiki/index.php?title=docs/cplat/push/api/list)

{% include JB/setup %}
