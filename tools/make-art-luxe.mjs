// Original artwork for Porcelain, Glass Garden, Lace and Desert Bloom → preview/library/.
// Run: node tools/make-art-luxe.mjs
// Most pieces are single-colour silhouettes meant to be used as CSS masks, so the
// template colours them with its palette tokens (one design, every colourway).
import { writeFileSync, mkdirSync } from 'node:fs';

const OUT = new URL('../preview/library/', import.meta.url);
mkdirSync(OUT, { recursive: true });
const f = (n) => Math.round(n * 100) / 100;
const svg = (vb, body, defs = '') => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${vb}">${defs ? `<defs>${defs}</defs>` : ''}${body}</svg>`;
let seed = 3;
const rnd = () => ((seed = (seed * 16807) % 2147483647) - 1) / 2147483646;
const K = '#000';

// ---------- shared drawing parts ----------
const petal = (len, w) => `M0 0 C ${f(w)} ${f(-len * 0.3)} ${f(w * 0.8)} ${f(-len * 0.9)} 0 ${f(-len)} C ${f(-w * 0.8)} ${f(-len * 0.9)} ${f(-w)} ${f(-len * 0.3)} 0 0Z`;
function flower(cx, cy, r, n = 8, fill = true) {
  let o = `<g transform="translate(${f(cx)} ${f(cy)})">`;
  for (let i = 0; i < n; i++) o += `<path d="${petal(r, r * 0.42)}" transform="rotate(${f((360 / n) * i)})" ${fill ? `fill="${K}" fill-opacity=".85"` : `fill="none" stroke="${K}" stroke-width="1.4"`}/>`;
  for (let i = 0; i < n; i++) o += `<path d="${petal(r * 0.6, r * 0.28)}" transform="rotate(${f((360 / n) * i + 180 / n)})" fill="none" stroke="${K}" stroke-width="1.1"/>`;
  return o + `<circle r="${f(r * 0.18)}" fill="${K}"/></g>`;
}
function leaf(x, y, len, ang, fill = true) {
  const w = len * 0.34;
  return `<g transform="translate(${f(x)} ${f(y)}) rotate(${f(ang)})"><path d="M0 0 Q ${f(w)} ${f(-len * 0.5)} 0 ${f(-len)} Q ${f(-w)} ${f(-len * 0.5)} 0 0Z" ${fill ? `fill="${K}"` : `fill="none" stroke="${K}" stroke-width="1.3"`}/>${fill ? '' : `<path d="M0 0 V${f(-len * 0.92)}" stroke="${K}" stroke-width="1"/>`}</g>`;
}

// ================= PORCELAIN (masks) =================
function porcelainTile() {
  let b = '';
  b += `<g fill="none" stroke="${K}" stroke-width="1.6" stroke-linecap="round">
<path d="M0 80 C 30 50 50 110 80 80 S 130 50 160 80"/><path d="M80 0 C 110 30 50 50 80 80 S 110 130 80 160"/></g>`;
  for (const [x, y, a] of [[30, 66, -40], [46, 98, 140], [114, 62, 40], [130, 96, 220], [66, 30, -130], [96, 46, 50], [62, 118, -50], [98, 134, 130]]) b += leaf(x, y, 18, a, false);
  b += flower(80, 80, 22, 8, false);
  for (const [x, y] of [[0, 0], [160, 0], [0, 160], [160, 160]]) b += flower(x, y, 12, 6, false);
  return svg('0 0 160 160', b);
}
function porcelainPlate() {
  let b = `<g fill="none" stroke="${K}">`;
  b += `<circle cx="200" cy="200" r="196" stroke-width="3"/><circle cx="200" cy="200" r="186" stroke-width="1.2"/>`;
  b += `<circle cx="200" cy="200" r="140" stroke-width="1.2"/><circle cx="200" cy="200" r="132" stroke-width="3"/></g>`;
  // band of flowers and leaves between r=140 and r=186
  for (let i = 0; i < 12; i++) {
    const a = (Math.PI * 2 * i) / 12, x = 200 + Math.cos(a) * 163, y = 200 + Math.sin(a) * 163;
    b += flower(x, y, 13, 6, true);
    const a2 = a + Math.PI / 12, x2 = 200 + Math.cos(a2) * 163, y2 = 200 + Math.sin(a2) * 163;
    b += leaf(x2, y2, 16, (a2 * 180) / Math.PI, true) + leaf(x2, y2, 16, (a2 * 180) / Math.PI + 180, true);
  }
  // fine scallop ring inside
  let sc = '';
  for (let i = 0; i < 48; i++) {
    const a = (Math.PI * 2 * i) / 48, x = 200 + Math.cos(a) * 126, y = 200 + Math.sin(a) * 126;
    sc += `<circle cx="${f(x)}" cy="${f(y)}" r="2.2" fill="${K}"/>`;
  }
  return svg('0 0 400 400', b + sc);
}
function porcelainCorner() {
  let b = `<path d="M8 150 C 8 70 70 8 150 8" fill="none" stroke="${K}" stroke-width="2"/><path d="M30 120 C 40 70 70 40 120 30" fill="none" stroke="${K}" stroke-width="1.3"/>`;
  for (const [x, y, a] of [[24, 96, -20], [40, 62, 20], [66, 38, 60], [98, 22, 100], [16, 130, -60], [130, 14, 140]]) b += leaf(x, y, 20, a, true);
  b += flower(46, 46, 20, 8, true) + flower(110, 60, 10, 6, false) + flower(60, 110, 10, 6, false);
  return svg('0 0 160 160', b);
}

// ================= GLASS GARDEN (masks) =================
function glasshouse() {
  const W = 400, H = 520;
  let b = `<g fill="none" stroke="${K}" stroke-linecap="round">`;
  const arch = (o) => `M${20 + o} ${H} V${210} C ${20 + o} ${90 + o} ${110 + o * 0.5} ${20 + o} 200 ${20 + o} C ${290 - o * 0.5} ${20 + o} ${380 - o} ${90 + o} ${380 - o} 210 V${H}`;
  b += `<path d="${arch(0)}" stroke-width="5"/><path d="${arch(14)}" stroke-width="2"/>`;
  for (let x = 70; x < 340; x += 52) b += `<path d="M${x} ${H} V${x < 200 ? 210 - (200 - x) * 0.35 : 210 - (x - 200) * 0.35}" stroke-width="2"/>`;
  for (let y = 260; y < H; y += 70) b += `<path d="M34 ${y} H366" stroke-width="1.6"/>`;
  // fan of the arch top
  for (let i = 1; i < 8; i++) {
    const a = Math.PI + (Math.PI * i) / 8, x = 200 + Math.cos(a) * 170, y = 210 + Math.sin(a) * 175;
    b += `<path d="M200 210 L${f(x)} ${f(y)}" stroke-width="1.6"/>`;
  }
  b += `<path d="M120 210 A80 80 0 0 1 280 210" stroke-width="2"/><circle cx="200" cy="210" r="16" stroke-width="2"/>`;
  b += `<path d="M200 20 V2 M192 10 H208" stroke-width="2.5"/></g>`;
  return svg(`0 0 ${W} ${H}`, b);
}
function fern() {
  let b = '';
  const frond = (x, y, len, ang) => {
    let o = `<g transform="translate(${x} ${y}) rotate(${ang})"><path d="M0 0 Q 8 ${-len * 0.5} 0 ${-len}" fill="none" stroke="${K}" stroke-width="2.2"/>`;
    for (let t = 0.08; t < 0.95; t += 0.065) {
      const l = (1 - t) * 34 + 6, yy = -len * t;
      o += leaf(0, yy, l, 62, true) + leaf(0, yy, l, -62, true);
    }
    return o + '</g>';
  };
  b += frond(110, 300, 260, -18) + frond(120, 300, 200, 22) + frond(100, 300, 180, -50);
  // monstera-ish big leaf
  b += `<g transform="translate(96 300) rotate(-24)"><path d="M0 0 C -70 -40 -80 -150 0 -190 C 80 -150 70 -40 0 0Z" fill="${K}"/>
${[-150, -115, -80, -45].map((y) => `<path d="M0 ${y} L-60 ${y + 30} L-58 ${y + 40} L0 ${y + 14}Z M0 ${y} L60 ${y + 30} L58 ${y + 40} L0 ${y + 14}Z" fill="#fff"/>`).join('')}
<path d="M0 0 V-185" stroke="#fff" stroke-width="3"/></g>`;
  return svg('-10 0 260 310', b, '').replace(/fill="#fff"/g, 'fill="#000" fill-opacity="0"');
}
function ivy() {
  let b = `<path d="M60 0 C 20 80 100 160 60 240 S 20 400 60 480" fill="none" stroke="${K}" stroke-width="2"/>`;
  for (let t = 0; t < 1; t += 0.07) {
    const y = t * 480, x = 60 + Math.sin(t * Math.PI * 4) * 30;
    const side = Math.round(t * 14) % 2 ? 1 : -1;
    b += `<g transform="translate(${f(x)} ${f(y)}) rotate(${side * 70})"><path d="M0 0 C 10 -6 18 -16 14 -26 C 8 -22 4 -30 0 -36 C -4 -30 -8 -22 -14 -26 C -18 -16 -10 -6 0 0Z" fill="${K}"/></g>`;
  }
  return svg('0 0 120 480', b);
}

// ================= LACE (masks + pearls) =================
function laceTile() {
  let b = `<g fill="none" stroke="${K}" stroke-width="1">`;
  for (let y = 0; y <= 120; y += 12) for (let x = (y / 12) % 2 ? 6 : 0; x <= 120; x += 12) b += `<path d="M${x} ${y - 6} L${x + 6} ${y} L${x} ${y + 6} L${x - 6} ${y}Z"/>`;
  b += `</g>`;
  b += flower(60, 60, 20, 8, true) + flower(0, 0, 12, 6, true) + flower(120, 0, 12, 6, true) + flower(0, 120, 12, 6, true) + flower(120, 120, 12, 6, true);
  for (const [x, y, a] of [[30, 60, -90], [90, 60, 90], [60, 30, 0], [60, 90, 180]]) b += leaf(x, y, 14, a, true);
  return svg('0 0 120 120', b);
}
function laceEdge() {
  let b = '';
  b += `<path d="M0 0 H80 V18 C 80 40 60 46 40 46 C 20 46 0 40 0 18Z" fill="${K}"/>`;
  b += `<circle cx="40" cy="22" r="7" fill="#000" fill-opacity="0" stroke="${K}"/>`;
  return svg('0 0 80 50', b).replace('<circle cx="40" cy="22" r="7" fill="#000" fill-opacity="0" stroke="#000"/>', '');
}
function laceEdgeHoles() {
  // scallop with an eyelet hole and a small flower, fill-rule evenodd for holes
  const d = 'M0 0 H80 V16 C 80 40 62 48 40 48 C 18 48 0 40 0 16 Z M40 18 m-8 0 a8 8 0 1 0 16 0 a8 8 0 1 0 -16 0 Z M14 10 m-3 0 a3 3 0 1 0 6 0 a3 3 0 1 0 -6 0 Z M66 10 m-3 0 a3 3 0 1 0 6 0 a3 3 0 1 0 -6 0 Z';
  let dots = '';
  for (let i = 0; i < 7; i++) { const a = Math.PI * (0.15 + i * 0.117); dots += ` M${f(40 + Math.cos(a) * 30)} ${f(14 + Math.sin(a) * 26)} m-1.8 0 a1.8 1.8 0 1 0 3.6 0 a1.8 1.8 0 1 0 -3.6 0 Z`; }
  return svg('0 0 80 50', `<path d="${d}${dots}" fill="${K}" fill-rule="evenodd"/>`);
}
function laceDoily() {
  let b = '';
  let outer = '';
  for (let i = 0; i < 24; i++) {
    const a = (Math.PI * 2 * i) / 24;
    outer += `<circle cx="${f(200 + Math.cos(a) * 182)}" cy="${f(200 + Math.sin(a) * 182)}" r="18"/>`;
  }
  b += `<g fill="${K}">${outer}</g><circle cx="200" cy="200" r="182" fill="${K}"/>`;
  // cut-outs (drawn as white, converted to transparent with a mask)
  let holes = '';
  for (let i = 0; i < 24; i++) {
    const a = (Math.PI * 2 * i) / 24;
    holes += `<circle cx="${f(200 + Math.cos(a) * 182)}" cy="${f(200 + Math.sin(a) * 182)}" r="7"/>`;
    holes += `<path d="${petal(30, 9)}" transform="translate(${f(200 + Math.cos(a) * 150)} ${f(200 + Math.sin(a) * 150)}) rotate(${f((a * 180) / Math.PI + 90)})"/>`;
  }
  for (let i = 0; i < 16; i++) { const a = (Math.PI * 2 * i) / 16; holes += `<circle cx="${f(200 + Math.cos(a) * 112)}" cy="${f(200 + Math.sin(a) * 112)}" r="10"/>`; }
  holes += `<circle cx="200" cy="200" r="92"/>`;
  return svg('0 0 400 400', `<mask id="m"><rect width="400" height="400" fill="#fff"/><g fill="#000">${holes}</g></mask><g mask="url(#m)">${b}</g>
<circle cx="200" cy="200" r="86" fill="none" stroke="${K}" stroke-width="2"/><circle cx="200" cy="200" r="80" fill="none" stroke="${K}" stroke-width="1" stroke-dasharray="3 4"/>`);
}
// pearl garland (shaded, used as a normal image)
function pearls() {
  let b = '';
  const n = 26;
  for (let i = 0; i <= n; i++) {
    const t = i / n, x = 10 + t * 580, y = 14 + Math.sin(Math.PI * t) * 70;
    const r = 7 + Math.sin(Math.PI * t) * 2.5;
    b += `<circle cx="${f(x)}" cy="${f(y)}" r="${f(r)}" fill="url(#p)"/>`;
  }
  const defs = `<radialGradient id="p" cx=".35" cy=".3" r=".75"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".45" stop-color="#F3EEE6"/><stop offset=".8" stop-color="#D8CFC2"/><stop offset="1" stop-color="#B9AE9F"/></radialGradient>`;
  return svg('0 0 600 100', b, defs);
}

// ================= DESERT (masks + sand) =================
function palm() {
  let b = `<path d="M118 400 C 112 300 104 220 120 120 C 124 220 130 300 132 400 Z" fill="${K}"/>`;
  for (let y = 140; y < 400; y += 14) b += `<path d="M${f(108 + (y - 140) * 0.02)} ${y} L${f(132 - (y - 140) * 0.01)} ${y - 4}" stroke="#000" stroke-opacity="0" />`;
  const frond = (ang, len, droop) => {
    let o = `<g transform="translate(120 120) rotate(${ang})"><path d="M0 0 Q ${len * 0.5} ${-droop} ${len} ${droop * 0.6}" fill="none" stroke="${K}" stroke-width="3"/>`;
    for (let t = 0.12; t < 1; t += 0.07) {
      const x = len * t, y = -droop * 4 * t * (1 - t) + droop * 0.6 * t * t;
      const l = 30 * (1 - t * 0.6);
      o += `<path d="M${f(x)} ${f(y)} l${f(l * 0.3)} ${f(l)} l3 -2Z M${f(x)} ${f(y)} l${f(l * 0.5)} ${f(-l * 0.7)} l3 2Z" fill="${K}"/>`;
    }
    return o + '</g>';
  };
  for (const [a, l, d] of [[-160, 110, 30], [-130, 120, 40], [-95, 100, 20], [-60, 120, 40], [-25, 110, 30], [10, 95, 20], [-190, 90, 20]]) b += frond(a, l, d);
  b += `<circle cx="112" cy="132" r="6" fill="${K}"/><circle cx="126" cy="134" r="6" fill="${K}"/><circle cx="119" cy="140" r="6" fill="${K}"/>`;
  return svg('0 0 240 400', b);
}
function desertRose() {
  let b = '';
  for (const [x, y, s] of [[80, 70, 1], [40, 100, 0.7], [120, 104, 0.75]]) {
    b += `<g transform="translate(${x} ${y}) scale(${s})">`;
    for (let i = 0; i < 5; i++) b += `<path d="${petal(36, 20)}" transform="rotate(${i * 72})" fill="${K}" fill-opacity=".9"/>`;
    b += `<circle r="7" fill="#000" fill-opacity="0"/></g>`;
  }
  for (const [x, y, a] of [[60, 130, -30], [100, 132, 30], [80, 140, 0], [30, 126, -60], [130, 128, 60]]) b += leaf(x, y, 34, a, true);
  return svg('0 0 160 160', b);
}
const sand = svg('0 0 300 300', `<rect width="300" height="300" filter="url(#s)"/>`,
  `<filter id="s"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/>
<feColorMatrix values="0 0 0 0 .55  0 0 0 0 .42  0 0 0 0 .25  0 0 0 .12 0"/></filter>`);
// 4-point sparkle (mask)
const sparkle = svg('0 0 40 40', `<path d="M20 0 C 22 14 26 18 40 20 C 26 22 22 26 20 40 C 18 26 14 22 0 20 C 14 18 18 14 20 0Z" fill="${K}"/>`);

const files = {
  'porcelain-tile.svg': porcelainTile(), 'porcelain-plate.svg': porcelainPlate(), 'porcelain-corner.svg': porcelainCorner(),
  'glasshouse.svg': glasshouse(), 'fern.svg': fern(), 'ivy.svg': ivy(),
  'lace-tile.svg': laceTile(), 'lace-edge.svg': laceEdgeHoles(), 'lace-doily.svg': laceDoily(), 'pearls.svg': pearls(),
  'palm.svg': palm(), 'desert-rose.svg': desertRose(), 'sand-grain.svg': sand, 'sparkle.svg': sparkle,
};
for (const [n, s] of Object.entries(files)) writeFileSync(new URL(n, OUT), s.replace(/\n\s*/g, ' '));
console.log('wrote', Object.keys(files).join(', '));
