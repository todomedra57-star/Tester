// Original artwork for the Deco, Atelier and Royal templates → preview/library/.
// Run: node tools/make-art-more.mjs
import { writeFileSync, mkdirSync } from 'node:fs';

const OUT = new URL('../preview/library/', import.meta.url);
mkdirSync(OUT, { recursive: true });
const GOLD = '#CDAA62', GOLD_D = '#8A6A2C', GOLD_L = '#F3DFA6';
const f = (n) => Math.round(n * 100) / 100;
const svg = (vb, body, defs = '') => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${vb}">${defs ? `<defs>${defs}</defs>` : ''}${body}</svg>`;
const metal = (id, w = 240, h = 260) => `<linearGradient id="${id}" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="${w}" y2="${h}"><stop offset="0" stop-color="${GOLD_D}"/><stop offset=".35" stop-color="${GOLD_L}"/><stop offset=".6" stop-color="${GOLD}"/><stop offset="1" stop-color="${GOLD_D}"/></linearGradient>`;

// ================= DECO =================
// fan ornament (half sunburst with stepped arcs)
function decoFan() {
  let b = `<g fill="none" stroke="url(#m)" stroke-width="1.6">`;
  for (let r = 30; r <= 110; r += 20) b += `<path d="M${120 - r} 120 A${r} ${r} 0 0 1 ${120 + r} 120"/>`;
  for (let i = 0; i <= 12; i++) {
    const a = Math.PI * (i / 12);
    b += `<path d="M${f(120 - Math.cos(a) * 30)} ${f(120 - Math.sin(a) * 30)} L${f(120 - Math.cos(a) * 110)} ${f(120 - Math.sin(a) * 110)}"/>`;
  }
  b += `</g><path d="M90 120 A30 30 0 0 1 150 120 Z" fill="url(#m)"/><path d="M4 120 H236" stroke="url(#m)" stroke-width="2"/>`;
  b += `<path d="M120 4 L126 14 L120 24 L114 14 Z" fill="url(#m)"/>`;
  return svg('0 0 240 124', b, metal('m', 240, 124));
}
// repeating scale/fan pattern tile
function decoTile() {
  let b = `<g fill="none" stroke="${GOLD}" stroke-width="1">`;
  for (const [x, y] of [[0, 40], [80, 40], [40, 80], [40, 0], [0, 120], [80, 120]]) {
    for (let r = 10; r <= 40; r += 10) b += `<path d="M${x - r} ${y} A${r} ${r} 0 0 1 ${x + r} ${y}"/>`;
  }
  return svg('0 0 80 80', b + '</g>');
}
// stepped corner
function decoCorner() {
  const steps = (o) => `M${o} 120 V${40 + o} H${20 + o} V${20 + o} H${40 + o} V${o} H120`;
  let b = `<g fill="none" stroke="url(#m)" stroke-width="2"><path d="${steps(4)}"/><path d="${steps(14)}" stroke-width="1"/></g>`;
  b += `<path d="M20 20 L34 20 L20 34 Z" fill="url(#m)"/><circle cx="60" cy="60" r="0"/>`;
  for (let i = 0; i < 5; i++) b += `<path d="M${30 + i * 6} ${52 + i * 6} L${52 + i * 6} ${30 + i * 6}" stroke="url(#m)" stroke-width="1"/>`;
  return svg('0 0 120 120', b, metal('m', 120, 120));
}

// ================= ATELIER =================
// marble texture: thin grey veins plus faint clouding, transparent
const marble = svg('0 0 600 600', `<rect width="600" height="600" filter="url(#cloud)"/><rect width="600" height="600" filter="url(#v)"/><rect width="600" height="600" filter="url(#v2)"/>`,
  `<filter id="v" x="0" y="0" width="100%" height="100%">
<feTurbulence type="fractalNoise" baseFrequency="0.0035 0.009" numOctaves="6" seed="21"/>
<feColorMatrix type="matrix" values="0 0 0 0 .32  0 0 0 0 .30  0 0 0 0 .27  1 0 0 0 0"/>
<feComponentTransfer><feFuncA type="table" tableValues="0 0 0 0 0 .1 .75 .1 0 0 0 0 0"/></feComponentTransfer></filter>
<filter id="v2" x="0" y="0" width="100%" height="100%">
<feTurbulence type="fractalNoise" baseFrequency="0.006 0.016" numOctaves="5" seed="5"/>
<feColorMatrix type="matrix" values="0 0 0 0 .55  0 0 0 0 .5  0 0 0 0 .42  0 1 0 0 0"/>
<feComponentTransfer><feFuncA type="table" tableValues="0 0 0 0 0 .05 .45 .05 0 0 0 0 0"/></feComponentTransfer></filter>
<filter id="cloud" x="0" y="0" width="100%" height="100%">
<feTurbulence type="fractalNoise" baseFrequency="0.003" numOctaves="3" seed="8"/>
<feColorMatrix type="matrix" values="0 0 0 0 .5  0 0 0 0 .48  0 0 0 0 .44  0 0 0 .22 -.05"/></filter>`);
// thin gold line flourish
const flourish = svg('0 0 260 40', `<g fill="none" stroke="url(#m)" stroke-width="1.3" stroke-linecap="round">
<path d="M10 20 H96"/><path d="M164 20 H250"/>
<path d="M96 20 C110 20 112 6 124 8 C136 10 128 26 118 22 C110 18 120 10 130 14"/>
<path d="M164 20 C150 20 148 34 136 32 C124 30 132 14 142 18 C150 22 140 30 130 26"/></g>
<circle cx="130" cy="20" r="2.5" fill="url(#m)"/>`, metal('m', 260, 40));

// ================= ROYAL =================
// damask tile: mirrored ornamental motif on an offset grid
function damaskMotif(cx, cy, s) {
  const half = `M0 ${-46 * s} C ${14 * s} ${-30 * s} ${16 * s} ${-12 * s} ${4 * s} 0 C ${22 * s} ${-4 * s} ${34 * s} ${-22 * s} ${26 * s} ${-36 * s} C ${44 * s} ${-20 * s} ${38 * s} ${6 * s} ${12 * s} ${10 * s} C ${24 * s} ${18 * s} ${30 * s} ${34 * s} ${16 * s} ${46 * s} C ${10 * s} ${34 * s} ${6 * s} ${24 * s} 0 ${22 * s}`;
  return `<g transform="translate(${cx} ${cy})"><path d="${half}"/><path d="${half}" transform="scale(-1 1)"/>
<path d="M0 ${-30 * s} C ${6 * s} ${-20 * s} ${6 * s} ${-10 * s} 0 ${-4 * s} C ${-6 * s} ${-10 * s} ${-6 * s} ${-20 * s} 0 ${-30 * s}Z"/>
<circle cy="${32 * s}" r="${3 * s}"/></g>`;
}
function damaskTile() {
  let b = `<g fill="${GOLD}" fill-opacity=".9">`;
  for (const [x, y] of [[70, 90], [0, 0], [140, 0], [0, 180], [140, 180]]) b += damaskMotif(x, y, 1);
  for (const [x, y] of [[0, 90], [140, 90], [70, 0], [70, 180]]) b += damaskMotif(x, y, 0.45);
  return svg('0 0 140 180', b + '</g>');
}
// crest: crown, shield, laurels, ribbon
function crest() {
  let leaves = '';
  for (const side of [1, -1]) {
    for (let i = 0; i < 9; i++) {
      const t = i / 8, a = Math.PI * (0.62 + t * 0.62);
      const x = 120 + side * Math.cos(a) * -92, y = 150 - Math.sin(a) * -10 + t * -100 + 60;
      const rot = side * (40 - t * 70);
      leaves += `<ellipse cx="${f(x)}" cy="${f(y)}" rx="6" ry="15" transform="rotate(${f(rot)} ${f(x)} ${f(y)})" fill="url(#m)"/>`;
    }
    leaves += `<path d="M${120 + side * 30} 226 Q ${120 + side * 98} 190 ${120 + side * 86} 96" fill="none" stroke="url(#m)" stroke-width="2.2"/>`;
  }
  const shield = 'M78 92 H162 V150 C162 186 140 204 120 214 C100 204 78 186 78 150 Z';
  const crown = 'M80 74 L86 40 L102 60 L120 30 L138 60 L154 40 L160 74 Z';
  return svg('0 0 240 260', `${leaves}
<path d="${crown}" fill="url(#m)" stroke="${GOLD_D}" stroke-width="1.2"/>
<rect x="78" y="74" width="84" height="10" rx="2" fill="url(#m)"/>
${[86, 102, 120, 138, 154].map((x, i) => `<circle cx="${x}" cy="${[40, 60, 30, 60, 40][i] - 4}" r="4" fill="${GOLD_L}"/>`).join('')}
<path d="${shield}" fill="#5A1420" fill-opacity=".35" stroke="url(#m)" stroke-width="4"/>
<path d="M88 100 H152 V148 C152 176 136 192 120 200 C104 192 88 176 88 148 Z" fill="none" stroke="url(#m)" stroke-width="1.2"/>
<path d="M120 112 L127 134 L150 134 L131 147 L138 170 L120 156 L102 170 L109 147 L90 134 L113 134 Z" fill="url(#m)"/>
<path d="M60 222 Q120 246 180 222 L188 238 Q120 262 52 238 Z" fill="url(#m)"/>
<path d="M60 222 L44 226 L52 238 M180 222 L196 226 L188 238" fill="none" stroke="url(#m)" stroke-width="2"/>`, metal('m'));
}
// filigree corner: scrolls anchored top-left
function filigree() {
  const g = `<g fill="none" stroke="url(#m)" stroke-width="1.8" stroke-linecap="round">
<path d="M6 120 V30 Q6 6 30 6 H120"/>
<path d="M18 110 V40 Q18 18 40 18 H110" stroke-width="1"/>
<path d="M30 70 C30 46 46 30 70 30 C86 30 92 46 80 54 C70 60 60 50 68 44"/>
<path d="M30 70 C30 86 46 92 54 80 C60 70 50 60 44 68"/>
<path d="M70 30 C96 30 104 18 112 10"/><path d="M30 70 C30 96 18 104 10 112"/></g>
<circle cx="30" cy="30" r="4" fill="url(#m)"/>`;
  return svg('0 0 124 124', g, metal('m', 124, 124));
}

const files = {
  'deco-fan.svg': decoFan(), 'deco-tile.svg': decoTile(), 'deco-corner.svg': decoCorner(),
  'marble.svg': marble, 'gold-flourish.svg': flourish,
  'damask-tile.svg': damaskTile(), 'royal-crest.svg': crest(), 'filigree-corner.svg': filigree(),
};
for (const [n, s] of Object.entries(files)) writeFileSync(new URL(n, OUT), s.replace(/\n\s*/g, ' '));
console.log('wrote', Object.keys(files).join(', '));
