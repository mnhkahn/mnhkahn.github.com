---
layout: post
title: "基于流媒体的对讲机系统——测试环境"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: ""
category: "Postgraduate design"
tags: ["Postgraduate design", Paper"]
---

本文系统测试环境为实验室无线局域网，搭建了SIP服务器用于SIP终端的注册与用户管理，采用两个智能手机终端搭载智能对讲机，系统拓扑结构如图6.1所示,系统测试设备配置如表6.1所示。

SIP服务器的功能主要有SIP注册、SIP重定向、IM服务、SIP路由等。本文使用OpenSIPS作为SIP服务器。OpenSIPS是一款成熟的开源SIP服务器实现，提供了一个高度灵活的、用户可配置的路由引擎，可以为语音、视频、IM和presence等服务提供强大高效的路由、鉴权、NAT、网关协议转化等功能。相比于Asterisk，OpenSIPS更易安装与配置,并且由于其稳定高效等特点，OpenSIPS已经被诸多电信运营商应用在自己的网络体系中。

本课题两个重要组成部分：SIP和RTSP流媒体。要对这两个模块进行测试，分别使用了linphone、OpenSIPS和VLC。linphone是开源的VOIP电话，使用linphone进行测试SIP注册和呼叫等功能是否正常工作。VLC同样也是开源的音视频播放器，同时，它还能作为视频流服务器，提供HTTP和RTSP，以及RTP视频流的缓存和传输功能。用它进行验证RTSP的流程和RTSP播放、缓存流媒体的功能。

本文使用tcpdump和WireShark对网络数据包分析，tcpdump是开源的网络抓包工具，WireShark是一款开源的网络数据包分析软件,提供数据包截取、过滤、按协议解码，以及SIP会话分析等功能。

使用两台不同Android设备进行测试：

+ Nexus 7

    Android version 4.4.2   
    Kernel version 3.4.0-gac9222c

+ 小米 1s

{% include JB/setup %}