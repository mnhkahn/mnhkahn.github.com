---
layout: page
title: Cyeam
tagline: Done is Better Than Perfect
---
{% include JB/setup %}

{% for post in site.posts %}
##{{post.title}}
{{post.date|date: "%Y-%m-%d"}}   
{{post.description}}[阅读全文]({{post.url}})
{% if post.figure %}
<a href="{{post.url}}">
    <img src="{{post.figure}}" alt="IMG-THUMBNAIL" />
</a>
{% endif %}
<br>
---
{% endfor %}