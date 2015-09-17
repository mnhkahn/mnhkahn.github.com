---
layout: post
title: "MySQL的find_in_set函数"
description: ""
category: "Database"
tags: ["Database", "MySQL"]
---

之前学校念书的时候，学过各种范式。范式里一般要求，就是只要遇到一对多或者多对多的关系，就把多这边拆出去。这样做一来是为了节约空间，如果关联的是字符串或者占用比较大的东西，拆出去用一个id来关联；还有一个就是可以防止多对多关系的变化，比如关联性别，已经有男和女了，如果加一个不男不女还行，但是要删一个女，那么就需要这个了，一般数据库也支持关联的修改。

但是我们都是比较懒的，还死活拿性别来说。性别就俩，男和女。为来也不会增加和减少，那么就不必要创建性别表，因为就是建了，也没有必要；一般我们也会省略关联表。而是只用一列进行关联，关联男或女就用1或0，如果关联两个，是用`0,1`表示。这也可能是大辉哥说的“反模式”。

这样数据库设计比较省事，但是查的时候不太好查。如果列里面是`1,2,3`，查里面有没有`1`，一般我也是笨笨得遍历一下。今天同事告诉我一个新牛逼的MySQL函数`FIND_IN_SET()`。

> FIND_IN_SET(str,strlist)

> Returns a value in the range of 1 to N if the string str is in the string list strlist consisting of N substrings. A string list is a string composed of substrings separated by “,” characters. If the first argument is a constant string and the second is a column of type SET, the FIND_IN_SET() function is optimized to use bit arithmetic. Returns 0 if str is not in strlist or if strlist is the empty string. Returns NULL if either argument is NULL. This function does not work properly if the first argument contains a comma (“,”) character.

这个是专门针对用逗号分隔的串的查找。如果没有找到，返回0；找到了，返回位置，位置从1开始。

---

######*参考文献*
+ 【1】[12.5 String Functions - FIND_IN_SET()](http://dev.mysql.com/doc/refman/5.0/en/string-functions.html#function_find-in-set)

{% include JB/setup %}
