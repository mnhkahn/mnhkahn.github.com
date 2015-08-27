---
layout: post
title: "too many open files错误"
description: "虽然一直在Linux下开发服务，但是说实话，Linux的东西我基本不懂。这次这个问题的解决，让我稍微知道一些东西了。"
category: "Golang"
tags: ["Golang"]
---

大家都知道，最近我模仿binux大婶的`pyspider`的害羞组在线上跑了一段时间了。后来加入了一些新的东西，比如代理池等。看瞅着代码越来越靠谱了，结果突然有一天，发现抓取停止了，紧接着去看日志：

	2015/08/12 23:18:22 Post http://api.duoshuo.com/posts/import.json: dial tcp: lookup api.duoshuo.com: too many open files
	
作为一个菜鸟，我哪知道这是啥啊。后来用Google去搜，发现这是Linux套接字占满了。在目录`/proc/{{.PID}}/fd/`下，里面有该进程所有打开的文件标识符相关文件，套接字也属于文件的一种。默认Linux下规定每个进程的最大socket并发数是1024，就是对打开的文件有所限制。我最早是通过进入该目录，使用命令`ll | wc -l`查看当前进程的socket连接数。

这一看就是有东西申请了没释放，果断重启了服务好了。但是到底是哪里没释放，我还是不得而知。只能是用Google继续查，我懂得少，查了很多东西，把结论说一下。

在`/proc/net/tcp`文件里，保存的是当前计算机的TCP协议连接，我这边服务器的结果如下：

	 sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode
	276: BE848368:80E5 2F80CFB7:0050 08 00000000:000019E4 00:00000000 00000000  1000        0 3748204 1 ffff8800182c1c00 116 4 30 10 -1
	
然后就是换算IP，这里面本地和远程IP都是16进制的，并且是倒着排的，换算完的本地IP是104.131.132.190:32997(BE848368:80E5)，远程IP是183.207.128.47:80(2F80CFB7:0050)，说明我的计算机连接这个IP没有正常断开。查了一下这个IP，他是我用的西祠代理里面提供的一个，说明代理那部分新写的代码有问题。

后来又得知，用`netstat`命令也成，而且比这个更牛逼。我一般还会用`-p`参数，这个能看到连接相关的进程，别的参数我也不懂了，大家想知道就Google把。`netstat -p | grep haixiuzu`这个就能看到我的害羞组程序的连接。当时显示出的一个结果如下表。此外，还发现一次抓取结束后会有30个CLOSE_WAIT状态的连接，其中`118.144.80.201`这个IP有20个，量也不小，他是多说API的IP，说明保存到多说的时候HTTP也没有释放连接。

	Proto Recv-Q Send-Q Local Address         Foreign Address     State      PID/Program name
	tcp        1      0 104.131.132.190:60059 118.144.80.201:http CLOSE_WAIT 14397/haixiuzu
	
网上查了查，大神们都说如果`Recv-Q`和`Send-Q`有不为0的就说明不对，这是发送和接受队列，说明一直在等待，一般需要两个小时操作系统才会自动释放这个资源，但是据我观察，两个小时也不会正常，要不也不会增加到1024个。

问题大体了定位好了，然后就是定位和修复。又去看了TCP连接的3次握手和断开的4次握手，大概猜测是握手握了一半没继续握。又去看了看Golang的`net/http`包，断开连接就是`resp.Body.Close()`，我没写这个，抱着试一试的态度改了一下，发现TCP连接恢复正常了。。。

我自己造的这个轮子还是可以的，让我学到了TCP的一些皮毛，还是很有成就感的。

本文所涉及到的完整源码请[参考](https://github.com/mnhkahn/maodou)。

{% include JB/setup %}