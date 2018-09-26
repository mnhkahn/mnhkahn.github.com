---
layout: post
title: "Golang实现HTTP发送gzip请求"
description: "beego的httplib不支持发送gzip请求，自己研究了一下。"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeam/gzip1-1.jpg"
category: "Golang"
tags: ["HTTP"]
---
 
 互联网是基于HTTP协议的，但是数据量大的情况下，HTTP就显得有点慢了，接口API一般使用Facebook开源的Thrift。但是Thrfit使用场景有限。这个时候就只能考虑减少数据量来优化HTTP请求了。

压缩的原理就是服务器端将本来要返回的数据进行压缩，传输给客户端之后，客户端用双方约定好的方式再解压缩。通过Fiddler和Debug测试，一般用Gzip相对于原数据能压缩80%~90%。而响应时间并没有因此而增加。

客户端和服务器之间是通过请求时的HTTP头`Content-Encoding`和`Accept-Encoding`来通知服务器进行何种方式压缩数据。

Golang提供了"compress/gzip"包进行压缩和解压缩处理。这个包里的`gunzip.go`文件实现了解压方法。结构体`Reader`实现了"io"包里的接口`Reader`：

type Reader interface {
	Read(p []byte) (n int, err error)
}

通过包`io/ioutil`包里的`ReadAll`函数，可以自动调用实现类里的`Read`函数。下面是基于Golang原生包`net/http`发送Gzip请求的完整代码。打印出来了解压前和解压后的数据量。
	
	client := http.Client{}
	req1, err := http.NewRequest("GET", "http://blog.cyeam.com", nil)
	req1.Header.Add("Content-Encoding", `gzip`)
	req1.Header.Add("Accept-Encoding", `gzip`)
	resp1, err := client.Do(req1)
	if err != nil {	
		panic(err)
	}
	defer resp1.Body.Close()
	body, err := ioutil.ReadAll(resp1.Body)
	fmt.Println("Length of uncompress: ", len(body))
	compressedReader, err := gzip.NewReader(resp1.Body)
	body1, err := ioutil.ReadAll(compressedReader)
	if err != nil {
		panic(err)
	}
	fmt.Println("Length of gzip: ", len(body1))

虽然接口定义了`Read`函数，能够通过此函数将数据读取出来，但是提取数据还是比较麻烦的。Golang提供了`io/ioutil`包辅助实现数据的读取，可以通过`ioutil.ReadAll`方法进行自动读取，它里面自动调用了`io`包的`Read`方法。我把源码里面调用的函数都贴了过来。

	func ReadAll(r io.Reader) ([]byte, error) {
		return readAll(r, bytes.MinRead) // 调用realAll
	}

	func readAll(r io.Reader, capacity int64) (b []byte, err error) {
		buf := bytes.NewBuffer(make([]byte, 0, capacity))
		// If the buffer overflows, we will get bytes.ErrTooLarge.
		// Return that as an error. Any other panic remains.
		defer func() {
			e := recover()
			if e == nil {
				return
			}
			if panicErr, ok := e.(error); ok && panicErr == bytes.ErrTooLarge {
				err = panicErr
			} else {
				panic(e)
			}
		}()
		_, err = buf.ReadFrom(r) // 调用ReadFrom
		return buf.Bytes(), err
	}

	func (devNull) ReadFrom(r io.Reader) (n int64, err error) {
	bufp := blackHolePool.Get().(*[]byte)
	readSize := 0
	for {
		readSize, err = r.Read(*bufp) // 在这里自动调用了实现类的Read函数进行读取操作。
		n += int64(readSize)
		if err != nil {
			blackHolePool.Put(bufp)
			if err == io.EOF {
				return n, nil
			}
			return
		}
	}
 
 
本文所涉及到的完整源码请[参考](https://github.com/mnhkahn/go_code/blob/master/test_gzip2.go)。
 
---
 
 
{% include JB/setup %}
