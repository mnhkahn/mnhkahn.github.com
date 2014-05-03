---
layout: post
title: "基于流媒体的对讲机系统——配置模块"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: ""
category: "Postgraduate design"
tags: ["Postgraduate design", Paper"]
---

根据前面的需求，这里详细介绍一下配置模块的具体功能：

+ 配置模块需要能对用户的角色进行选择。
+ 需要能对SIP用户名进行设置，这个必须要设置，才能有效的辨别不同的用户身份和其各自的职责。
+ 可以手动配置SIP服务器地址。实际使用过程中，如果服务器出现故障，需要及时切换到备用服务器上，这里用来便捷的切换。
+ 配置SIP端口，默认SIP使用5060，如果被其它类SIP应用程序占用端口，直接在这里更改端口即可。
+ 传输载体选择，可以选择wifi、3G、4G和CACT等通信方式。
+ 音频和视频的压缩率的选择，一般为了保持实时性，系统默认会采用较低的采样率进行采集。如果需要观察某个具体场景的细节时，可以手动调节成高清采样模式。
+ 在协作通信模块，指挥角色需要自定义协作的问题，例如：“是否都已准备好？”。而执行角色在应答的时候，也可以直接确认或者也可以使用在配置预先配置好的应答方式，例如：“A已就绪，但是存在B问题，但是不重要。”诸如此类，可以提高协作的灵活性和高效性。

+ 获取配置

		mSharedPreferences = PreferenceManager.getDefaultSharedPreferences(this);
        
+ 注册监听器

		mSharedPreferences.registerOnSharedPreferenceChangeListener(mOnSharedPreferenceChangeListener);

{% include JB/setup %}