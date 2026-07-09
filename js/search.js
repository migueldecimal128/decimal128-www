/*
 * Client-side, no-backend search + filter for the knowledge base page.
 * Relies on the KB_DATA array defined in data/faq-data.js (loaded before
 * this file). Works fully offline / from a local file, no build step,
 * no server, no external libraries.
 */

(function () {
  "use strict";

  const searchInput = document.getElementById("kb-search-input");
  const categoryContainer = document.getElementById("kb-categories");
  const resultsContainer = document.getElementById("kb-results");
  const metaContainer = document.getElementById("kb-meta");

  if (!searchInput || !resultsContainer) {
    return;
  }

  const data = typeof KB_DATA !== "undefined" && Array.isArray(KB_DATA) ? KB_DATA : [];
  const categories = Array.from(new Set(data.map((entry) => entry.category))).sort();

  let activeCategory = "All";
  let query = "";

  function escapeHtml(str) {
    return str.replace(/[&<>"']/g, (ch) => {
      switch (ch) {
        case "&": return "&amp;";
        case "<": return "&lt;";
        case ">": return "&gt;";
        case '"': return "&quot;";
        default: return "&#39;";
      }
    });
  }

  function highlight(text, term) {
    const safe = escapeHtml(text);
    if (!term) return safe;
    const escapedTerm = term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const re = new RegExp("(" + escapedTerm + ")", "ig");
    return safe.replace(re, "<mark>$1</mark>");
  }

  function buildCategoryButtons() {
    const allBtn = document.createElement("button");
    allBtn.type = "button";
    allBtn.className = "kb-category-btn";
    allBtn.textContent = "All topics";
    allBtn.dataset.category = "All";
    allBtn.setAttribute("aria-pressed", "true");
    categoryContainer.appendChild(allBtn);

    categories.forEach((cat) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "kb-category-btn";
      btn.textContent = cat;
      btn.dataset.category = cat;
      btn.setAttribute("aria-pressed", "false");
      categoryContainer.appendChild(btn);
    });

    categoryContainer.addEventListener("click", (e) => {
      const btn = e.target.closest(".kb-category-btn");
      if (!btn) return;
      activeCategory = btn.dataset.category;
      categoryContainer.querySelectorAll(".kb-category-btn").forEach((b) => {
        b.setAttribute("aria-pressed", String(b === btn));
      });
      render();
    });
  }

  function matches(entry, term) {
    if (!term) return true;
    const haystack = (
      entry.question + " " + entry.answer + " " +
      (entry.list || []).join(" ") + " " + (entry.tags || []).join(" ")
    ).toLowerCase();
    return haystack.includes(term);
  }

  function render() {
    const term = query.trim().toLowerCase();
    const filtered = data.filter((entry) => {
      const categoryOk = activeCategory === "All" || entry.category === activeCategory;
      return categoryOk && matches(entry, term);
    });

    resultsContainer.innerHTML = "";

    if (metaContainer) {
      const countLabel = filtered.length === 1 ? "1 result" : filtered.length + " results";
      metaContainer.textContent = countLabel + (activeCategory !== "All" ? " in “" + activeCategory + "”" : "");
    }

    if (filtered.length === 0) {
      const empty = document.createElement("p");
      empty.className = "kb-no-results";
      empty.textContent = "No entries match your search. Try a different term or choose “All topics”.";
      resultsContainer.appendChild(empty);
      return;
    }

    filtered.forEach((entry) => {
      const details = document.createElement("details");
      details.className = "kb-entry";

      const summary = document.createElement("summary");
      summary.innerHTML = "<span>" + highlight(entry.question, term) + "</span>";
      details.appendChild(summary);

      const body = document.createElement("div");
      body.className = "kb-entry-body";

      const catLabel = document.createElement("span");
      catLabel.className = "kb-category-label";
      catLabel.textContent = entry.category;
      body.appendChild(catLabel);

      const answer = document.createElement("p");
      answer.innerHTML = highlight(entry.answer, term);
      body.appendChild(answer);

      if (entry.list && entry.list.length) {
        const list = document.createElement("ul");
        entry.list.forEach((item) => {
          const li = document.createElement("li");
          li.innerHTML = highlight(item, term);
          list.appendChild(li);
        });
        body.appendChild(list);
      }

      (entry.links || []).forEach((link) => {
        const linkPara = document.createElement("p");
        const linkEl = document.createElement("a");
        linkEl.href = link.url;
        linkEl.target = "_blank";
        linkEl.rel = "noopener";
        linkEl.textContent = link.text + " ↗";
        linkPara.appendChild(linkEl);
        body.appendChild(linkPara);
      });

      (entry.tags || []).forEach((tag) => {
        const tagEl = document.createElement("span");
        tagEl.className = "kb-tag";
        tagEl.textContent = tag;
        body.appendChild(tagEl);
      });

      details.appendChild(body);
      resultsContainer.appendChild(details);
    });
  }

  searchInput.addEventListener("input", (e) => {
    query = e.target.value;
    render();
  });

  buildCategoryButtons();
  render();
})();
