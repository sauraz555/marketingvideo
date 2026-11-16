# marketingvideo

Make TikTok / Reels / Shorts-style vertical videos (1080x1920) from a voiceover, with HTML + GSAP animation rendered to MP4.

- **Bold captions and graphics** timed to the spoken words: big numbers that count up, stat cards, comparisons, charts, do / don't panels, lists, REFUSED / GRANTED stamps, quote cards, call-to-action.
- **Source screenshots** of public web pages with the right sentence highlighted automatically (`capture`).
- **With or without a presenter.** With one, the person is cut out of the footage so graphics can sit *behind* them, and they can shrink into a corner or get a camera punch-in.
- **Lossless frame rendering** (PNG frames, CRF 14) split across parallel browsers.
- A Claude Code agent (`.claude/agents/shorts-director.md`) that plans a short from a script: reads the voice timing, researches facts on official pages, captures sources, and checks a contact sheet before rendering.

This repo holds the tools and the template only. It contains no videos, footage, voices or client material.

## Install

```
pip install -r requirements.txt
python -m playwright install chromium
```

You also need `ffmpeg` and `ffprobe` on your PATH. Microsoft Edge or Google Chrome is used (via Playwright) for the presenter modes because the bundled Chromium cannot decode H.264.

## Quick start

```
python tools/shorts.py new my-topic --voice voice.mp3 [--presenter clip.mp4]   # creates projects/my-topic/ and lists the spoken lines
# edit projects/my-topic/script.js (one scene per spoken line; see the comment at the top of the file)
python tools/shorts.py capture my-topic --url "https://official-page" --find "exact sentence" --name src1
python tools/shorts.py sheet my-topic        # contact sheet of every scene: projects/my-topic/qa/sheet.jpg
python tools/shorts.py render my-topic       # projects/my-topic/output/my-topic-1080x1920.mp4
```

Add your own `logo.png` to the project folder and set `logo: 'logo.png'` in `script.js` (the template ships without one).

## Presenter footage (people)

1. Put the clip in the project as `presenter.mp4` (H.264, 1080x1920, 30 fps) and set `presenter: 'presenter.mp4'` in `script.js`.
2. Cut the person out once: `python tools/matte.py projects/my-topic/presenter.mp4` (writes `presenter-matte.mkv`, runs on CPU).
3. Render as usual. Hooks and numbers sit behind the person, cards sit low so the face stays clear. Add `moves` in `script.js` for the shrink and the punch-ins.

`tools/matte.py` needs the Robust Video Matting model, which is not included. Download `rvm_mobilenetv3_fp32.onnx` from the project's releases (https://github.com/PeterL1n/RobustVideoMatting/releases) and put it in `tools/models/`. Check that project's licence before redistributing the weights.

## Notes

- `capture` only loads public pages and never clicks forms. Check each source's terms and respect sites that block automated access.
- Keep API keys out of the repo; this code needs none. Voiceovers are made outside it and passed in as `voice.mp3`.
- Do not publish footage, voices or client details you do not have permission to share. `.gitignore` excludes `projects/`, media files and model weights for that reason.
