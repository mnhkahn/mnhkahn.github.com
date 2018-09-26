---
layout: post
title: "视频编解码技术H264"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeam/c168.png"
description: "关于H264视频编码格式的介绍和分析。"
category: "Postgraduate"
tags: ["Postgraduate design", "Paper"]
---

http://blog.csdn.net/tjy1985/article/details/7963531
MPEG正式审核程序是Moving Picture Experts Group的简称。这个名字本来的含义是指一个研究视频和音频编码标准的“动态图像专家组”组织，成立于1988年，致力开发视频、音频的压缩编码技术。现在我们所说的MPEG泛指由该小组制定的一系列视频编码标准正式审核程序。该小组于1988年组成，至今已经制定了MPEG-1、MPEG-2、MPEG-3、MPEG-4、MPEG-7等多个标准，MPEG-21正在制定中。MPEG是ISO和IEC的工作组，它的官方头衔为：第一技术委员会第二十九子委员会第十一号工作组正式审核程序，英文头衔为ISO/IEC JTC1/SC29 WG11。MPEG大约每2-3个月举行一次会议，每次会议大约持续5天，在会议期间，新的建议和技术细节先在小组中讨论，成熟后进入标准化的正式审核程序。与MPEG工作组相关的其他几个视频标准化工作组包括ITU-T VCEG以及JVT。

+ MPEG-1：第一个官方的视訊音訊压缩标准，随后在Video CD中被采用，其中的音訊压缩的第三级（MPEG-1 Layer 3）简称MP3，成为比较流行的音频压缩格式。

+ MPEG-2：广播质量的视訊、音訊和传输协议。被用于無線數位電視-ATSC、DVB以及ISDB、数字卫星电视（例如DirecTV）、数字有线电视信号，以及DVD视频光盘技术中。

+ MPEG-3：原本目标是为高解析度电视（HDTV）设计，随后發現MPEG-2已足夠HDTV應用，故MPEG-3的研發便中止。

+ MPEG-4：2003年发布的视訊压缩标准，主要是扩展MPEG-1、MPEG-2等標準以支援視訊／音訊物件（video/audio "objects"）的編碼、3D內容、低位元率編碼（low bitrate encoding）和數位版權管理（Digital Rights Management），其中第10部分由ISO/IEC和ITU-T联合发布，称为H.264/MPEG-4 Part 10。

+ H.264/MPEG-4第10部分，或称AVC（Advanced Video Coding，高级视频编码），是一种面向块的基于运动补偿的编解码器标准。H.264因其是蓝光碟片的一种编解码标准而著名，所有蓝光碟片播放器都必须能解码H.264。它也被广泛用于网络流媒體数据如Vimeo、YouTube、以及iTunes Store，网络软件如Adobe Flash Player和Microsoft Silverlight，以及各种高清晰度電視陆地广播（ATSC，ISDB-T，DVB-T或DVB-T2），线缆（DVB-C）以及卫星（DVB-S和DVB-S2）。


H264的功能分为两层，视频编码层（VCL）和网络提取层（NAL）。视频编码层负责高效的视频内容表示，而网络适配层负责以网络所要求的恰当的方式对数据进行打包和传送。引入NAL并使之与VCL分离带来的好处包括两方面：其一、使信号处理和网络传输分离，VCL 和NAL 可以在不同的处理平台上实现；其二、VCL 和NAL 分离设计，使得在不同的网络环境内，网关不需要因为网络环境不同而对VCL比特流进行重构和重编码。
       
H.264 的基本流由一系列NALU （Network Abstraction Layer Unit ）组成，不同的NALU数据量各不相同。H.264 草案指出[2]，当数据流是储存在介质上时，在每个NALU 前添加起始码：0x000001，用来指示一个 NALU的起始和终止位置。在这样的机制下，在码流中检测起始码，作为一个NALU得起始标识，当检测到下一个起始码时，当前NALU结束。每个NALU单元由一个字节的 NALU头（NALU Header）和若干个字节的载荷数据（RBSP）组成。

![IMG-THUMBNAIL](http://hi.csdn.net/attachment/201108/6/0_1312647261x7Lc.gif)


---

######*参考文献*
+ 【1】[H264码流打包分析 - szu030606的专栏](http://blog.csdn.net/china_video_expert/article/details/7211302)


{% include JB/setup %}
