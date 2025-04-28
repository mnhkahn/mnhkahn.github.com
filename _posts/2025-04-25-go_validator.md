---
layout: post
title: "validator 包使用方法"
description: "使用 Go 语言 validator 包的测试示例。"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1745831658/IMG_6647_gfhpml.jpg"
category: "Go"
tags: ["Validator", "Golang"]
---

* 目录
{:toc}
---

```go
package valiader

import (
	"github.com/go-playground/validator/v10"
	"github.com/stretchr/testify/assert"
	"os"
	"testing"
)

var v = validator.New()
var rules = map[string]string{
	"NotNull":        "required",
	"LargerThanZero": "gt=0",
	"Enum":           "required,oneof=1 2 3",
}

func TestMain(m *testing.M) {
	v.RegisterStructValidationMapRules(rules, Struct{})
	os.Exit(m.Run())
}

type Struct struct {
	NotNull        string
	LargerThanZero int
	Enum           int
}

// https://pkg.go.dev/github.com/go-playground/validator/v10#section-readme
func TestValidate(t *testing.T) {
	// 正常值放过
	var x Struct
	x.NotNull = "not null string"
	x.LargerThanZero = 1
	x.Enum = 1
	assert.NoError(t, v.Struct(x))

	// 异常值报错
	x.NotNull = ""
	x.LargerThanZero = -1
	x.Enum = 9
	err := v.Struct(x)
	assert.Error(t, err)
	t.Log(err)
}
```


{% include JB/setup %}
