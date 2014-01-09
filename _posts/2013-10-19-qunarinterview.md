---
layout: post
title: "去哪网Java开发面经"
figure: "/assets/images/qunar_logo.jpg"
description: "去哪网待遇非常给力，一个FE都能给到14x16。而且刚刚上市，发展很不错。我的面试官是重庆人，看到我的简历上写着本科是重庆大学的，也很照顾我，可惜我很不给力。一直摊开了问，从基础到Java源码、C++源码都问了一圈，还有C语言小技巧。面试难度符合他们公司的工资水平。"
category: "Collection"
tags: []
---
去哪网待遇非常给力，一个FE都能给到14x16。而且刚刚上市，发展很不错。我的面试官是重庆人，看到我的简历上写着本科是重庆大学的，也很照顾我，可惜我很不给力。一直摊开了问，从基础到Java源码、C++源码都问了一圈，还有C语言小技巧。面试难度符合他们公司的工资水平。

下面是记忆版的面试题目。

#####1. ArrayList实现 add方法如何分配内存

ArrayList基于数组实现，封装的数组，但是数组大小是固定了，而ArrayList是动态数组。动态数组是通过ensureCapacity(int minCapacity)实现。

    private void grow(int minCapacity) {
        // overflow-conscious code
        int oldCapacity = elementData.length;
        int newCapacity = oldCapacity + (oldCapacity >> 1);
        if (newCapacity - minCapacity < 0)
            newCapacity = minCapacity;
        if (newCapacity - MAX_ARRAY_SIZE > 0)
            newCapacity = hugeCapacity(minCapacity);
        // minCapacity is usually close to size, so this is a win:
        elementData = Arrays.copyOf(elementData, newCapacity);
    }

每次可以扩容1.5倍，将老数组拷贝一份到新数组。


#####2. HashMap如何实现？

HashMap是基于哈希表的Map接口的非同步实现。此类不保证映射的顺序，特别是它不保证该顺序恒久不变。HashMap实际上是一个“链表散列”的数据结构，即数组和链表的结合体。从上图中可以看出，HashMap底层就是一个数组结构，数组中的每一项又是一个链表。当新建一个HashMap的时候，就会初始化一个数组。

    Entry(int h, K k, V v, Entry<K,V> n) {
        value = v;
        next = n;
        key = k;
        hash = h;
    }
![Alt text](/assets/images/post/hashtable_link.png)

#####3. C++容器

#####4. 数据库索引建立

    CREATE INDEX idx_test4_name ON   test_tab (name );
+ 索引要建立在经常进行select操作的字段上。这是因为，如果这些列很少用到，那么有无索引并不能明显改变查询速度。相反，由于增加了索引，反而降低了系统的维护速度和增大了空间需求。
+ 索引要建立在值比较唯一的字段上。这样做才是发挥索引的最大效果。，比如主键的id字段，唯一的名字name字段等等。如果索引建立在唯一值比较少的字段，比如性别gender字段，寥寥无几的类别字段等，刚索引几乎没有任何意义。
+ 对于那些定义为text、image和bit数据类型的列不应该增加索引。因为这些列的数据量要么相当大，要么取值很少。
+ 当修改性能远远大于检索性能时，不应该创建索引。修改性能和检索性能是互相矛盾的。当增加索引时，会提高检索性能，但是会降低修改性能。当减少索引时，会提高修改性能，降低检索性能。因此，当修改性能远远大于检索性能时，不应该创建索引。
+ 在WHERE和JOIN中出现的列需要建立索引。
+ 在以通配符% 和_ 开头作查询时，mysql索引是无效的。但是这样索引是有效的：select * from tbl1 where name like 'xxx%'，所以mysql正确建立索引是很重要的。

#####5. 设计模式

#####6. 如何检测一个数是大端还是小段存储

    short x = 0x1234;
    char* arr;
    arr = reinterpret_cast<char*>(&x);
    cout << hex << static_cast<short>(arr[0]) << static_cast<short>(arr[1]) << endl;
    char y = x;
    cout << "0x" << hex << (short)y << endl;
    union endian {
        int i;
        float f;
        char s;
    };
    endian e;
    e.i = 1;
    cout << static_cast<int>(e.s) << endl;

#####7. Json的解析

#####8. ajax原理

#####9. 快速排序 堆排序 哪个快
这里的关键问题就在于第2步，堆底的元素肯定很小，将它拿到堆顶和原本属于最大元素的两个子节点比较，它比它们大的可能性是微乎其微的。实际上它肯定小于其中的一个儿子。而大于另一个儿子的可能性非常小。于是，这一次比较的结果就是概率不均等的，根据前面的分析，概率不均等的比较是不明智的，因为它并不能保证在糟糕情况下也能将问题的可能性削减到原本的1/2。可以想像一种极端情况，如果a肯定小于b，那么比较a和b就会什么信息也得不到——原本剩下多少可能性还是剩下多少可能性。
在堆排序里面有大量这种近乎无效的比较，因为被拿到堆顶的那个元素几乎肯定是很小的，而靠近堆顶的元素又几乎肯定是很大的，将一个很小的数和一个很大的数比较，结果几乎肯定是“小于”的，这就意味着问题的可能性只被排除掉了很小一部分。
这就是为什么堆排序比较慢（堆排序虽然和快速排序一样复杂度都是O(NlogN)但堆排序复杂度的常系数更大）。
MacKay也提供了一个修改版的堆排序：每次不是将堆底的元素拿到上面去，而是直接比较堆顶（最大）元素的两个儿子，即选出次大的元素。由于这两个儿子之间的大小关系是很不确定的，两者都很大，说不好哪个更大哪个更小，所以这次比较的两个结果就是概率均等的了。

#####10. TCP建立过程，传输过程syn码是否变化

#####11. Protobuf

#####12. 单件模式关键点 除了线程安全

    double check
    import java.lang.reflect.ParameterizedType;
    import java.lang.reflect.Type;
    //import javax.ejb.EntityContext;
    import org.apache.struts2.dispatcher.StaticContentLoader;
    public class ZSingleton<T> {
        
        private static Object instance;
        
        public ZSingleton() {
            Class<T> entityClass = (Class<T>)((ParameterizedType)getClass().getGenericSuperclass()).getActualTypeArguments()[0];
        }
        
        public static <T> T getInstance() {
    //      entityClass.cast(instance);
            
            if (instance == null) {
                // Delay load and synchronized load
                synchronized (ZSingleton.class) {
                    if (instance == null) {
    //                  instance = entityClass.getConstructors();
                    }
                }
            }
            return (T)instance;
        }
    }

#####13. Http状态码
+ 2xx成功
+ 3xx重定向
    + 304 Not Modified。如果客户端发送了一个带条件的GET请求且该请求已被允许，而文档的内容（自上次访问以来或者根据请求的条件）并没有改变，则服务器应当返回这个状态码。304响应禁止包含消息体，因此始终以消息头后的第一个空行结尾。
+ 4xx请求错误
+ 5xx服务器错误

#####14. Vector 与普通数组实现区别

    void reserve( int newCapacity )  
    {  
        Object *oldArray = objects;  
            //1.重设size,capacity  
        int numToCopy = newCapacity < theSize ? newCapacity : theSize;  
        //capacity是在size的基础上加一个常数  
        newCapacity += SPARE_CAPACITY;  
            //2.建立新的数组，并拷贝元素到新数组  
        objects = new Object[ newCapacity ];  
        for( int k = 0; k < numToCopy; k++ )  
            objects[ k ] = oldArray[ k ];  
      
        theSize = numToCopy;  
        theCapacity = newCapacity;  
            //删除原来的数组  
        delete [ ] oldArray;  
    }



---
一面后直接就被委婉的告知没戏了。下午还有完美世界的笔试，走在去清华的路上，拍到的这张北大的博雅塔。
![Alt text](/assets/images/博雅塔.JPG)
{% include JB/setup %}
