# Setup (≈10 min, once)

## 1. Swap the site (same address: https://renstonferns.github.io/)
1. Open https://github.com/renstonferns/renstonferns.github.io and press the `.` key. This opens the repo in an online editor (github.dev).
2. Select everything in the file list on the left (click the first item, then Shift-click the last), right-click and choose **Delete**. Expand `.github/workflows` and delete the files inside it too.
3. Unzip this file on your computer, then drag all of its contents (including the hidden `.github` folder and `.nojekyll`) into the github.dev file list.
4. Open Source Control (the branch icon on the left), type a message such as "New site", and press **Commit & Push**.
5. Settings → Pages → Source should already say **GitHub Actions**. Leave it.

About a minute later, the Actions tab shows "Deploy website to GitHub Pages" go green, and the new site is live at the same address.

## 2. Turn on auto-updates
1. Settings → Actions → General → Workflow permissions → **Read and write** → Save.
2. Actions tab → "Auto-update site data" → **Run workflow** (tick "Also refresh Google Scholar now" the first time). It then runs every 3 hours by itself.

From then on, these update with no work from you:
- **New papers**: anything linked to your ORCID or found by OpenAlex appears with a "New" tag for 60 days.
- **Citations & h-index**: from Google Scholar once `SERPAPI_KEY` is set (step 2b), with OpenAlex as a fallback.
- **Preprint → journal**: once the journal version lands, the SSRN version is dropped automatically.
- **Peer-review count + journals**: from your ORCID peer-review section.

## 2b. Google Scholar (2 min, free)
Google Scholar has no official API and blocks robots, so the site reads it through SerpAPI.
1. Sign up free at serpapi.com. The free plan gives 100 lookups a month, and the site uses one a day.
2. Copy your API key from the dashboard.
3. In the repo, go to Settings → Secrets and variables → Actions → New secret: name `SERPAPI_KEY`, value = the key.

From then on, total citations, h-index, per-paper citations, and any new paper that appears on your Scholar profile update daily.

**How often each source updates:**
- **ORCID** (reviews and papers): every 3 hours.
- **OpenAlex**: every 3 hours.
- **Instagram**: every 3 hours.
- **Google Scholar**: once a day.

## 3. Peer reviews → ORCID (once)
At webofscience.com go to Profile → Peer review → Settings, and turn on **export to ORCID**. Then, for each review, forward the journal's thank-you email to `reviews@webofscience.com`. It lands in ORCID, and the site shows it the next day. Reviews you can't verify go in `data/manual.json` → `reviews_not_on_orcid`.

## 4. Instagram (optional, automatic)
1. Switch the account to **Professional** (Creator is free; it's in the IG app settings).
2. At developers.facebook.com, create an app → add **Instagram API with Instagram Login** → generate a long-lived token for your account.
3. In the repo, go to Settings → Secrets → Actions → New secret: name `IG_TOKEN`, value = the token.

The daily run keeps the token refreshed. Your latest 6 posts and their images show under "Latest".

## 5. LinkedIn / X posts
LinkedIn and X don't let personal accounts pull their posts automatically (X's API is paid). Instead, add a post in `data/manual.json` → `posts`. On your phone, the GitHub app lets you edit that file in 20 seconds, and the post is live a minute later. Blogs, Substack and YouTube can be added as RSS feeds in `data/config.json`, and those update automatically.

## Editing text
All the words on the site (bio, vision, experience, education, toolkit, links) are in `data/profile.json`.

## What's carried over from your old site
Your photo, bio, typewriter lines, research areas, research vision, teaching statement, paper blurbs, experience and education (with bullet points), awards, languages, interests, toolkit logos, contact text, CV, blog post (`blog/why-circular-carbon-efuels-matter/`) and seminar talk all come from the Hugo repo. They now live in `data/profile.json` and `data/manual.json`.

- **Stats**: citations, h-index and reviews come straight from Google Scholar and ORCID. `data/manual.json` → `stats` now only holds the publications floor (12+) and talks (20+).
- **New paper appears automatically** → add a one-line blurb for it in `manual.json` → `blurbs` (keyed by DOI), if you want one.
- **New talk** → add it to `manual.json` → `posts` with `"platform": "talk"`.

## 6. Get it on Google for your name
Already done in the site:
- **Page title**: "Dr. Renston Jake Fernandes | Clean Fuels, LCA, TEA & E-Fuels".
- **Structured data**: Person schema listing your name variants, KAUST, photo, and links to Scholar, ORCID, LinkedIn and ResearchGate. This tells Google they're all the same person.
- **Crawler files**: `sitemap.xml` and `robots.txt`.
- **Google verification file**: `google6a54829eb01374c4.html`, carried over so your existing Search Console ownership keeps working.

You do (once):
1. Go to https://search.google.com/search-console and open the `renstonferns.github.io` property.
2. **Sitemaps** → submit `sitemap.xml`.
3. **URL inspection** → paste `https://renstonferns.github.io/` → **Request indexing**.
4. Put the site URL in the "Homepage" field of your Google Scholar profile, your ORCID "Websites" section, your LinkedIn contact info and your Instagram bio. Links from those high-authority pages are the strongest signal that this is your official site.

Google usually picks up the new version within a few days to two weeks.

## Pages
The site is split into pages: `/`, `/research/`, `/publications/`, `/talks/`, `/music/`, `/experience/` and `/contact/`.
- **Layout:** lives in `scripts/page.html`. Sections are wrapped in `<!--@pages ...-->` blocks that say which pages they appear on.
- **Content:** lives in `data/*.json`, the same as before.
- **Building:** `scripts/build_pages.py` generates every page and the sitemap, and the deploy runs it automatically. Don't edit the generated `index.html` files directly.
