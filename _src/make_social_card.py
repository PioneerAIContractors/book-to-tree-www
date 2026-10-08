"""Build assets/social-card.png, the 1200x630 link-preview image (og:image).

It reuses the page's own wordmark, icons, fonts and hand-drawn tree art from index.html, so
rerun it after the art changes (e.g. after _src/gen_art_c.py):

    python3 _src/make_social_card.py

Needs Google Chrome (headless).
"""
from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def main() -> None:
    page = (SITE / "index.html").read_text(encoding="utf-8")
    sprite = re.search(r'<svg class="sprite".*?</svg>', page, re.S).group(0)
    art = re.search(r'<svg class="art-wide".*?</svg>', page, re.S).group(0)
    fonts = '<link rel="stylesheet" href="assets/fonts.css">'   # self-hosted, resolved via <base>
    # the launch date, taken from the line under the hero button ("Opens December 1, 2026")
    soon = re.search(r'<p class="fine">(Opens [^.]+\d{4})', page).group(1)
    css = (SITE / "assets" / "site.css").resolve().as_uri()
    # <base> makes the art's relative image path (sample/page.jpg) resolve to the site root.
    html = f"""<!doctype html><html><head><meta charset="utf-8"><base href="{SITE.as_uri()}/">{fonts}
<link rel="stylesheet" href="{css}">
<style>
  html, body {{ margin: 0; }}
  .card {{ width: 1200px; height: 630px; box-sizing: border-box; padding: 52px 56px;
          display: grid; grid-template-columns: 470px minmax(0, 1fr); gap: 34px; align-items: center;
          background: var(--cream); }}
  .card .wordmark {{ font-size: 40px; }}
  .card .mark {{ width: 46px; height: 46px; }}
  .card h1 {{ font-size: 54px; text-align: left; margin: 30px 0 28px; max-width: none; }}
  .card .soon {{ font-size: 20px; padding: 8px 20px; }}
  .card .art {{ margin: 0; padding: 18px 18px 20px; }}
</style></head><body>{sprite}
<div class="card"><div>
  <div class="wordmark"><svg class="mark" aria-hidden="true"><use href="#i-sprout"/></svg><span class="wm-text">book<span class="two">2</span>tree</span></div>
  <h1>Grow a family tree from your family history book.</h1>
  <span class="soon">{soon}</span>
</div><figure class="art">{art}</figure></div></body></html>"""
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "card.html"
        src.write_text(html, encoding="utf-8")
        out = SITE / "assets" / "social-card.png"
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", "--window-size=1200,630",
                        "--allow-file-access-from-files", "--virtual-time-budget=8000",
                        f"--screenshot={out}", src.as_uri()],
                       check=True, capture_output=True, timeout=120)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
