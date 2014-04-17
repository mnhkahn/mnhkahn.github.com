---
layout: post
title: "基于Android的移动VoIP视频通话系统——实时流媒体协议RTSP"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: ""
category: "Postgraduate design"
tags: ["Postgraduate design", Paper"]
---

即时串流协定（Real Time Streaming Protocol，RTSP）是用来控制声音或影像的多媒体串流协议，并允许同时多个串流需求控制，传输时所用的网络通讯协定并不在其定义的范围内，服务器端可以自行选择使用TCP或UDP来传送串流内容，它的语法和运作跟HTTP 1.1类似，但并不特别强调时间同步，所以比较能容忍网络延迟。

![IMG-THUMBNAIL](http://cyeam.qiniudn.com/rtsp.jpg)

RTSP主要信令如下：

+ OPTIONS：获得服务器支持的RTSP消息类型。
+ DESCRIBE：获取服务器返回的SDP消息，其中包含媒体流ID、支持编解码、序列参数集SPS与图像参数集PPS等。
+ SETUP：交互双方的RTP端口号，客户端获取服务器分配的会话ID。
+　PLAY：通知服务器传输流媒体，请求必须包含在SETUP响应中的会话ID。
+　PAUSE：暂停当前会话，即停止媒体流传输，但是并不释放端口与资源。
+ TEARDOWN：结束当前会话，并释放端口、连接与资源。

---
######*参考文献*
+ 【1】[RTSP 协议分析 （一） 博水](http://www.cnblogs.com/qingquan/archive/2011/07/14/2106834.html)


{% include JB/setup %}