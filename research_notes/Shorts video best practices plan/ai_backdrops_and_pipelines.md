# AI-generated backdrops and programmatic / automated short-form video pipelines (state as of 16 Nov 2026)

> Reading note for the report writer. Research was done 2026-11-16. In this session almost every vendor site (kling.ai, elevenlabs.io, remotion.dev, artificialanalysis.ai, hyperframes.heygen.com, fal.ai pricing, Google, OpenAI, TikTok, Meta) was **not reachable by direct fetch**; only github.com pages were read in full. Everything else comes from web-search result summaries of the linked pages. Where a figure is marked "(search summary)" it was not read on the page itself and the link is the page the search engine attributed it to; where sources disagreed that is stated. All prices are USD and "observed 2026-11-16 via search" unless another date is given. Verify every price on the vendor page before budgeting.

## 1. AI video generators for backdrops / B-roll (Kling, Veo, Sora, Runway, Luma, Pika, Hailuo, Seedance, Wan, LTX, Hunyuan)

### Takeaway
For 9:16 background plates the practical API choices in Nov 2026 are Kling 3.0 (about $0.08-0.17/s, 3-15 s, start+end frame), Veo 3.1 Fast/Lite ($0.05-0.12/s), Seedance 2.0, Runway Gen-4.5 ($0.12/s, 720p) and the open Wan family (about $0.05/s hosted, Apache-2.0); OpenAI's Sora 2 API was shut down on 24 Sep 2026 and should be removed from any plan. Kling 4.0 (30 s clips, 10 keyframes) launched in the app in Oct 2026 but its API price is not published.

### Cited Findings

**Kling (Kuaishou)**
- Kling 3.0 official API price list shows per-second billing in "Units": 0.9 Units ($0.126)/s for one tier with native audio and 1.2 Units ($0.168)/s for the next (search summary) — [Kling API pricing doc](https://kling.ai/document-api/pricing/base/video.md)
- On fal.ai, Kling 3.0 Pro is reported as starting at $0.112/s without audio and $0.168/s with audio (search summary of fal's own tutorial) — [fal.ai: How to use Kling 3.0 Pro](https://fal.ai/learn/tools/how-to-use-kling-3-0-pro)
- Kling 3.0 Standard reported at $0.084/s without audio, $0.126/s with audio, $0.154/s with voice control; Pro $0.112 to $0.168 (third-party) — [Picasso IA comparison](https://blog.picassoia.com/cheapest-kling-3-0-api-pricing-compared); same std/pro numbers on [302.AI listing](https://302.ai/product/detail/wavespeed-kwaivgi-kling-video-v3-image-to-video)
- Older, cheaper tier still listed on fal: Kling 2.5 Turbo Pro at $0.07/s (search summary) — [fal.ai text-to-video APIs](https://fal.ai/explore/text-to-video-apis)
- Kling 3.0 inputs: text only, text + start frame, text + start and end frame; clip length 3-15 s; aspect ratios 1:1, 16:9, 9:16 — [Pletor docs: Kling 3.0](https://docs.pletor.ai/ai-model-library/video-models/kling-3.0)
- Multi-shot generation: sources disagree on the limit (up to 5 shots with auto/custom modes vs up to 6 camera cuts with per-shot duration, framing and camera direction) — [Higgsfield](https://higgsfield.ai/blog/Expectations-from-Kling-3.0-User-Discussions-on-Updates); [Cliprise](https://www.cliprise.app/models/kling-3-0); shot-by-shot custom mode described in [Morphic guide](https://morphic.com/resources/how-to/kling-3.0-guide)
- 4K: conflicting. Some sources describe native 4K output for Kling 3.0, others say default is 1080p with 4K as a separate, much more expensive tier — [CineD](https://www.cined.com/kling-3-0-ai-video-model-introduced-native-4k-); [3D AI Studio](https://www.3daistudio.com/VideoStudio/kling-3)
- Kling 4.0: announced 28 Sep 2026, generally available in the Kling app on 15 Oct 2026; 30 s single generations, up to 10 keyframes, up to 15 reference assets; 10-bit HDR/4K and 2-minute extension "coming soon" — [Kling blog: 4 vs 3](https://kling.ai/blog/kling-4-vs-3); [fal.ai: What is Kling 4.0](https://fal.ai/learn/tools/what-is-kling-4-0); [Let's Data Science](https://letsdatascience.com/news/kling-ai-opens-kling-40-to-all-users-d9dc6422)
- Kling 4.0 API: status conflicting ("coming soon" vs "available for early access"); no official per-second price published, and one tracker warns to distrust any site quoting one — [creaa.ai tracker](https://creaa.ai/blog/kling-4)

**Google Veo 3.1**
- Gemini API per-second rates (audio included): Standard $0.40 at 720p/1080p, $0.60 at 4K; Fast $0.10 at 720p, $0.12 at 1080p, $0.30 at 4K; Lite $0.05 at 720p, $0.08 at 1080p; read 2026-09-11; no free tier; model listed as Preview (search summary of aggregator) — [benchlm.ai Veo pricing](https://benchlm.ai/md/media-pricing/veo.md)
- fal.ai lists Veo 3.1 (720p/1080p with audio) at $0.40/s (search summary) — [fal.ai text-to-video APIs](https://fal.ai/explore/text-to-video-apis)
- Veo output carries an invisible SynthID watermark, plus C2PA credentials on newer Google models; no visible mark (secondary source) — [Sentisight: hidden watermarks](https://www.sentisight.ai/hidden-watermarks-in-generative-ai-models/)

**OpenAI Sora 2 — retired**
- OpenAI ran a two-stage shutdown: Sora web/app discontinued 26 Apr 2026; Videos API and sora-2 / sora-2-pro models shut down 24 Sep 2026, with no replacement listed — [The Decoder](https://the-decoder.com/openai-sets-two-stage-sora-shutdown-with-app-closing-april-2026-and-api-following-in-september/); [dev.to migration note](https://dev.to/mr_manushukla/sora-2-and-the-videos-api-shut-down-on-24-september-2026-the-migration-and-the-real-cost-per-second-bek); [AI Engineer Guide retirement page](https://aiengineerguide.com/tools/model-retirements/sora-2/)
- Last published rates (historical): Sora 2 $0.10/s at 720p; Sora 2 Pro $0.30/s at 720p up to $0.70/s at 1080p (one May 2026 article says $0.50/s for Pro 1080p) — [benchlm.ai media pricing](https://benchlm.ai/md/media-pricing.md)

**Runway Gen-4.5**
- 720p output, 2-10 s clips, 16:9 and 9:16, first-frame image control, $0.12/s (12 credits/s at $0.01/credit) — [OpenRouter: Runway Gen-4.5](https://openrouter.ai/runway/gen-4.5/api)
- A separate write-up reports a 720p ceiling and no audio parameter in the API schema — [tech-insider Gen-4.5 API setup](https://tech-insider.org/runway-gen-4-5-api-setup-ai-video-2026/)

**Luma Ray3**
- Ray3 offers SDR, HDR and HDR+EXR variants from 540p to 4K, Modify Video, and an API; newer Ray3.14 (native 1080p) and Ray3.2 (June 2026) are mentioned by different sources — [gradually.ai: Gen-4.5 vs Ray 3.2](https://www.gradually.ai/en/ai-video-model-comparison/runway-gen-4-5-vs-ray-3-2/)

**Seedance 2.0 (ByteDance)**
- fal.ai lists Seedance 2.0 (720p with audio) at $0.3034/s (search summary) — [fal.ai text-to-video APIs](https://fal.ai/explore/text-to-video-apis)
- Prices vary widely by host: about $0.685/s at 1080p on fal vs $0.45/s and $0.329/s on resellers; a "Fast" tier is quoted at $0.09/s (third-party, unverified) — [aiapi-pro pricing comparison](https://aiapi-pro.com/blog/ai-video-generation-api-pricing-2026)

**Open-weights models**
- Wan 2.2 is released under Apache-2.0 (commercial use, modification and distribution allowed) — [Thunder Compute: best open-source video models](https://www.thundercompute.com/blog/best-open-source-ai-video-generation-models)
- fal.ai's pricing page lists Wan 2.5 at $0.05 per second (search summary) — [fal.ai pricing](https://fal.ai/pricing)
- LTX-2 uses a Lightricks community licence, not Apache: entities with annual revenue of at least $10,000,000 must obtain a paid commercial licence — [LTX-2 licence text (ScanCode DB)](https://scancode-licensedb.aboutcode.org/ltx-2-cla-2026.LICENSE)
- fal lists LTX-2-19B at $0.0018 per megapixel of video (search summary) — [fal.ai image-to-video guide](https://fal.ai/learn/tools/ai-image-to-video-generators)
- HunyuanVideo uses a custom Tencent licence: reported restrictions include a 100M-MAU threshold for commercial use and territorial exclusions for the EU, UK and South Korea (secondary sources; some describe HunyuanVideo 1.5 as having no declared licence) — [Fora Soft self-hosting guide](https://www.forasoft.com/learn/ai-for-video-engineering/articles-ai/self-hosting-hunyuanvideo-cogvideox-mochi-ltx)

**Independent ranking**
- Artificial Analysis runs blind-vote Elo arenas with separate boards for text-to-video and image-to-video, each with and without audio — [Artificial Analysis methodology](https://artificialanalysis.ai/video/methodology)
- Undated snapshot of the official board (search summary): with-audio board led by Dreamina Seedance 2.0 720p and HappyHorse-1.0, both Elo 1211; without-audio board led by HappyHorse-1.0 at 1357; recent additions include Wan2.7, Gemini Omni Flash, HappyHorse-1.1 — [Artificial Analysis text-to-video leaderboard](https://artificialanalysis.ai/video/leaderboard/text-to-video)
- An August 2026 third-party snapshot instead puts Gemini Omni Flash first (1,245), MiniMax H3 second (1,238), Seedance 2.0 third (1,223) on the with-audio board — [howaiworks.ai](https://howaiworks.ai/blog/best-ai-video-generator)

**Watermarking / provenance**
- An April 2026 matrix places Kling and Seedance among models that ship no mandatory machine-readable provenance or rely on proprietary tracking (secondary, unverified) — [tianpan.co: C2PA, SynthID and the audit trail](https://tianpan.co/blog/2026-04-26-content-provenance-c2pa-synthid-audit-trail)

### Inferences
- For a muted backdrop behind captions, top-of-leaderboard quality is unnecessary: a 5-10 s 720p/1080p silent clip costs roughly $0.25-$1.70 on Wan 2.5, Veo 3.1 Lite/Fast, Kling 2.5 Turbo or Kling 3.0 Standard, versus $2-$4 on Veo 3.1 Standard. Always request the no-audio tier where one exists (Kling charges about 50% more for audio).
- Image-to-video with a start frame (and for Kling, start = end frame) is the most controllable route: generate or pick a brand-consistent still first, then animate it. Start = end frame is also the simplest way to ask for a loop (see section 3).
- 9:16 is confirmed for Kling 3.0 and Runway Gen-4.5; for others it must be checked per endpoint. 720p models (Runway Gen-4.5) will be upscaled to 1080x1920, which is acceptable only if the plate is blurred/darkened.
- The Sora shutdown is a concrete reason to put the generator behind a thin adapter (e.g. fal.ai or Replicate model id + params in config) rather than coding to one vendor.
- Licence risk ranking for self-hosting: Wan (Apache-2.0) is clean; LTX-2 is free only under $10M revenue; HunyuanVideo's territorial exclusions (EU/UK/South Korea) make it unsuitable for teams or audiences there without legal review.

### Gaps
- Could not open fal.ai, Replicate, Kling, Google, Runway, Luma or MiniMax pricing pages directly; all prices above are via search summaries and several conflict.
- Hailuo/MiniMax: only unattributable aggregator numbers found (Hailuo 2.3 quoted as about $0.10/s at 1080p without audio, or $0.28 per 6 s at 768p and $0.49 per clip at 1080p; "MiniMax H3" appears on leaderboards). No primary source.
- Luma Ray3 API per-second price not found (one table implies about $0.21/s; another says per-clip pricing). No information on Ray3 loop support via API.
- Pika: no 2026 API spec, limits or pricing found.
- Commercial-use terms and visible-watermark behaviour of API output for Kling, Runway, Luma, Seedance, Hailuo were not found in primary sources. Whether these APIs embed C2PA metadata (which triggers automatic platform labels, see section 5) is unverified.
- Camera-control parameters exposed by the Kling 3.0 API (as opposed to prompt-level direction) not verified.
- No November 2026 dated leaderboard snapshot; "HappyHorse" and "Gemini Omni Flash" were not researched further.

## 2. AI image generators for still backdrops (Flux, Imagen, GPT Image, Midjourney, Ideogram, Seedream, Nano Banana)

### Takeaway
Still backdrops cost roughly $0.003-$0.15 per image via API, two orders of magnitude less than a video clip; the mid-priced band ($0.03-$0.06: FLUX.2 pro, Seedream 4.x/5, Ideogram 3, Imagen 4) is adequate for plates that will be darkened and blurred. Midjourney still has no official public API.

### Cited Findings
- October 2026 comparison of 30+ models lists Seedream 5.0 Pro at $0.045/image; Seedream 4.5 around $0.04 (third-party) — [movcl.com image API prices, Oct 2026](https://movcl.com/blog/comparisons/ai-image-api-prices-compared/)
- Reported per-image prices from aggregator pages (not verified on vendor rate cards; attribution to individual pages is approximate): GPT Image quality tiers about $0.009 low / $0.034 medium / $0.133 high, with budget variants from $0.002-$0.005; FLUX.2 [pro] $0.03-$0.055 (priced per megapixel); Nano Banana Pro $0.134 at 1K-2K and $0.24 at 4K direct from Google; Ideogram 3 $0.03 Turbo / $0.06 Default / $0.09 Quality; Imagen 4 Fast $0.02 / Standard $0.04 / Ultra $0.06, with one source saying Imagen 4 Standard was deprecated in Aug 2026 — [aiapiprices.com](https://aiapiprices.com/ai-image-api-pricing/); [buildmvpfast, July 2026](https://www.buildmvpfast.com/api-costs/ai-image); [Atlas Cloud model comparison](https://www.atlascloud.ai/blog/tips/best-ai-image-generation-models-2026)
- Midjourney: a September 2026 guide states there is no official public API; access is Discord and web app only, while aggregators (Apiframe, CometAPI, Atlas Cloud, EvoLink) resell unofficial access. V8.2 became the default on 24 Jul 2026 and its Edit Model replaces Omni Reference / Character Reference — [tech-insider Midjourney V8.1 guide](https://tech-insider.org/how-to-use-midjourney-v8-1-2026/); [Atlas Cloud Midjourney V8.2 style transfer](https://www.atlascloud.ai/models/midjourney/v8.2/style-transfer)
- Midjourney style consistency uses `--sref` (style reference) with `--sw` style weight, range 0-1000, default 100 (non-official source) — [Blake Crosley Midjourney guide](https://www.blakecrosley.com/guides/midjourney)

### Inferences
- Because Midjourney has no sanctioned API, using it in an automated pipeline means either manual export or an unofficial reseller that may breach Midjourney's terms; treat it as a manual "art direction" tool only.
- The cheapest robust pattern is: one still (about $0.03-$0.05) + Ken Burns / parallax / grain in the existing GSAP pipeline, reserving image-to-video for hero shots.
- Text-rendering strength (Ideogram, GPT Image, Nano Banana Pro are generally positioned on this) is irrelevant for backdrops, where the goal is no text in the plate; choose on price, 9:16 support and reference-image/style control instead.

### Gaps
- No primary-source confirmation of native 9:16 (e.g. 1080x1920 or 768x1344) output per model; must be checked per endpoint.
- Style-consistency mechanisms for FLUX.2 (multi-reference, LoRA), Nano Banana Pro (reference images), Seedream and Ideogram (style codes/references) were not retrieved; the search returned nothing usable.
- Commercial-use/licence terms per image model not researched (notably FLUX open-weights "dev" variants have historically been non-commercial; not re-verified for FLUX.2).
- All prices are from affiliate/aggregator blogs that conflict with each other.

## 3. Prompting and compositing best practice for backdrops behind text

### Takeaway
State the empty text zone, a single slow cyclical motion and a quiet energy level in the prompt, then enforce legibility in compositing with a scrim or uniform darkening tested against the brightest frame, not the average; loops need an explicit seam check.

### Cited Findings
- Name the negative space in the prompt (e.g. "negative space at the lower third"); each prompt should name a cyclical motion, a quiet energy level and the empty area the overlay needs — [Cliprise: AI seamless loop video](https://www.cliprise.app/learn/guides/best-practices/ai-seamless-loop-video)
- Keep the background simple enough that small camera drift does not expose clutter and reserve a text area (e.g. "left third reserved for headline") — [askai.fyi abstract gradient background prompt](https://askai.fyi/@askai/p/abstract-gradient-background)
- Most AI video generators leave the loop seam (last frame meeting first) to the user; review takes on repeat for the join and motion stability — [Cliprise](https://www.cliprise.app/learn/guides/best-practices/ai-seamless-loop-video)
- For procedural backgrounds, drive motion with periodic functions so time wraps with no visible jump, and verify the t=0 and t=period frames match — [motion-background agent skill](https://aiagentskills.net/skill/iart-ai-motion-design-skills-motion-background)
- Contrast over moving video must hold on every frame: test against the brightest background value in the text area, not the average; WCAG minimums cited are 4.5:1 for normal text and 3:1 for large text — [OpenDesign: text over moving backgrounds](https://open-design.ai/blog/text-over-moving-backgrounds/)
- A scrim is a gradient overlay that suppresses what is behind it so foreground text stays legible; do not stack several scrims to fake a gradient — [Meta Wearables design: Scrim](https://wearables.developer.meta.com/docs/develop/webapps/design/components/mrbd/scrim/)
- A gradient scrim fails when text spans the whole frame (text becomes unreadable part-way across); in that case darken the whole image uniformly — [Suleiman: text over background images](https://blog.iamsuleiman.com/techniques-to-display-text-overlay-background-images/)
- Generated signage/glyphs degrade into nonsense after camera movement, and forcing clips to loop can distort motion — [Luke Angel: local video models test](https://www.lukeangel.com/blog/local-video-models-scene-renders-verb-does-not/); [arXiv 2511.19474](https://arxiv.org/pdf/2511.19474)

### Inferences
- A reusable backdrop prompt skeleton: subject-free abstract or environmental scene + brand palette named as 2-3 hex/colour words + "soft, low contrast, shallow depth of field, out of focus" + one slow motion verb (drift, sway, slow push-in) + "locked-off camera" or a single camera move + explicit negative space position matching the caption safe zone + negatives ("no people, no faces, no text, no logos, no signage, no UI"). This is a synthesis of the findings above, not a quoted recipe.
- Loop strategies in order of reliability for this pipeline: (1) procedural/periodic backgrounds in CSS/WebGL (perfect loop by construction); (2) image-to-video with identical start and end frame (Kling supports start+end frame); (3) ffmpeg crossfade of the clip's tail into its head; (4) ping-pong (forward then reversed), acceptable only for non-directional motion like bokeh or fog.
- Since the pipeline composites in HTML, the scrim, blur (`filter: blur()` on the `<video>`/`<img>`), brightness/saturation reduction and a film-grain overlay can all be CSS layers above the plate; an automated check can sample the caption box region on each contact-sheet frame and compute worst-case contrast ratio.
- Palette consistency is easier to guarantee by post-processing (duotone/gradient-map or colour overlay in the brand hue with a blend mode) than by prompt alone.

### Gaps
- No authoritative, AI-video-specific standard for backdrop prompting was found; sources are vendor/marketing pages and general design blogs.
- No measured guidance on blur radius or darkening percentage for 9:16 captions at phone size; values need in-house testing.
- WCAG figures are from a secondary source, not checked against W3C text.

## 4. Cheap non-AI alternatives: stock APIs, procedural backdrops, Ken Burns

### Takeaway
Pexels (photos and video), Pixabay (photos and video) and Unsplash (photos only) all permit free commercial use without mandatory attribution but forbid standalone redistribution or building a competing library; Pexels is the de-facto B-roll source in open-source shorts generators.

### Cited Findings
- Pexels licence allows free commercial use without mandatory attribution, but not use in trademarks/logos or in ways implying endorsement; default API limit cited as 200 requests/hour and 20,000/month, raisable on request; Pexels has a video library — [laozhang.ai: free image APIs 2026](https://blog.laozhang.ai/en/posts/free-image-api); [OpenReplay: free stock photo resources](https://blog.openreplay.com/free-stock-photo-resources/)
- Pixabay licence permits free commercial use without attribution but prohibits redistribution as standalone files or in a competing library; API needs a key and covers images and video — [OpenReplay](https://blog.openreplay.com/free-stock-photo-resources/)
- Unsplash licence allows commercial use, prohibits unmodified resale and compiling a competing service; free API tier cited at 50 requests/hour; no video — [dev.to: Unsplash free API](https://dev.to/0012303/unsplash-has-a-free-api-get-professional-photos-for-any-project-50-requestshour-2d70)
- MoneyPrinterTurbo (MIT, 143.9k GitHub stars) sources materials from Pexels, Pixabay and Coverr plus local uploads, and now also AI video (MiniMax H3, Seedance, WaveSpeed) — [MoneyPrinterTurbo README](https://github.com/harry0703/MoneyPrinterTurbo)
- HyperFrames ships a catalog of about 450 reusable blocks (transitions, overlays, captions, charts, maps, effects) and a WebGL `@hyperframes/shader-transitions` package, i.e. procedural visuals in the same HTML+GSAP idiom — [HyperFrames repo](https://github.com/heygen-com/hyperframes)

### Inferences
- Procedural backdrops (CSS gradient meshes, animated `conic/radial-gradient`, canvas/WebGL shaders, particles, SVG noise grain) are free, on-palette by construction, loop perfectly, carry no AI-label or licence question, and render deterministically in the existing headless-Chromium pipeline as long as they are driven from the GSAP timeline time rather than wall-clock `requestAnimationFrame`.
- Ken Burns on a still (GSAP scale 1.0 to about 1.08 plus small x/y drift, optionally 2-3 parallax layers cut from the image) gives "video-like" motion at image cost and avoids video-decode sync problems during frame capture.
- Stock video has people and recognisable places; the "no endorsement" clause in Pexels' licence matters if clips with identifiable people sit behind product claims.

### Gaps
- Stock licence and rate-limit details are from secondary developer blogs, not the Pexels/Pixabay/Unsplash terms pages; Pixabay rate limit and video-specific terms not found.
- No sources were gathered on shader/gradient-mesh libraries or on Ken Burns technique; the points above are engineering judgement.

## 5. Platform rules on labelling AI-generated content (TikTok, Meta, YouTube)

### Takeaway
All three platforms key their disclosure duty on realism: realistic AI-generated people, places or events must be labelled, while clearly unrealistic/animated content and cosmetic effects need not be; but platforms now auto-label from C2PA metadata and detectors, and auto-applied labels can be permanent.

### Cited Findings
- YouTube: creators must disclose content that is meaningfully altered or synthetically generated when it seems realistic; beauty filters and special-effects filters such as background blur or vintage effects do not require disclosure; the list is not exhaustive — [YouTube Help: disclosing altered or synthetic content](https://support.google.com/youtube/answer/14328491)
- YouTube excludes clearly unrealistic content such as animation, and colour/lighting adjustments; YouTube may add a label itself, and repeated non-disclosure can lead to content removal or YouTube Partner Program suspension — [YouTube blog](https://blog.youtube/news-and-events/disclosing-ai-generated-content)
- From May 2026 YouTube also labels automatically when it detects significant photorealistic AI; creators can dispute except where the label is permanent (content made with YouTube's own Veo/Dream Screen tools, or carrying C2PA metadata marking it fully generative) — [The Next Web](https://thenextweb.com/news/youtube-will-now-automatically-label-ai-generated-videos-whether-creators-disclose-them-or-not)
- TikTok: a label is needed for content that uses AI to generate or significantly alter realistic depictions of people, places or events; TikTok may auto-apply the "AI-generated" label to content it identifies as fully generated or significantly edited, and the creator cannot remove an auto label; turning the label on is said not to affect distribution (secondary guides quoting TikTok) — [Magic Hour: TikTok AI labels checklist](https://magichour.ai/blog/tiktok-ai-generated-content-labels); [Hootsuite](https://blog.hootsuite.com/ai-disclosure-policy-for-tiktok/)
- TikTok reportedly has labelled more than 3 billion items as AI-generated, and undisclosed AI in ads can be rejected or restricted (secondary) — [Storrito](https://storrito.com/resources/tiktoks-2026-ai-labeling-rules-and-what-they-signal-for-platform-governance/)
- Meta: applies an "AI info" label when it detects AI-generated/edited media including via embedded metadata; from 1 Jun 2026 ads detected as using third-party AI show this in "About this ad"; a profile label for AI-generated people reportedly became mandatory on Instagram on 31 Aug 2026 (secondary sources, partly conflicting on self-declaration vs detection) — [Billo: platform AI labeling 2026](https://billo.app/blog/ai-labeling/); [Metricool](https://metricool.com/how-to-label-ai-content/)
- EU AI Act Article 50 transparency obligations apply from 2 Aug 2026 — [tianpan.co](https://tianpan.co/blog/2026-04-26-content-provenance-c2pa-synthid-audit-trail)

### Inferences
- An abstract, obviously non-photoreal AI backdrop (gradients, bokeh, stylised shapes) falls outside the "realistic" trigger on YouTube and TikTok as described; a photoreal AI city street or office behind a presenter is "a realistic place that does not exist" and should be labelled.
- If the generator embeds C2PA/SynthID (Veo does) and that metadata survives into the final MP4, the platform may attach a permanent AI label regardless of creator choice. Compositing through headless Chromium + ffmpeg re-encodes pixels and normally drops container-level C2PA manifests, but pixel-level watermarks such as SynthID are designed to survive re-encoding. The safe policy is to disclose rather than rely on stripping, and stripping provenance to avoid a label is not recommended.
- Simplest compliance rule for the pipeline: record per-project in config whether any AI-generated realistic imagery or AI voice is used, and surface a "turn on the AI label at upload" reminder in the QA checklist.

### Gaps
- TikTok and Meta official policy pages were not reachable; their rules above are from secondary guides which conflict on details (especially Meta).
- Whether AI voiceover (ElevenLabs) alone triggers the label on each platform was not established.
- No source addressed "AI backdrop behind a real presenter" explicitly.

## 6. Programmatic video frameworks (Remotion, HyperFrames, Motion Canvas, Revideo, Manim, Shotstack/Creatomate/JSON2Video, ffmpeg-only, headless-Chromium + GSAP)

### Takeaway
HyperFrames (HeyGen, Apache-2.0) is architecturally the same thing as this repo's pipeline — HTML/CSS/GSAP seeked frame-by-frame in headless Chrome and encoded with ffmpeg — and is the most direct source of techniques or a drop-in replacement; Remotion is the mature React alternative but needs a paid company licence above 3 employees.

### Cited Findings

**HyperFrames (HeyGen)**
- Apache-2.0; "Write HTML. Render video. Built for agents."; requires Node.js 22+ and FFmpeg; 84.9k GitHub stars, 7,331 commits (read 2026-11-16) — [HyperFrames repo](https://github.com/heygen-com/hyperframes)
- Rendering: Puppeteer-driven engine seeks each frame in headless Chrome, encodes with FFmpeg; same input produces the same video; a producer package handles capture, encoding and audio mixing — [HyperFrames repo](https://github.com/heygen-com/hyperframes)
- Pipeline chain: HTML composition → runtime injection → frame-adapter seek → `HeadlessExperimental.beginFrame` capture → ordered frame buffering → FFmpeg → MP4; the adapter pauses all GSAP timelines and seeks them to the computed time — [HyperFrames: determinism](https://hyperframes.heygen.com/concepts/determinism); [HeyGen research: HTML to video](https://www.heygen.com/research/html-to-video)
- Supported animation runtimes: GSAP, CSS animations, Lottie, Three.js, Anime.js, WAAPI, or a custom frame adapter — [HyperFrames repo](https://github.com/heygen-com/hyperframes)
- Declarative timing via data attributes: `data-composition-id`, `data-start`, `data-duration`, `data-width`, `data-height`, `data-track-index`, `data-volume`; audio is placed as `<audio>` elements and mixed at render time — [HyperFrames repo](https://github.com/heygen-com/hyperframes)
- CLI scaffolds, previews, lints, inspects and renders (`init`, `preview`, `render`, `add`, `catalog`, `skills update`); nine agent skills including `/hyperframes`, `/media-use`, `/reverse-any-video`, `/style-sampling`, `/remotion-to-hyperframes` — [HyperFrames repo](https://github.com/heygen-com/hyperframes)
- HeyGen's own comparison says HyperFrames is single-machine today whereas Remotion has Lambda distributed rendering; HeyGen claims agents produced more varied visuals in HTML+GSAP than in Remotion (self-reported) — [HyperFrames vs Remotion guide](https://hyperframes.heygen.com/guides/hyperframes-vs-remotion)
- Unverified third-party benchmark: 60 s vs 162 s render and 4 MB vs 14 MB output in HyperFrames' favour — [besthub.dev](https://www.besthub.dev/articles/hyperframes-vs-remotion-why-html-beats-react-for-ai-video-generation-98afba2b29d8)
- Reported pitfalls: `document.fonts.ready` hanging forever after seek is wired up; "HeadlessExperimental.beginFrame wasn't found" on Chromium 147+ — [jonblog HyperFrames write-up](https://jonblog.pages.dev/2026-04-26-hyperframes-html-to-video/); [skillselion HyperFrames skill listing](https://skillselion.com/skills/nousresearch/hermes-agent/hyperframes)

**Deterministic capture in headless Chrome (applies to the in-house pipeline)**
- `beginFrame` control and virtual time are not supported in "new headless" Chrome; they remain in the separate `chrome-headless-shell` binary — [Chromium headless-dev thread](https://groups.google.com/a/chromium.org/g/headless-dev/c/WgNE0CAlx-8)
- `puppeteer-capture` packages virtual-time shims with a beginFrame loop and notes that if chrome-headless-shell is discontinued, beginFrame goes with it — [puppeteer-capture README](https://cdn.jsdelivr.net/npm/puppeteer-capture@1.58.0/README.md)
- Replit's alternative avoids beginFrame: inject a virtual clock into the page, advance it, fire timers and requestAnimationFrame callbacks, then screenshot, repeat — [Replit: browsers don't want to be cameras](https://blog.replit.com/browsers-dont-want-to-be-cameras)

**Remotion**
- Licence (read directly): free for individuals, for-profit organisations with three or fewer employees, non-profits, and evaluation; everyone else needs a Company License; selling/relicensing derivatives is disallowed; licence will change slightly in Remotion 5.0 — [Remotion LICENSE.md](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md)
- Company licence pricing (search summary; sources conflict): official page cited at $100/month for the company tier and Enterprise from $500/month; third parties describe about $25 per developer seat/month with a $100 minimum, and an "Automators" tier at $0.01 per render with $100/month minimum — [Remotion licence page](https://remotion.dev/docs/license); [Wireflow: Remotion pricing](https://www.wireflow.ai/blog/remotion-pricing)
- `@remotion/captions` `createTikTokStyleCaptions()` segments word-level tokens into caption "pages"; `combineTokensWithinMilliseconds` controls how many words show at once (lower = more word-by-word); each page exposes token timings for highlighting the active word — [Remotion docs: createTikTokStyleCaptions](https://remotion.dev/docs/captions/create-tiktok-style-captions)
- Remotion provides an official TikTok-style captions template — [remotion-dev/template-tiktok](https://github.com/remotion-dev/template-tiktok)
- GSAP fits poorly in Remotion because Remotion re-renders React per frame while GSAP keeps its own clock (third-party analysis) — [moda.app: HyperFrames vs Remotion](https://moda.app/blog/hyperframes-vs-remotion)

**Motion Canvas / Revideo**
- Revideo is an MIT-licensed TypeScript fork of Motion Canvas that adds headless rendering from code, audio support and a library-first API; Motion Canvas (MIT) requires pressing a render button in its editor UI — [Revideo repo listing](https://awesome.ecosyste.ms/projects/github.com%2Fredotvideo%2Frevideo); [Remotion's Motion Canvas comparison](https://www.remotion.dev/docs/compare/motion-canvas)

**Hosted JSON-template render APIs** (all figures from competitor/affiliate blogs, Oct 2026)
- Shotstack: Starter $39/month for 250 minutes (about $0.16/min, 1080p max), Pro $99 for 750 min, Scale $199 for 2,000 min; other sources quote $0.20-$0.30/min — [Wireflow: Shotstack pricing](https://www.wireflow.ai/blog/shotstack-pricing)
- JSON2Video: 1 credit per second at any resolution; Startup $99.95 for 500 minutes — [Wireflow: JSON2Video pricing](https://www.wireflow.ai/blog/json2video-pricing)
- Creatomate: priced by pixels x frame rate x length, cheap at 720p and expensive at 1080p/4K — [Wireflow: Creatomate pricing](https://www.wireflow.ai/blog/creatomate-pricing)

### Inferences
- Features worth borrowing into the custom GSAP pipeline, in rough priority order: (1) a caption "paging" function equivalent to `createTikTokStyleCaptions` (group word timestamps into pages by a max-gap/max-chars rule, expose per-word start/end for highlight); (2) HyperFrames-style declarative `data-start`/`data-duration`/`data-track-index` attributes so an LLM writes timing as markup and a tiny runtime builds the master timeline; (3) a `lint`/`inspect` step before render (missing assets, overlapping tracks, text overflow, fonts not loaded); (4) audio as `<audio data-start data-volume>` elements mixed by ffmpeg from a manifest; (5) a block/catalog of pre-tested transitions and overlays; (6) an explicit font-readiness gate with timeout, since `document.fonts.ready` hangs are a known failure.
- Determinism checklist implied by the sources: never let wall-clock time drive anything; pause all timelines and `seek(frame / fps)`; wait for fonts, images and video frame decode before each screenshot; pin the Chrome build (chrome-headless-shell) because beginFrame availability changes across Chromium versions; if staying on plain `page.screenshot()` after a seek (simpler than beginFrame), CSS animations, `<video>` elements and WebGL canvases need their own seek adapters.
- Adopt-vs-borrow: because HyperFrames is Apache-2.0 and uses the same stack, the team can either migrate compositions to it (gaining lint, preview, catalog, agent skills) or copy specific ideas with no licence friction. Remotion would mean rewriting everything in React and, for a team of more than 3, a paid licence. Hosted JSON APIs (Shotstack etc.) trade design freedom for scale and are a poor fit for bespoke GSAP motion.
- Parallelising frame capture across several browser pages/processes by frame range and concatenating segments is the obvious speed-up for a seek-based renderer, since each frame is independent once rendering is deterministic.

### Gaps
- Manim and ffmpeg-only pipelines (drawtext/ASS subtitles, xfade, zoompan) were not researched; no sources gathered.
- Remotion `@remotion/transitions` and current Remotion version number not retrieved; Remotion pricing page not readable, figures conflict.
- No primary benchmark of render speed across frameworks; the one HyperFrames-vs-Remotion number is an unverified blog claim.
- HyperFrames release version/date not shown on the repo page captured; hyperframes.heygen.com docs were unreachable so details of its captions block and determinism rules come from search summaries.
- Shotstack/Creatomate/JSON2Video prices not checked on vendor pages.

## 7. Automated shorts pipelines and agents (script → TTS → timestamps → captions → B-roll → render), QA and failure modes

### Takeaway
Open-source generators converge on the same linear architecture (LLM script → TTS → timestamps from TTS or Whisper → stock search by LLM-generated keywords → ffmpeg/Remotion render); what distinguishes production pipelines is gating: machine checks per scene, a verifier model that can accept/regenerate/re-plan, scene-level retries, and a final human "would I publish this" gate.

### Cited Findings
- MoneyPrinterTurbo (MIT, 143.9k stars, read 2026-11-16): LLM writes the script (OpenAI, Claude, Gemini, DeepSeek, Ollama, etc.); TTS default is Edge TTS with ElevenLabs, Azure, Kokoro and others optional; subtitles either "edge" mode (uses TTS timestamps, fast, default) or "whisper" mode (local faster-whisper large-v3, about 3 GB, more accurate timing); materials from Pexels/Pixabay/Coverr or AI video; background music; ffmpeg; outputs 9:16 1080x1920, 16:9 and 1:1 — [MoneyPrinterTurbo README](https://github.com/harry0703/MoneyPrinterTurbo)
- gyoridavid/short-video-maker (MIT, TypeScript): Kokoro TTS + Whisper captions + Pexels footage + Remotion composition, exposed as REST API and MCP server; English-only TTS, Pexels-only footage — [short-video-maker on Docker Hub](https://hub.docker.com/r/gyoridavid/short-video-maker)
- cstrp/vml: FFmpeg + Whisper.cpp + Kokoro TTS + Pexels with a Nuxt front end — [cstrp/vml](https://github.com/cstrp/vml)
- A Colab pipeline uses Edge-TTS/gTTS for voice, WhisperX for alignment, MoviePy for karaoke-style rendering, Pexels for footage — [dev.to: AI-powered shorts generator](https://dev.to/ryanboscobanze/ai-powered-shorts-generator-building-automated-karaoke-style-video-pipelines-in-google-colab-480d)
- mutonby/openshorts: clip generator plus "AI Shorts" (UGC with AI actors) and YouTube tooling — [openshorts](https://github.com/mutonby/openshorts)
- Production lesson: machine checks cover shape, duration and state, but "would I publish this" needs a separate review gate; retry at scene level rather than rebuilding the whole video; stop the pipeline before an expensive render when earlier stages are bad — [dev.to: Stop AI video pipelines before a bad render gets expensive](https://dev.to/woshiliyana/stop-ai-video-pipelines-before-a-bad-render-gets-expensive-1p9m)
- Separate per-scene QA (wrong product, face drift, truncated clips) from cross-scene QA (character drift, pacing mismatch) — [Humza Tareen: AI video generation pipeline architecture](https://humzakt.github.io/blog/ai-video-generation-pipeline-architecture.html)
- Verifier-in-the-loop: CollabVR uses a VLM to check each generated clip and then accept, regenerate or re-plan based on a diagnosis — [arXiv 2605.08735](https://arxiv.org/pdf/2605.08735)
- Vision-model limits relevant to frame-review QA: small text in frames can be unreadable to the model, and video models recognise objects but miss motion, event order and timing; recommended practice is sampled frames with timestamps and scene segmentation — [Aman's AI Journal: VLM primer](https://aman.ai/primers/ai/VLM/)
- Replit/PostHog-style "freeze time and capture" renderers exist partly to feed frames/video back to multimodal models for review — [PostHog: multimodal models need video](https://posthog.com/blog/multimodal-models-need-video)

### Inferences
- The repo's existing contact-sheet step (`tools/frames.py`, `shorts.py sheet`) is the right primitive for vision-model review, with two caveats from the findings: crop/zoom caption regions rather than relying on a full-frame thumbnail (small text is unreliable for VLMs), and add deterministic non-vision checks for what VLMs are bad at — DOM-measured text overflow (`scrollWidth > clientWidth`), caption box inside platform safe zones, per-frame contrast under captions, caption-vs-audio offset from the timestamp file, clip duration vs audio duration, black/duplicate frame detection.
- Likely failure modes for this specific pipeline (synthesis of the above plus section 6): TTS normalising numbers/abbreviations so caption text and aligned text diverge; captions drifting if animation beats are hard-coded instead of read from timestamps; fonts not loaded at capture; AI backdrop containing garbled text/faces; loop seam visible; backdrop too bright under captions in a few frames; B-roll semantically wrong for the line; LLM "director" inventing numbers or UI labels (the project rules require real numbers and exact UI labels, so script facts should be validated against source data before TTS spend).
- Cost-ordering the gates (script lint → TTS → alignment sanity → low-res draft frames → vision review → full render → human gate) follows directly from the "stop before an expensive render" advice; AI video backdrops are the most expensive asset and should be generated only after the script and timing are locked, and cached by prompt hash.

### Gaps
- No rigorous, sourced catalogue of failure modes specific to caption drift/text overflow in automated shorts was found; the search returned general VLM and pipeline write-ups.
- No independent quality comparison of the open-source generators; star counts only.
- Details of how LLM "director" agents structure scene plans (JSON schemas, storyboard formats) were not retrieved beyond HyperFrames' skills list.

## 8. Voiceover timing: ElevenLabs timestamps and alternatives

### Takeaway
ElevenLabs returns character-level timings alongside audio from its `with-timestamps` TTS endpoints, and separately offers a Forced Alignment API (audio + known text → word and character timings); either gives exact caption/animation sync without a Whisper pass, with WhisperX or faster-whisper as the free local fallback.

### Cited Findings
- `POST /v1/text-to-speech/{voice_id}/with-timestamps` generates speech with precise character-level timing; a streaming variant `/stream/with-timestamps` exists — [ElevenLabs API: convert with timestamps](https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps.md); [ElevenLabs API: streaming with timestamps](https://elevenlabs.io/docs/api-reference/streaming-with-timestamps)
- Response contains base64 audio plus an `alignment` object and a `normalized_alignment` object (same data for the normalised text); official docs use arrays such as `character_start_times_seconds`; some third-party docs describe milliseconds, so units must be confirmed — [ElevenLabs API: streaming with timestamps](https://elevenlabs.io/docs/api-reference/streaming-with-timestamps); [tessl registry copy of SDK docs](https://tessl.io/registry/tessl/npm-elevenlabs--elevenlabs-js/2.24.0/files/docs/text-to-speech.md)
- A multi-speaker `/v1/text-to-dialogue/with-timestamps` endpoint also returns character-level alignment — [ElevenLabs API: text-to-dialogue with timestamps](https://elevenlabs.io/docs/api-reference/text-to-dialogue/convert-with-timestamps.md)
- ElevenLabs Forced Alignment takes audio plus text and returns a time-aligned transcript; priced the same as Speech-to-Text; max file 3 GB, max audio 10 hours, max text 675,000 characters; diarised input not supported — [ElevenLabs docs: forced alignment](https://elevenlabs.io/docs/overview/capabilities/forced-alignment)
- Forced-alignment output has word entries with start, end and an alignment "loss" value, plus character-level timings; also hosted on fal.ai and WaveSpeed — [WaveSpeed: ElevenLabs forced alignment](https://wavespeed.ai/docs/docs-api/elevenlabs/elevenlabs-forced-alignment); [fal.ai: ElevenLabs forced alignment](https://fal.ai/models/fal-ai/elevenlabs/forced-alignment/api)
- Pipecat ships a helper that derives word timestamps from ElevenLabs character alignment — [Pipecat ElevenLabs TTS reference](https://reference-server.pipecat.ai/en/latest/api/pipecat.services.elevenlabs.tts.html)
- Alternatives in the wild: Edge TTS emits its own timestamps (MoneyPrinterTurbo "edge" subtitle mode); faster-whisper large-v3 / large-v3-turbo locally; WhisperX for alignment — [MoneyPrinterTurbo README](https://github.com/harry0703/MoneyPrinterTurbo); [dev.to Colab pipeline](https://dev.to/ryanboscobanze/ai-powered-shorts-generator-building-automated-karaoke-style-video-pipelines-in-google-colab-480d)

### Inferences
- Best fit for `tools/vo.py`: call the `with-timestamps` endpoint, save audio plus a `words.json` built by collapsing characters into words on whitespace (keeping punctuation attached), and have GSAP read scene and caption beats from that file. Use `alignment` (original text) for captions so on-screen text equals the script, and keep `normalized_alignment` for debugging number/abbreviation expansion.
- Generating per caption/scene segment (rather than one long take) makes scene-level retries cheap and gives hard scene boundaries, at the cost of prosody continuity; ElevenLabs request-stitching parameters could mitigate this but were not researched.
- Forced Alignment is the tool when audio already exists (human presenter recordings for the presenter-style shorts, or re-timing after an audio edit); the per-word loss value is a usable QA signal for script/audio mismatch.
- Whisper-based transcription is a worse default than TTS-native timestamps when the script is known, because it can mis-transcribe brand terms and numbers and then captions no longer match the script; use it only for unscripted audio.

### Gaps
- ElevenLabs docs were unreachable directly; field names/units, which models support timestamps (e.g. Eleven v3), and the dollar rate for Forced Alignment/STT were not confirmed.
- No sourced comparison of alignment accuracy (ElevenLabs vs WhisperX vs Montreal Forced Aligner etc.), and other TTS vendors' timestamp support (OpenAI, Azure, Google, Cartesia) was not researched.
