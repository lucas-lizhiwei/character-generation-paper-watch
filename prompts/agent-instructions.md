# Generative Image Paper Watch — compatibility fallback

Use `$generative-image-paper-watch` for every literature-watch, corpus-refresh, or verified generative-image paper request. This document is the complete human-readable fallback when that skill is unavailable, and replaces prior copied agent instructions.

## Scope

Track generative image modeling and editing: foundation text-to-image and image-editing models; diffusion, latent diffusion, rectified flow, and flow matching; U-Net, DiT, and MMDiT; LoRA, adapters, personalization, DreamBooth, and subject-driven generation; ControlNet and structural conditioning; IP-Adapter and reference conditioning; layered generation, relighting, compositing, harmonization, and shadow generation. Stable Diffusion, FLUX, and Qwen-Image are search/model-family terms, not automatic inclusion grounds.

## Formal admission rule

Add a paper to `index/papers.json` only when it is a full/main-conference paper at CVPR, ICCV, ECCV, NeurIPS, ICML, ICLR, SIGGRAPH, SIGGRAPH Asia, or 3DV; its acceptance is verified from official proceedings, an official program, or an accepted OpenReview record; it has relevance score 3–5; and it is deduplicated against the formal corpus.

Keep workshops, demos, tutorials, challenges, withdrawn or rejected submissions, and arXiv-only reports out of the formal index. Use arXiv, project pages, official GitHub repositories, Hugging Face, and author pages to enrich an eligible record or document a clearly non-formal pending candidate, never as acceptance proof.

## Relevance scoring

- 5: foundational generative-image model, objective, architecture, training, sampling, latent representation, diffusion, or flow-matching contribution.
- 4: enabling personalization, adapter, controllable-generation, structural/reference-conditioning, or general-purpose editing contribution.
- 3: broadly transferable applied generative method for layered generation, relighting, compositing, harmonization, or shadows.
- 2: adjacent work; retain only in pending notes.
- 1: tangential.
- 0: out of scope.

Evaluate venue eligibility before relevance. A relevant paper without verified eligible acceptance remains out of the formal corpus.

## On-demand workflow

1. Read `schema/papers.schema.json`, `index/papers.json`, the seen list, pending list, and run notes.
2. Search official venue and proceedings sources first across the covered topic families.
3. Verify the venue, main-conference track, acceptance, bibliographic identity, and authoritative evidence URL.
4. Add supplemental metadata and code status only after eligibility is established.
5. Deduplicate using DOI, OpenReview/venue/arXiv identifiers, normalized titles and aliases, author overlap, method/project identity, and code-repository identity.
6. Score relevance and record a concise rationale; unresolved acceptance, identity, or relevance belongs in pending notes.
7. Update the formal index, seen/pending memory, run notes, and a dated report as applicable.
8. Run `python skills/generative-image-paper-watch/scripts/validate_repository.py --repo .` and the full test suite before committing.

Each report should separate formal discoveries, important code/model updates, pending verification, notable exclusions, trends, search coverage, and limitations. Record failed or blocked sources in run notes; do not convert them into a claim of no results.

The repository automation is validation only: it validates the corpus and runs tests on pull requests, pushes to `main`, and manual dispatch. It does not perform scheduled semantic research. Git history is the archive for the retired corpus; do not migrate old entries into the new files solely because their keywords overlap.
