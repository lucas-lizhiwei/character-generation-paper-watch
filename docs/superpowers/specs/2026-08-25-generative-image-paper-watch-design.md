# Generative Image Paper Watch Redesign

## Objective

Replace the repository's Live2D and character-generation focus with a reusable, evidence-gated tracker for generative image modeling and editing papers. The formal corpus must contain only main-conference papers from CVPR, ICCV, ECCV, NeurIPS, ICML, ICLR, SIGGRAPH, SIGGRAPH Asia, and 3DV.

The redesign also delivers and installs a personal Codex skill named `generative-image-paper-watch` so the recurring research workflow no longer depends on a monolithic copied prompt.

## Scope

The core research scope is:

- foundation text-to-image and image-editing models;
- diffusion and latent diffusion;
- rectified flow and flow matching;
- U-Net, DiT, and MMDiT architectures;
- LoRA, adapters, personalization, DreamBooth, and subject-driven generation;
- ControlNet and other structural conditioning;
- IP-Adapter and reference-conditioned generation;
- image editing, layered generation, relighting, compositing, and shadow generation;
- methods built on or directly relevant to Stable Diffusion, FLUX, and Qwen-Image.

Generic Live2D, talking-avatar, portrait-animation, motion-generation, and 3D-character work is out of core scope unless the paper's central contribution is a transferable generative-image method that passes the relevance threshold.

## Publication Eligibility Gate

A paper enters `index/papers.json` only when all conditions hold:

1. It is a full/main-conference paper at one of the nine allowed venues.
2. Acceptance is confirmed by an official proceedings page, official conference program, or an accepted OpenReview record.
3. It scores at least 3/5 under the relevance rubric.
4. Its identity is deduplicated against the existing formal index.

Workshops, demos, tutorials, challenges, withdrawn submissions, rejected submissions, and arXiv-only reports are excluded from the formal index. arXiv, project pages, GitHub, Hugging Face, and author pages may supplement metadata and code status but cannot establish eligibility by themselves.

FLUX and Qwen-Image remain watched model families and search terms. A model report without an eligible conference version is not itself a formal paper entry.

## Relevance Rubric

- **5 — foundational:** core model, objective, architecture, training, sampling, latent representation, diffusion, or flow-matching contribution for image generation/editing.
- **4 — enabling:** personalization, LoRA/adapter, controllable generation, structural/reference conditioning, or general-purpose editing contribution.
- **3 — applied generative method:** layered generation, relighting, compositing, harmonization, or shadow generation where the generative method is central and broadly transferable.
- **2 — adjacent:** supporting perception, animation, video, 3D, avatar, or rendering work with indirect value. Keep only in pending notes when acceptance or transfer value needs review.
- **1 — tangential:** generative imagery is incidental.
- **0 — out of scope.**

The venue gate is evaluated before relevance. A highly relevant arXiv-only paper remains ineligible.

## Repository Architecture

The rebuilt repository contains:

- `README.md`: public purpose, venue policy, topic map, repository structure, and contribution rules.
- `prompts/agent-instructions.md`: human-readable compatibility prompt and migration entrypoint to the skill.
- `skills/generative-image-paper-watch/`: installable skill package with `SKILL.md`, UI metadata, focused references, and the deterministic repository validator.
- `schema/papers.schema.json`: machine-readable schema for the formal corpus.
- `index/papers.json`: reset formal index using a versioned top-level object and a `papers` array.
- `memory/seen-generative-image-papers.md`: compact human-readable record of confirmed formal entries.
- `memory/pending-generative-image-review.md`: candidates awaiting acceptance, identity, or relevance verification; never treated as formal entries.
- `memory/run-notes.md`: reproducible search coverage, sources, queries, exclusions, and anomalies.
- `reports/2026-08-25.md`: the first rebuilt run.
- `.github/workflows/validate-paper-watch.yml`: push/PR quality gate; it does not pretend to perform semantic literature research.
- `tests/`: validator and corpus-invariant tests.

Old dated reports, the old raw-array index, Live2D memory files, the empty `paper_watch.py`, and the misleading scheduled crawler workflow are removed from the current tree. Git history remains available. Existing GitHub issues are not modified.

## Paper Schema

Each formal paper record includes:

- stable `id` and normalized `title`;
- `aliases`, `authors`, `year`, `venue`, `track`, and publication identifiers;
- `acceptance_evidence` with evidence type and authoritative URL;
- paper, arXiv, project, code, demo, model, and dataset URLs where available;
- controlled topic, task, architecture, base-model, training-method, and conditioning-method tags;
- `relevance_score` and a concise `relevance_rationale`;
- official-code status and implementation coverage;
- first-seen and last-verified dates;
- dedupe keys and the originating report path;
- notes that distinguish verified facts from inference.

The JSON Schema constrains venue enums, score range, date format, URL format, required evidence, and allowed code-status values. The validator also checks invariants that JSON Schema alone cannot express, including unique IDs, normalized-title collisions, duplicate external identifiers, valid report paths, and the absence of forbidden venue/source labels.

## Discovery and Verification Workflow

Each run follows this data flow:

1. Read the schema, formal index, seen list, pending list, and run notes.
2. Search official venue/proceedings sources first using topic families and model aliases.
3. Confirm acceptance before extracting supplemental metadata.
4. Use arXiv/project/GitHub/Hugging Face only to enrich an eligible record or to populate a clearly non-formal pending candidate.
5. Deduplicate by DOI, OpenReview/venue ID, arXiv ID, normalized title, aliases, method name, author overlap, and project/code identity.
6. Score relevance and record the rationale.
7. Update the index, seen/pending memory, run notes, and one report for the run date.
8. Run schema and repository validation before any commit or push.

If acceptance cannot be verified, the item stays out of the formal index. If two records may describe the same work, neither is added as a second formal entry until identity is resolved. Network or source failures are recorded in run notes rather than silently treated as no results.

## First Rebuilt Run

The initial corpus covers 2020 through 2026. It combines canonical historical anchors with recent accepted papers, prioritizing 2024–2026. Coverage is recorded per venue and topic family; the report must not claim systematic completeness.

The first run produces only entries whose venue acceptance and bibliographic identity can be verified from authoritative sources. Older Live2D records are not migrated merely because they contain diffusion-related keywords.

## Skill Design and Replacement

The skill is named `generative-image-paper-watch` and remains eligible for automatic discovery. Its description targets requests to discover, verify, summarize, refresh, or maintain top-conference generative-image papers and excludes generic image-model explanations that do not require a literature-watch workflow.

`SKILL.md` stays concise and routes to three focused references:

- `references/scope-and-evidence.md` for venue, inclusion, and source authority rules;
- `references/workflow-and-dedup.md` for discovery, deduplication, scoring, and repository synchronization;
- `references/schema-and-output.md` for record fields, reports, memory, and validation.

The package includes `agents/openai.yaml` and a validator script. It is tested with baseline and skill-enabled scenarios, validated with the bundled skill validator, then copied to the personal Codex skills directory. Because no old Live2D skill exists locally, installation creates the new skill without deleting unrelated personal configuration.

The compatibility prompt tells existing scheduled agents to invoke `$generative-image-paper-watch`. No new scheduled task is created because no matching local task exists and no cadence change was requested.

## Testing and Delivery

Verification includes:

- validator tests written before the validator implementation;
- fixtures for eligible papers, arXiv-only rejection, forbidden venues, duplicate IDs/titles/identifiers, invalid evidence, and missing report paths;
- JSON Schema validation of the rebuilt corpus;
- repository-wide searches for stale Live2D/character-generation core language;
- skill RED/GREEN behavior scenarios and `quick_validate.py`;
- a clean worktree diff and a fresh full test run.

Changes are committed on `refactor/generative-image-paper-watch`, pushed to the existing repository, and published as a draft pull request against `main`. The final handoff lists deleted, rewritten, and added files; formal first-run discoveries; exclusions; validation evidence; the installed skill path; and any source-coverage limitations.

