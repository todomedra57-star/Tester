// Original geometric artwork for the Andalus template → preview/library/.
// Run: node tools/make-art-andalus.mjs
// All art is gold line work on transparent backgrounds, so it suits every palette.
import { writeFileSync, mkdirSync } from 'node:fs';

const OUT = new URL('../preview/library/', import.meta.url);
mkdirSync(OUT, { recursive: true });
const GOLD = '#C9A55C', GOLD_D = '#8C6B2E', GOLD_L = '#F1DCA4';
const f = (n) => Math.round(n * 100) / 100;

// 8-point star polygon points
function star(cx, cy, r, inner = 0.62, rot = 0, points = 8) {
  const out = [];
  for (let i = 0; i < points * 2; i++) {
    const a = (Math.PI / points) * i - Math.PI / 2 + rot;
    const rr = i % 2 ? r * inner : r;
    out.push(`${f(cx + Math.cos(a) * rr)},${f(cy + Math.sin(a) * rr)}`);
  }
  return out.join(' ');
}
const svg = (vb, body, defs = '') => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${vb}">${defs ? `<defs>${defs}</defs>` : ''}${body}</svg>`;

// 1 · zellige tile: star-and-cross, repeatable 120×120
function zellige() {
  const s = 120, r = 30;
  let b = `<g fill="none" stroke="${GOLD}" stroke-width="1.3" stroke-linejoin="round">`;
  for (const [x, y] of [[0, 0], [s, 0], [0, s], [s, s], [s / 2, s / 2]]) {
    b += `<polygon points="${star(x, y, r)}"/><polygon points="${star(x, y, r * 0.55, 0.62, Math.PI / 8)}"/>`;
  }
  // crosses joining the stars
  for (const [x, y] of [[s / 2, 0], [0, s / 2], [s, s / 2], [s / 2, s]]) {
    const a = 14, c = 6;
    b += `<path d="M${x - a} ${y - c} H${x - c} V${y - a} H${x + c} V${y - c} H${x + a} V${y + c} H${x + c} V${y + a} H${x - c} V${y + c} H${x - a} Z"/>`;
  }
  return svg(`0 0 ${s} ${s}`, b + '</g>');
}

// 2 · mashrabiya: lattice window with a pointed arch top
function mashrabiya() {
  const W = 400, H = 520;
  const arch = `M20 ${H} V200 C20 90 140 30 200 10 C260 30 380 90 380 200 V${H} Z`;
  const defs = `<pattern id="lat" width="40" height="40" patternUnits="userSpaceOnUse">
<g fill="none" stroke="${GOLD}" stroke-width="1.2"><polygon points="${star(20, 20, 13)}"/>
<path d="M0 20 H7 M33 20 H40 M20 0 V7 M20 33 V40"/><circle cx="0" cy="0" r="4"/><circle cx="40" cy="0" r="4"/><circle cx="0" cy="40" r="4"/><circle cx="40" cy="40" r="4"/></g></pattern>
<clipPath id="ar"><path d="${arch}"/></clipPath>`;
  return svg(`0 0 ${W} ${H}`, `<rect width="${W}" height="${H}" fill="url(#lat)" clip-path="url(#ar)"/>
<path d="${arch}" fill="none" stroke="${GOLD}" stroke-width="3"/>
<path d="M36 ${H} V204 C36 104 148 48 200 30 C252 48 364 104 364 204 V${H}" fill="none" stroke="${GOLD}" stroke-width="1.2"/>`, defs);
}

// 3 · lantern on a chain
function lantern() {
  let chain = '';
  for (let y = 4; y < 92; y += 11) chain += `<ellipse cx="50" cy="${y}" rx="${y % 2 ? 2.4 : 3.4}" ry="5" fill="none" stroke="${GOLD_D}" stroke-width="1.6"/>`;
  const body = 'M30 132 L22 160 L28 214 L50 232 L72 214 L78 160 L70 132 Z';
  let cuts = '';
  for (const [x, y] of [[50, 172], [36, 168], [64, 168], [50, 200], [38, 196], [62, 196]]) cuts += `<polygon points="${star(x, y, 6)}" fill="${GOLD_L}" opacity=".95"/>`;
  const defs = `<radialGradient id="glow" cx=".5" cy=".55" r=".55"><stop offset="0" stop-color="#FFE7A8" stop-opacity=".95"/><stop offset=".6" stop-color="#F2B95A" stop-opacity=".5"/><stop offset="1" stop-color="#F2B95A" stop-opacity="0"/></radialGradient>
<linearGradient id="metal" x1="0" x2="1"><stop offset="0" stop-color="${GOLD_D}"/><stop offset=".45" stop-color="${GOLD_L}"/><stop offset="1" stop-color="${GOLD_D}"/></linearGradient>`;
  return svg('0 0 100 270', `${chain}
<circle cx="50" cy="178" r="49" fill="url(#glow)"/>
<path d="M44 96 H56 L60 108 H40 Z" fill="url(#metal)"/>
<path d="M28 132 C30 112 42 106 50 104 C58 106 70 112 72 132 Z" fill="url(#metal)"/>
<path d="${body}" fill="#3A2A12" fill-opacity=".55" stroke="url(#metal)" stroke-width="3" stroke-linejoin="round"/>
${cuts}
<path d="M22 160 H78 M28 214 H72 M50 132 V232" stroke="${GOLD}" stroke-width="1.3" opacity=".8"/>
<path d="M44 232 L50 252 L56 232 Z" fill="url(#metal)"/><circle cx="50" cy="257" r="3.5" fill="${GOLD}"/>`, defs);
}

// 4 · corner rosette: a compact, complete ornament placed on card corners
function corner() {
  let b = `<g fill="none" stroke="${GOLD}" stroke-linejoin="round">`;
  b += `<circle cx="60" cy="60" r="56" stroke-width="1.6"/><circle cx="60" cy="60" r="50" stroke-width="0.8"/>`;
  b += `<polygon points="${star(60, 60, 46, 0.66)}" stroke-width="1.8"/><polygon points="${star(60, 60, 46, 0.66, Math.PI / 8)}" stroke-width="1.2"/></g>`;
  b += `<polygon points="${star(60, 60, 20, 0.6)}" fill="${GOLD}"/><circle cx="60" cy="60" r="4" fill="${GOLD_L}"/>`;
  return svg('0 0 120 120', b);
}

// 5 · medallion: a 16-point rosette
function medallion() {
  let b = `<g fill="none" stroke="${GOLD}" stroke-linejoin="round">`;
  b += `<circle cx="150" cy="150" r="146" stroke-width="1.2"/><circle cx="150" cy="150" r="138" stroke-width="0.7" stroke-dasharray="2 5"/>`;
  b += `<polygon points="${star(150, 150, 130, 0.72)}" stroke-width="1.6"/><polygon points="${star(150, 150, 130, 0.72, Math.PI / 8)}" stroke-width="1.6"/>`;
  b += `<polygon points="${star(150, 150, 84, 0.62)}" stroke-width="1.2"/><circle cx="150" cy="150" r="52" stroke-width="1"/>`;
  for (let i = 0; i < 16; i++) {
    const a = (Math.PI / 8) * i, x = 150 + Math.cos(a) * 112, y = 150 + Math.sin(a) * 112;
    b += `<circle cx="${f(x)}" cy="${f(y)}" r="3" fill="${GOLD}" stroke="none"/>`;
  }
  return svg('0 0 300 300', b + '</g>');
}

// 6 · divider
const divider = svg('0 0 260 30', `<g fill="none" stroke="${GOLD}" stroke-width="1.2">
<path d="M8 15 H100 M160 15 H252"/><polygon points="${star(130, 15, 13)}"/><polygon points="${star(130, 15, 7, 0.62, Math.PI / 8)}"/></g>
<g fill="${GOLD}"><path d="M104 15 l6 -4 l6 4 l-6 4z"/><path d="M144 15 l6 -4 l6 4 l-6 4z"/><circle cx="8" cy="15" r="2"/><circle cx="252" cy="15" r="2"/></g>`);

const files = {
  'zellige-tile.svg': zellige(),
  'mashrabiya.svg': mashrabiya(),
  'lantern.svg': lantern(),
  'geo-corner.svg': corner(),
  'rosette.svg': medallion(),
  'star-divider.svg': divider,
};
for (const [n, s] of Object.entries(files)) writeFileSync(new URL(n, OUT), s.replace(/\n\s*/g, ' '));
console.log('wrote', Object.keys(files).join(', '));
