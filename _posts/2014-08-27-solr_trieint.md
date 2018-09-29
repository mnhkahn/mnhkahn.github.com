---
layout: post
title: "Solr里的整形字段"
description: "东西不多，关于Solr查库遇到的小问题。"
category: "Solr"
tags: ["Solr", "int"]
---

今天一个项目，要在后台配置好id信息，用逗号分隔，然后我读取配置好的id信息，从Solr里查询，将结果返回。结果出了错误，接口并没有按照配置返回id信息，并且一条都没有返回。

看到错误，果断去抓Solr查询请求，请求很长，不太好看，不过运行一下就知道问题了。运行结果是返回了错误：`Invalid Number: `。报整数错误，第一反应了超出了范围，因为id之间是通过逗号分隔的，看来是因为少打了逗号导致的。

知道问题了，就去看看Solr的配置。id字段是int类型，而schema.xml里面配置的是：

	<fieldType name="int" class="solr.TrieIntField" precisionStep="0" positionIncrementGap="0"/>

再顺着去查`TrieIntField`：

> A numeric field that can contain 32-bit signed two's complement integer values.
> Min Value Allowed: -2147483648
> Max Value Allowed: 2147483647

验证了我的猜想。

---

###### *参考文献*
+ 【1】[Class TrieIntField](https://lucene.apache.org/solr/4_3_0/solr-core/org/apache/solr/schema/TrieIntField.html)


{% include JB/setup %}