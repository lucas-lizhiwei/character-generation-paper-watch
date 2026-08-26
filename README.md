# Generative Image Paper Watch

An evidence-gated corpus of top-conference papers on generative image modeling and editing. The formal corpus records only papers whose venue, main-conference status, acceptance evidence, relevance, and identity have been verified.

## Formal-corpus eligibility

A paper belongs in `index/papers.json` only when all of these conditions hold:

1. It is a full/main-conference paper at CVPR, ICCV, ECCV, NeurIPS, ICML, ICLR, SIGGRAPH, SIGGRAPH Asia, or 3DV.
2. Acceptance is established by official proceedings, an official conference program, or an accepted OpenReview record.
3. It scores at least 3/5 for relevance.
4. It is not a duplicate of an existing formal record.

Workshops, demos, tutorials, challenges, withdrawn or rejected submissions, and arXiv-only reports do not enter the formal corpus. Git history retains the pre-reset materials; they are not migrated into the current corpus.

## Research scope and relevance

The watch covers foundation text-to-image and image-editing models; diffusion and latent diffusion; rectified flow and flow matching; U-Net, DiT, and MMDiT; LoRA, adapters, personalization, DreamBooth, and subject-driven generation; ControlNet and structural conditioning; IP-Adapter and reference conditioning; plus image editing, layered generation, relighting, compositing, and shadow generation. Stable Diffusion, FLUX, and Qwen-Image are watched model families and search terms, not automatic formal entries.

Score papers after the venue gate:

| Score | Meaning |
| --- | --- |
| 5 | Foundational image-generation or editing model, objective, architecture, training, sampling, latent representation, diffusion, or flow-matching contribution. |
| 4 | Enabling personalization, adapter, controllable-generation, structural/reference-conditioning, or general-purpose editing contribution. |
| 3 | Transferable applied generative method for layered generation, relighting, compositing, harmonization, or shadows. |
| 2 | Adjacent work; retain only in the pending review notes. |
| 1 | Tangential. |
| 0 | Out of scope. |

## Evidence and sources

Use official venue, proceedings, program, and accepted OpenReview pages first to prove eligibility. Then use arXiv, project pages, official code repositories, Hugging Face, and author pages only to enrich metadata and code status. Supplemental sources never replace acceptance evidence.

## Repository layout

```text
├── index/papers.json                         # versioned formal corpus
├── schema/papers.schema.json                 # machine-readable record contract
├── papers/                                   # canonical PDFs, one per formal record when available
├── reports/                                  # dated run reports, once formal records exist
├── memory/seen-generative-image-papers.md    # compact confirmed-entry list
├── memory/pending-generative-image-review.md # non-formal verification queue
├── memory/run-notes.md                       # sources, coverage, exclusions, anomalies
├── prompts/agent-instructions.md             # compatibility fallback and skill entrypoint
├── skills/generative-image-paper-watch/      # skill and repository validator
├── tests/                                    # validator tests
└── .github/workflows/validate-paper-watch.yml # validation-only CI
```

`index/papers.json` is a versioned object with `schema_version`, `generated_at`, and `papers`. Each formal record must satisfy the JSON Schema and the deterministic repository validator.

Every formal record also carries an independent P1/P2/P3 reading priority, one primary PDF category, optional secondary categories, and explicit PDF storage metadata. A paper remains formal when a PDF download fails; only `pdf_status=stored` permits a non-empty path, SHA-256, and download date. The validator enforces one canonical file per stored work and rejects missing, malformed, misnamed, misplaced, duplicate, or orphan PDFs.

## Deduplication

Before adding a formal record, compare DOI, OpenReview ID, venue ID, arXiv ID, normalized title and aliases, method/project identity, author overlap, and code-repository identity. Alternate versions of the same work are one canonical record. Unresolved collisions stay in the pending queue rather than becoming duplicate formal records.

## Reports and maintenance

Each dated report records formal discoveries, important code or model updates, pending verification, notable exclusions, trends, search coverage, and limitations. Run notes must record source coverage and failures rather than interpreting unavailable sources as no results.

The GitHub workflow performs repository validation and tests only. Semantic literature discovery and verification are performed on demand through the skill; this repository does not claim an automated research crawler.

## Migration entrypoint

For a paper-watch request, use `$generative-image-paper-watch`. The complete human-readable fallback for environments where the skill cannot load is in [prompts/agent-instructions.md](prompts/agent-instructions.md). It preserves the same evidence gate, scope, deduplication, corpus, memory, report, and validation rules.
