# Instructions for AI agents (any model)

This repo makes motion videos from HTML + GSAP, rendered to MP4 with a headless browser and ffmpeg. Everything runs
from the shell, so any model or person can drive it. `CLAUDE.md` holds the same project rules for Claude Code.

## Portrait shorts (TikTok / Reels / YouTube Shorts, 1080x1920)

```
python tools/shorts.py doctor          # what this machine can do (nothing optional is required)
python tools/shorts.py guide           # the full brief, every scene type, every command   (--json for data)
python tools/shorts.py new <name> --voice voice.mp3
python tools/shorts.py config <name> --set key=value ...     # setup answers; ask the person, do not guess
python tools/shorts.py brand <name> --url https://company.com   # only if the video is for a brand
python tools/shorts.py plan <name> --text script.txt         # first-pass storyboard: format, beats, a design per beat
# then decide every beat yourself and write projects/<name>/script.js  (content only; short.html is the engine)
python tools/shorts.py lint <name> --json     # must have 0 errors
python tools/shorts.py sheet <name>           # look at projects/<name>/qa/sheet.jpg
python tools/shorts.py render <name>          # projects/<name>/output/<name>-1080x1920.mp4
```

- The brief is `templates/shorts/DIRECTOR.md`; the scene catalogue is `templates/shorts/scenes.json`; a finished
  example that passes `lint` is `projects/shorts-reference/`.
- Exit codes: `lint` exits 1 when there are errors (`--strict`: warnings too); every command exits non-zero on failure.

## Rules for every video in this repo

- Real numbers only, each with its source; never invent a figure, quote or claim.
- Captions are English unless the person asks otherwise; use exact UI labels.
- Never change data in an app being filmed: no Save / Submit / Delete during capture.
- API keys live only in the environment (`ELEVENLABS_API_KEY`). Never put a key in a command, a file or a commit.
- Do not use or share anything in `_archive/`.
- Never spend generator credits beyond the limit in the project's `config.json`.

16:9 explainer videos of app pages follow `.claude/skills/explainer-video/SKILL.md` (plain Markdown, readable by any model).
