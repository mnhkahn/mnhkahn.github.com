---
layout: page
title: Cyeam
tagline: 码到功成
---
{% include JB/setup %}

{% for post in site.posts %}
<h2>
    <a id="{{post.title}}">{{post.title}}</a>
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
<br>
---
{% endfor %}