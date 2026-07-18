# FULL_RESEARCH_PACK Validation — 2026-07-13

- Package: `research_center/pack_v2_lite/research_package_20260713_02.zip`
- Mode/status: `FULL_RESEARCH_PACK` / `COMPLETE`
- Rebuild evidence: current `exports/all_generated_alphas.csv` SHA-256 exactly matched the previous certified FULL snapshot; the package was rebuilt from that authoritative snapshot and the current accumulated research ledgers (`matching_full_snapshot_ledger_replay`). No WQ backtest, submission, or queue mutation was run.
- Completeness: `READY`; all 12 required core materials are non-empty and ZIP-integrity checked. Missing required components: none.

## Core material rows

| file | rows |
|---|---:|
| batch_progress.csv | 39 |
| queued_batch_plan.csv | 7,000 |
| candidate_snapshot.csv | 5,515 |
| field_catalog.csv | 8,593 |
| expression_index.csv | 57,254 |
| generation_control.csv | 396 |
| research_inventory.csv | 13,203 |
| template_family_pressure.csv | 934 |
| parent_child_feedback.csv | 5,002 |
| mutation_feedback.csv | 7 |
| sharpe_fitness_weight_fail.csv | 233 |
| decision_analysis.md | non-empty |

## New decision assets

| file | rows | validation |
|---|---:|---|
| semantic_pair_candidates.csv | 12,660 | actual-estimate, mean-median, high-low, max-min, call-put, count-dispersion and guidance-range all present |
| pass_near_stability_view.csv | 646 | stable multi-year 301; single-year event 215; review 130 |
| weight_repair_ready.csv | 408 | each parent capped at three one-variable directions |
| template_success_transfer_map.csv | 8,425 | non-empty |
| recent_batch_family_score.csv | 239 | non-empty |
| mutation_family_feedback.csv | 7 | non-empty |
| research_effectiveness_summary.csv | 829 | batch/family/dataset/template/stage/run_intent/repair-action aggregation |
| alpha_research_asset_ledger.md | non-empty | persisted in package and `research_center/` |

## Coverage and research effectiveness

- Recent complete batch coverage: batch98–batch107; latest complete batch is batch107.
- Target six/PnL/PnL-SHA/local-self/submitted/pass/structure/target-parent correlation coverage: all `1.0000`.
- Local self-correlation is independent checkpoint evidence; no submitted-correlation fallback is used.
- ACTIVE actions: 47.
- Candidate totals: planned 5,515; done 5,515; invalid 8; pass 41; near 605; fail 4,861; high-corr 41; pending 0.
- Pass rate: 0.7434%; research effectiveness `(pass + near) / done`: 11.7135%.
- Action effectiveness: 47 / 5,515 = 0.8522% for both action/research-actions and action/candidate-snapshot in this snapshot.
- Final submitted/generated rate: 0 / 5,515 = 0.0000%; the candidate snapshot has no submitted-flag evidence, so it does not exceed the retained 0.1% brute-force final-submission baseline.

## External candidate readiness

The package can support the next `external_candidates` CSV: it has a COMPLETE core, 47 ACTIVE actions, semantic-pair screening, stability segmentation, repair directions constrained to one variable, and STOP/transfer evidence. Final submit effectiveness remains a downstream observation gap, not a license to auto-submit.
