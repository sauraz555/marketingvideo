# Fix foundations before chasing karaoke captions

The research supports a clear ordering for our shorts pipeline: prove it end to end once, fix safe zones, audio loudness and a handful of render bugs, and only then invest in word-timed captions, richer data components and better matting. No shorts project has ever been built with the engine in this repo, and nothing was rendered during the audit, so every layout and quality claim about our own pipeline is still a reading of the code. The external evidence is also weaker than it looks. Four of the five researchers could not open primary pages and worked from search summaries, and almost every "retention uplift" number in this field comes from tool vendors with no published method. What is well supported is structural: a hook that is on screen at frame 0, short keyword captions, one idea per beat, animated transitions that end on a held and labelled frame, stacked rather than side-by-side comparisons in 9:16, and a temporally stable matte composited outside the browser. Our engine already does several of these. Its real gaps are that the caption presets and brand mark probably sit under platform UI, the mux has no loudness normalisation, several documented options have no code path, and the QA sheet does not show the final composite. Every default value below that I or a researcher derived, rather than found in a source, is labelled "inferred".

## Most numbers are vendor claims; the structural rules hold up

### How far to trust this report

The platform-practice, motion-graphics and AI-backdrop researchers had page fetching blocked for nearly every host, so their findings are search-result summaries of the linked pages. The matting researcher read the GitHub repositories directly but saw papers and two key articles only as summaries. The pipeline audit read the repo code in full at HEAD `2c18c1a` but ran nothing, because Playwright was not installed. Three consequences follow:

- Official figures (YouTube upload settings, Meta and TikTok ad safe zones, ElevenLabs field names) are reported as relayed and need checking at source before they are hard-coded.
- Prices conflict between sources and were observed on 16 Nov 2026 through search only.
- Percentages attributed to captions, cuts or hooks are directional at best. I leave most of them out.

### Hook, length and pacing

The only quasi-official hook rule is TikTok's ad guidance, relayed by third parties: state the proposition in the first 3 seconds and land the hook within 6 ([Stackmatix](https://www.stackmatix.com/blog/tiktok-creative-best-practices-2026)). No platform publishes organic retention curves, and one counter-view argues the 3-second cut-off is an artefact of an old metric ([Autoclip](https://autoclip.dev/blog/why-3-second-hooks-are-overrated)). The inferred default is stricter than our brief: subject and text hook visible at frame 0, proposition fully on screen by 1.5 s and spoken by 3 s, and legible with sound off.

On length, the best data found is Socialinsider's H1 2026 study of brand TikToks, relayed by secondary sites: **engagement rate peaks at 15-30 s (about 6%) while median views rise with length up to 2-3 minutes** ([Socialinsider](https://www.socialinsider.io/blog/how-long-are-tiktok-videos/) via [SocialRails](https://socialrails.com/blog/best-tiktok-video-length-maximum-engagement)). A 16,537-video Shorts analysis found 16-30 s strongest, with the caveat that feed distribution was not verified per video ([OverseerOS](https://www.overseeros.com/blog/best-youtube-shorts-length)). Our setup default is 45-60 s (`tools/shorts.py:48`). That is defensible for number-dense migration content, but a 20-35 s option should exist (inferred band), with 180 s as the hard cap because Shorts classification stops at three minutes ([YouTube Help](https://support.google.com/youtube/answer/15424877?hl=en), via snippet).

Cut cadence is convention. Guides say a visual change every 2-4 s, and that zooms, highlights and caption changes count as changes ([Postiv](https://postiv-marketing.pages.dev/blog/social-media-video-editing-guide), [FluxNote](https://fluxnote.io/guides/faceless-shorts-retention-tips-2026)). The counter-evidence is worth encoding too: viewers habituate to interrupts on an exact beat, so intervals should vary ([edicionvideopro](https://edicionvideopro.com/en/editing-for-platforms-video-marketing/pattern-interrupts-tiktok-retention-guide/)), and one long-form channel's views rose as its cuts per minute fell ([AIR Media-Tech](https://air.io/en/youtube-hacks/advanced-retention-editing-cutting-patterns-that-keep-viewers-past-minute-8)). Our brief's "new visual every 3-5 s, bigger break every 8-10 s" (`.claude/agents/shorts-director.md:26-40`) is within the convention.

### Captions

The strongest evidence comes from multimedia-learning research, not from platforms. Mayer's reviews report medium-to-large effects for cutting extraneous material, cueing the essential item and presenting in short segments ([Mayer 2017](https://zendy.io/title/10.1111/jcal.12197)). The effect of duplicating narration as on-screen text conflicts sharply between editions, 0.87 against 0.10 ([UNH handout](https://www.unh.edu/teaching-learning-resource-hub/sites/default/files/media/2023-06/itow-research-based-principles-for-designing-multimedia-instruction-mayer.pdf)). These figures came from secondary copies and should be confirmed before anyone quotes them.

That pattern favours what our engine already does: a short `lead` plus a 1-3 word `key`, rather than verbatim running subtitles. Word-by-word highlighted captions are the dominant style, but no independent A/B test was found, and the "+34% watch time" figure is one vendor's internal test of 80 videos ([FluxNote](https://fluxnote.io/blog/ai-captions-that-improve-watch-time)).

There is a second reason not to lead with karaoke captions. Our default voice is "nepali + english mix" with English captions that summarise rather than translate (`tools/shorts.py:39-40`, `templates/shorts/README.md:34-39`). Word-synced verbatim captions do not apply to that case at all. Word timings are still worth having, but for a different job: starting scenes and captions on the spoken word, which silence detection cannot do.

Practitioner sizes for 1080x1920 put the floor at about 48 px and the working range at 60-75 px bold ([BlitzCut](https://blitzcutai.com/blog/best-caption-size-tiktok-2026)). Our `lead` is 50 px and our `key` 112 px (`templates/shorts/short.html:66-68`), so the lead sits at the floor.

### Safe zones

Platforms publish safe zones for ads only, and the third-party figures conflict.

| Source (all as relayed) | Top | Bottom | Left | Right |
|---|---|---|---|---|
| Shorts, Google vertical ad guidance ([BreakReach](https://www.breakreach.com/tools/safe-zone-checker)) | 288 | 672 | 48 | 192 |
| Reels, Meta Ads Guide 14% / 35% / 6% ([BeReel](https://www.bereel.pro/blog/instagram-reels-size-dimensions-safe-zones)) | 269 | 672 | 65 | 65 |
| TikTok In-Feed template ([Upload-Post](https://www.upload-post.com/tools/safe-zone-checker/)) | 240 | 660 | 120 | 120 |
| TikTok organic, looser guides ([Uplads](https://uplads.com/tools/safe-zone-checker)) | 130 | 320-480 | n/a | 140 |

Taking the largest of each ad margin gives an inferred strict box of x 120-888, y 288-1248. Several guides use a looser organic working area of about 900x1400 centred ([AdaptlyPost](https://adaptlypost.com/blog/social-media-safe-zones-2026-complete-guide)).

Measured against those figures, our fixed positions look wrong in three places. This is my arithmetic on the code, with caption block heights estimated, since nothing was rendered.

- **Brand mark.** It sits at top 70 px (`templates/shorts/short.html:63`), inside every quoted top margin.
- **`plow` and `low` presets.** At 1500 and 1440 (`templates/shorts/short.html:71-72`, `:219`) they put caption text roughly between y 1440 and 1690, inside the 310-480 px organic bottom overlay most guides describe.
- **The brief's only safe-zone rule.** "Nothing sits in the bottom 150 px except captions" (`.claude/agents/shorts-director.md:78`) is looser than every figure found.

The default caption top of 1240 is plausible for organic posts but sits at the very edge of the strict box.

### Export and audio

YouTube's recommended upload bitrate for 1080p SDR at 30 fps is 8 Mbps, as shown in a search snippet of its help page ([YouTube Help](https://support.google.com/youtube/answer/1722171?hl=en)). The loudness target of about -14 LUFS integrated with -1 dBTP true peak is convention, not a published TikTok or Meta specification ([ThePostFlow](https://thepostflow.com/post-production/post-production-workflows/export-settings-youtube-instagram-tiktok/)).

Our shorts mux applies no loudness normalisation at all (`tools/shorts.py:442-460`), while the explainer tool already does (`tools/vo.py:124`). Music guidance is a bed 18-24 dB under the voice ([OverseerOS](https://www.overseeros.com/blog/background-music-volume-under-voiceover)) or ducking of 6-12 dB with 30-80 ms attack and 250-700 ms release ([CapCut](https://www.capcut.com/create/audio-ducking-for-clear-dialogue-in-video)). Our 0.18 gain is about -15 dB by my calculation, and the sidechain uses 20 ms attack and 400 ms release (`tools/shorts.py:448-454`). That is close enough to settle by ear.

## Stack comparisons vertically, animate once, then hold

### Comparisons

In 9:16 a top-and-bottom split keeps the full 1080 px width for each side. Creators are moving to that layout over the side-by-side split ([Adweek](https://www.adweek.com/sponsored/the-worlds-most-creative-people-show-you-how-to-master-vertical-video/)), and a layout that looks balanced in the editor can be indecipherable once panels shrink on a phone ([ShortGenius](https://shortgenius.com/blog/split-screen-video-editing)). No controlled study compares the two layouts in vertical video, so this is practitioner opinion plus pixel arithmetic.

Our `compare` scene is side-by-side 440 px cards only (`templates/shorts/short.html:343-349`, CSS `:93-98`), which is the weakest of the layouts the researcher ranked. For "how much bigger" stories the best-ranked treatment is two stacked horizontal bars with direct value labels. That also needs a horizontal mode our `chart` builder lacks (`templates/shorts/short.html:357-367`). Horizontal bars are the recommended form when labels are long or there are more than four or five categories ([Flourish](https://flourish.studio/blog/social-media-charts-and-graphs/), [Better News](https://betternews.org/making-data-visualizations-interactives-work-well-mobile/)).

### Animation versus static

The controlled evidence pulls in two directions, and the design answer is to use both.

- Animated transitions between chart states significantly improved object tracking and value estimation in Heer and Robertson's experiments ([UW Interactive Data Lab](https://idl.uw.edu/papers/animated-transitions)).
- A later study found static small multiples about 10% more accurate than animation for reading trends, though viewers preferred animation ([UW CSE442 slides](https://courses.cs.washington.edu/courses/cse442/18au/lectures/CSE442-Animation.pdf)). This is a lecture-slide summary and needs checking against the paper.

So grow the bar or count the number up, then hold a static, fully labelled end frame long enough to read. The associated design guidance is staging in simple steps and transitions "as long as needed but no longer" ([UW CSE442 slides](https://courses.cs.washington.edu/courses/cse442/24au/lectures/CSE442-Animation.pdf)).

### Dwell time and chart simplification

No source gives a tested minimum on-screen time for charts in shorts. The researcher derived a rule from Netflix's subtitle limits of 17 characters per second and 200 words per minute for adult programmes ([Netflix](https://backlothelp.netflix.com/hc/en-us/articles/216787938-Portuguese-Timed-Text-Style-Guide)):

- Inferred hold after the animation ends: the largest of 1.0 s, 0.3 s per word, or characters divided by 17, plus about 0.5 s per number the viewer must compare.
- A five-bar chart therefore needs roughly 3.5-4.5 s after the last bar lands. Our bars take 0.7 s with a 0.2 s stagger, so the scene must run well past its animation.

Chart-for-video guidance is consistent: bigger type than a web chart, direct labels in place of axes, remove what narration will say ([Online Journalism Blog](https://onlinejournalismblog.com/2026/06/23/showing-charts-on-video-here-are-two-essential-techniques-to-make-them-effective/)), and put the source on the chart because reshared posts lose context ([Flourish](https://flourish.studio/blog/social-media-charts-and-graphs/)). Our chart already scales to the largest value, highlights one bar and carries a source note. It is missing count-up on values other than `bignum` (`templates/shorts/short.html:330-331` against `:336-342`, `:360`, `:420-425`) and any second chart form.

### Motion vocabulary and screenshots

The motion defaults are convention. Material's legacy guidance has elements entering in about 225 ms, leaving in about 195 ms, and transitions over 400 ms feeling slow ([Material Design](https://m1.material.io/motion/duration-easing.html)). It is UI guidance, but it supports exits that are shorter than entrances. The researcher's inferred presets are:

- Word build: 0.3-0.4 s, `power3.out`, 0.06-0.10 s stagger. Our fixed 0.07 s stagger (`templates/shorts/short.html:319`) is inside that range.
- Overshoot: at most one overshoot ease per scene, and none on numbers the viewer must read.
- Total build of a text block: under about 1 s.

GSAP 3.13 made SplitText and the other formerly paid plugins free ([GSAP](https://gsap.com/blog/3-13/)). We load 3.12.5 from a CDN (`templates/shorts/short.html:14`). The exact API details were not confirmed, because gsap.com was unreachable.

For screenshots, vendor advice is to zoom to the element being acted on at about 1.5-2.2x ([OpenScreen](https://www.mintlify.com/siddharthvaddem/openscreen/guides/creating-demos)) and to pair the zoom with a gradual spotlight ([Trainn](https://trainn.co/answers/how-to-add-spotlight-effects-to-your-product-demo-videos/)). All of it comes from 16:9 tools. The researcher's arithmetic shows that range is too low for desktop UI in portrait: a 1440 px screenshot fitted to 1080 px renders 14 px labels at about 10 px. Every readable beat must therefore be a crop of roughly 350-450 source pixels, or a "callout extract" card (inferred). Our `web` and `doc` scenes scroll and highlight (`templates/shorts/short.html:433-459`) but cannot extract and enlarge a region.

## Keep RVM, composite in ffmpeg, and repair the edges

### Which matting model

The incumbent is the right default. Robust Video Matting is the only option surveyed that combines built-in temporal recurrence, no prompt or first-frame mask, and ONNX builds tested on CPU ([RVM repo](https://github.com/PeterL1n/RobustVideoMatting)). That matches a locked-off single presenter on modest hardware.

| Model | Temporal | Needs mask | Speed evidence | Licence | Role for us |
|---|---|---|---|---|---|
| RVM mobilenetv3 / resnet50 | Yes | No | ~110 fps at 1440² on an RTX 5080 laptop; no published CPU figure | GPL-3.0 | Default. Use resnet50 if a GPU exists |
| BiRefNet (HR-matting, portrait) | No, per frame | No | 17 fps at 1024² on an RTX 4090 | MIT | Stills and freeze-frames; hair-detail tier |
| BEN2 Base | No, per frame | No | 0.130 s per image on an RTX 3090 (vendor) | MIT | Alternative per-frame tier |
| MatAnyone 2 | Yes | First-frame mask | 9.3 fps at 1440² on an RTX 5080 laptop | NTU S-Lab 1.0 | Not cleared for commercial use until the licence is read |
| RMBG-2.0 | No | No | n/a | CC BY-NC 4.0 | Excluded. It is also the rembg default |

Sources: [BiRefNet repo](https://github.com/ZhengPeng7/BiRefNet), [BEN2 repo](https://github.com/PramaLLC/BEN2), [MatAnyone2 repo](https://github.com/pq-yang/MatAnyone2), [rembg README](https://github.com/danielgatis/rembg), [VRAutoMatte benchmarks](https://github.com/SifuInTheShell/VRAutoMatte/blob/master/docs/BENCHMARKS_2026-07-08.md).

Three caveats apply to this table:

- **Quality comparison.** No independent head-to-head measures flicker and hair across these models on talking-head footage. The one practitioner benchmark is a speed test with subjective quality notes, and it found resnet50 as fast as mobilenetv3 on NVIDIA hardware.
- **MatAnyone 2 licence.** The reading that S-Lab 1.0 is non-commercial is the researcher's recollection. The licence file could not be opened.
- **RVM licence.** That GPL-3.0 does not bite when we publish only rendered MP4s is a reading, not legal advice. It is helped by `tools/models/` being git-ignored (`.gitignore:19-20`).

### Alpha transport

Our architecture is already the most robust of the options ranked. Chromium renders graphics layers with transparent backgrounds, and ffmpeg merges footage and matte with `alphamerge` (`tools/shorts.py:343-415`). Remotion, a headless-Chrome renderer like ours, documents transparent video as roughly 40% slower to render and recommends an opaque fallback ([Remotion](https://www.remotion.dev/docs/transparent-videos)). The researcher took that as indirect evidence that seeking alpha video per frame in a browser is fragile. No primary test of frame-accurate seeking in headless Chromium was found. Our backdrop and photo videos, which are seeked in the page (`templates/shorts/short.html:560-570`), deserve a burned-in frame-number test.

### Edge quality

`tools/matte.py` leaves quality on the table in three ways:

- **No despill.** It discards RVM's predicted foreground and keeps only alpha (`tools/matte.py:62-64`), so edge pixels still carry the old wall colour. Using the foreground layer is the AI-matte equivalent of despill.
- **One fixed edge treatment.** The only control is a 5x5 blur (`tools/matte.py:50-51`). There is no choke or feather.
- **One hard-coded model.** The small model's path is fixed (`tools/matte.py:13`).

The RVM repo recommends a downsample ratio of 0.25 at 1080p and 0.375 at 720p. Our 720-wide, 0.375 default (`tools/matte.py:29-31`) is consistent, and a 1080-wide, 0.25 pass is the natural quality tier. The choke, feather, light-wrap and grain recipes in the notes are untested constructions from standard ffmpeg filters and need a visual pass. The claim that predicted foreground beats source colour at the edge has no measured comparison behind it.

### Presenter styles and fallbacks

No source catalogues cut-out presenter styles or measures retention by style, so the style list is common practice. Two parts of it matter for the plan.

First, our existing moves already match the sourced timing. Punch-ins should be fast, 0.3-0.5 s, and lose their effect at a second or more ([edicionvideopro](https://edicionvideopro.com/en/editing-for-platforms-video-marketing/pattern-interrupts-tiktok-retention-guide/)). Ours ramps in over 0.18 s at 12% (`tools/shorts.py:338-372`).

Second, the cheapest styles hide matte errors. All three are absent today:

- a white sticker stroke around the cut-out, which masks rough hair edges
- a picture-in-picture circle, which needs no matte
- a hard top/bottom split, which also needs no matte

The in-page fallback is a card shrink that only `pills` and `cta` trigger (`templates/shorts/short.html:526-530`).

### Shooting and disclosure

Shooting guidance is general: contrast between subject and background, even lighting, and distance from the wall ([cutout.pro](https://www.cutout.pro/learn/blog-remove-video-background-without-green-screen/), [Filmora](https://filmora.wondershare.com/video-editing-tips/remove-video-background-without-green-screen.html)). The fps and shutter advice in the notes is unsourced inference.

A real, matted presenter is an edit, not synthetic media. Under YouTube's rule, realistic altered or synthetic content must be disclosed, while effects such as background blur need not be ([YouTube Help](https://support.google.com/youtube/answer/14328491)). An AI avatar or a realistic AI voice is in scope on all three platforms, per secondary sources. Whether an AI voiceover alone triggers a label was not established.

## Stills and procedural plates first; Kling only for hero shots

### Cost and choice of generator

A still backdrop costs roughly $0.03-0.06 through an API in the mid-priced band ([movcl.com](https://movcl.com/blog/comparisons/ai-image-api-prices-compared/)), against about $0.25-1.70 for a 5-10 s silent video clip. That makes "one still plus Ken Burns in GSAP" the rational default and matches our config defaults of images and "free only" (`tools/shorts.py:44-47`). Procedural gradients are free, on-palette, loop perfectly and raise no AI-label question, provided they are driven from the timeline, not wall-clock time. That is engineering judgement, not a sourced finding.

| Video generator | Price per second (search summaries, 16 Nov 2026) | Notes |
|---|---|---|
| Kling 3.0 Standard / Pro | $0.084 / $0.112 silent; $0.126 / $0.168 with audio | 3-15 s, 9:16, start and end frame |
| Kling 4.0 | No published API price | App release 15 Oct 2026; API status conflicting |
| Veo 3.1 Lite / Fast / Standard | $0.05-0.08 / $0.10-0.12 / $0.40 | SynthID watermark; listed as Preview |
| Runway Gen-4.5 | $0.12 | 720p ceiling, 2-10 s, 9:16 |
| Wan 2.5 (hosted) | $0.05 | Wan 2.2 weights are Apache-2.0 |
| Sora 2 | Retired | API shut down 24 Sep 2026 |

Sources: [Picasso IA](https://blog.picassoia.com/cheapest-kling-3-0-api-pricing-compared), [Pletor](https://docs.pletor.ai/ai-model-library/video-models/kling-3.0), [creaa.ai](https://creaa.ai/blog/kling-4), [benchlm.ai](https://benchlm.ai/md/media-pricing/veo.md), [OpenRouter](https://openrouter.ai/runway/gen-4.5/api), [fal.ai](https://fal.ai/pricing), [The Decoder](https://the-decoder.com/openai-sets-two-stage-sora-shutdown-with-app-closing-april-2026-and-api-following-in-september/). No vendor pricing page was opened and several figures conflict.

Two points for our Kling guidance:

- **The brief names a default it cannot price.** It names `kling-video-v4_0` at 3-30 s as the default (`.claude/agents/shorts-director.md:46`), but no API price for Kling 4.0 was found and one tracker warns against any site quoting one. The brief should tell the agent to read the price from the connector's own estimate, fall back to 3.0, and always ask for the silent tier, since audio costs about 50% more.
- **Loops.** Start frame equal to end frame is the simplest loop request Kling supports (inferred).

Kling "integration" in this repo is prose only. There is no client, no ledger and no aspect check in code. The Sora shutdown is a reason to keep any future integration behind a thin adapter.

### Prompting and legibility

Backdrop prompting advice is thin and comes from vendor guides: name the empty text zone, one slow cyclical motion and a quiet energy level, and check the loop seam yourself ([Cliprise](https://www.cliprise.app/learn/guides/best-practices/ai-seamless-loop-video)). The legibility rule is firmer. Contrast over moving video must hold on the brightest frame in the text area, not the average ([OpenDesign](https://open-design.ai/blog/text-over-moving-backgrounds/)). A gradient scrim also fails when text spans the frame, so uniform darkening is safer ([Suleiman](https://blog.iamsuleiman.com/techniques-to-display-text-overlay-background-images/)). Our backdrops have a uniform `dim` of 0.38 and captions get only a drop shadow (`templates/shorts/short.html:534-550`, `:35`). No measured blur or dim values exist for 9:16 captions, so 0.38 needs an on-device check.

### AI labelling

The platforms key disclosure on realism. An abstract backdrop falls outside the trigger. A photoreal AI street behind a presenter should be labelled. YouTube now auto-labels and the label can be permanent when C2PA metadata marks content as fully generative ([The Next Web](https://thenextweb.com/news/youtube-will-now-automatically-label-ai-generated-videos-whether-creators-disclose-them-or-not)). The TikTok and Meta details are from secondary guides that disagree. The safe policy is to record AI use per project and disclose at upload. Our brief already forbids passing generated pictures off as real (`.claude/agents/shorts-director.md:42-53`).

### Frameworks and voice timing

HyperFrames from HeyGen is architecturally our pipeline: HTML and GSAP seeked frame by frame in headless Chrome and encoded with ffmpeg, under Apache-2.0, with a lint step and a catalogue of about 450 blocks ([HyperFrames repo](https://github.com/heygen-com/hyperframes)). Remotion requires a paid company licence above three employees ([Remotion licence](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md)).

My position is to borrow, not migrate. Our layered presenter composite and Python tooling are the parts that work, and the borrowable ideas are small: a lint step, a font-readiness timeout (a `document.fonts.ready` hang is a reported failure, per [jonblog](https://jonblog.pages.dev/2026-04-26-hyperframes-html-to-video/)), and a caption paging function like Remotion's `createTikTokStyleCaptions` ([Remotion docs](https://remotion.dev/docs/captions/create-tiktok-style-captions)).

For timing there are two ElevenLabs routes:

- **Generated voice.** The `with-timestamps` endpoint returns character-level alignment with the audio ([ElevenLabs](https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps.md)).
- **Supplied audio.** Forced Alignment takes existing audio plus known text and returns word timings with a per-word loss value ([ElevenLabs](https://elevenlabs.io/docs/overview/capabilities/forced-alignment)). This is the route that matches our default "I provide an audio file".

Field units and model support were not confirmed. Nothing in the research establishes how well either route, or Whisper, handles mixed Nepali and English speech.

## Four phases, ordered by impact against effort

The plan starts with verification, because both the research and the pipeline are unproven in the places that matter most. Line references are from `current_pipeline_audit.md` at HEAD `2c18c1a`. "Evidence" states how well the recommendation is supported, not how confident I am in the engineering. Nothing here has been implemented, and this report changed no file other than itself.

### Phase 0: verify locally before changing anything (one to two days)

Build one real short end to end in `projects/`, without a presenter first and then with one. Keep it as the committed reference, because "what good looks like" currently exists only in prose. During that build, settle the following questions.

| Verify | How | Why it gates later work |
|---|---|---|
| Safe zones | Download the TikTok In-Feed overlay, the Meta Ads Guide and Google's vertical spec. Upload an unlisted test to each app and screenshot it with UI visible | Every pixel figure is second-hand and conflicting. It decides the constants in 1.1 |
| Caption size and contrast | View the reference short on two phones. Check the 50 px lead and the 0.38 dim on the brightest backdrop frame | Size advice spans about 2x. No measured dim values exist |
| Render facts | Record render time, file size at CRF 14, and ffprobe output. Measure integrated loudness | None were measured (`tools/shorts.py:598`, `:442-460`) |
| Video seek accuracy | Use a backdrop clip with burned-in frame numbers. Compare 100 rendered frames | Inferred risk in `seekMedia` (`templates/shorts/short.html:560-570`) |
| H.264 decode | Confirm Edge or Chrome channels exist on the render machine | Bundled Chromium cannot decode H.264 (`tools/shorts.py:218-227`) |
| Matte speed and quality | Time `tools/matte.py` on a 10 s clip. Score flicker as mean frame-to-frame alpha change in a static region. Make a 200% hair contact sheet | No CPU figures exist anywhere. No independent quality comparison exists |
| Model weights | Record where `rvm_mobilenetv3_fp32.onnx` and the resnet50 build come from | Undocumented (`.gitignore:19-20`, `templates/shorts/README.md:74`) |
| Alignment on our audio | Run ElevenLabs Forced Alignment and a local Whisper pass on one Nepali and English voice file. Inspect word timings and loss values. Confirm field names and units | Decides whether 2.1 is viable for the default voice language |
| Kling connector | Read the model names, durations and price estimate the connector actually returns | The brief's `kling-video-v4_0` default has no published API price |

### Phase 1: high impact, low effort

| # | Change | Where | Evidence |
|---|---|---|---|
| 1.1 | Add safe-zone constants in two tiers, strict and organic. Move the brand mark and the `plow`, `low` and `ptop` presets inside them. Draw the guides on the QA sheet. Replace the "bottom 150 px" rule | `templates/shorts/short.html:63`, `:66`, `:71-72`, `:211`, `:218-219`; `tools/shorts.py:263-273`; `.claude/agents/shorts-director.md:78` | Relayed ad specs. Values inferred. Phase 0 confirms |
| 1.2 | Normalise the final mix with two-pass `loudnorm` to an inferred -14 LUFS and -1 dBTP. Set AAC to 48 kHz | `tools/shorts.py:442-460`; pattern at `tools/vo.py:124` | Convention. YouTube audio figures via snippet |
| 1.3 | Fix render paths that silently do the wrong thing: scale and crop presenter footage to 1080x1920; mix music when there is no voice; honour `--from/--to` in the plain path; extract the presenter's own audio; warn when `moves` exist without a matte | `tools/shorts.py:384` and `:370`; `:446-457`; `:437-438`; `:444-447`; `:429-430` with `templates/shorts/short.html:508`, `:523` | Code audit inference. Not yet reproduced |
| 1.4 | Make the QA sheet honest: composite the layered view for presenter projects, and report page errors and failed assets | `tools/shorts.py:245-274`; `templates/shorts/short.html:260`; pattern at `tools/frames.py:20-22` | Code audit inference |
| 1.5 | Add a font-readiness timeout. Vendor GSAP and the fonts so renders do not depend on CDNs | `tools/shorts.py:218-237`; `templates/shorts/short.html:14-16` | Reported failure in a similar renderer |
| 1.6 | Update the director brief: hook on screen at frame 0 and complete by an inferred 1.5 s; varied change intervals of about 2-4 s; strongest break near the midpoint; the hold-after-animation rule; a short CTA with no fade so the end loops; Kling 3.0 fallback, silent tier, start = end frame | `.claude/agents/shorts-director.md:26-40`, `:42-53`, `:46` | Practitioner convention. Dwell rule inferred from Netflix limits |
| 1.7 | Add a 20-35 s length choice and an `ai_disclosure` answer. Add an upload-label reminder to QA | `tools/shorts.py:38-53`, `:48`; `.claude/agents/shorts-director.md:76-80` | Length from relayed studies. Labelling from YouTube Help plus secondary sources |
| 1.8 | Bring the docs back in line with the code: all 19 scene types and the `backdrops`, `moves` and `logo` keys in the template header; one caption word rule; the look default; the card-shrink claim; weight download steps | `templates/shorts/script.js:9-28`; `templates/shorts/README.md:7`, `:34-39`, `:74`; `.claude/agents/shorts-director.md:30`; `tools/shorts.py:44` | Code audit |

Two notes on 1.8. The caption word rule conflicts between README (key 1-3 words) and the brief (2-5). Also, CLAUDE.md says captions are the voiceover script while the shorts README says they summarise a Nepali voice. That is a policy choice for the person to make, not something for the code to decide.

### Phase 2: high impact, medium effort

| # | Change | Where | Evidence | Verify first |
|---|---|---|---|---|
| 2.1 | Add word timings. Either a new `align` subcommand or an extension of `segments` writes `window.WORDS` beside `SEGMENTS`. Scenes may then start on a word. When voice and caption language match, the key words pop on their spoken times and one active word takes the accent colour | `tools/shorts.py:191-214`, dispatch `:617-618`; `templates/shorts/short.html:305-307`, `:313-319`; endpoint gap at `tools/vo.py:18` | ElevenLabs docs via summary. Benefit of word highlighting is vendor-only | Phase 0 alignment test. API field units |
| 2.2 | Caption legibility: an optional stroke or scrim behind captions, a Devanagari webfont when captions are Nepali, and a worst-frame contrast check | `templates/shorts/short.html:15`, `:35`, `:66-69`, `:552-554`; `tools/shorts.py:40` | WCAG thresholds from secondary sources. Stroke is convention | On-device check |
| 2.3 | Data components: a stacked layout for `compare`; a horizontal-bar mode with direct labels for `chart`; a shared count-up helper for `stat`, `badges` and chart values with tabular figures; removal of the dead `.nm` style | `templates/shorts/short.html:343-349` and `:93-98`; `:357-367` and `:114-124`, `:121`; `:330-331`, `:336-342`, `:360`, `:420-425` | Layout is practitioner opinion. Animate-then-hold is from controlled studies | Phone readability of each new layout |
| 2.4 | A `lint` subcommand run before `sheet`: DOM overflow, caption and visual overlap, safe-zone breach, missing assets, duration against `length_seconds`, seconds per scene, repeated scene types, dwell-rule breaches | `tools/shorts.py:617-618`, `:110-113`; rules now only in `.claude/agents/shorts-director.md:26-40`, `:78` | Pipeline write-ups. Thresholds inferred | Tune thresholds on the reference short |
| 2.5 | Matte quality flags: output RVM foreground as well as alpha; choke and feather controls; a model flag for resnet50; an execution-provider flag; a 1080-wide, 0.25-ratio tier | `tools/matte.py:13`, `:29-31`, `:42-46`, `:50-51`, `:62-67`; consumer at `tools/shorts.py:384-386`, `:426` | RVM repo read directly. Edge recipes untested | Phase 0 flicker and hair sheet, before and after |
| 2.6 | Presenter fallbacks that need no clean matte: a picture-in-picture circle and a hard top/bottom split. For matted footage, a sticker stroke and contact shadow, plus one grain pass over the final composite | `templates/shorts/short.html:217-240`, `:526-530`; `tools/shorts.py:343-415` | Common practice, unsourced | Visual pass |

### Phase 3: medium impact, medium effort

| # | Change | Where | Evidence |
|---|---|---|---|
| 3.1 | New scenes: progress ring, single-series line with end label, vertical timeline, before/after wipe, and a callout extract that enlarges a region of a `web` or `doc` capture. Let `pills` and `list` rows land on narrated beats | `templates/shorts/short.html:311-482`, `:350-356`, `:426-432`, `:433-459` | Component specs are inferred defaults. The portrait screenshot arithmetic is the researcher's |
| 3.2 | A small transition set (cut, wipe, zoom-through) and one slow ambient move per scene, kept off text layers | `templates/shorts/short.html:311-482`, `:487-488` | Convention. No measured values |
| 3.3 | Backdrops: a timeline-driven looping procedural option; automatic `dim` from the brightest frame under the caption box; writing the entry into `script.js`; a budget ledger and prompt-hash cache if a generator is ever wired in | `tools/shorts.py:129-165`, `:46-47`; `templates/shorts/short.html:534-550` | Contrast rule sourced. The rest is engineering judgement |
| 3.4 | Optional sound-effect cues per scene, mixed about 8-12 dB under the voice (inferred) | `tools/shorts.py:442-460`; `templates/shorts/script.js:22-28` | Convention only. No data |
| 3.5 | Export hygiene: bt709 tags and, if Phase 0 shows very large files, a higher CRF or a bitrate ceiling above 8 Mbps | `tools/shorts.py:413-414`, `:439-441`, `:598` | YouTube figure via snippet. The rest inferred |
| 3.6 | Move to GSAP 3.13 or later for SplitText masks | `templates/shorts/short.html:14` | Release post via summary. Confirm the API in the docs first |

### Phase 4: defer until the earlier phases prove a need

- A per-frame BiRefNet tier for freeze-frames and hero stills.
- Any use of MatAnyone 2, which waits on reading its licence.
- A serious evaluation of migrating to HyperFrames.
- AI avatars, multi-aspect exports, cover-frame export and hook variants.

None of these fixes a known defect, and each rests on evidence that is thinner than the work it would cost.

## Conclusion

The research changed the question. We set out to find better techniques and found that our engine's design choices are mostly the defensible ones: phrase captions with one emphasised word, staged entrances, ffmpeg-side presenter compositing and a recurrent matting model. Its weaknesses are unglamorous. Positions were chosen without reference to platform UI, the audio path was never finished, and the QA step does not show the final picture. The fashionable upgrade, word-by-word karaoke captions, has the weakest evidence of anything surveyed and does not even apply to a Nepali voice with English summary captions.

The durable gain is measurement we own. A committed reference short, a lint step that turns the brief's prose rules into checks, and platform retention curves from our own uploads will tell us more than any vendor percentage. Until those exist, every inferred default in this report should be read as a starting value to test, and Phase 0 is the work that turns them into facts.
