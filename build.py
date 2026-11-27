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

BRAND = ('<svg class="globe" viewBox="0 0 40 40" aria-hidden="true">'
         '<defs><clipPath id="globe-clip"><circle cx="20" cy="20" r="16.5"/></clipPath>'
         '<radialGradient id="globe-shade" cx=".35" cy=".3" r=".75"><stop offset="0" stop-color="#fff" stop-opacity=".45"/>'
         '<stop offset=".55" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#0b2a44" stop-opacity=".35"/></radialGradient></defs>'
         '<circle cx="20" cy="20" r="16.5" fill="#3d82bf"/>'
         '<g clip-path="url(#globe-clip)"><g class="globe-land" fill="#e07a1f" stroke="#24170d" stroke-width=".8"><path d="M4 12 c4 -4 10 -3 12 1 c2 4 -2 6 0 10 c2 4 -3 8 -6 5 c-3 -3 -1 -7 -4 -9 c-3 -2 -4 -5 -2 -7z"/><path d="M22 8 c4 -2 9 0 9 3 c0 3 -4 3 -5 6 c-1 3 3 4 2 8 c-1 5 -6 6 -7 2 c-1 -4 -3 -6 -2 -10 c1 -3 1 -7 3 -9z"/><path d="M34 24 c3 -1 6 1 6 4 c0 3 -4 4 -6 2 c-2 -2 -2 -5 0 -6z"/><path d="M44 10 c6 -3 14 -1 16 3 c2 4 -3 5 -2 9 c1 3 -2 5 -5 3 c-3 -2 -6 -1 -8 -4 c-2 -4 -4 -8 -1 -11z"/><path d="M62 22 c3 -2 8 0 9 3 c1 4 -3 8 -7 6 c-3 -2 -4 -6 -2 -9z"/><path d="M70 8 c3 -1 6 0 7 2 c1 2 -2 3 -4 3 c-2 0 -4 -3 -3 -5z"/><g transform="translate(80 0)"><path d="M4 12 c4 -4 10 -3 12 1 c2 4 -2 6 0 10 c2 4 -3 8 -6 5 c-3 -3 -1 -7 -4 -9 c-3 -2 -4 -5 -2 -7z"/><path d="M22 8 c4 -2 9 0 9 3 c0 3 -4 3 -5 6 c-1 3 3 4 2 8 c-1 5 -6 6 -7 2 c-1 -4 -3 -6 -2 -10 c1 -3 1 -7 3 -9z"/><path d="M34 24 c3 -1 6 1 6 4 c0 3 -4 4 -6 2 c-2 -2 -2 -5 0 -6z"/><path d="M44 10 c6 -3 14 -1 16 3 c2 4 -3 5 -2 9 c1 3 -2 5 -5 3 c-3 -2 -6 -1 -8 -4 c-2 -4 -4 -8 -1 -11z"/><path d="M62 22 c3 -2 8 0 9 3 c1 4 -3 8 -7 6 c-3 -2 -4 -6 -2 -9z"/><path d="M70 8 c3 -1 6 0 7 2 c1 2 -2 3 -4 3 c-2 0 -4 -3 -3 -5z"/></g></g>'
         '<g fill="none" stroke="#fff" stroke-opacity=".35" stroke-width=".7"><ellipse cx="20" cy="20" rx="7" ry="16.5"/><path d="M3.5 20 H36.5 M6 12 H34 M6 28 H34"/></g>'
         '<circle cx="20" cy="20" r="16.5" fill="url(#globe-shade)"/></g>'
         '<circle cx="20" cy="20" r="16.5" fill="none" stroke="#24170d" stroke-width="2.4"/></svg>')


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
<link rel="preload" href="/assets/home/fonts/urbanist-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/style.css">
<link rel="stylesheet" href="/assets/theme.css">{extra}
</head>
<body>
{SPRITE}
<a class="skip" href="#main">Skip to content</a>
<div class="tn"><nav class="topnav" aria-label="Main">
  <a class="me" href="/"><svg class="mark" aria-hidden="true" viewBox="0 0 32 32"><path d="M16 3 L27 7.5 V15.5 C27 22.5 22.2 27.4 16 29.5 C9.8 27.4 5 22.5 5 15.5 V7.5 Z" fill="none" stroke="#000" stroke-width="2" stroke-linejoin="round"/><path d="M19.6 10.6c-.7-1.2-2-1.9-3.6-1.9-2 0-3.5 1.1-3.5 2.7 0 3.6 7.2 2 7.2 5.8 0 1.7-1.6 2.9-3.7 2.9-1.7 0-3.1-.8-3.8-2.1" fill="none" stroke="#000" stroke-width="2" stroke-linecap="round"/><circle cx="16" cy="24" r="1.7" fill="#ff5a00"/></svg>ISHAKU</a>
  <a href="/research/"{" aria-current=\"page\"" if meta.get("active") == "projects" else ""}>Research</a>
  <a href="/#mission">Mission</a>
  <a href="/#writing"{" aria-current=\"page\"" if meta.get("active") == "writing" else ""}>Writing</a>
  <a href="/#contact">Contact</a>
</nav></div>
<main id="main">
{body}
</main>
<footer class="site-foot">
  <div class="wrap ft">
    <div><a href="/">lord-shax.github.io</a><br><a href="https://github.com/Lord-Shax">github.com/Lord-Shax</a></div>
    <div>Issue<br>Nov 2026</div>
    <div class="ftag">Making AI safe for all.</div>
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
        out.write_text(body if meta.get("standalone") else layout(meta, body), encoding="utf-8")
        print("built", out.relative_to(ROOT))


if __name__ == "__main__":
    build()
