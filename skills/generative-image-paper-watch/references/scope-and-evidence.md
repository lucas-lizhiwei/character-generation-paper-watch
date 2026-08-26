# Scope and evidence

Read this reference before classifying any candidate.

## Formal eligibility

A formal record satisfies every gate, in this order:

1. **Venue and track:** a full/main-conference paper at exactly one of CVPR, ICCV, ECCV, NeurIPS, ICML, ICLR, SIGGRAPH, SIGGRAPH Asia, or 3DV.
2. **Acceptance evidence:** an official proceedings page, official conference program, or accepted OpenReview record proves the accepted main-track identity.
3. **Relevance:** score 3–5 under the rubric below.
4. **Identity:** deduplication establishes that the work is not already represented.

Workshops, demos, tutorials, challenges, withdrawn or rejected submissions, and arXiv-only or technical reports are non-formal. A submission record does not prove acceptance. Page text must establish the paper, venue, year, accepted status, and main track; an official-looking hostname alone is insufficient.

Use venue/proceedings/program/OpenReview acceptance pages for the gate. Typical authoritative surfaces include CVF Open Access, official ECVA ECCV records, NeurIPS proceedings, PMLR, official ICLR program/proceedings, ACM or official SIGGRAPH records, and official 3DV proceedings. Use arXiv, project pages, GitHub, Hugging Face, author pages, and model cards only for supplemental identity, metadata, code, models, or datasets.

If accepted main-track status is not verified, classify the candidate as pending with its current evidence and the exact evidence still needed. FLUX, Qwen-Image, Stable Diffusion, and related model families are search terms or base-model tags; popularity and technical reports do not confer formal status.

## Relevance rubric

Score only after the venue and evidence gate passes.

| Score | Contract |
| --- | --- |
| 5 | Foundational image-generation/editing model, objective, architecture, training, sampling, latent representation, diffusion, or flow contribution. |
| 4 | Enabling personalization, LoRA/adapter, controllable generation, structural/reference conditioning, or general-purpose editing contribution. |
| 3 | Broadly transferable applied generative method for layers, relighting, compositing, harmonization, or shadows. |
| 2 | Adjacent perception, animation, video, 3D, avatar, or rendering work; pending only when transfer value needs review. |
| 1 | Tangential use of generative imagery. |
| 0 | Out of scope. |

Generic Live2D, talking-avatar, portrait-animation, motion-generation, and 3D-character papers are outside the formal scope unless their central contribution is a transferable generative-image method scoring at least 3.

