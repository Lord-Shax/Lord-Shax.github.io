"""One CV source, two outputs.

_src/cv/cv.html is the CV. This script
  1. prints it to cv/Ishaku-CV.pdf (A4, one page), and
  2. copies its body into _src/pages/cv/index.html between <!--cv--> markers,
     so the web page and the PDF never disagree.
Run: python3 _src/gen_cv.py && python3 build.py
"""
from pathlib import Path
import re

from playwright.sync_api import sync_playwright

SRC = Path(__file__).parent
ROOT = SRC.parent
CV = SRC / "cv" / "cv.html"
PAGE = SRC / "pages" / "cv" / "index.html"
PDF = ROOT / "cv" / "Ishaku-CV.pdf"


def main() -> None:
    html = CV.read_text(encoding="utf-8")
    body = re.search(r"<!--cv-->(.*?)<!--/cv-->", html, re.S).group(1).strip()
    page = PAGE.read_text(encoding="utf-8")
    page, n = re.subn(r"<!--cv-->.*?<!--/cv-->", lambda _: f"<!--cv-->\n{body}\n<!--/cv-->", page, flags=re.S)
    if n != 1:
        raise SystemExit(f"{PAGE} needs one <!--cv--><!--/cv--> marker pair")
    PAGE.write_text(page, encoding="utf-8")

    PDF.parent.mkdir(exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto(CV.resolve().as_uri())
        pg.wait_for_timeout(400)
        pg.pdf(path=str(PDF), format="A4", prefer_css_page_size=True, print_background=True)
        b.close()
    print("wrote", PDF, "and", PAGE)


if __name__ == "__main__":
    main()
