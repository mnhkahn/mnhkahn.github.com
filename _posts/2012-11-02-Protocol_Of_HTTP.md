---
layout: post
title: "请求网页所需协议"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeam/http.jpg"
description: "网页一次请求用的协议和访问流程的总结。"
category: "Network"
tags: ["Network"]
---

1.  请求页面`http://www.bit.edu.cn/index.htm`后，首先在本地查找DNS缓存。本机已有缓冲，故不再向DNS服务器请求DNS解析。

        www.bit.edu.cn
        ----------------------------------------
        Record Name . . . . . : www.bit.edu.cn
        Record Type . . . . . : 1
        Time To Live  . . . . : 84020
        Data Length . . . . . : 4
        Section . . . . . . . : Answer
        A (Host) Record . . . : 10.0.6.30


2. 清空本机的DNS缓存后，重新请求该页面。访问本地DNS服务器`10.0.0.10`，DNS服务器返回该域名的地址`10.0.6.30`。这个获得的是IPv4的地址，随后还执行了一次请求，请求IPv6的地址。
![Alt Text](https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeam/Protocol1.png)

3. 随后与`10.0.6.30`建立TCP连接，请求`index.htm`页面。使用了基于TCP的HTTP协议，所以基于80端口。建立TCP连接的过程使用了3次握手。第一次握手，`Flags: 0x002 (SYN)  Sequence number: 0    (relative sequence number)`；第二次握手，`Sequence number: 0    (relative sequence number)  Acknowledgment number: 1    (relative ack number)  Flags: 0x012 (SYN, ACK)`；第三次握手，`Sequence number: 1    (relative sequence number)  Acknowledgment number: 1    (relative ack number)  Flags: 0x010 (ACK)`。
![Alt Text](https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeam/Protocol2.png)

4. 服务器成功响应，发送过来index.htm文件。其中，Server: Apache/2.2.6 (Unix) mod_jk/1.2.27\r\n可以知道北京理工大学使用的服务器是Unix版本的Apache服务器2.2.6版。部分HTML代码如下。
![Alt Text](https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeam/Protocol3.png)

        <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <title></title>
            <SCRIPT type=text/javascript src="js/common.js" ></SCRIPT>
            <link href="http://www.bit.edu.cn/css/newcss1.css" rel="stylesheet" type="text/css" />
            <link href="http://www.bit.edu.cn/css/style.css" rel="stylesheet" type="text/css" />
            <link href="http://www.bit.edu.cn/favicon.ico" rel="shortcut icon" type="image/x-icon" />
            <link href="http://www.bit.edu.cn/favicon.ico" rel="icon" type="image/x-icon" />
        </head>
        </html>

5. 获取到index.htm之后，根据HTML代码下载Javascript脚本、CSS文件、显示用的图片。每一次获取，都要建立TCP连接。这是请求资源的过程。
![Alt Text](https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeam/Protocol4.png)
    登陆126.com与之前描述相当，只是在登陆时需要提交表单。其中，用户名和密码已经经过加密。
![Alt Text](https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeam/Protocol5.png)

        var=%3C%3Fxml%20version%3D%221.0%22%3F%3E%3Cobject%3E%3Cobject%20name%3D%22attrs%22%3E%3Cstring%20name%3D%22helptips%22%3E0000000300000085%3C%2Fstring%3E%3C%2Fobject%3E%3C%2Fobject%3E

{% include JB/setup %}