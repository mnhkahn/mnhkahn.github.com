---
layout: post
title: "Ask User Question：让 AI Agent 停下来问对问题"
description: "介绍 Ask user question 在 AI Agent Skill 中的使用方式、接口协议和跨平台兼容写法，重点对比 Claude Code 的 AskUserQuestion 与 Codex 的 request_user_input，并用 git-cmsg 的提交确认流程展示如何设计可靠的人机交互。"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1779721905/clipboard_1779721902212_v1onvenzs.webp"
category: "AI"
tags: ["AI", "Agent", "Skills", "Codex", "Claude Code"]
---

* 目录
{:toc}

---

## 概述

AI Agent 在执行任务时，最危险的不是不会做，而是**在需要用户决策时继续往前做**。

例如生成 Git 提交信息时，Agent 可以分析 diff、生成 commit message、暂存文件、执行提交。但真正进入 `git commit` 之前，有几个决策必须交给用户：

- 这些文件是不是都应该提交？
- 可疑文件要不要从暂存区移除？
- `.gitignore` 要不要更新？
- 生成的提交信息是否符合预期？

这些问题如果只靠普通文本问答，用户容易漏看，Agent 也容易误判。`Ask user question` 的价值就在这里：它把“问用户”变成一个结构化协议，让 Agent 明确暂停、展示选项、等待选择，然后再继续。

本文基于 `git-cmsg` Skill 的改造经验，整理 Ask user question 的使用方式、接口协议，以及同时兼容 Claude Code 和 Codex 的 Markdown 写法。

---

## 一、Ask user question 解决什么问题

在 Skill 里，很多步骤不是单纯的工具调用，而是“用户授权点”。

典型场景包括：

| 场景 | 为什么要问 |
|------|------------|
| 提交代码前确认 commit message | `git commit` 会改变仓库历史，必须用户确认 |
| 发现可疑文件 | `.env`、构建产物、缓存文件可能不应该提交 |
| 修改 `.gitignore` | 会写入仓库配置，需要用户同意 |
| 删除、覆盖、发布、部署 | 都是高影响操作，不能自动继续 |

普通文本提问当然也能用，但结构化提问有三个优势：

1. **边界更明确**：Agent 必须停下来，不能边问边继续执行。
2. **选项更稳定**：用户看到的是几个明确动作，而不是开放式问题。
3. **结果更好解析**：后续流程可以按选项分支处理，减少误解。

所以在 Skill 文档里，Ask user question 不应该只是“可以用的 UI”，而应该被写成流程控制的一部分。

---

## 二、Claude Code：AskUserQuestion

Claude Code 的结构化提问工具通常在 Skill frontmatter 的 `allowed-tools` 中声明：

```yaml
---
name: git-cmsg
description: Use when generating Git commit messages, writing commit messages, committing code, or when the user mentions commit、提交、commit message、提交信息.
argument-hint: "[--dry-run]"
allowed-tools: AskUserQuestion, Bash
---
```

在正文里，可以直接要求 Agent 使用 `AskUserQuestion`：

```markdown
Use AskUserQuestion to ask:

- question: "生成的提交信息是否符合要求？"
- header: "提交信息确认"
- options:
  - { label: "确认提交", description: "使用此提交信息进行提交" }
  - { label: "重新生成", description: "重新分析代码变更并生成新的提交信息" }
  - { label: "取消操作", description: "取消当前提交操作" }
```

这个写法适合 Claude Code，因为模型能看到 `AskUserQuestion` 这个工具，并能按 Skill 的要求调用它。

但问题是：如果同一份 Skill 也要给 Codex 使用，`AskUserQuestion` 就不是一个通用工具名。Codex 里如果没有这个工具，Agent 要么会退化成普通文本提问，要么更糟糕：尝试调用一个不存在的工具。

因此，跨平台 Skill 不能只写 `AskUserQuestion`，必须写清楚平台分支。

---

## 三、Codex：request_user_input

Codex 对应的结构化提问工具是 `request_user_input`。它的参数结构是一个 `questions` 数组，每个问题包含 `header`、`id`、`question` 和 `options`。

一个典型协议如下：

```json
{
  "questions": [
    {
      "header": "提交确认",
      "id": "commit_message_action",
      "question": "是否按上面的提交信息执行提交？",
      "options": [
        {
          "label": "确认提交 (Recommended)",
          "description": "使用此提交信息执行 git commit。"
        },
        {
          "label": "重新生成",
          "description": "重新分析代码变更并生成新的提交信息。"
        },
        {
          "label": "取消操作",
          "description": "停止流程，不执行提交。"
        }
      ]
    }
  ]
}
```

几个字段的含义：

| 字段 | 说明 |
|------|------|
| `header` | 短标题，适合 UI 展示，最好 12 个字符以内 |
| `id` | 稳定的 snake_case 标识，用于映射用户回答 |
| `question` | 真正的问题文本，可以包含必要上下文 |
| `options` | 2-3 个互斥选项 |
| `label` | 用户看到的短标签 |
| `description` | 说明选择后的影响或代价 |

Codex 的实践约束比普通 Markdown 文档更严格：

- 选项应控制在 2-3 个。
- 推荐项放第一个，并在 label 后加 `(Recommended)`。
- 不要提供没有意义的 “Other” 选项，客户端会自动支持自由输入。
- 工具不可用、模式不允许或调用失败时，要立即退回普通文本确认。

这里最后一点很关键。结构化提问不是所有 Codex 运行模式都可用，所以 Skill 必须写 fallback。

---

## 四、跨平台 Decision UI 写法

为了让同一份 Skill 同时支持 Claude Code 和 Codex，可以把具体工具名抽象成一个统一的 `Decision UI` 章节。

`git-cmsg` 的核心规则是：

```markdown
## Decision UI

For every user decision in this skill, use this order:

1. **Claude Code:** use `AskUserQuestion` with the listed `question`, `header`, and `options`.
2. **Codex:** use `request_user_input` with one question object. Include `header`, a stable snake_case `id`, `question`, and 2-3 options. Put the recommended option first and suffix its label with `(Recommended)`.
3. **Fallback:** if the current agent does not expose either structured question tool, or the tool is unavailable, not permitted, or fails, ask the same options as plain text. Do not continue until the user clearly chooses an option.

Never invent a tool name that is not available in the current runtime.
```

这个写法有几个好处：

1. **保留 Claude Code 能力**：不需要删掉 `AskUserQuestion`。
2. **支持 Codex 原生工具**：Codex 看到 `request_user_input` 就能使用自己的结构化 UI。
3. **避免工具幻觉**：明确要求不要发明当前运行时不存在的工具名。
4. **保证流程安全**：即使结构化工具不可用，也必须文本确认后再继续。

这比在全文里反复写“如果是 Claude 就怎样，如果是 Codex 就怎样”更清晰，也更容易维护。

---

## 五、接口协议设计建议

结构化提问最容易出问题的地方，不是工具调用，而是选项设计。

### 5.1 选项必须是动作，不是态度

不推荐：

```text
好 / 不好 / 随便
```

推荐：

```text
确认提交 / 重新生成 / 取消操作
```

好的选项应该直接对应后续流程分支。用户点完以后，Agent 不需要再猜“好”到底是什么意思。

### 5.2 高风险操作不要默认继续

发现可疑文件时，不应该把“继续提交”放在推荐位。更稳妥的推荐项是排除或移除：

```markdown
- { label: "移除文件", description: "从暂存区移除这些文件，但保留在工作区" }
- { label: "继续提交", description: "确认这些文件是故意提交的" }
- { label: "取消操作", description: "取消当前提交操作" }
```

这类顺序会影响模型行为。推荐项不是 UI 装饰，而是安全默认值。

### 5.3 不要把禁止动作放进选项

`git-cmsg` 有一条硬规则：只 commit，不 push。

如果确认选项里又出现“提交并推送”，就会形成自相矛盾的 Skill：

```markdown
7. Commit but do NOT push. Never `git push`.

options:
- 确认提交
- 提交并推送
- 取消操作
```

这种冲突会让 Agent 在执行时摇摆，也会让用户误以为 push 是被允许的。正确做法是：禁止动作不要出现在选项里。

### 5.4 每个问题都要有稳定 id

Codex 的 `request_user_input` 需要 `id`，建议命名成动作语义：

| 场景 | id |
|------|----|
| 可疑文件处理 | `suspicious_file_action` |
| `.gitignore` 更新 | `gitignore_action` |
| 提交信息确认 | `commit_message_action` |

稳定 id 方便后续流程映射，也方便调试日志和自动化测试。

---

## 六、完整示例：提交信息确认

下面是一段适合放进 Skill 的跨平台写法：

```markdown
6. MUST STOP: 使用 Decision UI 展示生成的 commit message 并等待用户确认
   - question: "生成的提交信息是否符合要求？\n\n提交信息预览：\n```\n{commit_message}\n```"
   - header: "提交信息确认"
   - id: "commit_message_action"
   - options: [
       { label: "确认提交", description: "使用此提交信息进行提交" },
       { label: "重新生成", description: "重新分析代码变更并生成新的提交信息" },
       { label: "取消操作", description: "取消当前提交操作" }
     ]
```

在 Claude Code 中，Agent 应该把这段转换成 `AskUserQuestion` 调用。

在 Codex 中，Agent 应该把它转换成 `request_user_input`：

```json
{
  "questions": [
    {
      "header": "提交信息确认",
      "id": "commit_message_action",
      "question": "生成的提交信息是否符合要求？\n\n提交信息预览：\n```\n{commit_message}\n```",
      "options": [
        {
          "label": "确认提交 (Recommended)",
          "description": "使用此提交信息进行提交。"
        },
        {
          "label": "重新生成",
          "description": "重新分析代码变更并生成新的提交信息。"
        },
        {
          "label": "取消操作",
          "description": "取消当前提交操作。"
        }
      ]
    }
  ]
}
```

如果结构化提问不可用，则退回普通文本：

```text
生成的提交信息是否符合要求？

提交信息预览：
docs(git-cmsg): 支持跨平台确认交互

请选择：确认提交 / 重新生成 / 取消操作。
```

注意 fallback 不是“跳过确认”。fallback 只是 UI 形式从结构化选项降级为文本选项，用户确认这个前置条件仍然存在。

---

## 七、写 Skill 时的检查清单

在给 Skill 增加 Ask user question 时，可以按这个清单自查：

- 是否所有高影响操作前都明确 `MUST STOP`？
- 是否写清楚 Claude Code 使用 `AskUserQuestion`？
- 是否写清楚 Codex 使用 `request_user_input`？
- 是否写了工具不可用时的文本 fallback？
- 是否每个问题都有 `header`、`id`、`question`、`options`？
- Codex 选项是否控制在 2-3 个？
- 推荐项是否是最安全的默认动作？
- 选项里是否出现了 Skill 明令禁止的操作？
- 用户未确认前，是否禁止继续执行？

这个检查清单比单纯“加一个提问工具”更重要。因为真正要保证的不是 UI 弹不弹，而是 Agent 的执行边界是否清楚。

---

## 总结

Ask user question 本质上是 AI Agent 的**流程刹车**。

它不是为了让界面更好看，而是为了把“必须由用户决定”的节点显式化。Claude Code 里的 `AskUserQuestion` 和 Codex 里的 `request_user_input` 名字不同、协议不同，但在 Skill 设计里的目标是一致的：

1. 展示上下文。
2. 给出有限、互斥、可执行的选项。
3. 等待用户选择。
4. 按选择继续，或停止。

如果一个 Skill 只服务单一平台，直接写平台工具名就够了。如果希望同一份 Skill 同时跑在 Claude Code 和 Codex 上，就应该抽象出 `Decision UI`：Claude Code 走 `AskUserQuestion`，Codex 走 `request_user_input`，两者都不可用时退回文本确认。

这套写法看起来只是几行 Markdown，但它能显著降低 Agent 自作主张的概率。对提交、删除、部署、发布这类操作来说，这几行就是安全边界。
