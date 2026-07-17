#!/usr/bin/env python3
"""Deterministic search over the generated WorldQuant field keyword index.

The script intentionally uses only the Python standard library so it works in a
fresh checkout.  The full CSV remains the source of truth; the compact keyword
index is the default read path for interactive retrieval.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = ROOT / "reports" / "data_fields" / "index" / "field_keyword_index.csv"
TOKEN_RE = re.compile(r"[\w]+", re.UNICODE)


def tokens(value: str) -> set[str]:
    return {token.casefold() for token in TOKEN_RE.findall(value or "") if len(token) > 1}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search the deterministic WorldQuant available-field keyword index."
    )
    parser.add_argument("--query", nargs="+", help="One or more terms; every term must match.")
    parser.add_argument("--dataset", help="Exact dataset_id filter.")
    parser.add_argument("--category", help="Exact dataset_category filter.")
    parser.add_argument("--field-type", help="Exact field_type filter, e.g. MATRIX or VECTOR.")
    parser.add_argument("--region", help="Exact region filter, e.g. USA.")
    parser.add_argument("--universe", help="Exact universe filter, e.g. TOP3000.")
    parser.add_argument("--delay", help="Exact delay filter.")
    parser.add_argument("--limit", type=int, default=20, help="Maximum rows to return (default: 20).")
    parser.add_argument(
        "--format",
        choices=("text", "csv", "tsv", "json"),
        default="text",
        dest="output_format",
        help="Output format (default: text).",
    )
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX, help="Keyword index path.")
    parser.add_argument(
        "--list-datasets",
        action="store_true",
        help="List dataset IDs and counts instead of searching.",
    )
    return parser.parse_args()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def row_matches(row: dict[str, str], args: argparse.Namespace) -> bool:
    filters = {
        "dataset_id": args.dataset,
        "dataset_category": args.category,
        "field_type": args.field_type,
        "region": args.region,
        "universe": args.universe,
        "delay": args.delay,
    }
    return all(expected is None or row.get(key, "").casefold() == expected.casefold() for key, expected in filters.items())


def score_row(row: dict[str, str], query_tokens: set[str]) -> int:
    if not query_tokens:
        return 0
    weighted = {
        "field_id": 8,
        "field_name": 7,
        "dataset_id": 5,
        "dataset_name": 4,
        "dataset_category": 3,
        "description": 2,
        "keywords": 1,
        "notes": 1,
    }
    score = 0
    for key, weight in weighted.items():
        value_tokens = tokens(row.get(key, ""))
        score += weight * len(query_tokens & value_tokens)
    return score


def searchable_tokens(row: dict[str, str]) -> set[str]:
    return set().union(
        *(tokens(row.get(key, "")) for key in (
            "field_id",
            "field_name",
            "dataset_id",
            "dataset_name",
            "dataset_category",
            "description",
            "keywords",
            "notes",
        ))
    )


def search(rows: Iterable[dict[str, str]], args: argparse.Namespace) -> list[dict[str, str]]:
    query_tokens = tokens(" ".join(args.query or []))
    matches: list[dict[str, str]] = []
    for row in rows:
        if not row_matches(row, args):
            continue
        score = score_row(row, query_tokens)
        if query_tokens and not query_tokens.issubset(searchable_tokens(row)):
            continue
        item = dict(row)
        item["_score"] = str(score)
        matches.append(item)
    matches.sort(
        key=lambda row: (
            -int(row["_score"]),
            row.get("dataset_id", ""),
            row.get("field_id", ""),
        )
    )
    return matches[: max(args.limit, 0)]


def write_rows(rows: list[dict[str, str]], output_format: str) -> None:
    clean_rows = [{key: value for key, value in row.items() if key != "_score"} for row in rows]
    if output_format == "json":
        json.dump(clean_rows, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return
    if not clean_rows:
        return
    columns = list(clean_rows[0])
    delimiter = "\t" if output_format == "tsv" else ","
    if output_format == "text":
        for row in rows:
            print(
                f"{row.get('field_id', '')}\t{row.get('dataset_id', '')}\t"
                f"{row.get('field_type', '')}\t{row.get('description', '')}"
            )
        return
    writer = csv.DictWriter(sys.stdout, fieldnames=columns, delimiter=delimiter, lineterminator="\n")
    writer.writeheader()
    writer.writerows(clean_rows)


def main() -> int:
    args = parse_args()
    if args.limit < 0:
        raise SystemExit("--limit must be non-negative")
    if not args.index.exists():
        raise SystemExit(f"index not found: {args.index}")
    rows = read_rows(args.index)
    if args.list_datasets:
        counts: dict[str, int] = {}
        for row in rows:
            if row_matches(row, args):
                counts[row.get("dataset_id", "")] = counts.get(row.get("dataset_id", ""), 0) + 1
        for dataset_id in sorted(counts):
            print(f"{dataset_id}\t{counts[dataset_id]}")
        return 0
    write_rows(search(rows, args), args.output_format)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
