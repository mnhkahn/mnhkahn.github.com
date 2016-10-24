---
layout: post
title: "最简单的HTTP SERVER"
description: "参考《HTTP权威指南》用Go做了一个最简单的HTTP服务器。"
category: "network"
tags: ["HTTP","Golang"]
---

到了新单位总算有点闲了，接着倒腾HTTP。之前的文章可以参考：[《基于TCP套接字，通过Golang模拟HTTP请求》](http://blog.cyeam.com/network/2014/09/28/go_http/)和[《基于TCP套接字，通过Golang模拟HTTP请求（续）》](http://blog.cyeam.com/network/2014/09/29/go_http2/)。

之前都是研究的客户端，现在来研究一下服务端。《HTTP权威指南》上面有一个非常简单的用`perl`开发的一个服务器，我就用大`Golang`照着写一个。HTTP协议是基于传输层的TCP协议，监听80端口。简单来写（复杂的我也不会），就是最简单的TCP监听，接收消息，处理并返回。我是参考的[《Go socket编程实践: TCP服务器和客户端实现》](http://colobu.com/2014/12/02/go-socket-programming-TCP/)。主逻辑就是这样：

	ln, err := net.Listen("tcp", fmt.Sprintf("%s:%d", "", *portFlag))
	defer ln.Close()
	if err != nil {
		panic(err)
	}

	log.Printf("<<<Server Accepting on Port %d>>>\n\n", *portFlag)
	for {
		conn, err := ln.Accept()
		if err != nil {
			log.Panicln(err)
		}
		go handleConnection(conn)
	}
	
我做东西喜欢从最简单开始，一个是因为我会的不多，一个是简单的来自己能理明白，以后维护其实更省事。

回归正题，这块其实从念书的时候就老写，分分钟搞定。然后就是HTTP协议的东西。当然，还是按最简单的来。HTTP分为三部分，起始行（start line）、首部（header）和主体（body）。

起始行只有一行，就是协议版本和状态码这些，以`CRLF`结尾，也就是`\r\n`；接着就是头，头里面的内容就是键值对，每组键值对以`CRLF`结尾；头和主体中间，还需要多一个`CRLF`，我猜是为了解析内容方便。主体之后不需要`CRLF`。

下图就是详细的请求格式。其中`SP`是空格。

![IMG-THUMBNAIL](http://7b1h1l.com1.z0.glb.clouddn.com/General%20format%20of%20an%20HTTP%20request%20message.JPG	)

![IMG-THUMBNAIL](http://7b1h1l.com1.z0.glb.clouddn.com/General%20format%20of%20an%20HTTP%20response%20message.JPG	)

一些必要的头（因为我发现如果没有，请求会失败），就是`Content-Type`和`Content-length`。Content-length就是Body的长度。

    func handleConnection(conn net.Conn) {
    	defer conn.Close()
    	log.Printf("[%s]<<<Request From %s>>>\n", time.Now().String(), conn.RemoteAddr())
    
    	serve_time := time.Now()
    	buffers := bytes.Buffer{}
    	buffers.WriteString("HTTP/1.1 200 OK\r\n")
    	buffers.WriteString("Server: Cyeam\r\n")
    	buffers.WriteString("Date: " + serve_time.Format(time.RFC1123) + "\r\n")
    	buffers.WriteString("Content-Type: text/html; charset=utf-8\r\n")
    	buffers.WriteString("Content-length:" + fmt.Sprintf("%d", len(DEFAULT_HTML)) + "\r\n")
    	buffers.WriteString("\r\n")
    	buffers.WriteString(DEFAULT_HTML)
    	conn.Write(buffers.Bytes())
    }
    
最后补充一点，连接记得关闭

---

###### *参考文献*
+ 【1】《HTTP权威指南》
+ 【2】James F.Kurose, Keith W.Ross.COMPUTER NETWORKING. A Top-Down Approach Featuring the Internet(Third Edition).
+ 【3】NETWORKING INFO BLOG. HTTP Message Format.

---

{% include JB/setup %}
