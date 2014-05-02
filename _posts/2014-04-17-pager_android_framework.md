---
layout: post
title: "基于流媒体的对讲机系统——Android的开发准备"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: ""
category: "Postgraduate design"
tags: ["Postgraduate design", Paper"]
---

本课题中需要在后台进行呼叫请求和音视频传输操作，Android平台提供了Service组建，在后台实现该功能。

Service运行于后台，没有任何用户界面。它们可以于Activity执行相同的操作。

特别说明一下，Android中的Service是指在后台运行的程序，与Acitivity的区别是没有界面而已。它依然是在主线程中，并不是新创建的子线程，虽然看上去很像。一般的策略是在Service启动之后，为其单独创建一个子线程。

在Android 3.0之后，考虑到网络访问影响用户交互，Android禁止在主线程中进行网络访问。如果要实现此功能，就要像前面说的创建子线程在子线程中实现。

本课题中还需要一个控制模块来订阅观察系统状态以及及时的对其作出响应。例如，对于SIP注册状态要及时响应，如果注册失败，要及时通知用户，增加系统的友好性和不必要的时间浪费。

Android平台提供了Broadcast Receiver。Broadcast Receiver是Android在系统级别对Observer模式(Pub-Sub)的实现。接收器一直等待，直到其订阅的事件发生时，才被激活。

Android平台还提供了更加友好的Notification来增加和用户的交互。这个部分将在后面进行详细介绍。

{% include JB/setup %}