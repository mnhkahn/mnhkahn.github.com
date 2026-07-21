---
layout: post
title: "把邮箱交给 AI：cyeam-cli mail skill 多邮箱收发指南"
description: "用 cyeam-cli 的 mail skill 管理 Zoho、Gmail 等多个邮箱：从读取、总结到发送邮件，再到安全配置的完整实践。"
category: "AI"
tags: ["AI", "cyeam-cli", "邮件", "Skill", "效率工具"]
figure: https://res.cloudinary.com/cyeam/image/upload/v1784648057/cyeam-cli-mail-skill.jpg
---

* 目录
{:toc}

---

每天打开邮箱、筛掉订阅通知、判断哪些邮件要回，再把结果转述给同事——这类工作看似零碎，却很容易打断真正重要的事。

`cyeam-cli` 的 `mail` skill 把收件箱接入 AI 助手：它既能连接多个邮箱，也能让你用自然语言完成查收、阅读、归纳、标记和发送邮件。上面的截图正是一个典型场景：一句“看一下未读邮件，总结主要内容”，AI 就读出 AdSense 政策通知，并明确告诉你这是一封无需处理的合规提醒。

# 能做什么

mail skill 通过标准 IMAP/SMTP 工作，支持 Zoho、Gmail、iCloud 等常见服务。它不会删除或移动邮件，适合作为一个稳妥的邮件助手。

## 先从自然语言开始

在支持 cyeam-cli skill 的 AI 对话中，直接说你的需求即可：

> 看一下我有哪些未读邮件，按重要程度总结；需要我处理的单独列出来。

助手会先列出已配置邮箱的近期邮件，再根据邮件的账户名和 UID 读取正文；如果你明确同意，也可以把已处理的邮件标记为已读。对你来说不必记命令，重点是把目标说清楚：哪个邮箱、看哪些邮件、是否标记已读、希望怎样总结。

常用对话还包括：

- “看一下 cyeam 邮箱最近 10 封邮件。”
- “读一下 Gmail 里 UID 123 的邮件，并标记已读。”
- “把 cyeam 里 UID 123、456 都标记为已读。”
- “用工作邮箱给 team@example.com 发封邮件，主题是本周进度，正文是……”

## 也可以直接在终端使用

skill 底层对应的是清晰的命令。想自己在终端操作时，下面这些就够用了：

```bash
# 一次查看所有账户的最近邮件，先获取账户名和 UID
cyeam mail list --all --limit 20

# 阅读指定账户中的一封邮件；加 --mark-read 会同时标为已读
cyeam mail read gmail 123 --mark-read

# 批量标记已读
cyeam mail mark-read cyeam --uids 123,456,789

# 发送邮件；--to 和 --cc 都可重复使用
cyeam mail send cyeam \
  --to team@example.com \
  --subject "本周进度" \
  --body "项目已完成测试，计划周五发布。"
```

这里有一个很实用的工作方式：**先 list，再 read**。邮件 UID 属于具体账户，所以先用 `cyeam mail list --all` 找到邮件对应的账户和 UID，再用 `cyeam mail read <账户> <uid>` 读取正文。

# 如何配置

配置文件位于 `~/.cyeam/mail.json`。每个账户写一组 IMAP/SMTP 连接参数，命令中使用的账户名由 `name` 决定。

推荐把邮箱地址和应用专用密码放进环境变量，而不是写进 JSON。这样配置文件可以安全地保存或同步，凭据也更容易按环境切换。

```json
{
  "accounts": [
    {
      "name": "cyeam",
      "imap_host": "imap.zoho.com",
      "imap_port": 993,
      "username_env": "CYEAM_MAIL_USERNAME",
      "password_env": "CYEAM_MAIL_PASS",
      "smtp_host": "smtp.zoho.com",
      "smtp_port": 465
    }
  ]
}
```

然后在终端或 shell 配置中设置变量：

```bash
export CYEAM_MAIL_USERNAME="you@cyeam.com"
export CYEAM_MAIL_PASS="你的应用专用密码"
```

`username` 也可以直接写入邮箱地址，但 `username_env` 更适合多设备和自动化场景。若省略 SMTP 设置，CLI 会默认将 IMAP 域名中的 `imap.` 替换为 `smtp.`，并使用 465 端口；为了让配置一眼可读，生产使用时仍建议显式写出。

## 配置前的三件事

1. 在邮箱后台开启 IMAP 访问。
2. 创建**应用专用密码**，不要使用日常登录密码。
3. 将应用专用密码设置到 `password_env` 指定的环境变量中。465 端口使用 TLS；若服务商要求 587，则使用 STARTTLS。

# 示例：个人 Gmail + 工作 Zoho

下面是一份可以直接改造的双邮箱配置。它把个人 Gmail 和工作 Zoho 邮箱放在同一个文件中，AI 可以先跨账户汇总，再按账户处理某一封邮件。

```json
{
  "accounts": [
    {
      "name": "gmail",
      "imap_host": "imap.gmail.com",
      "imap_port": 993,
      "username_env": "GMAIL_USERNAME",
      "password_env": "GMAIL_APP_PASSWORD",
      "smtp_host": "smtp.gmail.com",
      "smtp_port": 465
    },
    {
      "name": "work",
      "imap_host": "imap.zoho.com",
      "imap_port": 993,
      "username_env": "WORK_MAIL_USERNAME",
      "password_env": "WORK_MAIL_APP_PASSWORD",
      "smtp_host": "smtp.zoho.com",
      "smtp_port": 465
    }
  ]
}
```

对应的环境变量：

```bash
export GMAIL_USERNAME="your.name@gmail.com"
export GMAIL_APP_PASSWORD="Gmail 应用专用密码"
export WORK_MAIL_USERNAME="you@company.com"
export WORK_MAIL_APP_PASSWORD="Zoho 应用专用密码"
```

## 场景一：个人邮箱做信息分流

个人 Gmail 往往混杂账单、订阅、验证码、社群通知和旅行行程。每天早上可以让助手先做一次分类：

> 汇总 Gmail 未读邮件：账单或安全相关的标成高优先级；需要回复的列出下一步；广告和订阅只做一句摘要。

得到清单后，再让它读出一两封高优先级邮件。这样不会因几十封通知反复切换注意力，也能避免错过付款、安全提醒等真正重要的内容。

## 场景二：工作邮箱做待办提炼

工作 Zoho 邮箱更适合处理项目更新、客户回复和会议安排。你可以在开工前问：

> 查看工作邮箱未读邮件，提取需要我今天完成的事项；为每项标注截止时间、相关人和建议回复。

确认内容后，再让助手基于你的要点起草回复，或用 `cyeam mail send work` 发送。发信仍应由你确认收件人、语气与附件是否齐全——AI 负责压缩阅读和起草时间，最终判断仍在你手里。

# 安全边界

mail skill 的设计目标是让邮件操作足够有用，也足够克制：目前支持列出、读取、发送和标记已读/未读，不支持删除、移动邮件、下载附件或全文搜索。

日常使用时，仍建议做到以下几点：

- 为每个邮箱单独创建应用专用密码；不再使用时及时撤销。
- 不把 `mail.json` 中的密码提交到 Git；优先使用 `*_env` 字段。
- 发信前复核收件人、抄送人与正文，特别是涉及客户、合同和账号信息时。
- 在共享服务器或自动化环境中，用部署平台的 Secret 管理环境变量。

# 总结

cyeam-cli mail skill 不只是“在终端收发邮件”。它把多个收件箱变成 AI 可以理解的工作入口：先汇总，再定位，最后处理；你保留判断权，把重复阅读和整理交给助手。

从配置一个个人 Gmail 或工作 Zoho 邮箱开始，下一次面对满屏未读邮件时，试试直接问一句：**“帮我看看哪些真的需要处理。”**
