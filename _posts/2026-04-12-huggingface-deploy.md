---
layout: post
title: "Huggingface Spaces部署实战指南：AI模型托管与服务搭建全流程"
description: "详细介绍如何在Huggingface Spaces上部署AI模型，包括准备工作、创建Space、项目配置（Dockerfile、README.md、requirements.txt）、部署方式（Git推送、CLI上传）、环境变量配置和常见问题解决。文章涵盖从代码准备到服务上线的完整流程，适合AI模型开发者将模型快速部署为在线服务。"
category: "AI"
tags: ["AI", "Huggingface", "Docker"]
---

- 目录
{:toc}

---
## 1. 准备工作

### 1.1 必要条件

- [Huggingface](https://huggingface.co/) 账号
- 已安装 `git` 和 `git-lfs`（用于大文件管理）
- 模型文件和代码准备完毕

### 1.2 安装 Git LFS（大文件支持）

```bash
# macOS
brew install git-lfs

# Ubuntu/Debian
sudo apt-get install git-lfs

# 初始化 Git LFS
git lfs install
```
## 2. 创建 Space

### 2.1 通过 Web 界面创建

1. 登录 Huggingface
2. 点击右上角头像 → New Space
3. 填写 Space 信息：
  - Space Name: 您的 Space 名称（如 mo-ocr）
  - SDK: 选择 Docker（本教程使用 Docker 部署）
  - Space Hardware: 选择免费或付费硬件（如 CPU Basic 或 GPU）
  - Visibility: 选择 Public（公开）或 Private（私有）
4. 点击 Create Space

### 2.2 克隆 Space 仓库

创建完成后，在本地克隆仓库：

# 方式1：HTTPS
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME

# 方式2：SSH（需配置SSH密钥）
git clone git@huggingface.co:spaces/YOUR_USERNAME/YOUR_SPACE_NAME

---
## 3. 项目配置

### 3.1 必需文件清单

将以下文件放入项目目录：

```bash
┌──────────────────┬────────────────────────────────────┐
│       文件       │                说明                │
├──────────────────┼────────────────────────────────────┤
│ app.py           │ FastAPI 应用主入口                 │
├──────────────────┼────────────────────────────────────┤
│ Dockerfile       │ Docker 构建配置                    │
├──────────────────┼────────────────────────────────────┤
│ requirements.txt │ Python 依赖列表                    │
├──────────────────┼────────────────────────────────────┤
│ README.md        │ Space 说明文档（含 YAML 前置配置） │
├──────────────────┼────────────────────────────────────┤
│ 模型文件         │ .pth, .bin 等模型权重文件          │
└──────────────────┴────────────────────────────────────┘
```

### 3.2 Dockerfile 配置

```bash
# 选择基础 Python 镜像
FROM python:3.9

# 安装系统依赖（根据项目需要调整）
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \                    # OpenCV 依赖
    espeak-ng \                 # 语音合成依赖（可选）
    && rm -rf /var/lib/apt/lists/*

# 创建非 root 用户（安全最佳实践）
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# 设置工作目录
WORKDIR /app

# 先复制并安装依赖（利用 Docker 缓存层）
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
# 复制应用代码
COPY --chown=user . /app

# 启动命令（Huggingface Space 要求端口 7860）
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
```

重要：Huggingface Space 要求服务监听 7860 端口。

### 3.3 README.md 配置

```bash
README.md 需要包含 YAML 前置配置：

---
title: Mo Ocr                    # Space 标题
emoji: ⚡                        # 表情图标
colorFrom: red                   # 渐变色起始
colorTo: pink                    # 渐变色结束
sdk: docker                      # SDK 类型：docker
pinned: false                    # 是否置顶
license: apache-2.0              # 许可证
---
```

参考： https://huggingface.co/docs/hub/spaces-config-reference

### 3.4 requirements.txt 示例

```
fastapi
uvicorn[standard]
torch
torchvision
Pillow
opencv-python
numpy
python-multipart==0.0.9
transformers
huggingface_hub
# 其他项目依赖...
```

## 4. 部署方式

### 方式一：Git 推送部署（推荐）

```bash
# 进入项目目录
cd YOUR_SPACE_NAME

# 添加大文件追踪（模型文件）
git lfs track "*.pth"
git lfs track "*.bin"
git lfs track "*.ckpt"

# 添加所有文件
git add .
git add .gitattributes  # 重要：确保 LFS 配置被提交

# 提交并推送
git commit -m "Initial deployment"
git push
```

推送后，Huggingface 会自动构建 Docker 镜像并部署。

### 方式二：通过 Huggingface CLI 部署

```bash
# 安装 CLI
pip install huggingface-hub

# 登录
huggingface-cli login

# 上传文件（适合快速更新单个文件）
huggingface-cli upload YOUR_USERNAME/YOUR_SPACE_NAME app.py app.py
```

## 5. 环境变量配置

### 5.1 在 Space 设置中添加环境变量

1. 进入 Space 页面 → Settings → Variables and Secrets
2. 点击 New Variable 或 New Secret
3. 填写变量名和值

```bash
┌──────────┬──────────────────┬───────────────────────────┐
│   类型   │       说明       │         适用场景          │
├──────────┼──────────────────┼───────────────────────────┤
│ Variable │ 明文存储，可见   │ 非敏感配置如 MODEL_NAME   │
├──────────┼──────────────────┼───────────────────────────┤
│ Secret   │ 加密存储，不可见 │ API Key、Token 等敏感信息 │
└──────────┴──────────────────┴───────────────────────────┘
```

### 5.2 在代码中读取

```python
import os

# 读取环境变量
hf_token = os.getenv("read_token")
webhook_url = os.getenv("WEB_HOOK")

# 使用默认值
port = os.getenv("PORT", "7860")
```

### 5.3 常用环境变量

```python
# Huggingface 自动注入的变量
SPACE_ID = os.getenv("SPACE_ID")           # Space 完整ID
SPACE_REPO_NAME = os.getenv("SPACE_REPO_NAME")  # Space 名称

# 自定义变量示例
FEISHU_WEBHOOK_URL = os.getenv("FEISHU_WEBHOOK_URL")
MODEL_PATH = os.getenv("MODEL_PATH", "best_model.pth")
```

## 6. 常见问题

### Q1: 构建失败 / 容器无法启动

排查步骤：

1. 检查 Dockerfile 语法
2. 确认端口设置为 7860
3. 查看构建日志：Space 页面 → Files → Logs

```bash
# 本地测试 Dockerfile 是否正常
docker build -t test-space .
docker run -p 7860:7860 test-space
```

### Q2: 模型文件过大导致推送失败

解决方案：

```bash
# 确保使用 Git LFS
git lfs track "*.pth"

# 检查文件是否被 LFS 管理
git lfs ls-files

# 如果已提交到 Git，需重写历史
git lfs migrate import --include="*.pth"
```

### Q3: 内存/显存不足

优化方案：

1. 使用更小的模型 或 量化版本
2. 延迟加载模型：不在启动时加载，而是在第一次请求时加载

```python
# 延迟加载示例
model = None

def get_model():
    global model
    if model is None:
        model = load_model()  # 第一次调用时加载
    return model

@app.post("/predict")
async def predict():
    model = get_model()
    # ...
```

### Q4: 如何查看运行日志

Space 页面 → Files → Logs，或点击顶部的 Logs 标签查看实时日志。

### Q5: 免费版限制

```
┌────────┬──────────────────────┐
│ 限制项 │      免费版限制      │
├────────┼──────────────────────┤
│ CPU    │ 2 vCPU               │
├────────┼──────────────────────┤
│ 内存   │ 16 GB                │
├────────┼──────────────────────┤
│ 存储   │ 50 GB                │
├────────┼──────────────────────┤
│ 休眠   │ 48小时无访问自动休眠 │
├────────┼──────────────────────┤
│ GPU    │ 需申请或付费         │
└────────┴──────────────────────┘
```

{% include JB/setup %}
