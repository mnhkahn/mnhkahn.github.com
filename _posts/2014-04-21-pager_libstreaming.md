---
layout: post
title: "如何开发一个流媒体服务器？"
figure: "https://code.google.com/p/spydroid-ipcamera/logo?cct=1355471564"
description: "通过学习libstreaming源码，介绍如何在Android手机上开发一套简单的流媒体服务器。"
category: "Postgraduate design"
tags: ["Postgraduate design", Paper"]
---

> 用一句简单的话总结：RTSP发起/终结流媒体、RTP传输流媒体数据 、RTCP对RTP进行控制，同步。

关于涉及到的RTP/RTSP/RTCP协议的描述分别可以参考：

+ [实时流媒体协议RTSP](http://blog.cyeam.com/postgraduate%20design/2014/04/17/pager_rtsp/)
+ [实时传输协议RTP](http://blog.cyeam.com/postgraduate%20design/2014/04/17/pager_rtp/)

---

######*参考文献*
+ [RTMP/RTP/RTSP/RTCP的区别 | FrankieWang008的专栏](http://blog.csdn.net/frankiewang008/article/details/7665547)
+ [Supported Media Formats | Android Developers](http://developer.android.com/guide/appendix/media-formats.html)
+ [RFC 3984 RTP Payload Format for H.264 Video](https://github.com/mnhkahn/cInterphone/blob/master/docs/rfc3984_chn.txt)
+ [RTP Payload Format for Transport of MPEG-4 Elementary Streams](http://tools.ietf.org/html/rfc3640)

{% include JB/setup %}