# FULL_RESEARCH_PACK P0 Research Assets - 2026-07-16

## Final Package

- ZIP: `research_center/pack_v2_lite/research_package_20260716_04.zip`
- SHA-256: `b0377771498450552f4a4f63379f679412a0b5fff082f128a499d9af92497efa`
- Bytes: `6,655,563`
- Members: `33`
- Package mode/status: `FULL_RESEARCH_PACK` / `COMPLETE`
- Rebuild method: `matching_full_snapshot_ledger_replay`
- Completeness: no missing components; all three new assets are `required_for_complete=true` and `status=available`.
- Safety: no backtest, queue import, queue mutation, prune/score-zero, or alpha submission was executed.

## 1. repair_method_feedback.csv

- Rows: `5,002`
- Manifest: `available`, required for COMPLETE.
- UNKNOWN rows: `0`.
- Evidence availability: `4,922` rows have explicit parameter/expression changes; `2,996` have parent/child Turnover delta. The current parent-child source does not contain both-side Weight or pool-correlation evidence, so those deltas are blank and explicitly marked `UNAVAILABLE_PARENT_OR_CHILD` instead of being fabricated.
- Fields: `parent_alpha_id, child_alpha_id, family, dataset, repair_action, parameter_changes, parent_failed_checks, child_failed_checks, improved_failed_checks, new_failed_checks, failed_item_improved, failed_check_evidence_status, parent_sharpe, child_sharpe, delta_sharpe, parent_fitness, child_fitness, delta_fitness, parent_sub_universe, child_sub_universe, delta_sub_universe, parent_weight, child_weight, delta_weight, parent_turnover, child_turnover, delta_turnover, delta_weight_status, delta_turnover_status, parent_max_corr, child_max_corr, delta_corr, delta_corr_status, delta_corr_with_submitted, delta_corr_with_pass, parent_result_status, child_result_status, converted_to_pass_or_near, repair_outcome, next_action, confidence`.

Sample:

```json
{"parent_alpha_id":"1","child_alpha_id":"2951","family":"evo:dataset_substitution:price+price","dataset":"price_returns","repair_action":"EXPRESSION_LEVEL_REPAIR","parameter_changes":"decay:12->11;expression:3a1b842c22f7->b124dc18e1e5","delta_sharpe":"0.0700","delta_fitness":"0.0600","delta_turnover":"0.0069","delta_turnover_status":"AVAILABLE","delta_weight_status":"UNAVAILABLE_PARENT_OR_CHILD","delta_corr_status":"UNAVAILABLE_PARENT_OR_CHILD","converted_to_pass_or_near":"NO","next_action":"COLLECT_MORE_PARENT_CHILD_EVIDENCE","confidence":"MEDIUM"}
```

## 2. high_corr_asset_review.csv

- Rows: `274`
- Manifest: `available`, required for COMPLETE.
- UNKNOWN rows: `0`.
- Classification counts: `STOP_DUPLICATE=148`, `TEMPLATE_ASSET=1`, `REPLACE_CANDIDATE=18`, `TRANSFER_TO_NEW_FIELD=0`, `REPAIR_BEFORE_SUBMIT=107`.
- Fields: `alpha_id, record_key, batch_id, family, dataset, template_id, expression, result_status, quality_band, sharpe, fitness, sub_universe_sharpe, weight_value, turnover, corr_with_submitted, corr_with_pass, local_structure_corr, max_corr, nearest_corr_alpha, nearest_corr_family, failed_checks, asset_class, classification_reason, recommended_action, transfer_target, confidence`.

Sample:

```json
{"alpha_id":"1YdR0VkR","family":"max_min_probe","dataset":"analyst4","result_status":"pass","quality_band":"HIGH","sharpe":"1.58","fitness":"1.02","max_corr":"0.7091","asset_class":"TEMPLATE_ASSET","recommended_action":"PRESERVE_TEMPLATE_AND_TRANSFER_STRUCTURE_ONLY","confidence":"HIGH"}
```

## 3. daily_batch_lane_plan.csv

- Rows: `7`.
- Manifest: `available`, required for COMPLETE, `research_advice_only=true`, `auto_queue=false`.
- UNKNOWN rows: `0`.
- Lanes: `submit_hunt_repair`, `repair_method_mining`, `asset_transfer`, `strict_semantic_pairs`, `new_dataset_probe`, `high_corr_transfer`, `stage4_ab_trade_when`.
- Fields: `priority, lane, suggested_count, input_evidence, stop_condition, review_metrics, should_generate, generation_policy, reason`.

Sample:

```json
{"priority":"1","lane":"submit_hunt_repair","suggested_count":"30","input_evidence":"pass_or_near=814;candidate_rows=5684","stop_condition":"stop_when_no_corr_complete_parent_or_variant_cap_reached","review_metrics":"pass_conversion_rate;corr_below_0.50;failed_check_improvement","should_generate":"YES","generation_policy":"select_review_candidates_only","reason":"research_recommendation_only_no_queue_import_no_backtest"}
```

## Validation

- Local dry-run: Python compile plus `tests_daily_research_pack_assets.py` and `tests_daily_full_research_pack_assets.py` passed.
- Formal daily run: `recent_20260715_231350_599` reused completed download/six/PnL/self-corr/correlation/preflight checkpoints and ended `success`; `_03` passed orchestrator postflight and successful-run compaction.
- Resume hardening: a valid resumed preflight is accepted only with `resume_from_checkpoint=true`, `reused=true`, zero failed, zero issues, and `package_status_ceiling=READY`.
- ZIP hardening: matching replay ignores incomplete ZIPs before reading their manifest as reusable FULL evidence.
- Final replay: `_04` reused the byte-identical certified source SHA from `_03`, rebuilt all 33 members, passed the builder ZIP member/header gate, and remained `FULL_RESEARCH_PACK/COMPLETE`.
- Remote read-only dry-run: `worldquant-backtest=active`; service command contains `--single-slots 3`; live worker contains `--parallel-slots 3`; recent logs showed `active_slots=3/3`, queued `530`, running `3`; alternate-system flag absent. Only read-only `systemctl`, `ps`, `stat`, and `grep` commands were used.

## COMPLETE Impact

The three files are P0 required components. Missing/empty/invalid headers, or a lane plan not containing exactly seven rows, makes the package incomplete. In the final ZIP all three gates pass, so they do not reduce package status; the final package is `COMPLETE`.
