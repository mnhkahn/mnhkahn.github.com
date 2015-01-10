---
layout: post
title: "Android Quick Start"
figure: "http://cyeam.qiniudn.com/android.jpg"
description: "毕设题目《基于流媒体的语音视频通话系统》，基于Android实现。Android基础。"
category: "Postgraduate"
tags: ["Postgraduate design", "Android", "Quick Start", "Evaluate"]
---

MediaCodec
MediaPlayer
MediaRecorder
Handler
Notification
Thread Thread.interrupted()
MulticastSocket
FileWriter http://endual.iteye.com/blog/1128541

###Activity
+ Activity 定义

> 一个Acitvity，通常是指在某一时刻，在设备上看到的单独界面。对用于而言，这就是程序的外观部分。

+ Activity Manager

> 启动一个活动可能会消耗大量资源。它可能会涉及新建一个Linux进程、为UI对象申请内存空间、从XML布局填充所有对象，以及创建整个界面。既然我们在启动一个活动上花费了这么多工夫，一旦用户离开该界面，如果只是将它销毁那就实在太浪费了。为了避免这种浪费，Android通过活动管理器(Activity Manager)来管理活动的生命周期。

+ Activity 生命周期
Android编程主要是围绕程序的状态改变做出响应。

![IMG-THUMBNAIL](http://cyeam.qiniudn.com/android_activity.png)

**启动状态**

当一个活动太不存在于内存中时，我们称其处于启动状态。
> 从启动状态到运行状态的转换是最耗时的操作，对电池续航也有直接影响。所以不要轻易销毁Activity。

**运行状态**
> 获得焦点(in focus)的Activity，是处于运行状态的，与用户进行交互。正在运行的Activity可以优先获得系统资源。

**暂停状态**
> 当Activity没有获得焦点，但是仍然显示的情况下(e.g. 上面出现了对话框)，就是暂停(pause)状态。*最好在暂停状态执行保存数据的重要工作。*

**停止状态**
> 当Activity不显示却依然驻留在内存中时(e.g. 切换到其他应用程序)，处于停止(stopped)状态。停止状态的Activity可能随时被从内存中移除。

**销毁状态**
> 销毁状态的活动不再留住于内存中。

+ 创建用户界面

创建用户界面分为声明式和编程式两种，分别用到了XML和JAVA实现。这类似于HTML和Javascript的关系。

+ Layout

> Layout负责为子元素安排位置。布局如果嵌套太深，会浪费较多的CPU时间，电池的续航也会受到影响。

**LinearLayout** 

纵向或者横向排列(layout_orientation vertical/horizontal)子元素。

**TableLayout**

类似于html中的`<table>`标签。stretch columns指定那一列展开并占据所有空间。

**FrameLayout**

将其下的子元素重叠起来，只留最后一个在外面。

**RelativeLayout**

需要为每一个子元素提供一个ID。

**AbsoluteLayout**

灵活性不够，无法自动适应。

+ Intent

> Intent是指在主要构建之间传递的消息。它们能够触发并启动一个Activity，告诉一个服务启动还是停止，或者只是简单的广播。Intent是异步的。

Intent分为显式的和隐式的两种。*explicit*需要指明接收Intent的组件。*implicit*只需指定接收者的类型。所有能完成该操作的程序”竞相“完成这个操作。

###Service
> Service运行于后台，没有任何用户界面。它们可以于Activity执行相同的操作。

+ Service 生命周期
Android编程主要是围绕程序的状态改变做出响应。

![IMG-THUMBNAIL](http://cyeam.qiniudn.com/service_lifecycle.png)

onStartCommand有三种返回值：

+ START_STICKY：sticky的意思是“粘性的”。使用这个返回值时，我们启动的服务跟应用程序"粘"在一起，如果在执行完onStartCommand后，服务被异常kill掉，系统会自动重启该服务。当再次启动服务时，传入的第一个参数将为null;
+ START_NOT_STICKY：“非粘性的”。使用这个返回值时，如果在执行完onStartCommand后，服务被异常kill掉，系统不会自动重启该服务。
+ START_REDELIVER_INTENT：重传Intent。使用这个返回值时，如果在执行完onStartCommand后，服务被异常kill掉，系统会自动重启该服务，并将Intent的值传入。

特别说明一下，Android中的Service是指在后台运行的程序，与Acitivity的区别是没有界面而已。它依然是在主线程中，并不是新创建的子线程，虽然看上去很像。一般的策略是在Service启动之后，为其单独创建一个子线程。

在Android 3.0之后，考虑到网络访问影响用户交互，Android禁止在主线程中进行网络访问。如果要实现此功能，就要像前面说的创建子线程在子线程中实现。

###Thread

###Broadcast Receiver
Broadcast Receiver是Android在系统级别对Observer模式(Pub-Sub)的实现。接收器一直等待，直到其订阅的事件发生时，才被激活。

###Content Provider
> Content Provider是应用程序之间共享数据的接口，提供了一套很好的符合CRUD(insert(), update(), delete(), query())原则的接口。数据存储与用户界面程序的分离，为系统各部分之间的组合提供了更大的灵活性。

![IMG-THUMBNAIL](http://developer.android.com/images/providers/ContactsDataFlow.png)

###Application Context
Android四大组建Activity, Service, Content Provider, Broadcast Receiver构成了整个应用程序，共同处于同一个Application Context中。允许在不同的组建中共享数据和资源。

###Design Principle(多年来开发深有体会！！！)
+ **渐进式开发**
+ **保持完整，保持可用**
+ **重构代码**

---

######*参考文献*
+ 《Learning Android》 马尔科·加尔根塔 电子工业出版社 ISBN: 9787121172632

{% include JB/setup %}
