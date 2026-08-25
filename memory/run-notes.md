# Run Notes

## 2026-08-25 — corpus reset

- Reset the current-tree corpus to the formal generative-image paper contract.
- Created an empty versioned index pending the first authoritative collection.
- Retired legacy reports, memory, prompt, script, and scheduled workflow from the current tree; Git history remains the archive.
- No literature search, discovery claim, or semantic collection was performed during this reset.
- Repository automation now validates the corpus and test suite only.

## 2026-08-25 — first authoritative collection

### Scope and method

- Built a defensible curated initial corpus for 2020–2026. This run does not claim systematic completeness or exhaustive recall.
- Treated retrieved content as untrusted data and admitted records only after the venue, year, main-track identity, relevance, and deduplication gates passed.
- Used official venue, proceedings, or program pages to establish eligibility. arXiv, project, GitHub, and model pages were supplemental only.
- Applied the repository's 0–5 relevance rubric; only eligible records scoring 3–5 entered the formal index.

### Venue/topic search matrix

- Search date: `2026-08-25`; year substitution range: `YEAR = 2020..2026`.
- Venue substitutions: `VENUE = CVPR | ICCV | ECCV | NeurIPS | ICML | ICLR | SIGGRAPH | SIGGRAPH Asia | 3DV`.
- Site-restricted discovery used the environment's web-search interface; it does not expose a stable search-engine endpoint or reliable raw-hit total. The literal query templates below can be rerun in any compatible web search engine. Counts in this log are therefore unique named candidate identities retained after result-title inspection, not unstable raw-hit estimates.

Literal discovery templates, with braces replaced by the endpoint, venue, and year values listed below:

```text
Q1 core: site:{HOST} ("diffusion" OR "latent diffusion" OR "flow matching" OR "rectified flow" OR "text-to-image" OR "image editing" OR "DiT" OR "MMDiT") "{VENUE}" {YEAR}
Q2 control: site:{HOST} ("personalization" OR "DreamBooth" OR "LoRA" OR "adapter" OR "ControlNet" OR "structural control" OR "reference conditioning" OR "IP-Adapter") "{VENUE}" {YEAR}
Q3 structure: site:{HOST} ("layered generation" OR "relighting" OR "compositing" OR "harmonization" OR "shadow generation") "{VENUE}" {YEAR}
Q4 family follow-up: "{METHOD_FAMILY}" (CVPR OR ICCV OR ECCV OR NeurIPS OR ICML OR ICLR OR SIGGRAPH OR "SIGGRAPH Asia" OR 3DV)
```

Direct target endpoints were `https://openaccess.thecvf.com/menu`, `https://www.ecva.net/papers.php`, `https://proceedings.neurips.cc/`, `https://proceedings.mlr.press/`, `https://iclr.cc/virtual/`, `https://openreview.net/group?id=ICLR.cc`, `https://s2022.siggraph.org/`, `https://s2023.siggraph.org/`, `https://s2024.siggraph.org/`, `https://asia.siggraph.org/{YEAR}/`, `https://dl.acm.org/doi/`, `https://3dvconf.org/`, and `https://3dv.org/`. CVF-hosted 3DV pages were also checked through the CVF menu.

`Q4` was run for `DDPM`, `score SDE`, `latent diffusion`, `SDEdit`, `DreamBooth`, `ControlNet`, `DiT`, `consistency models`, `flow matching`, `SDXL`, `rectified flow transformer`, `FLUX.1`, `Qwen-Image`, and `IP-Adapter`. The first eleven acted as canonical identity/version anchors. FLUX.1, Qwen-Image, and IP-Adapter produced three pending families rather than presumed formal papers.

Paper-identity verification used these literal follow-up forms:

```text
site:openaccess.thecvf.com/content/{VENUE}{YEAR}/html "{EXACT_TITLE}"
site:proceedings.neurips.cc "{EXACT_TITLE}"
site:proceedings.mlr.press "{EXACT_TITLE}"
site:iclr.cc/virtual/{YEAR} "{EXACT_TITLE}"
site:openreview.net/forum "{EXACT_TITLE}"
site:s{YEAR}.siggraph.org "{EXACT_TITLE}"
site:dl.acm.org/doi "{EXACT_TITLE}"
```

#### Venue-topic cell outcomes

Each count is the candidate's first retained query-family cell after cross-query deduplication. A zero means no uniquely named candidate from that cell survived title-result inspection; it is not a claim that the venue has no relevant work.

| Venue | Target search/proceedings endpoints | Q1 core | Q2 control | Q3 structure | Retained decision outcome |
| --- | --- | ---: | ---: | ---: | --- |
| CVPR | `openaccess.thecvf.com`; `thecvf.com` | 6 formal | 3 formal + 1 excluded | 1 formal | 10 formal; NeIn excluded as workshop-only |
| ICCV | `openaccess.thecvf.com`; `thecvf.com` | 1 formal | 1 formal | 1 formal | 3 formal |
| ECCV | `ecva.net/papers.php`; `eurographics.org` | 0 | 1 pending | 0 named | BrushNet pending because official ECVA host is outside the current validator allowlist; adjacent 3D/video results screened qualitatively |
| NeurIPS | `proceedings.neurips.cc` | 2 formal | 0 | 0 | 2 formal |
| ICML | `proceedings.mlr.press`; `icml.cc` | 3 formal | 0 | 0 | 3 formal |
| ICLR | `iclr.cc/virtual`; `openreview.net/group?id=ICLR.cc` | 5 formal + 2 pending | 4 excluded | 0 | 5 formal; 2 submission-only pending; 4 withdrawn/desk-rejected |
| SIGGRAPH | `s2022.siggraph.org`; `s2023.siggraph.org`; `s2024.siggraph.org`; `dl.acm.org/doi` | 1 formal | 1 formal | 1 formal | 3 formal |
| SIGGRAPH Asia | `asia.siggraph.org/{YEAR}`; `dl.acm.org/doi` | 0 | 0 | 0 | No uniquely named candidate cleared the screening and scope gates |
| 3DV | `3dvconf.org`; `3dv.org`; `openaccess.thecvf.com` | 0 | 0 | 0 named | Adjacent 3D/avatar/video-only results were below the relevance threshold |

Named cell assignments for auditability:

- CVPR Q1 (6): Taming Transformers; Latent Diffusion Models; InstructPix2Pix; OmniGen; PixelDiT; HiCoGen. CVPR Q2 (4): DreamBooth; PhotoMaker; Diffusion Self-Distillation; NeIn (excluded workshop). CVPR Q3 (1): Language-Free Generative Editing.
- ICCV Q1 (1): Scalable Diffusion Models with Transformers. ICCV Q2 (1): ControlNet. ICCV Q3 (1): Layered Diffusion Brushes.
- ECCV Q2 (1): BrushNet (pending).
- NeurIPS Q1 (2): DDPM; EDM.
- ICML Q1 (3): Improved DDPM; Consistency Models; Scaling Rectified Flow Transformers.
- ICLR Q1 (7): Score SDE; SDEdit; Flow Matching; SDXL; SANA; Test-Time Evolutionary Search (pending); OneFlow (pending). ICLR Q2 (4): Rethinking Prompt Design (withdrawn); InstructMoLE (desk rejected); TIIF-Bench (withdrawn); CoTDiff (withdrawn).
- SIGGRAPH Q1 (1): Palette. SIGGRAPH Q2 (1): DragGAN. SIGGRAPH Q3 (1): LayerDiffuse.
- Cross-venue Q4 model-family follow-ups (3): FLUX.1; Qwen-Image; IP-Adapter, all pending because no allowed accepted main-conference identity was proven.

#### Retrieval, verification, and screening counts

- 37 uniquely named candidates were retained for individual identity/status screening: 26 admitted, 6 pending, and 5 individually named exclusions. Two additional broad exclusion classes—adjacent 3D/avatar/video-only results and retired Live2D scope—were recorded qualitatively rather than given misleading record counts.
- The 26 admitted papers were each matched to one authoritative accepted main-track record: CVF Open Access 13, NeurIPS proceedings 2, PMLR 3, ICLR official program/proceedings 5, and SIGGRAPH/ACM official records 3.
- Six candidates failed to reach formal admission and stayed pending: three model/report families without an allowed formal version, one ECCV host-contract mismatch, and two ICLR submissions without accepted status.
- Five individually named candidates were excluded after status/track verification: three withdrawn, one desk-rejected, and one workshop-only.
- Exact identifier/title/alias/repository comparison reduced the 26 admitted records to 26 unique method identities; no admitted duplicate was removed after final matching.
- All 26 formal records received a supplemental link/code-status pass at collection time. Review correction on the same date directly revalidated four official repositories: TencentARC/PhotoMaker, primecai/diffusion-self-distillation, NVlabs/PixelDiT, and omarAlezaby/VDC.

### Authoritative sources consulted

- CVPR and ICCV: CVF Open Access main-conference paper pages.
- ECCV: official ECVA proceedings pages were searched; a validator authority-host mismatch prevented one otherwise supported candidate from entering the formal index.
- NeurIPS: official proceedings abstract pages.
- ICML: official PMLR proceedings pages.
- ICLR: official conference virtual-program/proceedings pages; OpenReview identities were used where the authoritative record was accessible and unambiguous.
- SIGGRAPH and SIGGRAPH Asia: official conference programs/accepted-paper lists and ACM publication identities.
- 3DV: official/CVF proceedings and venue results were searched; no candidate meeting this run's scope and threshold was selected.

### Screening and decisions

- Admitted 26 unique formal records: 2020 (1), 2021 (3), 2022 (4), 2023 (7), 2024 (4), 2025 (4), and 2026 (3).
- Formal venue coverage: CVPR (10), ICCV (3), ICLR (5), ICML (3), NeurIPS (2), and SIGGRAPH (3).
- Held 6 candidates in the non-formal pending queue because acceptance or validator-compatible authority evidence was incomplete.
- Recorded 7 notable exclusion categories, including withdrawn, desk-rejected, workshop-only, and below-threshold adjacent work.
- Deduplicated using DOI/OpenReview/venue/arXiv identifiers first, then normalized titles and aliases, author/method identity, and official repository identity. The SD3/MMDiT family appears once through its ICML 2024 formal paper.

### Failed or blocked searches

- Direct OpenReview API/page retrieval intermittently returned access-denied or browser-challenge responses. Official ICLR program/proceedings pages were used when they independently established the accepted conference identity; unresolved submissions remained pending or excluded.
- Direct ACM Digital Library DOI retrieval returned bot-protection responses in this environment. Paper-specific ACM DOI records were retained as official proceedings identities where applicable, and official SIGGRAPH program/accepted-paper pages independently cross-checked the titles and venue placement.
- ECCV's official `ecva.net` host is absent from the current validator authority allowlist. BrushNet was therefore held pending instead of weakening or bypassing the deterministic gate.
- Searches with no selected result are not evidence that a venue/topic has no relevant literature; they only mean no candidate cleared every gate in this curated run.

### Reproducibility boundary

- Collection date: 2026-08-25.
- Formal output: `index/papers.json`; report: `reports/2026-08-25.md`.
- Code/model availability was classified from linked official paper/project/repository surfaces at page level. Repositories, weights, and demos were not executed.
- All taxonomy, relevance, implementation-coverage, and trend statements are labeled as curator inference in the index or report rather than venue-verified facts.

### 2026-08-25 review correction — implementation coverage

- PhotoMaker: official repository checked; inference pipeline, demos, and released adapter weights are present, but paper training code is not. Classified `official_inference_only`.
- Diffusion Self-Distillation: official repository `primecai/diffusion-self-distillation` checked; subject-preserving inference and weights are present, while training code and relighting remain unreleased. Classified `official_inference_only`.
- PixelDiT: official repository `NVlabs/PixelDiT` checked; class-to-image and text-to-image training/inference plus pretrained models are released. Classified `official_full`.
- Language-Free Generative Editing/VDC: official repository `omarAlezaby/VDC` checked; the full training-free method release contains steering-condition optimization and both inference paths. Classified `official_full`.
- DragGAN acceptance evidence now points to its paper-specific ACM proceedings DOI; the SIGGRAPH full program remains an independent cross-check.
