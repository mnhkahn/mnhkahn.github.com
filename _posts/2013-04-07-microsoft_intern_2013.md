---
layout: post
title: "微软2013年夏季实习生笔试题"
description: "2013 Microsoft Campus Intern Hiring Written Test"
category: "Collection"
tags: ["Job", "Exam"]
---

#####1. Which of the following convension(s) support(s) support variable length parameter (e.g. printf)? (3 Points)

A. cdecl

B. stdcall

C. pascal

D. fastcall

#####2.What's the output of the following code? (3 Points)

	class A
	{
	public:
	    virtual void f()
	    {
	        cout << "A::f()" << endl;
	    }
	    void f() const
	    {
	        cout << "A::f() const" << endl;
	    }
	};
	
	class B: public A
	{
	public:
	    void f()
	    {
	        cout << "B::f()" << endl;
	    }
	    
	    void f() const
	    {
	        cout << "B::f() const" << endl;
	    }
	};
	
	void g(const A *a)
	{
	    a->f();
	}
	
	int main()
	{
	    A *a = new B();
	    a->f();
	    g(a);
	    delete a;
	}

A. `B::f() B::f() const`

B. `B::f() A::f() const`

C. `A::f() B::f() const`

D. `A::f() A::f() const`

#####3.What is the difference between a linked list and an array? (3 Points)

A. Search complexity when both are sorted

B. Dynamically add/remove

C. Random access efficiency

D. Data storage type

#####4.About the Thread and Process in Windows, which description(s) is (are) correct? (3 Points)

A. One application in OS must have one Process, but not a necessary to have one Thread

B. Thre process could have its own Stack but the thread only could share the Stack of its parent Process

C. Thread must belong to a Process

D. Thread could change its belonging Process

#####5.What is the output of the following code? (3 Points)

	{
	    int x = 10;
	    int y = 10;
	    x = x++;
	    y = ++y;
	    
	    printf("%d, %d\n", x, y);
	}

A. 10, 10

B. 10, 11

C. 11, 10

D. 11, 11

#####6.For the following Java or C# code (3 Points)

	int[][] myArray3 =
        new int[3][] {
            new int[3]{5, 6, 2},
            new int[5]{6, 9, 7, 8, 3},
            new int[2]{3, 2}
        };

What will `myArray3[2][2]` return?

A. 9

B. 2

C. 6

D. overflow

#####7.Please choose the right statement about const usage: (3 Points)

A. const int a; // const integer

B. int const a; // const integer

C. int const *a; // a pointer which point to const integer

D. const int *a; // a const pointer which point to integer

E. int const *a; // a const pointer which point to integer

#####8.Given the following code: (3 Points)

	#include <iostream>
	class A
	{
	public:
	    long a;
	};
	
	class B: public A
	{
	public:
	    long b;
	}
	
	void seta(A *data, int idx)
	{
	    data[idx].a = 2;
	}
	
	int _tmain(int argc, _TCHAR *argv[])
	{
	    B data[4];
	    
	    for (int i = 0; i < 4; ++i)
	    {
	        data[i].a = 1;
	        data[i].b = 1;
	        seta(data, i);
	    }
	    
	    for (int i = 0; i < 4; ++i)
	    {
	        std::cout << data[i].a << data[i].b;
	    }
	    
	    return 0;
	}

What is the correct result?

A. 11111111

B. 12121212

C. 11112222

D. 21212121

#####9.1 of 1000 bottles of water is poisoned which will kill a rat in 1 week if the rat drunk any amount of the water. Given the bottles of water have no visual difference, how many rates are needed at least to find the poisoned one in 1 week? (5 Points)

A. 9

B. 10

C. 32

D. 999

E. None of the above

***为每瓶水编号，从1～1000，然后转成二进制，从0000000001~1111100111，找十只老鼠，按照二进制位对应得给老鼠喝水。最后查看死掉的老鼠编号，就能对应找到水的二进制编码。

#####10.Which of following statement(s) eaual(s) value 1 in C programming language? (5 Points)

A. the return value of main function if program ends normally

B. return (7 & 1);

C. char *str = "microsoft"; return str == "microsoft";

D. return "microsoft" == "microsoft";

E. None of the above

#####11.If you computed 32 bit signed integers F and G from 32 bit signed integer X using F = X/2 and G = (X >> 1), and if you found F != G, this implies that (5 Points)

A. There's a compiler error

B. x is odd

C. X is negative

D. F - G = 1

E. G - F = 1

#####12.How many rectangles you can find from 3 * 4 grid?***D*** (5 Points)

A. 18

B. 20

C. 40

D. 60

E. None of the above is correct

***3*4的网格，内部包含多少个矩形。长度取值有三种情况（1、2、3），宽度取值有四种情况（1、2、3、4），一共是C_{3}^{1}times C_{4}^{1}=12次。按照长宽的不同取值去计算，这样就不会少了。***

1*1：12个；
1*2：9个；
1*3：4个；
2*1：8个；
2*2：6个；
2*3：3个；
3*1：6个；
3*2：4个；
3*3：2个；
4*1：3个；
4*2：2个；
4*3：1个。一共60个。

#####13.One line can split of a surface to 2 parts, 2 lines can split a surface to 4 parts. Given 100 lines, no two parallel lines, no three lines join at same point, how many parts can 100 lines split? (5 Points)

A. 5051

B. 5053

C. 5510

D. 5511

#####14.Which of the following sorting algorithm(s) is(are) stabe sorting? (5 Points)

A. bubble sort

B. quicksort

C. heap sort

D. merge sort

E. Selection sort

#####15.Model-View-Contrller (MVC) is an architectural pattern that is frequently used in web applications. Which of the following statement(s) is(are) correct? (5 Points)

A. Models often represent data and the business logics needed to manipulate the data in the application

B. A View is a (visual) representation of its model. It renders the model into a form suitable for interaction, typically a user interface element

C. A controller is the linke between a user and the system. It accepts input from the user and instructs the model and a view to perform actions based on that input

D. The common practice of MVC in web applications is, the model receives GET or POST input from user and decides what to do with it, handing over to controller and which hand control to views (HTML-generating components)

#####16.We can recover the binary tree if given the output of (5 Points)

A. Preorder traversal and inorder traversal

B. Preorder traversal and postorder traversal

C. Inorder traversal and postorder traversal

D. Postorder traversal

#####17.Given a string with n characters, suppose all the characters are different from each other, how many substrings do we have? (5 Points)***C***

A. n + 1

B. n^2

C. n(n+1)/2

D. 2^n-1

E. n!

***首先想到的是，定位一个开头，一个结束位置。开头位置好定义，是n，结束位置要受开头位置影响，因为必须要在它后面。如果定义在最前面，那么结束位置有n-1个选择；如果是第二个，那么是n-2。依次类推，如果开头定位在最后一位，那么结束也只能是最后一位，为1。是一个等差数列相加。***

***还有一种解法，按照长度计算。如果长为1，有n中情况，长为2，有n-1中情况……长为n，只有一种情况。结果就是1+2+...n=n(n+1)/2***

#####18.Given the following database table, how many rows will the following SQL statement update? (5 Points)

	update Books set NumberofCopies = NumberOfCopies + 1 Where AuthorID
	in
	Select AutorID from Books
	group by AuthorID
	having sum(NumberOfCopies) <= 8

|| BookID || Title || Category || NumberOfCopies || AuthorID ||
|| 1 || SQL Server 2008 || MS || 3 || 1 ||
|| 2 || SharePoint 2007 || MS || 2 || 2 ||
|| 3 || SharePoint 2010 || MS || 4 || 2 ||
|| 5 || DB2 || IBM || 10 || 3 ||
|| 7 || SQL Server 2012 || MS || 6 || 1 ||

A. 1

B. 2

C. 3

D. 4

E. 5

#####19.What is the sortest path between S and node T, given the graph below? Note: the numbers represent the lengths of the connected nodes (13 Points)

![IMG-THUMBNAIL](https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeam/msintern2013.png)

#####20.Given a set of N balls and one of which is defective (weighs less than others), you are allowed to weigh with a balance 3 times to find the defective. Which of the following are possible N? (13 Points)

A. 12

B. 16

C. 20

D. 24

E. 28

{% include JB/setup %}