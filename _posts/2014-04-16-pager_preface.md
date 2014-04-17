---
layout: post
title: "基于Android的移动VoIP视频通话系统的设计与实现——写在前面"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: ""
category: "Postgraduate design"
tags: ["Postgraduate design", Paper"]
---

从研一一开始，导师就交给我这个任务，去做Android上的对讲机。期间，他对于这个项目并没有对我有过多的指导，只是说要使用流媒体去通信。对于我这个一不懂Android，二不懂流媒体的菜鸟，也就只能硬得头皮去做了。

这个东西技术上已经很成熟了，Apple的FaceTime已经能实现在iPhone、iPad和iMac上面的视频通话。而Android方面，Samsung等手机厂商也有在手机系统内直接支持SIP，连接上SIP服务器就可以直接使用了。在PC方面，最成功的应该算是linphone了，此外，它还支持了iOS和Android。

上面提到的linphone，已经对其所有平台的产品进行了开源，我没可以很容易的下载到[源代码](http://www.linphone.org/eng/download/git.html)，但是鄙人能力有限，在通过JNI编译C语言代码的部分，始终有问题，实在看不懂那么长的Makefile。。。

此外，还有了很多弯路。由于没有指导，只能看论文摸索着做，有时候分不清重点。有一段时间尝试着去跨平台编译ffmpeg，千辛万苦编译出来了，准备着编译RTP流的时候使用。但是后来发现Android新版本开始支持读RTSP流和H264和H263的编解码了，好像是从3.0开始支持H264编码的。哎，浪费了时间。。。

开发阶段也遇到过一些蛋疼的事情。最后借过一台MTK的平板，准备测试通话，可万万没想到，MTK平台下H264的编码器没有。。。代码执行不了，想想整个Android平台下碎片化的系统，多样化的硬件平台，难道叫我没把所有编码器都编译一下么。。。

期间，发现一篇很好的论文——《基于Android的移动VoIP高清视频通话系统的设计与实现》曹建龙，这是他的[个人博客](http://blog.csdn.net/cazicaquw/article/details/8650543)。主要参考了他的解决方案，但是用的开发工具我又找了适合我开发的类似的工具进行的实现。

项目代码托管在[GitHub cInterphone](https://github.com/mnhkahn/cInterphone)。欢迎拍砖。

好了，就啰嗦到这里吧，开始写论文。

{% include JB/setup %}