# AGENTS.md

## Project Overview
这是一个基于Jekyll的个人博客项目，主要用于分享技术文章、学习心得和开发经验。项目使用Markdown格式编写文章，通过Jekyll静态站点生成器构建。

## Build & Commands

### 安装依赖
```bash
bundle install
```

### 本地开发服务器
```bash
bundle exec jekyll serve
# 访问 http://localhost:4000
```

### 构建静态站点
```bash
bundle exec jekyll build
# 生成的静态文件在 _site 目录
```

### 检查链接
```bash
bundle exec htmlproofer ./_site
```

## Code Style

### Markdown 格式
- 使用标准Markdown语法
- 标题层级清晰（#, ##, ### 等）
- 代码块使用三个反引号并指定语言
- 图片使用相对路径或CDN链接

### 文章结构
- 每个文章包含YAML前置元数据（layout, title, description, category, tags等）
- 文章存放在 _posts 目录，命名格式为 YYYY-MM-DD-title.md
- 图片资源建议使用外部CDN存储

## Testing

### 本地预览
- 使用 `bundle exec jekyll serve` 启动本地服务器
- 检查文章渲染效果和链接是否正常

### 链接检查
- 使用 `htmlproofer` 检查站点中的死链接

## Security

### 敏感信息
- 不要在代码中硬编码API密钥、密码等敏感信息
- 使用环境变量或配置文件管理敏感配置

### 依赖安全
- 定期更新Gemfile中的依赖包
- 检查依赖包的安全漏洞

## Configuration

### 主要配置文件
- `_config.yml`：Jekyll站点配置
- `Gemfile`：Ruby依赖管理
- `_includes/`：布局组件
- `_layouts/`：页面布局模板

### 环境变量
- 开发环境：使用默认配置
- 生产环境：可通过环境变量覆盖配置