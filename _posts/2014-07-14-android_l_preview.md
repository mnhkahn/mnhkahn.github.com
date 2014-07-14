---
layout: post
title: "Android L 预览版"
description: "在微博上面，各种所谓关注科技的官微都在发各种Android L的更新截图，各种吵。我也就没忍住，去刷了一把。然后今天又刷了回来。"
figure: "http://cyeam.qiniudn.com/7d3f0ccdjw1eic56ksdlnj20fp07fmxp.jpg"
category: "Android"
tags: ["Android"]
---

> 官方安装教程 https://developers.google.com/android/nexus/images#instructions
> 官方下载系统镜像地址 http://developer.android.com/preview/setup-sdk.html

我的平板是Nexus 7（2013版），选择razor下载即可。安装也很简单。将设备通过USB连上电脑。这里可能需要配置驱动，如果需要，请参考[《Linux Mint下安装Nexus 7 驱动》](http://blog.cyeam.com/kaleidoscope/2014/02/01/linux_android_drivers)

+ 启动设备进入fastboot模式。`adb reboot bootloader `
+ 解压镜像文件
+ 执行脚本flash-all。`./flash-all.sh`

安装挺简单的，第一次这么安东西，挺爽。自打安上之后，我就开始找微博上面提到的东西。最喜欢的那个就是开机画面，然后再我真机上面看，还有竖屏变横屏时的问题。。。截了两张图：

![IMG-THUMBNAIL](http://cyeam.qiniudn.com/Screenshot_2014-07-14-21-22-04.png)
![IMG-THUMBNAIL](http://cyeam.qiniudn.com/Screenshot_2014-07-14-21-22-04.png)

接着就是更都的问题。微博启动不了，QQ各种显示问题。虽说是预览版，但是跟我想像还是差了好多。。。今天晚上把系统刷回了4.4。不过电池确实好了许多。



---

######*参考文献*
+ 【1】[nginx启动，重启，关闭命令 - 晓风残梦](http://www.cnblogs.com/derekchen/archive/2011/02/17/1957209.html)
+ 【2】[nginx conditional proxy pass - Stackoverflow](http://stackoverflow.com/questions/7878334/nginx-conditional-proxy-pass)

{% include JB/setup %}