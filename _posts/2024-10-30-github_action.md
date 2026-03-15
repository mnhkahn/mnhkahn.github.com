---
layout: post
title: "Github Actions 初探，代码发布成功后发送微信推送"
description: "完善部署监控能力，完善持续集成能力。"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1730298406/wechat_notify.jpg"
category: "Monitor"
tags: ["Github","wechat"]
---

* 目录
{:toc}
---

先看图感受下，当部署完成后可以在微信里收到推送。Github Actions支持自动触发，执行命令。本文不会讲解具体语法，可以参考阮一峰的博客[《GitHub Actions 入门教程》](https://www.ruanyifeng.com/blog/2019/09/getting-started-with-github-actions.html)。

## 代码自动部署（以fly.io为例）

1. 在代码仓库里执行`fly launch --no-deploy`创建部署文件`fly.toml`；
2. 执行命令`fly tokens create deploy -x 999999h`创建部署密钥；
3. 访问Github网址，点击自己的项目->Settings->Secrets and variables->Actions->Repository secrets->New repository secret，填写部署密钥。Name为`FLY_API_TOKEN`，Secret为第二步生成的内容；
4. 在代码仓库里，在这个目录里创建问题：`.github/workflows/fly.yml`，把下面的内容粘贴进去；

```
name: Fly Deploy
on:
  push:
    branches:
      - master    # change to main if needed
jobs:
  deploy:
    name: Deploy app
    runs-on: ubuntu-latest
    concurrency: deploy-group    # optional: ensure only one action runs at a time
    steps:
      - uses: actions/checkout@v4
      - uses: superfly/flyctl-actions/setup-flyctl@master
      - run: flyctl deploy --remote-only
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

5. 简单介绍下语法：
	- on/push，当master分支代码提交后触发执行；
	- jobs/deploy，触发后执行的内容。`runs-on`指运行环境，`steps`指运行指令，`env`加载之前第三部设置的环境变量，`uses`指引入了三方的工具包，这个例子是使用fly官方的部署包；

完整例子移步[Continuous Deployment with Fly.io and GitHub Actions](https://fly.io/docs/launch/continuous-deployment-with-github-actions/)。


## 微信通知

1. 重复上面第三步，新建一个Name为`WECHAT_WORK_BOT_WEBHOOK`的密钥，值为微信通知的Webhook地址，用企业微信创建一个即可（拉个微信群添加机器人后会展示出来）；
2. 在目录`github/workflows`里新建文件`notify.yml`，粘贴下面的内容：

```
name: Watch Workflow Status
on:
  workflow_run:
    workflows: [ "Fly Deploy" ]
    types: [ completed ]
env:
  WECHAT_WORK_BOT_WEBHOOK: ${{secrets.WECHAT_WORK_BOT_WEBHOOK}}

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - id: prep
        uses: hocgin/action-env@main
      - name: WeChat Work Notification
        uses: chf007/action-wechat-work@master
        env:
          WECHAT_WORK_BOT_WEBHOOK: ${{env.WECHAT_WORK_BOT_WEBHOOK}}
        with:
          msgtype: markdown
          content: "**【[${{ steps.prep.outputs.repo_full_name }}](${{ steps.prep.outputs.repo_html_url }})】** \n
          📌 ${{ github.event.workflow_run.conclusion == 'success' && '☀️☀️☀️☀️☀️' || '🌧️🌧️🌧️🌧️🌧️' }} \n
          🏃 [@${{ steps.prep.outputs.sender }}](${{ steps.prep.outputs.sender_html_url }})\n
          🕐 <font color=\"comment\">${{ steps.prep.outputs.action_trigger_at }}</font> \n
          🔧 <font color=\"warning\">${{ steps.prep.outputs.source_branch || '∅' }} -> ${{ steps.prep.outputs.target_branch || '∅' }}</font> \n
          🏆 <font color=\"comment\">${{ steps.prep.outputs.env || '未知版本' }} / ${{ steps.prep.outputs.version || '未知版本' }}</font> \n
          📝 提交信息: ${{ steps.prep.outputs.commit_body }} \n
          \n
          [查看更多](${{ steps.prep.outputs.repo_homepage || steps.prep.outputs.repo_html_url }})
          "
```

3. on/workflow_run 指在部署完成后执行这个脚本，`workflows`里的`Fly Deploy`是前面第一步的工作流名称，如果你用的不是fly，按照自己情况修改；
4. jobs 复用了`chf007/action-wechat-work@master`包的能力，发送markdown格式的消息，能使用的变量可以参考这个[文件](https://github.com/hocgin/action-env/blob/main/action.yml)。

## 飞书通知

```
name: Watch Workflow Status
on:
  workflow_run:
    workflows: [ "Fly Deploy" ]
    types: [ completed ]
env:
  # 飞书机器人 Webhook 地址（需在 Secrets 中配置 LARK_BOT_WEBHOOK）
  LARK_BOT_WEBHOOK: ${{ secrets.LARK_BOT_WEBHOOK }}

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - id: prep
        uses: hocgin/action-env@main

      - name: Send Lark notification
        env:
          LARK_WEBHOOK: ${{ env.LARK_BOT_WEBHOOK }}
        run: |
          # 使用 jq 构建飞书 post 消息
          jq -n \
            --arg repo_full_name "${{ steps.prep.outputs.repo_full_name }}" \
            --arg repo_html_url "${{ steps.prep.outputs.repo_html_url }}" \
            --arg conclusion "${{ github.event.workflow_run.conclusion }}" \
            --arg sender "${{ steps.prep.outputs.sender }}" \
            --arg sender_html_url "${{ steps.prep.outputs.sender_html_url }}" \
            --arg action_trigger_at "${{ steps.prep.outputs.action_trigger_at }}" \
            --arg source_branch "${{ steps.prep.outputs.source_branch }}" \
            --arg target_branch "${{ steps.prep.outputs.target_branch }}" \
            --arg env "${{ steps.prep.outputs.env }}" \
            --arg version "${{ steps.prep.outputs.version }}" \
            --arg commit_body "${{ steps.prep.outputs.commit_body }}" \
            --arg repo_homepage "${{ steps.prep.outputs.repo_homepage }}" \
            '{
              msg_type: "post",
              content: {
                post: {
                  zh_cn: {
                    title: "Cyeam站点部署通知（Fly Deploy）",
                    content: [
                      [ { tag: "a", text: "【\($repo_full_name)】", href: $repo_html_url } ],
                      [ { tag: "text", text: (if $conclusion == "success" then "☀️☀️☀️☀️☀️" else "🌧️🌧️🌧️🌧️🌧️" end) } ],
                      [ { tag: "a", text: "@\($sender)", href: $sender_html_url } ],
                      [ { tag: "text", text: "🕐 \($action_trigger_at)" } ],
                      [ { tag: "text", text: "🔧 \($source_branch // "∅") -> \($target_branch // "∅")" } ],
                      [ { tag: "text", text: "🏆 \($env // "未知版本") / \($version // "未知版本")" } ],
                      [ { tag: "text", text: "📝 提交信息: \($commit_body // "")" } ],
                      [ { tag: "a", text: "查看更多", href: ($repo_homepage // $repo_html_url) } ]
                    ]
                  }
                }
              }
            }' | curl -X POST -H "Content-Type: application/json" -d @- $LARK_WEBHOOK
```

---


{% include JB/setup %}
