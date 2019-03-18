---
layout: post
title: "Docker(Linux) 环境下如何配置 host"
description: "之前遇到一个问题，docker里面配置了 host，Go 程序发起 http 请求的时候没有用配置的 host，整理了一下原因。"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1552906016/cyeam/dns.png"
category: "Go"
tags: ["go","http"]
---

* 目录
{:toc}
---

### Linux 系统如何配置 host？

如果你有管理员权限

	sudo vi /etc/hosts

增加你想配置的 host，保持并退出

	127.0.0.1 cyeam.com

可以通过`ping`命令来检测一下

	ping cyeam.com

大部分情况到这里就结束了。

### Docker 里配置没起作用

测试俊哥在自己的 Docker 里搭起了我的服务，但是发现发 http 请求没有按照预想的用配置好的 host 发。但是我在自己的 Mac 上面配 host 是可以的。下面讲一下原因，特别感谢俊哥的研究。

### /etc/nsswitch.conf

Linux 系统解析域名，支持本地文件配置，也支持通过域名服务器查询。本地文件配置的方式就是第一步提到的 /etc/hosts。而域名解析服务器的配置则在 /etc/resolv.conf 中。此外，还有一个重要的文件 /etc/nsswitch.conf，它可以用来配置域名解析的优先级。

	hosts:          files dns

我的开发机上面是这样，意思是先读取文件，如果文件里没有从 dns 服务器查询。

而我们的情况是 docker 里面没有这个文件，当系统没有这个文件时，Go 的表现是：

	// If /etc/nsswitch.conf doesn't exist or doesn't specify any
	// sources for "hosts", assume Go's DNS will work fine.
	if os.IsNotExist(nss.err) || (nss.err == nil && len(srcs) == 0) {
		if c.goos == "solaris" {
			// illumos defaults to "nis [NOTFOUND=return] files"
			return fallbackOrder
		}
		if c.goos == "linux" {
			// glibc says the default is "dns [!UNAVAIL=return] files"
			// https://www.gnu.org/software/libc/manual/html_node/Notes-on-NSS-Configuration-File.html.
			return hostLookupDNSFiles
		}
		return hostLookupFilesDNS
	}

它会按照`dns [!UNAVAIL=return] files`的默认值来查询。也就是先查询 dns，如果 dns 服务器不可用，再查询本地 hosts 文件。

> The system takes the action associated with the STATUS (return) if the DNS method does not return UNAVAIL (!UNAVAIL)—that is, if DNS returns SUCCESS, NOTFOUND, or TRYAGAIN. As a consequence, the following method (files) is used only when the DNS server is unavailable: If the DNS server is not unavailable (read the two negatives as "is available"), the search returns the domain name or reports that the domain name was not found. The search uses the files method (check the local /etc/hosts file) only if the server is not available.

---

一个想当然的问题最后引出了这么多不了解的新知识，真好。

---


{% include JB/setup %}
