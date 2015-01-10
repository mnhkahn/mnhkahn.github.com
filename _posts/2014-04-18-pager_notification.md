---
layout: post
title: "Android 通知"
figure: "http://cyeam.qiniudn.com/android.jpg"
description: ""
category: "Postgraduate"
tags: ["Postgraduate design", "Evaluate", "Android"]
---

Android在通知栏方面相对于苹果来说比较开放。允许服务常驻后台，所以能够方便实现消息推送。而苹果的进程等待几分钟没有操作之后，就会自动退出，远程发送消息只能经过苹果的远程推送实现。鄙人曾经在公司尝试开发百万级的消息推送接口，说来惭愧，没能成功。

##1. 显示通知

发送通知需要用到`android.app.NotificationManager`和`android.app.Notification`。调用流程如下：

    NotificationManager mNotificationMgr = (NotificationManager) mContext
                .getSystemService(Context.NOTIFICATION_SERVICE);
    Notification notification = new Notification();
    // 初始化notifacation
    mNotificationMgr.notify(type, notification);

Notifaction提供flags、icon、sound等设置通知的类型，图标和声音。可以通过设置contentIntent为通知增加点击启动的Activity。

##2. 远程推送通知

关于远程推送，发现有使用IBM的MQTT的，还有建立长连接的。待我调研一翻，再来修改这里。

---

######*参考文献*
+ 【1】[Android中通知的使用-----Notification详解](http://blog.csdn.net/qinjuning/article/details/6915482)
+ 【2】[Notification - Android Developers](http://developer.android.com/reference/android/app/Notification.html)
+ 【3】[NotificationManager - Android Developers](http://developer.android.com/reference/android/app/NotificationManager.html)
+ 【4】[Push Notification （2）HTTP长连接](http://www.360doc.com/content/12/1121/14/7635_249300653.shtml)

{% include JB/setup %}
