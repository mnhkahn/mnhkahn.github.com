# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Jekyll blog** hosted on GitHub Pages at https://blog.cyeam.com. It contains technical articles about Go, backend development, and software engineering.

## Common Commands

```bash
# Install dependencies
bundle install

# Run local development server (Recommended)
bundle exec jekyll serve

# Or use the Rakefile convenience command
rake preview

# Create a new blog post
rake post title="Hello World" category="tech" tags="[tag1,tag2]"

# Create a new page
rake page name="about.html"
```

## Project Structure

- `_posts/` — Blog posts in markdown, naming format: `YYYY-MM-DD-title.md`
- `_layouts/` — Page templates
- `_includes/` — Reusable includes (themes, JB setup)
- `assets/` — Static assets (CSS, JS, images)
- `_config.yml` — Jekyll configuration

## Architecture

- **Markdown parser**: Kramdown with GFM support
- **Syntax highlighter**: Rouge
- **Pagination**: 10 posts per page
- **Comments**: Custom provider (Disqus)
- **Analytics**: Custom provider (Google Analytics)

## Workflow

1. Write posts in `_posts/` using markdown
2. Test locally with `bundle exec jekyll serve`
3. Push to master branch — GitHub Pages auto-deploys