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

{% include JB/setup %}
