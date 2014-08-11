---
layout: post
title: "微软2012年实习生笔试题"
figure: "http://cyeam.qiniudn.com/microsoft_bldg.jpg"
description: ""
category: "Collection"
tags: ["Job", "Exam"]
---

1.Suppose that a selection sort of 80 items has completed 32 iterations of the main loop. How many items are now guaranteed to be in their final spot (never to be moved again)? （**C**）

A、16 B、31 C、32 D、39 E、40

***80个元素进行选择排序，进行了32次循环，问有哪些元素已经在最终位置上了。考察选择排序基本原理。每一趟遍历都会从剩余待排元素中选择一个最大(小)的元素放在最终位置上，所以进行32次循环就是有32个元素在最终位置上了，选C。***

2.Which synchronization mechanism(s) is/are used to avoid race conditions among processes/threads in operating system?

A、Mutex B、Mailbox C、Semaphore D、Local procedure call  

3.There is a sequence of n numbers 1,2,3,...,n and a stack which can keep m numbers at most. Push the n numbers into the stack following the sequence and pop out randomly . Suppose n is 2 and m is 3,the output sequence may be 1,2 or 2,1,so we get 2 different sequences . Suppose n is 7,and m is 5,please choose the output sequence of the stack. 

A、1,2,3,4,5,6,7  
B、7,6,5,4,3,2,1  
C、5,6,4,3,7,2,1  
D、1,7,6,5,4,3,2  
E、3,2,1,7,5,6,4  

4.Which is the result of binary number 01011001 after multiplying by 0111001 and adding 1101110? 

A、0001010000111111  
B、0101011101110011  
C、0011010000110101   

5.What is output if you compile and execute the following c code?

    int main() 
    { 
        int i = 11; 
        int const * p = &i; 
        p++; 
        printf("%d", *p); 
        return 0; 
    }

A、11 B、12 C、Garbage value D、Compile error E、None of above

6.Which of following C++ code is correct ?
A.

    int f() 
    { 
        int *a = new int(3); 
        return *a; 
    }
B.

    int *f() 
    { 
        int a[3] = {1,2,3}; 
        return a; 
    }
C.

    vector<int> f() 
    { 
        vector<int> v(3); 
        return v; 
    }
D.

    void f(int *ret) 
    { 
        int a[3] = {1,2,3}; 
        ret = a; 
        return ; 
    }
E. None of above

7.Given that the 180-degree rotated image of a 5-digit number is another 5-digit number and the difference between the numbers is 78633, what is the original 5-digit number？

A、60918 B、91086 C、18609 D、10968 E、86901   

8.Which of the following statements are true?

A、We can create a binary tree from given inorder and preorder traversal sequences.
B、We can create a binary tree from given preorder and postorder traversal sequences.
C、For an almost sorted array,Insertion sort can be more effective than Quciksort.
D、Suppose `T(n)` is the runtime of resolving a problem with n elements, `T(n)=O(1)` if `n=1` `T(n)=2*T(n/2)+O(n)` if `n>1`; so T(n) is O(nlgn)
E、None of above

9.Which of the following statements are true?

A、Insertion sort and bubble sort are not efficient for large data sets.
B、Qucik sort makes O(n^2) comparisons in the worst case.
C、There is an array :7,6,5,4,3,2,1. If using selection sort (ascending),the number of swap operations is 6
D、Heap sort uses two heap operations:insertion and root deletion （插入、堆调整）
E、None of above   

10.Assume both x and y are integers, which one of the following returns the minimun of the two integers?

A、 `y^((x^y) & -(x<y))`
B、 `y^(x^y)`
C、 `x^(x^y)`
D、 `(x^y)^(y^x)`
E、 None of the above   

11.The Orchid Pavilion(兰亭集序) is well known as the top of “行书”in history of Chinese literature. The most fascinating sentence is "Well I know it is a lie to say that life and death is the same thing, and that longevity and early death make no difference Alas!"(固知一死生为虚诞，齐彭殇为妄作).By counting the characters of the whole content (in Chinese version),the result should be 391(including punctuation). For these characters written to a text file,please select the possible file size without any data corrupt.（**ABCD**）

A、782 bytes in UTF-16 encoding
B、784 bytes in UTF-16 encoding
C、1173 bytes in UTF-8 encoding
D、1176 bytes in UTF-8 encoding
E、None of above   

***关于编码，最早是ACSII，里面之后256个字符。这只能满足英文编码。我国发展出了GBK、Big5等中文编码，但是问题是，每个国家都定义了自己国家语言的编码，用不同的方式可以解出不同的文字。后来为了统一，出现了Unicode。Unicode的实现有几种方式。常见的就是UTF8、UTF16。UTF8以8位为单位，可以有1字节、2字节、3字节、4字节四种长度。而中文在UTF8编码当中是占3个字节。UTF16是以16位作为单位长度，有2字节和4字节两种。中文在UTF16当中占两个字节。Unicode也可以指是UTF16编码。***

***Unicode有多种实现方式，所以需要在开头定义出所用的编码形式：***

|| UTF编码　|| Byte Order Mark ||　
|| UTF-8 ||　EF BB BF ||　
|| UTF-16LE || FF FE ||　
|| UTF-16BE ||　FE FF ||
|| UTF-32LE ||　FF FE 00 00 ||
|| UTF-32BE ||　00 00 FE FF ||

***UTF8的Bom头占3个字节，UTF16的Bom头占2个字节。而Bom头并未规定是必须加的，也可以不加。***

***下面看这道题，391个字，UTF8将会占1173个字节，加上Bom头占1176个字节。UTF16是782个字节，加上Bom头是784个字节。***

12.Fill the blanks inside class definition

    class Test 
    { 
    public: 
        ____ int a; 
        ____ int b; 
        public: 
        Test::Test(int _a , int _b) : a( _a ) 
        { 
            b = _b; 
        } 
    }; 
    int Test::b; 

    int main(void) 
    { 
        Test t1(0 , 0) , t2(1 , 1); 
        t1.b = 10; 
        t2.b = 20; 
        printf("%u %u %u %u",t1.a , t1.b , t2.a , t2.b); 
        return 0; 
    }

Running result : 0 20 1 20  
A、static/const B、const/static C、--/static D、conststatic/static E、None of above

13.A 3-order B-tree has 2047 key words,what is the maximum height of the tree?

A、11 B、12 C、13 D、14   

14.In C++,which of the following keyword(s) can be used on both a variable and a function?(***ACE***)

A、static B、virtual C、extern D、inline E、const

***
+ static关键字，可以用来声明静态变量或者静态函数。static声明后在全局中唯一存在；
+ virtual关键字，C++语法，用来声明虚函数。虚函数声明之后，可以在派生类中实现。这与Java中的接口定义类似，可以帮助实现多态；
+ extern关键字。对于一个全局变量，它既可以在本源文件中被访问到，也可以在同一个工程的其它源文件中被访问，只需用extern进行声明即可。在C语言中，修饰符extern用在变量或者函数的声明前，用来说明此变量/函数是在别处定义的，要在此处引用。在C++中extern还有另外一种作用，用于指示C或者C＋＋函数的调用规范。比如在C++中调用C库函数，就需要在C++程序中用extern “C”声明要引用的函数。这是给链接器用的，告诉链接器在链接的时候用C函数规范来链接。主要原因是C＋＋和C程序编译完成后在目标代码中命名规则不同，用此来解决名字匹配的问题；
+ inline关键字，用来指示内联函数。每一次调用函数，都会使用到内存中的栈，用来保存此函数的地址、参数表、返回值等信息。如果此函数频繁被使用并且函数逻辑简单，就可以使用inline关键字。在C语言中，#define的作用类似于inline关键字。
+ const关键字，可以用来声明常量，常函数void Func(int a) const。
***

15.What is the result of the following program?

    char* f(char* str, char ch) 
    { 
        char* it1 = str; 
        char* it2 = str; 
        while(*it2 != '\0') 
        { 
            while(*it2 == ch) 
            { 
                it2++; 
            } 
            *it1++ = *it2++; 
        } 
        return str; 
    } 
     
    int main(int argc, char* argv[]) 
    { 
        char* a = new char[10]; 
        strcpy(a, "abcdcccd"); 
        cout<<f(a, 'c'); 
        return 0;
    }

A、abdcccd B、abdd C、abcc D、abddcccd E、Access violation

16.Consider the following definition of a recursive function,power,that will perform exponentiation.

    int power(int b , int e) 
    { 
        if(e == 0) 
            return 1; 
        if(e % 2 == 0) 
            return power(b*b , e/2); 
        else 
            return b * power(b*b , e/2); 
    }

Asymptotically（渐进地） in terms of the exponent e,the number of calls to power that occur as a result of the call power(b,e) is

A、logarithmic
B、linear
C、quadratic
D、exponential

17.Assume a full deck of cards has 52 cards,2 blacks suits (spade and club) and 2 red suits(diamond and heart). If you are given a full deck,and a half deck(with 1 red suit and 1 black suit),what is the possibility for each one getting 2 red cards if taking 2 cards?

A、1/2 1/2
B、25/102 12/50
C、50/51 24/25
D、25/51 12/25
E、25/51 1/2   

18.There is a stack and a sequence of n numbers(i.e. 1,2,3,...,n), Push the n numbers into the stack following the sequence and pop out randomly . How many different sequences of the n numbers we may get? Suppose n is 2 , the output sequence may 1,2 or 2,1, so wo get 2 different sequences .

A、C_2n^n
B、C_2n^n - C_2n^(n+1)
C、((2n)!)/(n+1)n!n!
D、n!
E、None of above   

19.Longest Increasing Subsequence(LIS) means a sequence containing some elements in another sequence by the same order, and the values of elements keeps increasing.
For example, LIS of {2,1,4,2,3,7,4,6} is {1,2,3,4,6}, and its LIS length is 5.
Considering an array with N elements , what is the lowest time and space complexity to get the length of LIS？

A、Time : N^2 , Space : N^2
B、Time : N^2 , Space : N
C、Time : NlogN , Space : N
D、Time : N , Space : N
E、Time : N , Space : C   

20.What is the output of the following piece of C++ code ？

    #include<iostream> 
    using namespace std; 

    struct Item 
    { 
        char c; 
        Item *next; 
    }; 

    Item *Routine1(Item *x) 
    { 
        Item *prev = NULL, 
        *curr = x; 
        while(curr) 
        { 
            Item *next = curr->next; 
            curr->next = prev; 
            prev = curr; 
            curr = next; 
        } 
        return prev; 
    } 

    void Routine2(Item *x) 
    { 
        Item *curr = x; 
        while(curr) 
        { 
            cout<<curr->c<<" "; 
            curr = curr->next; 
        } 
    } 

    int main(void) 
    { 
        Item *x, 
        d = {'d' , NULL}, 
        c = {'c' , &d}, 
        b = {'b' , &c}, 
        a = {'a' , &b}; 
        x = Routine1( &a ); 
        Routine2( x ); 
        return 0; 
    }

A、 c b a d B、 b a d c C、 d b c a D、 a b c d E、 d c b a

{% include JB/setup %}