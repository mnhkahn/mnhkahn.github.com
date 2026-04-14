---
layout: post
title: "Claude Code安装与使用完全指南：从OpenRouter到黄大善人模型"
description: "详细介绍Claude Code的安装方法，包括使用OpenRouter模型的环境变量配置和启动步骤，以及通过claude-code-router代理黄大善人模型的完整流程。文章还提供了Claude Code的常用快捷键列表，帮助开发者高效使用这一AI编码工具。"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1775371907/clipboard_1775371904806_ogum7e6k4.webp"
category: "AI"
tags: ["AI", "Claude"]
---

- 目录
{:toc}

---

# 准备

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

这里需要魔法，绕过Claude登录限制。

# 安装使用OpenRouter模型

官方文档：[Claude Code](https://openrouter.ai/docs/guides/coding-agents/claude-code-integration)

## 配置环境变量 

注意`ANTHROPIC_API_KEY`要留空，保存后执行`source`。

```bash
export OPENROUTER_API_KEY="<your-openrouter-api-key>"
export ANTHROPIC_BASE_URL="https://openrouter.ai/api"
export ANTHROPIC_AUTH_TOKEN="$OPENROUTER_API_KEY"
export ANTHROPIC_API_KEY=""

source ~/.zshrc # 记得要让模型生效
```

## 启动

如果前面的配置都正确，不会要求登录并且执行`/init`命令后会初始化项目，创建CLAUDE.md文件。

```bash
cd /path/to/your/project
claude
/status
/init
```

# 使用黄大善人模型

[claude-code-router](https://github.com/musistudio/claude-code-router?tab=readme-ov-file)支持在本地路由模型、做协议转换。在这里我们用它代理黄大善人的模型。

1. 注册。移步：[黄大善人官网](https://build.nvidia.com)。
   1. 注册好后创建API Key。
   2. 也可以点击右上角的View Code，能看到完整Url和API Key。
2. 安装代理`npm install -g @musistudio/claude-code-router`
3. 配置`ccr ui`。强烈建议用这个，比直接改配置省事。
4. 启动Claude。`ccr code`。

# 接入LangSmith

## 安装插件
```
/plugin marketplace add langchain-ai/langsmith-claude-code-plugins
/plugin install langsmith-tracing@langsmith-claude-code-plugins
/reload-plugins
```

## 配置Token

路径：`.claude/settings.local.json`。
```
{
  "env": {
    "TRACE_TO_LANGSMITH": "true",
    "CC_LANGSMITH_API_KEY": "<LangSmith API key>",
    "CC_LANGSMITH_PROJECT": "my-project"
  }
}
```

[Trace Claude Code applications](https://docs.langchain.com/langsmith/trace-claude-code)

# 模型选择

| 模型名称                                   | 别名     | 核心定位                   | 适用场景                                                         | 核心优势                                                               |
| ------------------------------------------ | -------- | -------------------------- | ---------------------------------------------------------------- |
| Claude 3.5/4.5 Sonnet（执行力 / 日常首选） | 十四行诗 | 开发主力                   | 日常代码编写、复杂需求理解、功能落地实现、代码重构优化           | 在模型智力与响应速度间达成完美平衡，是绝大多数编码任务的最高性价比选择 |
| Claude 3.5/4.5 Opus（逻辑王 / 高阶规划）   | 宏大乐章 | 复杂任务攻坚               | 系统架构设计、高复杂度算法开发、大型项目重构、超长上下文深度理解 | 思考逻辑缜密、具备全局统筹能力，是 Claude 系列中推理能力最强的型号     |
| Claude 3.5/4.5 Haiku（闪电速 / 轻量级）    | 俳句     | 简单辅助、高频轻量任务处理 | 简单样板代码生成、文档内容总结、代码格式化、轻量自动化脚本编写   | 响应速度最快，调用成本极低，适合高频次、低复杂度的辅助需求             |

# Claude Teams

官方文档：[协调 Claude Code 会话团队](https://code.claude.com/docs/zh-CN/agent-teams#%E5%90%AF%E7%94%A8-agent-teams)

```
我需要做一个安卓app，功能是xxxx。创建一个Agent团队， 从不同的角度来探索这个问题：一个负责调研xxxxxx；一个负责交互，要设计出来完整功能，例如xxxxxx；一个负责开发app，基于原生安卓框架开发；一个负责测试，确保调研和设计到功能都被实现。这几个角色的工作有依赖关系，注意工作流程。
```

# 增加提示音

这个很重要，由于CC能力很强需要后台做很多事情，所以需要提示音来提醒我们任务进度。你可以参考这篇文档调整自己喜欢的提示音[配置任务提示音](https://claude-docs.plugins-world.cn/claude-docs/experience/notification-sound.html)。

- Notification 需要操作确认时播放Glass.aiff
- Stop 任务完成时播放Ping.aiff

```
vi ~/.claude/settings.json

{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "afplay /System/Library/Sounds/Glass.aiff"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "afplay /System/Library/Sounds/Ping.aiff"
          }
        ]
      }
    ]
  }
}
```

# Shortcuts

| Shortcut  | Action                                     |
| --------- | ------------------------------------------ |
| Ctrl+C    | Cancel current generation or input         |
| Ctrl+D    | Exit Claude Code                           |
| Ctrl+L    | Clear terminal screen                      |
| Ctrl+R    | Reverse search command history             |
| Esc + Esc | Rewind to previous checkpoint (undo)       |
| Shift+Tab | Cycle permission modes (default/plan/yolo) |
| Ctrl+G    | Open input in external editor (vim, etc.)  |
| Ctrl+O    | Toggle verbose output                      |
| Ctrl+T    | Toggle task list                           |
| Ctrl+F    | Kill all background agents (press twice)   |

[Claude Code Cheat Sheet – Commands, Shortcuts, Tips](https://computingforgeeks.com/claude-code-cheat-sheet/#google_vignette)

# 配置文件

[Claude Code 设置](https://code.claude.com/docs/zh-CN/settings)。

{% include JB/setup %}
