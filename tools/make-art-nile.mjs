// Original artwork for the Nile Royale template → preview/library/.
// Run: node tools/make-art-nile.mjs
// Every piece is a single-colour silhouette used as a CSS mask, so the template
// colours it with palette tokens.
import { writeFileSync, mkdirSync } from 'node:fs';

const OUT = new URL('../preview/library/', import.meta.url);
mkdirSync(OUT, { recursive: true });
const K = '#000';
const f = (n) => Math.round(n * 100) / 100;
const svg = (vb, body) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${vb}">${body}</svg>`;

// slim column with an Egyptian lotus capital
function column() {
  let b = '';
  b += `<rect x="6" y="404" width="48" height="10" rx="1" fill="${K}"/><rect x="10" y="394" width="40" height="8" fill="${K}"/><rect x="14" y="386" width="32" height="6" fill="${K}"/>`;
  for (let i = 0; i < 4; i++) b += `<rect x="${17 + i * 7}" y="96" width="5" height="288" rx="2.5" fill="${K}"/>`;
  b += `<rect x="15" y="150" width="30" height="3" fill="${K}"/><rect x="15" y="156" width="30" height="1.5" fill="${K}"/>`;
  b += `<rect x="15" y="330" width="30" height="3" fill="${K}"/>`;
  // lotus capital: flared bell with petals
  b += `<path d="M16 96 C 8 70 2 52 2 40 L58 40 C 58 52 52 70 44 96 Z" fill="${K}"/>`;
  for (let i = 0; i < 5; i++) b += `<path d="M${f(10 + i * 10)} 44 Q ${f(14 + i * 8)} 70 ${f(18 + i * 6)} 92" stroke="#fff" stroke-width="1.6" fill="none"/>`;
  b += `<rect x="0" y="28" width="60" height="10" rx="1" fill="${K}"/><rect x="4" y="18" width="52" height="8" fill="${K}"/>`;
  b += `<path d="M30 0 L36 10 L30 16 L24 10 Z" fill="${K}"/>`;
  return svg('0 0 60 416', `<mask id="m"><rect width="60" height="416" fill="#fff"/><g stroke="#000" stroke-width="1.6" fill="none">${[0, 1, 2, 3, 4].map((i) => `<path d="M${f(10 + i * 10)} 44 Q ${f(14 + i * 8)} 70 ${f(18 + i * 6)} 92"/>`).join('')}</g></mask><g mask="url(#m)">${b.replace(/<path d="M[^"]*" stroke="#fff"[^>]*\/>/g, '')}</g>`);
}

// garden silhouette with distant palace domes and minarets
function garden() {
  let b = '';
  // distant palace
  b += `<path d="M190 150 V112 H230 V150 Z M200 112 Q210 84 220 112 Z" fill="${K}" fill-opacity=".55"/>`;
  b += `<path d="M236 150 V96 H300 V150 Z M244 96 Q268 52 292 96 Z" fill="${K}" fill-opacity=".55"/>`;
  // finial: a thin spike, a ball and a crescent
  b += `<rect x="267" y="40" width="2" height="16" fill="${K}" fill-opacity=".55"/><circle cx="268" cy="44" r="2.6" fill="${K}" fill-opacity=".55"/>`;
  b += `<path d="M264 34 a5 5 0 1 0 8 0 a4 4 0 1 1 -8 0 Z" fill="${K}" fill-opacity=".55"/>`;
  b += `<path d="M306 150 V118 H346 V150 Z M316 118 Q326 92 336 118 Z" fill="${K}" fill-opacity=".55"/>`;
  b += `<rect x="226" y="62" width="6" height="88" fill="${K}" fill-opacity=".55"/><path d="M224 62 L229 44 L234 62 Z" fill="${K}" fill-opacity=".55"/>`;
  b += `<rect x="350" y="70" width="6" height="80" fill="${K}" fill-opacity=".55"/><path d="M348 70 L353 52 L358 70 Z" fill="${K}" fill-opacity=".55"/>`;
  // garden: cypress, rounded bushes, palms
  const cypress = (x, h) => `<path d="M${x} 180 C ${x - 9} ${180 - h * 0.4} ${x - 6} ${180 - h * 0.85} ${x} ${180 - h} C ${x + 6} ${180 - h * 0.85} ${x + 9} ${180 - h * 0.4} ${x} 180 Z" fill="${K}"/>`;
  const bush = (x, r) => `<ellipse cx="${x}" cy="${180 - r * 0.6}" rx="${r}" ry="${r * 0.7}" fill="${K}"/>`;
  const palm = (x, h) => {
    let p = `<path d="M${x - 2} 180 Q ${x + 4} ${180 - h * 0.5} ${x + 2} ${180 - h} L${x + 5} ${180 - h} Q ${x + 8} ${180 - h * 0.5} ${x + 3} 180 Z" fill="${K}"/>`;
    for (const a of [-150, -120, -80, -40, -10, 20]) {
      const r = (a * Math.PI) / 180, ex = x + 3 + Math.cos(r) * 34, ey = 180 - h + Math.sin(r) * 14 + 8;
      p += `<path d="M${x + 3} ${180 - h} Q ${f((x + 3 + ex) / 2)} ${f(180 - h - 10)} ${f(ex)} ${f(ey)} Q ${f((x + 3 + ex) / 2)} ${f(180 - h - 2)} ${x + 3} ${180 - h + 3} Z" fill="${K}"/>`;
    }
    return p;
  };
  b += palm(40, 120) + cypress(90, 110) + bush(120, 26) + cypress(150, 90) + bush(180, 20);
  b += bush(420, 22) + cypress(452, 100) + bush(486, 28) + cypress(520, 120) + palm(560, 130);
  b += `<rect x="0" y="170" width="600" height="10" fill="${K}"/>`;
  return svg('0 0 600 180', b);
}

// jasmine and olive sprig, anchored at the bottom-left corner
const STEM = 'M6 196 C 40 170 70 140 100 112 S 160 54 206 26';
const LEAVES = [[18, 186, -30], [28, 172, -95], [44, 166, -10], [56, 150, -85], [70, 142, 5], [82, 126, -75], [98, 120, 10], [110, 100, -70], [126, 94, 15], [140, 76, -60], [156, 70, 20], [168, 54, -55], [186, 46, 25]];
const FLOWERS = [[204, 26, 15], [176, 30, 12], [132, 62, 11], [196, 64, 10], [100, 96, 9]];
const leaf = (x, y, a, len = 34) => `<path d="M0 0 Q ${len * 0.5} ${-len * 0.22} ${len} 0 Q ${len * 0.5} ${len * 0.22} 0 0 Z" transform="translate(${x} ${y}) rotate(${a})" fill="${K}"/>`;
const jasmine = (x, y, r) => {
  let o = `<g transform="translate(${x} ${y})">`;
  for (let i = 0; i < 5; i++) o += `<ellipse cx="0" cy="${-r * 0.55}" rx="${r * 0.32}" ry="${r * 0.58}" transform="rotate(${i * 72 + 10})" fill="${K}"/>`;
  return o + `</g>`;
};
function sprig() {
  let b = `<path d="${STEM}" fill="none" stroke="${K}" stroke-width="2.4" stroke-linecap="round"/>`;
  for (const [x, y, a] of LEAVES) b += leaf(x, y, a);
  for (const [x, y, r] of FLOWERS) b += jasmine(x, y, r);
  b += `<path d="M120 70 Q 124 80 132 86 M168 40 Q 174 48 180 52" stroke="${K}" stroke-width="1.4" fill="none"/>`;
  return svg('0 0 220 200', b);
}
function jasmineOnly() {
  let b = '';
  for (const [x, y, r] of FLOWERS) b += jasmine(x, y, r * 0.86);
  return svg('0 0 220 200', b);
}

// Nile-wave divider with a small star
function wave() {
  let b = `<g fill="none" stroke="${K}" stroke-linecap="round">`;
  const w = (y, amp, sw) => {
    let d = `M6 ${y}`;
    for (let x = 6; x < 254; x += 16) d += ` q 8 ${-amp} 16 0`;
    return `<path d="${d}" stroke-width="${sw}"/>`;
  };
  b += w(15, 5, 1.4) + w(23, 3.5, 0.9) + `</g>`;
  let st = '';
  for (let i = 0; i < 16; i++) {
    const a = (Math.PI / 8) * i - Math.PI / 2, r = i % 2 ? 4 : 9;
    st += `${f(130 + Math.cos(a) * r)},${f(12 + Math.sin(a) * r)} `;
  }
  b = b.replace(/<path d="M6 15[^>]*>/, (m) => m) ;
  return svg('0 0 260 32', `<mask id="m"><rect width="260" height="32" fill="#fff"/><circle cx="130" cy="13" r="14" fill="#000"/></mask><g mask="url(#m)">${b}</g><polygon points="${st}" fill="${K}"/>`);
}

const files = {
  'nile-column.svg': column(), 'nile-garden.svg': garden(),
  'jasmine-olive.svg': sprig(), 'jasmine-flowers.svg': jasmineOnly(), 'nile-wave.svg': wave(),
};
for (const [n, s] of Object.entries(files)) writeFileSync(new URL(n, OUT), s.replace(/\n\s*/g, ' '));
console.log('wrote', Object.keys(files).join(', '));
