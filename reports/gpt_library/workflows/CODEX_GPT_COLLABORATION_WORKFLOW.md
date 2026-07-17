# Codex / GPT WorldQuant Collaboration Workflow

## Purpose

This is the canonical five-stage handoff contract for WorldQuant research. It keeps
large deterministic work in Codex and bounded analysis/generation in GPT, with an
auditable path from source material to official backtest evidence.

## Roles

- **User:** chooses research goals, supplies completed-batch research packs, approves
  material production/runtime changes, and performs any manual Alpha submission.
- **Codex:** collects sources, distills and labels evidence, refreshes official field
  and operator entitlements, builds indexes, publishes the GitHub library, validates
  GPT output, imports approved batches, deploys when authorized, and verifies results.
- **GPT:** reads the library index and only the selected resources, analyzes completed
  research-pack evidence, proposes templates and CSV batches, and clearly marks
  uncertainty. GPT does not invent fields/operators or claim unrun tests passed.

## Fixed locations

- Local and GitHub library: `reports/gpt_library/`
- Official field indexes: `reports/data_fields/all_scopes/`
- Incoming completed research packs: `reports/gpt_library/research_packs/incoming/`
- GPT generation requests/prompts: `reports/gpt_library/prompts/`
- GPT proposed batches: `reports/gpt_library/batches/proposed/`
- Codex-validated batches: `reports/gpt_library/batches/validated/`
- Archived handoffs: `reports/gpt_library/archive/YYYYMMDD/`
- Curated templates/material: `reports/gpt_library/materials/` and `reports/gpt_library/templates/`
- Account/capability context: `reports/gpt_library/context/`
- Workflow and validation references: `reports/gpt_library/workflows/`
- Full scattered-source inventory: `reports/gpt_library/source_inventory_current.csv`

Do not hard-delete legacy files. Copy curated legacy assets into the fixed library,
record both locations, and migrate callers only after validation.

## Library curation rules

- `resource_catalog.csv` contains the small curated set GPT may read; the full source
  inventory is discovery evidence and is not a reading list.
- Keep one current curated copy per useful resource. Preserve dated originals and record
  SHA-256; do not move or delete them during curation.
- Generated `material_manager_*`, skill output folders, `reports_server` mirrors, raw DBs,
  queue snapshots, and incomplete research packs are index-only unless a task explicitly
  needs them. This prevents duplicate or stale runtime evidence from polluting GPT context.
- Every research pack must declare `COMPLETE`, `INCOMPLETE`, or `UNKNOWN`. Only COMPLETE
  packs are normal generation evidence; incomplete packs may be read only for gap analysis.
- New sources first enter the inventory, then pass credential scan, evidence labeling,
  duplicate/hash review, scope labeling, and catalog selection before GitHub publication.

## Five stages

### 1. User requests collection

The user names a forum/network topic or research objective. Codex records source URL,
capture date, market/scope, source type, and intended use. External and forum claims
are hypotheses, not account entitlement or official platform rules.

### 2. Codex distills, indexes, and publishes

Codex extracts economic logic, fields, operators, horizons, templates, risks, and
repair ideas; checks lightweight history; labels evidence; stores the result in the
fixed library; updates `resource_catalog.csv` and `LIBRARY_INDEX.md`; creates a
task-specific GPT prompt; scans for credentials; and publishes a small, reviewable
GitHub commit/PR. Large field catalogs are split by official region/delay/universe and
deduplicated through variant files.

### 3. User supplies completed-batch research pack

The pack is copied byte-for-byte to `research_packs/incoming/`. Codex records SHA-256,
scope, batch window, completeness, included result tables, and missing evidence. A
filename or activity label never proves PASS. Incomplete checks remain UNKNOWN/HOLD.

### 4. GPT generates the next batch

GPT first reads the task prompt, catalog, matching scope manifest, selected field
variants, templates/material, and completed-pack result summary. It outputs the strict
CSV schema plus provenance columns. Every field/operator must resolve to the supplied
indexes. Outputs are `REVIEW_ONLY`; activity-specific gates are explicit. Power Pool
is locked to USA/D1/TOP1000 and high-turnover returns-ratio remains a required official
test until evidence records PASS.

### 5. Codex validates and hands off to server

Codex validates schema, expressions, fields, operators, scope, duplicate/history risk,
test-gate declarations, and batch limits. Only validated rows move to `batches/validated/`.
Server upload/backtest occurs only when requested/authorized, uses the existing main
pipeline, preserves queue history, and is followed by server/runtime and result-timestamp
validation. Results return as a new completed research pack. Never auto-submit Alpha.

## Evidence labels

- `OFFICIAL_API`: current authenticated read-only API response.
- `OFFICIAL_DOC`: official BRAIN documentation.
- `LIVE_ACCOUNT`: current signed-in account page observation.
- `LOCAL_BACKTEST_EVIDENCE`: complete locally retained official backtest result.
- `FORUM_EXPERIENCE`: community experience; hypothesis only.
- `EXTERNAL_SOURCE`: network/article/paper material; hypothesis unless corroborated.
- `USER_PROVIDED`: user statement or package awaiting independent validation.
- `INFERENCE`: derived conclusion with its inputs named.

## Required gates

No stage may silently advance when its contract is incomplete. Missing provenance,
scope, field/operator resolution, research-pack completeness, or required test evidence
produces `UNKNOWN`, `HOLD`, or rejection—not a guessed value. GitHub publication is not
server deployment; server backtest is not Alpha submission.
