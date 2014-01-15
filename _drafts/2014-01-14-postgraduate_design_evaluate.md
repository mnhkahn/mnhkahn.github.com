---
layout: post
title: "毕业设计评估"
description: "我的毕设题目《基于流媒体的语音视频通话系统》，使用Android实现。先在这里做一下技术评估。"
category: "Postgraduate design"
tags: ["Postgraduate design", "Android", "RTP", "FFmpeg", "SIP", "Evaluate"]
---

毕业设计准备在Android平台上开发一个音视频通话软件，基于流媒体实现。项目的目的就是做一个山寨版的Faceime。目前了解到的实现技术是FFmpeg实现流媒体编码，RTP实现传输控制，SIP实现通话建立。我自己还想把SIP服务器部署到GAE上面，使其成为一个可用的项目。

#####1. 音视频采集，压缩，发送，解码，显示的流程

![系统流程图](http://cyeam.qiniudn.com/%E6%B5%81%E7%A8%8B%E5%9B%BE.png)

#####1. 流媒体编码
这是比较熟悉的一个部分，之前做过，而且用JNI调用成功了`hello, world`。。。

去Github找了找，发现有很多跨平台编译好的。

[havlenapetr / FFMpeg](https://github.com/havlenapetr/FFMpeg)

[halfninja / android-ffmpeg-x264](https://github.com/halfninja/android-ffmpeg-x264)

#####2. 流媒体传输
将采集到的音视频分别进行传输。

[hmgle / h264_to_rtp](https://github.com/hmgle/h264_to_rtp)
[Teaonly / _ref_AndroidRTC](https://github.com/Teaonly/_ref_AndroidRTC)

#####3. SIP(Session Initiation Protocol)
这块因为我想部署到GAE上面，所以不能使用C++，考虑使用Java的开源库。此外，还要调研GAE上面执行C++动态链接库的可行性。

[![OverSip](http://www.oversip.net/images/oversip-logo.png)](https://github.com/versatica/OverSIP)

#####4. 

#####5. 

+ 《基于Android的移动VoIP高清视频通话系统的设计与实现》曹建龙
+ 

{% include JB/setup %}