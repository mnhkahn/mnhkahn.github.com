---
layout: post
title: "数据库访问时区问题"
description: "今天第二篇，都一次一天发多篇干货"
category: "golang"
tags: ["golang", "hole", "MySQL", "Time Zone"]
---

今天是第二次跳进这个坑里面。

我要做的接口有一个需求，就是根据设定好的开始时间和结束时间过滤掉未开始和过期的内容。我用`xorm`作为ORM引擎进行数据库开发。直接一条解决了问题。当时还大概测了一下，没有任何问题。

	Where("displayorder<>0 AND effectivetime< ? AND expirationtime> ?", time.Now(), time.Now())

今天iOS开发要调用我的接口开发，因为我写的测试数据不完整，他叫测试配了几条测试数据。测试妹子很专业的，加了一条过期的，一条要显示的，一条未开始的，然后我这三条一条都没展示。。。

问题报给我之后，很明显就知道问题出在哪里了。肯定是那个Where查询错了。xorm支持记录SQL语句日志，一开始开发我就配置上了。果断去看日志。把SQL复制到Navicat里面运行，发现没有任何问题。。。这就邪了。百思不得其解。我就开始瞎猜。是不是传入的time.Now()有问题。我就把日期格式化了一下，可以了。

	const DATE_LAYOUT = "2006-01-02 15:04:05"
	now := time.Now()
	now_str := now.Format(DATE_LAYOUT)

这一次歪打正着让我觉得很不对劲（我的直觉还是很准确的！！！），然后就去请教了一下我万能的大哥，他说应该是UTC的问题。意思就是时区的问题，我才恍然大悟，之前我也踩过这个坑。在MySQL连接字符串里面加上时区信息就可以了。

	parseTime=true&loc=Asia%2FChongqing

最后，我万能的大哥还告诉我，根本不需要传时间进去，直接使用MySQL的函数`NOW()`就可以了。嗯，大哥就是大哥。。。

	Where("displayorder<>0 AND effectivetime< NOW() AND expirationtime> NOW()")

---

我团的Ruby团队据说是国内比较牛逼的Ruby团队了，因为主站一直用Ruby做开发的。我们Team只有5个人，选用了Golang作为主力开发语言，Golang又比较新，我们Team会不会成为国内比较牛逼的Golang团队呢？哈哈哈


{% include JB/setup %}