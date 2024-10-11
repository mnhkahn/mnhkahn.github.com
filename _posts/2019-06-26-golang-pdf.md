---
layout: post
title: "使用 Golang 生成 PDF"
description: "Go 作为年轻的语言对于 PDF 这种特殊的需求支持还是弱一些，调研了一番，记录在这里"
figure: "https://res.cloudinary.com/cyeam/image/upload/v1591587886/cyeam/pdf_pixabay_1493877090501.jpg"
category: "Go"
tags: ["go","pdf"]
---

* 目录
{:toc}
---

这是一个例子，可以先感受下：[口算大通关](https://www.cyeam.com/tool/arithmetic?utm_source=blog)。

### gofpdf

仓库：[https://github.com/jung-kurt/gofpdf](https://github.com/jung-kurt/gofpdf)

一开始就发现了这个包，纯 Go 实现，用起来很友好。

举几个简单的样例：

##### 加载字体
```
pdf.AddUTF8Font("NotoSansSC", "", "./resource/font/NotoSansSC-Regular.ttf")
```
##### 绘制矩形并填充颜色
```
pdf.SetFillColor(0, 0, 0)
pdf.Rect(30, 0, 26.5, 14, "FD")
```
##### 写字
```
pdf.Text(32, 9, "字字字")
// 多行文字，根据宽度自动换行
func TextMultiLine(pdf *gofpdf.Fpdf, text string, x, y, width, heightPerLine float64) {
	texts := pdf.SplitText(text, width)

	i := 0
	for _, text := range texts {
		_y := y + (heightPerLine * float64(i))
		pdf.Text(x, _y, text)
		i++
	}
}
```
##### 增加图片
```
pdf.Image("./resource/image/logo.jpeg", 2, 1.5, 26, 10, false, "", 0, "")
```
##### 简单的svg
```
sig, err = gofpdf.SVGBasicParse(templateStr)
if err == nil {
	scale := 100 / sig.Wd
	scaleY := 113 / sig.Ht
	if scale > scaleY {
		scale = scaleY
	}
	pdf.SetLineWidth(0.25)
	pdf.SetDrawColor(0, 0, 0)
	pdf.SetXY(0, 0)
	pdf.SVGBasicWrite(&sig, scale)
} else {
	pdf.SetError(err)
}
```
##### 条形码、二维码

```
key = barcode.RegisterCode128(pdf, "barcode")
width = 55
height = 6.7
barcode.BarcodeUnscalable(pdf, key, 39, 110.5, &width, &height, false)
```

##### 简单的 HTML
```
htmlStr := `You can now easily print text mixing different styles: <b>bold</b>, ` +
	`<i>italic</i>, <u>underlined</u>, or <b><i><u>all at once</u></i></b>!<br><br>` +
	`<center>You can also center text.</center>` +
	`<right>Or align it to the right.</right>` +
	`You can also insert links on text, such as ` +
	`<a href="http://www.fpdf.org">www.fpdf.org</a>, or on an image: click on the logo.`
html := pdf.HTMLBasicNew()
html.Write(lineHt, htmlStr)
```

##### 居中
```
pdf.SetXY(40, 117.8)
pdf.CellFormat(60, 2, "center", "", 0,
	"CM", false, 0, "")
```



优势：

1. 纯 Go 实现，使用方便；
2. 性能好 `BenchmarkSvg-4    100      15806543 ns/op`；
3. 支持格式多，除了上面的例子，还支持根据简单 HTML 绘制 PDF；
4. 非常完善的样例，`fpdf_test.go`里面有所有接口的生成样例，可以直接看效果；

缺陷：

1. svg 支持的比较简单。只支持最外层是path，path内只支持d，其他的比如坐标转换都不支持。其实大部分svg都是包含坐标转换的，这个不太友好。可以通过[Method-Draw](https://github.com/methodofaction/Method-Draw)将svg简化压缩一下。
2. html 支持的比较简单。上面的例子写得比较明白了，支持居中、加粗、超链接这种。


### wkhtmltopdf

网上经常能找到在线html转pdf的在线小工具，其实都是基于c语言的实现wkhtmltopdf做的。这个工具功能很强大，甚至可以解析`<script>`引入的jQuery外网包。Go 语言是通过cgo bind实现的包，[https://github.com/adrg/go-wkhtmltopdf](https://github.com/adrg/go-wkhtmltopdf)，功能非常强大，缺点是生成得太慢。


---


{% include JB/setup %}
