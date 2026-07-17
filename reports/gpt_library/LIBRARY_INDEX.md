# WorldQuant GPT Reading Library

This is the stable entry point for GPT research context. Read the task prompt first,
then consult `resource_catalog.csv`; open only resources matching the requested scope
and purpose. Official field availability is indexed separately under
`reports/data_fields/all_scopes/`.

## Reading order

1. `prompts/GPT_LIBRARY_RESEARCH_PROMPT.md`
2. `resource_catalog.csv`
3. Relevant consultant/workflow audit
4. Relevant distilled forum/template material
5. The matching completed research pack and official scope field index

## Curated sections

- `context/`: current factor, capability, and consultant implementation context.
- `workflows/`: material-to-queue and research-pack contracts and validation references.
- `templates/`: reviewed forum/template families; still `REVIEW_ONLY`.
- `materials/incoming/`: newly collected raw links or captures awaiting distillation.
- `materials/distilled/`: compact researcher-ready notes after provenance and duplicate checks.
- `research_packs/incoming/`: user-provided completed-batch packages awaiting completeness review.
- `research_packs/reference/`: bounded context/probe packages, not proof of test success.
- `batches/proposed/` and `batches/validated/`: GPT output before and after Codex validation.
- `source_inventory_current.csv`: discovery inventory only; do not bulk-read it as research context.

`resource_catalog.csv` is the allowlist. If a file is present elsewhere but absent from
the catalog, GPT should not treat it as selected evidence without a new task instruction.

All generated formulas and CSV rows are `REVIEW_ONLY`. Never invent a field/operator,
infer a passed test from a package name, upload to a queue, or submit an Alpha.
