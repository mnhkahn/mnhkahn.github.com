---
layout: post
title: "基于Android的移动VoIP视频通话系统的设计与实现——ListFragment"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: ""
category: "Postgraduate design"
tags: ["Postgraduate design", Evaluate"]
---

Android Support Library(支持库)提供了包含一个API库的JAR文件，当你的应用运行在Android早期版本时，Support Library(支持库)允许你的应用使用一些最近版本的Android API。例如：Support Library提供了一个让你能在Android1.6(API level 4)或者更高的版本上使用Fragment API的版本。

从Android 3.0开始，增加了Fragment的新特性。Fragment可以放在Activity里面，一个Activity可以包含多个Fragment，这样，可以实现UI分块管理，提供了更好的交互方式。可以把Fragment理解成一个Activity的模块或者区域，它有自己的生命周期，可以接收自己的输入事件。

ListFragment继承于Fragment。因此它具有Fragment的特性，能够作为Activity中的一部分，目的也是为了使页面设计更加灵活。相比Fragment，ListFragment的内容是以列表(list)的形式显示的。

ListFragment内部拥有一个ListView，用来展示List的内容。要展示的内容和绑定的数据，使用适配器模式来实现的。创建一个适配器，用来将原始的List格式转化成要展示的List格式。

---
######*参考文献*

{% include JB/setup %}