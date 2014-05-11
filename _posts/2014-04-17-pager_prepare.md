---
layout: post
title: "基于流媒体的对讲机系统——系统开发准备"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: "系统开发需要的预备知识——工欲善其事，必先利其器"
category: "Postgraduate design"
tags: ["Postgraduate design", Paper"]
---

工欲善其事，必先利其器。写代码也一样，借鉴优秀的工具辅助开发，可以帮助学习和了解相关知识和技术。

###1. tcpdump
开发网络通信程序需要能监测到网络通信流程以及通信内容，以便了解整个通信流程以及问题。在Linux下，一般是通过tcpdump和WireShark来实现该功能。tcpdump负责监控制定设备，从该设备抓包，而WireShark可以用来查看和解析包内容。甚至可以帮助我们分析整个通信流程。在此项目中，就可以用WireShark监测SIP注册和呼叫流程和RTSP和RTP流的传输过程。

	tcpdump -i wlan0 -w cInterphone.cap

在此命令中，`-i`用于指出要采集的设备，这里指出的是无线网卡wlan0；`-w`要指出采集到的数据输出的目录，这里指出是文件cInterphone.cap。此外，启动此命令还需要使用管理员权限。本项目中要监控的是手机的网络通信，所以还需要将手机的网络设成PC的网络代理，这样才能通过监控PC的网卡监控到手机的网络访问情况。

在使用WireShark的时候，采集到的数据量很大，所以需要进行过滤。查看我们需要的数据。

+ 通过网络协议过滤。如果我们要查看RTP协议或者RTSP协议的数据，在过滤器中输入RTP即可。
+ 通过IP过滤。本项目中是两个设备互相访问，采集到的数据也都是两个设备互相传输的全部数据。为了方便分析流程，可以只所以单独查看一个设备的。可以通过`ip.src=192.168.1.103`实现过滤。

###2. linphone
SIP呼叫部分的开发，如果呼叫和被叫方同时进行开发和测试，难度较大。本课题采用了Linux下的linphone作为辅助开发工作，用于测试SIP呼叫流程。

###3. VLC
本课题另一个比较重要的部分，就是流媒体的读取和播放。读取和播放展示是两个流程，需要分开进行开发。这就需要到一个辅助工具来进行测试开发。我们选取了VLC。VLC是一个非常优秀的跨平台流媒体播放器。既可以用来做RTSP服务器，也可以用来做RTSP客户端。

+ RTSP方式

        vlc -vvv sample1.avi --sout "#transcode{vcodec=h264,vb=0,scale=0,acodec=mpga,ab=128,channels=2,samplerate=44100}:rtp{sdp=rtsp://:8554/test}" 

+ HTTP方式

        vlc -vvv sample1.avi --sout "#transcode{vcodec=h264,vb=0,scale=0,acodec=mpga,ab=128,channels=2,samplerate=44100}:http{mux=ffmpeg{mux=flv},dst=:8080/test}" 

###4. adb
Android官方提供的开发工具，用于控制Android手机，adb服务器等。最好将`adb`加入到环境变量中，调试起来比较方便。

+ 安装Android程序。在此之前都是先将安装包放入手机再安装。。。

		adb install *.apk

+ 启动和关闭adb服务

		adb start-server
		adb kill-server

+ 神器，用于排查问题。一般adb启动不了都是因为端口被占用。我在Windows下都是被QQ占用。。。

		adb nodaemon server

---
######*参考文献*
+ [用vlc搭建简单流媒体服务器（UDP和TCP方式）](http://www.cnblogs.com/MikeZhang/archive/2012/09/09/vlcStreamingServer20120909.html)

{% include JB/setup %}