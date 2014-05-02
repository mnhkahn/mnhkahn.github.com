---
layout: post
title: "基于流媒体的对讲机系统——配置模块"
figure: "http://mnhkahn.github.io/assets/images/c168.png"
description: ""
category: "Postgraduate design"
tags: ["Postgraduate design", Paper"]
---

+ 获取配置

		mSharedPreferences = PreferenceManager.getDefaultSharedPreferences(this);
+ 注册监听器

		mSharedPreferences.registerOnSharedPreferenceChangeListener(mOnSharedPreferenceChangeListener);

{% include JB/setup %}