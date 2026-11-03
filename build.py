"""Build the site from _src/ into the repo root.

    python build.py

Pages live in _src/pages/ (same paths as the published site). Each starts with
a meta comment, for example:

    <!--meta {"title": "Page title", "desc": "Description", "active": "work"} -->

and contains only what goes inside <main>. The layout (head, header, footer,
figure library) is added here.

Figures: write <fig pose="cheer" kind="human"/> anywhere. Inside an SVG scene,
add x, y and h (height) to place it: <fig pose="run" kind="bad" x="20" y="40" h="120"/>.
kind is human (coffee), ai (orange) or bad (red); add flip to mirror it, and
head="ai-sad" etc. to override the head. Poses are the b-* symbols in
_src/partials/sprite.svg.
"""

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "_src"
SPRITE = (SRC / "partials" / "sprite.svg").read_text(encoding="utf-8")

NAV = [("ramblings", "/#ramblings", "Ramblings"), ("projects", "/#projects", "Projects"),
       ("vision", "/#vision", "My vision")]
HEADS = {"human": "human", "ai": "ai", "bad": "mask"}

BRAND = ('<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="10.5" fill="none" '
         'stroke="#24170d" stroke-width="3.4"/><ellipse cx="20" cy="20" rx="18" ry="6.8" fill="none" '
         'stroke="#e07a1f" stroke-width="2.8" transform="rotate(-25 20 20)"/><circle cx="35" cy="13" r="3.6" '
         'fill="#e07a1f"/></svg>')


def fig(m: re.Match) -> str:
    a = dict(re.findall(r'(\w[\w-]*)="([^"]*)"', m.group(1)))
    flags = re.findall(r'\s(flip)(?=\s|$)', " " + m.group(1) + " ")
    kind = a.get("kind", "human")
    head = a.get("head", HEADS[kind])
    pose = a["pose"]
    inner = f'<use href="#b-{pose}"/><use href="#h-{head}"/>'
    if flags:
        if head.startswith("ai"):  # mirror the body, but keep the "AI" hair readable
            inner = (f'<g transform="translate(100 0) scale(-1 1)"><use href="#b-{pose}"/>'
                     f'<use href="#h-{head}-bare"/></g><use href="#h-hair-ai"/>')
        else:
            inner = f'<g transform="translate(100 0) scale(-1 1)">{inner}</g>'
    cls = f'fig {kind} {a.get("class", "")}'.strip()
    if "x" in a:  # placed inside an SVG scene
        h = float(a.get("h", 160))
        w = h * 100 / 160
        return (f'<svg x="{a["x"]}" y="{a["y"]}" width="{w:g}" height="{h:g}" viewBox="0 0 100 160" '
                f'class="{cls}" overflow="visible">{inner}</svg>')
    return f'<svg class="{cls}" viewBox="0 0 100 160" aria-hidden="true" overflow="visible">{inner}</svg>'


def layout(meta: dict, body: str) -> str:
    nav = "".join(f'<a href="{href}"{" aria-current=\"page\"" if meta.get("active") == key else ""}>{label}</a>'
                  for key, href, label in NAV)
    title = html.escape(meta["title"])
    desc = html.escape(meta.get("desc", ""))
    extra = meta.get("head", "")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/archivo-latin-standard-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/style.css">{extra}
</head>
<body>
<div class="kente-strip" aria-hidden="true"></div>
{SPRITE}
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="/">{BRAND}<span>Ishaku</span></a>
    <a class="cv-pill" href="/cv/Ishaku-CV.pdf" download="Ishaku-Gayus-CV.pdf" aria-label="Download my CV as a PDF">CV <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2v8m-3.5-3.5L8 10l3.5-3.5M3 13h10" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
    <nav class="nav" aria-label="Main">{nav}</nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-foot">
  <div class="wrap">
    <span>© <span data-year>2026</span> Ishaku · <a href="/#contact">Contact</a> · <a href="/cv/Ishaku-CV.pdf" download="Ishaku-Gayus-CV.pdf">CV</a> · <a href="https://github.com/Lord-Shax">GitHub</a></span>
    <span>Original illustrations. Built with help from Claude.</span>
  </div>
</footer>
<script src="/assets/site.js" defer></script>
</body>
</html>
"""


def build() -> None:
    for src in sorted((SRC / "pages").rglob("*.html")):
        text = src.read_text(encoding="utf-8")
        m = re.match(r"\s*<!--meta\s+(\{.*?\})\s*-->\s*", text, re.S)
        if not m:
            raise SystemExit(f"{src}: missing <!--meta {{...}} --> header")
        meta = json.loads(m.group(1))
        body = re.sub(r"<fig\s+([^>]*?)/>", fig, text[m.end():])
        out = ROOT / src.relative_to(SRC / "pages")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(layout(meta, body), encoding="utf-8")
        print("built", out.relative_to(ROOT))


if __name__ == "__main__":
    build()
