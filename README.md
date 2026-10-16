# The Fintech Engineer — content kit

Self-sufficient folder for generating and publishing content for **The
Fintech Engineer** — a personal content/advisory brand for Naren
Viswanath (senior engineering manager, fintech: payments/cards,
lending/credit & risk, engineering leadership). Read this file first;
everything you need to write and ship a new post lives under this one
folder — brand assets, image-generation toolkit, worked examples, and
past posts.

This folder deliberately does **not** cover the n8n LinkedIn
auto-posting automation (that's infrastructure/ops, lives with the main
project checkout, and isn't needed to *create* content). Nothing here
assumes it exists.

## Channels

- **Substack** (long-form): [thefintechengineer.substack.com](https://thefintechengineer.substack.com)
- **LinkedIn Company Page**: [linkedin.com/company/the-fintech-engineer](https://www.linkedin.com/company/the-fintech-engineer)
- **Instagram**: planned, not yet live — when it launches, add the handle here.
- **Domain**: `thefintechengineer.dev` (registration status: check before assuming it's live)

## Folder contents

```
brand-identity/    Finalized identity kit (v1.0) — logos, colors, type, LinkedIn/social
                    images, favicons, brand-guide.pdf. Canonical source of truth for
                    every visual choice below. Start with brand-identity/README.txt.
post-images/        The toolkit for generating branded post images (see its own
                    README.md for the full workflow). Templates + export script +
                    worked examples, including everything for the reconciliation-drift
                    post as a live reference.
posts/              Published/drafted post copy (post.md per post, with its final
                    generated images alongside it).
```

## Brand, in brief

| token | hex | use |
|---|---|---|
| Ink | `#080D18` | primary text, dark surfaces |
| Signal | `#2F55E8` | the one accent — never a field/background, never more than one bracket of the mark |
| Paper | `#F1F3F7` | light card backgrounds |
| Slate | `#5B6472` | secondary/muted text |

Typeface: **Inter** (Google Fonts). Only two approved lockup pairings:
Ink-on-Paper and White-on-Ink — see `brand-identity/brand-guide.pdf` for
the full mark/lockup/clear-space/misuse rules before designing anything
new. Don't hand-copy hex values from memory or from this table if the
kit ever updates — `brand-identity/` is the source of truth, this table
is just a quick reference.

**Standing content rules** (apply to every post, LinkedIn/Substack/Instagram alike):
- Currency is always **`$`**, never `₹`/INR, even for India-flavored examples.
- Post copy (the LinkedIn/Substack text itself) should use emojis fairly
  liberally at hooks, key numbers, transitions, and the closing question
  — not a sparse, emoji-free technical-writer default.

## Generating a new post's images

See **`post-images/README.md`** for the full, authoritative workflow —
this is just the short version:

1. Copy the template that fits your content:
   - `post-images/templates/card-template.html` — one visual claim (a
     diagram, a trace, a comparison/infographic). 1080px wide, LinkedIn.
   - `post-images/templates/doc-template.html` — the full post copy
     typeset as a document image. 920px wide, LinkedIn.
   - `post-images/templates/collage-card-template.html` — a denser
     "editorial dossier" hook image: halftone texture, a torn-paper
     illustration panel with annotated leader-line callouts, and a
     marker-highlight headline (still Ink/Signal/Paper/Slate only — no
     off-brand colors). Use for the scroll-stopping *first* image on a
     post, not every image on every post. See
     `post-images/mcc-merchant-category-code/collage-card.html` for a
     fully worked example.
   - `post-images/templates/collage-ig-slide-template.html` — the same
     collage treatment for a single Instagram slide, for when you want
     the carousel to match a collage-style hook image. See
     `post-images/mcc-merchant-category-code/ig-slide-1.html` through
     `ig-slide-5.html` for a fully worked 5-slide arc.
   - For a plain (non-collage) **Instagram carousel**, there's no formal template yet (see
     "Open items" below) — copy the pattern from
     `post-images/reconciliation-drift/ig-slide-*.html` instead: a fixed
     `1080x1080` `.slide` container, **exactly square (1:1)** — this is
     Instagram's own recommendation, not a stylistic choice, so don't
     drift to 4:5 or any other ratio. **Dark theme** (Ink background,
     White-on-Ink pairing — deliberate Instagram-specific choice, distinct
     from the light Paper background LinkedIn images use), same brand
     tokens, swipe cues on all but the last slide, a CTA block + "Link in
     bio" on the last slide.
     **Vertically center the content, don't top-align it.** `.slide` is a
     column flexbox: `head-row` (logo + eyebrow) at the top, `footer-row`
     pinned at the bottom, and everything else wrapped in one
     `.content{ flex:1; display:flex; flex-direction:column;
     justify-content:center; }` block in between. A short amount of copy
     on a fixed square canvas will always leave whitespace — centering it
     splits that whitespace evenly above and below, which reads as
     deliberate. The earlier version of this pattern top-aligned the
     content and pinned the footer with `margin-top:auto`, which dumped
     all the leftover space into one dead gap directly above the footer —
     looked broken, not minimal. Don't reintroduce that.
2. Fill in the marked slots. Hand-author any diagram as inline `<svg>` —
   don't reach for a charting library.
3. Open the HTML file directly in a browser to sanity-check layout.
4. Export with `post-images/export_png.py`:
   ```
   python3 post-images/export_png.py <input.html> <output.png> --window=<W>,<H>
   ```
   - Card-template: `--window=1080,2400`
   - Doc-template: `--window=920,3400`
   - Instagram slide (fixed 1080x1080 square canvas): `--window=1080,1180`
   - `--scale 2` (default) for crisp embedding; the script autocrops
     leftover canvas automatically — for a *fixed*-size slide, give it a
     `height:` in CSS (and `overflow:hidden`) rather than letting content
     determine height, so every slide in a carousel set crops to the same
     final size. **Autocrop isn't pixel-perfect** — it may land a few
     pixels off the intended square (e.g. 2160×2184 instead of exactly
     2160×2160 at 2x scale). Verify each exported PNG's exact size and, if
     it's off, center-crop it to an exact square as a final step:
     ```python
     from PIL import Image
     im = Image.open(path)
     w, h = im.size
     if w != h:
         top = (h - w) // 2
         im.crop((0, top, w, top + w)).save(path)
     ```
   - Requires a local Chrome install (path auto-detected for macOS/Windows
     — see the `CHROME_CANDIDATES` list at the top of the script if it's
     installed somewhere else) and Pillow (`pip install pillow`).
5. Before treating any diagram as done, run it through the **"Diagram QA
   checklist"** in `post-images/README.md` — arrows must visibly start
   and end on a real shape (never float in empty space), boxes in a row
   must not overlap, labels must not sit on top of the lines they're near,
   and every caption must sit inside/below the section it labels, not
   floating disconnected nearby. Check this on the actual exported PNG at
   full resolution, not the browser preview — narrow preview panes clip
   exactly the kind of overflow/overlap this checklist catches.
6. Save the final PNG(s) into that channel's own folder — see "Per-channel
   folder layout" below.

## Per-channel folder layout

Each post gets one `posts/<date>-<slug>/` directory, but the copy and
images for each channel live in their **own subfolder** — a post going to
LinkedIn, Instagram and Substack ends up as:

```
posts/<date>-<slug>/
  linkedin/
    post.md                    the full LinkedIn-voiced copy (source of record for this channel)
    linkedin-post.txt          trimmed, markdown-stripped, ≤3000 chars — the paste-ready file
    substack-teaser-post.txt   (only if this post also has a substack/ folder) a short,
                               separate LinkedIn post whose only job is to send readers
                               to the full Substack piece — see "Writing a LinkedIn
                               teaser for a Substack post" below
    images/
      *.png                    card-template / doc-template exports for this post
  instagram/
    caption.txt                the carousel's caption — see "Writing an Instagram
                               caption" below
    images/
      instagram-carousel-1.png ... -N.png
  substack/
    substack-post.md      long-form markdown source (headers, code blocks, tables)
    substack-post.txt      plain-text version, no markdown, images swapped for
                           [IMAGE — filename.png] placeholders — this is what
                           actually gets pasted into Substack's editor
    images/
      *.png               one PNG per placeholder in substack-post.txt, plus
                           a hero/cover image
```

Only build the channel folders a given post actually targets — a
LinkedIn-only post doesn't need `instagram/` or `substack/` sitting empty.
Every post under `posts/` uses this layout, including the two earliest
(`2026-09-14-reconciliation-drift`, `2026-09-14-mcc-merchant-category-code`),
which were migrated from an older flat layout (`post.md` +
`linkedin-post.txt` + one shared `images/` folder at the post root) —
neither had a Substack file, so both only have `linkedin/` and
`instagram/` folders.

## Writing a new post

Create `posts/<YYYY-MM-DD>-<slug>/<channel>/post.md` (or
`substack-post.md`, etc.) with the post copy — see
`posts/2026-09-27-eventual-consistency-moving-money/linkedin/post.md` for
the shape: YAML frontmatter with title/status/channel/topic/created, then
the body. Voice/structure that's worked so far: open with a concrete
failure trace (not an abstract claim), walk the mechanism step by step,
land on a numbered/arrow-bulleted set of fixes, close with a genuine
question to invite replies. Generate the accompanying images per the
workflow above once the copy is settled — don't design the image before
the words.

## Publishing a LinkedIn-ready text file

`linkedin/post.md` is the source of record and can run long — LinkedIn
caps a post at **3,000 characters** and renders no markdown at all
(`**bold**`, `*italic*`, `- ` bullets all show up as literal characters).
Before publishing to LinkedIn, save a cleaned, limit-checked copy
alongside it:

1. Copy the post body (skip the YAML frontmatter) into
   `posts/<date>-<slug>/linkedin/linkedin-post.txt`.
2. Strip all markdown — remove `**`/`*` emphasis markers entirely (don't
   convert to unicode "bold" text; keep the brand's plain voice), and
   turn any `- ` bulleted list into plain lines (an emoji/arrow prefix
   like the numbered-emoji sections already in these posts works well,
   or just a plain hyphen).
3. Check the character count and trim if it's over the limit — tighten
   sentences rather than cutting facts/numbers/codes first; hashtags and
   the closing question are worth keeping intact since they drive
   engagement:
   ```
   python3 -c "
   with open('posts/<date>-<slug>/linkedin/linkedin-post.txt', encoding='utf-8') as f:
       print(len(f.read().rstrip()), '/ 3000')
   "
   ```
4. Leave `linkedin/post.md` untouched — it stays the full, unabridged
   source; only `linkedin-post.txt` is trimmed to fit the platform limit.

## Publishing a Substack-ready text file

`substack/substack-post.md` is the long-form source and keeps its
markdown (headers, code fences for diagrams-as-ASCII, tables) — that's
fine for reading in a repo or an editor that renders markdown. Substack's
own editor doesn't take raw markdown paste any better than LinkedIn does,
so before publishing, save a plain-text, image-annotated copy:

1. Copy the body into `posts/<date>-<slug>/substack/substack-post.txt`,
   converting every `##` header to a plain caps or title-case line, every
   code fence/table to plain prose or aligned lines, and stripping
   `**`/`*` emphasis the same way as the LinkedIn file.
2. Wherever the markdown source had a flow diagram (an ASCII box-and-arrow
   drawing, not a tiny SQL/JSON snippet), replace it with its own rendered
   PNG (`card-template`-based, built and exported the same way as any
   other post image) and drop a `[IMAGE — filename.png]` placeholder line
   in the `.txt` at that spot — this is the cue for where to paste that
   image when composing the Substack post in its editor. If the post has
   a hero/cover image, put one `[COVER IMAGE — filename.png — set as this
   post's featured/header image, not inline]` line at the very top of the
   file, before the body starts — it's a different Substack editor field
   from an inline `[IMAGE — ...]`, not just the first image in the post.
3. Leave `substack-post.md` untouched as the full markdown source.
4. Every `[IMAGE — ...]` / `[COVER IMAGE — ...]` placeholder needs its
   PNG physically present in `substack/images/` — a diagram built for a
   different channel (e.g. a card that's also referenced from
   `linkedin/post.md`) has to be *copied* into `substack/images/` too,
   not just left in the other channel's folder. Cross-check before
   calling the file done:
   ```
   cd posts/<date>-<slug>/substack
   grep -oE '(IMAGE|COVER IMAGE) — [a-zA-Z0-9_-]+\.png' substack-post.txt | sed -E 's/.*— //' | sort -u > /tmp/referenced.txt
   ls images/ | sort > /tmp/present.txt
   comm -23 /tmp/referenced.txt /tmp/present.txt   # referenced but missing — fix these
   comm -13 /tmp/referenced.txt /tmp/present.txt   # present but unused — probably fine, but worth a look
   ```

## Writing a LinkedIn teaser for a Substack post

When a post has a full long-form `substack/` version, also write a
second, much shorter LinkedIn post whose only job is to send people to
it — this is distinct from `linkedin/post.md`, which is a complete,
self-contained post in its own right (LinkedIn's algorithm and audience
still deserve a real post, not just a link-out). Save it as
`linkedin/substack-teaser-post.txt`:

- Keep it short — 4-6 short paragraphs, not the full argument. Lead with
  the same concrete hook/number the long-form piece opens with (don't
  make the reader guess what it's about), give one line of what makes it
  different or non-obvious, then explicitly point out what the full piece
  covers that this post doesn't have room for.
- The closing CTA is a link-out ("Read it on Substack:
  thefintechengineer.substack.com"), not an engagement question — the
  teaser's job is clicks to the article, not comments on the post.
- Same emoji-forward voice and hashtag block as every other LinkedIn
  post; no character-limit trimming step needed since it's already short.

## Writing an Instagram caption

Save the carousel's caption as `instagram/caption.txt`. It's a different
piece of writing from the slides themselves, not a copy-paste of any
slide's text:

- Instagram truncates a caption to roughly the first 125 characters
  before a "more" tap, so the opening line has to work completely on its
  own — usually the same concrete number/hook the first slide uses.
- Reference the swipe explicitly (e.g. "Swipe through for the mechanism →
  the fix") since that's the actual mechanic of a carousel — the caption
  should make someone want to swipe, not just restate slide 1.
- Close with "link in bio" (Instagram doesn't support clickable links in
  the caption body) rather than a URL.
- End with a `.` / `.` / `.` line-break spacer before the hashtag block —
  this is the standard IG convention for pushing hashtags below the
  caption's visible fold without deleting them.
- Hashtags can run heavier than LinkedIn's (LinkedIn: 4-6 topical tags;
  Instagram: 6-10 is normal) since discovery works more through tags here.

## Worked examples

`posts/2026-09-14-reconciliation-drift/` is a complete, real example:
`linkedin/post.md` plus two LinkedIn images (a trace diagram and a
pictorial comparison card, both `card-template`-based, in
`linkedin/images/`) and a 3-slide dark-theme Instagram carousel in
`instagram/images/`. Its sources live in
`post-images/reconciliation-drift/` if you want to see exactly how each
image was built.

`posts/2026-09-14-mcc-merchant-category-code/` is a second worked
example, covering the pieces the first one doesn't: a
`collage-card-template`-based hook image, a 5-slide collage-style
Instagram carousel (`post-images/mcc-merchant-category-code/`), and a
trimmed `linkedin/linkedin-post.txt` next to the full-length
`linkedin/post.md`.

`posts/2026-09-27-eventual-consistency-moving-money/` is the fullest
reference example — a `linkedin/` folder (condensed post + two cards,
plus a `substack-teaser-post.txt` since this post also has a long-form
version), an `instagram/` folder (5-slide carousel with real inline-SVG
diagrams, not text-only slides, plus its own `caption.txt`), and a
`substack/` folder (full long-form piece plus seven flow-diagram images
and a hero image). Its sources live in
`post-images/eventual-consistency-moving-money/`.

## Open items

- No formal `templates/carousel-template.html` for the *plain* Instagram
  style yet — the worked `ig-slide-*.html` files in
  `post-images/reconciliation-drift/` are the pattern to copy until one
  gets promoted to `templates/`. (The collage style already has a
  template: `post-images/templates/collage-ig-slide-template.html`.)
- Confirm `thefintechengineer.dev` registration status and update this
  file once it's live.
- Instagram account not yet created — add the handle/link here once it
  exists.
