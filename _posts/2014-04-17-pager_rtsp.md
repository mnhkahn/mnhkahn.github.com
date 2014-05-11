---
layout: post
title: "基于流媒体的对讲机系统——实时流媒体协议RTSP"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: ""
category: "Postgraduate design"
tags: ["Postgraduate design", Paper"]
---

即时串流协定（Real Time Streaming Protocol，RTSP）是用来控制声音或影像的多媒体串流协议，并允许同时多个串流需求控制，传输时所用的网络通讯协定并不在其定义的范围内，服务器端可以自行选择使用TCP或UDP来传送串流内容，它的语法和运作跟HTTP 1.1类似，但并不特别强调时间同步，所以比较能容忍网络延迟。RTSP协议是对于RTP协议的一层封装，可以用来自动传输音视频。

![IMG-THUMBNAIL](http://cyeam.qiniudn.com/rtsp.jpg)

RTSP主要信令如下：

+ OPTIONS：获得服务器支持的RTSP消息类型。
+ DESCRIBE：获取服务器返回的SDP消息，其中包含媒体流ID、支持编解码、序列参数集SPS与图像参数集PPS等。
+ SETUP：交互双方的RTP端口号，客户端获取服务器分配的会话ID。
+　PLAY：通知服务器传输流媒体，请求必须包含在SETUP响应中的会话ID。
+　PAUSE：暂停当前会话，即停止媒体流传输，但是并不释放端口与资源。
+ TEARDOWN：结束当前会话，并释放端口、连接与资源。

RTSP流程

+ 查询服务器端可用方法
	+ 客户端请求(OPTION request):---询问服务器有哪些方法可用

			"OPTIONS rtsp://192.168.1.122/TestSession RTSP/1.0"
			"CSeq: 2"
			"User-Agent: LibVLC/1.1.9 (LIVE555 Streaming Media v2011.01.06)"

	+ 服务器回应(OPTION response):---回复的所有方法在Public字段

			"RTSP/1.0 200 OK"
			"CSeq: 2"
			{"Public: OPTIONS, DESCRIBE, SETUP, TEARDOWN, PLAY, PAUSE"}
			""    //最后这个也很重要，最后一个消息头需要有两个CR LF

+ 得到媒体描述信息
	+ 客户端请求(DESCRIBE request):-----要求得到媒体描述信息

			"DESCRIBE rtsp://192.168.1.122/TestSession RTSP/1.0"
			"CSeq: 3"
			"User-Agent: LibVLC/1.1.9 (LIVE555 Streaming Media v2011.01.06)"
			"Accept: application/sdp"
	+ 服务器回应(DESCRIBE response):---回应媒体描述信息，一般是sdp信息

			"RTSP/1.0 200 OK"
			"CSeq: 3" //和请求的序号要对应
			{"Server: RTSP Service"
			 "Content-Base: rtsp://192.168.1.122/TestSession"
			 "Content-Type: application/sdp"         //表示回应的是sdp信息 
			 "Content-Length: 367"
			}
			"" 
	然后再发送生成的sdp信息，sdp信息也可以和上面的字符串组合一起发送。

+ 建立RTSP会话
	+ 客户端请求(SETUP request):-----通过Transport头字段列出可接受的传输选项，建立会话

			"SETUP rtsp://192.168.1.122/TestSession/trackID=1 RTSP/1.0"
			"CSeq: 4"
			"User-Agent: LibVLC/1.1.9 (LIVE555 Streaming Media v2011.01.06)"
			"Transport: RTP/AVP;unicast;client_port=2274-2275"
	+ 服务器回应(SETUP response):--建立会话，通过Transport头字段返回选择的具体传输选项，并返回建立的Session ID;

			"RTSP/1.0 200 OK"
			"CSeq: 4"
			"Session: 68422540987712"
			"Transport:RTP/AVP;unicast;source=192.168.1.122;server_port=8000-8001;client_port=2274-2275;ssrc=3969838262"
			""    

+ 请求开始传送数据
	+ 客户端请求(PLAY request): -----请求服务器开始发送数据

			"PLAY rtsp://192.168.1.122/TestSession RTSP/1.0" 
			"CSeq: 5"
			"User-Agent: LibVLC/1.1.9 (LIVE555 Streaming Media v2011.01.06)"
			"Session: 68422540987712"
			"Range: npt=0.000-"
	+ 服务器回应(PLAY response):------回应该请求的信息

			"RTSP/1.0 200 OK"
			"CSeq: 5"
			"Session: 68422540987712"
			"RTP-Info: url=rtsp://192.168.1.122/TestSession/trackID=1"
			""   
+ 数据传输

	服务器->客户端：发送流媒体数据， 通过RTP协议传输数据

+ 关闭会话，退出
	+ 客户端请求(TEARDOWN request):---------请求关闭会话

			"TEARDOWN rtsp://192.168.1.122/TestSession RTSP/1.0"
			"CSeq: 6"
			"User-Agent: LibVLC/1.1.9 (LIVE555 Streaming Media v2011.01.06)"
			"Session: 68422540987712"
	+ 服务器回应(TEARDOWN response):

			"RTSP/1.0 200 OK"
			"CSeq: 6"
			"Session: 68422540987712"
			"Connection: Close"
			""

---
######*参考文献*
+ 【1】[RTSP 协议分析 （一） 博水](http://www.cnblogs.com/qingquan/archive/2011/07/14/2106834.html)
+ 【2】[rtsp 交互流程](http://blog.csdn.net/wl_fln/article/details/6444261)


{% include JB/setup %}