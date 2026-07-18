#!/usr/bin/env python3
"""Offline SQLite service for a verified wqa Active Snapshot."""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any, Iterator


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class RegistryError(RuntimeError):
    pass


class LocalRegistryService:
    def __init__(self, repository: Path, database: Path, batch_size: int = 1000):
        self.repository = repository.resolve()
        self.database = database.resolve()
        self.batch_size = max(100, min(int(batch_size), 5000))

    def _path(self, relative: str) -> Path:
        path = (self.repository / relative).resolve()
        try:
            path.relative_to(self.repository)
        except ValueError as exc:
            raise RegistryError("manifest path escapes repository") from exc
        return path

    def verify(self, manifest_relative: str) -> dict[str, Any]:
        manifest_path = self._path(manifest_relative)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("coverage_status") not in {"COMPLETE", "PARTIAL"}:
            raise RegistryError("invalid coverage_status")
        seen: set[str] = set()
        for entry in manifest.get("files", []):
            relative = entry.get("path", "")
            if relative in seen:
                raise RegistryError(f"duplicate manifest path: {relative}")
            seen.add(relative)
            path = self._path(relative)
            if not path.is_file() or path.stat().st_size != entry.get("bytes"):
                raise RegistryError(f"size mismatch: {relative}")
            if sha256_file(path) != str(entry.get("sha256", "")).lower():
                raise RegistryError(f"hash mismatch: {relative}")
        return manifest

    def sync(self, manifest_relative: str) -> dict[str, Any]:
        manifest = self.verify(manifest_relative)
        self.database.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.database)
        try:
            connection.executescript("""
                PRAGMA journal_mode=WAL;
                PRAGMA synchronous=NORMAL;
                DROP TABLE IF EXISTS staging_fields;
                DROP TABLE IF EXISTS staging_datasets;
                DROP TABLE IF EXISTS staging_operators;
                DROP TABLE IF EXISTS staging_profiles;
                CREATE TABLE staging_fields(
                    snapshot_id TEXT NOT NULL, field_id TEXT NOT NULL, dataset_id TEXT NOT NULL,
                    field_name TEXT NOT NULL, description TEXT, field_type TEXT NOT NULL,
                    region TEXT NOT NULL, universe TEXT NOT NULL, delay INTEGER NOT NULL,
                    PRIMARY KEY(snapshot_id, field_id, region, universe, delay));
                CREATE TABLE staging_datasets(
                    snapshot_id TEXT NOT NULL, scope_key TEXT NOT NULL, region TEXT NOT NULL,
                    universe TEXT NOT NULL, delay INTEGER NOT NULL, dataset_id TEXT NOT NULL,
                    dataset_name TEXT, dataset_category TEXT, field_count INTEGER,
                    PRIMARY KEY(snapshot_id, scope_key, dataset_id));
                CREATE TABLE staging_operators(
                    snapshot_id TEXT NOT NULL, operator_id TEXT NOT NULL, signature TEXT NOT NULL,
                    category TEXT, description TEXT, access_level TEXT,
                    compatibility_status TEXT NOT NULL, PRIMARY KEY(snapshot_id, operator_id));
                CREATE TABLE staging_profiles(
                    snapshot_id TEXT NOT NULL, instrument_type TEXT NOT NULL, region TEXT NOT NULL,
                    universe TEXT NOT NULL, delay INTEGER NOT NULL, neutralization TEXT NOT NULL,
                    field_coverage_status TEXT NOT NULL,
                    PRIMARY KEY(snapshot_id, instrument_type, region, universe, delay, neutralization));
                CREATE TABLE IF NOT EXISTS registry_state(
                    singleton INTEGER PRIMARY KEY CHECK(singleton=1), snapshot_id TEXT NOT NULL,
                    manifest_path TEXT NOT NULL, source_commit TEXT NOT NULL, activated_at TEXT NOT NULL);
            """)
            snapshot_id = manifest["snapshot_id"]
            entries = {entry["kind"]: entry for entry in manifest["files"]}
            counts = {
                "fields": self._import_fields(connection, snapshot_id, self._path(entries["fields"]["path"])),
                "datasets": self._import_datasets(connection, snapshot_id, self._path(entries["datasets"]["path"])),
                "operators": self._import_operators(connection, snapshot_id, self._path(entries["operators"]["path"])),
                "profiles": self._import_profiles(connection, snapshot_id, self._path(entries["legal_profiles"]["path"])),
            }
            for kind, expected in (("fields", entries["fields"]), ("datasets", entries["datasets"]), ("operators", entries["operators"]), ("profiles", entries["legal_profiles"])):
                if counts[kind] != int(expected["record_count"]):
                    raise RegistryError(f"record count mismatch for {kind}")
            connection.executescript("""
                DROP TABLE IF EXISTS fields; ALTER TABLE staging_fields RENAME TO fields;
                DROP TABLE IF EXISTS datasets; ALTER TABLE staging_datasets RENAME TO datasets;
                DROP TABLE IF EXISTS operators; ALTER TABLE staging_operators RENAME TO operators;
                DROP TABLE IF EXISTS simulation_profiles; ALTER TABLE staging_profiles RENAME TO simulation_profiles;
                CREATE INDEX fields_lookup ON fields(snapshot_id, region, dataset_id, field_type, field_id);
                CREATE INDEX fields_text ON fields(snapshot_id, region, field_name, field_id);
                CREATE INDEX datasets_lookup ON datasets(snapshot_id, region, universe, delay, dataset_id);
            """)
            connection.execute("DELETE FROM registry_state")
            connection.execute(
                "INSERT INTO registry_state VALUES(1,?,?,?,?)",
                (snapshot_id, manifest_relative, manifest["source_commit"], manifest["generated_at"]),
            )
            connection.commit()
            return {"status": "ACTIVE", "snapshot_id": snapshot_id, "counts": counts}
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _batches(self, rows: Iterator[tuple[Any, ...]]) -> Iterator[list[tuple[Any, ...]]]:
        batch: list[tuple[Any, ...]] = []
        for row in rows:
            batch.append(row)
            if len(batch) >= self.batch_size:
                yield batch
                batch = []
        if batch:
            yield batch

    def _import_fields(self, db: sqlite3.Connection, snapshot: str, path: Path) -> int:
        def rows() -> Iterator[tuple[Any, ...]]:
            with gzip.open(path, "rt", encoding="utf-8", newline="") as handle:
                for row in csv.DictReader(handle):
                    yield (snapshot, row["field_id"], row["dataset_id"], row["field_name"], row["description"], row["field_type"].upper(), row["region"].upper(), row["universe"].upper(), int(row["delay"]))
        return self._insert(db, "INSERT INTO staging_fields VALUES(?,?,?,?,?,?,?,?,?)", rows())

    def _import_datasets(self, db: sqlite3.Connection, snapshot: str, path: Path) -> int:
        def rows() -> Iterator[tuple[Any, ...]]:
            with gzip.open(path, "rt", encoding="utf-8", newline="") as handle:
                for row in csv.DictReader(handle):
                    yield (snapshot, row["scope_key"], row["region"], row["universe"], int(row["delay"]), row["dataset_id"], row["dataset_name"], row["dataset_category"], int(row["field_count"]))
        return self._insert(db, "INSERT INTO staging_datasets VALUES(?,?,?,?,?,?,?,?,?)", rows())

    def _import_operators(self, db: sqlite3.Connection, snapshot: str, path: Path) -> int:
        def rows() -> Iterator[tuple[Any, ...]]:
            with path.open("r", encoding="utf-8") as handle:
                for line in handle:
                    row = json.loads(line)
                    yield (snapshot, row["operator_id"], row["signature"], row["category"], row["description"], row["access_level"], row["compatibility_status"])
        return self._insert(db, "INSERT INTO staging_operators VALUES(?,?,?,?,?,?,?)", rows())

    def _import_profiles(self, db: sqlite3.Connection, snapshot: str, path: Path) -> int:
        def rows() -> Iterator[tuple[Any, ...]]:
            with path.open("r", encoding="utf-8", newline="") as handle:
                for row in csv.DictReader(handle):
                    yield (snapshot, row["instrument_type"], row["region"], row["universe"], int(row["delay"]), row["neutralization"], row["field_coverage_status"])
        return self._insert(db, "INSERT INTO staging_profiles VALUES(?,?,?,?,?,?,?)", rows())

    def _insert(self, db: sqlite3.Connection, sql: str, rows: Iterator[tuple[Any, ...]]) -> int:
        count = 0
        for batch in self._batches(rows):
            db.executemany(sql, batch)
            count += len(batch)
        return count

    def search_fields(self, *, region: str, keyword: str = "", dataset_id: str = "", field_type: str = "", top_k: int = 10) -> list[dict[str, Any]]:
        limit = max(1, min(int(top_k), 50))
        db = sqlite3.connect(self.database)
        db.row_factory = sqlite3.Row
        try:
            state = db.execute("SELECT snapshot_id FROM registry_state WHERE singleton=1").fetchone()
            if state is None:
                raise RegistryError("no Active Snapshot")
            clauses = ["snapshot_id=?", "region=?"]
            params: list[Any] = [state[0], region.upper()]
            if dataset_id:
                clauses.append("dataset_id=?"); params.append(dataset_id)
            if field_type:
                clauses.append("field_type=?"); params.append(field_type.upper())
            if keyword:
                clauses.append("(lower(field_id) LIKE ? OR lower(field_name) LIKE ? OR lower(description) LIKE ?)")
                pattern = f"%{keyword.lower()}%"; params.extend([pattern, pattern, pattern])
            params.append(limit)
            rows = db.execute(
                "SELECT snapshot_id,field_id,dataset_id,field_name,field_type,region,universe,delay,description FROM fields WHERE " + " AND ".join(clauses) + " ORDER BY field_id LIMIT ?",
                params,
            ).fetchall()
            return [dict(row) for row in rows]
        finally:
            db.close()

    def validate_operator(self, operator_id: str) -> dict[str, Any]:
        db = sqlite3.connect(self.database); db.row_factory = sqlite3.Row
        try:
            row = db.execute("SELECT o.* FROM operators o JOIN registry_state s ON o.snapshot_id=s.snapshot_id WHERE o.operator_id=?", (operator_id,)).fetchone()
            if row is None:
                raise RegistryError("operator not in Active Snapshot")
            return dict(row)
        finally:
            db.close()

    def validate_profile(self, profile: dict[str, Any]) -> dict[str, Any]:
        db = sqlite3.connect(self.database)
        try:
            state = db.execute("SELECT snapshot_id FROM registry_state WHERE singleton=1").fetchone()
            if state is None:
                raise RegistryError("no Active Snapshot")
            values = (state[0], profile["instrument_type"], profile["region"], profile["universe"], int(profile["delay"]), profile["neutralization"])
            row = db.execute("SELECT field_coverage_status FROM simulation_profiles WHERE snapshot_id=? AND instrument_type=? AND region=? AND universe=? AND delay=? AND neutralization=?", values).fetchone()
            if row is None:
                raise RegistryError("illegal Simulation Profile")
            return {"snapshot_id": state[0], "profile": profile, "field_coverage_status": row[0], "simulation_profile_hash": canonical_hash(profile)}
        finally:
            db.close()
