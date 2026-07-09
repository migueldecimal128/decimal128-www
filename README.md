# Decimal128 website

A plain HTML/CSS/JS static website — no build step, no framework, no backend.
Designed to be hosted for free on GitHub Pages.

## Structure

```
index.html            Home page
about.html             About page
knowledge-base.html    Searchable, categorised FAQ / knowledge base
css/style.css          All styling
js/search.js           Client-side search + category filter logic
data/faq-data.js       Knowledge base content (edit this to add/change entries)
.nojekyll               Tells GitHub Pages not to run Jekyll processing
```

## Editing content

- Organisation name and GitHub URLs are now set to Decimal128 /
  `https://github.com/abigail-128` across `index.html`, `about.html`, and
  `knowledge-base.html`.
- Edit the repository list in `about.html` (`<ul class="repo-list">`).
- Add, edit, or remove knowledge base entries in `data/faq-data.js`. Each
  entry is a plain object with `category`, `question`, `answer`, and `tags`.
  New categories appear as filter buttons automatically — no other code
  changes needed.

## About the search

The knowledge base search is entirely client-side JavaScript (`js/search.js`)
filtering the array in `data/faq-data.js`. There is no server, database, or
build step (deliberately avoiding tools like Pagefind, which need a Node.js
indexing step) — the content is just plain JavaScript loaded by the browser,
so it works immediately on GitHub Pages and even when opening `index.html`
directly from disk.

## Previewing locally

Because the data is embedded in a `<script>` tag rather than fetched, you can
just double-click `index.html` to open it in a browser — no local server
required. (If you later switch to `fetch()`-based JSON loading, you would
need a local server due to browser CORS rules for `file://` pages.)

## Deploying to GitHub Pages

1. Create a new **public** GitHub repository (Pages' free tier requires the
   repo to be public, unless you're on a paid GitHub plan).
2. Push these files to the repository, keeping `index.html` at the
   repository root.
3. In the repository, go to **Settings → Pages**.
4. Under "Build and deployment", set **Source** to "Deploy from a branch".
5. Choose the branch (e.g. `main`) and folder `/ (root)`, then click **Save**.
6. Wait a minute or two, then GitHub will show your live URL, typically:
   `https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/`
7. Revisit the site after making changes — GitHub Pages redeploys
   automatically a short while after every push to the chosen branch.

Optional: if you want a custom domain, add a `CNAME` file with your domain
name at the repository root and configure DNS as described in GitHub's
"Managing a custom domain for your GitHub Pages site" documentation.
