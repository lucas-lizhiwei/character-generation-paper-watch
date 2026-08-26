# Schema and output contract

Read this reference before writing repository artifacts. `schema/papers.schema.json` is authoritative; inspect it rather than relying on this summary if it changes.

## Formal index

`index/papers.json` is a versioned object containing `schema_version`, ISO-date `generated_at`, and a `papers` array. Every formal paper contains:

- identity: `id`, canonical `title`, `aliases`, `authors`, `year`, allowed `venue`, and `track` equal to `main`;
- `identifiers`: `doi`, `openreview`, `venue`, and `arxiv` strings (use `""` when absent);
- `acceptance_evidence`: `type` (`official_proceedings`, `official_program`, or `openreview_accepted`) and authoritative `url`;
- `urls`: required `paper`, plus `arxiv`, `project`, `code`, `demo`, `model`, and `dataset` strings (use `""` when absent);
- taxonomy arrays: `topics`, `tasks`, `architectures`, `base_models`, `training_methods`, and `conditioning_methods`;
- curation: integer `relevance_score` 3–5 and concise `relevance_rationale`;
- implementation: `code_status` and `implementation_coverage`;
- reading/storage curation: `priority`, `primary_category`, and `secondary_categories`;
- PDF storage: `pdf_status`, `pdf_path`, `pdf_source_url`, `pdf_source_type`, `pdf_sha256`, and `pdf_downloaded_date`;
- provenance: ISO dates `first_seen_date` and `last_verified_date`, `dedupe_keys`, existing `report_path`, and `notes` separating verified facts from inference.

Allowed `code_status` values are `official_full`, `official_inference_only`, `official_demo_only`, `official_placeholder`, `unofficial`, `not_found`, and `unclear`. Use stable lowercase venue-year-title IDs and useful prefixed dedupe keys. Do not omit required keys merely because a value is unavailable.

## Memory and report

`memory/seen-generative-image-papers.md` contains only formal ID–title pairs. `memory/pending-generative-image-review.md` contains non-formal candidates, current evidence, unresolved gate, and evidence needed. `memory/run-notes.md` records the search date, literal queries/templates and substitutions, sources/endpoints, venue/topic cell outcomes, candidate/count basis, acceptance and dedupe decisions, exclusions, failures/fallbacks, and reproducibility limitations.

The dated report contains these sections, in order:

1. formal new discoveries;
2. important code/model updates;
3. pending verification;
4. notable exclusions;
5. trends;
6. search coverage;
7. limitations; and
8. AI-assistance disclosure when AI materially assisted the run.

State counts that reconcile with the index and memory. Each formal discovery also reports priority, primary/secondary categories, relevance, PDF status, and PDF path. Label trends, taxonomy, priority, relevance, and implementation assessments as curator inference. Do not turn source failures or unsearched cells into negative findings.

## Validation gate

Run from the repository root:

```text
python skills/generative-image-paper-watch/scripts/validate_repository.py --repo .
python -m pytest -v
```

The first command must report a count equal to `len(papers)`. Resolve schema errors, duplicate IDs/titles/aliases/identifiers, non-authoritative acceptance evidence, forbidden venue/track values, missing or escaping report/PDF paths, invalid filename/category mappings, SHA-256 mismatches, duplicate content, and orphan PDFs before committing or pushing. PDF count is never substituted for formal paper count.
