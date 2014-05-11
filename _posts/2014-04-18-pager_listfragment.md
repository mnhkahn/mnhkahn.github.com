---
layout: post
title: "基于流媒体的对讲机系统——联系人模块开发"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: ""
category: "Postgraduate design"
tags: ["Postgraduate design", Evaluate"]
---

从Android 3.0开始，Android增加了Fragment的新特性。Fragment可以看作是Activity的子标签，一般将其放在Activity里面，一个Activity可以包含多个Fragment，这样，可以实现UI分块管理。在开发支持不同尺寸设备的Android应用的时候，这个特性尤为重要，只要为不同你给的设备设计不同的Activity布局，而内部包含相同的只是位置和大小不同Fragment，这样就能轻易实现跨平台性和更多的交互方式。可以把Fragment理解成一个Activity的模块或者区域，它有自己的生命周期，可以接收自己的输入事件。

本系统的设计充分利用了Fragment为界面交互增加的多样交互性。简化了交互难度，美化了系统界面。系统主界面由三个部分组成：联系人界面、通话记录界面、收藏界面。

Android Support Library(支持库)提供了包含一个API库的JAR文件，当你的应用运行在Android早期版本时，Support Library(支持库)允许你的应用使用一些最近版本的Android API。例如：Support Library提供了一个让你能在Android1.6(API level 4)或者更高的版本上使用Fragment API的版本。

ListFragment继承于Fragment。因此它具有Fragment的特性，能够作为Activity中的一部分，目的也是为了使页面设计更加灵活。相比Fragment，ListFragment的内容是以列表(list)的形式显示的。

ListFragment内部拥有一个ListView，用来展示List的内容。要展示的内容和绑定的数据，使用适配器模式来实现的。创建一个适配器，用来将原始的List格式转化成要展示的List格式。

---
######*参考文献*

{% include JB/setup %}