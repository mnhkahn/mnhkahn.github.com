---
layout: post
title: "Golang实现大数乘法"
description: "用大数乘法实现长度不限的数字乘法。"
category: "Golang"
tags: ["Golang"]
---

大数乘法，简单的说，就是把小学学的列竖式计算的方法进行了实现。这其实也就是个乘法分配率的变形。

	5 * 12 = 5 * (2 + 10) = 5 * 2 + 5 * 10

所以第二行竖式，12的十位1与5相乘的时候，需要再最后空一位，其实是在最后省略了一个0。十位就是省略一个0，也就是左移一位，那么百位就是左移两位。以此类推。

通过代码实现，相乘的两个数就不能用整形表示了，因为存不了很大的整数。需要用字符串表示。按位相乘，最后把结果错位相加就行。乘法的结果等于乘数的位数，所以可以申请一个和乘数位数相同的数组，然后错位相加即可。但是这样太麻烦了。

![IMG-THUMBNAIL](https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeam/bignum.png)

乘法是从个位开始，但是遍历字符串是从最高为开始的，所以要首先将输入字符串反转。用i表示被乘数的遍历索引，j表示乘数的索引。前面说了左移的位数和乘数当前遍历的位相等，也就是j。相乘的时候，如果结果大于9，需要进位，现在暂不考虑进位问题。那么，结果的位数和乘数的长度将会是相等的，例子当中，都是6。如果不考虑偏移，那么乘法的结果将会和遍历的索引i相等。所以，可以得出，任意两位相乘，结果的位置是`i + j`。

	func LargeNumberMultiplication(a string, b string) (reuslt string) {
		a = strings.Reverse(a)
		b = strings.Reverse(b)
		c := make([]byte, len(a)+len(b))
	
		for i := 0; i < len(a); i++ {
			for j := 0; j < len(b); j++ {
				c[i+j] += (a[i] - '0') * (b[j] - '0')
			}
		}
	
		var plus byte = 0
		for i := 0; i < len(c); i++ {
			if c[i] == 0 {
				break
			}
			temp := c[i] + plus
			plus = 0
			if temp > 9 {
				plus = temp / 10
				reuslt += string(temp - plus*10 + '0')
			} else {
				reuslt += string(temp + '0')
			}
	
		}
		return strings.Reverse(reuslt)
	}

字符串的反转可以参考[《字符串反转》](http://blog.cyeam.com/golang/2014/08/14/go_reverse)。相乘的过程中，需要将字符和整数进行转换，通过`a[i] - '0'`和`temp + '0'`就能实现。进位在最后一并进行。通过变量`plus`保存上一次的进位数目。

本文所涉及到的完整源码请[参考](https://github.com/mnhkahn/go_code/blob/master/largenumberx.go)。

---

###### *参考文献*
+ 【1】[大数乘法](http://www2.lssh.tp.edu.tw/~hlf/class-1/lang-c/big_num3.htm)


{% include JB/setup %}
