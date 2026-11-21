You are a senior front-end designer and art director creating a new wedding-invitation template for our platform. The style is completely free: follow MY DESIGN IDEA wherever it goes (floral, modern, minimal, luxury, Islamic geometry, art deco, playful, cinematic, cultural, anything). Whatever the style, the result must feel premium, layered and alive, include the FEATURE BASELINE and the COUPLE OPTIONS below, and follow the platform rules exactly.

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

## FEATURE BASELINE: every template has all 13

Express each one in the style of MY DESIGN IDEA. Do more where it fits.

1. **At least 3 depth layers**: a fixed page layer (texture, pattern or gradient), a backdrop layer (art, sketch, shapes, light) and cards or panels floating above them with soft layered shadows.
2. **Art that crosses edges**: decoration that overlaps card or section edges (flowers, ribbons, geometric pieces, gold lines), so things sit in front of and behind each other.
3. **A composed cover scene**: not just text. A built scene (envelope, arch, frame, gate, window, stage, landscape, collage…) from CSS shapes and image tokens. Use the couple's story photos when they exist, and look complete when they don't. The scene grows with long names; the art stays below or around the text, never under it.
4. **A scroll moment**: sticky names that a card slides over, layers moving at different speeds, or one `data-parallax` layer.
5. **Scroll-driven motion**: at least one pure-CSS effect inside `@supports (animation-timeline: view())`, with a static fallback. For example: art growing in, a coverflow or fanned gallery, rosettes turning, curtains parting, lines drawing in.
6. **Its own reveal effect** (`.fx-<key>`) that suits the style, used on at least two sections.
7. **A special gallery**: a swipe strip with a 3D or depth mode and a flat fallback.
8. **A signature photo frame**: the template's own look, plus the frame options listed below.
9. **Typography with layers**: names as the hero, with a decorative element (huge faint joining word, monogram, flourish, frame).
10. **Rich small details**: dividers, a countdown treatment (number and/or calendar with a marked day), a styled program timeline, and a styled map button and wishes box.
11. **An opening that matches**: pick the best intro and ambient effect from the library, and suggest a new one if the style deserves it.
12. **A luxury finish**, adapted to the style:
    - **Metallic foil**: names, titles and numbers in a foil gradient built only from tokens, kept in a custom property (`--<p>-foil`, a `color-mix()` of accent with hero and a light token). Apply it with `background-clip: text`, plus a light sweep tied to the scroll (`animation-timeline: view()`).
    - **Metallic frames**: borders, photo frames and buttons use the foil (`border: 3px solid transparent; background: … padding-box, var(--<p>-foil) border-box`).
    - **Fine double frames**: an outer line plus a thin inner line (`outline-offset`, inset box-shadows), never thick blocks.
    - **Paper you can feel**: a texture image token, a soft vignette and a one-time shine crossing each card.
    - **Rich light**: layered shadows plus a faint accent-coloured glow under cards.
    - **Sparkles**: a few four-point glints in foil that twinkle as they scroll by.
    - **Restraint**: generous spacing, refined type (tracked caps in Latin only), one hero metal, no clutter.
13. **Nothing looks empty**: blocks the couple did not fill (verse, families, photos, story) disappear completely, and their card goes with them (`:not(:has(p, figure)) { display: none }`).

## COUPLE OPTIONS: every template offers all of these

Each option is a variant token printed on the root element as `data-<option>="{{variant "<option>"}}"` and styled with `.<root>[data-<option>="value"]`. Names in ar + en for every option.

| Option | Values |
|---|---|
| `coverLayout` | 3 layouts of the cover scene, e.g. full scene · framed panel · names only |
| `ornament` | `rich` · `refined` (hides the extra decoration) · `opulent` (gold glow on cards, names and photos) |
| `dateStyle` | `badge` · `ribbon` (notched, with a fine accent outline so it shows on any background) · `frame` (double line) · `line` (between hairlines) · `calendar` (hides the cover date, shows the month in the countdown) |
| `photoFrame` | the template's own 2–3 frames + `heart` · `hexagon` · `polaroid` |
| `galleryStyle` | `coverflow` · `stack` (fanned) · `strip` · `grid` (mosaic, first photo wide) · `scatter` (tilted polaroids); hide the swipe hint for grid and scatter |
| `photoTone` | `natural` · `golden` · `palette` · `noir`. Golden and palette: the photo frame gets the foil or a hero→accent gradient as background, and the image uses `mix-blend-mode: luminosity`. Noir: `grayscale(1)`. Only when an image exists (`:has(img)`) |
| `entrance` | `cinematic` (the cover builds piece by piece after opening: each piece fades in from `opacity: 0; scale: .92; filter: blur(10px)` with a growing delay) · `gentle` (fade only) · `none`. Not cinematic/gentle → also the **choreographed reveals**: in each section the title comes first, a thin accent line draws out under it (`::after`, `scaleX(0 → 1)`), then the text fades in |
| `metal` | `palette` · `champagne` · `roseGold` · `silver` · `iridescent`: redefine the foil from the accent with relative colours (`oklch(from var(--c-accent) …)`) inside `@supports (color: oklch(from red l c h))` |
| `fontPair` | `template` · `classic` · `modern` · `script` · `geometric`: extra font tokens (`classic`, `classicLatin`, …); the option sets `--font-display` and `--font-latin` to them |

Also:
- **5 palettes or more**, including at least one dark palette and gold, silver and rose-gold metals. Every palette sets every colour token.
- **Shimmering frames**: in `rich` and `opulent`, gilded photo frames get a conic-gradient background whose angle is a registered `@property` animated by the scroll, so light runs around the frame. Only when the frame holds an image.

## WHAT YOU DELIVER

1. **Design concept** (6–10 lines): the idea, the layers from back to front, and how each baseline feature appears.
2. **`manifest.json`**: identity, texts (ar + en), tokens (colours, fonts, lengths, images, variants), `defaultTheme` (a value for every token), `defaultAnimation`, own `effects`, and `couplePresets` (palettes, intros, ambients, motions, variants).
3. **`template.html`**: Handlebars sections, in order.
4. **`style.css`**: the whole look, only through tokens.
5. **Art list**: every image token. For each one give:
   - size and aspect ratio
   - transparent or not, and whether it is used as a mask
   - where it sits
   - a ready prompt for an AI image generator or a brief for an illustrator

   Prefer transparent WebP at 2×, about 150 KB at most.
6. **Feature checklist**: the 13 baseline features and every couple option, each with how this template does it.
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

- No `<script>`, no `on…=` attributes, no forms of your own, no `<link>` or `<style>`.
- Never `{{{ }}}`. Data is printed only with `{{field}}`.
- No fixed Arabic or English words. Everything comes from `{{text "key"}}`, and every key exists in both languages.
- Dates and times only through the helpers.
- Repeated items carry `data-item`. At most one element carries `data-parallax`.
- Images: `<img src="{{url}}" alt="{{text "..."}}" loading="lazy">`.
- Every variant in the manifest is printed on the root element as a data attribute.

## HARD RULES: style.css

- **Colours:**
  - Only through `var(--c-<key>)`, never a raw hex, `rgb()` or named colour.
  - Masks too: write `linear-gradient(var(--c-text), transparent)`, not `#000`.
  - Shades come from `color-mix()` on tokens. Relative colours from tokens (`oklch(from var(--c-accent) l c h)`) are allowed inside `@supports`.
- **Fonts, lengths, images:**
  - Fonts only through `var(--font-<key>)`, lengths through `var(--<key>)`.
  - Images only through `var(--img-<key>)`, applied under `.has-<key>`, with a plain fallback.
  - Prefer single-colour art used as a mask (`mask: var(--img-<key>) …; background: var(--c-…)`), so one drawing follows every palette. Keep shaded art (pearls, wax seals) as normal images.
- **Required tokens:** colours hero, onHero, accent, bg, text, card; fonts display and body; length radius.
- **Layout:**
  - Mobile first: 360–412px wide, centered at max ~520px.
  - Right to left by default with logical properties only (no `left`, `right`, `margin-left`, `text-align: left`…), so English mirrors itself. Use `:dir(rtl)` or `:lang(en)` only where art must flip.
  - No `letter-spacing` on Arabic text; only under `:lang(en)`.
  - 50-letter names wrap and never shrink below reading size. 0–6 family lines per side.
  - Tap targets at least 44px. Text stays readable on every background, in every palette.
- **Naming:**
  - Own classes are `.fx-<key>` / `.intro-<key>` / `.ambient-<key>`, and match the manifest effects.
  - Own keyframes start with the full template key (e.g. `desert-bloom-…`) or an own effect key.
- **At-rules:**
  - Only `@media`, `@supports`, `@keyframes` and `@property`. No `@import`, no `url()`.
- **Motion:**
  - Respect `prefers-reduced-motion`. Nothing loops forever except light background effects.
  - An own reveal effect hides the section with `opacity`. If it also uses `clip-path`, at least a quarter of the section stays inside the clip, so the runtime still detects it on screen. It ends in a clip larger than the box (`inset(-60px)`), so overlapping art isn't cut.
- **Allowed tools for depth:**
  - `position: sticky`, and `position: fixed` on the root's pseudo-elements
  - `perspective`, 3D transforms
  - `clip-path`, `mask`, `color-mix()`, `:has()`, `:dir()`, `backdrop-filter`
  - `animation-timeline` / `animation-range`, `@property`

## CHECK BEFORE YOU ANSWER

- The Arabic demo works (2 events, a program, a story, 3 gallery photos), and English mirrors correctly.
- The smallest invitation looks complete: one event, no story, verse, families or photos, and no empty cards.
- The longest invitation holds: 50-letter names, 6 family lines per side, 4 events, long venue names, with nothing overlapping the names.
- Every palette and every option value works, including the dark palette.
- Every baseline feature and every couple option is present, and no rule is broken. The template must pass `node tools/check-templates.mjs <key>` with no errors.

Then output the files in full, each in its own code block, with the file name above it.
