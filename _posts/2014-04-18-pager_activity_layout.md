---
layout: post
title: "基于Android的移动VoIP视频通话系统的设计与实现——Activity Layout"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: "Android Activity 布局"
category: "Postgraduate design"
tags: ["Postgraduate design", Evaluate"]
---

Android的布局有点像HTML的标签，也可以为其添加类似于CSS的样式。

+ LinearLayout
LinearLayout是最简单的布局了。可以通过属性layout_orientation横向(horizontal)或者纵向(vertical)排列布局，元素的绘制是按照加入顺序进行的。
+ TableLayout
TableLayout类似于HTML中的`<table>`标签，可以通过Table Row加入子元素作为一行元素。
+ FrameLayout
FrameLayout像一副扑克牌，最后一个显示在外面，其余的相互重叠起来。

本课题中主要使用到了AbsoluteLayout和RelativeLayout。

+ AbsoluteLayout
使用起来很简单，指定一个绝对位置即可。但是不太灵活，更换屏幕尺寸之后回无法自动适应。
+ RelativeLayout
RelativeLayout可以用来指出子元素的相对位置，所以每个子元素应该有唯一的ID。

---
######*参考文献*
+《Learning Android》 马尔科·加尔根塔 电子工业出版社 ISBN: 9787121172632

{% include JB/setup %}