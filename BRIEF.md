# book·to·tree coming-soon page: brief

Internal working notes. `_config.yml` keeps this file off the published site.

## Decided (2026-10-06)

- **Who it's for:** genealogists holding a scanned PDF of an old family-history book whose
  author is long gone. Not the book's author: someone who has the Word file probably has the
  GEDCOM too.
- **The promise:** upload a scanned PDF of the book; a few hours later, download
  1. the full text,
  2. the extraction CSV and the merged-extraction CSV,
  3. a GEDCOM of the tree.
- **Framing:** a head start to check, not a finished tree. For example: "a first draft of your
  tree, with every person linked to the page of the book they came from, so you can check it."
- **Input:** scanned PDFs only. Don't mention born-digital PDFs.
- **Call to action:** a "Notify me when it launches" button that links to a one-question
  Google Form (email address). Answers land in a Google Sheet. No form code on the site.
- **Price:** not mentioned. The FAQ says pricing will be announced before launch.
- **Sample:** `sample/` holds placeholders (an invented family, labeled as invented on its
  title page). They will be replaced with real files from a real book.
- **Hosting:** GitHub Pages from `PioneerAIContractors/book-to-tree-www`, on a custom domain
  (not chosen yet). The repo is public. Static HTML/CSS, no build step.
- **Name:** book·to·tree (the Review Console's wordmark), for now.
- **Design:** direction C, "Family Tree": warm cream with sage and terracotta, Fraunces headings,
  Nunito Sans text, and the family tree growing out of the book page. Picked 2026-10-06 from
  three directions plus the first draft on a design-shotgun board (rated 5/5). Its phone layout
  was then simplified, because the first version was too busy to read on a phone.

## Facts the page may rely on (checked against book-to-tree, 2026-10-06)

- **Input:** a scanned PDF, meaning each page is an embedded image. A born-digital PDF with
  no page images is refused at upload. Uploads up to 4 GiB.
- **Outputs:** OCR full text, page by page. The extraction CSV has one row per person per
  page, with names, dates and places copied as printed. The merged CSV combines the same
  person across pages into one row. The GEDCOM is version 5.5.1.
- **Citations:** every person in the GEDCOM cites the page of the book they came from. A
  person merged from several pages cites every one of those pages.
- **Review:** today a lead reviews each book before merge and export. The self-serve flow
  (upload, then download a few hours later with no review) is what's "coming soon". "A few
  hours" is the target, not a measurement.

## Audience

- Genealogists skew older: large type, strong contrast, plain words, obvious buttons.
- Pages like this get shared in Facebook genealogy groups, so the social preview card
  (Open Graph tags and image) matters.

## Still open

- The domain.
- What happens to uploaded PDFs and outputs (how long they're kept, deletion), and to living
  people in a tree. Decide before the FAQ promises anything.
- Who is behind the page, and a contact address.
- Launch timing: give a date or not.

## Next

- Drop in the Google Form link and set up the domain (see `README.md`).
- Optional polish, from a Claude Code session in this repo: `/design-review` (a visual check
  that fixes what it finds) and `/qa` (links, the form, the social card). `/design-shotgun`
  shows other visual directions. With no OpenAI key in `~/.gstack/openai.json`, it makes HTML
  wireframes instead of image mockups.

## Google Form setup

- One question: the email address. Use a short-answer question, or Settings → Responses →
  Collect email addresses → **Responder input**, which doesn't require a Google sign-in.
- If the form is made under a Google Workspace account, turn off **Restrict to users in
  <domain>**, or visitors hit a sign-in wall.
- Leave **Limit to 1 response** off. It forces visitors to sign in.
- Link the responses to a Sheet.
