// Generates the preview's image library (original SVG artwork) into preview/library/.
// Run: node tools/make-art.mjs
// These stand in for the platform's image library: on the platform they would be
// uploaded as library images and picked through image tokens.
import { writeFileSync, mkdirSync } from 'node:fs';

const OUT = new URL('../preview/library/', import.meta.url);
mkdirSync(OUT, { recursive: true });

// Seeded random so the art is the same on every run.
let seed = 7;
const rnd = () => ((seed = (seed * 16807) % 2147483647) - 1) / 2147483646;
const between = (a, b) => a + rnd() * (b - a);
const pick = (arr) => arr[Math.floor(rnd() * arr.length)];
const f = (n) => Math.round(n * 10) / 10;

const BLUES = ['#1F3A73', '#2E4F8F', '#3F66AE', '#5A82C6', '#7FA0D6', '#A9BFE6'];
const LEAVES = ['#4E6B5E', '#6F8A7A', '#88A08F', '#5D7690', '#7C93A8'];
const WHITES = ['#FBF8F2', '#F2EEE6', '#E9E3D8'];

const watercolor = (id, scale = 5, freq = 0.035) => `
<filter id="${id}" x="-15%" y="-15%" width="130%" height="130%">
  <feTurbulence type="fractalNoise" baseFrequency="${freq}" numOctaves="3" seed="${Math.floor(between(1, 99))}" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="${scale}" xChannelSelector="R" yChannelSelector="G" result="d"/>
  <feGaussianBlur in="d" stdDeviation="0.35"/>
</filter>`;

// ---------- flower parts ----------
function floret(x, y, s, color) {
  const rot = between(0, 90);
  let out = `<g transform="translate(${f(x)} ${f(y)}) rotate(${f(rot)})">`;
  for (let i = 0; i < 4; i++) {
    out += `<ellipse cx="0" cy="${f(-s * 0.55)}" rx="${f(s * 0.42)}" ry="${f(s * 0.6)}" transform="rotate(${i * 90 + between(-8, 8)})" fill="${color}" fill-opacity="${f(between(0.72, 0.92))}" stroke="#16295A" stroke-opacity=".25" stroke-width=".6"/>`;
  }
  return out + `<circle r="${f(s * 0.16)}" fill="#EEF2FA" fill-opacity=".85"/></g>`;
}

function hydrangea(cx, cy, R, light = false) {
  let out = `<g>`;
  out += `<circle cx="${cx}" cy="${cy}" r="${R * 0.92}" fill="${light ? '#A9BFE6' : '#2E4F8F'}" fill-opacity=".45"/>`;
  const n = Math.round(R * 0.95);
  const pts = [];
  for (let i = 0; i < n; i++) {
    const a = between(0, Math.PI * 2), r = Math.sqrt(rnd()) * R * 0.85;
    pts.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]);
  }
  pts.sort((a, b) => (a[0] + a[1]) - (b[0] + b[1])); // paint back to front
  for (const [x, y] of pts) {
    const shade = ((x - cx) + (y - cy)) / (R * 2); // -1 top-left .. 1 bottom-right
    const pal = light ? BLUES.slice(2) : BLUES;
    const idx = Math.max(0, Math.min(pal.length - 1, Math.round((1 - (shade + 1) / 2) * (pal.length - 1) + between(-1, 1))));
    out += floret(x, y, between(R * 0.2, R * 0.28), pal[idx]);
  }
  return out + `</g>`;
}

function rose(cx, cy, R, colors) {
  const [base, mid, dark] = colors;
  let out = `<g transform="translate(${cx} ${cy}) rotate(${f(between(0, 360))})">`;
  out += `<circle r="${R}" fill="${base}"/>`;
  for (let ring = 0; ring < 4; ring++) {
    const rr = R * (1 - ring * 0.22), count = 5 - (ring > 1 ? 1 : 0);
    for (let i = 0; i < count; i++) {
      const a = (360 / count) * i + ring * 31;
      out += `<path d="M0 0 C ${f(rr * 0.9)} ${f(-rr * 0.2)}, ${f(rr * 0.8)} ${f(-rr * 1.05)}, 0 ${f(-rr)} C ${f(-rr * 0.8)} ${f(-rr * 1.05)}, ${f(-rr * 0.9)} ${f(-rr * 0.2)}, 0 0Z" transform="rotate(${a})" fill="${ring % 2 ? mid : base}" fill-opacity=".9" stroke="${dark}" stroke-opacity=".45" stroke-width=".8"/>`;
    }
  }
  out += `<path d="M0 0 m-${f(R * 0.18)} 0 a ${f(R * 0.18)} ${f(R * 0.2)} 0 1 0 ${f(R * 0.36)} 0" fill="none" stroke="${dark}" stroke-width="1.2" stroke-opacity=".6"/>`;
  return out + `</g>`;
}

function leaf(x, y, len, angle, color) {
  const w = len * between(0.28, 0.36);
  return `<g transform="translate(${f(x)} ${f(y)}) rotate(${f(angle)})">
<path d="M0 0 Q ${f(w)} ${f(-len * 0.45)} 0 ${f(-len)} Q ${f(-w)} ${f(-len * 0.45)} 0 0Z" fill="${color}" fill-opacity=".88" stroke="#2F4A40" stroke-opacity=".3" stroke-width=".7"/>
<path d="M0 0 L0 ${f(-len * 0.9)}" stroke="#E8EEE6" stroke-opacity=".45" stroke-width=".8"/></g>`;
}

function filler(x, y, s) {
  let out = `<g transform="translate(${f(x)} ${f(y)})">`;
  for (let i = 0; i < 5; i++) out += `<ellipse cy="${f(-s * 0.5)}" rx="${f(s * 0.32)}" ry="${f(s * 0.5)}" transform="rotate(${i * 72})" fill="${pick(WHITES)}" stroke="#B9B2A4" stroke-opacity=".5" stroke-width=".5"/>`;
  return out + `<circle r="${f(s * 0.18)}" fill="#C9A45E"/></g>`;
}

function sprig(x, y, len, angle) {
  let out = `<g transform="translate(${f(x)} ${f(y)}) rotate(${f(angle)})"><path d="M0 0 Q ${f(len * 0.12)} ${f(-len * 0.5)} 0 ${f(-len)}" stroke="#5E786A" stroke-width="1.1" fill="none"/>`;
  for (let t = 0.25; t < 1; t += 0.14) {
    out += `<circle cx="${f(between(-4, 4))}" cy="${f(-len * t)}" r="${f(between(1.8, 3.2))}" fill="${pick(BLUES.slice(1, 5))}"/>`;
  }
  return out + `</g>`;
}

function bouquet(w, h, spec) {
  let body = '';
  for (const l of spec.leaves) body += leaf(...l, pick(LEAVES));
  for (const s of spec.sprigs) body += sprig(...s);
  for (const hy of spec.hydrangeas) body += hydrangea(...hy);
  for (const r of spec.roses) body += rose(...r);
  for (const fl of spec.fillers) body += filler(...fl);
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${spec.viewBox || `0 0 ${w} ${h}`}">
<defs>${watercolor('wc', 4)}</defs><g filter="url(#wc)">${body}</g></svg>`;
}

const ROSE_BLUE = ['#3B5FA6', '#5479BD', '#1E366B'];
const ROSE_WHITE = ['#F6F2EA', '#E7E0D2', '#9E9585'];

// Corner cluster: sits over a card corner (anchored bottom-right of its box).
const corner = bouquet(240, 260, { viewBox: "40 70 200 185",
  leaves: [[150, 170, 95, -70], [130, 160, 80, -20], [160, 150, 90, 15], [120, 190, 70, -105], [175, 175, 85, 40], [100, 175, 60, -45]],
  sprigs: [[140, 140, 90, -35], [150, 150, 80, 10], [120, 160, 70, -80]],
  hydrangeas: [[125, 165, 38], [175, 130, 30, true], [90, 195, 22, true]],
  roses: [[160, 185, 24, ROSE_WHITE], [110, 130, 17, ROSE_BLUE]],
  fillers: [[195, 175, 7], [85, 160, 6], [140, 205, 6], [150, 110, 5]],
});
// Tall spray for the sides of the cover scene.
const spray = bouquet(170, 380, {
  leaves: [[90, 330, 110, -10], [80, 260, 90, -40], [100, 220, 90, 30], [70, 160, 80, -25], [95, 120, 70, 20], [85, 300, 70, 45]],
  sprigs: [[90, 120, 100, -10], [80, 200, 90, 25], [95, 300, 90, -30]],
  hydrangeas: [[85, 250, 40], [95, 160, 28, true], [75, 320, 26, true]],
  roses: [[105, 205, 20, ROSE_WHITE], [70, 290, 16, ROSE_BLUE], [100, 95, 13, ROSE_BLUE]],
  fillers: [[60, 220, 7], [120, 270, 6], [70, 120, 5], [115, 150, 6]],
});

// ---------- paper grain (transparent, laid over the bg color) ----------
const paper = `<svg xmlns="http://www.w3.org/2000/svg" width="320" height="320">
<filter id="p"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="3" stitchTiles="stitch"/>
<feColorMatrix values="0 0 0 0 .35  0 0 0 0 .3  0 0 0 0 .22  0 0 0 .09 0"/></filter>
<filter id="q"><feTurbulence type="fractalNoise" baseFrequency=".012" numOctaves="2" stitchTiles="stitch"/>
<feColorMatrix values="0 0 0 0 .5  0 0 0 0 .42  0 0 0 0 .3  0 0 0 .07 0"/></filter>
<rect width="100%" height="100%" filter="url(#q)"/><rect width="100%" height="100%" filter="url(#p)"/></svg>`;

// ---------- palace sketch (faint line art) ----------
function palace() {
  const s = [];
  const L = (d, w = 1.2) => s.push(`<path d="${d}" stroke-width="${w}"/>`);
  const arch = (x, y, w, h) => L(`M${x} ${y} V${y - h + w / 2} A${w / 2} ${w / 2} 0 0 1 ${x + w} ${y - h + w / 2} V${y}`);
  L('M0 660 H600', 1.6);
  L('M40 660 V420 H560 V660');
  L('M30 420 H570 M30 412 H570', 1);
  for (let x = 34; x < 566; x += 9) L(`M${x} 412 V400`, 0.7);
  L('M30 400 H570', 1);
  for (let x = 60; x < 540; x += 48) {
    if (x > 236 && x < 350) continue;
    arch(x, 520, 26, 70); arch(x + 4, 516, 18, 60);
    arch(x, 630, 26, 76);
    L(`M${x - 8} 660 V430 M${x + 34} 660 V430`, 0.6);
  }
  L('M230 660 V360 H370 V660');
  arch(262, 660, 76, 200); arch(272, 660, 56, 180);
  L('M222 360 H378 M222 352 H378', 1);
  L('M240 352 V300 H360 V352');
  for (let x = 250; x < 352; x += 20) arch(x, 340, 12, 30);
  L('M232 300 Q300 150 368 300', 1.4);
  L('M248 300 Q300 180 352 300', 0.8);
  L('M300 172 V130 M292 150 Q300 140 308 150 M300 130 m-5 0 a5 5 0 1 0 10 0 a5 5 0 1 0 -10 0', 1);
  for (const tx of [40, 520]) {
    L(`M${tx} 660 V300 H${tx + 40} V660`);
    for (let y = 340; y < 640; y += 70) arch(tx + 10, y, 20, 40);
    L(`M${tx - 6} 300 H${tx + 46} M${tx - 6} 292 H${tx + 46}`, 1);
    L(`M${tx} 292 Q${tx + 20} 230 ${tx + 40} 292`, 1.2);
    L(`M${tx + 20} 240 V215`, 1);
  }
  for (let x = 150; x < 460; x += 300) {
    L(`M${x - 30} 420 V330 H${x + 30} V420`, 1);
    L(`M${x - 34} 330 Q${x} 270 ${x + 34} 330`, 1);
    arch(x - 9, 410, 18, 60);
  }
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 700" width="600" height="700">
<defs>${watercolor('h', 2.2, 0.02)}</defs>
<g filter="url(#h)" fill="none" stroke="#1C2A48" stroke-linecap="round" stroke-linejoin="round">${s.join('')}</g></svg>`;
}

// ---------- wax seal ----------
function seal() {
  const pts = [];
  for (let i = 0; i < 36; i++) {
    const a = (i / 36) * Math.PI * 2, r = 46 + between(-3, 4) + (i % 7 === 0 ? 5 : 0);
    pts.push(`${f(60 + Math.cos(a) * r)} ${f(60 + Math.sin(a) * r)}`);
  }
  const heart = 'M60 80 C 38 64, 40 44, 52 44 C 57 44, 60 49, 60 52 C 60 49, 63 44, 68 44 C 80 44, 82 64, 60 80Z';
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="120" height="120">
<defs><radialGradient id="g" cx=".38" cy=".32" r=".8"><stop offset="0" stop-color="#E7C27A"/><stop offset=".55" stop-color="#C08F43"/><stop offset="1" stop-color="#7E5622"/></radialGradient>
<filter id="s"><feGaussianBlur stdDeviation="2.2"/></filter></defs>
<polygon points="${pts.join(' ')}" transform="translate(2 4)" fill="#3B2810" opacity=".35" filter="url(#s)"/>
<polygon points="${pts.join(' ')}" fill="url(#g)"/>
<circle cx="60" cy="60" r="33" fill="none" stroke="#7E5622" stroke-opacity=".6" stroke-width="2.5"/>
<circle cx="60" cy="60" r="33" fill="none" stroke="#F4DFA9" stroke-opacity=".5" stroke-width="1" transform="translate(-1 -1)"/>
<path d="${heart}" fill="#A87A35" stroke="#6E4A1A" stroke-width="1.6"/>
<path d="${heart}" fill="none" stroke="#F6E2AE" stroke-opacity=".6" stroke-width=".9" transform="translate(-1.2 -1.2)"/></svg>`;
}

// ---------- divider ornament ----------
const divider = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 24" width="240" height="24">
<g fill="none" stroke="#A9864F" stroke-width="1" stroke-linecap="round">
<path d="M10 12 H96 M144 12 H230"/><path d="M96 12 q8 -8 16 0 M144 12 q-8 -8 -16 0"/>
<path d="M96 12 q8 8 16 0 M144 12 q-8 8 -16 0"/></g>
<g fill="#A9864F"><path d="M120 4 L126 12 L120 20 L114 12Z"/><circle cx="10" cy="12" r="1.6"/><circle cx="230" cy="12" r="1.6"/>
<circle cx="104" cy="12" r="1.2"/><circle cx="136" cy="12" r="1.2"/></g></svg>`;

const files = {
  'flowers-corner.svg': corner,
  'flowers-spray.svg': spray,
  'paper-grain.svg': paper,
  'palace-sketch.svg': palace(),
  'wax-seal.svg': seal(),
  'ornament.svg': divider,
};
for (const [name, svg] of Object.entries(files)) writeFileSync(new URL(name, OUT), svg.replace(/\n\s*/g, '\n'));
console.log('wrote', Object.keys(files).join(', '));
