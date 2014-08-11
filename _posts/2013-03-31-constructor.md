---
layout: post
title: "构造函数成员初始化列表"
description: ""
category: "Computer Science"
tags: ["Computer Science"]
---

我们平时习惯于在C++构造函数体中使用赋值操作符来初始化数据成员，其实这并不是真正的初始化过程。初始化是指使用参数表初始化。初始化列表位于构造函数参数表之后。

	class A{
	private:
		A m_a;
		A() : m_a(a);
	}

这样，初始化就在类的代码被执行之前调用，由编译器来实现。

+ 派生类可以在参数表中直接调用基类的构造函数；

	class A {
	public:
		A(int x);
	};
	class B : public A {
	private:
		B(int x, int y);
	};
	B::B(int x, int y) : A(y) { // 在初始化列表内调用A的初始化函数
	}
+ 非静态`const`成员只能在参数表中初始化；
+ 如果采用赋值操作符初始化，具体是先调用构造函数创建一个变量，然后在调用赋值函数进行赋值，效率较低；
+ 使用参数表来初始化数据成员时，初始化顺序并不一定是初始化列表的顺序，而且按照在类中声明的次序来初始化。

---

{% include JB/setup %}