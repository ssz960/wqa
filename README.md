# WQ GPT Factor Context

This repository contains a consultant-level WorldQuant BRAIN factor-design context snapshot.

## Files

- `reports/data_fields/gpt_factor_context_current.md`: prompt-safe catalog of datasets, operators, simulation settings, captured defaults, and GPT retrieval rules.
- `reports/data_fields/available_data_fields_current.csv`: exact USA / TOP3000 / delay 1 authoritative field registry.
- `reports/data_fields/index/field_catalog_manifest.json`: registry counts, scope, hashes, and index metadata.
- `reports/data_fields/index/field_keyword_index.csv`: compact recall index with `field_id`, dataset, type, description, keywords, coverage, region, and delay.
- `reports/data_fields/index/fields_by_dataset/`: one CSV per dataset for narrow retrieval.
- `tools/search_available_fields.py`: local deterministic search over the keyword index.

## Scope

- 299 datasets
- 85,612 fields
- 85 operators
- 18 simulation settings
- 8 regions exposed by the simulation OPTIONS schema
- Current field CSV scope: USA / TOP3000 / delay 1

The full CSV should be searched or retrieved by scope and dataset. It should not be pasted into one GPT prompt. No credentials, simulation submissions, alpha submissions, or Osmosis writes are included.

Example:

```text
python tools/search_available_fields.py --query earnings surprise --dataset analyst15 --field-type MATRIX --limit 20 --format json
```
