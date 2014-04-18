---
layout: post
title: "基于Android的移动VoIP视频通话系统——Android的架构"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: ""
category: "Postgraduate design"
tags: ["Postgraduate design", Paper"]
---

在2008年Google宣布Android SDK 1.0发布的时候，我们肯定不会想到，短短两三年间，不起眼的小机器人已经占据了手机市场半壁江山——凭借开放的策略。智能手机实现真正的平民化，彻底改变了手机市场的版图。

Android系统有如下特点：

###基于Linux系统

Android基于Linux系统。Android也继承了Linux的可移植性、安全性等特性。

###Dalvik虚拟机

传统的Java虚拟机(JVM)是为了适应各种不同的环境而设计的，强调泛用性。但Dalvik VM是专门为Android设计的虚拟机。采用此虚拟机可以降低开发难度，使用Java语言开发，一些Java已有的类库可以移植到Android平台下直接使用。Java的JNI可以直接调用C/C++类库，在Android(Linux)下是.so文件，也方便调用原本的C/C++类库。Java语言本身就方便于代码管理，模块化开发。基于这些特性，有了Dalvik VM。编译器会自动将Java代码编译成Dalvik byte code，而不同于传统的Java byte code，然后再Dalvik虚拟机上执行Dalvik byte code。

![IMG-THUMBNAIL](http://cyeam.qiniudn.com/dalvik.png)

当然，这样设计也会产生一些开发问题。Dalvik虚拟机并不是JVM，并没有对于跨平台进行设计，所以一些平台相关的Java包，是不能直接放到Android上直接使用的，需要进行移植。Dalvik虚拟机只是使用了Java语法，而很多原生的Java包没有办法使用。


###Android的五层架构
Android操作系统就像一个五层蛋糕，每一层都有自己的特性和用途。

![IMG-THUMBNAIL](http://cyeam.qiniudn.com/android_framework.png)

+ 2.1、Linux Kernel

Android基于Linux 2.6提供核心系统服务，例如：安全、内存管理、进程管理、网络堆栈、驱动模型。Linux Kernel也作为硬件和软件之间的抽象层，它隐藏具体硬件细节而为上层提供统一的服务。

如果你学过计算机网络知道OSI/RM，就会知道分层的好处就是使用下层提供的服务而为上层提供统一的服务，屏蔽本层及以下层的差异，当本层及以下层发生了变化不会影响到上层。也就是说各层各司其职，各层提供固定的SAP（Service Access Point），专业点可以说是高内聚、低耦合。

如果你只是做应用开发，就不需要深入了解Linux Kernel层。

+ 2.2、Android Runtime

Android包含一个核心库的集合，提供大部分在Java编程语言核心类库中可用的功能。每一个Android应用程序是Dalvik虚拟机中的实例，运行在他们自己的进程中。Dalvik虚拟机设计成，在一个设备可以高效地运行多个虚拟机。Dalvik虚拟机可执行文件格式是.dex，dex格式是专为Dalvik设计的一种压缩格式，适合内存和处理器速度有限的系统。

大多数虚拟机包括JVM都是基于栈的，而Dalvik虚拟机则是基于寄存器的。两种架构各有优劣，一般而言，基于栈的机器需要更多指令，而基于寄存器的机器指令更大。dx 是一套工具，可以將 Java .class 转换成 .dex 格式。一个dex文件通常会有多个.class。由于dex有時必须进行最佳化，会使文件大小增加1-4倍，以ODEX结尾。

Dalvik虚拟机依赖于Linux 内核提供基本功能，如线程和底层内存管理。

+ 2.3、Libraries

Android包含一个C/C++库的集合，供Android系统的各个组件使用。这些功能通过Android的应用程序框架（application framework）暴露给开发者。下面列出一些核心库：

系统C库——标准C系统库（libc）的BSD衍生，调整为基于嵌入式Linux设备
媒体库——基于PacketVideo的OpenCORE。这些库支持播放和录制许多流行的音频和视频格式，以及静态图像文件，包括MPEG4、 H.264、 MP3、 AAC、 AMR、JPG、 PNG
界面管理——管理访问显示子系统和无缝组合多个应用程序的二维和三维图形层
LibWebCore——新式的Web浏览器引擎,驱动Android 浏览器和内嵌的web视图
SGL——基本的2D图形引擎
3D库——基于OpenGL ES 1.0 APIs的实现。库使用硬件3D加速或包含高度优化的3D软件光栅
FreeType ——位图和矢量字体渲染
SQLite ——所有应用程序都可以使用的强大而轻量级的关系数据库引擎

+ 2.4、Application Framework

通过提供开放的开发平台，Android使开发者能够编制极其丰富和新颖的应用程序。开发者可以自由地利用设备硬件优势、访问位置信息、运行后台服务、设置闹钟、向状态栏添加通知等等，很多很多。

开发者可以完全使用核心应用程序所使用的框架APIs。应用程序的体系结构旨在简化组件的重用，任何应用程序都能发布他的功能且任何其他应用程序可以使用这些功能（需要服从框架执行的安全限制）。这一机制允许用户替换组件。

所有的应用程序其实是一组服务和系统，包括：

视图（View）——丰富的、可扩展的视图集合，可用于构建一个应用程序。包括包括列表、网格、文本框、按钮，甚至是内嵌的网页浏览器
内容提供者（Content Providers）——使应用程序能访问其他应用程序（如通讯录）的数据，或共享自己的数据
资源管理器（Resource Manager）——提供访问非代码资源，如本地化字符串、图形和布局文件
通知管理器（Notification Manager）——使所有的应用程序能够在状态栏显示自定义警告
活动管理器（Activity Manager）——管理应用程序生命周期,提供通用的导航回退功能

+ 2.5、Applications

Android装配一个核心应用程序集合，包括电子邮件客户端、SMS程序、日历、地图、浏览器、联系人和其他设置。所有应用程序都是用Java编程语言写的。更加丰富的应用程序有待我们去开发！

---
######*参考文献*
+ 【1】《Learning Android》 马尔科·加尔根塔 电子工业出版社 ISBN: 9787121172632
+ 【2】[Android开发之旅：android架构 吴秦](http://www.cnblogs.com/skynet/archive/2010/04/15/1712924.html)

{% include JB/setup %}