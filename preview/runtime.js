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

  // ----- opening -----
  if (cfg.intro && cfg.intro !== 'none') {
    document.body.classList.add('is-locked');
    const intro = document.createElement('div');
    intro.className = `intro intro-${cfg.intro}`;
    intro.innerHTML = '<div class="intro__half intro__half--l"></div><div class="intro__half intro__half--r"></div>' +
      '<div class="intro__content"><h2 class="intro__names"></h2><button class="intro-seal" type="button"></button><p class="intro__hint"></p></div>';
    intro.querySelector('.intro__names').textContent = cfg.names;
    const seal = intro.querySelector('.intro-seal');
    seal.textContent = cfg.monogram;
    seal.setAttribute('aria-label', W.tapToOpen);
    intro.querySelector('.intro__hint').textContent = W.tapToOpen;
    document.body.append(intro);
    seal.focus({ preventScroll: true });
    seal.addEventListener('click', () => {
      intro.classList.add('is-open');
      document.body.classList.remove('is-locked');
      setTimeout(() => { intro.classList.add('is-gone'); startReveal(); }, reduce ? 0 : 900);
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
