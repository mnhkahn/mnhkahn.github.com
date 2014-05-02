---
layout: post
title: "基于流媒体的对讲机系统——视频编解码技术"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: ""
category: "Postgraduate design"
tags: ["Postgraduate design", Paper"]
---

MPEG正式审核程序是Moving Picture Experts Group的简称。这个名字本来的含义是指一个研究视频和音频编码标准的“动态图像专家组”组织，成立于1988年，致力开发视频、音频的压缩编码技术。现在我们所说的MPEG泛指由该小组制定的一系列视频编码标准正式审核程序。该小组于1988年组成，至今已经制定了MPEG-1、MPEG-2、MPEG-3、MPEG-4、MPEG-7等多个标准，MPEG-21正在制定中。MPEG是ISO和IEC的工作组，它的官方头衔为：第一技术委员会第二十九子委员会第十一号工作组正式审核程序，英文头衔为ISO/IEC JTC1/SC29 WG11。MPEG大约每2-3个月举行一次会议，每次会议大约持续5天，在会议期间，新的建议和技术细节先在小组中讨论，成熟后进入标准化的正式审核程序。与MPEG工作组相关的其他几个视频标准化工作组包括ITU-T VCEG以及JVT。

+ MPEG-1：第一个官方的视訊音訊压缩标准，随后在Video CD中被采用，其中的音訊压缩的第三级（MPEG-1 Layer 3）简称MP3，成为比较流行的音频压缩格式。

+ MPEG-2：广播质量的视訊、音訊和传输协议。被用于無線數位電視-ATSC、DVB以及ISDB、数字卫星电视（例如DirecTV）、数字有线电视信号，以及DVD视频光盘技术中。

+ MPEG-3：原本目标是为高解析度电视（HDTV）设计，随后發現MPEG-2已足夠HDTV應用，故MPEG-3的研發便中止。

+ MPEG-4：2003年发布的视訊压缩标准，主要是扩展MPEG-1、MPEG-2等標準以支援視訊／音訊物件（video/audio "objects"）的編碼、3D內容、低位元率編碼（low bitrate encoding）和數位版權管理（Digital Rights Management），其中第10部分由ISO/IEC和ITU-T联合发布，称为H.264/MPEG-4 Part 10。

+ H.264/MPEG-4第10部分，或称AVC（Advanced Video Coding，高级视频编码），是一种面向块的基于运动补偿的编解码器标准。H.264因其是蓝光碟片的一种编解码标准而著名，所有蓝光碟片播放器都必须能解码H.264。它也被广泛用于网络流媒體数据如Vimeo、YouTube、以及iTunes Store，网络软件如Adobe Flash Player和Microsoft Silverlight，以及各种高清晰度電視陆地广播（ATSC，ISDB-T，DVB-T或DVB-T2），线缆（DVB-C）以及卫星（DVB-S和DVB-S2）。

---
######*参考文献*



{% include JB/setup %}