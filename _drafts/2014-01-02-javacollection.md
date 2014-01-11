---
layout: post
title: "Java面试宝典"
figure: "/assets/images/logo-java.jpg"
description: "从2013年9月开始找工作，在几个月的Java程序员求职过程中，总结了一些被问到的笔试题和面试题。Java语言博大精深，是整个程序界的上乘语言，应该得到重视。"
category: "Java 源码剖析"
tags: []
---

1. Java标识符，命名规范？
	+ 不能以数字开头；rake post title="hello world" category="life" date="2013-04-21" tags="" description="description"
	+ 区分大小写；
	+ 不能有@、‘-‘（运算符）；
	+ 可以出现中文；
	+ java关键字不能做为变量名；

2. Java基本类型及其范围   
<table cellpadding="0" cellspacing="0" class="c21"><tbody><tr class="c15"><td class="c29"><p class="c2 c6"><span>基本类型</span></p></td><td class="c10"><p class="c2 c6"><span>大小</span></p></td><td class="c13"><p class="c2 c6"><span>最小值</span></p></td><td class="c23"><p class="c2 c6"><span>最大值</span></p></td><td class="c13"><p class="c2 c6"><span>包装器</span></p></td><td class="c30"><p class="c2 c6"><span>默认值</span></p></td><td class="c9"><p class="c2 c6"><span>说明</span></p></td></tr><tr><td class="c29"><p class="c2 c6"><span>boolean</span></p></td><td class="c10"><p class="c2 c6"><span>-</span></p></td><td class="c13"><p class="c2 c6"><span>-</span></p></td><td class="c23"><p class="c2 c6"><span>-</span></p></td><td class="c13"><p class="c2 c6"><span>Boolean</span></p></td><td class="c30"><p class="c2 c6"><span>false</span></p></td><td class="c9"><p class="c2"><span>没有大小</span></p></td></tr><tr><td class="c29"><p class="c2 c6"><span>char</span></p></td><td class="c10"><p class="c2 c6"><span>16bits</span></p></td><td class="c13"><p class="c2 c6"><span>Unicode 0</span></p></td><td class="c23"><p class="c2 c6"><span>Unicode 2</span><span class="c32">16</span><span>-1</span></p></td><td class="c13"><p class="c2 c6"><span>Character</span></p></td><td class="c30"><p class="c2 c6"><span>\u0000‘ ‘</span></p></td><td class="c9"><p class="c2"><span>可以用来表示中文</span></p></td></tr><tr><td class="c29"><p class="c2 c6"><span>byte</span></p></td><td class="c10"><p class="c2 c6"><span>8bits</span></p></td><td class="c13"><p class="c2 c6"><span>-128</span></p></td><td class="c23"><p class="c2 c6"><span>127</span></p></td><td class="c13"><p class="c2 c6"><span>Byte</span></p></td><td class="c30"><p class="c2 c6"><span>0</span></p></td><td class="c9"><p class="c2"><span>与C++中的char相同</span></p></td></tr><tr><td class="c29"><p class="c2 c6"><span>short</span></p></td><td class="c10"><p class="c2 c6"><span>16bits</span></p></td><td class="c13"><p class="c2 c6"><span>-2</span><span class="c32">15</span></p></td><td class="c23"><p class="c2 c6"><span>2</span><span class="c32">15</span><span>-1</span></p></td><td class="c13"><p class="c2 c6"><span>Short</span></p></td><td class="c30"><p class="c2 c6"><span>0</span></p></td><td class="c9"><p class="c2 c26"><span></span></p></td></tr><tr><td class="c29"><p class="c2 c6"><span>int</span></p></td><td class="c10"><p class="c2 c6"><span>32bits</span></p></td><td class="c13"><p class="c2 c6"><span>-2</span><span class="c32">31</span></p></td><td class="c23"><p class="c2 c6"><span>2</span><span class="c32">31</span><span>-1</span></p></td><td class="c13"><p class="c2 c6"><span>Integer</span></p></td><td class="c30"><p class="c2 c6"><span>0</span></p></td><td class="c9"><p class="c2 c26"><span></span></p></td></tr><tr><td class="c29"><p class="c2 c6"><span>long</span></p></td><td class="c10"><p class="c2 c6"><span>64bits</span></p></td><td class="c13"><p class="c2 c6"><span>-2</span><span class="c32">63</span></p></td><td class="c23"><p class="c2 c6"><span>2</span><span class="c32">63</span><span>-1</span></p></td><td class="c13"><p class="c2 c6"><span>Long</span></p></td><td class="c30"><p class="c2 c6"><span>0</span></p></td><td class="c9"><p class="c2 c26"><span></span></p></td></tr><tr><td class="c29"><p class="c2 c6"><span>float</span></p></td><td class="c10"><p class="c2 c6"><span>32bits</span></p></td><td class="c13"><p class="c2 c6"><span>IEEE754</span></p></td><td class="c23"><p class="c2 c6"><span>IEEE754</span></p></td><td class="c13"><p class="c2 c6"><span>Float</span></p></td><td class="c30"><p class="c2 c6"><span>0.0</span></p></td><td class="c9"><p class="c2"><span>指数8位</span></p></td></tr><tr><td class="c29"><p class="c2 c6"><span>double</span></p></td><td class="c10"><p class="c2 c6"><span>64bits</span></p></td><td class="c13"><p class="c2 c6"><span>IEEE754</span></p></td><td class="c23"><p class="c2 c6"><span>IEEE754</span></p></td><td class="c13"><p class="c2 c6"><span>Double</span></p></td><td class="c30"><p class="c2 c6"><span>0.0</span></p></td><td class="c9"><p class="c2"><span>指数16位</span></p></td></tr><tr><td class="c29"><p class="c2 c6"><span>void</span></p></td><td class="c10"><p class="c2 c6"><span>-</span></p></td><td class="c13"><p class="c2 c6"><span>-</span></p></td><td class="c23"><p class="c2 c6"><span>-</span></p></td><td class="c13"><p class="c2 c6"><span>Void</span></p></td><td class="c30"><p class="c2 c6"><span>null</span></p></td><td class="c9"><p class="c2"><span>Void可以定义变量</span></p></td></tr></tbody></table>


{% include JB/setup %}