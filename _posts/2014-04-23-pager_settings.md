---
layout: post
title: "基于流媒体的对讲机系统——配置模块"
figure: "http://cyeam.qiniudn.com/c168.png"
description: ""
category: "Postgraduate design"
tags: ["Postgraduate design", Paper"]
---

##1. 读取配置信息

##2. 修改配置信息

##3. PreferenceActivity

##4. 监听配置信息的修改

针对不同的用户，可以通过不同的配置文件为用户私人定制不同的功能，提供个性化的服务。本课题中就在协作模块中用到了此特性。这些配置信息对于整个系统各个模块共享，可以认为是是系统的全局变量。一般在PC端开发的情况下，可以将配置信息保存在单独的文件中，在用的时候进行读取即可。但是这样做对于系统的安全性和完整性是个挑战。PC端有一种破解软件系统的方法，就是通过修改配置文件进行。而Android提供了专门的配置方案PreferenceManager。PreferenceManager创新性的技能作为配置文件为该系统中全局配置文件，也可以通过`PreferenceActivity`通过`addPreferencesFromResource`以界面的形式展示，并且可以在此界面中对配置的值进行修改。

根据前面的需求，这里详细介绍一下配置模块的具体功能：

+ 配置模块需要能对用户的角色进行选择。该选项通过`ListPreference`实现，用户需要三选一。默认值为普通选项。
+ 用户可以配置其对讲机用户名，还可以手动配置SIP服务器地址。实际使用过程中，如果服务器出现故障，需要及时切换到备用服务器上，这里用来便捷的切换使用`EditTextPreference`实现，按下之后直接修改即可。
+ 配置SIP端口，默认SIP使用5060，如果被其它类SIP应用程序占用端口，直接在这里更改端口即可。
+ 传输载体选择，可以选择wifi、3G、4G和CACT等通信方式。
+ 音频和视频的压缩率的选择，一般为了保持实时性，系统默认会采用较低的采样率进行采集。如果需要观察某个具体场景的细节时，可以手动调节成高清采样模式。
+ 在协作通信模块，指挥角色需要自定义协作的问题，例如：“是否都已准备好？”。而执行角色在应答的时候，也可以直接确认或者也可以使用在配置预先配置好的应答方式，例如：“A已就绪，但是存在B问题，但是不重要。”诸如此类，可以提高协作的灵活性和高效性。通过`EditTextPreference`实现。

在程序运行时动态获取配置信息，可以通过`PreferenceManager.getDefaultSharedPreferences()`实现。而应用监听模块、SIP注册模块等，正常工作都需要实时与配置信息同步。Android提供了监听器，监听器被调用时需要重新载入配置选项。监听器通过`registerOnSharedPreferenceChangeListener()`注册。

---
######*参考文献*
+ [How to create RadioButton group in preference.xml window? | Stackoverflow](http://stackoverflow.com/questions/4966816/how-to-create-radiobutton-group-in-preference-xml-window)
{% include JB/setup %}