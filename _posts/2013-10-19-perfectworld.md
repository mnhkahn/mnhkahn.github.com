---
layout: post
title: "完美世界2014校园招聘笔试"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeam/perfectworld_logo.jpg"
description: "只是简单了参加了一下笔试，地点是在清华。没有面试机会。这种游戏公司招人要求都有点高。"
category: "Collection"
tags: ["Job", "Exam"]
---
###一、单项选择题

#####1. 某工作站无法访问www.wanmei.com的服务器，使用ping命令对该服务器的IP地址进行测试，响应正常；但是对服务器域名进行测试时出现超时错误，可能出现的问题是（B）
* A. 线路故障
* B. 路由故障
* C. 域名解析故障
* D. 服务器网卡故障

***如果能ping通，那么说明DNS解析是正常的。就好比去访问facebook，肯定ping不通，因为DNS被污染了。同理，线路故障和网卡故障也会导致ping不通。一般服务器前面还会再增加一层负载均衡服务器，一般是Nginx或者Apache，会在这里做域名正则匹配，如果转发到错误的IP上面，有可能导致超时错误。***

#####2. 小明每次可以上1级、2级或者3级台阶、请问小明上6级台阶总共共有多少种方法（B）
* A. 23
* B. 24
* C. 25
* D. 26

#####3. 师徒四人西天取经，途中必需跨过一座桥、四个人从桥的同一端出发，你得帮助他们到达另一端，天色很暗，而他们只有一只手电筒。一次同时最多可以有两人一起过桥，而过桥的时候必须持有手电筒，所以就得有人把手电筒带来带去、来回桥两端。手电筒不能同丢的方式来传递。四个人的步行速度各不同，若两人同行则以较慢者的速度为准。大师兄需花1分钟过桥，二师兄需花2分钟过桥，三师兄需5分钟过桥， 师父需花10分钟过桥，请问他们最短在多少分钟内能过桥？（B）
* A. 16
* B. 17
* C. 18
* D. 19

#####4. 以下说法不正确的是：（A）
* A. 死锁的充分条件是互斥、占有且等待、非剥夺、循环等待，且缺一不可。
* B. Raid5至少需要3块磁盘。
* C. 地址空间和资源（例如打开文件句柄）在进程间相互独立，而同一进程的线程可以共享。
* D. 局部性原理主要包括时间局部性和空间局部性。

#####5. 权值为9，5，2，7的四个叶子构成的哈夫曼树，其带权路径长度是：（B）
* A. 23
* B. 44
* C. 46
* D. 50

#####6. 程序执行后，count的值将会是：（B）

    public class CrazyCount {
        private static volatile int count = 0;
        public static void main(String[] args) {
            for (int i = 0; i < 1000; i++) {
                new Thread(new Runnable() {
                    public void run() {
                        count++;
                    }
                }).start();
            }
        }
    }

* A. 无效值，因为对count的代码修改没有同步
* B. 1到1000中的一个值
* C. 正好1000
* D. 至少1000

// 在JVM中，每个线程都可以有自己的栈空间，volatile的作用是保证栈空间中的值和内存中的一致，并不会保证变量的原子性。保证原子性需要使用synchronized关键字，为cout++保证线程安全。

// 另：虽然1000个线程并行执行，但是保证了count++的线程安全之后，最终结果肯定是1000


#####7. 各处如下代码：

    public class Test {
        public static void main(String[] args) {
            int x = 5;
            boolean b1 = true;
            boolean b2 = false;
            if ((x == 4) && !b2)
                System.out.print("1");
            System.out.print("2");
            if ((b2 = true) && b1)
                System.out.print("3");
        }
    }

输出结果是：（D）
* A. 2
* B. 3
* C. 12
* D. 23
* E. 123
* F. 编译出错
* G. 运行时程序抛出异常

#####8. 编译运行下面的代码会出现哪种情况？（C）

    public class Test {
        public void myMethod(Object o) {
            System.out.println("My Object");
        }
        public void myMethod(String s) {
            System.out.println("My String");
        }
        public static void main(String args[]) {
            Test t = new Test();
            t.myMethod(null);
        }
    }

* A. 不能编译通过
* B. 编译通过，输出”My Object”
* C. 编译通过，输出”My String”
* D. 编译通过，但运行时报错

#####9. 以下代码运行时输出的结果是什么？（B）
    class C {
        C() {
            System.out.print("C");
        }
    }
    class A {
        C c = new C();
        A() {
            this("A");
            System.out.print("A");
        }
        A(String s) {
            System.out.print(s);
        }
    }
    class B extends A {
        B() {
            super("B");
            System.out.print("B");
        }
        public static void main(String[] args) {
            new B();
        }
    }

* A. BB
* B. CBB
* C. BAB
* D. 以上都不是

#####10. 栈是一种：（A）
* A. 存取受限的线性结构
* B. 存取不受限的线性结构
* C. 存取受限的非线性结构
* D. 存取不受限的非线性结构

#####11. java中一个char对象可以表示的数值范围是：（B）
* A. 0到255
* B. 0到65535
* C. -256到255
* D. -32768到32767
* E. 平台相关

// Java中char为16位，4个字节，使用Unicode编码

#####12. 以下描述正确的是：（B）
* A. Java支持多重继承，一个类可以实现多个接口；
* B. Java只支持单重继承，一个类可以实现多个接口；
* C. Java只支持单重继承，一个类只可以实现一个接口；
* D. Java支持多重继承，但一个类只可以实现一个接口。
 
#####13. 下列关于集合类描述错误的包括：（C）
* A. ArrayList和LinkedList均实现了List接口
* B. ArrayList的访问速度比LinkedList快
* C. 添加和删除元素时，ArrayList的表现更佳
* D. HashMap实现Map接口，它允许任何类型的键和值对象，并允许将null用作键或值

#####14. 执行如下程序代码后，c的值是：（A）

    a = 0; c = 1;
    do {
        --c;
        a = a - 1;
    } while (a > 0);

* A. 0
* B. 1
* C. -1
* D. 死循环

#####15. 下列关于修饰符混用的说法，错误的包括：（D）
* A. abstract不能与final并列修饰同一个类
* B. abstract类中可以有private的成员
* C. abstract方法必须在abstract类中
* D. static方法中能处理非static的成员变量


###二、填空题

#####1. 下面二叉树的中序遍历结果是：

#####2. 请至少列举出5个常用的设计模式：

#####3. 一个1300字节的IP包，包长度为20字节，进入一个MTU为500的网络中，请问该IP包被拆成（）段， 其中每段的长度分别是（）。

#####4. 完美世界的个性账号注册时要求账号由6-16位小写英文字母及数字组成且首位为字母，请写出验证账号合法的正则表达式（）。

#####5. 请给出以下程序的输出：
    class Value {
        public int i = 15;
    }
    public class Test {
        public static void main(String argv[]) {
            Test t = new Test();
            t.first();
        }
        public void first() {
            int i = 5;
            Value v = new Value();
            v.i = 25;
            second(v, i);
            System.out.println(v.i);
        }
        public void second(Value v, int i) {
            i = 0;
            v.i = 20;
            Value val = new Value();
            v = val;
            System.out.println(v.i + " " + i);
        }
    }


###三、简答题

#####1. 列举HTTP 1.1所支持的方法。
OPTIONS、HEAD、GET、POST、PUT、DELETE、TRACE、CONNECT

#####2. 什么是反射？反射的作用是什么？
反射就是可以在程序运行时刻动态获得类的信息，动态调用类的方法。
反射的作用是，可以动态的获得对象的内部接口，可以动态对一个对象进行操作。

#####3. 方法equals()和方法hashCode()有什么联系？它们各自有什么作用？实现这两个方法的时候有些什么要求？
equals()和hashCode()均继承自Object对象。equals()是通过比较两个对象的内存地址来判断时候相等，可以重写这个函数来进行内容判断。hashCode()用来实现Set等，可以简单的认为是使用物理内存地址来实现，这是一个native方法，会因为平台不同而不同。equals()需要自反性、对称性、传递性、一致性、对任何不适null的x，x.equals(null)一定返回false。



###四、编程题

#####1. 用java实现一个方法，从指定的mymap中删除所有值为value的对象，并返回删除的对象个数
    int removeValue(Map<Integer, Integer> mymap, int value);

    int removeValue(Map<Integer, Integer> mymap, int value) {
        int count = 0;
        List<Integer> list = new LinkedList<Integer>();
        Iterator<Entry<Integer, Integer>> iter = mymap.entrySet().iterator();
        Entry<Integer, Integer> entry;
        while (iter.hasNext()) {
            entry = iter.next();
            if (entry.getValue() == value) {
                list.add(entry.getKey());
            }
        }
        
        // 
        count = list.size();
        for (int i = 0; i < list.size(); i++) {
            mymap.remove(list.get(i));
        }
        
        return count;
    }



---
清华的一家飞机，也不知道是何来历。
![IMG-THUMBNAIL](https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeam/tsinghua_plane.jpg)
{% include JB/setup %}
