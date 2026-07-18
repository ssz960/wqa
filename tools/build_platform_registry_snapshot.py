#!/usr/bin/env python3
"""Build the immutable, manifest-addressed Platform Registry snapshot.

This builder is offline. It reads only versioned wqa assets, streams the large
field CSV, writes deterministic gzip files, and never contacts WorldQuant.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


SNAPSHOT_ID = "REG-20260718-001"
SCHEMA_VERSION = "platform-registry.v1"
MANIFEST_VERSION = "platform-registry-manifest.v1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_head(root: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
    ).strip()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def deterministic_gzip_csv(
    source: Path, destination: Path, *, transform: Any = None
) -> tuple[int, list[str]]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    columns: list[str] = []
    with source.open("r", encoding="utf-8-sig", newline="") as input_handle:
        reader = csv.DictReader(input_handle)
        columns = list(reader.fieldnames or [])
        with destination.open("wb") as raw:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
                with io.TextIOWrapper(zipped, encoding="utf-8", newline="") as text:
                    writer = csv.DictWriter(text, fieldnames=columns, lineterminator="\n")
                    writer.writeheader()
                    for row in reader:
                        output = transform(row) if transform else row
                        writer.writerow(output)
                        count += 1
    return count, columns


def nested_choices(settings: dict[str, Any], key: str) -> dict[str, list[dict[str, Any]]]:
    return settings[key]["choices"]["instrumentType"]["EQUITY"]["region"]


def build(root: Path, generated_at: str) -> None:
    source_commit = git_head(root)
    snapshot = root / "registry" / "snapshots" / SNAPSHOT_ID
    source_fields = root / "reports" / "data_fields" / "available_data_fields_current.csv"
    source_datasets = root / "reports" / "data_fields" / "all_scopes" / "dataset_scope_matrix_current.csv"
    source_scopes = root / "reports" / "data_fields" / "all_scopes" / "simulation_scope_matrix_current.csv"
    source_settings = root / "reports" / "data_fields" / "all_scopes" / "simulation_options_current.json"
    source_operators = root / "registry" / "raw" / "20260718" / "operators_ui.json"

    field_target = snapshot / "fields" / "EQUITY" / "USA" / "TOP3000" / "D1" / "fields.csv.gz"
    dataset_target = snapshot / "datasets" / "dataset_scopes.csv.gz"
    field_count, field_columns = deterministic_gzip_csv(source_fields, field_target)
    dataset_count, dataset_columns = deterministic_gzip_csv(source_datasets, dataset_target)

    operator_capture = json.loads(source_operators.read_text(encoding="utf-8"))
    operator_target = snapshot / "operators" / "operators.jsonl"
    operator_target.parent.mkdir(parents=True, exist_ok=True)
    with operator_target.open("w", encoding="utf-8", newline="\n") as handle:
        for record in operator_capture["records"]:
            normalized = {
                "operator_id": record["operator_id"],
                "signature": record["signature"],
                "category": record["category"],
                "description": record["description"],
                "access_level": record["access_level"],
                "compatibility_status": "UNVERIFIED",
                "compatible_field_types": [],
                "source": operator_capture["source_url"],
                "last_verified_at": operator_capture["captured_at"],
            }
            handle.write(json.dumps(normalized, ensure_ascii=False, sort_keys=True) + "\n")

    options = json.loads(source_settings.read_text(encoding="utf-8"))
    setting_children = options["actions"]["POST"]["settings"]["children"]
    universes = nested_choices(setting_children, "universe")
    delays = nested_choices(setting_children, "delay")
    neutralizations = nested_choices(setting_children, "neutralization")
    normalized_settings = {
        "schema_version": SCHEMA_VERSION,
        "source": "OPTIONS /simulations",
        "source_commit": source_commit,
        "last_verified_at": generated_at,
        "instrument_types": ["EQUITY"],
        "regions": sorted(universes),
        "universes_by_region": {k: [x["value"] for x in v] for k, v in universes.items()},
        "delays_by_region": {k: [x["value"] for x in v] for k, v in delays.items()},
        "neutralizations_by_region": {
            k: [x["value"] for x in v] for k, v in neutralizations.items()
        },
        "bounds": {
            key: {
                "min": setting_children[key].get("minValue"),
                "max": setting_children[key].get("maxValue"),
            }
            for key in ("decay", "truncation", "lookback", "testPeriod")
        },
        "enums": {
            key: [x["value"] for x in setting_children[key].get("choices", [])]
            for key in (
                "pasteurization", "unitHandling", "nanHandling", "language",
                "selectionHandling", "maxTrade", "maxPosition",
            )
        },
    }
    settings_target = snapshot / "settings" / "simulation_settings.json"
    write_json(settings_target, normalized_settings)

    profile_target = snapshot / "settings" / "legal_profiles.csv"
    profile_target.parent.mkdir(parents=True, exist_ok=True)
    profile_count = 0
    with source_scopes.open("r", encoding="utf-8-sig", newline="") as source_handle, profile_target.open(
        "w", encoding="utf-8", newline=""
    ) as target_handle:
        reader = csv.DictReader(source_handle)
        columns = [
            "instrument_type", "region", "universe", "delay", "neutralization",
            "dataset_count", "field_coverage_status", "coverage_status", "last_verified_at",
        ]
        writer = csv.DictWriter(target_handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for scope in reader:
            field_status = (
                "COMPLETE" if scope["region"] == "USA" and scope["universe"] == "TOP3000"
                and scope["delay"] == "1" else "MISSING"
            )
            for neutral in neutralizations[scope["region"]]:
                writer.writerow({
                    "instrument_type": "EQUITY",
                    "region": scope["region"],
                    "universe": scope["universe"],
                    "delay": scope["delay"],
                    "neutralization": neutral["value"],
                    "dataset_count": scope["dataset_count"],
                    "field_coverage_status": field_status,
                    "coverage_status": "COMPLETE" if field_status == "COMPLETE" else "DATASET_ONLY",
                    "last_verified_at": generated_at,
                })
                profile_count += 1

    scope_manifest_targets: list[Path] = []
    with source_scopes.open("r", encoding="utf-8-sig", newline="") as handle:
        for scope in csv.DictReader(handle):
            complete_fields = scope["region"] == "USA" and scope["universe"] == "TOP3000" and scope["delay"] == "1"
            target = snapshot / "scopes" / "EQUITY" / scope["region"] / scope["universe"] / f"D{scope['delay']}" / "scope.json"
            write_json(target, {
                "schema_version": SCHEMA_VERSION,
                "snapshot_id": SNAPSHOT_ID,
                "scope": {"instrument_type": "EQUITY", "region": scope["region"], "universe": scope["universe"], "delay": int(scope["delay"])},
                "dataset_count": int(scope["dataset_count"]),
                "dataset_coverage": "COMPLETE",
                "field_coverage": "COMPLETE" if complete_fields else "MISSING",
                "coverage_status": "COMPLETE" if complete_fields else "DATASET_ONLY",
                "missing_scope": [] if complete_fields else ["fields"],
                "last_verified_at": generated_at,
                "dataset_catalog": dataset_target.relative_to(root).as_posix(),
                "field_catalog": field_target.relative_to(root).as_posix() if complete_fields else None,
            })
            scope_manifest_targets.append(target)

    field_types_target = snapshot / "fields" / "field_types.json"
    type_counts: Counter[str] = Counter()
    with source_fields.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            type_counts[row["field_type"].upper()] += 1
    write_json(field_types_target, {
        "schema_version": SCHEMA_VERSION,
        "scope": {"instrument_type": "EQUITY", "region": "USA", "universe": "TOP3000", "delay": 1},
        "types": [{"field_type": key, "record_count": value} for key, value in sorted(type_counts.items())],
    })
    policy_target = snapshot / "dataset_policy.json"
    write_json(policy_target, {
        "schema_version": SCHEMA_VERSION,
        "final_validation_requires_authoritative_record": True,
        "retrieval_indexes_are_authoritative": False,
        "cross_region_field_inference_allowed": False,
        "operator_compatibility_fail_closed_when_unverified": True,
        "runtime_source": "local_active_snapshot_only",
        "candidate_logic_changed": False,
        "real_wq_allowed": False,
    })

    schema_target = root / "registry" / "schemas" / "manifest.schema.json"
    write_json(schema_target, {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": MANIFEST_VERSION,
        "type": "object",
        "required": ["snapshot_id", "generated_at", "source_commit", "files", "coverage_status"],
        "properties": {
            "snapshot_id": {"type": "string"}, "generated_at": {"type": "string", "format": "date-time"},
            "source_commit": {"type": "string", "pattern": "^[0-9a-f]{40}$"},
            "coverage_status": {"enum": ["COMPLETE", "PARTIAL"]}, "files": {"type": "array"},
        },
    })

    file_specs = [
        ("schema", schema_target, 1, {}, "local schema"),
        ("datasets", dataset_target, dataset_count, {"instrument_type": "EQUITY", "regions": sorted(universes)}, "GET /data-sets"),
        ("fields", field_target, field_count, {"instrument_type": "EQUITY", "region": "USA", "universe": "TOP3000", "delay": 1}, "GET /data-fields"),
        ("field_types", field_types_target, len(type_counts), {"region": "USA", "universe": "TOP3000", "delay": 1}, "GET /data-fields"),
        ("operators", operator_target, len(operator_capture["records"]), {"instrument_type": "EQUITY"}, operator_capture["source_url"]),
        ("settings", settings_target, len(setting_children), {"instrument_type": "EQUITY", "regions": sorted(universes)}, "OPTIONS /simulations"),
        ("legal_profiles", profile_target, profile_count, {"instrument_type": "EQUITY", "regions": sorted(universes)}, "OPTIONS /simulations + GET /data-sets"),
        ("dataset_policy", policy_target, 1, {}, "REG-20260718-001 governance"),
    ]
    file_specs.extend(
        ("scope_manifest", path, 1, json.loads(path.read_text(encoding="utf-8"))["scope"], "OPTIONS /simulations + GET /data-sets")
        for path in scope_manifest_targets
    )
    files = []
    for kind, path, count, scope, source in file_specs:
        files.append({
            "kind": kind,
            "path": path.relative_to(root).as_posix(),
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
            "record_count": count,
            "schema_version": SCHEMA_VERSION,
            "scope": scope,
            "source": source,
            "source_commit": source_commit,
        })
    missing = [
        f"EQUITY/{row['region']}/{row['universe']}/D{row['delay']}/fields"
        for row in csv.DictReader(source_scopes.open("r", encoding="utf-8-sig", newline=""))
        if not (row["region"] == "USA" and row["universe"] == "TOP3000" and row["delay"] == "1")
    ]
    manifest = {
        "manifest_schema_version": MANIFEST_VERSION,
        "schema_version": SCHEMA_VERSION,
        "snapshot_id": SNAPSHOT_ID,
        "generated_at": generated_at,
        "source_commit": source_commit,
        "coverage_status": "PARTIAL",
        "missing_scope": missing,
        "last_verified_at": generated_at,
        "files": files,
        "counts": {
            "dataset_scope_records": dataset_count, "field_records": field_count,
            "operator_records": len(operator_capture["records"]), "legal_profiles": profile_count,
        },
    }
    manifest_target = snapshot / "manifest.json"
    write_json(manifest_target, manifest)
    write_json(root / "registry" / "active.json", {
        "snapshot_id": SNAPSHOT_ID,
        "manifest": manifest_target.relative_to(root).as_posix(),
        "manifest_sha256": sha256_file(manifest_target),
        "activation_policy": "server sync must verify hash and import locally before activation",
    })

    coverage_target = root / "scope_coverage_matrix.csv"
    with source_scopes.open("r", encoding="utf-8-sig", newline="") as source_handle, coverage_target.open(
        "w", encoding="utf-8", newline=""
    ) as target_handle:
        reader = csv.DictReader(source_handle)
        columns = ["instrument_type", "region", "universe", "delay", "dataset_count", "dataset_coverage", "field_coverage", "operator_coverage", "settings_coverage", "coverage_status", "missing_scope", "last_verified_at"]
        writer = csv.DictWriter(target_handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for row in reader:
            complete_fields = row["region"] == "USA" and row["universe"] == "TOP3000" and row["delay"] == "1"
            missing_scope = "" if complete_fields else f"EQUITY/{row['region']}/{row['universe']}/D{row['delay']}/fields"
            writer.writerow({
                "instrument_type": "EQUITY", "region": row["region"], "universe": row["universe"],
                "delay": row["delay"], "dataset_count": row["dataset_count"], "dataset_coverage": "COMPLETE",
                "field_coverage": "COMPLETE" if complete_fields else "MISSING", "operator_coverage": "COMPLETE_IDS_DESCRIPTIONS_COMPATIBILITY_UNVERIFIED",
                "settings_coverage": "COMPLETE", "coverage_status": "COMPLETE" if complete_fields else "DATASET_ONLY",
                "missing_scope": missing_scope, "last_verified_at": generated_at,
            })

    inventory = []
    for path in sorted(p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts):
        relative = path.relative_to(root).as_posix()
        if relative == "platform_registry_inventory.json":
            continue
        if relative.startswith("registry/raw/"):
            classification = "authoritative_raw_capture"
        elif relative.startswith("registry/snapshots/"):
            classification = "canonical_snapshot"
        elif relative.startswith("registry/schemas/"):
            classification = "schema"
        elif "/index/" in relative:
            classification = "retrieval_index"
        elif relative.startswith("reports/data_fields/all_scopes/scopes/"):
            classification = "legacy_scope_split"
        elif relative.startswith("reports/data_fields/all_scopes/"):
            classification = "legacy_normalized_catalog"
        elif relative.startswith("reports/gpt_library/"):
            classification = "generated_or_historical_report"
        elif relative.startswith("tools/"):
            classification = "collector_or_builder"
        else:
            classification = "legacy_or_repository_metadata"
        inventory.append({"path": relative, "bytes": path.stat().st_size, "classification": classification})
    write_json(root / "platform_registry_inventory.json", {
        "schema_version": "platform-registry-inventory.v1", "generated_at": generated_at,
        "source_commit": source_commit, "file_count": len(inventory), "total_bytes": sum(x["bytes"] for x in inventory),
        "self_excluded": True,
        "audit": {
            "authoritative_raw_data": ["registry/raw/20260718/operators_ui.json", "reports/data_fields/available_data_fields_current.csv"],
            "canonical_normalized_root": f"registry/snapshots/{SNAPSHOT_ID}",
            "legacy_scope_layout": "reports/data_fields/all_scopes/scopes/<region>/D<delay>/<universe>",
            "canonical_scope_layout": f"registry/snapshots/{SNAPSHOT_ID}/scopes/<instrument_type>/<region>/<universe>/D<delay>",
            "duplicate_or_generated_views": ["reports/data_fields/index/field_keyword_index.csv", "reports/data_fields/index/fields_by_dataset/*", "reports/data_fields/gpt_factor_context_current.md"],
            "oversized_files_threshold_bytes": 10000000,
            "known_missing": ["non-USA authoritative field records", "authoritative operator-to-field-type compatibility matrix"],
            "traceability_gaps": ["legacy all_scopes manifest has no source_commit", "legacy current filenames are mutable pointers"],
            "naming_gaps": ["legacy D1 directory precedes universe", "reports mixes registry data, indexes, GPT packs, audits, and historical reports"],
        },
        "files": inventory,
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--generated-at", required=True)
    args = parser.parse_args()
    build(args.root.resolve(), args.generated_at)
    print(f"PASS: built {SNAPSHOT_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
