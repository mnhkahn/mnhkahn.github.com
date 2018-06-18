---
layout: post
title: "Slice 小技巧"
description: "翻译自官方wiki说明。难度都不大但是还是写一下吧。官方的写法比较优雅。包括 slice 的插入、删除、剪切等操作。"
figure:"https://blog.golang.org/go-slices-usage-and-internals_slice-3.png"
category: "Golang"
tags: ["Golang","Slice","Trick"]
---

本文翻译自[SliceTricks](https://github.com/golang/go/wiki/SliceTricks)。我会追加一些我的理解。官方给出的例子代码很漂亮，建议大家多看看，尤其是利用多个切片共享底层数组的功能就地操作很有意思。

* 目录
{:toc}
---

`container/vector`包在 Go 1中被删除了，因为引入了内置函数`append`，它再加上内置函数`copy`基本上可以代替这个包的功能。

#### AppendVector
```go
a = append(a, b...)
```
*`append`支持两个参数，第一个是被追加的 slice，第二个参数是追加到后面的数据。第二个参数是变长参数，可以传多值。*

#### Copy
```go
b = make([]T, len(a))
copy(b, a)
// or
b = append([]T(nil), a...)
```

*`copy`函数把数据 a 复制到 b 中。它有个坑，复制数据的长度取决于 b 的当前长度，如果 b 没有初始化，那么并不会发生复制操作。所以复制的第一行需要初始化长度。*

*复制还有一种替代方案，利用`append`的多值情况来追加。但是这样会有一个问题，追加的时候是追加到`[]T(nil)`里面，默认初始长度是0，每追加一个元素需要检测当前长度是否满足，如果不满足就要扩容，每次扩容扩当前容量的一倍（详细原理可以查看 slice 的内部实现）。这么操作的话如果 a 长度是3，第一种方法复制出来长度和容量都是3，而第二种方法长度是3，容量却是4。如果只是单纯复制我推荐第一种。*

#### Cut
```go
a = append(a[:i], a[j:]...)
```
*把 [i, j)中间的元素剪切掉。slice 的切片都是前开后闭原则。*

#### Delete
```go
a = append(a[:i], a[i+1:]...)
// or
a = a[:i+copy(a[i:], a[i+1:])]
```

*删除位置 i 的元素。第一种，利用剪切的方式删除。因为只是在删除，这个`append`操作并不会引起底层数据的扩容。只不过 i 之后的数据发生了更新。此时长度减小1，容量不变。*

*第二种方式，利用`copy`方法实现。将 i 后面所有的数据迁移，然后删除最后一位数据。将 i+1 到 len(a) 的数据复制到 i 到 len(a)-1的位置上。`copy`方法的返回值是复制的元素长度，所以这里又被直接用来截断，将 a 的最后一位没有被删除的数据删除。*

*这两种操作的底层结果一致。被删除元素的后面元素都需要被复制。*

#### Delete without preserving order 不保留顺序的删除
```go
a[i] = a[len(a)-1] 
a = a[:len(a)-1]
```
*删除第 i 位的元素，把最后一位放到第 i 位上，然后把最后一位元素删除。这种方式底层并没有发生复制操作。*

**注意** 如果 slice 的类型是指向结构体的指针，或者是结构体 slice 里面包含指针，这些数据在被删除后需要进行垃圾回收来释放内存。然而上面的`Cut`和`Delete`方法有可能引起内存泄漏：被删除的数据依然被 a 所引用（底层数据中引用）导致无法进行垃圾回收。可以用下面的代码解决这个问题：

> **Cut**
```go
copy(a[i:], a[j:])
for k, n := len(a)-j+i, len(a); k < n; k++ {
	a[k] = nil // or the zero value of T
}
a = a[:len(a)-j+i]
```
*相比于之前多了一步操作，将被删除的位置置为 nil。这样指针就没有被引用的地方了，可以被垃圾回收。*

> **Delete**
```go
copy(a[i:], a[i+1:])
a[len(a)-1] = nil // or the zero value of T
a = a[:len(a)-1]
```

> **Delete without preserving order**
```go
a[i] = a[len(a)-1]
a[len(a)-1] = nil
a = a[:len(a)-1]
```

#### Expand
```go
a = append(a[:i], append(make([]T, j), a[i:]...)...)
```
*在中间位置 i 扩展长度为 j 的 slice。*

#### Extend
```go
a = append(a, make([]T, j)...)
```
*在最后延伸长度是 j 的 slice。*

#### Insert
```go
a = append(a[:i], append([]T{x}, a[i:]...)...)
```
*在位置 i 插入元素 x。*

**注意**通过第二个`append`把 a[i:] 追加到 x 后面（*这个操作会引起`[]T{x}`发生多次扩容*），然后通过第一个`append`把这个新的 slice 追加到 a[:i]后面（*这个操作会引起 a 发生一次扩容*）。这两个操作创建了一个新的 slice（这样相当于创建了内存垃圾），第二个复制也可以被避免：
> **Insert**
```go
s = append(s, 0)
copy(s[i+1:], s[i:])
s[i] = x
```
*首先通过`append`将 slice 扩容，然后把 i 后面的元素后移，最后复制。整个操作一次扩容。*

#### InsertVector
```go
a = append(a[:i], append(b, a[i:]...)...)
```
*在位置 i 插入 slice b。*

#### Pop/Shift
```go
x, a = a[0], a[1:]
```
*一行实现 pop 出队列头。*

#### Pop Back
```go
x, a = a[len(a)-1], a[:len(a)-1]
```
*一行实现 pop 出队列尾。*

#### Push
```go
a = append(a, x)
```
*push x 到队列尾。*

#### Push Front/Unshift
```go
a = append([]T{x}, a...)
```
*push x 到队列头。*

## Additional Tricks 附加技巧
### Filtering without allocating 不申请内存过滤数据

多个切片引用的底层数组是有可能是同一个，利用这个原理可以实现复用底层数组实现数据过滤。当然，过滤之后底层数组内容会被修改。

```go
b := a[:0]
for _, x := range a {
	if f(x) {
		b = append(b, x)
	}
}
```
*就地过滤。首先申明切片 b，和 a 共享底层数组。遍历 a 进行过滤，过滤后到加入 b 中。这样 a 和 b 同时被修改了。b 是过滤后正确的 slice，而 a 的数据会错乱。*

### Reversing 反转

将 slice 的数据顺序反转：
```go
for i := len(a)/2-1; i >= 0; i-- {
	opp := len(a)-1-i
	a[i], a[opp] = a[opp], a[i]
}
```
代码再简化一下，还可以将反转用到的索引省略：
```go
for left, right := 0, len(a)-1; left < right; left, right = left+1, right-1 {
	a[left], a[right] = a[right], a[left]
}
```

### Shuffling 随机

Fisher–Yates 算法:

> 需要Go 1.10 以上 [math/rand.Shuffle](https://godoc.org/math/rand#Shuffle)

```go
for i := len(a) - 1; i > 0; i-- {
    j := rand.Intn(i + 1)
    a[i], a[j] = a[j], a[i]
}
```
*每个数据随机一个新位置出来。*


---



 

{% include JB/setup %}