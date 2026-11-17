# Shorts director brief

This brief is for whoever builds the video: a person, Claude, or any other AI model with a shell. It needs nothing but
Python, ffmpeg and a browser (`python tools/shorts.py doctor` checks them). `python tools/shorts.py guide` prints this
brief plus every scene type; `guide --json` gives the same catalogue as data.

You direct short vertical videos for this repo with `tools/shorts.py`. You write the content (`projects/<name>/script.js`); you never change the engine (`short.html`, `tools/shorts.py`) unless the person asks.

Read `projects/<name>/segments.js` for the spoken line timings (run `python tools/shorts.py segments <name>` if it is missing). `projects/shorts-reference/` is a finished example that passes `lint`.

## 0. Configure first (always, before anything else)
Do not start a video until the project is configured. Run `python tools/shorts.py config <name>` and read `projects/<name>/config.json`.
- If `status` is `needs-setup`, ask the person the unanswered questions **in the conversation** (with a question tool if you have one, otherwise in plain text; 3-4 questions at a time, suggested defaults first), then save every answer with `python tools/shorts.py config <name> --set key=value ...` until it prints `configuration: ready`.
- The questions (keys in `tools/shorts.py`): voiceover language, caption language, where the voice comes from (their file / generate with ElevenLabs / the presenter's own audio) and the voice name, the format (data explainer / product film / creator explainer / story b-roll / match a reference), person on camera or not, the brand (website or none), look (auto / clean / dark / warm), backdrop mode (images / video clips / mixed / none), **which tool makes the backdrops (kling / elevenlabs / higgsfield / bloom / their own files)**, the spend limit and its unit, target length, music, logo file, whether to verify facts on official pages and show sources, whether client names may appear, normal post or paid ad (sets `safe` in script.js: `organic` or `strict`), and whether the video has realistic AI-made people, voices or places (the platforms then require their AI label on upload).
- **Brand (ask, never assume):** ask whether the video is for a brand. No brand is a fine answer: the engine's `clean` look is a complete neutral design, so do not invent a brand or reuse another project's.
  - Given a website: `python tools/shorts.py brand <name> --url <site>` reads the public page (read only) and writes `brand.js` (name, handle, logo, accent colour) plus `brand/brand.json` (description, social handles, fonts, every colour it weighed) and `brand/site.jpg`. Look at `site.jpg` and the logo file, and tell the person what you found before building; if the colour or logo is wrong, correct it with `--accent "#hex"` / `--logo file`.
  - Given only a name, colour or logo file: `python tools/shorts.py brand <name> --name "..." --accent "#hex" --logo file.png`.
  - If the site cannot be reached, say so and ask for the colour and logo instead of guessing.
  - With `brand.js` in the project, `script.js` uses the brand automatically (leave `look` out). Use the brand's own words from `brand.json` only as context: every claim in the video still needs a source.
- Never spend credits beyond the stated limit. If a price is unknown, ask before running. Re-read `config.json` at the start of every later session on this project and follow it.
- Anything the person tells you later that changes a setting: update it with `--set` so the file stays the source of truth.

## Tools: use what exists, never assume
Nothing here depends on one service. At the start, look at the tools this session actually has (image or video generators such as Kling, ElevenLabs, Higgsfield, Bloom or any other; voice services; a browser or web search; the presenter cut-out model) and at what the person has (accounts, credits, their own media). Then plan around that. Anything missing degrades gracefully:
- **No image/video generator, no credits, or the person prefers free:** use their own photos or footage in `media/`, `python tools/shorts.py backdrop <name> --from-video clip.mp4` (a still from their footage), or the built-in free gradients (`backdrop <name>` for a colour-mesh image, `--video` for an animated gradient). A video with plain-but-designed backgrounds still works.
- **No voice service:** the person supplies `voice.mp3`, or you use the presenter's own audio, or make a silent captions-only video.
- **No browser or web search:** skip source screenshots, state only what the person gave you, and say which claims are unverified so they can add links.
- **No cut-out model:** skip `matte.py`; presenter videos still render (graphics sit on top, cards low).
Say plainly which of these you are using and why.

## Director's brief (attention first)
You are the director, not a typist. Every scene must earn the next 3 seconds of attention.
- **Hook (from frame 0, complete by about 1.5 s):** something must be on screen in the very first frame. Open on the most surprising or personal line: a direct question to the viewer, a big number, or a "this affects you if…" caption. Never open on a logo or a greeting.
- **Rhythm:** something new every 2–4 s, at uneven intervals (a row, a bar, a word counts; `lint` warns after 5 s of nothing). Put the biggest pattern break (full-screen number, source page, chart, do/don't panel) near the midpoint. Do not repeat the same scene type twice in a row.
- **Animate, then hold:** let a chart or number finish moving and stay still, fully labelled, long enough to read (about 17 characters per second, never under 0.85 s). `lint` checks this for captions.
- **Length:** 20–35 s unless the topic needs more; the voiceover sets it.
- **Safe area:** the apps cover the top 200 px, the bottom 400 px and the lower right-hand column (paid ads: 288 / 672). The engine keeps captions and the brand line inside; `sheet` draws the unsafe bands in red.
- **One idea per scene, one hero word per caption** (`hl: true` on the word that matters). Captions are short: 2–5 words in the key, a 3–6 word lead.
- **Pick the scene from the content:**
  - a number or date → `bignum` (with sources as `badges`) or `stat`
  - two or three things compared → `compare` (stacked rows with `bar: true` read best on a phone; `win: true` marks the winner)
  - the same measure across items → `chart` (up to 4 columns, or `dir: 'h'` rows for 5–6; real values only, name the source in `note`)
  - one percentage → `ring`; one trend over time → `line`; dates or deadlines → `timeline`
  - rules, mistakes, requirements → `dosdonts` (3 short phrases per side, verbs first)
  - steps or a checklist → `list`; "who is this for / not for" → `pills`
  - a claim from an official page → `web` via `capture --find` with the exact sentence highlighted
  - a feeling or transition → `hero` emoji for 1–2 s
- **Credibility on screen:** every factual claim shows its source (a `web` scene, a `badges` chip or a `note`). Never invent chart values; if the numbers are not on an official page, use a different scene.
- **Ending:** the last 3 s are one clear action (`cta`), spoken in the voiceover too. The last scene holds to the final frame (no fade to nothing), so the video cuts cleanly back to the hook when it loops.
- **Loop-friendly:** the first and last captions should connect so the video feels complete when it replays.
- **Words on the beat (optional):** with `words.js` (`python tools/shorts.py align <name>`), `word: 'visa'` starts a scene when that word is spoken, and `sync: true` on a caption pops its key words in time. Only use `sync` when the captions are in the voice's language.

## Formats (decide with the person before writing a scene)
Ask which kind of short this is (`format` in the setup questions), or work it out from a reference video they give you. The scene types mix freely; a format is a habit of pacing and layout, not a mode.

| Format | What it looks like | Scenes | Length |
|---|---|---|---|
| **Data explainer** | Voiceover, bold two-line captions, numbers and sources | `cap`, `bignum`, `chart`, `compare`, `ring`, `line`, `timeline`, `web`, `quote`, `cta` | 20–45 s |
| **Product film** | No presenter, little or no voice. Two to four big words at a time, a 3D phone, cards flying in, a glowing orb, a glass checklist. One idea per beat, a beat every 1.5–2.5 s, always moving | `phone`, `kinetic`, `orb`, `glass`, `screen`; `backdrops` with `style` | 12–20 s |
| **Creator explainer** | A presenter, intercut with full-screen graphics that build while they talk: a mind map on paper, sticky notes, words in ovals, a headline above the head. Small spoken captions that fill in word by word | `headline`, `stickies`, `tags`, `mindmap`, `screen`, `photo`; `captions: { style: 'pill' }` | 30–60 s |
| **Story b-roll** | Full-screen footage or generated clips tell a story first, with small outlined captions; then the presenter or a screen recording explains | `broll` / video `backdrops`, `screen`; `captions: { style: 'outline' }` | 30–90 s |

Rules that came out of the reference videos these formats were modelled on:
- **Product film:** the background changes with the story, not at random: light for the problem, a soft second tone for the turn, dark for the product, back to light for the line to remember (`backdrops: [{ style: 'white' | 'sky' | 'night' | 'brand', t, end }]`). Text is two-tone: one word in the accent colour (`*word*`), sometimes one in italic (`_word_`). Things enter with blur and leave by flying past the camera (`exit: 'zoom'`). End on three words or fewer.
- **Creator explainer:** graphics live in the top third, above the head; captions sit low; the middle belongs to the face. Cut to a full-screen graphic (`mindmap`) only when there is a structure to show, build it one node per spoken idea, move the camera to each new node, and finish zoomed out on the whole map with a `glow` on each part as it is recapped.
- **Story b-roll:** one clip per sentence, cut on the sentence; captions are two or three words and never cover the subject.
- **Spoken captions** (`captions`) are the transcript, so they need `words.js` and the voice's own language. Do not also add `cap` scenes saying the same words; use `cap` / `kinetic` for emphasis only.

## Matching a reference video
When the person gives a reference: `python tools/shorts.py frames <name> <video>` (frames with a pixel grid), and also look at it at 3–4 frames per second to see how things move. Write down, before building: the beats and their length, what is on screen in each (type, position in px, size), how each thing enters and leaves, the backgrounds and when they change, the caption style, and whether there is a voice. Then rebuild that **structure** with this engine's scenes and the person's own words, brand and footage. Never reuse the reference's footage, wording, logo or music, and never keep reference videos in a project's output.

## Backdrops (never leave the background plain)
A plain gradient looks cheap. Give every beat of the story a real image or video behind it.
- **Plan one backdrop per phase** of the story (every 5-12 s), matched to the meaning: the place, the object or the mood. Avoid identifiable faces, readable text and logos in generated media.
- **Make them** with whichever image or video generator this session has connected (or the free options above if none). Price one first (`estimate_only`) and tell the person the total before generating several. Ask for **9:16 portrait** in the generator's settings if it has an aspect option; a prompt that says "vertical" is NOT enough (some tools ignore it and return 16:9). If you only get 16:9, use `focus: [from, to]` to pan across it. Check each result: trim white bars if a portrait image came back padded, and look at it before using it.
- **Kling** (only if the session has it and the person chose it or left the tool on auto): call `who_am_i` first for the current model list, check `query_membership_and_credits`, then use `text_to_image` or `text_to_video` with a model from that list (do not assume a version: pick one whose price the tool can estimate, and prefer a silent tier since backdrops need no sound) with **`aspect_ratio: "9:16"`**, which Kling honours, so no pan or crop is needed. For a moving backdrop make a 5-10 s clip (it loops to fill its slot); for a still, make an image and animate it with `image_to_video` only if the motion is worth the credits. `image_to_video` needs the source image as a public URL or from the upload tool, not a local path. Tell the person the credits left and what you plan to spend before each batch, do not retry a failed job without asking, and keep every request free of faces, text and logos.
- **Save them** in `projects/<name>/media/` and list them in `script.js`:
  `backdrops: [{ src: 'media/bd1.png', t: 0, end: 10.8, focus: [15, 85], zoom: [1, 1.08], dim: 0.42 }, ...]`
  Start each backdrop 0.45 s before the previous one ends so they crossfade. Hold the last one to the final frame (`fadeOut: 0`).
- Videos work too (`src: 'media/clip.mp4'`): they loop to fill their slot. With a presenter and a cut-out (`tools/matte.py`), the backdrop **replaces the room** behind the person.
- **Frame the key photos.** For the two or three most important beats use a `photo` scene (polaroid or card, with a short caption) over a *blurred* copy of the same image as the backdrop. It looks designed, and it hides the softness of any enlarged image.
- Text turns white automatically while a backdrop is on screen; use the white logo (`logo-white.png`).
- Use only media you generated or have the right to use. Do not pass off a generated picture as a real photo of a real place or event.

## The director's job: pick the design from the content
You are given content (a script, a transcript, a voice file, footage, a brand, sometimes a reference video). You decide the format, the beats and the design of every beat; nobody hands you a storyboard.

1. **Get the words and their times.** A voice or presenter clip: `segments`, then `align` if you can (word times make everything better). Only text: save it as `projects/<name>/script.txt`.
2. **First pass:** `python tools/shorts.py plan <name>` (add `--text file` or `--format ...`; `--json` for data). It cuts the script into beats, names each beat's job (hook, definition, problem, example, steps, list, number, compare, payoff, cta, point), picks a format from what the project has (presenter? voice? length), and proposes a scene for every beat with the reason. It writes `plan.json`.
3. **Then direct.** The plan is made by rules and will be wrong in places. For every beat ask:
   - *What must the viewer understand or feel here?* If nothing new, stay on the presenter (or merge the beat into its neighbour).
   - *Is there a structure?* Parts of a whole → `mindmap` / `orbit`; an order → `list` / `picklist` / `timeline`; two sides → `compare`; a quantity → `bignum` / `chart` / `ring` / `line`; a piece of text → `skeleton` / `quote` / `web`; a product screen → `phone` / `screen`; a name to remember → `kinetic` / `headline`.
   - *Is the number real?* No source, no number scene.
   - *Does it move every 2–4 s?* A long beat gets built in steps (`at` times on rows, marks, nodes), not one static card.
   - *Is it a different picture from the last beat?* Keep one section title (`head`) across a section and change the diagram under it.
4. **Storytelling checks** on the script itself, before any design. If the script is the person's own, suggest edits and ask; never rewrite their voice silently.
   - The first sentence is the hook and names what the viewer gets.
   - Every new or technical idea is said twice: once precisely, once in plain words or a metaphor. The plain line is the one to put on screen.
   - One idea per sentence; a sentence over about 25 words gets split.
   - The ending asks for one action.
5. Write the storyboard table (see Return) and, when the person is present, show it before building.

## 1. Understand the script
- Map each spoken line (`seg n`) to one idea. Keep the language of the voice (Nepali here) and write captions in English unless the person asks otherwise.
- Decide the hook (first 2 s), the proof (numbers, a source), the steps, and the call to action (last 3 s).

## 2. Research (facts only from sources)
- Every number, date or rule in a caption must come from an official page you read (for Australian migration: the state site and business.gov.au / homeaffairs.gov.au). Note the URL and the exact sentence.
- If a fact cannot be found, leave it out of the video and list it under Open questions. Never invent a number.
- Use only public pages. Do not log in, fill forms or accept tracking.

## 3. Screenshots
- For each source sentence, run `python tools/shorts.py capture <name> --url <page> --find "<exact sentence or phrase from the page>" --name <short-name>`.
- The command prints a `scene` JSON with the highlight already placed. Paste it into `script.js` and give it the time (`seg` or `t`/`end`). Adjust `from` if the highlight is off-centre.

## 4. Placement from a reference video (when the person gives one)
- Run `python tools/shorts.py frames <name> <video>`, then read `projects/<name>/ref/grid-sheet.jpg`.
- For each reference shot, note in pixels (1080x1920): where the caption band sits, where the big number or card sits, where a face or footage sits, and the margins. Copy these into the scene's `pos`, a `top` value, or a new scene type. Match the reference's rhythm and keep the same caption position throughout.
- Say in the storyboard which reference frame each scene was matched to.

## 5. Engagement
- Hook from the first frame (question or big number). Something new every 2–4 s. Put the one key word in orange (`hl: true`). Use a numbered list or a comparison to break up long lines. End with one clear action.

## 6. Build and check
1. Write `script.js` with every scene timed to `segments.js`.
2. `python tools/shorts.py lint <name>` (`--json` for data). Fix every ERROR (text cut off, caption on top of a graphic, missing file, unknown scene type). Read each WARN (unsafe area, too short to read, nothing new for 5 s, no hook, no CTA) and fix it or say why it stands.
3. `python tools/shorts.py sheet <name>` and look at `projects/<name>/qa/sheet.jpg` (one settled frame per scene; red bands = covered by the app). Check what rules cannot: each web highlight lands on the right sentence, text is readable over its backdrop, the picture matches the words.
4. Repeat 2–3 until clean. With a presenter cut-out, also run a test cut (`render <name> --from 0 --to 3`), because the sheet does not show the final layering.
5. `python tools/shorts.py render <name>`. It prints length, size, bitrate and loudness (the mix is normalised to -14 LUFS). Check a few frames of the MP4 (ffmpeg, one frame every 10 s) before you report it done.
6. If the project's `ai_disclosure` answer is yes, remind the person to switch on the platform's AI label when uploading.

## Return
- **Storyboard**: table with Scene · Time · Visual (type, source URL) · Caption · Source of each number · Matched reference frame (if any).
- **Sources**: each URL and the exact sentence it supports.
- **Files**: the script, the shots, the output MP4 path.
- **Open questions**: only what blocks the video (for example a fact that could not be confirmed).

Rules: no fabricated numbers, quotes or claims. Never click anything that submits, saves or deletes. Keep personal details out of URLs and requests.
