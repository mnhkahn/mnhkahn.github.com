---
layout: post
title: "Nutch和Solr的安装和简单测试"
figure: "http://cyeam.qiniudn.com/nutch.jpg"
description: "之前看过《Lucene in Action》一部分，里面介绍了Nutch这个Java实现的网络爬虫，把测试的结果放在这里"
category: "nutch"
tags: ["Nutch", "Solr"]
---

之前在公司使用过Solr，这是基于Lucene实现的索引引擎。后来了解到，还有Nutch这个Java实现的网络爬虫。这两个搭配起来使用，就可以认为是一个完整的搜索引擎了。自己对Solr算是比较熟了，那么Nutch上手应该也不算难。果断尝试一下。

首先是去下载，网速不够给力，国内下载国外资源老是这样。果断使用360网盘帮我缓冲。我优先使用的百度云，结果他云端没有，还得去下载，速度跟我本机一样。据我猜想，他们两个的原理都一样，服务器只会保留一份文件，如果有人要下载，提供的URL一致，就会为其直接缓冲好。难道程序员都是用的360云？

> [apache-nutch-1.8-bin http://yunpan.cn/QhfHpuGMfP84d](http://yunpan.cn/QhfHpuGMfP84d) （提取码：bea3）   
> [solr-4.8.1.zip http://yunpan.cn/QhfHIdV8pjzVT](http://yunpan.cn/QhfHIdV8pjzVT) （提取码：2f5e）

Solr启动很简单，直接解压，进入example文件夹，默认提供了Jetty作为Servlet容器，使用`java -jar start.jar`就能启动了。

Nutch的安装是按照官网的教程。

> NutchTutorial [http://wiki.apache.org/nutch/NutchTutorial](http://wiki.apache.org/nutch/NutchTutorial)

+ 解压之后，将bin目录加入PATH里；
+ 修改文件`conf/nutch-site.xml`；

        <property>
         <name>http.agent.name</name>
         <value>My Nutch Spider</value>
        </property>

+ 接着我就报错了，`No agents listed in ´http.agent.name´ property`。需要再修改`conf/nutch-default.xml`，再增加value的值即可；

        <property>
          <name>http.agent.name</name>
          <value>Cyeam's Spider</value>
          <description>HTTP 'User-Agent' request header. MUST NOT be empty -
          please set this to a single word uniquely related to your organization.

          NOTE: You should also check other related properties:

                http.robots.agents
                http.agent.description
                http.agent.url
                http.agent.email
                http.agent.version

          and set their values appropriately.

          </description>
        </property>

+ 创建`urls`目录并且创建`seed.txt`文件，这个文件用于存放要爬的网站地址。我拿自己的网站来测试，写入了`http://blog.cyeam.com/`；

        mkdir -p urls
        cd urls
        touch seed.txt

+ 修改`conf/regex-urlfilter.txt`文件，修改成如下的形式；

        # accept anything else
        #+.
        +^http://([a-z0-9]*\.)*blog.cyeam.com/

+ 还需要增加字段，向`example/solr/collection1/conf/schema.xml`文件里加入

        <field name="digest" type="string" stored="true" indexed="false"/>
        <field name="segment" type="string" stored="true" indexed="false"/>
        <field name="boost" type="float" stored="true" indexed="false"/>
        <field name="tstamp" type="date" stored="true" indexed="false"/>

        <field name="anchor" type="string" stored="true" indexed="true"
                multiValued="true"/>
        <field name="cache" type="string" stored="true" indexed="false"/>

+ 最后，启动爬虫，爬到的数据就会被存入Solr当中。

        Usage: bin/crawl <seedDir> <crawlID> <solrURL> <numberOfRounds>
        Example: bin/crawl urls/seed.txt TestCrawl http://localhost:8983/solr/ 2

使用Solr查看数据，`http://localhost:8983/solr/collection1/select?q=*%3A*&rows=100&wt=json&indent=true`。只有22个结果，我的文章不只这么多，而且内容也有问题，第一条好像是爬的首页。大体就搭建完成了。我的博客差不多就搭建好了，在`blog.cyeam.com`。接下来是搭建主站，准备工作了去购买Linode。主站也要能够展示一些博客文章。原本想基于jekyll进行修改，现在算了，直接用爬虫搞定好了。

    {
        responseHeader: {
            status: 0,
            QTime: 1,
            params: {
            indent: "true",
            q: "*:*",
            wt: "json",
            rows: "100"
        }
        },
            response: {
                numFound: 22,
                start: 0,
                docs: [
                {
                content: [
                    "Archive Home Categories Archive Tags Pages 2014 June June 19, 2014 » 流程图打脸 June 17, 2014 » AndroidHTTP库——Asynchronous Http Client for Android June 15, 2014 » Android端RTSP解决方案——libstreaming June 11, 2014 » 百度云推送 May May 15, 2014 » 『hello, world』 如何运行 May 14, 2014 » 笔试题总结 May 7, 2014 » 浪潮之巅——腾讯帝国？ April April 23, 2014 » Android 配置 April 19, 2014 » 查看自己的top10 Linux命令 April 18, 2014 » 基于流媒体的对讲机系统——UI设计 April 18, 2014 » 基于流媒体的对讲机系统——数据库模块 April 18, 2014 » Android 通知 April 18, 2014 » 基于流媒体的对讲机系统——系统用户界面的设计和实现 April 17, 2014 » 视频编解码技术H264 April 17, 2014 » SDP协议及开发设计 April 17, 2014 » 实时流媒体协议RTSP April 17, 2014 » 实时传输协议RTP April 17, 2014 » 基于流媒体的对讲机系统——系统开发准备 April 17, 2014 » 基于流媒体的对讲机系统——Android的开发准备 April 13, 2014 » 基于流媒体的对讲机系统的设计与实现 March March 5, 2014 » SIP协议的分析以及opensips注册和通话的研究 February February 25, 2014 » 上周在知乎上关于朝鲜问题的争吵 February 7, 2014 » iPhone的CSS显示 February 5, 2014 » Android Quick Start February 4, 2014 » 安卓对讲机开发评估 February 1, 2014 » Linux Mint下安装Nexus 7 驱动 January January 28, 2014 » 对联 January 22, 2014 » Linux命令整理 January 21, 2014 » beego介绍 January 14, 2014 » 一些网站架构中常见的术语和技术 January 13, 2014 » 2013读书总结 January 12, 2014 » Markdown January 11, 2014 » Linux Mint 64bit下安装Dota 2 January 7, 2014 » 青帝使用手册 January 2, 2014 » Java面试宝典 2013 November November 25, 2013 » 电影《色|戒》最后王佳芝为什么没有吃下那颗为特工准备的自杀胶囊？ November 23, 2013 » 搜狗2014校园招聘笔试题 November 5, 2013 » 中科曙光2014校园招聘笔试 October October 30, 2013 » 方正国际2014校园招聘笔试 October 25, 2013 » 神州航天软件2014校园招聘笔试 October 24, 2013 » 乐视2014校园招聘笔试 October 24, 2013 » 趣游2014校园招聘笔试 October 21, 2013 » 巨人网络2014校园招聘笔试 October 19, 2013 » 去哪网2014校园招聘Java开发面经 October 19, 2013 » 完美世界2014校园招聘笔试 October 17, 2013 » 广联达2014校园招聘笔试 October 15, 2013 » 触控科技2014校园招聘笔试题 October 13, 2013 » 百度2014校园招聘后台开发笔试 September September 16, 2013 » 阿里巴巴2014校园招聘面经 September 9, 2013 » 神州航天软件发展规划部实习笔试 April April 20, 2013 » 微软2012年实习生笔试题 March March 5, 2013 » 又一年 January January 23, 2013 » 你永远都不知道自己有多傻逼 January 23, 2013 » Connect the dots January 13, 2013 » 2012读书总结 2012 November November 2, 2012 » 请求网页所需协议 May May 23, 2012 » 沉淀心情 March March 26, 2012 » 很多事情感觉都来不及计划 2010 November November 3, 2010 » 3Q大战 May May 31, 2010 » 我的阿凡达 2009 February February 16, 2009 » 又要走了，可是不怎么想走啊 2008 December December 31, 2008 » 又过了一年 © 2014 Bryce with help from Jekyll Bootstrap and Twitter Bootstrap Cyeam by Bryce is licensed under a Creative Commons Attribution 4.0 International License ."
                ],
                title: [
                    "Archive"
                ],
                segment: "20140621215120",
                boost: 0.10709364,
                digest: "c4b54b8331f0759333cd03dbf7e84032",
                tstamp: "2014-06-21T13:53:08.412Z",
                id: "http://blog.cyeam.com/archive.html",
                url: "http://blog.cyeam.com/archive.html",
                _version_: 1471528486701105200
            },

---

######*参考文献*
+ 【1】[ CentOS 6.4环境下的Apache Nutch 1.7 + Solr 4.4.0安装笔记](http://blog.csdn.net/panjunbiao/article/details/12171147)

{% include JB/setup %}