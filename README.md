# book-to-tree-www

The coming-soon page for book2tree (https://book2tree.com), served by GitHub Pages. `BRIEF.md` says what the page
says and why.

- **Preview locally:** `python3 -m http.server 8000`, then open http://localhost:8000. Opening
  `index.html` as a file shows everything except the sample excerpts, which are loaded from
  `sample/`.
- **Publish:** GitHub Pages deploys `main` / `(root)` on every push. The `CNAME` file holds the
  custom domain, book2tree.com; keep it, or Pages drops the domain.
- **Sign-ups:** the three "Notify me" links go to the Google Form at
  https://forms.gle/DX1Hvcd5wsC8ZeZDA; responses land in its linked Google Sheet.
- **Fonts are self-hosted** (`assets/fonts.css`, `assets/fonts/` with their OFL licenses), so
  a visit sends nothing to Google. `_src/vendor_fonts.py` re-downloads them if they change.
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

  Then rebuild the link-preview image (`assets/social-card.png`, which reuses that art):
  `python3 _src/make_social_card.py`.
