// Original artwork for the redesigned scene templates → preview/library/.
// Run: node tools/make-art-scenes.mjs
// Single-colour silhouettes used as CSS masks (the template colours them).
import { writeFileSync, mkdirSync } from 'node:fs';

const OUT = new URL('../preview/library/', import.meta.url);
mkdirSync(OUT, { recursive: true });
const K = '#000';
const f = (n) => Math.round(n * 100) / 100;
const svg = (vb, body) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${vb}">${body}</svg>`;
let seed = 11;
const rnd = () => ((seed = (seed * 16807) % 2147483647) - 1) / 2147483646;

// ---------- desert ----------
function camel(x, y, s = 1, rider = true) {
  const t = (px, py) => `${f(x + px * s)} ${f(y + py * s)}`;
  let b = `<path d="M${t(0, 0)} C ${t(4, -18)} ${t(14, -30)} ${t(26, -32)} C ${t(32, -46)} ${t(44, -48)} ${t(50, -36)} C ${t(56, -40)} ${t(64, -40)} ${t(68, -32)}
    L ${t(80, -44)} C ${t(84, -50)} ${t(92, -50)} ${t(94, -44)} L ${t(96, -40)} L ${t(90, -38)} L ${t(78, -22)} C ${t(76, -12)} ${t(72, -6)} ${t(70, 0)} Z" fill="${K}"/>`;
  for (const [lx, a] of [[8, -6], [16, 6], [58, -6], [66, 6]]) b += `<path d="M${t(lx, -2)} L ${t(lx + a * 0.5, 30)} L ${t(lx + a * 0.5 + 4, 30)} L ${t(lx + 6, -2)} Z" fill="${K}"/>`;
  if (rider) b += `<path d="M${t(34, -44)} C ${t(32, -60)} ${t(44, -62)} ${t(44, -46)} Z" fill="${K}"/><circle cx="${f(x + 39 * s)}" cy="${f(y - 66 * s)}" r="${f(6 * s)}" fill="${K}"/>`;
  return b;
}
const caravan = svg('0 0 520 120', camel(20, 86, 0.9) + camel(150, 90, 1) + camel(290, 88, 0.95, false) + camel(410, 90, 0.85)
  + `<path d="M0 116 Q 260 100 520 116 V120 H0 Z" fill="${K}"/>`);
const tent = svg('0 0 300 180', `<path d="M10 170 L150 20 L290 170 Z" fill="${K}"/><path d="M150 22 V2" stroke="${K}" stroke-width="3"/><path d="M151 3 L172 9 L151 15 Z" fill="${K}"/>
  <path d="M120 170 L150 90 L180 170 Z" fill="#fff"/><path d="M0 172 H300 V180 H0 Z" fill="${K}"/>`).replace('fill="#fff"', 'fill="#000" fill-opacity="0"');
const tentDoor = svg('0 0 300 180', `<path d="M120 170 L150 90 L180 170 Z" fill="${K}"/>`);

// ---------- royal ballroom ----------
function chandelier() {
  let b = `<path d="M100 0 V40" stroke="${K}" stroke-width="2"/><circle cx="100" cy="46" r="8" fill="${K}"/>`;
  for (const [w, y] of [[150, 80], [100, 116], [56, 146]]) {
    b += `<path d="M${100 - w / 2} ${y} Q 100 ${y + 26} ${100 + w / 2} ${y}" fill="none" stroke="${K}" stroke-width="3"/>`;
    for (let i = 0; i <= 6; i++) {
      const x = 100 - w / 2 + (w * i) / 6, yy = y + Math.sin((Math.PI * i) / 6) * 13;
      b += `<path d="M${f(x)} ${f(yy)} V${f(yy - 16)}" stroke="${K}" stroke-width="2.4"/><path d="M${f(x - 2.5)} ${f(yy - 16)} Q ${f(x)} ${f(yy - 26)} ${f(x + 2.5)} ${f(yy - 16)} Z" fill="${K}"/>`;
      b += `<path d="M${f(x)} ${f(yy)} l -3 8 l 3 7 l 3 -7 Z" fill="${K}"/>`;
    }
  }
  b += `<path d="M100 46 V170" stroke="${K}" stroke-width="2"/><path d="M92 170 L100 186 L108 170 Z" fill="${K}"/>`;
  return svg('0 0 200 190', b);
}
function ballWindow() {
  let b = `<path d="M10 400 V120 A90 90 0 0 1 190 120 V400 Z" fill="none" stroke="${K}" stroke-width="8"/>`;
  b += `<path d="M100 30 V400 M10 150 H190 M10 230 H190 M10 310 H190" stroke="${K}" stroke-width="3"/>`;
  b += `<path d="M28 120 A72 72 0 0 1 172 120" fill="none" stroke="${K}" stroke-width="2"/>`;
  for (let i = 1; i < 6; i++) { const a = Math.PI + (Math.PI * i) / 6; b += `<path d="M100 120 L${f(100 + Math.cos(a) * 88)} ${f(120 + Math.sin(a) * 88)}" stroke="${K}" stroke-width="2"/>`; }
  return svg('0 0 200 400', b);
}
function classicColumn() {
  let b = `<rect x="6" y="400" width="68" height="14" fill="${K}"/><rect x="12" y="390" width="56" height="10" fill="${K}"/>`;
  for (let i = 0; i < 6; i++) b += `<rect x="${16 + i * 8.4}" y="70" width="6" height="320" rx="3" fill="${K}"/>`;
  b += `<rect x="10" y="58" width="60" height="12" fill="${K}"/><path d="M4 58 C -6 40 18 34 22 48 M76 58 C 86 40 62 34 58 48" stroke="${K}" stroke-width="6" fill="none"/>`;
  b += `<rect x="0" y="40" width="80" height="12" fill="${K}"/>`;
  return svg('0 0 80 414', b);
}

// ---------- glass garden ----------
function butterfly() {
  return svg('0 0 100 80', `<path d="M50 40 C 30 0 0 6 6 30 C 10 46 30 44 48 42 Z" fill="${K}"/><path d="M50 40 C 70 0 100 6 94 30 C 90 46 70 44 52 42 Z" fill="${K}"/>
  <path d="M48 44 C 30 50 18 70 30 74 C 40 76 46 60 49 46 Z" fill="${K}"/><path d="M52 44 C 70 50 82 70 70 74 C 60 76 54 60 51 46 Z" fill="${K}"/>
  <rect x="48.5" y="30" width="3" height="30" rx="1.5" fill="${K}"/><path d="M50 30 Q 44 14 38 10 M50 30 Q 56 14 62 10" stroke="${K}" stroke-width="1.5" fill="none"/>`);
}
function urn() {
  let b = `<path d="M40 300 H160 L150 280 H50 Z M60 280 C 30 230 30 190 50 170 H150 C 170 190 170 230 140 280 Z M44 160 H156 V172 H44 Z" fill="${K}"/>`;
  // a plant spilling out
  for (let i = 0; i < 14; i++) {
    const a = -Math.PI + (Math.PI * i) / 13, len = 70 + rnd() * 50;
    const ex = 100 + Math.cos(a) * len, ey = 160 + Math.sin(a) * len * 1.2;
    b += `<path d="M100 162 Q ${f((100 + ex) / 2)} ${f(ey - 20)} ${f(ex)} ${f(ey)}" stroke="${K}" stroke-width="3" fill="none"/>`;
    b += `<path d="M${f(ex)} ${f(ey)} q 10 -8 18 0 q -8 8 -18 0 Z" fill="${K}" transform="rotate(${f((a * 180) / Math.PI)} ${f(ex)} ${f(ey)})"/>`;
  }
  return svg('0 0 200 300', b);
}
function treeLine() {
  let b = '';
  for (let x = -20; x < 640; x += 46 + rnd() * 30) { const r = 30 + rnd() * 30; b += `<circle cx="${f(x)}" cy="${f(150 - r * 0.7)}" r="${f(r)}" fill="${K}"/>`; }
  b += `<rect x="0" y="120" width="600" height="40" fill="${K}"/>`;
  return svg('0 0 600 160', b);
}

// ---------- lace boutique ----------
function bouquet() {
  let b = '';
  const rose = (x, y, r) => {
    let o = `<circle cx="${x}" cy="${y}" r="${r}" fill="${K}"/>`;
    for (let i = 0; i < 3; i++) o += `<path d="M${x - r * (0.7 - i * 0.2)} ${y} a ${r * (0.7 - i * 0.2)} ${r * (0.7 - i * 0.2)} 0 1 1 ${r * (1.4 - i * 0.4)} 0" fill="none" stroke="#fff" stroke-width="1.6"/>`;
    return o;
  };
  for (const [x, y, a] of [[60, 150, -60], [140, 150, 60], [40, 110, -90], [160, 110, 90], [100, 170, 0]]) b += `<path d="M100 200 Q ${x} ${y - 20} ${x} ${y}" stroke="${K}" stroke-width="3" fill="none"/><path d="M${x} ${y} q 16 -10 30 0 q -14 10 -30 0 Z" fill="${K}" transform="rotate(${a} ${x} ${y})"/>`;
  b += rose(100, 80, 26) + rose(64, 96, 20) + rose(136, 96, 20) + rose(84, 52, 16) + rose(118, 50, 15);
  b += `<path d="M86 200 L100 280 L114 200 Z" fill="${K}"/><path d="M80 210 Q 60 240 70 270 M120 210 Q 140 240 130 270" stroke="${K}" stroke-width="5" fill="none"/>`;
  return svg('0 0 200 290', `<mask id="m"><rect width="200" height="290" fill="#fff"/>${b.match(/<path d="M[^"]*a [^"]*" fill="none" stroke="#fff"[^>]*\/>/g)?.join('').replace(/#fff/g, '#000') || ''}</mask><g mask="url(#m)">${b.replace(/<path d="M[^"]*a [^"]*" fill="none" stroke="#fff"[^>]*\/>/g, '')}</g>`);
}

// ---------- porcelain landscape (blue ink) ----------
function mountains() {
  let b = '';
  const ridge = (base, amp, step, op) => {
    let d = `M0 ${base}`;
    for (let x = 0; x <= 600; x += step) d += ` L${x} ${f(base - amp * (0.4 + rnd() * 0.6) * Math.abs(Math.sin(x / 90 + base)))}`;
    return `<path d="${d} L600 200 L0 200 Z" fill="${K}" fill-opacity="${op}"/>`;
  };
  b += ridge(150, 110, 30, 0.45) + ridge(175, 70, 24, 0.75) + ridge(200, 40, 20, 1);
  return svg('0 0 600 200', b);
}
function willow() {
  let b = `<path d="M60 300 C 70 220 50 160 80 110 C 100 80 140 70 170 80" stroke="${K}" stroke-width="10" fill="none"/>`;
  for (let i = 0; i < 26; i++) {
    const sx = 70 + i * 6, sy = 90 + Math.sin(i / 4) * 16;
    b += `<path d="M${sx} ${sy} Q ${sx + 10} ${sy + 80} ${sx - 4 + (i % 3) * 6} ${sy + 150 + (i % 5) * 12}" stroke="${K}" stroke-width="1.4" fill="none"/>`;
  }
  return svg('0 0 260 320', b);
}
const bridge = svg('0 0 300 110', `<path d="M0 100 Q 150 0 300 100 L300 110 Q 150 24 0 110 Z" fill="${K}"/>
  <path d="M20 92 Q 150 -4 280 92" fill="none" stroke="${K}" stroke-width="3"/>${Array.from({ length: 11 }, (_, i) => { const x = 30 + i * 24, y = 92 - Math.sin((Math.PI * (x - 20)) / 260) * 70; return `<path d="M${f(x)} ${f(y)} V${f(y + 14)}" stroke="${K}" stroke-width="3"/>`; }).join('')}`);
const pavilion = svg('0 0 200 160', `<path d="M10 70 Q 100 20 190 70 L170 70 Q 100 44 30 70 Z" fill="${K}"/><path d="M100 10 V30" stroke="${K}" stroke-width="3"/>
  <path d="M40 70 V140 M160 70 V140 M80 70 V140 M120 70 V140" stroke="${K}" stroke-width="6"/><path d="M20 140 H180 V152 H20 Z" fill="${K}"/><path d="M30 80 H170" stroke="${K}" stroke-width="3"/>`);
const birds = svg('0 0 200 60', [[20, 30], [60, 18], [100, 34], [140, 14], [175, 26]].map(([x, y], i) => `<path d="M${x - 10} ${y} Q ${x - 5} ${y - 6} ${x} ${y} Q ${x + 5} ${y - 6} ${x + 10} ${y}" stroke="${K}" stroke-width="${2 - i * 0.15}" fill="none"/>`).join(''));

// ---------- andalus courtyard ----------
function arcade() {
  let b = `<rect x="0" y="0" width="600" height="40" fill="${K}"/>`;
  for (let i = 0; i < 6; i++) {
    const x = 10 + i * 98;
    b += `<path d="M${x} 300 V110 C ${x} 60 ${x + 20} 44 ${x + 40} 44 C ${x + 60} 44 ${x + 80} 60 ${x + 80} 110 V300 H${x + 98} V40 H${x - 10} V300 Z" fill="${K}" fill-rule="evenodd"/>`;
  }
  b += `<rect x="0" y="290" width="600" height="10" fill="${K}"/>`;
  return svg('0 0 600 300', b);
}
const cypress = svg('0 0 60 240', `<path d="M30 240 C 6 180 4 90 30 0 C 56 90 54 180 30 240 Z" fill="${K}"/>`);
const fountain = svg('0 0 200 140', `<path d="M20 120 H180 L170 140 H30 Z M60 120 Q 100 96 140 120 Z M96 120 V60 H104 V120 Z M70 62 Q 100 50 130 62 Q 100 70 70 62 Z" fill="${K}"/>
  <path d="M100 58 Q 80 20 60 60 M100 58 Q 120 20 140 60 M100 56 V24" stroke="${K}" stroke-width="2" fill="none" stroke-dasharray="3 4"/>`);

// ---------- deco rooftop ----------
function decoSkyline() {
  let b = '';
  const tower = (x, w, h, spire) => {
    let o = `<rect x="${x}" y="${300 - h}" width="${w}" height="${h}" fill="${K}"/>`;
    o += `<rect x="${x + w * 0.15}" y="${300 - h - 24}" width="${w * 0.7}" height="24" fill="${K}"/><rect x="${x + w * 0.3}" y="${300 - h - 44}" width="${w * 0.4}" height="20" fill="${K}"/>`;
    if (spire) o += `<path d="M${x + w * 0.35} ${300 - h - 44} L${x + w / 2} ${300 - h - 44 - spire} L${x + w * 0.65} ${300 - h - 44} Z" fill="${K}"/>`;
    for (let yy = 300 - h + 14; yy < 296; yy += 16) for (let xx = x + 6; xx < x + w - 6; xx += 10) o += `<rect x="${xx}" y="${yy}" width="4" height="8" fill="#000" fill-opacity="0"/>`;
    return o;
  };
  b += tower(10, 60, 150, 0) + tower(80, 46, 200, 70) + tower(136, 70, 120, 0) + tower(216, 56, 240, 110) + tower(282, 80, 160, 30) + tower(372, 50, 210, 60) + tower(430, 70, 130, 0) + tower(510, 60, 180, 50);
  return svg('0 0 580 300', b);
}
function fireworks() {
  let b = '';
  for (const [cx, cy, r] of [[80, 70, 50], [230, 50, 36], [330, 90, 44]]) {
    for (let i = 0; i < 18; i++) { const a = (Math.PI * 2 * i) / 18; b += `<path d="M${f(cx + Math.cos(a) * r * 0.25)} ${f(cy + Math.sin(a) * r * 0.25)} L${f(cx + Math.cos(a) * r)} ${f(cy + Math.sin(a) * r)}" stroke="${K}" stroke-width="2" stroke-linecap="round"/>`; b += `<circle cx="${f(cx + Math.cos(a) * (r + 5))}" cy="${f(cy + Math.sin(a) * (r + 5))}" r="1.8" fill="${K}"/>`; }
  }
  return svg('0 0 400 150', b);
}
function champagne() {
  let b = '';
  const glass = (x, y) => `<path d="M${x - 22} ${y} Q ${x} ${y + 18} ${x + 22} ${y} Z M${x - 2} ${y + 9} V${y + 34} H${x - 10} V${y + 38} H${x + 10} V${y + 34} H${x + 2} V${y + 9} Z" fill="${K}"/>`;
  const rows = [[1, 20], [2, 58], [3, 96], [4, 134]];
  for (const [n, y] of rows) for (let i = 0; i < n; i++) b += glass(150 - (n - 1) * 25 + i * 50, y);
  for (let i = 0; i < 9; i++) b += `<circle cx="${f(130 + rnd() * 40)}" cy="${f(10 + rnd() * 120)}" r="${f(1 + rnd() * 2)}" fill="${K}"/>`;
  return svg('0 0 300 180', b);
}

// ---------- atelier studio ----------
const dressForm = svg('0 0 160 400', `<path d="M80 10 C 90 10 96 18 96 26 L94 40 C 118 46 130 60 128 80 C 126 110 112 130 108 150 C 120 180 134 200 132 230 C 130 254 112 266 80 268 C 48 266 30 254 28 230 C 26 200 40 180 52 150 C 48 130 34 110 32 80 C 30 60 42 46 66 40 L64 26 C 64 18 70 10 80 10 Z" fill="${K}"/>
  <rect x="76" y="268" width="8" height="100" fill="${K}"/><path d="M40 396 L80 360 L120 396 Z M76 360 H84 V396 H76 Z" fill="${K}"/>`);
function rack() {
  let b = `<path d="M10 40 H290 M20 40 V300 M280 40 V300 M10 300 H40 M260 300 H290" stroke="${K}" stroke-width="6" fill="none"/>`;
  for (let i = 0; i < 6; i++) {
    const x = 50 + i * 40;
    b += `<path d="M${x} 40 q -6 -10 0 -16 q 6 -4 6 4" stroke="${K}" stroke-width="2" fill="none"/><path d="M${x - 20} 60 L${x} 46 L${x + 20} 60 L${x + 26} ${200 + (i % 3) * 30} L${x - 26} ${200 + (i % 3) * 30} Z" fill="${K}"/>`;
  }
  return svg('0 0 300 310', b);
}

// ---------- navy-bloom garden ----------
function trellisArch() {
  let b = `<path d="M30 400 V160 A120 120 0 0 1 270 160 V400" fill="none" stroke="${K}" stroke-width="10"/><path d="M50 400 V164 A100 100 0 0 1 250 164 V400" fill="none" stroke="${K}" stroke-width="4"/>`;
  for (let y = 180; y < 400; y += 30) b += `<path d="M30 ${y} L50 ${y + 15} M270 ${y} L250 ${y + 15}" stroke="${K}" stroke-width="3"/>`;
  return svg('0 0 300 400', b);
}

// ---------- midnight observatory ----------
const observatory = svg('0 0 600 220', `<path d="M0 220 V170 Q 150 120 300 160 Q 450 120 600 170 V220 Z" fill="${K}"/>
  <path d="M360 150 V100 H470 V150 Z M350 100 A65 60 0 0 1 480 100 Z" fill="${K}"/><path d="M405 44 L430 44 L430 100 L405 100 Z" fill="#000" fill-opacity="0"/>
  <path d="M418 70 L470 20" stroke="${K}" stroke-width="10" stroke-linecap="round"/>`);
function constellation() {
  const pts = [[30, 120], [80, 80], [130, 100], [170, 50], [220, 70], [260, 30], [300, 90], [340, 60]];
  let b = `<path d="M${pts.map((p) => p.join(' ')).join(' L')}" stroke="${K}" stroke-width="1.2" fill="none" stroke-dasharray="4 5"/>`;
  for (const [x, y] of pts) b += `<path d="M${x} ${y - 6} L${x + 2} ${y - 2} L${x + 6} ${y} L${x + 2} ${y + 2} L${x} ${y + 6} L${x - 2} ${y + 2} L${x - 6} ${y} L${x - 2} ${y - 2} Z" fill="${K}"/>`;
  return svg('0 0 370 150', b);
}
const comet = svg('0 0 200 60', `<path d="M10 40 Q 100 34 180 20 Q 188 24 180 30 Q 100 42 10 44 Z" fill="${K}" fill-opacity=".5"/><circle cx="182" cy="25" r="8" fill="${K}"/>`);

const files = {
  'caravan.svg': caravan, 'tent.svg': tent, 'tent-door.svg': tentDoor,
  'chandelier.svg': chandelier(), 'ballroom-window.svg': ballWindow(), 'classic-column.svg': classicColumn(),
  'butterfly.svg': butterfly(), 'urn.svg': urn(), 'tree-line.svg': treeLine(),
  'bouquet.svg': bouquet(),
  'ink-mountains.svg': mountains(), 'willow.svg': willow(), 'ink-bridge.svg': bridge, 'pavilion.svg': pavilion, 'birds.svg': birds,
  'arcade.svg': arcade(), 'cypress.svg': cypress, 'fountain.svg': fountain,
  'deco-skyline.svg': decoSkyline(), 'fireworks.svg': fireworks(), 'champagne.svg': champagne(),
  'dress-form.svg': dressForm, 'garment-rack.svg': rack(),
  'trellis-arch.svg': trellisArch(),
  'observatory.svg': observatory, 'constellation.svg': constellation(), 'comet.svg': comet,
};
for (const [n, s] of Object.entries(files)) writeFileSync(new URL(n, OUT), s.replace(/\n\s*/g, ' '));
console.log('wrote', Object.keys(files).length, 'files');
