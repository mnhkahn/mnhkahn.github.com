---
layout: post
title: "介绍一下Json的Number"
description: "目前英国做接口都是用Json格式，Json格式也是比较容易理解的一种格式，上手很容易。但是还是有一些需要记录的东西。"
category: "golang"
tags: ["Golang","Json"]
---

Json的使用基本没有什么难度，就拿Golang来说，直接来个`encoding/json`包里的`func Marshal(v interface{}) ([]byte, error)`和`func Unmarshal(data []byte, v interface{}) error`就能对Json进行编解码了。具体的文件就是采用反射的方法，可以参考我之前的文章[『Golang通过反射实现结构体转成JSON数据』](http://blog.cyeam.com/golang/2014/08/11/go_json/)。

现在问题来了，如下的map需要大家是如何解析的？

	{"10000000000":10000000000,"111":1}
	
如果直接定义一个map来解析，定义成`map[string]int64`，我们是肯定可以解析成功的，解析的时候会将数据转换为我们需要的数据类型。那么问题来了：如果把类型定义成`map[string]interface{}`会是如何解析的呢？

我一直是用显示定义的来解析，也就是`map[string]int64`，当我用`map[string]interface{}`解析的时候，我就想当然的认为，`interface{}`里面存的是`int64`的数据。后来调试了一通，最后才发现是本末倒置了。

Json数据其实就是一个字符串，里面按照一定的格式保存我们的数据。Json支持的数据类型与Golang语言的关系如下：

	bool, for JSON booleans
	float64, for JSON numbers
	string, for JSON strings
	[]interface{}, for JSON arrays
	map[string]interface{}, for JSON objects
	nil for JSON null

我们可以注意到，Json格式的数字和Golang语言里面的`float64`是相关联的。也就是说，默认情况下数字类型将会转换成`float64`类型。如果我们显示的指出了数字类型，比如`int64`，他会将数字再转成`int64`。

我们看一下源码，`encoding/json/decode.go func (d *decodeState) literalStore(item []byte, v reflect.Value, fromQuoted bool)`

	func (d *decodeState) literalStore(item []byte, v reflect.Value, fromQuoted bool) {
		...
		switch c := item[0]; c {
			case 'n': // null
			...
			case 't', 'f': // true, false
			...
			case '"': // string
			...
			default: // number
			if c != '-' && (c < '0' || c > '9') {
				if fromQuoted {
					d.error(fmt.Errorf("json: invalid use of ,string struct tag, trying to unmarshal %q into %v", item, v.Type()))
				} else {
					d.error(errPhase)
				}
			}
			s := string(item)
			switch v.Kind() {
			default:
				if v.Kind() == reflect.String && v.Type() == numberType {
					v.SetString(s)
					break
				}
				if fromQuoted {
					d.error(fmt.Errorf("json: invalid use of ,string struct tag, trying to unmarshal %q into %v", item, v.Type()))
				} else {
					d.error(&UnmarshalTypeError{"number", v.Type(), int64(d.off)})
				}
			case reflect.Interface:
				n, err := d.convertNumber(s)
				if err != nil {
					d.saveError(err)
					break
				}
				if v.NumMethod() != 0 {
					d.saveError(&UnmarshalTypeError{"number", v.Type(), int64(d.off)})
					break
				}
				v.Set(reflect.ValueOf(n))

			case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32, reflect.Int64:
				n, err := strconv.ParseInt(s, 10, 64)
				if err != nil || v.OverflowInt(n) {
					d.saveError(&UnmarshalTypeError{"number " + s, v.Type(), int64(d.off)})
					break
				}
				v.SetInt(n)

			case reflect.Uint, reflect.Uint8, reflect.Uint16, reflect.Uint32, reflect.Uint64, reflect.Uintptr:
				n, err := strconv.ParseUint(s, 10, 64)
				if err != nil || v.OverflowUint(n) {
					d.saveError(&UnmarshalTypeError{"number " + s, v.Type(), int64(d.off)})
					break
				}
				v.SetUint(n)

			case reflect.Float32, reflect.Float64:
				n, err := strconv.ParseFloat(s, v.Type().Bits())
				if err != nil || v.OverflowFloat(n) {
					d.saveError(&UnmarshalTypeError{"number " + s, v.Type(), int64(d.off)})
					break
				}
				v.SetFloat(n)
			}
		}
	}
	
	func (d *decodeState) convertNumber(s string) (interface{}, error) {
		if d.useNumber {
			return Number(s), nil
		}
		f, err := strconv.ParseFloat(s, 64)
		if err != nil {
			return nil, &UnmarshalTypeError{"number " + s, reflect.TypeOf(0.0), int64(d.off)}
		}
		return f, nil
	}
	
可以看出来，Json解析实现的时候通过反射来判断要生成的具体的类型。如果是`interface{}`类型，通过`converNumber`方法转成`float64`（里面是通过`strconv.ParseFloat`实现），如果类型是整形相关，通过`strconv.ParseInt`方法转换。无符号整形是通过`strconv.ParseUint`实现。



---

###### 

---

{% include JB/setup %}