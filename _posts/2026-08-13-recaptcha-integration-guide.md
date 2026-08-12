---
layout: post
title: "网站接入 reCAPTCHA 人机验证实战指南"
description: "从注册密钥、前端集成到 Go 后端验证，完整讲解 Google reCAPTCHA 的接入流程、版本选择、分数判定与安全注意事项。"
category: "编程"
tags: ["编程", "安全", "Go", "验证码", "Web"]
---

* 目录
{:toc}

---

注册接口被批量刷号、登录接口被撞库、评论区被垃圾内容淹没——只要是暴露在公网的表单，迟早会遇到机器人。人机验证（CAPTCHA）是成本最低的第一道防线，而 Google 的 reCAPTCHA 是其中用得最广、接入最简单的一个：前端加载一段脚本拿到令牌，后端调一个接口验证真伪，免费额度对绝大多数站点绰绰有余。

这篇文章按实际接入的顺序，把版本选择、密钥注册、前端集成、后端验证到上线后的注意事项完整走一遍。后端示例使用 Go，但验证流程就是一个 HTTPS 请求，换任何语言都一样。

# 版本怎么选

reCAPTCHA 目前有三个常见版本，适用场景不同：

- **v2 复选框**：用户勾选「我不是机器人」，风险高时弹出图片点选挑战。拦截确定性最强，但打断用户操作，适合注册、找回密码这类低频关键操作。
- **v2 隐形验证**：页面上没有复选框，提交表单时触发，可疑用户才会看到挑战。体验好于复选框，逻辑稍复杂。
- **v3 评分制**：完全不打扰用户，根据行为返回 0.0 到 1.0 的风险分（1.0 是人），由后端自己决定阈值和处置策略。适合登录、搜索、评论等高频接口，也是新项目的首选。

另外还有面向企业的 **reCAPTCHA Enterprise**，提供更细的分数档、账户防御（防密码泄露/撞库）和移动端 SDK，按调用量计费。一般个人站点用免费版 v3 就够了。

本文以 v3 为主线，v2 复选框的差异在后文单独说明。

# 注册站点密钥

打开 [reCAPTCHA 管理后台](https://www.google.com/recaptcha/admin/create)，用 Google 账号登录后创建站点：

1. **标签**：随便起个名字，方便区分多个站点。
2. **类型**：选择「基于挑战（v2）」或「基于得分（v3）」。
3. **域名**：填写站点域名，不带协议和路径，如 `example.com`。支持多个域名和子域名；本地开发加上 `localhost`。

创建成功后会得到一对密钥：

- **网站密钥（Site Key）**：公开的，写在前端页面里。
- **密钥（Secret Key）**：保密的，只存在于服务端，用于调用验证接口。**永远不要提交到前端代码或公开的仓库里。**

Google 还提供了一对永远验证通过的测试密钥，方便在 CI 和开发环境使用：

```
Site Key:   6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI
Secret Key: 6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe
```

# 前端接入

## v3：无感评分

v3 的接入分两步：加载脚本，提交表单时换取令牌。

在页面中引入脚本，`render` 参数填入 Site Key：

```html
<script src="https://www.google.com/recaptcha/api.js?render=YOUR_SITE_KEY"></script>
```

在用户提交表单前，调用 `grecaptcha.execute` 获取令牌，塞进表单一起提交：

```javascript
$('#login-form').on('submit', function (e) {
    e.preventDefault();
    var form = this;

    grecaptcha.ready(function () {
        grecaptcha.execute('YOUR_SITE_KEY', { action: 'login' }).then(function (token) {
            // 把令牌放入隐藏字段，随表单一起提交
            $('#recaptcha-token').val(token);
            form.submit();
        });
    });
});
```

配合一个隐藏字段：

```html
<form id="login-form" method="post" action="/login">
    <input type="hidden" id="recaptcha-token" name="recaptcha_token">
    <!-- 用户名、密码等其他字段 -->
</form>
```

两个要点：

- **`action` 参数**：给这次操作起个名字（如 `login`、`comment`、`signup`）。后端验证时会拿到这个值，可以用来做更精细的风控——例如 `login` 动作的平均分通常应该是多少，异常波动就说明有问题。
- **令牌有效期只有 2 分钟，且只能用一次**。所以要在用户真正提交的那一刻去取令牌，而不是页面加载时就取好。

## v2 复选框：显式验证

v2 更简单，在表单里放一个带 `data-sitekey` 的 `div`：

```html
<script src="https://www.google.com/recaptcha/api.js" async defer></script>

<form method="post" action="/signup">
    <!-- 其他字段 -->
    <div class="g-recaptcha" data-sitekey="YOUR_SITE_KEY"></div>
    <button type="submit">注册</button>
</form>
```

用户勾选后，表单会自动带上 `g-recaptcha-response` 字段，后端验证这个字段即可。脚本渲染的 iframe 默认是全局样式，放在 Bootstrap 表单里通常不用再调整。

# 后端验证

无论 v2 还是 v3，后端要做的事都一样：拿着 Secret Key 和用户令牌，向 `siteverify` 接口发一个 POST 请求。

```go
package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
	"time"
)

const (
	siteVerifyURL = "https://www.google.com/recaptcha/api/siteverify"
	secretKey     = "YOUR_SECRET_KEY" // 生产环境请从配置或环境变量读取
)

type siteVerifyResponse struct {
	Success     bool      `json:"success"`
	ChallengeTS time.Time `json:"challenge_ts"`
	Hostname    string    `json:"hostname"`
	Score       float64   `json:"score"`  // 仅 v3 返回
	Action      string    `json:"action"` // 仅 v3 返回
	ErrorCodes  []string  `json:"error-codes"`
}

func verifyRecaptcha(token, remoteIP string) (*siteVerifyResponse, error) {
	client := &http.Client{Timeout: 5 * time.Second}

	resp, err := client.PostForm(siteVerifyURL, url.Values{
		"secret":   {secretKey},
		"response": {token},
		"remoteip": {remoteIP},
	})
	if err != nil {
		return nil, fmt.Errorf("siteverify request: %w", err)
	}
	defer resp.Body.Close()

	var result siteVerifyResponse
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("decode response: %w", err)
	}
	return &result, nil
}
```

在登录处理函数里调用：

```go
func HandleLogin(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()
	token := r.FormValue("recaptcha_token")
	if token == "" {
		http.Error(w, "missing recaptcha token", http.StatusBadRequest)
		return
	}

	result, err := verifyRecaptcha(token, r.RemoteAddr)
	if err != nil {
		// 验证服务不可用时如何选择放行还是拦截，要根据业务定
		http.Error(w, "recaptcha unavailable", http.StatusServiceUnavailable)
		return
	}

	if !result.Success {
		http.Error(w, "recaptcha verification failed", http.StatusForbidden)
		return
	}

	// v3：按分数判定
	if result.Score < 0.5 {
		http.Error(w, "suspicious request", http.StatusForbidden)
		return
	}

	// 继续登录逻辑……
}
```

返回的 JSON 各字段含义：

- `success`：令牌是否有效（未过期、未重复使用、密钥匹配）。
- `hostname`：令牌是在哪个域名下发的。
- `score`：v3 专属，0.0（极可能是机器人）到 1.0（极可能是真人）。
- `action`：v3 专属，前端传入的动作名。
- `error-codes`：失败原因，如 `invalid-input-secret`、`timeout-or-duplicate`。

# 分数与 action 怎么用

v3 把判断权交给了你，这也意味着要用好它有几个实践要点：

- **默认阈值 0.5 起步**，然后观察管理后台里的分数分布再调整。正常用户的分数通常集中在 0.7 以上；如果你的真实用户大量落在 0.3 以下，说明阈值定高了。
- **分数低不等于直接拒绝**。更稳妥的做法是分级处置：0.5 以下直接拒绝，0.5～0.7 追加二次验证（短信验证码、邮箱确认、降级为 v2 图片挑战），0.7 以上直接放行。
- **校验 action**。后端确认返回的 `action` 与预期一致，防止攻击者拿一个低敏感度页面（如首页浏览）的令牌来刷登录接口——每个页面各用各的 action，令牌互不通用。
- **重要操作单独打分**。可以在关键页面（结算、改密码）调用 `grecaptcha.execute` 换取该操作专属的 action 令牌，分数只代表这一次操作的风险。

# 国内网络环境

`google.com` 在国内不可达，如果站点有国内用户，把前端脚本和验证接口的域名换成 Google 官方提供的镜像 `recaptcha.net`：

```
前端脚本：https://www.recaptcha.net/recaptcha/api.js
验证接口：https://www.recaptcha.net/recaptcha/api/siteverify
```

功能与 `google.com` 完全一致，只是域名不同。一个常见做法是后端自动切换：检测到请求来自国内 IP 就用 `recaptcha.net` 验证。前端也可以简单降级——先尝试加载 `google.com` 的脚本，超时后 fallback 到 `recaptcha.net`。

# 安全注意事项与常见坑

- **Secret Key 不出服务端**。把它写进环境变量或配置中心，不要硬编码进仓库。一旦泄露，在管理后台重新生成。
- **必须服务端验证**。前端拿到令牌不代表验证通过，令牌可以伪造；只有 `siteverify` 的返回结果可信。也不要在前端根据分数做拦截逻辑。
- **校验 hostname**。返回里的 `hostname` 如果不是你的域名，说明令牌来自别的站点，应拒绝。
- **令牌一次性、两分钟过期**。重复提交会返回 `timeout-or-duplicate`。如果用户提交失败后重试，前端要重新 `execute` 取新令牌。
- **给验证请求加超时**。`siteverify` 不可用时不要让整个登录流程挂死；并提前想好熔断策略——验证服务挂了是放行（可用性优先）还是拒绝（安全优先），不同业务答案不同。
- **reCAPTCHA 不是银弹**。它挡的是自动化脚本，挡不住人工打码平台。高价值接口（支付、领券）仍需要配合频率限制、设备指纹、行为分析等多层防护。
- **别忘了隐私合规**。页面使用了 reCAPTCHA，按 Google 的要求需要在站点上声明使用并链接其隐私政策。

# 总结

接入 reCAPTCHA 的核心流程就四步：管理后台注册密钥 → 前端加载脚本取令牌 → 表单携带令牌提交 → 后端调用 `siteverify` 验证。新项目优先选 v3，无打扰且能拿到量化的风险分；分数按 0.5 起步、分级处置，action 和 hostname 都要校验。国内站点记得把域名换成 `recaptcha.net`。整套接入一两个小时就能完成，但对垃圾注册和撞库的拦截效果是立竿见影的。

> 参考文档：
> - [reCAPTCHA v3 官方文档](https://developers.google.com/recaptcha/docs/v3)
> - [reCAPTCHA 管理后台](https://www.google.com/recaptcha/admin)
> - [siteverify 接口说明](https://developers.google.com/recaptcha/docs/verify)
> - [常见问题（含 recaptcha.net 镜像）](https://developers.google.com/recaptcha/docs/faq)
