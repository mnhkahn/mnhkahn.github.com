---
layout: post
title: "Java面试宝典"
figure: "http://cyeam.qiniudn.com/java_logo.jpg"
description: "从2013年9月开始找工作，在几个月的Java程序员求职过程中，总结了一些被问到的笔试题和面试题。Java语言博大精深，是整个程序界的上乘语言，应该得到重视。"
category: "Java 源码剖析"
tags: []
---

###1. Java标识符，命名规范？
+ 不能以数字开头；rake post title="hello world" category="life" date="2013-04-21" tags="" description="description"
+ 区分大小写；
+ 不能有@、‘-‘（运算符）；
+ 可以出现中文；
+ java关键字不能做为变量名；

###2. Java基本类型及其范围
<table cellpadding="0" cellspacing="0" class="c21"><tbody><tr class="c15"><td class="c29"><p class="c2 c6"><span>基本类型</span></p></td><td class="c10"><p class="c2 c6"><span>大小</span></p></td><td class="c13"><p class="c2 c6"><span>最小值</span></p></td><td class="c23"><p class="c2 c6"><span>最大值</span></p></td><td class="c13"><p class="c2 c6"><span>包装器</span></p></td><td class="c30"><p class="c2 c6"><span>默认值</span></p></td><td class="c9"><p class="c2 c6"><span>说明</span></p></td></tr><tr><td class="c29"><p class="c2 c6"><span>boolean</span></p></td><td class="c10"><p class="c2 c6"><span>-</span></p></td><td class="c13"><p class="c2 c6"><span>-</span></p></td><td class="c23"><p class="c2 c6"><span>-</span></p></td><td class="c13"><p class="c2 c6"><span>Boolean</span></p></td><td class="c30"><p class="c2 c6"><span>false</span></p></td><td class="c9"><p class="c2"><span>没有大小</span></p></td></tr><tr><td class="c29"><p class="c2 c6"><span>char</span></p></td><td class="c10"><p class="c2 c6"><span>16bits</span></p></td><td class="c13"><p class="c2 c6"><span>Unicode 0</span></p></td><td class="c23"><p class="c2 c6"><span>Unicode 2</span><span class="c32">16</span><span>-1</span></p></td><td class="c13"><p class="c2 c6"><span>Character</span></p></td><td class="c30"><p class="c2 c6"><span>\u0000‘ ‘</span></p></td><td class="c9"><p class="c2"><span>可以用来表示中文</span></p></td></tr><tr><td class="c29"><p class="c2 c6"><span>byte</span></p></td><td class="c10"><p class="c2 c6"><span>8bits</span></p></td><td class="c13"><p class="c2 c6"><span>-128</span></p></td><td class="c23"><p class="c2 c6"><span>127</span></p></td><td class="c13"><p class="c2 c6"><span>Byte</span></p></td><td class="c30"><p class="c2 c6"><span>0</span></p></td><td class="c9"><p class="c2"><span>与C++中的char相同</span></p></td></tr><tr><td class="c29"><p class="c2 c6"><span>short</span></p></td><td class="c10"><p class="c2 c6"><span>16bits</span></p></td><td class="c13"><p class="c2 c6"><span>-2</span><span class="c32">15</span></p></td><td class="c23"><p class="c2 c6"><span>2</span><span class="c32">15</span><span>-1</span></p></td><td class="c13"><p class="c2 c6"><span>Short</span></p></td><td class="c30"><p class="c2 c6"><span>0</span></p></td><td class="c9"><p class="c2 c26"><span></span></p></td></tr><tr><td class="c29"><p class="c2 c6"><span>int</span></p></td><td class="c10"><p class="c2 c6"><span>32bits</span></p></td><td class="c13"><p class="c2 c6"><span>-2</span><span class="c32">31</span></p></td><td class="c23"><p class="c2 c6"><span>2</span><span class="c32">31</span><span>-1</span></p></td><td class="c13"><p class="c2 c6"><span>Integer</span></p></td><td class="c30"><p class="c2 c6"><span>0</span></p></td><td class="c9"><p class="c2 c26"><span></span></p></td></tr><tr><td class="c29"><p class="c2 c6"><span>long</span></p></td><td class="c10"><p class="c2 c6"><span>64bits</span></p></td><td class="c13"><p class="c2 c6"><span>-2</span><span class="c32">63</span></p></td><td class="c23"><p class="c2 c6"><span>2</span><span class="c32">63</span><span>-1</span></p></td><td class="c13"><p class="c2 c6"><span>Long</span></p></td><td class="c30"><p class="c2 c6"><span>0</span></p></td><td class="c9"><p class="c2 c26"><span></span></p></td></tr><tr><td class="c29"><p class="c2 c6"><span>float</span></p></td><td class="c10"><p class="c2 c6"><span>32bits</span></p></td><td class="c13"><p class="c2 c6"><span>IEEE754</span></p></td><td class="c23"><p class="c2 c6"><span>IEEE754</span></p></td><td class="c13"><p class="c2 c6"><span>Float</span></p></td><td class="c30"><p class="c2 c6"><span>0.0</span></p></td><td class="c9"><p class="c2"><span>指数8位</span></p></td></tr><tr><td class="c29"><p class="c2 c6"><span>double</span></p></td><td class="c10"><p class="c2 c6"><span>64bits</span></p></td><td class="c13"><p class="c2 c6"><span>IEEE754</span></p></td><td class="c23"><p class="c2 c6"><span>IEEE754</span></p></td><td class="c13"><p class="c2 c6"><span>Double</span></p></td><td class="c30"><p class="c2 c6"><span>0.0</span></p></td><td class="c9"><p class="c2"><span>指数16位</span></p></td></tr><tr><td class="c29"><p class="c2 c6"><span>void</span></p></td><td class="c10"><p class="c2 c6"><span>-</span></p></td><td class="c13"><p class="c2 c6"><span>-</span></p></td><td class="c23"><p class="c2 c6"><span>-</span></p></td><td class="c13"><p class="c2 c6"><span>Void</span></p></td><td class="c30"><p class="c2 c6"><span>null</span></p></td><td class="c9"><p class="c2"><span>Void可以定义变量</span></p></td></tr></tbody></table>

###3. Java中变量的初始化
+ 局部变量必须初始化，如果没有初始化而使用，会编译错误。数组会自动初始化；
+ 类中的变量可以在调用构造函数的时候自动初始化，且有默认值；
+ Java对于变量初始化赋值很严格，float f = 0.0(0.0为double类型)，这在C++中是会有警告，而在Java中是编译不过的。

###4. Java操作有优先级？
<table cellpadding="0" cellspacing="0" class="c21"><tbody><tr><td class="c18"><p class="c2 c6"><span>优先级</span></p></td><td class="c24"><p class="c2 c6"><span>运算符</span></p></td><td class="c3"><p class="c2 c6"><span>结合性</span></p></td></tr><tr><td class="c18"><p class="c2 c6"><span>1</span></p></td><td class="c24"><p class="c2 c6"><span>() [] .</span></p></td><td class="c3"><p class="c2 c6"><span>从左到右</span></p></td></tr><tr><td class="c18"><p class="c2 c6"><span>2</span></p></td><td class="c24"><p class="c2 c6"><span>! +(正) &nbsp;-(负) ~ ++ --</span></p></td><td class="c3"><p class="c2 c6"><span>从右向左</span></p></td></tr><tr><td class="c18"><p class="c2 c6"><span>3</span></p></td><td class="c24"><p class="c2 c6"><span>* / %</span></p></td><td class="c3"><p class="c2 c6"><span>从左向右</span></p></td></tr><tr><td class="c18"><p class="c2 c6"><span>4</span></p></td><td class="c24"><p class="c2 c6"><span>+(加) -(减)</span></p></td><td class="c3"><p class="c2 c6"><span>从左向右</span></p></td></tr><tr><td class="c18"><p class="c2 c6"><span>5</span></p></td><td class="c24"><p class="c2 c6"><span>&lt;&lt; &gt;&gt; &gt;&gt;&gt;</span></p></td><td class="c3"><p class="c2 c6"><span>从左向右</span></p></td></tr><tr><td class="c18"><p class="c2 c6"><span>6</span></p></td><td class="c24"><p class="c2 c6"><span>&lt; &lt;= &gt; &gt;= instanceof</span></p></td><td class="c3"><p class="c2 c6"><span>从左向右</span></p></td></tr><tr><td class="c18"><p class="c2 c6"><span>7</span></p></td><td class="c24"><p class="c2 c6"><span>== &nbsp; !=</span></p></td><td class="c3"><p class="c2 c6"><span>从左向右</span></p></td></tr><tr><td class="c18"><p class="c2 c6"><span>8</span></p></td><td class="c24"><p class="c2 c6"><span>&amp;(按位与)</span></p></td><td class="c3"><p class="c2 c6"><span>从左向右</span></p></td></tr><tr><td class="c18"><p class="c2 c6"><span>9</span></p></td><td class="c24"><p class="c2 c6"><span>^</span></p></td><td class="c3"><p class="c2 c6"><span>从左向右</span></p></td></tr><tr><td class="c18"><p class="c2 c6"><span>10</span></p></td><td class="c24"><p class="c2 c6"><span>|</span></p></td><td class="c3"><p class="c2 c6"><span>从左向右</span></p></td></tr><tr><td class="c18"><p class="c2 c6"><span>11</span></p></td><td class="c24"><p class="c2 c6"><span>&amp;&amp;</span></p></td><td class="c3"><p class="c2 c6"><span>从左向右</span></p></td></tr><tr><td class="c18"><p class="c2 c6"><span>12</span></p></td><td class="c24"><p class="c2 c6"><span>||</span></p></td><td class="c3"><p class="c2 c6"><span>从左向右</span></p></td></tr><tr><td class="c18"><p class="c2 c6"><span>13</span></p></td><td class="c24"><p class="c2 c6"><span>?:</span></p></td><td class="c3"><p class="c2 c6"><span>从右向左</span></p></td></tr><tr><td class="c18"><p class="c2 c6"><span>14</span></p></td><td class="c24"><p class="c2 c6"><span>= += -= *= /= %= &amp;= |= ^= &nbsp;~= &nbsp;&lt;&lt;= &gt;&gt;= &nbsp; &gt;&gt;&gt;=</span></p></td><td class="c3"><p class="c2 c6"><span>从右向左</span></p></td></tr></tbody></table>

###5. 自加++、自减--操作符
+ 前缀操作，可以理解为先加再赋值，后缀操作是先赋值再加；
+ 如果为后缀自加，加的操作在该语句执行结束后执行；
+ 当有多种可以解析的情况下，如下，可以解析成test1+(++test2)或者test1++ + test2，会从左至右就近的匹配。test3是1而不是2。

        int test1 = 0;
        int test2 = 1;
        int test3 = test1+++test2;

###6. 负数如何进行取模运算？
对于负数，先对其绝对值取模，再加上符号。

###7. 是什么操作符？
+ Java中新增了一种操作符，无符号右移>>>，无论正负数，高位都是补0；
+ 有符号右移>>，正数时高位补0，负数时高位补1(1是符号位)；
+ 移位运算符可以高效的实现与2的倍数的乘除法。

###8. &与&&的区别？
+ &是按位与运算，也可以进行boolean运算；
+ 与&&的区别是，&&可以进行短路求值。

###9. 8 | 9 & 10 ^ 11的运算结果？
|、&、^操作符的优先顺序是&、^、|，首先`9(1001)&10(1010)=8(1000)`，然后`8(1000)^11(1011)=3`，最后`(0011)8(1000)|3(0011)=11(1011)`。

###10. 下面代码的输出是什么？

    int n = 7;
    n <<= 3;
    n = n & n + 1 | n + 2 ^ n + 3;
    n >>= 2;
    System.out.println(n);
n向左移3位，相当于乘以8，得到56。+的优先级高于按位操作符的优先级，先进行加法，变成`56&57|58^59`，剩下的操作与9题类似，得到14。

###11. 下面代码的执行结果是什么？

    x = 5;
    y = 3;
    int z = x + (x++) + (++x) + y;
根据优先级，要先执行x++，x后加，先赋值5，最后再加，现在还不加；然后执行++x，先加，再赋值，此时x为6。注意，此时第一个x也是6，这是比较容易出错的地方。最后再加y，6+5+6+3=20。

###12. equals()和==的区别？
+ `==`是二元运算符，在判断基本数据类型的时候，是判断其值，值相等则为true；在判断引用对象的时候，是判断其内存地址，是同一个变量则为true；
+ equals()是Object的一个函数，默认通过hashCode()来判断时候相等，而hashCode()是通过计算引用对象的内存地址得到的。可以重写这两个函数来判断两个引用对象的内容是否相等；
+ `==`用于判断原生类型(primitive)相等，equals()用于判断对象的相等。

###13. 描述一下Java中的参数传递？
+ 对于基本类型，Java采用按值传递，参数的值是不能够修改的；
+ 而如果传递的是对象的引用，则会按引用传递。这个也不矛盾，如果是对象的引用，可以理解成是传递的是对象的地址，这个地址是按值传递的，我们不能修改，而这个地址的对象，我们是可以修改的，这和C++中的是一样的。

###14. 如何获得数组的长度？

    int arr[] = new int[4];
    arr.length;

###15. private和protected是否可以是class的访问修饰符？
+ 不能。class只支持public和friendly(不写，默认的)访问修饰符，其余的都不支持；
+ 一个.java文件中最多只能有一个public类，作为该文件对外的接口，且该类要与文件名相同(一个文件中可以有多个类)；
+ 如果想定义成private那样的类，可以将其构造函数定义成private的访问权限，也可达到目的。

###16. final、finally、finalize的区别？
+ final用来定义常量，使其初始化之后不能修改。定义函数，使其在继承类中不能被覆盖，也能实现内嵌调用，从而提高效率。定义类，该类则不能被继承，例如String；
+ finally是try/catch块之后执行且总是被执行，会在return之前被调用；
+ finalize()是Object中的一个方法，释放内存时会被调用，可以覆盖该函数来实现内存的释放。

###17. Java访问修饰符？
<table cellpadding="0" cellspacing="0" class="c21"><tbody><tr class="c15"><td class="c12"><p class="c8 c6"><span></span></p></td><td class="c12"><p class="c17 c6"><span>当前类</span></p></td><td class="c12"><p class="c17 c6"><span>当前包</span></p></td><td class="c12"><p class="c17 c6"><span>继承类</span></p></td><td class="c12"><p class="c17 c6"><span>其他包</span></p></td></tr><tr class="c15"><td class="c12"><p class="c17 c6"><span>public</span></p></td><td class="c12"><p class="c17 c6"><span class="c22 c1">√</span></p></td><td class="c12"><p class="c17 c6"><span class="c22 c1">√</span></p></td><td class="c12"><p class="c17 c6"><span class="c22 c1">√</span></p></td><td class="c12"><p class="c6 c17"><span class="c22 c1">√</span></p></td></tr><tr class="c15"><td class="c12"><p class="c17 c6"><span>protected</span></p></td><td class="c12"><p class="c17 c6"><span class="c22 c1">√</span></p></td><td class="c12"><p class="c17 c6"><span class="c22 c1">√</span></p></td><td class="c12"><p class="c17 c6"><span class="c22 c1">√</span></p></td><td class="c12"><p class="c17 c6"><span class="c22 c1">×</span></p></td></tr><tr class="c15"><td class="c12"><p class="c17 c6"><span>包访问权限(friendly)</span></p></td><td class="c12"><p class="c17 c6"><span class="c22 c1">√</span></p></td><td class="c12"><p class="c17 c6"><span class="c22 c1">√</span></p></td><td class="c12"><p class="c17 c6"><span class="c22 c1">×</span></p></td><td class="c12"><p class="c17 c6"><span class="c22 c1">×</span></p></td></tr><tr class="c15"><td class="c12"><p class="c17 c6"><span>private</span></p></td><td class="c12"><p class="c17 c6"><span class="c1 c22">√</span></p></td><td class="c12"><p class="c17 c6"><span class="c22 c1">×</span></p></td><td class="c12"><p class="c17 c6"><span class="c22 c1">×</span></p></td><td class="c12"><p class="c17 c6"><span class="c22 c1">×</span></p></td></tr></tbody></table>

###18. 下面代码的执行结果是什么？

    class AA extends BB {
        private int radius = 1;
        public void draw() {
            System.out.println("A.draw(),radius=" + radius);
        }
        public AA(int radius) {
            this.radius = radius;
            System.out.println("A constructor");
        }
    }
    class BB {
        private int radius = 10;
        public void draw() {
            System.out.println("B.draw(),radius=" + radius);
        }
        public BB() {
            System.out.println("B constructor");
            draw();
        }
        public BB(int radius) {
            System.out.println("B constructor with parameter");
            draw();
        }
    }
    B constructor
    A.draw(),radius=1
    A constructor
调用构造函数的一般顺序：

+ 父类的静态变量初始化；
+ 子类的静态变量初始化；
+ 父类的非静态变量初始化；
+ 父类的静态代码块初始化(只在声明的时候初始化)；
+ 父类的非静态代码块初始化；
+ 父类的无参数构造函数初始化；
+ 子类的非静态变量初始化；
+ 子类的静态代码块初始化；
+ 子类的非静态代码块初始化；
+ 子类被调用的构造函数初始化。

此题中，先调用父类的无参数构造函数，输出B constructor，再调用draw函数，draw是自己的draw函数(draw函数被覆盖)。

###19. 下面语句有什么问题？

    if (x) {
        x = 0;
    }
Java中的if条件表达式只支持boolean类型，这不同于C++中还可以支持整型。

###20. 可以用于switch条件表达式的类型是什么？
+ switch支持整型表达式，默认支持int；
+ byte、char、short可以自动向下转换，不会造成数据丢失，所以也可以使用；
+ long、float、double转换成int时会丢失数据，不能使用。
+ Java 7之后，switch开始支持字符串String。

###21. 下列代码的执行结果是什么？

    int i = 10, j = 18, k = 30;
    switch(j - i) {
    case 8: System.out.println(++k);
    case 9: System.out.println(k+=3);
    case 10: System.out.println(k<<=1);
    default: System.out.println(k/=j);
    }
如果匹配到case，从该case开始执行，直到遇到break为止。该题目中，四个语句都执行过，++k得到31，k+=3得到34，k乘以2得到68，再除以18得到3(小数部分抹掉)。

###22. Throwable的子类是哪两个？
+ Error
+ Exception

###23. 下面代码的输出结果是什么？

    try {
        String a = null;
        a.length();
    } catch(nullPointerException e) {
        System.out.println("NullPointerException");
    } catch(Exception e) {
        System.out.println("Exception");
    } finally {
        System.out.println("finally");
    }
会输出NullPointerException和finally，并列的多个catch，要先写子类，再写父类，匹配到一个catch后，不再匹配，执行finally语句。

###24. throw和throws的区别？
+ throws定义函数，声明这个方法会抛出这种类型的异常，使其他地方调用它时知道要捕获这个异常。使用try/catch来捕获；
+ throw是具体向外抛异常的动作，所以它一定会抛出一个异常实例。

###25. Java支持多继承么？
Java默认只支持单继承extends，C++中的多继承对于继承的概念不是很严谨，因为继承多个对象无法确定该对象到底是属于哪个类型。而Java又提供了接口，可以被实现implements，一个类可以实现多个接口。这也是实现多继承的一种方式，而且也符合继承的概念，一个类只能有一个父类，这样不会造成混乱，实现多个接口，又能增加其他类中才有的功能。

###26. 什么是重载？
+ 对于同一个动作，可以有不同的执行方法，这时就需要重载；
+ 重载函数名必须相同；
+ 参数表必须不同，只能通过参数表来区别重载函数；
+ 返回值不能用来区别重载函数。如果只有返回值不同，由于返回值可以转换类型，所以不能用来区别重载函数。

###27. 什么是重写？
+ 在继承关系中，子类可以重写继承到的父类的函数，来定义自己的功能实现；
+ 重写的函数，函数名，返回值，参数表必须完全相同；
+ 子类重写的函数的访问修饰符不能比父类的小；
+ 子类重写的函数抛出的异常不能比父类的多。

###28. 下面代码的执行结果是什么？

    public class Parent{
        public int x;
        public int y;
        public Parent(int x, int y) {
            this.x = x;
            this.y = y;
        }
        public void increaseX(int x) {
            this.x = getX() + x;
        }
        public int getX() {
            return x;
        }
        public void increaseY(int y) {
            this.y = getY() + y;
        }
        public int getY() {
            return y;
        }
    }
    public class Child extends Parent {
        private int x;
        private int y;
        public Child(int x, int y) {
            super(x, y);
            this.y = y + 250;
            this.x = x + 150;
        }
        public int getX() {
            return x;
        }
        public int getY() {
            return y;
        }
    }
    Child child = new Child(50, 50);
    child.increaseX(100);
    child.increaseY(100);
x和y结果分别是200和300。在重写当中，具体还可以分为覆盖和隐藏。对于函数，子类中重写的函数会覆盖掉父类的函数，而对于变量，子类中重写的变量将会隐藏掉父类的变量。在new Child(50, 50)的时候，调用父类的带参数构造函数，在这里对x和y赋值，x和y是父类的x和y，不会影响到子类的x和y。接着this.y = y + 250，这里修改的是子类的x和y，得到200和300。接着执行increaseX和increaseY，子类并没有定义这两个函数，调用的是父类的这两个函数，而调用的时候修改的是父类中x和y的值，不会影响到子类的结果。

###29. 下列代码插入标记处不会编译出错的是哪一个？

    class MyTest extends Test {
        int count;
        public MyTest(int cnt, int num) {
            super(num);
            count = cnt;
        }
        // insert code here
    }
    public class Test {
        int number;
        public Test(int i) {
            number = i;
        }
    }
+ MyTest() {}
+ MyTest(int cnt) {count = cnt}
+ MyTest(int cnt) {super(); count = cnt;}
+ MyTest(int cnt) {count = cnt; super(cnt);}
+ MyTest(int cnt) {this(cnt, cnt);}
+ MyTest(int cnt) {super(cnt); this(cnt, 0)}

首先，Java中子类的构造函数会默认有一句super()，来调用父类的构造函数，该语句可以省略。该语句需要放在构造函数第一行；
Java中this()也可以用在构造函数的第一行，用来调用本类的其他构造函数。this()和super()不能同时使用；
如果为super增加参数，那可以调用父类对应带参数的构造函数；
如果父类不定义构造函数，会自动为其分配一个不带参数的构造函数。如果父类定义了构造函数，那么将不再会自动分配。也就是说，定义了一个带参数的构造函数，那么该类就没有不带参数的构造函数了；
上题中，A、B、C、都显示或隐式地调用了super()函数，而父类没有定义不带参数的构造函数。D中super不在第一行。F同时使用了super和this。答案为E。

###30. Java是否可以手动释放内存？
Java提供了一个方法，System.gc()，建议Java虚拟机去释放内存，当JVM决定去释放内存是，会调用该对象的finalize()方法。Java中申请内存由程序员实现，内存会申请到堆中，释放内存由GC实现。

###31. Java是否会出现内存泄漏？
![GC](http://cyeam.qiniudn.com/javacollection_gc.gif)

GC会自动回收垃圾，GC采用有向图的方法，一般情况下，如果一个对象没有被引用，则该对象所占的内存将会被释放。例如，o2=o1后，o2原本引用的内存将会被释放；

    Vector v = new Vector(10);
    for (int i=1;i<100; i++)
    {
        Object o=new Object();
        v.add(o);
        o=null;        
    }
但是当一个对象没有被引用，但是在有向图中又是可达的，而且又没有用处，那么此时就发生了内存泄漏。o=null后，由于之前指向的内存可以从v可达，那么该部分内存将不可被释放，知道v=null或v的内存释放为止。

###32. Thread的五个状态？
+ 创建状态
+ 就绪状态
+ 运行状态
+ 阻塞状态
+ 死亡状态

###33. Thread中run()和start()的区别？
+ start()会立刻返回。调用start()方法，会创建一个线程，处于就绪状态，调用run()方法运行线程体，运行结束后，该线程结束；
+ run()就是一个方法，不会创建新线程。

###34. Thread中run()和start()的区别？
+ start()会立刻返回。调用start()方法，会创建一个线程，处于就绪状态，调用run()方法运行线程体，运行结束后，该线程结束；
+ run()就是一个方法，不会创建新线程。

###35. synchronized和java.util.concurrent.Locks.Lock的区别？
synchronized可以作用域函数，代码块，静态函数中。在函数中使用，以当前实例为锁，表示当前实例this在不同的线程中要互斥访问。在代码块中使用，要为synchronized增加参数，要以对象为锁，互斥访问，如果以this同步，和之前的以函数同步含义相同。也可以指定对象来同步。如果同步的是静态函数，函数调用的时候可能还没有实例，不能使用this，可以使用Foo.class作为锁。

    Public synchronized void method(){
        //......
    }
    public void method()
    {
        synchronized (this)
        {
            //......
        }
    }
    public void method(SomeObject so) {
        synchronized(so)
        {
            //......
        }
    }
+ 所有对象都自动含有单一的锁。 JVM负责跟踪对象被加锁的次数。如果一个对象被解锁，其计数变为0。在任务（线程）第一次给对象加锁的时候，计数变为1。每当这个相同的任务（线程）在此对象上获得锁时，计数会递增。 只有首先获得锁的任务（线程）才能继续获取该对象上的多个锁。
+ Lock有比Synchronized更精确的线程域城予以和更好的性能。Synchronized会自动释放锁，但是Lock一定要求程序员手工释放，并且必须在finally从句中释放。

###36. wait()、notify()、notifyAll()的作用？
+ 这三个方法最终调用的都是jvm级的native方法。随着jvm运行平台的不同可能有些许差异。
+ 如果对象调用了wait方法就会使持有该对象的线程把该对象的控制权交出去，然后处于等待状态。
+ 如果对象调用了notify方法就会通知某个正在等待这个对象的控制权的线程可以继续运行。
+ 如果对象调用了notifyAll方法就会通知所有等待这个对象控制权的线程继续运行。

Java面试中也会常常去问对于Java包源码的理解。下面按照根据Java包来介绍。
java.lang包，Java的基础包，编译时会自动导入，主要包含Java基类Object，包装类Boolean、Character、Byte、Short、Integer、Long、Float、Double，Enum，String、StringBuffer、StringBuilder，Thread，Process，Math，Throwable，Error，Exception。

###37. java.lang.Object
<table cellpadding="0" cellspacing="0" class="c21"><tbody><tr><td class="c19"><p class="c2"><span class="c1">方法</span></p></td><td class="c25"><p class="c2"><span class="c1">说明</span></p></td></tr><tr><td class="c19"><p class="c2"><span class="c1">public final native Class&lt;?&gt; getClass();</span></p></td><td class="c25"><p class="c2"><span class="c1">返回一个对象的运行时类</span></p></td></tr><tr><td class="c19"><p class="c2"><span class="c1">public native int hashCode();</span></p></td><td class="c25"><p class="c2"><span class="c1">返回该对象的哈希码值，将对象在内存中的地址转成int并返回</span></p></td></tr><tr><td class="c19"><p class="c2"><span class="c1">public boolean equals(Object obj) {</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; return (this == obj);</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; }</span></p></td><td class="c25"><p class="c2"><span class="c1 c28">指示某个其他对象是否与此对象“相等”。默认使用==来判断引用对象的地址。</span></p></td></tr><tr><td class="c19"><p class="c2"><span class="c1">protected native Object clone() throws CloneNotSupportedException;</span></p></td><td class="c25"><p class="c2"><span class="c1">创建并返回此对象的一个副本。该对象要实现Cloneable接口，否则会抛出CloneNotSupportedException异常</span></p></td></tr><tr><td class="c19"><p class="c2"><span class="c1">public String toString() {</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; return getClass().getName() + "@" + Integer.toHexString(hashCode());</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; }</span></p></td><td class="c25"><p class="c2"><span class="c28 c1">返回该对象的字符串表示，用hashCode()辅助实现</span></p></td></tr><tr><td class="c19"><p class="c2"><span class="c1">public final native void notify();</span></p></td><td class="c25"><p class="c2"><span class="c28 c1">唤醒在此对象监视器上等待的单个线程</span></p></td></tr><tr><td class="c19"><p class="c2"><span class="c1">public final native void notifyAll();</span></p></td><td class="c25"><p class="c2"><span class="c28 c1">唤醒在此对象监视器上等待的所有线程</span></p></td></tr><tr><td class="c19"><p class="c2"><span class="c1">public final native void wait(long timeout) throws InterruptedException;</span></p></td><td class="c25"><p class="c2"><span class="c28 c1">导致当前的线程等待，直到其他线程调用此对象的 notify() 方法或 notifyAll() 方法，或者超过指定的时间量</span></p></td></tr><tr><td class="c19"><p class="c2"><span class="c1">public final void wait(long timeout, int nanos) throws InterruptedException</span></p></td><td class="c25"><p class="c2"><span class="c28 c1">导致当前的线程等待，直到其他线程调用此对象的 notify() 方法或 notifyAll() 方法，或者其他某个线程中断当前线程，或者已超过某个实际时间量</span></p></td></tr><tr><td class="c19"><p class="c2"><span class="c1">public final void wait() throws InterruptedException {</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; wait(0);</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; }</span></p></td><td class="c25"><p class="c2"><span class="c28 c1">导致当前的线程等待，直到其他线程调用此对象的 notify() 方法或 notifyAll() 方法</span></p></td></tr><tr><td class="c19"><p class="c2"><span class="c1">protected void finalize() throws Throwable { }</span></p></td><td class="c25"><p class="c2"><span class="c1">当垃圾回收器确定不存在对该对象的更多引用时，由对象的垃圾回收器调用此方法</span></p></td></tr></tbody></table>

###38. java.lang.Math
Math是一个final类，不能被继承，提供了一套静态方法，实现数字计算的常见功能。
<table cellpadding="0" cellspacing="0" class="c21"><tbody><tr><td class="c0"><p class="c2"><span class="c1">方法</span></p></td><td class="c0"><p class="c2"><span class="c1">说明</span></p></td></tr><tr><td class="c0"><p class="c2"><span class="c1">public static double ceil(double a) {</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; return StrictMath.ceil(a); // default impl. delegates to StrictMath</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; }</span></p></td><td class="c0"><p class="c2"><span class="c1">向上取整</span></p></td></tr><tr><td class="c0"><p class="c2"><span class="c1">public static double floor(double a) {</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; return StrictMath.floor(a); // default impl. delegates to StrictMath</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; }</span></p></td><td class="c0"><p class="c2"><span class="c1">向下取整</span></p></td></tr><tr><td class="c0"><p class="c2"><span class="c1">public static int round(float a) {</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; if (a != 0x1.fffffep-2f) // greatest float value less than 0.5</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; return (int)floor(a + 0.5f);</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; else</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; return 0;</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; }</span></p></td><td class="c0"><p class="c2"><span class="c1">加0.5后向下取整。</span></p><p class="c2"><span class="c1">ceil和floor返回的都是double，round返回的是int和long</span></p></td></tr></tbody></table>

###39. java.lang.String
String是一个final类，不可以被继承。Java里是没有运算符重载的，String+是StringBuffer的append()方法来实现的，如：String str = new String("abc");编译时等效于String str = new StringBuffer().append("a").append("b").append("c").toString();

<table cellpadding="0" cellspacing="0" class="c21"><tbody><tr class="c15"><td class="c0"><p class="c2 c5"><span class="c1">类方法或变量</span></p></td><td class="c0"><p class="c2 c5"><span class="c1">说明</span></p></td></tr><tr><td class="c0"><p class="c2"><span class="c1">private final char value[];</span></p></td><td class="c0"><p class="c2"><span class="c1">String是封装的字符数组，而且被定义成final类型，一经赋值，不能修改</span></p></td></tr><tr><td class="c0"><p class="c2"><span class="c1">private int hash;</span></p></td><td class="c0"><p class="c2"><span class="c1">默认为0，hashCode()的返回值</span></p></td></tr><tr><td class="c0"><p class="c2"><span class="c1">public String() {</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; this.value = new char[0];</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; }</span></p></td><td class="c0"><p class="c2 c26"><span class="c1"></span></p></td></tr><tr><td class="c0"><p class="c2"><span class="c1">public String(String original) {</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; this.value = original.value;</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; this.hash = original.hash;</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; }</span></p></td><td class="c0"><p class="c2 c26"><span class="c1"></span></p></td></tr><tr><td class="c0"><p class="c2"><span class="c1">public String(char value[]) {</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; this.value = Arrays.copyOf(value, value.length);</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; }</span></p></td><td class="c0"><p class="c2 c26"><span class="c1"></span></p></td></tr><tr><td class="c0"><p class="c2"><span class="c1">public String(char value[], int offset, int count);</span></p></td><td class="c0"><p class="c2"><span class="c1">根据字符数组一部分对象创建字符串对象</span></p></td></tr><tr><td class="c0"><p class="c2"><span class="c1">public String(int[] codePoints, int offset, int count);</span></p></td><td class="c0"><p class="c2 c26"><span class="c1"></span></p></td></tr><tr><td class="c0"><p class="c2"><span class="c1">public int length() {</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; return value.length;</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; }</span></p></td><td class="c0"><p class="c2"><span class="c1">返回字符数组长度</span></p></td></tr><tr><td class="c0"><p class="c2"><span class="c1">public char charAt(int index) {</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; if ((index &lt; 0) || (index &gt;= value.length)) {</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; throw new StringIndexOutOfBoundsException(index);</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; }</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; return value[index];</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; }</span></p></td><td class="c0"><p class="c2 c26"><span class="c1"></span></p></td></tr><tr><td class="c0"><p class="c2"><span class="c1">public boolean equals(Object anObject);</span></p></td><td class="c0"><p class="c2"><span class="c1">根据字符数组逐个比较</span></p></td></tr><tr><td class="c0"><p class="c2"><span class="c1">public int compareTo(String anotherString);</span></p></td><td class="c0"><p class="c2"><span class="c1">相同返回0，当前字符串大，返回整数；小，返回负数</span></p></td></tr><tr><td class="c0"><p class="c2"><span class="c1">public int indexOf(int ch) {</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; return indexOf(ch, 0);</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; }</span></p></td><td class="c0"><p class="c2"><span class="c1">返回字符ch首先出现的位置，没有返回-1</span></p></td></tr><tr class="c15"><td class="c0"><p class="c2 c5"><span class="c1">public String substring(int beginIndex, int endIndex);</span></p></td><td class="c0"><p class="c2 c5"><span class="c1">通过索引和value，创建一个新的String并返回。不包括endIndex所指的字符。</span></p><p class="c2 c26 c5"><span class="c1"></span></p><p class="c2 c5"><span class="c1">Java 6之前，String类内部还有两个成员变量count和offset，当调用substring并返回时，同样还是引用的同一个字符数组，只是改变了count和offset。当你有一个非常长的字符串，而你只是想保留其中的一小部分，Java 6会一直保存着整个字符串，这样会造成性能问题。解决的方法是x = x.substring(i, j) + “”;</span></p><p class="c2 c5"><span class="c1">Java 7会帮你new一个新的字符串并只保留substring要用到的字符。</span></p></td></tr><tr class="c15"><td class="c0"><p class="c2 c5"><span class="c1">public String concat(String str);</span></p></td><td class="c0"><p class="c2 c5"><span class="c1">创建一个新的字符数组，将当前字符数组和str的都放到该数组中，用这个数组创建一个新的String并返回</span></p></td></tr><tr class="c15"><td class="c0"><p class="c2 c5"><span class="c1">public String replace(char oldChar, char newChar);</span></p></td><td class="c0"><p class="c2 c5"><span class="c1">用newChar替换所有当前字符串中oldChar并创建一个新String返回</span></p></td></tr></tbody></table>

###40. java.lang.StringBuilder
StringBuilder是可变长字符串，是Java 5.0新增的，之前的是StringBuffer，相比于StringBuffer，StringBuilder是线程不安全的，但性能得到提升。这两个类的接口是保持一致的。Java 5.0之后，字符串+操作符采用StringBuilder实现
<table cellpadding="0" cellspacing="0" class="c21"><tbody><tr><td class="c0"><p class="c2"><span class="c1">类变量或方法</span></p></td><td class="c0"><p class="c2"><span class="c1">说明</span></p></td></tr><tr class="c15"><td class="c0"><p class="c2 c5"><span class="c1">char[] value;</span></p></td><td class="c0"><p class="c2 c5"><span class="c1">AbstractStringBuilder类中，可以返回capacity</span></p></td></tr><tr class="c15"><td class="c0"><p class="c2 c5"><span class="c1">int count;</span></p></td><td class="c0"><p class="c2 c5"><span class="c1">AbstractStringBuilder类中</span></p></td></tr><tr><td class="c0"><p class="c2"><span class="c1">public StringBuilder(String str) {</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; super(str.length() + 16);</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; append(str);</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; }</span></p></td><td class="c0"><p class="c2"><span class="c1">默认空的StringBuilder的capacity为16，以String初始化的capacity为String的长度加16</span></p></td></tr><tr><td class="c0"><p class="c2"><span class="c1">&nbsp;public StringBuilder append(String str) {</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; super.append(str);</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; return this;</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; }</span></p></td><td class="c0"><p class="c2 c26"><span class="c1"></span></p></td></tr><tr><td class="c0"><p class="c2"><span class="c1">public StringBuilder delete(int start, int end) {</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; super.delete(start, end);</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; return this;</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; }</span></p></td><td class="c0"><p class="c2 c26"><span class="c1"></span></p></td></tr><tr><td class="c0"><p class="c2"><span class="c1">public StringBuilder insert(int index, char[] str, int offset,</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; int len)</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; {</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; super.insert(index, str, offset, len);</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; return this;</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; }</span></p></td><td class="c0"><p class="c2 c26"><span class="c1"></span></p></td></tr><tr><td class="c0"><p class="c2"><span class="c1">public int length() {</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; return count;</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; }</span></p></td><td class="c0"><p class="c2 c26"><span class="c1"></span></p></td></tr><tr><td class="c0"><p class="c2"><span class="c1">public int capacity() {</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; return value.length;</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; }</span></p></td><td class="c0"><p class="c2"><span class="c1">capacity与length不同，length()个返回保存的字符串长度，capacity()返回申请的字符数组大小</span></p></td></tr><tr class="c15"><td class="c0"><p class="c2 c5"><span class="c1">public void setLength(int newLength)</span></p></td><td class="c0"><p class="c2 c26 c5"><span class="c16 c1"></span></p></td></tr></tbody></table>

###41. 包装类java.lang.Integer
`public final class Integer extends Number implements Comparable<Integer>`
<table cellpadding="0" cellspacing="0" class="c21"><tbody><tr class="c15"><td class="c0"><p class="c2 c5"><span class="c1">类变量或方法</span></p></td><td class="c0"><p class="c2 c5"><span class="c1">说明</span></p></td></tr><tr><td class="c0"><p class="c2"><span class="c1">public static final int &nbsp; MIN_VALUE = 0x80000000;</span></p></td><td class="c0"><p class="c2 c26"><span class="c1"></span></p></td></tr><tr><td class="c0"><p class="c2"><span class="c1">public static final int &nbsp; MAX_VALUE = 0x7fffffff;</span></p></td><td class="c0"><p class="c2 c26"><span class="c1"></span></p></td></tr><tr><td class="c0"><p class="c2"><span class="c1">public static int parseInt(String s, int radix)</span></p><p class="c2"><span class="c1">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; throws NumberFormatException</span></p></td><td class="c0"><p class="c2 c26"><span class="c1"></span></p></td></tr><tr><td class="c0"><p class="c2"><span class="c1">public static int reverse(int i)</span></p></td><td class="c0"><p class="c2 c26"><span class="c1"></span></p></td></tr></tbody></table>

java.util包包含Date，容器类Collection，日历Calendar，随机数Random。其中，容器类是常见的面试内容。
集合类主要分类两大类，Collection和Map。Collection允许有重复对象。继承Collection的有List、Set、Vector、Stack接口。List要求有序，可以有重复元素。Set表示集合，无序，但不能有重复元素。
![Collection](http://cyeam.qiniudn.com/javacollection_collection.png)

###42. java.util.Collection
Collection接口中常见操作
<table cellpadding="0" cellspacing="0" class="c21"><tbody><tr class="c15"><td class="c0"><p class="c17"><span class="c1">接口变量或方法</span></p></td><td class="c0"><p class="c17"><span class="c1">说明</span></p></td></tr><tr class="c15"><td class="c0"><p class="c17"><span class="c1">int size();</span></p></td><td class="c0"><p class="c8"><span class="c1"></span></p></td></tr><tr class="c15"><td class="c0"><p class="c2 c5"><span class="c1">boolean isEmpty()</span></p></td><td class="c0"><p class="c2 c5"><span class="c1">判断集合时候有任何元素</span></p></td></tr><tr class="c15"><td class="c0"><p class="c17"><span class="c1">boolean contains(Object o);</span></p></td><td class="c0"><p class="c8"><span class="c1"></span></p></td></tr><tr class="c15"><td class="c0"><p class="c2 c5"><span class="c1">Iterator iterator()</span></p></td><td class="c0"><p class="c2 c5"><span class="c1">返回迭代器，用来访问各个元素</span></p></td></tr><tr class="c15"><td class="c0"><p class="c17"><span class="c1">boolean add(E e);</span></p></td><td class="c0"><p class="c17"><span class="c1">在最后增加元素e</span></p></td></tr><tr class="c15"><td class="c0"><p class="c17"><span class="c1">boolean remove(Object o);</span></p></td><td class="c0"><p class="c17"><span class="c1">从当前List中删除第一次出现的元素o</span></p></td></tr><tr class="c15"><td class="c0"><p class="c2 c5"><span class="c1">boolean containsAll(Collection c)</span></p></td><td class="c0"><p class="c2 c26 c5"><span class="c16 c1"></span></p></td></tr><tr class="c15"><td class="c0"><p class="c2 c5"><span class="c1">boolean addAll(Collection c)</span></p></td><td class="c0"><p class="c2 c26 c5"><span class="c16 c1"></span></p></td></tr><tr class="c15"><td class="c0"><p class="c17"><span class="c1">void clear();</span></p></td><td class="c0"><p class="c17"><span class="c1">删除所有元素</span></p></td></tr><tr class="c15"><td class="c0"><p class="c2 c5"><span class="c1">void removeAll(Collection c)</span></p></td><td class="c0"><p class="c2 c26 c5"><span class="c16 c1"></span></p></td></tr><tr class="c15"><td class="c0"><p class="c2 c5"><span class="c1">void retainAll(Collection c)</span></p></td><td class="c0"><p class="c2 c5"><span class="c1">从集合中删除集合c中不包含的元素</span></p></td></tr><tr class="c15"><td class="c0"><p class="c17"><span class="c1">boolean equals(Object o);</span></p></td><td class="c0"><p class="c8"><span class="c1"></span></p></td></tr><tr class="c15"><td class="c0"><p class="c17"><span class="c1">int hashCode();</span></p></td><td class="c0"><p class="c8"><span class="c1"></span></p></td></tr><tr class="c15"><td class="c0"><p class="c17"><span class="c1">Object[] toArray()</span></p></td><td class="c0"><p class="c17"><span class="c1">返回含集合所有元素的数组</span></p></td></tr><tr class="c15"><td class="c0"><p class="c17"><span class="c1">Object[] toArray(Object[] a)</span></p></td><td class="c0"><p class="c17"><span class="c1">返回含集合所有元素的数组，返回的数组与参数a的类型相同</span></p></td></tr></tbody></table>

###43. java.util.List
<table cellpadding="0" cellspacing="0" class="c21"><tbody><tr><td class="c0"><p class="c2"><span class="c1">接口变量或方法</span></p></td><td class="c0"><p class="c2"><span class="c1">说明</span></p></td></tr><tr><td class="c0"><p class="c2"><span class="c1">E get(int index);</span></p></td><td class="c0"><p class="c2"><span class="c1">获得指定位置的元素</span></p></td></tr><tr class="c15"><td class="c0"><p class="c2 c5"><span class="c1">E set(int index, E element);</span></p></td><td class="c0"><p class="c2 c5"><span class="c1">将指定位置的元素替换为element</span></p></td></tr><tr class="c15"><td class="c0"><p class="c2 c5"><span class="c1">List&lt;E&gt; subList(int fromIndex, int toIndex);</span></p></td><td class="c0"><p class="c2 c5"><span class="c1">不包括toIndex指定的元素</span></p></td></tr></tbody></table>

List有两个实现类，ArrayList和LinkedList，都是线程不安全的。LinkedList使用双向链表实现，保存头结点first和尾结点last。ArrayList使用动态数组实现，默认容量为10，每当容量不够的时候，就要重新申请新的内存，并将之前的内容复制进来。
int newCapacity = oldCapacity + (oldCapacity >> 1);
申请的内存是之前的1.5倍。ArrayList可以随机访问，但是增加和删除消耗大，每次这样的操作都要移动其余的元素。而LinkedList按索引访问时要按照指针一次遍历，访问消耗大。
然而，如果每次插入和删除都是在队列尾部，ArrayList效率要高，因为不需要移动元素。
Vector同样实现的是List接口，是一个重量级列表，线程安全的。也是采用动态数组实现，每次动态分配的内存和ArrayList不同，默认是2倍。
`int newCapacity = oldCapacity + ((capacityIncrement > 0) ?
                                         capacityIncrement : oldCapacity);`

###43. java.util.Set
Set不存在重复的元素，依靠equals()来检测独一性。与Collection有着完全一样的接口，根据值来确定。
+ HashSet。实现了SortedSet接口。其对快速查找进行了优化。存入的元素必须定义hashCode()。
+ TreeSet。底层为树结构。可以从Set中提取有序的序列。元素必须实现Comparable接口。
+ LinkedHashSet。具有HashSet的查询速度，内部使用链表维护元素的顺序(插入的顺序)，使用迭代器遍历Set时，会按照插入的顺序显示。存入的元素必须实现hashCode()方法。

###44. java.util.Iterator
List可以通过get来遍历整个链表，但是对于其他的数据接口，这些遍历方法将不能通用。所以使用Iterator接口来封装遍历操作，使遍历所有的集合，都能有一个共同的接口。
<table cellpadding="0" cellspacing="0" class="c21"><tbody><tr class="c15"><td class="c0"><p class="c17"><span class="c1">接口变量或方法</span></p></td><td class="c0"><p class="c17"><span class="c1">说明</span></p></td></tr><tr class="c15"><td class="c0"><p class="c17"><span class="c1">boolean hasNext();</span></p></td><td class="c0"><p class="c8"><span class="c1"></span></p></td></tr><tr class="c15"><td class="c0"><p class="c17"><span class="c1">E next();</span></p></td><td class="c0"><p class="c17"><span class="c1">将指定位置的元素替换为element</span></p></td></tr><tr class="c15"><td class="c0"><p class="c17"><span class="c1">void remove();</span></p></td><td class="c0"><p class="c17"><span class="c1">删除上一次iterator返回的元素</span></p></td></tr></tbody></table>

###45. java.util.Map
Map中不允许有重复的key。
<table cellpadding="0" cellspacing="0" class="c21"><tbody><tr class="c15"><td class="c0"><p class="c17"><span class="c1">接口变量或方法</span></p></td><td class="c0"><p class="c17"><span class="c1">说明</span></p></td></tr><tr class="c15"><td class="c0"><p class="c17"><span class="c1">Object put(Object key, Object value);</span></p></td><td class="c0"><p class="c8"><span class="c1"></span></p></td></tr><tr class="c15"><td class="c0"><p class="c17"><span class="c1">Object remove(Object key);</span></p></td><td class="c0"><p class="c17"><span class="c1">根据key删除元素</span></p></td></tr><tr class="c15"><td class="c0"><p class="c17"><span class="c1">void putAll(Map m);</span></p></td><td class="c0"><p class="c17"><span class="c1">将m中所有元素存入当前map</span></p></td></tr><tr class="c15"><td class="c0"><p class="c17"><span class="c1">void clear();</span></p></td><td class="c0"><p class="c8"><span class="c1"></span></p></td></tr><tr class="c15"><td class="c0"><p class="c17"><span class="c1">Object get(Object key);</span></p></td><td class="c0"><p class="c17"><span class="c1">根据key获得元素</span></p></td></tr><tr class="c15"><td class="c0"><p class="c17"><span class="c1">int size();</span></p></td><td class="c0"><p class="c8"><span class="c1"></span></p></td></tr><tr class="c15"><td class="c0"><p class="c17"><span class="c1">boolean isEmpty();</span></p></td><td class="c0"><p class="c8"><span class="c1"></span></p></td></tr><tr class="c15"><td class="c0"><p class="c17"><span class="c1">boolean containsKey(Object key);</span></p></td><td class="c0"><p class="c17"><span class="c1">检测是否有指定key的对象</span></p></td></tr><tr class="c15"><td class="c0"><p class="c17"><span class="c1">boolean containsValue(Object value);</span></p></td><td class="c0"><p class="c17"><span class="c1">检测是否有指定value的对象</span></p></td></tr><tr class="c15"><td class="c0"><p class="c17"><span class="c1">boolean equals(Object o);</span></p></td><td class="c0"><p class="c8"><span class="c1"></span></p></td></tr><tr class="c15"><td class="c0"><p class="c2 c5"><span class="c1">Set&lt;K&gt; keySet();</span></p></td><td class="c0"><p class="c2 c5"><span class="c1">返回一个Set，里面保存map中所有的key</span></p></td></tr><tr class="c15"><td class="c0"><p class="c2 c5"><span class="c1">Collection&lt;V&gt; values();</span></p></td><td class="c0"><p class="c2 c5"><span class="c1">返回一个Collection，保存map中的所有value</span></p></td></tr><tr class="c15"><td class="c0"><p class="c2 c5"><span class="c1">Set&lt;Map.Entry&lt;K, V&gt;&gt; entrySet();</span></p></td><td class="c0"><p class="c2 c5"><span class="c1">返回一个Set，保存所有mappings</span></p></td></tr><tr class="c15"><td class="c0"><p class="c17"><span class="c1">interface Entry&lt;K,V&gt;</span></p></td><td class="c0"><p class="c17"><span class="c1">存储单个键/值对</span></p></td></tr></tbody></table>

HashMap。Java 2.0引入，是非同步的，但是提高了性能。基于散列表实现，解决哈希冲突使用链接法。
HashMap哈希的方法，是将key的hashCode与key的总数求余，得到哈希的索引。如果key是常量，则有可能相同，即使不同，与key的总数求余也有可能有哈希冲突。HashMap使用链接法解决冲突。

    int hash = key.hashCode();
    int index = hash % Entity[].length;
    Entity[index] = value;
![Hash](http://cyeam.qiniudn.com/javacollection_hash.png)

    public V put(K key, V value) {
        if (table == EMPTY_TABLE) {
            inflateTable(threshold);
        }
        if (key == null)
            return putForNullKey(value);
        int hash = hash(key);
        int i = indexFor(hash, table.length);
        for (Entry<K,V> e = table[i]; e != null; e = e.next) {
            Object k;
            if (e.hash == hash && ((k = e.key) == key || key.equals(k))) {
                V oldValue = e.value;
                e.value = value;
                e.recordAccess(this);
                return oldValue;
            }
        }
        modCount++;
        addEntry(hash, key, value, i);
        return null;
    }
+ Hashtable是Dictionary的子类，是同步的。
+ TreeMap。采用红黑树实现，可以获得字数subTree()。

###47. java.io
Java IO采用Decorator模式，可以动态装配不同功能的Stream。IO体系分Input/Output和Reader/Writer两类，区别在于Reader/Writer读写文本时自动转换内码。
System.out是PrintStream的一个子类，PrintStream继承了FilterOutputStream类，FilterOutputStream类继承了OutputStream类。
![InputStream](http://cyeam.qiniudn.com/javacollection_inputstream.png)

![Reader](http://cyeam.qiniudn.com/javacollection_reader.png)

###48. Servlet生命周期
![Servlet](http://cyeam.qiniudn.com/javacollection_servlet.png)

+ 装载Servlet。
+ 创建Servlet实例。
+ 调用Servlet的init()方法。Servlet只初始化一次。
+ 当一个客户端请求到达后，创建一个request对象和一个response对象。
+ 调用service()方法，处理数据，并将结果返回客户端。
+ 当服务器不再需要Servlet时，调用destroy()方法。

###49. Servlet的转发和重定向
javax.servlet.RequestDispatcher的forward方法
javax.servlet.http.HttpServletResponse的sendRedirect(String)方法

{% include JB/setup %}

