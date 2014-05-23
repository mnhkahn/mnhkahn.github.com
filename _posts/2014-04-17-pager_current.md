---
layout: post
title: "Android 端流媒体库的分析调研"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: ""
category: "Postgraduate design"
tags: ["Postgraduate design", Paper"]
---

在Android端的流媒体服务产品已经比较成熟的有：sipdroid、linphone，还有Android官方提供的SipManager和SipAudioCall。

linphone 是比较成熟的流媒体产品，实现了跨平台，linphone分别支持Windows、Linux、Macintosh、iOS、Android这些主流系统，已经帮助解决了跨平台的问题。linphone 对于流媒体发送的底层实现是通过编译和移植C/C++语言编写的oRTP代码库实现的。将已有的PC端的代码通过NDK进行跨平台编译移植到移动端，这也是Android早期在官方没有提供相应解决方案的时候解决问题的一般方法。NDK是JNI开发的一个扩展工具包，针对Android平台，其支持的设备型号繁多，单单就设备的核心CPU而言，都有三大类：ARM、x86和MIPS，况且ARM又分为ARMv5和ARMv7等等，通过NDK编译将会导致只能适配指定CPU产品的情况，跨平台支持较弱。linphone 官方只提供了一套完整的Sip和RTP流媒体解决方案，只能进行VOIP开发，无法进行二次封装开发。

sipdroid 只是针对Android开发的流媒体产品，其内部流媒体传输并没有使用本地C/C++代码，而是使用Java实现，这样就提高了Android中跨平台的特性。但是其在流媒体传输方面并没有严格按照RTP协议实现。如果要进行视频通话只能使用其专门定制的SIP服务器。虽然sipdroid代码开源，而该服务器内部实现规范并没有公开。

从Android 2.3 Gingerbread 开始，Android官方开始对Sip和RTP流媒体进行支持。可以通过SipManager和SipAudioCall方便的实现。但是Android官方并没有提供SipVideoCall的实现，并且该实现方式比较封闭，不适合二次开发。虽然进行音频通话开发难度较低，但是视频却无法基于已有的东西增加。此方案也无法使用。

虽然Android端也有一些不错的流媒体解决方案，但是针对本课题，没有可用的现有的来辅助开发。本课题通过分析协议RFC 3684和RFC 3640，开发了一个Android端的流媒体服务器。

---

######*参考文献*

+ 【1】[Session Initiation Protocol developer guide - Android Developers](http://developer.android.com/guide/topics/connectivity/sip.html)
+ 【2】[Android NDK开发简介 - zhiweiofli - 开源中国社区](http://my.oschina.net/zhiweiofli/blog/112287)
+ 【3】[Android历史版本 - 维基百科](http://zh.wikipedia.org/wiki/Android%E6%AD%B7%E5%8F%B2%E7%89%88%E6%9C%AC)

{% include JB/setup %}