# Post images — generating branded LinkedIn PNGs

How to make the images that accompany The Fintech Engineer LinkedIn posts:
a single "card" visual (a diagram, a trace, a mini-infographic) and/or the
full post copy rendered as a branded document image. Read this before
building a new one.

## The pattern

Every image is a self-contained HTML file — no build step, no external JS.
The `.card`/`.doc` div **is** the uploadable asset: flat, full-bleed, no
border-radius, no box-shadow, no surrounding margin. Its background color
(`--paper`) fills the frame edge to edge. This matters — see "Why the card
is flat, not floating" below before you're tempted to add a shadow back in
for looks.

Five shapes — four have formal templates, one doesn't yet:

- **`templates/card-template.html`** — one visual claim: a system/sequence
  diagram, a request trace, a quote card. Use this when the post needs an
  image that shows a *mechanism* — something a sentence would say slower
  than a picture. See `examples/retry-trace.html` for a fully worked one
  (a 3-participant request trace showing exactly where a naive retry
  double-charges a customer).
- **`templates/doc-template.html`** — the entire post copy, typeset as a
  document image (headline pull-quote, body paragraphs, a highlighted
  "fix" block, hashtags, footer). Use this for archiving a post as an
  image, portfolio use, or cross-posting somewhere that wants an image
  instead of pasted text. See `examples/retry-post.html`.
- **`templates/collage-card-template.html`** — a denser "editorial dossier"
  variant of `card-template.html`: halftone dot texture, film grain, a
  torn-paper illustration panel with leader-line callouts, a torn-paper
  tag, and a marker-highlight sweep through the headline (Signal blue,
  never an off-brand color). Use this for a scroll-stopping *hook* image
  — the first image on a post — not for every image on every post; it's
  heavier than the standard card. See `mcc-merchant-category-code/collage-card.html`
  for a fully worked one (a payment-terminal illustration with three
  annotated callouts for rewards/fraud/interchange), and the template's
  own header comment for the gotchas hit building it (callout text
  overflow, caption/shadow z-index, ink-vs-signal contrast).
- **`templates/collage-ig-slide-template.html`** — the same collage
  treatment adapted to a single dark-theme Instagram slide. Use alongside
  the plain Instagram carousel pattern below when you want the carousel to
  carry the same visual identity as a collage-style hook image. See
  `mcc-merchant-category-code/ig-slide-1.html` through `ig-slide-5.html`
  for a fully worked 5-slide arc (hook → mechanism → heuristic → detail →
  CTA) and the template's header comment for the arc breakdown.
- **Instagram carousel slide** (plain, light-touch) — no `templates/` file
  yet; copy the pattern from `reconciliation-drift/ig-slide-{1,2,3}.html`
  instead. A fixed `1080x1080` **exactly square** `.slide` (Instagram's own
  requirement, not a style choice), **dark theme** (Ink background,
  White-on-Ink — the other approved pairing, distinct from the light
  Paper card/doc backgrounds above), a swipe cue on every slide but the
  last, a CTA + "Link in bio" block on the last slide. See "Exporting to
  PNG" below for the square-specific export steps — this shape needs two
  extra things card/doc don't: a fixed height instead of autocropped
  variable height, and a manual crop-to-exact-square safety step.

Both share the same brand tokens (see `brand-identity/README.txt` for the
canonical source — don't hand-copy values from memory, re-check there if
the kit ever updates):

| token | hex | use |
|---|---|---|
| `--ink` | `#080D18` | primary text, dark surfaces |
| `--signal` | `#2F55E8` | the one accent — the failure hop, the retry, links |
| `--paper` | `#F1F3F7` | the card's own background |
| `--slate` | `#5B6472` | secondary/muted text |

Typeface is Inter, loaded from Google Fonts (`family=Inter:opsz,wght@...`)
— this is the one external host the Artifact/export pipeline can reach,
so don't swap in a different font host.

Every card ends with the same footer: `THE FINTECH ENGINEER` on the left,
`linkedin.com/company/the-fintech-engineer` on the right, separated by a
hairline rule. Keep this — it's the only piece of every export that's
non-negotiable.

## Building a new one

1. Copy the template that fits (`card-template.html` for one visual claim,
   `doc-template.html` for a full post-as-document, `collage-card-template.html`
   / `collage-ig-slide-template.html` for the denser editorial-collage hook
   treatment — see "The pattern" above for when to reach for the collage
   variant instead of the plain one).
2. Fill in the marked slots. For a diagram, hand-author inline `<svg>` —
   don't reach for a charting/diagram library. Load the `artifact-diagramming`
   skill for the inline-SVG conventions (viewBox sizing, arrow markers,
   label legibility, "one figure, one claim") before drawing anything
   non-trivial.
3. Open the file directly in a browser to check layout before exporting —
   faster than round-tripping through the export script.
4. Export (see below).

**Diagram content rule:** draw the mechanism the post's argument hinges
on, not a generic illustration of the topic. `examples/retry-trace.html`
works because it shows the exact hop (a lost response, then a retry with
no idempotency key) that turns into a duplicate charge — a reader can
point at the frame where it breaks. Reserve `--signal` for that one hop;
everything else stays ink/slate so the accent actually reads as "look
here."

**Instagram carousel specifics** (see `reconciliation-drift/ig-slide-*.html`):

- Structure `.slide` as a column flexbox: `head-row` at the top,
  `footer-row` at the bottom, and *everything else* wrapped in one
  `.content{ flex:1; display:flex; flex-direction:column;
  justify-content:center; }` block in between. **Vertically center that
  content — don't top-align it.** A short amount of copy on a fixed
  square canvas always leaves whitespace; centering splits it evenly
  above and below, which reads as deliberate. An earlier version of this
  pattern top-aligned the content and pinned the footer with
  `margin-top:auto` alone, which dumped all the leftover space into one
  large, obviously-dead gap sitting directly above the footer — it read
  as broken, not minimal. Don't reintroduce that.
- Give `.slide` both `width:1080px` and a fixed `height:1080px` (plus
  `overflow:hidden` as a safety net) rather than letting content
  determine height the way card/doc do — every slide in a set needs to
  crop to the *same* size.
- Swap the mark SVG's non-accent brackets from ink (`#080D18`) to paper
  (`#F1F3F7`) fill so the logo reads on the dark background.

## Exporting to PNG

```
python3 export_png.py <input.html> <output.png> [--scale 2] [--window W,H]
```

- Renders the HTML in headless Chrome, then autocrops any leftover white
  margin so the output is a tight fit.
- **Set `--window`'s width to exactly the card's CSS `width`** (e.g. `1080`
  for `card-template.html`, `920` for `doc-template.html`) — `body` has no
  side padding and the card has `margin:0 auto`, so a matching window width
  means zero horizontal crop and the paper background runs edge to edge,
  left and right, with no white sliver at the sides.
- Set the window's **height** generously oversized (content is variable-
  height and top-aligned, so excess height is just white space below the
  card, which the autocrop step trims back to nothing) — `2400` covers a
  single card-template image; a long doc-template post may need `3400`+.
  If the output looks clipped at the bottom, re-run with a taller height.
- `--scale` is the device pixel ratio — default `2` for crisp embedding on
  LinkedIn; drop to `1` only for a quick low-stakes preview.
- Requires a local Google Chrome install and Pillow (`pip install pillow`
  if `python3 -c "import PIL"` fails).

Example:

```
python3 export_png.py examples/retry-trace.html examples/retry-trace.png --window=1080,2400
python3 export_png.py examples/retry-post.html examples/retry-post.png --window=920,3400
```

**Instagram square slides need one extra step.** `--window` only needs
to be slightly taller than the fixed `1080x1080` canvas (`1080,1180`),
but the autocrop isn't pixel-perfect — it can land a few pixels off
(e.g. `2160x2184` instead of an exact `2160x2160` at `--scale 2`), which
is close enough to look fine at a glance but isn't actually 1:1. Always
check the exported file's exact size and, if it's off, center-crop it to
a true square as a final step:

```
python3 export_png.py reconciliation-drift/ig-slide-1.html reconciliation-drift/ig-slide-1.png --window=1080,1180
```

```python
from PIL import Image
im = Image.open(path)
w, h = im.size
if w != h:
    top = (h - w) // 2
    im.crop((0, top, w, top + w)).save(path)
```

### Why the card is flat, not floating

An earlier version of these templates centered the card on an oversized
white canvas with a drop shadow and rounded corners, meant for previewing
in an Artifact gallery. That's wrong for the actual upload: LinkedIn (and
most platforms) render the image as a plain rectangle, so a "floating
card on white" export ships with dead white space and a shadow baked into
what should be a clean, full-bleed asset — it looks unfinished and doesn't
crop the way you'd expect at upload time. Keep `border-radius`, `box-shadow`,
and any outer body padding off the `.card`/`.doc` element. If you want a
softer look for some other destination (a slide, a portfolio page), do
that centering/shadow treatment in *that* destination's own container —
never bake it into the exported PNG itself.

## Where output goes

Two locations, for two different purposes — don't collapse them into one:

- **`post-images/<slug>/*.html` and `*.png`** — the editable sources and
  their raw exports. Every diagram for a post lives here, flat, one HTML
  + one PNG per image (`post-images/eventual-consistency-moving-money/`
  is a fully worked example with seven diagrams, a hero card and a
  5-slide carousel). This is where you iterate: edit the HTML, re-run
  `export_png.py`, re-check. Never publish straight from here.
- **`posts/<date>-<slug>/<channel>/images/*.png`** — the finished,
  approved copies, sorted into the channel that actually uses them (see
  the top-level project `README.md`'s "Per-channel folder layout"). A
  card built for the LinkedIn post goes in `linkedin/images/`, an IG
  carousel slide goes in `instagram/images/`, a Substack flow diagram
  goes in `substack/images/`. These are the files that get uploaded to
  LinkedIn/Instagram/Substack or fed into the n8n posting workflow.

Once a PNG in `post-images/<slug>/` passes the QA checklist below, copy
it (don't move it — keep the editable source tree intact) into the
matching channel folder under `posts/`. If you edit and re-export after
copying, re-copy to keep the two in sync.

## Diagram QA checklist — before calling an SVG diagram done

Every diagram bug found in practice so far has been one of these four.
Check all four on the **actual exported PNG at full resolution** — the
in-browser preview pane is often narrower than the 1080/1920px canvas
and will silently clip or compress problems into invisibility. Read the
exported file back with an image-reading tool and look at it at full
size before considering the diagram finished.

1. **Every arrow starts and ends on a real, visible shape.** An arrow
   whose `x1,y1` is a bare coordinate with no box, lifeline, or other
   drawn element behind it reads as "coming from nowhere" — a real bug
   found and fixed in this project's own carousel (a "commit" arrow was
   floating in empty space with only a text label nearby, not a shape).
   If two things need to happen "at the same time" from two different
   sources into one destination (a race, a fan-in), don't invent ad hoc
   diagonal lines between arbitrary points — use the sequence-diagram
   pattern instead: draw each participant as a box up top, drop a dashed
   vertical lifeline straight down from each one, and draw every
   horizontal arrow strictly *between two lifelines*. That's what
   `race-trace.html` / the fixed `ig-slide-2.html` do, and it's
   structurally impossible to get a floating arrow out of it, because
   every arrow's start and end x-coordinate is pinned to a lifeline that
   itself traces back to a box.
2. **No two boxes overlap.** When laying out N boxes in a row, compute
   positions from a single width+gap formula (e.g. `x = margin + i *
   (width + gap)`) rather than eyeballing each `x` by hand — a manual
   layout is exactly how two adjacent boxes (`Fraud` / `Customer
   timeline` in `sync-coupling-trap.html`) ended up 20px into each
   other. Do the arithmetic once, then generate all N positions from it.
3. **No text sits on top of a line it isn't labeling a fixed point on.**
   A label placed at the exact midpoint of a diagonal or long line reads
   as struck-through. Two acceptable fixes, in order of preference:
   (a) move the label off the line's path entirely — into whitespace
   below the source box, as its own caption, not fighting the line's
   trajectory; (b) if the label must sit near a specific point on a
   *short, mostly-static* line (like a "SAME INSTANT" divider), mask a
   small background rect behind just that text, sized tightly to the
   text's own bounding box. Never mask a rect over the middle of a long
   directional arrow — that's what produces the "floating disconnected
   segment" bug in point 1; a mask is for decorative dividers, not for
   arrows that are supposed to read as one continuous path.
4. **Every caption/label is inside the section it's labeling, not
   floating near it.** A stray word like "eventual" sitting in open
   whitespace to the side of a box row doesn't read as labeling that
   row — it reads as a leftover fragment. Give it a full caption
   matching its counterpart's style (e.g. if the strongly-consistent
   group has a boxed "STRONGLY CONSISTENT" header, the eventually-
   consistent group needs an equally complete "EVENTUALLY CONSISTENT ·
   CAN CATCH UP LATER" caption, placed where it can't be crossed by any
   arrow — typically below the row it describes, after all arrows have
   already terminated).
