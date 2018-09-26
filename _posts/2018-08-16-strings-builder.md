---
layout: post
title: "strings.Builder 源码分析"
description: "Go 1.10开始，引入了期盼已久的strings.Builder，Go 的作者是不是看到雨痕大大的优化文章搞的这个呢？"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeamWX20180824-163756@2x.png?imageView2/0/q/75|watermark/1/image/aHR0cDovL2N5ZWFtLnFpbml1ZG4uY29tL2JyeWNlLmpwZw==/dissolve/60/gravity/SouthEast/dx/10/dy/10|imageslim"
category: "Golang"
tags: ["Golang","string"]
---

* 目录
{:toc}
---

众所周知，Go 里面的字符串是常量，对字符串的修改会重新申请内存地址。为了优化这个，我之前都是用 bytes.Buffer 代替字符串的拼接等操作。这种方案避免了字符串修改过程中的内存申请，但是最后从`[]byte`转成字符串时会重新内存申请，这个无法避免。从 Go 1.10 开始，提供了更友好性能更好的方法 strings.Builder。

### strings.Builder 和 bytes.Buffer 接口设计上基本一致

支持的方法是 bytes.Buffer 的子集，仔细看了一下，它实现了`io.Writer`接口，而 bytes.Buffer 实现了`io.Reader`和`io.Writer`两个接口。

> type Builder
    func (b *Builder) Grow(n int)
    func (b *Builder) Len() int
    func (b *Builder) Reset()
    func (b *Builder) String() string
    func (b *Builder) Write(p []byte) (int, error)
    func (b *Builder) WriteByte(c byte) error
    func (b *Builder) WriteRune(r rune) (int, error)
    func (b *Builder) WriteString(s string) (int, error)

```
type Writer interface {
        Write(p []byte) (n int, err error)
}
```

### 底层实现

```
type Builder struct {
	addr *Builder // of receiver, to detect copies by value
	buf  []byte
}
```

它底层还是用`[]byte`保存数据的，这和 bytes.Buffer 是一致的。

如果写入数据，就是在`[]byte`后面追加内容：

```
func (b *Builder) Write(p []byte) (int, error) {
	b.copyCheck()
	b.buf = append(b.buf, p...)
	return len(p), nil
}
```

追加内容也有讲究，因为底层是 slice，追加数据时有可能引起 slice 扩容。一般的优化方案是为 slice 初始化合理的空间，避免多次扩容复制。Builder 也提供了预分配内存的方法：

```
func (b *Builder) grow(n int) {
	buf := make([]byte, len(b.buf), 2*cap(b.buf)+n)
	copy(buf, b.buf)
	b.buf = buf
}

func (b *Builder) Grow(n int) {
	b.copyCheck()
	if n < 0 {
		panic("strings.Builder.Grow: negative count")
	}
	if cap(b.buf)-len(b.buf) < n {
		b.grow(n)
	}
}
```

注意扩容的容量和 slice 直接扩容两倍的方式略有不同，它是`2*cap(b.buf)+n`，之前容量的两倍加n。

+ 如果容量是10，长度是5，调用`Grow(3)`结果是什么？当前容量足够使用，没有任何操作；
+ 如果容量是10，长度是5，调用`Grow(7)`结果是什么？剩余空间是5，不满足7个扩容空间，底层需要扩容。扩容的时候按照之前容量的两倍再加n的新容量扩容，结果是2*10+7=27。

### String() 方法有门道

```
func (b *Builder) String() string {
	return *(*string)(unsafe.Pointer(&b.buf))
}
```

返回当前数据的字符串，先获取`[]byte`地址，然后转成字符串指针，然后再取地址。

> 从 ptype 输出的结构来看，string 可看做 [2]uintptr，而 [ ]byte 则是 [3]uintptr，这便于我们编写代码，无需额外定义结构类型。如此，str2bytes 只需构建 [3]uintptr{ptr, len, len}，而 bytes2str 更简单，直接转换指针类型，忽略掉 cap 即可。

![](https://segmentfault.com/img/bVvaxk)

详细可以参考雨痕的[【Go性能优化技巧 1/10】](https://segmentfault.com/a/1190000005006351)。

### 不允许复制

还是再看一下 Builder 的底层数据，它还有个字段`addr`，是一个指向 Builder 的指针。

```
type Builder struct {
	addr *Builder // of receiver, to detect copies by value
	buf  []byte
}
```

默认情况是它会指向自己：

```
b.addr = (*Builder)(noescape(unsafe.Pointer(b)))
```

而如果`addr`和当前指针所指地址不同，会引发`panic`异常。

```
func (b *Builder) copyCheck() {
	if b.addr == nil {
		// This hack works around a failing of Go's escape analysis
		// that was causing b to escape and be heap allocated.
		// See issue 23382.
		// TODO: once issue 7921 is fixed, this should be reverted to
		// just "b.addr = b".
		b.addr = (*Builder)(noescape(unsafe.Pointer(b)))
	} else if b.addr != b {
		panic("strings: illegal use of non-zero Builder copied by value")
	}
}
```

`copyCheck`用来保证复制后不允许修改的逻辑。仔细看下源码，如果`addr`是空，也就是没有数据的时候是可以被复制后修改的，一旦那边有数据了，就不能这么搞了。在`Grow`、`Write`、`WriteByte`、`WriteString`、`WriteRune`这五个函数里都有这个检查逻辑。

### 线程不安全

这个包并不是线程安全的，整个例子看看：

```
package main

import (
	"fmt"
	"strings"
	"sync"
	"sync/atomic"
)

func main() {
	var b strings.Builder
	var n int32
	var wait sync.WaitGroup
	for i := 0; i < 1000; i++ {
		wait.Add(1)
		go func() {
			atomic.AddInt32(&n, 1)
			b.WriteString("1")
			wait.Done()
		}()
	}
	wait.Wait()
	fmt.Println(len(b.String()), n)
}
```

结果是`902 1000`，并不都是1000。如果想保证线程安全，需要在`WriteString`的时候加锁。

```
package main

import (
	"fmt"
	"strings"
	"sync"
	"sync/atomic"
)

func main() {
	var b strings.Builder
	var n int32
	var wait sync.WaitGroup
	var lock sync.Mutex
	for i := 0; i < 1000; i++ {
		wait.Add(1)

		go func() {
			atomic.AddInt32(&n, 1)

			lock.Lock()
			b.WriteString("1")
			lock.Unlock()
			wait.Done()
		}()
	}
	wait.Wait()

	fmt.Println(len(b.String()), n)
}
```

---

###### *参考文献*
+ 【1】[7 notes about strings.builder in Golang](https://medium.com/@thuc/8-notes-about-strings-builder-in-golang-65260daae6e9)



{% include JB/setup %}
