# book-to-tree-www

The coming-soon page for book·to·tree, served by GitHub Pages. `BRIEF.md` says what the page
says and why.

- **Preview locally:** `python3 -m http.server 8000`, then open http://localhost:8000. Opening
  `index.html` as a file shows everything except the sample excerpts, which are loaded from
  `sample/`.
- **Publish:** Settings → Pages → Deploy from a branch → `main` / `(root)`. Set the custom domain
  on the same screen.
- **Before launch:** replace the three `https://forms.gle/REPLACE-WITH-FORM-LINK` links in
  `index.html` with the Google Form, and add `og:url` / `og:image` once the domain exists (see
  the TODO in `<head>`). Fonts (Fraunces, Nunito Sans) load from Google Fonts; self-host them if
  you'd rather visitors' browsers not contact Google.
- **Internal notes stay off the site.** Pages builds with Jekyll, which skips `_src/` and
  dot-folders, and `_config.yml` excludes `BRIEF.md`, `README.md`, `DESIGN.md` and `CLAUDE.md`.
  Add any new internal file to that list.

## The sample

`sample/` holds placeholders (an invented family), to be replaced with real files under the same
names: `book.pdf`, `page.jpg` (the page shown on the site), `full-text.txt`, `extracted.csv`,
`extracted-merged.csv` and `tree.ged`.

- **The excerpts update themselves.** `assets/sample.js` reads the "See an example" rows and
  GEDCOM record from those files. Set `data-page` on `#example` in `index.html` to the page number
  (the CSV's `image` value) that `page.jpg` shows.
- **The family-tree art does not.** It names the invented Larkworth family in three places:
  1. **The hand-drawn SVG art** (the opening and the "head start" illustration). Edit `KIDS`,
     `FAMILY` and the circled line in `_src/gen_art_c.py`, then run `python3 _src/gen_art_c.py`.
     It rewrites only the marked SVG blocks in `index.html`.
  2. **The phone version of the opening art**, the `art-phone` block in `index.html`. Edit the
     couple and children by hand.
  3. **The `alt` text** of both `page.jpg` images in `index.html`.
