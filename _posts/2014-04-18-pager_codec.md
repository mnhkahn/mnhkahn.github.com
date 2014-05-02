---
layout: post
title: "基于流媒体的对讲机系统——音视频编解码"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: "Andoird音视频编码的调研"
category: "Postgraduate design"
tags: ["Postgraduate design", Evaluate"]
---

在之前，由于Android碎片话的原因，各个厂商使用的都是老版本的Android 2.3，要进行H264编码只能跨平台移植ffmpeg。前面也提到过，跨平台移植虽然运行效率高，但是移植难度大。在此之前的解决方案都是采用移植ffmpeg的方法。到本项目开展的时候，已经到了Android 4.0时代，也就不能盲目的跟随之前的解决方案，要及时采用Android 4.0之后提供的新特性才行。

Android 4.0 内置H264硬件编码方案，采用Unix域协议，获取OpenCore媒体框架的编码数据。

###OpenCore
![IMG-THUMBNAIL](http://cyeam.qiniudn.com/opencore.jpg)

根据层次划分，OpenCORE主要分为内容策略管理（Content Pollcy Manager）、多媒体引擎（MultiMedia Engines）、数据格式解析器（Data Formats Parser）、视频编解码器（Video Codecs）、音频编解码器（Audio Codecs）、操作系统兼容库（OSCL, Operating System Compatibility Library）等几个部分。

目前OpenCORE已经能够支持全部的主流音、视频格式。音频格式有AAC、AMR、MP3、WAV等，视频格式有3GP、MP4、JPG等。
为了更好地在不同操作系统提供可移植性。OSCL包含了基本数据类型、配置、字符串工具、输入/输出、错误处理、线程等内容，类似一个基础的C++库。
相对其他模块而言，OpenCORE的代码量非常庞大，OpenCORE基于C++实现，定义了全功能的操作系统移植层，各种基本功能均被封装成类的形式，各层次之间的接口多使用继承等方式。

---
######*参考文献*
+ [Supported Media Formats | Android Developers](http://developer.android.com/guide/appendix/media-formats.html)
+ [Android OpenCORE 概述](http://www.3g-edu.org/news/art068.htm)

{% include JB/setup %}