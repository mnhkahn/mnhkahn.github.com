---
layout: post
title: "基于流媒体的对讲机系统——Android的开发准备"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeam/c168.png"
description: ""
category: "Postgraduate"
tags: ["Postgraduate design", "Paper"]
---

根据系统的大体设计并结合Android自身特性，将会主要用到下列几个Android自身控件。下面做简单介绍：

+ 用户交互界面由Activity实现，对该部分的详细介绍，请参考[5.1节](https://blog.cyeam.com/postgraduate/2014/04/18/pager_listfragment)。
+ 系统主要模块都是在后台自动调用并执行的，这样能简化系统设计并提高系统运行速度。Android平台提供了Service组件，支持在后台自动启动和停止，系统的音视频通话模块、SIP模块都可以直接基于Service实现。。

    Service运行于后台，没有任何用户界面。它们可以于Activity执行相同的操作。
    特别说明一下，Android中的Service是指在后台运行的程序，与Acitivity的区别是没有界面而已。它依然是在主线程中，并不是新创建的子线程，虽然看上去很像。一般的策略是在Service启动之后，为其单独创建一个子线程。

    在Android 3.0之后，考虑到网络访问影响用户交互，Android禁止在主线程中进行网络访问。如果要实现此功能，就要像前面说的创建子线程在子线程中实现。

+ 为了将系统设计成高内聚，低耦合，将各个模块进行了封装。用户交互界面和后台通信逻辑等模块进行了分离。这几个模块消息的传输，就要通过一个控制模块来订阅观察系统状态以及及时的对其作出响应。例如，对于SIP注册状态要及时响应，如果注册失败，要及时通知用户，增加系统的友好性和不必要的时间浪费。

    Android平台提供了Broadcast Receiver。Broadcast Receiver是Android在系统级别对Observer模式(Pub-Sub)的实现。接收器一直等待，直到其订阅的事件发生时，才被激活。系统的核心引擎使用了该设计模式。

+ Android平台还提供了更加友好的Notification来增加和用户的交互。这个部分将在[5.3.2节](https://blog.cyeam.com/postgraduate/2014/04/18/pager_notification)进行详细介绍。

{% include JB/setup %}
