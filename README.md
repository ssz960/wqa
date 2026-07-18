# WorldQuant Platform Registry Upstream

`wqa` is the versioned, read-only upstream asset repository for Alpha Mining OS Platform Registry. It contains no credentials, simulation submissions, alpha submissions, PnL, or production runtime data.

The canonical entry point is [`registry/active.json`](registry/active.json). A server synchronizer must pin a Git commit, fetch only the referenced Manifest and files, verify every SHA-256, stream-import them into a local database, validate the staging snapshot, then atomically activate it. Runtime, Materializer, Admission, and AI retrieval query only that local Active Snapshot; they must not read GitHub or scan the complete CSV during a request.

## Canonical layout

```text
registry/
  active.json
  raw/20260718/                         authenticated read-only source evidence
  schemas/manifest.schema.json
  snapshots/REG-20260718-001/
    manifest.json
    dataset_policy.json
    datasets/dataset_scopes.csv.gz
    fields/EQUITY/USA/TOP3000/D1/fields.csv.gz
    operators/operators.jsonl
    settings/{simulation_settings.json,legal_profiles.csv}
    scopes/EQUITY/<region>/<universe>/D<delay>/scope.json
```

`reports/data_fields/` is legacy source and generated retrieval material. Its `current` names are mutable pointers, its `index/` files are recall views only, and its legacy Scope order is `<region>/D<delay>/<universe>`. New canonical snapshots use `<instrument_type>/<region>/<universe>/D<delay>` and immutable snapshot IDs.

## Coverage and safety

- Dataset and Simulation Settings coverage: 43 legal Equity scopes across USA, GLB, EUR, ASI, CHN, JPN, IND, and MEA.
- Field coverage: complete only for USA/TOP3000/D1 (85,612 records). Every other Scope is explicitly `MISSING`; USA fields must never be projected into another Region.
- Operators: 85 visible platform records. IDs, signatures, categories, access level, and descriptions are authoritative UI capture; operator-to-field-type compatibility is `UNVERIFIED` and must fail closed.
- Indexes are recall-only. Final field and Operator validation returns to the authoritative Active Snapshot records.

Offline build and validation:

```text
python tools/build_platform_registry_snapshot.py --generated-at <ISO-8601 UTC>
python tools/validate_registry_sync.py
python tools/assess_registry_capacity.py
```

See `platform_registry_inventory.json`, `scope_coverage_matrix.csv`, `server_capacity_assessment.md`, and `registry_sync_validation.md` for the audit evidence and deployment limits.
