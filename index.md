---
layout: page
title: Cyeam
tagline: 谁人没试过犹豫，达到理想不太易。
---
{% include JB/setup %}

<script>
  (function() {
    var cx = 'partner-pub-1651120361108148:7762571300';
    var gcse = document.createElement('script');
    gcse.type = 'text/javascript';
    gcse.async = true;
    gcse.src = 'https://cse.google.com/cse.js?cx=' + cx;
    var s = document.getElementsByTagName('script')[0];
    s.parentNode.insertBefore(gcse, s);
  })();
</script>
<gcse:searchbox-only></gcse:searchbox-only>

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
