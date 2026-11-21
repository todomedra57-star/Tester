#!/usr/bin/env node
// Template rule checker: checks every templates/<key>/ against the rules in the
// "Anatomy of an invitation" guide. No dependencies.
//   node tools/check-templates.mjs            all templates
//   node tools/check-templates.mjs andalus    one template
// Exit code 1 when any template has errors (warnings do not fail).
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..', 'templates');
const HELPERS = new Set(['text', 'variant', 'formatDate', 'formatTime', 'eventTime', 'eventLabel', 'daysUntil', 'calendarMonth']);
const BLOCKS = new Set(['if', 'unless', 'each', 'with', 'else']);
const RUNTIME_EFFECTS = new Set(['none', 'fade', 'fade-up', 'zoom-in', 'slide-side', 'blur-in']);
const SECTION_ORDER = ['cover', 'countdown', 'story', 'gallery', 'events', 'wishes', 'footer'];
const REQUIRED_SECTIONS = ['cover', 'countdown', 'story', 'events', 'wishes', 'footer'];
const REQUIRED_TOKENS = { color: ['hero', 'onHero', 'accent', 'bg', 'text', 'card'], font: ['display', 'body'], length: ['radius'] };
const AT_RULES = new Set(['media', 'supports', 'keyframes', 'property']);
const PHYSICAL = /(^|[\s;{])(margin|padding|border)-(left|right)(-[a-z]+)?\s*:|(^|[\s;{])(left|right)\s*:|text-align\s*:\s*(left|right)\b|float\s*:\s*(left|right)\b/;
const NAMED_COLORS = /\b(white|black|red|blue|green|yellow|gold|silver|gray|grey|pink|purple|orange|brown|navy|ivory|beige)\b/;

function checkTemplate(key) {
  const dir = join(ROOT, key);
  const errors = [], warnings = [];
  const err = (m) => errors.push(m), warn = (m) => warnings.push(m);
  for (const f of ['manifest.json', 'template.html', 'style.css']) if (!existsSync(join(dir, f))) err(`missing ${f}`);
  if (errors.length) return { key, errors, warnings };

  // ---------------------------------------------------------------- manifest
  let man;
  try { man = JSON.parse(readFileSync(join(dir, 'manifest.json'), 'utf8')); } catch (e) { err(`manifest.json is not valid JSON: ${e.message}`); return { key, errors, warnings }; }
  if (man.key !== key) err(`manifest key "${man.key}" does not match the folder name "${key}"`);
  for (const l of ['ar', 'en']) if (!man.name?.[l]) err(`name.${l} missing`);
  if (!Array.isArray(man.languages) || !man.languages.includes('ar')) err('languages must include "ar"');
  const langs = man.languages || ['ar', 'en'];
  for (const [k, v] of Object.entries(man.texts || {})) for (const l of langs) if (!v?.[l]) err(`text "${k}" has no ${l} wording`);
  const tokens = man.tokens || [];
  const byKey = new Map(tokens.map((t) => [t.key, t]));
  if (byKey.size !== tokens.length) err('duplicate token keys');
  for (const [type, keys] of Object.entries(REQUIRED_TOKENS)) for (const k of keys) if (byKey.get(k)?.type !== type) err(`required ${type} token "${k}" missing`);
  const theme = man.defaultTheme || {};
  const variants = tokens.filter((t) => t.type === 'variant');
  for (const t of tokens) {
    if (!['color', 'font', 'length', 'image', 'variant'].includes(t.type)) { err(`token "${t.key}" has unknown type "${t.type}"`); continue; }
    const v = theme[t.key];
    if (v === undefined) { err(`defaultTheme has no value for token "${t.key}"`); continue; }
    if (t.type === 'color' && !/^#[0-9a-f]{6}$/i.test(v)) err(`defaultTheme.${t.key} must be #rrggbb, got "${v}"`);
    if (t.type === 'length' && (typeof v !== 'number' || v < t.min || v > t.max)) err(`defaultTheme.${t.key}=${v} outside ${t.min}..${t.max}`);
    if (t.type === 'variant') {
      if (!t.options?.length) err(`variant "${t.key}" has no options`);
      for (const o of t.options || []) for (const l of langs) if (!t.choices?.[o]?.[l]) err(`variant "${t.key}" option "${o}" has no ${l} name`);
      if (!t.options?.includes(v)) err(`defaultTheme.${t.key}="${v}" is not one of its options`);
    }
  }
  const colorKeys = tokens.filter((t) => t.type === 'color').map((t) => t.key);
  const cp = man.couplePresets || {};
  const pals = cp.palettes || [];
  if (!pals.length) warn('no couple palettes');
  if (cp.defaultPalette && !pals.some((p) => p.key === cp.defaultPalette)) err(`defaultPalette "${cp.defaultPalette}" not found`);
  for (const p of pals) {
    for (const l of langs) if (!p.name?.[l]) err(`palette "${p.key}" has no ${l} name`);
    for (const [k, v] of Object.entries(p.values || {})) {
      if (!colorKeys.includes(k)) err(`palette "${p.key}" sets "${k}", which is not a colour token`);
      if (!/^#[0-9a-f]{6}$/i.test(v)) err(`palette "${p.key}".${k} must be #rrggbb`);
    }
    for (const k of colorKeys) if (!(k in (p.values || {}))) err(`palette "${p.key}" has no value for colour "${k}"`);
  }
  for (const v of cp.variants || []) if (!byKey.has(v.key) || byKey.get(v.key).type !== 'variant') err(`couplePresets.variants lists unknown variant "${v.key}"`);
  const ownEffects = new Set((man.effects || []).map((e) => e.key));
  const effectsOk = (e) => RUNTIME_EFFECTS.has(e) || ownEffects.has(e);
  for (const [s, cfg] of Object.entries(man.defaultAnimation?.sections || {})) if (!effectsOk(cfg.effect)) err(`section "${s}" uses unknown effect "${cfg.effect}"`);
  for (const a of cp.ambients || []) if (a !== 'none' && !ownEffects.has(a) && !['petals', 'sparkles', 'lights'].includes(a)) warn(`ambient "${a}" is neither a library nor an own effect`);

  // ---------------------------------------------------------------- template.html
  const html = readFileSync(join(dir, 'template.html'), 'utf8');
  if (/<script\b/i.test(html)) err('template.html contains <script>');
  if (/\son[a-z]+\s*=/i.test(html)) err('template.html contains an on…= attribute');
  if (/<form\b/i.test(html)) err('template.html contains its own <form>');
  if (/\{\{\{/.test(html)) err('template.html uses unescaped {{{ }}}');
  if (/<(link|style|iframe|object|embed)\b/i.test(html)) err('template.html loads styles or embeds content');
  const order = [...html.matchAll(/data-animate="([a-z-]+)"/g)].map((m) => m[1]);
  for (const s of REQUIRED_SECTIONS) if (!order.includes(s)) err(`section "${s}" (data-animate) missing`);
  const known = order.filter((s) => SECTION_ORDER.includes(s));
  if (known.join() !== [...known].sort((a, b) => SECTION_ORDER.indexOf(a) - SECTION_ORDER.indexOf(b)).join()) err(`sections out of order: ${known.join(' → ')}`);
  const wb = (html.match(/<wishes-box><\/wishes-box>/g) || []).length;
  if (wb !== 1) err(`needs exactly one <wishes-box></wishes-box>, found ${wb}`);
  else {
    const at = html.indexOf('<wishes-box>'), sec = html.lastIndexOf('data-animate="', at);
    if (!html.slice(sec, sec + 30).includes('"wishes"')) err('<wishes-box> is not inside the wishes section');
  }
  const parallax = (html.match(/data-parallax/g) || []).length;
  if (parallax > 1) err(`data-parallax used ${parallax} times (one layer only)`);
  for (const m of html.matchAll(/\{\{\s*[#/]?\s*\(?\s*([a-zA-Z]+)/g)) {
    const name = m[1];
    if (!HELPERS.has(name) && !BLOCKS.has(name) && !/^[a-z]/.test(name)) warn(`unknown helper "${name}"`);
  }
  for (const m of html.matchAll(/\(?\b([a-zA-Z]+)\s+"[^"]*"/g)) {
    if (/^(text|variant)$/.test(m[1]) || HELPERS.has(m[1])) continue;
  }
  for (const m of html.matchAll(/\{\{\s*text\s+"([^"]+)"\s*\}\}/g)) if (!man.texts?.[m[1]]) err(`{{text "${m[1]}"}} has no entry in manifest texts`);
  for (const m of html.matchAll(/variant\s+"([^"]+)"(?:\s+"([^"]+)")?/g)) {
    const t = byKey.get(m[1]);
    if (!t || t.type !== 'variant') err(`variant "${m[1]}" used in HTML but not defined`);
    else if (m[2] && !t.options.includes(m[2])) err(`variant "${m[1]}" has no option "${m[2]}"`);
  }
  for (const v of variants) {
    const attr = 'data-' + v.key.replace(/[A-Z]/g, (c) => '-' + c.toLowerCase());
    if (!html.includes(`variant "${v.key}"`)) warn(`variant "${v.key}" is never printed in the HTML (add ${attr}="{{variant "${v.key}"}}")`);
  }
  const visible = html.replace(/\{\{[\s\S]*?\}\}/g, ' ').replace(/<[^>]+>/g, ' ').replace(/&[a-z]+;/g, ' ');
  const words = visible.match(/[A-Za-z؀-ۿ]{2,}/g);
  if (words) err(`fixed words in the HTML (use {{text}}): ${[...new Set(words)].slice(0, 6).join(', ')}`);
  for (const m of html.matchAll(/<img\b[^>]*>/g)) {
    if (!/loading="lazy"/.test(m[0])) warn('an <img> without loading="lazy"');
    if (!/alt="/.test(m[0])) err('an <img> without alt');
  }

  // ---------------------------------------------------------------- style.css
  const rawCss = readFileSync(join(dir, 'style.css'), 'utf8');
  const css = rawCss.replace(/\/\*[\s\S]*?\*\//g, '');
  const opens = (css.match(/\{/g) || []).length, closes = (css.match(/\}/g) || []).length;
  if (opens !== closes) err(`unbalanced braces in style.css (${opens} "{" vs ${closes} "}")`);
  for (const m of css.matchAll(/@([a-z-]+)/g)) if (!AT_RULES.has(m[1])) err(`at-rule @${m[1]} is not allowed`);
  if (/url\(/i.test(css)) err('style.css uses url(); images must come from image tokens');
  // declarations: property: value
  const decls = [...css.matchAll(/([a-z-]+)\s*:\s*([^;{}]+)[;}]/g)].map((m) => ({ prop: m[1], value: m[2] }));
  const colorProps = /^(color|background|background-color|background-image|border|border-[a-z-]+|outline|outline-color|box-shadow|text-shadow|fill|stroke|filter|mask|mask-image|-webkit-mask|-webkit-mask-image|-webkit-text-stroke|-webkit-box-reflect|caret-color|accent-color|text-decoration-color|column-rule)$/;
  const rawColors = new Set();
  for (const { prop, value } of decls) {
    if (prop.startsWith('--')) continue;
    if (/#[0-9a-f]{3,8}\b/i.test(value)) rawColors.add(`${prop}: ${value.trim().slice(0, 50)}`);
    if (colorProps.test(prop) && (/\b(rgb|rgba|hsl|hsla)\(/.test(value) || NAMED_COLORS.test(value.replace(/var\([^)]*\)/g, '')))) rawColors.add(`${prop}: ${value.trim().slice(0, 50)}`);
  }
  for (const m of css.matchAll(/(--[a-z0-9-]+)\s*:\s*([^;{}]+)[;}]/g)) if (/#[0-9a-f]{3,8}\b/i.test(m[2])) rawColors.add(`${m[1]}: ${m[2].trim().slice(0, 50)}`);
  for (const r of [...rawColors].slice(0, 8)) err(`raw colour (use tokens): ${r}`);
  if (rawColors.size > 8) err(`…and ${rawColors.size - 8} more raw colours`);
  for (const { prop, value } of decls) {
    if (prop === 'font-family' && !/^\s*(var\(--font-[a-z-]+\)|inherit)\s*$/.test(value)) err(`font-family must use a font token: "${value.trim()}"`);
  }
  const physical = css.split('}').filter((b) => PHYSICAL.test(b.slice(b.indexOf('{') + 1)));
  for (const b of physical.slice(0, 4)) err(`physical property (use logical): ${b.trim().split('{')[0].trim().slice(0, 60)}`);
  if (!/prefers-reduced-motion/.test(css)) err('no prefers-reduced-motion handling');
  const prefixes = [key, ...ownEffects];
  for (const m of css.matchAll(/@keyframes\s+([a-z0-9-]+)/g)) if (!prefixes.some((p) => m[1].startsWith(p))) err(`keyframes "${m[1]}" must start with the template key or an own effect key`);
  for (const m of css.matchAll(/\.(fx|intro|ambient)-([a-z0-9-]+)/g)) {
    if (m[1] === 'fx' && RUNTIME_EFFECTS.has(m[2])) continue;
    if (!ownEffects.has(m[2])) err(`.${m[1]}-${m[2]} styles an effect this template does not declare`);
  }
  for (const block of css.split('}')) {
    const [sel, body] = block.split('{');
    const ls = body && body.match(/letter-spacing\s*:\s*([^;}]+)/);
    if (ls && !/^(0|normal)\b/.test(ls[1].trim()) && sel && !/:lang\(en\)/.test(sel)) warn(`letter-spacing outside :lang(en): ${sel.trim().slice(0, 60)}`);
  }
  for (const t of tokens.filter((t) => t.type === 'image')) {
    const cssName = '--img-' + t.key.replace(/[A-Z]/g, (c) => '-' + c.toLowerCase());
    if (!css.includes(cssName)) warn(`image token "${t.key}" is never used (${cssName})`);
  }
  return { key, errors, warnings };
}

const only = process.argv[2];
const keys = readdirSync(ROOT, { withFileTypes: true }).filter((d) => d.isDirectory() && (!only || d.name === only)).map((d) => d.name).sort();
let failed = 0;
for (const k of keys) {
  const { errors, warnings } = checkTemplate(k);
  if (errors.length) failed++;
  console.log(`${errors.length ? '✗' : '✓'} ${k}  (${errors.length} errors, ${warnings.length} warnings)`);
  for (const e of errors) console.log(`    error: ${e}`);
  for (const w of warnings) console.log(`    warn:  ${w}`);
}
console.log(`\n${keys.length - failed}/${keys.length} templates pass.`);
process.exit(failed ? 1 : 0);
