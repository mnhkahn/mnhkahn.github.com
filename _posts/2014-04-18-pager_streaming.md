---
layout: post
title: "基于流媒体的对讲机系统——流媒体传输解决方案"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: "Andoird流媒体传输的调研"
category: "Postgraduate design"
tags: ["Postgraduate design", Evaluate"]
---

从Android 4.0开始，Android自身提供了视频录制和视频播放的功能。分别是MediaPlayer和MediaRecorder。并且MediaPlayer还支持HTTP流和RTSP流的播放。所以，本课题再完成RTSP Server即可。

MediaPlayer是Android提供的可以用来控制播放视频和音频的控件，同时支持播放文件和流媒体。MedialPayer还可以将读到的媒体信息通过setDisplay、setSurface方法播放在指定展示控件上。

在Android端进行音视频压缩，有两种方式：

+ 软编码的方式。Android支持通过NDK的方式将用C/C++实现的代码库跨平台编译到Android端上，然后通过JNI调用即可。本课题没有选择这种方法，软编码是通过算法的方式进行计算得到的，这样解码效率高、耗电量大，并且可移植性差，不同的硬件平台都要为其单独进行NDK跨平台编码。
+ 硬编码方式。在Android手机搭载的核心芯片ARM在设计的时候，就为一些常见视频压缩格式进行了电路设计。调用其进行压缩，速度快、节能、可移植性高，并且Android未来的发展趋势就是ARM芯片处理能力越来越强，所以直接使用硬件编码即可。

MediaRecorder是Android官方提供的录制视频的解决方案，提供将拍摄到的音视频信息保存为文件的方法。而本课题需要采集到的是流媒体信息，所以原生的方法不能彻底解决录制问题。上面提到的libstreaming方法就是基于此方法，将录制好的视频文件再解析成RTSP流。

RTSP Server实现难度并不大，只要按照RTSP协议的通信流程实现即可。RTSP的流程前面已经介绍过。RTSP Server的设计将在后面进行详细设计。

---
######*参考文献*
+ [MediaPlayer | Android Developers](http://developer.android.com/reference/android/media/MediaPlayer.html)
+ [fyhertz/libstreaming | GitHub](https://github.com/fyhertz/libstreaming)
+ [MediaRecorder | Android Developers](http://developer.android.com/reference/android/media/MediaRecorder.html)


{% include JB/setup %}