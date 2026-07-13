---
layout: default
permalink: /qa.html
title: "Q&A — Decimal128"
description: "Search frequently asked questions about Decimal128, organised by topic. No account or sign-up needed."
heading: "Q&A"
extra_js:
  - js/faq-data.js
  - js/search.js
---

<div class="kb-controls">
  <div class="kb-search-field">
    <label class="visually-hidden" for="kb-search-input">Search the knowledge base</label>
    <input
      type="search"
      id="kb-search-input"
      placeholder="Search questions, answers, or tags…"
      autocomplete="off"
    >
  </div>
  <div class="kb-categories" id="kb-categories" role="group" aria-label="Filter by category">
    <!-- Category buttons are generated automatically by js/search.js -->
  </div>
</div>

<p class="kb-meta" id="kb-meta" aria-live="polite"></p>

<div class="kb-results" id="kb-results" aria-live="polite">
  <!-- Results are generated automatically by js/search.js -->
</div>
