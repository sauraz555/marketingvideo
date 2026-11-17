"""Portrait shorts (TikTok / Reels / Shorts, 1080x1920) from templates/shorts/.

Works from any shell, for a person or for any AI model: `guide` prints the whole brief and the scene catalogue,
`doctor` says what this machine can do, `lint --json` returns machine-readable problems. No service is compulsory.

Run from the repo root:
  python tools/shorts.py direct <name> --video clip.mp4 [--brand https://site] [--frame landscape] [--format ...]   # ONE COMMAND: a full first draft
  python tools/shorts.py guide [--json]            # how to make a short: the brief, every scene type, every command
  python tools/shorts.py doctor                    # what is installed (browser, ffmpeg, fonts, cut-out model, voice key)
  python tools/shorts.py new <name> [--voice <voice.mp3>] [--presenter <clip.mp4>]   # projects/<name>/
  python tools/shorts.py config <name> --interactive   # project setup questions (asked first; answers saved in config.json)
  python tools/shorts.py brand <name> --url https://company.com   # read name, logo and colours from the brand's site -> brand.js
  python tools/shorts.py brand <name> --name "Acme" --accent "#E4002B" [--logo logo.png]   # or give them yourself
  python tools/shorts.py voice <name> --text script.txt [--voice-id ID]   # optional: ElevenLabs voice.mp3 + words.js
  python tools/shorts.py segments <name>          # find the spoken lines in voice.mp3 -> segments.js
  python tools/shorts.py align <name> [--from words.json|subs.srt] [--text script.txt]   # word timings -> words.js
  python tools/shorts.py plan <name> --text script.txt   # director's first pass: beats, format and a design per beat -> plan.json
  python tools/shorts.py backdrop <name> [--video] [--from-video clip.mp4]   # free backdrop, no account needed
  python tools/shorts.py capture <name> --url <page> [--find "exact text on the page"] [--name shot]
  python tools/shorts.py lint <name> [--json]     # rule check: safe zones, overlaps, cut-off text, missing files, pacing
  python tools/shorts.py sheet <name>             # QA contact sheet of every scene -> projects/<name>/qa/sheet.jpg
  python tools/shorts.py render <name> [--music bg.mp3] [--fps 30] [--from 3 --to 8]   # -> projects/<name>/output/<name>-1080x1920.mp4

A project holds short.html (engine, copied from the template), script.js (the content you edit),
segments.js / words.js (written by `segments` / `align`), voice.mp3 and optionally presenter.mp4 and images.
"""
import argparse, asyncio, base64, json, os, pathlib, re, shutil, subprocess, sys, urllib.error, urllib.request, uuid

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "templates" / "shorts"


def proj(name):
    p = pathlib.Path(name)
    p = p if p.is_dir() else ROOT / "projects" / name
    if not (p / "short.html").exists():
        sys.exit(f"{p} has no short.html (create it with: python tools/shorts.py new <name> --voice <file>)")
    return p.resolve()


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def has_audio(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True).stdout
    return bool(out.strip())


# ---------- configuration (asked before anything else) ----------
CONFIG_QUESTIONS = [
    ("voice_language", "What language is the voiceover?", ["nepali", "english", "nepali + english mix"], "nepali + english mix"),
    ("caption_language", "What language should the on-screen captions be?", ["english", "nepali", "same as the voice"], "english"),
    ("voice_source", "Where does the voiceover come from?", ["i provide an audio file", "generate it with a voice service I have (e.g. ElevenLabs)", "the presenter's own audio", "no voice (captions and music only)"], "i provide an audio file"),
    ("voice_name", "Voice name (only if generating; leave blank otherwise)", None, ""),
    ("format", "What kind of short?", ["data explainer (voice, bold captions, charts and sources)", "product film (big type, 3D phone, cards; little or no voice)", "creator explainer (presenter intercut with a mind map, notes and screen recordings)", "split explainer (presenter card below, diagram panel above, one-word captions)", "story b-roll (full-screen footage with small spoken captions)", "crimson explainer (presenter, black-to-red glass cards, diamonds, numbered lanes)", "match a reference video I will give you"], "data explainer (voice, bold captions, charts and sources)"),
    ("presenter", "Is there a person on camera?", ["no", "yes, footage provided"], "no"),
    ("brand", "Is this for a brand? Give its website (the logo, colours and name are read from it), or 'none' for a clean neutral design", None, "none"),
    ("look", "Visual look", ["auto (the brand's colours if a brand is given, otherwise clean)", "clean", "dark", "warm"], "auto (the brand's colours if a brand is given, otherwise clean)"),
    ("backdrop_mode", "Backdrops behind the scenes", ["images", "video clips", "mixed images and video", "none (plain background)"], "images"),
    ("backdrop_tool", "Where do the backdrops come from? Nothing here is compulsory: 'auto' uses whatever image or video generators this session has, and falls back to free options if there are none", ["auto (use what I have)", "my own files", "free built-in gradients (no account)", "frames from my footage", "kling", "elevenlabs", "higgsfield", "bloom", "other"], "auto (use what I have)"),
    ("backdrop_budget", "Spend limit for generated media (number and unit, e.g. '1 USD' or '100 credits'), or 'free only'", None, "free only"),
    ("length_seconds", "Target length in seconds (20-35 holds attention best in the studies we found; longer is fine for a deeper topic)", None, "20-35"),
    ("music", "Background music", ["none", "my own licensed track"], "none"),
    ("logo", "Logo file inside the project folder", None, "logo.png"),
    ("sources", "Check facts on official pages and show the sources on screen?", ["yes", "no"], "yes"),
    ("privacy", "Names and personal details", ["no client names", "names are allowed"], "no client names"),
    ("safe_zone", "Keep text clear of the app buttons for", ["organic posts", "paid ads (stricter)"], "organic posts"),
    ("ai_disclosure", "Does the video contain realistic AI-made people, voices or places? (platforms require their AI label on upload if so)", ["no", "yes: remind me to switch on the AI label when I upload"], "no"),
]
CONFIG_OPTIONAL = {"voice_name"}


def config_path(p):
    return pathlib.Path(p) / "config.json"


def new_config():
    return {"status": "needs-setup", "answers": {k: None for k, _, _, _ in CONFIG_QUESTIONS}}


def load_config(p):
    f = config_path(p)
    if not f.exists():
        return None
    cfg = json.loads(f.read_text(encoding="utf-8"))
    for k, _, _, _ in CONFIG_QUESTIONS:      # questions added after the project was made
        cfg.setdefault("answers", {}).setdefault(k, None)
    return cfg


def save_config(p, cfg):
    missing = [k for k, _, _, _ in CONFIG_QUESTIONS if k not in CONFIG_OPTIONAL and cfg["answers"].get(k) in (None, "")]
    cfg["status"] = "ready" if not missing else "needs-setup"
    config_path(p).write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
    return missing


def configure(p, interactive=False, sets=(), redo=False):
    cfg = load_config(p) or new_config()
    for item in sets:
        k, _, v = item.partition("=")
        if k not in cfg["answers"]:
            sys.exit("unknown setting '%s'. Settings: %s" % (k, ", ".join(cfg["answers"])))
        cfg["answers"][k] = v.strip()
    if interactive:
        print("\nProject setup. Press Enter to accept the suggestion in [brackets].\n")
        for key, question, choices, default in CONFIG_QUESTIONS:
            if cfg["answers"].get(key) not in (None, "") and not redo:
                continue
            print(question)
            for i, c in enumerate(choices or [], 1):
                print("  %d) %s" % (i, c))
            try:
                raw = input("  [%s] > " % default).strip()
            except EOFError:        # no real terminal (piped input): stop asking, leave the rest unanswered
                print("(no terminal to ask in: answer later with --interactive or --set)")
                break
            if raw.isdigit() and choices and 1 <= int(raw) <= len(choices):
                raw = choices[int(raw) - 1]
            cfg["answers"][key] = raw or default
            print()
    missing = save_config(p, cfg)
    print("configuration: %s" % cfg["status"])
    for key, question, _, _ in CONFIG_QUESTIONS:
        print("  %-18s %s" % (key, cfg["answers"].get(key) if cfg["answers"].get(key) not in (None, "") else "(not set)"))
    if missing:
        print("\nstill needed: %s\nanswer with:  python tools/shorts.py config <project> --interactive   or   --set key=value" % ", ".join(missing))
    return cfg, missing


def warn_config(p):
    cfg = load_config(p)
    if cfg is not None and cfg.get("status") != "ready":
        print("WARNING: %s is not configured yet. Run: python tools/shorts.py config %s --interactive" % (pathlib.Path(p).name, pathlib.Path(p).name), file=sys.stderr)


def cmd_config(a):
    p = proj(a.project)
    cfg, missing = configure(p, interactive=a.interactive, sets=a.set or [], redo=a.redo)
    if missing:
        sys.exit(1)


# ---------- free backdrops (no account, no credits) ----------
def _hex(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def cmd_backdrop(a):
    """Make a backdrop without any generator: a soft colour-mesh image, an animated gradient video, or a still from your own footage."""
    p = proj(a.project)
    media = p / "media"
    media.mkdir(exist_ok=True)
    name = a.name or ("backdrop-" + ("frame" if a.from_video else "video" if a.video else "mesh"))
    if a.from_video:
        out = media / (name + ".jpg")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(a.at), "-i", a.from_video, "-frames:v", "1",
                        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920", "-q:v", "2", str(out)], check=True)
        print("wrote %s  (use blur: 14 in the backdrop entry to soften it)" % out)
        return
    colors = [c.strip() for c in a.colors.split(",") if c.strip()]
    if a.video:
        out = media / (name + ".mp4")
        cs = "".join(":c%d=0x%s" % (i, c.lstrip("#")) for i, c in enumerate(colors[:8]))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
                        "gradients=size=1080x1920:rate=30:duration=%s:speed=0.015:nb_colors=%d%s:seed=%d" % (a.seconds, min(len(colors), 8), cs, a.seed),
                        "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", str(out)], check=True)
        print("wrote %s  (loops to fill its slot)" % out)
        return
    import numpy as np
    from PIL import Image
    rng = np.random.default_rng(a.seed)
    H, W = 1920, 1080
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rgb = [np.array(_hex(c), np.float32) for c in colors]
    img = np.zeros((H, W, 3), np.float32) + rgb[0]
    for c in (rgb[1:] * 2):
        cx, cy, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0.18, 0.38) * H
        w = np.exp(-(((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * r * r)))[..., None]
        img = img * (1 - 0.85 * w) + c * 0.85 * w
    vig = 1 - 0.35 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / 2
    img = img * vig[..., None] + rng.normal(0, 2.2, img.shape)
    out = media / (name + ".png")
    Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).save(out)
    print("wrote %s  (add it to backdrops in script.js)" % out)


# ---------- new ----------
def cmd_new(a):
    dst = ROOT / "projects" / a.name
    if dst.exists():
        sys.exit(f"{dst} already exists")
    shutil.copytree(TEMPLATE, dst, ignore=shutil.ignore_patterns("README.md", "DIRECTOR.md", "scenes.json", "segments.js", "words.js"))
    (dst / "output").mkdir()
    if a.voice:
        shutil.copy(a.voice, dst / "voice.mp3")
    if a.presenter:
        shutil.copy(a.presenter, dst / ("presenter" + pathlib.Path(a.presenter).suffix.lower()))
    print(f"created {dst}")
    save_config(dst, new_config())
    if sys.stdin.isatty():
        configure(dst, interactive=True)
    else:
        print(f"configuration needed first: python tools/shorts.py config {a.name} --interactive   (or let the director agent ask you)")
    if a.voice:
        a.project = a.name
        cmd_segments(a)


# ---------- segments ----------
def cmd_segments(a):
    p = proj(a.project)
    voice = p / "voice.mp3"
    if not voice.exists():
        pres = next(iter(p.glob("presenter.*")), None)
        if pres and has_audio(pres):     # "the presenter's own audio": take the sound of the footage as the voice
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(pres), "-vn", "-c:a", "libmp3lame", "-q:a", "2", str(voice)], check=True)
            print(f"took the voice from {pres.name} -> voice.mp3")
        else:
            sys.exit(f"put the voiceover at {voice} (or a presenter clip with sound in the project)")
    total = duration(voice)
    log = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(voice), "-af",
                          f"silencedetect=noise={a.noise}dB:d={a.min_pause}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    segs, cur = [], 0.0
    for s, e in zip(starts, ends):
        if s - cur > 0.15:
            segs.append([round(cur, 2), round(s, 2)])
        cur = e
    if total - cur > 0.15:
        segs.append([round(cur, 2), round(total, 2)])
    (p / "segments.js").write_text(
        "// written by tools/shorts.py segments: [start, end] of each spoken line in voice.mp3\n"
        f"window.AUDIO_DURATION = {round(total, 2)};\nwindow.SEGMENTS = {json.dumps(segs)};\n", encoding="utf-8")
    print(f"{len(segs)} lines in {total:.1f}s of voice:")
    for i, (s, e) in enumerate(segs):
        print(f"  seg {i:2d}  {s:6.2f} - {e:6.2f}  ({e - s:4.1f}s)")


# ---------- browser ----------
def _find_chrome():
    """A Chromium binary when Playwright's own download is missing: $SHORTS_BROWSER, then the Playwright cache folders."""
    env = os.environ.get("SHORTS_BROWSER")
    if env and pathlib.Path(env).exists():
        return env
    roots = [os.environ.get("PLAYWRIGHT_BROWSERS_PATH"), "/opt/pw-browsers", str(pathlib.Path.home() / ".cache" / "ms-playwright"),
             str(pathlib.Path.home() / "AppData" / "Local" / "ms-playwright"), str(pathlib.Path.home() / "Library" / "Caches" / "ms-playwright")]
    for r in filter(None, roots):
        r = pathlib.Path(r)
        if r.is_file():
            return str(r)
        for pat in ("chromium-*/chrome-linux*/chrome", "chromium-*/chrome-win*/chrome.exe", "chromium-*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium", "chromium"):
            hits = sorted(x for x in r.glob(pat) if x.is_file())
            if hits:
                return str(hits[-1])
    for name in ("google-chrome", "chromium", "chromium-browser", "microsoft-edge"):
        w = shutil.which(name)
        if w:
            return w
    return None


async def launch(pw, h264=False):
    """Edge/Chrome first when footage must be decoded (bundled Chromium has no H.264), else Playwright's Chromium, else any Chromium found."""
    if os.environ.get("SHORTS_BROWSER"):
        return await pw.chromium.launch(executable_path=os.environ["SHORTS_BROWSER"])
    if h264:
        for ch in ("msedge", "chrome"):
            try:
                return await pw.chromium.launch(channel=ch)
            except Exception:
                pass
    try:
        return await pw.chromium.launch()
    except Exception as e:
        exe = _find_chrome()
        if not exe:
            sys.exit("no browser found. Run `python -m playwright install chromium`, or set SHORTS_BROWSER to a Chrome/Chromium/Edge binary.\n(%s)" % str(e).splitlines()[0])
        return await pw.chromium.launch(executable_path=exe)


async def open_page(pw, html, presenter, alpha=False, guides=False):
    browser = await launch(pw, h264=bool(presenter))
    W, H = frame_size(html.parent)
    page = await browser.new_page(viewport={"width": W, "height": H})
    page.issues = []      # anything that failed to load or threw: reported by sheet / lint / render
    page.on("requestfailed", lambda r: None if (r.failure or "").endswith("ERR_ABORTED") and re.search(r"\.(mp4|webm|mov|m4v|mp3|wav)$", r.url, re.I)
            else page.issues.append("did not load: " + r.url.split("/")[-1]))      # media range requests the browser drops on purpose are fine
    page.on("response", lambda r: r.status >= 400 and page.issues.append("did not load (%d): %s" % (r.status, r.url.split("/")[-1])))
    page.on("pageerror", lambda e: page.issues.append("script error: " + str(e).splitlines()[0]))
    q = "&".join(x for x in ("alpha=1" if alpha else "", "guides=1" if guides else "") if x)
    await page.goto(html.as_uri() + ("?" + q if q else ""), wait_until="load")
    if not await page.evaluate("() => !!window.gsap && typeof TL !== 'undefined'"):
        await browser.close()
        sys.exit("the page did not start: %s\n(GSAP is in vendor/ of the template; an old project without it needs the network, or copy templates/shorts/vendor into it)" % "; ".join(page.issues[:5]))
    # fonts: wait, but never hang (a blocked font request must not stall the render)
    ok = await page.evaluate("() => Promise.race([document.fonts.ready.then(() => true), new Promise(r => setTimeout(() => r(false), 8000))])")
    if not ok:
        page.issues.append("fonts were not ready after 8 s (text may use a fallback font)")
    await page.wait_for_timeout(400)
    await page.add_style_tag(content=(
        f"body{{padding:0!important;display:block!important;background:{'transparent' if alpha else '#000'}!important}}"
        f"#viewport{{width:{W}px!important;border-radius:0!important;box-shadow:none!important}}"
        "#controls{display:none!important}"))
    await page.evaluate("() => { fit(); TL.pause(); }")
    return browser, page


def issues_of(page):
    seen, out = set(), []
    for x in page.issues:
        if x not in seen and not any(o in x for o in ("segments.js", "words.js", "brand.js")):   # optional files
            seen.add(x)
            out.append(x)
    return out


async def seek(page, t):
    await page.evaluate("async t => { TL.seek(t); await window.seekMedia(t); }", t)


# ---------- sheet ----------
async def sheet(p, guides=True):
    from PIL import Image
    html = p / "short.html"
    qa = p / "qa"
    qa.mkdir(exist_ok=True)
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        browser, page = await open_page(pw, html, any(p.glob("presenter.*")), guides=guides)
        # one settled frame per scene (everything revealed, just before it leaves), plus the first and last frame
        times = await page.evaluate("""() => { const d = window.DUR, ts = new Set([0.6, +(d - .1).toFixed(1)]);
            window.SCENE_INFO.forEach(s => ts.add(+Math.max(s.t + .3, Math.min(s.end - .45, s.t + 4)).toFixed(1)));
            return [...ts].filter(t => t > 0 && t < d).sort((a, b) => a - b).filter((t, i, a) => i === 0 || t - a[i - 1] > .25); }""")
        shots = []
        for t in times:
            await seek(page, t)
            f = qa / f"t{t:06.1f}.jpg"
            await page.screenshot(path=str(f), type="jpeg", quality=80)
            shots.append((t, f))
        problems = issues_of(page) + await page.evaluate("() => window.PAGE_ERRORS || []")
        await browser.close()
    FW, FH = frame_size(p)
    cols, w, h = (6, 270, 480) if FH > FW else (4, 480, 270)
    rows = (len(shots) + cols - 1) // cols
    sheet_img = Image.new("RGB", (cols * w, rows * (h + 30)), "white")
    from PIL import ImageDraw
    d = ImageDraw.Draw(sheet_img)
    for i, (t, f) in enumerate(shots):
        x, y = (i % cols) * w, (i // cols) * (h + 30)
        sheet_img.paste(Image.open(f).resize((w, h)), (x, y + 30))
        d.text((x + 8, y + 8), f"{t:.1f}s", fill="black")
    out = qa / "sheet.jpg"
    sheet_img.save(out, quality=85)
    print(f"wrote {out} ({len(shots)} moments{', red bands = platform buttons / unsafe area' if guides else ''})")
    for x in dict.fromkeys(problems):
        print("PROBLEM:", x)
    if any(p.glob("presenter.*")) and any(p.glob("*matte*.mkv")):
        print("NOTE: this project has a cut-out. The sheet shows the browser preview (graphics over the footage), not the final\n"
              "      layering. Check that with a short test render: python tools/shorts.py render %s --from 0 --to 3" % p.name)
    return problems


def cmd_sheet(a):
    warn_config(proj(a.project))
    asyncio.run(sheet(proj(a.project), guides=not a.no_guides))


# ---------- render ----------
async def frames(p, out, fps, workers=4, start=None, end=None):
    """Screenshot every frame as lossless PNG; `workers` browsers each take an interleaved share of frames."""
    from playwright.async_api import async_playwright
    presenter = any(p.glob("presenter.*"))
    async with async_playwright() as pw:
        b0, pg0 = await open_page(pw, p / "short.html", presenter)
        dur = await pg0.evaluate("() => window.DUR")
        f0 = int(round((start or 0) * fps))
        total = min(int(round(dur * fps)), int(round((end if end is not None else dur) * fps)))
        done = [0]

        async def worker(k, browser, page):
            for i in range(f0 + k, total, workers):
                await seek(page, i / fps)
                await page.screenshot(path=str(out / f"{i:05d}.png"), type="png")
                done[0] += 1
                if done[0] % 300 == 0:
                    print(f"frame {done[0]}/{total - f0}", flush=True)
            await browser.close()

        for x in issues_of(pg0):
            print("PROBLEM:", x, file=sys.stderr)
        others = [await open_page(pw, p / "short.html", presenter) for _ in range(workers - 1)]
        await asyncio.gather(*(worker(k, b, pg) for k, (b, pg) in enumerate([(b0, pg0)] + others)))
        return dur, f0, total


async def frames_layered(p, out, fps, workers=4, start=None, end=None):
    """Draw the graphics twice per frame, transparent: 'back' (behind the presenter) and 'front' (in front)."""
    from playwright.async_api import async_playwright
    (out / "back").mkdir(exist_ok=True)
    (out / "front").mkdir(exist_ok=True)
    async with async_playwright() as pw:
        pages = [await open_page(pw, p / "short.html", False, alpha=True) for _ in range(workers)]
        dur = await pages[0][1].evaluate("() => window.DUR")
        moves = await pages[0][1].evaluate("() => (window.SCRIPT && window.SCRIPT.moves) || []")
        backdrops = await pages[0][1].evaluate("() => (window.SCRIPT && window.SCRIPT.backdrops) || []")
        layers = ("bd", "back", "front") if backdrops else ("back", "front")
        (out / "bd").mkdir(exist_ok=True)
        f0 = int(round((start or 0) * fps))
        f1 = min(int(round(dur * fps)), int(round((end if end is not None else dur) * fps)))
        done = [0]

        async def worker(k, browser, page):
            for i in range(f0 + k, f1, workers):
                await page.evaluate("async t => { TL.seek(t); await window.seekMedia(t); }", i / fps)
                for layer in layers:
                    await page.evaluate("l => { document.body.dataset.layer = l; }", layer)
                    await page.screenshot(path=str(out / layer / f"{i:05d}.png"), type="png", omit_background=True)
                done[0] += 1
                if done[0] % 150 == 0:
                    print(f"frame {done[0]}/{f1 - f0}", flush=True)
            await browser.close()

        await asyncio.gather(*(worker(k, b, pg) for k, (b, pg) in enumerate(pages)))
    return dur, f0, f1, moves, backdrops


TO_YUV = "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p"     # RGB frames -> video-range BT.709, the colour phones expect
BT709 = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
LOUD = "I=-14:TP=-1:LRA=11"      # loudness the platforms play back at (convention; see reports/)


def _ease(x):
    c = "clip(" + x + ",0,1)"
    return "(" + c + "*" + c + "*(3-2*" + c + "))"          # smoothstep


def frame_size(p):
    """(width, height) of the project's frame: SCRIPT.frame = 'landscape' -> 1920x1080, otherwise portrait 1080x1920."""
    try:
        txt = (p / "script.js").read_text(encoding="utf-8")
    except OSError:
        return 1080, 1920
    return (1920, 1080) if re.search(r"""\bframe\s*:\s*['"]landscape['"]""", txt) else (1080, 1920)


def composite(p, matte, out, silent, fps, f0, f1, crf, moves=(), backdrops=()):
    """presenter (graded) -> [blurred backdrop while shrunk] -> back graphics -> person (matte) -> front graphics.
    moves: 'anchor' = the cut-out person shrinks to a corner (graphics fill the space behind them);
           'punch'  = a quick camera zoom-in on the footage."""
    import numpy as np
    from PIL import Image
    presenter = next(p.glob("presenter.*"))
    W, H = frame_size(p)
    ys = np.arange(H, dtype=np.float32) * (1920 / H)        # the shade curve is drawn on a 1920-high scale
    top = 150 * (1 - np.clip(ys, 0, 900) / 900) ** 1.6
    bot = 170 * (np.clip(ys - 1150, 0, None) / 770) ** 1.4
    arr = np.zeros((H, W, 4), np.uint8)
    arr[..., 3] = np.clip(top + bot, 0, 255).astype(np.uint8)[:, None]
    Image.fromarray(arr, "RGBA").save(out / "grad.png")
    start, D = f0 / fps, 0.45
    T = "(t+%.3f)" % start
    anchors = sorted([m for m in moves if m.get("mode") == "anchor"], key=lambda m: m["t"])
    punches = [m for m in moves if m.get("mode") == "punch"]

    def pulse(m):
        return "(" + _ease("((%s-%s)/%s)" % (T, m["t"], D)) + "-" + _ease("((%s-(%s-%s))/%s)" % (T, m["end"], D, D)) + ")"

    S = "(1" + "".join("+(%s-1)*%s" % (m.get("scale", 0.6), pulse(m)) for m in anchors) + ")"
    side = {"right": 1, "left": -1}
    DX = "(0" + "".join("+(%d*(%d*(1-%s)-14))*%s" % (side.get(m.get("side", "right"), 0), W // 2, m.get("scale", 0.6), pulse(m))
                        for m in anchors) + ")"
    Z = "(1" + "".join("+%s*(%s-%s)" % (m.get("amount", 0.12), _ease("((%s-%s)/0.18)" % (T, m["t"])),
                                         _ease("((%s-(%s+0.18))/0.75)" % (T, m["t"]))) for m in punches) + ")"
    # zoom (push-in / pull-out) and pan: a scale plus a focus point the crop follows
    zooms = [m for m in moves if m.get("mode") in ("zoom", "pan")]
    FX, FY = "(0.5", "(0.4"
    for m in zooms:
        t0, t1 = float(m["t"]), float(m.get("end", float(m["t"]) + 1))
        r = _ease("((%s-%s)/%s)" % (T, t0, max(0.3, t1 - t0)))                    # 0 -> 1 across the move
        back = "0" if m.get("hold") else _ease("((%s-%s)/0.4)" % (T, t1))          # 0 -> 1 after it ends
        on = "gte(%s,%s)*(1-%s)" % (T, t0, back)
        if m["mode"] == "zoom":
            a_, b_ = float(m.get("from", 1)), float(m.get("to", 1.2))
            Z = Z[:-1] + "+%s*((%s+(%s)*%s)-1))" % (on, a_, b_ - a_, r)
            f = m.get("focus") or [0.5, 0.4]
            FX += "+%s*(%s-0.5)" % (on, f[0]); FY += "+%s*(%s-0.4)" % (on, f[1])
        else:
            z = float(m.get("zoom", 1.25)); f0_, f1_ = m.get("from") or [0.3, 0.4], m.get("to") or [0.7, 0.4]
            Z = Z[:-1] + "+%s*%s)" % (on, z - 1)
            FX += "+%s*((%s+(%s)*%s)-0.5)" % (on, f0_[0], f1_[0] - f0_[0], r); FY += "+%s*((%s+(%s)*%s)-0.4)" % (on, f0_[1], f1_[1] - f0_[1], r)
    FX, FY = "clip(%s),0,1)" % FX, "clip(%s),0,1)" % FY
    zoom = ("scale=w='trunc(%d*%s/2)*2':h='trunc(%d*%s/2)*2':eval=frame,crop=%d:%d:x='(iw-ow)*%s':y='(ih-oh)*%s'" % (W, Z, H, Z, W, H, FX, FY)) if (punches or zooms) else "null"
    pscale = ("scale=w='trunc(%d*%s/2)*2':h='trunc(%d*%s/2)*2':eval=frame" % (W, S, H, S)) if anchors else "null"
    ovp = ("overlay=x='(main_w-overlay_w)/2+%s':y='main_h-overlay_h':format=auto" % DX) if anchors else "overlay=format=auto"
    # backdrop intervals: union of the anchor moves (adjacent ones share one fade)
    spans = []
    def _has_bd(a_, b_):  # a generated backdrop already fills this stretch: no blurred room needed
        return any((x.get("t") or 0) <= a_ + 0.01 and (x.get("end") if x.get("end") is not None else 1e9) >= b_ - 0.01 for x in backdrops)
    for m in anchors:
        if spans and m["t"] <= spans[-1][1] - D + 0.01:
            spans[-1][1] = max(spans[-1][1], m["end"])
        else:
            spans.append([m["t"], m["end"]])
    spans = [sp for sp in spans if not _has_bd(sp[0], sp[1])]
    pad = "tpad=stop_mode=clone:stop_duration=60"  # footage shorter than the voiceover holds its last frame
    fit = "scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,setsar=1" % (W, H, W, H)   # any size or shape of footage fills the frame
    fc = ["[0:v]fps=%s,%s,%s,eq=contrast=1.04:saturation=1.06,format=rgb24,split=%d[va][vb]%s" % (fps, fit, pad, 3 if spans else 2, "[vc]" if spans else ""),
          "[1:v]fps=%s,%s,%s,format=gray[mv]" % (fps, fit, pad),
          "[vb][mv]alphamerge[pm]",
          "[va]%s[vz]" % zoom,
          "[pm]%s,%s[pz]" % (zoom, pscale),
          ("[vz][5:v]overlay=format=auto[vbd];[vbd][4:v]overlay=format=auto[g0]" if backdrops else "[vz][4:v]overlay=format=auto[g0]")]
    cur = "g0"
    if spans:
        n = len(spans)
        blur = "[vc]scale=%d:%d,gblur=sigma=8,scale=%d:%d," % (W // 4, H // 4, W, H) + "eq=brightness=-0.2:saturation=0.9,format=rgba"
        if n > 1:
            fc.append(blur + ",split=%d%s" % (n, "".join("[bl%d]" % i for i in range(n))))
        else:
            fc.append(blur + "[bl0]")
        for i, (a, b) in enumerate(spans):
            fc.append("[bl%d]fade=t=in:st=%.3f:d=%s:alpha=1,fade=t=out:st=%.3f:d=%s:alpha=1[bf%d]" % (i, a - start, D, b - D - start, D, i))
            fc.append("[%s][bf%d]overlay=format=auto[g%d]" % (cur, i, i + 1))
            cur = "g%d" % (i + 1)
    fc += ["[%s][2:v]overlay=format=auto[b1]" % cur,
           "[b1][pz]%s[b2]" % ovp,
           "[b2][3:v]overlay=format=auto,%s[v]" % TO_YUV]
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-ss", "%.3f" % start, "-i", str(presenter),
           "-ss", "%.3f" % start, "-i", str(matte),
           "-framerate", str(fps), "-start_number", str(f0), "-i", str(out / "back" / "%05d.png"),
           "-framerate", str(fps), "-start_number", str(f0), "-i", str(out / "front" / "%05d.png"),
           "-framerate", str(fps), "-loop", "1", "-i", str(out / "grad.png")]
    if backdrops:
        cmd += ["-framerate", str(fps), "-start_number", str(f0), "-i", str(out / "bd" / "%05d.png")]
    cmd += ["-filter_complex", ";".join(fc), "-map", "[v]", "-frames:v", str(f1 - f0),
           "-c:v", "libx264", "-preset", "slow", "-crf", str(crf), "-pix_fmt", "yuv420p", "-profile:v", "high", *BT709, str(silent)]
    subprocess.run(cmd, check=True)


def mux_audio(silent, mp4, dur, voice=None, music=None, music_vol="0.18", loudnorm=True):
    """Voice and/or music onto the picture. Music ducks under the voice and fades out; the mix is normalised (two-pass) to -14 LUFS."""
    cmd = ["ffmpeg", "-y", "-hide_banner", "-nostats", "-i", str(silent)]
    graph = None
    if voice and music:
        cmd += ["-i", str(voice), "-stream_loop", "-1", "-i", str(music)]
        graph = (f"[2:a]volume={music_vol},afade=t=out:st={max(0, dur - 2):.2f}:d=2[m];"
                 "[m][1:a]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[md];"
                 "[1:a][md]amix=inputs=2:duration=first:normalize=0")
    elif voice:
        cmd += ["-i", str(voice)]
        graph = "[1:a]anull"
    elif music:          # captions-and-music video: the track at full level, faded out at the end
        cmd += ["-stream_loop", "-1", "-i", str(music)]
        graph = f"[1:a]afade=t=out:st={max(0, dur - 2):.2f}:d=2"
    tail = ["-c:v", "copy", "-t", f"{dur:.3f}", "-movflags", "+faststart", str(mp4)]
    if graph is None:
        subprocess.run(cmd + ["-loglevel", "error", "-an"] + tail, check=True)
        return None
    graph += f",apad,atrim=0:{dur:.3f}"
    measured = None
    if loudnorm:
        log = subprocess.run(cmd + ["-filter_complex", graph + f",loudnorm={LOUD}:print_format=json[a]", "-map", "[a]", "-f", "null", "-"],
                             capture_output=True, text=True).stderr
        m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", log)
        if m:
            j = json.loads(m.group(0))
            if "inf" not in j["input_i"]:
                measured = j
                graph += (f",loudnorm={LOUD}:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
                          f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    subprocess.run(cmd + ["-loglevel", "error", "-filter_complex", graph + ",aresample=48000[a]", "-map", "0:v", "-map", "[a]",
                          "-c:a", "aac", "-b:a", "256k", "-ar", "48000"] + tail, check=True)
    return measured


def cmd_render(a):
    p = proj(a.project)
    warn_config(p)
    out = ROOT / "frames" / f"short-{p.name}"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    silent = out / "silent.mp4"
    matte = next(iter(sorted(p.glob("*matte*.mkv"))), None)
    test = a.start is not None or a.end is not None
    if matte and re.search(r"\bsplit\s*:\s*true", (p / "script.js").read_text(encoding="utf-8")):
        print("NOTE: this script uses the split layout, which plays the footage in the page; the cut-out is not used for this render.")
        matte = None
    if any(p.glob("presenter.*")) and matte:
        # presenter + cutout: graphics behind the person, the person, graphics in front
        dur, f0, f1, moves, backdrops = asyncio.run(frames_layered(p, out, a.fps, a.workers, a.start, a.end))
        composite(p, matte, out, silent, a.fps, f0, f1, a.crf, moves, backdrops)
    else:
        if any(p.glob("presenter.*")) and re.search(r"\bmoves\s*:\s*\[\s*\{", (p / "script.js").read_text(encoding="utf-8")):
            print("NOTE: no cut-out, so the moves run on the whole picture (zoom, pan, the footage shrinks into a card) and graphics sit on top.\n"
                  "      For graphics BEHIND the person, cut them out first: python tools/matte.py %s" % (p / "presenter.mp4"), file=sys.stderr)
        dur, f0, f1 = asyncio.run(frames(p, out, a.fps, a.workers, a.start, a.end))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(a.fps), "-start_number", str(f0), "-i", str(out / "%05d.png"),
                        "-vf", TO_YUV, "-c:v", "libx264", "-preset", "slow", "-crf", str(a.crf), "-pix_fmt", "yuv420p",
                        "-profile:v", "high", "-x264-params", "aq-mode=3", *BT709, str(silent)], check=True)
    if test:
        t = p / "output" / f"{p.name}-test.mp4"
        t.parent.mkdir(exist_ok=True)
        shutil.copy(silent, t)
        print(f"wrote {t} (test cut {f0 / a.fps:.1f}-{f1 / a.fps:.1f}s, no audio)")
        return
    mp4 = p / "output" / ("%s-%dx%d.mp4" % ((p.name,) + frame_size(p)))
    mp4.parent.mkdir(exist_ok=True)
    voice = p / "voice.mp3"
    measured = mux_audio(silent, mp4, dur, voice if voice.exists() else None, a.music, a.music_vol, not a.no_loudnorm)
    size = mp4.stat().st_size / 1e6
    print(f"wrote {mp4}  ({dur:.1f}s, {size:.1f} MB, {size * 8 / dur:.1f} Mbps"
          + (f", audio {measured['input_i']} -> -14 LUFS" if measured else ", no audio" if not (voice.exists() or a.music) else "") + ")")
    cfg = load_config(p) or {}
    if str((cfg.get("answers") or {}).get("ai_disclosure") or "").startswith("yes"):
        print("REMINDER: this video has realistic AI-made content. Switch on the platform's AI label when you upload it.")


# ---------- capture ----------
async def capture(p, url, find, name, height, width):
    """Read-only: load a public page like a phone, find the text to highlight, screenshot just that area."""
    from playwright.async_api import async_playwright
    shots = p / "shots"
    shots.mkdir(exist_ok=True)
    k = 3  # device pixels per CSS pixel (device_scale_factor below)
    async with async_playwright() as pw:
        browser = await launch(pw, h264=True)
        ctx = await browser.new_context(
            viewport={"width": width, "height": 932}, device_scale_factor=k, locale="en-AU",
            user_agent="Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Mobile Safari/537.36 Edg/130.0")
        pg = await ctx.new_page()
        try:
            await pg.goto(url, wait_until="networkidle", timeout=60000)
        except Exception as e:
            print(f"load issue ({e.__class__.__name__}); capturing what loaded")
        await pg.wait_for_timeout(2000)
        for sel in ["button:has-text('Decline')", "button:has-text('Reject')", "button:has-text('Accept only essential')"]:
            try:
                await pg.locator(sel).first.click(timeout=800)  # close consent banners, never accept tracking
            except Exception:
                pass
        headings = await pg.evaluate(
            "() => [...document.querySelectorAll('h1,h2,h3')].map(h => h.innerText.trim()).filter(Boolean).slice(0, 12)")
        matches = []
        if find:
            matches = await pg.evaluate("""(t) => {
                t = t.toLowerCase(); const hits = [];
                for (const el of document.querySelectorAll('p,li,h1,h2,h3,h4,dd,dt,blockquote,td,a,span,div')) {
                    const txt = (el.innerText || '').trim();
                    if (!txt || !txt.toLowerCase().includes(t)) continue;
                    if ([...el.children].some(c => (c.innerText || '').toLowerCase().includes(t))) continue; // keep the deepest element
                    const r = el.getBoundingClientRect();
                    if (r.width < 2 || r.height < 2) continue;
                    hits.push({ text: txt.slice(0, 160), x: r.left, y: r.top + scrollY, w: r.width, h: r.height });
                }
                return hits.slice(0, 6);
            }""", find)
            if not matches:
                print(f"'{find}' was not found on the page; capturing the top instead (check the headings list)")
        page_h = await pg.evaluate("() => document.documentElement.scrollHeight")
        if matches:
            m = matches[0]
            top = max(0, m["y"] - 240)
            bottom = min(page_h, m["y"] + m["h"] + 700)
        else:
            top, bottom = 0, min(page_h, height)
        clip_h = bottom - top
        out = shots / f"{name}.png"
        await pg.screenshot(path=str(out), full_page=True, clip={"x": 0, "y": top, "width": width, "height": clip_h})
        await browser.close()

    marks = [{"y": round((m["y"] - top) * k), "h": round(m["h"] * k), "at": 1.2} for m in matches[:1]]
    start = max(0, marks[0]["y"] - 600) if marks else 0
    info = {
        "img": f"shots/{name}.png", "url": url, "srcWidth": width * k, "height_px": round(clip_h * k),
        "headings": headings, "matches": matches,
        "scene": {"type": "web", "img": f"shots/{name}.png", "url": url.split("//")[-1].rstrip("/"),
                  "srcWidth": width * k, "from": start, "to": start, "marks": marks},
    }
    (shots / f"{name}.json").write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
    return info


def cmd_capture(a):
    p = proj(a.project)
    name = a.name or re.sub(r"[^a-z0-9]+", "-", a.url.split("//")[-1].lower()).strip("-")[:40]
    info = asyncio.run(capture(p, a.url, a.find, name, a.height, a.width))
    print(f"wrote {p / 'shots' / (name + '.png')} ({info['height_px'] // 3}px tall, CSS)")
    print("headings:", info["headings"][:6])
    for m in info["matches"][:3]:
        print("match:", m["text"][:110])
    print("scene (paste into script.js and set its time):")
    print(json.dumps(info["scene"], ensure_ascii=False))


# ---------- reference frames ----------
def cmd_frames(a):
    """Cut a reference video into one frame per --every seconds and draw a 1080x1920 coordinate grid on each,
    so caption, graphic and face positions can be read off in pixels and copied into script.js."""
    from PIL import Image, ImageDraw
    p = proj(a.project)
    src = pathlib.Path(a.video).resolve()
    out = p / "ref"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(src), "-vf",
                    f"fps=1/{a.every},scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black",
                    str(out / "f_%03d.jpg")], check=True)
    files = sorted(out.glob("f_*.jpg"))
    cols, w, h = 5, 216, 384
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows * (h + 22)), "white")
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(files):
        im = Image.open(f).convert("RGB").resize((w, h))
        x, y = (i % cols) * w, (i // cols) * (h + 22)
        sheet.paste(im, (x, y + 22))
        for gy in range(0, 1920, 240):  # grid every 240 px (1/8 of the height)
            yy = y + 22 + int(gy * h / 1920)
            d.line([(x, yy), (x + w, yy)], fill=(255, 0, 0), width=1)
            d.text((x + 3, yy + 1), str(gy), fill=(255, 0, 0))
        for gx in range(0, 1080, 270):
            xx = x + int(gx * w / 1080)
            d.line([(xx, y + 22), (xx, y + 22 + h)], fill=(0, 160, 255), width=1)
        d.text((x + 3, y + 4), f"{i * a.every}s", fill="black")
    sheet_path = out / "grid-sheet.jpg"
    sheet.save(sheet_path, quality=88)
    print(f"{len(files)} frames in {out}")
    print(f"grid sheet: {sheet_path}  (red lines = y in px of 1920; blue = x in px of 1080)")


# ---------- brand ----------
BRAND_JS = r"""() => {
  const meta = n => (document.querySelector(`meta[property="${n}"],meta[name="${n}"]`) || {}).content || '';
  const rgb = c => { const m = String(c).match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(/[ ,\/]+/).map(parseFloat); return (p[3] === 0) ? null : p.slice(0, 3); };
  const hexOf = p => '#' + p.map(v => Math.round(v).toString(16).padStart(2, '0')).join('');
  const hsl = ([r, g, b]) => { r /= 255; g /= 255; b /= 255; const mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2, d = mx - mn;
    if (!d) return [0, 0, l]; const s = d / (1 - Math.abs(2 * l - 1)); let h = mx === r ? ((g - b) / d) % 6 : mx === g ? (b - r) / d + 2 : (r - g) / d + 4; return [(h * 60 + 360) % 360, s, l]; };
  const votes = {};
  const vote = (c, w, why) => { const p = typeof c === 'string' && c[0] === '#' ? [1, 3, 5].map(i => parseInt(c.length === 4 ? c[(i + 1) / 2].repeat(2) : c.slice(i, i + 2), 16)) : rgb(c);
    if (!p || p.some(isNaN)) return; const [h, s, l] = hsl(p); if (s < .25 || l < .12 || l > .85) return;      // greys, near-black and near-white are not brand colours
    const k = hexOf(p); votes[k] = votes[k] || {hex: k, hue: h, w: 0, why: []}; votes[k].w += w; if (!votes[k].why.includes(why)) votes[k].why.push(why); };
  vote(meta('theme-color'), 6, 'theme-color meta');
  const root = getComputedStyle(document.documentElement);
  for (const sheet of document.styleSheets) { let rules; try { rules = sheet.cssRules; } catch (e) { continue; }
    for (const r of rules) if (r.selectorText && /^(:root|html|body)$/.test(r.selectorText.trim())) for (const name of r.style)
      if (name.startsWith('--') && /primary|brand|accent|main|theme/i.test(name)) { const v = root.getPropertyValue(name).trim(); vote(/^#/.test(v) ? v : (v.startsWith('rgb') ? v : ''), 5, 'CSS variable ' + name); } }
  const area = el => { const r = el.getBoundingClientRect(); return Math.min(4, Math.max(.5, r.width * r.height / 8000)); };
  document.querySelectorAll('button, [class*="btn" i], [class*="button" i], [role="button"], input[type="submit"]').forEach(el => { const r = el.getBoundingClientRect(); if (r.width > 20 && r.height > 12) vote(getComputedStyle(el).backgroundColor, 3 * area(el), 'buttons'); });
  document.querySelectorAll('header, nav, footer, [class*="hero" i], [class*="banner" i]').forEach(el => vote(getComputedStyle(el).backgroundColor, 2, 'header / hero background'));
  [...document.querySelectorAll('a')].slice(0, 80).forEach(el => vote(getComputedStyle(el).color, .4, 'links'));
  [...document.querySelectorAll('h1, h2')].slice(0, 12).forEach(el => vote(getComputedStyle(el).color, 1.5, 'headings'));
  const ranked = Object.values(votes).sort((a, b) => b.w - a.w);
  const accent = ranked[0] || null, far = (a, b) => Math.min(Math.abs(a - b), 360 - Math.abs(a - b)) >= 40;
  const secondary = accent ? ranked.find(v => far(v.hue, accent.hue)) || null : null;
  // logo: an image or SVG that calls itself a logo, else the first image inside the home link / header
  const vis = el => { const r = el.getBoundingClientRect(); return r.width >= 24 && r.height >= 12 && r.width <= 700 && r.top < 1400 && getComputedStyle(el).visibility !== 'hidden'; };
  const picks = ['img[src*="logo" i]', 'img[alt*="logo" i]', '[class*="logo" i] img', '[id*="logo" i] img', '[class*="logo" i] svg', '[id*="logo" i] svg', 'svg[class*="logo" i]',
                 'header a[href="/"] img', 'header a[href="/"] svg', '[class*="brand" i] img', '[class*="brand" i] svg', 'header img', 'nav img'];
  let logo = null, how = '';
  for (const sel of picks) { const el = [...document.querySelectorAll(sel)].find(vis); if (el) { el.setAttribute('data-shorts-logo', '1'); logo = el.tagName; how = sel; break; } }
  let bgUnder = null; if (logo) { for (let e = document.querySelector('[data-shorts-logo]'); e; e = e.parentElement) { const p = rgb(getComputedStyle(e).backgroundColor); if (p) { bgUnder = hexOf(p); break; } } }
  const icon = [...document.querySelectorAll('link[rel~="apple-touch-icon"], link[rel~="icon"]')].map(l => ({href: l.href, size: parseInt((l.sizes && l.sizes.value) || '0') || (l.rel.includes('apple') ? 180 : 16)})).sort((a, b) => b.size - a.size)[0];
  const socials = {}; document.querySelectorAll('a[href]').forEach(a => { const m = a.href.match(/(tiktok|instagram|youtube|facebook|linkedin|x|twitter)\.com\/(@?[\w.\-]+)/i);
    if (m && !/^(share|sharer|intent|watch|p|reel)$/i.test(m[2])) socials[m[1].toLowerCase()] = socials[m[1].toLowerCase()] || m[2]; });
  const fam = el => el ? getComputedStyle(el).fontFamily.split(',')[0].replace(/["']/g, '').trim() : '';
  const name = meta('og:site_name') || (document.title || '').split(/\s[|–—\-:·]\s/)[0].trim();
  return {name, title: document.title, description: meta('description') || meta('og:description'), ogImage: meta('og:image'), icon: icon && icon.href,
          accent, secondary, ranked: ranked.slice(0, 6).map(v => ({hex: v.hex, weight: +v.w.toFixed(1), from: v.why})), logo, logoFrom: how, logoBackground: bgUnder, socials,
          fonts: {heading: fam(document.querySelector('h1, h2')), body: fam(document.body)}, lang: document.documentElement.lang || ''};
}"""


def _lum(hexc):
    r, g, b = [(v / 255 / 12.92) if v / 255 <= 0.03928 else ((v / 255 + 0.055) / 1.055) ** 2.4 for v in _hex(hexc)]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


async def brand_crawl(p, url):
    """Read-only visit of a public page: name, description, logo, colours, fonts, social handles. Nothing is clicked or submitted."""
    from playwright.async_api import async_playwright
    out = p / "brand"
    out.mkdir(exist_ok=True)
    async with async_playwright() as pw:
        browser = await launch(pw)
        ctx = await browser.new_context(viewport={"width": 1366, "height": 900}, device_scale_factor=2)
        pg = await ctx.new_page()
        try:
            await pg.goto(url, wait_until="networkidle", timeout=45000)
        except Exception as e:
            if pg.url in ("about:blank", "") or pg.url.startswith("chrome-error"):
                await browser.close()
                sys.exit("could not open %s (%s). Give the brand by hand instead:\n  python tools/shorts.py brand %s --name \"...\" --accent \"#hex\" --logo file.png"
                         % (url, str(e).splitlines()[0][:120], p.name))
        await pg.wait_for_timeout(800)
        info = await pg.evaluate(BRAND_JS)
        logo = None
        if info["logo"]:
            try:
                el = pg.locator("[data-shorts-logo]").first
                await el.screenshot(path=str(out / "logo.png"), omit_background=True)
                logo = "brand/logo.png"
            except Exception:
                pass
        if not logo:
            for src in filter(None, [info.get("icon"), info.get("ogImage")]):
                try:
                    r = await ctx.request.get(src, timeout=20000)
                    if r.ok and len(await r.body()) > 200:
                        ext = (re.search(r"\.(png|jpe?g|svg|webp|ico)(?:\?|$)", src, re.I) or [None, "png"])[1].lower()
                        (out / ("logo." + ext)).write_bytes(await r.body())
                        logo, info["logoFrom"] = "brand/logo." + ext, "site icon" if src == info.get("icon") else "og:image"
                        break
                except Exception:
                    pass
        await pg.screenshot(path=str(out / "site.jpg"), type="jpeg", quality=70)
        await browser.close()
    info["logoFile"] = logo
    return info


def cmd_brand(a):
    """Brand kit for a project: brand.js (used by the engine) and brand/brand.json (everything that was found, for the director)."""
    p = proj(a.project)
    info = {}
    if a.url:
        url = a.url if re.match(r"https?://|file:", a.url) else "https://" + a.url
        info = asyncio.run(brand_crawl(p, url))
        info["url"] = url
    if a.clear:
        for x in (p / "brand.js", p / "brand" / "brand.json"):
            x.unlink(missing_ok=True)
        print("brand removed: the project uses the clean neutral look")
        return
    old = {}
    if (p / "brand" / "brand.json").exists() and not a.url:
        old = json.loads((p / "brand" / "brand.json").read_text(encoding="utf-8"))
    theme = dict(old.get("theme") or {})
    if info.get("accent"):
        theme["accent"] = info["accent"]["hex"]
    if info.get("secondary"):
        theme["secondary"] = info["secondary"]["hex"]
    for k in ("accent", "secondary", "dark", "bg"):
        v = getattr(a, k)
        if v:
            theme[k] = v if v.startswith("#") else "#" + v
    if theme.get("accent") and "dark" not in theme:
        r, g, b = _hex(theme["accent"])
        theme["dark"] = "#%02x%02x%02x" % (int(r * 0.22), int(g * 0.22), int(b * 0.26))     # cards: a deep shade of the brand colour
    logo = old.get("logo")
    if info.get("logoFile"):
        logo = info["logoFile"]
    if a.logo:
        src = pathlib.Path(a.logo)
        (p / "brand").mkdir(exist_ok=True)
        if src.resolve().parent != (p / "brand").resolve():
            shutil.copy(src, p / "brand" / ("logo" + src.suffix.lower()))
        logo = "brand/logo" + src.suffix.lower()
    name = a.name or info.get("name") or old.get("name") or ""
    socials = info.get("socials") or old.get("socials") or {}
    handle = a.handle or old.get("handle") or next(("@" + h.lstrip("@") for k in ("tiktok", "instagram", "youtube") for h in [socials.get(k)] if h), "")
    brand = {"name": name, "handle": handle, "url": info.get("url") or old.get("url") or "", "logo": logo, "theme": theme,
             "description": info.get("description") or old.get("description") or "", "socials": socials,
             "fonts": info.get("fonts") or old.get("fonts") or {}, "found": {k: info.get(k) for k in ("ranked", "logoFrom", "logoBackground", "title", "lang")} if info else old.get("found", {})}
    if not (name or theme or logo):
        sys.exit("nothing to save: give --url, or --name / --accent / --logo")
    (p / "brand").mkdir(exist_ok=True)
    (p / "brand" / "brand.json").write_text(json.dumps(brand, ensure_ascii=False, indent=2), encoding="utf-8")
    (p / "brand.js").write_text("// written by tools/shorts.py brand: the brand this short is made for (details in brand/brand.json)\n"
                                "window.BRAND = %s;\n" % json.dumps({k: brand[k] for k in ("name", "handle", "url", "logo", "theme")}, ensure_ascii=False, indent=2), encoding="utf-8")
    cfg = load_config(p)
    if cfg and brand["url"] and cfg["answers"].get("brand") in (None, "", "none"):
        cfg["answers"]["brand"] = brand["url"]
        save_config(p, cfg)
    print("brand: %s%s" % (name or "(no name)", "  " + handle if handle else ""))
    print("  logo    %s%s" % (logo or "none found (give one with --logo file.png)", ("  [from %s]" % info["logoFrom"]) if info.get("logoFile") else ""))
    if logo and info.get("logoBackground") and _lum(info["logoBackground"]) < 0.2:
        print("          the logo sits on a dark background on the site, so it is probably light: fine over backdrops, weak on the light look (use look: 'dark')")
    print("  accent  %s%s" % (theme.get("accent", "none found: the clean look's blue is used (set one with --accent \"#hex\")"),
                              ("  [from %s]" % ", ".join(info["accent"]["why"])) if info.get("accent") else ""))
    if theme.get("secondary"):
        print("  second  %s" % theme["secondary"])
    for r_ in (info.get("ranked") or [])[1:4]:
        print("  other   %s  (%s)" % (r_["hex"], ", ".join(r_["from"])))
    if brand["description"]:
        print("  about   %s" % brand["description"][:140])
    if info:
        print("  fonts   heading: %s, body: %s  (recorded only; the video keeps its own fonts unless you add the font files)" % (brand["fonts"].get("heading") or "?", brand["fonts"].get("body") or "?"))
        print("  look at %s to confirm the colours match the site" % (p / "brand" / "site.jpg"))
    print("wrote %s and brand/brand.json. script.js uses the brand unless it sets its own `look`." % (p / "brand.js"))


# ---------- lint ----------
LINT_JS = """async () => {
  const st = document.getElementById('stage'), cs = getComputedStyle(st), px = v => parseFloat(cs.getPropertyValue(v)) || 0;
  const safe = {top: px('--safe-top'), bottom: px('--safe-bottom'), left: px('--safe-left'), right: px('--safe-right')};
  const k = st.getBoundingClientRect().width / (window.STAGE_W || 1080), o = st.getBoundingClientRect();
  // the box of the text itself (a centred line in a full-width block must not count as touching the edges)
  const R = el => { let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; const rg = document.createRange();
    for (const n of el.childNodes) { if (n.nodeType !== 3 || !n.textContent.trim()) continue; rg.selectNodeContents(n);
      for (const r of rg.getClientRects()) { x0 = Math.min(x0, r.left); y0 = Math.min(y0, r.top); x1 = Math.max(x1, r.right); y1 = Math.max(y1, r.bottom); } }
    return {x: (x0 - o.left) / k, y: (y0 - o.top) / k, w: (x1 - x0) / k, h: (y1 - y0) / k}; };
  const shown = el => { for (let e = el; e && e !== st; e = e.parentElement) { const c = getComputedStyle(e); if (c.visibility === 'hidden' || c.display === 'none' || +c.opacity < .05) return false; } return true; };
  const leaves = root => [...root.querySelectorAll('*')].filter(e => shown(e) && ([...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) ));
  const out = [];
  for (const [i, sc] of window.SCENE_INFO.entries()) {
    const el = document.querySelector(`[data-scene="${i}"]`), at = Math.max(sc.t + .05, Math.min(sc.end - .45, sc.t + 4));
    TL.seek(at); await window.seekMedia(at);
    const boxes = leaves(el).map(e => ({...R(e), text: e.textContent.trim().slice(0, 40)})).filter(b => b.w > 1 && b.h > 1);
    const media = [...el.querySelectorAll('img,video')].map(m => ({src: (m.getAttribute('src') || '').split('/').pop(), ok: m.tagName === 'IMG' ? (m.complete && m.naturalWidth > 0) : (!m.error && m.readyState > 0)}));
    // the other lane's elements on screen at this moment (for overlap)
    const others = [...document.querySelectorAll('[data-scene]')].filter(x => x !== el && shown(x) && window.SCENE_INFO[+x.dataset.scene].lane !== sc.lane)
      .map(x => ({scene: +x.dataset.scene, boxes: leaves(x).map(R).filter(b => b.w > 1 && b.h > 1)}));
    out.push({i, at, boxes, media, others});
  }
  const bds = [...document.querySelectorAll('#bds img, #bds video, #pvideo')].filter(m => m.getAttribute('src')).map(m => ({src: m.getAttribute('src').split('/').pop(), ok: m.tagName === 'IMG' ? (m.complete && m.naturalWidth > 0) : (!m.error && m.readyState > 0)}));
  const changes = [...new Set(TL.getChildren(false, true, false).filter(c => c.duration() > .05).map(c => Math.round(c.startTime() * 10) / 10))].sort((a, b) => a - b);
  return {safe, changes, scenes: window.SCENE_INFO, probes: out, dur: window.DUR, errors: window.PAGE_ERRORS || [], media: bds,
          script: {scenes: window.SCRIPT.scenes, captions: !!window.SCRIPT.captions, audio: window.SCRIPT.audio, presenter: window.SCRIPT.presenter, safe: window.SCRIPT.safe, hasWords: (window.WORDS || []).length, hasSegs: (window.SEGMENTS || []).length}};
}"""
CPS = 17            # reading speed, characters per second (Netflix subtitle limit for adults; used here as a proxy)
MIN_HOLD = 0.85     # shortest time any text should stay up, seconds
RAIL_TOP = 800      # the right-hand button column starts about here (y px); above it the right edge is free (inferred from the templates)
MAX_GAP = 5.0       # longest stretch with nothing new on screen, seconds (practitioner convention: 2-4 s)


def _length_range(text):
    nums = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", str(text or ""))]
    return (min(nums), max(nums)) if nums else None


async def lint(p):
    """Open the page, visit every scene and report what breaks the rules. Returns a list of {level, t, scene, type, rule, msg}."""
    from playwright.async_api import async_playwright
    cat = json.loads((TEMPLATE / "scenes.json").read_text(encoding="utf-8"))
    found = []

    def add(level, rule, msg, t=None, i=None, typ=None):
        found.append({"level": level, "rule": rule, "t": None if t is None else round(t, 2), "scene": i, "type": typ, "msg": msg})

    async with async_playwright() as pw:
        browser, page = await open_page(pw, p / "short.html", any(p.glob("presenter.*")))
        d = await page.evaluate(LINT_JS)
        net = issues_of(page)
        await browser.close()
    for x in dict.fromkeys(net + d["errors"]):
        add("error", "load", x)
    for m in d["media"]:
        if not m["ok"]:
            add("error", "missing-file", "backdrop or footage did not load: %s" % m["src"])
    safe, scenes, dur = d["safe"], d["scenes"], d["dur"]
    W, H = frame_size(p)
    rail = RAIL_TOP if H > W else 0          # landscape: no button column, the right margin applies all the way down
    FULL = {"broll", "hero", "web", "doc", "photo", "phone", "screen", "mindmap", "stickies", "tags", "orb", "orbit"}     # picture scenes: only frame cut-off is checked, not the safe zone
    for sc, pr in zip(scenes, d["probes"]):
        i, typ, t = pr["i"], sc["type"], sc["t"]
        for m in pr["media"]:
            if not m["ok"]:
                add("error", "missing-file", "did not load: %s" % m["src"], t, i, typ)
        cut = [b for b in pr["boxes"] if b["x"] < -2 or b["y"] < -2 or b["x"] + b["w"] > W + 2 or b["y"] + b["h"] > H + 2]
        if cut and typ not in ("web", "doc", "mindmap", "screen", "phone"):     # these move a camera or a device through the frame on purpose
            add("error", "cut-off", "text runs off the frame: “%s”" % cut[0]["text"], t, i, typ)
        if typ not in FULL:
            for b in pr["boxes"]:
                side = ("top" if b["y"] < safe["top"] - 2 else "bottom" if b["y"] + b["h"] > H - safe["bottom"] + 2 else
                        "left" if b["x"] < safe["left"] - 2 else
                        "right" if b["x"] + b["w"] > W - safe["right"] + 2 and b["y"] + b["h"] > rail else None)
                if side and not (b in cut):
                    add("warn", "safe-zone", "“%s” sits in the %s unsafe area (app buttons / text cover it)" % (b["text"], side), t, i, typ)
                    break
        if sc["lane"] == "cap":
            for o in pr["others"]:
                hit = any(a["x"] < b["x"] + b["w"] - 6 and b["x"] < a["x"] + a["w"] - 6 and a["y"] < b["y"] + b["h"] - 6 and b["y"] < a["y"] + a["h"] - 6
                          for a in pr["boxes"] for b in o["boxes"])
                if hit:
                    other = scenes[o["scene"]]
                    add("error", "overlap", "caption “%s” sits on top of the %s scene's text (move it with pos:'top'|'mid'|'low' or shorten the scene)" % (sc["key"][:30], other["type"]), t, i, typ)
        hold = sc["end"] - sc["t"]
        if sc["lane"] == "cap":
            chars = len(sc["key"]) + len(sc["lead"])
            need = max(MIN_HOLD, chars / CPS)
            if hold + 0.05 < need:
                add("warn", "dwell", "caption is up for %.1fs but needs about %.1fs to read (%d characters)" % (hold, need, chars), t, i, typ)
            if len(sc["key"].split()) > 5:
                add("warn", "caption-length", "key line has %d words; keep it to 2-5" % len(sc["key"].split()), t, i, typ)
            if len(sc["lead"].split()) > 7:
                add("warn", "caption-length", "lead line has %d words; keep it to 3-6" % len(sc["lead"].split()), t, i, typ)
        elif hold < 1.0 and typ != "hero":
            add("warn", "dwell", "%s is on screen for only %.1fs" % (typ, hold), t, i, typ)
    # script-level rules
    raw = d["script"]["scenes"]
    for n, sc in enumerate(raw):
        spec = cat["scenes"].get(sc.get("type"))
        if not spec:
            add("error", "unknown-type", "scene %d has type '%s'; known types: %s" % (n, sc.get("type"), ", ".join(cat["scenes"])))
            continue
        for key in spec["required"]:
            if sc.get(key) in (None, "", []):
                add("error", "missing-field", "%s scene needs `%s`" % (sc["type"], key), sc.get("t"))
        n_items = len(sc.get("items") or sc.get("points") or [])
        limits = {"chart": 6, "compare": 3, "list": 5, "timeline": 5, "line": 8, "badges": 3, "pills": 6, "glass": 5, "stickies": 5, "tags": 3, "pillar": 4, "diamonds": 4, "lanes": 6, "rules": 4}
        if n_items > limits.get(sc["type"], 99):
            add("warn", "too-much", "%s has %d items; more than %d does not read on a phone" % (sc["type"], n_items, limits[sc["type"]]), sc.get("t"))
        if sc["type"] == "chart" and not sc.get("note"):
            add("warn", "source", "chart has no `note` naming where the numbers come from", sc.get("t"))
    starts = sorted({s_["t"] for s_ in scenes})
    if not starts or starts[0] > 0.1:
        add("warn", "hook", "nothing is on screen at 0.0s; the hook must be there from the first frame")
    WORDY = {"kinetic", "phone", "stickies", "bignum"}       # scenes whose own words can be the hook
    if not any((s_["lane"] == "cap" or s_["type"] in WORDY) and s_["t"] <= 1.5 for s_ in scenes) and not d["script"].get("captions"):
        add("warn", "hook", "no caption, title or headline scene in the first 1.5s")
    moves_ = [c for c in d["changes"] if c < dur - 0.3]       # every moment something starts moving (rows, bars, words)
    for a_, b_ in zip(moves_, moves_[1:] + [dur]):
        if b_ - a_ > MAX_GAP + 0.01:
            add("warn", "pacing", "nothing new on screen for %.1fs (aim for a change every 2-4s)" % (b_ - a_), a_)
    vis = sorted((s_ for s_ in scenes if s_["lane"] == "vis"), key=lambda s_: s_["t"])
    for a_, b_ in zip(vis, vis[1:]):
        if a_["type"] == b_["type"] and a_["type"] not in ("broll", "photo", "kinetic", "orb", "screen"):
            add("warn", "variety", "two %s scenes in a row" % a_["type"], b_["t"])
    if vis and not (vis[-1]["type"] in ("cta", "kinetic") and dur - vis[-1]["t"] <= 6):
        add("warn", "ending", "the video does not end on a `cta` (one clear action) or a closing `kinetic` line in the last 3-4s")
    cfg = load_config(p)
    if cfg is None or cfg.get("status") != "ready":
        add("warn", "config", "project setup is not finished: python tools/shorts.py config %s --interactive" % p.name)
    else:
        ans = cfg["answers"]
        rng = _length_range(ans.get("length_seconds"))
        if rng and not (rng[0] - 2 <= dur <= rng[1] + 2):
            add("warn", "length", "video is %.1fs; the project asked for %s s" % (dur, ans.get("length_seconds")))
        want = "strict" if str(ans.get("safe_zone", "")).startswith("paid") else "organic"
        if (d["script"]["safe"] or "organic") != want:
            add("warn", "safe-zone", "config says '%s' but script.js has safe: '%s'" % (ans.get("safe_zone"), d["script"]["safe"] or "organic"))
        if str(ans.get("ai_disclosure") or "").startswith("yes"):
            add("info", "ai-label", "realistic AI-made content: switch on the platform's AI label when uploading")
    return found, {"duration": round(dur, 2), "scenes": len(scenes), "safe": safe}


def cmd_lint(a):
    p = proj(a.project)
    found, meta = asyncio.run(lint(p))
    errors = sum(x["level"] == "error" for x in found)
    warns = sum(x["level"] == "warn" for x in found)
    if a.json:
        print(json.dumps({"project": p.name, **meta, "errors": errors, "warnings": warns, "problems": found}, ensure_ascii=False, indent=2))
    else:
        for x in sorted(found, key=lambda x: ({"error": 0, "warn": 1, "info": 2}[x["level"]], x["t"] or 0)):
            where = ("%6.2fs " % x["t"]) if x["t"] is not None else "        "
            print("%-5s %s%-14s %s" % (x["level"].upper(), where, x["rule"], x["msg"]))
        print("%s: %.1fs, %d scenes, %d errors, %d warnings" % (p.name, meta["duration"], meta["scenes"], errors, warns))
    if errors or (a.strict and warns):
        sys.exit(1)


# ---------- word timings ----------
def _words_from_chars(chars, starts, ends):
    words, cur, s0, e0 = [], "", None, None
    for c, s, e in zip(chars, starts, ends):
        if c.isspace():
            if cur:
                words.append({"w": cur, "s": round(s0, 3), "e": round(e0, 3)})
            cur, s0 = "", None
        else:
            cur += c
            s0 = s if s0 is None else s0
            e0 = e
    if cur:
        words.append({"w": cur, "s": round(s0, 3), "e": round(e0, 3)})
    return words


def _stamp(x):
    h_, m, s = x.replace(",", ".").split(":")[-3:] if x.count(":") == 2 else ["0"] + x.replace(",", ".").split(":")
    return int(h_) * 3600 + int(m) * 60 + float(s)


def parse_words(path):
    """Word timings from: a JSON list / {"words": [...]} with (w|word|text, s|start, e|end); an ElevenLabs alignment
    (characters + character_start_times_seconds); Whisper JSON (segments[].words[]); or .srt / .vtt (words spread evenly in each cue)."""
    path = pathlib.Path(path)
    raw = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() in (".srt", ".vtt"):
        words = []
        for m in re.finditer(r"([\d:.,]+)\s*-->\s*([\d:.,]+)[^\n]*\n((?:.+\n?)+)", raw):
            s, e = _stamp(m.group(1)), _stamp(m.group(2))
            toks = re.sub(r"<[^>]+>", "", m.group(3)).split()
            total = sum(len(t) for t in toks) or 1
            at = s
            for t in toks:
                d = (e - s) * len(t) / total
                words.append({"w": t, "s": round(at, 3), "e": round(at + d, 3)})
                at += d
        return words, "approximate (spread across each subtitle cue)"
    j = json.loads(raw)
    al = j.get("alignment") or j.get("normalized_alignment") or j if isinstance(j, dict) else None
    if isinstance(al, dict) and "characters" in al and "character_start_times_seconds" in al:
        return _words_from_chars(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]), "character timings"
    items = j if isinstance(j, list) else j.get("words") or [w for seg in j.get("segments", []) for w in seg.get("words", [])]
    words = []
    for w in items:
        text = str(w.get("w") or w.get("word") or w.get("text") or "").strip()
        s, e = w.get("s", w.get("start")), w.get("e", w.get("end"))
        if text and s is not None:
            words.append({"w": text, "s": round(float(s), 3), "e": round(float(e if e is not None else s + 0.3), 3)})
    return words, "word timings"


def _multipart(fields, files):
    b = uuid.uuid4().hex
    body = b""
    for k, v in fields.items():
        body += ("--%s\r\nContent-Disposition: form-data; name=\"%s\"\r\n\r\n%s\r\n" % (b, k, v)).encode()
    for k, (name, data, ctype) in files.items():
        body += ("--%s\r\nContent-Disposition: form-data; name=\"%s\"; filename=\"%s\"\r\nContent-Type: %s\r\n\r\n" % (b, k, name, ctype)).encode() + data + b"\r\n"
    return body + ("--%s--\r\n" % b).encode(), "multipart/form-data; boundary=" + b


def _eleven(url, data, ctype):
    key = os.environ.get("ELEVENLABS_API_KEY") or sys.exit("ELEVENLABS_API_KEY is not set in the environment (never put the key in a command or a file)")
    req = urllib.request.Request(url, data=data, method="POST", headers={"xi-api-key": key, "Content-Type": ctype})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        sys.exit("ElevenLabs refused the request (HTTP %d): %s" % (e.code, e.read().decode()[:300]))


def write_words(p, words, how):
    (p / "words.js").write_text("// written by tools/shorts.py align: every spoken word {w, s: start, e: end} in seconds (%s)\n"
                                "window.WORDS = %s;\n" % (how, json.dumps(words, ensure_ascii=False)), encoding="utf-8")
    print("%d words -> %s  (%s)" % (len(words), p / "words.js", how))
    print("  " + "  ".join("%s@%.2f" % (w["w"], w["s"]) for w in words[:12]) + (" ..." if len(words) > 12 else ""))
    print("use them in script.js:  { word: 'visa', type: ... } starts a scene when the word is said;  syncWords: true pops caption words in time")


def cmd_align(a):
    p = proj(a.project)
    voice = p / "voice.mp3"
    if a.source:
        words, how = parse_words(a.source)
        if not words:
            sys.exit("no word timings found in %s" % a.source)
        return write_words(p, words, how + ", from " + pathlib.Path(a.source).name)
    if not voice.exists():
        sys.exit(f"put the voiceover at {voice}")
    engine = a.engine
    if engine == "auto":
        try:
            import faster_whisper  # noqa: F401
            engine = "whisper"
        except ImportError:
            engine = "elevenlabs" if os.environ.get("ELEVENLABS_API_KEY") and a.text else None
    if engine == "whisper":
        from faster_whisper import WhisperModel
        segs, _ = WhisperModel(a.model, compute_type="int8").transcribe(str(voice), word_timestamps=True, language=a.language)
        words = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)} for sg in segs for w in sg.words if w.word.strip()]
        return write_words(p, words, "speech recognition, faster-whisper %s; check the spelling of names and numbers" % a.model)
    if engine == "elevenlabs":
        if not a.text:
            sys.exit("--text <file with the exact words spoken> is needed for ElevenLabs forced alignment")
        body, ctype = _multipart({"text": pathlib.Path(a.text).read_text(encoding="utf-8")}, {"file": ("voice.mp3", voice.read_bytes(), "audio/mpeg")})
        j = _eleven("https://api.elevenlabs.io/v1/forced-alignment", body, ctype)
        words = [{"w": w["text"].strip(), "s": round(float(w["start"]), 3), "e": round(float(w["end"]), 3)} for w in j.get("words", []) if w.get("text", "").strip()]
        if not words:
            sys.exit("ElevenLabs returned no words; the response keys were: %s" % ", ".join(j))
        return write_words(p, words, "ElevenLabs forced alignment")
    sys.exit("no way to time the words on this machine. Any ONE of these works:\n"
             "  - give timings you already have:   align %s --from words.json   (or .srt / .vtt, or the JSON any speech tool returns)\n"
             "  - pip install faster-whisper        (local, free; downloads a model once)\n"
             "  - set ELEVENLABS_API_KEY and pass   --text script.txt\n"
             "Word timings are optional: `segments` alone is enough to build a short." % p.name)


def cmd_voice(a):
    """Optional: make voice.mp3 from a script with ElevenLabs, and words.js from the timings it returns."""
    p = proj(a.project)
    text = pathlib.Path(a.text).read_text(encoding="utf-8").strip()
    if (p / "voice.mp3").exists() and not a.force:
        sys.exit("voice.mp3 already exists; --force replaces it (and spends credits again)")
    body = json.dumps({"text": text, "model_id": a.model_id}).encode()
    j = _eleven("https://api.elevenlabs.io/v1/text-to-speech/%s/with-timestamps?output_format=mp3_44100_128" % a.voice_id, body, "application/json")
    (p / "voice.mp3").write_bytes(base64.b64decode(j["audio_base64"]))
    print("wrote %s (%.1fs)" % (p / "voice.mp3", duration(p / "voice.mp3")))
    al = j.get("alignment") or j.get("normalized_alignment")
    if al:
        write_words(p, _words_from_chars(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]), "ElevenLabs timestamps")
    a.noise, a.min_pause = "-35", 0.35
    cmd_segments(a)


# ---------- plan: the director's first pass (content -> beats -> a design for each) ----------
STOP = set("a an the and or but so if then than that this these those is are was were be been being am do does did have has had i you he she it we they me my your our their them his her its of to in on at for with by from as about into over after before up down out off not no yes just very really can could will would should may might must there here what which who whom when where why how all any some each every both few more most other such only own same too also get got make made let like one two".split())
ROLES = [   # (role, pattern) checked in order; the first match names the beat
    ("cta",        r"\b(comment|follow|subscribe|link in (the )?bio|dm me|send (it|you)|download|sign up|book a|click|tap the|share this|save this)\b"),
    ("example",    r"\b(for example|for instance|let'?s say|imagine|picture this|suppose|here'?s an example)\b"),
    ("steps",      r"\b(first(ly)?,|second(ly)?,|third(ly)?,|step (one|two|three|\d)|next,|then you|finally|lastly)"),
    ("definition", r"\b(it'?s called|is called|are called|known as|what is|what really is|means that|stands for|think of it (like|as))\b"),
    ("compare",    r"\b(versus|vs\.?|compared (to|with)|instead of|rather than|better than|worse than|more than|less than|on the other hand|whereas)\b"),
    ("problem",    r"\b(the reason|the problem|that'?s why|because|struggl\w*|mistake|fail\w*|confus\w*|swipe away|churn|lose|losing|hard to)\b"),
    ("payoff",     r"\b(if you do this|you will|you'?ll|will go (way )?up|so that|which means|the result|that'?s how)\b"),
    ("list",       r"(\b\w+, \w+(,| and| or) \w+)"),
]
NUM = r"(\$?\d[\d,.]*(?:\s?(?:%|percent\b|x\b|k\b|million\b|billion\b|times\b|seconds?\b|minutes?\b|hours?\b|days?\b|weeks?\b|months?\b|years?\b))?|\b(two|three|four|five|six|seven|eight|nine|ten) (times|x|steps|ways|things|principles|rules|reasons|tips)\b)"
DESIGNS = {   # role -> scene per format: (type, layout, why)
    "data explainer": {"hook": ("title", "full", "the hook as two bold lines from the first frame"), "number": ("bignum", "full", "one number carries the point; add the source as a badge"),
                       "definition": ("kinetic", "full", "name the idea in two to four big words"), "problem": ("stamp", "full", "a verdict or the pain, slammed on screen"),
                       "example": ("quote", "full", "show the example sentence and highlight the phrase"), "steps": ("list", "full", "one row per step, each on its spoken beat"),
                       "list": ("pills", "full", "the items as pills"), "compare": ("compare", "full", "stacked rows, winner outlined"), "payoff": ("stat", "full", "the outcome as one line on a card"),
                       "cta": ("cta", "full", "one clear action, held to the last frame"), "point": ("cap", "full", "bold caption over the backdrop")},
    "product film":   {"hook": ("phone", "full", "open on the product in the hand: 3D phone with cards flying in"), "number": ("orb", "full", "chip with the number beside the orb"),
                       "definition": ("kinetic", "full", "two-tone big type"), "problem": ("kinetic", "full", "the pain as a question, light background"),
                       "example": ("screen", "full", "the real screen, tilted and zooming to the detail"), "steps": ("glass", "full", "glass checklist"), "list": ("glass", "full", "glass checklist"),
                       "compare": ("kinetic", "full", "before line, then the after line on a new background"), "payoff": ("kinetic", "full", "glow line on the dark background"),
                       "cta": ("kinetic", "full", "three words or fewer, back on white"), "point": ("kinetic", "full", "two to four words")},
    "creator explainer": {"hook": ("headline", "full", "serif headline above the head; the face carries the hook"), "number": ("tags", "full", "the figure in an oval beside the head"),
                       "definition": ("mindmap", "panel", "start the map: the idea in the middle"), "problem": ("stickies", "full", "the messy version as sticky notes"),
                       "example": ("headline", "full", "the example typed on above the head"), "steps": ("mindmap", "panel", "one node per step, camera follows"), "list": ("tags", "full", "one oval per item as it is said"),
                       "compare": ("mindmap", "panel", "two branches side by side"), "payoff": ("mindmap", "panel", "zoom out on the whole map, glow each part"),
                       "cta": ("cta", "full", "one clear action"), "point": ("presenter", "full", "stay on the face; captions only")},
    "split explainer": {"hook": ("orbit", "split", "examples circling the idea, the name lands in the middle; title on top"), "number": ("bignum", "split", "the number on the panel"),
                       "definition": ("skeleton", "split", "a script page with the line highlighted and a callout naming it"), "problem": ("line", "split", "what goes wrong, as a curve (only with real data) or a phone example"),
                       "example": ("skeleton", "split", "the real sentences typed on, each marked, then bracketed and named"), "steps": ("picklist", "split", "numbered pills"), "list": ("picklist", "split", "numbered pills, the one that matters in focus"),
                       "compare": ("compare", "split", "stacked rows on the panel"), "payoff": ("presenter", "full", "back to the face for the promise"),
                       "cta": ("cta", "full", "the face, one action, a quoted keyword if there is one"), "point": ("presenter", "full", "full-screen presenter with one-word captions")},
    "story b-roll":   {"hook": ("broll", "full", "the most striking clip first"), "point": ("broll", "full", "one clip per sentence"), "cta": ("cta", "full", "one clear action"),
                       "example": ("screen", "full", "the screen recording"), "steps": ("screen", "full", "the screen recording, zoomed to the click"), "number": ("bignum", "full", "the number over the clip")},
    "crimson explainer": {"hook": ("kinetic", "full", "the claim in big words on the crimson background, one word blurring in at a time"), "number": ("bignum", "full", "the figure huge behind the head, a small lead word above it"),
                       "definition": ("callout", "full", "name the thing beside the head in a red pill"), "problem": ("kinetic", "full", "the key sentence with the painful phrase in red"),
                       "example": ("screen", "full", "the real example on a glass panel over crimson"), "steps": ("diamonds", "full", "numbers in red diamonds, names first, meanings as each is explained"), "list": ("pillar", "full", "a glass pillar card per part of the framework"),
                       "compare": ("lanes", "full", "one numbered lane per option, the camera moving on each cue"), "payoff": ("rules", "full", "the checklist as red numbered pills"),
                       "cta": ("cta", "full", "one clear action"), "point": ("presenter", "full", "back to the face between sections")},
}
LENGTHS = {"data explainer": (20, 45), "product film": (12, 20), "creator explainer": (30, 60), "split explainer": (45, 90), "story b-roll": (30, 90), "crimson explainer": (45, 90)}


def _keywords(sent, n=3):
    m = re.search(r"(?:called|known as)\s+(?:the\s+)?[\"“']?([\w' -]{3,30}?)[\"”']?(?:[.,!?]|$| method| hack| rule)", sent, re.I)
    if m:
        return m.group(1).strip()
    q = re.search(r"[\"“]([^\"”]{3,40})[\"”]", sent)
    if q:
        return q.group(1)
    words = [w for w in re.findall(r"[A-Za-z0-9$%'-]+", sent) if w.lower() not in STOP and len(w) > 2]
    words.sort(key=lambda w: (-(w[0].isupper() and sent.find(w) > 0), -len(w)))
    keep = set(words[:n])
    return " ".join(w for w in re.findall(r"[A-Za-z0-9$%'-]+", sent) if w in keep)[:40]


def cmd_plan(a):
    """Read the script (or transcript), cut it into beats, name each beat's job and pick a design for it. Writes plan.json."""
    p = proj(a.project)
    cfg = (load_config(p) or {}).get("answers", {})
    words = []
    if (p / "words.js").exists():
        m = re.search(r"window\.WORDS\s*=\s*(\[.*\]);", (p / "words.js").read_text(encoding="utf-8"), re.S)
        words = json.loads(m.group(1)) if m else []
    if a.text:
        text = pathlib.Path(a.text).read_text(encoding="utf-8")
    elif (p / "script.txt").exists():
        text = (p / "script.txt").read_text(encoding="utf-8")
    elif words:
        text = " ".join(w["w"] for w in words)
    else:
        sys.exit("give the words: --text script.txt, or projects/%s/script.txt, or run `align` first" % p.name)
    sents = [x.strip() for x in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", text)) if x.strip()]
    presenter = any(p.glob("presenter.*")) or str(cfg.get("presenter") or "").startswith("yes")
    has_voice = (p / "voice.mp3").exists() or presenter or not str(cfg.get("voice_source") or "").startswith("no voice")
    # timing: real word times when there are any, else an estimate at 160 words a minute
    counts = [len(x.split()) for x in sents]
    spans, k, t = [], 0, 0.0
    timed = bool(words) and abs(len(words) - sum(counts)) <= max(3, 0.08 * sum(counts))
    for c in counts:
        if timed:
            ws = words[k:k + c] or words[-1:]
            spans.append((ws[0]["s"], ws[-1]["e"]))
            k += c
        else:
            spans.append((round(t, 2), round(t + c / 3.0, 2)))
            t += c / 3.0 + 0.2
    total = spans[-1][1] + 0.5
    fmt = a.format if a.format != "auto" else next((f for f in DESIGNS if str(cfg.get("format") or "").startswith(f)), None)
    why_fmt = "asked for" if fmt else ""
    if not fmt:
        if not has_voice:
            fmt, why_fmt = "product film", "no voice: type and motion carry it"
        elif presenter:
            fmt, why_fmt = ("split explainer", "a presenter and %.0f s of teaching: the panel keeps a diagram on screen while the face stays visible" % total) if total > 40 else ("creator explainer", "a presenter and a short script: graphics above the head")
        else:
            fmt, why_fmt = "data explainer", "voice without a presenter: captions, numbers and sources"
    table = DESIGNS[fmt]
    beats = []
    for i, (sent, (s0, s1)) in enumerate(zip(sents, spans)):
        low = sent.lower()
        role = "hook" if s0 < 2.0 and i < 2 else next((r for r, pat in ROLES if re.search(pat, low)), None)
        if role in (None, "list", "problem", "payoff") and re.search(NUM, low) and not re.search(r"\b(one|two) (of|thing)\b", low):
            role = "number" if role is None else role
        role = role or "point"
        if role == "cta" and s0 < total * 0.6:
            role = "point"                              # a call to action only counts near the end
        typ, layout, why = table.get(role) or table.get("point") or ("cap", "full", "bold caption")
        num = re.search(NUM, sent, re.I)
        beats.append({"n": i, "t": round(s0, 2), "end": round(s1, 2), "role": role, "say": sent, "scene": typ, "layout": layout, "why": why,
                      "key": (num.group(0).strip() if role == "number" and num else _keywords(sent)), "words": len(sent.split())})
    # merge neighbours that would repeat the same full-screen presenter beat; note where a long beat needs a second change
    notes = []
    lo, hi = LENGTHS[fmt]
    if not lo - 3 <= total <= hi + 5:
        notes.append("length %.0f s is outside the usual %d-%d s for a %s: %s" % (total, lo, hi, fmt, "cut lines" if total > hi else "fine if the idea is complete"))
    if beats[0]["end"] - beats[0]["t"] > 4:
        notes.append("the hook takes %.1f s to say: put its key words on screen in the first frame" % (beats[0]["end"] - beats[0]["t"]))
    if not any(b["role"] == "cta" for b in beats):
        notes.append("no call to action found near the end: add one line and a `cta` scene")
    for b in beats:
        if b["end"] - b["t"] > 5:
            b["note"] = "%.1f s on one beat: build it in two or three steps (rows, marks, a second scene) so something changes every 2-4 s" % (b["end"] - b["t"])
        if b["words"] > 28:
            b["note"] = (b.get("note", "") + " Long sentence: consider splitting it, or follow it with a simpler repeat line.").strip()
    if any(b["scene"] in ("chart", "line", "bignum", "stat", "ring") for b in beats):
        notes.append("number scenes need real figures with a source; if the script gives none, use a different scene")
    runs = [b for a_, b in zip(beats, beats[1:]) if a_["scene"] == b["scene"] and b["scene"] not in ("presenter", "kinetic", "broll", "cap", "mindmap")]
    for b in runs:
        b["note"] = (b.get("note", "") + " Same scene type as the beat before: make it one scene that keeps building, or vary it.").strip()
    script_keys = {"data explainer": {}, "product film": {"audio": None, "backdrops": "style: white -> sky -> night -> white, changing with the story"},
                   "creator explainer": {"captions": {"style": "pill"}}, "split explainer": {"captions": {"style": "word", "pos": "split"}},
                   "story b-roll": {"captions": {"style": "outline"}},
                   "crimson explainer": {"backdrops": "style: crimson behind every full-screen graphic; the presenter footage between sections", "theme": {"accent": "#E3202E"}}}[fmt]
    plan = {"project": p.name, "format": fmt, "format_reason": why_fmt, "duration": round(total, 1), "timing": "word times from words.js" if timed else "estimated at about 170 words a minute (run `align` for real times)",
            "script_keys": script_keys, "notes": notes, "beats": beats}
    (p / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    if a.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return
    print("format: %s  (%s)\nlength: %.0f s, %d beats, timing %s" % (fmt, why_fmt, total, len(beats), plan["timing"]))
    if script_keys:
        print("script.js: " + json.dumps(script_keys, ensure_ascii=False))
    print()
    for b in beats:
        print("%5.1f-%5.1f  %-10s %-9s %-5s  key: %s" % (b["t"], b["end"], b["role"], b["scene"], b["layout"], b["key"]))
        print("             “%s”" % (b["say"] if len(b["say"]) < 110 else b["say"][:107] + "..."))
        print("             why: %s%s" % (b["why"], ("\n             NOTE: " + b["note"]) if b.get("note") else ""))
    for n_ in notes:
        print("NOTE: " + n_)
    print("\nwrote %s. This is a first pass by rule: read every beat, change what does not fit, then write script.js." % (p / "plan.json"))


# ---------- direct: one command from footage (or a script) to a first draft of the whole edit ----------
# Places the draft can put on a map without a network: name -> (lat, lon). Extend freely.
GAZETTEER = {
    "india": (22.0, 79.0), "delhi": (28.6, 77.2), "new delhi": (28.6, 77.2), "mumbai": (19.08, 72.88), "bangalore": (12.97, 77.59), "bengaluru": (12.97, 77.59),
    "kolkata": (22.57, 88.36), "chennai": (13.08, 80.27), "hyderabad": (17.39, 78.49), "pune": (18.52, 73.86), "nepal": (28.4, 84.1), "kathmandu": (27.7, 85.32),
    "pokhara": (28.21, 83.99), "dubai": (25.2, 55.27), "abu dhabi": (24.45, 54.38), "uae": (24.0, 54.0), "qatar": (25.3, 51.2), "doha": (25.29, 51.53),
    "saudi arabia": (24.0, 45.0), "riyadh": (24.71, 46.68), "pakistan": (30.0, 70.0), "bangladesh": (24.0, 90.0), "dhaka": (23.81, 90.41), "sri lanka": (7.9, 80.8),
    "london": (51.51, -0.13), "uk": (54.0, -2.0), "england": (52.5, -1.5), "ireland": (53.0, -8.0), "dublin": (53.35, -6.26), "paris": (48.86, 2.35), "france": (46.0, 2.0),
    "berlin": (52.52, 13.4), "germany": (51.0, 10.0), "amsterdam": (52.37, 4.9), "netherlands": (52.2, 5.3), "spain": (40.0, -4.0), "madrid": (40.42, -3.7),
    "italy": (42.8, 12.8), "rome": (41.9, 12.5), "sweden": (62.0, 15.0), "europe": (50.0, 10.0), "russia": (60.0, 90.0), "turkey": (39.0, 35.0), "istanbul": (41.01, 28.98),
    "usa": (39.0, -98.0), "united states": (39.0, -98.0), "america": (39.0, -98.0), "new york": (40.71, -74.0), "san francisco": (37.77, -122.42),
    "los angeles": (34.05, -118.24), "chicago": (41.88, -87.63), "canada": (56.0, -106.0), "toronto": (43.65, -79.38), "vancouver": (49.28, -123.12), "mexico": (23.0, -102.0),
    "brazil": (-10.0, -55.0), "australia": (-25.0, 134.0), "sydney": (-33.87, 151.21), "melbourne": (-37.81, 144.96), "adelaide": (-34.93, 138.6),
    "brisbane": (-27.47, 153.03), "perth": (-31.95, 115.86), "new zealand": (-41.0, 174.0), "auckland": (-36.85, 174.76), "singapore": (1.35, 103.82),
    "malaysia": (4.0, 102.0), "thailand": (15.0, 101.0), "bangkok": (13.76, 100.5), "vietnam": (16.0, 108.0), "indonesia": (-2.0, 118.0), "philippines": (13.0, 122.0),
    "japan": (36.0, 138.0), "tokyo": (35.68, 139.69), "china": (35.0, 103.0), "beijing": (39.9, 116.4), "shanghai": (31.23, 121.47), "hong kong": (22.32, 114.17),
    "korea": (36.0, 128.0), "seoul": (37.57, 126.98), "egypt": (26.0, 30.0), "nigeria": (9.0, 8.0), "kenya": (0.0, 38.0), "south africa": (-30.0, 25.0),
    "africa": (2.0, 20.0), "asia": (34.0, 100.0)}
ORDINAL = r"^(?:and\s+)?(first(?:ly)?|second(?:ly)?|third(?:ly)?|fourth|fifth|next|finally|lastly|number (?:one|two|three|four|five)|one|two|three|four|five)\b[,.:]?\s*"
FULLSCREEN = {"pillar", "diamonds", "lanes", "rules", "list", "glass", "compare", "chart", "dosdonts", "timeline", "quote", "mindmap", "map", "picklist", "orbit",
              "skeleton", "line", "ring", "pills", "stat"}


def _clean(w):
    return re.sub(r"[^\w%$'-]", "", w.lower())


WORDNUM = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
COUNT_NOUN = r"\b(principles|pillars|rules|steps|ways|lanes|stages|tips|things|reasons|tools|ideas|mistakes|levels|parts|questions|habits|lessons)\b"


def _short(text, n=3):
    ws, seen = [], set()
    for w in re.findall(r"[\w%$'&+/-]+", text):
        if w.lower() not in seen:
            seen.add(w.lower())
            ws.append(w)
    while ws and ws[0].lower() in STOP:
        ws.pop(0)
    while ws and ws[-1].lower() in STOP:
        ws.pop()
    return " ".join(ws[:n])


def _items(sent):
    """'four principles: timing, weight, rhythm, and intention' -> ['Timing', 'Weight', 'Rhythm', 'Intention']"""
    s = sent.split(":", 1)[1] if ":" in sent else sent
    parts = [x.strip() for x in re.split(r",\s*(?:and\s+|or\s+)?|\s+(?:and|or)\s+", s.rstrip(".!?")) if x.strip()]
    if len(parts) < 3 and not (":" in sent and len(parts) >= 2):
        return []
    if s.count(",") < 2 and ":" not in sent:          # a real list: "a, b, and c" (or "...: a and b")
        return []
    if any(len(x.split()) > 3 for x in parts[1:-1]):   # the middle of a list is short items, not clauses
        return []
    run = parts
    if len(run[0].split()) > 3:
        run[0] = " ".join(run[0].split()[-2:])
    if len(run[-1].split()) > 3:
        run[-1] = " ".join(run[-1].split()[:2])
    out = [_short(x, 3) for x in run]
    out = [x[:1].upper() + x[1:] for x in out if x and len(x.split()) <= 3]
    return out[:6] if len(out) >= 2 else []


def _places(sent):
    low = " " + re.sub(r"[^\w ]", " ", sent.lower()) + " "
    found = []
    for name in sorted(GAZETTEER, key=len, reverse=True):
        if " %s " % name in low and not any(name in f for f in found):
            found.append(name)
    return sorted(found, key=lambda n: low.find(" %s " % n))


def _kin(key):
    ws = str(key).split()
    if not ws:
        return key
    return " ".join(ws[:-1] + ["*%s*" % ws[-1]]) if len(ws) > 1 else "*%s*" % ws[0]


def _draft(p, plan, words, presenter, frame, style, has_voice):
    """Turn plan.json beats into script.js: scenes with real content, timed to the words, and camera moves on the footage."""
    W, H = (1920, 1080) if frame == "landscape" else (1080, 1920)
    fmt = plan["format"]
    beats = plan["beats"]
    total = plan["duration"]
    idx = [(i, _clean(w["w"])) for i, w in enumerate(words)]

    def when(term, t0, t1, say=""):
        """time the first word of `term` is said inside [t0, t1] (the beat); without word timings, estimated from its place in the sentence"""
        first = _clean(str(term).split()[0]) if str(term).split() else ""
        for i, w in idx:
            if words[i]["s"] >= t0 - 0.15 and words[i]["s"] <= t1 + 0.15 and first and (w == first or (len(first) > 3 and w.startswith(first[:5]))):
                return words[i]["s"]
        if say and first:
            ws = [_clean(x) for x in say.split()]
            k = next((j for j, x in enumerate(ws) if x == first or (len(first) > 3 and x.startswith(first[:5]))), None)
            if k is not None:
                return round(t0 + (t1 - t0) * k / max(1, len(ws)), 2)
        return t0

    scenes, moves, used = [], [], set()
    part = [0]

    def add(sc, why):
        sc["_why"] = why
        scenes.append(sc)

    for bi, b in enumerate(beats):
        if bi in used:
            continue
        say, t0, t1, role, typ = b["say"], b["t"], b["end"], b["role"], b["scene"]
        items = _items(say)
        places = _places(say)
        # parallel lines: "For a basic ..., For intermediate ..., For advanced ..." (or "If you ...") -> one lanes scene, a lane per line
        lead = lambda x: re.match(r"^(?:and\s+|now\s*,?\s+)?(for|if you(?:'re| are)?|with)\s+(?:an?\s+|the\s+)?([\w-]+)", x, re.I)   # noqa: E731
        if lead(say) and not items:
            run = [bi]
            while run[-1] + 1 < len(beats) and lead(beats[run[-1] + 1]["say"]) and lead(beats[run[-1] + 1]["say"]).group(1).lower() == lead(say).group(1).lower():
                run.append(run[-1] + 1)
            if len(run) >= 3:
                lanes = []
                for j in run:
                    m_ = lead(beats[j]["say"])
                    rest = beats[j]["say"][m_.end():]
                    lanes.append({"title": m_.group(2).title(), "subs": [_short(rest, 4)] if _short(rest, 4) else []})
                    used.add(j)
                add({"t": t0, "end": round(beats[run[-1]]["end"] + 0.3, 2), "type": "lanes" if fmt in ("crimson explainer",) else "list",
                     **({"label": _short(" ".join(beats[bi - 1]["say"].split()[-3:]), 3).title() if bi else "", "items": lanes, "at": [round(beats[j]["t"] - t0, 2) for j in run]}
                        if fmt in ("crimson explainer",) else {"items": [x["title"] + (": " + x["subs"][0] if x["subs"] else "") for x in lanes],
                                                              "at": [round(beats[j]["t"] - t0, 2) for j in run]})},
                    "%d parallel lines (%s ...)" % (len(run), lead(say).group(1)))
                continue
        # a list said once, then explained one by one: one scene that keeps building (names on the list, meanings on the explanations)
        if items and len(items) >= 2:
            cn = re.search(COUNT_NOUN, say + " " + (beats[bi - 1]["say"] if bi else ""), re.I)
            title = ("%d %s" % (len(items), cn.group(1).lower())).title() if cn else _short(b["key"], 3).title() or "Overview"
            name_at = [round(when(x, t0, t1, say) - t0, 2) for x in items]
            subs, sub_at, last_end = [""] * len(items), [None] * len(items), t1
            for bj in range(bi + 1, min(len(beats), bi + 1 + 3 * len(items))):
                nxt = beats[bj]
                head = " ".join(re.sub(ORDINAL, "", nxt["say"], flags=re.I).split()[:4]).lower()
                for k, x in enumerate(items):
                    if sub_at[k] is None and _clean(x.split()[0]) in [_clean(h) for h in head.split()]:
                        body = re.sub(r"^.*?\b%s\b[,.:]?\s*" % re.escape(x.split()[0]), "", nxt["say"], count=1, flags=re.I)
                        sub_at[k] = round(nxt["t"] - t0, 2)
                        used.add(bj)
                        last_end = nxt["end"]
                        if len(body.split()) < 3 and bj + 1 < len(beats):      # "First, timing." -> the meaning is the next sentence
                            body = beats[bj + 1]["say"]
                            used.add(bj + 1)
                            last_end = beats[bj + 1]["end"]
                        subs[k] = _short(body, 8)
                        break
            explained = sum(1 for x in sub_at if x is not None)
            kind = {"crimson explainer": "diamonds" if len(items) <= 4 else "lanes", "product film": "glass", "creator explainer": "tags",
                    "split explainer": "picklist", "story b-roll": "list"}.get(fmt, "list")
            if kind == "diamonds" and explained >= 2 and len(items) <= 4:
                part[0] += 1
                sc = {"t": t0, "end": round(last_end + 0.3, 2), "type": "pillar" if part[0] % 2 else "diamonds"}
                if sc["type"] == "pillar":
                    sc.update(kicker="Part %d" % part[0], title=title,
                              items=[{"name": x, "sub": subs[k]} for k, x in enumerate(items)], at=name_at,
                              subAts=[s if s is not None else name_at[k] + 0.4 for k, s in enumerate(sub_at)])
                else:
                    sc.update(items=[{"name": x, "sub": subs[k]} for k, x in enumerate(items)], at=name_at,
                              subAts=[s if s is not None else name_at[k] + 0.4 for k, s in enumerate(sub_at)])
            elif kind == "lanes":
                sc = {"t": t0, "end": round(last_end + 0.3, 2), "type": "lanes", "label": _short(b["key"], 4),
                      "items": [{"title": x, "subs": [subs[k]] if subs[k] else []} for k, x in enumerate(items)],
                      "at": [s if s is not None else name_at[k] for k, s in enumerate(sub_at)]}
            elif kind == "tags":
                sc = {"t": t0, "end": round(last_end + 0.3, 2), "type": "tags", "items": [{"text": x} for x in items[:3]]}
            elif kind == "picklist":
                sc = {"t": t0, "end": round(last_end + 0.3, 2), "type": "picklist", "items": items, "split": True}
            else:
                sc = {"t": t0, "end": round(last_end + 0.3, 2), "type": kind, "items": items[:5], "at": name_at[:5]}
                if kind == "list":
                    sc["title"] = title
            add(sc, "a list of %d, %s" % (len(items), "each explained after" if explained else "said once"))
            continue
        if places and fmt != "product film":
            pts = [GAZETTEER[x] for x in places[:5]]
            add({"t": t0, "end": round(t1 + 0.3, 2), "type": "map", "pins": [{"label": x.title(), "lat": la, "lon": lo, "at": round(when(x, t0, t1, say) - t0, 2)}
                                                                              for x, (la, lo) in zip(places, pts)], "route": len(pts) > 1},
                "places named: " + ", ".join(places))
            continue
        num = re.search(NUM, say, re.I)
        tk = when(b["key"], t0, t1)
        if role == "number" and num:
            v = num.group(0).strip()
            w0 = v.split()[0].lower()
            if w0 in WORDNUM:                                   # "four principles" -> 4 principles
                v = "%d %s" % (WORDNUM[w0], " ".join(v.split()[1:]))
            m_ = re.match(r"\$?([\d,.]+)\s*(.*)", v)
            if presenter:
                add({"t": tk, "end": round(t1 + 0.3, 2), "type": "bignum", "value": (m_.group(1).replace(",", "") if m_ else v),
                     "unit": (m_.group(2) if m_ else "") or _short(say[num.end():], 3)}, "a number: huge behind the head")
            else:
                add({"t": tk, "type": "bignum", "value": (m_.group(1).replace(",", "") if m_ else v), "unit": (m_.group(2) if m_ else "") or _short(say[num.end():], 3)},
                    "a number carries this beat")
            if presenter:
                moves.append({"mode": "punch", "t": round(tk, 2), "amount": 0.1, "_why": "punch on the number"})
            continue
        if role == "cta":
            add({"t": t0, "type": "cta", "text": _short(say, 4)}, "call to action")
            continue
        if role == "compare" and re.search(r"\b(don'?t|never|stop|avoid)\b", say, re.I):
            add({"t": t0, "end": round(t1 + 0.3, 2), "type": "dosdonts", "title": _short(b["key"], 3),
                 "donts": [_short(x, 4) for x in re.split(r"\b(?:instead|rather than|but)\b", say)[:1]],
                 "dos": [_short(x, 4) for x in re.split(r"\b(?:instead|rather than|but)\b", say)[1:2]] or ["(fill in)"]}, "do / don't")
            continue
        if bi == 0 or role in ("hook", "definition", "problem", "payoff"):
            if presenter and role == "definition" and fmt in ("crimson explainer", "creator explainer"):
                ax, ay = (int(W * 0.27), int(H * 0.62)) if frame == "portrait" else (int(W * 0.28), int(H * 0.7))
                add({"t": tk, "end": round(t1 + 0.2, 2), "type": "callout", "text": _short(b["key"], 3).title(), "at": [ax, ay], "to": [int(W * 0.46), int(H * (0.52 if frame == "portrait" else 0.5))]},
                    "names the idea beside the head")
            elif fmt == "creator explainer" and presenter:
                add({"t": t0, "end": round(t1 + 0.3, 2), "type": "headline", "title": _kin(_short(b["key"], 3))}, "headline above the head")
            else:
                add({"t": tk, "end": round(t1 + 0.3, 2), "type": "kinetic", "text": _kin(_short(b["key"], 4)), **({"pos": "top"} if presenter else {})},
                    "%s in big words" % role)
            continue
        if not presenter:      # nobody on screen: every beat needs a picture
            add({"t": t0, "type": "kinetic", "text": _kin(_short(b["key"], 4))}, "a beat without a presenter: its key words")
    # ---- camera moves on the footage: a push-in on the hook, punches on numbers, the person steps aside for big graphics,
    #      a pull-out on the payoff / call to action, and slow pushes or pans on long talking stretches so the frame keeps moving
    if presenter:
        busy = []
        for sc in scenes:
            if sc["type"] in FULLSCREEN:
                e = sc.get("end") or sc["t"] + 3
                moves.append({"mode": "anchor", "t": round(sc["t"], 2), "end": round(e, 2), "scale": 0.4, "side": "right", "_why": "the person steps aside for the %s" % sc["type"]})
                busy.append((sc["t"], e))
        if beats:
            h = beats[0]
            if not any(a_ < h["end"] and b_ > h["t"] for a_, b_ in busy):
                moves.append({"mode": "zoom", "t": h["t"], "end": h["end"], "from": 1.0, "to": 1.12, "focus": [0.5, 0.35], "_why": "slow push-in on the hook"})
                busy.append((h["t"], h["end"]))
        for b in beats:
            if b["role"] in ("payoff", "cta") and not any(a_ < b["end"] and b_ > b["t"] for a_, b_ in busy):
                moves.append({"mode": "zoom", "t": b["t"], "end": b["end"], "from": 1.15, "to": 1.0, "focus": [0.5, 0.35], "hold": True, "_why": "pull out for the %s" % b["role"]})
                busy.append((b["t"], b["end"]))
        flip = 0
        for b in beats:
            if b["end"] - b["t"] >= 2.4 and not any(a_ < b["end"] and b_ > b["t"] for a_, b_ in busy):
                flip += 1
                mv = ({"mode": "zoom", "t": b["t"], "end": b["end"], "from": 1.0, "to": 1.1, "focus": [0.5, 0.35]} if flip % 2 else
                      {"mode": "pan", "t": b["t"], "end": b["end"], "zoom": 1.15, "from": [0.42, 0.38], "to": [0.58, 0.38]})
                mv["_why"] = "long talking beat: keep the frame moving"
                moves.append(mv)
                busy.append((b["t"], b["end"]))
        moves = [m for m in moves if not (m["mode"] == "punch" and any(a_ <= m["t"] <= b_ for a_, b_ in busy))]
        moves.sort(key=lambda m: m["t"])
    scenes.sort(key=lambda s: s["t"])
    if scenes and scenes[0]["t"] < 2.0:
        scenes[0]["t"] = 0                                     # the hook is on screen from the first frame
    keys = {k: v for k, v in plan.get("script_keys", {}).items() if not isinstance(v, str)}
    script = {"frame": frame, "brand": "", "presenter": presenter or None}
    if (p / "brand.js").exists():
        script.pop("brand")
    if not has_voice:
        script.update(audio=None, duration=round(total, 1))
    script.update(keys)
    if fmt == "crimson explainer" or style == "crimson":
        script["theme"] = {"accent": "#E3202E"}
        script["backdrops"] = [{"style": "crimson", "t": 0, "end": round(total, 1), "fadeIn": 0, "fadeOut": 0}]
    elif fmt == "product film":
        script["backdrops"] = [{"style": "night", "t": 0, "end": round(total, 1), "fadeIn": 0, "fadeOut": 0}]
    if presenter and words and "captions" not in script:
        script["captions"] = {"style": "pill"}
    if not presenter and "captions" in script and not words:
        script.pop("captions")
    head = ["// FIRST DRAFT written by `python tools/shorts.py direct` from plan.json (format: %s, frame: %s)." % (fmt, frame),
            "// Every scene and move says why it is there. Read the contact sheet (qa/sheet.jpg), then fix wording, swap scenes,",
            "// add photos / screens / b-roll where a note asks for them, and render. Field reference: python tools/shorts.py guide",
            "window.SCRIPT = {"]
    body = []
    for k, v in script.items():
        if v is None and k == "presenter":
            continue
        body.append("  %s: %s," % (k, json.dumps(v, ensure_ascii=False)))
    if moves:
        body.append("  moves: [")
        for m in [dict(x) for x in moves]:
            why = m.pop("_why", "")
            body.append("    %s,   // %s" % (json.dumps(m, ensure_ascii=False), why))
        body.append("  ],")
    body.append("  scenes: [")
    for sc in [dict(x) for x in scenes]:
        why = sc.pop("_why", "")
        sc = {"t": round(sc.pop("t"), 2), **sc}
        body.append("    %s,   // %s" % (json.dumps(sc, ensure_ascii=False), why))
    body.append("  ],")
    (p / "script.js").write_text("\n".join(head + body + ["};", ""]), encoding="utf-8")
    return scenes, moves


def cmd_direct(a):
    """footage or script in -> project, brand, audio, transcript, plan, a complete first-draft script.js with camera moves, cut-out, lint, sheet."""
    name = a.project
    p = ROOT / "projects" / name
    src = pathlib.Path(a.video).resolve() if a.video else None
    if not src and not a.script:
        sys.exit("give the footage (--video clip.mp4) or the words (--script script.txt [--voice voice.mp3])")
    if src and not src.exists():
        sys.exit("no such file: %s" % src)
    step = lambda s: print("\n== %s" % s, flush=True)   # noqa: E731
    # 1. project
    if not p.exists():
        step("new project %s" % p)
        shutil.copytree(TEMPLATE, p, ignore=shutil.ignore_patterns("README.md", "DIRECTOR.md", "scenes.json", "segments.js", "words.js"))
        (p / "output").mkdir(exist_ok=True)
        save_config(p, new_config())
    else:
        step("using project %s" % p)
    # 2. footage -> presenter.mp4 (H.264 so the browser preview can play it) and voice.mp3
    frame = a.frame
    presenter = None
    if src:
        info = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_name,width,height", "-of", "csv=p=0", str(src)],
                              capture_output=True, text=True).stdout.strip().split(",")
        codec, vw, vh = info[0], int(info[1]), int(info[2])
        if frame == "auto":
            frame = "landscape" if vw > vh else "portrait"
        dst = p / "presenter.mp4"
        cut = (["-ss", str(a.start)] if a.start else []) + (["-to", str(a.end)] if a.end else [])
        step("footage %dx%d %s -> presenter.mp4 (%s frame)" % (vw, vh, codec, frame))
        if codec == "h264" and not cut and src.suffix.lower() == ".mp4":
            shutil.copy(src, dst)
        else:
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *cut, "-i", str(src), "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "192k", str(dst)], check=True)
        presenter = "presenter.mp4"
        if has_audio(dst):
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(dst), "-vn", "-ac", "1", "-ar", "44100", "-q:a", "2", str(p / "voice.mp3")], check=True)
            print("audio -> voice.mp3")
    elif a.voice:
        shutil.copy(a.voice, p / "voice.mp3")
    if frame == "auto":
        frame = "portrait"
    if a.script:
        shutil.copy(a.script, p / "script.txt")
    has_voice = (p / "voice.mp3").exists()
    # 3. brand: logo, colours and fonts from the brand's site, or given by hand; a reference video's look is studied from a frame grid
    if a.brand or a.logo or a.accent:
        step("brand kit")
        cmd_brand(argparse.Namespace(project=name, url=a.brand, name=a.brand_name, handle=None, accent=a.accent, secondary=None, dark=None, bg=None, logo=a.logo, clear=False))
    if a.reference:
        step("reference video -> frame grid to study its style")
        cmd_frames(argparse.Namespace(project=name, video=a.reference, every=a.every))
    # 4. words: transcript with word times
    if has_voice and not (p / "words.js").exists():
        step("transcribe (word timings)")
        try:
            cmd_align(argparse.Namespace(project=name, source=None, text=a.script, engine="auto", model=a.model, language=a.language))
        except SystemExit as e:
            if not a.script:
                raise
            print("could not time the words (%s); timing is estimated from the script" % str(e).splitlines()[0])
    words = []
    if (p / "words.js").exists():
        m = re.search(r"window\.WORDS\s*=\s*(\[.*\]);", (p / "words.js").read_text(encoding="utf-8"), re.S)
        words = json.loads(m.group(1)) if m else []
        if not a.script:
            (p / "transcript.txt").write_text(" ".join(w["w"] for w in words), encoding="utf-8")
    # 5. config answers the setup would otherwise ask
    fmt = a.format
    sets = ["presenter=%s" % ("yes, footage provided" if presenter else "no"),
            "voice_source=%s" % ("the presenter's own audio" if presenter and has_voice else "i provide an audio file" if has_voice else "no voice (captions and music only)")]
    if fmt != "auto":
        sets.append("format=%s" % fmt)
    cfg = load_config(p) or new_config()
    for item in sets:
        k_, _, v_ = item.partition("=")
        cfg["answers"][k_] = v_
    save_config(p, cfg)
    # 6. plan
    step("plan the beats")
    cmd_plan(argparse.Namespace(project=name, text=a.script, format=fmt, json=False))
    plan = json.loads((p / "plan.json").read_text(encoding="utf-8"))
    if words:
        plan["duration"] = round(max(plan["duration"], words[-1]["e"] + 0.6), 1)
    # 7. the draft
    step("write the first draft: script.js")
    scenes, moves = _draft(p, plan, words, presenter, frame, a.style, has_voice)
    for sc in scenes:
        print("  %6.2fs  %-9s %s" % (sc["t"], sc["type"], json.dumps({k: v for k, v in sc.items() if k not in ("t", "type", "end")}, ensure_ascii=False)[:100]))
    for m in moves:
        print("  %6.2fs  move:%-7s %s" % (m["t"], m["mode"], "-> %.2fs" % m["end"] if "end" in m else ""))
    # 8. cut-out, so graphics can sit behind the person
    if presenter and not a.no_cutout:
        model = ROOT / "tools" / "models" / "rvm_mobilenetv3_fp32.onnx"
        if model.exists():
            step("cut the person out (this takes a while on a CPU)")
            subprocess.run([sys.executable, str(ROOT / "tools" / "matte.py"), str(p / "presenter.mp4")], check=False)
        else:
            print("\nNOTE: no cut-out model, so moves happen on the whole picture (zoom, pan, the footage shrinks into a card).\n"
                  "      For graphics BEHIND the person: python tools/matte.py --download   then   python tools/matte.py %s" % (p / "presenter.mp4"))
    # 9. check
    step("lint")
    try:
        cmd_lint(argparse.Namespace(project=name, json=False, strict=False))
    except SystemExit:
        pass
    step("contact sheet")
    asyncio.run(sheet(p, guides=True))
    print("\nDraft ready. Look at %s, edit %s, then:  python tools/shorts.py render %s" % (p / "qa" / "sheet.jpg", p / "script.js", name))


# ---------- guide / doctor: for any person or AI model working from a shell ----------
def cmd_guide(a):
    cat = json.loads((TEMPLATE / "scenes.json").read_text(encoding="utf-8"))
    if a.json:
        cat["config_questions"] = [{"key": k, "question": q, "choices": c, "default": d} for k, q, c, d in CONFIG_QUESTIONS]
        cat["commands"] = [ln.strip() for ln in __doc__.splitlines() if ln.strip().startswith("python tools/shorts.py")]
        print(json.dumps(cat, ensure_ascii=False, indent=2))
        return
    print((TEMPLATE / "DIRECTOR.md").read_text(encoding="utf-8"))
    print("\n## Scene types (templates/shorts/scenes.json)\n")
    for name, sp in cat["scenes"].items():
        fields = ", ".join(sp["required"] + ["[%s]" % o for o in sp["optional"]])
        print("- %-9s %s\n            { %s }%s%s" % (name, sp["use"], fields,
              ("\n            item: { %s }" % ", ".join(sp["item"])) if sp.get("item") else "", ("\n            " + sp["notes"]) if sp.get("notes") else ""))
    print("\n## Formats (pick with the person; mix scenes freely)\n")
    for k, v in cat.get("formats", {}).items():
        print("- %-18s %s" % (k, v))
    print("\n## script.js keys\n")
    for k, v in cat["script_keys"].items():
        print("- %-16s %s" % (k, v))
    print("\n## Timing\n")
    for k, v in cat["timing"].items():
        print("- %-8s %s" % (k, v))
    print("\n## Commands\n\n" + "\n".join(ln for ln in __doc__.splitlines() if ln.strip().startswith(("python tools/shorts.py", "#"))))


def cmd_doctor(a):
    rows = []

    def row(name, ok, detail, need="needed"):
        rows.append((name, ok, detail, need))

    for tool in ("ffmpeg", "ffprobe"):
        row(tool, bool(shutil.which(tool)), shutil.which(tool) or "not on PATH", "needed")
    try:
        import playwright  # noqa: F401
        from playwright.async_api import async_playwright

        async def probe():
            async with async_playwright() as pw:
                b = await launch(pw)
                v = b.version
                await b.close()
                return v
        row("browser", True, "Chromium " + asyncio.run(probe()))
    except SystemExit as e:
        row("browser", False, str(e).splitlines()[0])
    except ImportError:
        row("browser", False, "pip install playwright  then  python -m playwright install chromium")
    try:
        import PIL, numpy  # noqa: F401,E401
        row("Pillow + numpy", True, "contact sheets, free backdrops")
    except ImportError as e:
        row("Pillow + numpy", False, "pip install -r requirements.txt (%s)" % e.name)
    v = TEMPLATE / "vendor"
    row("offline assets", (v / "gsap.min.js").exists() and (v / "fonts.css").exists(), "GSAP and fonts in templates/shorts/vendor" if (v / "gsap.min.js").exists() else "missing: renders will need the network")
    h264 = bool(shutil.which("google-chrome") or shutil.which("microsoft-edge") or shutil.which("msedge"))
    row("H.264 browser", h264, "Chrome/Edge found: presenter footage plays in the page" if h264 else "only needed for presenter .mp4 WITHOUT a cut-out (or convert the clip to .webm)", "optional")
    models = sorted((ROOT / "tools" / "models").glob("rvm_*.onnx"))
    try:
        import onnxruntime, cv2  # noqa: F401,E401
        deps = True
    except ImportError:
        deps = False
    row("presenter cut-out", bool(models) and deps, (models[0].name if models else "no model in tools/models (see templates/shorts/README.md)") + ("" if deps else "; pip install onnxruntime opencv-python"), "optional")
    try:
        import faster_whisper  # noqa: F401
        row("word timings (local)", True, "faster-whisper", "optional")
    except ImportError:
        row("word timings (local)", False, "pip install faster-whisper, or pass timings with align --from", "optional")
    row("ElevenLabs key", bool(os.environ.get("ELEVENLABS_API_KEY")), "ELEVENLABS_API_KEY is set" if os.environ.get("ELEVENLABS_API_KEY") else "not set: bring your own voice.mp3", "optional")
    bad = False
    for name, ok, detail, need in rows:
        print("%-4s %-22s %s%s" % ("ok" if ok else ("MISS" if need == "needed" else "-"), name, detail, "" if ok or need == "needed" else "  (optional)"))
        bad = bad or (not ok and need == "needed")
    print("\nready to make shorts" if not bad else "\nfix the MISS lines first")
    if bad:
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new", help="create projects/<name>/ from the template"); n.add_argument("name"); n.add_argument("--voice"); n.add_argument("--presenter")
    n.add_argument("--noise", default="-35"); n.add_argument("--min-pause", type=float, default=0.35)
    s = sub.add_parser("segments"); s.add_argument("project")
    s.add_argument("--noise", default="-35", help="silence threshold in dB (default -35)")
    s.add_argument("--min-pause", type=float, default=0.35, help="shortest pause that splits lines, seconds")
    q = sub.add_parser("sheet", help="QA contact sheet"); q.add_argument("project")
    q.add_argument("--no-guides", action="store_true", help="leave the safe-zone bands off the sheet")
    li = sub.add_parser("lint", help="check the rules before rendering"); li.add_argument("project")
    li.add_argument("--json", action="store_true", help="machine-readable output"); li.add_argument("--strict", action="store_true", help="warnings also fail")
    al = sub.add_parser("align", help="word timings -> words.js"); al.add_argument("project")
    al.add_argument("--from", dest="source", help="timings you already have: JSON, .srt or .vtt")
    al.add_argument("--text", help="file with the exact spoken words (ElevenLabs forced alignment)")
    al.add_argument("--engine", choices=["auto", "whisper", "elevenlabs"], default="auto")
    al.add_argument("--model", default="small", help="faster-whisper model (default small)"); al.add_argument("--language", help="e.g. en, ne")
    vo = sub.add_parser("voice", help="optional: ElevenLabs voiceover + word timings"); vo.add_argument("project")
    vo.add_argument("--text", required=True); vo.add_argument("--voice-id", default="IKne3meq5aSn9XLyUdCD"); vo.add_argument("--model-id", default="eleven_multilingual_v2")
    vo.add_argument("--force", action="store_true")
    br = sub.add_parser("brand", help="brand kit: name, logo and colours from a website or by hand"); br.add_argument("project")
    br.add_argument("--url", help="the brand's public website (read only)"); br.add_argument("--name"); br.add_argument("--handle", help="e.g. @acme")
    br.add_argument("--accent", help="main brand colour, #hex"); br.add_argument("--secondary"); br.add_argument("--dark", help="colour of the dark cards, #hex"); br.add_argument("--bg")
    br.add_argument("--logo", help="logo file (transparent PNG or SVG is best)"); br.add_argument("--clear", action="store_true", help="remove the brand (back to the clean look)")
    pl = sub.add_parser("plan", help="first-pass storyboard from the script: beats, their job, a design for each"); pl.add_argument("project")
    pl.add_argument("--text", help="the script or transcript (default: script.txt in the project, else words.js)")
    pl.add_argument("--format", default="auto", choices=["auto"] + list(DESIGNS)); pl.add_argument("--json", action="store_true")
    di = sub.add_parser("direct", help="ONE COMMAND: footage or a script in -> brand, transcript, plan, a full first-draft edit with graphics and camera moves, cut-out, lint, sheet")
    di.add_argument("project"); di.add_argument("--video", help="the footage to edit (a person talking, any size)"); di.add_argument("--script", help="the words, if there is no footage (or to fix the transcript)")
    di.add_argument("--voice", help="voiceover for a script"); di.add_argument("--frame", choices=["auto", "portrait", "landscape"], default="auto", help="auto = the footage's own shape")
    di.add_argument("--format", default="auto", choices=["auto"] + list(DESIGNS)); di.add_argument("--style", help="style pack to lean on, e.g. crimson")
    di.add_argument("--brand", help="brand website: logo, colours, fonts are read from it"); di.add_argument("--brand-name"); di.add_argument("--logo"); di.add_argument("--accent")
    di.add_argument("--reference", help="a reference video whose look to study (writes a frame grid)"); di.add_argument("--every", type=float, default=2.0)
    di.add_argument("--from", dest="start", type=float, help="use the footage from this second"); di.add_argument("--to", dest="end", type=float, help="... to this second")
    di.add_argument("--model", default="small", help="speech model for the transcript"); di.add_argument("--language")
    di.add_argument("--no-cutout", action="store_true", help="skip cutting the person out")
    gd = sub.add_parser("guide", help="the brief, scene types and commands"); gd.add_argument("--json", action="store_true")
    sub.add_parser("doctor", help="what this machine can do")
    r = sub.add_parser("render"); r.add_argument("project"); r.add_argument("--fps", type=int, default=30)
    r.add_argument("--music"); r.add_argument("--music-vol", default="0.18")
    r.add_argument("--workers", type=int, default=4, help="parallel browsers (default 4)")
    r.add_argument("--from", dest="start", type=float, help="test render: start second (writes output/<name>-test.mp4, no audio)")
    r.add_argument("--to", dest="end", type=float, help="test render: end second")
    r.add_argument("--crf", type=int, default=14, help="x264 quality, lower = better (default 14, visually lossless)")
    r.add_argument("--no-loudnorm", action="store_true", help="keep the audio level as it is (default: normalise to -14 LUFS)")
    c = sub.add_parser("capture"); c.add_argument("project"); c.add_argument("--url", required=True)
    c.add_argument("--find", help="exact text on the page to highlight (copy it from the page)")
    c.add_argument("--name", help="shot name (default: from the URL)")
    c.add_argument("--height", type=int, default=1100, help="CSS px to capture when --find is not given")
    c.add_argument("--width", type=int, default=430, help="phone width in CSS px")
    cf = sub.add_parser("config"); cf.add_argument("project")
    cf.add_argument("--interactive", action="store_true", help="ask the setup questions")
    cf.add_argument("--set", action="append", metavar="KEY=VALUE", help="set one answer (repeatable)")
    cf.add_argument("--redo", action="store_true", help="ask every question again, even answered ones")
    bk = sub.add_parser("backdrop", help="make a free backdrop (no account needed)"); bk.add_argument("project")
    bk.add_argument("--name"); bk.add_argument("--seed", type=int, default=7)
    bk.add_argument("--colors", default="#0B1F3F,#1E4E8C,#3B82C4,#0A1530", help="comma-separated hex colours (default: deep blues)")
    bk.add_argument("--video", action="store_true", help="animated gradient clip instead of a still")
    bk.add_argument("--seconds", type=int, default=12)
    bk.add_argument("--from-video", dest="from_video", help="use a still from this footage instead"); bk.add_argument("--at", type=float, default=1.0)
    fr = sub.add_parser("frames"); fr.add_argument("project"); fr.add_argument("video")
    fr.add_argument("--every", type=float, default=1.0, help="seconds between reference frames (default 1)")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")      # Windows consoles
    a = ap.parse_args()
    {"new": cmd_new, "segments": cmd_segments, "sheet": cmd_sheet, "render": cmd_render,
     "capture": cmd_capture, "frames": cmd_frames, "config": cmd_config, "backdrop": cmd_backdrop,
     "brand": cmd_brand, "plan": cmd_plan, "direct": cmd_direct, "lint": cmd_lint, "align": cmd_align, "voice": cmd_voice, "guide": cmd_guide, "doctor": cmd_doctor}[a.cmd](a)


main()
