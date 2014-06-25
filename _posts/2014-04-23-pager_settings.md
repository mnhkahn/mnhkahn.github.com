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

    Editor edit = settings.edit();
    edit.putBoolean(PREF_MESSAGE, true);
    edit.commit();

##3. PreferenceActivity

使用`PreferenceActivity`，通过`addPreferencesFromResource`以界面的形式展示，并且可以在此界面中对配置的值进行修改。展示的布局将会按照首选项的配置文件自动生成。每一项都是由指定的`android:title`和该项的值组成。

用户更新了设置之后，还要将最新用户设置的内容展现出来，能够让用户判断是否选择正确。

    getPreferenceScreen().findPreference(PREF_ROLE).setSummary(role);

##4. 首选项内容

单选提供了`android.preference.ListPreference`，它类似于HTML的下拉列表，可以为其提供选项值和选项标签。

    <string-array name="role">
        <item>指挥</item>
        <item>协调</item>
        <item>默认</item>
    </string-array>
    <string-array name="role_values">
        <item>commander</item>
        <item>coordinator</item>
        <item>default</item>
    </string-array>

    <ListPreference
        android:defaultValue="默认"
        android:entries="@array/role"
        android:entryValues="@array/role"
        android:key="role"
        android:title="@string/settings_current_role" />

##5. 监听配置信息的修改

设置监听需要实现`android.content.OnSharedPreferenceChangeListener`接口，通过`settings.registerOnSharedPreferenceChangeListener(this);`进行注册监听。事件处理在`onSharedPreferenceChanged`。

+ `registerOnSharedPreferenceChangeListener`
+ `unregisterOnSharedPreferenceChangeListener`


---

######*参考文献*
+ 【1】[How to create RadioButton group in preference.xml window? - Stackoverflow](http://stackoverflow.com/questions/4966816/how-to-create-radiobutton-group-in-preference-xml-window)
+ 【2】[SharedPreferences - Android Developers](http://developer.android.com/reference/android/content/SharedPreferences.html)
+ 【3】Marko Gargenta, Learning Android[M]. 电子工业出版社, 2012.7.
 

{% include JB/setup %}