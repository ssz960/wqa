#!/usr/bin/env python3
"""Build deterministic retrieval indexes for the available-data-fields CSV."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIELDS = ROOT / "reports" / "data_fields" / "available_data_fields_current.csv"
DEFAULT_OUTPUT = ROOT / "reports" / "data_fields"
TOKEN_RE = re.compile(r"[\w]+", re.UNICODE)
STOPWORDS = {"a", "an", "and", "for", "in", "of", "on", "or", "the", "to", "with"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def keywords(row: dict[str, str]) -> str:
    source = " ".join(
        row.get(key, "")
        for key in (
            "dataset_id",
            "dataset_name",
            "dataset_category",
            "field_id",
            "field_name",
            "description",
            "notes",
        )
    )
    values = {
        token.casefold()
        for token in TOKEN_RE.findall(source)
        if len(token) > 1 and token.casefold() not in STOPWORDS
    }
    return " ".join(sorted(values))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the WQ field keyword and dataset indexes.")
    parser.add_argument("--fields", type=Path, default=DEFAULT_FIELDS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def write_csv(path: Path, rows: list[dict[str, str]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    fields_path = args.fields.resolve()
    output_dir = args.output_dir.resolve()
    with fields_path.open("r", encoding="utf-8-sig", newline="") as handle:
        source_rows = list(csv.DictReader(handle))
    if not source_rows:
        raise SystemExit("source CSV is empty")
    source_columns = list(source_rows[0])
    required = {"dataset_id", "dataset_name", "dataset_category", "field_id", "field_type"}
    missing = sorted(required - set(source_columns))
    if missing:
        raise SystemExit(f"source CSV missing required columns: {', '.join(missing)}")

    rows: list[dict[str, str]] = []
    by_dataset: dict[str, list[dict[str, str]]] = defaultdict(list)
    categories = Counter()
    field_types = Counter()
    regions = Counter()
    universes = Counter()
    delays = Counter()
    dataset_meta: dict[str, dict[str, object]] = {}
    for source_row in source_rows:
        row = {column: source_row.get(column, "") for column in source_columns}
        row["keywords"] = keywords(row)
        rows.append(row)
        dataset_id = row["dataset_id"]
        by_dataset[dataset_id].append(row)
        categories[row.get("dataset_category", "")] += 1
        field_types[row.get("field_type", "")] += 1
        regions[row.get("region", "")] += 1
        universes[row.get("universe", "")] += 1
        delays[row.get("delay", "")] += 1
        meta = dataset_meta.setdefault(
            dataset_id,
            {
                "dataset_id": dataset_id,
                "dataset_name": row.get("dataset_name", ""),
                "dataset_category": row.get("dataset_category", ""),
                "field_count": 0,
                "field_types": Counter(),
            },
        )
        meta["field_count"] = int(meta["field_count"]) + 1
        meta["field_types"][row.get("field_type", "")] += 1

    rows.sort(key=lambda row: (row["dataset_id"], row["field_id"]))
    index_columns = source_columns + ["keywords"]
    index_dir = output_dir / "index"
    dataset_dir = index_dir / "fields_by_dataset"
    write_csv(index_dir / "field_keyword_index.csv", rows, index_columns)
    for dataset_id in sorted(by_dataset):
        dataset_rows = sorted(by_dataset[dataset_id], key=lambda row: row["field_id"])
        write_csv(dataset_dir / f"{dataset_id}.csv", dataset_rows, index_columns)

    try:
        source_display_path = fields_path.relative_to(ROOT).as_posix()
    except ValueError:
        source_display_path = fields_path.name
    manifest = {
        "schema_version": "wq-field-catalog.v1",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source": {
            "path": source_display_path,
            "bytes": fields_path.stat().st_size,
            "sha256": sha256_file(fields_path),
            "columns": source_columns,
        },
        "scope": {
            "regions": sorted(key for key in regions if key),
            "universes": sorted(key for key in universes if key),
            "delays": sorted(key for key in delays if key),
        },
        "counts": {
            "fields": len(rows),
            "datasets": len(by_dataset),
            "categories": len(categories),
        },
        "distributions": {
            "categories": dict(sorted(categories.items())),
            "field_types": dict(sorted(field_types.items())),
            "regions": dict(sorted(regions.items())),
            "universes": dict(sorted(universes.items())),
            "delays": dict(sorted(delays.items())),
        },
        "artifacts": {
            "keyword_index": "index/field_keyword_index.csv",
            "dataset_directory": "index/fields_by_dataset",
            "dataset_file_count": len(by_dataset),
            "keyword_index_columns": index_columns,
        },
        "datasets": [
            {
                **{key: value for key, value in dataset_meta[dataset_id].items() if key != "field_types"},
                "field_types": dict(sorted(dataset_meta[dataset_id]["field_types"].items())),
                "path": f"index/fields_by_dataset/{dataset_id}.csv",
            }
            for dataset_id in sorted(dataset_meta)
        ],
    }
    manifest_path = output_dir / "field_catalog_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"fields={len(rows)}")
    print(f"datasets={len(by_dataset)}")
    print(f"sha256={manifest['source']['sha256']}")
    print(f"keyword_index={index_dir / 'field_keyword_index.csv'}")
    print(f"manifest={manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
