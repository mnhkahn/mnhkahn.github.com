---
layout: post
title: "基于Android的移动VoIP视频通话系统——系统开发准备"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: "系统开发需要的预备知识"
category: "Postgraduate design"
tags: ["Postgraduate design", Paper"]
---

###1. tcpdump
开发网络通信程序需要能监测到网络通信流程以及通信内容，以便了解整个通信流程以及问题。在Linux下，一般是通过tcpdump和WireShark来实现该功能。tcpdump负责监控制定设备，从该设备抓包，而WireShark可以用来查看和解析包内容。甚至可以帮助我们分析整个通信流程。在此项目中，就可以用WireShark监测SIP注册和呼叫流程和RTSP和RTP流的传输过程。

	tcpdump -i wlan0 -w cInterphone.cap

在此命令中，`-i`用于指出要采集的设备，这里指出的是无线网卡wlan0；`-w`要指出采集到的数据输出的目录，这里指出是文件cInterphone.cap。此外，启动此命令还需要使用管理员权限。本项目中要监控的是手机的网络通信，所以还需要将手机的网络设成PC的网络代理，这样才能通过监控PC的网卡监控到手机的网络访问情况。

在使用WireShark的时候，采集到的数据量很大，所以需要进行过滤。查看我们需要的数据。

+ 通过网络协议过滤。如果我们要查看RTP协议或者RTSP协议的数据，在过滤器中输入RTP即可。
+ 通过IP过滤。本项目中是两个设备互相访问，采集到的数据也都是两个设备互相传输的全部数据。为了方便分析流程，可以只所以单独查看一个设备的。可以通过`ip.src=192.168.1.103`实现过滤。

---
######*参考文献*



{% include JB/setup %}