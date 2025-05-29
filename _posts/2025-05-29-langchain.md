---
layout: post
title: "LangSmith介绍以及Golang的介绍方法"
description: "本次我们会学习LangSmith，会介绍它能做什么，以及如何在Python/Golang中使用它。"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1748527429/langchain_stack_112024_efvvgt.svg"
category: "AI"
tags: ["AI","Python", "Golang", "LangSmith"]
---

* 目录
{:toc}
---

### LangSmith

LangSmith是一个用于管理和监控机器学习模型生命周期的平台，它可以帮助开发者更好地监控和优化他们的模型。

- 可观察性。可以支持分析、追踪，并且可以基于这些数据配置看板和报警；
- 评估。评估您的应用在生产流量中的表现。
- Prompt 工程。通过版本控制迭代升级你的提示词。

特性也可以看下面这个图，完整资料移步[官网](https://docs.smith.langchain.com/?_gl=1*13mwwef*_ga*MTM1NDY2MTAwMy4xNzQ4MDc4MjY5*_ga_47WX3HKKY2*czE3NDg0ODAwNDEkbzkkZzEkdDE3NDg0ODAyODQkajYwJGwwJGgw)：

![IMG-THUMBNAIL](https://res.cloudinary.com/cyeam/image/upload/v1748528362/ls-diagram-5be7dd68b135f573a7b0e163692e6800_t0heck.png)

#### 效果

![IMG-THUMBNAIL](https://res.cloudinary.com/cyeam/image/upload/v1748528659/langsmith_ece94p.jpg)

看到这个效果基本就知道LangSmith的强大了，它能完整记录跟LLM交互的过程以及相应内容。

#### Python 接入

Python 默认就可以打开，不需要额外的代码，你可以直接设定好环境变量或者通过如下代码配置。

```python
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGSMITH_ENDPOINT"]="https://api.smith.langchain.com"
os.environ["LANGSMITH_API_KEY"]="你申请到的Key"
os.environ["LANGSMITH_PROJECT"]="你创建的项目名称"
```

### Golang 接入

Golang 本身langchaingo包不支持，我看ISSUE里作者也提到他没想到如何像Python一样自动记录，我目前找到一个十来个Star的包`github.com/devalexandre/langsmithgo`。

#### 初始化

```go
var smith *langsmithgo.Client
os.Setenv("LANGSMITH_API_KEY", "你申请到的Key")
os.Setenv("LANGSMITH_PROJECT_NAME", "你创建的项目名称")

smith, err = langsmithgo.NewClient()
if err != nil {
  return fmt.Errorf("langsmithgo.NewClient: %v", err)
}
```

#### 写入请求和响应

```go
import (
	"context"
	"fmt"

	"github.com/devalexandre/langsmithgo"
	"github.com/google/uuid"
	"github.com/mnhkahn/gogogo/logger"
	"github.com/tmc/langchaingo/llms"
)
func SmithStart(ctx context.Context, prompt string) string {
	runId := uuid.New().String()
	err := smith.Run(&langsmithgo.RunPayload{
		RunID:   runId,
		Name:    "langsmithgo-chain",
		RunType: langsmithgo.Chain,
		Inputs: map[string]interface{}{
			"prompt": prompt,
		},
	})
	if err != nil {
		logger.Errorf("smith.Run: %v", err)
	}
	return runId
}

func SmithEnd(ctx context.Context, runId, output string) {
	err := smith.PatchRun(runId, &langsmithgo.RunPayload{
		Outputs: map[string]interface{}{
			"output": output,
		},
	})

	if err != nil {
		logger.Errorf("smith.PatchRun: %v", err)
	}
}
```


{% include JB/setup %}
