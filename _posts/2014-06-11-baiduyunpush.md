---
layout: post
title: "百度云推送"
figure: "http://cyeam.qiniudn.com/baiduyunpush.png"
description: "百度云推送的Go语言实现。Github 地址： https://github.com/mnhkahn/BaiduYunPush。"
category: "Golang"
tags: ["Golang", "android", "notification"]
---

<iframe src="http://ghbtns.com/github-btn.html?user=mnhkahn&repo=BaiduYunPush&type=watch&count=true&size=large"
  allowtransparency="true" frameborder="0" scrolling="0" width="170" height="30"></iframe>

<iframe src="http://ghbtns.com/github-btn.html?user=mnhkahn&repo=BaiduYunPush&type=fork&count=true&size=large"
  allowtransparency="true" frameborder="0" scrolling="0" width="170" height="30"></iframe>

<iframe src="http://ghbtns.com/github-btn.html?user=mnhkahn&type=follow&count=true&size=large"
  allowtransparency="true" frameborder="0" scrolling="0" width="185" height="30"></iframe>

百度云推送支持通知、消息和富媒体的发送。我只实现了最简单的群推送通知的功能。还有针对指定ID的发送，指定通知布局，指定打开网页等一系列设置都没有包含。接下来还要用到这个的时候再去进行开发好了。

关于Android端的推送，有Google的官方支持，但是大家懂得，只能另寻它法。Android不同于iOS，它运行程序在后台有常驻进程。所以就有了其它通知方法。这样就可以由后台进程获取到通知内容后自行展示。发送通知还能用IBM的MQTT，虽然我在他们部门实习过，但是这个东西不会用。。。还有自己实现HTTP长连接Keep-Alive，发送Request之后等待Response。这些都是目前常用的方法，我都不会。那么，我就去找了现成的百度云推送。

百度提供了两种实现方式：SDK和REST API。SDK包括了PHP、JAVA、Python、Node.js和C#这些语言。而我选择比较熟悉的Go语言开发REST接口发送。接口请参考百度提供的文档。

> http://developer.baidu.com/wiki/index.php?title=docs/cplat/push/api/list

发送消息需要验证用户身份，需要按照百度的规则将内容计算出的MD5码一并发送用于验证。先开始验证逻辑的时候，一直用的Javascript的encodeURI和网上找的MD532位加密算法验证，都不成功。十分受挫。后来去Github找了前辈OopsWare用Java写的SDK[BaiduPush-Server-SDK](https://github.com/OopsWare/BaiduPush-Server-SDK)。通过调试抓取它的sign码的计算结果，然后我再用Go照着结果去写。结果发现一下子就连上了，可能是我验证用的工具不对的原因把。。。愁

这个东西我原本是要在毕设当中使用的，毕设用了beego做服务器开发，这里也就一并用来开发了。等到答辩结束之后，争取能够开发出第一个Go语言实现的SDK。

> 百度提供的签名算法：http://developer.baidu.com/wiki/index.php?title=docs/cplat/push/api#.E7.AD.BE.E5.90.8D.E7.AE.97.E6.B3.95

Android客户端的开发可以直接参考百度提供的Demo和[Android开发文档](http://bs.baidu.com/push-sdk-release/Baidu-Push-SDK-Android-L2-4.0.0.zip)，照着样子挪到自己的项目里就可以了。

---

当时下载了百度提供的PushDemo，看到libs文件夹里的这三个文件夹，瞬间槽点满满。怪不得人们都说：“Android只是玩具，要开发应用，还得靠iOS”。Google管理下乱七八糟的硬件生态圈（包括软件也是。。。），通过NDK开发就要针对三个平台分别编译，如果是大型游戏，那么应用占用空间将会是iOS的三倍。除非你只想支持一种。而且其平台的混乱，还使得基于芯片的代码优化困难重重。这也就是为什么Android至今都没有大型应用的原因。

![IMG-THUMBNAIL](http://cyeam.qiniudn.com/android_tucao.png)

再加上最新得知Google香港也对中国进行了关键字屏蔽，曾经的好感又少了不少。。。每一个Android程序员开发过一阵程序之后，都会说要转iOS开发，我想说我也是这么想的。。。

{% include JB/setup %}
