# Workflow and deduplication

Read this reference for discovery, refresh, identity resolution, and repository synchronization.

## Discovery and verification

1. Read the schema, formal index, seen list, pending list, run notes, and current report.
2. Build a venue × year × topic query matrix. Cover all nine allowed venues and relevant families such as diffusion/latent diffusion, flow matching/rectified flow, text-to-image, editing, DiT/MMDiT, personalization/LoRA/adapters, ControlNet, reference conditioning/IP-Adapter, layers, relighting, compositing, harmonization, and shadows.
3. Search official venue and proceedings surfaces first. Record literal query strings, hosts/endpoints, date and year range, per-cell outcomes, and candidate counts that have a defined counting basis.
4. Verify accepted main-track identity before enrichment. Put unresolved candidates in pending.
5. Enrich eligible identities from arXiv, project, official repository, model, demo, and dataset pages. Distinguish source-verified facts from curator inference.
6. Deduplicate, score relevance, write all artifacts, then validate.

Log blocked or failed sources and the fallback used. A zero-result cell means only that no retained candidate cleared the stated screening in that run; it is not proof that the venue or topic has no relevant work. Do not claim systematic completeness unless the search design supports it.

## Canonical identity contract

Compare in this order:

1. DOI, OpenReview ID, venue ID, and arXiv ID;
2. normalized canonical title and every alias;
3. method/project name and author overlap; and
4. project, code-repository, model, or dataset identity.

An arXiv title and a conference title for the same work produce one canonical formal record. Prefer the accepted conference title and venue identity; retain the preprint title/ID as aliases and supplemental identifiers. If a collision remains unresolved, do not create a second formal record: describe the identity question in pending notes.

## Repository synchronization

Treat the formal index as the source of truth. In the same run:

- update `index/papers.json` and its `generated_at` date;
- make the seen list mirror formal IDs and titles only;
- remove resolved items from pending and add unresolved candidates with evidence needed;
- append reproducible coverage, decisions, failures, and anomalies to run notes; and
- write or update exactly one report for the run date, with every formal `report_path` pointing to an existing report.

For an approved scope reset, delete the identified legacy current-tree index, reports, memory, prompts, scripts, and workflows and rebuild only the approved replacement artifacts. **Git history is the archive. Do not fabricate a new current-tree legacy archive, preserve excluded records behind a `legacy` flag, or carry retired counts and claims into current outputs unless the user explicitly requests a new archive.** An empty formal corpus is valid.
