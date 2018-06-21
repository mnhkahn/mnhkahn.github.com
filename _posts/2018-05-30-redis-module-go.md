---
layout: post
title: "用 Go 给 Redis 写组件"
description: "Redis 从4.0开始支持组件开发，用户编译生成一个动态链接库，启动时加载就可以启用。"
figure: "http://cyeam.qiniudn.com/redis-modules-features.png"
category: "Redis"
tags: ["Golang","Redis","Module"]
---

* 目录
{:toc}
---

### 写在前面
Redis 从4.0开始支持组件开发，用户编译生成一个动态链接库，启动时加载就可以启用。Redis 时 C语言开发的，写插件还得用 C 语言。还好 Go 语言也能开发组件，我也能尝试一把开发一个插件了。

### 一个 C 语言的例子

可以参考这个例子[Writing Redis Modules](https://redislabs.com/blog/writing-redis-modules/)来大概了解下开发流程。

文章里描述了一下如何自己写一个`HGETSET`命令，他组合了`HGET`和`HSET`这两个原生的命令。

从这里可以下载到源代码[RedisModulesSDK](https://github.com/RedisLabs/RedisModulesSDK)。需要编译出来一个动态链接库文件。例子提供的很完善，编译脚本都写在了 Makefile 里面。会生成`module.so`文件。

    git clone https://github.com/RedisLabs/RedisModulesSDK.git
    cd RedisModulesSDK/
    cd example/
    make all

我们需要用到最新版的 Redis，并且编译。

	wget http://download.redis.io/releases/redis-4.0.9.tar.gz
	tar -zxvf redis-4.0.9.tar.gz
	cd redis-4.0.9
	make

启动 Redis，通过`loadmodule`参数指出动态链接库的地址。`port`参数指定启动端口，`loglevel`设置日志打印级别。

	./redis-server --loadmodule ~/code/ccode/RedisModulesSDK/example/module.so --loglevel debug --port 6340


最后启动 Redis 客户端，试着输入下面的命令，很有成就感有没有。

	redis-cli -p 6340
	
	127.0.0.1:6340> EXAMPLE.HGETSET foo bar baz
	(nil)
	127.0.0.1:6340> EXAMPLE.HGETSET foo bar vaz
	"baz"
	127.0.0.1:6340> EXAMPLE.PARSE SUM 5 2
	(integer) 7
	127.0.0.1:6340> EXAMPLE.PARSE PROD 5 2
	(integer) 10
	127.0.0.1:6340> EXAMPLE.TEST
	PASS


#### Redis 的组件

Redis 的热门组件都放在[这里](https://redis.io/modules)。有人用他做了搜索引擎，还有支持 SQL，还有一些扩展了数据结构，比如 JSON 类型、布隆过滤器、bitmap 等等。

完整的开发[文档](https://redis.io/topics/modules-api-ref)。

大概说下流程：

+ 程序入口是`int RedisModule_OnLoad(RedisModuleCtx *ctx)`，里面完成相关初始化操作；
+ 初始化组件`RedisModule_Init`；
+ 如果扩展了数据类型，也需要注册。`moduleType *RedisModule_CreateDataType(RedisModuleCtx *ctx, const char *name, int encver, void *typemethods_ptr);`。
	+ **name**：这是一个 9 字符的字符串，必须是9个字符。可以使用 A-Z、a-z、0-9、-、_这些字符。一般命名规则是***类型-vendor***；
	+ **encver**：编码版本号，用于备份到磁盘时用；
	+ **typemethods_ptr**，这个结构体保存了数据类型相关的操作函数， 比如rdb格式的加载和备份等等。
+ 创建命令，`int RedisModule_CreateCommand(RedisModuleCtx *ctx, const char *name, RedisModuleCmdFunc cmdfunc, const char *strflags, int firstkey, int lastkey, int keystep);`
	+ **name**是命令名字，这是实际调用命令时要输入的名字；
	+ **cmdfunc**是注册的函数，函数的定义格式是`int MyCommand_RedisCommand(RedisModuleCtx *ctx, RedisModuleString **argv, int argc);`; 
+ 获取一个 key 的句柄，`void *RedisModule_OpenKey(RedisModuleCtx *ctx, robj *keyname, int mode);`，有了这个句柄，可以查看当前 key 的类型，并且操作这个 key，写入值、写入过期时间、删除等操作；
+ 从 Redis 获取值。`void *RedisModule_ModuleTypeGetValue(RedisModuleKey *key);`
+ 把值写入 Redis，`int RedisModule_ModuleTypeSetValue(RedisModuleKey *key, moduleType *mt, void *value);`；
+ 命令的返回需要注意，返回值只能是成功`REDISMODULE_OK`和失败`REDISMODULE_ERR`，但是只返回这个是不行的，还需要返回内容。
	+ `RedisModule_ReplyWithError`，返回错误；
	+ `RedisModule_ReplyWithSimpleString`，返回字符串；
	+ `RedisModule_ReplyWithNull`，返回空，一般查询的 key 没有对应值的时候用。


### 用 Go 实现一个 Redis 组件

不太会用 C，自己想写个组件不是很好搞，还好有一个 Go 版本的库来辅助用 Go 开发。[go-rm](https://github.com/wenerme/go-rm)，看头像是个国人，很不错。README 里有用 Go 实现了最开始举的`HGETSET`的例子，可以跑起来看看。

这个 Go 语言的包函数命名和 C 的差不太多，上手不是很费劲。

#### 开发一个 JSON 格式的组件

我准备着手开发支持 JSON 格式的组件，它支持保存 JSON，根据用户输入的参数返回 JSON 内符合条件的数据。命令大概是这个样子：

	127.0.0.1:6340> json.set doc '{"foo":"bar","baz":43}'
	"{\"foo\":\"bar\",\"baz\":43}"
	
	127.0.0.1:6340> json.get doc baz a
	{"baz":43}

#### echo 命令

先写一个简单的练练手。初始化当前组件：

    func init() {
        rm.Mod = CreateMyMod()
    }
    
    func CreateMyMod() *rm.Module {
        mod := rm.NewMod()
        mod.Name = "json"
        mod.Version = 1
        mod.Commands = []rm.Command{CreateCommand_ECHO()}
        return mod
    }
    
    func main() {
        // In case someone try to run this
        rm.Run()
    }

编写 echo 的命令实现。里面有参数校验，调用`Reply`很重要，否则客户的会卡死。

    func CreateCommand_ECHO() rm.Command {
        return rm.Command{
            Usage:    "print message",
            Desc:     `like echo.`,
            Name:     "print",
            Flags:    "",
            FirstKey: 1, LastKey: 1, KeyStep: 1,
            Action: func(cmd rm.CmdContext) int {
                ctx, args := cmd.Ctx, cmd.Args
                if len(args) != 2 {
                    return ctx.WrongArity()
                }
                ctx.ReplyWithString(args[1])
                return rm.OK
            },
        }
    }


#### 写入 Redis

把数据解析到一个`map[string]interface{}`里面保存。

    func CreateCommand_JSONSET() rm.Command {
        return rm.Command{
            Usage:    `json.set a {"foo":"bar","baz":42}`,
            Desc:     `store a json object.`,
            Name:     "json.set",
            Flags:    "",
            FirstKey: 1, LastKey: 1, KeyStep: 1,
            Action: func(cmd rm.CmdContext) int {
                ctx, args := cmd.Ctx, cmd.Args
                if len(args) != 3 {
                    return ctx.WrongArity()
                }
    
                ctx.AutoMemory()
                key, ok := openHashKey(ctx, args[1])
                if !ok {
                    return rm.ERR
                }
    
                // var val *JsonData
                raw := args[2].String()
                rm.LogDebug("raw: %s", raw)
    
                val := new(JsonData)
                val.Name = args[1]
                val.data = make(map[string]interface{}, 1)
                err := json.Unmarshal([]byte(raw), &val.data)
                if err != nil {
                    ctx.ReplyWithError(fmt.Sprintf("ERR %v", err))
                    return rm.ERR
                }
    
                if key.IsEmpty() {
                    if key.ModuleTypeSetValue(ModuleType, unsafe.Pointer(val)) == rm.ERR {
                        ctx.ReplyWithError("ERR Failed to set module type value")
                        return rm.ERR
                    }
                } else {
                    valOld := (*JsonData)(key.ModuleTypeGetValue())
                    valOld.data = val.data
                }
    
                ctx.ReplyWithString(args[2])
                return rm.OK
            },
        }
    }

#### 读取 JSON

如果没有找到 key，需要返回空。

    func CreateCommand_JSONGET() rm.Command {
        return rm.Command{
            Usage:    `json.get a foo`,
            Desc:     `get a json object.`,
            Name:     "json.get",
            Flags:    "",
            FirstKey: 1, LastKey: 1, KeyStep: 1,
            Action: func(cmd rm.CmdContext) int {
                ctx, args := cmd.Ctx, cmd.Args
                if len(args) < 2 {
                    return ctx.WrongArity()
                }
    
                key, ok := openHashKey(ctx, args[1])
                if !ok {
                    return rm.ERR
                }
                val := (*JsonData)(key.ModuleTypeGetValue())
                rm.LogDebug("raw: %v", val)
    
                if val == nil || val.data == nil {
                    ctx.ReplyWithNull()
                    return rm.OK
                }
    
                resLen := len(args[2:])
    
                var resMap map[string]interface{}
                if resLen == 0 {
                    resMap = make(map[string]interface{}, len(val.data))
                    for k, v := range val.data {
                        resMap[k] = v
                    }
                } else {
                    resMap = make(map[string]interface{}, resLen)
                    for _, arg := range args[2:] {
                        a := arg.String()
                        rm.LogDebug(a)
                        if v, exists := val.data[a]; exists {
                            resMap[a] = v
                        }
                    }
                }
    
                res, err := json.Marshal(resMap)
                if err != nil {
                    ctx.ReplyWithError(err.Error())
                    return rm.ERR
                }
    
                ctx.ReplyWithSimpleString(string(res))
                return rm.OK
            },
        }
    }

### 总结

Redis 这个组件功能真的是很厉害，用Redis的分布式、主从同步、自动备份到磁盘这些特性，分分钟搭起一个高可用分布式应用。



关于数据备份和恢复的部分我还没有研究，等下次搞明白了再说吧。完整的代码放在[GitHub](https://github.com/mnhkahn/RedisJsonGo)上面，有需要可以去看。

---



 

{% include JB/setup %}
