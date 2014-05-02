---
layout: post
title: "基于流媒体的对讲机系统——核心引擎"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: ""
category: "Postgraduate design"
tags: ["Postgraduate design", Paper"]
---

本课题是一个庞大的系统，所以需要将各个子模块进行整合，使其能协同完成任务。

+ cInterphoneEngine 主要负责调用SIP协议栈，提供注册、注销、发起会话请求、接受/拒绝/结束会话的流程，控制SIP通信的流程。
+ Receiver 对于系统不同的状态进行响应。可以给予用于以更好的体验。系统进入不同的状态，会有不同的响应模式，例如通知栏和不同的响应界面。
+ InCallScreen 控制着SIP会话过程中的界面展示。SIP会话请求、被请求和接通后的界面流程展示。

广播是一种Android提供的系统级别的进程间通信功能，使用的是观察者设计模式。广播事件的接收要通过提前注册好的广播接收器和广播过滤器实现。

![IMG-THUMBNAIL](http://cyeam.qiniudn.com/receiver.png)

本系统在会话部分又分成接收端和发送端两个字模块。发送端要分别对语音和视频进行录制，将其解析成RTP包，然后建立RTSP服务器，通过RTSP进行发送。接收端反过来即可。

![IMG-THUMBNAIL](http://cyeam.qiniudn.com/%E6%B5%81%E7%A8%8B%E5%9B%BE.png)

收藏的联系人和最近通话记录使用SQLite保存在本地，方便查找和使用。

![IMG-THUMBNAIL](http://cyeam.qiniudn.com/service_framework.png)


{% include JB/setup %}