"""Scene kit: builds a calm, multi-layer "diorama" invitation template from a config.

Every template made with the kit gets the Nile Royale treatment:
  * a cover scene of many depth planes; each plane drifts at its own speed as the
    cover scrolls away (CSS scroll timeline, transform only, run on the GPU),
  * its own opening (runtime intro), its own countdown emblem, its own photo veils
    that open once, its own events path with a traveller that rides along (sticky),
  * one-time reveals only, no loops, nothing that repaints while scrolling.

Written CSS uses "@@" for the class prefix and "@K@" for the template key; the
build replaces them. Used by tools/build-scenes.py.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIB = ROOT / "preview" / "library"


def kebab(s):
    return re.sub(r"([A-Z])", lambda m: "-" + m.group(1).lower(), s)


def aspect(lib):
    m = re.search(r'viewBox="([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+)"', (LIB / f"{lib}.svg").read_text())
    return f"{float(m.group(3)):g} / {float(m.group(4)):g}"


def mix(a, b, p):
    return f"color-mix(in srgb, {a} {p}%, {b})"


SHADE, FOIL, GLOW = "var(--@@-shade)", "var(--@@-foil)", "var(--@@-glow)"


# ----------------------------------------------------------------- layers
class Scene:
    """Collects the cover planes (back to front), their markup, CSS and image tokens."""

    def __init__(self):
        self.html, self.css, self.images = [], [], {}

    def lay(self, name, css, dy=0, dx=0, inner="", decor=False):
        cls = f"@@-layer @@-{name}" + (" @@-decor" if decor else "")
        self.html.append(f'<span class="{cls}" aria-hidden="true">{inner}</span>')
        drift = f" --dy: {dy}px;" + (f" --dx: {dx}px;" if dx else "")
        self.css.append(f".@@-{name} {{{drift} {css} }}")
        if dx:
            self.css.append(f".@@-{name}:dir(rtl) {{ --dx: {-dx}px; }}")
        return self

    def art(self, name, token, lib, box, fill, dy=0, dx=0, pos="center bottom", size="contain", rep="no-repeat", extra="", decor=False, inner="", ar=True):
        """A plane cut from a library drawing (CSS mask) and coloured by tokens."""
        self.images[token] = lib
        asp = f" aspect-ratio: {aspect(lib)};" if ar else ""
        self.lay(name, f"{box};{asp} display: none; background: {fill}; {extra}", dy, dx, inner, decor)
        k = kebab(token)
        self.css.append(f".has-{k} .@@-{name} {{ display: block; -webkit-mask: var(--img-{k}) {pos} / {size} {rep}; mask: var(--img-{k}) {pos} / {size} {rep}; }}")
        return self

    def raw(self, html):
        self.html.append(html)
        return self


def stars(seed, n, col_a, col_b):
    """Deterministic scattered stars as radial gradients (one paint, then still)."""
    import random
    r = random.Random(seed)
    out = []
    for i in range(n):
        s = r.choice((1, 1, 1.2, 1.4, 1.7))
        out.append(f"radial-gradient({s}px {s}px at {r.randint(2, 98)}% {r.randint(2, 96)}%, {col_b if i % 4 == 0 else col_a}, transparent)")
    return ", ".join(out)


# ----------------------------------------------------------------- markup
def template_html(cfg, scene):
    layers = list(scene.html)
    cart = f"""<div class="@@-layer @@-cartouche @@-cartouche--{cfg['cart_mode']}">
          <span class="@@-monogram" aria-hidden="true"></span>
          <p class="@@-lead">{{{{text "lead"}}}}</p>
          <h1 class="@@-names">
            <span class="@@-name">{{{{couple.groom.name}}}}</span>
            {{{{#if couple.bride.name}}}}<span class="@@-and">{{{{text "and"}}}}</span><span class="@@-name">{{{{couple.bride.name}}}}</span>{{{{/if}}}}
          </h1>
          {{{{#unless (variant "dateStyle" "calendar")}}}}<p class="@@-date">{{{{formatDate mainDate}}}}</p>{{{{/unless}}}}
        </div>"""
    layers.insert(cfg["cart_index"], cart)
    stage = "\n        ".join(layers)
    h = f"""<main class="@@" data-cover-layout="{{{{variant "coverLayout"}}}}" data-ornament="{{{{variant "ornament"}}}}" data-date-style="{{{{variant "dateStyle"}}}}" data-photo-frame="{{{{variant "photoFrame"}}}}" data-gallery-style="{{{{variant "galleryStyle"}}}}" data-photo-tone="{{{{variant "photoTone"}}}}" data-entrance="{{{{variant "entrance"}}}}" data-font-pair="{{{{variant "fontPair"}}}}" data-metal="{{{{variant "metal"}}}}">

  <section class="@@-cover" data-animate="cover">
    <!-- {cfg['scene_note']} -->
    <div class="@@-diorama">
      <div class="@@-stage">
        {stage}
        <p class="@@-cue">{{{{text "scrollHint"}}}}</p>
      </div>
    </div>

    <div class="@@-sheet">
      {{{{#if verse}}}}<p class="@@-verse">{{{{verse}}}}</p>{{{{/if}}}}
      <div class="@@-families">
        <div class="@@-family">
          {{{{#if couple.groom.father}}}}<p class="@@-family__label">{{{{text "sonOf"}}}}</p><p class="@@-family__name">{{{{couple.groom.father}}}}</p>{{{{/if}}}}
          {{{{#each couple.groom.family}}}}<p class="@@-family__label">{{{{label}}}}</p><p class="@@-family__name">{{{{name}}}}</p>{{{{/each}}}}
        </div>
        <div class="@@-family">
          {{{{#if couple.bride.father}}}}<p class="@@-family__label">{{{{text "daughterOf"}}}}</p><p class="@@-family__name">{{{{couple.bride.father}}}}</p>{{{{/if}}}}
          {{{{#each couple.bride.family}}}}<p class="@@-family__label">{{{{label}}}}</p><p class="@@-family__name">{{{{name}}}}</p>{{{{/each}}}}
        </div>
      </div>
    </div>
  </section>

  <!-- countdown: {cfg['emblem_note']} -->
  <section class="@@-section @@-countdown" data-animate="countdown">
    <h2 class="@@-title">{{{{text "countdownTitle"}}}}</h2>
    <div class="@@-emblem">
      <span class="@@-emblem__a" aria-hidden="true"></span>
      <span class="@@-emblem__b" aria-hidden="true"></span>
      <span class="@@-emblem__c" aria-hidden="true"></span>
      <p class="@@-count"><span class="@@-count__num">{{{{daysUntil mainDate}}}}</span><span class="@@-count__unit">{{{{text "countdownUnit"}}}}</span></p>
    </div>
    {{{{#if (variant "dateStyle" "calendar")}}}}
      {{{{#with (calendarMonth mainDate)}}}}
        <div class="@@-card @@-cal">
          <p class="@@-cal__title">{{{{title}}}}</p>
          <div class="@@-cal__grid">
            {{{{#each weekdays}}}}<span class="@@-cal__wd">{{{{this}}}}</span>{{{{/each}}}}
            {{{{#each cells}}}}<span class="@@-cal__cell{{{{#if wedding}}}} is-wedding{{{{/if}}}}">{{{{label}}}}</span>{{{{/each}}}}
          </div>
        </div>
      {{{{/with}}}}
    {{{{/if}}}}
  </section>

  {{{{#if story.text}}}}
    <div class="@@-divider" aria-hidden="true"></div>
    <!-- story: {cfg['veil_note']} -->
    <section class="@@-section @@-story" data-animate="story">
      <h2 class="@@-title">{{{{text "storyTitle"}}}}</h2>
      {{{{#if story.photos.length}}}}
        <div class="@@-photos">
          {{{{#each story.photos}}}}
            <figure class="@@-photo" data-item>
              <img src="{{{{url}}}}" alt="{{{{text "storyPhoto"}}}}" loading="lazy">
              <span class="@@-veil @@-veil--a" aria-hidden="true"></span>
              <span class="@@-veil @@-veil--b" aria-hidden="true"></span>
            </figure>
          {{{{/each}}}}
        </div>
      {{{{/if}}}}
      <p class="@@-story__text">{{{{story.text}}}}</p>
      {{{{#if story.engagementDate}}}}<p class="@@-story__date">{{{{text "engagement"}}}} {{{{formatDate story.engagementDate}}}}</p>{{{{/if}}}}
    </section>
  {{{{/if}}}}

  {{{{#if gallery.length}}}}
    <section class="@@-section @@-gallery" data-animate="gallery"{{{{#if (variant "galleryStyle" "carousel")}}}} data-scene="contain"{{{{/if}}}}>
      <div class="@@-gallery__stage">
        <h2 class="@@-title">{{{{text "galleryTitle"}}}}</h2>
        <div class="@@-flow">
          {{{{#each gallery}}}}<figure class="@@-flow__item" data-item><img src="{{{{url}}}}" width="{{{{width}}}}" height="{{{{height}}}}" alt="{{{{text "galleryPhoto"}}}}" loading="lazy"></figure>{{{{/each}}}}
        </div>
        {{{{#if gallery.[1]}}}}<p class="@@-hint">{{{{text "galleryHint"}}}}</p>{{{{/if}}}}
      </div>
    </section>
  {{{{/if}}}}

  <div class="@@-divider" aria-hidden="true"></div>

  <!-- events: {cfg['path_note']} -->
  <section class="@@-section @@-events" data-animate="events">
    <h2 class="@@-title">{{{{text "eventsTitle"}}}}</h2>
    <div class="@@-journey">
      <span class="@@-path" aria-hidden="true"><span class="@@-traveller"></span></span>
      {{{{#each events}}}}
        <article class="@@-card @@-event" data-item>
          <h3 class="@@-event__type">{{{{eventLabel type}}}}</h3>
          <p class="@@-event__date">{{{{formatDate date}}}}</p>
          <p class="@@-event__time">{{{{eventTime this}}}}</p>
          <p class="@@-event__place">{{{{venue}}}}{{{{#if area}}}}{{{{text "listSeparator"}}}}{{{{area}}}}{{{{/if}}}}</p>
          {{{{#if program.length}}}}
            <div class="@@-program">
              <p class="@@-program__title">{{{{text "programTitle"}}}}</p>
              <ol class="@@-program__list">
                {{{{#each program}}}}<li class="@@-program__item"><span class="@@-program__time">{{{{formatTime time}}}}</span><span class="@@-program__what">{{{{title}}}}</span></li>{{{{/each}}}}
              </ol>
            </div>
          {{{{/if}}}}
          {{{{#if mapUrl}}}}<a class="@@-map" href="{{{{mapUrl}}}}" target="_blank" rel="noopener">{{{{text "openMap"}}}}</a>{{{{/if}}}}
        </article>
      {{{{/each}}}}
    </div>
  </section>

  <section class="@@-section @@-wishes" data-animate="wishes">
    <div class="@@-panel">
      <span class="@@-panel__decor" aria-hidden="true"></span>
      <h2 class="@@-title @@-title--panel">{{{{text "wishesTitle"}}}}</h2>
      <wishes-box></wishes-box>
    </div>
  </section>

  <footer class="@@-section @@-footer" data-animate="footer">
    <span class="@@-footer__art" aria-hidden="true"></span>
    <span class="@@-monogram" aria-hidden="true"></span>
    {{{{#if closingLine}}}}<p class="@@-closing">{{{{closingLine}}}}</p>{{{{/if}}}}
    {{{{#if wishes.closeDate}}}}<p class="@@-until">{{{{text "openUntil"}}}} {{{{formatDate wishes.closeDate}}}}</p>{{{{/if}}}}
    {{{{#if showBranding}}}}<p class="@@-brand">{{{{text "madeWith"}}}}</p>{{{{/if}}}}
  </footer>
</main>
"""
    return h


# ----------------------------------------------------------------- shared CSS
BASE_CSS = r"""
/* ---------- base ---------- */
.@@ {
  --@@-gd: color-mix(in srgb, var(--c-accent) 58%, var(--c-hero));
  --@@-gl: color-mix(in srgb, var(--c-accent) 45%, var(--c-card));
  --@@-foil: linear-gradient(115deg, var(--@@-gd) 0%, var(--c-accent) 20%, var(--@@-gl) 34%, var(--c-accent) 46%,
    var(--@@-gd) 60%, var(--c-accent) 76%, var(--@@-gl) 90%, var(--c-accent) 100%);
  --@@-ink: linear-gradient(115deg, var(--c-hero) 0%, var(--c-hero) 38%, var(--@@-gd) 48%, var(--c-accent) 52%, var(--c-hero) 62%, var(--c-hero) 100%);
  --@@-glow: var(--c-card);
  --@@-shade: var(--c-deep);
  --@@-photo-r: var(--radius);
  position: relative;
  isolation: isolate;
  max-inline-size: 520px;
  margin-inline: auto;
  color: var(--c-text);
  font-family: var(--font-body);
  font-size: 16px;
  line-height: 1.75;
  text-align: center;
  overflow-x: clip;
}
@supports (color: oklch(from red l c h)) {
  .@@ { --@@-glow: oklch(from var(--c-accent) 0.96 0.035 h); --@@-shade: oklch(from var(--c-deep) calc(l * 0.62) c h); }
}
.@@ :where(p, h1, h2, h3, ol, figure) { margin: 0; }
.@@::before { content: ""; position: fixed; inset: 0; z-index: -2;
  background: radial-gradient(140% 100% at 50% 40%, transparent 55%, color-mix(in srgb, var(--c-text) 10%, transparent)), var(--c-bg); }
.has-paper-texture .@@::before { background: radial-gradient(140% 100% at 50% 40%, transparent 55%, color-mix(in srgb, var(--c-text) 10%, transparent)), var(--img-paper-texture), var(--c-bg); }
.has-pattern-tile .@@::after { content: ""; position: fixed; inset: 0; z-index: -1; pointer-events: none; opacity: 0.05;
  background: var(--c-accent); -webkit-mask: var(--img-pattern-tile) 0 0 / 120px; mask: var(--img-pattern-tile) 0 0 / 120px; }
.@@-section { position: relative; padding-block: 64px; padding-inline: 20px; }
.@@-wishes, .@@-footer { content-visibility: auto; contain-intrinsic-size: auto 700px; }

/* type */
.@@ :is(.@@-names, .@@-title, .@@-count__num, .@@-event__type) {
  background: var(--@@-ink) 0 0 / 220% 100%; -webkit-background-clip: text; background-clip: text; color: transparent; }
.@@ :is(.@@-title--panel, .@@-closing) {
  background: var(--@@-foil) 0 0 / 220% 100%; -webkit-background-clip: text; background-clip: text; color: transparent; }
.@@-title { margin-block-end: 26px; font-family: var(--font-display); font-weight: 400; font-size: 34px; line-height: 1.3; }
.@@:lang(en) .@@-title { font-family: var(--font-latin); }
.@@-names { display: flex; flex-direction: column; align-items: center; font-family: var(--font-display); font-weight: 400; font-size: min(var(--name-size), 12vw); line-height: 1.25; }
.@@:lang(en) .@@-names { font-family: var(--font-latin); line-height: 1.12; }
.@@-name { max-inline-size: 100%; overflow-wrap: anywhere; text-wrap: balance; }
.@@-and { font-size: 0.55em; line-height: 1.6; }
.@@-lead { max-inline-size: 26ch; margin-inline: auto; font-size: 14px; color: var(--c-muted); }
.@@:lang(en) .@@-lead { font-family: var(--font-latin); font-style: italic; font-size: 16px; }
.@@-monogram { display: none; inline-size: 40px; block-size: 40px; margin-inline: auto; background: var(--@@-foil); }
.has-monogram-art .@@-monogram { display: block; -webkit-mask: var(--img-monogram-art) center / contain no-repeat; mask: var(--img-monogram-art) center / contain no-repeat; }

/* ---------- 1 · the diorama ---------- */
.@@-cover, .@@-diorama { position: relative; }
.@@-stage { position: relative; block-size: max(100svh, 680px); overflow: hidden; isolation: isolate; }
/* every plane drifts at its own speed as the cover scrolls away: far planes lag
   behind, near planes move ahead. One transform per plane, run by the browser on
   the GPU from the scroll position: no script, no repaint. */
.@@-layer { position: absolute; will-change: transform; }
@supports (animation-timeline: view()) {
  .@@-stage { view-timeline: --@@-cover block; }
  .@@-layer { animation: @K@-drift linear both; animation-timeline: --@@-cover; animation-range: exit 0% exit 100%; }
  .@@[data-cover-layout="still"] .@@-layer { animation: none; }
}
@keyframes @K@-drift { to { transform: translate(var(--dx, 0px), var(--dy, 0px)); } }

.@@-cartouche {
  inset-block-start: var(--@@-cart-top, 17%); inset-inline: 0; margin-inline: auto; z-index: 5;
  inline-size: min(300px, 80%); --dy: 60px;
  display: flex; flex-direction: column; align-items: center; gap: 8px;
  padding-block: 26px 30px; padding-inline: 20px;
}
.@@-cartouche .@@-monogram { inline-size: 30px; block-size: 30px; }
.@@-date { padding-block: 7px; padding-inline: 20px; border: 1px solid var(--c-accent); border-radius: 999px; color: var(--c-hero); font-size: 14px; }
.@@-spark { position: absolute; z-index: 4; inline-size: 16px; block-size: 16px; display: none; background: var(--@@-foil); pointer-events: none; }
.has-sparkle-art .@@-spark { display: block; -webkit-mask: var(--img-sparkle-art) center / contain no-repeat; mask: var(--img-sparkle-art) center / contain no-repeat; }
.@@-cue { position: absolute; inset-block-end: 3%; inset-inline: 0; z-index: 7; font-size: 12px; color: var(--@@-cue, var(--c-muted)); }
.@@-cue::after { content: ""; display: block; inline-size: 1px; block-size: 26px; margin: 6px auto 0; background: linear-gradient(var(--c-accent), transparent); }
.@@[data-cover-layout="still"] .@@-cue { display: none; }
.@@[data-ornament="refined"] .@@-decor { display: none !important; }

/* night scenes: names in foil over a soft dark halo */
.@@-cartouche--night { color: var(--@@-glow); background: radial-gradient(closest-side, color-mix(in srgb, var(--c-deep) 62%, transparent), color-mix(in srgb, var(--c-deep) 30%, transparent) 70%, transparent); }
.@@-cartouche--night .@@-names { background: var(--@@-foil) 0 0 / 220% 100%; -webkit-background-clip: text; background-clip: text; color: transparent;
  filter: drop-shadow(0 2px 12px color-mix(in srgb, var(--c-deep) 90%, transparent)); font-size: min(calc(var(--name-size) * 0.9), 11vw); }
.@@-cartouche--night .@@-lead { color: color-mix(in srgb, var(--@@-glow) 85%, transparent); font-size: 13.5px; }
.@@-cartouche--night .@@-date { color: var(--@@-glow); background: color-mix(in srgb, var(--c-deep) 78%, transparent); border-color: var(--c-accent); }
/* day scenes: ink names over a soft light halo */
.@@-cartouche--day { background: radial-gradient(closest-side, color-mix(in srgb, var(--c-card) 88%, transparent), color-mix(in srgb, var(--c-card) 55%, transparent) 70%, transparent); }
.@@-cartouche--day .@@-names { font-size: min(calc(var(--name-size) * 0.9), 11vw); }
.@@-cartouche--day .@@-date { background: color-mix(in srgb, var(--c-card) 80%, transparent); }

/* ---------- the invitation sheet ---------- */
.@@-sheet { position: relative; margin-block: 30px 10px; margin-inline: 22px; padding-block: 56px; padding-inline: 30px;
  border-radius: var(--radius); background: var(--c-card); outline: 1px solid var(--c-accent); outline-offset: -10px;
  box-shadow: 0 0 0 1px var(--c-line), 0 30px 50px -30px color-mix(in srgb, var(--c-deep) 55%, transparent); }
.@@-sheet:not(:has(p)) { display: none; }
.has-frame-art .@@-sheet::before, .has-frame-art .@@-sheet::after {
  content: ""; position: absolute; inset-inline: 22px; block-size: 20px; background: var(--c-accent);
  -webkit-mask: var(--img-frame-art) center / auto 100% repeat-x; mask: var(--img-frame-art) center / auto 100% repeat-x; }
.@@-sheet::before { inset-block-start: 20px; }
.@@-sheet::after { inset-block-end: 20px; rotate: x 180deg; }
.@@-verse { margin-block-end: 18px; font-family: var(--font-display); font-size: 19px; line-height: 1.9; }
.@@-families { display: grid; grid-template-columns: 1fr 1fr; }
.@@-families:not(:has(p)) { display: none; }
.@@-verse + .@@-families { padding-block-start: 20px; border-block-start: 1px solid var(--c-line); }
.@@-family { display: flex; flex-direction: column; gap: 2px; padding-inline: 8px; min-inline-size: 0; }
.@@-family + .@@-family { border-inline-start: 1px solid var(--c-line); }
.@@-family__label { font-size: 12px; color: var(--c-muted); }
.@@-family__label:not(:first-child) { margin-block-start: 8px; }
.@@-family__name { font-size: 14px; font-weight: 600; line-height: 1.5; overflow-wrap: anywhere; }

/* ---------- cards ---------- */
.@@-card { position: relative; z-index: 1; padding-block: 48px; padding-inline: 26px; border-radius: var(--radius); background: var(--c-card);
  outline: 1px solid var(--c-accent); outline-offset: -10px;
  box-shadow: inset 0 0 0 14px var(--c-card), inset 0 0 0 15px color-mix(in srgb, var(--c-accent) 45%, transparent), 0 0 0 1px var(--c-line),
    0 30px 50px -28px color-mix(in srgb, var(--c-deep) 55%, transparent); }
.has-corner-art .@@-card::after { content: ""; position: absolute; inset-block-end: -18px; inset-inline-end: -14px; inline-size: 84px; aspect-ratio: 1; pointer-events: none;
  background: var(--@@-corner, var(--c-accent)); -webkit-mask: var(--img-corner-art) center / contain no-repeat; mask: var(--img-corner-art) center / contain no-repeat; }
.@@-card:dir(rtl)::after { rotate: y 180deg; }
.@@[data-ornament="refined"] .@@-card::after { display: none; }
.@@-divider { inline-size: 240px; block-size: 30px; margin-inline: auto; background: linear-gradient(var(--c-accent), var(--c-accent)) center / 100% 1px no-repeat; }
.has-divider-art .@@-divider { background: var(--@@-foil); -webkit-mask: var(--img-divider-art) center / contain no-repeat; mask: var(--img-divider-art) center / contain no-repeat; }

/* ---------- 2 · countdown emblem ---------- */
.@@-countdown { display: flex; flex-direction: column; align-items: center; }
.@@-emblem { position: relative; display: grid; place-items: center; }
.@@-emblem > span { position: absolute; display: block; pointer-events: none; }
.@@-count { position: relative; z-index: 2; display: flex; flex-direction: column; align-items: center; line-height: 1.05; }
.@@-count__num { font-family: var(--font-display); font-size: 46px; }
.@@:lang(en) .@@-count__num { font-family: var(--font-latin); }
.@@-count__unit { font-size: 12px; color: var(--c-hero); }
/* emblem pieces settle once when the section arrives */
.@@-emblem > span { transition: transform 1.6s cubic-bezier(.3, .7, .2, 1) .3s, opacity 1.2s ease .3s; }
.@@-cal { inline-size: 100%; max-inline-size: 360px; margin-block-start: 30px; padding-block: 36px; }
.@@-cal__title { margin-block-end: 12px; font-family: var(--font-display); font-size: 22px; color: var(--c-hero); }
.@@:lang(en) .@@-cal__title { font-family: var(--font-latin); }
.@@-cal__grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px 0; font-size: 13px; }
.@@-cal__wd { font-size: 11px; color: var(--c-muted); }
.@@-cal__cell { display: grid; place-items: center; block-size: 34px; }
.@@-cal__cell.is-wedding { justify-self: center; inline-size: 34px; border-radius: 50%; background: var(--@@-foil); color: var(--c-hero); font-weight: 700; }

/* ---------- 3 · story: photos behind veils that open once ---------- */
.@@-photos { display: flex; justify-content: center; gap: 18px; margin-block-end: 28px; --open: 1; }
.@@-story.fx:not(.is-in) .@@-photos { --open: 0; }
.@@-photo { position: relative; flex: 0 1 44%; aspect-ratio: 3 / 4; perspective: 700px; padding: 5px; border-radius: var(--@@-photo-r); background: var(--@@-foil);
  box-shadow: inset 0 0 0 1px var(--@@-gd), 0 0 0 4px var(--c-card), 0 0 0 5px color-mix(in srgb, var(--c-accent) 70%, transparent), 0 20px 30px -16px color-mix(in srgb, var(--c-deep) 60%, transparent); }
.@@-photo:nth-child(2) { margin-block-start: 34px; }
.@@-photo:nth-child(n+3) { display: none; }
.@@-photo { overflow: hidden; }
.@@-photo img { position: relative; display: block; inline-size: 100%; block-size: 100%; object-fit: cover; border-radius: inherit; }
.@@-veil { position: absolute; inset-block: 5px; inline-size: calc(50% - 5px); z-index: 2; overflow: hidden; will-change: transform;
  transition: transform 1.6s cubic-bezier(.65, 0, .25, 1) .5s, opacity 1.2s ease .7s; }
.@@-veil--a { inset-inline-start: 5px; }
.@@-veil--b { inset-inline-end: 5px; }
.@@:not([data-photo-frame="veiled"]) .@@-veil { display: none; }
.@@[data-photo-frame="oval"] .@@-photo { border-radius: 50%; padding: 4px; outline: 2px dotted var(--c-accent); outline-offset: 5px; }
.@@[data-photo-frame="arch"] .@@-photo { border-radius: 999px 999px 6px 6px; }
.@@-story__text { max-inline-size: 30ch; margin-inline: auto; font-size: 17px; }
.@@-story__date { margin-block-start: 12px; font-size: 13px; color: var(--c-muted); }

/* ---------- 4 · gallery ---------- */
.@@-gallery { padding-inline: 0; }
.@@-gallery__stage { display: flex; flex-direction: column; align-items: center; }
.@@-flow { display: flex; inline-size: 100%; overflow-x: auto; scroll-snap-type: x mandatory; padding-block: 16px 34px; padding-inline: 22%; scrollbar-width: none; }
.@@-flow::-webkit-scrollbar { display: none; }
.@@-flow__item { flex: 0 0 56%; aspect-ratio: 3 / 4; scroll-snap-align: center; padding-inline: 8px; }
.@@-flow__item img { display: block; inline-size: 100%; block-size: 100%; object-fit: cover; border-radius: var(--@@-photo-r); border: 3px solid transparent;
  background: var(--@@-foil) border-box; box-shadow: 0 24px 36px -20px color-mix(in srgb, var(--c-deep) 70%, transparent); }
/* the ring needs the scene engine and at least three photos */
.scene-on .@@[data-gallery-style="carousel"] .@@-gallery[data-n]:not([data-n="1"]):not([data-n="2"]) { block-size: 280svh; padding-block: 0; }
.scene-on .@@[data-gallery-style="carousel"] .@@-gallery[data-n]:not([data-n="1"]):not([data-n="2"]) .@@-gallery__stage {
  position: sticky; inset-block-start: 0; block-size: 100svh; justify-content: center; overflow: hidden; perspective: 1100px; }
.scene-on .@@[data-gallery-style="carousel"] .@@-gallery[data-n]:not([data-n="1"]):not([data-n="2"]) .@@-flow {
  position: relative; display: block; overflow: visible; block-size: 360px; padding: 0; transform-style: preserve-3d; rotate: x -6deg;
  --w: 168px; --r: calc(var(--w) / 2 / tan(0.5turn / var(--n)) + 46px); }
.scene-on .@@[data-gallery-style="carousel"] .@@-gallery[data-n]:not([data-n="1"]):not([data-n="2"]) .@@-flow__item {
  position: absolute; inset-block-start: 40px; inset-inline-start: calc(50% - var(--w) / 2); inline-size: var(--w); padding: 0;
  transform: rotateY(calc((var(--i) / var(--n) - var(--p, 0) * (var(--n) - 1) / var(--n)) * 1turn)) translateZ(var(--r)); }
.scene-on .@@[data-gallery-style="carousel"] .@@-gallery[data-n]:not([data-n="1"]):not([data-n="2"]) .@@-hint { display: none; }
@supports (animation-timeline: view(inline)) {
  .@@[data-gallery-style="coverflow"] .@@-flow { perspective: 900px; }
  .@@[data-gallery-style="coverflow"] .@@-flow__item { padding-inline: 0; animation: @K@-flow linear both; animation-timeline: view(inline); }
  .@@[data-gallery-style="coverflow"] .@@-flow:dir(rtl) .@@-flow__item { animation-name: @K@-flow-rtl; }
}
.@@-hint { font-size: 13px; color: var(--c-muted); }
@keyframes @K@-flow { 0% { transform: translateZ(-160px) rotateY(-46deg); opacity: 0.75; } 50% { transform: none; opacity: 1; } 100% { transform: translateZ(-160px) rotateY(46deg); opacity: 0.75; } }
@keyframes @K@-flow-rtl { 0% { transform: translateZ(-160px) rotateY(46deg); opacity: 0.75; } 50% { transform: none; opacity: 1; } 100% { transform: translateZ(-160px) rotateY(-46deg); opacity: 0.75; } }

/* ---------- 5 · events along a path, a traveller rides with the reader ---------- */
.@@-journey { position: relative; display: flex; flex-direction: column; gap: 46px; padding-inline-start: 58px; text-align: start; }
.@@-path { position: absolute; inset-block: -20px; inset-inline-start: 10px; inline-size: 30px; border-radius: 15px; }
.@@-traveller { position: sticky; inset-block-start: 46vh; z-index: 3; display: none; margin-inline-start: -16px; inline-size: 62px; aspect-ratio: var(--@@-trav, 1); background: var(--@@-foil); }
.has-traveller-art .@@-traveller { display: block; -webkit-mask: var(--img-traveller-art) center / contain no-repeat; mask: var(--img-traveller-art) center / contain no-repeat; }
.@@-traveller:dir(rtl) { rotate: y 180deg; }
.@@-event { padding-block: 36px 40px; padding-inline: 26px; }
.@@-event::before { content: ""; position: absolute; inset-block-start: 40px; inset-inline-start: -52px; inline-size: 18px; block-size: 18px; border-radius: 50%;
  background: radial-gradient(circle, var(--@@-glow) 30%, var(--c-accent) 60%); box-shadow: 0 0 0 4px color-mix(in srgb, var(--c-accent) 25%, transparent); }
.@@-event__type { margin-block-end: 4px; font-family: var(--font-display); font-weight: 400; font-size: 26px; }
.@@:lang(en) .@@-event__type { font-family: var(--font-latin); }
.@@-event__date, .@@-event__time { font-size: 15px; }
.@@-event__time { font-weight: 600; }
.@@-event__place { font-size: 14px; color: var(--c-muted); overflow-wrap: anywhere; }
.@@-program { margin-block-start: 18px; padding-block-start: 16px; border-block-start: 1px solid var(--c-line); }
.@@-program__title { margin-block-end: 10px; font-size: 13px; color: var(--c-muted); }
.@@-program__list { list-style: none; padding: 0; display: grid; gap: 8px; }
.@@-program__item { display: flex; gap: 12px; font-size: 14px; }
.@@-program__item::before { content: ""; flex: none; inline-size: 7px; block-size: 7px; margin-block-start: 0.7em; rotate: 45deg; background: var(--@@-foil); }
.@@-program__time { flex: none; min-inline-size: 64px; font-weight: 600; color: var(--c-hero); }
.@@-map { display: inline-flex; align-items: center; justify-content: center; min-block-size: 46px; margin-block-start: 20px; padding-inline: 26px;
  border-radius: 999px; background: var(--@@-foil); color: var(--c-hero); font-size: 14px; font-weight: 600; text-decoration: none;
  box-shadow: 0 0 0 3px var(--c-card), 0 0 0 4px color-mix(in srgb, var(--c-accent) 60%, transparent); }
.@@-map:focus-visible { outline: 2px solid var(--c-hero); outline-offset: 6px; }

/* ---------- 6 · wishes panel ---------- */
.@@-panel { position: relative; overflow: hidden; padding-block: 52px 40px; padding-inline: 24px; border-radius: var(--radius);
  background: radial-gradient(80% 40% at 50% 100%, color-mix(in srgb, var(--c-accent) 22%, transparent), transparent 70%),
    linear-gradient(color-mix(in srgb, var(--c-deep) 90%, var(--c-card)), var(--c-deep));
  color: var(--@@-glow); box-shadow: 0 30px 50px -28px color-mix(in srgb, var(--c-deep) 70%, transparent); }
.@@-panel__decor { position: absolute; inset: 0; pointer-events: none; }
.@@-panel > :not(.@@-panel__decor) { position: relative; }
.@@ .wb { text-align: start; }
.@@ .wb-chip { border-color: color-mix(in srgb, var(--c-accent) 70%, transparent); color: var(--@@-glow); }
.@@ .wb-label { color: color-mix(in srgb, var(--@@-glow) 75%, transparent); }
.@@ .wb-input, .@@ .wb-textarea { background: color-mix(in srgb, var(--c-deep) 80%, var(--@@-glow)); border-color: color-mix(in srgb, var(--c-accent) 45%, transparent); color: var(--@@-glow); }
.@@ .wb-input::placeholder, .@@ .wb-textarea::placeholder { color: color-mix(in srgb, var(--@@-glow) 55%, transparent); }
.@@ .wb-input:focus, .@@ .wb-textarea:focus { outline: 2px solid var(--c-accent); outline-offset: 0; }
.@@ .wb-send { border-radius: 999px; background: var(--@@-foil); color: var(--c-deep); }
.@@ .wb-status { color: var(--c-accent); }
.@@ .wb-item { background: transparent; border: 0; border-inline-start: 2px solid var(--c-accent); border-radius: 0; }
.@@ .wb-item__name { color: var(--c-accent); }
.@@ .wb-item__text { color: var(--@@-glow); }
/* light panels */
.@@-panel--light { background: var(--c-card); color: var(--c-text); box-shadow: 0 0 0 1px var(--c-line), 0 30px 50px -28px color-mix(in srgb, var(--c-deep) 45%, transparent); }
.@@-panel--light .@@-title--panel { background: var(--@@-ink) 0 0 / 220% 100%; -webkit-background-clip: text; background-clip: text; }
.@@-panel--light .wb-chip { color: var(--c-text); }
.@@-panel--light .wb-label { color: var(--c-muted); }
.@@-panel--light :is(.wb-input, .wb-textarea) { background: var(--c-bg); color: var(--c-text); }
.@@-panel--light :is(.wb-input, .wb-textarea)::placeholder { color: var(--c-muted); }
.@@-panel--light .wb-send { color: var(--c-hero); }
.@@-panel--light .wb-item__text { color: var(--c-text); }

/* ---------- 7 · footer ---------- */
.@@-footer { display: flex; flex-direction: column; align-items: center; gap: 12px; padding-block: 70px 64px; overflow: hidden; }
.@@-footer__art { display: none; inline-size: 150px; aspect-ratio: var(--@@-fa, 1); background: var(--@@-foil); }
.has-footer-art .@@-footer__art { display: block; -webkit-mask: var(--img-footer-art) center bottom / contain no-repeat; mask: var(--img-footer-art) center bottom / contain no-repeat; }
.@@-closing { max-inline-size: 20ch; font-family: var(--font-display); font-size: 30px; line-height: 1.5; }
.@@:lang(en) .@@-closing { font-family: var(--font-latin); }
.@@-until, .@@-brand { font-size: 13px; color: var(--c-muted); }

/* ---------- cover layout "names": only the names, no scene ---------- */
.@@[data-cover-layout="names"] .@@-stage { block-size: auto; padding-block: 90px 40px; overflow: visible; }
.@@[data-cover-layout="names"] .@@-layer:not(.@@-cartouche), .@@[data-cover-layout="names"] .@@-cue { display: none; }
.@@[data-cover-layout="names"] .@@-cartouche { position: relative; inset: auto; margin-inline: auto; background: none; animation: none; }
.@@[data-cover-layout="names"] .@@-cartouche::before, .@@[data-cover-layout="names"] .@@-cartouche::after { display: none; }
.@@[data-cover-layout="names"] .@@-names { background: var(--@@-ink) 0 0 / 220% 100%; -webkit-background-clip: text; background-clip: text; filter: none; font-size: calc(var(--name-size) * 1.1); }
.@@[data-cover-layout="names"] .@@-lead { color: var(--c-muted); }
.@@[data-cover-layout="names"] .@@-date { color: var(--c-hero); background: none; }
"""

REDUCE_CSS = r"""
/* ---------- reduced motion: a still, complete scene ---------- */
@media (prefers-reduced-motion: reduce) {
  .@@ *, .@@ *::before, .@@ *::after { animation: none !important; transition: none !important; }
  .@@-photos, .@@-story.fx:not(.is-in) .@@-photos { --open: 1; }
}
"""

# veil motions: how the two veils over each story photo open (once, on arrival)
VEILS = {
    "swing": """.@@-veil--a { transform-origin: 0 50%; transform: rotateY(calc(var(--open) * -112deg)); }
.@@-veil--b { transform-origin: 100% 50%; transform: rotateY(calc(var(--open) * 112deg)); }
.@@-veil--a:dir(rtl) { transform-origin: 100% 50%; transform: rotateY(calc(var(--open) * 112deg)); }
.@@-veil--b:dir(rtl) { transform-origin: 0 50%; transform: rotateY(calc(var(--open) * -112deg)); }""",
    "slide": """.@@-veil--a { transform: translateX(calc(var(--open) * -104%)); }
.@@-veil--b { transform: translateX(calc(var(--open) * 104%)); }
.@@-veil--a:dir(rtl) { transform: translateX(calc(var(--open) * 104%)); }
.@@-veil--b:dir(rtl) { transform: translateX(calc(var(--open) * -104%)); }
""",
    "part": """.@@-veil { opacity: calc(1 - var(--open)); }
.@@-veil--a { transform: translateX(calc(var(--open) * -70%)); }
.@@-veil--b { transform: translateX(calc(var(--open) * 70%)); }
.@@-veil--a:dir(rtl) { transform: translateX(calc(var(--open) * 70%)); }
.@@-veil--b:dir(rtl) { transform: translateX(calc(var(--open) * -70%)); }""",
    "lift": """.@@-veil--a { inline-size: auto; inset-inline: 5px; transform: translateY(calc(var(--open) * -40%)); opacity: calc(1 - var(--open)); }
.@@-veil--b { display: none; }""",
    "page": """.@@-veil--a { inline-size: auto; inset-inline: 5px; transform-origin: 0 50%; transform: rotateY(calc(var(--open) * -150deg)); opacity: calc(1 - var(--open) * 0.6); }
.@@-veil--a:dir(rtl) { transform-origin: 100% 50%; transform: rotateY(calc(var(--open) * 150deg)); }
.@@-veil--b { display: none; }""",
    "envelope": """.@@-veil--a { inline-size: auto; inset-inline: 5px; block-size: 52%; inset-block-end: auto; z-index: 3; border-radius: 0; transform-origin: 50% 0;
  transform: rotateX(calc(var(--open) * 180deg)); opacity: calc(1 - var(--open)); clip-path: polygon(0 0, 100% 0, 50% 100%); }
.@@-veil--b { inline-size: auto; inset-inline: 5px; block-size: 62%; inset-block-start: auto; border-radius: 0; transform: translateY(calc(var(--open) * 110%)); opacity: calc(1 - var(--open));
  clip-path: polygon(0 0, 50% 40%, 100% 0, 100% 100%, 0 100%); }
""",
}


def build_css(cfg, scene):
    head = f"/* {cfg['name']['en']}: {cfg['css_note']}\n   Built by tools/build-scenes.py with the scene kit (tools/scenekit.py): calm GPU\n   drift on the cover, one-time reveals, no loops. Tokens only; logical properties. */\n"
    parts = [head, BASE_CSS, "/* ---------- the scene: planes from far to near ---------- */",
             "\n".join(scene.css), cfg["css"], VEILS[cfg["veil"]], REDUCE_CSS]
    css = "\n".join(parts)
    return css.replace("@@", cfg["P"]).replace("@K@", cfg["key"])


# ----------------------------------------------------------------- manifest
BASE_TEXTS = None


def build_manifest(cfg, scene):
    global BASE_TEXTS
    if BASE_TEXTS is None:
        BASE_TEXTS = json.loads((ROOT / "templates" / "nile-royal" / "manifest.json").read_text(encoding="utf-8"))["texts"]
    texts = json.loads(json.dumps(BASE_TEXTS))
    for k, (ar, en) in cfg["texts"].items():
        texts[k] = {"ar": ar, "en": en}
    images = {"paperTexture": cfg.get("paper", "paper-grain"), **cfg["images"], **scene.images}
    colors = ["hero", "onHero", "accent", "bg", "text", "muted", "card", "line", "deep", "leaf"]
    tokens = [{"key": c, "type": "color"} for c in colors]
    tokens += [{"key": f, "type": "font"} for f in ("display", "body", "latin")]
    tokens += [{"key": "radius", "type": "length", "min": 0, "max": 24, "unit": "px"},
               {"key": "nameSize", "type": "length", "min": 34, "max": 64, "unit": "px"}]
    tokens += [{"key": k, "type": "image"} for k in images]

    def vt(key, opts):
        return {"key": key, "type": "variant", "options": [o[0] for o in opts], "choices": {o[0]: {"ar": o[1], "en": o[2]} for o in opts}}
    tokens += [
        vt("coverLayout", [("scene", "مشهد بعمق يتحرك بهدوء", "Scene with gentle depth"), ("still", "مشهد ثابت", "Still scene"), ("names", "الأسماء فقط", "Names only")]),
        vt("ornament", [("rich", "زخرفة كاملة", "Rich ornament")]),
        vt("dateStyle", [("badge", "التاريخ على الغلاف", "Date on the cover"), ("calendar", "تقويم الشهر", "Month calendar")]),
        vt("photoFrame", [("veiled", *cfg["veil_name"]), ("arch", "قوس", "Arch"), ("oval", "بيضاوي", "Oval")]),
        vt("galleryStyle", [("coverflow", "عرض ثلاثي الأبعاد", "3D coverflow"), ("carousel", "حلقة ثلاثية الأبعاد", "3D carousel ring"), ("strip", "شريط بسيط", "Simple strip")]),
    ]
    pal = cfg["palettes"]
    theme = {**pal[0][3], **cfg["fonts"], "radius": cfg.get("radius", 14), "nameSize": cfg.get("nameSize", 50), **images,
             "coverLayout": "scene", "ornament": "rich", "dateStyle": "badge", "photoFrame": "veiled", "galleryStyle": "coverflow"}
    man = {
        "key": cfg["key"], "name": cfg["name"], "description": cfg["description"], "languages": ["ar", "en"],
        "texts": texts, "tokens": tokens, "defaultTheme": theme,
        "defaultAnimation": {"intro": cfg["intro"], "ambient": "none", "duration": 1100, "stagger": 160, "parallax": True,
                             "sections": {"cover": {"effect": "fade"}, "countdown": {"effect": "fade-up"}, "story": {"effect": "fade-up"},
                                          "gallery": {"effect": "fade"}, "events": {"effect": "fade-up"}, "wishes": {"effect": "fade-up"}, "footer": {"effect": "fade"}}},
        "runtime": {"scene": True, "intros": [cfg["intro"]]},
        "effects": [], "fields": [],
        "couplePresets": {
            "label": cfg["name"], "defaultPalette": pal[0][0],
            "palettes": [{"key": k, "name": {"ar": ar, "en": en}, "values": v} for k, ar, en, v in pal],
            "intros": [cfg["intro"], "doors", "curtain", "none"],
            "ambients": ["none", "sparkles"],
            "motions": {"calm": {"duration": 1100, "stagger": 160, "parallax": True}, "lively": {"duration": 700, "stagger": 100, "parallax": True}},
            "variants": [{"key": k} for k in ("coverLayout", "ornament", "dateStyle", "photoFrame", "galleryStyle")],
            "hiddenEffects": [],
        },
    }
    return man


# ----------------------------------------------------------------- palettes
def _rgb(h):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def _mixhex(a, b, t):
    A, B = _rgb(a), _rgb(b)
    return "#" + "".join(f"{round(x * t + y * (1 - t)):02X}" for x, y in zip(A, B))


def palette(key, ar, en, hero, onHero, accent, bg, text, deep, leaf, dark=False):
    card = _mixhex(bg, text, 0.93) if dark else _mixhex(bg, "#FFFFFF", 0.3)
    return (key, ar, en, dict(hero=hero, onHero=onHero, accent=accent, bg=bg, text=text,
                              muted=_mixhex(text, bg, 0.6), card=card, line=_mixhex(bg, text, 0.86), deep=deep, leaf=leaf))


def write(cfg, scene):
    d = ROOT / "templates" / cfg["key"]
    d.mkdir(parents=True, exist_ok=True)
    html = template_html(cfg, scene).replace("@@", cfg["P"])
    (d / "template.html").write_text(html, encoding="utf-8")
    (d / "style.css").write_text(build_css(cfg, scene), encoding="utf-8")
    (d / "manifest.json").write_text(json.dumps(build_manifest(cfg, scene), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
