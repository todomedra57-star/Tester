// Preview stand-in for the platform runtime, running inside the invitation
// iframe. The real platform builds these behaviours itself; the template has
// no JavaScript of its own.
(() => {
  const cfg = JSON.parse(document.getElementById('runtime-config').textContent);
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const W = cfg.words;

  // ----- ambient effect -----
  if (cfg.ambient && cfg.ambient !== 'none') {
    const layer = document.createElement('div');
    layer.className = `ambient ambient-${cfg.ambient}`;
    layer.setAttribute('aria-hidden', 'true');
    document.body.append(layer);
  }

  // ----- reveal effects -----
  const root = document.documentElement;
  root.style.setProperty('--fx-dur', `${cfg.motion.duration}ms`);
  root.style.setProperty('--fx-stagger', `${cfg.motion.stagger}ms`);
  const sections = [...document.querySelectorAll('[data-animate]')];
  sections.forEach((s) => {
    const effect = cfg.sections[s.dataset.animate]?.effect || 'fade-up';
    s.classList.add('fx', `fx-${effect}`);
    s.querySelectorAll('[data-item]').forEach((el, i) => el.style.setProperty('--i', i));
  });
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
  }, { threshold: 0.15 });
  const startReveal = () => sections.forEach((s) => io.observe(s));

  // ----- parallax (one layer) -----
  const px = document.querySelector('[data-parallax]');
  if (px && cfg.motion.parallax && !reduce) {
    addEventListener('scroll', () => { px.style.translate = `0 ${Math.min(scrollY, 800) * 0.25}px`; }, { passive: true });
  }

  // ----- scene engine -----
  // Templates mark elements with data-scene ("contain" for a tall pinned section,
  // "cover" for a section passing through the screen). The engine writes, every
  // frame and smoothed for weight:
  //   on each scene:  --p   scroll progress 0..1   ·  --n / data-n  number of [data-item]
  //   on :root:       --tx / --ty  device tilt (or pointer) -1..1
  // and adds .scene-on to <html>. Templates do all choreography in CSS with these.
  const scene = (() => {
    const els = [...document.querySelectorAll('[data-scene]')];
    els.forEach((el) => { const n = el.querySelectorAll('[data-item]').length; el.style.setProperty('--n', n); el.dataset.n = n; });
    const clamp = (v) => Math.max(0, Math.min(1, v));
    const progress = (el) => {
      const r = el.getBoundingClientRect(), vh = innerHeight, range = r.height - vh;
      if (el.dataset.scene !== 'cover' && range > 40) return clamp(-r.top / range);
      return clamp((vh - r.top) / (vh + r.height));
    };
    const state = new Map();
    let tx = 0, ty = 0, cx = 0, cy = 0, hasTilt = false;
    if (!reduce) {
      root.classList.add('scene-on');
      addEventListener('pointermove', (e) => { if (hasTilt) return; tx = (e.clientX / innerWidth - 0.5) * 2; ty = (e.clientY / innerHeight - 0.5) * 2; }, { passive: true });
      addEventListener('deviceorientation', (e) => {
        if (e.gamma == null) return;
        hasTilt = true;
        tx = Math.max(-1, Math.min(1, e.gamma / 25));
        ty = Math.max(-1, Math.min(1, (e.beta - 45) / 25));
      });
    }
    const frame = () => {
      for (const el of els) {
        const target = progress(el);
        const cur = state.has(el) ? state.get(el) + (target - state.get(el)) * (reduce ? 1 : 0.14) : target;
        state.set(el, cur);
        el.style.setProperty('--p', cur.toFixed(4));
      }
      if (!reduce) {
        cx += (tx - cx) * 0.07; cy += (ty - cy) * 0.07;
        root.style.setProperty('--tx', cx.toFixed(3));
        root.style.setProperty('--ty', cy.toFixed(3));
      }
      requestAnimationFrame(frame);
    };
    if (els.length || !reduce) requestAnimationFrame(frame);
    return {
      // iOS asks for motion permission; it must be requested inside a tap (the opening)
      askTilt() {
        const D = window.DeviceOrientationEvent;
        if (!reduce && D && typeof D.requestPermission === 'function') D.requestPermission().catch(() => {});
      },
    };
  })();

  // ----- opening -----
  if (cfg.intro && cfg.intro !== 'none') {
    document.body.classList.add('is-locked');
    const intro = document.createElement('div');
    intro.className = `intro intro-${cfg.intro}`;
    const doors = cfg.intro === 'palace'
      ? '<div class="intro__doors"><div class="intro__door intro__door--l"><span class="intro__lattice"></span></div><div class="intro__door intro__door--r"><span class="intro__lattice"></span></div></div>'
      : '<div class="intro__half intro__half--l"></div><div class="intro__half intro__half--r"></div>';
    intro.innerHTML = doors +
      '<div class="intro__content"><h2 class="intro__names"></h2><button class="intro-seal" type="button"></button><p class="intro__hint"></p></div>';
    intro.querySelector('.intro__names').textContent = cfg.names;
    const seal = intro.querySelector('.intro-seal');
    seal.textContent = cfg.monogram;
    seal.setAttribute('aria-label', W.tapToOpen);
    intro.querySelector('.intro__hint').textContent = W.tapToOpen;
    document.body.append(intro);
    seal.focus({ preventScroll: true });
    seal.addEventListener('click', () => {
      scene.askTilt();
      intro.classList.add('is-open');
      document.body.classList.remove('is-locked');
      if (cfg.intro === 'palace' && !reduce) {
        // the page behind the doors settles from a slight zoom while the doors swing open
        document.body.classList.add('intro-settle');
        setTimeout(() => document.body.classList.remove('intro-settle'), 2200);
      }
      setTimeout(() => { intro.classList.add('is-gone'); startReveal(); }, reduce ? 0 : (cfg.intro === 'palace' ? 1700 : 900));
    }, { once: true });
  } else {
    startReveal();
  }

  // ----- wishes box -----
  customElements.define('wishes-box', class extends HTMLElement {
    connectedCallback() {
      const el = (tag, cls, text) => { const n = document.createElement(tag); if (cls) n.className = cls; if (text) n.textContent = text; return n; };
      const box = el('form', 'wb');
      box.noValidate = true;

      if (cfg.wishes.presets.length) {
        const chips = el('div', 'wb-chips');
        cfg.wishes.presets.forEach((p) => {
          const c = el('button', 'wb-chip', p);
          c.type = 'button';
          c.addEventListener('click', () => { msg.value = p; msg.focus(); });
          chips.append(c);
        });
        box.append(chips);
      }
      const field = (label, input) => { const f = el('label', 'wb-field'); f.append(el('span', 'wb-label', label), input); return f; };
      const name = el('input', 'wb-input'); name.maxLength = 50; name.placeholder = W.namePh;
      const msg = el('textarea', 'wb-textarea'); msg.maxLength = 500; msg.placeholder = W.messagePh;
      const send = el('button', 'wb-send', W.send); send.type = 'submit';
      const status = el('p', 'wb-status'); status.setAttribute('role', 'status');
      box.append(field(W.name, name), field(W.message, msg), send, status);

      box.addEventListener('submit', (e) => {
        e.preventDefault();
        if (!name.value.trim() || !msg.value.trim()) { status.textContent = W.fill; return; }
        status.textContent = W.sent;
        name.value = ''; msg.value = '';
      });

      if (cfg.wishes.showOnPage && cfg.wishes.approved.length) {
        const list = el('div', 'wb-list');
        cfg.wishes.approved.forEach((w) => {
          const item = el('div', 'wb-item');
          item.append(el('p', 'wb-item__name', w.name), el('p', 'wb-item__text', w.text));
          list.append(item);
        });
        box.append(list);
      }
      this.append(box);
    }
  });
})();
