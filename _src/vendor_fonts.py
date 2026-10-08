"""Download the page's web fonts from Google Fonts once and serve them from this site, so a
visit to the page sends nothing to Google. Writes assets/fonts.css and assets/fonts/*.woff2,
plus each font's OFL license. Rerun only to change or refresh the fonts:

    python3 _src/vendor_fonts.py

Keeps Google's own subsets and unicode-ranges for Latin and Latin Extended (accented names
such as Müller or Łukasiewicz), so a browser downloads a file only when the page uses it.
"""
from __future__ import annotations

import re
import urllib.request
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
FONTS = SITE / "assets" / "fonts"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")   # a UA that gets WOFF2 + subsets

REQUESTS = [
    # Fraunces 600 with the soft axis at 100 (headings); Nunito Sans 400 and 700 (text)
    ("https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT@9..144,600,100"
     "&family=Nunito+Sans:wght@400;700&display=swap", {"latin", "latin-ext"}),
    # Pinyon Script, only the "2" of the wordmark
    ("https://fonts.googleapis.com/css2?family=Pinyon+Script&text=2&display=swap", {None}),
]
LICENSES = {"Fraunces": "fraunces", "Nunito Sans": "nunitosans", "Pinyon Script": "pinyonscript"}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def main() -> None:
    FONTS.mkdir(parents=True, exist_ok=True)
    out = ["/* Self-hosted web fonts (see _src/vendor_fonts.py). SIL Open Font License; the",
           "   licenses are in assets/fonts/OFL-*.txt. */", ""]
    saved: dict[str, str] = {}
    for url, keep in REQUESTS:
        css = fetch(url).decode("utf-8")
        for subset, block in re.findall(r"(?:/\* ([\w-]+) \*/\s*)?(@font-face \{.*?\})", css, re.S):
            subset = subset or None
            if subset not in keep:
                continue
            family = re.search(r"font-family: '([^']+)'", block).group(1)
            src = re.search(r"url\((https://[^)]+)\)", block).group(1)
            if src not in saved:
                slug = family.lower().replace(" ", "-")
                name = f"{slug}-{subset}.woff2" if subset else f"{slug}-wordmark.woff2"
                (FONTS / name).write_bytes(fetch(src))
                saved[src] = name
            out.append((f"/* {family}, {subset} */\n" if subset else f"/* {family}, the wordmark's 2 */\n")
                       + block.replace(src, "fonts/" + saved[src]).replace("url(fonts/", "url('fonts/")
                       .replace(".woff2)", ".woff2')") + "\n")
    (SITE / "assets" / "fonts.css").write_text("\n".join(out), encoding="utf-8")
    for family, folder in LICENSES.items():
        text = fetch(f"https://raw.githubusercontent.com/google/fonts/main/ofl/{folder}/OFL.txt")
        (FONTS / f"OFL-{family.replace(' ', '')}.txt").write_bytes(text)
    for name in sorted(set(saved.values())):
        print(f"{name}  {(FONTS / name).stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
