---
layout: post
title: "Tmux入门指南：终端多窗口管理与工作区持久化"
description: "详细介绍Tmux的核心功能、安装方法、配置技巧和常用快捷键。文章涵盖会话管理、窗口操作、面板分屏、复制粘贴等实用功能，提供完整的配置示例和操作指南，帮助开发者提升终端工作效率，实现任务持久化和多任务并行处理。"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1776085217/clipboard_1776085213621_jheqdgknz.webp"
category: "Tool"
tags: ["Tmux", "AI", "Claude"]
---

- 目录
{:toc}

---

## 什么是TMUX

**Tmux = 终端里的多窗口管理器 + 永不消失的工作区**

1. 会话持久化：关闭终端不中断任务，随时断开重连。
2. 三层结构：会话、窗口、面板，实现多任务并行。
3. 终端分屏：一个窗口内切多屏，同时看代码、日志、AI。
4. 多窗口标签：像浏览器标签一样管理多个工作区。
5. 跨平台一致：Mac/Linux/ 服务器操作完全相同。
6. 纯键盘高效：快捷键为主，不用鼠标也能快速操作。
7. 鼠标支持：点选、滚轮、拖拽分屏都可用。
8. 高度可定制：改快捷键、配色、状态栏，适配自己习惯。
9. 会话保存恢复：关机重启也能恢复之前布局。
10. 共享协作：多人同屏操作，适合结对编程。（Claude Teams）。这也是我学习Tmux的原因。

## 安装
```bash
# macOS
brew install tmux

# Ubuntu/Debian
sudo apt install tmux

# CentOS/RHEL
sudo yum install tmux
```

## 配置
```bash
# ------------------------------
# Tmux 基础配置（Claude Teams 专用）
# ------------------------------

# 前缀键改为 Ctrl+a (更顺手)
set -g prefix C-a
unbind C-b
bind C-a send-prefix

# 解决按键延迟问题
set -sg escape-time 0

# 窗口/面板索引从 1 开始
set -g base-index 1
setw -g pane-base-index 1

# 开启鼠标支持（必须！）
set -g mouse on

# 历史记录行数
set -g history-limit 50000

# 快速重载配置文件: C-a r
bind r source-file ~/.tmux.conf \; display-message "✅ Tmux 配置已重载"

# ------------------------------
# 分屏快捷键（超级好用）
# ------------------------------
bind | split-window -h  # 左右分屏
bind - split-window -v  # 上下分屏

# ------------------------------
# 面板切换（方向键）
# ------------------------------
bind -n M-Left select-pane -L
bind -n M-Right select-pane -R
bind -n M-Up select-pane -U
bind -n M-Down select-pane -D

# ------------------------------
# 视觉主题 + 状态栏配色
# ------------------------------
set -g status-position bottom
set -g status-bg colour237
set -g status-fg white
set -g status-style "bg=colour237,fg=white"

# 左边：会话名 + 用户
set -g status-left-length 40
set -g status-left "#[fg=green]#S #[fg=yellow]#(whoami)#[default]"

# 右边：时间 + 前缀状态提示
set -g status-right-length 60
set -g status-right "#{?client_prefix,🔴 前缀已激活 ,}#[fg=cyan]%Y-%m-%d %H:%M#[default]"

# 窗口标签样式
setw -g window-status-style "fg=colour245,bg=colour237"
setw -g window-status-current-style "fg=white,bg=blue,bold"

# 面板边框
set -g pane-border-style "fg=colour238"
set -g pane-active-border-style "fg=blue"

# ------------------------------
# 按下前缀键时 状态栏变红（超级明显）
# ------------------------------
set -g status-style "fg=white,bg=#{?client_prefix,red,colour237}"
set -g message-style "fg=white,bg=blue"
```

## 窗口&面板
这是一个易混淆概念，窗口和面板快捷键是不同的，下图可以帮助理解。

````
窗口1 (Window 1)
┌─────────────┬─────────────┐
│ 面板1       │ 面板2        │ ← 这俩用 方向键 切换
│ (Pane 1)    │ (Pane 2)     │
└─────────────┴─────────────┘
      ↑
      你只有这一个窗口，所以 n/p 没用
```

## 快捷键

### 会话管理

| 操作     | 命令 / 快捷键               | 说明                       |
| -------- | --------------------------- | -------------------------- |
| 新建会话 | tmux new -s 会话名          | 例：tmux new -s claude-dev |
| 查看会话 | tmux ls                     | 列出所有会话               |
| 进入会话 | tmux a -t 会话名            | a=attach                   |
| 退出会话 | 前缀键 + d                  | detach，后台保留           |
| 关闭会话 | tmux kill-session -t 会话名 | 彻底关闭                   |
| 切换会话 | 前缀键 + s                  | 列表选择切换               |

### 窗口管理

| 操作       | 快捷键     | 说明       |
| ---------- | ---------- | ---------- |
| 新建窗口   | 前缀键 + c | create     |
| 下一个窗口 | 前缀键 + n | next       |
| 上一个窗口 | 前缀键 + p | previous   |
| 重命名窗口 | 前缀键 + , | 自定义名称 |
| 关闭窗口   | 前缀键 + & | 确认关闭   |
| 窗口列表   | 前缀键 + w | 可视化选择 |

### 面板管理

| 操作     | 快捷键                              | 说明                 |
| -------- | ----------------------------------- | -------------------- |
| 左右分屏 | 前缀键 + %                          | 垂直分割             |
| 上下分屏 | 前缀键 + "                          | 水平分割             |
| 切换面板 | 前缀键 + 方向键                     | 上下左右切换         |
| 关闭面板 | 前缀键 + x                          | 确认关闭             |
| 全屏面板 | 前缀键 + z                          | 放大 / 恢复          |
| 调整大小 | 前缀键 + Alt + 方向键               | 微调面板尺寸         |
| 同步输入 | 前缀键 + :setw synchronize-panes on | 所有面板同步执行命令 |

### 复制/粘贴

| 操作         | 快捷键     | 说明          |
| ------------ | ---------- | ------------- |
| 进入复制模式 | 前缀键 + [ | 可滚动 / 选择 |
| 开始选择     | Space      | 光标移动选中  |
| 复制         | Enter      | 复制到缓冲区  |
| 粘贴         | 前缀键 + ] | 粘贴内容      |

{% include JB/setup %}
