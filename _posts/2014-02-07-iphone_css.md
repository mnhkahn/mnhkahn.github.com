---
layout: post
title: "iPhone的CSS显示"
description: "iPhone的CSS显示，费了我stackoverflow 6个声望问到的。。。"
category: "Kaleidoscope"
tags: ["CSS", "iPhone"]
---

###1. 通过给图片加CSS实现
<div class="iphone">
    <img src="https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeam/nexus7_screenshot.png" />
</div>

做这个是为了做cInterphone贴图片用的。代码很简单，只要给想加iPhone显示的CSS就行。调用代码如下：

	<div class="iphone">
	    <img src="https://res.cloudinary.com/cyeam/image/upload/v1537933530/cyeam/nexus7_screenshot.png" />
	</div>

一位大神提供的前端代码，我也懒得去读了，直接拿来用。以后有兴趣再去研究。CSS代码直接贴这里了：

	/* iPhone */
	/* First, we'll make the body. After that we'll use :after and :before elements to make other things like buttons */
	
	.iphone {
		position: relative;
		height: 495px;
		width: 250px;
		border-radius: 35px;
		margin: 50px auto;
		
		/* We are going to use multiple background images (linear-gradients) here to create the main background, the shine and the screen */
		/* This is our first gradient, to draw more, we'll have to write them before this one separated by a comma */
		/* Now, we'll draw the screen */
		/* The screen should be below the shine, right? */
		background: 
			linear-gradient(-165deg, rgba(255,255,255,0.4), rgba(255,255,255,0.15) 35%, transparent 35%),
			linear-gradient(top, transparent 85px, #222222 85px, #151515 410px, transparent 410px),
			linear-gradient(top, #000, #0a0a0a);
		
		/* Something isn't right... */
		/* Now, it's perfect. Try playing with the values below to get a better understanding */
		background-repeat: no-repeat;
		background-size: 100% 100%, 220px 100%, 100% 100%;
		background-position: 0 0, 15px 0, 0 0;
		
		
		
		/* Now we need the aluminium borders and the top button */
		/* We'll use box shadows for that */
		box-shadow: 0 0 0 3px black,
								/* A small divider */
								-40px -128px 0 -123px black,
								0 0 0 5px #a09f9d,
								/* Some metallic shine on the button */
								49px -130px 3px -123px #777,
								46px -130px 2px -123px #ddd,
								/* Top button from here */
								62px -111px 0 -105px #8e8d8b,
								62px -112px 0 -105px #b4b3b1,
								62px -113px 0 -105px #666;
	}
	
	
	/* Our phone's body is complete! Now we'll move onto the home button, front cam and the speaker.. */
	/* We are going to use :after pseudo element for that and a lot of box-shadow awesomeness */
	.iphone:after {
		content: '▢';
		line-height: 46px;
		text-align: center;
		font-size: 28px;
		color: #666;
		position: absolute;
		width: 46px;
		height: 46px;
		border-radius: 50%;
		background: white;
		bottom: 18px;
		left: 100px;
		border: 2px solid #0a0a0a;
		
		
		
		/* We'll use gradients for the depth */
		background-image:
			linear-gradient(left, rgba(0, 0, 0, 0.85), black); /* Looking good */
	
		/* Now some box-shadow magic to create speaker and front cam */
		box-shadow:
			/* Front Cam: looking good */
			-39px -410px 0 -23px #000f31,
			-39px -410px 0 -22px #0a1c5a,
			-40px -410px 0 -21px #0d1216,
			-40px -410px 0 -19px #1b191a,
			
			
		
			/* Speaker, it's a mess. Really. */ 
			/* now the outer covering of speaker, another mess */
			-12px -410px 0 -22px #333,
			-8px -410px 0 -22px #333,
			-4px -410px 0 -22px #333,
			-0px -410px 0 -22px #333,
			4px -410px 0 -22px #333,
			8px -410px 0 -22px #333,
			12px -410px 0 -22px #333,
			16px -410px 0 -22px #333,
			20px -410px 0 -22px #333,
			24px -410px 0 -22px #333,
			
			-12px -410px 0 -18px #0a0a0a,
			-9px -410px 0 -18px #0a0a0a,
			-6px -410px 0 -18px #0a0a0a,
			-3px -410px 0 -18px #0a0a0a,
			0px -410px 0 -18px #0a0a0a,
			3px -410px 0 -18px #0a0a0a,
			6px -410px 0 -18px #0a0a0a,
			9px -410px 0 -18px #0a0a0a,
			12px -410px 0 -18px #0a0a0a,
			15px -410px 0 -18px #0a0a0a,
			18px -410px 0 -18px #0a0a0a,
			21px -410px 0 -18px #0a0a0a,
			24px -410px 0 -18px #0a0a0a;
	
	}
	
	/* Looks good till now. But we are still missing the side buttons and those are pretty easy to make. We'll only use gradient for that ;) */
	.iphone:before {
		position: absolute;
		content: '';
		width: 2px;
		height: 117px;
		background: transparent;
		top: 40px;
		left: -7px;
		
		/* The shape is building up */
		background-image:
			/* This is going to be a long top to bottom linear gradient so see the output and code */
			/* A final touch ;) */
			linear-gradient(left, transparent 0px, transparent 1px, #7a7879 2px),
			linear-gradient(top, #383838 1px, #b9b9b9 3px, #b9b9b9 10px, #383838 19px, #b9b9b9 23px, transparent 23px, transparent 53px, #383838 53px, #b9b9b9 54px, #dadada 58px, #383838 62px, black 62px, black 66px, #383838 66px, #b9b9b9 67px, #dadada 68px, #383838 70px, transparent 70px, transparent 100px, #383838 100px, #b9b9b9 101px, #dadada 105px, #383838 109px, black 109px, black 113px, #383838 113px, #b9b9b9 114px, #dadada 115px, #383838 117px);
		
	}
	
	.iphone img {
		position: absolute;
		left: 6px;
		top: 65px;
	}


> http://cssdeck.com/labs/iphone_with_css3

###2. 通过嵌套DIV实现

今天无意间在百度Site App里看到的可以模拟Android的，iPhone和Android凑齐了，哈哈。

	.phone-bg {
	    margin-top: 10px;
	    padding-top: 60px;
	    background: url(http://siteapp.baidu.com/static/webappservice/pic/new-bg-mobile_dafd5fd.png) no-repeat 0 -10px;
	    height: 614px;
	    width: 332px;
	    margin-right: -10px;
	    position: relative;
	}
	.phone-bg .phone_display {
	    margin-left: 34px;
	    width: 272px;
	    height: 465px;
	    background-color: #fff;
	}

	<div class="phone-bg ">
	    <div class="phone_display"></div>
	</div>

这个显示需要加入额外的CSS。

<div class="phone-bg ">
    <div class="phone_display">
		效果效果
	</div>
</div>


{% include JB/setup %}