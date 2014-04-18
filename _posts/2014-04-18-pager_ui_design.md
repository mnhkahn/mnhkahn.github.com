---
layout: post
title: "基于Android的移动VoIP视频通话系统的设计与实现——UI设计"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: ""
category: "Postgraduate design"
tags: ["Postgraduate design", "SIP", "opensips", "Evaluate"]
---

现如今，所有UI设计都在趋向扁平化。Android也不例外，据说新一代的Android会和Google的Web界面一道，进行扁平化处理。虽然UI设计不是我们课题的重点，但是也要尽量跟上这个潮流。扁平化的设计，主要是将UI里的控件进行处理，不能再是之前的拟物设计了。下面，主要来介绍Android的扁平化处理。

Android中的drawable不仅只能是图片，还可以是自定义的图形(Shape)，用XML文件来描述。Shape可以被其他控件，例如按钮(Button)使用，显示出指定形状的按钮来。这里我们要进行扁平化处理，所以需要一个圆形的Shape。

    <?xml version="1.0" encoding="utf-8"?>
    <shape xmlns:android="http://schemas.android.com/apk/res/android"
        android:shape="oval" >
        <!-- 填充的颜色 -->
        <solid android:color="#FFFFFF" />
        <!-- 设置按钮的四个角为弧形 -->
        <corners android:radius="50dip" />
    </shape>

我们的控件只要设置`android:background="@drawable/round"`，就能限定成圆形的。但这还不够，我们还需要在圆形的控件内绘制图片，需要使用`ImageView`控件，为其增加`android:src`属性。

---
######*参考文献*
+ [Drawable Resources | Android Developers](http://developer.android.com/guide/topics/resources/drawable-resource.html)

{% include JB/setup %}