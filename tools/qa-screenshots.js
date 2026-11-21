#!/usr/bin/env node
// Visual QA: renders every template x test case (full page) and a cover in every
// palette, runs automatic layout checks, and writes qa/report.html.
//   1. serve the repo:   python3 -m http.server 8765
//   2. run:              node tools/qa-screenshots.js [template]
// Options (env): QA_URL (default http://localhost:8765/),
//                QA_HANDLEBARS=/path/handlebars.min.js to serve Handlebars locally
//                when the CDN is unreachable.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const URL = process.env.QA_URL || 'http://localhost:8765/';
const OUT = path.join(__dirname, '..', 'qa');
const SHOTS = path.join(OUT, 'shots');
const CASES = ['demo-ar', 'demo-en', 'minimal', 'longest'];
const WIDTH = 390, HEIGHT = 844;
const HEIGHT_PX = HEIGHT;
fs.mkdirSync(SHOTS, { recursive: true });

async function main() {
  const only = process.argv[2];
  const browser = await chromium.launch();
  const ui = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  if (process.env.QA_HANDLEBARS) {
    await ui.route('**/handlebars.min.js', (r) => r.fulfill({ path: process.env.QA_HANDLEBARS, contentType: 'text/javascript' }));
  }
  await ui.goto(URL);
  await ui.waitForSelector('#template option', { state: 'attached' });
  const templates = (await ui.$$eval('#template option', (o) => o.map((x) => x.value))).filter((t) => !only || t === only);
  const page = await browser.newPage({ viewport: { width: WIDTH, height: HEIGHT }, deviceScaleFactor: Number(process.env.QA_DPR || 0.5) });
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));

  // render what the preview built for the current choices, at phone size, same origin
  async function render() {
    await ui.waitForTimeout(500);
    const html = await ui.$eval('#frame', (f) => f.srcdoc);
    // load the rendered invitation as a real page (document.write would leave custom elements such as <wishes-box> un-upgraded)
    fs.writeFileSync(path.join(OUT, '_render.html'), html);
    errors.length = 0;
    await page.goto(URL + 'qa/_render.html');
    // wait until the stylesheets and the runtime have really arrived (first loads are not cached)
    await page.waitForFunction(() => window.customElements.get('wishes-box')
      && [...document.querySelectorAll('link[rel="stylesheet"]')].every((l) => { try { return l.sheet && l.sheet.cssRules; } catch (e) { return true; } }), null, { timeout: 15000 });
    await page.waitForTimeout(300);
    await page.evaluate(() => {
      // capture the final, revealed state: skip transition timing for the screenshot
      const st = document.createElement('style');
      // fixed page layers only cover one screen in a full-page capture: stretch them over the page instead
      st.textContent = '*, *::before, *::after { transition-duration: 0s !important; transition-delay: 0s !important; } main::before, main::after { position: absolute !important; } * { content-visibility: visible !important; }';
      document.head.append(st);
      document.querySelectorAll('img').forEach((i) => { i.loading = 'eager'; });
      document.querySelectorAll('[data-animate]').forEach((s) => s.classList.add('is-in'));
    });
    await page.waitForTimeout(400);
    // transitions the runtime already started keep their timing: jump them to the end
    await page.evaluate(() => document.getAnimations().forEach((a) => { if (a instanceof CSSTransition) a.finish(); }));
    await page.waitForTimeout(1200);
  }

  async function checks() {
    return page.evaluate((vw) => {
      const issues = [];
      const doc = document.documentElement;
      if (doc.scrollWidth > vw + 1) issues.push(`page scrolls sideways (${doc.scrollWidth}px wide)`);
      const broken = [...document.images].filter((i) => i.complete && i.naturalWidth === 0).length;
      if (broken) issues.push(`${broken} image(s) failed to load`);
      const off = new Set();
      for (const el of document.querySelectorAll('main p, main h1, main h2, main h3, main li, main a, main span')) {
        if (el.closest('[aria-hidden="true"]') || !el.textContent.trim() || el.children.length > 3) continue;
        const r = el.getBoundingClientRect();
        if (r.width === 0) continue;
        if (r.left < -2 || r.right > vw + 2) off.add(el.className || el.tagName);
      }
      if (off.size) issues.push(`text outside the screen: ${[...off].slice(0, 4).join(', ')}`);
      const hidden = [...document.querySelectorAll('main p, main h1, main h2')].filter((el) => {
        if (el.closest('[aria-hidden="true"]') || !el.textContent.trim()) return false;
        let n = el;
        while (n && n !== document.body) { if (getComputedStyle(n).opacity === '0') return true; n = n.parentElement; }
        return false;
      }).length;
      if (hidden) issues.push(`${hidden} text element(s) still invisible after reveal`);
      return issues;
    }, WIDTH);
  }

  const report = [];
  for (const t of templates) {
    await ui.selectOption('#template', t);
    await ui.waitForTimeout(600);
    await ui.selectOption('#intro', 'none');
    const entry = { template: t, cases: [], palettes: [] };
    const palettes = await ui.$$eval('#palette option', (o) => o.map((x) => [x.value, x.textContent]));
    for (const c of CASES) {
      await ui.selectOption('#case', c);
      await render();
      const file = `${t}--${c}.jpg`;
      const issues = [...(await checks()), ...errors.map((e) => `page error: ${e}`)];
      // templates using the scene engine play while scrolling: capture a scroll-through instead of one tall picture
      const frames = [];
      if (await page.evaluate(() => !!document.querySelector('[data-scene]'))) {
        const total = await page.evaluate(() => document.documentElement.scrollHeight - innerHeight);
        const steps = Math.min(14, Math.ceil(total / (HEIGHT_PX * 0.85)) + 1);
        for (let i = 0; i < steps; i++) {
          await page.evaluate((y) => scrollTo(0, y), Math.round((total * i) / Math.max(1, steps - 1)));
          await page.waitForTimeout(700);
          const f = `${t}--${c}--${String(i).padStart(2, '0')}.jpg`;
          await page.screenshot({ path: path.join(SHOTS, f), type: 'jpeg', quality: 72 });
          frames.push(f);
        }
        await page.evaluate(() => scrollTo(0, 0));
      }
      await page.screenshot({ path: path.join(SHOTS, file), fullPage: true, type: 'jpeg', quality: 70 });
      entry.cases.push({ c, file, frames, issues });
      console.log(`${t} ${c}: ${issues.length ? issues.join(' | ') : 'ok'}`);
    }
    await ui.selectOption('#case', 'demo-ar');
    for (const [pal, label] of palettes) {
      await ui.selectOption('#palette', pal);
      await render();
      const file = `${t}--palette-${pal}.jpg`;
      await page.screenshot({ path: path.join(SHOTS, file), type: 'jpeg', quality: 72 });
      const issues = [...(await checks()), ...errors.map((e) => `page error: ${e}`)];
      entry.palettes.push({ pal, label, file, issues });
      if (issues.length) console.log(`${t} palette ${pal}: ${issues.join(' | ')}`);
    }
    await ui.selectOption('#palette', palettes[0][0]);
    report.push(entry);
  }
  await browser.close();
  fs.writeFileSync(path.join(OUT, 'report.json'), JSON.stringify(report, null, 2));
  fs.writeFileSync(path.join(OUT, 'report.html'), html(report));
  const n = report.reduce((a, e) => a + e.cases.concat(e.palettes).filter((x) => x.issues.length).length, 0);
  console.log(`\nWrote qa/report.html — ${report.length} templates, ${n} screen(s) with issues.`);
}

const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const LABEL = { 'demo-ar': 'Arabic demo', 'demo-en': 'English', minimal: 'Smallest', longest: 'Longest' };
function html(report) {
  const total = report.reduce((a, e) => a + e.cases.concat(e.palettes).filter((x) => x.issues.length).length, 0);
  const card = (src, title, issues, cls) => `<figure class="${cls}${issues.length ? ' bad' : ''}"><a href="${src}" target="_blank" rel="noopener"><img src="${src}" alt="${esc(title)}" loading="lazy"></a>
<figcaption><b>${esc(title)}</b>${issues.length ? `<ul>${issues.map((i) => `<li>${esc(i)}</li>`).join('')}</ul>` : '<span class="ok">No issues found</span>'}</figcaption></figure>`;
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Template QA Report</title>
<style>
:root { --bg: #F4F5F8; --panel: #FFFFFF; --text: #1A2233; --muted: #5E6880; --line: #DDE1EA; --bad: #B42318; --good: #1B7F4B; color-scheme: light; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg: #0C111B; --panel: #131A28; --text: #E3E8F2; --muted: #95A0B8; --line: #263048; --bad: #FF8A80; --good: #6FD39B; color-scheme: dark; } }
:root[data-theme="dark"] { --bg: #0C111B; --panel: #131A28; --text: #E3E8F2; --muted: #95A0B8; --line: #263048; --bad: #FF8A80; --good: #6FD39B; color-scheme: dark; }
* { box-sizing: border-box; }
body { margin: 0; padding: 24px 16px 60px; background: var(--bg); color: var(--text); font: 14px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; }
header, section { max-width: 1200px; margin: 0 auto; }
h1 { margin: 0 0 4px; font-size: 22px; } h2 { margin: 36px 0 12px; font-size: 18px; } h3 { margin: 18px 0 8px; font-size: 13px; color: var(--muted); text-transform: uppercase; letter-spacing: .06em; }
.sub { margin: 0; color: var(--muted); }
nav { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 14px; } nav a { padding: 4px 10px; border: 1px solid var(--line); border-radius: 999px; color: inherit; text-decoration: none; background: var(--panel); }
.row { display: flex; gap: 12px; overflow-x: auto; padding-bottom: 8px; align-items: flex-start; }
figure { margin: 0; flex: none; background: var(--panel); border: 1px solid var(--line); border-radius: 10px; overflow: hidden; }
figure.bad { border-color: var(--bad); box-shadow: 0 0 0 1px var(--bad); }
.full { width: 200px; } .full img { display: block; width: 100%; height: 720px; object-fit: cover; object-position: top; }
.cover { width: 150px; } .cover img { display: block; width: 100%; aspect-ratio: 390 / 844; object-fit: cover; }
figcaption { padding: 8px 10px; font-size: 12px; } figcaption ul { margin: 4px 0 0; padding-inline-start: 16px; color: var(--bad); } .ok { display: block; color: var(--good); }
.summary { display: inline-block; margin-top: 10px; padding: 4px 10px; border-radius: 6px; background: var(--panel); border: 1px solid var(--line); }
</style></head><body>
<header><h1>Template QA report</h1>
<p class="sub">Every template in four test cases (full page) and its cover in every palette, rendered at 390px. Red frames have automatic findings. Tap a picture to open it full size.</p>
<span class="summary">${report.length} templates · ${report.reduce((a, e) => a + e.cases.length + e.palettes.length, 0)} screens · ${total ? `${total} with findings` : 'no automatic findings'}</span>
<nav>${report.map((e) => `<a href="#${e.template}">${esc(e.template)}</a>`).join('')}</nav></header>
${report.map((e) => `<section id="${e.template}"><h2>${esc(e.template)}</h2><h3>Test cases</h3>${e.cases.some((x) => x.frames && x.frames.length)
  ? e.cases.map((x) => `<h3>${esc(LABEL[x.c])} · scroll-through</h3><div class="row">${x.frames.map((f, i) => card('shots/' + f, `${i + 1}/${x.frames.length}`, i ? [] : x.issues, 'cover')).join('')}</div>`).join('')
  : `<div class="row">${e.cases.map((x) => card('shots/' + x.file, LABEL[x.c], x.issues, 'full')).join('')}</div>`}
<h3>Palettes</h3><div class="row">${e.palettes.map((x) => card('shots/' + x.file, x.label, x.issues, 'cover')).join('')}</div></section>`).join('\n')}
</body></html>`;
}

main().catch((e) => { console.error(e); process.exit(1); });
