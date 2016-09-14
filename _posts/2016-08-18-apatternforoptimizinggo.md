---
layout: post
title: "【译】优化Go的模式"
figure: "http://cyeam.qiniudn.com/gopherswrench.jpg"
description: "最近在优化Go项目，学习了一下Golang的调优相关内容。发现了一篇很不错的文章，翻译出来分享给大家。"
category: "golang"
tags: ["Golang","Optimize"]
---

之前写过一篇文章《为什么SignalFx metric proxy通过Go语言开发》，这篇文章将会关注以我们的ingest服务为例，来讲述我们是如何优化Go代码的。

SingalFx基于流分析和时间报警序列，例如应用程序指标，可以为时间序列数据的现代应用开发的高级监控平台（“我的应用程序收到了多少请求？”），还有系统级指标（“我的Linux服务器使用了多少网络流量？”）。我们用户流量很大并且粒度很高，每次用户的流量都要先通过我们的ingest服务才能访问其它的SignalFx服务。
 
###第一步：启用pprof
 
####啥是pprof？
pprof是Go语言内置的标准方法用来调试Go程序性能。可以通过HTTP的方式调用pprof包，它能提取出来应用程序的CPU和内存数据，此外还有运行的代码行数和内容信息。
 
####如何启用pprof？
你可以通过在你的应用增加一行代码 `import _ "net/http/pprof"`，然后启动你的应用服务器，pprof就算是启动了。还有一种方式，就是我们在做SignalFx的时候，为了在外部控制pprof，我们附加了一些处理程序，可以用过路由设置暴露出去，代码如下：


	import "github.com/gorilla/mux"
	import "net/http/pprof"
	var handler *mux.Router
	// ...
	handler.PathPrefix("/debug/pprof/profile").HandlerFunc(pprof.Profile)
	handler.PathPrefix("/debug/pprof/heap").HandlerFunc(pprof.Heap)


###第二步：找到可以优化的代码
 
####要执行什么？


	curl http://ingest58:6060/debug/pprof/profile > /tmp/ingest.profile
	go tool pprof ingest /tmp/ingest.profile
	(pprof) top7


####这是干嘛的？
Go语言包含了一个本地的pprof工具来可视化输出pprof的结果。我们配置的路由`/debug/pprof/profile`可以收集30秒数据。我上面的操作，第一步是保存输出到本地文件，然后运行保存后的文件。值得一提的是，最后一个参数可以直接输入一个URL来取代文件（译者注：`go  tool pprof ingest http://ingest58:6060/debug/pprof/profile`）。 命令top7可以展示消耗CPU最好的7个函数。
 
####结果


	12910ms of 24020ms total (53.75%)
	Dropped 481 nodes (cum <= 120.10ms)
	Showing top 30 nodes out of 275 (cum >= 160ms)
	     flat  flat%   sum%        cum   cum%
	   1110ms  4.62%  4.62%     2360ms  9.83%  runtime.mallocgc
	    940ms  3.91%  8.53%     1450ms  6.04%  runtime.scanobject
	    830ms  3.46% 11.99%      830ms  3.46%  runtime.futex
	    800ms  3.33% 15.32%      800ms  3.33%  runtime.mSpan_Sweep.func1
	    750ms  3.12% 18.44%      750ms  3.12%  runtime.cmpbody
	    720ms  3.00% 21.44%      720ms  3.00%  runtime.xchg
	    580ms  2.41% 23.86%      580ms  2.41%  runtime._ExternalCode
 
####为啥是这个结果
我们可以发现，这些函数我们都没有直接调用过。然而，`mallocgc`、`sacnobject`还有`mSpan_Sweep`全部都会导致是垃圾回收的时候CPU占用高。我们可以深入了解这些函数，而不是去优化Go语言的垃圾回收器本身，更好的优化办法是我们来优化我们代码里面使用Go语言的垃圾回收器的方法。在这个例子中，我们可以优化的是减少在堆上面创建对象。
 
###第三步：探究GC的原因
 
####执行啥？


	curl http://ingest58:6060/debug/pprof/heap > /tmp/heap.profile
	go tool pprof -alloc_objects /tmp/ingest /tmp/heap.profile
	(pprof) top3

####做了啥？
可以注意到这次下载的URL和之前的有点像，但是是以/heap结尾的。这个将会给我们提供机器上面堆的使用总结的数据。我再一次保存成文件用户后面的比较。参数-alloc_objects将会可视化应用程序在执行过程中分配的对象数量。
 
####结果


	4964437929 of 7534904879 total (65.89%)
	Dropped 541 nodes (cum <= 37674524)
	Showing top 10 nodes out of 133 (cum >= 321426216)
	     flat  flat%   sum%        cum   cum%
	853721355 11.33% 11.33%  859078341 11.40%  github.com/signalfuse/sfxgo/ingest/tsidcache/tsiddiskcache.(*DiskKey).EncodeOld
	702927011  9.33% 20.66%  702927011  9.33%  reflect.unsafe_New
	624715067  8.29% 28.95%  624715067  8.29%  github.com/signalfuse/sfxgo/ingest/bus/rawbus.(*Partitioner).Partition
 
####啥意思？
可以看出，11.33%的对象分配都发生在对象`DiskKey`的函数`EncodeOld`里面，我们预期也是这个结果。然而，没有料到的是Partition函数占用了全部内存分配的8.29%，因为这个函数只是一些基本的计算，我得着重研究一下这个问题。
 
###第四步：找到为什么partitioner使用如此多内存的原因
 
####执行啥？


	(pprof) list Partitioner.*Partition
 
####做了啥？
这个命令可以打印出来我关注的源代码行，还有就是函数内部哪些代码引起了堆的内存申请。这是pprof里面许多命令的其中一个。另一个非常有用的是查看调用方和被调用方。可以通过help命令查看完整的帮助并且都试一试。
 
####结果


	Total: 11323262665
	ROUTINE ======================== github.com/signalfuse/sfxgo/ingest/bus/rawbus.(*Partitioner).Partition in /opt/jenkins/workspace/ingest/gopath/src/github.com/signalfuse/sfxgo/ingest/bus/rawbus/partitioner.go
	927405893  927405893 (flat, cum)  8.19% of Total
	        .          .     64: if ringSize == 0 {
	        .          .     65: return 0, ErrUnsetRingSize
	        .          .     66: }
	        .          .     67: var b [8]byte
	        .          .     68: binary.LittleEndian.PutUint64(b[:], uint64(message.Key.(*partitionPickingKey).tsid))
	239971917  239971917     69: logherd.Debug2(log, "key", message.Key, "numP", numPartitions, "Partitioning")
	        .          .     70: murmHash := murmur3.Sum32(b[:])
	        .          .     71:
	        .          .     72: // 34026 => 66
	        .          .     73: setBits := uint(16)
	        .          .     74: setSize := uint32(1 << setBits)
	        .          .     75: shortHash := murmHash & (setSize - 1)
	        .          .     76: smallIndex := int32(shortHash) * int32(k.ringSize) / int32(setSize)
	687433976  687433976     77: logherd.Debug3(log, "smallIndex", smallIndex, "murmHash", murmHash, "shortHash", shortHash, "Sending to partition")
	        .          .     78: return smallIndex, nil
	        .          .     79:}
	        .          .     80:
 
####啥意思？
这个可以表示debug日志是引起变量从栈逃逸到堆的原因。因为调试日志并不是直接需要的，我能够直接删掉这些行。但是首先，还是让我们来确认这个假设。`logherd.Debug2`函数看起来封装了如下所示，如果日志级别debug没有符合条件，WithField对象并不会调用。


	// Debug2 to logger 2 key/value pairs and message.  Intended to save the mem alloc that WithField creates
	func Debug2(l *logrus.Logger, key string, val interface{}, key2 string, val2 interface{}, msg string) {
	     if l.Level >= logrus.DebugLevel {
	          l.WithField(key, val).WithField(key2, val2).Debug(msg)
	     }
	}

从pprof检测看起来是传递整数到`Debug2`函数引起的内存分配，让我们进一步确认。
 
###第五步：找到日志语句引起内存分配的原因
####执行什么：


	go build -gcflags='-m' . 2>&1 | grep partitioner.go
 
####这个用来干啥？
通过-m参数编译可以让编译器打印内容到stderr。这包括编译器是否能够在栈上面分配内存还是一定得将变量放到堆上面申请。如果编译器不能决定一个变量是否在外部继续被调用，他会被Go语言放到堆上面。
 
####结果


	./partitioner.go:63: &k.ringSize escapes to heap
	./partitioner.go:62: leaking param: k
	./partitioner.go:70: message.Key escapes to heap
	./partitioner.go:62: leaking param content: message
	./partitioner.go:70: numPartitions escapes to heap
	./partitioner.go:77: smallIndex escapes to heap
	./partitioner.go:77: murmHash escapes to heap
	./partitioner.go:77: shortHash escapes to heap
	./partitioner.go:68: (*Partitioner).Partition b does not escape
	./partitioner.go:71: (*Partitioner).Partition b does not escape

注意第77行，`smallIndex`、`murmHash`还有`shortHash`全部逃逸到了堆上面。编译器为短生命周期的变量在堆上面申请了空间，导致我们在对上创建了很多我们并不需要的对象。
 
###第六步：对partition函数压测
####写什么？


	func BenchmarkPartition(b *testing.B) {
	
	     r := rand.New(rand.NewSource(0))
	
	     k := partitionPickingKey{}
	
	     msg := sarama.ProducerMessage {
	
	          Key: &k,
	
	     }
	
	     p := Partitioner{
	
	          ringSize: 1024,
	
	          ringName: "quantizer.ring",
	
	     }
	
	     num_partitions := int32(1024)
	
	     for i := 0; i < b.N; i++ {
	
	          k.tsid = r.Int63()
	
	          part, err := p.Partition(&msg, num_partitions)
	
	          if err != nil {
	
	               panic("Error benchmarking")
	
	          }
	
	          if part < 0 || part >= num_partitions {
	
	               panic("Bench failure")
	
	          }
	
	     }
	
	}

压测只是简单的创建了B.N个对象，并且在返回的时候做了一个基本的检查来确认对象不会被简单的优化掉。我们推荐当程序员在优化代码之前编写压测代码来确保你在朝着正确的方向进行。
 
###第七步：对partition函数压测内存分配
####执行啥？


	go test -v -bench . -run=_NONE_ -benchmem BenchmarkPartition

####做了啥？
压测会按照正则匹配符合“.”条件的函数，-benchmen将会追踪每次循环的堆使用平均情况。通过传递参数`-run=_NONE_`，我可以节约一些时间，这样测试只会运行有“_NONE_”字符串的单元测试。换句话说，不下运行任何一个单元测试，只运行全部的压力测试。
 
####结果


	PASS

	BenchmarkPartition-8 10000000       202 ns/op      64 B/op       4 allocs/op

####意味着啥？
每一次循环消耗平均202ns，最重要的是，每个操作有4次对象分配。
 
###第八步：删掉日志语句
####咋写？


	@@ -66,7 +65,6 @@ func (k *Partitioner) Partition(message *sarama.ProducerMessage, numPartitions i
	
	       }
	
	       var b [8]byte
	
	       binary.LittleEndian.PutUint64(b[:], uint64(message.Key.(*partitionPickingKey).tsid))
	
	-       logherd.Debug2(log, "key", message.Key, "numP", numPartitions, "Partitioning")
	
	       murmHash := murmur3.Sum32(b[:])
	
	       // 34026 => 66
	
	@@ -74,7 +72,6 @@ func (k *Partitioner) Partition(message *sarama.ProducerMessage, numPartitions i
	
	       setSize := uint32(1 << setBits)
	
	       shortHash := murmHash & (setSize - 1)
	
	       smallIndex := int32(shortHash) * int32(k.ringSize) / int32(setSize)
	
	-       logherd.Debug3(log, "smallIndex", smallIndex, "murmHash", murmHash, "shortHash", shortHash, "Sending to partition")
	
	       return smallIndex, nil
	
	}

####干了什么？
我的修复方式是删除日志代码。测试期间/调试期间，我增加了这些调试代码，但是一直没有删掉它们。这种情况下，删掉这些代码最简单。
 
###第九步：重新编译评估是否变量逃逸到了堆
 
####如何执行？


	go build -gcflags='-m' . 2>&1 | grep partitioner.go

####结果


	./partitioner.go:62: &k.ringSize escapes to heap

	./partitioner.go:61: leaking param: k
	
	./partitioner.go:61: (*Partitioner).Partition message does not escape
	
	./partitioner.go:67: (*Partitioner).Partition b does not escape
	
	./partitioner.go:68: (*Partitioner).Partition b does not escape
 
####意味着什么？
可以发现`smallIndex`、`murmHash`和`shortHash`变量不在有逃逸到堆的消息。
 
###第十步：重新压测评估每个操作的内存分配情况
 
####如何执行？


	go test -v -bench . -run=_NONE_ -benchmem BenchmarkPartition

####结果


	PASS
	
	BenchmarkPartition-8 30000000        40.5 ns/op       0 B/op       0 allocs/op
	
	ok   github.com/signalfuse/sfxgo/ingest/bus/rawbus 1.267s
 
####啥意思？
注意到每个操作只消耗40ns，更重要的是，每个操作不再有内存分配。因为我是准备来优化堆，这对我来说很重要。
 
###结束语
pprof是非常有用的工具来剖析Go代码的性能问题。通过结合Go语言内置的压测工具，你能够得到关于代码改变引起的变化的真正的数字。不幸的是，性能衰退会随着时间而攀升。下一步，读者可以练习，保存benchmark的结果到数据库，这样你可以在每一次代码提交之后查看代码的性能。



---

###### 

---

{% include JB/setup %}