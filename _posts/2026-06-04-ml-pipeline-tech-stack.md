---
layout: post
title: "大模型从训练到落地：一文看懂全链路技术栈"
description: "从模型训练、格式转换、高性能推理到 AI 应用开发，梳理大模型落地的四大核心环节及其关键工具与框架。"
category: "AI"
tags: ["AI", "大模型", "训练", "推理", "技术栈"]
---

* 目录
{:toc}

---

大模型从训练到真正落地，中间会经历四个核心环节：**训练 → 转换 → 推理 → 应用开发**。每个环节都有不同的目标、产出和工具链。

# 训练环节

从大规模数据中学习模型参数，包含预训练、微调、对齐等。

| 维度 | 说明 |
|---|---|
| **典型产出** | `.pth` / `.pt` (PyTorch), `.h5` / `.keras` (Keras), `.pb` (TensorFlow), `model.bin` (HuggingFace) |
| **基础框架** | PyTorch, TensorFlow, JAX |
| **并行训练** | Megatron-LM, DeepSpeed, Colossal-AI |
| **微调/对齐** | HuggingFace Transformers, TRL (RLHF), LoRA |
| **数据/监控** | Spark, Weights & Biases, TensorBoard |

# 转换环节

将训练好的专用格式模型转换为通用中间表示，便于跨框架部署优化。

| 维度 | 说明 |
|---|---|
| **典型产出** | `.onnx` |
| **导出工具** | torch.onnx, tf2onnx, keras2onnx |
| **优化工具** | ONNX Simplifier, ONNX Optimizer |

# 推理环节

高性能、低延迟地执行模型预测，并提供服务化能力。

| 维度 | 说明 |
|---|---|
| **典型产出** | `.engine` / `.plan` (TensorRT), `.onnx`, `.mlmodel` (Core ML), `.gguf` (llama.cpp) |
| **高性能引擎** | vLLM (LLM 专用 PagedAttention), TensorRT / TensorRT-LLM (NVIDIA GPU 极致优化), ONNX Runtime (通用跨平台), TGI (HuggingFace 生态), Llama.cpp (CPU/Apple 芯片) |
| **服务化框架** | NVIDIA Triton Inference Server, BentoML, Ray Serve |

# AI 应用开发

拿到大模型后，通过编排构建出复杂的 AI 应用（如 Agent、RAG、自动化工作流）。

| 维度 | 说明 |
|---|---|
| **产出** | 不产生特定模型文件，产出为业务代码和编排配置 |
| **代表框架** | Eino (Go, 字节跳动), LangChain (Python), LlamaIndex (Python) |

# 总结

四个环节环环相扣：训练环节产出能力，转换环节打通部署壁垒，推理环节保障性能和服务，应用开发环节把模型能力真正转化为产品价值。选型时需根据团队技术栈、业务场景和硬件条件灵活组合。
