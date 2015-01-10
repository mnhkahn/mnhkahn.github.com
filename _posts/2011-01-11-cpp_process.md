---
layout: post
title: "用CreateProcess创建线程，指定运行QQ.EXE"
description: "操作系统作业。"
category: "Computer"
tags: ["Computer Science", "Operating System", "Windows"]
---

	STARTUPINFOsi;
	PROCESS_INFORMATIONpi;
	
	ZeroMemory( &si,sizeof(si));
	si.cb = sizeof(si);
	ZeroMemory( &pi,sizeof(pi));
	
	
	if (!CreateProcess(NULL,
	        "D:\\Program Files\\Tencent\\QQ\\Bin\\QQ.exe",
	        NULL,
	        NULL,
	        FALSE,
	        0,
	        NULL,
	        NULL,
	        &si,
	        &pi)
	        )
	{
	        cout << "CreateProcessfailed:" << GetLastError()<< endl;
	}
	cout << "CreateProcesssuccess" << endl;
	return 0;

![IMG-THUMBNAIL](http://cyeam.qiniudn.com/fec64b549c09021b574e002b.jpg)

用SPY++查看

![IMG-THUMBNAIL](http://cyeam.qiniudn.com/f3891238056f24bdb311c735.jpg)


{% include JB/setup %}
