# Decimal128 website

A Jekyll site — page content lives in plain Markdown files so it's easy to
edit without knowing HTML, CSS, or JavaScript. GitHub Pages builds Jekyll
sites automatically; there is no local build step required to publish.

## Structure

```
index.md                    Home page content (Markdown) — includes what used to be the About page
qa.md                         Q&A page (mostly a shell — see below)
business-case.md                Business Case page content (Markdown)
benchmarks.md                  Benchmarks page content (Markdown)
whitepapers.md                 Whitepapers page content (Markdown)
_data/faqs.yml                Q&A questions/answers — edit this file
_layouts/default.html         Shared page shell: nav bar, header, footer (HTML)
css/style.css                 All styling (HTML/CSS)
js/search.js                  Client-side search + category filter logic (JS)
js/faq-data.js                Auto-generated from _data/faqs.yml at build time — don't edit
_config.yml                    Site title/tagline and Jekyll settings
```

## Editing content (no HTML needed)

- **Page text** — edit `index.md`, `business-case.md`, `benchmarks.md`, or
  `whitepapers.md` directly. These are plain Markdown: blank line
  between paragraphs, `## Heading` for a section heading, `- item` for a
  bulleted list, `[link text](https://...)` for a link, `**bold**` for
  bold text.
- **Q&A questions** — edit `_data/faqs.yml`. Copy an existing entry and
  change the `question`/`answer`/`category`. New `category` values
  automatically get their own filter button *and* their own group in the
  Table of Contents at the top of the Q&A page — no other changes needed.
  Each entry's `id` must stay unique — it's used to build the "jump to this
  question" links in the Table of Contents, so don't reuse an `id` from
  another entry. Optional fields:
  - `tags`: a few keywords to help search match this entry
  - `list`: a bulleted list of points shown under the answer
  - `links`: a list of `{ text, url }` shown as clickable links under the answer
- **Adding a brand new page** — create a new `.md` file at the repository
  root with front matter like the other pages (`layout: default`,
  `permalink`, `title`, `description`, `heading`), then add a matching
  `<li>` link to it in the nav list in `_layouts/default.html`.
- **Nav bar, header, footer, and overall look** — these live in
  `_layouts/default.html` and `css/style.css`. This part is meant to be
  maintained by someone comfortable with HTML/CSS; everyday content edits
  never need to touch it.

## About the search

The Q&A search is entirely client-side JavaScript (`js/search.js`).
`js/faq-data.js` is generated automatically by Jekyll from `_data/faqs.yml`
every time the site builds — GitHub Pages does this on every push, so
editing `_data/faqs.yml` and pushing is all that's needed to update the
Q&A page. There is no server, database, or separate indexing step
(deliberately avoiding tools like Pagefind, which need their own Node.js
build step).

## Previewing locally

This repo has no local Ruby/Jekyll installed in the environment it was
built in, so changes were verified by pushing to a branch and checking
GitHub's live build. If you have Ruby and Bundler installed locally, you
can preview changes before pushing:

```
gem install bundler jekyll
bundle init
bundle add jekyll
bundle exec jekyll serve
```

Then open `http://localhost:4000/` in a browser.

## Deploying to GitHub Pages

1. Push changes to the repository's default branch (`main`).
2. In the repository, go to **Settings → Pages** and confirm **Source** is
   set to "Deploy from a branch", with branch `main` and folder `/ (root)`.
   GitHub detects `_config.yml` and runs Jekyll automatically — no
   `.nojekyll` file and no GitHub Actions workflow needed.
3. Wait a minute or two after each push; GitHub Pages rebuilds and
   redeploys automatically.

Optional: if you want a custom domain, add a `CNAME` file with your domain
name at the repository root and configure DNS as described in GitHub's
"Managing a custom domain for your GitHub Pages site" documentation.
