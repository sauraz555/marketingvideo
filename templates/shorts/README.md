# Shorts template (TikTok / Reels / YouTube Shorts, 1080x1920)

The "explainer creator" format: bold two-line captions, numbers that count up, stat cards, stacked comparisons,
bar / line / ring charts, timelines, pill lists, recap badges, source pages with the sentence highlighted and a
closing CTA, timed to a voiceover.

Four formats share the one engine (details in `DIRECTOR.md`): **data explainer** (above), **product film** (big type,
3D phone, cards, orb, glass card, changing backgrounds; example `projects/shorts-kinetic-reference/`), **creator
explainer** (headline above the presenter, sticky notes, oval tags, a mind map that draws itself, spoken pill captions),
**split explainer** (presenter card below, a black panel above with a section title and a diagram that builds, one-word
captions) and **story b-roll** (full-screen clips with small outlined captions).

`python tools/shorts.py plan <name> --text script.txt` is the director's first pass: it reads the script, cuts it into
beats, picks the format and proposes a scene for every beat with the reason (`plan.json`).

Works **with people** (put the talking-head clip in the project as `presenter.mp4` and set
`presenter: 'presenter.mp4'` in `script.js`; `pills` and `cta` scenes with `shrink: true` shrink the footage into a card)
or **without people** (designed background, everything else the same).

Works **for any brand or none**: by default the look is `clean`, a neutral design. `python tools/shorts.py brand <name>
--url https://company.com` reads the name, logo and main colour from the brand's site and the video takes them on.

Works **from any AI model or by hand**: everything is a shell command. `python tools/shorts.py guide` prints the brief
(`DIRECTOR.md`) and every scene type (`scenes.json`); `doctor` says what the machine can do; `lint --json` returns
problems as data. `projects/shorts-reference/` is a finished example.

## Make one

```
python tools/shorts.py new my-topic --voice "C:/Users/.../Downloads/voice.mp3" [--presenter clip.mp4]
#   -> projects/my-topic/  and prints the spoken lines it found:  seg 0  0.00-4.01 ...
# edit projects/my-topic/script.js: one scene per line, `seg: n` ties it to spoken line n
python tools/shorts.py lint my-topic      # rules: cut-off text, caption on a graphic, unsafe area, missing files, pacing
python tools/shorts.py sheet my-topic     # contact sheet -> projects/my-topic/qa/sheet.jpg (red bands = covered by the app)
python tools/shorts.py render my-topic [--music bed.mp3]   # -> projects/my-topic/output/my-topic-1080x1920.mp4
python tools/shorts.py render my-topic --from 3 --to 8     # quick test cut -> output/my-topic-test.mp4
```
The render is H.264 1080x1920 at 30 fps with BT.709 colour; the audio is normalised to -14 LUFS (`--no-loudnorm` to skip).
No voice file? A presenter clip with sound becomes the voice (`segments` extracts it), or set `duration` in `script.js`
for a captions-and-music video (`render --music track.mp3`).

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

## Safe zones
The apps draw their buttons and text over the video. The engine keeps captions and the brand line clear of the top
200 px, the bottom 400 px and the lower right-hand column (`safe: 'organic'`, the default), or 288 / 672 px for paid
ads (`safe: 'strict'`). `sheet` shows the covered areas in red and `lint` warns when text sits in them. These figures
come from second-hand copies of the platforms' templates: upload one unlisted test and check before a campaign.

## Words on the beat (optional)
```
python tools/shorts.py align my-topic                       # local speech recognition, if faster-whisper is installed
python tools/shorts.py align my-topic --from words.json     # or timings from any tool: JSON, .srt, .vtt
python tools/shorts.py align my-topic --text script.txt     # or ElevenLabs forced alignment (ELEVENLABS_API_KEY)
```
writes `words.js`. Then `{ word: 'visa', type: 'bignum', ... }` starts a scene when the word is spoken, and
`sync: true` on a caption pops its key words in time (only when captions are in the voice's language).
The two ElevenLabs paths (`align --text`, `voice`) follow the published API but have not been run against the live service yet.

## Rules
- One idea per scene; the caption `key` is 2-5 words, UPPERCASE in the render; `lead` is the short line above it.
- Accent box (`hl: true`) for the one word that matters in a line, not for every caption.
- Real numbers only, with the source on screen (`badges` on a `bignum`, a `note` on a chart, or a `web` / `doc` scene).
- Something on screen from the first frame (`title` + `hero` or `bignum`), something new every 2-4 s, CTA in the last 3 s.
- Nepali voice + English captions works: captions summarise the line; they do not need to translate every word.

## Backdrops: images and videos behind the scenes
```js
backdrops: [
  { src: 'media/airport.png', t: 0,     end: 10.8, focus: [15, 85], zoom: [1, 1.08], dim: 0.42 },  // focus = slow sideways drift (wide images)
  { src: 'media/city.mp4',    t: 10.35, end: 22.1, dim: 0.40 },                                      // videos loop to fill the slot
]
```
Neighbouring backdrops crossfade (start the next 0.45 s early). Text switches to white automatically while a backdrop is on screen. With a presenter and a cut-out (`tools/matte.py`) the backdrop replaces the room behind the person. Generate the media with any image or video tool you have, then save it in `projects/<name>/media/`.

## Setup comes first
Every new project asks its setup questions before anything else (voice language, caption language, voice source, person on camera, brand website or none, look, backdrop mode and **which tool makes the backdrops: Kling, ElevenLabs, Higgsfield, Bloom or your own files**, spend limit, length, music, logo, sources, privacy, normal post or paid ad, AI-content label). Answers are saved in `projects/<name>/config.json`.
```
python tools/shorts.py new my-topic --voice voice.mp3      # asks the questions in a terminal
python tools/shorts.py config my-topic --interactive       # ask (or ask the rest) later
python tools/shorts.py config my-topic --set "backdrop_tool=free built-in gradients (no account)" --set backdrop_budget="free only"
```
The `shorts-director` agent reads `config.json` first, asks you anything still unanswered in the chat, and never spends beyond the limit you set.

## Framed photos
```js
{ t: 4.46, end: 8.0, type: 'photo', src: 'media/airport.png', caption: 'Waiting…', tilt: -4 }                         // polaroid with tape
{ t: 12, end: 18, type: 'photo', style: 'card', items: [{ src: 'media/a.png' }, { src: 'media/b.png' }] }              // 2-3 photo collage
```
Photos and short video clips drop in with a tilt and float gently. For the most professional look, put the same picture behind it as a **blurred backdrop** (`blur: 14`), so the framed photo sits on its own colours.

## Works with whatever you have (nothing is compulsory)
No single service is required. Each optional piece has a free fallback:

| You do not have | What happens instead |
|---|---|
| An image or video generator (Kling, ElevenLabs, Higgsfield, Bloom, ...) or credits | Your own photos or footage in `media/`; `python tools/shorts.py backdrop <name>` (colour-mesh image, `--video` for an animated gradient, `--from-video clip.mp4` for a still of your footage). No account. |
| A voice service | Supply your own `voice.mp3`, use the presenter's own audio, or make a captions-only video. |
| A browser or web search | No source screenshots; the video states only what you give it and the unverified claims are listed so you can add links. |
| The cut-out model | Presenter videos still render (graphics on top, cards in the lower third); only "graphics behind the person" and the shrink move need it. Get it once with `python tools/matte.py --download` (15 MB, GPL-3.0), then `python tools/matte.py projects/<name>/presenter.mp4` (`--choke 1 --feather 3` cleans the edge; `--model resnet50` on a GPU). |
| A brand | The `clean` look. |
| Word timings | Scenes are timed to the spoken lines (`segments`) instead. |

The setup questions (`python tools/shorts.py config <name> --interactive`) default to **auto: use what I have**, and **free only** for spend.
