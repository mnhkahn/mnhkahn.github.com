---
layout: post
title: "通过两个例子介绍一下 Golang For Range 循环原理"
description: "通过两个例子介绍一下 For Range 内部实现原理"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1540867053/cyeam/step_four-_subtract.png"
category: "Golang"
tags: ["golang"]
---

* 目录
{:toc}
---

### 下面的代码是死循环么？

```
func main() {
	v := []int{1, 2, 3}
	for i := range v {
		v = append(v, i)
	}
}
```

上面的代码先初始化了一个内容为1、2、3的`slice`，然后遍历这个`slice`，然后给这个切片追加元素。随着遍历的进行，数组`v`也在逐渐增大，那么这个`for`循环是一个死循环么？

答案是否。只会遍历三次，`v`的结果是`[0, 1, 2]`。并不是死循环，原因就在于`for range`实现的时候用到了语法糖。

### 语法糖

> 语法糖（Syntactic sugar），也译为糖衣语法，是由英国计算机科学家彼得·蘭丁发明的一个术语，指计算机语言中添加的某种语法，这种语法对语言的功能没有影响，但是更方便程序员使用。 语法糖让程序更加简洁，有更高的可读性。

对于切片的`for range`，它的底层代码就是：

```
//   for_temp := range
//   len_temp := len(for_temp)
//   for index_temp = 0; index_temp < len_temp; index_temp++ {
//           value_temp = for_temp[index_temp]
//           index = index_temp
//           value = value_temp
//           original body
//   }
```

可以看到，在遍历之前就获取的切片的长度`len_temp := len(for_temp)`，遍历的次数不会随着切片的变化而变化，上面的代码自然不会是死循环了。

### 下面的代码有什么问题么？

```
slice := []int{0, 1, 2, 3}
myMap := make(map[int]*int)

for index, value := range slice {
	myMap[index] = &value
}
fmt.Println("=====new map=====")
for k, v := range myMap {
	fmt.Printf("%d => %d\n", k, *v)
}
```

这也是实际编码中有可能会遇到的问题，循环切片，把切片值的地址保存到`myMap`中，这样的操作结果是：

```
=====new map=====
0 => 3
1 => 3
2 => 3
3 => 3
```

结果完全一样，都是最后一次遍历的值。通过上面的底层代码看下，遍历后的值赋给了`value`，而在我们的例子中，会把`value`的地址保存到`myMap`的值中。这里的`value`是个「全局变量」，所以赋完值之后`myMap`里面所有的值都是`value`，所以结构都是一样的而且是最后一个值。

注意，这里必须是保存指针才会有问题，如果直接保存的是`value`，因为 Golang 是值拷贝，所以值会重新复制再保存，这种情况下结果就会是正确的了。

### 切片For Range原理

总结一下，通过For Range遍历切片，***首先，计算遍历次数（切片长度）；每次遍历，都会把当前遍历到的值存放到一个全局变量`index`中。***

### 其它语法糖

另外，For Range 不光支持切片。其它的语法糖底层代码。

#### map
```
// Lower a for range over a map.
// The loop we generate:
//   var hiter map_iteration_struct
//   for mapiterinit(type, range, &hiter); hiter.key != nil; mapiternext(&hiter) {
//           index_temp = *hiter.key
//           value_temp = *hiter.val
//           index = index_temp
//           value = value_temp
//           original body
//   }
```

#### channel
```
// Lower a for range over a channel.
// The loop we generate:
//   for {
//           index_temp, ok_temp = <-range
//           if !ok_temp {
//                   break
//           }
//           index = index_temp
//           original body
//   }
```

#### 数组
```
// Lower a for range over an array.
// The loop we generate:
//   len_temp := len(range)
//   range_temp := range
//   for index_temp = 0; index_temp < len_temp; index_temp++ {
//           value_temp = range_temp[index_temp]
//           index = index_temp
//           value = value_temp
//           original body
//   }
```

#### 字符串
```
// Lower a for range over a string.
// The loop we generate:
//   len_temp := len(range)
//   var next_index_temp int
//   for index_temp = 0; index_temp < len_temp; index_temp = next_index_temp {
//           value_temp = rune(range[index_temp])
//           if value_temp < utf8.RuneSelf {
//                   next_index_temp = index_temp + 1
//           } else {
//                   value_temp, next_index_temp = decoderune(range, index_temp)
//           }
//           index = index_temp
//           value = value_temp
//           // original body
//   }
```

[完整底层代码。](https://github.com/golang/gofrontend/blob/e387439bfd24d5e142874b8e68e7039f74c744d7/go/statements.cc#L5384)

---

推荐阅读：[Go Range Loop Internals](https://garbagecollected.org/2017/02/22/go-range-loop-internals/)

---


{% include JB/setup %}
