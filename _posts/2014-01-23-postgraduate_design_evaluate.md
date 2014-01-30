---
layout: post
title: "安卓对讲机开发评估"
description: "毕设题目《基于流媒体的语音视频通话系统》，使用Android实现。先在这里做一下技术评估。"
category: "Postgraduate design"
tags: ["Postgraduate design", "Android", "RTP", "FFmpeg", "SIP", "Evaluate"]
---

毕业设计准备在Android平台上开发一个音视频通话软件，基于流媒体实现。项目的目的就是做一个山寨版的Faceime。目前了解到的实现技术是FFmpeg实现流媒体编码，RTP实现传输控制，SIP实现通话建立。我自己还想把SIP服务器部署到GAE上面，使其成为一个可用的项目。

#####1. 音视频采集，压缩，发送，解码，显示的流程

![系统流程图](http://cyeam.qiniudn.com/%E6%B5%81%E7%A8%8B%E5%9B%BE.png)

#####1. 流媒体编码
视频采集可以直接使用硬件编码，而解码需要使用到软件解码。使用开源的C库FFmpeg进行解码。
这是比较熟悉的一个部分，之前做过，而且用JNI调用成功了`hello, world`。。。现在考虑去Github找，使用开源的编译好的库。

+ [havlenapetr / FFMpeg](https://github.com/havlenapetr/FFMpeg)
+ [halfninja / android-ffmpeg-x264](https://github.com/halfninja/android-ffmpeg-x264)

#####2. 流媒体传输
将采集到的音视频分别进行传输。_ref_AndroidRTC里面只有c的源文件，没有编译好的动态链接库。可能还需要自己编译。

+ [Teaonly / _ref_AndroidRTC](https://github.com/Teaonly/_ref_AndroidRTC)

#####3. SIP(Session Initiation Protocol)
这块因为我想部署到GAE上面，所以不能使用C++，考虑使用Java的开源库。此外，还要调研GAE上面执行C++动态链接库的可行性。

+ [jitsi.org](https://jitsi.org/)
+ [jitsi / jitsi](https://github.com/jitsi/jitsi)
+ [jitsi / jitsi-android](https://github.com/jitsi/jitsi-android)
+ [Jitsi（SIP communicator）的环境部署和打包发布](http://blog.csdn.net/nomousewch/article/details/7012392)

---

######*开发环境*
+ Nexus 7
    + Android version **4.4.2**
    + Kernel version **3.4.0-gac9222c**

![Nexus 7](http://cyeam.qiniudn.com/portable-product-1200.jpg)


######*参考文献*
+ 《基于Android的移动VoIP高清视频通话系统的设计与实现》曹建龙
+ [Android 中如何使用SIP服务](http://www.3g-edu.org/news/art014.htm)
+ [jitsi打包](http://blog.csdn.net/nomousewch/article/details/7012392)

{% include JB/setup %}