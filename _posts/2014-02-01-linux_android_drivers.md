---
layout: post
title: "Linux Mint下root Nexus 7"
figure: "http://cyeam.qiniudn.com/writing_udev_rules.jpg"
description: "为了能够让我的Nexus 7翻墙，我决定root。是在Linux Mint下root Android。看着也不难，结果搞了好几天。越到一半机子驱动问题，没办法继续了，看着一块砖头放在那，真叫个急啊。root成功后，twitter还是上不去，还得再写一篇文章来总结一下Android翻墙。"
category: "Kaleidoscope"
tags: ["Nexus 7", "Root Android", "Mint"]
---

整个越狱的大体过程，是按照这篇文章[Steps to Root Nexus 7 2013 in Linux](http://itsfoss.com/root-nexus-7-2013-ubuntu-linux/)来做的。先开始讲的挺详细的，最后在Linux下Android设备驱动和fastboot mode下启动少写了一些，对于我这种小白来讲果断是不能自己处理的，所以搞了好几天才搞定。

+ 里面用到的TWRP无法下载，使用[百度网盘](http://pan.baidu.com/wap/link?uk=3593604652&shareid=453410427&third=0)提供的下载

**在一切都搞定，执行最后一步的时候，出现了`<wait for devices>`的错误，是因为Linux下设备的驱动问题，没有配置好。在Windows在需要安装设备对应的驱动就能搞定，Mac下都不需要操作，而Linux下需要配置udev才能正常运行。**

+ 简单的说一下，Linux是通过udev来管理设备的，udev的入门资料可以参考——[《使用 udev 高效、动态地管理 Linux 设备文件》](http://www.ibm.com/developerworks/cn/linux/l-cn-udev/)。一些基本的udev配置文件规则可以在这里找到。

+ 接着是去写配置文件。基本上所有Google到的文章里面都说了要在`/etc/udev/rules.d`里面创建`51-android.rules`，里面的写法也是基本一致的，但是没有说明为什么这么写，所以可能具体到个人，那样复制过来就不行了。

+ 文件`51-android.rules`命名的缘由——[《为什么是“51-android.rules”？》](http://www.cnblogs.com/frydsh/archive/2013/03/07/2949089.html)

+ `51-android.rules`的配置。[《Adding udev rules for USB debugging Android devices》](http://www.janosgyerik.com/adding-udev-rules-for-usb-debugging-android-devices/)

    + 使用命令`lsusb`找到Android设备的Bus和Device

            Bus 003 Device 006: ID 18d1:4ee2 Google Inc. Nexus 4 (debug)

    + 看到上面的Google的Bus是`003`，Device是`006`，Linux是通过文件来管理设备的，所以该Android设备对应的文件就是`/dev/bus/usb/003/006`，查看其文件权限。`ls -l /dev/bus/usb/003/006`查看其文件权限。

            crw-rw----+ 1 root audio 189, 261  2月  2 14:56 /dev/bus/usb/003/006

    + 编辑`/etc/udev/rules.d/51-android.rules`。该文件内需要添加用户组和用户名，之前不确定是什么，试了好几次，也不知道对了没有，可以通过上一步直接查看到其权限。我的配置如下：

            SUBSYSTEM=="usb", ATTR{idVendor}=="18d1", ATTR{idProduct}=="d001", MODE="0666", OWNER="root", GROUP="plugdev", SYMLINK+="android%n"

    + 按照之前查看到的设备vendor和productid，还有访问权限，在配置完之后，重新插上设备，会在`/dev`目录下生成`android`的文件，其后面会带一个数字。*前面几步贴的结果都是配置好之后重新执行命令得到的结果，可能不准确*。 

   
+ 如果在`/dev`下面生成了以`android`开头的文件，表明已经配置好了，可以通过`adb devices`看到设备序列号了。接着是在fastboot mode下启动系统。那篇文章中并没有强调说在fastboot mode下执行，而我也不懂。。。所以，这个也搞了很久还发现的。。。还是靠这个提问[《Android Fastboot devices not returning device》](http://stackoverflow.com/questions/8588595/android-fastboot-devices-not-returning-device)，才想到可能是在fastboot mode下执行，因为按照之前的步骤，都是在recovery mode下，所以切换了mode，果断可以了。此时，成功的标志是`fastboot devices`会返回设备序号。

---

<div id="stacktack-21499972"></div>

######*参考文献*
+ [ubuntu下galaxy nexus的fastboot连接不上的问题](http://blog.csdn.net/gexueyuan/article/details/8720570)
+ [Setting up a Device for Development](http://developer.android.com/tools/device.html)
+ [51-android.rules](https://github.com/M0Rf30/android-udev-rules/blob/master/51-android.rules)
+ http://www.janosgyerik.com/adding-udev-rules-for-usb-debugging-android-devices/
+ https://code.google.com/p/51-android/

{% include JB/setup %}