# Midnight: a minimal dark-blue invitation template

A template built to the "Anatomy of an invitation" guide: three files written
against the view model, plus a preview harness to see it.

```
templates/midnight/
  manifest.json   texts (ar/en), tokens, palettes, variants, default animation
  template.html   Handlebars sections: cover, countdown, story, gallery, events, wishes, footer
  style.css       token variables only, logical properties, mobile first, max 520px
preview/          stand-in for the platform (helpers, opening, reveal, wishes box)
index.html        preview page
```

## Preview

Serve the folder over http (fetch doesn't work from `file://`):

```
npx serve .        # or: python3 -m http.server
```

Use the controls to switch test case (Arabic demo, English, smallest, longest),
palette, date style, countdown style, photo frame, opening, stars and motion.

## The design

- **Palettes:** Navy & ice (default), Navy & gold, Indigo & pearl.
- **Signature:** hairline frame inset on the cover, a thread dropping to a small
  crescent, a diamond on each divider, and offset hairline photo frames.
- **Variants:** `dateStyle` line | badge | calendar · `countdownStyle` ring | plain ·
  `photoFrame` offset | arch | circle.
- **Own effect:** `ambient-stars`, quiet twinkling stars for night weddings.

## Making another template like this

Copy `templates/midnight/`, rename the `key`, and change mainly `style.css` and
the palettes. Keep the rules from the guide: no `<script>`, no fixed words in
the HTML (`{{text "key"}}`), no `{{{ }}}`, colors and fonts only via `--c-*` /
`--font-*`, own classes prefixed `.fx-` / `.intro-` / `.ambient-`.
To preview it, change `TEMPLATE` at the top of `preview/preview.js`.
