---
layout: post
title: "Sub2API Fly.io 零成本部署实战指南：AI API网关搭建全流程"
description: "详细介绍如何将Sub2API（开源AI API网关平台）零成本部署到Fly.io，配合Neon PostgreSQL和Upstash Redis构建完整方案。文章包含架构原理、部署步骤、环境变量配置、一键部署脚本使用，以及解决Neon连接方式、JWT密钥设置、配置文件重写等常见问题的详细指南。适合个人或小型团队自建AI API代理服务，月成本为$0。"
category: "AI"
tags: ["AI", "Sub2API", "Fly.io"]
---

- 目录
{:toc}

---

# Sub2API Fly.io 部署实战指南

## 项目简介

**Sub2API** 是一个开源的 AI API 网关平台，用于集中管理和分发 Claude、Gemini、OpenAI 等 AI 服务的 API 配额。它支持多账号管理、Token 级计费、智能调度、并发控制等功能，适合自建 AI API 代理服务。

本文介绍如何将 Sub2API 零成本部署到 Fly.io，配合 Neon PostgreSQL 和 Upstash Redis 构建完整的免费方案。

---

## 架构原理

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Fly.io (免费)   │────▶│  Upstash Redis   │────▶│  Neon Postgres  │
│  Sub2API 应用    │     │   每日 10k 命令   │     │   500MB 存储    │
│  256MB RAM      │     │   256MB 存储     │     │                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

**服务分工**：
- **Fly.io**: 运行 Sub2API 容器，提供 HTTP 服务
- **Neon**: Serverless PostgreSQL，存储用户、账号、用量等数据
- **Upstash**: Serverless Redis，作为缓存和队列

---

## 部署步骤

### 1. 准备工作

注册三个服务账号：
- [Fly.io](https://fly.io) - 应用托管
- [Neon](https://neon.tech) - PostgreSQL 数据库
- [Upstash](https://upstash.com) - Redis 缓存

### 2. 获取连接信息

**Neon**：创建项目后，在 Connect 页面选择 **Direct** 连接方式（重要！），复制连接参数。

**Upstash**：创建 Redis 数据库后，在 Details 页面获取 Endpoint 和 Password。

### 3. 配置环境变量

复制模板文件并填写：

```bash
cp .env.example .env
vim .env
```

关键配置项：
```bash
# PostgreSQL (必须使用 Direct 连接，不能用 Pooled)
DATABASE_HOST=xxx.cloud.neon.tech
DATABASE_USER=neondb_owner
DATABASE_PASSWORD=xxx
DATABASE_DBNAME=neondb

# Redis
REDIS_HOST=xxx.upstash.io
REDIS_PASSWORD=xxx

# JWT 密钥 (必须设置固定值，否则重启后登录失效)
JWT_SECRET=$(openssl rand -hex 32)

# TOTP 密钥 (用于 2FA，可选)
TOTP_ENCRYPTION_KEY=$(openssl rand -hex 32)

# 管理员账号
ADMIN_EMAIL=your-email@example.com
```

### 4. 一键部署

```bash
./deploy/deploy.sh
```

脚本会自动：
- 验证环境变量
- 设置 Fly Secrets
- 部署应用到 Fly.io

部署成功后，访问 `https://your-app.fly.dev` 即可使用。

---

## 遇到的坑

### 坑 1：Neon Pooled 连接导致 SQL 错误

**现象**：登录后页面频繁报错 500，日志显示：
```
pq: bind message supplies 5 parameters, but prepared statement "" requires 2
```

**原因**：Neon 的 Pooled 连接使用 PgBouncer，不支持 PostgreSQL Prepared Statements，而 Sub2API 代码中使用了大量预处理语句。

**解决**：在 Neon Console 中切换为 **Direct** 连接，不使用 `-pooler` 的 host。

### 坑 2：JWT_SECRET 未设置导致登录失效

**现象**：登录后 5 秒自动跳回登录页，会话无法保持。

**原因**：Sub2API 使用 JWT Token 验证登录状态，如果 `JWT_SECRET` 未设置或每次部署变化，Token 会失效。

**解决**：必须设置固定的 `JWT_SECRET`（64 位 hex 字符串），通过 `fly secrets set` 配置。

### 坑 3：fly.toml 被自动重写

**现象**：配置文件里的 `memory = '256mb'` 被改成 `memory = '1gb'`，还自动添加了 `max_machines_running = 2`。

**原因**：Flyctl 在部署时会"优化"配置文件，可能导致超出免费额度。

**解决**：在 `fly.toml` 中明确设置：
```toml
[[vm]]
  memory = '256mb'
  cpu_kind = 'shared'
  cpus = 1

[http_service]
  max_machines_running = 1  # 限制最多 1 台实例
```

### 坑 4：数据卷配置问题

**现象**：部署报错需要创建 `sub2api_data` 卷。

**解决**：如果不需要持久化配置文件和日志，可以直接注释掉 `fly.toml` 中的 `[[mounts]]` 部分，所有配置通过环境变量传递。

### 坑 5：CORS 和代理设置

**现象**：前端 API 调用返回 401 或跨域错误。

**原因**：Fly.io 的代理层默认不信任 X-Forwarded-For，可能导致 IP 验证失败。

**解决**：在 `fly.toml` 中设置 `force_https = true`，并确保 `SERVER_MODE=release`。

---

## 运维建议

1. **监控日志**：`fly logs --app sub2api-flyio`
2. **查看状态**：`fly status --app sub2api-flyio`
3. **注意免费额度**：
   - Fly.io：256MB 内存，闲置时会休眠
   - Neon：500MB 存储，超出需付费
   - Upstash：每日 10k 命令

4. **数据备份**：定期导出 Neon 数据库，免费套餐无自动备份。

---

## 总结

通过 Fly.io + Neon + Upstash 的组合，可以零成本部署 Sub2API，适合个人使用或小型团队。关键是正确配置数据库连接（用 Direct 不用 Pooled）和固定 JWT 密钥。整个方案月成本为 $0，但需要注意免费额度限制。

完整代码和配置请参考项目仓库。

{% include JB/setup %}
