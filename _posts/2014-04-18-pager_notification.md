---
layout: post
title: "基于Android的移动VoIP视频通话系统的设计与实现——通知模块"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: ""
category: "Postgraduate design"
tags: ["Postgraduate design", "Evaluate"]
---

在状态栏(Status Bar)中，通知主要有两类(使用FLAG_标记)：
 
+ 正在运行的事件
+ 通知事件

常量：

      //表示发送一个Notification的所携带的效果
     DEFAULT_ALL              使用默认字段
     DEFAULT_LIGHTS       默认闪光
     DEFAULT_SOUND      默认声音(uri，指向路径)
     DEFAULT_VIRATE       默认震动，后来得知需要添加震动权限VIBRATE： android.permission.VIBRATE
 
PS：以上的效果常量可以累加,即通过mNotifaction.defaults |=DEFAULT_SOUND   (有些效果只能在真机上才有，比如震动)

    //设置Flag位
    FLAG_AUTO_CANCEL           该通知能被状态栏的清除按钮给清除掉
    FLAG_NO_CLEAR                  该通知不能被状态栏的清除按钮给清除掉
    FLAG_ONGOING_EVENT      通知放置在正在运行

---
######*参考文献*
+ [Android中通知的使用-----Notification详解](http://blog.csdn.net/qinjuning/article/details/6915482)
+ [Notification | Android Developers](http://developer.android.com/reference/android/app/Notification.html)

{% include JB/setup %}