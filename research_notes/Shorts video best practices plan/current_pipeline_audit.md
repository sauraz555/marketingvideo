# Current portrait-shorts pipeline audit (repo: motion-video-generator, branch feature/shorts-backdrops-kling)

Method: read the code and docs in the repo; nothing was executed (Playwright is not installed in this audit environment, so no render or sheet was run). "Sources" are `path:line` in the repo at HEAD `2c18c1a`. Statements under "Inferences" are deductions from the code, not tested behaviour.

Abbreviations: `short.html` = `templates/shorts/short.html`; `script.js` = `templates/shorts/script.js`; `README` = `templates/shorts/README.md`; `shorts.py` = `tools/shorts.py`; `director` = `.claude/agents/shorts-director.md`.

---

## 1. What do short.html, script.js and README provide (scene model, config schema, captions, components, presenter, backdrops, transitions, safe zones, themes)?

### Takeaway
The engine is a single 1080x1920 HTML page driven by one paused GSAP timeline, with content in `script.js` (`window.SCRIPT`) and timing from `segments.js` (silence-split voice lines) or explicit seconds. It ships 19 scene builders (including an animated bar chart, count-up number, compare cards, do/don't panel, framed photos, web-source page), phrase-level two-line captions (not word-synced), 3 looks, image/video backdrops and presenter "moves"; there are no safe-zone guides, no transition library and no word-level caption timing.

### Cited Findings

**Stage, runtime, libraries**
- Stage is a fixed 1080x1920 `#stage` scaled into a 9:16 `#viewport` preview (max 430 px wide) — `templates/shorts/short.html:39-40`, `:572`.
- GSAP 3.12.5 loaded from jsDelivr CDN; fonts Poppins (400-900) and Playfair Display (700-900) from Google Fonts CDN — `templates/shorts/short.html:14-16`. No other font families are loaded.
- One paused timeline `TL`; total length `DUR` = `SCRIPT.duration` or `AUDIO_DURATION` (from segments.js) or last scene end + 0.6 s — `templates/shorts/short.html:308`, `:485-486`.
- Layer DOM order (back to front): `#bg` (gradient + 2 blobs), `#pwrap` (presenter video + bottom shade), `#bds` (backdrops), `#grain`, `#vis` (visual lane), `#caps` (caption lane), `#brand` — `templates/shorts/short.html:276-282`.
- Browser preview has Play button, scrub slider, time readout; preview syncs timeline to the `<audio>` element's currentTime — `templates/shorts/short.html:285-286`, `:575-586`.

**Scene / segment model**
- Scenes are a flat array `SCRIPT.scenes`; each has `type` plus timing by `t`/`end` (seconds) or `seg: n` / `seg: [n, m]` (indexes into `window.SEGMENTS`) — `templates/shorts/script.js:3-7`, `templates/shorts/short.html:305-307`.
- Two lanes: `cap`/`title` scenes form the caption lane, everything else the visual lane; any visual may embed its own caption via `cap: {lead, key, ...}`, which is pushed into the caption lane with the visual's timing — `templates/shorts/short.html:490-494`, `templates/shorts/script.js:5-7`.
- End rule: a caption ends when the next scene of either lane starts; a visual ends when the next visual starts (or its own `end`/seg end, whichever is earlier) — `templates/shorts/short.html:496-497`, `:517-518`.
- Each builder returns `{el, inn(tl,t,end), out(tl,t)}`; `out` is skipped for a visual that runs to the end of the video — `templates/shorts/short.html:310`, `:524-525`.

**`window.SCRIPT` schema (every top-level field the engine reads)**
- `look` ('warm' default, 'dark', 'interlace') — `templates/shorts/short.html:294`; `brand` (text handle) or `logo` (image, replaces brand text) — `:298-299`; `audio` — `:300`; `presenter`, `presenterOffset` — `:297`, `:567`; `duration` — `:308`; `scenes` — `:491`; `moves` — `:500-502`; `backdrops` — `:534-536`.
- The template `script.js` only declares `brand, look, audio, presenter, presenterOffset, scenes` — `templates/shorts/script.js:22-28`; `logo`, `duration`, `moves`, `backdrops` are not present or documented there.
- Per-scene common fields: `type`, `t`, `end`, `seg`, `cap`, `pos`, `depth` ('back'/'front' override of layer), `shrink` — `templates/shorts/short.html:306-307`, `:493`, `:516`, `:527`.

**Scene types (builders `B.*`) and their fields**
- `cap {lead, key, hl, pos}` and `title` (= cap with pos 'mid') — `templates/shorts/short.html:312-322`.
- `bignum {value, unit, kicker, badges[]}`: 340 px number, count-up tween 0 -> value over 0.9 s when value is numeric, auto font shrink for values longer than 4 chars, source "chips" — `templates/shorts/short.html:323-335`.
- `stat {value, label}`: dark card, 200 px number (no count-up) — `templates/shorts/short.html:336-342`.
- `compare {items:[{icon, name, value, sub}]}`: side-by-side cards 440 px wide, tilt-in with stagger — `templates/shorts/short.html:343-349`, CSS `:93-98`.
- `pills {title, items[], ok}`: red-cross or green-tick pill list — `templates/shorts/short.html:350-356`.
- `chart {title, items:[{name, value, label, hl}], note}`: vertical bars scaled to the largest value, bars grow with `scaleY` 0->1 (0.7 s, 0.2 s stagger), highlighted bar in accent with others at 40% opacity, source `note` — `templates/shorts/short.html:357-367`, CSS `:114-124`. Bar chart is the only chart type.
- `dosdonts {title, dos[], donts[], gap}`: two columns, items alternate DO/DON'T — `templates/shorts/short.html:368-378`.
- `stamp {text, good, sub}`: slammed rotated stamp with impact shake and flash — `templates/shorts/short.html:379-389`.
- `quote {source, text, mark, by, url, at}`: quote card with a highlighter sweep on the `mark` phrase — `templates/shorts/short.html:390-398`.
- `photo {src | items:[{src, caption, tilt, x, y}], style:'polaroid'|'card', caption, tilt}`: framed image or video, 1 or a 2-3 item collage, drop-in plus gentle float — `templates/shorts/short.html:399-419`, CSS `:154-167`.
- `badges {items:[{value,label}]}` round recap badges — `templates/shorts/short.html:420-425`.
- `list {title, items[], icons[], gap}` numbered rows appearing one by one (default 0.8 s apart) — `templates/shorts/short.html:426-432`.
- `doc {img, marks[]}` paper with highlighter bars; placeholder paper when no image — `templates/shorts/short.html:433-442`.
- `web {img, url, srcWidth, from, to, marks:[{y,h,at,ring}], scrollFor}` browser-window mock with scroll and highlight or ring — `templates/shorts/short.html:443-459`.
- `broll {src}` full-screen image/video with slow zoom-out 1.15 -> 1 — `templates/shorts/short.html:460-466`.
- `hero {icon}` 360 px emoji with bob — `templates/shorts/short.html:467-473`; `cta {icon, text, sub}` — `:474-481`.
- The scene-type comment in `script.js` documents only 12 types (cap, title, bignum, stat, compare, pills, badges, list, doc, broll, hero, cta); `chart`, `dosdonts`, `stamp`, `quote`, `photo`, `web` are not listed there — `templates/shorts/script.js:9-21`. `photo` is documented in README — `templates/shorts/README.md:59-64`; `chart`/`dosdonts`/`web` only in the director brief — `.claude/agents/shorts-director.md:31-37`; `stamp` and `quote` are documented only in code comments — `templates/shorts/short.html:380`, `:391`.

**Caption system**
- A caption is two lines: small `lead` (500 weight, 50 px) and big `key` (800 weight, 112 px, `text-transform:uppercase`), centred, 60 px side margins, default top 1240 px — `templates/shorts/short.html:66-68`.
- Positions: default 1240, `top` 300, `mid` 780, `low` 1440, presenter `ptop` 230 and `plow` 1500 — `templates/shorts/short.html:71-72`, `:211`, `:218-219`.
- `hl: true` puts the whole key in an accent-colour box and animates it as one block; otherwise the key is split into `.w` word spans that pop in with a fixed 0.07 s stagger — `templates/shorts/short.html:69`, `:313-319`.
- Captions are timed at scene level only (scene start from `t` or segment start); the word stagger is a fixed animation constant, not tied to spoken-word times — `templates/shorts/short.html:306`, `:319`.
- Key font auto-shrinks by character count (<=9: 112 px, <=12: 96, <=15: 80, else 66) "so they stay on one line" — `templates/shorts/short.html:521-522`.
- Caption colour is `--capink` (ink on plain backgrounds); switches to white with a drop shadow when a presenter (`data-presenter`) or a backdrop (`data-bd`) is active — `templates/shorts/short.html:22`, `:35`, `:264`, `:552-554`.
- Caption exit: fade + 20 px rise over 0.2 s — `templates/shorts/short.html:320`.
- README caption rules: key is 1-3 words, uppercase; `hl` for "the one word that matters"; captions summarise rather than translate (Nepali voice + English captions) — `templates/shorts/README.md:34-39`. The director brief says key 2-5 words, lead 3-6 words — `.claude/agents/shorts-director.md:30`.

**Presenter modes and moves**
- Setting `SCRIPT.presenter` shows the clip full-frame (`object-fit:cover`) with a bottom shade, hides the blobs, and switches captions to white — `templates/shorts/short.html:51-55`, `:297`, `:35`.
- Presenter layout overrides move/scale every scene type into zone A (above the head) or zone B (lower third, top ~1040-1260 px), "the face stays clear" — `templates/shorts/short.html:217-240`.
- Auto caption placement with a presenter: `ptop` normally; `plow` when the concurrent visual is bignum/hero/badges or during an anchor move — `templates/shorts/short.html:498-509`.
- Depth: each element gets class `back` or `front` (cap/title/bignum/hero/badges go behind the person, other visuals in front), used by the layered render — `templates/shorts/short.html:213-216`, `:499`, `:516`.
- `SCRIPT.moves`: `{t, end, mode:'anchor', scale:.6, side:'right'|'left'|'center'}` (cut-out person shrinks to a bottom corner, graphics use the space and go behind) and `{t, mode:'punch', amount:.12}` (quick camera zoom-in); applied to the footage by `tools/shorts.py`, not by the page — `templates/shorts/short.html:500`, `:523`, `:242-254`; `tools/shorts.py:343-372`.
- In-page "card shrink": for builders flagged `card:true` (only `pills` and `cta`) and `shrink === true`, the presenter wrapper scales to 0.56 with a 60 px radius — `templates/shorts/short.html:352`, `:476`, `:526-530`. README says "list and CTA scenes shrink the footage into a card" — `templates/shorts/README.md:7`; the `list` builder has no `card` flag — `templates/shorts/short.html:426-432`.

**Backdrops**
- `SCRIPT.backdrops = [{src, t, end, zoom:[1,1.14], pan:'left'|'right'|'up'|'down', dim:.38, blur:0, fadeIn:.45, fadeOut:.45, focus:[from,to]}]` — `templates/shorts/short.html:534-550`.
- Image or video (mp4/webm/mov/m4v, muted, looped to fill its slot); linear zoom, +/-3% pan, `focus` drifts `object-position` across a wide image; dim overlay `rgba(6,16,36,dim)`; optional CSS blur — `templates/shorts/short.html:537-550`, `:568`.
- Crossfade is done by overlapping two entries by 0.45 s (authoring convention) — `templates/shorts/README.md:48`, `.claude/agents/shorts-director.md:49`.
- In the in-page (non-layered) view, backdrops are hidden whenever a presenter is set — `templates/shorts/short.html:260`; with a presenter + matte they are rendered as their own `bd` layer and replace the room — `templates/shorts/short.html:261-263`, `tools/shorts.py:316-317`, `:389`.

**Transitions / motion**
- All transitions are per-builder enter/exit tweens (fade, slide, scale, `back.out` overshoot, tilt); no shared scene-to-scene transition (wipe, whip-pan, zoom-through) exists — `templates/shorts/short.html:311-482`.
- Background blobs drift over the whole duration; a static SVG noise grain at 6% opacity — `templates/shorts/short.html:47-48`, `:487-488`.

**Safe zones**
- Hard-coded positions only: brand at top 70 px, captions 60 px left/right, default caption top 1240, lowest preset `plow` 1500 — `templates/shorts/short.html:63`, `:66`, `:219`.
- No safe-zone overlay, guide layer or constants for platform UI (TikTok/Reels/Shorts) exist in the engine; a case-insensitive search of `short.html` for "safe" returns no matches (file also read in full, lines 1-590).
- The only written rule is in the director QA step: "nothing sits in the bottom 150 px except captions" — `.claude/agents/shorts-director.md:78`.

**Looks / colours**
- `warm` (root defaults: beige `#F1E6D8`, orange accent `#FF7A1A`), `dark` (`#17120F`), `interlace` (white/pastel blue, primary `#3267AD`, Playfair Display numerals) via `data-look` and CSS variables — `templates/shorts/short.html:18-34`.
- Semantic colours: good `#1F9D55`, bad `#E5484D` — `templates/shorts/short.html:22`.

### Inferences
- Captions are phrase-level (one lead + one key per scene). Word-by-word "karaoke" captions synced to speech are not possible with the current data model because no word timestamps exist anywhere in the pipeline (see sections 2 and 4).
- Because `key` is forced uppercase and only Poppins/Playfair (Latin) are loaded, the `caption_language: nepali` config option (`tools/shorts.py:40`) would render Devanagari in a system fallback font; no Devanagari webfont is loaded (`templates/shorts/short.html:15`).
- The template `script.js` defaults to `look: 'warm'` (`templates/shorts/script.js:24`) while the setup default is `interlace` (`tools/shorts.py:44`); nothing copies the config answer into `script.js`, so the two can disagree.
- The emoji used for `hero`, `compare` icons, `cta` and the web lock icon render with whatever emoji font the rendering machine has, so appearance can differ between machines (no emoji font bundled; `templates/shorts/short.html:15`, `:447`, `:468`).
- CSS `.chart .nm` (`templates/shorts/short.html:121`) is not emitted by the chart builder (`:360`), i.e. dead style.

### Gaps
- Could not visually confirm layouts (no render run); overlap/clipping behaviour of each scene type in presenter mode is unverified.

---

## 2. What does tools/shorts.py do in each subcommand?

### Takeaway
`shorts.py` has 8 subcommands (new, config, backdrop, segments, sheet, render, capture, frames). Voice timing is derived only from ffmpeg `silencedetect`; rendering is per-frame Playwright PNG screenshots at 30 fps encoded with libx264 CRF 14, with a 3-layer ffmpeg composite when a presenter matte exists; the only external network use in the tool itself is loading the page CDNs and, for `capture`, the target public URL. No generator (Kling etc.), ASR or TTS service is called from this file.

### Cited Findings

**Dispatch** — subcommands: `new, segments, sheet, render, capture, frames, config, backdrop` — `tools/shorts.py:617-618`. CLAUDE.md lists only "config / new / segments / capture / sheet / render" — `CLAUDE.md` (project instructions, last bullet).

**config**
- 14 questions with keys: `voice_language, caption_language, voice_source, voice_name, presenter, look, backdrop_mode, backdrop_tool, backdrop_budget, length_seconds, music, logo, sources, privacy` — `tools/shorts.py:38-53`.
- Defaults: voice "nepali + english mix", captions "english", voice source "i provide an audio file", presenter "no", look "interlace", backdrop_mode "images", backdrop_tool "auto (use what I have)", budget "free only", length "45-60", music "none", logo "logo.png", sources "yes", privacy "no client names" — `tools/shorts.py:39-52`.
- Stored in `projects/<name>/config.json` as `{status: 'needs-setup'|'ready', answers:{...}}`; `voice_name` is the only optional key — `tools/shorts.py:54-74`.
- Flags: `--interactive`, `--set KEY=VALUE` (repeatable), `--redo`; exits 1 while answers are missing — `tools/shorts.py:604-607`, `:116-120`.
- The config is only consulted by `warn_config` (a stderr warning in `sheet` and `render`) — `tools/shorts.py:110-113`, `:278`, `:420`. No other code path reads `answers`.

**new**
- Copies `templates/shorts/` (minus README.md and segments.js) to `projects/<name>/`, creates `output/`, copies `--voice` to `voice.mp3` and `--presenter` to `presenter.<ext>`, writes an empty config, asks the questions if stdin is a TTY, then runs `segments` — `tools/shorts.py:169-187`.

**segments (voiceover timing)**
- Runs `ffmpeg -af silencedetect=noise=<-35>dB:d=<0.35>` on `voice.mp3`, turns the gaps between silences into `[start, end]` pairs (ignoring spans shorter than 0.15 s), and writes `segments.js` with `window.AUDIO_DURATION` and `window.SEGMENTS` — `tools/shorts.py:191-214`; defaults `--noise -35`, `--min-pause 0.35` — `:590-591`.
- Requires `voice.mp3` to exist (exits otherwise) — `tools/shorts.py:194-195`.

**backdrop (added in HEAD commit)**
- Three modes, all local: (a) default: numpy/PIL colour-mesh PNG 1080x1920 (Gaussian colour blobs, vignette, noise) -> `media/backdrop-mesh.png`; (b) `--video`: ffmpeg lavfi `gradients` source, 1080x1920, 30 fps, default 12 s, libx264 CRF 16 -> `media/backdrop-video.mp4`; (c) `--from-video clip --at 1.0`: one frame scaled/cropped to 1080x1920 JPEG — `tools/shorts.py:129-165`, args `:608-613`.
- Default colours are deep blues `#0B1F3F,#1E4E8C,#3B82C4,#0A1530` — `tools/shorts.py:610`.
- It writes the file only; it does not add the entry to `script.js` (prints "add it to backdrops in script.js") — `tools/shorts.py:165`.

**sheet (QA contact sheet)**
- Opens the page at 1080x1920, samples one screenshot ~0.9 s after each timeline child start (deduplicated to >0.8 s apart) plus the last frame, JPEG q80, tiles 6 columns of 270x480 thumbnails with a time label -> `projects/<name>/qa/sheet.jpg` — `tools/shorts.py:245-274`.

**render**
- Args: `--fps` (default 30), `--music`, `--music-vol` (0.18), `--workers` (4 parallel browsers), `--from/--to` (test cut, presenter + matte mode only), `--crf` (default 14) — `tools/shorts.py:593-598`.
- Page setup: viewport 1080x1920, waits for `document.fonts.ready` + 1.2 s, strips preview chrome, pauses TL — `tools/shorts.py:218-237`.
- Frame capture: for each frame `TL.seek(t)` then `await window.seekMedia(t)` (seeks presenter/backdrop/photo videos and waits for `seeked`, 3 s timeout), then `page.screenshot` PNG; frames are interleaved across workers — `tools/shorts.py:240-241`, `:283-304`; `templates/shorts/short.html:560-570`.
- Presenter playback in the browser tries Edge then Chrome channels because "bundled Chromium cannot decode H.264" — `tools/shorts.py:218-227`.
- Plain path (no presenter, or presenter without matte): PNG sequence -> `libx264 -preset slow -crf 14 -pix_fmt yuv420p -profile:v high -x264-params aq-mode=3` — `tools/shorts.py:437-441`.
- Layered path (presenter + `*matte*.mkv` in the project): the page is opened with `?alpha=1` (transparent stage, background/presenter/grain hidden) and each frame is screenshotted up to 3 times with `omit_background` for layers `bd`, `back`, `front` — `tools/shorts.py:307-335`, `templates/shorts/short.html:213-216`, `:261-263`, `:296`.
- Composite order in ffmpeg: presenter footage (graded `eq=contrast=1.04:saturation=1.06`) -> [backdrop layer] -> top/bottom darkening gradient PNG -> [blurred, darkened copy of the footage during anchor moves when no backdrop covers them] -> back graphics -> cut-out person (alphamerge of footage and matte, scaled/offset for anchor moves) -> front graphics -> yuv420p; libx264 preset slow, profile high — `tools/shorts.py:343-415`.
- Move maths: anchor uses a smoothstep pulse with D = 0.45 s, default scale 0.6, bottom-aligned, side offset; punch ramps in over 0.18 s and eases out over 0.75 s, default amount 0.12 — `tools/shorts.py:338-372`.
- Footage shorter than the voiceover holds its last frame (`tpad stop_duration=60`) — `tools/shorts.py:383`.
- Audio mux: `voice.mp3` -> AAC 256 kb/s; with `--music` the track is looped, set to volume 0.18, faded out over the last 2 s, sidechain-compressed by the voice (threshold 0.03, ratio 8, attack 20 ms, release 400 ms) and mixed with `amix normalize=0`; video stream copied, `-movflags +faststart`, trimmed to `dur` — `tools/shorts.py:442-460`.
- Output: `projects/<name>/output/<name>-1080x1920.mp4`; test cut `<name>-test.mp4` without audio — `tools/shorts.py:431-436`, `:442`.
- Frames scratch: `frames/short-<name>/` (cleared each render) — `tools/shorts.py:421-424`.

**capture (source screenshots)**
- Loads a public URL in a phone-like context (430 px CSS width, device scale 3, Android Edge UA, locale en-AU), clicks "Decline/Reject/Accept only essential" consent buttons, collects up to 12 headings, finds the deepest element containing `--find`, screenshots a clip around it (240 px above, 700 px below) and writes `<shot>.png` + `<shot>.json` containing a ready `web` scene with the highlight mark — `tools/shorts.py:464-544`.

**frames (reference video grid)**
- Cuts a reference video at one frame per `--every` seconds, pads to 1080x1920 and writes `ref/grid-sheet.jpg` with a 240 px y-grid (red, labelled) and 270 px x-grid (blue) — `tools/shorts.py:548-581`.

### Inferences
- `render` ignores the music track when there is no `voice.mp3`: the `--music` branch sits inside `if voice.exists()` (`tools/shorts.py:446-457`), so the config option "no voice (captions and music only)" (`tools/shorts.py:41`) yields a silent MP4. Also `segments` cannot run without a voice file (`:194-195`), so such a project must use explicit `t`/`end` seconds.
- "The presenter's own audio" option has no code path: nothing extracts audio from `presenter.mp4` into `voice.mp3`; the mux uses only `voice.mp3` (`tools/shorts.py:444-447`). It would need a manual ffmpeg step.
- The composite never scales the presenter footage to 1080x1920 (filter at `tools/shorts.py:384` has fps/tpad/eq only; crop to 1080x1920 happens only when punches exist, `:370`), so presenter clips are assumed to already be 1080x1920; other sizes would misalign with the 1080x1920 graphic layers.
- `tpad stop_duration=60` implies a presenter clip more than 60 s shorter than the voiceover would run out of frames (`tools/shorts.py:383`).
- In presenter-without-matte mode, `moves` (anchor/punch) are not applied to the footage (only `composite` reads them, `tools/shorts.py:429-430`), but the page still applies anchor layout classes and `plow` captions for those time ranges (`templates/shorts/short.html:508`, `:523`), so the layout would change without the person shrinking.
- `--from/--to` are silently ignored in the non-layered path (`tools/shorts.py:437-438` passes no start/end).
- The `sheet` command screenshots the non-alpha page, so for presenter + matte projects the QA sheet shows the in-browser presenter view (no cut-out layering, no backdrop: `#bds` hidden at `short.html:260`), which differs from the final composite.
- `sheet` does not collect page errors or failed asset loads (unlike `tools/frames.py:20-22`), so a missing image or CDN failure is only visible by eye.
- Loudness is not normalised in the shorts mux (no `loudnorm` in `tools/shorts.py`; the only `loudnorm` in the repo is `tools/vo.py:124`).
- Encoder output is 8-bit 4:2:0 H.264 with no explicit bitrate cap, colour tags (bt709) or audio sample-rate setting (`tools/shorts.py:413-414`, `:439-441`, `:457-458`).
- Rendering needs internet for GSAP/fonts (CDN links at `templates/shorts/short.html:14-16`; root README states this for the repo, `README.md:48`).

### Gaps
- Render speed, output bitrate/file size and actual visual quality were not measured (no render executed).
- Whether headless Edge/Chrome channels exist on the user's machines (needed for H.264 presenter/backdrop video decode) is environment-specific and unknown; README example paths suggest Windows (`templates/shorts/README.md:13`).

---

## 3. What does tools/matte.py do?

### Takeaway
`matte.py` runs Robust Video Matting (MobileNetV3, ONNX, CPU) locally and writes a lossless grayscale FFV1 `.mkv` matte at the source resolution and frame rate; `shorts.py render` merges it with the footage via ffmpeg `alphamerge`. Model weights are not in the repo and no download instructions exist.

### Cited Findings
- Model: `tools/models/rvm_mobilenetv3_fp32.onnx`, onnxruntime `CPUExecutionProvider`, recurrent states carried across frames — `tools/matte.py:7`, `:13`, `:42-46`, `:62`.
- Input: any video ffmpeg can decode; frames are scaled to `--width` (default 720) for inference with `downsample_ratio` `--ratio` 0.375; `--seconds N` limits to the first N seconds — `tools/matte.py:29-31`, `:38-39`, `:48-49`.
- Output: alpha upscaled to source WxH with bicubic resize, 5x5 Gaussian blur on the edge, written as gray FFV1 at source fps to `<stem>-matte.mkv` (default) — `tools/matte.py:34`, `:50-51`, `:64-67`.
- Alpha transport: the matte is a separate video file; `render` picks the first `*matte*.mkv` in the project and uses `[vb][mv]alphamerge` — `tools/shorts.py:426`, `:385-386`. The page itself never sees alpha video.
- Script exits if the model file is missing — `tools/matte.py:35-36`. `tools/models/` is git-ignored with the comment "download separately, see templates/shorts/README.md" — `.gitignore:19-20`; the README contains no download instruction (only mentions "the cut-out model" as optional) — `templates/shorts/README.md:74`. `tools/models/` does not exist in the checkout.
- Dependencies numpy, opencv-python, onnxruntime are marked optional — `requirements.txt:4-7`.

### Inferences
- Only the alpha (`pha`) output is used; RVM's predicted foreground (`fgr`) is discarded (`tools/matte.py:62-64`), so there is no colour decontamination/despill of edges; the original footage pixels are used under the matte.
- No temporal smoothing, erosion/choke or edge feathering control beyond the fixed 5x5 blur; no GPU provider option; the larger RVM ResNet50 model is not supported by a flag (path is hard-coded, `tools/matte.py:13`).
- No hard resolution/fps limit is coded; speed is CPU-bound and printed as fps progress (`tools/matte.py:69-71`).

### Gaps
- Matte quality on real footage (hair, hands, fast motion) is unverified; no sample footage or matte exists in the repo.
- Where the user obtains the ONNX weights is undocumented.

---

## 4. What do tools/vo.py, tools/render.py and tools/frames.py do that the shorts pipeline relies on?

### Takeaway
The shorts pipeline does not call any of the three; they serve the 16:9 explainers. `vo.py` (ElevenLabs TTS) is structurally incompatible with `short.html`, and it does not request character/word timestamps, so no word-level timing exists anywhere in the repo.

### Cited Findings
- `vo.py gen` calls ElevenLabs `POST /v1/text-to-speech/{voice}?output_format=mp3_44100_128` (model `eleven_multilingual_v2`, default voice "Charlie, Australian English", speed 1.0), one clip per caption with `previous_text`/`next_text` context, cached in `vo/clips.json` — `tools/vo.py:18-21`, `:40-44`, `:70-85`. Key read from `ELEVENLABS_API_KEY` env only — `tools/vo.py:59`.
- Timing in `vo.py` comes from each clip's duration via ffprobe and is written as `const WARP=[...]` anchors that stretch the page timeline; it parses `const DUR=` and `const CAP=[...]` from the page — `tools/vo.py:25-30`, `:36-38`, `:87-99`. It does not use the ElevenLabs `with-timestamps` endpoint (API URL at `:18`).
- `vo.py mux` places clips with `adelay`, mixes, applies `loudnorm=I=-16:TP=-1.5:LRA=11`, AAC 192k — `tools/vo.py:122-130`.
- `short.html` has no `const CAP`, `const DUR=` literal or `const WARP` (it uses `window.SCRIPT` and `window.DUR`) — `templates/shorts/short.html:292-308`; so `vo.py gen` would fail on a short at `tools/vo.py:27-28`.
- `render.py`: single browser, JPEG q93 frames, viewport follows stage size ("1080x1920 for portrait"), `libx264 -crf 18`, FPS from env (default 30), no audio; seeks only `TL` and CSS animations, not media elements — `tools/render.py:13`, `:26-28`, `:36-41`, `:64-65`.
- `frames.py`: contact sheets at chosen times / `--every` / `--scenes` (needs a `SCN` array), reports page errors, failed requests and HTTP >= 400 — `tools/frames.py:20-22`, `:30-33`, `:63-72`.
- `.claude/settings.json` pre-allows `tools/frames.py`, `tools/render.py`, `vo.py mux`, ffmpeg and ffprobe; `tools/shorts.py` and `tools/matte.py` are not in the allow list — `.claude/settings.json:3-12`.
- `shorts.py` imports neither tool; its voice config option says "generate it with a voice service I have (e.g. ElevenLabs)" — `tools/shorts.py:17`, `:41`.

### Inferences
- For shorts, generated voice has no scripted path: the director would have to produce a single `voice.mp3` by some other means (e.g. an ElevenLabs tool in the session) and then run `segments`. Caption-to-speech alignment then depends on silence detection matching the script's line breaks.
- `frames.py <short.html> --every N` would work on a short (it only needs `TL`, `fit`, `stage`), and would add the asset-failure report that `shorts.py sheet` lacks; `--scenes` would fail (`SCN` undefined in `short.html`).

### Gaps
- None material; all three files were read in full.

---

## 5. What do shorts-director.md, style.md and qa-checklist.md instruct?

### Takeaway
The director brief encodes a workflow (configure -> tool inventory -> research -> capture -> optional reference matching -> build -> sheet QA -> render -> frame spot-check) and several attention heuristics, all as prose for the agent; none are enforced by code. `style.md` and `qa-checklist.md` are written for 1920x1080 explainers; only their content rules (real numbers, exact labels, one idea per caption) transfer.

### Cited Findings

**shorts-director.md**
- Agent tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch; it edits `script.js` only, never the engine unless asked — `.claude/agents/shorts-director.md:4`, `:7`.
- Step 0: run `config`, ask unanswered questions in chat 3-4 at a time, save with `--set`, never spend beyond the limit, re-read config each session — `.claude/agents/shorts-director.md:11-16`.
- Tool inventory and graceful fallbacks for missing generator / voice / browser / cut-out model — `.claude/agents/shorts-director.md:18-24`.
- Director's brief: hook in 0-2 s (question, big number or "this affects you if..."; never a logo or greeting); new visual every 3-5 s; bigger pattern break every 8-10 s; no same scene type twice in a row; one hero word per caption; scene-type selection table; a source on screen for every factual claim; last 3 s one CTA also spoken; loop-friendly first/last captions — `.claude/agents/shorts-director.md:26-40`.
- Backdrops: "never leave the background plain"; one per story phase (5-12 s); avoid faces, readable text and logos in generated media; price first (`estimate_only`); insist on 9:16 in generator settings; `focus` pan for 16:9 results; crossfade by 0.45 s overlap; last one `fadeOut: 0`; frame key photos over a blurred copy; only media you have rights to; do not pass generated pictures off as real — `.claude/agents/shorts-director.md:42-53`.
- Kling instructions (MCP-style tool names `who_am_i`, `query_membership_and_credits`, `text_to_image` default `kling-image-v3_0_omni`, `text_to_video` default `kling-video-v4_0` 3-30 s 720p/1080p, `aspect_ratio: "9:16"`, `image_to_video` needs a public URL) — `.claude/agents/shorts-director.md:46`.
- Research: every number/date/rule from an official page with URL and exact sentence; public pages only — `.claude/agents/shorts-director.md:59-62`.
- Reference matching via `frames` grid sheet — `.claude/agents/shorts-director.md:68-71`.
- QA: read `qa/sheet.jpg` and check "no caption on top of a graphic, no text cut off at the edges, long numbers fit, each web highlight lands on the right sentence, nothing sits in the bottom 150 px except captions"; repeat until clean; after render check one frame every 10 s with ffmpeg — `.claude/agents/shorts-director.md:76-80`.
- Return format: storyboard table, sources, files, open questions — `.claude/agents/shorts-director.md:82-86`.

**style.md / qa-checklist.md (explainer skill)**
- Frame: 1920x1080, 30 fps, H.264 CRF 18, 60 px safe margin, reserved bottom caption band, Plus Jakarta Sans — `.claude/skills/explainer-video/style.md:6-8`.
- Caption rules: one idea, <= ~80 characters, 3.5-5 s on screen (~2.5 words/s), exact UI labels, real numbers only, no abbreviations the voice cannot read — `.claude/skills/explainer-video/style.md:44-50`.
- QA checklist: no `PROBLEM` lines, nothing cut off (60 px margin), numbers traceable, timing checks, ffprobe confirms 1920x1080 — `.claude/skills/explainer-video/qa-checklist.md:5-30`.
- CLAUDE.md repo-wide rules that apply to shorts: captions are the voiceover script, English unless asked, real numbers only, exact UI labels; no keys in commands/files; `_archive/` not to be used; never change data in filmed apps — `CLAUDE.md` (bullets 4-7).

### Inferences
- The explainer caption pacing (3.5-5 s, <= 80 chars, bottom band) conflicts with the shorts style (1-3 word uppercase key, new visual every 3-5 s); there is no shorts-specific style.md or qa-checklist.md, so shorts QA criteria live only in one sentence of the director brief (`.claude/agents/shorts-director.md:78`).
- The director is told not to open on a logo, yet `#brand`/logo is shown from frame 0 at top 70 px for the whole video (`templates/shorts/short.html:63`, `:298-299`); this is a persistent watermark rather than an opening card, so it is not a direct contradiction, but it is never animated or hidden.
- Heuristics such as "no same scene type twice in a row", "visual change every 3-5 s", "hook in 2 s" are not checked by any tool; compliance depends on the agent.
- Kling tool names in the brief imply an MCP connector in the session; nothing in the repo configures such a connector (`.claude/settings.json:1-14` has permissions only).

### Gaps
- `.claude/skills/explainer-video/SKILL.md` was only grepped (no shorts/portrait mentions found), not read in full.

---

## 6. Are there existing shorts projects under projects/?

### Takeaway
No project built with the shorts engine exists. The only portrait asset is a hand-built 1080x1920 cut of an older bumper, which does not use `templates/shorts`.

### Cited Findings
- Projects present: `genuine-solutions-bumper`, `interlace-promo`, `migration-eoi-analysis`, `migration-occupation-detail`, `signature-template-builder` — `README.md:23-28` and directory listing.
- No project contains `short.html`, `script.js`, `segments.js` or `config.json` (file search of `projects/` to depth 2 found none).
- `projects/genuine-solutions-bumper/index-60s-portrait.html` has its own 1080x1920 stage in Plus Jakarta Sans (not the shorts engine) — `projects/genuine-solutions-bumper/index-60s-portrait.html:26`, `:666`; rendered output `genuine-bumper-60s-portrait-1080x1920.mp4` is listed — `projects/genuine-solutions-bumper/README.md:9`.
- The first shorts commit states "No media, footage or client material" was added — commit `e922b7e` message.
- `_archive/` (third-party reference videos) is git-ignored and absent from this checkout — `.gitignore:4-5`.

### Inferences
- The shorts engine has no committed reference output, so "what good looks like" for shorts is defined only by prose (README "match the reference style", `templates/shorts/README.md:34`) and by reference videos that are not in the repo.
- The engine and director defaults (Nepali voice, Australian migration sources, `en-AU` locale) indicate the intended first use case is Interlace migration-education shorts (`tools/shorts.py:39`, `:480`; `.claude/agents/shorts-director.md:56`, `:60`).

### Gaps
- The portrait bumper HTML was not read beyond a grep; its techniques were not audited.

---

## 7. What is in the two most recent commits on feature/shorts-backdrops-kling, and what is stubbed or half-finished?

### Takeaway
`e922b7e` added the whole shorts system (1,434 lines across 9 files); `2c18c1a` made backdrops optional (auto/free defaults), added the local `backdrop` command and docs. Kling "integration" is instructions in the agent brief only: there is no Kling (or other generator) API code in the repo. There are no TODO/FIXME markers, but several documented features have no code path.

### Cited Findings
- Branch state: only `feature/shorts-backdrops-kling` exists locally and on origin (no `main` ref in this clone); HEAD = `2c18c1a`, parent `e922b7e`; working tree clean — `git branch -a`, `git status`.
- `e922b7e` (Mon Nov 16 2026 18:19 +1000) added `.claude/agents/shorts-director.md` (80 lines), `templates/shorts/{README.md 64, script.js 44, short.html 590}`, `tools/matte.py` (78), `tools/shorts.py` (569), and edited `.gitignore`, `CLAUDE.md`, `requirements.txt` — `git log -2 --stat`.
- `2c18c1a` (18:29 +1000) changed 3 files (+80/-8): `tools/shorts.py` (+`cmd_backdrop`, new `backdrop` parser, reworded `voice_source`/`voice_name`/`backdrop_tool`/`backdrop_budget` questions and defaults), `templates/shorts/README.md` (fallback table, free-backdrop example), `.claude/agents/shorts-director.md` ("Tools: use what exists" section; Kling only "if the session has it and the person chose it or left the tool on auto") — `git show 2c18c1a`.
- Config default changes in `2c18c1a`: `backdrop_tool` default `kling` -> `auto (use what I have)`; `backdrop_budget` default `ask me before spending` -> `free only`; new voice option "no voice (captions and music only)" — `git show 2c18c1a` (diff of `tools/shorts.py` lines 38-49).
- The `2c18c1a` message says it "Adds the photo (framed) scene and video backdrops", but that commit does not touch `short.html`; the `photo` builder and video backdrops were already in `e922b7e`'s `short.html` — `git show 2c18c1a --stat`; `templates/shorts/short.html:399-419`, `:537-538`.
- No `TODO`, `FIXME`, `XXX`, "stub" or "not implemented" strings in `tools/`, `templates/shorts/` or the director brief (grep returned nothing).
- The strings "kling", "higgsfield", "bloom", "elevenlabs" occur in `tools/shorts.py` only as config choice labels — `tools/shorts.py:41`, `:46`; they do not occur in `tools/matte.py`, `short.html` or `script.js`.

### Inferences (half-finished or inconsistent items)
- Kling: prose-only (`.claude/agents/shorts-director.md:46`). No client, no credit check, no download/save helper, no aspect-ratio verification or auto-crop of returned media in code. The branch name overstates the integration.
- `config.json` answers are not consumed by the engine or renderer (`tools/shorts.py:110-113` is the only reader besides `config`), so `look`, `logo`, `music`, `length_seconds`, `privacy`, `sources` are advisory for the agent; nothing validates the final video against them (e.g. length 45-60 s).
- "no voice (captions and music only)" and "the presenter's own audio" have no implementation in `render`/`segments` (see section 2 inferences).
- `.gitignore:19` points to README for model download instructions that are not there (`templates/shorts/README.md` has none).
- `templates/shorts/script.js` was not updated for the later features: its header omits 6 scene types and the `backdrops`/`moves`/`logo` keys, and its look comment lists only warm/dark (`templates/shorts/script.js:9-28`).
- README line 7 claims list scenes shrink the presenter into a card; code does this only for `pills`/`cta` with `shrink: true` (`templates/shorts/short.html:526-530`).
- `CLAUDE.md` and root `README.md` do not mention the `backdrop` and `frames` subcommands, and root `README.md:11-33` does not mention shorts at all.
- `.claude/settings.json` has no allow rule for `python tools/shorts.py` or `tools/matte.py`, so each run would prompt for permission.
- The two commits were made 10 minutes apart with no shorts project or rendered output committed, which suggests the pipeline has not yet been exercised end-to-end inside this repo history (inference from `git log` and section 6).

### Gaps
- Whether the code was tested outside the repo (e.g. on the author's machine with uncommitted projects) cannot be determined from the repo.

---

## 8. Explicit gaps: things commonly expected in shorts that are absent

### Takeaway
The engine is strong on designed data graphics and presenter compositing but lacks word-level captions, any transcription/alignment, platform safe-zone guides, SFX, loudness normalisation, hook/structure templates in code, and automated QA rules; several items are present in a basic form only (one chart type, a count-up, simple music ducking).

### Cited Findings (present, for calibration)
- Present: animated bar chart — `templates/shorts/short.html:357-367`; count-up number — `:330-331`; comparison cards — `:343-349`; do/don't panel — `:368-378`; music bed with sidechain ducking and end fade — `tools/shorts.py:448-454`; QA contact sheet — `tools/shorts.py:245-274`; reference-video pixel grid — `tools/shorts.py:548-581`; presenter cut-out layering and punch-ins — `tools/shorts.py:343-415`; hook/rhythm/CTA guidance as prose — `.claude/agents/shorts-director.md:26-40`.

### Inferences (absent or partial; each is "no code found" after reading the cited files in full)
Captions
- No word-by-word / karaoke captions synced to speech: caption timing is per scene, word stagger is a fixed 0.07 s (`templates/shorts/short.html:319`).
- No transcription or forced alignment (no Whisper/ASR, no ElevenLabs timestamps; grep for `whisper|timestamps|srt|vtt` in `tools/` and `templates/shorts/` returned nothing). Timing relies on `silencedetect` (`tools/shorts.py:197-198`), which splits on pauses, not on sentences or words.
- No full-transcript subtitle mode (verbatim running captions) and no SRT/VTT export for platform closed captions; captions are author-written summaries (`templates/shorts/README.md:39`).
- No active-word highlight colour change, no per-word emphasis styles beyond a single `hl` box for the whole key (`templates/shorts/short.html:69`, `:314`).
- No caption background/stroke option for legibility beyond a drop shadow (`templates/shorts/short.html:35`); no automatic contrast check against backdrops.
- No Devanagari (or other non-Latin) font despite a Nepali caption option (`templates/shorts/short.html:15`; `tools/shorts.py:40`).
- No max-characters-per-line or reading-speed validation; only a length-based font shrink (`templates/shorts/short.html:521-522`).

Graphics
- Charts: vertical bars only; no line/area, horizontal bar, pie/donut, progress ring, stacked or before/after chart; no axis ticks or gridlines; negative values unsupported (heights are `value/max`, `templates/shorts/short.html:359-360`).
- Count-up exists only in `bignum`; `stat`, `badges`, `chart` value labels and `compare` values are static text (`templates/shorts/short.html:337`, `:360`, `:421`, `:344`).
- Comparison layouts: cards side by side only; no versus/split-screen, table, timeline, map, before/after slider, ranking/leaderboard or progress/step-tracker component.
- No icon set (emoji only, `templates/shorts/short.html:468`, `:344`), no SVG/Lottie support, no lower-third name tag, no progress bar / chapter indicator, no end card with handle/follow animation beyond `cta`.
- No scene-to-scene transitions and no kinetic-typography presets beyond the per-builder entrances (`templates/shorts/short.html:311-482`).

Safe zones and layout
- No platform safe-zone constants or overlay (TikTok/Reels/Shorts UI areas) in the engine or the sheet; the QA sheet draws no guides (`tools/shorts.py:263-273`). The only rule is the "bottom 150 px" sentence (`.claude/agents/shorts-director.md:78`).
- Default caption top 1240 px and `plow` 1500 px (`templates/shorts/short.html:66`, `:219`) are fixed values with no documented relation to platform UI.
- No multi-aspect export (1:1, 4:5, 16:9) or per-platform variants; output is always 1080x1920 (`tools/shorts.py:228`, `:442`).

Audio
- No loudness normalisation or true-peak limiting in the shorts mux (`tools/shorts.py:445-459`); contrast `tools/vo.py:124`.
- No sound effects (whoosh/pop/impact) tied to scene entrances; no SFX library or cue mechanism in `script.js`.
- Music: user-supplied file only (`tools/shorts.py:49`, `:594`), no beat detection/sync, no library; ignored when there is no voice (section 2).
- No voice clean-up (denoise, EQ, compression, silence trimming/pacing tighten) and no speed control.
- No TTS path for shorts (`tools/vo.py` is explainer-only, section 4).

Structure / content
- No hook templates, script templates or structure presets in code; `script.js` is a single demo timeline (`templates/shorts/script.js:28-43`).
- No length enforcement against `length_seconds` (`tools/shorts.py:48`), no pacing report (seconds per scene, visual-change frequency), no check for repeated scene types.
- No thumbnail/cover-frame export, no title/description/hashtag output, no A/B hook variants.

QA / automation
- No automated QA rules: no overflow/clipping detection, overlap detection between caption and visual lanes, contrast check, safe-zone check, missing-asset report or duration check; QA is a human/agent reading `sheet.jpg` (`.claude/agents/shorts-director.md:78`).
- No ffprobe post-render verification step in the tool (resolution, fps, duration, audio presence, loudness); the brief only asks for a frame every 10 s (`.claude/agents/shorts-director.md:80`).
- No tests, no example project, no shorts-specific style guide or checklist files (section 5, 6).

Presenter
- No auto-reframe/face tracking for landscape footage, no face-position detection to keep graphics off the face (zones are fixed CSS, `templates/shorts/short.html:217-240`), no jump-cut/silence removal, no automatic punch-ins from speech emphasis (moves are hand-authored, `templates/shorts/short.html:500`).
- Matte uses the small MobileNetV3 RVM on CPU with fixed edge blur; no quality tiers or despill (section 3).

Generators
- No code integration with Kling/Higgsfield/Bloom/ElevenLabs for backdrops; no cost ledger enforcing `backdrop_budget` (`tools/shorts.py:47` is a free-text answer).

Rendering / delivery
- CDN dependency for GSAP and fonts at render time (`templates/shorts/short.html:14-16`); no vendored copies.
- No explicit colour tagging, bitrate ceiling or platform upload presets; CRF 14 "visually lossless" default (`tools/shorts.py:598`) will produce large files (size not measured).
- 60 fps is possible via `--fps` but presenter footage is resampled with ffmpeg `fps=` (`tools/shorts.py:384`); no motion-blur option.

### Gaps
- This list is derived from reading code, not from a platform best-practice source; which of these gaps matter most should be decided by the external-research notes. Items marked "partial" were not evaluated visually.
