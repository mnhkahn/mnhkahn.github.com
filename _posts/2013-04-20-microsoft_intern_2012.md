---
layout: post
title: "微软2012年实习生笔试题"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeam/microsoft_bldg.jpg"
description: ""
category: "Collection"
tags: ["Job", "Exam"]
---

1.Suppose that a selection sort of 80 items has completed 32 iterations of the main loop. How many items are now guaranteed to be in their final spot (never to be moved again)? （**C**）

A、16 B、31 C、32 D、39 E、40

***80个元素进行选择排序，进行了32次循环，问有哪些元素已经在最终位置上了。考察选择排序基本原理。每一趟遍历都会从剩余待排元素中选择一个最大(小)的元素放在最终位置上，所以进行32次循环就是有32个元素在最终位置上了，选C。***

2.Which synchronization mechanism(s) is/are used to avoid race conditions among processes/threads in operating system?(***AC***)

A、Mutex B、Mailbox C、Semaphore D、Local procedure call

+ ***Mutex,(Mutual exclusion, 互斥锁)，可以通过互斥的方式来保护临界资源。有硬件和软件两种实现方式；***
+ ***Semaphore，信号量，用户多线程同步。值为2的信号量就是互斥锁；***
+ ***Local procedure call，本地过程调用。***

3.There is a sequence of n numbers 1,2,3,...,n and a stack which can keep m numbers at most. Push the n numbers into the stack following the sequence and pop out randomly . Suppose n is 2 and m is 3,the output sequence may be 1,2 or 2,1,so we get 2 different sequences . Suppose n is 7,and m is 5,please choose the output sequence of the stack. (***AC***)

A、1,2,3,4,5,6,7  
B、7,6,5,4,3,2,1  
C、5,6,4,3,7,2,1  
D、1,7,6,5,4,3,2  
E、3,2,1,7,5,6,4

***有一个大小为5的栈，有1～7的5个数，随机的进出栈，判断出栈结果。常见的数据结构栈的题目。***

+ ***如果每push进去一个数字，立刻pop出来，结果就是A，此时需要栈空间最小为1；***
+ ***B中第一个pop出来的是7，说明是将这7个数字都push进栈之后才pop，需要栈空间最小为7；***
+ ***C中第一个pop出来的是5，说明栈中之前有5个元素(1,2,3,4,5)，pop之后，还剩4个(1,2,3,4)。然后push进6，pop出4和3，push 7，pop2和1，此过程中，需要最小的栈空间为5；***
+ ***D中push 1之后立刻pop，之后pop出来的是7，说明pop 7之前栈中有6个元素，需要最小的栈空间是6；***
+ ***E中首先pop 3，2，1，此时栈为空，然后将4，5，6，7依次push进栈。此时战中是(4,5,6,7)，pop的话结果只有一种，就是7,6,5,4，此选项的出栈序列是错误的。***

4.Which is the result of binary number 01011001 after multiplying by 0111001 and adding 1101110? (***A***)

A、0001010000111111  
B、0101011101110011  
C、0011010000110101

***如果数字二进制乘法和加法的话可以考虑计算一下，这里是将二进制数字转换成十进制后计算再转成二进制。***

***题目要计算01011001(89)*0111001(57)+1101110(110)，得到5183，转换为二进制为0001010000111111。***

5.What is output if you compile and execute the following c code?(***C***)

    int main() 
    { 
        int i = 11; 
        int const * p = &i; 
        p++; 
        printf("%d", *p); 
        return 0; 
    }

***此处，第4行声明了指向常量的指针，说明指针p所指向的int类型的变量i不可以更改。接着，第五行执行p++，p指向了后四个字节的内存，由于该内存并没有进行初始化操作，所以此时p的值不确定，为Garbage value，选C。***

A、11 B、12 C、Garbage value D、Compile error E、None of above

6.Which of following C++ code is correct ?(***C***)
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

+ ***(A)选项，会动态分配一个指向int类型，值为3的指针，但是这样并不会释放内存，导致内存泄漏；***
+ ***(B)a[3]是局部变量，会分配在栈中，函数返回后就会释放。这样编译的过程中会有警告；***
+ ***(C)STL中的ector是动态分配到堆中的，正确；***
+ ***(D)ret只是赋给了指针a的值，而指针a保存的是指向局部变量的地址，错误同(B)。***

7.Given that the 180-degree rotated image of a 5-digit number is another 5-digit number and the difference between the numbers is 78633, what is the original 5-digit number？(***D***)

A、60918 B、91086 C、18609 D、10968 E、86901

***算是一道智力题。五位数旋转180度得到另一个五位数，两个数的差是78633。问原来的那个五位数是多少。10968旋转后是89601，差正好是78633。***

8.Which of the following statements are true?(***ACD***)

A、We can create a binary tree from given inorder and preorder traversal sequences.
B、We can create a binary tree from given preorder and postorder traversal sequences.
C、For an almost sorted array,Insertion sort can be more effective than Quciksort.
D、Suppose `T(n)` is the runtime of resolving a problem with n elements, `T(n)=O(1)` if `n=1` `T(n)=2*T(n/2)+O(n)` if `n>1`; so T(n) is O(nlgn)
E、None of above

+ ***根据前序和后序序列无法唯一确定一颗二叉树，例如前序为abc，后序为cba，就会有两种结果；必须要有中序遍历；***
+ ***前序和中序，或者后序和中序，可以确定根结点位置，从而得到二叉树；***
+ ***对于基本有序的序列，插入排序比快速排序有效。快速排序适于基本无序的情况；***
	+ 
	+ ***T(1)=1;T(2)=2T(2)+2=4=2*2;T(4)=2T(2)+4=12=4*3=N*(k+1)=2^{k}times (k+1);T(N)=Ntimes (log_2 N+1).***

9.Which of the following statements are true?(***ABD***)

A、Insertion sort and bubble sort are not efficient for large data sets.
B、Qucik sort makes O(n^2) comparisons in the worst case.
C、There is an array :7,6,5,4,3,2,1. If using selection sort (ascending),the number of swap operations is 6
D、Heap sort uses two heap operations:insertion and root deletion （插入、堆调整）
E、None of above

+ ***插入排序和冒泡排序时间复杂度都是o(n^{2})，对于大数据集效率很低；***
+ ***快序排序最差情况，就是序列是倒序的时候，此时快速排序会退化成成冒泡排序，复杂度变为o(n^{2});***
+ ***7,6,5,4,3,2,1，使用选择排序，首先选到最小的1，与队列头7交换，变成1,6,5,4,3,2,7。然后选到2，与队列头6交换，变成1,2,5,4,3,6,7，选择到3，与队列头5交换，得到1,2,3,4,5,6,7，只交换了3次；***
+ ***堆排序两个操作是建堆和堆调整。***

10.Assume both x and y are integers, which one of the following returns the minimun of the two integers?(***A***)

A、 `y^((x^y) & -(x<y))`
B、 `y^(x^y)`
C、 `x^(x^y)`
D、 `(x^y)^(y^x)`
E、 None of the above

***据异或操作的自反性，(B)的结果是x，(C)的结果是y，(D)的结果是0。下面来看(A)，如果x<y，(x<y)结果是1，而-1的补码是11111111，所以原式变为：***

	y^((x^y) & 11111111)

***结果是x；如果x>y，(x<y)结果是0，而0的补码是00000000，所以原式化简为***

	y^((x^y) & 00000000)

***结果是y，(A)正确。***

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

(***C***)

A、static/const B、const/static C、--/static D、conststatic/static E、None of above

***在17、18行，分别修改了对象t1和t2的成员变量b，输出之后，值一样，同为20，说明b为静态变量，可以被所有对象共享，所以b是static静态变量；变量a的值是通过Test类的构造函数的参数表进行初始化的，所以此处可以是空或者是const(const对象可以使用参数表进行初始化)。***

13.A 3-order B-tree has 2047 key words,what is the maximum height of the tree?

A、11 B、12 C、13 D、14   

14.In C++,which of the following keyword(s) can be used on both a variable and a function?(***ACE***)

A、static B、virtual C、extern D、inline E、const

+ ***static关键字，可以用来声明静态变量或者静态函数。static声明后在全局中唯一存在；***
+ ***virtual关键字，C++语法，用来声明虚函数。虚函数声明之后，可以在派生类中实现。这与Java中的接口定义类似，可以帮助实现多态；***
+ ***extern关键字。对于一个全局变量，它既可以在本源文件中被访问到，也可以在同一个工程的其它源文件中被访问，只需用extern进行声明即可。在C语言中，修饰符extern用在变量或者函数的声明前，用来说明此变量/函数是在别处定义的，要在此处引用。在C++中extern还有另外一种作用，用于指示C或者C＋＋函数的调用规范。比如在C++中调用C库函数，就需要在C++程序中用extern “C”声明要引用的函数。这是给链接器用的，告诉链接器在链接的时候用C函数规范来链接。主要原因是C＋＋和C程序编译完成后在目标代码中命名规则不同，用此来解决名字匹配的问题；***
+ ***inline关键字，用来指示内联函数。每一次调用函数，都会使用到内存中的栈，用来保存此函数的地址、参数表、返回值等信息。如果此函数频繁被使用并且函数逻辑简单，就可以使用inline关键字。在C语言中，#define的作用类似于inline关键字。***
+ ***const关键字，可以用来声明常量，常函数void Func(int a) const。***

15.What is the result of the following program?(***D***)

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

***简单考察了C-style string概念的理解。首先将常量字符串”abcdcccd”赋值给变量a，然后调用函数f。while(*it2 != ‘’)用来遍历整个字符串。内存循环***

	while(*it2 == ch)  
	{  
	      it2++;  
	}

***用来将指定字符去除，这里是要将字符’c’去除，所以去除之后是”abdd”。然而，虽然去除了指定字符，但是并没有在该字符串末尾追加’’，所以”abdd”并不是最终结果，当输出的时候，结果是输出到`\n`为止，所以输出完”abdd”后还会继续输出。所以原字符串的cccd也会输出。***

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

17.Assume a full deck of cards has 52 cards,2 blacks suits (spade and club) and 2 red suits(diamond and heart). If you are given a full deck,and a half deck(with 1 red suit and 1 black suit),what is the possibility for each one getting 2 red cards if taking 2 cards?(***B***)

A、1/2 1/2
B、25/102 12/50
C、50/51 24/25
D、25/51 12/25
E、25/51 1/2

***一副扑克牌共52张，其中红色花色(红桃、方片)各13张，黑色花色(梅花、黑桃)各13张。现在有一副全套扑克牌，还有一套半套的扑克牌(有13张黑牌和13张红牌)，从这两副牌中抽取不放回两张牌，两次都是红色花色的概率。***

+ ***第一副全套牌，从54张牌中抽取1张红色的概率是frac{26}{52}，此时还剩51张牌，红色还剩25张，再抽出一张红色的概率是frac{25}{51}，两次都是红色的概率是frac{26}{52}*frac{25}{51}=frac{25}{102}；***
+ ***第二副牌，计算方法相同，从26张牌中抽取一张红色牌概率是frac{13}{26}，从剩余25张牌中抽取12张红色中的一张的概率是frac{12}{25}，两次都是红色的概率是frac{13}{26}*frac{12}{25}=frac{6}{25}。选B。***

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