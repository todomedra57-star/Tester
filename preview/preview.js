// Preview harness: renders the Midnight template the way the platform would
// (view model + manifest texts + tokens), inside an iframe at phone width.
import { CASES } from './demo-data.js';

const TEMPLATE = 'templates/midnight/';
const BASE = new URL('.', location.href).href;
const TZ = 'Asia/Riyadh';

// Stand-in for the platform's font library.
const FONT_LIBRARY = {
  amiri: "'Amiri', 'Times New Roman', serif",
  plexArabic: "'IBM Plex Sans Arabic', system-ui, sans-serif",
  cormorant: "'Cormorant Garamond', 'Amiri', Georgia, serif",
  reemKufi: "'Reem Kufi', 'IBM Plex Sans Arabic', sans-serif",
};
const FONTS_CSS = 'https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=IBM+Plex+Sans+Arabic:wght@400;500;600&family=Reem+Kufi:wght@400;500&display=swap';

// Platform words (the runtime owns these, not the template).
const PLATFORM = {
  ar: {
    events: { katb: 'كتب الكتاب', henna: 'الحنة', engagement: 'الخطوبة', wedding: 'الفرح' },
    weekdays: ['س', 'ح', 'ن', 'ث', 'ر', 'خ', 'ج'],
    words: { tapToOpen: 'اضغط لفتح الدعوة', name: 'اسمك', message: 'رسالتك', namePh: 'مثلًا: خالة منى',
      messagePh: 'اكتب تهنئتك أو دعوتك هنا', send: 'أرسل الدعوة', sent: 'وصلت دعوتك للعروسين. جزاك الله خيرًا',
      fill: 'اكتب اسمك ورسالتك أولًا' },
  },
  en: {
    events: { katb: 'Katb el-ketab', henna: 'Henna night', engagement: 'Engagement', wedding: 'Wedding' },
    weekdays: ['Sa', 'Su', 'Mo', 'Tu', 'We', 'Th', 'Fr'],
    words: { tapToOpen: 'Tap to open the invitation', name: 'Your name', message: 'Your message', namePh: 'e.g. Aunt Mona',
      messagePh: 'Write your wishes here', send: 'Send your wish', sent: 'Your wish has reached the couple. Thank you!',
      fill: 'Please add your name and a message' },
  },
};

// ---------- render context + helpers (the documented helper set) ----------
let ctx = { lang: 'ar', manifest: null, variants: {} };
const locale = () => (ctx.lang === 'ar' ? 'ar-EG' : 'en-GB');
const toDate = (v) => (v ? new Date(/T/.test(v) ? v : `${v}T12:00:00+03:00`) : null);
const ymd = (d) => {
  const p = Object.fromEntries(new Intl.DateTimeFormat('en-CA', { timeZone: TZ, year: 'numeric', month: 'numeric', day: 'numeric' })
    .formatToParts(d).map((x) => [x.type, +x.value]));
  return [p.year, p.month, p.day];
};
const num = (n) => new Intl.NumberFormat(locale()).format(n);

function registerHelpers(H) {
  H.registerHelper('text', (key) => ctx.manifest.texts[key]?.[ctx.lang] ?? '');
  H.registerHelper('variant', function (key, option) {
    const value = ctx.variants[key];
    return arguments.length === 2 ? value : value === option;
  });
  H.registerHelper('formatDate', (v) => {
    const d = toDate(v);
    return d ? new Intl.DateTimeFormat(locale(), { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric', timeZone: TZ }).format(d) : '';
  });
  const formatTime = (t) => {
    const m = /^(\d{1,2}):(\d{2})$/.exec(t || '');
    if (!m) return t || '';
    const d = new Date(`2000-01-01T${m[1].padStart(2, '0')}:${m[2]}:00+03:00`);
    return new Intl.DateTimeFormat(ctx.lang === 'ar' ? 'ar-EG' : 'en-US', { hour: 'numeric', minute: '2-digit', timeZone: TZ }).format(d);
  };
  H.registerHelper('formatTime', formatTime);
  H.registerHelper('eventTime', (ev) => formatTime(ev.time));
  H.registerHelper('eventLabel', (type) => PLATFORM[ctx.lang].events[type] || type);
  H.registerHelper('daysUntil', (v) => {
    const [a, b] = [ymd(new Date()), ymd(toDate(v))];
    const days = Math.round((Date.UTC(...b.map((x, i) => (i === 1 ? x - 1 : x))) - Date.UTC(...a.map((x, i) => (i === 1 ? x - 1 : x)))) / 864e5);
    return num(Math.max(0, days));
  });
  H.registerHelper('calendarMonth', (v) => {
    const d = toDate(v);
    const [y, m, day] = ymd(d);
    const first = new Date(Date.UTC(y, m - 1, 1)).getUTCDay(); // 0 = Sunday
    const offset = (first + 1) % 7;                             // Saturday first
    const count = new Date(Date.UTC(y, m, 0)).getUTCDate();
    const cells = [
      ...Array.from({ length: offset }, () => ({ label: '', empty: true, wedding: false })),
      ...Array.from({ length: count }, (_, i) => ({ label: num(i + 1), empty: false, wedding: i + 1 === day })),
    ];
    return {
      title: new Intl.DateTimeFormat(locale(), { month: 'long', year: 'numeric', timeZone: TZ }).format(d),
      weekdays: PLATFORM[ctx.lang].weekdays,
      cells,
    };
  });
}

// ---------- tokens → CSS variables ----------
const kebab = (k) => k.replace(/[A-Z]/g, (c) => '-' + c.toLowerCase());
function tokenCss(manifest, theme) {
  const out = [];
  for (const t of manifest.tokens) {
    const v = theme[t.key];
    if (t.type === 'color' && /^#[0-9a-f]{6}$/i.test(v)) out.push(`--c-${kebab(t.key)}: ${v};`);
    if (t.type === 'font' && FONT_LIBRARY[v]) out.push(`--font-${kebab(t.key)}: ${FONT_LIBRARY[v]};`);
    if (t.type === 'length' && typeof v === 'number') out.push(`--${kebab(t.key)}: ${Math.min(t.max, Math.max(t.min, v))}${t.unit};`);
  }
  return `:root{${out.join('')}}`;
}

// ---------- UI ----------
const $ = (id) => document.getElementById(id);
const frame = $('frame');
let manifest, compiled, playIntro = true;

function fillSelect(sel, options) {
  sel.innerHTML = '';
  for (const [value, label] of options) sel.append(new Option(label, value));
}

function render() {
  const c = CASES[$('case').value];
  const palette = manifest.couplePresets.palettes.find((p) => p.key === $('palette').value);
  const motion = manifest.couplePresets.motions[$('motion').value];
  const theme = { ...manifest.defaultTheme, ...palette.values };
  ctx = {
    lang: c.lang,
    manifest,
    variants: { dateStyle: $('dateStyle').value, countdownStyle: $('countdownStyle').value, photoFrame: $('photoFrame').value },
  };
  const body = compiled(c.vm);
  const { groom, bride } = c.vm.couple;
  const runtime = {
    intro: playIntro ? $('intro').value : 'none',
    ambient: $('ambient').value,
    motion,
    sections: manifest.defaultAnimation.sections,
    names: bride.name ? `${groom.name} ${ctx.manifest.texts.and[c.lang]} ${bride.name}` : groom.name,
    monogram: groom.name.trim()[0] || '♡',
    words: PLATFORM[c.lang].words,
    wishes: c.vm.wishes,
  };
  const keepScroll = !playIntro && frame.contentWindow ? frame.contentWindow.scrollY : 0;
  frame.onload = () => { if (keepScroll) frame.contentWindow.scrollTo(0, keepScroll); };
  frame.srcdoc = `<!doctype html><html lang="${c.lang}" dir="${c.lang === 'ar' ? 'rtl' : 'ltr'}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="${FONTS_CSS}">
<link rel="stylesheet" href="${BASE}preview/runtime.css">
<link rel="stylesheet" href="${BASE}${TEMPLATE}style.css">
<style>${tokenCss(manifest, theme)}</style></head><body>${body}
<script type="application/json" id="runtime-config">${JSON.stringify(runtime).replace(/</g, '\\u003c')}</script>
<script src="${BASE}preview/runtime.js"></script></body></html>`;
  playIntro = false;
}

async function init() {
  const [m, tpl] = await Promise.all([
    fetch(TEMPLATE + 'manifest.json').then((r) => r.json()),
    fetch(TEMPLATE + 'template.html').then((r) => r.text()),
  ]);
  manifest = m;
  registerHelpers(window.Handlebars);
  compiled = window.Handlebars.compile(tpl, { strict: false });

  const name = (o) => o.name?.en ?? o;
  const variant = (key) => manifest.tokens.find((t) => t.key === key);
  fillSelect($('case'), Object.entries(CASES).map(([k, v]) => [k, v.label]));
  fillSelect($('palette'), manifest.couplePresets.palettes.map((p) => [p.key, name(p)]));
  for (const key of ['dateStyle', 'countdownStyle', 'photoFrame']) {
    const t = variant(key);
    fillSelect($(key), t.options.map((o) => [o, t.choices[o].en]));
    $(key).value = manifest.defaultTheme[key];
  }
  fillSelect($('intro'), manifest.couplePresets.intros.map((i) => [i, i]));
  $('intro').value = manifest.defaultAnimation.intro;
  fillSelect($('ambient'), manifest.couplePresets.ambients.map((i) => [i, i]));
  $('ambient').value = manifest.defaultAnimation.ambient;
  fillSelect($('motion'), Object.keys(manifest.couplePresets.motions).map((k) => [k, k]));

  document.querySelectorAll('.controls select').forEach((s) => s.addEventListener('change', () => {
    if (s.id === 'intro' || s.id === 'case') playIntro = true;
    render();
  }));
  $('replay').addEventListener('click', () => { playIntro = true; render(); });
  document.querySelectorAll('[name="device"]').forEach((r) => r.addEventListener('change', () => {
    document.querySelector('.stage').dataset.device = r.value;
  }));
  render();
}

init().catch((err) => {
  $('error').hidden = false;
  $('error').textContent = `Could not load the template: ${err.message}. Serve this folder over http (e.g. "npx serve .") instead of opening the file directly.`;
});
