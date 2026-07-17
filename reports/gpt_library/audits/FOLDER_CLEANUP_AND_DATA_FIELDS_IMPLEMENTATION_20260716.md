# Folder Cleanup and Consultant Data Fields - 2026-07-16

## Outcome

- Root and field-registry folders were reorganized without hard deletion.
- Low-risk deletion candidates were isolated under `pending_delete/20260716_folder_cleanup`; `manifest.csv` records source, target, byte size, SHA-256, reason, and status.
- New field exports use one shallow `reports/data_fields/history/` directory. Probe and smoke output no longer live in the repository root.
- Root-level test artifact paths were moved under `tmp/` in their tests, so reruns do not recreate `tmp_guardrails`, `tmp_hourly_report_schedule`, or `tmp_slot_scheduler` at root.
- The consultant-level USA / delay 1 / TOP3000 field refresh is finalized in the section below.

## Upstream and downstream map

```text
WorldQuant BRAIN signed-in account
  -> /data-sets and /data-fields API
  -> brain_common.py login/request_json
  -> refresh_available_data_fields.bat
  -> scripts/export_available_data_fields.py
       -> tmp/data_fields_refresh_USA_D1_TOP3000.jsonl (interrupt-only checkpoint)
       -> reports/data_fields/history/available_data_fields_<scope>_<timestamp>.csv
       -> reports/data_fields/available_data_fields_current.csv
       -> reports/data_fields/export_report_current.md
  -> alpha_store.py / material_manager.py / research_pack_builder.py
     / run_all_generated_alphas.py / scripts/fill_pack_v2_lite_data.py
```

`scripts/sync_worldquant_runtime.ps1` includes the exporter source, but it does not deploy the generated current CSV. This change is local-only: no production service was restarted and no server-side field cache was represented as refreshed.

## Isolation batch

The batch contains:

- unused root duplicate of the field exporter;
- obsolete root probe report;
- reinstallable Python installer and old deployment ZIP from `assets`;
- byte-identical dated duplicate from the stale `reports_server` snapshot;
- one-dataset probe/smoke artifacts;
- root-level scheduler, guardrail, and hourly-report test databases;
- one verified-empty old server-cleanup test backup.

No `docs`, active archive evidence, backup tree, pipeline run, queue state, database history, label/color data, or production file was hard-deleted. Large `tmp/pipeline_runs`, `backups`, and prior `pending_delete` batches remain separate review scopes.

## Consultant-level current snapshot

- Local canonical CSV: 85,612 rows, 299 datasets, 16 categories, USA / TOP3000 / delay 1.
- Field types: MATRIX 67,205; VECTOR 16,351; GROUP 2,041; UNIVERSE 7; SYMBOL 8.
- SHA-256: `F5CD01F3F4820E1753A6BF99029BA7A2FF30772813158BC12A1F5CF5DC99A102`.
- Local `reports_server` fallback mirror has the same byte count and SHA-256.
- Live operator catalog: 85 operators across Arithmetic, Cross Sectional, Group, Logical, Special, Time Series, Transformational, and Vector.
- Live simulation OPTIONS: 18 settings fields; 8 equity regions; region-dependent universes, delays, and neutralization choices; language `PYTHON` / `FASTEXPR`; bounds include decay `0..512`, truncation `0..1`, lookback `0..1024`, selection limit `10..1000`, and test period `P0Y0M0D..P6Y0M0D`.
- Captured UI default profile: USA / TOP3000 / delay 1, subindustry neutralization, decay 4, truncation 0.08, pasteurization ON, unit handling VERIFY, NaN handling OFF, one year, max trade OFF, max position OFF. This is a visible UI baseline, not an entitlement proof.
- GPT delivery assessment: the full field CSV is too large for a single prompt. Use the compact context plus retrieval by scope, dataset/category, and semantic query; send roughly 10-80 candidate fields per factor-design turn, then validate operators and settings before backtest.

The generated GPT artifacts are `reports/data_fields/gpt_factor_context_current.json` and `reports/data_fields/gpt_factor_context_current.md`.

## Validation

- Exporter compile and focused unit tests: passed.
- Exporter checkpoint round-trip test: passed.
- Hourly schedule path test: passed.
- Slot scheduler path test: passed (`slot_scheduler_ok exported=5`).
- Production guardrail suite reached the existing hourly formatter assertion and failed there (`batch_block_visible=False`, `suggestion_short_visible=False`); the test-path edits themselves compiled and ran.
- Quarantined file hashes are recorded in the isolation manifest; current output is replaced only by a complete, non-regressive export.
- Read-only API collection did not POST simulations, submit alphas, or write Osmosis points.

## Remaining cleanup review

1. Review failed/no-manifest `tmp/pipeline_runs` against package manifests and acceptance evidence before proposing another isolation batch.
2. Review each `backups` tree independently; do not use age alone as a deletion criterion.
3. Apply an explicit retention decision to older `pending_delete` batches before any hard deletion.
4. Keep `docs` and `archive` because they currently contain active guidance and historical evidence, not generic disposable clutter.
