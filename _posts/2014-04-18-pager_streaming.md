---
layout: post
title: "基于流媒体的对讲机系统——流媒体传输解决方案"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: "Andoird流媒体传输的调研"
category: "Postgraduate design"
tags: ["Postgraduate design", Evaluate"]
---
###MediaPlayer
MediaPlayer是Android提供的可以用来控制播放视频和音频的控件，同时支持播放文件和流媒体。MedialPayer还可以将读到的媒体信息通过setDisplay、setSurface方法播放在指定展示控件上。

###libstreaming
除了有流媒体的播放，还需要有流媒体的采集，这就需要有一个RTSP服务器。这里找到了开源的RTSP解决方案，该方案是将读到的RTP流转成RTSP协议控制的流媒体格式。

###MediaRecorder
MediaRecorder是Android官方提供的录制视频的解决方案，提供将拍摄到的音视频信息保存为文件的方法。而本课题需要采集到的是流媒体信息，所以原生的方法不能彻底解决录制问题。上面提到的libstreaming方法就是基于此方法，将录制好的视频文件再解析成RTSP流。

---
######*参考文献*
+ [MediaPlayer | Android Developers](http://developer.android.com/reference/android/media/MediaPlayer.html)
+ [fyhertz/libstreaming | GitHub](https://github.com/fyhertz/libstreaming)
+ [MediaRecorder | Android Developers](http://developer.android.com/reference/android/media/MediaRecorder.html)


{% include JB/setup %}