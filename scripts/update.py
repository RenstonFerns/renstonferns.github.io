#!/usr/bin/env python3
"""Daily site refresh. Run by .github/workflows/update.yml.

Writes:
  data/pubs.json     publications (ORCID + OpenAlex) with citations, first-author flag, "added" date
  data/reviews.json  peer-review count + journals (ORCID peer-review section)
  data/social.json   latest Instagram posts (needs IG_TOKEN secret) + RSS/Atom items

Every source is optional: if one fails, its previous file is kept.
"""
import json, os, re, sys, datetime as dt, urllib.request, urllib.parse, xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CFG = json.loads((DATA / "config.json").read_text())
MAN = json.loads((DATA / "manual.json").read_text())
ORCID = CFG["orcid"]
EMAIL = CFG.get("contact_email_for_apis", "")
NAMES = [n.lower() for n in CFG.get("name_variants", ["fernandes"])]
NOW = dt.datetime.now(dt.timezone.utc)
TODAY = NOW.date().isoformat()
UA = f"personal-site-updater (mailto:{EMAIL})"


def get(url, accept="application/json", raw=False):
    req = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        body = r.read()
    return body if raw else json.loads(body)


def load(name, default):
    p = DATA / name
    return json.loads(p.read_text()) if p.exists() else default


def save(name, obj):
    (DATA / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n")


def norm_doi(d):
    if not d:
        return ""
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", d.strip(), flags=re.I).lower()


def norm_title(t):
    t = (t or "").translate(str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789"))
    return re.sub(r"[^a-z0-9]", "", t.lower())[:70]


def is_me(name):
    n = (name or "").lower()
    return any(v in n for v in NAMES)


def short(name):
    """'Renston Jake Fernandes' -> 'R. J. Fernandes'"""
    parts = (name or "").replace(".", " ").split()
    if len(parts) < 2:
        return name or ""
    return " ".join(p[0].upper() + "." for p in parts[:-1]) + " " + parts[-1]


def kind(oa_type, venue):
    v = (venue or "").lower()
    if oa_type in ("book-chapter", "book"):
        return "chapter"
    if oa_type in ("dissertation",):
        return "thesis"
    if oa_type == "preprint" or "ssrn" in v or "arxiv" in v:
        return "preprint"
    if any(k in v for k in ("sae technical paper", "proceedings", "conference", "procedia", "icef", "congress")):
        return "conference"
    return "journal"


# ---------------------------------------------------------------- google scholar
def scholar_profile(old):
    """Google Scholar has no public API; SerpAPI's free plan (100 calls/month) covers one call a day.
    Skipped (keeping the last numbers) when SERPAPI_KEY is not set or the last fetch is under 20 h old."""
    key = os.environ.get("SERPAPI_KEY")
    sid = CFG.get("scholar_id")
    if not key or not sid:
        return None
    last = old.get("scholar_fetched")
    if last and os.environ.get("FORCE_SCHOLAR") != "1":
        try:
            if (NOW - dt.datetime.fromisoformat(last)).total_seconds() < 20 * 3600:
                return None
        except Exception:
            pass
    try:
        arts, start = [], 0
        while True:
            q = urllib.parse.urlencode({"engine": "google_scholar_author", "author_id": sid, "hl": "en",
                                        "num": 100, "start": start, "api_key": key})
            d = get("https://serpapi.com/search.json?" + q)
            for a in d.get("articles", []):
                arts.append({"title": a.get("title", ""), "authors": a.get("authors"), "publication": a.get("publication"),
                             "year": a.get("year"), "link": a.get("link"),
                             "cites": ((a.get("cited_by") or {}).get("value")) or 0})
            if start == 0:
                tbl = (d.get("cited_by") or {}).get("table", [])
                pick = lambda name: next((r[name]["all"] for r in tbl if name in r), None)
                totals = {"citations": pick("citations"), "h_index": pick("h_index"), "i10_index": pick("i10_index")}
            if len(d.get("articles", [])) < 100:
                break
            start += 100
        print(f"scholar: {len(arts)} articles, {totals}")
        return {"articles": arts, "totals": totals, "fetched": NOW.isoformat()}
    except Exception as e:
        print("Scholar skipped:", e, file=sys.stderr)
        return None


# ---------------------------------------------------------------- publications
def publications():
    old = load("pubs.json", {"items": []})
    first_seen = {norm_doi(p.get("doi")) or norm_title(p.get("title")): p.get("added") for p in old.get("items", [])}
    # never let a citation count go down (keeps Google Scholar numbers imported by hand)
    old_cites = {norm_title(p.get("title")): p.get("cites") for p in old.get("items", []) if p.get("cites") is not None}

    items = {}

    # 1) OpenAlex: works linked to the ORCID (best metadata: authors in order, citations)
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode({
        "filter": f"author.orcid:{ORCID}", "per_page": 200, "mailto": EMAIL,
        "select": "id,doi,display_name,publication_year,publication_date,cited_by_count,type,authorships,primary_location"})
    for w in get(url)["results"]:
        au = w.get("authorships") or []
        venue = ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
        first = au[0]["author"].get("orcid", "") if au else ""
        key = norm_doi(w.get("doi")) or norm_title(w.get("display_name"))
        items[key] = {
            "title": w.get("display_name"),
            "authors": [short(a["author"].get("display_name")) for a in au],
            "venue": venue,
            "year": w.get("publication_year"),
            "type": kind(w.get("type"), venue),
            "doi": norm_doi(w.get("doi")),
            "first_author": bool(au) and ((ORCID in (first or "")) or is_me(au[0]["author"].get("display_name"))),
            "cites": w.get("cited_by_count", 0),
        }

    # 2) ORCID: catch anything OpenAlex hasn't linked yet
    try:
        og = get(f"https://pub.orcid.org/v3.0/{ORCID}/works")
        for g in og.get("group", []):
            s = g["work-summary"][0]
            title = ((s.get("title") or {}).get("title") or {}).get("value")
            doi = ""
            for e in (s.get("external-ids") or {}).get("external-id", []):
                if e.get("external-id-type") == "doi":
                    doi = norm_doi(e.get("external-id-value"))
            key = doi or norm_title(title)
            if key in items or any(norm_title(title) == norm_title(v["title"]) for v in items.values()):
                continue
            year = (((s.get("publication-date") or {}).get("year") or {}) or {}).get("value")
            venue = ((s.get("journal-title") or {}) or {}).get("value") or ""
            cites = None
            if doi:
                try:
                    cites = get(f"https://api.openalex.org/works/doi:{doi}?select=cited_by_count&mailto={EMAIL}").get("cited_by_count")
                except Exception:
                    pass
            items[key] = {"title": title, "authors": [], "venue": venue, "year": int(year) if year else None,
                          "type": kind((s.get("type") or "").replace("_", "-"), venue), "doi": doi,
                          "first_author": None, "cites": cites}
    except Exception as e:
        print("ORCID works skipped:", e, file=sys.stderr)

    # 3) manual extras (thesis, accepted papers). Dropped once a matching title appears.
    for m in MAN.get("extra_publications", []):
        if not m.get("title"):
            continue
        key = norm_doi(m.get("doi")) or norm_title(m["title"])
        if key in items:
            items[key]["first_author"] = items[key]["first_author"] if items[key]["first_author"] is not None else m.get("first_author")
            continue
        match = next((v for v in items.values() if norm_title(m["title"]) == norm_title(v["title"]) and v["type"] != "preprint"), None)
        if match:
            # manual entry wins for tidy metadata (title case, authors, venue, first-author flag)
            for f in ("key", "title", "authors", "venue", "first_author", "url"):
                if m.get(f) not in (None, "", []):
                    match[f] = m[f]
            continue
        items[key] = {k: m.get(k) for k in ("title", "authors", "venue", "year", "type", "doi", "first_author", "url", "key")} | {"cites": m.get("cites")}
        if m.get("doi"):
            items[key]["doi"] = norm_doi(m["doi"])

    # 4) a preprint whose journal version now exists -> drop the preprint
    journal_titles = {norm_title(v["title"]) for v in items.values() if v["type"] != "preprint"}
    items = {k: v for k, v in items.items() if not (v["type"] == "preprint" and norm_title(v["title"]) in journal_titles)}

    # 5) Google Scholar (via SerpAPI): authoritative citation counts + profile totals + any paper Scholar has first
    scholar = scholar_profile(old)
    scholar_titles = set()
    if scholar and scholar.get("articles"):
        for a in scholar["articles"]:
            st = norm_title(a["title"].rstrip("…. "))
            if not st or "ssrn" in (a.get("publication") or "").lower():
                continue
            match = next((v for v in items.values() if norm_title(v["title"]).startswith(st[:60]) or st.startswith(norm_title(v["title"])[:60])), None)
            if match:
                match["cites"] = a.get("cites", 0)
                scholar_titles.add(norm_title(match["title"]))
            else:
                key = st
                authors = [x.strip() for x in (a.get("authors") or "").split(",") if x.strip()]
                items[key] = {"title": a["title"], "authors": authors, "venue": a.get("publication") or "",
                              "year": int(a["year"]) if str(a.get("year") or "").isdigit() else None,
                              "type": kind("", a.get("publication")), "doi": "", "url": a.get("link"),
                              "first_author": bool(authors) and is_me(authors[0]), "cites": a.get("cites", 0)}
                scholar_titles.add(norm_title(a["title"]))

    # 6) keep anything already on the site that a source missed this run (APIs drop records now and then)
    have = {norm_title(v["title"]) for v in items.values()}
    for p in old.get("items", []):
        t = norm_title(p.get("title"))
        if t and t not in have and not any(t.startswith(h[:60]) or h.startswith(t[:60]) for h in have):
            items[norm_doi(p.get("doi")) or t] = dict(p)
            have.add(t)

    hide = {norm_doi(d) for d in MAN.get("hide_dois", [])}
    out = []
    for k, v in items.items():
        if v["doi"] and v["doi"] in hide:
            continue
        v["first_author"] = bool(v["first_author"]) if v["first_author"] is not None else bool(v["authors"] and is_me(v["authors"][0]))
        oc = old_cites.get(norm_title(v.get("title")))
        if norm_title(v.get("title")) not in scholar_titles and oc is not None and (v.get("cites") is None or v["cites"] < oc):
            v["cites"] = oc
        v["added"] = first_seen.get(k) or (TODAY if old.get("source") != "seed" and old.get("items") else None)
        out.append(v)
    out.sort(key=lambda p: (-(p["year"] or 0), -(p["cites"] or 0)))
    rec = {"updated": NOW.isoformat(), "source": "scholar+orcid+openalex" if scholar else "orcid+openalex", "items": out}
    if scholar:
        rec["scholar"] = scholar["totals"]
        rec["scholar_fetched"] = scholar["fetched"]
    elif old.get("scholar"):
        rec["scholar"] = old["scholar"]
        rec["scholar_fetched"] = old.get("scholar_fetched")
    save("pubs.json", rec)
    print(f"pubs: {len(out)} items")


# ---------------------------------------------------------------- peer review
def reviews():
    d = get(f"https://pub.orcid.org/v3.0/{ORCID}/peer-reviews")
    counts = {}
    total = 0
    for grp in d.get("group", []):
        for pg in grp.get("peer-review-group", []):
            for s in pg.get("peer-review-summary", []):
                total += 1
                gid = s.get("review-group-id", "")
                counts[gid] = counts.get(gid, 0) + 1
    journals = []
    for gid, n in counts.items():
        name = gid
        m = re.match(r"issn:(\S+)", gid or "")
        if m:
            try:
                name = get(f"https://api.openalex.org/sources/issn:{m.group(1)}?select=display_name&mailto={EMAIL}")["display_name"]
            except Exception:
                pass
        journals.append({"name": name, "count": n})
    journals.sort(key=lambda j: -j["count"])
    save("reviews.json", {"updated": NOW.isoformat(), "source": "orcid", "count": total, "journals": journals})
    print(f"reviews: {total}")


# ---------------------------------------------------------------- social
def instagram(n):
    tok = os.environ.get("IG_TOKEN")
    if not tok or not CFG.get("instagram"):
        return []
    try:  # keep the long-lived token alive (valid 60 days from last refresh)
        get("https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=" + tok)
    except Exception as e:
        print("IG refresh skipped:", e, file=sys.stderr)
    q = urllib.parse.urlencode({"fields": "id,caption,media_type,media_url,thumbnail_url,permalink,timestamp", "limit": n, "access_token": tok})
    media = get("https://graph.instagram.com/me/media?" + q).get("data", [])
    imgdir = ROOT / "assets" / "social"
    imgdir.mkdir(parents=True, exist_ok=True)
    keep, out = set(), []
    for m in media:
        src = m.get("thumbnail_url") if m.get("media_type") == "VIDEO" else m.get("media_url")
        fn = f"ig_{m['id']}.jpg"
        keep.add(fn)
        if src and not (imgdir / fn).exists():
            try:
                (imgdir / fn).write_bytes(get(src, accept="*/*", raw=True))
            except Exception as e:
                print("IG image skipped:", e, file=sys.stderr)
        out.append({"platform": "instagram", "date": m.get("timestamp"), "url": m.get("permalink"),
                    "text": (m.get("caption") or "")[:280], "image": f"assets/social/{fn}" if (imgdir / fn).exists() else None})
    for f in imgdir.glob("ig_*.jpg"):  # tidy old images
        if f.name not in keep:
            f.unlink()
    return out


def rss():
    out = []
    for f in CFG.get("rss_feeds", []):
        if not f.get("url"):
            continue
        try:
            root = ET.fromstring(get(f["url"], accept="application/rss+xml, application/atom+xml, */*", raw=True))
            ns = {"a": "http://www.w3.org/2005/Atom"}
            for it in (root.findall(".//item") or root.findall(".//a:entry", ns))[:5]:
                t = it.findtext("title") or it.findtext("a:title", namespaces=ns) or ""
                link = it.findtext("link") or (it.find("a:link", ns).get("href") if it.find("a:link", ns) is not None else "")
                date = it.findtext("pubDate") or it.findtext("a:published", namespaces=ns) or it.findtext("a:updated", namespaces=ns)
                try:
                    from email.utils import parsedate_to_datetime
                    date = parsedate_to_datetime(date).isoformat()
                except Exception:
                    pass
                out.append({"platform": "rss", "source": f.get("name") or "Blog", "date": date, "url": link, "text": t})
        except Exception as e:
            print("RSS skipped:", f.get("url"), e, file=sys.stderr)
    return out


def social():
    items = instagram(CFG.get("instagram_posts", 6)) + rss()
    if not items:
        old = load("social.json", {"items": []})
        if old.get("items"):
            return  # keep last good feed rather than blanking it
    save("social.json", {"updated": NOW.isoformat(), "items": items})
    print(f"social: {len(items)} items")


if __name__ == "__main__":
    failed = 0
    for step in (publications, reviews, social):
        try:
            step()
        except Exception as e:
            failed += 1
            print(f"{step.__name__} failed: {e}", file=sys.stderr)
    sys.exit(1 if failed == 3 else 0)
