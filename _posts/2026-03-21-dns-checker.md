---
layout: post
title: "最近切换域名服务器，为了查问题用了很多方法，这里记录下"
description: "如果怀疑是域名服务器异常，如何快速排查？"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1774100673/clipboard_1774100667693_4oyzo79tr.webp"
category: "CSS"
tags: ["CSS", "Tool", "Mobile"]
---

- 目录
{:toc}

---

Chrome浏览器报错如下，中间走了很多网路，TLS配置、QUIC、服务器限流等等，确实有知识盲区，领取Chrome报错也太不清楚了。。。

```
检查网络连接
检查代理服务器和防火墙
ERR_CONNECTION_CLOSED 访问网页有问题
```

1. 确定是不是真有问题
   1. [https://downforeveryoneorjustme.com/](https://downforeveryoneorjustme.com/);
   2. [Ping](https://ping.chinaz.com/www.cyeam.com);

2. 查询域名服务器，选择NS类型
   1. [ITDog](https://linux.die.net/man/8/dig)
   2. `while true; do dig cyeam.com NS +short; sleep 20; done`

3. 查询解析结果，AA、AAAA
   1. [ITDog](https://linux.die.net/man/8/dig)
   2. `while true; do dig cyeam.com AAAA +short; sleep 20; done`

4. 用[IP138](https://www.ip138.com/)检测解析出来的结果是否正确，拿着IP查询所在地，是Cloudflare还是其他服务器；

5. 检查浏览器DNS解析结果
   1. `chrome://net-internals/#dns` 输入域名cyeam.com查询

因为是偶发问题很难复现，最后问题就是出现在第5步，当出问题时查了下域名记录，结果如下，其中多了`ech_config_list`，这就是问题所在，该记录携带了 Cloudflare 的 ECH 加密配置和 Cloudflare 边缘节点 IP，Chrome 优先用这个 Cloudflare 节点发起连接；但我们无法正常使用ECH，收到请求后直接关闭了 TCP 连接。其他人也需要了[类似问题](https://v2ex.com/t/1077702)，Cloudflare无法在页面关闭，需要用命令行。

```
Resolved IP addresses of "note.cyeam.com": ["66.241.124.103","2a09:8280:1::1:d40a"].
Alternative endpoint: {"alpns":["h2","http/1.1"],"ech_config_list":"fdsafafdafadsfadsfdsa","ip_endpoints":["1.1.1.1"]}
```

{% include JB/setup %}
