---
layout: post
title: "【译】在 Go 语言中使用猴子补丁"
description: "最近写单元测试多亏了这个 monkey 包，昨天看到了官方的原理介绍，很受启发，翻译出来大伙一起看看。"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeamMSM010-2.jpg?imageView2/0/q/75|watermark/1/image/aHR0cDovL2N5ZWFtLnFpbml1ZG4uY29tL2JyeWNlLmpwZw==/dissolve/60/gravity/SouthEast/dx/10/dy/10|imageslim"
category: "Golang"
tags: ["Golang","Monkey Patch"]
---

* 目录
{:toc}
---

很多人认为**猴子补丁**（A [monkey patch](https://en.wikipedia.org/wiki/Monkey_patch) is a way for a program to extend or modify supporting system software locally (affecting only the running instance of the program). 指可以在运行时动态修改或扩展程序的一种方法）是那些语言，比如 Ruby 和 Python 才有的东西。这并不对，计算机只是愚蠢的机器而我们总能让他们按照我们的想法工作！让我们来看看 Go 的函数如何工作，再看看我们如何在运行时修改它们。这篇文章将会使用 Intel 的汇编语法，所以我假设你了解过它或者在阅读的过程中参考[官方文档](https://software.intel.com/en-us/articles/introduction-to-x64-assembly)。

**如果你对猴子补丁的原理没有兴趣，只想使用猴子补丁，可以直接移步到[代码仓库](https://github.com/bouk/monkey)。**

看看下面的代码反编译之后的结果：

```
package main

func a() int { return 1 }

func main() {
  print(a())
}
```

编译完成后通过[Hopper](http://hopperapp.com/)查看，上面的代码将会展示下面的汇编代码：

![](https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeamy2yaYfm.png)

我将参考屏幕左侧显示的各种指令的地址。

我们的代码从过程`main.main`开始，指令 0x2010 到 0x2026 初始化了栈。你可以参考这些[扩展阅读](https://dave.cheney.net/2013/06/02/why-is-a-goroutines-stack-infinite)，下面的文章将会忽略那些代码。

0x202a 行调用了函数`main.a`，0x2000 行简单得把 0x1 压入栈返回。0x202f 到 0x2037 行把值传给了`runtime.printint`。

够简单了！现在咱们一起看看 Go 里面的函数值是如何实现的。

### Go 语言中函数值如何工作

看下面的代码：

```
package main

import (
  "fmt"
  "unsafe"
)

func a() int { return 1 }

func main() {
  f := a
  fmt.Printf("0x%x\n", *(*uintptr)(unsafe.Pointer(&f)))
}
```

在第11行把`a`赋值给了`f`，这就意味着调用`f()`将会调用`a`。接下来用`unsafe`包读取出存在`f`里面的值。如果你是有 C 语言背景的程序员你可能会认为简单得把指向函数`a`的指针打印出来将会得到 0x2000（就是上面汇编里面看到的地址）。当我运行上面的代码得到了 0x102c38，这个地址相差了十万八千里！反编译后，这是第11行的代码：

![](https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeamnAF7zmI.png)

这里引用了`main.a.f`，我们看看那个位置，可以发现：

![](https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeame26F32n.png)

啊哈！`main.a.f`在 0x102c38 并且包含值 0x2000，它正好是`main.a`的地址。看起来`f`并不是指向函数的指针，而是指向函数的指针的指针。让我们修改代码证实：

```
package main
 
import (
  "fmt"
  "unsafe"
)
 
func a() int { return 1 }
 
func main() {
  f := a
  fmt.Printf("0x%x\n", **(**uintptr)(unsafe.Pointer(&f)))
}
```

和我们期望的一样，将会打印 0x2000。在[这里](https://github.com/golang/go/blob/e9d9d0befc634f6e9f906b5ef7476fbd7ebd25e3/src/runtime/runtime2.go#L75-L78)我们也能找到一些线索。Go 语言的函数值包含了额外的信息，这是闭包和绑定实例实现的方式。

```
type funcval struct {
	fn uintptr
	// variable-size, fn-specific data here
}
```

接下来看看调用函数值的实现。把代码改成下面这样，给`f`赋值之后调用它。

```
package main

func a() int { return 1 }

func main() {
	f := a
	f()
}
```

反编译后可以得到下面的结果：

![](https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeambQr6Nbr.png)

`main.a.f`加载到寄存器`rdx`里，然后把`rdx`寄存器指向的地址存入`rbx`里，最后调用。函数的地址值总是会加载到`rdx`寄存器里面，当代码调用的时候可以用来加载一些可能会用到的额外信息。这里的额外信息是指向绑定的实例和匿名函数闭包的指针。如果你想了解更多我建议你深入研究一下反编译代码！

让我们用新的知识实现 Go 语言里面的猴子补丁。

### 运行时替换函数

我们是想实现的是让下面的代码打印出来2:

```
package main

func a() int { return 1 }
func b() int { return 2 }

func main() {
	replace(a, b)
	print(a())
}
```

如何实现`replace`?我们需要修改函数`a`，让它跳转到`b`的代码，跳过执行它自己的代码。实际上，我们需要通过这种方法来实现替换，加载函数`b`到寄存器`rdx`，然后执行时跳转到`rdx`上面。

```
mov rdx, main.b.f ; 48 C7 C2 ?? ?? ?? ??
jmp [rdx] ; FF 22
```

我在汇编代码旁边附上了相应的机器码（你可以用[这种](https://defuse.ca/online-x86-assembler.htm)在线汇编工具来模拟测试）。编写一个生成上面汇编代码的函数就很简单了，类似于下面这样：

```
func assembleJump(f func() int) []byte {
  funcVal := *(*uintptr)(unsafe.Pointer(&f))
  return []byte{
    0x48, 0xC7, 0xC2,
    byte(funcval >> 0),
    byte(funcval >> 8),
    byte(funcval >> 16),
    byte(funcval >> 24), // MOV rdx, funcVal
    0xFF, 0x22,          // JMP [rdx]
  }
}
```

这样就能把`a`的函数体指向`b`了！下面的代码尝试复制机器代码到函数题上。

```
package main

import (
	"syscall"
	"unsafe"
)

func a() int { return 1 }
func b() int { return 2 }

func rawMemoryAccess(b uintptr) []byte {
	return (*(*[0xFF]byte)(unsafe.Pointer(b)))[:]
}

func assembleJump(f func() int) []byte {
	funcVal := *(*uintptr)(unsafe.Pointer(&f))
	return []byte{
		0x48, 0xC7, 0xC2,
		byte(funcVal >> 0),
		byte(funcVal >> 8),
		byte(funcVal >> 16),
		byte(funcVal >> 24), // MOV rdx, funcVal
		0xFF, 0x22,          // JMP [rdx]
	}
}

func replace(orig, replacement func() int) {
	bytes := assembleJump(replacement)
	functionLocation := **(**uintptr)(unsafe.Pointer(&orig))
	window := rawMemoryAccess(functionLocation)
	
	copy(window, bytes)
}

func main() {
	replace(a, b)
	print(a())
}
```

运行上面的代码并不会工作，结果会是 segementation fault 段错误。这是因为加载后的二进制文件[默认不允许修改](https://en.wikipedia.org/wiki/Segmentation_fault#Writing_to_read-only_memory)。我们可以使用系统调用`mprotect`来关掉这个保护，这个最终版的代码终于可以像期望的那样，通过调用替换后的函数来打印出来 2。

```
package main

import (
	"syscall"
	"unsafe"
)

func a() int { return 1 }
func b() int { return 2 }

func getPage(p uintptr) []byte {
	return (*(*[0xFFFFFF]byte)(unsafe.Pointer(p & ^uintptr(syscall.Getpagesize()-1))))[:syscall.Getpagesize()]
}

func rawMemoryAccess(b uintptr) []byte {
	return (*(*[0xFF]byte)(unsafe.Pointer(b)))[:]
}

func assembleJump(f func() int) []byte {
	funcVal := *(*uintptr)(unsafe.Pointer(&f))
	return []byte{
		0x48, 0xC7, 0xC2,
		byte(funcVal >> 0),
		byte(funcVal >> 8),
		byte(funcVal >> 16),
		byte(funcVal >> 24), // MOV rdx, funcVal
		0xFF, 0x22,          // JMP rdx
	}
}

func replace(orig, replacement func() int) {
	bytes := assembleJump(replacement)
	functionLocation := **(**uintptr)(unsafe.Pointer(&orig))
	window := rawMemoryAccess(functionLocation)
	
	page := getPage(functionLocation)
	syscall.Mprotect(page, syscall.PROT_READ|syscall.PROT_WRITE|syscall.PROT_EXEC)
	
	copy(window, bytes)
}

func main() {
	replace(a, b)
	print(a())
}
```

### 封装到库中

我把上面的代码[封装到了一个易用的库](https://github.com/bouk/monkey)中。它支持32位，关闭补丁，对实例打方法补丁。我在 README 中写了一些例子。

### 结论

有志者事竟成！我们可以在运行时修改程序了，它能让我们做一些很酷的事情，例如猴子补丁。

我希望你读了本文之后能有所收获，我玩得很开心！

[Hacker News](https://news.ycombinator.com/item?id=9290917)

[Reddit](https://www.reddit.com/r/golang/comments/30try1/monkey_patching_in_go/)

[原文地址](http://bouk.co/blog/monkey-patching-in-go/)。

---





{% include JB/setup %}
