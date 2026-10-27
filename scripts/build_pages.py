#!/usr/bin/env python3
"""Build the site's pages from scripts/page.html.

Edit scripts/page.html (layout) or data/*.json (content), never the generated
index.html / research/index.html etc. The deploy workflow runs this before
publishing, so a commit that only touches the template still updates every page.

Blocks in the template are wrapped as
    <!--@pages home research-->  ...  <!--@end-->
and kept only on the pages listed.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TPL = (ROOT / "scripts" / "page.html").read_text()

NAME = "Dr. Renston Jake Fernandes"
PAGES = [
    # key, path, <title>, meta description, H1, subtitle
    ("home", "", f"{NAME} | Clean Fuels, LCA, TEA & E-Fuels",
     "Academic portfolio of Dr. Renston Jake Fernandes — circular carbon e-fuels, process modelling, life cycle assessment, techno-economic analysis, clean combustion, and rock music.",
     "", ""),
    ("research", "research/", f"Research | {NAME}",
     "Research areas, vision and teaching philosophy of Dr. Renston Jake Fernandes: circular carbon e-fuels, industrial decarbonisation, LCA and TEA.",
     "Research", "Circular carbon e-fuels, industrial decarbonisation, and the tools to judge them: process modelling, LCA and TEA."),
    ("publications", "publications/", f"Publications | {NAME}",
     "Publications of Dr. Renston Jake Fernandes with live citation counts, and the journals he peer-reviews for.",
     "Publications & Reviewing", "Papers, chapters and thesis with citation counts that sync automatically, plus my peer-review record."),
    ("talks", "talks/", f"Talks & Writing | {NAME}",
     "Seminars, blog posts and updates from Dr. Renston Jake Fernandes.",
     "Talks & Writing", "Seminars, conference talks, blog posts and updates."),
    ("music", "music/", f"Music | {NAME}",
     "Renston Jake Fernandes — rock vocalist and songwriter: The Speksy Pscyentist, Sounds Fishy, The Southern Bandits and Avalanche Brakedown. Releases, stages and press.",
     "Music", "Rock vocalist, songwriter and guitarist — from Mangaluru's battle-of-the-bands circuit to UK festival stages and VEVO."),
    ("experience", "experience/", f"Experience | {NAME}",
     "Experience, education, awards, languages and technical toolkit of Dr. Renston Jake Fernandes.",
     "Experience", "Roles, education, awards and the tools I work with."),
    ("contact", "contact/", f"Contact | {NAME}",
     "Contact Dr. Renston Jake Fernandes for research collaboration, consulting and policy-relevant fuel assessment.",
     "Contact", "Open to postdoctoral research, academic collaborations, consulting, and policy-relevant fuel assessment."),
]
LABEL = {p[0]: p[4] for p in PAGES}

# faded corner art per page; music gets a full-bleed live video header
IMG = lambda src: f'<div class="phead-art" aria-hidden="true"><img src="{src}" alt="" loading="eager"></div>'
ART = {
    "research": (IMG("assets/img/blog-circular-carbon.jpg"), ""),
    "publications": (IMG("assets/img/talk-emethanol-tea.jpg"), ""),
    "talks": (IMG("assets/img/caricature.jpg"), ""),
    "experience": (IMG("assets/img/presenting.jpg"), ""),
    "contact": (IMG("assets/img/caricature.jpg"), ""),
    "music": ('<div class="phead-art yt" aria-hidden="true"><iframe class="lazyyt" title="Sympathetic Race (background)" tabindex="-1" '
              'data-src="https://www.youtube-nocookie.com/embed/90K5BCROdXA?autoplay=1&amp;mute=1&amp;controls=0&amp;loop=1&amp;playlist=90K5BCROdXA&amp;start=106&amp;playsinline=1&amp;rel=0&amp;modestbranding=1&amp;iv_load_policy=3&amp;disablekb=1&amp;enablejsapi=1" '
              'allow="autoplay; encrypted-media"></iframe></div>', " dark"),
}
ORDER = [p[0] for p in PAGES if p[0] != "home"]

BLOCK = re.compile(r"<!--@pages ([a-z ]+)-->\n?(.*?)\n?<!--@end-->", re.S)


def esc(t):
    return t.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def build(key, path, title, desc, h1, sub):
    html = BLOCK.sub(lambda m: m.group(2) if key in m.group(1).split() else "", TPL)
    nxt = ""
    if key in ORDER:
        i = ORDER.index(key)
        if i + 1 < len(ORDER):
            n = ORDER[i + 1]
            nxt = f'<a class="btn primary" href="{n}/">{LABEL[n]} →</a>'
    html = (html.replace("{{TITLE}}", esc(title)).replace("{{DESC}}", esc(desc))
                .replace("{{PATH}}", path).replace("{{PAGE}}", key)
                .replace("{{H1}}", h1.replace("&", "&amp;")).replace("{{SUB}}", esc(sub))
                .replace("{{NEXT}}", nxt)
                .replace("{{ART}}", ART.get(key, ("", ""))[0]).replace("{{PHEAD_CLASS}}", ART.get(key, ("", ""))[1]))
    html = html.replace(f'data-nav="{key}"', f'data-nav="{key}" aria-current="page"')
    out = ROOT / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    return out


def sitemap():
    urls = [("", "daily", "1.0")] + [(p[1], "weekly", "0.8") for p in PAGES[1:]] + [
        ("blog/why-circular-carbon-efuels-matter/", "monthly", "0.6"),
        ("uploads/FERNANDES_CV.pdf", "monthly", "0.5")]
    body = "".join(f"  <url><loc>https://renstonfernandes.com/{u}</loc><changefreq>{c}</changefreq><priority>{p}</priority></url>\n"
                   for u, c, p in urls)
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                                      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "</urlset>\n")


if __name__ == "__main__":
    for p in PAGES:
        print("built", build(*p).relative_to(ROOT))
    sitemap()
