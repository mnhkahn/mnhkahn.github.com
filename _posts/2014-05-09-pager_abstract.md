---
layout: post
title: "基于流媒体的对讲机系统——摘要"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: ""
category: "Postgraduate design"
tags: ["Postgraduate design", Paper"]
---

随着近些年来只能手机的普及和网络的覆盖范围扩大，只能设备对于传统设备的革新就一直在进行中。在传统对讲机的应用中，对讲机强调实时性，在现场指挥中一直有着不可替代的作用。然而，由于对讲机所使用的频率范围较固定，故而无法保证通信的安全；而且，对讲机还受到频率和波长的衰减的影响，无法提供长距离通信；对讲机还受到技术的限制，只能提供音频通话，一直无法实现实时视频对讲。

本文设计和实现了一种基于Android系统的只能对讲机系统，在共用网络下，使用自身定制的通信协议进行实现，无法被监听窃取信息；基于互联网进行通信，不受地理位置的影响，能够轻易实现长距离传输；创造性的增加了视频通话功能。

此外，还正对对讲机实际使用中常见的场景进行了实现。传统的对讲机采用半双工通信，一直时刻只能有一部对讲机发言，其余设备只能等待其通话结束后才能发言。本课题对此问题进行了解决和优化，在紧急情况下需要抢占式发言的时候，按下音量+键就能进行抢占式通话。

有时候指挥中心需要对其余进行确认工作。传统对讲机的使用中，是通过一定的顺序进行人工语音确认，这是一个繁复和容易出错的操作。在这里可以结合到Android设备的优势进行简化：指挥中心需要确认时，会向需要确认的用户发出确认请求，在用户的设备界面上展示一个对话框，让用户进行选择确认。

对所设计的系统进行丢包率、语音质量、视频流畅度等多方面性能测试,系统均表现优异,可以在无线网络下实现流畅高清的视频通话。系统的设计方案对于Android系统下的音视频通话、UI界面设计以及SIP呼叫应用开发者有一定的借鉴作用。

关键词：对讲机，Android，SIP，H264，AAC


###Abstract
With only expand coverage in recent years the popularity of mobile phones and network equipment for traditional equipment only innovation has been in progress. In a traditional intercom applications, intercom emphasize real-time, on -site command has been an irreplaceable role. However, due to the frequency range used by walkie-talkie than fixed , and therefore can not guarantee the security of communication ; Moreover, walkie-talkies also influenced by the frequency and wavelength attenuation , can not provide long-distance communication ; walkie-talkies also subject to technical limitations, can only provide audio call , has been unable to achieve real-time video intercom .

This paper designs and implements only intercom system based on Android system , in a shared network , uses its own custom communication protocol implementation, and can not be listening to steal information ; communicate on the Internet , is not affected by geographical location, can easily achieve long distance transmission ; creative adds video call feature.

In addition, the transceiver being of practical use in the realization of a common scene . The traditional half-duplex intercom communication , there can be only one walkie-talkie has time to speak , the rest of the device can only wait to speak after the end of their conversation . The topic of this issue resolved and optimized in emergency situations when needed preemptive speech , press Volume + button can be preemptive call.

Sometimes the command center to confirm the need for the rest of the work . Traditional walkie-talkie use, artificial voice confirmed certain order , which is a cumbersome and error-prone operation. Here you can combine the advantages of Android devices can be simplified : The need to confirm the command center will send a confirmation request to the user needs identified in the user's device interface display a dialog box that allows users to select OK.

The system is designed for packet loss rate, voice quality, fluency , and many other video performance test systems are outstanding performance, you can achieve smooth HD video calls in a wireless network. System design for the Android system under the audio and video calls , UI interface design and application developers SIP call a certain reference.

Keywords : walkie-talkie , Android, SIP, H264, AAC

{% include JB/setup %}