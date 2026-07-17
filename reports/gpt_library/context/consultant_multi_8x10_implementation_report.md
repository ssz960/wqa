# Consultant Multi-Simulation 8x10 implementation report

Date: 2026-07-16 (Asia/Shanghai)

## Result

The main-chain implementation, additive migration, controlled live ladder, and legacy rollback are complete. The production service now runs `consultant_multi` with capacity defined as 8 concurrent parent slots x 10 REGULAR children; `--single-slots 3` remains in the same service command as the immediate rollback contract. The current queue is too small to occupy all 80 child positions, so capacity and active load are reported separately. No Alpha submission or Osmosis points write was performed.

The accepted local proof is one replay of 8 parents x 10 children = 80 children. The controlled live proof submitted 1x5, 1x10, 2x10, and a first strict 4x10 attempt on the same primary worker. A later revalidation exposed a pre-fix mixed-size look-ahead (10, 10, 5, 3), so it is recorded as diagnostic evidence, not as a second strict 4x10 rung. The first 3-child discovery batch failed at the platform child level and was never re-submitted.

## Frozen and deployed evidence

- Local preflight backup: `backups/consultant_multi_preflight_20260716_132412`.
- Remote preflight backup: `/root/worldquant/backups/consultant_multi_preflight_20260716_133200`.
- Remote migration was run twice successfully with `user_version=1`.
- Remote service after deployment: `worldquant-backtest=active` and enabled.
- Remote service command explicitly contains `--single-slots 3 --transport-profile consultant_multi`.
- Live worker contains `--parallel-slots 3 --transport-profile consultant_multi`; watchdog reported `mode=CONSULTANT_MULTI_8X10`, `compliant=true`, `parent_slots_total=8`, `children_per_parent=10`, and `child_capacity=80`.
- Live log after restart showed repeated `active_slots=3/3`, queue reduction from 309 to 302, and normal result collection.
- Remote `tests_consultant_multi.py` passed all replay tests.

The remote code was compiled before migration and the service was restarted once after the final runtime copy, so the running process loaded the deployed modules.

## Capability probe

Read-only probe artifact: `reports/consultant_capability_probe_20260716.json`.

Observed:

- `OPTIONS https://api.worldquantbrain.com/simulations` returned HTTP 200 and `Allow: POST, OPTIONS`.
- The POST schema exposes `children`, `parent`, `progress`, `location`, `regular`, and `settings`, and ACE-compatible settings choices were readable for region, universe, delay, neutralization, and related fields.
- The activity endpoint returned a `DAILY` record shape with `current`, `yesterday`, `previous`, and `total` values.
- The response did not expose authoritative REGULAR max concurrent batches, max children, daily cap, day boundary, failure billing, or parent/child counting semantics.
- The configured 8×10 and 5000/day values remain explicitly labeled `USER_CONFIRMED_NEEDS_RUNTIME_PROBE`; they are not silently inferred and are not enabled by the service.

No `/simulations` POST was issued by the probe. `simulation_posted=false`, `alpha_submitted=false`, and `osmosis_points_written=false` are recorded in the artifact.

## Modified implementation

- `consultant_multi.py`: capability profiles, fail-closed resolution, schema migration helpers, request hashes, batch builder, budget reservation, parent/child state, recovery, import-once, throughput snapshot, and one-worker replay engine.
- `alpha_store.py`: additive schema initialization; old `alphas`, `backtests`, and `queue_events` remain readable.
- `stable_single_backtest.py`: feature-flagged multi branch inside the existing worker; legacy single branch is retained.
- `backtest_from_store.py` and `autonomous_research_loop.py`: profile/config propagation without changing legacy defaults.
- `pipeline_watchdog.py`: read-only `active_batches`, `active_children`, `single_active`, budget, and inconsistency checks while retaining the 3-slot availability alarm.
- `worldquant-backtest.service` and watchdog unit: explicit legacy profile/default and profile-aware description.
- `consultant_multi_migration.py`, `migrations/consultant_multi_001.sql`, `migrations/consultant_multi_001_down.sql`: repeatable additive migration and rollback.
- `consultant_capability_profile.json`: explicit user-confirmed candidate limits, marked partial and disabled by default.
- `consultant_capability_profile_stage_1x5.json`, `consultant_capability_profile_stage_1x10.json`, `consultant_capability_profile_stage_2x10.json`, `consultant_capability_profile_stage_4x10.json`: temporary controlled-rung profiles, all explicitly sourced and not default-enabled.
- `tests_consultant_multi.py`: migration, profile, builder, budget, idempotency, parent 429 retry, restart rehydrate, partial failure, no-Location, CANCELLED child closure, 2/5/10, and 8x10 replay coverage.
- `agents.md`, `ai_memory/ACTIVE_REQUIREMENTS.md`, and `reports/audits/consultant_upgrade_phase_plan.csv`: new P0 wording and actual implementation status.

## Schema and state model

New tables:

- `capability_snapshots(snapshot_id, payload_json, probe_status, expires_at, source_refs_json, ...)`
- `simulation_batches(batch_id, parent_request_key, platform_location, idempotency_key, requested/reserved/submitted/completed/failed counts, status, retry/error fields, ...)`
- `simulation_batch_children(child_id, batch_id, alpha_id, child_index, platform_alpha_id, child_request_hash, child_status, metrics/error/import timestamps, ...)`
- `daily_simulation_budget(platform_day, daily_cap, reserved_children, submitted_children, counted_failures, released_reservations, day-boundary source, ...)`

Nullable compatibility columns were added to `alphas` and `backtests`; no old table was dropped or redefined.

Parent states are `PLANNED → RESERVED → SUBMITTING → SUBMITTED → POLLING → PARTIAL/COMPLETE`, with `FAILED_RETRYABLE`, `FAILED_TERMINAL`, `RECOVERY_REQUIRED`, and `ABORTED`. Child states are `PENDING`, `RUNNING`, `SUCCEEDED`, `FAILED_RETRYABLE`, `FAILED_TERMINAL`, `IMPORT_PENDING`, and `IMPORTED`.

Parent idempotency is deterministic over ordered child request hashes. Child request hashes, child IDs, and the `backtests.child_id` uniqueness check prevent duplicate final writes. Missing parent Location or unknown parent/poll HTTP state becomes `RECOVERY_REQUIRED`; it is never blindly re-submitted as a whole batch.

## Tests

Passed locally:

- fresh DB, old DB, repeated migration, rollback preserving legacy rows;
- capability complete/partial/failed fixtures and explicit-source enforcement;
- batch sizes 2, 5, and 10;
- compatible REGULAR builder, priority/cooldown/score-zero filtering, and single fallback;
- 8x10 replay with 80 children, duplicate idempotency calls, 80 unique child imports, and budget ledger `reserved=0, submitted=80`;
- parent without Location, Retry-After/error handling, terminal child failure, partial-child path, and import-once;
- existing SQLite lock-resilience, backtest availability, authentication recovery, platform identity, slot scheduler, and pipeline smoke tests.

The full `tests_production_guardrails.py` run still stops at an existing hourly formatter assertion (`batch_block_visible`/`suggestion_short_visible`) before completion. Its failure is unrelated to the consultant multi files; it is recorded as unresolved rather than bypassed.

## Live ladder and blockers

| rung | status | evidence |
|---|---|---|
| 1x5 | passed live | 1 parent, 5/5 children IMPORTED, 5 platform Alpha IDs, no 429 |
| 1x10 | passed live | 1 parent, 10/10 children IMPORTED, 10 platform Alpha IDs, no 429 |
| 2x10 | passed live | 2 parents, 20/20 children IMPORTED, no duplicate parent/child writes, no 429 |
| 4x10 | failed and downgraded | Strict first attempt: 3 parents completed 30 children; 1 parent had 10/10 FAILED_TERMINAL children; no 429. A later diagnostic revalidation had 10/10 and 10/10 terminal failures plus 5/5 and 3/3 completions after the pre-fix mixed-size bug was exposed. |
| 8x10 local replay | passed | 8 parents, 80 children, no duplicate submit/import, no lost child, budget not oversold |
| consultant multi production capacity | enabled | same primary worker; 8 parent slots x 10 children; watchdog compliant; WeCom displays parent slots and child capacity |
| legacy single rollback | retained | service command keeps `--single-slots 3`; changing only the transport profile restores the one-worker 3-slot path |

Live parent evidence retained in the remote DB:

- 1x5: `batch_334d42e32f844f91932c5a4fb873e586`, Location ending `4n2fkZ3m14RFb9QF2RRJDKN`, 5/5 imported.
- 1x10: `batch_e09fd3f5b1de479d80522710452e4b4a`, Location ending `HriOU5JR4ik8HoKq9SUhwW`, 10/10 imported.
- 2x10: `batch_7fd3b4466e63450cbc10e0922a4c32ef` and `batch_de8fbcbac6e5456f823393872bcb72f5`, 20/20 imported.
- 4x10: `batch_a13d0d0b43da40488dae4eafe999d228`, `batch_a3f961295d6e4ad6945e5ebcb69e9e76`, and `batch_783271e148bb4f0185e9fccf04687a67` completed 30 children; `batch_44b7793f0a6e4c37ad01c8de7c2e93f5` ended with 10/10 `FAILED_TERMINAL` children. The initial parser-discovery parent `batch_dabb49e629b3447598d2213e831f0bc2` ended with 3/3 terminal child failures and was not re-posted.
- Diagnostic revalidation after the first failure: `batch_b45f796a511d4eb18dc612034f5558bb` completed 5/5; `batch_8d5972f0f53e4b9987ce51ee19a62265` completed 3/3; `batch_1f54da7e49c34d9994c53190d723dd89` failed 10/10; `batch_b01ab02ad7d14ed2b86a8fe7fc92663e` failed 10/10 with platform children reported `CANCELLED`. This run was mixed-size under the old builder and is not strict 4x10 evidence.

Across all controlled live Multi-Simulation submissions, 88 child results were imported and 53 children failed terminally; the budget ledger shows `reserved=0`, `submitted=141`, `counted_failures=0` because failure billing is not authoritative, and 4859 remaining against the explicit 5000/day candidate cap. The production switch submitted three new 10-child parents: one completed 10/10 and two ended 10/10 terminal failure. Observed live `parent_429=0` and `child_429=0`. The 2-core/2-GB host remained healthy. Final watchdog evidence is `mode=CONSULTANT_MULTI_8X10`, `compliant=true`, `active_batches=0`, `active_children=0`, `single_active=3`, with 6 queued candidates actively using the single fallback lane.

The remaining blocker is full 8/8 occupancy, not the transport interface. Earlier inspection found only 36 batch128 expressions without direct MATRIX fields, and live batch128 parents repeatedly returned generic parent `ERROR` with terminal child errors. After normal queue consumption and the production switch, 6 positive-priority queued candidates remain below the exact 10-child minimum for a new parent; they are now running through the retained single fallback lane instead of looping. The worker therefore reports `父槽0/8｜子任务0/80｜回退single3/3`, separating unused multi capacity from actual single fallback load. Creating or padding a new Consultant target layer remains outside this task. The API still does not expose authoritative entitlement or failure-billing semantics; live runs use the explicitly labeled `USER_CONFIRMED_NEEDS_RUNTIME_PROBE` profile and ledger every submitted child.

The Enterprise WeChat `查询` and hourly brief now use parent-slot semantics in multi mode. Verified server output: `【系统状态】运行中｜队列6｜父槽0/8｜子任务0/80｜回退single3/3`. Legacy mode keeps the previous `运行x/3` wording.

The pre-fix mixed-size diagnostic parents were closed exactly once after deploying `min_children_per_batch` and CANCELLED parsing: `batch_b45f796a511d4eb18dc612034f5558bb` completed 5/5, `batch_8d5972f0f53e4b9987ce51ee19a62265` completed 3/3, `batch_1f54da7e49c34d9994c53190d723dd89` failed 10/10, and `batch_b01ab02ad7d14ed2b86a8fe7fc92663e` failed 10/10. No parent was re-posted. Future exact rungs require the staged profile's explicit minimum of 10 children; shorter compatible groups fall back to single.

## Rollback

Disable multi immediately by keeping the service command at `--transport-profile legacy_single`, then reload/restart the same service:

```bash
sudo systemctl daemon-reload
sudo systemctl restart worldquant-backtest
sudo systemctl is-active worldquant-backtest
pgrep -af 'autonomous_research_loop.py|backtest_from_store.py|stable_single_backtest.py'
```

To remove only the additive schema while preserving legacy rows:

```bash
sudo /root/worldquant/.venv/bin/python /root/worldquant/consultant_multi_migration.py \
  --db /root/worldquant/alpha_store.db --rollback
```

The preflight DB/queue/unit backup remains at `/root/worldquant/backups/consultant_multi_preflight_20260716_133200`; no hard delete or Alpha submission was used.
