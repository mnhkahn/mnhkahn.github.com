---
layout: post
title: "AI 模型类型速查指南"
description: "一文搞懂 Text、Multimodal、Reasoning、Image Generation 等各类 AI 模型的区别和代表产品。"
category: "AI"
tags: ["AI", "模型", "Claude", "GPT"]
---

* 目录
{:toc}

---

## AI 模型类型总览

| 类型 | 图标 | 用途 | 代表模型 | 备注 |
|------|------|------|----------|------|
| **Text** | 📝 | 聊天、写代码、翻译、总结文本 | Llama 4、Qwen 3.5、GPT-4.5、DeepSeek V4 | 最常见 |
| **Multimodal / Vision** | 👁️ | 看懂图片、视频内容 | GPT-4o、Gemini 2.5 Pro、Gemini 2 Flash | 理解图片，非生成 |
| **Reasoning** | 🧠 | 解数学题、逻辑推理、复杂算法 | DeepSeek R1 Zero、o3-mini、Claude 3.7 Sonnet | 慢但准 |
| **Image Generation** | 🎨 | 从文字生成图片 | Flux 1.1 Pro、SD 3.5、DALL-E 3 | 免费列表暂无 |
| **OCR** | 🔍 | 图片转文字 | DeepSeek-OCR V2、PaddleOCR v3 | 专用工具 |
| **Embedding** | 🔗 | 文本向量化（用于检索） | BGE M3、GTE-Qwen、Jina Embeddings v2 | 专用工具 |
| **Reranker** | 📊 | 搜索结果重排序 | BGE Reranker v3、Jina Reranker v2 | 专用工具 |
| **ASR / TTS** | 🎤 | 语音转文字 / 文字转语音 | Whisper v3、SenseVoice、Kokoro v1.5 | 专用工具 |

## 易混淆对比

> **图像理解 vs 图像生成**：完全不同的两类模型
> - **图像理解**：你给它一张图，它告诉你图里有什么（👁️ 看图片）
> - **图像生成**：你给它一段文字，它画出一张图（🎨 画图片）

## Claude 系列说明

| 模型 | 类型 | 定位 |
|------|------|------|
| **Opus** | Text + Multimodal | Claude 旗舰级，推理和多模态理解能力极强 |
| **Sonnet** | Text + Multimodal | 主力模型，性能与速度平衡，日常首选 |
| **Haiku** | Text + Multimodal | 轻量级，极速响应、低延迟 |

💡 **Claude 全系都支持多模态（看图片）**，只是能力强弱不同。

### Thinking / 扩展思考支持

| 模型 | 多模态 | Thinking / 扩展思考 |
|------|--------|---------------------|
| **Opus** | ✅ 支持 | ✅ 有深度推理能力 |
| **Sonnet 3.7** | ✅ 支持 | ✅ **支持 extended thinking**（2025年新特性） |
| **Haiku** | ✅ 支持 | ❌ 不支持 |

## 什么是多模态？

> **模态 = 信息的表现形式**
>
> **多模态 = 同时处理多种不同形式的信息**

### 常见模态类型

- 📝 **文本**：对话、文章、代码
- 👁️ **图像**：图片、照片、截图
- 🎥 **视频**：短视频、监控画面
- 🎤 **音频**：语音、音乐、声音

### 关键区分：输入 vs 输出

| 能力 | 行为 | 术语 |
|------|------|------|
| **图像理解** | 你给它图，它告诉你图里有什么 | 这就是 **多模态** |
| **图像生成** | 你给它文字，它给你画出一张图 | 这是生成式AI，**不是多模态的必要条件** |

> 💡 **理解图片就叫多模态了！不需要能生成图片。**
>
> 现在绝大多数多模态模型（GPT-4o、Claude、Gemini）都只能理解图片，不能生成图片。

## 免费模型现状

当前免费模型列表中**没有图像生成模型**（Stable Diffusion、DALL-E 等），只有以下几类：

- ✅ Text（最多）
- ✅ Reasoning（推理模型）
- ✅ Multimodal（多模态/视觉理解）
- ✅ 专用工具（OCR、Embedding、ASR 等）

## 总结

模型确实很多，但按功能来分就很清晰了。记住这几个核心分类，就不会被各种名词绕晕：

- 📝 **Text**：说话写字
- 👁️ **Vision**：看图片（理解）
- 🧠 **Reasoning**：动脑子解题
- 🎨 **Image Gen**：画图片（生成）
- 🔧 **其他**：专门工具
