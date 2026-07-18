# Registry Sync Validation — REG-20260718-001

Result: **PASS with coverage limits**. The deployment classification is `READY_WITH_LIMITS`.

## Verified chain

The validator read `registry/snapshots/REG-20260718-001/manifest.json`, whose source commit is `8548481557fbf51b970a7a22f988bad19f1f7732`. Network sockets were disabled for the complete validation. Every listed file was checked for path containment, byte size, and SHA-256 before import.

The importer streamed gzip/JSONL/CSV records in batches of 1,000 into a temporary SQLite staging database, checked Manifest record counts, created bounded lookup indexes, and switched the database state to Active only after successful import.

Imported records:

- Dataset Scope records: 6,509.
- Fields: 85,612 (USA/TOP3000/D1 only).
- Operators: 85.
- Legal Region/Universe/Delay/Neutralization profiles: 483.

The service queried the local Active Snapshot by Region=`USA`, Dataset=`analyst15`, Field type=`MATRIX`, keyword=`earnings`, Top-K=`5`. It returned five authoritative Field records without accessing GitHub or scanning the source CSV at request time.

`ts_rank` was found in the Active Snapshot with its platform signature and description. Its type compatibility remains `UNVERIFIED`, so the registry can validate Operator existence but must reject a final field/operator compatibility decision until authoritative compatibility data is available.

The Simulation Profile `EQUITY/USA/TOP3000/D1/SUBINDUSTRY` was accepted and produced:

```text
snapshot_id: REG-20260718-001
simulation_profile_hash: 9bacfc9691578e7e94a82aace249f738fc4c6477b33ff6e62ee90ef62c2a26d5
```

## Measured performance

- Hash/Manifest verification: approximately 0.02 seconds.
- Import: approximately 5.5 seconds.
- SQLite size: 41,320,448 bytes.
- Estimated index bytes: 25,910,288 (this SQLite build has no `dbstat`; conservative file-size delta method used).
- Peak process RSS: 33,624,064 bytes.
- Query latency: median approximately 1.99 ms, P95 approximately 2.85 ms over 25 local queries.
- Embeddings: disabled. Vector database: disabled. Real WQ calls: zero.

Machine-readable evidence is in `registry_sync_validation_metrics.json`.

## Failure-closed coverage

The snapshot is `PARTIAL`: all non-USA/TOP3000/D1 Field scopes are listed in Manifest `missing_scope` and in `scope_coverage_matrix.csv`. Dataset/Settings availability does not imply Field availability. This validation does not modify candidate research logic, Admission rules, Materializer behavior, or any execution adapter.
