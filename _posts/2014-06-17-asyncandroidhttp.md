---
layout: post
title: "AndroidHTTP库——Asynchronous Http Client for Android"
description: ""
category: "Android"
tags: ["Android", "HTTP"]
---

项目做了一个REST服务器，提供给Android客户端访问。Android为了保证界面交互，目前不能够在主线程当中使用发起HTTP请求。简单的做法是建立一个线程，在里面发送HTTP请求，收到结果之后，再创建一个Handler，通过Handler发送出更新界面的消息，在Handler里面更新。这样做比较麻烦，要创建Thread和Handler才能完成一次请求。当时我要做的是能够重复发送请求，就在线程中加了一个`while`判断，需要更新时更新。这样做功能上是可以了，我就去睡觉了。睡觉以前还有75%的电，起来后发现没电关机了。我被我牛逼的代码震惊了。

后来去Github找了一个开源的Android Http异步请求库android-async-http，非常好用。[官方网站](http://loopj.com/android-async-http/)。调用之后会异步返回，返回之后仍然在界面类当中，所以也不需要再新建Handler发送消息就能够直接处理界面响应了。

<iframe src="http://ghbtns.com/github-btn.html?user=loopj&repo=android-async-http&type=fork&count=true&size=large"
  allowtransparency="true" frameborder="0" scrolling="0" width="170" height="30"></iframe>

请求的发送基于`org.apache.http.impl.client.DefaultHttpClient`封装。尽管Android官网推荐在2.3及后续版本中使用HttpURLConnection作为网络开发首选类，但在连接管理和线程安全方面，HttpClient还是具有很大优势。`DefaultHttpClient`提供了一套拦截器，用来处理即将离开的请求和即将到达的响应。

    httpClient.addRequestInterceptor(new HttpRequestInterceptor() {
            @Override
            public void process(final HttpRequest request, final HttpContext context) throws HttpException, IOException {
            }
    });

此外，它还使用了`org.apache.http.impl.conn.tsccm.ThreadSafeClientConnManager`来管理连接。

    httpClient = new DefaultHttpClient(cm, httpParams);

{% include JB/setup %}