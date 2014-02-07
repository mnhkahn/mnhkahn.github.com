---
layout: post
figure: "http://cyeam.qiniudn.com/Linus-Torvalds-Fuck-You-Nvidia.jpg"
title: "Linux Mint 64bit下安装Dota 2"
description: "现在的新电脑大都用的双显卡，一张Intel的集成显卡，一张Nvidia的独立显卡。默认运行集成显卡，在玩游戏这些需要大量图形计算的时候运行独立显卡。这个自动切换的过程在Windows和Mac环境下，都是由Nvidia的显卡驱动自动完成的，而在Linux下，伟大的Nvidia却不提供这样的切换功能了。所以Linus问候了它。"
category: "Toss"
tags: ["Cyeam", "Linux", "Steam", "Dota2", "Toss"]
---

![IMG-THUMBNAIL](http://cyeam.qiniudn.com/dota-2-logo.jpg)

为了能在Linux下玩Dota 2，前前后后折腾了好几个礼拜，先写一下Linux下安装环境的难度，这也是这个解决问题的思路。

+ Linux下Nvidia显卡驱动不支持自动切换显卡的功能，需要安装第三方驱动。Nvidia显卡切换技术叫做Optimus，也就是擎天柱
现在在Linux下面柱子无效，因此第三方开发团队的开发了好基友Bumblebee大黄蜂；
+ Bumblebee在开发的时候也对Nvidia原生驱动进行了修改，所以还需要安装第三方的驱动（如果已经安装了Nvidia的驱动，需要删除）;
+ 最恶心人的不是这些还不算。Steam是开发的32位版本，而如果你是64位电脑，那么还要注意，Steam提供的解决方案默认是32位的解决方案，所以你还得去找找64位的安装方案。这也是一直让我纠结的地方，所有都安好了，就是一直报错`You appear to have OpenGL 1.4.0, but we need at least 2.0.0!`，让我一直以为是OpenGL的原因，在这里绕弯子了。


#####1. 安装Bumblebee的方法参考下面的网址，我就不抄了。
http://cjenkins.wordpress.com/2013/01/01/steam-for-linux-on-optimus-enabled-computer-running-ubuntu-12-04-64bits/#install_bumblebee

#####2. 测试安装要用到glxspheres，64位系统的安装方法也比较特殊。。。
    wget http://goo.gl/L7rsGZ -O virtualgl_2.3.3_amd64.deb 
    sudo dpkg -i --force-depends virtualgl_2.3.3_amd64.deb 
    sudo apt-get -f install

运行的命令如下，也可以创建一个快捷方式到/usr/bin下，这样用起来方便一些。

    /opt/VirtualGL/bin/glxspheres64

http://www.upubuntu.com/2013/11/how-to-check-3d-acceleration-fps-in.html

#####3. 安装好之后，出现了这个问题
一般等这些都安好以后，安装提示，将运行Dota 2的命令改成`primusrun %command%`，运行Dota 2，就会出现这个错误了。

    PROBLEM: You appear to have OpenGL 1.4.0, but we need at least 2.0.0!

第一次装的时候一直一位是OpenGL的问题，今天又去查了查，无意中发现了Steam文档中的一句话：

    Note - Primus must be installed with 32-bit support because Steam for Linux (and most games downloaded from Steam) are 32-bit.

https://support.steampowered.com/kb_article.php?ref=6316-GJKC-7437

我意识到可能是我安装成64位Primus造成的。所以开始着手安装32位版本。Steam官方也没特别明确的提供，还得自己找。。。

#####4. Linux 64位系统下32位Primus安装
    sudo apt-get install primus-libs-ia32:i386

http://www.webupd8.org/2012/11/primus-better-performance-and-less.html

#####5. 查看Nvidia显卡是否启动
    lspci |grep VGA

类似结果如下

    00:02.0 VGA compatible controller: Intel Corporation 3rd Gen Core processor Graphics Controller (rev 09)
    01:00.0 VGA compatible controller: NVIDIA Corporation GF108M [NVS 5400M] (rev ff)
rev代表启动状态，ff为未启动。其他为已启动（其实电脑发热量大了，风扇开始响了，就代表启动了。。。）。
http://www.webupd8.org/2012/11/primus-better-performance-and-less.html

#####6. 跳过Training
进入Dota 2以后，还要蛋疼的强迫你Training，作为资深Dota玩家的我，果断是要跳过的啊。在Steam里面启动Dota 2的环境变量最后加上如下参数，就可以跳过了。

    +dota_full_ui 1

完整的变量如下：

    primusrun %command% +dota_full_ui 1

#####7. 游戏修改为中文界面
增加启动参数，改为完美世界的

    -perfectworld -language schinese
完整的变量如下：

    primusrun %command% +dota_full_ui 1 perfectworld -language schinese

http://www.douban.com/group/topic/41787706/

#####8. 连接完美世界服务器游戏
配置好所有的之后，可以打AI了，但是还是有问题，就是不能和人打。匹配区域只能显示欧洲、东南亚这些，匹配很久也匹配不到。

解决方案，还是修改启动参数

    -perfectworld steam

完整的变量如下：

    primusrun %command% +dota_full_ui 1 perfectworld -language schinese -perfectworld steamt

---
最后奉上游戏截图，我最爱的Pom
![IMG-THUMBNAIL](http://cyeam.qiniudn.com/dota2_pom.png)
{% include JB/setup %}