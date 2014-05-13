---
layout: post
title: "基于流媒体的对讲机系统——功能测试"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: ""
category: "Postgraduate design"
tags: ["Postgraduate design", Paper"]
---

功能测试是对系统设计和实现进行的验证测试，查看系统是否满足需求和设计。这里主要是针对SIP注册、SIP呼叫、音视频通话、系统抢占式通话、系统协作模块进行测试。

+ 对讲机SIP注册、SIP呼叫、SIP结束等流程。使用了PC端的linphone和Android端的linphone和本系统都进行了测试，SIP流程兼容性好，没有出现不同设备、不同SIP实现的协议栈不兼容的情况。
+ 对讲机音视频通话

    高清视频需要提供多种分辨率、帧率、采样率,用于适应网络环境,通过H.264编解码器,向用户提供清晰且流畅的视频画面。系统进行了PC-Phone的测试，PC端使用VLC分别作为RTSP服务器和播放器进行测试；Phone-Phone测试，采用小米1S和Nexus 7进行测试；下图为Phone-Phone自身录制和播放进行测试截图。
    
![IMG-THUMBNAIL](http://cyeam.qiniudn.com/device-2014-04-23-110907.png)

+ 系统抢占式通话

    抢占式通话将会在按下音量+键后开始。

+ 系统协作模块

    协作方式通过SIP Message实现。当发送消息后，会返回200 OK的成功响应。使用PC-Phone的测试方式进行，PC端使用Oracle提供的TextClient进行。TextClient是基于Jain-SIP实现的PC端SIP Message客户端。


{% include JB/setup %}