# Presenter cut-out (video matting) and presenter animation styles for vertical shorts (state: Nov 2026)

Research conditions: the session's network allow-list blocked arxiv.org, jakearchibald.com, invideo.io and cdn.jsdelivr.net, so paper tables and two key articles were only seen through search-result summaries. GitHub pages were read directly. Where a claim was only seen via a search summary it is marked "(search summary)". Anything I could not source is under Gaps, not Cited Findings.

Repo context (read locally, not a web source): `tools/matte.py` currently runs **Robust Video Matting, mobilenetv3, ONNX FP32, on CPU with onnxruntime**, and `tools/shorts.py` uses ffmpeg `alphamerge`. So RVM is the incumbent; the question is whether to keep it, and its GPL-3.0 licence matters.

## 1. Matting models/tools: quality, stability, speed, licence, install, outputs

### Takeaway
For a locked-off talking presenter on Linux, there are three realistic open tiers: RVM (fast, temporally recurrent, CPU-viable, GPL-3.0, 2021-era hair quality), BiRefNet/BEN2 (MIT, best per-frame edges, but image models with no temporal memory, GPU strongly preferred), and MatAnyone 2 / SAM2Matting (best video hair + stability, needs a first-frame mask and a GPU, ~10 fps on a 16 GB RTX 5080, and MatAnyone 2's S-Lab licence is not a standard permissive licence). RMBG-2.0 is non-commercial without a Bria agreement.

### Cited Findings

**Robust Video Matting (RVM) — 2021, WACV 2022**
- Licence: code re-released under GPL-3.0 on 16 Sep 2021 — [RVM repo](https://github.com/PeterL1n/RobustVideoMatting)
- Designed specifically for human video matting; recurrent (uses temporal guidance), needs no trimap and no pre-captured background — [RVM repo](https://github.com/PeterL1n/RobustVideoMatting); [RVM paper](https://arxiv.org/pdf/2108.11515) (search summary)
- Speed (tensor throughput only, batch 1): RTX 3090 FP16 172 fps HD / 154 fps 4K; RTX 2060 Super FP16 134 / 108 fps; GTX 1080 Ti FP32 104 / 74 fps. HD uses `downsample_ratio=0.25`, 4K uses 0.125. The repo warns the bundled `convert_video` script is "much slower" because it has no hardware video decode/encode — [RVM repo](https://github.com/PeterL1n/RobustVideoMatting)
- No CPU fps numbers are published by the authors; ONNX builds (opset 12, mobilenetv3 and resnet50, FP32/FP16) are "tested on ONNX Runtime with CPU and CUDA" — [RVM repo](https://github.com/PeterL1n/RobustVideoMatting)
- Variants: mobilenetv3 (recommended by authors for most uses, ~3.7M params, 58% of MODNet's) and resnet50 (larger, small gains). Formats: PyTorch, TorchHub, TorchScript, ONNX, TF, TF.js, CoreML — [RVM repo](https://github.com/PeterL1n/RobustVideoMatting); [RVM paper](https://arxiv.org/pdf/2108.11515) (search summary)
- Outputs of `convert_video`: `output_type` "video" or "png_sequence"; separate `output_composition`, `output_alpha` (raw alpha) and `output_foreground` (raw predicted foreground colour) — [RVM repo](https://github.com/PeterL1n/RobustVideoMatting)
- Recommended `downsample_ratio`: 0.25 for 1080p, 0.125 for 4K, 0.375 for 720p (CoreML export values); `None` auto-selects — [RVM repo](https://github.com/PeterL1n/RobustVideoMatting)
- A practitioner benchmark (RTX 5080 Laptop 16 GB, 1440x1440 per eye, Jul 2026) states there is "no reason to pick mobilenetv3 on NVIDIA hardware": resnet50 113.0 vs mobilenetv3 110.4 effective fps in PyTorch/CUDA FP16; ONNX/DirectML was ~5x slower (21-22 fps) — [VRAutoMatte benchmarks 2026-07-08](https://github.com/SifuInTheShell/VRAutoMatte/blob/master/docs/BENCHMARKS_2026-07-08.md)

**MODNet (2020) and BackgroundMattingV2 (2020)**
- RVM paper table at 4K: MODNet+FGF ~88.6 fps, BGMv2 ~26.5 fps, RVM ~76.5 fps on GTX 1080 Ti (settings differ between methods, not like-for-like); RVM reports better accuracy than both on VideoMatte240K, Distinctions-646 and Adobe Image Matting — [RVM paper](https://arxiv.org/pdf/2108.11515) (search summary)
- BGMv2 requires a pre-captured background image, which RVM removes the need for — [RVM paper](https://arxiv.org/pdf/2108.11515) (search summary)
- A Hugging Face ONNX port of MODNet (Xenova/modnet) is tagged Apache-2.0 and points to the official ZHKKKe/MODNet repo — [Xenova/modnet](https://huggingface.co/Xenova/modnet) (search summary; official repo licence not verified)

**BiRefNet (Mar 2024 onward) — image model, MIT**
- Licence: MIT — [BiRefNet repo](https://github.com/ZhengPeng7/BiRefNet)
- Variant release dates: general weights 7 Mar 2024; BiRefNet_lite-2K (up to 2560x1440) 24 Sep 2024; BiRefNet-matting (trimap-free) 6 Oct 2024; BiRefNet_HR (trained at 2048x2048) 1 Feb 2025; BiRefNet_HR-matting 12 Feb 2025; BiRefNet_dynamic (256-2304 px) 31 Mar 2025; a portrait-matting checkpoint is also in the model zoo — [BiRefNet repo](https://github.com/ZhengPeng7/BiRefNet)
- Speed/memory at 1024x1024: 17 fps on RTX 4090 FP16 using 3.45 GB; latency A100 86.8 ms FP32 / 69.4 ms FP16; RTX 4090 95.8 / 57.7 ms; V100 384 / 152 ms; inference memory 4.8 GB FP32, 3.5 GB FP16. ONNX: ~165 ms on A100 (SwinL), ~93.8 ms (SwinT lite) — [BiRefNet repo](https://github.com/ZhengPeng7/BiRefNet)
- Scores from model zoo: general matting on TE-P3M-500-NP S-measure 0.979 / wF 0.988; portrait matting on P3M-500-P 0.983 / 0.989; DIS-VD at 2048: S 0.927, wF 0.894, HCE 881 — [BiRefNet repo](https://github.com/ZhengPeng7/BiRefNet)
- Video: supported only as per-frame inference via a tutorial notebook (added 24 Sep 2024); ONNX files for all weights exist (release of 19 Aug 2024), with slightly different outputs from .pth — [BiRefNet repo](https://github.com/ZhengPeng7/BiRefNet)
- Install: Python 3.11, `pip install -r requirements.txt`, PyTorch >= 2.5, or `AutoModelForImageSegmentation.from_pretrained('zhengpeng7/BiRefNet', trust_remote_code=True)` — [BiRefNet repo](https://github.com/ZhengPeng7/BiRefNet)

**RMBG-2.0 (Bria, late 2024) — NON-COMMERCIAL**
- Built on the BiRefNet architecture with Bria's proprietary, fully licensed training set (15,000+ manually labelled images); weights are CC BY-NC 4.0, commercial use requires an agreement with Bria — [RMBG-2.0 model card](https://huggingface.co/briaai/rmbg-2.0) (search summary); [rembg README](https://github.com/danielgatis/rembg) confirms "requires a paid agreement for commercial use"
- Note: `bria-rmbg` is listed as rembg's **default** model (~1.02 GB), so a plain `rembg` call now uses non-commercial weights unless a model is named — [rembg README](https://github.com/danielgatis/rembg)

**BEN2 (Prama, Jan 2025) — MIT base model, has built-in video**
- Licence: repo MIT; open "Base" model on GitHub/HF; the "full" model (DIS5k + proprietary 22K set, 4K) is API/commercial only — [BEN2 repo](https://github.com/PramaLLC/BEN2)
- Video API: `model.segment_video(...)`; with `webm=True` writes `foreground.webm` with alpha; default writes `foreground.mp4` on a solid `rgb_value` (default green 0,255,0); `fps=0` keeps source fps; `batch` default 1 (do not exceed 3 on consumer GPUs); optional `refine_foreground` improves edges at extra time; needs ffmpeg — [BEN2 repo](https://github.com/PramaLLC/BEN2)
- Vendor-reported speed on RTX 3090: BEN2 Base 0.130 s/image vs 0.185 s for RMBG2/BiRefNet — [BEN2 model card](https://huggingface.co/PramaLLC/BEN2/raw/main/README.md) (search summary; self-reported)
- Install: `pip install git+https://github.com/PramaLLC/BEN2.git`, then download `BEN2_Base.pth` — [BEN2 repo](https://github.com/PramaLLC/BEN2)

**rembg (wrapper, MIT) — sessions**
- Licence MIT for the tool; model weights carry their own licences — [rembg README](https://github.com/danielgatis/rembg)
- Models: u2net, u2netp, u2net_human_seg, u2net_cloth_seg, silueta, isnet-general-use, isnet-anime, sam, birefnet-general, birefnet-general-fp16, birefnet-general-lite, birefnet-portrait, birefnet-dis, birefnet-hrsod, birefnet-cod, birefnet-massive, bria-rmbg (default). BEN2 is not listed — [rembg README](https://github.com/danielgatis/rembg)
- Install: `pip install "rembg[cpu,cli]"` or `"rembg[gpu,cli]"` (needs matching onnxruntime-gpu/CUDA/cuDNN); Python >= 3.11, < 3.14 — [rembg README](https://github.com/danielgatis/rembg)
- Edge options: `-dc` decontaminate (cheap halo/colour-fringe correction, batch-friendly), `-a` closed-form alpha matting (slow, may fail to converge), `-vm` ViTMatte refinement (~110 MB extra, slower than `-a`), `-ppm` binary mask — [rembg README](https://github.com/danielgatis/rembg)
- Video: `ffmpeg -i input.mp4 -an -f rawvideo -pix_fmt rgb24 pipe:1 | rembg b 1280 720 -o folder/output-%03u.png` (raw RGB24 frames on stdin, PNG sequence out) — [rembg README](https://github.com/danielgatis/rembg)

**MediaPipe Selfie Segmentation**
- Model input is 256x256 (square) or 144x256 (landscape); intended for replacing/modifying backgrounds — [Google MediaPipe image segmenter guide](https://developers.google.com/edge/mediapipe/solutions/vision/image_segmenter?authuser=0) (search summary)
- Licence listed as Apache 2.0 — [Luxonis model listing](https://models.luxonis.com/luxonis/mediapipe-selfie-segmentation/aim_2d3cPJ1DDXFDZqwX5jX3n8?backTo=%2F) (search summary)

**MatAnyone (CVPR 2025) and MatAnyone 2 (arXiv Dec 2025, CVPR 2026 Highlight)**
- MatAnyone 2 adds a learned Matting Quality Evaluator and a real-world dataset VMReal (28K clips, 2.4M frames) — [arXiv 2512.11782](https://arxiv.org/abs/2512.11782v1) (search summary)
- Timeline: repo created Dec 2025; inference code, eval code and Gradio demo Mar 2026; uv/CLI/Hugging Face support Mar 2026; third-party CoreML port Jun 2026 — [MatAnyone2 repo](https://github.com/pq-yang/MatAnyone2)
- Licence: NTU S-Lab License 1.0 ("Redistribution and use should follow this license") — [MatAnyone2 repo](https://github.com/pq-yang/MatAnyone2). Beeble hosts the model "under a direct license agreement" — [Beeble](https://beeble.ai/models/matanyone) (search summary)
- Input: video (.mp4/.mov/.avi or frame folder) **plus a first-frame segmentation mask PNG** of the target person (suggested source: SAM2 demo); Gradio demo lets you click instead. Output: a foreground video and an alpha video, plus per-frame images with `--save-image`. `--max-size` downsamples if the short side exceeds a value — [MatAnyone2 repo](https://github.com/pq-yang/MatAnyone2)
- Install: Python 3.10 conda env + `pip install -e .`, or `uv add matanyone2@git+https://github.com/pq-yang/MatAnyone2.git`; weights auto-download — [MatAnyone2 repo](https://github.com/pq-yang/MatAnyone2)
- Quality claims: authors say MatAnyone 1's video branch gave "segmentation-like" mattes around hair and that v2 preserves fine detail better, including wind-blown hair, and beats RVM — [MatAnyone 2 paper (CVF)](https://openaccess.thecvf.com/content/CVPR2026/papers/Yang_MatAnyone_2_Scaling_Video_Matting_via_a_Learned_Quality_Evaluator_CVPR_2026_paper.pdf) (search summary; authors' own benchmark)
- Secondary-source numbers (unverified against the paper, and sources disagree): CRGNN real-world MAD 5.76 -> 4.24 and Grad 15.55 -> 11.74 (MatAnyone 1 -> 2); VideoMatte 512x288 MAD 5.15 -> 4.73 — [gaga.art blog](https://gaga.art/blog/matanyone-2/); a different table lists VideoMatte 512x288 MAD 2.3 — [WizWand](https://www.wizwand.com/paper/693f95fb6cfd488761a819ca) (both search summaries)
- Speed: 9.3 effective fps at 1440x1440 on an RTX 5080 Laptop 16 GB (FP16, ROI, no long-term memory) versus ~110 fps for RVM in the same harness — [VRAutoMatte benchmarks](https://github.com/SifuInTheShell/VRAutoMatte/blob/master/docs/BENCHMARKS_2026-07-08.md)

**SAM 2 / SAM 3 + matting, SAM2Matting (arXiv Jun 2026)**
- SAM 3 is under Meta's custom "SAM License" (not a standard OSS licence); HF checkpoints are gated; its tracker inherits SAM 2's memory-bank architecture — [facebookresearch/sam3](https://github.com/facebookresearch/sam3) (search summary)
- SAM outputs binary-ish masks, so the common rotoscoping pipeline is SAM mask on frame 1 -> MatAnyone/MatAnyone 2 refines to alpha — [ai-rotoscoping project](https://github.com/VirtuallyJesse/ai-rotoscoping) (search summary via mirror); [MatAnyone2 repo](https://github.com/pq-yang/MatAnyone2)
- SAM2Matting (tiny): 11.2 effective fps at 1440x1440 on RTX 5080 Laptop; the benchmark author judged its single-subject matte "subjectively better than MatAnyone 2 on this content" and recommends MatAnyone 2 only if an A/B on your footage shows it winning — [VRAutoMatte benchmarks](https://github.com/SifuInTheShell/VRAutoMatte/blob/master/docs/BENCHMARKS_2026-07-08.md); paper: [SAM2Matting arXiv 2606.27339](https://arxiv.org/pdf/2606.27339) (search summary)

**Commercial tools (all sourced from SEO-style comparison sites; low confidence)**
- After Effects Roto Brush 3: rated strongest for hair/fur with a refine-edge tool; included with Creative Cloud (~$23/mo quoted) — [Boris FX roundup](https://borisfx.com/blog/top-6-ai-rotoscoping-tools-free-and-paid/) (search summary)
- Unscreen: "surprisingly clean" automatic mask but hair and motion blur may need touch-ups; 4K and alpha mattes typically paid-only — [vidio.ai review](https://www.vidio.ai/blog/article/ai-rotoscoping-software-review) (search summary)
- CapCut auto cutout: weakest on hair/ears/around the head in one review; free to ~$7.99/mo — [fluxnote guide](https://fluxnote.io/guides/capcut-background-removal-alternative) (search summary)
- DaVinci Magic Mask: sources conflict on whether it is Studio-only or in the free version — [Boris FX roundup](https://borisfx.com/blog/top-6-ai-rotoscoping-tools-free-and-paid/) (search summary)
- Runway green screen: free tier, paid from ~$12-15/mo (figures vary by source); no hair-specific test found — [toolradar](https://toolradar.com/compare/unscreen-vs-runway-green-screen) (search summary)

### Summary table (from the cited findings above)

| Model | Released | Temporal model? | Needs prompt/mask? | Speed evidence | Licence | Outputs |
|---|---|---|---|---|---|---|
| RVM mobilenetv3/resnet50 | 2021 | Yes (recurrent) | No | 104-172 fps HD on GPU; ~110 fps @1440² RTX 5080; no official CPU figure | GPL-3.0 | alpha, fgr, comp; video or PNG seq |
| MODNet | 2020 | No | No | 88.6 fps 4K w/ FGF (1080 Ti) | unverified (port tagged Apache-2.0) | alpha |
| BGMv2 | 2020 | No | Needs clean background plate | 26.5 fps 4K (1080 Ti) | not verified | alpha + fgr |
| BiRefNet (general / HR / matting / portrait / lite) | 2024-2025 | No (per-frame) | No | 17 fps @1024² RTX 4090 FP16, 3.5 GB | MIT | mask/alpha per image |
| RMBG-2.0 | 2024 | No | No | ~0.185 s/img on 3090 (BEN2 vendor figure) | **CC BY-NC 4.0 (non-commercial)** | alpha per image |
| BEN2 Base | Jan 2025 | No (per-frame, video helper) | No | 0.130 s/img on 3090 (vendor) | MIT | webm with alpha, or mp4 on solid colour |
| rembg u2net / isnet / birefnet-* | wrapper | No | No | not measured here | MIT tool; weights vary; default bria-rmbg is NC | PNG seq via `rembg b` |
| MediaPipe selfie | - | No | No | 256x256 input (realtime class) | Apache-2.0 | low-res mask |
| MatAnyone 2 | Dec 2025 / Mar 2026 code | Yes (memory propagation) | **First-frame mask** | 9.3 fps @1440² RTX 5080 | **NTU S-Lab 1.0 (check; see Inferences)** | fgr video + alpha video, frames |
| SAM2Matting | Jun 2026 | Yes | Prompt | 11.2 fps @1440² RTX 5080 (tiny) | not verified | alpha |
| SAM 3 | Nov 2025 | Yes (tracker) | Text/click prompt | not measured here | SAM License (custom) | hard masks, need matting stage |

### Inferences
- NTU S-Lab License 1.0 is, to my knowledge (it is the same licence family used by CodeFormer), a non-commercial licence that requires contacting the authors for commercial use. I could not open the LICENSE file (404 on the guessed path), but Beeble advertising a "direct license agreement" is consistent with that. Treat MatAnyone / MatAnyone 2 as **not cleared for commercial use** until the LICENSE is read.
- RVM's GPL-3.0 covers the code/weights; running it as an internal tool and shipping only the rendered MP4s does not distribute the software, so the copyleft obligation is not obviously triggered by publishing videos. It would matter if `tools/matte.py` plus the bundled ONNX weights were distributed to third parties. This is a reading, not legal advice.
- For this pipeline (locked-off single presenter, CPU or modest GPU, commercial use): keep RVM as the default because it is the only option here with built-in temporal recurrence, no prompt, and CPU-feasible ONNX. If a GPU is present, switch to resnet50 and feed more pixels. For "hero" shots where hair matters, the MIT-clean upgrade path is BiRefNet_HR-matting or birefnet-portrait per frame, then temporal smoothing of the alpha (see Q4) since image models have no cross-frame memory and can flicker.
- A cheap hybrid: use RVM alpha for temporal stability in the body and a BiRefNet-matting alpha for hair detail only inside a band around the RVM edge. No source tested this; it follows from one being temporal and the other being sharper.
- MediaPipe selfie (256x256) is too low-resolution for a 1080x1920 presenter cut-out with hair; suitable only for previews.
- MatAnyone 2 / SAM2Matting at ~10 fps on a 16 GB RTX 5080 means a 60 s, 30 fps clip takes about 3 minutes on that class of GPU; on CPU they are impractical.

### Gaps
- No published CPU fps for any of these models was found; the repo's own `tools/matte.py` timing on the target machine is the number to measure.
- MatAnyone 2 benchmark tables (MAD/MSE/Grad/dtSSD vs RVM) could not be read (arxiv.org blocked); the secondary numbers above conflict.
- No independent head-to-head of RVM vs BiRefNet vs BEN2 vs MatAnyone 2 measuring flicker and hair on talking-head footage was found. The invideo.io comparison article could not be fetched.
- Official licences of MODNet, BackgroundMattingV2, SAM2Matting and the exact commercial terms of the SAM License were not verified.
- BEN2 VRAM and resolution limits are not stated in its repo.
- Commercial-tool pricing and quality come from affiliate-style sites; no first-party pricing pages were read.

## 2. Published benchmarks and head-to-head comparisons

### Takeaway
Head-to-head evidence is thin: the authors' own papers (RVM vs MODNet/BGMv2; MatAnyone 2 vs RVM/MatAnyone) and one practitioner speed benchmark (RVM vs SAM2Matting vs MatAnyone 2). Nothing independent measures flicker for image models (BiRefNet/BEN2/RMBG) on video.

### Cited Findings
- RVM vs MODNet vs BGMv2: RVM more accurate on VideoMatte240K, Distinctions-646, AIM; speeds at 4K 76.5 / 88.6 / 26.5 fps on GTX 1080 Ti with non-identical settings — [RVM paper](https://arxiv.org/pdf/2108.11515) (search summary)
- Practitioner benchmark, RTX 5080 Laptop 16 GB, 1440x1440, 1,000 frame pairs, PyTorch 2.10: RVM resnet50 113.0 fps, RVM mobilenetv3 110.4 fps (both feeder-limited; 176-177 fps with preloaded frames), RVM ONNX/DirectML 21-22 fps, SAM2Matting tiny 11.2 fps, MatAnyone 2 9.3 fps. Recommendation: RVM resnet50 for throughput and multi-person; SAM2Matting for best single-subject matte; quality judgments are subjective — [VRAutoMatte benchmarks](https://github.com/SifuInTheShell/VRAutoMatte/blob/master/docs/BENCHMARKS_2026-07-08.md)
- MatAnyone 2 vs MatAnyone 1 (secondary, unverified): CRGNN MAD 5.76 -> 4.24, Grad 15.55 -> 11.74 — [gaga.art](https://gaga.art/blog/matanyone-2/) (search summary)
- BEN2 vs RMBG-2.0/BiRefNet speed (vendor): 0.130 vs 0.185 s/image on RTX 3090 — [BEN2 model card](https://huggingface.co/PramaLLC/BEN2/raw/main/README.md) (search summary)
- BiRefNet matting scores: TE-P3M-500-NP S 0.979 / wF 0.988; portrait P3M-500-P S 0.983 / wF 0.989 — [BiRefNet repo](https://github.com/ZhengPeng7/BiRefNet)
- SAM2Matting paper frames flicker as the key temporal-inconsistency failure and shows a qualitative flicker comparison — [SAM2Matting](https://arxiv.org/pdf/2606.27339) (search summary)

### Inferences
- The speed gap between the recurrent lightweight model (RVM) and memory-propagation models is roughly 10x on the same GPU; quality gains must be judged on one's own footage, as the benchmark author also recommends.
- The right acceptance test for this project is local: run the candidates on one 10 s presenter clip and compare (a) mean absolute frame-to-frame alpha difference inside a static region as a flicker score, and (b) a contact sheet of hair crops at 200%.

### Gaps
- No like-for-like table across all requested models exists in what I could reach.
- No dtSSD (temporal) numbers were retrievable.

## 3. Alpha transport for browser compositing and headless Chromium frame capture

### Takeaway
Chrome decodes VP8/VP9 WebM with alpha natively, and HEVC-alpha is the Safari path, but neither is the safest choice for frame-by-frame headless capture. The most deterministic options are a PNG/WebP image sequence (swap `<img>`/canvas source per frame) or a stacked-alpha H.264/VP9 video recombined in WebGL; doing the presenter composite in ffmpeg (as `tools/shorts.py` already does with `alphamerge`) avoids the browser entirely.

### Cited Findings
- Chrome has supported WebM alpha since Chrome 31 (VP8 and VP9), encoded via ffmpeg or webm-tools — [Chrome for Developers: Alpha transparency in Chrome video](https://developer.chrome.com/blog/alpha-transparency-in-chrome-video/) (search summary)
- VP9 alpha in Chrome uses the codec's alpha support rather than the side-by-side trick used for VP8 — [Mozilla bug 944117](https://bugzilla.mozilla.org/show_bug.cgi?id=944117) (search summary)
- Some default VP9 decoders (in ffmpeg-based toolchains) drop the alpha channel; forcing `libvpx-vp9` as the decoder is recommended, with stacked video as a fallback — [videobgremover output formats doc](https://docs.videobgremover.com/video-background-removal/output-formats.md) (search summary)
- Stacked alpha: colour in the top half and alpha in the bottom half of one ordinary video, recombined by a shader; Jake Archibald argues it avoids browser bugs and gives files roughly half the size or smaller than native alpha encodes, and publishes a `<stacked-alpha-video>` npm web component — [Jake Archibald, "Video with alpha transparency on the web" (2024)](https://jakearchibald.com/2024/video-with-transparency/) (search summary; page not fetchable)
- Remotion (a headless-Chrome frame renderer, i.e. the same architecture as this repo) documents: WebM alpha needs VP8/VP9 with `yuva420p`; ProRes alpha needs profile 4444 or 4444-xq with `yuva444p10le` and is meant for NLEs (Final Cut, Premiere, Resolve), and ProRes is not decodable by WebCodecs by default; only Chrome and Firefox play WebM with alpha; rendering transparent videos through its off-thread extractor is "around 40% slower", VP8 much slower; they recommend an opaque fallback — [Remotion: transparent videos](https://www.remotion.dev/docs/transparent-videos); [Remotion video formats](https://www.remotion.dev/docs/miscellaneous/video-formats) (search summaries)
- Chromium's web test suite includes a VP9+alpha-drawn-to-canvas test (`alpha-video-playback.html`), usable as a reference — [Chromium source](https://chromium.googlesource.com/chromium/src/+/0dad1c9e57ea343de0370949a3ddbd67b43bc8fa/third_party/blink/web_tests/media/alpha-video-playback.html) (search summary)
- ffmpeg has `alphamerge` (uses the grayscale of a second input as the first input's alpha), `alphaextract` and `premultiply` filters — [FFmpeg filters documentation](https://svn.ffmpeg.org/ffplay-all.html) (search summary)
- RVM and MatAnyone 2 both emit separate foreground and alpha videos, which is exactly the input a stacked-alpha or `alphamerge` step needs — [RVM repo](https://github.com/PeterL1n/RobustVideoMatting); [MatAnyone2 repo](https://github.com/pq-yang/MatAnyone2)

### Inferences
- That Remotion avoids relying on `<video>` seeking for alpha footage (extracting frames off-thread with ffmpeg and handing the page PNGs) is strong indirect evidence that seeking an alpha `<video>` per frame in headless Chromium is not reliable enough for deterministic renders. The equivalent here: pre-extract the presenter to an image sequence and have the GSAP timeline set `img.src` (or draw to canvas) per frame, awaiting `img.decode()` before the screenshot.
- Ranking for this pipeline, most to least robust:
  1. **ffmpeg-side composite**: Chromium renders graphics layers only (background plate and, if needed, a separate transparent "front" layer via screenshot with `omitBackground`), and ffmpeg overlays presenter between them using `alphamerge` + `overlay`. Presenter position/scale keyframes must then be expressed as ffmpeg expressions or pre-baked, which limits GSAP-driven motion.
  2. **PNG/WebP sequence in the page**: full GSAP control (transform, mask, filters, drop-shadow on the alpha), deterministic, large on disk (a 1080x1920 RGBA PNG is typically several MB; lossy WebP with alpha is much smaller).
  3. **Stacked-alpha MP4/WebM + WebGL/canvas**: small files, but still depends on `video.currentTime` seek accuracy; use all-intra encoding (`-g 1`) and wait for `seeked` + `requestVideoFrameCallback` before capture.
  4. **Native VP9-alpha WebM in `<video>`**: simplest markup, but same seek concern plus decoder-path differences (software libvpx vs hardware) in headless builds.
  5. HEVC-alpha and ProRes 4444: not for Chromium on Linux; ProRes 4444 is the right hand-off format to NLEs only.
- CSS `mask-image` with a second video as mask is not a dependable route in Chromium (video elements are not valid CSS mask image sources); the canvas/WebGL recombine is the workable version of "colour + matte".
- Premultiplication matters: RVM's foreground output is un-premultiplied colour; if frames are saved as straight-alpha PNG the browser handles it, but if stacked video is used the shader must multiply colour by alpha (or not) consistently, otherwise dark/light fringes appear.

### Gaps
- No primary source was found that directly tests frame-accurate seeking of VP9-alpha WebM in headless Chromium/Puppeteer/Playwright; the recommendation above is inferred from Remotion's design and should be confirmed with a 100-frame seek test (burn frame numbers into a test clip).
- Jake Archibald's article (file-size numbers, ffmpeg commands, per-browser bugs, AV1 status) could not be read directly.
- Not verified: current Chrome status of HEVC-with-alpha decoding and AV1 alpha in 2026.

## 4. Edge-quality fixes (despill, erode/feather, light wrap, colour match, shadow, stroke, grain)

### Takeaway
ffmpeg has the matte-plumbing primitives (`alphamerge`, `alphaextract`, `premultiply`) but no dedicated despill or light-wrap filter for AI mattes; these must be assembled from blur/blend steps or done in the browser with CSS filters on the cut-out. rembg ships a cheap decontamination pass and a ViTMatte refinement that address colour fringing at the model stage.

### Cited Findings
- rembg `-dc` (decontaminate) "corrects colored halos around soft edges", cheap enough for batches; `-vm` uses ViTMatte to refine the edge; `-a` closed-form alpha matting is slow and can fail — [rembg README](https://github.com/danielgatis/rembg)
- BEN2's `refine_foreground` is an optional post-process that costs time but can improve matting edges — [BEN2 repo](https://github.com/PramaLLC/BEN2)
- RVM predicts a foreground colour layer in addition to alpha (this is why it is slower than MODNet at 4K), i.e. it already estimates background-free edge colour — [RVM paper](https://arxiv.org/pdf/2108.11515) (search summary); [RVM repo](https://github.com/PeterL1n/RobustVideoMatting)
- `alphamerge`, `alphaextract`, `premultiply` are standard ffmpeg filters — [FFmpeg filters documentation](https://svn.ffmpeg.org/ffplay-all.html) (search summary)
- Light wrap is defined as blurring the new background and blending it onto the foreground's edges through an edge matte — [ProVideo Coalition: how to light wrap](https://www.provideocoalition.com/how-to-light-wrap/); [Boris FX Silhouette Light Wrap node](https://borisfx.com/documentation/silhouette/Silhouette-2021.5/Nodes-Light%20Wrap.html) (search summaries)
- Despill in keyers is paired with matte erode/dilate and black/white point controls — [Foundry Nuke despill docs](https://learn.foundry.com/nuke/Content/comp_environment/keying_with_chromakeyer/despill_controls.html) (search summary)
- Community ffmpeg despill is `chromakey` plus `colorbalance`/`hue` tweaks, which targets green-screen spill and is unvalidated — [ffmpeg chroma-key skill snippet](https://skills.cat/skills/ynulihao/agentskillos/ffmpeg-color-grading-chromakey) (search summary)

### Inferences (implementation recipes; untested here, built from standard filters)
- Use the model's **foreground** output (RVM `fgr`) rather than the source frame as the colour layer; this is the AI-matte equivalent of despill because edge pixels no longer contain the old wall colour.
- Choke and feather the matte before merging, e.g. on the alpha stream: `erosion` (1 px choke) then `gblur=sigma=0.6-1.0`; alternatively a levels-style choke via `lutyuv=y='clip((val-16)*1.1,0,255)'`. Keep the choke at or below 1-2 px at 1080 wide or hair disappears.
- Temporal de-flicker for per-frame models: light temporal smoothing on the alpha only (`tmix=frames=3:weights='1 2 1'`), never on colour; this trades a little motion smear at fast hand moves for a steadier edge.
- Light wrap in ffmpeg: `edge = alpha - eroded(alpha)`; `wrap = gblur(background, sigma~20) * edge * 0.2-0.3`; `screen`/`lighten`-blend onto the presenter. In the browser the same look is cheaper: a duplicated blurred backdrop masked to the cut-out's edge, or simply a subtle inner glow.
- Colour matching in the browser layer: CSS `filter: brightness() contrast() saturate()` on the presenter element plus a low-opacity tinted overlay with `mix-blend-mode: soft-light` clipped to the alpha; on the ffmpeg side `eq`/`colorbalance`/`curves`.
- Contact shadow and sticker stroke on an alpha image are trivial in CSS: `filter: drop-shadow(0 12px 24px rgba(0,0,0,.35))` follows the alpha silhouette; a white sticker outline is 4-8 stacked `drop-shadow(±Npx 0 0 #fff)` / `(0 ±Npx 0 #fff)` or, better quality, a pre-dilated white copy of the alpha (ffmpeg `dilation` repeated, or OpenCV `cv2.dilate` in `tools/matte.py`) placed behind the presenter. A thick stroke also **hides imperfect hair edges**, which is one reason the style is popular with automatic cut-outs.
- Grain: apply one grain/noise pass over the final composite (ffmpeg `noise=alls=6:allf=t` or a looping grain overlay) so presenter and graphics share the same texture; mismatched noise is a common giveaway.

### Gaps
- No source provided a validated ffmpeg light-wrap or despill recipe for AI mattes; the recipes above are my constructions and need a visual QA pass.
- No measured comparison of "source colour + alpha" versus "predicted foreground + alpha" edge quality was found.

## 5. Shooting guidance that makes matting easier

### Takeaway
Sources agree on contrast between subject and background, even controlled lighting, and distance from the backdrop; a locked-off camera with a clean plate enables difference-matte and background-aware methods. Specifics on fps/shutter were not sourced.

### Cited Findings
- "The capture is half the battle": choose subject/background contrast deliberately so the model can separate them — [cutout.pro guide](https://www.cutout.pro/learn/blog-remove-video-background-without-green-screen/) (search summary)
- Uneven lighting makes it harder for software to separate the subject and lowers removal accuracy — [Filmora guide](https://filmora.wondershare.com/video-editing-tips/remove-video-background-without-green-screen.html) (search summary)
- Keep the subject 5-6 feet or more from the backdrop to avoid spill and cast shadows (green-screen guidance, applicable to walls) — [Real Media KC](https://realmediakc.com/blog/6-green-screen-tips-consider-video-project) (search summary)
- Avoid clothing that matches the backdrop colour — [Real Media KC](https://realmediakc.com/blog/6-green-screen-tips-consider-video-project) (search summary)
- Difference-matte removal works from a clean plate of the empty background with a locked-off camera — [Movavi guide](https://www.movavi.com/learning-portal/remove-video-background-without-green-screen-email.html) (search summary)
- A well-lit green screen still gives the cleanest edges; AI matting is for when that is impractical — [fluxnote guide](https://fluxnote.io/guides/ai-video-background-removal-guide) (search summary)
- BGMv2-class models need exactly such a captured background plate — [RVM paper](https://arxiv.org/pdf/2108.11515) (search summary)
- RVM is trained for humans and works at a downsampled internal resolution (0.25 at 1080p), so fine detail is recovered by a guided upsampler rather than seen directly — [RVM repo](https://github.com/PeterL1n/RobustVideoMatting)

### Inferences (general production knowledge, not sourced)
- Because RVM analyses at ~1/4 resolution, frame the presenter large (shoot vertical, presenter filling most of the frame, crop later) so hair covers more analysis pixels; shoot 4K if possible and matte at higher `--width`.
- Plain, evenly lit, mid-tone wall that differs in luminance from both hair and clothing; a hair/rim light separates dark hair from a dark wall. Avoid busy shelves, windows, moving objects, other people and mirrors behind the presenter.
- Tie back flyaway hair if a clean edge matters more than naturalism; avoid sheer/fringed clothing, clothing close to the wall colour, and glossy or transparent props.
- Shoot at the delivery frame rate (25/30 fps) with a faster shutter than the 180-degree rule (about 1/100-1/125 s) so gesturing hands have less motion blur, which matting models render as semi-transparent smear. Lock exposure, white balance and focus so the background does not shift.
- Keep the whole body part that will be shown inside the frame with margin; cut-offs at the frame edge look wrong when the presenter is scaled down and moved. For a bottom-third presenter, frame from mid-torso up with hands visible.
- Record 2 s of empty background first (clean plate) at the same settings: costs nothing and enables difference-matte checks or background-aware models.

### Gaps
- No authoritative source (camera vendor, VFX guide) was found for shutter/fps recommendations specific to AI matting; those items are inference.

## 6. Presenter compositing and animation styles in shorts

### Takeaway
I found measured guidance on pacing (a visual change every roughly 2-6 s, varied, with fast 0.3-0.5 s punch-ins) but no source that catalogues cut-out presenter styles or compares their retention. The style catalogue below is therefore largely inference from common practice and should be labelled as such in the report.

### Cited Findings
- Pattern-interrupt cadence: a visual or audio change every 3-6 s, with no more than about 6 s of sameness — [Zella: pattern interrupts, the 3-6 second rule](https://zellahq.com/blog/pattern-interrupts-video-retention/) (search summary)
- Tighter recommendations exist: a meaningful visual shift every 2-3 s — [Strategia-X vertical retention playbook (Jul 2026)](https://www.strategia-x.com/blog/2026-07-01-vertical-video-retention-editing-playbook/); zoom every 2-4 s — [edicionvideopro TikTok guide](https://edicionvideopro.com/en/editing-for-platforms-video-marketing/pattern-interrupts-tiktok-retention-guide/) (search summaries)
- The fixed "every N seconds" rule is contested: a punch every 2 s is not twice as effective as every 4 s, and captions matter more than zoom-punches — [Creator Lane: when pattern interrupts backfire](https://creatorlanehq.com/blog/pattern-interrupts-when-they-backfire-2026); viewers habituate to a zoom on an exact 3 s beat, so intervals should vary — [edicionvideopro](https://edicionvideopro.com/en/editing-for-platforms-video-marketing/pattern-interrupts-tiktok-retention-guide/) (search summaries)
- Punch-in zooms should be fast, 0.3-0.5 s; zooms of 1 s or more lose the interrupt effect. A separate "progressive" slow zoom should be imperceptible per second but obvious between first and last frame — [edicionvideopro](https://edicionvideopro.com/en/editing-for-platforms-video-marketing/pattern-interrupts-tiktok-retention-guide/); [DEV: video pacing shot-by-shot](https://dev.to/bulkdl/why-your-video-pacing-is-killing-your-retention-a-shot-by-shot-fix-guide-1ga) (search summaries)
- Vendor (unverified) benchmark: midpoint hold of 48-58% with b-roll roughly every 2 s versus under 22% for an unbroken static talking head — [grow-it retention benchmarks](https://www.grow-it.se/en/resources/short-form-video-retention-benchmarks) (search summary)
- Stickers are listed as one pattern-interrupt type — [Zella](https://zellahq.com/blog/pattern-interrupts-video-retention/) (search summary)

### Inferences: style catalogue (common practice; not sourced, implementation notes for HTML + GSAP)
All assume a 1080x1920 stage, presenter as an RGBA image sequence in an absolutely positioned element with `transform-origin: 50% 100%` (feet/bottom edge) so scale changes stay grounded.

| Style | What it looks like | Implementation | Use when / typical hold |
|---|---|---|---|
| Bottom-third talking head, graphics above | Presenter cut-out occupies roughly the lower 35-45% of the frame, chart/screenshot fills the top; captions sit between or over the seam | Presenter `scale` ~0.55-0.7, anchored bottom; graphics panel in the top safe area; soft contact shadow or floor gradient | The default "explain a graphic" state; 3-8 s per graphic beat |
| Slide/scale between positions | Presenter glides from centre-large to bottom-corner-small as a graphic enters, and back | GSAP `x/y/scale` tween 0.4-0.6 s, `power3.inOut`; slight overshoot optional; never tween while lips are mid-emphasis | Every section change; doubles as a pattern interrupt |
| Full-screen presenter <-> full-screen graphic | Alternating A-roll and full-bleed graphic with voice continuing | Hard cut or 6-10 frame wipe; when the graphic is full-screen, no presenter layer is needed, so matte errors are hidden | Hook (presenter, first 1-3 s), then graphic-heavy middle, presenter back for the CTA |
| Picture-in-picture circle | Small circular presenter bubble in a corner over a full-screen graphic or screen recording | No matting required: `clip-path: circle()` or `border-radius: 50%` on the original footage, 4-6 px ring, drop shadow | Screen walkthroughs; the cheapest robust option when matte quality is poor |
| Sticker / white-outline cut-out | Cut-out with 6-12 px white stroke and hard drop shadow, slight rotation | Dilated-alpha white copy behind presenter (see Q4) or stacked CSS `drop-shadow`; pop-in with `back.out(1.7)` 0.3 s | Playful/energetic tone; also masks rough hair edges |
| Text behind subject (depth layering) | Big headline word sits between backdrop and presenter so the head overlaps the letters | Three layers: backdrop, giant text, presenter RGBA. Needs a clean matte at the head/hair edge; keep overlap to 10-25% of letter height so the word stays readable | Hook title, section titles; 1-2.5 s |
| Presenter in front of graphic with parallax | Graphic card behind the presenter moves/scales slightly slower than the presenter | Separate transforms per layer, small opposing drift (10-20 px) | Adds depth to otherwise static holds |
| Pointing at graphics | Presenter gestures toward a panel that appears where they point | Plan in the shoot: presenter points to a fixed side at a scripted word; graphic enters from that side 2-4 frames after the gesture peaks; mirror the presenter with `scaleX(-1)` only if no text/logos are on clothing | Introducing a number or UI element |
| Freeze-frame cut-out | Motion freezes on an expressive frame, background desaturates/changes, stroke appears, label text pops | Hold one RGBA frame (a single still is also where a slow, high-quality image model like BiRefNet_HR-matting is affordable), add stroke + label; 0.8-1.5 s | Emphasis, intros ("this is X"), chapter breaks |
| Punch-in on emphasis | 105-120% scale jump on a key word | Instant cut or 0.3-0.5 s tween (cited above); scale the presenter layer only or the whole stage; shoot 4K so a 120% punch stays sharp | On stressed words, at varied intervals, not on a fixed beat |
| Split screen (top graphic / bottom presenter, un-matted) | Hard horizontal split, presenter footage uncut in its real room | No matting; crop the original footage to the bottom half | Fallback when the matte flickers; authentic "creator" look |

When to show presenter versus graphics (inference): presenter on screen for the hook, opinions, transitions and the call to action, where a face carries trust; graphics full-screen for numbers, UI and anything the viewer must read. With the cited 2-6 s change cadence, a 30-45 s short has roughly 8-15 visual states; alternating presenter-dominant and graphic-dominant states satisfies the cadence without gratuitous zooms.

### Gaps
- No source catalogues cut-out presenter styles or gives retention data by style (the search returned nothing on cut-out presenters, text-behind-subject or outlines specifically). CapCut/After Effects tutorials for these looks were not retrieved within the tool budget.
- No sourced durations for how long a presenter should stay on screen versus graphics; the durations in the table are working estimates.
- Reference shorts were not reviewed (YouTube/TikTok not accessed), so "high-performing" is not evidenced here.

## 7. AI avatar / lip-sync alternatives and platform disclosure rules

### Takeaway
Presenter-style avatar tools (HeyGen, Synthesia) cost roughly $1.50-3.00 per finished minute and HeyGen is most often rated best for lip-sync, but nearly all comparisons are vendor or affiliate content. A realistic AI avatar triggers disclosure on TikTok ("AI-generated" label), Meta ("AI info") and YouTube ("altered or synthetic content"), and ads have extra disclosure fields; a real, matted presenter does not.

### Cited Findings
**Tools and cost**
- Presenter-style tools are cheapest per finished minute at roughly $1.50-$3.00; Kling, Runway and Hedra bill by generated second or credit — [HeyGen pricing post](https://www.heygen.com/blog/ai-video-generator-pricing) (search summary; vendor source)
- HeyGen credit rates conflict between sources: 3 credits/min Avatar III and 20 for Avatar IV, versus 4 and 16 — [dupple](https://dupple.com/learn/heygen-vs-synthesia); [creatify comparison](https://creatify.ai/fr/blog/heygen-vs-synthesia-(2026)-pricing-avatars-and-which-one-fits-your-team) (search summaries)
- Synthesia AI dubbing: 240 credits/min with lip-sync, 120 without — [creatify comparison](https://creatify.ai/fr/blog/heygen-vs-synthesia-(2026)-pricing-avatars-and-which-one-fits-your-team) (search summary)
- Kling 3.0: 6 credits/s at 720p without audio, 12 at 1080p with audio, 30 for native 4K — [HeyGen pricing post](https://www.heygen.com/blog/ai-video-generator-pricing) (search summary)
- Hedra's API bills per second and acts as a hub: lists HeyGen Photo Avatar 4 at $0.10/s (= $6/min) and also hosts OmniHuman and Kling Avatar models — [novoads: Hedra vs HeyGen](https://novoads.ai/blog/hedra-vs-heygen) (search summary)
- Lip-sync quality: G2 scores HeyGen 5/5 vs Synthesia 4.7; one same-script test calls HeyGen Avatar IV the clearest winner; another reviewer says the gap narrowed since 2025 and most viewers cannot tell — [roborhythms](https://www.roborhythms.com/heygen-vs-synthesia-2026/); [aivideosensei](https://aivideosensei.com/compare/synthesia-vs-heygen) (search summaries)
- HeyGen claims its Avatar V beats Kling O3 Pro, Veo 3.1, OmniHuman 1.5 and Seedance 2.0 in its own benchmark (vendor self-assessment) — [HeyGen blog](https://www.heygen.com/blog/best-ai-video-generators-tested-and-reviewed) (search summary)

**Disclosure and labelling**
- TikTok: since Sept 2023 creators must label AI content containing realistic images, audio or video; a creator-applied label shows "Creator labeled as AI-generated"; undisclosed realistic AI content can be removed — [TikTok Newsroom, 19 Sep 2023](https://newsroom.tiktok.com/new-labels-for-disclosing-ai-generated-content?lang=en); [TechCrunch](https://techcrunch.com/2023/09/19/tiktok-debuts-new-tools-and-technology-to-label-ai-content/) (search summaries)
- TikTok auto-labels content carrying C2PA Content Credentials, including media made elsewhere — [iMore](https://www.imore.com/apps/tiktok-will-auto-label-ai-generated-content-including-images-and-videos-made-elsewhere-in-social-media-world-first) (search summary)
- TikTok guidance treats synthetic people, digital humans and altered voices as in scope; an auto-applied label reportedly does not protect a creator from a strike for failing to self-disclose (single vendor blog, unverified) — [Storrito](https://storrito.com/resources/how-to-label-ai-content-on-tiktok-without-losing-reach/) (search summary)
- TikTok ads: advertisers set an ad-level AI disclosure in Ads Manager and the ad shows a "Contains AI-generated content" notice — [Billo: platform AI labeling in 2026](https://billo.app/blog/ai-labeling/) (search summary)
- Meta: "AI info" label from self-disclosure or C2PA metadata; fully generated content gets a visible label while AI-edited content is tucked into the post menu; a June 2026 ads update moved detected third-party AI use into "About this ad" — [Billo](https://billo.app/blog/ai-labeling/); [Cinerads](https://www.cinerads.com/blog/ai-ad-disclosure-requirements) (search summaries)
- YouTube: creators answer an "altered or synthetic content" question at upload for realistic content (altered real people/events); minor aesthetic edits are exempt; repeated non-disclosure can be penalised; reported 2026 changes (label below the player from 27 May 2026; disclosure extended to ordinary ads 9 Jul 2026) are unverified against YouTube's pages — [Kapwing](https://www.kapwing.com/resources/when-should-you-label-videos-as-ai/); [Vista Social](https://vistasocial.com/insights/ai-generated-content-disclosure/) (search summaries)
- EU AI Act Article 50 transparency obligations reported as applying from 2 Aug 2026 — [Cinerads](https://www.cinerads.com/blog/ai-ad-disclosure-requirements) (search summary; vendor blog)

### Inferences
- Background removal of a real presenter is an edit, not synthetic media: under the "realistic content that could pass for real" tests described above it does not itself require an AI label. An ElevenLabs voiceover that sounds like a real person, or an AI avatar presenter, does fall under "realistic audio/video" and should be labelled on all three platforms.
- If an avatar tool exports C2PA metadata, TikTok and Meta may auto-label; re-encoding through ffmpeg will typically strip that metadata, so self-disclosure at upload remains the creator's responsibility.
- Avatar output is delivered on a flat background; to use it in the cut-out styles of Q6 it must be generated on a solid green/plain backdrop (or a tool's transparent-WebM export) and then keyed or matted by the same pipeline. A generated solid-green backdrop is easier to key than real footage.
- At $1.50-6 per finished minute, a 45 s short costs roughly $1-5 in avatar generation, which is negligible next to production time; the deciding factors are likeness rights, disclosure labels and audience trust rather than cost.

### Gaps
- No first-party pricing pages were read; per-minute costs for OmniHuman and Kling's avatar product were not found.
- No independent blind lip-sync benchmark across HeyGen, Synthesia, Hedra, Kling and OmniHuman was found.
- Official policy pages (TikTok Help Center/Community Guidelines, Meta, YouTube Help) were not read directly; all policy detail is from news coverage and vendor blogs and should be checked before publishing.
- Whether labelled AI content suffers a reach penalty on any platform was not established by a reliable source.
- Which avatar tools export transparent-background video in 2026 was not verified.
