---
---
/*
 * Auto-generated at build time by Jekyll from _data/faqs.yml — do not edit
 * this file directly. To change knowledge base content, edit
 * _data/faqs.yml instead.
 */
const KB_DATA = [
{% for faq in site.data.faqs %}
  {
    id: {{ faq.id | jsonify }},
    category: {{ faq.category | jsonify }},
    question: {{ faq.question | jsonify }},
    answer: {{ faq.answer | jsonify }}{% if faq.list %},
    list: {{ faq.list | jsonify }}{% endif %}{% if faq.links %},
    links: {{ faq.links | jsonify }}{% endif %},
    tags: {{ faq.tags | jsonify }}
  }{% unless forloop.last %},{% endunless %}
{% endfor %}
];
