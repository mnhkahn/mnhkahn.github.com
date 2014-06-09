---
layout: post
title: "基于流媒体的对讲机系统——语音编解码技术"
figure: "http://cyeam.qiniudn.com/c168.png"
description: ""
category: "Postgraduate design"
tags: ["Postgraduate design", Paper"]
---
http://blog.csdn.net/tjy1985/article/details/7963531
AAC（Advanced Audio Coding），中文称为“高级音频编码”，出现于1997年，基于 MPEG-2的音频编码技术。由诺基亚，苹果等公司共同开发，目的是取代MP3格式。2000年，MPEG-4标准出现后，AAC 重新集成了其特性，加入了SBR技术和PS技术。

AAC可以支持多达48个音轨，15个低频（LFE）音轨，5.1多声道支持，更高的采样率（最高可达96kHz，音频CD为44.1kHz）和更高的采样精度（支持8bit、16bit、24bit、32bit，音频CD为16bit）以及有多种语言的兼容能力，更高的解码效率，一般来说，AAC可以在对比MP3文件缩小30%的前提下提供更好的音质。

AAC与MP3规格对比:

+ 比特率：AAC - 最高512kbps（双声道时）/MP3 - 32~320kbps
+ 采样率：AAC - 最高96kHz / MP3 - 最高48kHz
+ 声道数：AAC - （5.1）六声道 / MP3 - 两声道
+ 采样精度：AAC - 最高32bit / MP3 - 最高16bit

杜比实验室通过与传统mp3大量的测试和比对，得到如下结论：

+ 128Kbps的AAC立体声音乐被专家认为不易察觉到与原来未压缩音源的区别；
+ AAC格式在96Kbps码率的表现超过了128Kbps的MP3格式；
+ 同样是128Kbps，AAC格式的音质明显好于MP3；
+ AAC是唯一一个，能够在所有的EBU试听测试项目的获得“优秀”的网络广播格式。

---

######*参考文献*
+ [高级音频编码 | 维基百科](http://zh.wikipedia.org/wiki/%E9%80%B2%E9%9A%8E%E9%9F%B3%E8%A8%8A%E7%B7%A8%E7%A2%BC)



{% include JB/setup %}