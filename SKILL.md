---
name: blog-maintenance
description: 博客维护和管理相关的技能集合，包括文章发布、图片处理、链接检查等。
---

# 博客维护技能

## 描述
本技能提供了博客项目的日常维护和管理功能，帮助智能体快速完成博客相关任务。

## 使用场景
- 发布新文章
- 处理图片资源
- 检查站点链接
- 优化文章格式
- 管理博客配置

## 指令

### 发布新文章
1. 在 `_posts` 目录创建新文件，命名格式为 `YYYY-MM-DD-title.md`
2. 添加YAML前置元数据，包括：
   ```yaml
   ---
   layout: post
   title: "文章标题"
   description: "文章描述"
   figure: "文章封面图链接"
   category: "分类"
   tags: ["标签1", "标签2"]
   ---
   ```
3. 编写Markdown内容，包括标题、段落、代码块等
4. 使用 `bundle exec jekyll serve` 本地预览
5. 提交并部署

### 生成标题和描述
1. 文章标题建议在60个字符以内，更新到name字段上，能够突出重点吸引人打开文章
2. 文章描述建议在300个字符以内，更新到description字段上，能够突出重点吸引人打开文章

### 同步更新架构师知识库

执行`python scripts/index_to_qdrant.py`上传。

### 图片处理
1. 图片建议使用外部CDN存储（如Cloudinary）
2. 图片尺寸建议适中，避免过大影响加载速度
3. 图片添加适当的alt属性
4. 使用响应式图片标签

### 链接检查
1. 构建站点：`bundle exec jekyll build`
2. 运行链接检查：`bundle exec htmlproofer ./_site`
3. 修复发现的死链接或错误链接

### 优化文章格式
1. 使用清晰的标题层级
2. 代码块添加语言标识
3. 适当使用列表和引用
4. 保持段落短小精悍
5. 添加目录（在文章开头添加 `- 目录\n{:toc}`）

### 管理博客配置
1. 修改 `_config.yml` 文件调整站点设置
2. 更新 `Gemfile` 管理依赖
3. 配置主题和插件
4. 优化SEO设置

## 示例

### 发布新文章示例

**输入：**
```bash
# 创建新文章文件
 touch _posts/2026-04-03-example-post.md
```

**文章内容：**
```markdown
---
layout: post
title: "示例文章"
description: "这是一篇示例文章"
figure: "https://example.com/image.jpg"
category: "技术"
tags: ["示例", "教程"]
---

- 目录
{:toc}

---

# 示例文章

这是文章内容...
```

**预览：**
```bash
bundle exec jekyll serve
```

### 链接检查示例

**输入：**
```bash
bundle exec jekyll build
bundle exec htmlproofer ./_site
```

**输出：**
```
Running on ./_site
Checking 100 links...
HTML-Proofer finished successfully.
```