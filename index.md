---
layout: page
title: Cyeam
tagline: 你不要用战术的勤奋掩盖战略的懒惰。 
---
{% include JB/setup %}

{% for post in site.posts %}
	{% if forloop.index == 10 %}
		{% break %}
	{% endif %}
<div class="cyeam_post">
    <h2>
        <a id="{{post.title}}" href="{{post.url}}" target="_blank">
            {{post.title}}
        </a>
    </h2>
    <p class="date">
        <span class="icon-calendar">
        </span>
        {{post.date|date: "%Y-%m-%d"}}
    </p>
    <p class="description">{{post.description}}</p>

    <p class="read-all">
        <a href="{{post.url}}" target="_blank">
            <span class="icon-resize-full">
            </span>
            阅读全文
        </a>
    </p>
    {% if post.figure %}
    <p class="figure center">
        <a href="{{post.url}}" target="_blank">
            <img src="{{post.figure}}" alt="IMG-THUMBNAIL"/>
        </a>
    </p>
    {% endif %}
</div>
<br>
---
{% endfor %}

<center>
<a class="btn btn-large btn-primary" type="button" href="/all.html" target="_blank">全部文章</a>
</center>