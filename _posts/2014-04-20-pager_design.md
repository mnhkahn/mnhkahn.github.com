---
layout: post
title: "基于流媒体的对讲机系统——系统总体设计"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: ""
category: "Postgraduate design"
tags: ["Postgraduate design", Paper"]
---

根据上一章的需求分析，再根据Android平台特性进行优化，得到如下改进：

+ 根据上一章的权限和分析，系统需要三个角色类型：指挥角色、协调角色、默认角色。系统需求要求的在线设备并不多，而过多的设备会影响通信逻辑和效率，本课题支持10个在线设备，包括一个指挥角色、7个协调角色和2个默认角色。系统程序启动的时候要进行选择各自的角色，并将其保存在配置文件当中，然后系统为其进行自动SIP注册。SIP注册需要的用户名可以在配置选项中自行设置。
+ 当需要开始进行对讲时，由指挥角色向其他所有设备进行发起SIP请求，被呼叫方需要进行接听操作，以避免不必要的麻烦。
+ 接通之后，是进行的音频通话。在SIP链接建立后，按下音量-，进行发送视频操作。系统默认是进行音频通话，在有视频通话需求的时候再进行视频连接，这样来减少带宽的占用。
+ 在按下音量+键之后，指挥角色可以进行抢占式发言。其它所有设备的话筒采用静音操作，音频和视频停止发送。
+ 协作模块可以直接使用Android提供的Dialog对话框来实现。由指挥角色发起，协作的内容要在配置项中进行预先的设置。
+ 考虑到网络的不稳定性，为了保证实时性，需要增加配置音频和视频采样率的模块。


![IMG-THUMBNAIL](http://cyeam.qiniudn.com/framework.png)

+ 系统从cInterphone这个Activity启动。该Activity包含3个Fragment，分别是Favourite Fragment、History Fragment、Contact Fragment。
+ 其中，Favourite Fragment和History Fragment关联到两个SQLite数据库表Favourite和History。使用适配器ContactAdapter进行数据关联显示。
+ cInterphone的ActionBar上面，还增加了设置模块按钮，可以启动Settings这个Activity，用于进行手动配置用户名和SIP服务器。
+ Recevier继承自BroadcastReceiver，使用单件模式和观察者模式，用于获取cInterphoneEngine的单件实例和响应状态，例如：进入视频界面，通知栏更改状态等等。
+ cInterphoneEngine模块负责SIP协议栈的封装，用于注册SIP服务器、发起会话、结束会话等会话控制操作。
+ 在准备建立会话时，Receiver会启动InCallScreen，用于显示呼叫或者被呼叫界面。会话建立成功后，启动VideoCamera Activity进行视频通话。
+ VideoCamera Activity会启动RtspServer Service用于发送音视频RTSP流。并且使用MediaPlayer读取RSTP流。

{% include JB/setup %}