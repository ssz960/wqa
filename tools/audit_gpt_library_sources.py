from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOTS = (".", "reports", "docs", "research_center", "research_memory", "skills", "reports_server")
EXTENSIONS = {".md", ".csv", ".json", ".zip", ".txt", ".pdf"}
NAME_PATTERN = re.compile(
    r"gpt|forum|template|material|research.?pack|consultant|genius|power.?pool|probe|prompt|skill|audit|factor",
    re.IGNORECASE,
)
EXCLUDED_PARTS = {".git", ".venv", "tmp", "backups", "pending_delete", "brain_data", "gpt_library"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def classify(path: Path) -> tuple[str, str]:
    value = path.as_posix().lower()
    if value.startswith("reports_server/"):
        return "SERVER_MIRROR", "INDEX_ONLY"
    if "/outputs/" in value or "material_manager_" in value:
        return "GENERATED_HISTORY", "INDEX_ONLY"
    if value.startswith("skills/"):
        return "SKILL_REFERENCE", "INDEX_ONLY"
    if "research_package" in value or "research-pack" in value:
        return "RESEARCH_PACK", "REVIEW_FOR_COMPLETENESS"
    if "template" in value or "forum" in value or "material" in value:
        return "RESEARCH_MATERIAL", "REVIEW_FOR_CURATED_COPY"
    if "consultant" in value or "genius" in value or "audit" in value:
        return "GOVERNANCE_EVIDENCE", "REVIEW_FOR_CURATED_COPY"
    if "gpt" in value or "prompt" in value:
        return "GPT_CONTEXT", "REVIEW_FOR_CURATED_COPY"
    return "RELATED_RESOURCE", "INDEX_ONLY"


def discover(roots: list[str]) -> list[dict[str, str | int]]:
    seen: set[Path] = set()
    rows: list[dict[str, str | int]] = []
    for root_name in roots:
        root = (ROOT / root_name).resolve()
        if not root.exists():
            continue
        if root == ROOT.resolve():
            candidates = [path for path in root.iterdir() if path.is_file()]
        elif root.is_file():
            candidates = [root]
        else:
            discovered: list[Path] = []
            for current, directories, filenames in os.walk(root):
                directories[:] = [name for name in directories if name.lower() not in EXCLUDED_PARTS]
                discovered.extend(Path(current) / name for name in filenames)
            candidates = discovered
        for path in candidates:
            if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
                continue
            relative = path.resolve().relative_to(ROOT.resolve())
            if relative in seen or any(part.lower() in EXCLUDED_PARTS for part in relative.parts):
                continue
            if not NAME_PATTERN.search(relative.as_posix()):
                continue
            seen.add(relative)
            category, action = classify(relative)
            stat = path.stat()
            content_hash = ""
            hash_status = "SKIPPED_INDEX_ONLY"
            if action != "INDEX_ONLY" and stat.st_size <= 25 * 1024 * 1024:
                content_hash = sha256(path)
                hash_status = "SHA256"
            elif stat.st_size > 25 * 1024 * 1024:
                hash_status = "SKIPPED_GT_25_MIB"
            rows.append(
                {
                    "source_path": relative.as_posix(),
                    "category": category,
                    "recommended_action": action,
                    "bytes": stat.st_size,
                    "modified_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).replace(microsecond=0).isoformat(),
                    "hash_status": hash_status,
                    "sha256": content_hash,
                }
            )
    return sorted(rows, key=lambda row: (str(row["category"]), str(row["source_path"])))


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory scattered GPT/WQ research resources without moving originals.")
    parser.add_argument("--output", default="reports/gpt_library/source_inventory_current.csv")
    parser.add_argument("--root", action="append", dest="roots")
    args = parser.parse_args()
    rows = discover(args.roots or list(DEFAULT_ROOTS))
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("source_path", "category", "recommended_action", "bytes", "modified_utc", "hash_status", "sha256"),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"inventory_rows={len(rows)} output={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
