---
layout: post
title: "基于流媒体的对讲机系统——系统用户界面的设计和实现"
figure: "http://cyeam.qiniudn.com/c168.png"
description: "Android Activity 布局"
category: "Postgraduate design"
tags: ["Postgraduate design", Evaluate"]
---

本系统主要的用户界面包括带有ActionBar的启动界面，系统通话界面和系统配置界面。Android的布局可以比作是HTML的标签，可以为其添加类似于CSS的样式。界面的构造支持两种方式：通过XML文件定义，通过Java代码定义。前者可以进行所见即所得地静态编辑，而后者主要是在程序中根据反馈动态修改。本课题主要使用前者实现。

+ 带有ActionBar的系统启动界面

    从Android 3.0开始，ActionBar替代了之前的标题栏作为Activity头部展示内容的默认方式。使用ActionBar需要使用Android 3.0或者API 11以上的最低SDK版本。在ActionBar上面增加按钮也很简单，为其增加菜单即可。为了美观，可以为按钮增加图标和`SHOW_AS_ACTION_IF_ROOM`选项。表示有多余位置的时候用图标展示，位置不够的时候用下拉菜单表示。这样能兼容不同尺寸的不同设备。

    Android自身提供了丰富全面的图标，需要的话可以去开发包中查找。引用的R文件需要进行相应的修改。
+ 系统通话界面。

    系统通话界面要设为全屏，主要包括三个按钮：结束通话按钮、切换摄像头按钮、静音按钮。在视频通话时还要通过小视窗展示自身摄像头预览信息。

    系统预览时，将该视窗放在远程视频框之上。有时可能会对视频内容进行遮挡。为了方便视频对话，将预览视窗设计成可以通过手动触碰进行移动的视窗。一旦发生遮挡，将其移动到其它位置即可。要实现此功能，要用到绝对布局(AbsoluteLayout)，系统启动时为其设置默认的绝对右上角的位置。AbsoluteLayout使用起来很简单，指定一个绝对位置即可。但是不太灵活，更换屏幕尺寸之后回无法自动适应。悬浮框使用WindowsManager实现，通过`setOnTouchListener`和`updateViewLayout`，在用户手指按下预览窗口并移动后，获取手指位置，并更新浮动框位置坐标即可。

    界面底部的三个按钮，也是要放置在远程视频源之上的层叠放置的按钮。此时的布局就是立体的，而不是传统的平面布局。使用相对布局(RelativeLayout)可以解决此问题。按钮相对于父控件靠下放置：`android:layout_alignParentBottom="true"`。RelativeLayout可以用来指出子元素的相对位置，所以每个子元素应该有唯一的ID。


    现如今，所有UI设计都在趋向扁平化。Android也不例外，新一代的Android会和Google的Web界面一道，进行扁平化处理。虽然UI设计不是我们课题的重点，但是也要尽量跟上这个潮流。扁平化的设计，主要是将UI里的控件进行处理，不能再是之前的拟物设计了。下面，主要来介绍Android的扁平化处理。

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
+ 《Learning Android》 马尔科·加尔根塔 电子工业出版社 ISBN: 9787121172632
+ [Drawable Resources - Android Developers](http://developer.android.com/guide/topics/resources/drawable-resource.html)
+ [Android 实现顶层窗口、浮动窗口（附Demo）](http://www.cnblogs.com/mythou/p/3244208.html)

{% include JB/setup %}