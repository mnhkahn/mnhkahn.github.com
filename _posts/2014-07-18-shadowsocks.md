---
layout: post
title: "Linux Mint 下ShadowSocks安装试用"
description: "自从6月份开始，上网越来越难。goagent基本废了，只能另寻它法。"
category: "Kaleidoscope"
tags: ["Life"]
---

随着墙越垒越高，梯子也得赶得上趟才行。发现现在各路神仙都是在用ShadowSocks（简称SS）。

它与goagent的区别就在于，goagent是用过GAE所以代理服务器。在本地，通过Chrome浏览器的插件Proxy SwitchySharp，将请求代理到本地的goagent客户端，一般是8087端口。goagent客户端再将请求发送到GAE上面，从而达到梯子的作用。GAE的域名appspot.com一直是处于无法访问的状态，而解决访问GAE服务器的方法也很简单。强大的Google服务器集群，能够做到，访问Google的URL请求，发送到任意一个Google的服务器，都能够正常工作。如果我没有记错的话，GoAgent PAC就是用的这个方法。也就是说，只要墙有一道缝，就可以轻易化解。

然而，自从方教授去和病魔抗争离开工作岗位之后，据说来了一位女士接替他的工作。女人发狠起来比男人礼拜多了，实在是堵的太严实了。

下面是正题。其实，ShadowSocks与goagent最大的区别就是，ShadowSocks并不是通过GAE服务器访问网络，而是通过好心人共享出自己的网络实现上网的功能。这就需要在国外的热心人士安装上对应的客户端，共享出自己家的带宽了。这样的话，由于IP分布很广，所以通过IP拦截的方式就很难起作用了。然后，有人发现，如果GFW发现网络上在发送加密的包，那么，可能会自动做丢包处理，或者为该包选择最差路由路径传输。还有，使用VPN的用户，长时间连接的都是同样的地址，虽然内容无法侦测，但是会自动屏蔽掉改IP。

有一个中文版的ShadowSocks公益组织`https://www.shadowsocks.net/`，这里面提供了Windows下DOT NET开发的客户端程序，我的Mint果断不能用。如此高大上的东西，绝对不只是Windows平台的，所以继续找，`http://shadowsocks.org/en/download/clients.html`这个好像是官方网站，在Linux平台下依然写着shadowsocks-go，这应该是我大Golang开发的，但是去下载，发现是404。。。对node.js没有好感，果断选择了Python客户端。

我不会用Python，电脑上只有简单的开发环境，要安装程序，还需要安装必要的依赖:

    sudo apt-get install python-m2crypto

接着，安装ShadowSocks客户端。如果安不上，可以选择豆瓣提供的源。而Ruby，可以选择淘宝提供的源。为这两个公司点个赞：

    pip install shadowsocks

安装教程2，要在`/etc/shadowsocks`目录下创建文件config.json。去ShadowSocks中文网站，可以免费申请到帐号，按照此格式填入即可：

    {
        "server":"remote-shadowsocks-server-ip-addr",
        "server_port":8883,
        "local_address":"127.0.0.1",
        "local_port":8883,
        "password":"whosyourdaddy",
        "timeout":300,
        "method":"aes-256-cfb",
        "fast_open":false,
        "workers":1
    }`

最后，启动客户端。这个东西应该能直接加到开机启动里面，我不会，先这样吧。。。

    sslocal -c /etc/shadowsocks/config.json

最后，配置Proxy SwitchySharp。它和goagent配置差不多，只是它用的是SOCK5传输，而不是HTTP，所以要在SOCKS Host里面填入`localhost`和配置文件里写的端口号，并选择SOCKS v5。

在Android和iOS端也都有相应的实现，iOS端由于权限的原因，只是一个浏览器，但是很好用。我的Nexus 7也安上了客户端，看着功能比较强，但是无法启动，可能需要root吧。ShadowSocks大家都知道是啥，但是为啥只提供Google Play一种安装方式，安起来好辛苦的说。。。

---

###### *参考文献*
+ 【1】[ShadowSocks公益组织](https://www.shadowsocks.net/)
+ 【2】[Shadowsocks (简体中文)](https://wiki.archlinux.org/index.php/Shadowsocks_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)#.E5.AE.A2.E6.88.B7.E7.AB.AF)
+ 【3】[Chrome谷歌浏览器代理插件Proxy SwitchySharp简要教程](https://bbs.shadowsocks.net/discussion/6/)

{% include JB/setup %}