---
layout: post
title: "Ubuntu通过Bing壁纸自动更新"
description: "用代码给生活家点小情调。"
category: "Kaleidoscope"
tags: ["Kaleidoscope", "Life"]
---

在我自己的Nexus 7上面自己写了一个小程序，每天可以定时获取Bing当日的最新壁纸。每天早上起来看到都是不一样的画面，还是很开心的。

后来，也想自己写一个桌面的。本来想说用Qt去写，这样就能同时在我的Ubuntu和公司的Windows运行了。写了一半，就是读取图片这部分，设置壁纸这块不同的系统需要根据系统自身提供的接口才能修改，Windows有点麻烦，当时也有点事情，暂且作罢。

之前我的想法比较复杂，希望通过HTTP得到图片之后，将其转换成二进制编码，通过设置壁纸接口直接修改。这样做的好处是不需要保存临时文件，就是编码比较复杂。后来找了一个用Python写的Qt代码。他的思路是将文件保存到本地临时目录里面，然后通过Linux命令来修改壁纸。如此一来，省去了Linux系统接口编码的繁琐。

他的代码直接下载下来是有问题的，如果没有记错的话，是最后的`madWindow`函数对齐错了，加个缩进就可以了。后来，我还改了一下壁纸文件目录，我放到了`home`下，现在觉得放在`/tmp/`更好一点。最后应该是一个Linux修改壁纸命令`gsettings set org.gnome.desktop.background picture-uri "file:///home/%s/%s.jpg"`，并没有去研究这个，大家有兴趣可以看一下。

![IMG-THUMBNAIL](http://cyeam.qiniudn.com/bing.png)

本文所涉及到的完整源码请[参考](https://github.com/mnhkahn/python_code/blob/master/bing.py)。

---
+ 【1】[Ubuntu下实现用Python开机自动更新壁纸为bing壁纸](http://www.linuxidc.com/Linux/2014-06/103854.htm)

{% include JB/setup %}