#!/usr/bin/env python3
"""Writes the Porcelain, Glass Garden, Lace and Desert Bloom templates.

Shared structure (sections, families, calendar, programme, gallery modes,
foil, sparkles, the "refined" ornament switch) comes from one skeleton with a
class prefix; each template adds its own cover scene and look. The output is
the usual three self-contained files per template in templates/<key>/.
Run: python3 tools/build-luxe-templates.py
"""
import json, math, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent / "templates"

def scallop_polygon(lobes=20, steps=6, depth=4.0):
    pts = []
    n = lobes * steps
    for i in range(n):
        a = 2 * math.pi * i / n - math.pi / 2
        r = 50 - depth + depth * abs(math.cos(math.pi * (i % steps) / steps))
        pts.append(f"{50 + math.cos(a) * r:.1f}% {50 + math.sin(a) * r:.1f}%")
    return "polygon(" + ", ".join(pts) + ")"

SCALLOP = scallop_polygon()

# ---------------------------------------------------------------- HTML
def families(P):
    side = lambda who, rel: f"""      <div class="{P}-family">
        {{{{#if couple.{who}.father}}}}<p class="{P}-family__label">{{{{text "{rel}"}}}}</p><p class="{P}-family__name">{{{{couple.{who}.father}}}}</p>{{{{/if}}}}
        {{{{#each couple.{who}.family}}}}<p class="{P}-family__label">{{{{label}}}}</p><p class="{P}-family__name">{{{{name}}}}</p>{{{{/each}}}}
      </div>"""
    return f"""    <div class="{P}-families">
{side('groom', 'sonOf')}
{side('bride', 'daughterOf')}
    </div>"""

def names(P, tag="h1"):
    return f"""<{tag} class="{P}-names">
        <span class="{P}-name">{{{{couple.groom.name}}}}</span>
        {{{{#if couple.bride.name}}}}<span class="{P}-and">{{{{text "and"}}}}</span><span class="{P}-name">{{{{couple.bride.name}}}}</span>{{{{/if}}}}
      </{tag}>"""

def sparks(P, n=3):
    return "".join(f'<span class="{P}-spark {P}-spark--{i} {P}-decor" aria-hidden="true"></span>' for i in range(1, n + 1))

def page(P, cover, card_decor="", footer_decor=""):
    return f"""<main class="{P}" data-cover-layout="{{{{variant "coverLayout"}}}}" data-ornament="{{{{variant "ornament"}}}}" data-date-style="{{{{variant "dateStyle"}}}}" data-photo-frame="{{{{variant "photoFrame"}}}}" data-gallery-style="{{{{variant "galleryStyle"}}}}">

{cover}

  <section class="{P}-section {P}-countdown" data-animate="countdown">
    <div class="{P}-card">
      {card_decor}{sparks(P, 2)}
      <h2 class="{P}-title">{{{{text "countdownTitle"}}}}</h2>
      <p class="{P}-count"><span class="{P}-count__num">{{{{daysUntil mainDate}}}}</span><span class="{P}-count__unit">{{{{text "countdownUnit"}}}}</span></p>
      {{{{#if (variant "dateStyle" "calendar")}}}}
        {{{{#with (calendarMonth mainDate)}}}}
          <div class="{P}-cal">
            <p class="{P}-cal__title">{{{{title}}}}</p>
            <div class="{P}-cal__grid">
              {{{{#each weekdays}}}}<span class="{P}-cal__wd">{{{{this}}}}</span>{{{{/each}}}}
              {{{{#each cells}}}}<span class="{P}-cal__cell{{{{#if wedding}}}} is-wedding{{{{/if}}}}">{{{{label}}}}</span>{{{{/each}}}}
            </div>
          </div>
        {{{{/with}}}}
      {{{{/if}}}}
    </div>
  </section>

  {{{{#if story.text}}}}
    <div class="{P}-divider" aria-hidden="true"></div>
    <section class="{P}-section {P}-story" data-animate="story">
      <div class="{P}-card">
        {card_decor}
        <h2 class="{P}-title">{{{{text "storyTitle"}}}}</h2>
        {{{{#if story.photos.length}}}}
          <div class="{P}-photos">
            {{{{#each story.photos}}}}<figure class="{P}-photo" data-item><img src="{{{{url}}}}" alt="{{{{text "storyPhoto"}}}}" loading="lazy"></figure>{{{{/each}}}}
          </div>
        {{{{/if}}}}
        <p class="{P}-story__text">{{{{story.text}}}}</p>
        {{{{#if story.engagementDate}}}}<p class="{P}-story__date">{{{{text "engagement"}}}} {{{{formatDate story.engagementDate}}}}</p>{{{{/if}}}}
      </div>
    </section>
  {{{{/if}}}}

  {{{{#if gallery.length}}}}
    <section class="{P}-section {P}-gallery" data-animate="gallery">
      <h2 class="{P}-title">{{{{text "galleryTitle"}}}}</h2>
      <div class="{P}-flow">
        {{{{#each gallery}}}}<figure class="{P}-flow__item" data-item><img src="{{{{url}}}}" width="{{{{width}}}}" height="{{{{height}}}}" alt="{{{{text "galleryPhoto"}}}}" loading="lazy"></figure>{{{{/each}}}}
      </div>
      {{{{#if gallery.[1]}}}}<p class="{P}-hint">{{{{text "galleryHint"}}}}</p>{{{{/if}}}}
    </section>
  {{{{/if}}}}

  <div class="{P}-divider" aria-hidden="true"></div>

  <section class="{P}-section {P}-events" data-animate="events">
    <h2 class="{P}-title">{{{{text "eventsTitle"}}}}</h2>
    {{{{#each events}}}}
      <article class="{P}-card {P}-event" data-item>
        {card_decor}
        <h3 class="{P}-event__type">{{{{eventLabel type}}}}</h3>
        <p class="{P}-event__date">{{{{formatDate date}}}}</p>
        <p class="{P}-event__time">{{{{eventTime this}}}}</p>
        <p class="{P}-event__place">{{{{venue}}}}{{{{#if area}}}}{{{{text "listSeparator"}}}}{{{{area}}}}{{{{/if}}}}</p>
        {{{{#if program.length}}}}
          <div class="{P}-program">
            <p class="{P}-program__title">{{{{text "programTitle"}}}}</p>
            <ol class="{P}-program__list">
              {{{{#each program}}}}<li class="{P}-program__item"><span class="{P}-program__time">{{{{formatTime time}}}}</span><span class="{P}-program__what">{{{{title}}}}</span></li>{{{{/each}}}}
            </ol>
          </div>
        {{{{/if}}}}
        {{{{#if mapUrl}}}}<a class="{P}-map" href="{{{{mapUrl}}}}" target="_blank" rel="noopener">{{{{text "openMap"}}}}</a>{{{{/if}}}}
      </article>
    {{{{/each}}}}
  </section>

  <section class="{P}-section {P}-wishes" data-animate="wishes">
    <div class="{P}-card">
      {card_decor}
      <h2 class="{P}-title">{{{{text "wishesTitle"}}}}</h2>
      <wishes-box></wishes-box>
    </div>
  </section>

  <footer class="{P}-section {P}-footer" data-animate="footer">
    {footer_decor}
    {{{{#if closingLine}}}}<p class="{P}-closing">{{{{closingLine}}}}</p>{{{{/if}}}}
    {{{{#if wishes.closeDate}}}}<p class="{P}-until">{{{{text "openUntil"}}}} {{{{formatDate wishes.closeDate}}}}</p>{{{{/if}}}}
    {{{{#if showBranding}}}}<p class="{P}-brand">{{{{text "madeWith"}}}}</p>{{{{/if}}}}
  </footer>
</main>
"""

# ---------------------------------------------------------------- shared CSS
BASE_CSS = """
/* ---------- base ---------- */
.@@ {
  --@@-gold-deep: color-mix(in srgb, var(--c-accent) 58%, var(--c-hero));
  --@@-gold-light: color-mix(in srgb, var(--c-accent) 45%, var(--c-card));
  --@@-foil: linear-gradient(115deg, var(--@@-gold-deep) 0%, var(--c-accent) 20%, var(--@@-gold-light) 34%,
    var(--c-accent) 46%, var(--@@-gold-deep) 60%, var(--c-accent) 76%, var(--@@-gold-light) 90%, var(--c-accent) 100%);
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
.@@ :where(p, h1, h2, h3, ol, figure) { margin: 0; }
.@@-section { position: relative; padding-block: 60px; padding-inline: 20px; }

/* foil text */
.@@ :is(.@@-names, .@@-title, .@@-count__num, .@@-closing, .@@-event__type) {
  background: var(--@@-foil-text, var(--@@-foil)) 0 0 / 220% 100%;
  -webkit-background-clip: text;
          background-clip: text;
  color: transparent;
}
.@@-title { margin-block-end: 26px; font-family: var(--font-display); font-weight: 400; font-size: 34px; line-height: 1.3; }
.@@:lang(en) .@@-title { font-family: var(--font-latin); }
.@@-names { display: flex; flex-direction: column; align-items: center; font-family: var(--font-display); font-weight: 400; font-size: var(--name-size); line-height: 1.25; }
.@@:lang(en) .@@-names { font-family: var(--font-latin); }
.@@-name { max-inline-size: 100%; overflow-wrap: anywhere; text-wrap: balance; }
.@@-and { font-size: 0.6em; }

/* sparkles: four-point glints in foil, twinkling as they scroll by */
.@@-spark { position: absolute; z-index: 4; inline-size: 18px; block-size: 18px; display: none; pointer-events: none; background: var(--@@-foil); }
.has-sparkle-art .@@-spark { display: block; -webkit-mask: var(--img-sparkle-art) center / contain no-repeat; mask: var(--img-sparkle-art) center / contain no-repeat; }
.@@-spark--1 { inset-block-start: 14px; inset-inline-start: 18%; }
.@@-spark--2 { inset-block-start: 34px; inset-inline-end: 14%; inline-size: 12px; block-size: 12px; }
.@@-spark--3 { inset-block-end: 22%; inset-inline-end: 8%; inline-size: 22px; block-size: 22px; }

/* "refined" hides the extra ornament for a quieter look */
.@@[data-ornament="refined"] .@@-decor { display: none !important; }

/* dividers */
.@@-divider { block-size: 22px; inline-size: 200px; margin-inline: auto; background: linear-gradient(var(--c-accent), var(--c-accent)) center / 100% 1px no-repeat; position: relative; }
.@@-divider::after { content: ""; position: absolute; inset: 0; margin: auto; inline-size: 9px; block-size: 9px; background: var(--@@-foil); rotate: 45deg; }

/* the invitation card under the cover disappears when the couple filled nothing for it */
.@@-invite:not(:has(p, figure)) { display: none; }

/* families */
.@@-families { display: grid; grid-template-columns: 1fr 1fr; margin-block-start: 24px; padding-block-start: 20px; border-block-start: 1px solid var(--c-line); }
.@@-families:not(:has(p)) { display: none; }
.@@-family { display: flex; flex-direction: column; gap: 2px; padding-inline: 8px; min-inline-size: 0; }
.@@-family + .@@-family { border-inline-start: 1px solid var(--c-line); }
.@@-family__label { font-size: 12px; color: var(--c-muted); }
.@@-family__label:not(:first-child) { margin-block-start: 8px; }
.@@-family__name { font-size: 14px; font-weight: 600; line-height: 1.5; overflow-wrap: anywhere; }
.@@-verse { font-family: var(--font-display); font-size: 18px; line-height: 1.9; }
.@@-lead { max-inline-size: 28ch; margin-inline: auto; font-size: 16px; color: var(--c-muted); }

/* countdown + calendar */
.@@-count { display: flex; flex-direction: column; align-items: center; line-height: 1.1; }
.@@-count__num { font-family: var(--font-display); font-size: 76px; }
.@@:lang(en) .@@-count__num { font-family: var(--font-latin); }
.@@-count__unit { margin-block-start: 4px; font-size: 14px; color: var(--c-muted); }
.@@-cal { margin-block-start: 26px; padding-block-start: 20px; border-block-start: 1px solid var(--c-line); }
.@@-cal__title { margin-block-end: 12px; font-family: var(--font-display); font-size: 22px; }
.@@:lang(en) .@@-cal__title { font-family: var(--font-latin); }
.@@-cal__grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px 0; font-size: 13px; }
.@@-cal__wd { font-size: 11px; color: var(--c-muted); }
.@@-cal__cell { display: grid; place-items: center; block-size: 34px; }
.@@-cal__cell.is-wedding { justify-self: center; inline-size: 34px; border-radius: 50%; background: var(--@@-foil); color: var(--c-hero); font-weight: 700; box-shadow: 0 0 0 3px var(--c-card), 0 0 0 4px var(--c-accent); }

/* story photos */
.@@-photos { display: flex; justify-content: center; gap: 18px; margin-block-end: 26px; }
.@@-photo { position: relative; flex: 0 1 44%; aspect-ratio: 3 / 4; }
.@@-photo:nth-child(2) { margin-block-start: 30px; }
.@@-photo:nth-child(n+3) { display: none; }
.@@-photo img { position: relative; display: block; inline-size: 100%; block-size: 100%; object-fit: cover; border-radius: inherit; }
.@@-story__text { max-inline-size: 30ch; margin-inline: auto; font-size: 17px; }
.@@-story__date { margin-block-start: 12px; font-size: 13px; color: var(--c-muted); }

/* gallery: coverflow · stack · strip */
.@@-gallery { padding-inline: 0; }
.@@-flow { display: flex; overflow-x: auto; scroll-snap-type: x mandatory; padding-block: 18px 40px; padding-inline: 22%; perspective: 900px; scrollbar-width: none; }
.@@-flow::-webkit-scrollbar { display: none; }
.@@-flow__item { flex: 0 0 56%; aspect-ratio: 3 / 4; scroll-snap-align: center; padding-inline: 8px; }
.@@-flow__item img { display: block; inline-size: 100%; block-size: 100%; object-fit: cover; }
@supports (animation-timeline: view(inline)) {
  .@@:not([data-gallery-style="strip"]) .@@-flow__item { padding-inline: 0; animation: %%-flow linear both; animation-timeline: view(inline); }
  .@@:not([data-gallery-style="strip"]) .@@-flow:dir(rtl) .@@-flow__item { animation-name: %%-flow-rtl; }
  .@@[data-gallery-style="stack"] .@@-flow__item { animation-name: %%-stack; }
  .@@[data-gallery-style="stack"] .@@-flow:dir(rtl) .@@-flow__item { animation-name: %%-stack-rtl; }
}
@keyframes %%-flow { 0% { transform: translateZ(-160px) rotateY(-46deg); filter: brightness(0.8); } 50% { transform: none; filter: none; } 100% { transform: translateZ(-160px) rotateY(46deg); filter: brightness(0.8); } }
@keyframes %%-flow-rtl { 0% { transform: translateZ(-160px) rotateY(46deg); filter: brightness(0.8); } 50% { transform: none; filter: none; } 100% { transform: translateZ(-160px) rotateY(-46deg); filter: brightness(0.8); } }
@keyframes %%-stack { 0% { transform: translateY(24px) rotate(12deg) scale(0.84); } 50% { transform: none; } 100% { transform: translateY(24px) rotate(-12deg) scale(0.84); } }
@keyframes %%-stack-rtl { 0% { transform: translateY(24px) rotate(-12deg) scale(0.84); } 50% { transform: none; } 100% { transform: translateY(24px) rotate(12deg) scale(0.84); } }
.@@-hint { font-size: 13px; color: var(--c-muted); }

/* events */
.@@-events { display: flex; flex-direction: column; gap: 56px; }
.@@-events .@@-title { margin-block-end: 0; }
.@@-event__type { margin-block-end: 6px; font-family: var(--font-display); font-weight: 400; font-size: 28px; line-height: 1.3; }
.@@:lang(en) .@@-event__type { font-family: var(--font-latin); }
.@@-event__date { font-size: 16px; }
.@@-event__time { margin-block-start: 2px; font-size: 16px; font-weight: 600; }
.@@-event__place { font-size: 14px; color: var(--c-muted); overflow-wrap: anywhere; }
.@@-program { margin-block-start: 22px; padding-block-start: 18px; border-block-start: 1px solid var(--c-line); }
.@@-program__title { margin-block-end: 12px; font-size: 13px; color: var(--c-muted); }
.@@-program__list { list-style: none; padding: 0; display: grid; gap: 10px; max-inline-size: 280px; margin-inline: auto; }
.@@-program__item { display: flex; align-items: center; gap: 12px; font-size: 14px; text-align: start; }
.@@-program__item::before { content: ""; flex: none; inline-size: 7px; block-size: 7px; rotate: 45deg; background: var(--@@-foil); }
.@@-program__time { flex: none; min-inline-size: 66px; font-weight: 600; }
.@@-map {
  display: inline-flex; align-items: center; justify-content: center;
  min-block-size: 46px; margin-block-start: 24px; padding-inline: 28px;
  border-radius: 999px; background: var(--@@-foil) 0 0 / 220% 100%; color: var(--c-hero);
  box-shadow: 0 0 0 3px var(--c-card), 0 0 0 4px color-mix(in srgb, var(--c-accent) 60%, transparent), 0 12px 22px -12px color-mix(in srgb, var(--c-accent) 90%, transparent);
  font-size: 14px; font-weight: 600; text-decoration: none; transition: background-position .8s ease;
}
.@@-map:hover, .@@-map:focus-visible { background-position: 100% 0; }
.@@-map:focus-visible { outline: 2px solid var(--c-hero); outline-offset: 6px; }

/* wishes box */
.@@ .wb { text-align: start; }
.@@ .wb-chip { border-color: var(--c-accent); color: var(--c-text); }
.@@ .wb-label { color: var(--c-muted); }
.@@ .wb-input, .@@ .wb-textarea { background: color-mix(in srgb, var(--c-card) 70%, var(--c-bg)); border-color: var(--c-line); color: var(--c-text); }
.@@ .wb-input::placeholder, .@@ .wb-textarea::placeholder { color: var(--c-muted); }
.@@ .wb-input:focus, .@@ .wb-textarea:focus { outline: 2px solid var(--c-accent); outline-offset: 0; }
.@@ .wb-send { border-radius: 999px; background: var(--@@-foil) 0 0 / 220% 100%; color: var(--c-hero); transition: background-position .8s ease; }
.@@ .wb-send:hover { background-position: 100% 0; }
.@@ .wb-status { color: var(--c-muted); }
.@@ .wb-item { background: transparent; border: 0; border-inline-start: 2px solid var(--c-accent); border-radius: 0; }
.@@ .wb-item__name, .@@ .wb-item__text { color: var(--c-text); }

/* footer */
.@@-footer { display: flex; flex-direction: column; align-items: center; gap: 14px; padding-block: 40px 64px; }
.@@-closing { max-inline-size: 20ch; font-family: var(--font-display); font-size: 32px; line-height: 1.5; }
.@@:lang(en) .@@-closing { font-family: var(--font-latin); }
.@@-until, .@@-brand { font-size: 13px; color: var(--c-muted); }

/* scroll-driven life shared by all */
@supports (animation-timeline: view()) {
  .@@ :is(.@@-names, .@@-title, .@@-count__num, .@@-closing, .@@-event__type, .@@-map) { animation: %%-foil linear both; animation-timeline: view(); }
  .@@-spark { animation: %%-twinkle linear both; animation-timeline: view(); }
}
@keyframes %%-foil { from { background-position: 0% 0; } to { background-position: 100% 0; } }
@keyframes %%-twinkle { 0%, 100% { scale: 0.3; opacity: 0.2; rotate: 0deg; } 30% { scale: 1.15; opacity: 1; } 55% { scale: 0.6; opacity: 0.6; rotate: 45deg; } 75% { scale: 1; opacity: 1; } }
"""

REDUCED = """
@media (prefers-reduced-motion: reduce) {
  .@@ *, .@@ *::before, .@@ *::after { animation: none !important; }
  .@@-map, .@@ .wb-send { transition: none; }
}
"""

def base_css(P, key):
    return BASE_CSS.replace("@@", P).replace("%%", key)

# ---------------------------------------------------------------- manifests
COMMON_TEXTS = {
    "and": {"ar": "و", "en": "&"},
    "sonOf": {"ar": "نجل", "en": "Son of"},
    "daughterOf": {"ar": "كريمة", "en": "Daughter of"},
    "countdownUnit": {"ar": "يوم", "en": "days"},
    "storyPhoto": {"ar": "صورة من حكايتنا", "en": "A photo from our story"},
    "engagement": {"ar": "الخطوبة:", "en": "Engaged on"},
    "galleryPhoto": {"ar": "صورة من معرض الصور", "en": "Gallery photo"},
    "programTitle": {"ar": "فقرات الحفل", "en": "Programme"},
    "openMap": {"ar": "افتح الموقع على الخريطة", "en": "Open in maps"},
    "listSeparator": {"ar": "، ", "en": ", "},
    "openUntil": {"ar": "الصفحة مفتوحة حتى", "en": "This page is open until"},
    "madeWith": {"ar": "اتعملت بحب", "en": "Made with love"},
}

def color_tokens(extra=()):
    keys = ["hero", "onHero", "accent", "bg", "text", "muted", "card", "line", *extra]
    return [{"key": k, "type": "color"} for k in keys]

def variant(key, options):
    return {"key": key, "type": "variant", "options": [o[0] for o in options],
            "choices": {o[0]: {"ar": o[1], "en": o[2]} for o in options}}

COMMON_VARIANTS = lambda cover, frames: [
    variant("coverLayout", cover),
    variant("ornament", [("rich", "زخرفة كاملة", "Rich ornament"), ("refined", "هادئ وراقي", "Refined and quiet")]),
    variant("dateStyle", [("badge", "التاريخ على الغلاف", "Date on the cover"), ("calendar", "تقويم الشهر", "Month calendar")]),
    variant("photoFrame", frames),
    variant("galleryStyle", [("coverflow", "عرض ثلاثي الأبعاد", "3D coverflow"), ("stack", "كأوراق متراصة", "Fanned stack"), ("strip", "شريط بسيط", "Simple strip")]),
]

def manifest(key, name, desc, texts, extra_colors, images, cover, frames, palettes, fonts, theme_images,
             own_reveal, own_ambient=None, intro="doors", sizes=(14, 52)):
    pal0 = palettes[0]
    effects = [{"key": own_reveal[0], "kind": "reveal", "name": {"ar": own_reveal[1], "en": own_reveal[2]}}]
    ambients = ["none"]
    if own_ambient:
        effects.append({"key": own_ambient[0], "kind": "ambient", "name": {"ar": own_ambient[1], "en": own_ambient[2]}})
        ambients.append(own_ambient[0])
    variants = COMMON_VARIANTS(cover, frames)
    theme = dict(pal0["values"])
    theme.update(fonts)
    theme.update({"radius": sizes[0], "nameSize": sizes[1]})
    theme.update(theme_images)
    theme.update({v["key"]: v["options"][0] for v in variants})
    sections = {s: {"effect": own_reveal[0]} for s in ["countdown", "story", "wishes"]}
    sections.update({"cover": {"effect": "fade"}, "gallery": {"effect": "fade"}, "events": {"effect": "fade-up"}, "footer": {"effect": "fade"}})
    return {
        "key": key, "name": name, "description": desc, "languages": ["ar", "en"],
        "texts": {**texts, **COMMON_TEXTS},
        "tokens": color_tokens(extra_colors) + [
            {"key": "display", "type": "font"}, {"key": "body", "type": "font"}, {"key": "latin", "type": "font"},
            {"key": "radius", "type": "length", "min": 0, "max": 28, "unit": "px"},
            {"key": "nameSize", "type": "length", "min": 34, "max": 68, "unit": "px"},
        ] + [{"key": k, "type": "image"} for k in images] + variants,
        "defaultTheme": theme,
        "defaultAnimation": {"intro": intro, "ambient": own_ambient[0] if own_ambient else "none",
                             "duration": 1000, "stagger": 150, "parallax": True, "sections": sections},
        "effects": effects, "fields": [],
        "couplePresets": {
            "label": name, "defaultPalette": pal0["key"], "palettes": palettes,
            "intros": ["none", "doors", "curtain"], "ambients": ambients,
            "motions": {"calm": {"duration": 1000, "stagger": 150, "parallax": True},
                        "lively": {"duration": 650, "stagger": 90, "parallax": True}},
            "variants": [{"key": v["key"]} for v in variants], "hiddenEffects": [],
        },
    }

def pal(key, ar, en, **v):
    return {"key": key, "name": {"ar": ar, "en": en}, "values": v}

def texts(lead, countdown, story, gallery, hint, events, wishes):
    return {"lead": lead, "countdownTitle": countdown, "storyTitle": story, "galleryTitle": gallery,
            "galleryHint": hint, "eventsTitle": events, "wishesTitle": wishes}

# ======================================================================== PORCELAIN
P = "pc"
porcelain_cover = f"""  <section class="pc-cover" data-animate="cover">
    <div class="pc-panel">
      <span class="pc-panel__pattern pc-decor" aria-hidden="true"></span>
      <div class="pc-plate">
        <span class="pc-plate__band" aria-hidden="true"></span>
        <span class="pc-plate__glaze" aria-hidden="true"></span>
        {{{{#if story.photos.length}}}}
          {{{{#with story.photos.[0]}}}}<figure class="pc-plate__photo"><img src="{{{{url}}}}" alt="{{{{text "storyPhoto"}}}}" loading="lazy"></figure>{{{{/with}}}}
        {{{{else}}}}
          <span class="pc-plate__amp" aria-hidden="true">{{{{text "and"}}}}</span>
        {{{{/if}}}}
        {sparks(P, 3)}
      </div>
      <p class="pc-lead">{{{{text "lead"}}}}</p>
      {names(P)}
      {{{{#unless (variant "dateStyle" "calendar")}}}}<p class="pc-date">{{{{formatDate mainDate}}}}</p>{{{{/unless}}}}
    </div>
    <div class="pc-card pc-invite">
      {{{{#if verse}}}}<p class="pc-verse">{{{{verse}}}}</p>{{{{/if}}}}
{families(P)}
    </div>
  </section>"""

porcelain_css = """/* Porcelain: fine blue-and-white china with gold rims.
   Layers: fixed glaze page + a vine pattern (mask, coloured by hero) → the cover
   panel with a gilded plate turning in 3D as you scroll → glazed cards with gold
   and cobalt rim lines and vine corners crossing their edges.
   All art is a mask filled with palette tokens, so every colourway works. */
""" + base_css(P, "porcelain") + f"""
/* ---------- page layers ---------- */
.pc::before {{ content: ""; position: fixed; inset: 0; z-index: -2;
  background: radial-gradient(110% 60% at 20% 0%, var(--c-card), transparent 60%), radial-gradient(90% 60% at 100% 100%, color-mix(in srgb, var(--c-hero) 8%, transparent), transparent 70%), var(--c-bg); }}
.has-pattern-tile .pc::after {{ content: ""; position: fixed; inset: 0; z-index: -1; pointer-events: none; opacity: 0.09;
  background: var(--c-hero); -webkit-mask: var(--img-pattern-tile) 0 0 / 150px; mask: var(--img-pattern-tile) 0 0 / 150px; }}
.pc[data-ornament="refined"]::after {{ opacity: 0.04; }}
.pc-title {{ color: var(--c-hero); }}
.pc:lang(en) .pc-title {{ font-style: italic; font-size: 36px; }}
.pc {{ --pc-foil-text: linear-gradient(115deg, var(--c-hero) 0%, var(--c-hero) 38%, var(--pc-gold-deep) 50%, var(--c-hero) 62%, var(--c-hero) 100%); }}

/* ---------- 1 · cover: the gilded plate ---------- */
.pc-cover {{ padding-block: 40px 30px; padding-inline: 18px; }}
.pc-panel {{ position: relative; isolation: isolate; display: flex; flex-direction: column; align-items: center; gap: 16px; padding-block: 30px 40px; padding-inline: 20px; perspective: 900px; }}
.pc-plate {{
  position: relative; display: grid; place-items: center;
  inline-size: min(330px, 86vw); aspect-ratio: 1; border-radius: 50%;
  border: 8px solid transparent;
  background: radial-gradient(circle at 35% 30%, var(--c-card), color-mix(in srgb, var(--c-card) 88%, var(--c-hero)) 75%) padding-box, var(--pc-foil) border-box;
  box-shadow: 0 0 0 2px color-mix(in srgb, var(--c-accent) 60%, transparent), 0 40px 50px -26px color-mix(in srgb, var(--c-hero) 55%, transparent), 0 0 70px -20px color-mix(in srgb, var(--c-accent) 45%, transparent);
  transform: rotateX(18deg);
}}
.pc-plate__band {{ position: absolute; inset: 5%; display: none; background: var(--c-hero); }}
.has-plate-art .pc-plate__band {{ display: block; -webkit-mask: var(--img-plate-art) center / contain no-repeat; mask: var(--img-plate-art) center / contain no-repeat; }}
.pc-plate__glaze {{ position: absolute; inset: 0; border-radius: 50%; pointer-events: none;
  background: linear-gradient(120deg, transparent 30%, color-mix(in srgb, var(--c-card) 85%, transparent) 45%, transparent 58%) 140% 0 / 260% 100% no-repeat; mix-blend-mode: screen; }}
.pc-plate__photo {{ inline-size: 52%; aspect-ratio: 1; border-radius: 50%; padding: 4px; background: var(--pc-foil); box-shadow: 0 0 0 5px var(--c-card), 0 0 0 6px var(--c-hero); }}
.pc-plate__photo img {{ display: block; inline-size: 100%; block-size: 100%; object-fit: cover; border-radius: 50%; }}
.pc-plate__amp {{ font-family: var(--font-latin); font-style: italic; font-size: 110px; line-height: 1; background: var(--pc-foil); -webkit-background-clip: text; background-clip: text; color: transparent; }}
.pc-lead {{ margin-block-start: 22px; }}
.pc:lang(en) .pc-lead {{ font-style: italic; }}
.pc:lang(en) .pc-names {{ font-style: italic; }}
.pc-date {{ padding-block: 8px; padding-inline: 24px; border-block: 1px solid var(--c-accent); font-size: 15px; color: var(--c-hero); }}
/* layout "frame": a patterned porcelain tile panel with a small medallion */
.pc-panel__pattern {{ display: none; }}
.pc[data-cover-layout="frame"] .pc-panel {{ padding-block: 56px; padding-inline: 34px; background: var(--c-card);
  box-shadow: 0 0 0 1px var(--c-line), 0 30px 50px -28px color-mix(in srgb, var(--c-hero) 55%, transparent); outline: 2px solid var(--c-accent); outline-offset: -12px; border-radius: var(--radius); }}
.pc[data-cover-layout="frame"] .pc-panel__pattern {{ display: block; position: absolute; inset: 0; z-index: -1; border-radius: var(--radius); background: var(--c-hero); }}
.pc[data-cover-layout="frame"] .pc-panel__pattern {{ -webkit-mask: var(--img-pattern-tile) 0 0 / 110px; mask: var(--img-pattern-tile) 0 0 / 110px; clip-path: polygon(evenodd, 0 0, 100% 0, 100% 100%, 0 100%, 0 0, 26px 26px, 26px calc(100% - 26px), calc(100% - 26px) calc(100% - 26px), calc(100% - 26px) 26px, 26px 26px); }}
.pc[data-cover-layout="frame"] .pc-plate {{ inline-size: 170px; border-width: 5px; transform: none; }}
.pc[data-cover-layout="frame"] .pc-plate__amp {{ font-size: 60px; }}

/* ---------- glazed cards with gold + cobalt rims ---------- */
.pc-card {{
  position: relative; z-index: 1; padding-block: 50px; padding-inline: 28px; border-radius: var(--radius);
  background: linear-gradient(115deg, transparent 36%, color-mix(in srgb, var(--c-card) 80%, var(--c-bg)) 50%, transparent 64%) 160% 0 / 250% 100% no-repeat, var(--c-card);
  outline: 2px solid var(--c-accent); outline-offset: -9px;
  box-shadow: inset 0 0 0 14px var(--c-card), inset 0 0 0 15px var(--c-hero), 0 0 0 1px var(--c-line),
    0 32px 50px -28px color-mix(in srgb, var(--c-hero) 55%, transparent), 0 0 60px -26px color-mix(in srgb, var(--c-accent) 50%, transparent);
}}
.pc-invite {{ margin-block-start: 10px; }}
.has-corner-art .pc-card::before, .has-corner-art .pc-card::after {{
  content: ""; position: absolute; inset-block-start: -20px; inline-size: 92px; block-size: 92px; z-index: 2; pointer-events: none;
  background: var(--c-hero); -webkit-mask: var(--img-corner-art) center / contain no-repeat; mask: var(--img-corner-art) center / contain no-repeat; }}
.has-corner-art .pc-card::before {{ inset-inline-start: -18px; }}
.has-corner-art .pc-card::after {{ inset-inline-end: -18px; }}
.pc-card:dir(ltr)::after, .pc-card:dir(rtl)::before {{ transform: scaleX(-1); }}
.pc[data-ornament="refined"] .pc-card::before, .pc[data-ornament="refined"] .pc-card::after {{ display: none; }}
.pc-count__num {{ font-size: 84px; }}

/* photo frames: plate · arch · scalloped */
.pc-photo {{ padding: 5px; border-radius: 50%; aspect-ratio: 1; background: var(--pc-foil); box-shadow: 0 0 0 4px var(--c-card), 0 0 0 5px var(--c-hero), 0 18px 28px -16px color-mix(in srgb, var(--c-hero) 60%, transparent); }}
.pc[data-photo-frame="arch"] .pc-photo {{ aspect-ratio: 3 / 4; border-radius: 999px 999px 6px 6px; }}
.pc[data-photo-frame="scalloped"] .pc-photo, .pc[data-photo-frame="scalloped"] .pc-photo img {{ aspect-ratio: 1; border-radius: 0; box-shadow: none; clip-path: {SCALLOP}; }}
.pc[data-photo-frame="scalloped"] .pc-photo {{ padding: 6px; }}
.pc-flow__item img {{ border: 4px solid transparent; background: var(--pc-foil) border-box; border-radius: var(--radius); box-shadow: inset 0 0 0 2px var(--c-card), 0 24px 36px -20px color-mix(in srgb, var(--c-hero) 70%, transparent); }}

/* ---------- motion ---------- */
@supports (animation-timeline: view()) {{
  .pc-plate {{ animation: porcelain-spin linear both; animation-timeline: view(); }}
  .pc-plate__glaze {{ animation: porcelain-glaze linear both; animation-timeline: view(); }}
  .pc-card {{ animation: porcelain-shine linear both; animation-timeline: view(); animation-range: entry 20% cover 60%; }}
}}
@keyframes porcelain-spin {{ from {{ transform: rotateX(28deg) rotate(-20deg); }} to {{ transform: rotateX(8deg) rotate(25deg); }} }}
@keyframes porcelain-glaze {{ from {{ background-position: 140% 0; }} to {{ background-position: -40% 0; }} }}
@keyframes porcelain-shine {{ from {{ background-position: 160% 0, 0 0; }} to {{ background-position: -60% 0, 0 0; }} }}
.pc[data-cover-layout="frame"] .pc-plate {{ animation: none; }}

/* own reveal: a glaze that settles */
.fx-glaze {{ opacity: 0; transform: scale(0.96); filter: brightness(1.3) saturate(0.5);
  transition: opacity var(--fx-dur, 1s) ease, transform var(--fx-dur, 1s) cubic-bezier(.2, .7, .2, 1), filter var(--fx-dur, 1s) ease; }}
.fx-glaze.is-in {{ filter: none; }}
""" + REDUCED.replace("@@", P)

porcelain_manifest = manifest(
    "porcelain", {"ar": "بورسلين", "en": "Porcelain"},
    {"ar": "خزف أزرق وأبيض بحواف ذهبية: طبق مذهب يدور بعمق ثلاثي الأبعاد، نقش أغصان ناعم، وكروت مزججة.",
     "en": "Fine blue-and-white china with gold rims: a gilded plate turning in 3D, a soft vine pattern and glazed cards."},
    texts({"ar": "يسعدنا دعوتكم لحضور حفل زفاف", "en": "Together with their families invite you to the wedding of"},
          {"ar": "باقي على الفرح", "en": "Counting the days"}, {"ar": "حكايتنا", "en": "Our story"},
          {"ar": "من صورنا", "en": "Moments"}, {"ar": "اسحبوا لمشاهدة كل الصور", "en": "Swipe through the moments"},
          {"ar": "المواعيد", "en": "The celebrations"}, {"ar": "اكتب دعوة للعروسين", "en": "Leave a wish"}),
    [], ["patternTile", "plateArt", "cornerArt", "sparkleArt"],
    [("plate", "طبق مذهب ثلاثي الأبعاد", "Gilded 3D plate"), ("frame", "لوحة خزف بإطار منقوش", "Patterned tile frame")],
    [("plate", "إطار طبق دائري", "Round plate"), ("arch", "قوس", "Arch"), ("scalloped", "حافة مموجة", "Scalloped")],
    [pal("cobalt", "كوبالت وذهبي", "Cobalt & gold", hero="#1E3F8C", onHero="#F7F8FB", accent="#C6A15B", bg="#F4F6FA", text="#1C2A4A", muted="#5F6B85", card="#FFFFFF", line="#D9DFEC"),
     pal("celadon", "سيلادون", "Celadon", hero="#2C6A58", onHero="#F5FAF7", accent="#C6A15B", bg="#F2F7F4", text="#1E3A31", muted="#5C7268", card="#FFFFFF", line="#D5E3DB"),
     pal("rouge", "أحمر صيني", "Rouge", hero="#9B2B2B", onHero="#FFF8F5", accent="#C6A15B", bg="#FBF4F1", text="#3B1A1A", muted="#7D5F5B", card="#FFFFFF", line="#EBD9D3"),
     pal("rosePorcelain", "وردي وذهب وردي", "Rose & rose gold", hero="#B0607A", onHero="#FFF7F9", accent="#C99A84", bg="#FBF3F5", text="#3F2430", muted="#7F6470", card="#FFFFFF", line="#EDD8DE"),
     pal("midnightChina", "خزف ليلي", "Midnight china", hero="#E3E9F7", onHero="#10182E", accent="#D4B26B", bg="#10182E", text="#EEF1F8", muted="#9AA6C2", card="#1A2440", line="#2C3858")],
    {"display": "amiri", "body": "serifPair", "latin": "cormorant"},
    {"patternTile": "porcelain-tile", "plateArt": "porcelain-plate", "cornerArt": "porcelain-corner", "sparkleArt": "sparkle"},
    ("glaze", "تزجيج", "Glaze settle"), None, "doors", (14, 52))

# ======================================================================== GLASS GARDEN
P = "gg"
glass_cover = f"""  <section class="gg-cover" data-animate="cover">
    <div class="gg-house">
      <span class="gg-house__glass" aria-hidden="true"></span>
      <span class="gg-house__frame" aria-hidden="true"></span>
      <span class="gg-house__glare" aria-hidden="true"></span>
      <span class="gg-ivy gg-decor" aria-hidden="true"></span>
      <span class="gg-plant gg-plant--start" aria-hidden="true" data-parallax></span>
      <span class="gg-plant gg-plant--end gg-decor" aria-hidden="true"></span>
      {sparks(P, 3)}
      <div class="gg-house__content">
        {{{{#if story.photos.length}}}}
          {{{{#with story.photos.[0]}}}}<figure class="gg-portrait"><img src="{{{{url}}}}" alt="{{{{text "storyPhoto"}}}}" loading="lazy"></figure>{{{{/with}}}}
        {{{{/if}}}}
        <p class="gg-lead">{{{{text "lead"}}}}</p>
        {names(P)}
        {{{{#unless (variant "dateStyle" "calendar")}}}}<p class="gg-date">{{{{formatDate mainDate}}}}</p>{{{{/unless}}}}
      </div>
    </div>
    <div class="gg-card gg-invite">
      {{{{#if verse}}}}<p class="gg-verse">{{{{verse}}}}</p>{{{{/if}}}}
{families(P)}
    </div>
  </section>"""

glass_css = """/* Glass Garden: a Victorian glasshouse at golden hour.
   Layers: fixed golden-hour gradient + light rays → the glasshouse (frosted
   panes, brass frame as a mask, a glare crossing the glass as you scroll) →
   ferns and ivy overlapping the frame → frosted-glass cards (backdrop blur)
   with brass corner brackets. Ambient: floating pollen light. */
""" + base_css(P, "glass-garden") + """
/* ---------- page layers ---------- */
.gg::before { content: ""; position: fixed; inset: 0; z-index: -2;
  background:
    radial-gradient(80% 50% at 15% 0%, color-mix(in srgb, var(--c-accent) 35%, transparent), transparent 70%),
    linear-gradient(170deg, color-mix(in srgb, var(--c-accent) 18%, var(--c-bg)) 0%, var(--c-bg) 45%, color-mix(in srgb, var(--c-hero) 16%, var(--c-bg)) 100%); }
.gg::after { content: ""; position: fixed; inset-block-start: -10%; inset-inline: 0; block-size: 90svh; z-index: -1; pointer-events: none;
  background: repeating-conic-gradient(from 150deg at 0% 0%, color-mix(in srgb, var(--c-card) 45%, transparent) 0deg 3deg, transparent 3deg 11deg);
  -webkit-mask-image: radial-gradient(90% 80% at 0% 0%, var(--c-text) 10%, transparent 70%); mask-image: radial-gradient(90% 80% at 0% 0%, var(--c-text) 10%, transparent 70%); }
.gg-title { color: var(--c-hero); }
.gg:lang(en) .gg-title { letter-spacing: 0.08em; font-size: 32px; }
.gg { --gg-foil-text: linear-gradient(115deg, var(--c-hero) 0%, var(--c-hero) 38%, var(--gg-gold-deep) 50%, var(--c-hero) 62%, var(--c-hero) 100%); }

/* ---------- 1 · cover: the glasshouse ---------- */
.gg-cover { padding-block: 30px 30px; padding-inline: 16px; }
.gg-house { position: relative; isolation: isolate; inline-size: 100%; aspect-ratio: 400 / 560; display: flex; align-items: flex-end; justify-content: center; }
.gg-house__glass { position: absolute; inset: 2% 6% 0; z-index: -2; border-radius: 50% 50% 0 0 / 34% 34% 0 0;
  background: linear-gradient(160deg, color-mix(in srgb, var(--c-card) 55%, transparent), color-mix(in srgb, var(--c-card) 20%, transparent) 60%, color-mix(in srgb, var(--c-accent) 18%, transparent));
  -webkit-backdrop-filter: blur(6px); backdrop-filter: blur(6px); }
.gg-house__frame { position: absolute; inset: 0; z-index: -1; background: var(--gg-foil); display: none; }
.has-frame-art .gg-house__frame { display: block; -webkit-mask: var(--img-frame-art) center / 100% 100% no-repeat; mask: var(--img-frame-art) center / 100% 100% no-repeat; filter: drop-shadow(0 6px 10px color-mix(in srgb, var(--c-hero) 30%, transparent)); }
.gg-house__glare { position: absolute; inset: 2% 6% 0; z-index: -1; border-radius: 50% 50% 0 0 / 34% 34% 0 0; pointer-events: none;
  background: linear-gradient(115deg, transparent 30%, color-mix(in srgb, var(--c-card) 75%, transparent) 42%, transparent 50%, transparent 56%, color-mix(in srgb, var(--c-card) 40%, transparent) 60%, transparent 66%) 150% 0 / 260% 100% no-repeat; }
.gg-house__content { position: relative; z-index: 1; display: flex; flex-direction: column; align-items: center; gap: 14px; padding-block: 0 56px; padding-inline: 46px; }
.gg-portrait { inline-size: 120px; aspect-ratio: 3 / 4; padding: 4px; border-radius: 999px 999px 8px 8px; background: var(--gg-foil); box-shadow: 0 16px 30px -14px color-mix(in srgb, var(--c-hero) 60%, transparent); }
.gg-portrait img { display: block; inline-size: 100%; block-size: 100%; object-fit: cover; border-radius: inherit; }
.gg-lead { color: var(--c-text); }
.gg:lang(en) .gg-names { letter-spacing: 0.04em; }
.gg-date { padding-block: 8px; padding-inline: 22px; border-radius: 999px; background: color-mix(in srgb, var(--c-card) 60%, transparent); -webkit-backdrop-filter: blur(8px); backdrop-filter: blur(8px); box-shadow: inset 0 0 0 1px var(--c-accent); font-size: 15px; }
/* plants overlapping the frame */
.gg-plant { position: absolute; inset-block-end: -6%; z-index: 2; inline-size: 44%; aspect-ratio: 260 / 310; display: none; background: var(--c-hero); pointer-events: none; }
.has-plant-art .gg-plant { display: block; -webkit-mask: var(--img-plant-art) center bottom / contain no-repeat; mask: var(--img-plant-art) center bottom / contain no-repeat; }
.gg-plant--start { inset-inline-start: -8%; }
.gg-plant--end { inset-inline-end: -10%; inline-size: 36%; transform: scaleX(-1); filter: brightness(1.25); }
.gg-plant--start:dir(rtl) { transform: scaleX(-1); }
.gg-plant--end:dir(rtl) { transform: none; }
.gg-ivy { position: absolute; inset-block-start: 4%; inset-inline-end: 4%; z-index: 2; inline-size: 18%; aspect-ratio: 120 / 480; display: none; background: var(--c-hero); pointer-events: none; transform-origin: 50% 0; }
.has-vine-art .gg-ivy { display: block; -webkit-mask: var(--img-vine-art) center top / contain no-repeat; mask: var(--img-vine-art) center top / contain no-repeat; }
/* layout "window": a round rose window instead of the house */
.gg[data-cover-layout="window"] .gg-house { aspect-ratio: auto; flex-direction: column; align-items: center; padding-block-start: 300px; }
.gg[data-cover-layout="window"] .gg-house__frame, .gg[data-cover-layout="window"] .gg-ivy { display: none; }
.gg[data-cover-layout="window"] .gg-house__glass, .gg[data-cover-layout="window"] .gg-house__glare {
  inset: 0; margin-inline: auto; inline-size: 270px; block-size: 270px; border-radius: 50%; border: 6px solid transparent;
  background: repeating-conic-gradient(from 0deg, var(--c-accent) 0deg 1deg, transparent 1deg 30deg) padding-box,
    radial-gradient(circle, transparent 28%, var(--c-accent) 28.5% 29.5%, transparent 30%, transparent 62%, var(--c-accent) 62.5% 63.5%, transparent 64%) padding-box,
    radial-gradient(circle at 35% 30%, color-mix(in srgb, var(--c-card) 70%, transparent), color-mix(in srgb, var(--c-card) 25%, transparent)) padding-box,
    var(--gg-foil) border-box; }
.gg[data-cover-layout="window"] .gg-house__glare { background: linear-gradient(115deg, transparent 35%, color-mix(in srgb, var(--c-card) 70%, transparent) 48%, transparent 58%) 150% 0 / 260% 100% no-repeat; border-color: transparent; }
.gg[data-cover-layout="window"] .gg-house__content { padding-block-end: 20px; }
.gg[data-cover-layout="window"] .gg-plant { inset-block-end: auto; inset-block-start: 140px; }

/* ---------- frosted glass cards with brass brackets ---------- */
.gg-card {
  position: relative; z-index: 1; padding-block: 48px; padding-inline: 26px; border-radius: var(--radius);
  background: linear-gradient(115deg, transparent 35%, color-mix(in srgb, var(--c-card) 70%, transparent) 48%, transparent 60%) 160% 0 / 250% 100% no-repeat,
    color-mix(in srgb, var(--c-card) 58%, transparent);
  -webkit-backdrop-filter: blur(18px) saturate(1.3); backdrop-filter: blur(18px) saturate(1.3);
  box-shadow: inset 0 1px 0 color-mix(in srgb, var(--c-card) 90%, transparent), inset 0 0 0 1px color-mix(in srgb, var(--c-card) 70%, transparent),
    0 30px 50px -30px color-mix(in srgb, var(--c-hero) 55%, transparent), 0 0 60px -30px color-mix(in srgb, var(--c-accent) 60%, transparent);
}
.gg-card::before, .gg-card::after { content: ""; position: absolute; inline-size: 34px; block-size: 34px; pointer-events: none; border: 2px solid var(--c-accent); }
.gg-card::before { inset-block-start: 10px; inset-inline-start: 10px; border-inline-end: 0; border-block-end: 0; border-start-start-radius: 8px; }
.gg-card::after { inset-block-end: 10px; inset-inline-end: 10px; border-inline-start: 0; border-block-start: 0; border-end-end-radius: 8px; }
.gg-invite { margin-block-start: 10px; }
.gg-sprig { position: absolute; inset-block-end: -26px; inset-inline-start: -22px; z-index: 2; inline-size: 96px; aspect-ratio: 260 / 310; display: none; background: var(--c-hero); pointer-events: none; }
.has-plant-art .gg-sprig { display: block; -webkit-mask: var(--img-plant-art) center bottom / contain no-repeat; mask: var(--img-plant-art) center bottom / contain no-repeat; }
.gg-sprig:dir(rtl) { transform: scaleX(-1); }
.gg-event:nth-of-type(odd) .gg-sprig { inset-inline: auto -22px; transform: scaleX(-1); }
.gg-event:nth-of-type(odd) .gg-sprig:dir(rtl) { transform: none; }

/* photo frames: arch · circle · pane */
.gg-photo { padding: 4px; border-radius: 999px 999px 8px 8px; background: var(--gg-foil); box-shadow: 0 18px 28px -16px color-mix(in srgb, var(--c-hero) 60%, transparent); }
.gg[data-photo-frame="circle"] .gg-photo { aspect-ratio: 1; border-radius: 50%; }
.gg[data-photo-frame="pane"] .gg-photo { border-radius: 4px; }
.gg[data-photo-frame="pane"] .gg-photo::after { content: ""; position: absolute; inset: 4px; pointer-events: none;
  background: linear-gradient(var(--c-accent), var(--c-accent)) center / 3px 100% no-repeat, linear-gradient(var(--c-accent), var(--c-accent)) center 38% / 100% 3px no-repeat,
    linear-gradient(130deg, transparent 40%, color-mix(in srgb, var(--c-card) 45%, transparent) 50%, transparent 60%); }
/* gallery panes with a reflection on the glasshouse floor */
.gg-flow__item img { border-radius: var(--radius); border: 3px solid transparent; background: var(--gg-foil) border-box;
  -webkit-box-reflect: below 8px linear-gradient(transparent 62%, color-mix(in srgb, var(--c-text) 28%, transparent)); }
.gg-flow { padding-block-end: 90px; }

/* ---------- motion ---------- */
@supports (animation-timeline: view()) {
  .gg-house__glare { animation: glass-garden-glare linear both; animation-timeline: view(); }
  .gg-ivy { animation: glass-garden-sway linear both; animation-timeline: view(); }
  .gg-card { animation: glass-garden-shine linear both; animation-timeline: view(); animation-range: entry 20% cover 60%; }
}
@keyframes glass-garden-glare { from { background-position: 150% 0; } to { background-position: -50% 0; } }
@keyframes glass-garden-sway { 0% { rotate: 4deg; } 50% { rotate: -3deg; } 100% { rotate: 1deg; } }
@keyframes glass-garden-shine { from { background-position: 160% 0, 0 0; } to { background-position: -60% 0, 0 0; } }

/* own reveal: frost clearing from the glass */
.fx-frost { opacity: 0; transform: translateY(20px); filter: blur(12px);
  transition: opacity var(--fx-dur, 1s) ease, transform var(--fx-dur, 1s) cubic-bezier(.2, .7, .2, 1), filter var(--fx-dur, 1s) ease; }
.fx-frost.is-in { filter: none; }

/* own ambient: pollen light floating up */
.ambient-pollen { background-image:
    radial-gradient(2px 2px at 14% 30%, color-mix(in srgb, var(--c-accent) 80%, transparent), transparent),
    radial-gradient(3px 3px at 42% 70%, color-mix(in srgb, var(--c-card) 90%, transparent), transparent),
    radial-gradient(2px 2px at 70% 40%, color-mix(in srgb, var(--c-accent) 80%, transparent), transparent),
    radial-gradient(2.5px 2.5px at 88% 85%, color-mix(in srgb, var(--c-card) 90%, transparent), transparent);
  background-size: 260px 460px; opacity: 0.8; animation: pollen-float 30s linear infinite; }
@keyframes pollen-float { to { background-position: 40px -460px; } }
@media (prefers-reduced-motion: reduce) { .ambient-pollen { animation-duration: 120s; } }
""" + REDUCED.replace("@@", P)

glass_manifest = manifest(
    "glass-garden", {"ar": "حديقة زجاجية", "en": "Glass Garden"},
    {"ar": "بيت زجاجي فيكتوري وقت الغروب: ألواح زجاج مثلجة، إطار نحاسي، سرخس ولبلاب يتخطى الحواف، وكروت من زجاج.",
     "en": "A Victorian glasshouse at golden hour: frosted panes, a brass frame, ferns and ivy spilling over the edges, and frosted-glass cards."},
    texts({"ar": "بين الزهور والضوء، ندعوكم لحضور حفل زفاف", "en": "Among the leaves and the light, please join us for the wedding of"},
          {"ar": "باقي على الفرح", "en": "Until we bloom"}, {"ar": "حكايتنا", "en": "Our story"},
          {"ar": "من صورنا", "en": "Through the glass"}, {"ar": "اسحبوا لمشاهدة كل الصور", "en": "Swipe through the panes"},
          {"ar": "المواعيد", "en": "The celebrations"}, {"ar": "اكتب دعوة للعروسين", "en": "Leave a note in the garden"}),
    [], ["frameArt", "plantArt", "vineArt", "sparkleArt"],
    [("glasshouse", "بيت زجاجي", "Glasshouse"), ("window", "نافذة دائرية", "Rose window")],
    [("arch", "قوس", "Arch"), ("circle", "دائرة", "Circle"), ("pane", "لوح زجاج", "Glass pane")],
    [pal("sageBrass", "مريمية ونحاس", "Sage & brass", hero="#3E5E45", onHero="#F6F4EC", accent="#B08D57", bg="#EEF1E8", text="#1F2E24", muted="#5E6C60", card="#FAFBF6", line="#D3DBCB"),
     pal("blushGlass", "زجاج وردي", "Blush glass", hero="#A0566A", onHero="#FFF8F6", accent="#C49A82", bg="#F7ECEC", text="#3A2229", muted="#7D6268", card="#FFF9F8", line="#EBD6D6"),
     pal("aqua", "تركواز", "Aqua", hero="#2F6F73", onHero="#F4FBFA", accent="#B9975B", bg="#EAF3F2", text="#19393B", muted="#587577", card="#F8FCFB", line="#CFE2E0"),
     pal("ivoryGold", "عاجي وذهبي", "Ivory & gold", hero="#5F6A34", onHero="#FFFDF6", accent="#C8A45E", bg="#F6F2E6", text="#2B2A1C", muted="#6E6B58", card="#FFFDF6", line="#E3DCC6"),
     pal("nightGarden", "حديقة ليلية", "Night garden", hero="#CFE3C8", onHero="#0E1C14", accent="#D2B26A", bg="#0E1C14", text="#EAF2E6", muted="#9DB3A0", card="#1B3323", line="#2B4733")],
    {"display": "elMessiri", "body": "plexArabic", "latin": "italiana"},
    {"frameArt": "glasshouse", "plantArt": "fern", "vineArt": "ivy", "sparkleArt": "sparkle"},
    ("frost", "انقشاع الضباب", "Frost clearing"), ("pollen", "ضوء متطاير", "Floating pollen light"), "doors", (20, 50))

# ======================================================================== LACE
P = "lc"
lace_cover = f"""  <section class="lc-cover" data-animate="cover">
    <span class="lc-pearls lc-decor" aria-hidden="true"></span>
    <div class="lc-veil">
      <span class="lc-doily" aria-hidden="true"></span>
      <div class="lc-veil__center">
        {{{{#if story.photos.length}}}}
          {{{{#with story.photos.[0]}}}}<figure class="lc-portrait"><img src="{{{{url}}}}" alt="{{{{text "storyPhoto"}}}}" loading="lazy"></figure>{{{{/with}}}}
        {{{{else}}}}
          <span class="lc-veil__amp" aria-hidden="true">{{{{text "and"}}}}</span>
        {{{{/if}}}}
      </div>
      {sparks(P, 3)}
    </div>
    <div class="lc-card lc-invite">
      <span class="lc-ribbon lc-decor" aria-hidden="true"></span>
      <p class="lc-lead">{{{{text "lead"}}}}</p>
      {names(P)}
      {{{{#unless (variant "dateStyle" "calendar")}}}}<p class="lc-date">{{{{formatDate mainDate}}}}</p>{{{{/unless}}}}
      {{{{#if verse}}}}<p class="lc-verse">{{{{verse}}}}</p>{{{{/if}}}}
{families(P)}
    </div>
  </section>"""

lace_css = """/* Lace: bridal lace and pearls on silk.
   Layers: fixed satin page with soft folds + a lace net (mask, lace colour) →
   a pearl garland across the top → a lace doily framing the couple's portrait →
   silk cards with a pearl row on top and a lace trim hanging below the edge.
   Names in a flowing script. */
""" + base_css(P, "lace") + f"""
/* ---------- page layers ---------- */
.lc::before {{ content: ""; position: fixed; inset: 0; z-index: -2;
  background: linear-gradient(115deg, var(--c-bg) 0%, color-mix(in srgb, var(--c-bg) 70%, var(--c-card)) 22%, var(--c-bg) 40%, color-mix(in srgb, var(--c-bg) 86%, var(--c-hero)) 62%, color-mix(in srgb, var(--c-bg) 70%, var(--c-card)) 80%, var(--c-bg) 100%); }}
.has-pattern-tile .lc::after {{ content: ""; position: fixed; inset: 0; z-index: -1; pointer-events: none; opacity: 0.35;
  background: var(--c-lace); -webkit-mask: var(--img-pattern-tile) 0 0 / 96px; mask: var(--img-pattern-tile) 0 0 / 96px; }}
.lc[data-ornament="refined"]::after {{ opacity: 0.15; }}
.lc-title {{ color: var(--c-hero); }}
.lc:lang(en) .lc-title {{ font-size: 44px; }}
.lc {{ --lc-foil-text: linear-gradient(115deg, var(--c-hero) 0%, var(--c-hero) 38%, var(--lc-gold-deep) 50%, var(--c-hero) 62%, var(--c-hero) 100%); }}
.lc-names {{ font-size: var(--name-size); line-height: 1.35; }}
.lc:lang(en) .lc-names {{ font-size: calc(var(--name-size) * 1.15); line-height: 1.2; }}
.lc-and {{ font-size: 0.7em; }}

/* ---------- 1 · cover: pearls, doily, portrait ---------- */
.lc-cover {{ position: relative; padding-block: 70px 30px; padding-inline: 18px; }}
.lc-pearls {{ position: absolute; inset-block-start: 0; inset-inline: -4%; block-size: 90px; display: none; z-index: 3; pointer-events: none; filter: drop-shadow(0 4px 4px color-mix(in srgb, var(--c-text) 25%, transparent)); }}
.has-pearl-art .lc-pearls {{ display: block; background: var(--img-pearl-art) center top / 100% auto no-repeat; }}
.lc-veil {{ position: relative; display: grid; place-items: center; inline-size: min(360px, 92vw); aspect-ratio: 1; margin-inline: auto; }}
.lc-doily {{ position: absolute; inset: 0; display: none; background: var(--c-lace); filter: drop-shadow(0 10px 14px color-mix(in srgb, var(--c-text) 22%, transparent)); }}
.has-doily-art .lc-doily {{ display: block; -webkit-mask: var(--img-doily-art) center / contain no-repeat; mask: var(--img-doily-art) center / contain no-repeat; }}
.lc-veil__center {{ position: relative; display: grid; place-items: center; inline-size: 44%; aspect-ratio: 1; }}
.lc-portrait {{ inline-size: 100%; aspect-ratio: 4 / 5; border-radius: 50%; border: 7px dotted var(--c-lace); padding: 3px; background: var(--c-card) padding-box; box-shadow: 0 0 0 2px var(--c-accent); filter: drop-shadow(0 6px 8px color-mix(in srgb, var(--c-text) 30%, transparent)); }}
.lc-portrait img {{ display: block; inline-size: 100%; block-size: 100%; object-fit: cover; border-radius: 50%; }}
.lc-veil__amp {{ font-family: var(--font-latin); font-size: 110px; line-height: 1; background: var(--lc-foil); -webkit-background-clip: text; background-clip: text; color: transparent; }}
.lc-invite {{ margin-block-start: 12px; padding-block-start: 56px; }}
.lc-lead {{ font-style: italic; }}
.lc-date {{ display: inline-block; margin-block-start: 14px; padding-block: 8px; padding-inline: 24px; border-radius: 999px; box-shadow: inset 0 0 0 1px var(--c-accent); color: var(--c-hero); font-size: 15px; }}
.lc-verse {{ margin-block-start: 18px; }}
/* satin ribbon tied across the top of the invitation */
.lc-ribbon {{ position: absolute; inset-block-start: -14px; inset-inline: 30%; block-size: 28px; z-index: 3; border-radius: 4px;
  background: linear-gradient(var(--c-hero), color-mix(in srgb, var(--c-hero) 70%, var(--c-card)) 45%, var(--c-hero)); box-shadow: 0 6px 10px -4px color-mix(in srgb, var(--c-text) 40%, transparent); }}
.lc-ribbon::before, .lc-ribbon::after {{ content: ""; position: absolute; inset-block-start: 22px; inline-size: 22px; block-size: 44px; background: inherit; }}
.lc-ribbon::before {{ inset-inline-start: 34%; rotate: 18deg; clip-path: polygon(0 0, 100% 0, 100% 100%, 50% 82%, 0 100%); }}
.lc-ribbon::after {{ inset-inline-end: 34%; rotate: -18deg; clip-path: polygon(0 0, 100% 0, 100% 100%, 50% 82%, 0 100%); }}
/* layout "card": no doily, the invitation becomes the hero with a wide lace frame */
.lc[data-cover-layout="card"] .lc-veil {{ display: none; }}
.lc[data-cover-layout="card"] .lc-invite {{ padding-block: 90px 70px; }}
.lc[data-cover-layout="card"] .lc-invite::before {{ block-size: 18px; }}

/* ---------- silk cards: pearl row above, lace trim below ---------- */
.lc-card {{
  position: relative; z-index: 1; margin-block-end: 26px; padding-block: 48px 52px; padding-inline: 26px; border-radius: var(--radius);
  background: linear-gradient(115deg, transparent 35%, color-mix(in srgb, var(--c-card) 60%, var(--c-bg)) 48%, transparent 62%) 160% 0 / 250% 100% no-repeat, var(--c-card);
  outline: 1px solid var(--c-accent); outline-offset: -10px;
  box-shadow: 0 0 0 1px var(--c-line), 0 30px 46px -28px color-mix(in srgb, var(--c-text) 40%, transparent), 0 0 60px -28px color-mix(in srgb, var(--c-accent) 55%, transparent);
}}
.lc-card::before {{ content: ""; position: absolute; inset-block-start: -7px; inset-inline: 18px; block-size: 14px; pointer-events: none;
  background: radial-gradient(circle at 38% 34%, color-mix(in srgb, var(--c-lace) 70%, var(--c-card)) 0 18%, var(--c-lace) 38%, color-mix(in srgb, var(--c-lace) 75%, var(--c-text)) 70%, transparent 72%) 0 0 / 14px 14px repeat-x;
  filter: drop-shadow(0 2px 2px color-mix(in srgb, var(--c-text) 25%, transparent)); }}
.lc-card::after {{ content: ""; position: absolute; inset-block-end: -24px; inset-inline: 0; block-size: 26px; display: none; pointer-events: none; background: var(--c-card); }}
.has-edge-art .lc-card::after {{ display: block; -webkit-mask: var(--img-edge-art) 0 0 / 52px 100% repeat-x; mask: var(--img-edge-art) 0 0 / 52px 100% repeat-x; filter: drop-shadow(0 6px 5px color-mix(in srgb, var(--c-text) 18%, transparent)); }}
.lc[data-ornament="refined"] .lc-card::before {{ display: none; }}

/* photo frames: pearl oval · arch · scalloped */
.lc-photo {{ border-radius: 50%; border: 7px dotted var(--c-lace); padding: 3px; background: var(--c-card) padding-box; box-shadow: 0 0 0 2px var(--c-accent); filter: drop-shadow(0 8px 10px color-mix(in srgb, var(--c-text) 25%, transparent)); }}
.lc[data-photo-frame="arch"] .lc-photo {{ border-radius: 999px 999px 8px 8px; border: 4px solid transparent; background: var(--lc-foil) border-box; box-shadow: none; padding: 0; }}
.lc[data-photo-frame="scalloped"] .lc-photo, .lc[data-photo-frame="scalloped"] .lc-photo img {{ aspect-ratio: 1; border: 0; border-radius: 0; box-shadow: none; clip-path: {SCALLOP}; }}
.lc[data-photo-frame="scalloped"] .lc-photo {{ padding: 6px; background: var(--lc-foil); }}
.lc-flow__item img {{ border: 8px solid var(--c-card); border-block-end-width: 30px; border-radius: 2px; box-shadow: 0 0 0 1px var(--c-line), 0 22px 34px -18px color-mix(in srgb, var(--c-text) 50%, transparent); }}

/* ---------- motion ---------- */
@supports (animation-timeline: view()) {{
  .lc-doily {{ animation: lace-turn linear both; animation-timeline: view(); }}
  .lc-card {{ animation: lace-shine linear both; animation-timeline: view(); animation-range: entry 20% cover 60%; }}
  .lc-pearls {{ animation: lace-swing linear both; animation-timeline: view(); transform-origin: 50% 0; }}
}}
@keyframes lace-turn {{ from {{ rotate: -18deg; }} to {{ rotate: 30deg; }} }}
@keyframes lace-shine {{ from {{ background-position: 160% 0, 0 0; }} to {{ background-position: -60% 0, 0 0; }} }}
@keyframes lace-swing {{ from {{ translate: 0 -10px; }} to {{ translate: 0 14px; }} }}

/* own reveal: unfurls downward like a veil */
.fx-unfurl {{ opacity: 0; clip-path: inset(0 0 70% 0);
  transition: opacity var(--fx-dur, 1s) ease, clip-path var(--fx-dur, 1s) cubic-bezier(.6, 0, .2, 1); }}
.fx-unfurl.is-in {{ clip-path: inset(-60px -60px -60px -60px); }}
""" + REDUCED.replace("@@", P)

lace_manifest = manifest(
    "lace", {"ar": "دانتيل", "en": "Lace"},
    {"ar": "دانتيل العروس واللؤلؤ على الحرير: عقد لؤلؤ، مفرش دانتيل حول صورتكم، كروت حرير بحافة دانتيل، وخط يدوي ناعم.",
     "en": "Bridal lace and pearls on silk: a pearl garland, a lace doily around your portrait, silk cards with lace trims, and a flowing script."},
    texts({"ar": "بكل الحب ندعوكم لمشاركتنا فرحة زفاف", "en": "With love, we invite you to celebrate the marriage of"},
          {"ar": "باقي على الفرح", "en": "Until we say yes"}, {"ar": "حكايتنا", "en": "Our love story"},
          {"ar": "من صورنا", "en": "Sweet moments"}, {"ar": "اسحبوا لمشاهدة كل الصور", "en": "Swipe through our moments"},
          {"ar": "المواعيد", "en": "The celebrations"}, {"ar": "اكتب دعوة للعروسين", "en": "Write us a little note"}),
    ["lace"], ["patternTile", "edgeArt", "doilyArt", "pearlArt", "sparkleArt"],
    [("veil", "مفرش دانتيل حول الصورة", "Lace doily portrait"), ("card", "كارت دانتيل فقط", "Lace card only")],
    [("pearl", "إطار لؤلؤ بيضاوي", "Pearl oval"), ("arch", "قوس", "Arch"), ("scalloped", "حافة مموجة", "Scalloped")],
    [pal("ivoryChampagne", "عاجي وشمبانيا", "Ivory & champagne", hero="#8A6D4B", onHero="#FFFDF8", accent="#C8A97A", bg="#F4EBE0", text="#3B2E24", muted="#7A6A5C", card="#FFFCF7", line="#E8DCCB", lace="#FFFFFF"),
     pal("blushRose", "وردي وذهب وردي", "Blush & rose gold", hero="#A35D6A", onHero="#FFF8F6", accent="#C99A84", bg="#F1DEDA", text="#40262C", muted="#7F6168", card="#FFF8F6", line="#E9D0CB", lace="#FFFFFF"),
     pal("doveSilver", "رمادي وفضي", "Dove & silver", hero="#5E6470", onHero="#FAFAFB", accent="#AEB4BF", bg="#E9E9EC", text="#2A2D33", muted="#6B6F78", card="#FAFAFB", line="#DADBE0", lace="#FFFFFF"),
     pal("sageLace", "دانتيل مريمية", "Sage lace", hero="#5E7360", onHero="#FBFCFA", accent="#B9A16E", bg="#E5EBE3", text="#263027", muted="#66705F", card="#FBFCFA", line="#D6DED4", lace="#FFFFFF"),
     pal("midnightLace", "دانتيل على كحلي", "Midnight lace", hero="#F1EAE0", onHero="#141B2E", accent="#D3B47A", bg="#141B2E", text="#F2ECE2", muted="#A7AEC0", card="#1D2640", line="#313B58", lace="#E9E4DA")],
    {"display": "arefRuqaa", "body": "serifPair", "latin": "pinyon"},
    {"patternTile": "lace-tile", "edgeArt": "lace-edge", "doilyArt": "lace-doily", "pearlArt": "pearls", "sparkleArt": "sparkle"},
    ("unfurl", "انسدال الطرحة", "Veil unfurl"), None, "curtain", (10, 48))

# ======================================================================== DESERT BLOOM
P = "db"
desert_cover = f"""  <section class="db-cover" data-animate="cover">
    <div class="db-scene">
      <span class="db-stars" aria-hidden="true"></span>
      <span class="db-sun" aria-hidden="true"></span>
      {sparks(P, 3)}
      <div class="db-sky">
        <p class="db-lead">{{{{text "lead"}}}}</p>
        {names(P)}
        {{{{#unless (variant "dateStyle" "calendar")}}}}<p class="db-date">{{{{formatDate mainDate}}}}</p>{{{{/unless}}}}
      </div>
      <span class="db-dune db-dune--1" aria-hidden="true"></span>
      <span class="db-dune db-dune--2" aria-hidden="true"></span>
      <span class="db-palm db-palm--start" aria-hidden="true"></span>
      <span class="db-dune db-dune--3" aria-hidden="true"></span>
      <span class="db-palm db-palm--end db-decor" aria-hidden="true"></span>
      <span class="db-dune db-dune--4" aria-hidden="true"></span>
      <span class="db-bloom db-decor" aria-hidden="true"></span>
    </div>
    <div class="db-card db-invite">
      {{{{#if story.photos.length}}}}
        {{{{#with story.photos.[0]}}}}<figure class="db-portrait"><img src="{{{{url}}}}" alt="{{{{text "storyPhoto"}}}}" loading="lazy"></figure>{{{{/with}}}}
      {{{{/if}}}}
      {{{{#if verse}}}}<p class="db-verse">{{{{verse}}}}</p>{{{{/if}}}}
{families(P)}
    </div>
  </section>"""

desert_css = """/* Desert Bloom: an Arabian desert at sunset.
   Layers: fixed sunset sky → stars and a glowing sun → four dunes that move at
   different speeds as you scroll (real multi-layer parallax, CSS only) → date
   palms and desert roses (masks in palette colours) standing on the dunes →
   sand cards with gold double frames, a gold star crossing the top edge and a
   desert rose on a corner. Ambient: sand glints drifting on the wind. */
""" + base_css(P, "desert-bloom") + """
/* ---------- page layers ---------- */
.db::before { content: ""; position: fixed; inset: 0; z-index: -2;
  background: linear-gradient(var(--c-bg) 0%, color-mix(in srgb, var(--c-bg) 55%, var(--c-glow)) 40%, var(--c-glow) 70%, color-mix(in srgb, var(--c-glow) 60%, var(--c-dune)) 100%); }
.has-sand-texture .db::after { content: ""; position: fixed; inset: 0; z-index: -1; pointer-events: none; background: var(--img-sand-texture) 0 0 / 300px; opacity: 0.6; }
.db-title { color: var(--c-hero); }
.db { --db-foil-text: linear-gradient(115deg, var(--c-hero) 0%, var(--c-hero) 36%, var(--db-gold-deep) 48%, var(--c-accent) 52%, var(--c-hero) 64%, var(--c-hero) 100%); }
.db:lang(en) .db-title { text-transform: uppercase; letter-spacing: 0.16em; font-size: 24px; }

/* ---------- 1 · cover: dunes at sunset ---------- */
.db-cover { padding-block: 0 30px; padding-inline: 0; }
.db-scene { position: relative; isolation: isolate; min-block-size: 720px; overflow: hidden; }
/* the sky grows with long names; the dunes stay pinned to the bottom below the text */
.db-stars { position: absolute; inset: 0 0 50%; z-index: -1; opacity: 0.7;
  background-image: radial-gradient(1.2px 1.2px at 10% 12%, var(--c-card), transparent), radial-gradient(1px 1px at 30% 26%, var(--c-card), transparent), radial-gradient(1.4px 1.4px at 52% 8%, var(--c-accent), transparent),
    radial-gradient(1px 1px at 72% 20%, var(--c-card), transparent), radial-gradient(1.2px 1.2px at 88% 10%, var(--c-card), transparent), radial-gradient(1px 1px at 64% 34%, var(--c-card), transparent);
  -webkit-mask-image: linear-gradient(var(--c-text), transparent); mask-image: linear-gradient(var(--c-text), transparent); }
.db-sun { position: absolute; inset-block-end: 210px; inset-inline-start: calc(50% - 90px); inline-size: 180px; block-size: 180px; border-radius: 50%; z-index: -1;
  background: radial-gradient(circle, var(--c-card) 0%, color-mix(in srgb, var(--c-accent) 70%, var(--c-card)) 38%, var(--c-accent) 60%, transparent 62%);
  box-shadow: 0 0 80px 30px color-mix(in srgb, var(--c-accent) 45%, transparent), 0 0 200px 80px color-mix(in srgb, var(--c-glow) 60%, transparent); }
.db-sky { position: relative; z-index: 2; display: flex; flex-direction: column; align-items: center; gap: 12px; padding-block: 76px 390px; padding-inline: 26px; }
.db-lead { color: var(--c-text); }
.db:lang(en) .db-lead { text-transform: uppercase; letter-spacing: 0.22em; font-size: 12px; line-height: 2; }
.db-names { filter: drop-shadow(0 2px 10px color-mix(in srgb, var(--c-glow) 80%, transparent)); }
.db:lang(en) .db-names { text-transform: uppercase; letter-spacing: 0.06em; font-size: calc(var(--name-size) * 0.8); }
.db-date { padding-block: 8px; padding-inline: 24px; border-block: 1px solid var(--c-accent); color: var(--c-hero); font-size: 15px; }
/* dunes: four layers of soft curves, darker as they come closer */
.db-dune { position: absolute; inset-inline: -20%; border-radius: 50% 50% 0 0 / 100% 100% 0 0; }
.db-dune--1 { inset-block-end: 150px; block-size: 160px; inset-inline: -40% 10%; background: linear-gradient(color-mix(in srgb, var(--c-dune) 70%, var(--c-glow)), var(--c-dune)); z-index: 0; }
.db-dune--2 { inset-block-end: 100px; block-size: 170px; inset-inline: 20% -50%; background: linear-gradient(color-mix(in srgb, var(--c-dune) 85%, var(--c-hero)), color-mix(in srgb, var(--c-dune) 75%, var(--c-hero))); z-index: 1; }
.db-dune--3 { inset-block-end: 40px; block-size: 160px; inset-inline: -50% 25%; background: linear-gradient(color-mix(in srgb, var(--c-dune) 65%, var(--c-hero)), color-mix(in srgb, var(--c-dune) 55%, var(--c-hero))); z-index: 3; }
.db-dune--4 { inset-block-end: -40px; block-size: 150px; inset-inline: -10% -30%; background: linear-gradient(color-mix(in srgb, var(--c-dune) 45%, var(--c-hero)), color-mix(in srgb, var(--c-dune) 35%, var(--c-hero))); z-index: 5;
  box-shadow: inset 0 3px 0 color-mix(in srgb, var(--c-accent) 50%, transparent); }
.db-palm { position: absolute; display: none; background: var(--c-silhouette); pointer-events: none; aspect-ratio: 240 / 400; }
.has-palm-art .db-palm { display: block; -webkit-mask: var(--img-palm-art) center bottom / contain no-repeat; mask: var(--img-palm-art) center bottom / contain no-repeat; }
.db-palm--start { inset-block-end: 190px; inset-inline-start: 4%; inline-size: 120px; z-index: 2; }
.db-palm--end { inset-block-end: 120px; inset-inline-end: -2%; inline-size: 170px; z-index: 4; }
.db-bloom { position: absolute; inset-block-end: 40px; inset-inline-start: 10%; inline-size: 110px; aspect-ratio: 1; display: none; z-index: 6; background: color-mix(in srgb, var(--c-accent) 55%, var(--c-hero)); pointer-events: none; }
.has-flower-art .db-bloom { display: block; -webkit-mask: var(--img-flower-art) center / contain no-repeat; mask: var(--img-flower-art) center / contain no-repeat; }
/* layout "arch": the same scene seen through a gilded arch window */
.db[data-cover-layout="arch"] .db-scene { inline-size: min(360px, 88%); margin-block-start: 30px; margin-inline: auto; min-block-size: 620px; border: 5px solid transparent;
  border-radius: 50% 50% 4px 4px / 32% 32% 4px 4px; background: linear-gradient(var(--c-bg), var(--c-glow)) padding-box, var(--db-foil) border-box;
  outline: 1px solid var(--c-accent); outline-offset: 8px; box-shadow: 0 40px 60px -30px color-mix(in srgb, var(--c-hero) 70%, transparent); }
.db[data-cover-layout="arch"] .db-scene { min-block-size: 700px; }
.db[data-cover-layout="arch"] .db-sun { inset-block-end: 140px; inline-size: 140px; block-size: 140px; inset-inline-start: calc(50% - 70px); }
.db[data-cover-layout="arch"] .db-sky { padding-block-start: 96px; padding-inline: 30px; }
.db[data-cover-layout="arch"] .db-palm--start { inset-block-end: 170px; inline-size: 90px; }
.db[data-cover-layout="arch"] .db-palm--end { inset-block-end: 110px; inline-size: 120px; }
.db[data-cover-layout="arch"] .db-names { font-size: calc(var(--name-size) * 0.82); }

/* ---------- sand cards with gold frames ---------- */
.db-card {
  position: relative; z-index: 6; padding-block: 52px; padding-inline: 28px; border-radius: var(--radius);
  background: linear-gradient(115deg, transparent 36%, color-mix(in srgb, var(--c-card) 75%, var(--c-glow)) 50%, transparent 64%) 160% 0 / 250% 100% no-repeat, var(--c-card);
  outline: 1px solid var(--c-accent); outline-offset: -10px;
  box-shadow: inset 0 0 0 14px var(--c-card), inset 0 0 0 15px color-mix(in srgb, var(--c-accent) 55%, transparent), 0 0 0 1px var(--c-line),
    0 32px 50px -28px color-mix(in srgb, var(--c-hero) 60%, transparent), 0 0 70px -26px color-mix(in srgb, var(--c-accent) 60%, transparent);
}
.has-sand-texture .db-card { background: linear-gradient(115deg, transparent 36%, color-mix(in srgb, var(--c-card) 75%, var(--c-glow)) 50%, transparent 64%) 160% 0 / 250% 100% no-repeat, var(--img-sand-texture) 0 0 / 300px, var(--c-card); }
.db-card::before { content: ""; position: absolute; inset-block-start: -15px; inset-inline-start: calc(50% - 15px); inline-size: 30px; block-size: 30px; display: none; background: var(--db-foil); }
.has-sparkle-art .db-card::before { display: block; -webkit-mask: var(--img-sparkle-art) center / contain no-repeat; mask: var(--img-sparkle-art) center / contain no-repeat; }
.db-card::after { content: ""; position: absolute; inset-block-end: -24px; inset-inline-end: -16px; inline-size: 84px; aspect-ratio: 1; display: none; pointer-events: none; background: color-mix(in srgb, var(--c-accent) 50%, var(--c-hero)); }
.has-flower-art .db-card::after { display: block; -webkit-mask: var(--img-flower-art) center / contain no-repeat; mask: var(--img-flower-art) center / contain no-repeat; }
.db[data-ornament="refined"] .db-card::after { display: none; }
.db-invite { margin-block-start: -60px; margin-inline: 18px; }
.db-portrait { inline-size: 120px; aspect-ratio: 3 / 4; margin-inline: auto; margin-block-end: 18px; padding: 4px; border-radius: 999px 999px 8px 8px; background: var(--db-foil); }
.db-portrait img { display: block; inline-size: 100%; block-size: 100%; object-fit: cover; border-radius: inherit; }

/* photo frames: arch · circle · dome */
.db-photo { padding: 4px; border-radius: 999px 999px 6px 6px; background: var(--db-foil); box-shadow: 0 18px 28px -16px color-mix(in srgb, var(--c-hero) 60%, transparent); }
.db[data-photo-frame="circle"] .db-photo { aspect-ratio: 1; border-radius: 50%; }
.db[data-photo-frame="dome"] .db-photo { border-radius: 50% 50% 6px 6px / 70% 70% 6px 6px; }
.db-flow__item img { border-radius: 999px 999px 6px 6px; border: 3px solid transparent; background: var(--db-foil) border-box; box-shadow: 0 24px 36px -20px color-mix(in srgb, var(--c-hero) 70%, transparent); }

/* ---------- motion: dunes move at different speeds ---------- */
@supports (animation-timeline: view()) {
  .db-dune--1 { animation: desert-bloom-far linear both; animation-timeline: view(); animation-range: exit 0% exit 100%; }
  .db-dune--2 { animation: desert-bloom-mid linear both; animation-timeline: view(); animation-range: exit 0% exit 100%; }
  .db-dune--3, .db-palm--start { animation: desert-bloom-near linear both; animation-timeline: view(); animation-range: exit 0% exit 100%; }
  .db-sun { animation: desert-bloom-set linear both; animation-timeline: view(); animation-range: exit 0% exit 100%; }
  .db-card { animation: desert-bloom-shine linear both; animation-timeline: view(); animation-range: entry 20% cover 60%; }
}
@keyframes desert-bloom-far { to { translate: 0 -40px; } }
@keyframes desert-bloom-mid { to { translate: 0 -90px; } }
@keyframes desert-bloom-near { to { translate: 0 -150px; } }
@keyframes desert-bloom-set { to { translate: 0 120px; scale: 1.15; } }
@keyframes desert-bloom-shine { from { background-position: 160% 0, 0 0, 0 0; } to { background-position: -60% 0, 0 0, 0 0; } }

/* own reveal: a mirage settling */
.fx-mirage { opacity: 0; transform: translateY(40px) scaleY(1.04); filter: blur(5px);
  transition: opacity var(--fx-dur, 1s) ease, transform var(--fx-dur, 1s) cubic-bezier(.2, .7, .2, 1), filter var(--fx-dur, 1s) ease; }
.fx-mirage.is-in { filter: none; }

/* own ambient: sand glints drifting on the wind */
.ambient-sand-glints { background-image:
    radial-gradient(1.6px 1.6px at 10% 40%, var(--c-accent), transparent), radial-gradient(1.2px 1.2px at 46% 70%, var(--c-card), transparent),
    radial-gradient(2px 2px at 72% 30%, var(--c-accent), transparent), radial-gradient(1.2px 1.2px at 90% 84%, var(--c-card), transparent);
  background-size: 320px 380px; opacity: 0.75; animation: sand-glints-drift 26s linear infinite; }
@keyframes sand-glints-drift { to { background-position: -320px 60px; } }
@media (prefers-reduced-motion: reduce) { .ambient-sand-glints { animation-duration: 120s; } }
""" + REDUCED.replace("@@", P)

desert_manifest = manifest(
    "desert-bloom", {"ar": "زهرة الصحراء", "en": "Desert Bloom"},
    {"ar": "صحراء عربية وقت الغروب: كثبان تتحرك بسرعات مختلفة مع التمرير، شمس متوهجة، نخيل وورد صحراوي، وكروت رملية بإطار ذهبي.",
     "en": "An Arabian desert at sunset: dunes that move at different speeds as you scroll, a glowing sun, date palms and desert roses, and sand cards framed in gold."},
    texts({"ar": "تحت سماء الصحراء، ندعوكم لحضور حفل زفاف", "en": "Under the desert sky, please join us for the wedding of"},
          {"ar": "باقي على الفرح", "en": "Until sunset"}, {"ar": "حكايتنا", "en": "Our story"},
          {"ar": "من صورنا", "en": "Moments"}, {"ar": "اسحبوا لمشاهدة كل الصور", "en": "Swipe through the moments"},
          {"ar": "المواعيد", "en": "The celebrations"}, {"ar": "اكتب دعوة للعروسين", "en": "Leave a wish under the stars"}),
    ["glow", "dune", "silhouette"], ["palmArt", "flowerArt", "sandTexture", "sparkleArt"],
    [("dunes", "كثبان على امتداد الشاشة", "Full-screen dunes"), ("arch", "الكثبان من نافذة مقوسة", "Dunes through a gilded arch")],
    [("arch", "قوس", "Arch"), ("circle", "دائرة", "Circle"), ("dome", "قبة", "Dome")],
    [pal("goldenHour", "الساعة الذهبية", "Golden hour", hero="#5A2A1C", onHero="#FFF4E4", accent="#D4A64F", bg="#E5A066", text="#3E2216", muted="#7C5A45", card="#FBF1E2", line="#EBD3B5", glow="#F8D9A0", dune="#D9925A", silhouette="#4A2418"),
     pal("desertNight", "ليل الصحراء", "Desert night", hero="#F3E2C2", onHero="#141A3A", accent="#D9B46A", bg="#141A3A", text="#F3E9D8", muted="#B5A99A", card="#1E2448", line="#363E6A", glow="#3B2F5C", dune="#6E5266", silhouette="#0B0F24"),
     pal("roseDune", "كثبان وردية", "Rose dune", hero="#5C2630", onHero="#FFF5F2", accent="#CFA066", bg="#E7A9A0", text="#43202A", muted="#84606A", card="#FCF1EE", line="#EED2CC", glow="#F7D6C4", dune="#D68B7E", silhouette="#4E1F28"),
     pal("oasis", "واحة", "Oasis", hero="#1F4A4C", onHero="#F8F3E8", accent="#C9A050", bg="#93C6C4", text="#173638", muted="#4E6567", card="#F8F3E8", line="#E3D8C2", glow="#F1D9A7", dune="#D9B07C", silhouette="#173A3B"),
     pal("ivorySand", "رمال عاجية", "Ivory sand", hero="#6B4A2B", onHero="#FFFBF3", accent="#C2A061", bg="#F1E6D2", text="#3A2A1A", muted="#7A6650", card="#FFFBF3", line="#E8DCC6", glow="#FBF3E4", dune="#E2C9A2", silhouette="#5B3E24")],
    {"display": "amiri", "body": "serifPair", "latin": "cormorant"},
    {"palmArt": "palm", "flowerArt": "desert-rose", "sandTexture": "sand-grain", "sparkleArt": "sparkle"},
    ("mirage", "سراب", "Mirage settle"), ("sand-glints", "بريق الرمال", "Drifting sand glints"), "curtain", (12, 54))

# ---------------------------------------------------------------- write
BUILDS = [
    ("porcelain", page("pc", porcelain_cover, footer_decor='<span class="pc-divider" aria-hidden="true"></span>'), porcelain_css, porcelain_manifest),
    ("glass-garden", page("gg", glass_cover, card_decor='<span class="gg-sprig gg-decor" aria-hidden="true"></span>', footer_decor='<span class="gg-divider" aria-hidden="true"></span>'), glass_css, glass_manifest),
    ("lace", page("lc", lace_cover, footer_decor='<span class="lc-divider" aria-hidden="true"></span>'), lace_css, lace_manifest),
    ("desert-bloom", page("db", desert_cover, footer_decor='<span class="db-divider" aria-hidden="true"></span>'), desert_css, desert_manifest),
]
for key, html, css, man in BUILDS:
    d = ROOT / key
    d.mkdir(parents=True, exist_ok=True)
    (d / "template.html").write_text(html, encoding="utf-8")
    (d / "style.css").write_text(css, encoding="utf-8")
    (d / "manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote", key)

# extra couple options (palettes, frames, galleries, dates, ornament) for every template
import subprocess, sys
subprocess.run([sys.executable, str(pathlib.Path(__file__).with_name("add-options.py"))], check=True)
