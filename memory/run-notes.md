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

- Venue families searched: CVPR, ICCV, ECCV, NeurIPS, ICML, ICLR, SIGGRAPH, SIGGRAPH Asia, and 3DV.
- Query families covered: diffusion and latent diffusion; flow matching and rectified flow; text-to-image; image editing; DiT and MMDiT; personalization, DreamBooth, LoRA, and adapters; ControlNet and structural control; reference conditioning and IP-Adapter; layered generation; relighting; compositing; harmonization; and shadow generation.
- Canonical method-family seeds included DDPM, score SDEs, latent diffusion, SDEdit, DreamBooth, ControlNet, DiT, consistency models, flow matching, SDXL, and rectified-flow transformers. FLUX and Qwen-Image were searched as model families rather than presumed eligible papers.

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
- Direct ACM Digital Library DOI retrieval returned bot-protection responses in this environment. SIGGRAPH eligibility was cross-checked against official conference program/accepted-paper pages, while DOI identities remain supplemental canonical links.
- ECCV's official `ecva.net` host is absent from the current validator authority allowlist. BrushNet was therefore held pending instead of weakening or bypassing the deterministic gate.
- Searches with no selected result are not evidence that a venue/topic has no relevant literature; they only mean no candidate cleared every gate in this curated run.

### Reproducibility boundary

- Collection date: 2026-08-25.
- Formal output: `index/papers.json`; report: `reports/2026-08-25.md`.
- Code/model availability was classified from linked official paper/project/repository surfaces at page level. Repositories, weights, and demos were not executed.
- All taxonomy, relevance, implementation-coverage, and trend statements are labeled as curator inference in the index or report rather than venue-verified facts.
