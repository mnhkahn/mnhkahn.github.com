---
layout: post
title: "基于流媒体的对讲机系统——系统总体设计"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: ""
category: "Postgraduate design"
tags: ["Postgraduate design", Paper"]
---

![IMG-THUMBNAIL](http://cyeam.qiniudn.com/framework.png)

+ 系统从cInterphone这个Activity启动。该Activity包含3个Fragment，分别是Favourite Fragment、History Fragment、Contact Fragment。
+ 其中，Favourite Fragment和History Fragment关联到两个SQLite数据库表Favourite和History。使用适配器ContactAdapter进行数据关联显示。
+ cInterphone的ActionBar上面，还增加了设置模块按钮，可以启动Settings这个Activity，用于进行手动配置用户名和SIP服务器。
+ Recevier继承自BroadcastReceiver，使用单件模式和观察者模式，用于获取cInterphoneEngine的单件实例和响应状态，例如：进入视频界面，通知栏更改状态等等。
+ cInterphoneEngine模块负责SIP协议栈的封装，用于注册SIP服务器、发起会话、结束会话等会话控制操作。
+ 在准备建立会话时，Receiver会启动InCallScreen，用于显示呼叫或者被呼叫界面。会话建立成功后，启动VideoCamera Activity进行视频通话。
+ VideoCamera Activity会启动RtspServer Service用于发送音视频RTSP流。并且使用MediaPlayer读取RSTP流。

{% include JB/setup %}