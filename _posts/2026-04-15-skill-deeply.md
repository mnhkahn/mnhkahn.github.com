---
layout: post
title: "npx skills深度解析：AI Agent技能包管理器完全指南"
description: "详细介绍npx skills（Vercel开源AI代理技能管理器）的使用方法，包括常用命令、核心结构、SKILL.md文档YAML规范。文章对比Claude Code Skills、OpenClaw Skills和Vercel Skill的差异，分析格式兼容性、模型绑定、安全模型等关键维度，并提供优秀Skill案例和提示词设计洞察，帮助开发者高效管理和分享AI Agent技能包。"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1776251967/clipboard_1776251964128_fnof8lfxg.webp"
category: "AI"
tags: ["AI", "Skills", "Claude Code", "OpenClaw", "Agent"]
---

- 目录
{:toc}

---

# npx skills——AI Agent 能力包管理器

**npx skills = Vercel 开源 AI 代理技能管理器 CLI（Claude Code / Cursor / OpenCode 专用**

一键安装 / 管理 AI 技能包（SKILL.md），自动放到 Claude/Cursor 对应目录（.claude/skills）。全局安装要在HOME目录下执行。

官方商店：[The Agent Skills Directory](https://skills.sh)

## 常用命令

```
npx skills add 仓库地址       # 安装技能
npx skills list               # 查看已装技能
npx skills init               # 新建自己的 SKILL.md
npx skills find react        # 查找 React 相关技能包
npx skills remove 作者/仓库名  # 删除技能包
npx skills update 作者/仓库名  # 更新技能包
npx skills path               # 查看技能包目录
```
## 核心结构

```
skill-name/
├── SKILL.md          # 必填：元数据 + 使用说明/指令
├── scripts/          # 可选：可执行代码
├── references/       # 可选：参考文档
├── assets/           # 可选：模板、资源文件
└── ...               # 其他任意附加文件或目录
```

1. system prompt（AI 行为规则）
2. tools（可执行命令 / API / 浏览器操作）
3. knowledge（文档 / 规范 / 最佳实践）

## 测试Skill


```
# 校验技能文件
npx skills-ref validate ~/.claude/skills/wiki/SKILL.md
```

## SKILL.md 文档YAML规范

| 字段          | 必填 | 约束说明                                                                |
| ------------- | ---- | ----------------------------------------------------------------------- |
| name          | 是   | 最多 64 个字符。仅允许小写字母、数字和连字符。不能以连字符开头或结尾。  |
| description   | 是   | 最多 1024 个字符。不能为空。描述该技能的功能及适用场景。                |
| license       | 否   | 许可证名称，或指向内置许可证文件的引用。                                |
| compatibility | 否   | 最多 500 个字符。说明环境依赖要求（目标产品、系统软件包、网络权限等）。 |
| metadata      | 否   | 用于附加元数据的任意键值对配置。                                        |
| allowed-tools | 否   | 由空格分隔的字符串，列出该技能可使用的预授权工具。（实验性功能）        |

# Claude Code Skill / OpenCLaw Skill / Vercel Skill

有这么多工具都支持Skill，他们是一回事么？区别是什么？

| 维度        | Claude Code Skills                                      | OpenClaw Skills                                                            |
| ----------- | ------------------------------------------------------- | -------------------------------------------------------------------------- |
| 开发者      | Anthropic                                               | OpenClaw 社区（开源）                                                      |
| 核心文件    | `SKILL.md`（YAML frontmatter + Markdown 正文）          | `SKILL.md`（YAML frontmatter + Markdown 正文）                             |
| 文件格式    | 完全相同，均为 YAML frontmatter + Markdown 指令         | 同左，OpenClaw 官方称其为 AgentSkills，但格式一致                          |
| 目录结构    | `.claude/skills//SKILL.md` + `scripts/` + `references/` | `~/.openclaw/skills//SKILL.md` + `scripts/` + `references/`                |
| 作用域      | 项目级 `.claude/skills/` 或全局 `~/.claude/skills/`     | 项目级工作区 或 全局 `~/.openclaw/skills/`                                 |
| 触发方式    | Agent 自动匹配 description 或用户 `/slash-command`      | Agent 自动匹配 或 `/slash-command`                                         |
| 底层模型    | 仅限 Claude（Anthropic 闭源生态）                       | 模型无关：Claude、GPT-4、Llama 3、Mistral 等均可                           |
| 运行环境    | Anthropic 云端 或 本地终端                              | 完全自托管，代码在用户基础设施上运行                                       |
| 互相迁移    | —                                                       | 需补充 YAML frontmatter 中 `name:` `description:` 字段才能在 OpenClaw 识别 |
| 环境变量    | 通过系统环境变量读取                                    | 支持 `openclaw.json` 中的 `skills.entries..env` 配置                       |
| Vercel 兼容 | 支持，`npx skills add` 可安装                           | 支持，同一个 Vercel Skill 包无需修改                                       |
| 安全模型    | Anthropic 托管 + 权限沙箱                               | 用户自行负责：需审计 Skill 内容防止 RCE、数据泄露                          |
| 生态规模    | 官方内置 + 社区贡献                                     | ClawHub 市场 860+ 技能 + 社区贡献                                          |

## 关键差异总结

1. 格式层面几乎一致 — 都是 `SKILL.md` + YAML frontmatter + Markdown 指令 + scripts/references 辅助文件，迁移成本低
2. 最大差异在模型绑定 — Claude Code 锁定 Anthropic 生态，OpenClaw 支持任意 LLM
3. 安全模型不同 — Claude Code 有 Anthropic 官方沙箱保护；OpenClaw 需自行审计 Skill 安全性（已有案例：Cisco 安全团队发现第三方 Skill 存在数据泄露和 prompt 注入风险）
4. 迁移注意 — Claude Code Skill 迁移到 OpenClaw 时，需确保 frontmatter 包含 `name:` 和 `description:` 字段，否则 OpenClaw 无法加载

# 优秀案例

Skill除了官方商店，还可以自行实现，下面这个例子就非常经典可以深入学习。它做到了仅用一篇文档就能够实现带命令行的技能包，效果不亚于代码实现。

[wiki-gen-skill.md](https://gist.github.com/farzaa/c35ac0cfbeb957788650e36aabea836d)。

## 命令

```
/wiki ingest        # Convert your data into raw markdown entries
/wiki absorb all    # Compile entries into wiki articles
/wiki query 什么是agent  # Ask questions about the wiki 
```

## 提示词洞察

### Hint

```
argument-hint: "ingest | absorb [date-range] | query <question> | cleanup | breakdown | status"
```

### ingest

> Write a Python script ingest.py to do this. This step is mechanical, no LLM intelligence needed.

让AI现场写脚本实现，禁止模型转换文档，非常有想象力，除了节省token，关键是手写脚本，一般我们都是自己先写好，非常大胆。

> Process entries one at a time, chronologically. Read _index.md before each entry to match against existing articles. Re-read every article before updating it. This is non-negotiable.

语气比我写的更重——**绝对不能商量**。

### absorb

- Anti-Cramming反灌输。禁止文件过大堆砌
- Anti-Thinning 禁止创建无实质内容的空页面 / 薄页面
- Every 15 Entries: Checkpoint 每 15 条做质量审计

**定期检查**，这里的检查策略跟之前提到过的harness很像——强力提示词：

> 1. Quality audit: Pick your 3 most-updated articles. Re-read each as a whole piece. Ask:
>    1. Does it tell a coherent story, or is it a chronological dump?
>    2. Does it have sections organized by theme, not date?
>    3. Does it use direct quotes to carry emotional weight?
>    4. Does it connect to other articles in revealing ways?
>    5. Would a reader learn something non-obvious? If any article reads like an event log, rewrite it.
> 2. Check if any articles exceed 150 lines and should be split.

### query

**不要猜、不要阅读整个wiki、禁止修改**

> - Never read raw diary entries (raw/entries/). The wiki is the knowledge base.
> - Don't guess. If the wiki doesn't cover it, say so.
> - Don't read the entire wiki. Be surgical.
> - Don't modify any wiki files. Query is read-only.

## 关系图谱可视化

生成的关系图谱可以用工具可视化：[Obsidian](https://release-assets.githubusercontent.com/github-production-release-asset/262342594/c77de2d1-539d-4976-bd10-6eebc9e43184?sp=r&sv=2018-11-09&sr=b&spr=https&se=2026-04-14T02%3A45%3A51Z&rscd=attachment%3B+filename%3DObsidian-1.12.7.dmg&rsct=application%2Foctet-stream&skoid=96c2d410-5711-43a1-aedd-ab1947aa7ab0&sktid=398a6654-997b-47e9-b12b-9515b896b4de&skt=2026-04-14T01%3A45%3A02Z&ske=2026-04-14T02%3A45%3A51Z&sks=b&skv=2018-11-09&sig=SI02YTivj8%2FlbTzaDjNqtHLLnZ65XOW82LHLgh8h0PA%3D&jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmVsZWFzZS1hc3NldHMuZ2l0aHVidXNlcmNvbnRlbnQuY29tIiwia2V5Ijoia2V5MSIsImV4cCI6MTc3NjEzNjExMSwibmJmIjoxNzc2MTMyNTExLCJwYXRoIjoicmVsZWFzZWFzc2V0cHJvZHVjdGlvbi5ibG9iLmNvcmUud2luZG93cy5uZXQifQ.usFElitqhWQxEiPysghDs7biTxHARBNr7u4EraBVWcQ&response-content-disposition=attachment%3B%20filename%3DObsidian-1.12.7.dmg&response-content-type=application%2Foctet-stream)。它会扫描当前目录所有md文件，所以打开目录时选择要注意下要选择生成的文件夹，选根目录内容会非常多。

{% include JB/setup %}
