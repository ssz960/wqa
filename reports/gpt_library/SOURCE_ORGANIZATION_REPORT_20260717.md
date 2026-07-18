# GPT/WQ source organization report — 2026-07-17

## Outcome

The fixed library now separates curated GPT reading resources from a repository-wide
discovery inventory. Originals remain in place; no runtime, database, queue, history,
server mirror, or research result was moved or deleted.

## Inventory

`source_inventory_current.csv` records 907 matching files:

- 426 skill references;
- 332 server-mirror files;
- 98 generated-history files;
- 15 governance/evidence files;
- 9 GPT-context files;
- 9 research-material files;
- 17 related resources;
- 1 research pack requiring completeness review.

Of these, 873 are index-only, 33 require curated-copy review, and one research pack
requires completeness review. The latest `research_package_20260717_07.zip` reports
`INCOMPLETE` with `blocking_research_data_gap`, so it was not copied into the GPT
allowlist as completed evidence.

## Curated copies added

- current factor context and consultant capability/implementation context;
- material-to-queue and full research-pack workflow/validation references;
- reviewed forum template library and current field-cleanup audit;
- portable 85,612-field context package and seven-dataset probe package.

Generated `material_manager_*` files, `reports_server` mirrors, skill output folders,
and incomplete research packs remain at their original paths and are inventory-only.

## Future rule

Run `tools/audit_gpt_library_sources.py`, review changed hashes and new candidates, scan
selected resources for credentials, copy only useful current evidence, update
`resource_catalog.csv`, then publish the small curated delta to GitHub.
