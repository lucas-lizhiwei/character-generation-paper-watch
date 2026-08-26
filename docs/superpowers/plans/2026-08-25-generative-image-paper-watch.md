# Generative Image Paper Watch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the repository as an evidence-gated top-conference generative-image paper corpus, run the first verified collection, and install a tested `generative-image-paper-watch` Codex skill.

**Architecture:** The Codex skill performs semantic discovery and verification; the repository stores the durable corpus, run memory, and reports. A JSON Schema plus a deterministic Python validator enforces venue, acceptance-evidence, deduplication, and path invariants, while GitHub Actions runs the same quality gate on every proposed change.

**Tech Stack:** Markdown, JSON Schema Draft 2020-12, Python 3.11, pytest, jsonschema, Git, GitHub Actions, GitHub plugin, Codex personal skills.

**Spec:** `docs/superpowers/specs/2026-08-25-generative-image-paper-watch-design.md`

## Global Constraints

- Formal entries are limited to main-conference papers from CVPR, ICCV, ECCV, NeurIPS, ICML, ICLR, SIGGRAPH, SIGGRAPH Asia, and 3DV.
- An official proceedings page, official conference program, or accepted OpenReview record is required for every formal entry.
- Workshops, demos, tutorials, challenges, withdrawn/rejected submissions, and arXiv-only reports never enter `index/papers.json`.
- Relevance must score at least 3/5 after the venue gate passes.
- Initial coverage is 2020–2026, prioritizing 2024–2026, without claiming systematic completeness.
- Existing GitHub issues remain unchanged.
- No replacement scheduled task is created; the compatibility prompt points future tasks to `$generative-image-paper-watch`.
- The personal skill installation must not delete or overwrite unrelated skills.

## File Structure

- `README.md`: public repository contract and topic/venue overview.
- `prompts/agent-instructions.md`: compatibility prompt for old agent configurations.
- `schema/papers.schema.json`: formal index schema.
- `index/papers.json`: versioned corpus object with `papers` array.
- `memory/seen-generative-image-papers.md`: confirmed-entry memory.
- `memory/pending-generative-image-review.md`: non-formal verification queue.
- `memory/run-notes.md`: reproducible search log.
- `reports/2026-08-25.md`: first rebuilt scan.
- `skills/generative-image-paper-watch/SKILL.md`: concise skill router.
- `skills/generative-image-paper-watch/agents/openai.yaml`: skill UI metadata.
- `skills/generative-image-paper-watch/references/scope-and-evidence.md`: eligibility and source authority.
- `skills/generative-image-paper-watch/references/workflow-and-dedup.md`: run workflow, scoring, dedupe, sync.
- `skills/generative-image-paper-watch/references/schema-and-output.md`: data and report contract.
- `skills/generative-image-paper-watch/scripts/validate_repository.py`: deterministic quality gate.
- `tests/conftest.py`: temporary repository factory.
- `tests/test_validate_repository.py`: schema and invariant tests.
- `.github/workflows/validate-paper-watch.yml`: CI quality gate.

---

### Task 1: Capture Skill RED Baseline

**Files:**
- Create during execution: local test notes outside the repository worktree; do not commit baseline transcripts containing incidental environment details.

**Interfaces:**
- Consumes: the approved design and three realistic paper-watch requests.
- Produces: a baseline failure matrix containing exact decisions, omissions, and rationalizations that the skill must correct.

- [ ] **Step 1: Define three baseline scenarios without exposing the future skill**

Scenario A asks for five recent diffusion papers and pressures the worker to include a highly relevant arXiv-only FLUX/Qwen-Image report because the user is in a hurry. Scenario B supplies the same paper under an arXiv title and a conference title and pressures the worker to count both. Scenario C asks for Live2D/talking-avatar papers and pressures the worker to preserve the old scope because the repository name still says character generation.

- [ ] **Step 2: Run each scenario with a fresh subagent that does not receive the skill**

Record whether it verifies venue acceptance, enforces the nine-venue allowlist, deduplicates versions, excludes old-scope work, and separates formal from pending records.

- [ ] **Step 3: Verify RED and capture exact failures**

Expected RED: at least one scenario violates or omits a required invariant. If all controls already comply, reframe the scenarios with stronger time, authority, and sunk-cost pressure; do not author redundant guidance for behavior that does not fail.

- [ ] **Step 4: Commit**

No repository commit. Store only the distilled failure categories needed by Task 6.

---

### Task 2: Write Validator Tests First

**Files:**
- Create: `tests/conftest.py`
- Create: `tests/test_validate_repository.py`

**Interfaces:**
- Consumes: repository root path and JSON documents written by test fixtures.
- Produces: tests for `validate_repository(repo_root: Path) -> list[str]` and the CLI exit contract.

- [ ] **Step 1: Create the temporary repository factory**

Implement a pytest fixture that writes `schema/papers.schema.json`, `index/papers.json`, and the referenced report path into `tmp_path`, returning the root path and a mutable valid-paper dictionary.

- [ ] **Step 2: Write failing tests for valid and invalid corpus behavior**

Cover: a valid eligible paper; arXiv-only evidence rejection; forbidden venue rejection; relevance score below 3 rejection; duplicate IDs; normalized-title collision; duplicate DOI/OpenReview/arXiv identifiers; non-authoritative acceptance evidence; and missing `report_path`.

- [ ] **Step 3: Write a failing CLI test**

Run `python skills/generative-image-paper-watch/scripts/validate_repository.py --repo <fixture>` and assert exit code `0` with `validated 1 paper` for valid data and non-zero with actionable messages for invalid data.

- [ ] **Step 4: Run tests and verify RED**

Run: `python -m pytest tests/test_validate_repository.py -v`

Expected: collection/import failure because `validate_repository.py` does not exist.

- [ ] **Step 5: Commit**

```powershell
git add -- tests/conftest.py tests/test_validate_repository.py
git commit -m "test: define paper corpus validation contract"
```

---

### Task 3: Implement Schema and Deterministic Validator

**Files:**
- Create: `schema/papers.schema.json`
- Create: `skills/generative-image-paper-watch/scripts/validate_repository.py`
- Modify: `tests/conftest.py`

**Interfaces:**
- Consumes: `--repo PATH`; `schema/papers.schema.json`; `index/papers.json`.
- Produces: `validate_repository(repo_root: Path) -> list[str]`; CLI exit `0` on success and `1` with one error per line on failure.

- [ ] **Step 1: Add the minimal Draft 2020-12 schema**

Require top-level `schema_version`, `generated_at`, and `papers`. Require every paper's identity, venue/year/track, identifiers, acceptance evidence, URLs, taxonomy arrays, relevance, code status, dates, dedupe keys, report path, and notes. Constrain venue to the nine allowed values and relevance to integers 3–5.

- [ ] **Step 2: Implement schema loading and validation**

Use `jsonschema.Draft202012Validator.iter_errors` and return stable, path-qualified messages rather than raising on the first record.

- [ ] **Step 3: Implement cross-record invariants**

Normalize titles with Unicode NFKC, lowercase alphanumerics, and whitespace folding. Reject duplicate IDs, normalized titles/aliases, non-empty DOI/OpenReview/venue/arXiv identifiers, missing report paths, forbidden venue labels, and acceptance URLs outside authoritative conference/proceedings/OpenReview hosts.

- [ ] **Step 4: Run focused tests and verify GREEN**

Run: `python -m pytest tests/test_validate_repository.py -v`

Expected: all validator tests pass.

- [ ] **Step 5: Run formatting and syntax checks**

Run: `python -m compileall skills/generative-image-paper-watch/scripts tests`

Expected: exit code `0`.

- [ ] **Step 6: Commit**

```powershell
git add -- schema/papers.schema.json skills/generative-image-paper-watch/scripts/validate_repository.py tests/conftest.py
git commit -m "feat: enforce formal paper corpus invariants"
```

---

### Task 4: Reset the Old Corpus and Repository Contract

**Files:**
- Delete: `reports/2026-05-18.md`
- Delete: `reports/2026-07-06.md`
- Delete: `reports/2026-07-13.md`
- Delete: `reports/YYYY-MM-DD.md`
- Delete: `memory/seen-character-generation-papers.md`
- Delete: `memory/pending-character-generation-review.md`
- Delete: `scripts/paper_watch.py`
- Delete: `.github/workflows/scheduled-watch.yml`
- Rewrite: `README.md`
- Rewrite: `prompts/agent-instructions.md`
- Rewrite: `index/papers.json`
- Rewrite: `memory/run-notes.md`
- Create: `memory/seen-generative-image-papers.md`
- Create: `memory/pending-generative-image-review.md`
- Create: `.github/workflows/validate-paper-watch.yml`

**Interfaces:**
- Consumes: the approved design and validator contract.
- Produces: an empty but valid new corpus and a truthful agent/CI architecture.

- [ ] **Step 1: Remove the explicitly approved old current-tree content**

Use `apply_patch` to delete only the listed legacy files. Preserve `.git`, design/plan documents, and GitHub issues.

- [ ] **Step 2: Write an empty valid corpus and reset memory**

Set `schema_version` to `1.0.0`, `generated_at` to `2026-08-25`, and `papers` to `[]`. The seen and pending files explain their new roles and contain no migrated Live2D entries. Run notes begin with a reset record dated `2026-08-25`.

- [ ] **Step 3: Rewrite README and compatibility prompt**

Document the nine venues, eligibility gate, new topic scope, relevance rubric, source hierarchy, repository layout, dedupe policy, report format, and `$generative-image-paper-watch` migration path.

- [ ] **Step 4: Replace the scheduled crawler with CI validation**

Trigger on pull requests, pushes to `main`, and manual dispatch. Install `pytest` and `jsonschema`, run the validator, then run the full tests. Do not retain a scheduled semantic-research claim.

- [ ] **Step 5: Verify the reset**

Run: `python skills/generative-image-paper-watch/scripts/validate_repository.py --repo .`

Expected: `validated 0 papers`.

Run: `rg -n -i "text-to-live2d|talking avatar|portrait animation|seen-character-generation|pending-character-generation" README.md prompts index memory reports .github skills`

Expected: no stale core-scope or legacy-path matches; explicit exclusion/migration explanations are reviewed manually and allowed.

- [ ] **Step 6: Commit**

Stage only the files listed in this task and commit with `refactor: reset repository for generative image papers`.

---

### Task 5: Run the First Authoritative Literature Collection

**Files:**
- Create working evidence matrix during execution outside the formal index until each candidate passes all gates.
- Modify after verification: `index/papers.json`
- Modify after verification: `memory/seen-generative-image-papers.md`
- Modify after verification: `memory/pending-generative-image-review.md`
- Modify after verification: `memory/run-notes.md`
- Create after verification: `reports/2026-08-25.md`

**Interfaces:**
- Consumes: official venue/proceedings/OpenReview pages plus supplemental arXiv/project/GitHub metadata.
- Produces: a verified 2020–2026 formal corpus, pending queue, reproducible run log, and Chinese report.

- [ ] **Step 1: Build the venue/topic search matrix**

For each allowed venue, search combinations covering diffusion/latent diffusion, flow matching/rectified flow, text-to-image, image editing, DiT/MMDiT, personalization/DreamBooth/LoRA/adapters, ControlNet/structural control, reference conditioning/IP-Adapter, layered generation, relighting, compositing, harmonization, and shadow generation.

- [ ] **Step 2: Seed canonical anchors and recent candidates**

Start with known method families such as DDPM, latent diffusion, DreamBooth, ControlNet, DiT, consistency/flow methods, personalization, controllable generation, and image editing. Treat FLUX and Qwen-Image as search/model-family terms rather than automatically eligible papers.

- [ ] **Step 3: Verify acceptance and identity from authoritative sources**

For every candidate, record the authoritative venue URL, venue/year/track, title, authors, and identifiers. Exclude any candidate whose main-conference acceptance cannot be confirmed.

- [ ] **Step 4: Enrich eligible records**

Use arXiv, project pages, official GitHub repositories, and Hugging Face only for supplemental links, model/code availability, and implementation coverage. Mark inference separately from verified facts.

- [ ] **Step 5: Deduplicate and score**

Apply exact identifiers first, then normalized titles/aliases, author overlap, method/project identity, and code repository identity. Score 0–5; only eligible scores 3–5 enter the corpus.

- [ ] **Step 6: Write the first index, report, and memory**

The report sections are: formal new discoveries, important code/model updates, pending verification, notable exclusions, trends, search coverage, and limitations. Run notes list sources and failed/blocked searches. The seen file mirrors formal IDs and titles only.

- [ ] **Step 7: Validate the research artifacts**

Run: `python skills/generative-image-paper-watch/scripts/validate_repository.py --repo .`

Expected: exit code `0` and a paper count equal to the formal index length.

- [ ] **Step 8: Commit**

```powershell
git add -- index/papers.json memory/seen-generative-image-papers.md memory/pending-generative-image-review.md memory/run-notes.md reports/2026-08-25.md
git commit -m "data: initialize verified generative image paper corpus"
```

---

### Task 6: Author the Replacement Skill from RED Evidence

**Files:**
- Create: `skills/generative-image-paper-watch/SKILL.md`
- Create: `skills/generative-image-paper-watch/agents/openai.yaml`
- Create: `skills/generative-image-paper-watch/references/scope-and-evidence.md`
- Create: `skills/generative-image-paper-watch/references/workflow-and-dedup.md`
- Create: `skills/generative-image-paper-watch/references/schema-and-output.md`

**Interfaces:**
- Consumes: Task 1 failure matrix, approved design, schema, validator CLI, and first-run artifacts.
- Produces: an automatically discoverable, self-contained skill whose detailed references correct observed baseline failures.

- [ ] **Step 1: Complete the existing skill directory without reinitializing it**

Task 3 already creates the skill's `scripts/` directory and validator. Add `SKILL.md`, `agents/openai.yaml`, and the three references directly with `apply_patch`; do not run the initializer over an existing skill directory. Do not add examples, assets, or unused placeholders.

- [ ] **Step 2: Write discriminating frontmatter and concise routing**

Use name `generative-image-paper-watch`. The description starts with `Use when` and names paper discovery, verification, top-conference generative-image literature, corpus refresh, and Stable Diffusion/FLUX/Qwen-Image-related tracking without summarizing the workflow.

- [ ] **Step 3: Write the three focused references**

Put venue/source rules in `scope-and-evidence.md`; observed dedupe/scoping failures plus workflow/repository synchronization in `workflow-and-dedup.md`; and the exact schema/report/memory contract in `schema-and-output.md`. Use positive output contracts for shape failures and explicit prohibitions only for observed gate-skipping rationalizations.

- [ ] **Step 4: Write UI metadata**

Set quoted `display_name`, a 25–64 character `short_description`, and a one-sentence `default_prompt` that explicitly invokes `$generative-image-paper-watch`. Keep implicit invocation enabled and do not add an MCP dependency because ordinary web and GitHub capability selection remains runtime-specific.

- [ ] **Step 5: Run static skill validation**

Run: `python C:/Users/lizhi/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/generative-image-paper-watch`

Expected: validation success with no scaffold placeholders.

- [ ] **Step 6: Commit**

Stage only the skill entrypoint, metadata, and references; the validator script was committed in Task 3. Commit with `feat: add generative image paper watch skill`.

---

### Task 7: Verify and Refactor Skill Behavior

**Files:**
- Modify if failures require it: `skills/generative-image-paper-watch/SKILL.md`
- Modify if failures require it: `skills/generative-image-paper-watch/references/*.md`

**Interfaces:**
- Consumes: the same scenarios from Task 1 and the completed skill.
- Produces: GREEN behavior matrix showing correct eligibility, deduplication, scope, and output separation under pressure.

- [ ] **Step 1: Run the three original scenarios with fresh subagents given the skill**

Require each worker to act, not merely recite rules. Record formal/pending decisions, evidence selection, dedupe result, and old-scope treatment.

- [ ] **Step 2: Verify GREEN**

Expected: all workers enforce the venue gate, reject arXiv-only formal inclusion, merge alternate versions, exclude generic Live2D/avatar work, and preserve supplemental metadata without elevating it to acceptance evidence.

- [ ] **Step 3: Refactor only observed loopholes**

If a worker invents a new rationalization, add the smallest targeted counter or positive contract, then rerun that scenario. Do not accumulate hypothetical universal rules.

- [ ] **Step 4: Run one counter-example scenario**

Ask for a generic explanation of ICLR versus ICML with no paper-watch or corpus task. Expected: the skill does not hijack the request.

- [ ] **Step 5: Re-run static and repository validation**

Run the skill `quick_validate.py`, repository validator, and full pytest suite.

- [ ] **Step 6: Commit**

If refactoring changed files, stage only those paths and commit with `fix: harden paper watch skill gates`. If no files changed, record the GREEN evidence without an empty commit.

---

### Task 8: Install the Skill and Complete GitHub Delivery

**Files:**
- Install copy: `C:/Users/lizhi/.codex/skills/generative-image-paper-watch/`
- No additional repository files unless verification exposes a defect.

**Interfaces:**
- Consumes: verified repository skill package and clean feature branch.
- Produces: installed personal skill, pushed branch, and one draft PR against `main`.

- [ ] **Step 1: Run the full completion gate**

Run: `python -m pytest -v`

Run: `python skills/generative-image-paper-watch/scripts/validate_repository.py --repo .`

Run: `python C:/Users/lizhi/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/generative-image-paper-watch`

Run: `git diff --check` and `git status --short --branch`.

Expected: zero test failures, validator success, skill validation success, no whitespace errors, and only intentional changes.

- [ ] **Step 2: Install without overwriting unrelated skills**

Verify the exact destination. If it does not exist, copy the verified skill directory to `C:/Users/lizhi/.codex/skills/generative-image-paper-watch/`. If it appears during execution, compare it and stop for user direction rather than replacing unknown work.

- [ ] **Step 3: Validate the installed copy**

Run `quick_validate.py` against the installed path and compare hashes of the repository and installed skill files.

- [ ] **Step 4: Inspect final history and remote state**

Confirm the branch is not `main`, the worktree is clean, the remote head has not diverged unexpectedly, and no matching open PR already exists.

- [ ] **Step 5: Push and create the draft PR**

Push `refactor/generative-image-paper-watch` and create exactly one draft PR with base `main` and head `refactor/generative-image-paper-watch`. Summarize the destructive reset, eligibility policy, first-run corpus, skill installation, tests, and known coverage limitations.

- [ ] **Step 6: Final evidence-backed handoff**

Report deleted, rewritten, and added files; formal first-run papers and exclusions; exact validation counts; commit/PR links; installed skill path; and the fact that no scheduled task was created or modified.

