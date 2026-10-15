mnhkahn.github.com
==================

    rake post title="hello world" category="life" date="2013-04-21" tags="" description="description"

## 博客邮件订阅

所有文章在 Gitalk 评论前显示订阅卡片，表单直接提交到 Mailchimp，并在新窗口显示实际订阅结果。公开的表单参数在 `_config.yml` 的 `newsletter` 中维护；API Key 仅保存在仓库 Actions Secret `MAILCHIMP_API_KEY`，不进入网页或源码。

`Send Blog Newsletter` 在默认分支的 `pages-build-deployment` 成功后运行。它读取线上 `/newsletter.json`，确认其 revision 与该次部署一致，再通过 Mailchimp Marketing API 发信。发件人使用 Audience 的默认配置，默认将同批新增文章合并成一封标题、摘要和原文链接邮件。

- 首次运行登记当时全部已发布文章，不补发历史内容。
- 以后只发新增文章；修改现有文章不发送。文章唯一标识使用 Jekyll `post.id`，变更日期、分类或文件名可能被视为新文章。
- 单篇文章的 YAML 元数据可添加 `newsletter: false` 跳过通知。
- 持久状态保存在 `newsletter-state` 分支的 `state.json`，不要删除或重置它。此分支不作为 Pages 发布来源。
- 创建的 Campaign ID 会在发送前保存。发送结果不明确时，重跑会查询同一个 Campaign，避免重复发送。
- Mailchimp 发送检查失败时保留草稿和待发送状态；在 Mailchimp 修正账户、发件人或额度问题后，手动运行此工作流并取消 `dry_run` 即可重试。
- 手动运行默认勾选 `dry_run`，只预览新文章，不创建 Campaign、不发送、不更新状态。首次初始化需要取消勾选，或等待首次部署成功自动初始化。
- 工作流需要 `contents: write` 权限，以维护状态分支；API Key 不需要放在 GitHub Variables 中。

本地验证（不调用发送 API）：

```bash
bundle exec jekyll build
python3 -m unittest discover -s tests -v
NEWSLETTER_MANIFEST=_site/newsletter.json DRY_RUN=true python3 scripts/send_newsletter.py > /tmp/cyeam-newsletter-preview.html
```
