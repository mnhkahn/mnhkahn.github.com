---
layout: post
title: "【译】并发、协程和GOMAXPROCS"
description: "第一次翻译英文的文章。协程这个东西之前面试被问过，这次终于明白些了。之前只知道它是一个轻量级线程，其实感觉就是又多包了一层。"
category: "Golang"
tags: ["Golang", "Concurrency"]
---
 
####介绍

当有新人加入Go-Miami组，他们经常希望去学习的并发模型。当我刚刚开始听说Go语言的时候，并发似乎看起来是这门语言的热门词汇。当我看了Rob Pike的[Go并发模式](http://www.youtube.com/watch?v=f6kdp27TYZs)的视频之后，我认为我应该去学习这门语言了。

为了去理解是如何通过Go语言编写出更简单、难出错的并发程序，我们首先需要去理解什么是并发程序和并发程序的结果是什么这两个问题。我不会去讲述CSP（通信顺序进程、Communicating Sequential Processes），这是Go语言实现管道（channel）的基础。这篇文章将着重讲并发是什么，协程的角色是什么，环境变量GOMAXPROCS和运行时函数如何影响Go语言的程序的执行。

####进程和线程

当我们运行一个应用，比如我写这篇文章用的浏览器，操作系统会为这个应用创建一个进程。进程的任务就像是一个容器，为这个应用运行的时候使用和管理资源。这些资源包括内存地址空间、指向文件的句柄、设备和线程。

线程是执行的一部分，它会被操作系统调度去执行进程里面、被我们在函数里面实现的代码。一个进程开始于一个线程，也叫做主线程，当这个线程结束整个进程也会随之结束。这是因为主线程是应用程序的来源。主线程可以反过来创建更多的线程，而这些线程还能创建更多的线程。

操作系统可以调度一个线程在一个可用的处理器上面执行，而不管处理这个线程的父线程在哪个处理器上面执行。每个操作系统都有自己的调度算法，并不是特定的一种，来决定最好的方式让我们开发并行程序。并且这些算法将会随着操作系统的每次升级发生改变，这个需要我们注意。

####协程和并行

Go语言里面任何函数或者方法可以创建一个协程。我们可以认为主方法执行起来是一个协程，然而Go的运行时并没有启动这个协程。协程可以认为是轻量级的，因为它们占用很小的内存和资源，并且它初始化的栈空间也很小。早先的Go语言1.2版本栈空间会被初始化为4K，目前的1.4版本会被初始化为8K。这个栈可以随着需要自动增加空间。

操作系统调度可用的处理器来执行线程，Go的运行时会通过一个操作系统线程来调度协程。默认情况下，Go的运行时会分配一个逻辑处理器来执行代码里面定义的全部协程。甚至通过这一个逻辑处理器和操作系统线程，成百上千个协程可以被并发的高效迅速地调用执行。不建议添加更多的逻辑处理器，但如果你想在并行运行协程，Go提供了通过GOMAXPROCS环境变量或运行时函数来增加逻辑处理器。

并发并不是并行。并行是在多核处理器不能的核同时并行得执行两个或两个以上的线程。如果你配置运行时的逻辑处理器多于1个，调度器将会在这些逻辑处理器上面分配协程，这样做的结果就是在不同的操作系统线程上面执行多个协程。然而，想要真正的实现并行执行你的服务器必须是多核处理器。如果不是，即使Go的运行时被设置为需要多个逻辑处理器，协程仍会并发的在同一个处理处理器上面执行协程。

####并发的例子

我们来创建一个小程序来展示Go并发执行协程s。这个例子我们是在默认设置下面执行，默认设置是要使用一个逻辑处理器。

	package main

	import (
	    "fmt"
	    "sync"
	)

	func main() {
	    var wg sync.WaitGroup
	    wg.Add(2)

	    fmt.Println("Starting Go Routines")
	    go func() {
		defer wg.Done()

		for char := 'a'; char < 'a'+26; char++ {
		    fmt.Printf("%c ", char)
		}
	    }()

	    go func() {
		defer wg.Done()

		for number := 1; number < 27; number++ {
		    fmt.Printf("%d ", number)
		}
	    }()

	    fmt.Println("Waiting To Finish")
	    wg.Wait()

	    fmt.Println("\nTerminating Program")
	}

这个程序通过关键字`go`启动了两个协程，声明了两个匿名函数。第一个协程打印了小写英语字母表，第二个打印了1到26这些数字。当我们运行这个程序，将会得到以下的结果：


	Starting Go Routines
	Waiting To Finish
	a b c d e f g h i j k l m n o p q r s t u v w x y z 1 2 3 4 5 6 7 8 9 10 11
	12 13 14 15 16 17 18 19 20 21 22 23 24 25 26
	Terminating Program


我们来看一下输出的结果，代码被并发的执行。一旦这两个协程被启动，主的协程将会等待这两个协程执行结束。我们需要用这个方法否则一旦主协程运行结束，整个程序就结束了。`WaitGroup`是一个不错的方来用来在不同的协程之间通信是否完成。

我们可以发现第一个协程完整地展示了26个字母之后，第二个协程才开始展示26个数字。因为这两个协程执行速度太快，毫秒时间内就能执行结束，我们并没有能够看到是否调度器在第一个协程执行完之前中断了它。我们可以在第一个协程里面增加一个等待时间来判断调度器的策略。

	package main

	import (
	    "fmt"
	    "sync"
	    "time"
	)

	func main() {
	    var wg sync.WaitGroup
	    wg.Add(2)

	    fmt.Println("Starting Go Routines")
	    go func() {
		defer wg.Done()

		time.Sleep(1 * time.Microsecond)
		for char := 'a'; char < 'a'+26; char++ {
		    fmt.Printf("%c ", char)
		}
	    }()

	    go func() {
		defer wg.Done()

		for number := 1; number < 27; number++ {
		    fmt.Printf("%d ", number)
		}
	    }()

	    fmt.Println("Waiting To Finish")
	    wg.Wait()

	    fmt.Println("\nTerminating Program")
	}

这次我们在第一个协程里面增加了1秒钟的等待时间，调用`sleep`导致了调度器交换了两个协程的执行顺序：

	Starting Go Routines
	Waiting To Finish
	1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 a
	b c d e f g h i j k l m n o p q r s t u v w x y z
	Terminating Program

这次数字在字母前面。`sleep`会影响调度器停止第一个协程，先执行第二个协程。

####并行的例子

我们上面的两个例子协程都是在并发执行，并不是并行的。我们改变一下代码来允许代码并行执行。我们需要做的就是为调度器增加一个逻辑处理器让他能够使用两个线程：

	package main

	import (
	    "fmt"
	    "runtime"
	    "sync"
	)

	func main() {
	    runtime.GOMAXPROCS(2)

	    var wg sync.WaitGroup
	    wg.Add(2)

	    fmt.Println("Starting Go Routines")
	    go func() {
		defer wg.Done()

		for char := 'a'; char < 'a'+26; char++ {
		    fmt.Printf("%c ", char)
		}
	    }()

	    go func() {
		defer wg.Done()

		for number := 1; number < 27; number++ {
		    fmt.Printf("%d ", number)
		}
	    }()

	    fmt.Println("Waiting To Finish")
	    wg.Wait()

	    fmt.Println("\nTerminating Program")
	}

这是程序的输出：

	Starting Go Routines
	Waiting To Finish
	a b 1 2 3 4 c d e f 5 g h 6 i 7 j 8 k 9 10 11 12 l m n o p q 13 r s 14
	t 15 u v 16 w 17 x y 18 z 19 20 21 22 23 24 25 26
	Terminating Program

每一次我们运行这个程序将会得到不同的结果。调度器并不会每一次都执行得到相同的结果。我们可以看到协程这次真的是并行执行了。两个协程立刻开始运行，并且你可以看到两个都在竞争输出各自的结果。

####结论

我们可以为调度器增加多个逻辑处理器，但这不意味着我们必须要这么做。Go团队把运行时的并行数默认设为1是有原因的。随意添加逻辑处理器和并行的协程并不会一定为你的程序提供更好的性能。要做好性能压力测试，确保修改Go运行时GOMAXPROCS一定能优化性能时再这么做。

在我们的应用里面创建并发的协程，这个问题最终将会导致我们的协程可以同时尝试访问同样的资源。读写共享资源一定要是原子性的。换句话说，读和写操作一定要在一个协程里面同一个时刻只有一个操作被执行，否则我们就需要在代码里面创建临界条件。学习更多的[竞争条件](http://www.goinggo.net/2013/09/detecting-race-conditions-with-go.html)可以读这篇文章。

管道是Go语言里面安全和优雅的编写并发程序的方法，它消除了编写竞争条件，可以使得开发并行程序更加有趣。我们现在已经知道协程是如何工作、被调度和如果并行执行，接下来我们将会讲述管道。

---

######*参考文献*
1. [Concurrency, Goroutines and GOMAXPROCS](http://www.goinggo.net/2014/01/concurrency-协程s-and-gomaxprocs.html)
2. [并发和并行的区别：吃馒头的比喻](http://developer.51cto.com/art/200908/141553.htm)

{% include JB/setup %}