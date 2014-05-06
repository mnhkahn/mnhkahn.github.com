---
layout: post
title: "基于流媒体的对讲机系统的设计与实现——总结"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: ""
category: "Postgraduate design"
tags: ["Postgraduate design", Paper"]
---

从研一一开始，导师就交给我这个任务，去做Android上的对讲机。这个课题对于我来说是一个完全不了解的领域，这也让我一开始入手很难，进行了比较长时间的前期开发调研工作。

首先是了解了已有的相关技术：VOIP。这个东西技术上已经很成熟了，Apple的FaceTime已经能实现在iPhone、iPad和iMac上面的视频通话。而Android方面，Samsung等手机厂商也有在手机系统内直接支持SIP，连接上SIP服务器就可以直接使用了。在PC方面，最成功的应该算是linphone了，此外，它还支持了iOS和Android。

上面提到的linphone，已经对其所有平台的产品进行了开源，我们可以很容易的下载到[源代码](http://www.linphone.org/eng/download/git.html)，由于该站点有时会被墙，特此提供下载。但是鄙人能力有限，在通过JNI编译C语言代码的部分，始终有问题，实在看不懂那么长的Makefile。。。

发现一篇很好的论文——《基于Android的移动VoIP高清视频通话系统的设计与实现》曹建龙，这是他的[个人博客](http://blog.csdn.net/cazicaquw/article/details/8650543)。主要参考了他的解决方案，但是用的开发工具我又找了适合我开发的类似的工具进行的实现。

接着，是去研究对讲机的通信原理和实际使用过程中要用到的现场指挥方式。并对于对讲机在Android平台进行了创新性的设计：抢占通信模式和协作应答模式。

最后，就是围绕前期的需求和设计框架进行开发工作。开发阶段也遇到过一些蛋疼的事情。最后借过一台MTK的平板，准备测试通话，可万万没想到，MTK平台下H264的编码器没有。。。代码执行不了，想想整个Android平台下碎片化的系统，多样化的硬件平台，难道叫我没把所有编码器都编译一下么。。。

整个项目持续时间较长，从Android 2.3流行的时代到Android 4.0 普及的时代。早期的设计是围绕Android 2.3特性来做的，而有些工作内容到了Android 4.0时代就得到了解决。有一段时间尝试着去跨平台编译ffmpeg，Android 2.3的时代并不支持H264编码。千辛万苦编译出来了，准备着编译RTP流的时候使用。但是后来发现Android新版本开始支持读RTSP流和H264和H263的编解码了，从3.0开始支持H264编码的。

开发过程中还使用了比较流行的开发工具：Github。项目就托管在[那里](https://github.com/mnhkahn/cInterphone)。欢迎拍砖。

经过功能与性能测试，本项目实现了无线网络高清视频通信，满足了移动对讲机业务的基本要求。本文的系统依然有待完善,今后可以从以下几个方面作出进一步的改进:

+ 本系统主要是针对移动端进行开发，未来还需要增加总控制台的服务器。

{% include JB/setup %}