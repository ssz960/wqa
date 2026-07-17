# WQ GPT Factor Context

This repository is a read-only research context package for WorldQuant BRAIN
field discovery and factor-design planning. It contains no credentials,
simulation submissions, alpha submissions, or Osmosis writes.

## Repository layout

```text
reports/
└─ data_fields/
   ├─ gpt_factor_context_current.md
   ├─ available_data_fields_current.csv
   ├─ field_catalog_manifest.json
   └─ index/
      ├─ field_keyword_index.csv
      └─ fields_by_dataset/
tools/
├─ build_field_index.py
└─ search_available_fields.py
```

The complete CSV is the source of truth. The keyword index and the per-dataset
files are generated retrieval views, so a refresh should replace them together.
The current registry is USA / TOP3000 / delay 1 with 85,612 fields across 299
datasets. Do not paste the full CSV into a single GPT prompt; retrieve a small,
scope-locked candidate set instead.

## Search examples

```text
python tools/search_available_fields.py --query earnings surprise --dataset analyst15 --field-type MATRIX --limit 20 --format json
python tools/search_available_fields.py --query cash flow --category Fundamental --limit 30
python tools/search_available_fields.py --list-datasets --category Analyst
grep -i "surprise" reports/data_fields/index/field_keyword_index.csv
```

Use `field_catalog_manifest.json` to verify the source hash, row count, scope,
and index paths before using a result in research. GPT consumes the compact
context and selected field results; Codex maintains, regenerates, and verifies
the registry and indexes.
