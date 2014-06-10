---
layout: post
title: "Android 配置"
figure: "http://cyeam.qiniudn.com/android.jpg"
description: ""
category: "Postgraduate design"
tags: ["Postgraduate design", Paper", "Android"]
---

`android.content.SharedPreferences`配置内容可以在Activity、Service、Broadcast和Content Provider中使用。在程序运行时动态获取配置信息，可以通过`android.preference.PreferenceManager.getDefaultSharedPreferences()`获取实例。

##1. 读取配置信息

SharedPreferences 提供如下方法直接获取配置的信息。

|| **#** || **方法** ||
|| 1 || getString ||
|| 2 || getBoolean ||
|| 3 || getInt ||
|| 4 || getLong ||
|| 5 || getFloat ||

##2. 修改配置信息

修改配置需要用到`android.content.SharedPerferences.Editor`。Editor提供了如下方法修改首选项内容。获取Editor通过`SharedPerferences.editor()`获得。

|| **#** || **方法** ||
|| 1 || putString ||
|| 2 || putBoolean ||
|| 3 || putInt ||
|| 4 || putLong ||
|| 5 || putFloat ||

##3. PreferenceActivity

使用`PreferenceActivity`，通过`addPreferencesFromResource`以界面的形式展示，并且可以在此界面中对配置的值进行修改。展示的布局将会按照首选项的配置文件自动生成。每一项都是由指定的`android:title`和该项的值组成。

##4. 首选项内容

+ 配置模块需要能对用户的角色进行选择。该选项通过`ListPreference`实现，用户需要三选一。默认值为普通选项。
+ 用户可以配置其对讲机用户名，还可以手动配置SIP服务器地址。实际使用过程中，如果服务器出现故障，需要及时切换到备用服务器上，这里用来便捷的切换使用`EditTextPreference`实现，按下之后直接修改即可。
+ 配置SIP端口，默认SIP使用5060，如果被其它类SIP应用程序占用端口，直接在这里更改端口即可。
+ 传输载体选择，可以选择wifi、3G、4G和CACT等通信方式。
+ 音频和视频的压缩率的选择，一般为了保持实时性，系统默认会采用较低的采样率进行采集。如果需要观察某个具体场景的细节时，可以手动调节成高清采样模式。
+ 在协作通信模块，指挥角色需要自定义协作的问题，例如：“是否都已准备好？”。而执行角色在应答的时候，也可以直接确认或者也可以使用在配置预先配置好的应答方式，例如：“A已就绪，但是存在B问题，但是不重要。”诸如此类，可以提高协作的灵活性和高效性。通过`EditTextPreference`实现。

##5. 监听配置信息的修改

+ `registerOnSharedPreferenceChangeListener`
+ `unregisterOnSharedPreferenceChangeListener`


---

######*参考文献*
+ 【1】[How to create RadioButton group in preference.xml window? | Stackoverflow](http://stackoverflow.com/questions/4966816/how-to-create-radiobutton-group-in-preference-xml-window)
+ 【2】[SharedPreferences | Android Developers](http://developer.android.com/reference/android/content/SharedPreferences.html)
+ 【3】Marko Gargenta, Learning Android[M]. 电子工业出版社, 2012.7.
 

{% include JB/setup %}