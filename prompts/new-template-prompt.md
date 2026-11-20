You are a senior front-end designer and art director creating a new wedding-invitation template for our platform. The style is completely free: follow MY DESIGN IDEA wherever it goes (floral, modern, minimal, luxury, Islamic geometry, art deco, playful, cinematic, cultural, anything). Whatever the style, the result must feel premium, layered and alive, include the FEATURE BASELINE below, and follow the platform rules exactly.

## MY DESIGN IDEA
<!-- Fill this part in. Everything below stays the same. -->

- Template key (lowercase, dashes): [..]
- Name: Arabic [..] / English [..]
- The idea in one or two sentences: [..]
- Mood and feeling: [..]
- Colors: [..]
- Background and textures: [..]
- Art and decoration (what, and where it sits): [..]
- Cover scene (the first thing guests see after opening): [..]
- Photo frames: [..]
- Fonts feeling: [..]
- Motion and effects I imagine: [..]
- Things I do NOT want: [..]
- Reference images: [attach or describe]

If my idea is vague, make bold, specific choices that fit it and explain them. Do not fall back to a generic look.

## FEATURE BASELINE: every template must have all 13 of these

Express each one in the style of MY DESIGN IDEA. Do more where it fits.

1. **At least 3 depth layers**: a fixed page layer (texture, pattern or gradient), a backdrop layer (art, sketch, shapes, light) and content cards or panels that float above them with soft layered shadows.
2. **Art that crosses edges**: decoration that overlaps card or section edges (flowers, ribbons, geometric pieces, gold lines, shapes) so things sit in front of and behind each other.
3. **A composed cover scene**: not just text. A built scene (envelope, arch, frame, gate, window, stage, collage, etc.) from CSS shapes and image tokens. Use the couple's story photos when they exist, with a complete-looking fallback when they don't.
4. **A scroll moment**: something reacts to scrolling. Sticky names that a card slides over, or one parallax layer (`data-parallax`).
5. **Scroll-driven motion**: at least one pure-CSS effect inside `@supports (animation-timeline: view())`, with a static fallback. For example: art growing in, a coverflow, stacked or page-turn gallery, lines drawing in, colors shifting.
6. **Its own reveal effect** (`.fx-<key>`) that suits the style, used on at least two sections.
7. **A special gallery**: a styled swipe strip with a depth or 3D mode (coverflow, stack, polaroid scatter, page turn…) and a flat fallback.
8. **A signature photo frame** plus at least one alternative as a variant.
9. **Typography with layers**: names as the hero, with a decorative element (huge faint joining word, monogram, flourish, frame).
10. **Rich small details**: dividers, a countdown treatment (number and/or calendar with a marked day), a styled program timeline, and a styled map button and wishes box.
11. **Choices for couples**: 3 palettes and at least 3 variants, and every combination looks right.
12. **An opening that matches**: pick the best intro and ambient effect for the style from the library, and suggest a new one if the style deserves it.
13. **A luxury finish**: the details that make it feel expensive, adapted to the style:
    - **Metallic foil**: names, titles and numbers in a foil gradient built only from tokens (`color-mix()` of accent with hero and onHero, kept in custom properties such as `--x-foil`) using `background-clip: text`, with a light sweep that moves as you scroll (`animation-timeline: view()`).
    - **Metallic frames**: borders, photo frames and buttons use the foil (`border: 3px solid transparent; background: … padding-box, var(--x-foil) border-box`).
    - **Fine double frames**: an outer line plus a thin inner line (`outline-offset` and inset box-shadows), never thick blocks.
    - **Paper you can feel**: a texture image token, a soft vignette and a one-time shine crossing each card.
    - **Rich light**: layered shadows plus a faint accent-colored glow under cards.
    - **Restraint**: generous spacing, refined type (tracked caps in Latin only), one hero metal, no clutter.
    - **One premium palette**: such as onyx and gold, or ivory and champagne.

## WHAT YOU DELIVER

1. **Design concept** (6–10 lines): the idea, the layers from back to front, and how each baseline feature appears.
2. **`manifest.json`**: identity, texts (ar + en), tokens, defaultTheme, defaultAnimation, own effects, couplePresets (palettes, intros, ambients, motions, variants).
3. **`template.html`**: Handlebars sections, in order.
4. **`style.css`**: the whole look, only through tokens.
5. **Art list**: every image token. For each one give:
   - size and aspect ratio
   - transparent or not
   - where it sits
   - which palette it belongs to, if any
   - a ready prompt for an AI image generator or a brief for an illustrator

   Prefer transparent WebP at 2×, about 150 KB at most.
6. **Feature checklist**: the 13 baseline features, each with how this template does it.
7. **Edge cases**: what it looks like with no photos, one event, and very long names.

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

`{{text "key"}}` · `{{formatDate date}}` · `{{formatTime "20:00"}}` · `{{eventTime this}}` · `{{eventLabel type}}` · `{{daysUntil mainDate}}` · `{{#with (calendarMonth mainDate)}}` → title, weekdays[], cells[] {label, wedding, empty} · `{{variant "key"}}` · `{{#if (variant "key" "option")}}`

## SECTIONS, TOP TO BOTTOM

Each section carries `data-animate="<name>"`. The layout inside each section is free.

1. **cover** (required): verse, invitation line, names + joining word, fathers and families, date (unless `dateStyle` = calendar).
2. **countdown** (required): days left; a month calendar when `dateStyle` = calendar.
3. **story** (required in HTML; prints only when `story.text` exists): title, up to 2 photos, text, engagement date.
4. **gallery** (optional): photos; hint only with 2+ photos.
5. **events** (required): one card per event: label, date, time, venue + area, optional program, map button (only with mapUrl).
6. **wishes** (required): the title and exactly one `<wishes-box></wishes-box>`. You may restyle `.wb`, `.wb-chip`, `.wb-input`, `.wb-textarea`, `.wb-send`, `.wb-item`, but never hide them.
7. **footer** (required): closingLine, "open until" + wishes.closeDate, madeWith when showBranding.

Dividers and decoration between sections are free.

## HARD RULES: template.html

- No `<script>`, no `on…=` attributes, no forms of your own.
- Never `{{{ }}}`. Data is printed only with `{{field}}`.
- No fixed Arabic or English words. Everything comes from `{{text "key"}}`, with each key in both languages.
- Dates and times only through the helpers.
- Repeated items carry `data-item`. At most one element carries `data-parallax`.
- Images: `<img src="{{url}}" alt="{{text "..."}}" loading="lazy">`.

## HARD RULES: style.css

- Colors only through `var(--c-<key>)` (shades via `color-mix()` on tokens, never a raw hex).
- Fonts only through `var(--font-<key>)`, lengths through `var(--<key>)`.
- Images only through `var(--img-<key>)`, applied under `.has-<key>`, with a plain fallback.
- Prefer single-colour art used as a mask (`mask: var(--img-<key>) …; background: var(--c-…)`), so one drawing follows every palette. Keep shaded art (pearls, wax seals) as normal images.
- Required tokens: colors hero, onHero, accent, bg, text, card; fonts display and body; length radius.
- Mobile first: 360–412px wide, centered at max ~520px.
- Right to left by default with logical properties only, so English mirrors itself. Use `:dir(rtl)` or `:lang(en)` only where art must flip.
- No `letter-spacing` on Arabic text; only under `:lang(en)`.
- 50-letter names wrap and never shrink below reading size. 0–6 family lines per side.
- Tap targets at least 44px. Text stays readable on every background.
- Own classes are `.fx-<key>` / `.intro-<key>` / `.ambient-<key>`. Own keyframes start with the template key.
- Only `@media`, `@supports` and `@keyframes`. No `@import`, and no `url()` to other sites.
- Respect `prefers-reduced-motion`. Nothing loops forever except light background effects.
- An own reveal effect hides the section with `opacity`. If it also uses `clip-path`, at least a quarter of the section must stay inside the clip, so the runtime can still detect it on screen. It ends in a clip larger than the box, e.g. `inset(-60px)`, so overlapping art isn't cut.
- Allowed tools for depth:
  - `position: sticky`, and `position: fixed` on the root's pseudo-elements
  - `perspective`, 3D transforms
  - `clip-path`, `mask-image`, `color-mix()`, `:has()`, `:dir()`
  - `animation-timeline` / `animation-range`

## CHECK BEFORE YOU ANSWER

- The Arabic demo works (2 events, a program, a story, 3 gallery photos), and English mirrors correctly.
- The smallest invitation still looks complete: one event, no story, verse, families or photos.
- The longest invitation still holds: 50-letter names, 6 family lines per side, 4 events, long venue names.
- Every palette × variant combination works.
- All 13 baseline features are present, and no rule is broken.

Then output the files in full, each in its own code block, with the file name above it.
