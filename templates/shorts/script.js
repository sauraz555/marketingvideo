// Content of the short. Edit this file only; short.html is the engine.
//
// Timing: give each scene `seg: n` (starts with spoken line n from segments.js),
// `seg: [n, m]` (lines n..m), or explicit seconds `t: 3.2, end: 6`.
// A scene runs until the next scene in its lane starts. Captions (`cap`/`title`) are one lane,
// visuals (everything else) the other, so a caption and a visual can be on screen together.
// Any visual can carry its own caption: { type:'bignum', ..., cap:{ lead:'...', key:'...' } }.
//
// `word: 'visa'` starts a scene when that word is spoken (needs words.js from `tools/shorts.py align`).
//
// Scene types (full field list: `python tools/shorts.py guide`, or templates/shorts/scenes.json)
//   cap      { lead, key, hl, pos }      small lead line + big bold keyword(s); hl = accent box; pos = 'top' | 'mid' | 'low'
//   title    { lead, key, hl }           same as cap, centred (hooks)
//   bignum   { value, unit, kicker, badges:[..] }   counts up when value is a number
//   stat     { value, label }            dark card, big number
//   compare  { items:[{ icon, name, value, sub, bar, win }], layout }   'stack' rows (3+ items or bars) or 'side' cards
//   chart    { title, items:[{ name, value, label, hl }], note, dir }    'v' columns (up to 4) or 'h' rows (5-6)
//   ring     { value, label, note }      one percentage (0-100)
//   line     { title, points:[{ x, y, label }], note }   one trend, first and last value labelled
//   timeline { title, items:[{ when, text }] }           dated steps
//   dosdonts { title, dos:[..], donts:[..] }             3 short phrases per side
//   pills    { title, items:[..], ok }   "NOT RECOMMENDED FOR" style list (ok:true = green ticks)
//   list     { title, items:[..], icons:[..], gap, at:[..] }  numbered steps appearing one by one
//   badges   { items:[{ value, label }] } round recap badges
//   stamp    { text, good, sub }         REFUSED / GRANTED slammed on screen
//   quote    { source, text, mark, by, url }   a sentence from an official source, key phrase highlighted
//   web      { img, url, marks }         source page with the sentence highlighted (paste what `capture` prints)
//   doc      { img, marks:[y,..] }       document / notice B-roll; marks = highlighter bars (px from top of page)
//   photo    { src, caption, style }     framed photo or clip (polaroid | card); items:[..] for a collage
//   broll    { src }                     full-screen image or video
//   hero     { icon }                    big emoji
//   cta      { icon, text, sub }         closing call to action
//   -- product film --
//   kinetic  { text: 'Not *anymore*', glow, sub }   big words; *accent*, _italic_
//   phone    { title, screen | call:{ name, status }, notes:[{ name, text, time }] }   3D phone, cards fly in
//   orb      { label, chip, at:[x,y], to:[x,y] }    glowing orb (assistant / AI / signal)
//   glass    { title, items:[..], icons:[..], exit:'zoom' }   glass checklist card
//   screen   { src, tilt, to, zoom, spot }          screen recording or screenshot floating in 3D
//   -- creator explainer --
//   headline { kicker, title, sub, body }           editorial title above the head; body types on
//   stickies { items:[{ text }] }                   sticky notes
//   tags     { items:[{ text, at }] }               words in hand-drawn ovals
//   mindmap  { nodes:[{ id, text, x, y, parent, at }], cam:[{ at, x, y, zoom }], glow:[..] }   framework drawn on paper
//   -- split explainer (add split: true and head: 'Section *title*' to panel scenes) --
//   orbit    { hub, items:[{ img | icon | text }] }  tiles on a turning ring, the idea lands in the middle
//   skeleton { lines, marks, callout, bracket }      a script page as bars; a line highlighted and explained
//   picklist { items:[..], focus }                   numbered pills, one in focus
//
// Top-level keys besides scenes: captions: { style: 'pill' | 'outline' | 'bold' } (spoken captions from words.js),
// brand | logo, look, theme, safe ('organic' | 'strict'), captionStyle ('stroke' | 'scrim'),
// syncWords, audio, duration (no voice), presenter, presenterOffset, backdrops:[{ src | style:'white'|'sky'|'night'|'brand'|'paper', t, end, dim, blur, zoom, pan, focus }],
// moves:[{ t, end, mode:'anchor' | 'punch' }] (presenter with a cut-out only).
window.SCRIPT = {
  brand: '@yourhandle',
  // look: leave out = the brand from brand.js when there is one (`tools/shorts.py brand`), otherwise 'clean'.
  // Or force one: 'clean' | 'dark' | 'warm' | 'brand'.  theme: { accent: '#E4002B' } recolours any look.
  safe: 'organic',         // keep text clear of the app buttons: 'organic' posts | 'strict' for paid ads
  audio: 'voice.mp3',      // voiceover; length sets the video length (no voice: audio: null and duration: seconds)
  presenter: null,         // 'presenter.mp4' for a version with a person on camera
  presenterOffset: 0,      // seconds to skip at the start of presenter.mp4
  scenes: [
    { t: 0.0,  type: 'title', lead: 'Want videos like this', key: 'IN MINUTES?', hl: false },
    { t: 0.0,  type: 'hero', icon: '🎬' },
    { t: 3.0,  type: 'cap', lead: 'Every line becomes a', key: 'BOLD CAPTION', hl: true },
    { t: 6.0,  type: 'bignum', value: '400', unit: 'mg / day', kicker: 'Big numbers', badges: ['Source A', 'Source B'],
               cap: { lead: 'Numbers', key: 'COUNT UP' } },
    { t: 10.0, type: 'stat', value: '17', label: 'Stat cards for one key fact' },
    { t: 13.0, type: 'compare', items: [{ icon: '🥤', name: 'Option A', value: '32 / 100' }, { icon: '🧃', name: 'Option B', value: '30 / 100' }],
               cap: { lead: 'Side-by-side', key: 'COMPARISONS' } },
    { t: 17.0, type: 'doc', marks: [300, 420], cap: { lead: 'Show the', key: 'SOURCE', hl: true } },
    { t: 21.0, type: 'pills', title: 'Not for', items: ['Children', 'Pregnant women', 'Diabetics'] },
    { t: 25.0, type: 'badges', items: [{ value: '400', label: 'per day' }, { value: '100', label: 'per can' }, { value: '2', label: 'max' }],
               cap: { lead: 'Just remember', key: '3 NUMBERS' } },
    { t: 29.0, end: 32.5, type: 'cta', icon: '👇', text: 'Comment your number', sub: 'Follow for more' },
  ],
};
