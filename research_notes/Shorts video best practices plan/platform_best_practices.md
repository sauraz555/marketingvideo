# Short-form vertical video best practices (TikTok, Reels, Shorts) — state as of Nov 2026

> **Read this first — evidence quality.** Page fetching was blocked in this research session (every host, including support.google.com and ads.tiktok.com, failed DNS resolution), so **all findings below come from web-search result summaries, not from pages opened and read in full**. No official platform page was verified directly. Where a figure is attributed to an official doc (YouTube Help, Meta Ads Guide, TikTok In-Feed template, Google Ads), it is the official figure *as relayed by third-party sites or search snippets*. Almost all quantitative "retention uplift" claims in this field come from tool vendors with a commercial stake and no published methodology; they are labelled **[vendor, unverified]**. Claims without data are labelled **[opinion]**. Nothing cited here is older than 2024 unless flagged **[pre-2024]**.

## Hook: what works in the first 1-3 seconds

### Takeaway
The only quasi-official rule is TikTok's ad guidance: state the proposition in the first 3 s and land the hook within 6 s. No platform publishes organic retention curves, and every specific uplift number found (e.g. "+23%", "0.84 correlation") is vendor or single-creator data — encode the 3 s / 6 s structure as a default, not the percentages.

### Cited Findings
- TikTok's creative guidance (as relayed by third parties, not verified on TikTok's page): introduce the content proposition in the first 3 seconds (tied to recall/awareness) and prioritise the hook in the first 6 seconds (tied to engagement/watch time) — [Stackmatix](https://www.stackmatix.com/blog/tiktok-creative-best-practices-2026); [Sovran](https://sovran.ai/blog/tiktok-creative-best-practices)
- "63% of highest-performing TikTok ads capture attention / show the message within the first 3 seconds" is widely repeated; sources disagree on its origin, and one notes it describes ad creative, not organic video. Treat as ad-only and secondhand — [Soku](https://soku.ai/blog/ai-creative-guide-tiktok-ads); [mbadv](https://www.mbadv.agency/tiktok-ads/creative-best-practices)
- The "45% keep watching after 3 s" figure often attributed to TikTok is flagged by one source as originating from Facebook Business, not TikTok (likely [pre-2024]) — [Teleprompter.com](https://www.teleprompter.com/blog/tiktok-3-second-rule)
- Hook rate (3-second views / impressions) benchmarks for ads disagree: 20-25% "typical", 25-30% for short-form ads, or a 15-35% range — [Kickbite](https://www.kickbite.io/en/blog/hook-rate); [NestScale](https://nestscale.com/?p=47200)
- YouTube Shorts "viewed vs swiped away": YouTube publishes no universal threshold; third-party targets are 75-80% viewed, or tiers of <60% weak / 70-90% strong — [1of10](https://1of10.com/blog/youtube-shorts-analytics/); [Shortimize](https://www.shortimize.com/blog/youtube-shorts-retention-rate); [vidIQ](https://vidiq.com/blog/post/youtube-shorts-algorithm/) (vidIQ summary: retain at least ~60% of viewers past the first seconds)
- [vendor, unverified] Openings that target a specific pain point outperform generic openings by ~23% in retention ("2026 study", original not located) — [dev.to / bulkdl](https://dev.to/bulkdl/hook-engineering-the-science-of-the-first-3-seconds-in-short-form-video-2026-2jp9)
- [vendor, unverified] Videos with a pattern interrupt every ~4 s held 58% average retention vs 41% for static talking-head; source not named — [Joyspace](https://joyspace.ai/the-3-second-rule-science-stopping-scroll)
- [single creator, n=120 videos on 3 own accounts] 0.84 correlation between 3-second retention and total views; and a vendor claim that 70% retention at 3 s makes a video 8x more likely to reach 100k views (vendor's own clip data) — [Virlo](https://virlo.ai/blog/why-the-first-few-seconds-matter)
- Counter-view: the 3-second cutoff derives from an old TikTok "video watched" metric; optimise the whole arc, not only the opening — [Autoclip](https://autoclip.dev/blog/why-3-second-hooks-are-overrated)
- One guide says viewers may decide to scroll in ~1.5 s, shorter than the 3 s most sources assume [opinion, unsourced] — [tlinky](https://tlinky.com/3-second-hook/)
- Hooks must work muted: a significant share of viewers start with sound off (no official percentage found) — [Teleprompter.com](https://www.teleprompter.com/blog/tiktok-3-second-rule)
- TikTok guidance as relayed: when using on-screen text, 5-10 words per second [sic — as relayed; implausibly fast for reading, verify before using], and text overlays should give context — [Stackmatix](https://www.stackmatix.com/blog/tiktok-creative-best-practices-2026)

### Inferences
- Encodable defaults: (a) frame 0 must already show the subject plus a text hook — no logo sting, no fade from black; (b) the proposition/number/question is fully on screen by t <= 1.5 s and spoken by t <= 3.0 s; (c) a second "re-hook" or first payoff beat lands by t <= 6 s; (d) the hook is legible with sound off.
- For data-led content (visa/migration numbers, SaaS dashboards) the natural hook is a concrete number or a pain-point question, consistent with the (unverified) pain-point finding and the repo rule "real numbers only".
- Because the 1.5 s vs 3 s window is contested, the safer rule is to front-load to 1.5 s.

### Gaps
- No official TikTok, Meta or YouTube organic retention curve or hook benchmark was found; no peer-reviewed 2025-2026 study on short-form hooks was found.
- TikTok's official creative best-practice page could not be opened, so the 3 s / 6 s wording and the "63%" statistic are unverified at source.
- No data comparing visual hook vs text hook vs spoken hook in isolation.

## Pacing: cut cadence, total length, loops, CTA placement

### Takeaway
Best-supported length data: on TikTok (Socialinsider, millions of brand videos, H1 2026) engagement rate peaks at 15-30 s while median views rise with length up to 2-3 min; on Shorts one 16.5k-video analysis found 16-30 s strongest. Cut-cadence guidance (a visual change every ~2-4 s) is practitioner convention with only unverified vendor numbers behind it.

### Cited Findings
**Length — platform limits**
- YouTube Shorts: up to 3 minutes, square or vertical; limit took effect October 2024; Help article states square/vertical uploads up to three minutes are categorised as Shorts — [YouTube Help: Understand three-minute YouTube Shorts](https://support.google.com/youtube/answer/15424877?hl=en) (via search snippet)
- Instagram Reels: recording/editing up to 20 minutes per Help Center, but Reels over 3 minutes are reported as not recommended to new audiences — [AdCheckLab](https://adchecklab.com/articles/instagram-reels-safe-zone-template); [hanna-eng](https://www.hanna-eng.com/guides/format-reels-instagram/). One source claiming a 90 s default cap conflicts and is unreliable — [ScreenSnap](https://www.screensnap.pro/blog/instagram-reels-size-guide)
- TikTok: uploads up to 60 minutes, 10 minutes recorded in-app — [CreateSocial](https://createsocial.ai/blog/how-long-can-a-tiktok-be)

**Length — performance data**
- TikTok, Socialinsider 2026 (brand accounts ~1K-1M followers, Jan-Jun 2026; sample cited as "6M+" by some and 8,000,795 on Socialinsider's own pages — count unsettled): median views rise from ~1,000 (15-30 s) to ~11,136 (120-180 s), ~10,150 beyond 3 min; engagement rate is highest for 15-30 s at ~6.00%, all buckets fall in ~4.20-6.00%. Framing: ~30 s for engagement, ~2 min for views — [Socialinsider](https://www.socialinsider.io/blog/how-long-are-tiktok-videos/) as relayed by [SocialRails](https://socialrails.com/blog/best-tiktok-video-length-maximum-engagement) and [TTS Vibes](https://insights.ttsvibes.com/tiktok-rewatch-rate-statistics)
- TikTok, Fanpage Karma (~32,000 TikToks, one month): no universally optimal length; choose by goal (reach vs engagement) — [Fanpage Karma](https://www.fanpagekarma.com/insights/?p=15609)
- TikTok, Creafico benchmark of 24,373 videos (views, length, view dips, posting frequency) exists but its figures were not retrieved — [Creafico](https://www.creafico.com/research/tiktok-benchmark-2026)
- YouTube Shorts, OverseerOS (16,537 videos, 1-180 s, Oct 2026): 16-30 s had the strongest median performance; caveat: aspect ratio / Shorts-feed distribution not verified per video — [OverseerOS](https://www.overseeros.com/blog/best-youtube-shorts-length)
- YouTube Shorts, Adobe Express survey (507 creators with >=1,000 subs; self-reported preference, not measured): 34% favour <30 s, 34% favour 30-60 s — [Adobe Express](https://www.adobe.com/express/learn/blog/youtube-shorts-length-study)
- Conflicting: Joyspace recommends 50-58 s for Shorts (sample not shown) — [Joyspace](https://joyspace.ai/ideal-video-length-social-platform-2026); Toptal argues length alone has little to do with a Short going viral — [Toptal](https://www.toptal.com/creator/post/youtube-shorts-length)
- Revid.ai analysed 756,851 videos, but these are exports from its own tool, not a random platform sample — [Revid](https://www.revid.ai/blog/the-anatomy-of-a-viral-short-2026)
- Metricool publishes a 2026 short-form report across TikTok/Reels/Shorts; figures not retrieved — [Metricool](https://metricool.com/short-video-report/)
- Most short-form statistics circulate with no sample size attached — [Vidico](https://vidico.com/news/short-form-video-statistics/)

**Cut / visual-change cadence** (all practitioner or vendor)
- Rule of thumb: a visual change every 2-3 s; this need not be a hard cut (zoom, text overlay, B-roll, angle change all count) [opinion] — [Postiv](https://postiv-marketing.pages.dev/blog/social-media-video-editing-guide)
- Faceless Shorts guide: change image every 2-4 s; a 30 s Short should have 8-12 distinct scenes; any scene longer than 4 s gets a zoom/pan or a cut. Same guide: [vendor, unverified, "5,000 Shorts"] 82% retention at changes every 2-3 s, 71% at 4-5 s, 58% at 6+ s — [FluxNote](https://fluxnote.io/guides/faceless-shorts-retention-tips-2026)
- Faster claim: cuts every 0.5-1.5 s for TikTok/Reels, slightly longer for Shorts [opinion] — [BlitzCut](https://blitzcutai.com/blog/3-second-rule-tiktok-jump-cuts)
- Counter-evidence: more cuts do not guarantee retention; MrBeast's cuts fell from 38 to 23 per sampled minute (Mar 2023 → Mar 2024) while views rose (long-form, single channel) — [AIR Media-Tech](https://air.io/en/youtube-hacks/advanced-retention-editing-cutting-patterns-that-keep-viewers-past-minute-8)

**Loops and completion**
- Third-party Shorts targets: average percentage viewed ~80%+; one table lists 90%+ and "looping past 100%" for Shorts under 35 s and says loops count (single source, unverified) — [1of10](https://1of10.com/blog/youtube-shorts-analytics/); [Subscribr](https://subscribr.ai/p/youtube-shorts-analytics-metrics-growth)
- Rewatches may not count as extra engaged views but watch time still accumulates — [Agentio](https://www.agentio.com/blog/youtube-view-vs-engaged-view)

**CTA placement**
- Templates place the CTA last, after the teaching content ("Follow for more tips") [opinion] — [FreeAcademy](https://freeacademy.ai/lessons/short-form-video-strategy); [Kwiga](https://kwiga.com/blog/short-form-video-for-educators-turning-tiktok-and-reels-into-enrollment-machines)

### Inferences
- Default duration targets a pipeline could encode: primary 20-35 s (inside both the TikTok engagement peak of 15-30 s and the Shorts 16-30 s band); "deep" variant 60-120 s for TikTok reach; hard cap 180 s (Shorts classification and Reels recommendation limit both sit at 3 min).
- Default visual-change rule: no on-screen state static for more than ~3-4 s; target 8-12 scene beats per 30 s (mean 2.5-3.75 s); count GSAP zooms, highlight reveals and caption changes as changes, not only cuts. For data/UI screenshots, comprehension argues against the 0.5-1.5 s extreme.
- Loop rule: keep the final beat short (<= ~2 s CTA), no fade to black and no end card hold, and make the last frame visually/semantically lead into frame 0. This is inferred from loop/APV logic; no source measured it.
- CTA: one CTA, final 2-3 s, kept short so it does not depress completion; a soft mid-video CTA is not supported by any data found.

### Gaps
- No Reels-specific large-sample length study with numbers was retrieved (Metricool/Socialinsider Reels figures not accessible).
- No independent, methodologically disclosed study of cut cadence vs retention on short-form.
- No measured data on loopable endings or on CTA position (end vs middle vs caption-only).
- Socialinsider's exact sample size and whether views are medians or means differ between secondary sources.

## Captions: style, size, placement, readability, impact

### Takeaway
Burned-in captions are near-universal practice and plausibly help watch time, but the specific uplifts (12-40%) are vendor claims; the only rigorous number is a 2019 survey. Practitioner consensus for 1080x1920: bold sans, ~48-72 px (some say up to ~10% of frame height), 3-5 words per caption, white with black stroke, one highlight colour, text width <= 80-85% of frame.

### Cited Findings
**Impact**
- [pre-2024, possibly outdated] Verizon Media/Publicis 2019 survey of 5,616 US adults: 80% said they were more likely to watch a video to completion when captions are available (captions in general, self-reported) — relayed by [Kapwing](https://www.kapwing.com/resources/how-many-people-use-subtitles-in-2026-2/)
- [vendor, unverified] Word-by-word colour-emphasis captions +34% watch time vs plain auto-captions (7 styles, 80 short videos, internal test, no methodology) — [FluxNote](https://fluxnote.io/blog/ai-captions-that-improve-watch-time)
- [vendor, unverified] Generic captions: +15-25% or +12-25% average watch time; "closed captions increase watch time by 17% on TikTok"; animated vs static +10-20% from unpublished creator tests — [ClipSpeed](https://clipspeed.ai/blog/ai-captions-increase-views.html); [BlitzCut](https://blitzcutai.com/blog/animated-captions-vs-static-captions); [dev.to / clamper](https://dev.to/clamper_ai/how-ai-caption-styles-affect-watch-time-and-engagement-409i). Another source says the animated-vs-static advantage is only theorised — [ClipSpeed](https://www.clipspeed.ai/blog/subtitles-vs-captions-which-better.html)
- Widely repeated premise: 70-85% of short-form social video is watched with sound off or low (no primary source located) — [VoxBooster](https://voxbooster.com/blog/short-form-video-caption-usage-statistics-2026)
- Academic: a 2023 arXiv study found time-synchronised word highlighting improved comprehension for language learners (comprehension, not feed watch time) [pre-2024] — relayed via [dev.to / clamper](https://dev.to/clamper_ai/how-ai-caption-styles-affect-watch-time-and-engagement-409i)

**Size at 1080x1920**
- 48-70 px depending on style; floor 48 px; over 72 px crowds the safe zone — [BlitzCut (Shorts)](https://blitzcutai.com/blog/best-caption-size-youtube-shorts-2026); [BlitzCut (TikTok)](https://blitzcutai.com/blog/best-caption-size-tiktok-2026)
- 55-65 px for full-sentence Shorts captions; 40-60 px cited for 5-inch screens — [OpusClip](https://www.opus.pro/blog/youtube-shorts-caption-subtitle-best-practices); [BlitzCut](https://blitzcutai.com/blog/best-caption-size-youtube-shorts-2026)
- Larger school: 7-10% of frame height (~134-192 px line box at 1920), "if unsure it is almost certainly too small" — [OpenClip](https://openclip.app/guides/caption-styling-guide); [ClipSpeed](https://www.clipspeed.ai/blog/best-fonts-for-captions.html)
- Common preset: weight 700-900, 60-75 px, black outline; 3-4 px black stroke on white text — [BlitzCut](https://blitzcutai.com/blog/how-to-make-captions-look-professional); [Subclip](https://subclip.app/blogs/subtitle-styles-that-convert)

**Words / characters**
- Word-group (karaoke) style: 3-5 words per caption segment is the "sweet spot"; short-phrase style 3-7 words per frame — [OpenClip](https://openclip.app/guides/caption-styling-guide); [Subclip](https://subclip.app/blogs/animated-captions-2026-best-practices-reels-shorts-x-exporting-srt)
- Sentence style: 32-42 characters per line (~5-7 words); keep text width to 80-85% of frame width — [Pictory](https://pictory.ai/blog/tiktok-captions); [OpusClip](https://www.opus.pro/blog/youtube-shorts-caption-subtitle-best-practices)

**Accessibility**
- WCAG: contrast >= 4.5:1 for regular text, >= 3:1 for large text (18 pt regular / 14 pt bold); WCAG does not prefer any font; stroke/box advice is convention, not WCAG — [VEED](https://www.veed.io/video-accessibility/which-subtitle-font-is-best)

**Placement**
- Cross-platform guidance: keep captions roughly between y=220 and y=1440, or inside a centred 900x1400 box — [reap.video](https://reap.video/blog/short-form-video-safe-zones); [AdaptlyPost](https://adaptlypost.com/blog/social-media-safe-zones-2026-complete-guide) (see safe-zone section for conflicts)

### Inferences
- Encodable caption defaults: bold sans (700-900); 64 px minimum for word-group captions, up to ~96 px for 1-3-word emphasis style; 3-5 words per caption (max 2 lines, <= 42 chars/line for phrase style); max text width 864-918 px (80-85% of 1080); white fill + 3-4 px black stroke (scale stroke ~5-6% of font size) and/or soft shadow; exactly one highlight colour for the active/key word; contrast check >= 4.5:1 against the worst-case backdrop (or use a semi-opaque box).
- At 150-165 wpm (2.5-2.75 words/s) a 3-5 word caption stays up ~1.1-2.0 s, which also satisfies the 2-4 s visual-change rule on its own.
- Phrase captions vs word-by-word: no independent data settles it. For number-dense explainer content, phrase groups with a highlighted key word/number are the lower-risk default (keeps numbers and UI labels intact on one caption — consistent with the repo's "exact UI labels" rule); pure one-word-at-a-time is unsupported by any verified measurement.
- Caption vertical position should be driven by the common safe area (below), i.e. captions in the lower-middle band, not the bottom third.

### Gaps
- No independent, published A/B test of word-by-word vs phrase captions on any platform.
- No official platform guidance on caption font size in px was found.
- The "sound-off" share for TikTok/Reels/Shorts in 2025-2026 has no located primary source.
- The size recommendations span roughly 2x (48 px vs ~10% of frame height); needs an on-device test.

## Safe zones at 1080x1920

### Takeaway
Platforms publish safe zones for ads only, and third-party organic figures conflict. Taking the most conservative published ad margins gives a universal safe box of about x 120-888, y 288-1248 (768x960); a looser organic working area used by several guides is ~900x1400 centred. Critical text (captions, numbers) should live in the strict box.

### Cited Findings
- YouTube Shorts (Google vertical video ad guidance, as relayed): 288 px top, 672 px bottom, 48 px left, 192 px right; described as the only pixel figures Google publishes for Shorts — [BreakReach](https://www.breakreach.com/tools/safe-zone-checker); [Takes](https://gettakes.app/short-video-specs)
- Instagram Reels (Meta Ads Guide, as relayed): 14% top, 35% bottom, 6% each side for ads; Meta publishes no organic safe zone — [BeReel](https://www.bereel.pro/blog/instagram-reels-size-dimensions-safe-zones). Third-party measurement of organic Reels: ~13% top, ~16.6% bottom — [AdCheckLab](https://adchecklab.com/articles/instagram-reels-safe-zone-template). Another guide: 210 px top, 310 px bottom; "most conservative" 996x1400 centred for feed + Explore — [PostPlanify](https://postplanify.com/blog/social-media-safe-zones-2026-complete-guide)
- TikTok (In-Feed ad template, drawn at 720x1280 and scaled, as relayed; TikTok provides it only as a downloadable template, no numbers in text): ~240 px top, ~660 px bottom, ~120 px each side; button column on the right from ~840 px down (width given as 180 px by some, 300 px by one) — [Upload-Post](https://www.upload-post.com/tools/safe-zone-checker/); [ToolsWebPro](https://www.toolswebpro.com/guides/tiktok-reels-shorts-safe-zones-2026); [BlitzReels](https://blitzreels.com/glossary/safe-zone)
- TikTok conflicting figures: top 130 / bottom 320 / right 140 (organic) with 480 px bottom for ads in the same tool; bottom 320 / right 120 in another; safe box 900x1442 (ads) vs 900x1492 (organic) in another — [Uplads](https://uplads.com/tools/safe-zone-checker); [AdaptlyPost](https://adaptlypost.com/blog/social-media-safe-zones-2026-complete-guide); [PostPlanify](https://postplanify.com/blog/social-media-safe-zones-2026-complete-guide)
- Cross-platform suggestions: 900x1400 centred in 1080x1920; or keep content between y=220 and y=1440 — [AdaptlyPost](https://adaptlypost.com/blog/social-media-safe-zones-2026-complete-guide); [reap.video](https://reap.video/blog/short-form-video-safe-zones)
- Instagram grid/feed crops: profile grid shows the middle 1080x1440 (3:4); another source describes a central band surviving the 4:5 feed crop and square grid (sources disagree) — [BreakReach](https://www.breakreach.com/guides/instagram-reel-size); [InVideo](https://invideo.io/blog/instagram-reel-size-guide/)
- Platforms publish safe zones for ads only; overlays change over time; check with in-app preview — [Viberoll](https://viberoll.questera.ai/learn/short-form-video-specs/)

### Inferences
- Converting Meta's percentages: 14% x 1920 = 269 px top; 35% x 1920 = 672 px bottom; 6% x 1080 = 65 px each side.
- **Strict common safe box (max of every published ad margin)**: top 288 (Shorts), bottom 672 (Shorts/Reels), left 120 (TikTok), right 192 (Shorts) → x 120-888, y 288-1248, i.e. 768x960 px. Use for captions, key numbers, CTA text.
- **Relaxed organic working box**: ~900x1400 centred (x 90-990, y 260-1660). Use for non-critical visuals (charts, screenshots, presenter); note its lower ~400 px overlaps ad-safe bottom margins and the TikTok/Shorts right rail, so nothing essential on the right edge below y≈840.
- Ad bottom margins (660-672 px) are larger than organic overlays because ads carry CTA buttons/cards; organic bottom overlays (username, description, audio) are roughly 310-480 px per the third-party figures. A two-tier config (strict vs organic) lets the pipeline choose per use case.
- Keep the hook title inside the middle 1080x1440 so it survives the Instagram 3:4 grid crop, and make the cover frame readable in that crop.

### Gaps
- None of the official templates (TikTok In-Feed template, Meta Ads Guide, Google Ads spec) could be opened; all pixel values are secondhand and should be verified against the official downloads before being hard-coded.
- No official organic safe zone exists for any of the three platforms.
- TikTok's right-rail width (180 vs 300 px) and organic bottom margin (320 vs 480 px) are unresolved.

## Technical export specs

### Takeaway
Safe universal master: 1080x1920, 9:16, MP4, H.264 + AAC, 30 fps, and a bitrate at or above YouTube's official 8 Mbps for 1080p30 (practitioners use 10-20 Mbps since every platform re-encodes), audio ~-14 LUFS integrated with -1 dBTP true peak. Only YouTube's bitrate/audio numbers are from an official doc (via snippet); the loudness target is convention, not a published TikTok/Meta spec.

### Cited Findings
- 1080x1920 at 9:16 is the standard master for all three; Reels minimum width 720 px — [Moonb](https://www.moonb.io/blog/vertical-video-dimensions); [Hopper HQ](https://www.hopperhq.com/blog/instagram-reel-size/)
- YouTube official recommended upload settings (via search snippet): MP4 container; variable bitrate, no bitrate limit required; 1080p SDR 8 Mbps at 24/25/30 fps and 12 Mbps at 48/50/60 fps (10 / 15 Mbps appear to be the HDR values); audio 128 kbps mono, 384 kbps stereo, 512 kbps 5.1. Third-party guides add H.264 High Profile and AAC-LC 48 kHz from the same page (not confirmed in the snippet) — [YouTube Help](https://support.google.com/youtube/answer/1722171?hl=en); [Compresto](https://compresto.app/blog/best-video-format-for-youtube)
- Codec: documented figures exist for Reels and TikTok as H.264 with AAC; complete official codec/fps figures for Reels and Shorts are scarce — [blckalpaca](https://blckalpaca.at/en/knowledge-base/social-media/social-media-content-creation-formats/instagram-reels-format-shorts-tiktok-specs)
- Bitrate recommendations vary (practitioner starting points, not platform limits): VBR 15-20 Mbps; TikTok master 16-20 Mbps; 6-8 Mbps — [ThePostFlow](https://thepostflow.com/post-production/post-production-workflows/export-settings-youtube-instagram-tiktok/); [CrePal](https://crepal.ai/blog/aivideo/blog-seedance-2-0-export-settings-tiktok-reels-shorts/); [Filmora](https://filmora.wondershare.com/trending-tech/what-is-tiktok-video-specs.html)
- Frame rate: 30 fps default; use 60 fps only if the source was 60 or motion benefits — [Nemo Video](https://www.nemovideo.com/blog/best-capcut-export-settings-shorts)
- Loudness: most sources favour about -14 LUFS integrated, true peak ~-1 dBTP (TikTok); another gives -14 to -16 LUFS; one outlier suggests -10 to -12 LUFS for TikTok/Reels — [ThePostFlow](https://thepostflow.com/post-production/post-production-workflows/export-settings-youtube-instagram-tiktok/); [ConvertIntoMP4](https://convertintomp4.com/blog/best-video-format-social-media-2026); outlier: [skills.lc ffmpeg skill](https://www.skills.lc/JosiahSiegel/claude-plugin-marketplace/josiahsiegel-claude-plugin-marketplace-plugins-ffmpeg-master-skills-viral-video-platform-specs-skill-md)

### Inferences
- Encodable render default: `1080x1920, 30 fps, H.264 High, yuv420p, MP4 (+faststart), AAC-LC 48 kHz stereo`, video 10-16 Mbps VBR (above YouTube's 8 Mbps floor, giving headroom for platform re-encoding of flat UI graphics and fine text), audio 256-384 kbps.
- GSAP animation rendered frame-by-frame should be authored for 30 fps; 60 fps doubles render time and bitrate needs with no platform requirement.
- Loudness default: normalise the final mix to -14 LUFS integrated, -1 dBTP (two-pass `loudnorm`), since it matches YouTube's known normalisation reference and the majority view for TikTok/Reels.
- Screenshot-based content with small text is the worst case for re-encoding; larger type and higher source bitrate matter more than exact codec flags.

### Gaps
- No official TikTok or Instagram organic-upload bitrate, codec-profile or loudness specification was found or verified.
- No official statement that TikTok or Instagram loudness-normalise uploads; -14 LUFS is convention.
- HEVC/AV1 upload benefits on these platforms were not researched.

## Audio: voiceover pacing, music ducking, sound effects

### Takeaway
Voiceover at roughly 150-165 wpm (ceiling ~180) with the music bed ~18-24 dB below the voice is the consistent practitioner guidance; all of it is vendor convention, none measured against retention.

### Cited Findings
- Narration pace: typical speech ~150 wpm; 130-160 wpm standard range for comprehension; slower for detail-heavy narration — [Moonb](https://www.moonb.io/blog/how-to-voice-over-videos); [Syllaby](https://syllaby.io/blog/voiceover-pacing-silence-trimming-retention-editing/)
- TikTok-specific: 155-170 wpm for rapid pacing; 150-165 wpm for casual conversational; above ~180 wpm linked to listening fatigue and drop-off [opinion] — [Cliprise](https://cliprise.app/learn/workflows/marketing/ai-video-ai-voice-social-media-workflow); [NarrationBox](https://narrationbox.com/blog/how-to-do-ai-voiceover-for-tiktok-2025-updated)
- Static music level under narration: -18 to -24 dB below the voice; or -18 to -25 dB; one CapCut workflow: voice 0 dB reference, SFX -8 dB, music -15 dB — [OverseerOS](https://www.overseeros.com/blog/background-music-volume-under-voiceover); [VidPros](https://vidpros.com/fix-background-music-too-loud-video/); [Cursa](https://cursa.app/en/page/audio-enhancements-in-capcut-clean-voice-music-balance-and-sound-effects)
- Dynamic ducking: start at 6-12 dB reduction, attack 30-80 ms, release 250-700 ms; over-ducking 15-20 dB on every line sounds clumsy in short-form; one guide suggests only 2-4 dB — [CapCut](https://www.capcut.com/create/audio-ducking-for-clear-dialogue-in-video); [Nemo Video](https://www.nemovideo.com/blog/ai-video-models/yue2-video-soundtrack)
- Audio-led cutting (cut on the waveform, let the next line overlap slightly) and trimming silences are standard retention-editing techniques [opinion] — [Syllaby](https://syllaby.io/blog/voiceover-pacing-silence-trimming-retention-editing/); [AIR Media-Tech](https://air.io/en/youtube-glossary/what-is-retention-editing)

### Inferences
- Script-length budget: at 155 wpm ≈ 2.6 words/s → ~75-80 words for 30 s, ~155 words for 60 s; cap ElevenLabs output at ~170 wpm and trim inter-sentence silences to ~150-250 ms.
- For number-dense migration/visa content, sit at the lower end (145-155 wpm) and let numbers land on a caption highlight; speed alone is not supported by any data.
- Mix defaults: voice as reference, music bed -18 to -20 dB relative to voice (or sidechain duck 8-10 dB, attack ~50 ms, release ~400 ms), SFX ~-8 to -12 dB relative to voice, then normalise the whole mix to -14 LUFS / -1 dBTP.
- Transition SFX (whoosh/tick on scene change, soft pop on number reveal) are convention only; keep them subtle and optional.

### Gaps
- No measured data linking voiceover wpm, music presence, or transition SFX to retention on short-form.
- No platform guidance on music vs voice balance; no data on AI voice vs human voice performance was researched.
- Sound-effects guidance specifically was not found in any source with data.

## Structure templates for educational / explainer shorts

### Takeaway
Sources converge on a single-idea arc: hook (0-3 s) → value/steps → proof or payoff → short end CTA. This is practitioner consensus without measured comparisons between templates.

### Cited Findings
- Three-part pattern hook → body → payoff, same template for TikTok, Reels and Shorts; educational hook is typically a claim-style opener [opinion] — [Socialync](https://www.socialync.io/blog/short-form-video-structure-guide-2026)
- Four-step educator variant: hook → value → proof → CTA; hook opens with a thought-provoking claim, question or pain point [opinion] — [Kwiga](https://kwiga.com/blog/short-form-video-for-educators-turning-tiktok-and-reels-into-enrollment-machines)
- Template with CTA last: hook → problem → "the better way in 3 steps" → CTA ("Follow for more tips") [opinion] — [FreeAcademy](https://freeacademy.ai/lessons/short-form-video-strategy)
- One idea per short: one idea, one hook, one payoff, then stop; each educational Short answers one focused question [opinion] — [Eliro](https://eliro.pro/blog/short-form-video-hooks-script-guide-2026); [OpusClip](https://www.opus.pro/blog/ideal-youtube-shorts-length-format-retention)
- Product explainers: keep to 60 s or less [opinion] — [Zubtitle](https://zubtitle.com/blog/unlock-your-product-the-short-form-explainer-video-guide)
- TikTok ad guidance (relayed): proposition in first 3 s, hook within 6 s — [Stackmatix](https://www.stackmatix.com/blog/tiktok-creative-best-practices-2026)

### Inferences
- A segment schema the pipeline could encode for a ~30 s short (timings derived by combining the 3 s / 6 s rule, the 2-4 s beat cadence and the 15-30 s length band — not from any single source):
  1. **Hook** 0.0-3.0 s — number/claim/question on screen at frame 0, spoken by 3 s (~7-8 words).
  2. **Context / stakes** 3-7 s — who this matters to; first payoff tease by 6 s.
  3. **Value** 7-20 s — 2-3 beats of 3-5 s each (one fact, step or UI highlight per beat).
  4. **Proof** 20-26 s — the real number, source label or screenshot evidence.
  5. **Payoff + CTA** 26-30 s — one-line takeaway, CTA <= 2 s, last frame leading back into the hook for the loop.
- 60 s variant: same arc with 5-7 value beats; insert a re-hook ("but here's the catch") around the midpoint, since retention sources recommend pattern interrupts but give no verified interval.
- Alternative templates worth offering as presets: "Myth → Truth → Proof → CTA", "Question → Answer first → Why → CTA" (answer-first suits search-style queries such as visa processing times), "Number → What it means → What to do".

### Gaps
- No data comparing structure templates against each other; no source measured answer-first vs suspense-payoff for educational content.
- Nothing found specific to regulated/advice-adjacent topics (migration/visa) such as disclaimer placement or platform policy constraints.
- No verified guidance on series/episodic formats or on presenter vs faceless performance for explainer content.
