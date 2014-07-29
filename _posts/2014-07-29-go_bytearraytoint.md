---
layout: post
title: "Golang binary包——byte数组如何转int？"
description: "看布隆过滤器源码https://github.com/willf/bloom，里面用了binary包，在这里做记录。"
category: "Hash"
tags: ["Golang", "FNV", "MD5"]
---

在C语言笔试的时候，比较喜欢考这个东西，如何将一个char数组转成int类型。当年看过，不过早就忘记了。后来看到这种东西`binary.BigEndian.Uint32(a)`，直接瞎了。后来去看[文档](http://golang.org/pkg/encoding/binary/)，看了半天也没搞明白。

在这里直接说一下，[源码](https://github.com/mnhkahn/go_code/blob/master/test_uint8arraytouint32.go)。下面这个是`uint8`，也就是`byte`数组，大小为4，转换成int32的代码。

	package main
	
	import "fmt"
	import "encoding/binary"
	
	func main() {
		var a []byte = []byte{0, 1, 2, 3}
		fmt.Println(a)
		fmt.Println(binary.BigEndian.Uint32(a))
		fmt.Println(binary.LittleEndian.Uint32(a))
	}

执行结果：

	[0 1 2 3]
	66051
	50462976

转换有两种不同的方式，也就是大端和小端。大端就是内存中低地址对应着整数的高位。按照上面的例子说，就是按照0123的顺序拼成`int32`，整数的最高8位是0，接着是1，以此类推，所以是66051。小端就是反过来，最高8位是3，也就是`00000101`，这样最后得到50462976。

在Golang源码目录`encoding/binary.go`下，有函数的实现。不过里面没有对byte数组长度的检查，如果传入的数组长度小于4，自然会报错：`panic: runtime error: index out of range`。

	func (bigEndian) Uint32(b []byte) uint32 {
		return uint32(b[3]) | uint32(b[2])<<8 | uint32(b[1])<<16 | uint32(b[0])<<24
	}

上面讲的`BigEndian`和`LittleEndian`都是实现类，都是实现的类`ByteOrder`。

	type ByteOrder interface {
        Uint16([]byte) uint16
        Uint32([]byte) uint32
        Uint64([]byte) uint64
        PutUint16([]byte, uint16)
        PutUint32([]byte, uint32)
        PutUint64([]byte, uint64)
        String() string
	}

---

######*参考文献*
+ 【1】[字节序（Endian），大端（Big-Endian），小端（Little-Endian） - 牵着老婆满街逛](http://www.cppblog.com/tx7do/archive/2009/01/06/71276.html)
+ 【2】[Package binary - The Go Programming Language](http://golang.org/pkg/encoding/binary/)

{% include JB/setup %}