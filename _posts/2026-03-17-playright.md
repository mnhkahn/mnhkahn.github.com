---
layout: post
title: "用Playwright扫描渲染问题"
description: "如何扫描整个站点，查找渲染问题？"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1773741757/68149f0271ec27bc6d3118eb_1_gMiUPuRGC36nxZHe2zthOg.png.png"
category: "CSS"
tags: ["CSS", "Tool", "Mobile"]
---

- 目录
{:toc}

---

按照依赖包：

```
npm install playwright --save
npx playwright install
```

保存下面的脚本，用命令`node scan.js`运行即可。

```node
const { chromium, devices } = require('playwright');
const https = require('https');
const fs = require('fs');
const path = require('path');

// --- 配置区域 ---
const CONFIG = {
  // 两种模式自动切换：
  // 1. 仅填1个sitemap.xml地址 → 自动解析sitemap
  // 2. 填多个URL/非sitemap地址 → 直接使用配置的URL列表
  urls: [
    // 示例1: sitemap模式 (仅保留这一行)
    'https://www.cyeam.com/sitemap.xml',
    
    // 示例2: 手动URL模式 (保留多个URL)
    // 'https://www.cyeam.com/',
    // 'https://www.cyeam.com/tool/pixel',
    // 'https://www.cyeam.com/baby/chaizi/onegrade2nd',
    // 'https://www.cyeam.com/geek',
    // 'https://blog.cyeam.com/css/2026/03/16/overflow'
  ],
  outputDir: './scan-results',
  timeout: 30000,
  headless: true,
  // 定义要测试的设备列表
  devicesToTest: [
    { name: 'Desktop-1080p', viewport: { width: 1920, height: 1080 } },
    { name: 'Mobile-iPhone-15', preset: 'iPhone 15' }
  ],
  maxSitemapUrls: 50 // sitemap模式下最多解析的URL数量（可调整）
};

// --- 辅助函数：原生解析Sitemap ---
const fetchSitemapUrls = (sitemapUrl) => {
  return new Promise((resolve, reject) => {
    https.get(sitemapUrl, (res) => {
      let xml = '';
      res.on('data', (chunk) => xml += chunk);
      res.on('end', () => {
        const urlRegex = /<loc>(.*?)<\/loc>/g;
        const urls = [];
        let match;
        while ((match = urlRegex.exec(xml)) !== null) {
          urls.push(match[1]);
        }
        // 过滤掉非当前域名的URL，只保留同域名
        const baseDomain = new URL(sitemapUrl).hostname;
        const filteredUrls = urls.filter(url => {
          try {
            return new URL(url).hostname === baseDomain;
          } catch (e) {
            return false;
          }
        });
        // 限制最大数量
        resolve(filteredUrls.slice(0, CONFIG.maxSitemapUrls));
      });
    }).on('error', reject);
  });
};

// --- 辅助函数：初始化目录 ---
const initDirs = (deviceName) => {
  const dir = path.join(CONFIG.outputDir, deviceName);
  const shotDir = path.join(dir, 'screenshots');
  if (!fs.existsSync(shotDir)) fs.mkdirSync(shotDir, { recursive: true });
  return { dir, shotDir };
};

// --- 核心逻辑 ---
(async () => {
  try {
    let urls = [];
    let isSitemapMode = false;

    // 自动判断模式：仅1个URL且是sitemap.xml → sitemap模式
    if (CONFIG.urls.length === 1 && CONFIG.urls[0].toLowerCase().includes('sitemap.xml')) {
      isSitemapMode = true;
      const sitemapUrl = CONFIG.urls[0];
      console.log(`🔍 检测到sitemap模式，正在解析: ${sitemapUrl}`);
      urls = await fetchSitemapUrls(sitemapUrl);
      console.log(`✅ 从sitemap解析出 ${urls.length} 个URL\n`);
    } else {
      // 手动URL模式
      urls = CONFIG.urls;
      console.log(`📋 使用手动配置的URL列表，共 ${urls.length} 个URL\n`);
    }

    if (urls.length === 0) {
      console.log('❌ 未找到可检测的URL，请检查配置！');
      return;
    }

    // 遍历测试设备
    for (const deviceConfig of CONFIG.devicesToTest) {
      console.log(`\n========== 正在测试设备: ${deviceConfig.name} ==========`);
      const { dir, shotDir } = initDirs(deviceConfig.name);
      const results = [];

      // 启动浏览器
      const browser = await chromium.launch({ headless: CONFIG.headless });
      
      let context;
      if (deviceConfig.preset) {
        const device = devices[deviceConfig.preset];
        context = await browser.newContext({ ...device });
      } else {
        context = await browser.newContext({ viewport: deviceConfig.viewport });
      }

      const page = await context.newPage();

      // 遍历每个URL检测
      for (const url of urls) {
        const pageResult = { url, errors: [], screenshot: null };
        const safeFilename = url.replace(/[^a-zA-Z0-9]/g, '_');

        try {
          // 监听JS错误
          page.on('pageerror', err => pageResult.errors.push(`[JS] ${err.message}`));
          
          // 访问页面
          await page.goto(url, { waitUntil: 'networkidle', timeout: CONFIG.timeout });

          // 检查1: 横向滚动条（布局溢出）
          const hasHorizontalScroll = await page.evaluate(() => {
            return document.documentElement.scrollWidth > document.documentElement.clientWidth;
          });
          if (hasHorizontalScroll) {
            pageResult.errors.push('[Layout] 检测到横向滚动条，内容溢出屏幕');
          }

          // 检查2: 裂图检测（跳过大图预览的viewer图片）
          const brokenImages = await page.evaluate(() => {
            const imgs = Array.from(document.images);
            return imgs
              .filter(img => !img.alt.includes('大图预览')) // 跳过viewer图片
              .filter(img => img.naturalWidth === 0) // 筛选裂图
              .map(img => {
                // 生成XPath定位
                const getXPath = (element) => {
                  if (element.id !== '') return `//*[@id="${element.id}"]`;
                  if (element === document.body) return '/html/body';
                  
                  let ix = 0;
                  const siblings = element.parentNode.childNodes;
                  for (let i = 0; i < siblings.length; i++) {
                    const sibling = siblings[i];
                    if (sibling === element) return `${getXPath(element.parentNode)}/${element.tagName.toLowerCase()}[${ix + 1}]`;
                    if (sibling.nodeType === 1 && sibling.tagName === element.tagName) ix++;
                  }
                  return getXPath(element.parentNode);
                };

                return {
                  src: img.src,
                  alt: img.alt,
                  html: img.outerHTML,
                  xpath: getXPath(img)
                };
              });
          });

          // 记录裂图详情
          if (brokenImages.length > 0) {
            for (const brokenImg of brokenImages) {
              const errMsg = `[Layout] 裂图详情：
                - 链接: ${brokenImg.src}
                - Alt文本: ${brokenImg.alt || '无'}
                - HTML代码: ${brokenImg.html}
                - XPath路径: ${brokenImg.xpath}`;
              pageResult.errors.push(errMsg);
            }
          }

          // 截图保存
          const screenshotPath = path.join(deviceConfig.name, 'screenshots', `${safeFilename}.png`);
          await page.screenshot({ path: path.join(CONFIG.outputDir, screenshotPath), fullPage: true });
          pageResult.screenshot = screenshotPath;

        } catch (e) {
          pageResult.errors.push(`[Critical] ${e.message}`);
        }

        results.push(pageResult);
        
        // 控制台输出结果（带错误明细）
        if (pageResult.errors.length > 0) {
          console.log(`❌ ${url}`);
          pageResult.errors.forEach(err => console.log(`   - ${err}`));
        } else {
          console.log(`✅ ${url}`);
        }
      }

      // 保存检测报告
      fs.writeFileSync(path.join(dir, 'report.json'), JSON.stringify(results, null, 2));
      await browser.close();
    }

    console.log(`\n🎉 扫描完成！结果已保存至: ${path.resolve(CONFIG.outputDir)}`);
  } catch (error) {
    console.error('💥 运行出错:', error);
  }
})();
```

{% include JB/setup %}
