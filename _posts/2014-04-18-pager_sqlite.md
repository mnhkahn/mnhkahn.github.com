---
layout: post
title: "基于流媒体的对讲机系统——数据库模块"
figure: "http://cyeam.qiniudn.com/c168.png"
description: ""
category: "Postgraduate"
tags: ["Postgraduate design", "Evaluate"]
---

移动设备中的数据库是对在线网络存储的一个重要补充。本课题的需求中，要求能保存关注的联系人和通话历史，所以使用SQLite来实现。SQLite可以像普通数据库一样机型增删改查的操作。

###游标
查询指令会返回游标，可以通过`moveToNext`方法进行遍历处理。

###android.content.ContentValues
ContentValues是Android提供的一个容器，类似于Map，可以通过Key-Map的方式加入值。

###SQLiteOpenHelper

###SQLiteDatabase

---

######*参考文献*
+ 《Learning Android》 马尔科·加尔根塔 电子工业出版社 ISBN: 9787121172632

{% include JB/setup %}
