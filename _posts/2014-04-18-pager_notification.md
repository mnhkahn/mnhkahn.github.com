---
layout: post
title: "基于流媒体的对讲机系统——通知模块"
figure: "http://cyeam.qiniudn.com/c168.png"
description: ""
category: "Postgraduate design"
tags: ["Postgraduate design", "Evaluate"]
---

Android在通知栏方面相对于苹果来说比较开放。允许服务常驻后台，所以能够方便实现消息推送。而苹果的进程等待几分钟没有操作之后，就会自动退出，远程发送消息只能经过苹果的远程推送实现。鄙人曾经在公司尝试开发百万级的消息推送接口，说来惭愧，没能成功。

##1. 显示通知

发送通知需要用到`android.app.NotificationManager`和`android.app.Notification`。调用流程如下：

    NotificationManager mNotificationMgr = (NotificationManager) mContext
                .getSystemService(Context.NOTIFICATION_SERVICE);
    Notification notification = new Notification();
    // 初始化notifacation
    mNotificationMgr.notify(type, notification);

Notifaction提供flags、icon、sound等设置通知的类型，图标和声音。

|| *Year* || *Temperature (low)* || *Temperature (high)* ||
|| 1900 || -10 || 25 ||
|| 1910 || -15 || 30 ||
|| 1920 || -10 || 32 ||

##2. 远程推送通知

Android提供了通知(Notification)模块，出现在通知栏中，用户从屏幕上方滑下就可以看到。通知栏还可以常驻，在界面最上一层，可以使用图标说明当前状态：红色按钮代表SIP注册失败，绿色按钮代表SIP注册成功，还可以增加未接来电图标、呼叫失败图标，既直观又方便。

在状态栏(Status Bar)中，通知主要有两类(使用FLAG_标记)：
 
+ 通知事件。会发出通信的响声并且在状态栏显示图标。
+ 正在运行的事件。可以动态修改状态栏上的图标，和上一种通知的区别就是上一种可以被通过系统提供的清空通知键清除，而后一种只能在关闭程序后通过代码清除。

通知的效果可以自定义，`DEFAULT_LIGHTS`使用默认闪光，`DEFAULT_SOUND`使用默认声音，`DEFAULT_VIRATE`指默认震动模式，需要增加权限`android.permission.VIBRATE`。

以上的效果常量可以累加，通过或运算符可以通过为一个值附上多个参数，即通过`mNotifaction.defaults |=DEFAULT_SOUND`增加，达到传入动态多个参数的效果。

本课题中，会用到这两种通知类型。系统常驻的通知，用来通知SIP注册情况，使用户方便判断使用流程。而未接来电、呼叫失败等，使用通知事件展示，此通知只要被用户看到一次即可，不需要常驻。这两种模式的设置也很简单，常驻类型使用`FLAG_ONGOING_EVENT`，通知事件使用`FLAG_AUTO_CANCEL`。

---

######*参考文献*
+ 【1】[Android中通知的使用-----Notification详解](http://blog.csdn.net/qinjuning/article/details/6915482)
+ 【2】[Notification | Android Developers](http://developer.android.com/reference/android/app/Notification.html)
+ 【3】[NotificationManager | Android Developers](http://developer.android.com/reference/android/app/NotificationManager.html)

{% include JB/setup %}