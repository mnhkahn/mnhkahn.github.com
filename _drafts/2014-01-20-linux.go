---
layout: post
title: "Linux命令整理"
figure: "http://cyeam.qiniudn.com/terminal.png"
description: "用到的一些常见的Linux命令，在这里记录一下。"
category: "Linux"
tags: ["linux", "shell"]
---

+ curl

	+ 查看网页源码

			curl mnhkahn.github.io
	+ 显示网页头
		
			curl -i mnhkahn.github.io

	+ 显示通信过程

			 curl -v http://mnhkahn.github.io/pages.html
			* About to connect() to mnhkahn.github.io port 80 (#0)
			*   Trying 199.27.79.133... connected
			* Connected to mnhkahn.github.io (199.27.79.133) port 80 (#0)
			> GET /pages.html HTTP/1.1
			> User-Agent: curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.19.7 NSS/3.13.1.0 zlib/1.2.3 libidn/1.18 libssh2/1.2.2
			> Host: mnhkahn.github.io
			> Accept: */*

			curl --trace output.txt mnhkahn.github.io


[curl网站开发指南](http://www.ruanyifeng.com/blog/2011/09/curl.html)

+ grep

查找文件里符合条件的字符串

+ Synchronize Github

## Force Synchronize
	git reset --hard HEAD
	git clean -f
	git pull

## Commit 	
	git add -A
	git status
	git commit -a""
	git push origin master

## Import & Export MySql
	create user 'qingdy'@'localhost' identified by '';
	mysqldump -u qingdy -p QingDy > C:/Users/Bryce/Documents/GitHub/QingDy/data/qingdy.sql
	mysql -u qingdy -p QingDy < C:/Users/Bryce/Documents/GitHub/QingDy/data/qingdy.sql

## UnZip File
	unzip upload.zip -d [DIRECTRY]
	
## Passport
	[ip] 121.199.55.106
	[SSH] root Qingdiwang66
	[Aliyun] kangdakd@163.com qingdiwang66
	[mysql] bryce selinai5
	[ftp] ftp Qingdiwang66
	
## 查看占用端口
	lsof -i:8080
	
## Kill a Process
	kill -9 [pid]

sudo aptitude install
sudo aptitude remove