---
layout: default
title: Home
---

# {{ site.title }}

{{ site.description }}

Each criterion below has its own page with expected behavior, pass/fail criteria, and a reference — plus a discussion thread where anyone can comment or propose a change to the standard.

{% for category in site.data.categories %}
  {% assign items = site.criteria | where: "category", category | sort: "order" %}
  <h2 id="{{ category | slugify }}">{{ category }}</h2>
  <ul>
    {% for item in items %}
      <li><a href="{{ item.url | relative_url }}">{{ item.title }}</a></li>
    {% endfor %}
  </ul>
{% endfor %}
