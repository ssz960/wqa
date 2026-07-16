from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = ROOT / "reports" / "data_fields" / "index" / "field_keyword_index.csv"
OUTPUT_COLUMNS = [
    "field_id",
    "dataset_id",
    "field_type",
    "description",
    "keywords",
    "coverage",
    "region",
    "delay",
]


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9_]{2,}", text.lower())


def score(row: dict[str, str], query_tokens: list[str]) -> int:
    field_id = row.get("field_id", "").lower()
    keywords = set(tokens(row.get("keywords", "")))
    description = row.get("description", "").lower()
    total = 0
    for token in query_tokens:
        if token == field_id:
            total += 100
        elif token in field_id:
            total += 20
        elif token in keywords:
            total += 8
        elif token in description:
            total += 3
    return total


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search the indexed WorldQuant field catalog.")
    parser.add_argument("--query", required=True, help="Field id, concept, or keyword query.")
    parser.add_argument("--dataset")
    parser.add_argument("--field-type")
    parser.add_argument("--region")
    parser.add_argument("--delay")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--format", choices=("csv", "json"), default="csv")
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    query_tokens = tokens(args.query)
    if not query_tokens:
        raise SystemExit("query must contain at least one alphanumeric token")

    matches: list[tuple[int, dict[str, str]]] = []
    with args.index.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if args.dataset and row.get("dataset_id", "").lower() != args.dataset.lower():
                continue
            if args.field_type and row.get("field_type", "").upper() != args.field_type.upper():
                continue
            if args.region and row.get("region", "").upper() != args.region.upper():
                continue
            if args.delay and row.get("delay", "") != args.delay:
                continue
            item_score = score(row, query_tokens)
            if item_score:
                matches.append((item_score, row))

    matches.sort(key=lambda item: (-item[0], item[1].get("field_id", "")))
    rows = [{key: row.get(key, "") for key in OUTPUT_COLUMNS} for _, row in matches[: max(1, args.limit)]]
    if args.format == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0

    writer = csv.DictWriter(__import__("sys").stdout, fieldnames=OUTPUT_COLUMNS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
