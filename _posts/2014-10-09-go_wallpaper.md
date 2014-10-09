---
layout: post
title: "用Golang写了一个更新壁纸的小程序"
description: "把程序放到启动目录里面，这样就能每次开机更新啦。"
category: "kaleidoscope"
tags: ["Kaleidoscope", "Life"]
---

之前安装了安了Ubuntu 14.04，还写了个小程序，能开机更新桌面壁纸——[《Ubuntu通过Bing壁纸自动更新》](http://blog.cyeam.com/kaleidoscope/2014/09/17/ubuntu_bing_bg/)。结果谁知道Ubuntu这个版本是怎么回事，一把开发环境配置好，就开不了机了。。。我这种学渣实在是处理不了，只能换Windows 8了。

换了Windows 8还是惦记着我的更新壁纸程序。Windows系统和Linux不同，并没有提供修改壁纸的命令，只能提供Windows API编程进行修改。本科学游戏开发的我对这个还是比较熟悉的。

	#include "stdafx.h"
	#include <windows.h>
	#include <iostream>
	#include <string>
	
	using namespace std;
	
	int main(int argc, char** argv)
	{
		LPWSTR file_path = L"C:\\wallpaper.jpg";
	
		int result;
		result = SystemParametersInfo(SPI_SETDESKWALLPAPER, 0, file_path, SPIF_UPDATEINIFILE);
	
		if (result == TRUE)
		{
			cout << "Wallpaper set" << result;
		}
		else
		{
			cout << "Wallpaper not set";
			cout << "SPI returned" << result;
		}
	
		return 0;
	}

修改也很好做，然后就是获取Bing每日更新的壁纸。需要发送HTTP请求获取列表和解析RSS的XML文件。学渣我只用过Qt自带的库处理过，做这个东西不需要做界面，用这样的库意思也不大。果断想到了我大Golang和cgo。我大Golang是C语言之父设计的，cgo支持调用C语言，但是不支持C++。

cgo需要mingw提供gcc编译器，如果是64位系统还需要mingw64，这个可以去下载编译好的，默认官网下载的是32位的。

接着就是将上面的代码改写成调用C语言包的Golang语法。调用的难度在于传入壁纸文件地址。大Golang语言级别实现了字符串，而C语言只有用字符数组表示字符串。先开始都是用字符串来存的，然后传入字符串的指针，一直不成功。

这个函数`SystemParametersInfo`只有四个参数，`SPI_SETDESKWALLPAPER`表示用来设置壁纸，第二个参数表示壁纸位置（好像是这样。。。），`SPIF_UPDATEINIFILE`表示修改之后直接展示。这三个参数应该都没错，都是整形往里面传。有错误的可能就是文件路径了，他是`LPWSTR`类型。查了一下，它的定义`typedef _Null_terminated_ WCHAR *NWPSTR, *LPWSTR, *PWSTR;`，也就是`typedef wchar_t WCHAR;`。它是2个字节的Unicode字符类型。也就是说，`LPWSTR`是一个字符数组，函数调用的时候就是传入字符数组的指针进去。后来我就把字符串转换成数组`[]byte`类型（文件路径不会有中文，所以用`[]byte`还是`[]rune`都没有影响）。然后像C语言一样，把数组名称传进去（C语言里面，字符数组名称就是这个数组的指针）。结果还是不行，后来发现大Golang的数组名称不是地址。。。大Golang获取数组地址应该是这样`&path[0]`。

大Golang做json解析非常简单，我起初也是按照json的方式来解析XML，结果不行。后来参考了谢大的《Go Web 编程》。具体原因我没有去了解。关于XML的后面再补。

编译程序：

	go build go_code/wallpaper/win32api
	go install go_code/wallpaper/win32api

	go build go_code/wallpaper/app
	go install go_code/wallpaper/app

最后，将编译好的程序放到目录`C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup`下面，就可以咯。

本文所涉及到的代码可以参考[这里](https://github.com/mnhkahn/go_code/tree/master/wallpaper)。如果是64位系统，可以直接用里面编译好的文件。主要还是在讲我做过程中的思路，具体的实现，比如cgo这些，可以直接看我的代码，我这里就不详细写了。

---

######*参考文献*
+ 【1】[《使用 Go 调用 Windows API》](http://www.tairan.net/blog/2012/04/15/the-go-with-win32-api/)
+ 【2】[《Go Web 编程》 - XML处理](https://github.com/astaxie/build-web-application-with-golang/blob/master/ebook/07.1.md)
+ 【3】[Windows手动添加开机启动项](http://blog.csdn.net/cashey1991/article/details/6776349)


{% include JB/setup %}