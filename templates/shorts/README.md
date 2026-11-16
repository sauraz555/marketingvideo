# Shorts template (TikTok / Reels / YouTube Shorts, 1080x1920)

The "explainer creator" format: bold two-line captions, big stat numbers that count up, stat cards,
side-by-side comparisons, pill lists, recap badges, document B-roll and a closing CTA, timed to a voiceover.

Works **with people** (put the talking-head clip in the project as `presenter.mp4` and set
`presenter: 'presenter.mp4'` in `script.js`; list and CTA scenes shrink the footage into a card)
or **without people** (designed warm/dark background, everything else the same).

## Make one

```
python tools/shorts.py new my-topic --voice "C:/Users/.../Downloads/voice.mp3" [--presenter clip.mp4]
#   -> projects/my-topic/  and prints the spoken lines it found:  seg 0  0.00-4.01 ...
# edit projects/my-topic/script.js: one scene per line, `seg: n` ties it to spoken line n
python tools/shorts.py sheet my-topic     # contact sheet -> projects/my-topic/qa/sheet.jpg
python tools/shorts.py render my-topic [--music bed.mp3]   # -> projects/my-topic/output/my-topic-1080x1920.mp4
```

Open `short.html` in a browser to play it with the voice and scrub.

If lines are split badly, re-run `segments` with `--min-pause 0.5` (fewer, longer lines) or `0.25` (more),
or `--noise -30` for noisy audio. Scenes can also use exact seconds: `t: 12.4, end: 15`.

## Adding web screenshots (sources on screen)
```
python tools/shorts.py capture my-topic --url "https://official-page" --find "exact sentence on that page" --name roi
python tools/shorts.py frames my-topic reference.mp4      # optional: a reference video cut into gridded frames
```
`capture` prints a ready `scene` line with the highlight placed. `frames` writes `ref/grid-sheet.jpg` so layout can be matched to a reference (pixel grid of the 1080x1920 frame).

For a full build with research and checks, use the `shorts-director` agent in `.claude/agents/`.

## Rules (match the reference style)
- One idea per scene; the caption `key` is 1-3 words, UPPERCASE in the render; `lead` is the short line above it.
- Orange highlight (`hl: true`) for the one word that matters in a line, not for every caption.
- Real numbers only, with the source on screen (`badges` on a `bignum`, or a `doc` scene).
- Hook in the first 2 seconds (`title` + `hero` or `bignum`), CTA in the last 3.
- Nepali voice + English captions works: captions summarise the line; they do not need to translate every word.
