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
  urls: [
// 'https://www.cyeam.com/tool/ddl2gostruct',
// 'https://www.cyeam.com/tool/json2ddl',
 
    'https://www.cyeam.com/sitemap.xml',
   ],
  outputDir: './scan-results',
  timeout: 10000,
  headless: true,
  devicesToTest: [
    { name: 'Mobile-iPhone-15', preset: 'iPhone 15' },
    { name: 'Desktop-MacBook-Pro-16', preset: 'MacBook Pro 16' },
  ],
  maxSitemapUrls: 300,
  retryTimes: 3 // 重试次数
};

// --- 辅助函数：带重试的page.goto ---
const gotoWithRetry = async (page, url, options, maxRetries) => {
  let lastError;
  for (let retry = 1; retry <= maxRetries; retry++) {
    try {
      if (retry > 1) {
        console.log(`   🔄 重试(${retry}/${maxRetries})访问: ${url}`);
      }
      await page.goto(url, options);
      return; // 成功则直接返回
    } catch (error) {
      lastError = error;
      if (error.message.includes('Timeout') || error.message.includes('timeout')) {
        if (retry === maxRetries) {
          throw new Error(`[Retry Failed] 超过${maxRetries}次重试仍无法访问: ${url}，错误：${error.message}`);
        }
        await new Promise(resolve => setTimeout(resolve, 1000));
      } else {
        throw error;
      }
    }
  }
  throw lastError;
};

// --- 辅助函数：原生解析Sitemap ---
const fetchSitemapUrls = (sitemapUrl) => {
  return new Promise((resolve, reject) => {
    https.get(sitemapUrl, (res) => {
      let xml = '';
      // 1. 处理编码问题（避免chunk拼接乱码）
      res.setEncoding('utf8');
      
      res.on('data', (chunk) => xml += chunk);
      res.on('end', () => {
        try {
          // 2. 替换正则匹配方式：用matchAll（ES2020+），避免lastIndex陷阱
          const urlRegex = /<loc>(.*?)<\/loc>/g;
          // 兼容写法：如果环境不支持matchAll，用while循环+重置lastIndex
          const urls = [];
          let match;
          // 重置正则lastIndex，确保从头匹配
          urlRegex.lastIndex = 0;
          while ((match = urlRegex.exec(xml)) !== null) {
            if (match[1]) {
              urls.push(match[1].trim()); // 去除首尾空格，避免无效URL
            }
          }

          // 3. 优化域名过滤逻辑：匹配主域名（而非完整hostname）
          const baseUrlObj = new URL(sitemapUrl);
          // 提取主域名（如从www.cyeam.com提取cyeam.com）
          const baseDomain = baseUrlObj.hostname.split('.').slice(-2).join('.');
          
          const filteredUrls = urls.filter(url => {
            try {
              const urlObj = new URL(url);
              // 匹配主域名（支持所有子域名：www/blog/note/game.cyeam.com）
              const urlDomain = urlObj.hostname.split('.').slice(-2).join('.');
              return urlDomain === baseDomain;
            } catch (e) {
              console.warn('无效URL:', url, e.message);
              return false;
            }
          });

          // 4. 最终结果：按CONFIG截断（但先确保CONFIG值足够大）
          const result = filteredUrls.slice(0, CONFIG.maxSitemapUrls);
          console.log(`提取结果：总匹配${urls.length}个 → 过滤后${filteredUrls.length}个 → 最终${result.length}个`);
          resolve(result);
        } catch (e) {
          reject(new Error(`解析XML失败：${e.message}`));
        }
      });
    })
    // 处理请求错误（如超时、连接失败）
    .on('error', (err) => reject(new Error(`请求Sitemap失败：${err.message}`)))
    // 处理超时
    .setTimeout(10000, () => reject(new Error('请求Sitemap超时')));
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

    if (CONFIG.urls.length === 1 && CONFIG.urls[0].toLowerCase().includes('sitemap.xml')) {
      isSitemapMode = true;
      const sitemapUrl = CONFIG.urls[0];
      console.log(`🔍 检测到sitemap模式，正在解析: ${sitemapUrl}`);
      urls = await fetchSitemapUrls(sitemapUrl);
      console.log(`✅ 从sitemap解析出 ${urls.length} 个URL\n`);
    } else {
      urls = CONFIG.urls;
      console.log(`📋 使用手动配置的URL列表，共 ${urls.length} 个URL\n`);
    }

    if (urls.length === 0) {
      console.log('❌ 未找到可检测的URL，请检查配置！');
      return;
    }

    for (const deviceConfig of CONFIG.devicesToTest) {
      console.log(`\n========== 正在测试设备: ${deviceConfig.name} ==========`);
      const { dir, shotDir } = initDirs(deviceConfig.name);
      const results = [];

      const browser = await chromium.launch({ headless: CONFIG.headless });
      
      let context;
      if (deviceConfig.preset) {
        const device = devices[deviceConfig.preset];
        context = await browser.newContext({ ...device });
      } else {
        context = await browser.newContext({ viewport: deviceConfig.viewport });
      }

      const page = await context.newPage();

      for (const url of urls) {
        // 1. 初始化结果对象，新增timeCost字段
        const pageResult = { url, errors: [], screenshot: null, timeCost: 0 };
        const safeFilename = url.replace(/[^a-zA-Z0-9]/g, '_');
        
        // 2. 记录访问开始时间（毫秒级）
        const startTime = Date.now();

        try {
          page.on('pageerror', err => pageResult.errors.push(`[JS] ${err.message}`));
          
          // 访问页面（包含重试逻辑）
          await gotoWithRetry(page, url, { waitUntil: 'load', timeout: CONFIG.timeout }, CONFIG.retryTimes);

          // 检查横向滚动条
          const hasHorizontalScroll = await page.evaluate(() => {
            return document.documentElement.scrollWidth > document.documentElement.clientWidth;
          });
          if (hasHorizontalScroll) {
            pageResult.errors.push('[Layout] 检测到横向滚动条，内容溢出屏幕');
          }

          // 检查裂图
          const brokenImages = await page.evaluate(() => {
            const imgs = Array.from(document.images);
            return imgs
              .filter(img => !img.alt.includes('大图预览'))
              .filter(img => img.naturalWidth === 0)
              .map(img => {
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
        } finally {
          // 3. 计算总耗时（无论成功/失败，都会执行）
          pageResult.timeCost = Date.now() - startTime;
        }

        results.push(pageResult);
        
        // 4. 控制台输出时展示耗时
        if (pageResult.errors.length > 0) {
          console.log(`❌ ${url} (耗时: ${pageResult.timeCost}ms)`);
          pageResult.errors.forEach(err => console.log(`   - ${err}`));
        } else {
          console.log(`✅ ${url} (耗时: ${pageResult.timeCost}ms)`);
        }
      }

      // 保存检测报告（包含耗时字段）
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
