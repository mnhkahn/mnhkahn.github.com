---
layout: post
title: "【Go实现】熔断机制"
description: ""
figure: "https://res.cloudinary.com/practicaldev/image/fetch/s--LDr4sIMX--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://thepracticaldev.s3.amazonaws.com/i/bk0c85is3c5767cc3qzt.png"
category: "Framework"
tags: ["go","circuitbreaker"]
---

* 目录
{:toc}
---

### 什么是熔断？

熔断是指在下游发生错误时上游主动关闭或限制对下游的请求。

![](https://res.cloudinary.com/cyeam/image/upload/v1610534796/image.png)

### 原理

1. 通常熔断器分为三个时期: CLOSED，OPEN，HALFOPEN
2. RPC正常时，为CLOSED；
3. 当RPC错误增多时，熔断器会被触发, 进入OPEN；
4. OPEN后经过一定的冷却时间，熔断器变为HALFOPEN；
5. HALFOPEN时会对下游进行一些有策略的访问, 然后根据结果决定是变为CLOSED，还是OPEN；

总得来说三个状态的转换大致如下图：

![](https://res.cloudinary.com/practicaldev/image/fetch/s--LDr4sIMX--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://thepracticaldev.s3.amazonaws.com/i/bk0c85is3c5767cc3qzt.png)

### Go 实现

[https://github.com/rubyist/circuitbreaker](https://github.com/rubyist/circuitbreaker)

1. IsAllowed 是否允许请求，根据当前状态判断
	- CLOSE 允许
	- OPEN
		- 在 CoolingTimeout 冷却时间内，不允许
		- 过了冷却时间，状态变为 HALFOPEN，允许访问


`atomic.StoreInt32((*int32)(&b.state), int32(HALFOPEN))`


	- HALFOPEN
		- 在 DetectTimeout 检测时间内，允许访问
		- 否则不允许

2. trip 判断是否达到熔断限额（可以自定义）

```
type TripFunc func(Metricser) bool
```


	- ThresholdTripFunc 错误阈值
	- ConsecutiveTripFunc 连续错误超过阈值
	- RateTripFunc 根据最少访问数和错误率判断

3. Metricser 访问统计，包括成功数、失败数、超时数、错误率、采样数、连续错误数

```
type Metricser interface {
   Fail()    // records a failure
   Succeed() // records a success
   Timeout() // records a timeout

   Failures() int64    // return the number of failures
   Successes() int64   // return the number of successes
   Timeouts() int64    // return the number of timeouts
   ConseErrors() int64 // return the consecutive errors recently
   ErrorRate() float64 // rate = (timeouts + failures) / (timeouts + failures + successes)
   Samples() int64     // (timeouts + failures + successes)
   Counts() (successes, failures, timeouts int64)

   Reset()
}
```


	- window 实现类

```
type window struct {
   sync.RWMutex
   oldest  int32     // oldest bucket index
   latest  int32     // latest bucket index
   buckets []bucket // buckets this window holds

   bucketTime time.Duration // time each bucket holds
   bucketNums int32         // the numbe of buckets
   inWindow   int32         // the number of buckets in the window

   allSuccess int64
   allFailure int64
   allTimeout int64

   conseErr int64
}

type bucket struct {
   failure int64
   success int64
   timeout int64
}
```


用环形队列实现动态统计。把一个连续的时间切成多个小份，每一个 bucket 保存 BucketTime 的统计数据，BucketTime * BucketNums 是统计的时间区间。

每 BucketTime，会有一个 bucket 过期

```
if w.inWindow == w.bucketNums {
   // the lastest covered the oldest(latest == oldest)
   oldBucket := &w.buckets[w.oldest]
   atomic.AddInt64(&w.allSuccess, -oldBucket.Successes())
   atomic.AddInt64(&w.allFailure, -oldBucket.Failures())
   atomic.AddInt64(&w.allTimeout, -oldBucket.Timeouts())
   w.oldest++
   if w.oldest >= w.bucketNums {
      w.oldest = 0
   }
} else {
   w.inWindow++
}

w.latest++
if w.latest >= w.bucketNums {
   w.latest = 0
}
(&w.buckets[w.latest]).Reset()
```

4. Panel Metricser 的容器
5. PanelStateChangeHandler 熔断事件

```
type PanelStateChangeHandler func(key string, oldState, newState State, m Metricser)
```


#### 缺陷

1. 所有 breaker 公用同一个 BucketTime，统计周期不支持更新
2. 冷却时间不支持动态更新


---


{% include JB/setup %}
