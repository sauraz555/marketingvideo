# Motion graphics techniques and data/comparison representation for 9:16 short-form video (state as of Nov 2026)

Research-method note for the report writer: page fetches were blocked in this session for every host tried (gsap.com, flourish.studio, onlinejournalismblog.com, grid.uns.ac.rs), so all cited findings below come from search-result extracts of those pages, not full-page reads. Where a number is from a vendor blog with no published method it is labelled "vendor, unverified". Everything under "Inferences" is my own synthesis or a suggested implementation default (opinion), not a sourced fact. Frame assumed throughout: 1080x1920 px, 30 fps.

## 1. Comparisons: how A-vs-B is shown in vertical video, and which treatments work best on a phone

### Takeaway
In 9:16 the default comparison layout is a top/bottom (stacked) split rather than side-by-side, because each half keeps the full 1080 px width; side-by-side halves are only 540 px wide and become unreadable once panels shrink. Research on animated versus static comparison is mixed: animation helps viewers track a change between two states, but static side-by-side "small multiples" beat animation for accuracy, so the safest pattern is to animate the transition and then hold both states on screen together.

### Cited Findings
- Creators are moving away from the traditional side-by-side split in vertical video and instead use a horizontal divide, giving a top-and-bottom layout — [Adweek](https://www.adweek.com/sponsored/the-worlds-most-creative-people-show-you-how-to-master-vertical-video/)
- Top-and-bottom suits moments when the viewer must see two parts of one action at the same time; split screens work best timed to a hook, reveal or comparison point, and can appear immediately for a direct comparison or enter after context is set — [CapCut](https://www.capcut.com/create/split-screen-effects-multi-frame-videos)
- A split layout can look balanced in the editor and still be indecipherable once each panel is reduced; check on an actual phone — [ShortGenius](https://shortgenius.com/blog/split-screen-video-editing)
- For bar charts with more than four or five categories, go vertical in layout (i.e. stack horizontal bars down the page), per the WSJ graphics editor's advice reported for mobile — [Better News](https://betternews.org/making-data-visualizations-interactives-work-well-mobile/)
- Use horizontal bars when category labels are long — [Flourish](https://flourish.studio/blog/social-media-charts-and-graphs/)
- Heer and Robertson (InfoVis 2007) ran two controlled experiments on transitions between bar charts, pie charts and scatter plots and found animated transitions can significantly improve graphical perception, with significant advantages over static transitions for object tracking and value estimation — [UW Interactive Data Lab](https://idl.uw.edu/papers/animated-transitions)
- Their design guidance as summarised in UW course slides: use staging for complex transitions (simple stages), minimise occlusion, and make transitions as long as needed but no longer — [UW CSE442 slides](https://courses.cs.washington.edu/courses/cse442/24au/lectures/CSE442-Animation.pdf)
- A later study (Robertson et al., InfoVis 2008, as summarised in the same lecture slides): small multiples were 10% more accurate than animation for comprehension questions, animation was 82% slower than multiples for analysis, yet users preferred animation. Secondary summary; verify against the paper before quoting — [UW CSE442 slides](https://courses.cs.washington.edu/courses/cse442/18au/lectures/CSE442-Animation.pdf)
- Transition strategies for animated bar charts specifically (the bar-chart-race family) "have not been fully explored", unlike scatterplot transitions — [Visual Intelligence, 2023](https://link.springer.com/10.1007/s44267-023-00015-w)
- In video, a vertical wipe can be used on bar charts and histograms to create the effect of bars growing upwards or outwards, and chart elements that are narrated or that animation adds later can be removed from the initial chart — [Online Journalism Blog, June 2026](https://onlinejournalismblog.com/2026/06/23/showing-charts-on-video-here-are-two-essential-techniques-to-make-them-effective/)
- Complex chart types are a poor fit for social: "not the time or place for a multi-level Sankey or ten-category chord diagram" — [Flourish](https://flourish.studio/blog/social-media-charts-and-graphs/)

### Inferences
All of the following are opinion / suggested component defaults derived from the findings above, the safe-zone figures in section 6 and the reading-speed figures in section 2.

Ranking of comparison treatments for a phone screen (best first), with reasoning:
1. **Two stacked horizontal bars with direct value labels** (A above B). Uses the full width, needs no legend, and length comparison on a shared baseline is the easiest judgement. Best when the point is "how much bigger".
2. **Top/bottom versus cards.** Each card is about 960 px wide x 600-650 px tall inside the safe area, with a "VS" chip on the divider. Best for qualitative or 2-3 attribute comparisons.
3. **Tick/cross checklist that builds row by row.** Works because it is segmented (one row per narrated beat). Cap at 4-5 rows.
4. **Before/after wipe** on a single image or screenshot. Best for the same object in two states; a vertical-moving (top-to-bottom) or horizontal divider both work, but keep labels "Before" / "After" pinned in opposite corners.
5. **Table that builds row by row.** Maximum 2 value columns plus a label column and 4-5 rows; anything larger should be split across scenes.
6. **Ranking / bar chart race.** Use for a "who overtook whom" story only. The research above suggests animation is preferred by viewers but is less accurate than static views, so end on a held final frame with labels and limit to 5-6 bars.
7. **Side-by-side (left/right) panels.** Weakest in 9:16 because each panel is at most about 460 px wide after gutters; acceptable only for two tall objects (two phones, two people).

Suggested GSAP component specs (30 fps, opinion):
- **VersusCards:** card A slides in from y:+80 px with opacity 0 to 1, 0.5 s, `power3.out`; card B the same 0.15 s later; "VS" chip scales 0 to 1, 0.35 s, `back.out(1.7)` at +0.3 s. On the verdict beat the winner scales to 1.04 and the loser dims to 40-50% opacity over 0.3 s, `power2.out`. Hold the verdict frame at least 1.5 s.
- **StackedBars (A vs B):** bar height 96-120 px, gap 48 px, label above bar at 44-52 px, value at bar end at 64-80 px bold. Bars grow with `scaleX` from 0, transform-origin left, 0.8 s, `power3.out`, stagger 0.2 s; value counter runs in sync with its bar. Hold 2 s after the last value lands.
- **Checklist:** rows 120-140 px tall; each row fades/slides in (x:-40 to 0, 0.35 s, `power2.out`), then its tick or cross pops (scale 0 to 1, 0.3 s, `back.out(2)`) 0.1 s later. One row per narration beat rather than a fixed stagger; if not narrated, 0.6-0.8 s between rows.
- **BeforeAfterWipe:** animate a `clip-path: inset()` on the "after" layer plus a 6 px divider line, 0.9-1.2 s, `power2.inOut`; hold each state at least 1 s before and after the wipe.
- **RowBuildTable:** header fades first (0.3 s), rows rise 24 px with opacity, 0.35 s, `power2.out`, stagger 0.25-0.4 s; highlight the differing cell with a background sweep (0.4 s) after the full table is built.
- **Rank race:** animate `y` position swaps over 0.6-0.8 s `power2.inOut` per step with at least 0.5 s pause between steps; never run steps back-to-back without pauses (staging principle).

### Gaps
- No controlled study was found that compares top/bottom versus side-by-side comparison layouts in vertical video, or that tests before/after wipes; the layout ranking above is practitioner opinion plus pixel arithmetic.
- No direct, sourced critique of bar chart races was retrieved (one search only); the caution is inferred from the Robertson et al. 2008 result on animated trends.
- The Online Journalism Blog and Flourish pages could not be opened in full, so named examples and any further numbers in them are missing.

## 2. Data representation: counters, charts, rings, pictograms, maps, timelines, stat cards; how much fits and how long it must stay

### Takeaway
Practitioner guidance for charts in video converges on radical simplification: one message per chart, bigger text than a web chart, direct labels instead of axes and legends, and letting narration or animation carry what you remove. No source gives a hard "data points per screen" number beyond the 4-5 category rule for bars; dwell time is best derived from subtitle reading-speed standards (about 17 characters per second / 200 words per minute for adults).

### Cited Findings
- For video, use bigger fonts than a normal online chart and replace y-axis scales with direct labels; elements that are narrated or added later by animation can be removed from the chart — [Online Journalism Blog, June 2026](https://onlinejournalismblog.com/2026/06/23/showing-charts-on-video-here-are-two-essential-techniques-to-make-them-effective/)
- For social, remove as much as you can while still delivering the visual impact that conveys the message — [Tableau](https://www.tableau.com/blog/6-tips-to-design-charts-for-social-media)
- Without interactivity, labels and annotations are needed to make a chart self-explanatory (a slightly different emphasis from Tableau's declutter advice) — [Flourish](https://flourish.studio/blog/social-media-charts-and-graphs/)
- Use short, bold titles containing the key number; square or vertical layouts; high-contrast palettes for mobile — [everviz](https://www.everviz.com/blog/social-media-charts-case-study/)
- Include the data source on the chart itself, because reshared posts lose context — [Flourish](https://flourish.studio/blog/social-media-charts-and-graphs/)
- More than four or five bar categories: switch to a vertical (stacked) layout — [Better News](https://betternews.org/making-data-visualizations-interactives-work-well-mobile/)
- Netflix timed-text rules: minimum subtitle duration 5/6 of a second (20 frames at 24 fps), maximum 7 seconds, at least 2 frames gap between events — [Netflix Timed Text Style Guide: General Requirements](https://backlothelp.netflix.com/hc/en-us/articles/215758617)
- Netflix reading-speed limits (as stated in its Portuguese guide): adult programmes 200 words per minute / 17 characters per second; children's 160 wpm / 13 cps — [Netflix Portuguese Timed Text Style Guide](https://backlothelp.netflix.com/hc/en-us/articles/216787938-Portuguese-Timed-Text-Style-Guide)
- Secondary sources give up to 20 cps for English adult content and report a BBC target of 160-180 wpm (about 15 cps, roughly 0.3 s per word); these conflict slightly with each other and were not checked against primary BBC text — [Subtitle Toolset guide](https://subtitle-toolset.pages.dev/guides/subtitle-reading-speed/)
- GSAP ships the tools needed for data animation: eases are strings (default `"power1.out"`), stagger takes a number or an object such as `{ each: 0.1, from: "center" }` — [GSAP llms-full.txt](https://gsap.com/llms-full.txt)
- Since GSAP 3.13 (2025, after the Webflow acquisition) all formerly Club-only plugins, including SplitText and MorphSVG (and by the same statement DrawSVG), are free — [GSAP 3.13 release post](https://gsap.com/blog/3-13/)
- Vox-style map animation workflow: style the map, then keyframe a "camera" to follow the data path; the look is muted palettes with high-contrast lines that favour legibility over realism — [No Film School](https://nofilmschool.com/how-create-vox-style-map-animations-after-effects)

### Inferences
Dwell-time rule (opinion, derived from the Netflix/BBC figures): time on screen after the element has finished animating in = max(1.0 s, words x 0.3 s, characters / 17 s), plus about 0.5 s for each number the viewer must compare. Examples: a stat card "68% of users" (3 words) needs at least 1.0-1.5 s of hold; a 5-bar chart with 5 labels and 5 values needs roughly 3.5-4.5 s after the last bar lands. Never exceed about 7 s on one unchanged data frame (the Netflix maximum, and well past typical shorts pacing).

Capacity per screen (opinion; only the 4-5 bar rule is sourced):
- Big-number stat card: 1 number, 1 label of up to 6 words, optional 1 source line.
- Horizontal bars: 3-5 (6 absolute maximum); vertical columns: 4-6 because 1080 px width limits label length.
- Line chart: 1-2 series, 1 annotated point at a time, end-of-line labels instead of a legend; at most 4-5 x-axis ticks.
- Progress ring / donut: 1 ring per screen (2 if side by side at about 400 px diameter each).
- Pictogram / isotype grid: 10x10 = 100 icons works at about 80 px pitch across an 880-960 px content width; 5x4 = 20 for "1 in 5" style claims.
- Timeline: 3-5 nodes vertical (the axis runs top to bottom, which suits 9:16), revealing one node per beat.
- Map: 1 highlighted region plus at most 3 labels; push in so the region fills at least 60% of frame width.

Suggested GSAP component specs (opinion):
- **Counter / roll-up:** tween a proxy object value and write `textContent` on update with `snap` to the display precision; 0.8-1.2 s, `power2.out` or `expo.out` so it decelerates into the final number. Use `font-variant-numeric: tabular-nums` and a fixed-width container so digits do not jitter. Finish with a 1.00 to 1.06 to 1.00 scale pulse (0.25 s) to mark arrival. Digit size 180-280 px for a hero stat.
- **Bars draw-on:** `scaleX`/`scaleY` from 0, 0.6-0.9 s, `power3.out`, stagger 0.08-0.15 s; value labels fade in at 70% of each bar's tween.
- **Line draw-on:** SVG `stroke-dasharray`/`stroke-dashoffset` (or DrawSVG `drawSVG: "0%"` to `"100%"`), 1.2-2.0 s, `power1.inOut` (near-linear reads as "time passing"); stroke 6-8 px; a dot rides the line head; annotation pops in when the head reaches the point.
- **Progress ring:** SVG circle with stroke-dashoffset, stroke 28-40 px on a 400-520 px diameter ring, 1.0 s, `power2.out`, with the counter in the centre in sync.
- **Pictogram fill:** icons scale 0 to 1, 0.25 s each, `back.out(1.7)`, grid stagger `{ each: 0.015-0.03, from: "start", grid: "auto" }`, then the highlighted subset changes colour in a second staged step 0.3 s later.
- **Timeline:** spine draws 0.6 s per segment `power2.inOut`; node dot pops 0.3 s `back.out(2)`; date and label slide in 0.35 s `power2.out`.
- **Map:** region fill opacity 0 to 1 over 0.5 s; outline draw 0.8 s; camera push (scale 1 to 1.15-1.3) 2-4 s `power1.inOut`.

### Gaps
- No source states a tested maximum number of data points per vertical frame or a tested minimum on-screen time for charts in short-form video; the capacity and dwell rules above are derived, not measured.
- No Datawrapper, Bloomberg or Reuters guidance specific to vertical video was retrieved.
- No source was found on isotype/pictogram or progress-ring effectiveness in video specifically.
- Exact GSAP API details (`snap`, `roundProps`, DrawSVG syntax) could not be confirmed from gsap.com because the host was unreachable; verify against the docs before coding.

## 3. Kinetic typography: word-by-word emphasis, scale/pop, highlight sweeps, masks; durations, eases, staggers

### Takeaway
Word-by-word highlighted captions are the dominant 2025-2026 short-form caption treatment and every vendor data set points the same way (higher retention), but the numbers are unverified marketing figures and the one academic study found only that there is an optimal speed range and that some interpolation styles hurt readability. GSAP's SplitText (free since 3.13) with its `mask` option covers the standard reveal patterns.

### Cited Findings
- GSAP core eases are power1-power4 and expo, each with `.in`, `.out`, `.inOut`; back, elastic, bounce and `steps(n)` are in the EasePack plugin — [GSAP cheat sheet](https://gsap.com/cheatsheet)
- Ease strings and defaults: `"none"`, `"power1.out"` (default), `"power2.inOut"`, `"back.out(1.7)"`, `"elastic.out(1, 0.3)"`; stagger as `0.05` or `{ each: 0.1, from: "center" }` — [GSAP llms-full.txt](https://gsap.com/llms-full.txt)
- back.out overshoot parameter defaults to 1.7 (third-party tutorial, not official) — [animation-beta-one tutorial](https://animation-beta-one.vercel.app/learn/gsap/easing)
- SplitText `mask: "lines" | "words" | "chars"` (GSAP 3.13.0+) wraps each unit in an extra clipping element for reveal effects; only one mask type per instance — [GSAP SplitText docs](https://gsap.com/docs/v3/Plugins/SplitText/)
- Typical pattern: split a heading into lines, words and letters with `mask: "lines"`; use a smaller stagger for letters than for lines because animating dozens or hundreds of characters "would take forever" — [Codrops, May 2025](https://tympanus.net/codrops/2025/05/14/from-splittext-to-morphsvg-5-creative-demos-using-free-gsap-plugins/)
- A study from RIT Croatia / University of Zagreb (GRID symposium 2024) on kinetic typography in motion-graphic clips found an optimal speed range that supports comprehension and retention without losing engagement, and that specific interpolation techniques enhanced readability while others hindered it (effect sizes and sample not visible in the abstract) — [GRID 2024 paper](https://www.grid.uns.ac.rs/symposium/download/2024/89.pdf)
- Vendor, unverified: animated word-by-word captions give an 18-28% average retention boost versus 8-12% for static subtitles (no data source given) — [Clipspeed](https://clipspeed.ai/blog/ai-captions-increase-views.html)
- Vendor, unverified: across 7 caption styles and 80 videos, word-by-word emphasis with colour performed about 34% better on watch time than plain captions — [FluxNote](https://fluxnote.io/blog/ai-captions-that-improve-watch-time)
- Practitioner opinion: word-by-word presets retain best for educational content — [Opus Pro](https://www.opus.pro/blog/best-caption-presets-styles-boost-retention)
- Counter-view: kinetic text forces viewers to process reading and motion at once, which can reduce comprehension (the article's "Kinetic Readability Score" is proprietary) — [Advids](https://advids.co/insights/the-cognitive-load-paradox-why-engaging-animation-reduces-comprehension-and-how-to-fix-it)
- Captions that are too fast or too complex become a competing task — [Cursa](https://cursa.app/en/page/caption-systems-and-kinetic-text-for-clarity)
- Legacy Material Design UI timing for reference: elements entering about 225 ms, leaving about 195 ms, large full-screen transitions about 375 ms, and transitions over 400 ms can feel too slow (UI context, not video) — [Material Design (M1) duration and easing](https://m1.material.io/motion/duration-easing.html)

### Inferences
Suggested typographic motion presets (opinion; durations chosen to sit between the UI figures above and the reading-speed limits in section 2):

| Pattern | Split | From state | Duration | Ease | Stagger |
|---|---|---|---|---|---|
| Headline line reveal (masked rise) | lines, `mask: "lines"` | `yPercent: 100` | 0.6-0.8 s | `expo.out` or `power4.out` | 0.08-0.12 s |
| Word-by-word build | words | `y: 30, opacity: 0` | 0.3-0.4 s | `power3.out` | 0.06-0.10 s, or sync to voiceover word timings |
| Word pop (emphasis word) | single word | `scale: 0.6, opacity: 0` | 0.3-0.45 s | `back.out(1.7)` to `back.out(2.5)` | n/a |
| Character cascade (short words only, up to about 12 chars) | chars | `yPercent: 110` | 0.4-0.5 s | `power3.out` | 0.02-0.035 s |
| Active-word caption highlight | words | colour/background swap, scale 1 to 1.08 | 0.08-0.12 s | `power1.out` | driven by word timestamps |
| Highlight sweep (marker behind phrase) | background span | `scaleX: 0`, origin left | 0.35-0.5 s | `power2.inOut` | start 0.1-0.2 s after text settles |
| Underline draw | SVG path | dashoffset | 0.4-0.6 s | `power2.out` | n/a |
| Exit | whole block | `y: -30, opacity: 0` | 0.2-0.3 s | `power2.in` | 0-0.03 s |

- Total build time of a text block (duration + stagger x (n-1)) should stay under about 1 s, or under the time it takes to speak it, so the viewer is never waiting for text to finish arriving.
- Exits should be shorter than entrances (mirrors Material's 195 ms leave versus 225 ms enter).
- Use overshoot eases (`back.out`, `elastic.out`) only on 1 emphasised element per scene; everything else on `power3.out`/`expo.out`. Overshoot on body copy or on numbers that the viewer must read is the kind of interpolation likely to hurt readability (consistent with, but not proven by, the GRID study).
- Words per caption chunk: 2-5 words, 1-2 lines, so that the chunk can be read in about 1 s at 200 wpm.

### Gaps
- No primary source gives measured optimal durations, eases or stagger values for kinetic type in short-form video; the table is practitioner-style defaults.
- The GRID 2024 paper's specific speeds and which interpolations helped or hurt could not be read (host unreachable); worth opening directly.
- No independent (non-vendor) A/B data on word-by-word captions versus static captions was found.
- Official GSAP ease visualiser values (e.g. the back default of 1.7) were confirmed only through third-party pages.

## 4. Motion design principles applied to shorts: anticipation, overshoot, staging, parallax, continuous motion, camera moves, transitions

### Takeaway
The evidence-backed principles are staging (break complex changes into simple steps), keeping transitions only as long as needed, and decelerating into the end state; the "something changes every 2-4 seconds" pacing rule is ubiquitous in creator guidance but rests on unverified vendor numbers. Specific values for overshoot, parallax and Ken Burns moves are convention, not measured.

### Cited Findings
- Staging and brevity: use simple stages for complex transitions, minimise occlusion, make transitions as long as needed but no longer (Heer and Robertson principles as taught at UW) — [UW CSE442 slides](https://courses.cs.washington.edu/courses/cse442/24au/lectures/CSE442-Animation.pdf)
- Standard easing is asymmetrical: elements speed up quickly then slow down gently, focusing attention on the end of the transition — [Google Design, "Motion Design Doesn't Have to Be Hard"](https://medium.com/google-design/33089196e6c2)
- Design-system duration scales reserve 400 ms and 600 ms for large, page-level or full-screen transitions (Atlassian tokens); Material 3 long durations are reported second-hand as 500/550/600 ms with standard easing cubic-bezier(0.2, 0, 0, 1) — [Atlassian Design](https://atlassian.design/foundations/motion/applying-motion)
- expo.out is described in third-party GSAP guides as a strong ease-out used for dramatic reveals and page transitions; power3.out as a strong deceleration — [GSAP easing skill reference](https://skills.sh/microck/gsap-skills/gsap-easing)
- Vendor guidance: change the on-screen image every 2-4 seconds in faceless Shorts — [FluxNote](https://fluxnote.io/guides/faceless-shorts-retention-tips-2026)
- Vendor guidance: the midpoint is the weakest point of the average Shorts retention curve, so place the largest pattern interrupt there — [GoFaceless](https://www.gofaceless.ai/en/blog/high-retention-youtube-shorts-attributes)
- Vox style details: motion graphics deliberately animated at 12 fps, and stepped texture changes on lower thirds, give the videos their rhythm — [PremiumBeat](https://www.premiumbeat.com/blog/replicating-vox-motion-graphic/)
- Vox/Johnny Harris map sequences keyframe a virtual camera to follow the data path across a styled map — [No Film School](https://nofilmschool.com/how-create-vox-style-map-animations-after-effects)
- A vertical wipe is a recommended reveal for charts in video — [Online Journalism Blog, June 2026](https://onlinejournalismblog.com/2026/06/23/showing-charts-on-video-here-are-two-essential-techniques-to-make-them-effective/)

### Inferences
Suggested defaults (opinion):
- **Never a static frame:** every scene carries one slow ambient tween for its whole length: background or screenshot scale 1.00 to 1.04-1.08 (Ken Burns push) with `ease: "none"` or `power1.inOut`, and/or a 10-20 px drift. Keep it slow enough that text riding on it remains readable; do not put the ambient move on the text layer itself.
- **Beat cadence:** a new visual event (element enters, highlight moves, number lands, cut) every 2-4 s, matching the vendor pacing guidance; put the strongest change (layout swap, colour inversion, biggest number) near the midpoint.
- **Anticipation:** a 0.10-0.15 s counter-move before a big move (scale 1 to 0.96, or 8-12 px opposite to travel) using `power2.in`, or GSAP `back.in(1.4)` on exits.
- **Overshoot:** `back.out(1.4-2.0)` gives roughly 5-10% overshoot, suitable for chips, ticks, icons and stat cards; reserve `elastic.out(1, 0.5)` for one playful accent. Avoid overshoot on full-screen moves.
- **Stagger:** 0.05-0.12 s for sibling items (cards, rows); total cascade under about 0.6 s; use `from: "center"` or `"edges"` for grids.
- **Parallax:** 2-3 depth layers moving at about 0.4x / 0.7x / 1.0x of the camera move; with a 60 px camera drift that is 24 / 42 / 60 px.
- **Transitions:** hard cut on the beat is the default; whip (translate a full frame height or width in 0.25-0.35 s, `power4.inOut`, with 12-24 px motion blur via CSS filter at the midpoint); zoom-through (outgoing scale 1 to 1.6-3 with fade, incoming 0.6 to 1, 0.4-0.5 s, `expo.inOut`); mask wipe (`clip-path` circle or inset, 0.5-0.7 s, `power3.inOut`); match cut (shared element holds position and size across the cut while everything else changes). Keep transitions at or under about 0.5 s, in line with the "over 400 ms feels slow" UI guidance scaled up slightly for full-frame video.
- **Stepped animation:** a 12 fps stepped look (GSAP `steps()` ease or rendering holds) on texture or hand-drawn accents is a cheap way to get the Vox editorial feel without changing the main 30 fps motion.

### Gaps
- No School of Motion, Motion Design School or Ben Marriott material was retrieved in this session, so the classic-principles guidance is not directly sourced to those educators.
- No measured data on optimal Ken Burns scale ranges, parallax ratios or transition lengths for vertical video was found.
- A claim that videos with a pattern interrupt every 4 seconds averaged 58% retention versus 41% for static talking heads appeared in search results, but I could not pin it to a specific page or data set; treat as unattributed and unverified.

## 5. UI / screenshot presentation: mockups, zoom-to-region, cursor, arrows, blur-and-spotlight

### Takeaway
Screen-recording tool vendors agree on a small set of rules: zoom to the element being acted on (not the cursor's rough area) at about 1.5-2.2x, keep the cursor visible and enlarged, pair zoom with a gradual dim/spotlight, and use effects only where they aid comprehension. This matches the signaling principle from multimedia-learning research (section 7).

### Cited Findings
- Zoom range guidance: 1.5x-2.2x for subtle emphasis — [OpenScreen guide](https://www.mintlify.com/siddharthvaddem/openscreen/guides/creating-demos)
- Auto-zoom tools expose 1.0x-4.0x — [FocuSee review, UX Planet](https://uxplanet.org/create-eye-catching-videos-with-focusee-38f22adabe53)
- Zoom should land on the field or button being clicked, typically triggered on the click itself — [Trainn](https://trainn.co/answers/how-to-add-zoom-effects-to-product-demo-videos/)
- Do not hide the cursor: viewers cannot follow micro-movements, so use a larger, more visible cursor; disable trails, sparkles and "fun" effects — [Clueso](https://www.clueso.io/blog/how-to-make-tasteful-screen-capture-videos)
- Audience tuning: larger cursors, slower animations and persistent spotlights for beginner/general audiences; subtle click indicators and brief zooms for expert audiences — [Docsie](https://www.docsie.io/blog/glossary/cursor-and-focus-polish/)
- Spotlight should be a gradual, professional dimming rather than a flat grey overlay; combine a zoom to enlarge a form field with a spotlight to hold the eye during narration — [Trainn](https://trainn.co/answers/how-to-add-spotlight-effects-to-your-product-demo-videos/)
- Use effects only when they improve comprehension — [TechSmith](https://www.techsmith.com/blog/edit-demo-recording/)
- Vendor, unverified: videos with cursor zoom receive 34% fewer "I can't see" comments — [Docsie](https://www.docsie.io/blog/glossary/cursor-and-focus-polish/)

### Inferences
Vertical-specific arithmetic and suggested specs (opinion):
- A 1440 px-wide desktop screenshot fitted to 1080 px is at 0.75x; 14 px UI text becomes about 10.5 video px, far below the roughly 48 px caption floor in section 6. To make a 14 px label reach about 40 px in frame you need roughly 2.9x of the original (about 3.8x of the fitted image). So in 9:16 a desktop screenshot can only ever be an establishing shot; every readable beat must be a crop/zoom to a region no wider than about 350-450 source px. The 1.5-2.2x guidance is from 16:9 demos and is too low for desktop UI in vertical.
- **Screenshot card:** rounded corners 24-32 px, soft shadow (0 30 px 80 px at 25-35% black), optional browser or phone chrome, 60 px side margins, slight 3D tilt (rotateX/rotateY 4-8 degrees) easing to flat as it settles, plus the ambient 1.00 to 1.05 push.
- **Zoom-to-region:** animate scale and x/y of the screenshot container together, 0.7-1.0 s, `power3.inOut`; hold at least 1.5 s; one zoom target per narration sentence. Prefer cutting between regions over long pans across the page.
- **Spotlight:** dim overlay at 55-70% black (dark theme) or 60% white wash plus 6-10 px blur (light theme) with a rounded-rectangle cut-out 16-24 px larger than the target; fade 0.3-0.4 s, `power2.out`. Move the cut-out between targets over 0.5 s rather than fading out and in.
- **Callout extract (often better than zoom in 9:16):** duplicate the region as its own card, scale it up to the full content width, and connect it to its origin with a thin line; the full page stays visible but dimmed above or below.
- **Cursor:** draw a synthetic cursor at 2-3x native size (about 64-96 px in frame); move along a slightly curved path 0.5-0.8 s, `power2.inOut`; click = scale 1 to 0.85 to 1 in 0.15 s plus a ripple ring expanding 0 to 120 px, fading over 0.4 s.
- **Arrows / annotations:** hand-drawn SVG stroke 6-8 px, draw-on 0.4-0.6 s `power2.out`, label 44-56 px; one annotation on screen at a time; ring highlights 6 px stroke with a 1.00 to 1.06 pulse.
- For this repo's rule that captions use exact UI labels, the callout extract makes the real label legible so the caption and the UI visibly match.

### Gaps
- All sources are 16:9 screen-recording tool vendors; nothing retrieved addresses presenting desktop UI inside a 9:16 frame specifically.
- No evidence on device-mockup framing versus bare screenshots for retention or trust.
- No sourced timing values for zoom duration or spotlight opacity; the figures are suggested defaults.

## 6. Visual hierarchy and style: type scale for 1080x1920, words on screen, contrast, grid, and 2025-2026 trends

### Takeaway
Safe-zone figures differ between sources, but the conservative consensus is a central content area of roughly 880-960 px by 1,380-1,420 px, with the bottom 480-660 px and a right-hand strip treated as unsafe on TikTok. Vendor guidance puts the minimum meaningful text size at about 48 px with 60-75 px bold as the working caption range. Trend roundups for 2026 agree on grain/texture, typography-as-motion, restrained glass and bento modules, though "generic bento" is already called dated.

### Cited Findings
- TikTok publishes no fixed pixel margins; its spec says the safe zone varies with video dimensions, caption length and add-ons and it supplies downloadable safe-zone overlay files — [ManyPixels](https://www.manypixels.co/blog/social-media-design/tiktok-ad-specs)
- Conservative in-feed figures for 1080x1920 (reported as taken from TikTok's files): keep text, faces and logos out of the top 240 px, bottom 660 px and 120 px on each side — [Socialync](https://www.socialync.io/tools/safe-zones/tiktok)
- Looser figures: top 130 px, bottom 480+ px, right 140 px — [Spilno Agency](https://spilnoagency.com.ua/en/instructions-us/tiktok-ads-creative-sizes-2026); or about 250 px bottom, 150 px right, 130 px top — [RecurPost](https://recurpost.com/blog/tiktok-video-sizes/)
- Effective content area estimates: about 880x1420 px — [Argil](https://argil.ai/blog/tiktok-aspect-ratio-cec4c); about 960x1386 px — [PostEverywhere](https://posteverywhere.ai/blog/tiktok-aspect-ratio); roughly 900x1400 px across platforms — [PostPlanify](https://postplanify.com/blog/social-media-safe-zones-2026-complete-guide)
- Rule of thumb: keep headlines and subtitles in the middle 70% of the screen — [SubtitleBee](https://subtitlebee.com/blog/tiktok-video-size/)
- Caption size on a 1080x1920 frame: about 48-55 px is the minimum readable for meaningful captions, 60-75 px the usual working range; weight matters (a 55 px bold 700 caption reads better than 70 px at weight 300) — [BlitzCut, TikTok caption size 2026](https://blitzcutai.com/blog/best-caption-size-tiktok-2026)
- Same thresholds for YouTube Shorts (48 px floor, 60-75 px standard) — [BlitzCut, Shorts caption size 2026](https://blitzcutai.com/blog/best-caption-size-youtube-shorts-2026)
- Lower figure from a practitioner forum: 30 px minimum for the smallest text, with the caveat that social video is rarely shown at full resolution and is recompressed on upload — [Adobe Community](https://community.adobe.com/questions-529/new-to-creating-animations-for-instagram-reels-and-i-unsure-what-size-to-make-my-body-copy-text-52535)
- Subtitle line length convention: 42 characters per line, 2 lines maximum (Netflix English, via secondary source) — [Subtitle Toolset guide](https://subtitle-toolset.pages.dev/guides/subtitle-reading-speed/)
- Use high-contrast palettes for mobile charts — [everviz](https://www.everviz.com/blog/social-media-charts-case-study/)
- 2026 trend roundups (vendor blogs, not research; the search extract did not preserve which page made which statement, so attribution within this group is approximate): bento grids are established but "generic bento grids with stock illustrations" now look dated; glassmorphism returns in a restrained form and Apple's iOS 26 "liquid glass" (transparency and refraction) is the emerging premium look; grain, noise and texture return as primary surface treatments with zine/collage/film-photo references; typography is "no longer merely supporting motion" but is the motion; editorial layouts with clear hierarchy and white space; a reaction against "clean and competent" AI-era design in favour of crafted imperfection — [Videobolt](https://blog.videobolt.net/post/top-motion-graphics-trends-2026); [Line25](https://line25.com/articles/web-design-trends-2026/); [Graphic Design Junction](https://graphicdesignjunction.com/2026/01/video-and-motion-creative-trends-2026/); [Designity](https://designity.com/blog/2d-animation-trends-2026); [Renderforest](https://www.renderforest.com/blog/design-trends-in-2026)

### Inferences
Physical-size check (opinion; uses common phone widths of about 390-430 pt, which I did not source): a 1080 px-wide video shown full-width maps 1 video px to about 0.36-0.40 pt, so 48 px is about 17-19 pt (around normal phone body text) and 30 px is about 11-12 pt (footnote size, marginal after compression). That supports 48 px as the floor for anything the viewer must read and 30-36 px only for source lines.

Suggested type scale for 1080x1920 (opinion):

| Role | Size | Weight | Notes |
|---|---|---|---|
| Hero number | 200-300 px | 800-900 | tabular figures; unit or % at 50-60% of digit size |
| Hook / headline | 96-140 px | 700-900 | 3-7 words, 2-3 lines, line-height 1.0-1.1, tracking -1 to -2% |
| Sub-headline / card title | 64-80 px | 600-700 | up to about 8 words |
| Caption / body | 56-72 px | 600-700 | 2 lines max, about 18-24 characters per line at 64 px in a 880-960 px column |
| Chart labels | 44-56 px | 500-600 | direct labels, no legend |
| Source / footnote | 30-36 px | 500 | 70% opacity is acceptable; keep inside safe area |

Layout grid (opinion, built on the conservative safe-zone numbers):
- Safe content box: x 120-960 (840 px wide) when designing for TikTok's strictest figures, or x 60-940 with the right-hand 140 px kept free of text only in the lower half where the action rail sits; y 240-1380 as the "everything important" zone. Captions sit with their baseline no lower than about y = 1380-1440 (bottom margin 480-540 px); never in the bottom 480 px.
- 6-column grid inside the safe box, 24 px gutters; 8 px spacing unit; card radius 32-48 px; card padding 40-48 px.
- One focal element per frame; at most about 12-15 words visible in total including the caption (derived from 200 wpm and 2-4 s beats: a 3 s beat allows about 10 words of reading at most, and the viewer is also listening).
- Contrast: aim for at least 4.5:1 for all text and effectively 7:1+ for captions (WCAG thresholds; not sourced in this session), using a solid or 60-80% scrim, stroke or shadow behind captions over imagery. One accent colour reserved for the highlighted word, bar or number; a second colour only for the "B" side of a comparison.
- Trend application that suits HTML/CSS rendering: SVG `feTurbulence` or PNG noise overlay at 4-8% opacity (optionally stepped at 8-12 fps for a film-grain flicker); glass cards with `backdrop-filter: blur(20-30px)`, 8-14% white fill and a 1 px 20% white border; bento stat grids of 2 columns x 3-4 rows where one tile spans both columns; oversized editorial serif or grotesque headlines mixed with a mono or small-caps label; subtle 3D depth via `perspective` and 4-8 degree tilts with layered shadows. Because trend sources warn that generic bento looks dated, use bento for genuinely multi-stat recap frames, not as the default layout.
- Brand consistency for this repo: keep the existing light and dark explainer palettes as the two themes and express every component through shared tokens (type scale, radius, accent, ease set, duration set) so shorts and 16:9 explainers read as one family.

### Gaps
- No platform-published minimum font size exists in the sources; all sizes are vendor or forum figures. TikTok's, Instagram's and YouTube's own current overlay templates were not retrieved, and the safe-zone numbers conflict (bottom margin anywhere from 250 px to 660 px).
- No source gives a tested "maximum words on screen" for shorts; the 12-15 word ceiling is derived from reading speed.
- WCAG contrast ratios are quoted from memory, not from a source fetched here.
- Trend sources are vendor roundups with overlapping, non-attributable claims; no usage data shows which styles actually perform better.

## 7. Evidence on which graphic treatments improve retention or comprehension

### Takeaway
The strongest evidence is from multimedia-learning research: cut extraneous material (coherence), cue the essential item (signaling) and present in short segments, each with medium-to-large effect sizes; duplicating full narration as on-screen text has at best a weak and inconsistent effect, which argues for short keyword captions rather than full sentences when there is a voiceover. Platform-style retention claims for captions, word-by-word highlights and pattern interrupts all point upward but come from vendors without published methods.

### Cited Findings
- Mayer's 2017 review (Journal of Computer Assisted Learning) reports median effect sizes of d = 0.87 for redundancy, 0.46 for signaling and 0.70 for segmenting — [Mayer 2017, "Using multimedia for e-learning"](https://zendy.io/title/10.1111/jcal.12197)
- Later tables (Mayer 2021 as cited in a UNH handout and an EdTech Books chapter) give coherence 0.86, signaling about 0.69-0.70, segmenting 0.67, and redundancy only 0.10; the redundancy figures conflict sharply between editions (0.87 versus 0.10) — [UNH handout of Mayer's principles](https://www.unh.edu/teaching-learning-resource-hub/sites/default/files/media/2023-06/itow-research-based-principles-for-designing-multimedia-instruction-mayer.pdf); [EdTech Books](https://edtechbooks.org/docx/10349)
- The redundancy principle concerns adding on-screen text that duplicates narration to narrated graphics; segmenting concerns breaking a lesson into parts rather than one continuous stream — [Mayer 2020 principles summary](https://ugc.futurelearn.com/uploads/files/7d/d6/7dd6188d-c343-4311-b064-ac98d2c95abc/Multimedia_Principles._R._E._Mayer__2020.pdf)
- Animated transitions between chart states significantly improve graphical perception versus static cuts in controlled experiments (object tracking, value estimation) — [Heer and Robertson 2007](https://idl.uw.edu/papers/animated-transitions)
- For reading trends, static small multiples were 10% more accurate than animation and animation was 82% slower for analysis, although participants preferred animation (Robertson et al. 2008, via lecture slides) — [UW CSE442 slides](https://courses.cs.washington.edu/courses/cse442/18au/lectures/CSE442-Animation.pdf)
- Kinetic typography has an optimal speed range for comprehension and retention, and interpolation choice affects readability — [GRID 2024 paper](https://www.grid.uns.ac.rs/symposium/download/2024/89.pdf)
- Vendor, unverified: burned-in captions give a 17% higher completion rate (attributed to Tubular Labs, original not located) — [FluxNote](https://fluxnote.io/guides/increase-audience-retention-youtube-shorts)
- Vendor, unverified: on-screen text gives an 18% watch-time increase (attributed to "Instavar's 2026 research", original not located) — [GoFaceless](https://www.gofaceless.ai/en/blog/high-retention-youtube-shorts-attributes)
- Vendor, unverified: word-by-word animated captions 18-28% retention lift versus 8-12% for static subtitles — [Clipspeed](https://clipspeed.ai/blog/ai-captions-increase-views.html); word-by-word colour emphasis about 34% better watch time across 80 videos — [FluxNote](https://fluxnote.io/blog/ai-captions-that-improve-watch-time)
- Vendor, unverified: cursor zoom yields 34% fewer "I can't see" comments — [Docsie](https://www.docsie.io/blog/glossary/cursor-and-focus-polish/)

### Inferences
- Mapping research to components (opinion): signaling = spotlight, highlight sweep, accent colour on one bar or word, arrow callouts; segmenting = one idea per 2-4 s beat, row-by-row builds, staged chart reveals; coherence = strip axes, gridlines, decorative icons and background clutter, and avoid ambient motion that competes with the focal element; temporal contiguity = sync each element's entrance to the narrated word.
- On captions with voiceover: the research does not clearly condemn or endorse verbatim captions (0.87 versus 0.10 across editions), while platform reality is that many viewers watch muted. A defensible compromise for this repo, where captions are the voiceover script, is short 2-5 word chunks synced to speech, placed away from the graphic's focal region, and never a second, different block of text competing with the caption.
- Animation is justified where the viewer must track "this became that" (bar growth, rank change, before/after); for reading exact values, hold a static, labelled end frame. Combining both (animate then hold) fits both Heer and Robertson results.
- Because every retention number specific to shorts is vendor-sourced, the report should present them as directional and recommend the team A/B test its own treatments using platform retention curves.

### Gaps
- No peer-reviewed or platform-published study was found that isolates a graphic treatment (stat cards, charts, kinetic captions, zooms, transitions) and measures retention on TikTok, Reels or Shorts.
- The original Tubular Labs and "Instavar" figures could not be located; they may not exist in the form cited.
- Mayer effect sizes were taken from search extracts of secondary copies; the exact table (edition, number of experiments) should be confirmed in Multimedia Learning, 3rd ed. (2021) before publication.
- The Robertson et al. 2008 numbers come from lecture slides, not the paper.
- Hosts that must be allowed in the session's network settings for a fuller pass: gsap.com, flourish.studio, onlinejournalismblog.com, www.grid.uns.ac.rs (all failed to resolve here).
