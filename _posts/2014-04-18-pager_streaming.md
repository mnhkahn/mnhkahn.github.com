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

MediaRecorder是Android官方提供的录制视频的解决方案，提供将拍摄到的音视频信息保存为文件的方法。而本课题需要采集到的是流媒体信息，所以原生的方法不能彻底解决录制问题。上面提到的libstreaming方法就是基于此方法，将录制好的视频文件再解析成RTSP流。

RTSP Server实现难度并不大，只要按照RTSP协议的通信流程实现即可。RTSP的流程前面已经介绍过。RTSP Server的设计将在后面进行详细设计。

---
######*参考文献*
+ [MediaPlayer | Android Developers](http://developer.android.com/reference/android/media/MediaPlayer.html)
+ [fyhertz/libstreaming | GitHub](https://github.com/fyhertz/libstreaming)
+ [MediaRecorder | Android Developers](http://developer.android.com/reference/android/media/MediaRecorder.html)


{% include JB/setup %}