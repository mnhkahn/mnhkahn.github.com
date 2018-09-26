---
layout: post
title: "查看自己的top10 Linux命令"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeam/shell.jpg"
description: "在V2EX发现的有趣的查看自己输入历史的top10 命令。"
category: "Linux"
tags: ["linux", "shell"]
---

	history | awk '{CMD[$2]++;count++;}END { for (a in CMD)\
	print CMD[a] " " CMD[a]/count*100 "% " a;}' | grep -v "./" \
	| column -c3 -s " " -t | sort -nr | nl | head -n10

> [来晒晒你使用过的 Linux 命令的 top 10 吧! - V2EX](http://www.v2ex.com/t/109153#reply26)

我的结果是：

	 1	133  26.5469%   git
     2	111  22.1557%   sudo
     3	58   11.5768%   cd
     4	53   10.5788%   ls
     5	24   4.79042%   grep
     6	22   4.39122%   go
     7	10   1.99601%   jekyll
     8	10   1.99601%   gor
     9	10   1.99601%   adb
    10	7    1.39721%   ssh

最近都在GitHub Pagers上面写论文，所以git和jekyll都榜上有名。。。

不过感觉次数少了点，查了一下，`history`默认保存500条命令(可以通过`echo $HISTSIZE`查看)。不过直接用`history`命令，能看到多于500条的命令，看到了519条。原因是如果你不注销或者关机，那么执行`hisotry`命令 只要永久保存，可能记录大于500。如果你注销了以后，.bash_history只保存最近的500条记录。

`awk`是一个强大的文本分析工具。`awk`其名称得自于它的创始人 Alfred Aho 、Peter Weinberger 和 Brian Kernighan 姓氏的首个字母。`awk`工作流程是这样的：读入有`'\n'`换行符分割的一条记录，然后将记录按指定的域分隔符划分域，填充域，$0则表示所有域,$1表示第一个域,$n表示第n个域。默认域分隔符是`"空白键"` 或 `"[tab]`键",所以$1表示登录用户，$3表示登录用户ip,以此类推。

> [linux awk命令详解 - 简单，可复制](http://www.cnblogs.com/ggjucheng/archive/2013/01/13/2858470.html)

`head`可以用来查看文件头部指定行数，所以最后的`head -n10`就是要显示前10行，就是前10个，去掉就是显示全部了。