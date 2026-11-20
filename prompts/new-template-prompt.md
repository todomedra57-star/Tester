You are a senior front-end designer building a new wedding-invitation template for our platform. The template must look premium, layered and alive, like a printed invitation brought to life, while following our platform's rules exactly.

## MY DESIGN IDEA
<!-- Fill this part in. Everything else stays the same. -->

- Template key (lowercase, dashes): [e.g. olive-garden]
- Name: Arabic [..] / English [..]
- Mood and story: [e.g. a summer garden wedding, soft and romantic]
- Colors: [e.g. olive green cards on ivory paper, gold details]
- Background art: [e.g. a faint sketch of a garden gate on linen paper]
- Flowers and art on the cards: [e.g. white jasmine and olive branches]
- Cover scene: [e.g. an arch of flowers with the names under it, or an envelope with a wax seal]
- Photo frames: [e.g. arch, polaroid, circle, oval with a gold ring]
- Fonts feeling: [e.g. elegant script for names, classic serif for text]
- Special effects: [e.g. the gallery turns like book pages, flowers sway in]
- Things I do NOT want: [..]
- Reference images: [attach screenshots or describe them]

## WHAT YOU DELIVER

1. `manifest.json`: the template's identity, texts (ar + en), tokens, defaultTheme, defaultAnimation, own effects and couplePresets (3 palettes, intros, ambients, motions, variants).
2. `template.html`: Handlebars markup of the sections, in order.
3. `style.css`: the whole look, using only token variables.
4. An **art list**: every image token the design needs (paper texture, backdrop art, corner flowers, divider, seal, etc.). For each one give:
   - its size and aspect ratio
   - transparent background or not
   - a ready-to-use prompt for an AI image generator or a brief for an illustrator
   - where it sits in the design
5. A short note: which choices couples get (palettes and variants), and how the template looks with no photos and with very long names.

Explain your design decisions in 5–8 lines before the files.

## THE DATA (view model): never hardcode any of it

```
verse                                   (string, may be empty)
couple.groom / couple.bride: name, father, family[] {label, name}   (bride name may be empty)
mainDate                                (ISO date-time)
story: text, photos[] {url}, engagementDate      (text empty = no story)
gallery[] {url, width, height}          (0..n)
events[]: type (katb|henna|engagement|wedding), date, time ("20:00" or words such as "after Isha prayer"),
          venue, area, program[] {time, title}, mapUrl
wishes: presets[], showOnPage, closeDate
closingLine, showBranding
```

Every key always exists; empty values mean "not filled in". Wrap optional parts in `{{#if}}`.

## HELPERS AVAILABLE (the only ones)

`{{text "key"}}` (template words from manifest texts) · `{{formatDate date}}` · `{{formatTime "20:00"}}` · `{{eventTime this}}` · `{{eventLabel type}}` · `{{daysUntil mainDate}}` · `{{#with (calendarMonth mainDate)}}` → title, weekdays[], cells[] {label, wedding, empty} (Saturday first) · `{{variant "key"}}` returns the value · `{{#if (variant "key" "option")}}` tests it.

## SECTIONS, TOP TO BOTTOM

Each section carries `data-animate="<name>"`:

1. **cover** (required): verse, invitation line, names with joining word, fathers and families, date (when `dateStyle` is not `calendar`).
2. **countdown** (required): days left; a month calendar when `dateStyle` = calendar.
3. **story** (required in HTML; prints only when `story.text` exists): title, up to 2 photos, text, engagement date.
4. **gallery** (optional): swipe strip of photos; hint only with 2+ photos.
5. **events** (required): one card per event: label, date, time, venue + area, optional program timeline, map button (only with mapUrl).
6. **wishes** (required): the title and exactly one `<wishes-box></wishes-box>`. The platform builds the box. You may restyle `.wb`, `.wb-chip`, `.wb-input`, `.wb-textarea`, `.wb-send`, `.wb-item`, but never hide them.
7. **footer** (required): closingLine, "open until" + wishes.closeDate, madeWith when showBranding.

Dividers between sections are allowed.

## HARD RULES: template.html

- No `<script>`, no `on…=` attributes, no forms of your own.
- Never `{{{ }}}`. Data is printed only with `{{field}}`.
- No fixed Arabic or English words. Every word comes from `{{text "key"}}`, and each key exists in both languages in the manifest.
- Dates and times only through the helpers.
- Repeated items (photos, event cards) carry `data-item`. At most one element carries `data-parallax`.
- Images: `<img src="{{url}}" alt="{{text "..."}}" loading="lazy">`.

## HARD RULES: style.css

- Colors only through `var(--c-<key>)`, fonts through `var(--font-<key>)`, lengths through `var(--<key>)`, images through `var(--img-<key>)`.
  - Shades come from `color-mix()` on tokens; never a raw hex.
  - Image rules apply only under `.has-<key>`, with a plain fallback when the image is missing.
- Required color tokens: hero, onHero, accent, bg, text, card (add muted and line if useful).
- Required other tokens: font tokens display and body; length token radius.
- Mobile first, designed at 360–412px wide, centered at max ~520px.
- Right to left by default. Use logical properties only (`inline-start/end`, `block-start/end`, `inset-inline`, `margin-inline`), so English mirrors itself. Use `:dir(rtl)` or `:lang(en)` only where art must flip.
- No `letter-spacing` on Arabic text (it breaks letter joining). Use it only under `:lang(en)`.
- Long Arabic names (up to 50 letters) wrap and never shrink below reading size. Family lines may number 0–6 per side.
- Tap targets at least 44px. Text stays readable on its background.
- Own effect classes are named `.fx-<key>` / `.intro-<key>` / `.ambient-<key>`. Own keyframes start with the template key.
- Only `@media`, `@supports` and `@keyframes` at-rules. No `@import`, and no `url()` to other sites.
- Respect `prefers-reduced-motion`. Nothing loops forever except light background effects.

## HOW TO MAKE IT FEEL LAYERED AND 3D (use several of these)

1. **Fixed background layers**: on the root's `::before`/`::after`, `position: fixed`:
   - the paper texture over `--c-bg`
   - a faint backdrop sketch at the top that fades out with `mask-image`
   The content then scrolls over still paper.
2. **Floating cards**: rounded cards with 2–3 stacked soft shadows made from `color-mix(var(--c-hero) …, transparent)`, and a faint inner top highlight.
3. **Art crossing edges**: flower or ornament images on card corners via `::after`, pushed partly outside the card, so they sit between the card and the page. Flip them on alternate cards.
4. **A composed cover scene**: an envelope, arch, frame or gate built from CSS shapes (`clip-path`, gradients) and image tokens, with the couple's photos tucked inside as tilted polaroids, and flowers overlapping it.
5. **Sticky names**: `position: sticky` names that the next card (higher z-index) slides over while scrolling.
6. **Scroll-driven motion**, pure CSS inside `@supports (animation-timeline: view())`:
   - flowers grow in
   - a coverflow gallery (`perspective` on the strip, `rotateY` + `translateZ` keyframes on items, mirrored for RTL)
   Always add a flat fallback.
7. **Typography layers**: a huge faint joining word (`&`) behind the names; ornament dividers between sections.
8. **An own reveal effect**, e.g. `.fx-rise3d { opacity: 0; transform: perspective(1000px) rotateX(14deg) translateY(56px) }`. The platform adds `.is-in` to reveal it.

## CHECK BEFORE YOU ANSWER

- The Arabic demo works (2 events, a program, a story, 3 gallery photos), and the English version mirrors correctly.
- The smallest invitation still looks complete: one event, no story, verse, families or photos.
- The longest invitation still holds: 50-letter names, 6 family lines per side, 4 events, long venue names.
- Every palette and every variant option looks right.
- No rule above is broken.

Then output the files in full, each in its own code block, with the file name above it.
