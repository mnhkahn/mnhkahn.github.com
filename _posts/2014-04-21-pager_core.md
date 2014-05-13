---
layout: post
title: "基于流媒体的对讲机系统——核心引擎"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: ""
category: "Postgraduate design"
tags: ["Postgraduate design", Paper"]
---

本课题是一个庞大的系统，为了降低系统耦合度，需要将各个子模块进行独立开发和封装。最后要对整个系统进行整合，连通各个子模块，使其能协同完成任务。前面已经介绍了系统界面、系统配置模块、数据库模块、系统通知模块，此外，还有流媒体传输模块，这些模块需要复杂的消息传输，如果随意调用，将会导致耦合度太高，需要进行特殊设计完善通信机制。

![IMG-THUMBNAIL](http://cyeam.qiniudn.com/service_framework.png)


+ Receiver 对于系统不同的状态进行响应。可以给予用于以更好的体验。系统进入不同的状态，会有不同的响应模式，例如通知栏和切换到不同的响应界面。使用广播实现。广播Broadcast是一种Android提供的系统级别的进程间通信功能，使用的是观察者设计模式。广播事件的接收要通过提前注册好的广播接收器和广播过滤器实现。
    
    ![IMG-THUMBNAIL](http://cyeam.qiniudn.com/receiver.png)

    本课题通信逻辑较复杂，按照有限状态机设计可以简化流程。为系统设计出不同的状态，每当执行流程到需要修改状态的时候，调用`onState`切换系统状态：

    + 空闲状态`UA_STATE_IDLE`；
    + 对讲机工作状态`UA_STATE_IN_CALL`
    + 对讲机请求呼入状态`UA_STATE_INCOMING_CALL`；
    + 对讲机请求呼出状态`UA_STATE_OUTGOING_CALL`。

    此外，还要对于界面反馈进行设计，不同的系统状态系统界面要有不同的对应的反馈：

    + 对讲机呼叫未接来电通知`MISSED_CALL_NOTIFICATION`；
    + 对讲机SIP注册中通知`REGISTER_NOTIFICATION`；
    + 对讲机SIP注册服务器成功通知`REGISTER_SUCCESS_NOTIFICATION`；
    + 对讲机SIP注册服务器失败通知`REGISTER_FAILURE_NOTIFICATION`。

+ cInterphoneEngine 主要负责调用SIP协议栈，要针对MjSIP进行封装，提供注册、注销、发起会话请求、接受/拒绝/结束会话的流程，控制SIP通信的流程。

    对讲机注册SIP服务器要随着系统界面的启动而进行，这样能并发的初始化系统UI和SIP进行注册:

    + 初始化核心引擎主要在两种情况下进行，在CInterphone主Activiy启动时，在onCreate启动函数中启动，当用户修改配置信息，例如SIP服务器地址和端口等信息后，要重新注册。要重载`onSharedPreferenceChanged`函数，对配置信息的修改进行响应；
    + 初始化过程包括初始化SIP协议栈，获取配置文件中的服务器地址和端口等信息，通过网卡获取本机IP地址，初始化得到本机SIP信息并封装到UserAgent当中；
    + 在CInterphone主Activity的onStart启动函数中启动SIP注册过程，发送REGISTER消息；
    + 注册成功之后启动监听，用来监听SIP会话INVITE请求；
    + 用户发起对讲请求时，发送INVITE消息；
    + 用户选择加入对讲时，修改系统当前状态到`UA_STATE_IN_CALL`状态，解析SIP协议中所包含的SDP消息，获取到音频和视频的端口等信息，在根据得到的信息初始化RTSP服务器和RTSP客户端进行音视频通信。对方接收时同理；
    + 用户选择挂断对讲时，关闭摄像头和麦克风，关闭RTSP服务器，更改系统到`UA_STATE_IDLE`状态。

+ 控制音视频通信建立和传输。

    ![IMG-THUMBNAIL](http://cyeam.qiniudn.com/%E6%B5%81%E7%A8%8B%E5%9B%BE.png)

    本系统在会话部分又分成接收端和发送端两个子模块。发送端可以看作是RTSP服务器，要分别对语音和视频进行录制，将其解析成RTP包，然后启动RTSP服务器，通过RTSP协议进行发送。接收端要对得到的流媒体进行解包操走，得到RTP包，将RTP包解码，就得到了音频和视频文件。关于RTSP流媒体的传输将在下一节详细介绍。

+ InCallScreen 控制着SIP会话过程中的界面展示。SIP会话请求、被请求和接通后的界面流程展示。

    系统在被SIP对讲呼叫或者SIP对讲呼出时，就会从系统主界面切换到对讲界面。对讲界面又可以分为呼叫界面、呼入界面、通话界面和视频通话界面。这几个界面的切换都是由此模块完成。

    当进入会话状态后，要初始化两个SurfaceView用来展示对方的视频信息和自身的视频预览信息。

+ 对于抢占式通话和视频通话的发起事件进行注册，当音量+被按下时启动抢占式发言，当音量-被按下时进行视频通信。
+ 协作模块的消息，使用SIP消息作为载体进行发送。


{% include JB/setup %}