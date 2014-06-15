---
layout: post
title: "Android端RTSP解决方案——libstreaming"
figure: "http://cyeam.qiniudn.com/libstreaming_icon.png"
description: Postgraduate design"
tags: ["Postgraduate design", Paper", "Android", "libstreaming"]

---

本来是想自己实现RTP传输的，看了好多资料，还看了libstreaming的源代码。大体步骤是这样的：

+ 使用MediaRecorder采集，放入流当中；
+ 然后建立本地发送线程，sipdroid封装UDP直接实现的，而libstreaming是通过多播实现；
+ 采集到的音视频数据不能直接发送到发现线程当中，需要再建立两个本地套接字用于发送和接收；
+ 在发送线程里，读取H264的流信息，跳过mp4容器的头信息；
+ 接着就是获取NALU分割标记，一般是用`00000001`分隔不同的包，而libstreaming源码讲的是NAL头内存放的是包长度数据；
+ 然后，放入NAL和视频帧发送；
+ 一个RTP包最大容量是1200字节，如果H264包长度大于1300-sizeof(RTP Header)-sizeof(NAL)=1287字节的话，就要分包发送；

RTSP用于建立RTP会话，可以认为是RTP的一层封装。libstreaming也封装了RTP封包发送的代码，我就基于此进行了二次开发。原本准备直接用sipdroid进行RTP二次开发的，后来解了半天，也没有办法得到H264流，后来才发现它用的是H263，一群草你马奔驰而过。自己新建的一个多播和libstreaming的进行通信，可以获取到RTP包。通过解析RTP包的头，发现头信息基本正确，证明此法可用。然后接着开发，将H264流重新组包播放。

这里却遇到了一个非常大的问题。H264如果是用多个连续的包发送一个大的H264帧的时候，得到的包有可能是乱续的，还需要重新组装排序。我开发的时候想直接丢掉这些包，只解析包含单个H264的RTP包，但是又不成功。我猜测是被分包的大包是视频流的关键帧，而小包是基于关键帧的运动补偿信息（鄙人对视频压缩基本不懂，只能猜测这么多。。。）。如果是这样的话，那么我之前的做法就不行了。由于时间有限，学校催着交论文呢，而且也没找到简单的方法解决组包问题，这个就没继续做了。

---

不废话了，下面是本文的重点。。。

用RTP自己发送不成功，那么还是用libstreaming传输吧。我有一台Nexus 7和借来的联想A3000-H。做Demo我的Nexus 7 没有任何问题，而联想的用同样的代码就不行。一直以为是编码器的问题，因为Logcat一直提示找不到编码器。后来才发现是我太弱了。应该是联想的摄像头支持的参数和Nexus这些主流的不一样，导致的问题。有时候也会提示说分辨率不对，但其实是帧率不对，逗我呢。。。

通过`Camera.Parameters.getSupportedPreviewSizes`可以获得预览尺寸，通过`Camera.Parameters.getSupportedPreviewFpsRange`可以获得预览帧率。


{% include JB/setup %}