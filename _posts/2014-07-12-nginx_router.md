---
layout: post
title: "Nginx根据域名转发"
description: "虽然一直没有直接配置过公司的Nginx服务器，但是还是耳濡目染了解到了一些相关内容，知道Nginx能够根据域名进行转发请求。这样，一台服务器就能够配置多个域名和多个应用程序。"
figure: "http://cyeam.qiniudn.com/nginx.jpg"
category: "Nginx"
tags: ["Nginx"]
---

Nginx的安装这里就不提了。安装成功之后，能显示默认的页面。

首先，要测试通过Nginx将不同的域名转发到不同的服务器，要注册一个域名。我通过免费域名提供商`dot.tk`注册了`cyeam.tk`这个域名，并且新建了两个A记录，将两个子域名都绑定要同一个IP上面。

![IMG-THUMBNAIL](http://cyeam.qiniudn.com/tk_nginx_test.png)

接着，在服务器上面启动两个服务。我使用beego进行测试。通过命令`bee new`很方便的创建了两个应用，然后修改`conf/app.conf`里面的监听端口，修改其中一个即可。这两个服务就可以正常启动了。

最后，就是编写转发规则。Nginx的配置文件在`/usr/local/nginx/conf`里面。之前在公司群里看到过转发规则，后来又去Stackoverflow找了一篇大概介绍配置文件写法的进行参考，照猫画虎了写了，成功了。将访问域名，分别转发到了331端口和8080端口。

    location / {
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $remote_addr;
            proxy_set_header Host $http_host;

    if ($http_host = "blog.cyeam.tk") {
        proxy_pass http://127.0.0.1:331;
    }

    if ($http_host = "www.cyeam.tk") {
        proxy_pass http://127.0.0.1:8080;
    }
        root   html;
        index  index.html index.htm;
    }

修改完之后，通过命令`sbin/nginx -t`检查配置文件是否正确，然后通过命令`sbin/nginx -s reload`重新载入配置文件。

可以通过这两个域名访问到这两个应用，我对页面稍微做了修改，可以看出来转发到了不同的端口。

---

昨天成功了，今天再来看，就不行了。。。是因为我没有备案。没有办法展示效果了。
![IMG-THUMBNAIL](http://cyeam.qiniudn.com/fuck_miit.png)


这样做可能还不是很完善，因为可以通过域名加端口的方式访问到具体服务。比如，blog.cyeam.tk设定是转发到331端口，如果通过blog.cyeam.tk:8080依然可以访问8080端口的服务。我觉得还需要对防火墙进行设定，不允许从外网访问除80等一些常见端口以外的端口。


---

######*参考文献*
+ 【1】[nginx启动，重启，关闭命令 - 晓风残梦](http://www.cnblogs.com/derekchen/archive/2011/02/17/1957209.html)
+ 【2】[nginx conditional proxy pass - Stackoverflow](http://stackoverflow.com/questions/7878334/nginx-conditional-proxy-pass)

{% include JB/setup %}