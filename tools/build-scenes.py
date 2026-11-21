"""Builds ten scene templates with the scene kit (tools/scenekit.py).

Each template is its own world with its own cover diorama, opening, countdown
emblem, photo veils, events path and traveller. Everything stays calm: the cover
planes drift on the GPU as the cover scrolls away, the rest reveals once.

  python3 tools/build-scenes.py      # writes templates/<key>/ and runs add-options
"""
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from scenekit import Scene, stars, palette, write, aspect, mix, SHADE, FOIL, GLOW, ROOT  # noqa: E402

A, H, D, L, C, B = "var(--c-accent)", "var(--c-hero)", "var(--c-deep)", "var(--c-leaf)", "var(--c-card)", "var(--c-bg)"


def night_sky(S, horizon=62, dy=260):
    S.lay("sky", f"inset: -40% 0 0; background: radial-gradient(80% 30% at 50% {horizon}%, {mix(A, 'transparent', 26)}, transparent 70%), "
                 f"linear-gradient({mix(D, C, 92)} 0%, {D} 42%, {mix(D, A, 72)} {horizon - 1}%, {D} {horizon + 1}%)", dy)


def crescent(S, name, box, dy, size=58):
    S.lay(name, f"{box}; inline-size: {size}px; block-size: {size}px; border-radius: 50%; rotate: -24deg; "
                f"box-shadow: inset {size // 4.5:.0f}px -{size // 10:.0f}px 0 0 {GLOW}, 0 0 60px 6px {mix(GLOW, 'transparent', 14)}", dy)


def full_moon(S, name, box, dy, size=70):
    S.lay(name, f"{box}; inline-size: {size}px; block-size: {size}px; border-radius: 50%; "
                f"background: radial-gradient(circle at 38% 36%, {GLOW}, {mix(GLOW, A, 84)} 66%, {mix(A, GLOW, 55)}); "
                f"box-shadow: 0 0 40px 12px {mix(GLOW, 'transparent', 30)}, 0 0 140px 60px {mix(A, 'transparent', 14)}", dy)


def sparks(S, spots):
    for i, _ in enumerate(spots, 1):
        S.raw(f'<span class="@@-spark @@-spark--{i} @@-decor" aria-hidden="true"></span>')
    return "\n".join(f".@@-spark--{i} {{ {pos} }}" for i, pos in enumerate(spots, 1))


def T(ar, en):
    return (ar, en)


CONFIGS = []

# =================================================================== Desert Bloom
S = Scene()
night_sky(S, 60)
S.lay("stars", f"inset: 0 0 48%; background-image: {stars(11, 26, GLOW, A)}", 240)
crescent(S, "moon", "inset-block-start: 9%; inset-inline-end: 16%", 220)
S.lay("dune-far", f"inset-block: 56% -10%; inset-inline: -30% -10%; border-radius: 60% 40% 0 0 / 20% 14% 0 0; background: linear-gradient({mix(A, D, 34)}, {D} 40%)", 170)
S.art("caravan", "caravanArt", "caravan", "inset-block-start: 50.4%; inset-inline-end: 2%; inline-size: 46%", SHADE, dy=170, dx=46)
S.lay("glow", f"inset-block-start: 46%; inset-inline-start: -6%; inline-size: 74%; aspect-ratio: 1.5; background: radial-gradient(closest-side, {mix(A, 'transparent', 38)}, transparent)", 120)
S.lay("dune-mid", f"inset-block: 61% -10%; inset-inline: -10% -40%; border-radius: 45% 55% 0 0 / 18% 26% 0 0; background: linear-gradient({mix(A, D, 50)}, {mix(D, A, 84)} 50%)", 120)
S.art("tent", "tentArt", "tent", "inset-block-start: 47.5%; inset-inline-start: 3%; inline-size: 52%", f"linear-gradient({mix(A, D, 62)}, {mix(A, D, 36)})", dy=120)
S.art("tent-door", "tentDoorArt", "tent-door", "inset-block-start: 47.5%; inset-inline-start: 3%; inline-size: 52%", f"radial-gradient(closest-side at 50% 85%, {GLOW}, {A})", dy=120)
S.lay("dune-near", f"inset-block: 71% -12%; inset-inline: -40% -20%; border-radius: 55% 45% 0 0 / 22% 14% 0 0; background: linear-gradient({mix(A, D, 66)}, {mix(A, D, 32)} 60%)", 70)
S.art("palm", "palmArt", "palm", "inset-block-end: 17%; inset-inline-end: -9%; inline-size: 36%", SHADE, dy=50)
cart_i = len(S.html)
S.art("bloom-start", "bloomArt", "desert-rose", "inset-block-end: -5%; inset-inline-start: -12%; inline-size: 42%", mix(A, H, 72), dy=-60, decor=True)
S.art("bloom-end", "bloomArt", "desert-rose", "inset-block-end: -9%; inset-inline-end: -12%; inline-size: 30%", mix(A, C, 60), dy=-40, decor=True)
sp = sparks(S, ["inset-block-start: 20%; inset-inline-start: 16%;", "inset-block-start: 13%; inset-inline-start: 62%; inline-size: 11px; block-size: 11px;", "inset-block-start: 38%; inset-inline-end: 9%; inline-size: 19px; block-size: 19px;"])
CONFIGS.append(dict(
    key="desert-bloom", P="db", intro="tent", cart_index=cart_i, cart_mode="night", veil="swing",
    name={"ar": "زهرة الصحراء", "en": "Desert Bloom"},
    description={"ar": "ليلة في الصحراء بعمق حقيقي: كثبان وقافلة تسير على الأفق وخيمة مضيئة ونخلة وزهور، تُفتح بستارة الخيمة، مع ساعة رملية للعد وقافلة ترافقكم بين المناسبات.",
                 "en": "A desert night with real depth: dunes, a caravan walking the ridge, a glowing tent, a palm and desert roses. Opens with tent flaps, counts down in an hourglass, and a caravan walks you through the events."},
    scene_note="the desert at night: sky, stars, moon, three dune ridges, a caravan, a lit tent, a palm and roses drift at their own speeds",
    emblem_note="an hourglass whose sand starts to fall when it arrives",
    veil_note="each photo waits behind striped tent flaps that open once",
    path_note="a trail of footprints in the sand; the caravan walks along with you",
    css_note="a desert night with a caravan, a glowing tent and an hourglass.",
    veil_name=T("خيمة تنفتح", "Tent flaps"),
    fonts={"display": "arefRuqaa", "body": "plexArabic", "latin": "italiana"},
    images={"patternTile": "sand-grain", "monogramArt": "rosette", "sparkleArt": "sparkle", "travellerArt": "caravan", "footerArt": "tent",
            "frameArt": "star-divider", "dividerArt": "star-divider", "cornerArt": "desert-rose"},
    texts={"countdownTitle": T("الرمل يعدّ الأيام", "The sand counts the days"), "storyTitle": T("حكايتنا", "Our story"),
           "galleryTitle": T("لحظات تحت النجوم", "Moments under the stars"), "eventsTitle": T("رحلة القافلة", "The caravan's journey"),
           "wishesTitle": T("دعوة حول النار", "A wish by the fire")},
    palettes=[palette("desertNight", "ليل الصحراء", "Desert night", "#6B3A1E", "#FFF6E8", "#D9A85B", "#F6EBDD", "#3A2414", "#1E1A33", "#8A7A4E"),
              palette("saffron", "زعفران", "Saffron", "#7A4512", "#FFF7E8", "#E0A63E", "#F8EBD2", "#3D2410", "#2A1A2E", "#9A8450"),
              palette("roseSand", "رمل وردي", "Rose sand", "#7E3F4A", "#FFF7F4", "#D3A07E", "#F7ECE6", "#3E2329", "#2B1E33", "#A39078"),
              palette("oasisTeal", "واحة فيروزية", "Oasis teal", "#1F5755", "#F6FBF8", "#D2AE6D", "#EFEDE3", "#173A39", "#10283A", "#6E8E78"),
              palette("duneDark", "كثبان الليل", "Midnight dunes", "#F0DDBE", "#1A1626", "#D9A85B", "#1A1626", "#F3E9DA", "#110E1C", "#8A7A4E", dark=True)],
    css=sp + f"""
.@@ {{ --@@-cart-top: 9%; --@@-photo-r: 50% 50% 8px 8px / 26% 26% 8px 8px; --@@-trav: {aspect('caravan')}; --@@-fa: {aspect('tent')}; --@@-corner: {mix(A, H, 70)}; }}
.@@-cartouche {{ border-radius: 50% 50% 22px 22px / 34% 34% 22px 22px; outline: 1px solid {mix(A, 'transparent', 80)}; outline-offset: -3px;
  box-shadow: inset 0 0 0 7px transparent, inset 0 0 0 8px {mix(A, 'transparent', 35)}; }}
/* hourglass */
.@@-emblem {{ inline-size: 150px; block-size: 230px; margin-block-end: 76px; }}
.@@-emblem__a {{ inset: 0; border-radius: 4px;
  background: linear-gradient(90deg, var(--@@-gd), var(--@@-gl), var(--@@-gd)) 0 0 / 100% 14px no-repeat, linear-gradient(90deg, var(--@@-gd), var(--@@-gl), var(--@@-gd)) 0 100% / 100% 14px no-repeat,
    linear-gradient({A}, {A}) 8px 0 / 5px 100% no-repeat, linear-gradient({A}, {A}) calc(100% - 8px) 0 / 5px 100% no-repeat; }}
.@@-emblem__b {{ inset-block: 14px; inset-inline: 22px; clip-path: polygon(0 0, 100% 0, 100% 6%, 57% 47%, 57% 53%, 100% 94%, 100% 100%, 0 100%, 0 94%, 43% 53%, 43% 47%, 0 6%);
  background: linear-gradient(transparent 0 24%, {mix(A, H, 78)} 24% 46%, transparent 46% 72%, {mix(A, H, 78)} 72%), linear-gradient(90deg, {mix(C, 'transparent', 45)}, {mix(C, 'transparent', 15)} 40%, {mix(C, 'transparent', 40)}); }}
.@@-emblem__c {{ inset-block: 48% 12%; inset-inline: calc(50% - 1px); inline-size: 2px; background: {mix(A, H, 78)}; transform-origin: 50% 0; }}
.@@-countdown.fx:not(.is-in) .@@-emblem__c {{ transform: scaleY(0); }}
.@@-count {{ position: absolute; inset-block-start: calc(100% + 14px); padding-block: 6px; padding-inline: 24px; border-block: 1px solid {A}; }}
/* tent flaps over the photos */
.@@-veil {{ background: repeating-linear-gradient(100deg, {H} 0 14px, {mix(H, A, 80)} 14px 28px); box-shadow: inset 0 0 0 3px {mix(A, 'transparent', 70)}; }}
/* footprints in the sand */
.@@-path {{ background: radial-gradient(circle, {mix(A, 'transparent', 75)} 2.5px, transparent 3.5px) 8px 0 / 14px 24px repeat-y,
  radial-gradient(circle, {mix(A, 'transparent', 75)} 2.5px, transparent 3.5px) 16px 12px / 14px 24px repeat-y, linear-gradient(90deg, transparent, {mix(A, 'transparent', 14)}, transparent); }}
.@@-traveller, .@@-traveller:dir(rtl) {{ inline-size: 120px; margin-inline-start: -45px; rotate: 90deg; }}
.@@-panel__decor {{ background-image: {stars(5, 16, GLOW, A)}, radial-gradient(60% 30% at 50% 108%, {mix(A, 'transparent', 45)}, transparent); }}
""",
))
CONFIGS[-1]["scene"] = S

# =================================================================== Royal Crest
S = Scene()
S.lay("wall", f"inset: -40% 0 0; background: linear-gradient({mix(D, A, 84)}, {D} 60%)", 250,
      inner="")
S.art("windows", "windowArt", "ballroom-window", "inset-block-start: 11%; inset-inline: 3%; block-size: 46%", f"linear-gradient({GLOW}, {mix(GLOW, A, 55)})",
      dy=210, pos="center top", size="auto 100%", rep="space no-repeat", ar=False)
S.lay("beams", f"inset-block: 30% 0; inset-inline: 0; background: linear-gradient(160deg, transparent 22%, {mix(GLOW, 'transparent', 13)} 32%, transparent 46%), linear-gradient(200deg, transparent 22%, {mix(GLOW, 'transparent', 13)} 32%, transparent 46%)", 180)
S.art("chandelier-s", "chandelierArt", "chandelier", "inset-block-start: -1%; inset-inline-start: 4%; inline-size: 22%", FOIL, dy=200, decor=True)
S.art("chandelier-e", "chandelierArt", "chandelier", "inset-block-start: -1%; inset-inline-end: 4%; inline-size: 22%", FOIL, dy=200, decor=True)
S.lay("floor", "inset-block: 66% -20%; inset-inline: -30%; perspective: 320px", 110, inner='<span class="@@-floor__tiles"></span>')
S.art("column-s", "columnArt", "classic-column", "inset-block-end: 24%; inset-inline-start: 2%; block-size: 60%",
      f"linear-gradient(90deg, {mix(D, A, 70)}, {mix(GLOW, A, 70)} 45%, {mix(D, A, 60)})", dy=100)
S.art("column-e", "columnArt", "classic-column", "inset-block-end: 24%; inset-inline-end: 2%; block-size: 60%",
      f"linear-gradient(90deg, {mix(D, A, 60)}, {mix(GLOW, A, 70)} 55%, {mix(D, A, 70)})", dy=100)
S.art("chandelier", "chandelierArt", "chandelier", "inset-block-start: -7%; inset-inline: 0; margin-inline: auto; inline-size: 50%", FOIL, dy=130)
cart_i = len(S.html)
S.lay("drape-s", f"inset-block: -2% 0; inset-inline-start: -5%; inline-size: 26%; background: repeating-linear-gradient(90deg, {L} 0 8px, {mix(L, D, 66)} 16px, {L} 26px); clip-path: polygon(0 0, 100% 0, 62% 38%, 34% 58%, 46% 100%, 0 100%)", 30)
S.lay("drape-e", f"inset-block: -2% 0; inset-inline-end: -5%; inline-size: 26%; rotate: y 180deg; background: repeating-linear-gradient(90deg, {L} 0 8px, {mix(L, D, 66)} 16px, {L} 26px); clip-path: polygon(0 0, 100% 0, 62% 38%, 34% 58%, 46% 100%, 0 100%)", 30)
S.lay("valance", f"inset-block-start: -2%; inset-inline: -4%; block-size: 10%; background: radial-gradient(circle at 50% 0, {L} 63%, transparent 64%) 0 100% / 56px 38px repeat-x, linear-gradient({A}, {A}) 0 calc(100% - 38px) / 100% 3px no-repeat, linear-gradient({L}, {L}) 0 0 / 100% calc(100% - 38px) no-repeat", 20)
sp = sparks(S, ["inset-block-start: 30%; inset-inline-start: 22%;", "inset-block-start: 24%; inset-inline-end: 20%; inline-size: 12px; block-size: 12px;", "inset-block-start: 52%; inset-inline-end: 14%; inline-size: 18px; block-size: 18px;"])
CONFIGS.append(dict(
    key="royal", P="ry", intro="velvet", cart_index=cart_i, cart_mode="night", veil="slide",
    name={"ar": "التاج الملكي", "en": "Royal Crest"},
    description={"ar": "قاعة رقص ملكية بعمق: نوافذ يضيئها القمر وثريات وأعمدة وأرضية رخامية وستائر مخملية، تُفتح بستارة مخملية، مع ساعة مذهبة للعد وسجادة حمراء بين المناسبات.",
                 "en": "A royal ballroom in depth: moonlit windows, chandeliers, columns, a marble floor and velvet drapes. Opens with velvet curtains, counts down on a gilded clock, and a red carpet leads through the events."},
    scene_note="the ballroom: damask wall, moonlit windows, light beams, chandeliers, marble floor, columns and velvet drapes drift at their own speeds",
    emblem_note="a gilded clock whose hand settles when it arrives",
    veil_note="each photo waits behind velvet curtains that part once",
    path_note="a red carpet with gold edges; the royal crest walks along with you",
    css_note="a moonlit ballroom with chandeliers, velvet drapes and a gilded clock.",
    veil_name=T("ستارة مخملية", "Velvet curtains"),
    fonts={"display": "amiri", "body": "plexArabic", "latin": "cinzel"},
    images={"patternTile": "damask-tile", "monogramArt": "royal-crest", "sparkleArt": "sparkle", "travellerArt": "royal-crest", "footerArt": "chandelier",
            "frameArt": "gold-flourish", "dividerArt": "gold-flourish", "cornerArt": "filigree-corner"},
    texts={"countdownTitle": T("تدق الساعة لليلتنا", "The clock counts to our night"), "storyTitle": T("حكايتنا", "Our story"),
           "galleryTitle": T("من القاعة", "From the ballroom"), "eventsTitle": T("برنامج الليلة الملكية", "The royal evening"),
           "wishesTitle": T("اكتبوا تهنئتكم", "Leave your wishes")},
    palettes=[palette("burgundyGold", "عنابي وذهبي", "Burgundy & gold", "#5A1A2A", "#FBF3E8", "#CFAB63", "#F6EEE4", "#2E1A20", "#1D1424", "#6E1A2C"),
              palette("royalPurple", "بنفسجي ملكي", "Royal purple", "#3B1E5A", "#F7F1FB", "#CFAB63", "#F4EFF6", "#2A1A33", "#1A1028", "#4A2368"),
              palette("emeraldCrown", "تاج زمردي", "Emerald crown", "#164A3A", "#F4FAF6", "#CBAA63", "#F0F0E8", "#183329", "#0F2A24", "#1C5A44"),
              palette("navyIvory", "كحلي وعاجي", "Navy & ivory", "#1E2B4E", "#F6F4EE", "#C9AA6C", "#F2F0EA", "#1C2440", "#121A30", "#28366A"),
              palette("onyxRoyal", "أسود ملكي", "Onyx royal", "#EADCB8", "#121214", "#CFAB63", "#141416", "#F1E8D6", "#0B0B0D", "#4E1424", dark=True)],
    css=sp + f"""
.@@ {{ --@@-cart-top: 26%; --@@-photo-r: 999px 999px 6px 6px; --@@-trav: {aspect('royal-crest')}; --@@-fa: {aspect('chandelier')}; }}
.has-pattern-tile .@@-wall::after {{ content: ""; position: absolute; inset: 0; background: {mix(A, 'transparent', 16)}; -webkit-mask: var(--img-pattern-tile) 0 0 / 84px; mask: var(--img-pattern-tile) 0 0 / 84px; }}
.@@-floor__tiles {{ position: absolute; inset: 0; transform: rotateX(58deg); transform-origin: 50% 0;
  background: linear-gradient({mix(D, 'transparent', 10)}, {mix(GLOW, 'transparent', 20)} 40%, transparent), conic-gradient({mix(C, D, 26)} 25%, {mix(A, D, 32)} 0 50%, {mix(C, D, 26)} 0 75%, {mix(A, D, 32)} 0) 0 0 / 70px 70px; }}
.@@-cartouche {{ border-radius: 46% 46% 18px 18px / 30% 30% 18px 18px; outline: 1px solid {mix(A, 'transparent', 70)}; outline-offset: -3px; }}
.@@-cartouche .@@-monogram {{ inline-size: 50px; block-size: 54px; }}
/* gilded clock */
.@@-emblem {{ inline-size: 220px; aspect-ratio: 1; margin-block: 6px 20px; }}
.@@-emblem__a {{ inset: 0; border-radius: 50%; background: radial-gradient(closest-side, {C} 82%, transparent 83%), {FOIL};
  box-shadow: 0 0 0 4px {C}, 0 0 0 5px {mix(A, 'transparent', 60)}, 0 24px 40px -20px {mix(D, 'transparent', 50)}; }}
.@@-emblem__b {{ inset: 22px; border-radius: 50%; background: repeating-conic-gradient({A} 0 1.4deg, transparent 1.4deg 30deg);
  -webkit-mask: radial-gradient(closest-side, transparent 84%, var(--c-text) 85%); mask: radial-gradient(closest-side, transparent 84%, var(--c-text) 85%); }}
.@@-emblem__c {{ inset-block: 16% 50%; inset-inline: calc(50% - 1.5px); inline-size: 3px; border-radius: 2px; background: {H}; transform-origin: 50% 100%; transform: rotate(-60deg); }}
.@@-countdown.fx:not(.is-in) .@@-emblem__c {{ transform: rotate(0deg); }}
.@@-emblem::before {{ content: ""; position: absolute; inset-block: 28% 50%; inset-inline: calc(50% - 2.5px); inline-size: 5px; border-radius: 3px; background: {H}; transform-origin: 50% 100%; rotate: 60deg; }}
.@@-emblem::after {{ content: ""; position: absolute; inset-block-start: calc(50% - 7px); inset-inline-start: calc(50% - 7px); inline-size: 14px; block-size: 14px; border-radius: 50%; background: {FOIL}; }}
.@@-count {{ position: absolute; inset-block-start: 55%; }}
.@@-count__num {{ font-size: 34px; }}
/* velvet curtains over the photos */
.@@-veil {{ background: repeating-linear-gradient(90deg, {L} 0 6px, {mix(L, D, 66)} 12px, {L} 20px); box-shadow: inset 0 -30px 30px {mix(D, 'transparent', 40)}; }}
/* the red carpet */
.@@-path {{ inline-size: 26px; border-radius: 2px; background: linear-gradient(90deg, {A} 0 3px, {L} 3px calc(100% - 3px), {A} calc(100% - 3px)); }}
.@@-traveller {{ inline-size: 52px; margin-inline-start: -13px; }}
.@@-event::before {{ background: radial-gradient(circle at 40% 35%, {mix(L, C, 60)}, {L} 60%); box-shadow: 0 0 0 3px {mix(L, 'transparent', 40)}; }}
.@@-panel {{ background: radial-gradient(80% 40% at 50% 0, {mix(A, 'transparent', 22)}, transparent 70%), linear-gradient({mix(L, D, 80)}, {mix(L, D, 50)}); }}
.has-pattern-tile .@@-panel__decor {{ background: {A}; opacity: 0.1; -webkit-mask: var(--img-pattern-tile) 0 0 / 70px; mask: var(--img-pattern-tile) 0 0 / 70px; }}
""",
))
CONFIGS[-1]["scene"] = S

# =================================================================== Glass Garden
S = Scene()
S.lay("sky", f"inset: -40% 0 0; background: radial-gradient(60% 30% at 70% 52%, {mix(GLOW, 'transparent', 80)}, transparent 70%), linear-gradient({mix(B, L, 70)}, {B} 60%)", 250)
S.art("trees", "treesArt", "tree-line", "inset-block-start: 40%; inset-inline: -10%", mix(L, B, 45), dy=200)
S.lay("panes", f"inset-block: 8% 26%; inset-inline: 0; margin-inline: auto; inline-size: 86%; border-radius: 50% 50% 0 0 / 24% 24% 0 0; "
      f"background: linear-gradient(115deg, {mix(C, 'transparent', 45)}, {mix(C, 'transparent', 12)} 46%, {mix(C, 'transparent', 38)} 60%, {mix(C, 'transparent', 10)})", 150)
S.art("house", "houseArt", "glasshouse", "inset-block-start: 6%; inset-inline: 0; margin-inline: auto; inline-size: 92%", FOIL, dy=150)
S.lay("floor", "inset-block: 72% -20%; inset-inline: -20%; perspective: 300px", 100, inner='<span class="@@-floor__tiles"></span>')
S.art("ivy-s", "ivyArt", "ivy", "inset-block-start: -6%; inset-inline-start: 1%; block-size: 48%", L, dy=90, pos="center top")
S.art("ivy-e", "ivyArt", "ivy", "inset-block-start: -10%; inset-inline-end: 1%; block-size: 40%", mix(L, D, 80), dy=110, pos="center top", extra="rotate: y 180deg;")
S.art("fern-s", "fernArt", "fern", "inset-block-end: 25%; inset-inline-start: -4%; inline-size: 40%", L, dy=60)
S.art("fern-e", "fernArt", "fern", "inset-block-end: 25%; inset-inline-end: -4%; inline-size: 40%", mix(L, D, 85), dy=60, extra="rotate: y 180deg;")
S.art("urn-s", "urnArt", "urn", "inset-block-end: 11%; inset-inline-start: 4%; inline-size: 27%", FOIL, dy=60)
S.art("urn-e", "urnArt", "urn", "inset-block-end: 11%; inset-inline-end: 4%; inline-size: 27%", FOIL, dy=60)
cart_i = len(S.html)
S.art("fly-1", "butterflyArt", "butterfly", "inset-block-start: 30%; inset-inline-start: 12%; inline-size: 34px", A, dy=40, dx=90, extra="rotate: -16deg;", decor=True)
S.art("fly-2", "butterflyArt", "butterfly", "inset-block-start: 60%; inset-inline-end: 20%; inline-size: 26px", mix(A, H, 70), dy=-30, dx=-60, extra="rotate: 20deg;", decor=True)
S.art("fly-3", "butterflyArt", "butterfly", "inset-block-start: 15%; inset-inline-end: 24%; inline-size: 22px", A, dy=80, dx=40, decor=True)
S.art("fern-near", "fernArt", "fern", "inset-block-end: -12%; inset-inline-start: -18%; inline-size: 54%", mix(L, D, 70), dy=-60, decor=True)
CONFIGS.append(dict(
    key="glass-garden", P="gg", intro="glass", cart_index=cart_i, cart_mode="day", veil="swing",
    name={"ar": "حديقة زجاجية", "en": "Glass Garden"},
    description={"ar": "بيت زجاجي في ضوء النهار بعمق: أشجار بعيدة وألواح زجاج وأوراق متدلية وسرخس وجرار ذهبية وفراشات، يُفتح بباب زجاجي، مع مزولة شمسية للعد وفراشة ترافقكم في ممر الحديقة.",
                 "en": "A glasshouse in daylight with depth: far trees, glass panes, hanging ivy, ferns, gold urns and butterflies. Opens through glass doors, counts down on a sundial, and a butterfly follows you down the garden path."},
    scene_note="the conservatory: sky, far trees, glass panes, iron frame, floor, ivy, ferns, urns and butterflies drift at their own speeds",
    emblem_note="a sundial whose shadow moves into place when it arrives",
    veil_note="each photo waits behind glass doors that open once",
    path_note="stepping stones through the garden; a butterfly flies along with you",
    css_note="a daylight conservatory with ferns, urns, butterflies and a sundial.",
    veil_name=T("أبواب زجاجية", "Glass doors"),
    fonts={"display": "elMessiri", "body": "plexArabic", "latin": "cormorant"},
    images={"patternTile": "fern", "monogramArt": "rosette", "sparkleArt": "sparkle", "travellerArt": "butterfly", "footerArt": "glasshouse",
            "frameArt": "ornament", "dividerArt": "ornament", "cornerArt": "fern"},
    texts={"countdownTitle": T("الظل يقترب من يومنا", "The shadow nears our day"), "storyTitle": T("حكايتنا", "Our story"),
           "galleryTitle": T("من الحديقة", "From the garden"), "eventsTitle": T("ممر الحديقة", "Down the garden path"),
           "wishesTitle": T("ازرعوا دعوة", "Plant a wish")},
    palettes=[palette("sageIvory", "مريمية وعاجي", "Sage & ivory", "#2F4A3A", "#F6FAF6", "#B9975B", "#EEF1E8", "#22332A", "#2E4638", "#6F8F62"),
              palette("lavenderMist", "ضباب لافندر", "Lavender mist", "#5B4A86", "#FBF9FF", "#B9A06E", "#F1EEF7", "#2B2442", "#3E3460", "#8C9A6E"),
              palette("terracotta", "تيراكوتا", "Terracotta", "#8C4A32", "#FFF7F1", "#C49A5E", "#F6ECE4", "#3A2117", "#4A2E22", "#7F8F5E"),
              palette("blushGreen", "وردي وأخضر", "Blush & green", "#7A4855", "#FFF8F8", "#C2A06E", "#F7EEEE", "#3A2228", "#3E3A30", "#7E9A72"),
              palette("nightHouse", "بيت زجاجي ليلي", "Night glasshouse", "#E6E2C8", "#14201A", "#C9AD6E", "#14201A", "#ECEAD8", "#0C150F", "#5E7E58", dark=True)],
    css=f"""
.@@ {{ --@@-cart-top: 23%; --@@-photo-r: 999px 999px 10px 10px; --@@-trav: {aspect('butterfly')}; --@@-fa: {aspect('glasshouse')}; --@@-corner: {L}; --@@-cue: {H}; }}
.@@-floor__tiles {{ position: absolute; inset: 0; transform: rotateX(60deg); transform-origin: 50% 0;
  background: linear-gradient({mix(B, 'transparent', 30)}, transparent 50%), conic-gradient({mix(C, L, 70)} 25%, {mix(L, C, 45)} 0 50%, {mix(C, L, 70)} 0 75%, {mix(L, C, 45)} 0) 0 0 / 64px 64px; }}
.@@-cartouche {{ background: {mix(C, 'transparent', 78)}; border-radius: 140px 140px var(--radius) var(--radius); outline: 1px solid {A}; outline-offset: -8px;
  box-shadow: 0 24px 40px -26px {mix(D, 'transparent', 45)}; }}
/* sundial */
.@@-emblem {{ inline-size: 230px; aspect-ratio: 1; margin-block-end: 16px; }}
.@@-emblem__a {{ inset: 0; border-radius: 50%; background: {C}; box-shadow: inset 0 0 0 7px {mix(A, C, 45)}, inset 0 0 0 9px {A}, 0 0 0 3px {mix(A, 'transparent', 60)}, 0 20px 30px -18px {mix(D, 'transparent', 45)}; }}
.@@-emblem__b {{ inset: 18px; border-radius: 50%; background: repeating-conic-gradient(from 270deg, {A} 0 1deg, transparent 1deg 15deg);
  -webkit-mask: radial-gradient(closest-side, transparent 62%, var(--c-text) 63% 90%, transparent 91%), linear-gradient(var(--c-text) 50%, transparent 50%); -webkit-mask-composite: source-in;
  mask: radial-gradient(closest-side, transparent 62%, var(--c-text) 63% 90%, transparent 91%) intersect, linear-gradient(var(--c-text) 50%, transparent 50%); }}
.@@-emblem__c {{ inset-block: 16% 50%; inset-inline: calc(50% - 3px); inline-size: 6px; border-radius: 3px 3px 0 0; background: {FOIL}; }}
.@@-emblem::before {{ content: ""; position: absolute; inset-block: 14% 50%; inset-inline: calc(50% - 3px); inline-size: 6px; border-radius: 3px;
  background: linear-gradient(transparent, {mix(D, 'transparent', 40)}); transform-origin: 50% 100%; rotate: -48deg; transition: rotate 2s cubic-bezier(.3, .7, .2, 1) .4s; }}
.@@-countdown.fx:not(.is-in) .@@-emblem::before {{ rotate: -84deg; }}
.@@-count {{ position: absolute; inset-block-start: 56%; }}
.@@-count__num {{ font-size: 36px; }}
/* glass doors over the photos */
.@@-veil {{ background: linear-gradient({A}, {A}) 50% 0 / 2px 100% no-repeat, linear-gradient({A}, {A}) 0 42% / 100% 2px no-repeat,
  linear-gradient(115deg, {mix(C, 'transparent', 80)}, {mix(C, 'transparent', 45)} 60%, {mix(C, 'transparent', 70)}); box-shadow: inset 0 0 0 3px {A}; }}
/* stepping stones */
.@@-path {{ background: radial-gradient(ellipse 11px 7px at 50% 50%, {mix(L, C, 45)} 90%, transparent) 0 0 / 30px 44px repeat-y,
  linear-gradient(90deg, transparent, {mix(L, 'transparent', 18)}, transparent); }}
.@@-traveller {{ inline-size: 46px; margin-inline-start: -8px; }}
.@@-panel__decor {{ background: linear-gradient(90deg, transparent calc(50% - 1px), {mix(A, 'transparent', 24)} 0 calc(50% + 1px), transparent 0),
  linear-gradient(transparent calc(40% - 1px), {mix(A, 'transparent', 24)} 0 calc(40% + 1px), transparent 0); }}
""",
    panel_light=True,
))
CONFIGS[-1]["scene"] = S

# =================================================================== Lace
S = Scene()
S.lay("wall", f"inset: -40% 0 0; background: radial-gradient(70% 40% at 50% 46%, {C}, transparent 70%), linear-gradient({mix(B, H, 86)}, {B} 70%)", 240)
S.lay("mirror", f"inset-block-start: 8%; inset-inline: 0; margin-inline: auto; inline-size: 66%; block-size: 62%; border-radius: 999px 999px 12px 12px; border: 6px solid {A}; "
      f"background: linear-gradient(135deg, {mix(C, L, 78)}, {mix(C, 'transparent', 92)} 40%, {mix(L, C, 32)} 62%, {C}); "
      f"box-shadow: 0 0 0 2px var(--@@-gd), 0 0 0 10px {mix(C, 'transparent', 70)}, 0 0 0 11px {mix(A, 'transparent', 60)}, 0 30px 50px -30px {mix(D, 'transparent', 50)}", 170)
S.art("curtain-s", "laceArt", "lace-tile", "inset-block: -2% 10%; inset-inline-start: -4%; inline-size: 32%", mix(C, "transparent", 88), dy=110,
      pos="0 0", size="58px", rep="repeat", ar=False, extra="clip-path: polygon(0 0, 100% 0, 72% 50%, 42% 100%, 0 100%);")
S.art("curtain-e", "laceArt", "lace-tile", "inset-block: -2% 10%; inset-inline-end: -4%; inline-size: 32%", mix(C, "transparent", 88), dy=110,
      pos="0 0", size="58px", rep="repeat", ar=False, extra="clip-path: polygon(0 0, 100% 0, 100% 100%, 58% 100%, 28% 50%);")
S.art("pearls", "pearlsArt", "pearls", "inset-block-start: 0; inset-inline: -6%", f"linear-gradient({C}, {mix(C, A, 72)})", dy=80)
S.art("pearls-2", "pearlsArt", "pearls", "inset-block-start: 5%; inset-inline: 14%", f"linear-gradient({C}, {mix(C, A, 72)})", dy=60, decor=True)
S.lay("table", f"inset-block: 79% -20%; inset-inline: -10%; border-radius: 50% 50% 0 0 / 26% 26% 0 0; background: linear-gradient({mix(L, C, 46)}, {mix(L, D, 70)})", 50)
S.art("doily", "doilyArt", "lace-doily", "inset-block-start: 70%; inset-inline-start: -5%; inline-size: 110%", C, dy=40, pos="center", extra="rotate: x 70deg;")
S.art("bouquet", "bouquetArt", "bouquet", "inset-block-end: 13%; inset-inline-end: 3%; inline-size: 34%", f"linear-gradient({mix(L, C, 60)}, {H})", dy=30)
cart_i = len(S.html)
S.art("edge", "edgeArt", "lace-edge", "inset-block-end: -1%; inset-inline: -2%; block-size: 46px", C, dy=-40, size="auto 100%", rep="repeat-x", ar=False, extra="rotate: x 180deg;")
sp = sparks(S, ["inset-block-start: 26%; inset-inline-start: 20%;", "inset-block-start: 18%; inset-inline-end: 24%; inline-size: 12px; block-size: 12px;", "inset-block-start: 56%; inset-inline-start: 14%; inline-size: 18px; block-size: 18px;"])
CONFIGS.append(dict(
    key="lace", P="lc", intro="veil", cart_index=cart_i, cart_mode="day", veil="lift",
    name={"ar": "دانتيل", "en": "Lace"},
    description={"ar": "بوتيك عرائس بعمق: ستائر دانتيل وعقود لؤلؤ ومرآة مذهبة وطاولة بمفرش دانتيل وباقة ورد، يُفتح برفع الطرحة، مع علبة خاتم للعد وشريط ساتان بين المناسبات.",
                 "en": "A bridal boutique in depth: lace curtains, pearl strands, a gilded mirror, a lace-covered table and a bouquet. Opens as the veil lifts, counts down in a ring box, and a satin ribbon leads through the events."},
    scene_note="the bridal boutique: wall, gilded mirror, lace curtains, pearl strands, table, doily, bouquet and lace edge drift at their own speeds",
    emblem_note="a ring box whose lid opens when it arrives",
    veil_note="each photo waits under a tulle veil that lifts once",
    path_note="a satin ribbon; a bouquet travels along with you",
    css_note="a bridal boutique with lace, pearls, a gilded mirror and a ring box.",
    veil_name=T("طرحة ترتفع", "Lifting veil"),
    fonts={"display": "arefRuqaa", "body": "plexArabic", "latin": "pinyon"},
    images={"patternTile": "lace-tile", "monogramArt": "rosette", "sparkleArt": "sparkle", "travellerArt": "bouquet", "footerArt": "pearls",
            "frameArt": "lace-edge", "dividerArt": "pearls", "cornerArt": "filigree-corner"},
    texts={"countdownTitle": T("الخاتم بانتظار يومنا", "The ring awaits our day"), "storyTitle": T("حكايتنا", "Our story"),
           "galleryTitle": T("لحظات بيضاء", "White moments"), "eventsTitle": T("على شريط الساتان", "Along the satin ribbon"),
           "wishesTitle": T("اكتبوا أمنية للعروسين", "Write a wish for the couple")},
    palettes=[palette("blushPearl", "وردي لؤلؤي", "Blush pearl", "#6E4B5A", "#FFF9FA", "#C7A27C", "#F7F0EE", "#3A2A30", "#5A4450", "#B9A3A8"),
              palette("ivoryChampagne", "عاجي وشمبانيا", "Ivory & champagne", "#6A5434", "#FFFBF2", "#C9AA74", "#F7F2E8", "#3A2E1E", "#5C4B33", "#C4B49A"),
              palette("lilacLace", "دانتيل ليلكي", "Lilac lace", "#5E4C7E", "#FBF9FD", "#BFA6C8", "#F1ECF4", "#2E2540", "#4A3D63", "#B5A6C8"),
              palette("sageLace", "دانتيل مريمي", "Sage lace", "#4A5E50", "#F7FAF7", "#BFA67C", "#EFF1EC", "#263329", "#3E4E42", "#A9B8A8"),
              palette("blackLace", "دانتيل أسود", "Black lace", "#EADFC8", "#121212", "#D4B26B", "#141414", "#F2EBDD", "#0A0A0A", "#5E554A", dark=True)],
    css=sp + f"""
.@@ {{ --@@-cart-top: 21%; --@@-photo-r: 999px 999px 999px 999px / 60% 60% 40% 40%; --@@-trav: {aspect('bouquet')}; --@@-fa: {aspect('pearls')}; --@@-cue: {H}; }}
.has-pattern-tile .@@-wall::after {{ content: ""; position: absolute; inset: 0; background: {mix(H, 'transparent', 7)}; -webkit-mask: var(--img-pattern-tile) 0 0 / 70px; mask: var(--img-pattern-tile) 0 0 / 70px; }}
.@@-cartouche {{ background: none; }}
/* ring box */
.@@-emblem {{ inline-size: 200px; block-size: 220px; perspective: 600px; }}
.@@-emblem__a {{ inset-block: 46% 0; inset-inline: 8%; border-radius: 10px 10px 18px 18px; background: linear-gradient({mix(H, C, 90)}, {H} 40%, {mix(H, D, 70)});
  box-shadow: inset 0 3px 0 {A}, inset 0 -6px 12px {mix(D, 'transparent', 40)}, 0 20px 30px -16px {mix(D, 'transparent', 55)}; }}
.@@-emblem__b {{ inset-block: 2% 55%; inset-inline: 8%; border-radius: 50% 50% 10px 10px / 70% 70% 10px 10px; transform-origin: 50% 100%;
  background: radial-gradient(70% 60% at 50% 70%, {mix(C, L, 70)}, {mix(L, H, 60)}); box-shadow: inset 0 0 0 6px {H}, inset 0 0 0 7px {A}; }}
.@@-countdown.fx:not(.is-in) .@@-emblem__b {{ transform: rotateX(-88deg); }}
.@@-emblem__c {{ inset-block-start: 31%; inset-inline-start: calc(50% - 24px); inline-size: 48px; aspect-ratio: 1; border-radius: 50%; border: 6px solid {A};
  box-shadow: inset 0 0 0 1px var(--@@-gd), 0 2px 0 var(--@@-gl); }}
.@@-emblem__c::before {{ content: ""; position: absolute; inset-block-start: -20px; inset-inline-start: calc(50% - 9px); inline-size: 18px; block-size: 18px; rotate: 45deg;
  background: linear-gradient(135deg, {C}, {mix(L, C, 40)} 50%, {C}); box-shadow: 0 0 14px 4px {mix(C, 'transparent', 60)}; }}
.@@-count {{ position: absolute; inset-block-start: 58%; }}
.@@-count__num {{ font-size: 40px; background: {FOIL} 0 0 / 220% 100%; -webkit-background-clip: text; background-clip: text; }}
.@@-count__unit {{ color: var(--c-on-hero); }}
/* the tulle veil */
.@@-veil {{ background: {mix(C, 'transparent', 74)}; }}
.has-lace-art .@@-veil::before {{ content: ""; position: absolute; inset: 0; background: {C}; -webkit-mask: var(--img-lace-art) 0 0 / 48px; mask: var(--img-lace-art) 0 0 / 48px; }}
/* the satin ribbon */
.@@-path {{ inline-size: 14px; inset-inline-start: 18px; border-radius: 0;
  background: radial-gradient(circle, {C} 0 3px, {mix(A, 'transparent', 60)} 4px, transparent 5px) 50% 0 / 14px 36px repeat-y, linear-gradient(90deg, {mix(L, C, 70)}, {C} 45%, {mix(L, C, 60)}); }}
.@@-traveller {{ inline-size: 44px; margin-inline-start: -15px; }}
.has-edge-art .@@-panel__decor::before, .has-edge-art .@@-panel__decor::after {{ content: ""; position: absolute; inset-inline: 0; block-size: 26px; background: {mix(L, C, 60)};
  -webkit-mask: var(--img-edge-art) 0 0 / auto 100% repeat-x; mask: var(--img-edge-art) 0 0 / auto 100% repeat-x; }}
.@@-panel__decor::before {{ inset-block-start: 0; }}
.@@-panel__decor::after {{ inset-block-end: 0; rotate: x 180deg; }}
.@@-panel {{ padding-block: 64px 54px; }}
""",
    panel_light=True,
))
CONFIGS[-1]["scene"] = S

# =================================================================== Porcelain
S = Scene()
S.lay("sky", f"inset: -40% 0 0; background: radial-gradient(50% 24% at 30% 60%, {mix(C, 'transparent', 90)}, transparent), linear-gradient({B}, {mix(B, H, 88)} 70%)", 250)
S.lay("sun", f"inset-block-start: 15%; inset-inline-start: 16%; inline-size: 64px; aspect-ratio: 1; border-radius: 50%; background: {mix(A, C, 50)}", 230)
S.art("mountains", "mountainsArt", "ink-mountains", "inset-block-start: 29%; inset-inline: -10%", mix(H, B, 22), dy=200)
S.art("birds", "birdsArt", "birds", "inset-block-start: 22%; inset-inline-end: 10%; inline-size: 32%", mix(H, B, 70), dy=170, dx=-70)
S.lay("mist", f"inset-block-start: 43%; inset-inline: -20%; block-size: 12%; background: linear-gradient(transparent, {mix(B, 'transparent', 88)}, transparent)", 160)
S.art("mountains-near", "mountainsArt", "ink-mountains", "inset-block-start: 39%; inset-inline: -30% -10%", mix(H, B, 45), dy=140, extra="rotate: y 180deg;")
S.lay("cliff", f"inset-block: 52% 0; inset-inline-start: -12%; inline-size: 48%; border-start-end-radius: 70% 40%; background: linear-gradient({mix(H, B, 55)}, {mix(H, B, 22)})", 110)
S.art("pavilion", "pavilionArt", "pavilion", "inset-block-start: 41.5%; inset-inline-start: 0; inline-size: 32%", H, dy=110)
S.lay("water", f"inset-block: 64% -20%; inset-inline: -20%; background: repeating-linear-gradient(transparent 0 9px, {mix(H, 'transparent', 14)} 9px 10px), linear-gradient({mix(B, H, 90)}, {mix(B, H, 76)})", 90)
S.art("bridge", "bridgeArt", "ink-bridge", "inset-block-start: 57%; inset-inline-end: -6%; inline-size: 68%", H, dy=80)
S.art("willow", "willowArt", "willow", "inset-block-start: -4%; inset-inline-end: -18%; inline-size: 62%", mix(H, D, 80), dy=40, pos="center top")
cart_i = len(S.html)
S.art("corner-s", "cornerArt", "porcelain-corner", "inset-block-end: 2%; inset-inline-start: 2%; inline-size: 24%", H, dy=-40, extra="rotate: x 180deg;", decor=True)
S.art("corner-e", "cornerArt", "porcelain-corner", "inset-block-end: 2%; inset-inline-end: 2%; inline-size: 24%", H, dy=-40, extra="rotate: 180deg;", decor=True)
CONFIGS.append(dict(
    key="porcelain", P="pc", intro="fold", cart_index=cart_i, cart_mode="day", veil="swing",
    name={"ar": "بورسلين", "en": "Porcelain"},
    description={"ar": "منظر بالحبر الأزرق كأنه مرسوم على البورسلين: جبال وضباب وطيور وجناح على الجرف وجسر وصفصاف، يُفتح بستارة قابلة للطي، مع فنجان شاي للعد وحجارة عبور فوق الماء.",
                 "en": "A blue-ink landscape as if painted on porcelain: mountains, mist, birds, a pavilion on a cliff, a bridge and a willow. Opens with a folding screen, counts down in a teacup, and stepping stones cross the water."},
    scene_note="the ink landscape: paper sky, sun, two mountain ranges, birds, mist, cliff with a pavilion, water, bridge and willow drift at their own speeds",
    emblem_note="a porcelain teacup on its saucer",
    veil_note="each photo waits behind painted screen panels that fold open once",
    path_note="stepping stones across the water; birds fly along with you",
    css_note="a blue-ink landscape with a pavilion, a bridge, a willow and a teacup.",
    veil_name=T("ستارة قابلة للطي", "Folding screen"),
    fonts={"display": "amiri", "body": "plexArabic", "latin": "playfair"},
    images={"patternTile": "porcelain-tile", "monogramArt": "porcelain-plate", "sparkleArt": "sparkle", "travellerArt": "birds", "footerArt": "pavilion",
            "frameArt": "ornament", "dividerArt": "ornament"},
    texts={"countdownTitle": T("فنجان ينتظر يومنا", "A cup poured for our day"), "storyTitle": T("حكايتنا", "Our story"),
           "galleryTitle": T("لوحات من أيامنا", "Painted moments"), "eventsTitle": T("على حجارة العبور", "Across the stepping stones"),
           "wishesTitle": T("اكتبوا دعوة", "Leave a wish")},
    palettes=[palette("cobalt", "أزرق كوبالت", "Cobalt", "#1F3F7A", "#F7F9FC", "#C9A55C", "#F6F3EC", "#1C2A44", "#23407A", "#7F95BF"),
              palette("celadon", "سيلادون", "Celadon", "#2F5E57", "#F5FBF9", "#C2A469", "#F1F3EC", "#1F3532", "#2C5550", "#8DB0A6"),
              palette("roseFamille", "وردي عائلي", "Famille rose", "#8A3D55", "#FFF8FA", "#C9A55C", "#F8F1EF", "#3C2029", "#7A3550", "#C99AA8"),
              palette("indigoGold", "نيلي وذهبي", "Indigo & gold", "#2B2F6B", "#F7F7FC", "#CBA85E", "#F3F2F6", "#1E2148", "#262B63", "#8C90C4"),
              palette("inkNight", "حبر الليل", "Ink night", "#DCE4F2", "#121A2E", "#C9A55C", "#121A2E", "#E6EBF4", "#0A1020", "#3E5280", dark=True)],
    css=f"""
.@@ {{ --@@-cart-top: 9%; --@@-photo-r: 50%; --@@-trav: {aspect('birds')}; --@@-fa: {aspect('pavilion')}; --@@-corner: {H}; --@@-cue: {H}; }}
.@@-cartouche {{ inline-size: min(264px, 72%); gap: 4px; padding-block: 26px 30px; border-radius: 50% / 30%;
  background: radial-gradient(closest-side, {C} 84%, {mix(C, H, 90)} 85% 92%, {C} 93%);
  box-shadow: 0 0 0 3px {H}, 0 0 0 6px {C}, 0 0 0 7px {A}, 0 30px 40px -24px {mix(D, 'transparent', 45)}; }}
.@@-cartouche .@@-monogram {{ background: {H}; }}
/* teacup */
.@@-emblem {{ inline-size: 240px; block-size: 200px; margin-block-end: 12px; }}
.@@-emblem__b {{ inset-block-end: 0; inset-inline: 2%; block-size: 36px; border-radius: 50%; background: radial-gradient(closest-side, {C} 52%, {mix(C, H, 84)} 53% 68%, {C} 69%); box-shadow: inset 0 0 0 2px {H}, 0 10px 18px -8px {mix(D, 'transparent', 45)}; }}
.@@-emblem__a {{ inset-block: 6% 12%; inset-inline: 14% 24%; border-radius: 8px 8px 50% 50% / 8px 8px 72% 72%;
  background: linear-gradient(transparent 11%, {H} 11% 15%, transparent 15% 19%, {mix(H, 'transparent', 60)} 19% 20%, transparent 20%), {C}; box-shadow: inset 0 0 0 3px {H}, inset 0 -14px 20px {mix(H, 'transparent', 88)}; }}
.@@-emblem__c {{ inset-block-start: 22%; inset-inline-end: 10%; inline-size: 42px; block-size: 58px; border: 7px solid {H}; border-radius: 50%; border-inline-start-color: transparent; }}
.@@-emblem::before {{ content: ""; position: absolute; inset-block-start: -36px; inset-inline-start: calc(45% - 30px); inline-size: 60px; block-size: 44px;
  background: radial-gradient(14px 22px at 20% 60%, transparent 60%, {mix(H, 'transparent', 30)} 64%, transparent 70%), radial-gradient(14px 22px at 60% 40%, transparent 60%, {mix(H, 'transparent', 30)} 64%, transparent 70%);
  transition: transform 2s ease .6s, opacity 2s ease .6s; }}
.@@-countdown.fx:not(.is-in) .@@-emblem::before {{ transform: translateY(14px); opacity: 0; }}
.@@-count {{ margin-inline-end: 10%; margin-block-start: -16px; }}
.@@-count__unit {{ color: {H}; }}
/* painted screen panels over the photos */
.@@-veil {{ background: linear-gradient({mix(B, H, 90)}, {C}); box-shadow: inset 0 0 0 4px {H}, inset 0 0 0 6px {C}, inset 0 0 0 7px {A}; }}
.has-pattern-tile .@@-veil::before {{ content: ""; position: absolute; inset: 12px; background: {H}; opacity: 0.35; -webkit-mask: var(--img-pattern-tile) 0 0 / 40px; mask: var(--img-pattern-tile) 0 0 / 40px; }}
/* stepping stones across the water */
.@@-path {{ background: radial-gradient(ellipse 11px 7px at 50% 50%, {mix(H, B, 55)} 90%, transparent) 0 0 / 30px 40px repeat-y, linear-gradient(90deg, transparent, {mix(H, 'transparent', 16)} 30% 70%, transparent); }}
.@@-traveller {{ inline-size: 70px; margin-inline-start: -20px; }}
.has-pattern-tile .@@-panel__decor::before, .has-pattern-tile .@@-panel__decor::after {{ content: ""; position: absolute; inset-inline: 0; block-size: 22px; background: {H};
  -webkit-mask: var(--img-pattern-tile) 0 0 / 22px repeat-x; mask: var(--img-pattern-tile) 0 0 / 22px repeat-x; }}
.@@-panel__decor::before {{ inset-block-start: 0; }}
.@@-panel__decor::after {{ inset-block-end: 0; }}
.@@-panel {{ padding-block: 64px 54px; }}
""",
    panel_light=True,
))
CONFIGS[-1]["scene"] = S


# 8-point star polygon for Andalus
def octagram(r1=50, r2=38):
    import math
    pts = []
    for i in range(16):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * 2 * i / 16 - math.pi / 2
        pts.append(f"{50 + r * math.cos(a):.1f}% {50 + r * math.sin(a):.1f}%")
    return f"polygon({', '.join(pts)})"


# =================================================================== Andalus
S = Scene()
night_sky(S, 58)
S.lay("stars", f"inset: 0 0 50%; background-image: {stars(23, 24, GLOW, A)}", 240)
crescent(S, "moon", "inset-block-start: 7%; inset-inline-start: 45%", 220, 50)
S.art("cypress", "cypressArt", "cypress", "inset-block-start: 42%; inset-inline: 0; block-size: 24%", SHADE, dy=190, size="auto 100%", rep="space no-repeat", ar=False)
S.lay("arch-glow", f"inset-block: 54% 22%; inset-inline: 0; background: radial-gradient(60% 50% at 50% 60%, {mix(A, 'transparent', 45)}, transparent)", 150)
S.art("arcade", "arcadeArt", "arcade", "inset-block-start: 49%; inset-inline: -14%", f"linear-gradient({mix(C, A, 70)}, {mix(C, D, 42)})", dy=150)
S.lay("pool", f"inset-block: 79% -20%; inset-inline: -20%; background: linear-gradient({mix(C, D, 28)}, {D} 40%); box-shadow: inset 0 5px 0 {mix(C, A, 55)}", 100)
S.art("reflection", "arcadeArt", "arcade", "inset-block-start: 80%; inset-inline: -14%", f"linear-gradient({mix(C, D, 30)}, transparent 70%)", dy=100, pos="center top", extra="rotate: x 180deg;")
S.art("fountain", "fountainArt", "fountain", "inset-block-start: 72%; inset-inline: 0; margin-inline: auto; inline-size: 40%", FOIL, dy=90)
S.art("lantern-s", "lanternArt", "lantern", "inset-block-start: -3%; inset-inline-start: 5%; inline-size: 15%", FOIL, dy=70, pos="center top")
S.art("lantern-e", "lanternArt", "lantern", "inset-block-start: -8%; inset-inline-end: 8%; inline-size: 11%", FOIL, dy=110, pos="center top", decor=True)
cart_i = len(S.html)
S.lay("tiles", f"inset-block: 89% -10%; inset-inline: -10%; background: linear-gradient({mix(D, A, 80)}, {D})", 30)
S.art("geo-s", "geoArt", "geo-corner", "inset-block-end: 1%; inset-inline-start: 1%; inline-size: 22%", FOIL, dy=-30, extra="rotate: x 180deg;", decor=True)
S.art("geo-e", "geoArt", "geo-corner", "inset-block-end: 1%; inset-inline-end: 1%; inline-size: 22%", FOIL, dy=-30, extra="rotate: 180deg;", decor=True)
CONFIGS.append(dict(
    key="andalus", P="an", intro="screen", cart_index=cart_i, cart_mode="night", veil="slide",
    name={"ar": "الأندلس", "en": "Andalus"},
    description={"ar": "فناء أندلسي ليلي بعمق: سرو وأروقة مقوسة مضيئة وبركة تعكسها ونافورة وفوانيس، يُفتح بمشربيتين تنزلقان، مع نجمة زليج للعد وقناة ماء بين المناسبات.",
                 "en": "An Andalusian courtyard at night with depth: cypresses, lit arcades, a reflecting pool, a fountain and lanterns. Opens as two mashrabiya screens slide apart, counts down in a zellige star, and a water channel leads through the events."},
    scene_note="the courtyard: sky, stars, moon, cypresses, lit arcade, reflecting pool, fountain, lanterns and tiles drift at their own speeds",
    emblem_note="an eight-pointed zellige star that turns into place when it arrives",
    veil_note="each photo waits behind mashrabiya screens that slide apart once",
    path_note="a water channel like the Alhambra's; a lantern travels along with you",
    css_note="an Andalusian courtyard with arcades, a reflecting pool and a zellige star.",
    veil_name=T("مشربية تنزلق", "Sliding mashrabiya"),
    fonts={"display": "reemKufi", "body": "plexArabic", "latin": "marcellus"},
    images={"patternTile": "zellige-tile", "screenArt": "mashrabiya", "monogramArt": "rosette", "travellerArt": "lantern", "footerArt": "fountain",
            "frameArt": "star-divider", "dividerArt": "star-divider", "cornerArt": "geo-corner"},
    texts={"countdownTitle": T("تقترب ليلة الفناء", "Our night in the courtyard draws near"), "storyTitle": T("حكايتنا", "Our story"),
           "galleryTitle": T("من الأروقة", "From the arcades"), "eventsTitle": T("على قناة الماء", "Along the water channel"),
           "wishesTitle": T("اكتبوا دعوة طيبة", "Leave a kind wish")},
    palettes=[palette("tealGold", "فيروزي وذهبي", "Teal & gold", "#1E4B5F", "#F5FAFA", "#C9A55C", "#F3EEE3", "#1F2F38", "#172437", "#4F6B4E"),
              palette("amethyst", "جمشت وذهبي", "Amethyst & gold", "#4A2A5E", "#F8F3FA", "#C9A55C", "#F4EFF2", "#2E1A3B", "#21142E", "#5E6B4E"),
              palette("terracottaCourt", "فناء تيراكوتا", "Terracotta court", "#8A4632", "#FFF7F2", "#CDA864", "#F5ECE2", "#3A2117", "#2A1C22", "#6B7A4E"),
              palette("emeraldCourt", "فناء زمردي", "Emerald court", "#1F5A44", "#F4FAF6", "#C9A55C", "#EFF0E6", "#1A3328", "#122A26", "#4E7A52"),
              palette("nightCourt", "فناء الليل", "Night courtyard", "#EDE0C2", "#101826", "#C9A55C", "#101826", "#EFE7D6", "#0A101C", "#3E5A44", dark=True)],
    css=f"""
.@@ {{ --@@-cart-top: 9%; --@@-photo-r: 50% 50% 6px 6px / 34% 34% 6px 6px; --@@-trav: {aspect('lantern')}; --@@-fa: {aspect('fountain')}; }}
.has-pattern-tile .@@-tiles::after {{ content: ""; position: absolute; inset: 0; background: {A}; opacity: 0.45; -webkit-mask: var(--img-pattern-tile) 0 0 / 44px; mask: var(--img-pattern-tile) 0 0 / 44px; }}
.@@-cartouche {{ border-radius: 50% 50% 20px 20px / 38% 38% 20px 20px; outline: 1px solid {A}; outline-offset: -4px; box-shadow: inset 0 0 0 9px transparent, inset 0 0 0 10px {mix(A, 'transparent', 40)}; }}
/* zellige star */
.@@-emblem {{ inline-size: 220px; aspect-ratio: 1; margin-block: 10px 24px; }}
.@@-emblem__a, .@@-emblem__b {{ inset: 15%; background: {FOIL}; box-shadow: 0 16px 30px -18px {mix(D, 'transparent', 40)}; }}
.@@-emblem__b {{ transform: rotate(45deg); }}
.@@-countdown.fx:not(.is-in) .@@-emblem__a {{ transform: rotate(-45deg); }}
.@@-countdown.fx:not(.is-in) .@@-emblem__b {{ transform: rotate(90deg); }}
.@@-emblem__c {{ inset: 21%; clip-path: {octagram()}; background: {D}; }}
.has-pattern-tile .@@-emblem__c::before {{ content: ""; position: absolute; inset: 0; background: {A}; opacity: 0.3; -webkit-mask: var(--img-pattern-tile) center / 40px; mask: var(--img-pattern-tile) center / 40px; }}
.@@-count__num {{ background: {FOIL} 0 0 / 220% 100%; -webkit-background-clip: text; background-clip: text; font-size: 44px; }}
.@@-count__unit {{ color: {GLOW}; }}
/* mashrabiya screens over the photos */
.@@-veil {{ background: {D}; box-shadow: inset 0 0 0 3px {A}; }}
.has-screen-art .@@-veil::before {{ content: ""; position: absolute; inset: 8px; background: {A}; opacity: 0.7; -webkit-mask: var(--img-screen-art) center / cover; mask: var(--img-screen-art) center / cover; }}
/* water channel */
.@@-path {{ inline-size: 22px; inset-inline-start: 14px; border-radius: 3px;
  background: repeating-linear-gradient(transparent 0 9px, {mix(GLOW, 'transparent', 30)} 9px 10px), linear-gradient({mix(D, A, 72)}, {D}); box-shadow: 0 0 0 3px {mix(C, A, 60)}; }}
.@@-traveller {{ inline-size: 30px; margin-inline-start: -4px; }}
.has-pattern-tile .@@-panel__decor {{ background: {A}; opacity: 0.12; -webkit-mask: var(--img-pattern-tile) 0 0 / 70px; mask: var(--img-pattern-tile) 0 0 / 70px; }}
""",
))
CONFIGS[-1]["scene"] = S

# =================================================================== Gatsby Deco
S = Scene()
night_sky(S, 64)
S.lay("beams", f"inset: -10% -30% 30%; background: conic-gradient(from 155deg at 30% 100%, transparent 0deg, {mix(GLOW, 'transparent', 15)} 6deg, transparent 12deg), "
      f"conic-gradient(from 192deg at 72% 100%, transparent 0deg, {mix(GLOW, 'transparent', 13)} 5deg, transparent 10deg)", 230)
S.lay("stars", f"inset: 0 0 50%; background-image: {stars(41, 16, GLOW, A)}", 240)
S.art("fireworks", "fireworksArt", "fireworks", "inset-block-start: 3%; inset-inline: -6%", FOIL, dy=220, decor=True)
S.art("skyline", "skylineArt", "deco-skyline", "inset-block-start: 36%; inset-inline: -20% -4%", mix(D, A, 72), dy=170)
S.art("skyline-near", "skylineArt", "deco-skyline", "inset-block-start: 45%; inset-inline: -40% -30%", SHADE, dy=120, extra="rotate: y 180deg;")
S.lay("terrace", f"inset-block: 74% -20%; inset-inline: -10%; background: linear-gradient({mix(D, A, 78)}, {D})", 80)
S.lay("rail", f"inset-block-start: 66%; inset-inline: -4%; block-size: 9%; background: linear-gradient({A}, {A}) 0 0 / 100% 5px no-repeat, linear-gradient({A}, {A}) 0 100% / 100% 4px no-repeat, "
      f"repeating-linear-gradient(90deg, transparent 0 10px, {mix(A, D, 80)} 10px 14px, transparent 14px 24px)", 80)
S.art("fan", "fanArt", "deco-fan", "inset-block-start: 9%; inset-inline: 0; margin-inline: auto; inline-size: 88%", FOIL, dy=90, extra="opacity: 0.55;")
S.art("champagne", "champagneArt", "champagne", "inset-block-end: 5%; inset-inline-end: -10%; inline-size: 60%", FOIL, dy=40)
cart_i = len(S.html)
S.art("corner-s", "cornerArt", "deco-corner", "inset-block-start: 2%; inset-inline-start: 2%; inline-size: 20%", FOIL, dy=-20, decor=True)
S.art("corner-e", "cornerArt", "deco-corner", "inset-block-start: 2%; inset-inline-end: 2%; inline-size: 20%", FOIL, dy=-20, extra="rotate: y 180deg;", decor=True)
CONFIGS.append(dict(
    key="deco", P="dc", intro="fan", cart_index=cart_i, cart_mode="night", veil="slide",
    name={"ar": "غاتسبي ديكو", "en": "Gatsby Deco"},
    description={"ar": "سطح ناطحة سحاب في ليلة احتفال بعمق: أضواء كاشفة وألعاب نارية ومدينة ديكو وسور ذهبي وبرج شمبانيا، يُفتح بمروحة ديكو، مع لوحة أضواء للعد ومؤشر مصعد يتنقل بين فقرات الليلة.",
                 "en": "A skyscraper rooftop on a party night with depth: searchlights, fireworks, a deco skyline, a gold balustrade and a champagne tower. Opens with a deco fan, counts down on a marquee sign, and an elevator dial travels through the evening."},
    scene_note="the rooftop: sky, searchlights, stars, fireworks, two skylines, terrace, balustrade, deco fan and champagne tower drift at their own speeds",
    emblem_note="a marquee sign whose bulbs light up when it arrives",
    veil_note="each photo waits behind gilded elevator doors that slide open once",
    path_note="an elevator shaft marked floor by floor; the dial indicator travels with you",
    css_note="a rooftop party with searchlights, a deco skyline and a marquee countdown.",
    veil_name=T("أبواب مصعد مذهبة", "Gilded elevator doors"),
    fonts={"display": "elMessiri", "body": "plexArabic", "latin": "poiret"},
    images={"patternTile": "deco-tile", "monogramArt": "deco-fan", "travellerArt": "deco-fan", "footerArt": "champagne",
            "frameArt": "gold-flourish", "dividerArt": "gold-flourish"},
    texts={"countdownTitle": T("الأضواء تعدّ لليلتنا", "The lights count to our night"), "storyTitle": T("حكايتنا", "Our story"),
           "galleryTitle": T("من الحفل", "From the party"), "eventsTitle": T("طوابق الليلة", "Floor by floor"),
           "wishesTitle": T("ارفعوا نخب العروسين", "Raise a toast")},
    palettes=[palette("navyGold", "كحلي وذهبي", "Navy & gold", "#142238", "#F4EBD6", "#CDAA62", "#F2EEE4", "#182336", "#0B1324", "#2E6B5E"),
              palette("emeraldDeco", "زمردي ديكو", "Emerald deco", "#0F3A30", "#F2F8F4", "#CDAA62", "#EFEFE6", "#14302A", "#08201B", "#2E5A6B"),
              palette("rubyDeco", "ياقوت ديكو", "Ruby deco", "#5A1420", "#FBF2EA", "#CFA862", "#F5EDE6", "#2E1418", "#1E0B10", "#2E4A5E"),
              palette("champagneDeco", "شمبانيا", "Champagne", "#3A3226", "#FBF7EE", "#C8AB72", "#F5F1E8", "#2A241C", "#1A1712", "#5E6B5E"),
              palette("onyxDeco", "أسود ديكو", "Onyx deco", "#EADCB8", "#0E0E10", "#CDAA62", "#0E0E10", "#EFE6D2", "#060608", "#2E5A4E", dark=True)],
    css=f"""
.@@ {{ --@@-cart-top: 19%; --@@-photo-r: 6px; --@@-trav: {aspect('deco-fan')}; --@@-fa: {aspect('champagne')}; --@@-cue: {GLOW}; }}
.@@-cartouche {{ border-radius: 0; background: {mix(D, 'transparent', 70)}; outline: 1px solid {A}; outline-offset: 5px; box-shadow: inset 0 0 0 1px {A}, inset 0 0 0 5px transparent, inset 0 0 0 6px {mix(A, 'transparent', 45)}; }}
.@@-cartouche::before, .@@-cartouche::after {{ content: ""; position: absolute; inset-inline: 30%; block-size: 9px; background: {FOIL}; clip-path: polygon(0 50%, 12% 0, 88% 0, 100% 50%, 88% 100%, 12% 100%); }}
.@@-cartouche::before {{ inset-block-start: -12px; }}
.@@-cartouche::after {{ inset-block-end: -12px; }}
/* marquee sign */
.@@-emblem {{ inline-size: 250px; block-size: 170px; margin-block: 6px 16px; }}
.@@-emblem__a {{ inset: 0; border-radius: 12px; background: {D}; box-shadow: inset 0 0 0 3px {A}, 0 20px 30px -16px {mix(D, 'transparent', 40)}; }}
.@@-emblem__b {{ inset: 8px; padding: 14px; border-radius: 6px; background: radial-gradient(circle, {GLOW} 0 2.6px, {mix(A, 'transparent', 55)} 3.4px, transparent 6.5px) 0 0 / 18px 18px;
  -webkit-mask: linear-gradient(var(--c-text) 0 0) content-box, linear-gradient(var(--c-text) 0 0); -webkit-mask-composite: xor;
  mask: linear-gradient(var(--c-text) 0 0) content-box exclude, linear-gradient(var(--c-text) 0 0); }}
.@@-countdown.fx:not(.is-in) .@@-emblem__b {{ opacity: 0.15; }}
.@@-emblem__c {{ inset: 32px; border: 1px solid {mix(A, 'transparent', 60)}; }}
.@@-count__num {{ background: {FOIL} 0 0 / 220% 100%; -webkit-background-clip: text; background-clip: text; }}
.@@-count__unit {{ color: {GLOW}; letter-spacing: 0.2em; }}
/* elevator doors over the photos */
.@@-veil {{ background: repeating-linear-gradient(135deg, transparent 0 10px, {mix(D, 'transparent', 70)} 10px 12px), linear-gradient(90deg, var(--@@-gd), var(--@@-gl) 50%, var(--@@-gd)); box-shadow: inset 0 0 0 3px {D}; }}
/* elevator shaft */
.@@-path {{ inline-size: 24px; inset-inline-start: 13px; border-radius: 3px; background: repeating-linear-gradient(transparent 0 38px, {A} 38px 40px), {D}; box-shadow: inset 0 0 0 2px {A}; }}
.@@-traveller {{ inline-size: 54px; margin-inline-start: -15px; rotate: 180deg; }}
.@@-traveller:dir(rtl) {{ rotate: 180deg; }}
.@@-panel__decor {{ background: repeating-conic-gradient(from -90deg at 50% 100%, {mix(A, 'transparent', 13)} 0 2deg, transparent 2deg 10deg); }}
""",
))
CONFIGS[-1]["scene"] = S

# =================================================================== Atelier
S = Scene()
S.lay("wall", f"inset: -40% 0 0; background: radial-gradient(60% 40% at 50% 46%, {C}, transparent 70%), linear-gradient({mix(B, D, 84)}, {B} 60%)", 240)
S.lay("spots", f"inset: -10% 0 22%; background: conic-gradient(from 166deg at 22% 0, transparent, {mix(C, 'transparent', 75)} 7deg, transparent 16deg), conic-gradient(from 176deg at 82% 0, transparent, {mix(C, 'transparent', 65)} 8deg, transparent 18deg)", 200)
S.art("rack", "rackArt", "garment-rack", "inset-block-start: 31%; inset-inline-start: -8%; inline-size: 62%", mix(D, B, 26), dy=170)
S.lay("sweep", f"inset-block: 63% -20%; inset-inline: -10%; border-radius: 50% 50% 0 0 / 10% 10% 0 0; background: linear-gradient({mix(C, B, 90)}, {mix(B, D, 82)})", 120)
S.art("form", "formArt", "dress-form", "inset-block-start: 40%; inset-inline-end: 2%; block-size: 56%",
      f"linear-gradient(90deg, {mix(L, D, 78)}, {L} 40%, {mix(L, D, 70)})", dy=100)
S.lay("fabric", f"inset-block: 52% -6%; inset-inline-start: -10%; inline-size: 44%; background: repeating-linear-gradient(80deg, {mix(H, L, 30)} 0 10px, {mix(H, L, 12)} 18px, {mix(H, L, 30)} 28px); clip-path: polygon(0 12%, 64% 0, 100% 100%, 0 100%)", 60)
cart_i = len(S.html)
S.lay("tape", f"inset-block-end: 6%; inset-inline: -10%; block-size: 34px; rotate: -7deg; background: repeating-linear-gradient(90deg, {H} 0 1px, transparent 1px 8px) 0 0 / 100% 40% no-repeat, "
      f"repeating-linear-gradient(90deg, {H} 0 1.5px, transparent 1.5px 40px) 0 0 / 100% 70% no-repeat, {mix(A, C, 70)}; box-shadow: 0 10px 14px -8px {mix(D, 'transparent', 45)}", -40, decor=True)
sp = sparks(S, ["inset-block-start: 30%; inset-inline-start: 34%;", "inset-block-start: 40%; inset-inline-end: 34%; inline-size: 12px; block-size: 12px;", "inset-block-start: 60%; inset-inline-start: 50%; inline-size: 16px; block-size: 16px;"])
CONFIGS.append(dict(
    key="atelier", P="at", intro="page", cart_index=cart_i, cart_mode="day", veil="page",
    name={"ar": "أتيليه", "en": "Atelier"},
    description={"ar": "استوديو أزياء راقٍ بعمق: أضواء كاشفة وراف ملابس ومانيكان وقماش منسدل وشريط قياس، يُفتح كغلاف مجلة يُقلب، مع بطاقة أزياء للعد وشريط فيلم للصور.",
                 "en": "A couture studio with depth: spotlights, a garment rack, a dress form, draped fabric and a tape measure. Opens as a magazine cover turns, counts down on a clothing tag, and the gallery runs like a film strip."},
    scene_note="the studio: wall, spotlights, garment rack, paper sweep, dress form, fabric and tape measure drift at their own speeds",
    emblem_note="a clothing tag that swings once when it arrives",
    veil_note="each photo waits under a page of tissue paper that turns once",
    path_note="a tape measure; the dress form travels along with you",
    css_note="a couture studio with a dress form, spotlights and a clothing tag.",
    veil_name=T("ورق حرير يُقلب", "Turning tissue page"),
    fonts={"display": "reemKufi", "body": "plexArabic", "latin": "bodoni"},
    images={"monogramArt": "rosette", "sparkleArt": "sparkle", "travellerArt": "dress-form", "footerArt": "garment-rack", "dividerArt": "ornament"},
    texts={"countdownTitle": T("العدّ قبل العرض", "Countdown to the show"), "storyTitle": T("حكايتنا", "Our story"),
           "galleryTitle": T("لقطات", "Frames"), "eventsTitle": T("جدول العرض", "The running order"),
           "wishesTitle": T("اكتبوا كلمة للعروسين", "Write a note for the couple")},
    palettes=[palette("inkNude", "حبر ونود", "Ink & nude", "#1E1E22", "#F8F5F0", "#B8946A", "#F3EFEA", "#1E1E22", "#3A3436", "#C9B8A8"),
              palette("blushAtelier", "وردي هادئ", "Blush", "#3A2A2E", "#FBF4F2", "#C29A84", "#F5ECE8", "#2E2124", "#4A383C", "#D9B8B0"),
              palette("navyAtelier", "كحلي", "Navy", "#14213D", "#F4F1EA", "#B89B5E", "#EEF0F4", "#121B30", "#2A3450", "#B8C0CF"),
              palette("oliveAtelier", "زيتوني", "Olive", "#2F3426", "#F6F6EF", "#B59A62", "#F0EFE6", "#262A1F", "#3E4432", "#BDB79A"),
              palette("noirAtelier", "نوار", "Noir", "#EDE6DA", "#141414", "#C2A274", "#141414", "#EFE9DE", "#0C0C0C", "#5A524C", dark=True)],
    css=sp + f"""
.@@ {{ --@@-cart-top: 8%; --@@-photo-r: 2px; --@@-trav: {aspect('dress-form')}; --@@-fa: {aspect('garment-rack')}; --@@-cue: {H}; }}
.@@-cartouche {{ background: none; inline-size: 90%; gap: 10px; }}
.@@-cartouche .@@-lead {{ text-transform: uppercase; letter-spacing: 0.12em; font-size: 12px; }}
.@@-cartouche .@@-names {{ font-size: min(calc(var(--name-size) * 1.05), 12vw); }}
.@@-cartouche::before, .@@-cartouche::after {{ content: ""; position: absolute; inset-inline: 20%; block-size: 1px; background: {H}; }}
.@@-cartouche::before {{ inset-block-start: 8px; }}
.@@-cartouche::after {{ inset-block-end: 8px; }}
.@@-cartouche .@@-date {{ border-radius: 0; border-color: {H}; letter-spacing: 0.08em; }}
/* clothing tag */
.@@-emblem {{ inline-size: 160px; block-size: 250px; margin-block: -10px 10px; transform-origin: 50% 0; transition: rotate 2.2s cubic-bezier(.3, 1.5, .4, 1) .2s; }}
.@@-countdown.fx:not(.is-in) .@@-emblem {{ rotate: -9deg; }}
.@@-emblem__a {{ inset-block: 0 70%; inset-inline: calc(50% - 1px); inline-size: 2px; background: {H}; }}
.@@-emblem__b {{ inset-block: 26% 0; inset-inline: 0; background: {A}; clip-path: polygon(50% 0, 100% 16%, 100% 100%, 0 100%, 0 16%); }}
.@@-emblem__c {{ inset-block: calc(26% + 2px) 2px; inset-inline: 2px; background: {C}; clip-path: polygon(50% 0, 100% 16%, 100% 100%, 0 100%, 0 16%); }}
.@@-emblem__c::before {{ content: ""; position: absolute; inset-block-start: 9%; inset-inline-start: calc(50% - 8px); inline-size: 16px; block-size: 16px; border-radius: 50%; background: {B}; box-shadow: inset 0 0 0 2px {A}; }}
.@@-emblem__c::after {{ content: ""; position: absolute; inset-block-end: 14px; inset-inline: 20px; block-size: 18px; background: repeating-linear-gradient(90deg, {H} 0 2px, transparent 2px 4px, {H} 4px 5px, transparent 5px 8px); }}
.@@-count {{ margin-block-start: 60px; }}
/* tissue paper over the photos */
.@@-veil {{ background: linear-gradient(120deg, {mix(C, 'transparent', 92)}, {mix(C, B, 80)} 50%, {mix(C, 'transparent', 90)}); box-shadow: inset 0 0 0 1px {mix(H, 'transparent', 20)}; }}
/* gallery as a film strip */
.@@:is([data-gallery-style="coverflow"], [data-gallery-style="strip"]) .@@-flow {{ padding-block: 30px 30px;
  background: radial-gradient(circle 3px, {B} 90%, transparent) 0 6px / 16px 16px repeat-x, radial-gradient(circle 3px, {B} 90%, transparent) 0 calc(100% - 6px) / 16px 16px repeat-x, {H}; }}
.@@:is([data-gallery-style="coverflow"], [data-gallery-style="strip"]) .@@-gallery__stage {{ gap: 0; }}
/* tape measure */
.@@-path {{ inline-size: 26px; border-radius: 2px; background: repeating-linear-gradient({H} 0 1px, transparent 1px 8px) 0 0 / 40% 100% no-repeat,
  repeating-linear-gradient({H} 0 1.5px, transparent 1.5px 40px) 0 0 / 70% 100% no-repeat, {mix(A, C, 70)}; }}
.@@-traveller {{ inline-size: 36px; margin-inline-start: -5px; background: {H}; }}
.@@-panel {{ background: {D}; }}
.@@-panel__decor {{ inset: 12px; border: 1px solid {mix(GLOW, 'transparent', 30)}; }}
""",
))
CONFIGS[-1]["scene"] = S

# =================================================================== Navy Bloom
S = Scene()
night_sky(S, 60)
S.lay("stars", f"inset: 0 0 50%; background-image: {stars(57, 24, GLOW, A)}", 240)
full_moon(S, "moon", "inset-block-start: 8%; inset-inline-start: 14%", 220, 62)
S.art("trees", "treesArt", "tree-line", "inset-block-start: 40%; inset-inline: -10%", mix(D, L, 70), dy=190)
S.lay("fireflies", "inset: 30% 0 30%; background-image: " + ", ".join(f"radial-gradient(3px 3px at {x}% {y}%, {mix(A, GLOW, 70)}, transparent)" for x, y in ((12, 30), (30, 70), (48, 20), (66, 60), (84, 34), (92, 80), (22, 90))), 160)
S.lay("hedge", f"inset-block: 56% -10%; inset-inline: -10%; background: radial-gradient(circle at 50% 100%, {mix(L, D, 60)} 66%, transparent 67%) 0 0 / 70px 46px repeat-x, linear-gradient(transparent 44px, {mix(L, D, 60)} 0)", 130)
S.lay("path", f"inset-block: 63% -10%; inset-inline: 0; clip-path: polygon(44% 0, 56% 0, 92% 100%, 8% 100%); background: linear-gradient({mix(GLOW, D, 40)}, {mix(GLOW, D, 22)})", 100)
S.art("arch", "archArt", "trellis-arch", "inset-block-start: 13%; inset-inline: 0; margin-inline: auto; inline-size: 82%", f"linear-gradient({mix(L, D, 72)}, {mix(L, D, 50)})", dy=90)
S.art("bloom-s", "bloomArt", "flowers-corner", "inset-block-start: 9%; inset-inline-start: 2%; inline-size: 46%", mix(GLOW, L, 30), dy=85)
S.art("bloom-e", "bloomArt", "flowers-corner", "inset-block-start: 9%; inset-inline-end: 2%; inline-size: 46%", mix(GLOW, L, 30), dy=85, extra="rotate: y 180deg;")
S.art("hydrangea-s", "sprayArt", "flowers-spray", "inset-block-end: 2%; inset-inline-start: -10%; inline-size: 34%", mix(GLOW, L, 42), dy=40)
S.art("hydrangea-e", "sprayArt", "flowers-spray", "inset-block-end: 2%; inset-inline-end: -10%; inline-size: 34%", mix(GLOW, L, 42), dy=40, extra="rotate: y 180deg;")
cart_i = len(S.html)
S.lay("fireflies-near", "inset: 36% 0 8%; background-image: " + ", ".join(f"radial-gradient(4px 4px at {x}% {y}%, {mix(A, GLOW, 60)}, transparent)" for x, y in ((8, 40), (26, 84), (74, 70), (90, 30), (60, 92))), 50, decor=True)
CONFIGS.append(dict(
    key="navy-bloom", P="nb", intro="envelope", cart_index=cart_i, cart_mode="day", veil="envelope",
    name={"ar": "زهر كحلي", "en": "Navy Bloom"},
    description={"ar": "حديقة في ليلة مقمرة بعمق: أشجار وسياج وممر وقوس ورد وأزهار هيدرانجيا ويراعات، تُفتح بظرف رسالة، مع ختم شمع للعد ورسائل تخرج من أظرفها.",
                 "en": "A garden on a moonlit night with depth: trees, a hedge, a path, a flower arch, hydrangeas and fireflies. Opens like an envelope, counts down on a wax seal, and each photo slides out of its envelope."},
    scene_note="the moonlit garden: sky, stars, moon, trees, fireflies, hedge, path, flower arch, blooms and hydrangeas drift at their own speeds",
    emblem_note="a wax seal pressed once when it arrives",
    veil_note="each photo waits in an envelope that opens once",
    path_note="a vine along the garden; a wax seal travels with you",
    css_note="a moonlit garden with a flower arch, fireflies and a wax seal.",
    veil_name=T("ظرف رسالة", "Envelope"),
    fonts={"display": "amiri", "body": "plexArabic", "latin": "italiana"},
    images={"patternTile": "damask-tile", "sealArt": "wax-seal", "monogramArt": "rosette", "travellerArt": "wax-seal", "footerArt": "trellis-arch",
            "frameArt": "ornament", "dividerArt": "ornament", "cornerArt": "flowers-corner"},
    texts={"countdownTitle": T("مختومة حتى يومنا", "Sealed until our day"), "storyTitle": T("حكايتنا", "Our story"),
           "galleryTitle": T("رسائل مصورة", "Letters in pictures"), "eventsTitle": T("في الحديقة", "In the garden"),
           "wishesTitle": T("اكتبوا رسالة للعروسين", "Write the couple a letter")},
    palettes=[palette("navyIvory", "كحلي وعاجي", "Navy & ivory", "#1B2A4A", "#F6F2EA", "#C7A867", "#F2EFE8", "#1B2A4A", "#111C33", "#3E5A4A"),
              palette("emeraldIvory", "زمردي وعاجي", "Emerald & ivory", "#0F3D30", "#F5F1E8", "#A9864F", "#F2EDE3", "#123A2F", "#0B261F", "#3E6A4A"),
              palette("dustyBlue", "أزرق مغبر", "Dusty blue", "#3E5675", "#F7F9FB", "#C2A877", "#F1F2F2", "#24364C", "#1A2840", "#5A7A62"),
              palette("plumGarden", "حديقة البرقوق", "Plum garden", "#4A2440", "#FBF5F8", "#C9A46C", "#F5EFF0", "#33192C", "#22121E", "#4E6A4A"),
              palette("midnightSilver", "كحلي وفضي", "Midnight & silver", "#E4E8F0", "#121A2C", "#AEB6C4", "#121A2C", "#E8ECF2", "#0A1020", "#3A5248", dark=True)],
    css=f"""
.@@ {{ --@@-cart-top: 25%; --@@-photo-r: 4px; --@@-trav: {aspect('wax-seal')}; --@@-fa: {aspect('trellis-arch')}; --@@-corner: {mix(A, C, 60)}; --@@-cue: {GLOW}; }}
.@@-cartouche {{ inline-size: min(270px, 74%); background: {C}; border-radius: 4px; padding-block: 30px 40px;
  box-shadow: inset 0 0 0 8px {C}, inset 0 0 0 9px {mix(A, 'transparent', 55)}, 0 30px 40px -20px {mix(D, 'transparent', 30)}; }}
.@@-cartouche::after {{ content: ""; position: absolute; inset-block-end: -22px; inset-inline-start: calc(50% - 22px); inline-size: 44px; block-size: 44px; border-radius: 50%;
  background: radial-gradient(circle at 38% 32%, {mix(H, C, 70)}, {H} 60%); box-shadow: 0 4px 8px {mix(D, 'transparent', 60)}; }}
/* wax seal */
.@@-emblem {{ inline-size: 200px; aspect-ratio: 1; margin-block: 0 40px; }}
.@@-emblem__a, .@@-emblem__c {{ inset-block: 58% -26%; inline-size: 26%; background: linear-gradient({H}, {mix(H, D, 70)}); clip-path: polygon(0 0, 100% 0, 100% 100%, 50% 84%, 0 100%); }}
.@@-emblem__a {{ inset-inline-start: 26%; rotate: 12deg; }}
.@@-emblem__c {{ inset-inline-end: 26%; rotate: -12deg; }}
.@@-emblem__b {{ inset: 0; border-radius: 50%; background: radial-gradient(circle at 38% 32%, {mix(H, C, 62)}, {H} 55%, {mix(H, D, 78)}); }}
.has-seal-art .@@-emblem__b {{ border-radius: 0; -webkit-mask: var(--img-seal-art) center / contain no-repeat; mask: var(--img-seal-art) center / contain no-repeat; }}
.@@-countdown.fx:not(.is-in) .@@-emblem__b {{ transform: scale(1.25); opacity: 0; }}
.@@-count__num {{ background: {FOIL} 0 0 / 220% 100%; -webkit-background-clip: text; background-clip: text; }}
.@@-count__unit {{ color: var(--c-on-hero); }}
/* envelopes around the photos */
.@@-veil--a {{ background: linear-gradient({mix(C, H, 82)}, {mix(C, H, 92)}); }}
.@@-veil--b {{ background: {mix(C, H, 94)}; }}
/* a vine along the garden */
.@@-path {{ background: linear-gradient(90deg, transparent 13px, {mix(L, C, 70)} 13px 17px, transparent 17px),
  radial-gradient(ellipse 7px 3.5px at 30% 50%, {L} 90%, transparent) 0 0 / 30px 34px repeat-y, radial-gradient(ellipse 7px 3.5px at 70% 50%, {L} 90%, transparent) 0 17px / 30px 34px repeat-y; }}
.@@-traveller {{ inline-size: 44px; margin-inline-start: -7px; background: radial-gradient(circle at 38% 32%, {mix(H, C, 62)}, {H} 60%); }}
.@@-panel__decor {{ background-image: {", ".join(f"radial-gradient(3px 3px at {x}% {y}%, {mix(A, GLOW, 60)}, transparent)" for x, y in ((10, 20), (24, 76), (40, 12), (62, 88), (78, 18), (90, 60), (52, 50)))}; }}
""",
))
CONFIGS[-1]["scene"] = S

# =================================================================== Midnight
S = Scene()
S.lay("sky", f"inset: -40% 0 0; background: radial-gradient(70% 30% at 50% 64%, {mix(L, 'transparent', 55)}, transparent 70%), linear-gradient({mix(D, C, 92)}, {D} 50%, {mix(D, L, 60)} 64%)", 270)
S.lay("milkyway", f"inset: -10% -30% 30%; rotate: -24deg; background: radial-gradient(46% 12% at 50% 50%, {mix(GLOW, 'transparent', 16)}, transparent), {stars(71, 30, mix(GLOW, 'transparent', 70), GLOW)}", 255)
S.lay("stars", f"inset: 0 0 40%; background-image: {stars(73, 22, GLOW, A)}", 245)
S.art("constellation", "constellationArt", "constellation", "inset-block-start: 8%; inset-inline: 8%", mix(GLOW, "transparent", 80), dy=230)
S.art("comet", "cometArt", "comet", "inset-block-start: 5%; inset-inline-end: 4%; inline-size: 38%", f"linear-gradient(90deg, transparent, {GLOW})", dy=210, dx=-110, extra="rotate: 16deg;")
crescent(S, "moon", "inset-block-start: 15%; inset-inline-start: 10%", 215, 66)
S.lay("hills-far", f"inset-block: 58% -10%; inset-inline: -30% 20%; border-radius: 50% 50% 0 0 / 30% 30% 0 0; background: {mix(L, D, 70)}", 160)
S.lay("hills-far-2", f"inset-block: 60% -10%; inset-inline: 30% -40%; border-radius: 50% 50% 0 0 / 30% 30% 0 0; background: {mix(L, D, 56)}", 150)
S.art("observatory", "observatoryArt", "observatory", "inset-block-start: 45%; inset-inline: -4%", SHADE, dy=120)
S.lay("hills-near", f"inset-block: 70% -12%; inset-inline: -20%; border-radius: 40% 60% 0 0 / 20% 30% 0 0; background: linear-gradient({mix(L, D, 45)}, {SHADE})", 70)
S.art("trees", "treesArt", "tree-line", "inset-block-end: -2%; inset-inline: -20%", SHADE, dy=30)
cart_i = len(S.html)
CONFIGS.append(dict(
    key="midnight", P="mn", intro="starfall", cart_index=cart_i, cart_mode="night", veil="part",
    name={"ar": "منتصف الليل", "en": "Midnight"},
    description={"ar": "ليلة فلكية بعمق: درب التبانة ونجوم وأبراج ومذنب يعبر السماء وقمر ومرصد على التلال، تُفتح بحلول الليل، مع أطوار القمر للعد ومذنب يرافقكم على خريطة النجوم.",
                 "en": "An astronomer's night with depth: the Milky Way, stars, a constellation, a comet crossing the sky, the moon and an observatory on the hills. Opens as night falls, counts down in moon phases, and a comet rides the star map through the events."},
    scene_note="the night sky: sky, Milky Way, stars, constellation, comet, moon, hills, observatory and trees drift at their own speeds",
    emblem_note="five phases of the moon that rise one after another",
    veil_note="each photo waits behind night clouds that part once",
    path_note="a star map; the comet travels along with you",
    css_note="an astronomer's night with an observatory, a comet and moon phases.",
    veil_name=T("غيوم تنقشع", "Parting clouds"),
    fonts={"display": "elMessiri", "body": "plexArabic", "latin": "marcellus"},
    images={"monogramArt": "rosette", "travellerArt": "comet", "footerArt": "observatory", "dividerArt": "star-divider", "frameArt": "star-divider"},
    texts={"countdownTitle": T("القمر يعدّ الليالي", "The moon counts the nights"), "storyTitle": T("حكايتنا", "Our story"),
           "galleryTitle": T("من ليالينا", "From our nights"), "eventsTitle": T("على خريطة النجوم", "On the star map"),
           "wishesTitle": T("اكتبوا أمنية للنجوم", "Wish upon a star")},
    palettes=[palette("deepNight", "ليل عميق", "Deep night", "#E9DFC8", "#0D1222", "#CDB27A", "#0D1222", "#ECE6D8", "#070B18", "#2C3A5E", dark=True),
              palette("ivoryNight", "ليل عاجي", "Ivory night", "#1A2340", "#F7F4EC", "#C6A86C", "#F1EEE6", "#1A2340", "#0B1226", "#2C3A5E"),
              palette("onyxGold", "أسود وذهبي", "Onyx & gold", "#EEE6D4", "#0A0A0B", "#CFAE6A", "#111112", "#E9E4DA", "#060607", "#2A2A36", dark=True),
              palette("emeraldNight", "ليل زمردي", "Emerald night", "#E2EEE6", "#06201A", "#C9B37E", "#0A2A22", "#DCE9E2", "#041612", "#1E4A3A", dark=True),
              palette("violetSky", "سماء بنفسجية", "Violet sky", "#ECE4F2", "#150F24", "#C9AE7A", "#150F24", "#ECE6F2", "#0C0818", "#3E2E5E", dark=True)],
    css=f"""
.@@ {{ --@@-cart-top: 21%; --@@-photo-r: 50%; --@@-trav: {aspect('comet')}; --@@-fa: {aspect('observatory')}; --@@-cue: {GLOW}; }}
.@@-cartouche::before {{ content: ""; position: absolute; inset: -18px; border-radius: 50%; background: repeating-conic-gradient({mix(A, 'transparent', 60)} 0 0.7deg, transparent 0.7deg 6deg);
  -webkit-mask: radial-gradient(closest-side, transparent 95%, var(--c-text) 96%); mask: radial-gradient(closest-side, transparent 95%, var(--c-text) 96%); }}
/* moon phases */
.@@-emblem {{ inline-size: 290px; block-size: 70px; margin-block-end: 90px; }}
.@@-emblem > span, .@@-emblem::before, .@@-emblem::after {{ inset-block-start: 14px; inline-size: 40px; block-size: 40px; border-radius: 50%; border: 1px solid {mix(GLOW, 'transparent', 30)}; }}
.@@-emblem::before, .@@-emblem::after {{ content: ""; position: absolute; transition: opacity 1.2s ease; }}
.@@-emblem__a {{ inset-inline-start: 0; box-shadow: inset -10px 0 0 0 {GLOW}; }}
.@@-emblem::before {{ inset-inline-start: 22%; box-shadow: inset -20px 0 0 0 {GLOW}; transition-delay: .5s; }}
.@@-emblem__b {{ inset-block-start: 0; inset-inline: 0; margin-inline: auto; inline-size: 66px; block-size: 66px; background: radial-gradient(circle at 38% 36%, {GLOW}, {mix(A, GLOW, 55)}); box-shadow: 0 0 30px 6px {mix(GLOW, 'transparent', 25)}; transition-delay: .8s; }}
.@@-emblem::after {{ inset-inline-end: 22%; box-shadow: inset 20px 0 0 0 {GLOW}; transition-delay: 1.1s; }}
.@@-emblem__c {{ inset-inline-end: 0; box-shadow: inset 10px 0 0 0 {GLOW}; transition-delay: 1.4s; }}
.@@-countdown.fx:not(.is-in) :is(.@@-emblem > span, .@@-emblem::before, .@@-emblem::after) {{ opacity: 0; }}
.@@-emblem__a {{ transition-delay: .2s; }}
.@@-count {{ position: absolute; inset-block-start: calc(100% + 10px); }}
/* night clouds over the photos */
.@@-veil {{ background: radial-gradient(circle at 70% 30%, {mix(L, GLOW, 70)} 0 22%, transparent 23%), radial-gradient(circle at 30% 60%, {mix(L, GLOW, 80)} 0 28%, transparent 29%), {mix(D, L, 70)}; }}
/* star map */
.@@-path {{ background: radial-gradient(circle, {GLOW} 0 1.6px, transparent 2.6px) 50% 0 / 30px 26px repeat-y, linear-gradient(90deg, transparent 14px, {mix(A, 'transparent', 45)} 14px 15px, transparent 15px); }}
.@@-traveller, .@@-traveller:dir(rtl) {{ inline-size: 96px; margin-inline-start: -33px; rotate: 90deg; background: linear-gradient(90deg, transparent, {GLOW}); }}
.has-constellation-art .@@-panel__decor {{ background: {GLOW}; opacity: 0.25; -webkit-mask: var(--img-constellation-art) 50% 6% / 80% auto no-repeat; mask: var(--img-constellation-art) 50% 6% / 80% auto no-repeat; }}
.@@-panel {{ padding-block-start: 120px; }}
""",
))
CONFIGS[-1]["scene"] = S


# =================================================================== build
def main():
    only = set(sys.argv[1:])
    kit = {}
    for cfg in CONFIGS:
        if only and cfg["key"] not in only:
            continue
        S = cfg["scene"]
        if cfg.get("panel_light"):
            cfg["css"] += "\n"
        write(cfg, S)
        # entrance stages: the scene builds back to front, then the names, then the sheet
        names = [h.split('class="')[1].split('"')[0].split()[1] for h in S.html if 'class="@@-layer' in h]
        back = names[:cfg["cart_index"]]
        q = max(1, len(back) // 3)
        groups = [back[i:i + q] for i in range(0, len(back), q)]
        front = names[cfg["cart_index"]:]
        P = cfg["P"]
        stages = [", ".join("." + n.replace("@@", P) for n in g) for g in groups] + [f".{P}-cartouche"]
        if front:
            stages.append(", ".join("." + n.replace("@@", P) for n in front))
        stages.append(f".{P}-sheet")
        kit[cfg["key"]] = {"P": P, "stages": stages}
        print(f"built {cfg['key']:13} planes={len(names) + 1}")
    if cfg.get("panel_light"):
        pass
    # light panels: switch the wishes panel class in the template
    for cfg in CONFIGS:
        if cfg.get("panel_light") and (not only or cfg["key"] in only):
            p = ROOT / "templates" / cfg["key"] / "template.html"
            p.write_text(p.read_text(encoding="utf-8").replace(f'class="{cfg["P"]}-panel"', f'class="{cfg["P"]}-panel {cfg["P"]}-panel--light"'), encoding="utf-8")
    kpath = ROOT / "tools" / "kit-templates.json"
    old = json.loads(kpath.read_text()) if kpath.exists() else {}
    old.update(kit)
    kpath.write_text(json.dumps(old, indent=2) + "\n")
    subprocess.run([sys.executable, str(ROOT / "tools" / "add-options.py")], check=True)


if __name__ == "__main__":
    main()
