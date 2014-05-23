---
layout: post
title: "如何开发一个流媒体服务器？"
figure: "https://code.google.com/p/spydroid-ipcamera/logo?cct=1355471564"
description: "通过学习libstreaming源码，介绍如何在Android手机上开发一套简单的流媒体服务器。"
category: "Postgraduate design"
tags: ["Postgraduate design", Paper"]
---

+ [关于Android端的流媒体库的调研](http://blog.cyeam.com/postgraduate%20design/2014/04/17/pager_current/)
+ RTSP/RTCP/RTP 协议分析

    > 用一句简单的话总结：RTSP发起/终结流媒体、RTP传输流媒体数据 、RTCP对RTP进行控制，同步。

    关于涉及到的RTP/RTSP/RTCP协议的描述分别可以参考：

    + [实时流媒体协议RTSP](http://blog.cyeam.com/postgraduate%20design/2014/04/17/pager_rtsp/)
    + [实时传输协议RTP](http://blog.cyeam.com/postgraduate%20design/2014/04/17/pager_rtp/)
    + 三者的关系如下：

        ![IMG-THUMBNAIL](http://images.cnblogs.com/cnblogs_com/whyandinside/RTPRTSP.jpg)

+ [H264/AVC](http://blog.cyeam.com/postgraduate%20design/2014/04/17/pager_video/)
+ 流媒体服务器的实现

    + [从SDP获取音视频通信消息](http://blog.cyeam.com/postgraduate%20design/2014/04/17/pager_sdp)
    + [RTSP请求分析](http://blog.cyeam.com/postgraduate%20design/2014/04/17/pager_rtsp)
    + [RTP打包](http://blog.cyeam.com/postgraduate%20design/2014/04/17/pager_rtp)

+ 流媒体传输同步处理


---

######*参考文献*
+ 【2】[Supported Media Formats - Android Developers](http://developer.android.com/guide/appendix/media-formats.html)
+ 【3】[RFC 3984 RTP Payload Format for H.264 Video](https://github.com/mnhkahn/cInterphone/blob/master/docs/rfc3984_chn.txt)
+ 【4】[RTP Payload Format for Transport of MPEG-4 Elementary Streams](http://tools.ietf.org/html/rfc3640)

{% include JB/setup %}