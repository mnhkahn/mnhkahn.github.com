---
layout: post
title: "位运算符(Bitwise Operators)"
description: "位运算符的一些介绍。"
category: "Computer"
tags: ["Bitwise", "Computer Science"]
---

### 按位与&(bitwise AND)

+ 两个都是1时结果才为1
+ `e.g. 1&0=0, 0&1=0, 0&0=0, 1&1=1`
+ 任意一位，和0与操作，结果都为0；和1与操作，结果不变
+ 经常用来屏蔽某些二进制位

### 按位或|(bitwise inclusive OR)

+ 两个有一个是1结果就为1
+ `e.g. 1|1=1, 1|0=1, 0|0=0, 0|1=1`
+ 任意一位，与0或操作，结果不变；与1或操作，变为1
+ 经常用来将某些二进制位设为1

### 按位异或^(bitwise exclusive OR)
+ 当两位相异时，结果为1
+ `e.g. 1^1=0, 1^0=1, 0^1=1, 0^0=0`
+ 可以简单的理解为不进位加法,1+1=0, 0+0=0, 1+0=1,  0+1=1 
+ 任意一位，和0异或操作不变，和自身异或操作为0
+ 对于任何数,都有A^0=A A^A=0
+ 自反性：A^B^A=B^0=B

### 左移运算符<<(left shift)
+ 高位左移后溢出,右边用0补
+ 左右移位比乘除法效率高。左移用来计算乘法，n<<2等效于n*2

### 右移运算符>>(right shift)
+ 由于数字采用补码表示，右移时，正数低位右移溢出，左边用0补；负数右移溢出后用1补
+ `e.g. 00001010>>2 = 00000010 10001010>>3 = 11110001`
+ 右移用来计算正数的除法(向下取整)

### 取反操作符~(one’s complement)
+ 求该数反码，该数二进制位上1变为0，0变为1

## 常见面试题：
+ 设置一个数的某一位为1

		n |= 1 << x;

+ 清除一个数的某一位

		if (n & (1 << x))

+ 开关某一位

		n &= ~(1 << x);

+ 检查某一位状态

		n ^= 1 << x;

## 实例代码：
 
	int n = 5; // 101(binary)
	int x = 1;
	
	// 设置一个数的某一位(x)为1
	n |= 1 << x;
	// x = 00000000000000000000000000000111(binary)
	printf("n=%dn", n);
	
	// 检查某一位状态
	if (n & (1 << x))
	printf("onn");
	else
	printf("offn");
	
	// 清除一个数的某一位
	n &= ~(1 << x);
	// x = 00000000000000000000000000000101(binary)
	printf("n=%dn", n);
	
	// 开关某一位(如果打开，则关闭；反之，则打开)
	n ^= 1 << x;
	// x = 00000000000000000000000000000111(binary)
	printf("n=%dn", n);
	
	//使用异或交换两个整数
	//a' = a ^ b
	//b' = b ^ a' = b ^ a ^ b = a
	//a' = a' ^ b = a ^ b ^ b = b
	//00000000000000000000000000001011 ^ 00000000000000000000000000101101 = 0000000000000000000
	//00000000000000000000000000101101 ^ 00000000000000000000000000100110 = 0000000000000000000
	//00000000000000000000000000001011 ^ 00000000000000000000000000100110 = 0000000000000000000
	int a = 11;
	int b = 45;
	a = a ^ b;
	b = b ^ a;
	a = a ^ b;
	printf("使用异或交换11和45: %d %dn", a, b);

+ 计算一个正数的二进制数中1的个数。

可以借鉴上面的题目2，逐位判断是否为1。从最低位开始判断，下次判断倒数第二位，以此类推，但是不能进行通过右移操作来实现(因为右移涉及到正负数问题，会引入新的1进来)。可以移动用来判断的位。

	int NumberOfOne(int n) {
		int on = 0;
		unsigned int flat = 1;
		while (flag)
		{
			if (n & flag)
			on++;
			flag = flag << 1;
		}
		return on;
	}

+ 一个数组中有多个整数，其中只有一个没有重复过，求出该数。

考虑使用异或操作帮助实现。
 
	int AppearOnce(int data[], int length)
	{
		int i;
		int once = 0;
		for (i = 0; i < length; i++)
		{
			once ^= data[i];
		}
		return once;
	}

+ 不用+、-、*、/四则运算计算处两个数的和。

异或操作可以理解为不进位加法，所以先将两个数异或，然后再加入进位来实现。进位只要在1+1的时候才会出现，所以可以使用1&1来代替，如果两个数都是1，与操作得到1，然后左移1位得到10，实现了进位。
 
	int add(int a, int b) {
		int sum, carry;
		do {
			sum = a ^ b;
			carry = (a & b) << 1;
			
			a = sum; 
			b = carry;
		} while (b != 0);
		
		return a;
	}

---


{% include JB/setup %}
