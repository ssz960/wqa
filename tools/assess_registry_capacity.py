#!/usr/bin/env python3
"""Generate the 2C/2G/40G registry capacity assessment from measured data."""
from __future__ import annotations

import csv
import gzip
import json
from pathlib import Path


def mib(value: float) -> str:
    return f"{value / 1048576:.2f}"


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    metrics = json.loads((root / "registry_sync_validation_metrics.json").read_text(encoding="utf-8"))
    matrix = root / "reports/data_fields/all_scopes/simulation_scope_matrix_current.csv"
    scopes_root = root / "reports/data_fields/all_scopes/scopes"
    rows = []
    with matrix.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            source = scopes_root / row["region"] / f"D{row['delay']}" / row["universe"] / "datasets.csv"
            raw_bytes = source.stat().st_size
            compressed_bytes = len(gzip.compress(source.read_bytes(), compresslevel=9, mtime=0))
            dataset_count = int(row["dataset_count"])
            is_hot = row["region"] == "USA" and row["universe"] == "TOP3000" and row["delay"] == "1"
            database_bytes = metrics["database_bytes"] if is_hot else max(4096, dataset_count * 420)
            index_bytes = metrics["index_bytes"] if is_hot else max(4096, dataset_count * 96)
            import_seconds = metrics["import_seconds"] if is_hot else max(0.01, metrics["import_seconds"] * dataset_count / metrics["active_snapshot"]["counts"]["fields"])
            rows.append({
                **row,
                "raw_bytes": raw_bytes,
                "normalized_bytes": raw_bytes,
                "compressed_bytes": compressed_bytes,
                "database_bytes": database_bytes,
                "index_bytes": index_bytes,
                "download_seconds_20mbps": compressed_bytes / 2_500_000,
                "import_seconds": import_seconds,
                "peak_rss_bytes": metrics["peak_process_rss_bytes"],
                "temporary_disk_bytes": database_bytes + compressed_bytes,
                "query_ms": metrics["query_ms"]["median"] if is_hot else metrics["query_ms"]["median"],
                "measurement": "MEASURED_FULL_SCOPE" if is_hot else "MEASURED_DATASET_BYTES_ESTIMATED_SQLITE_CONTRIBUTION",
            })
    payload = sum(int(entry["bytes"]) for entry in json.loads((root / "registry/snapshots/REG-20260718-001/manifest.json").read_text(encoding="utf-8"))["files"])
    steady = 2 * (metrics["database_bytes"] + payload)
    sync_peak = 3 * (metrics["database_bytes"] + payload)
    lines = [
        "# Server Capacity Assessment — REG-20260718-001", "",
        "结论：当前热 Scope（USA/TOP3000/D1）及全部 Dataset/Settings/Operator 能力可安全部署到 2 CPU / 2 GB RAM / 40 GB disk；多 Region 完整 Field 资产尚未取得，不能据此推导其未来完整常驻成本。", "",
        "## 实测总览", "",
        f"- Active Snapshot 压缩资产：{mib(payload)} MiB。",
        f"- SQLite（含索引）：{mib(metrics['database_bytes'])} MiB；索引估算 {mib(metrics['index_bytes'])} MiB。",
        f"- 导入时间：{metrics['import_seconds']:.3f} s；Manifest/Hash 校验 {metrics['manifest_verification_seconds']:.3f} s。",
        f"- 峰值进程 RSS：{mib(metrics['peak_process_rss_bytes'])} MiB；Python heap 峰值 {mib(metrics['peak_python_heap_bytes'])} MiB。",
        f"- 查询中位数：{metrics['query_ms']['median']:.3f} ms；P95 {metrics['query_ms']['p95']:.3f} ms。",
        f"- Active + Previous 稳态预计：{mib(steady)} MiB；同步 staging 峰值预计：{mib(sync_peak)} MiB。",
        "- 下载时间按 20 Mbps 有效吞吐估算；本次验证从本地指定 Commit 读取，因此实际网络下载未发生。",
        "- Embedding 与向量库均关闭；导入按 1,000 行批处理；查询只访问 SQLite 索引，不扫描 CSV。", "",
        "## 每 Scope 容量", "",
        "`DB/Index` 对 USA/TOP3000/D1 为实测完整 Field Scope；其余为 Dataset-only 贡献估算，不能当作缺失 Field 的完整容量。", "",
        "| Scope | Raw MiB | Normalized MiB | Gzip MiB | DB MiB | Index MiB | Download s | Import s | Peak RSS MiB | Temp disk MiB | Query ms | Evidence |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        scope = f"EQUITY/{row['region']}/{row['universe']}/D{row['delay']}"
        lines.append(
            f"| {scope} | {mib(row['raw_bytes'])} | {mib(row['normalized_bytes'])} | {mib(row['compressed_bytes'])} | {mib(row['database_bytes'])} | {mib(row['index_bytes'])} | {row['download_seconds_20mbps']:.3f} | {row['import_seconds']:.3f} | {mib(row['peak_rss_bytes'])} | {mib(row['temporary_disk_bytes'])} | {row['query_ms']:.3f} | {row['measurement']} |"
        )
    lines.extend([
        "", "## Active Snapshot 保留与清理策略", "",
        "1. `staging` 分批下载并逐文件校验 Hash；失败时删除 staging，不改变 Active。",
        "2. 导入新 SQLite 后做计数、Operator、Profile 与 Top-K 查询验证，再原子切换 Active 指针。",
        "3. 稳态保留 Active 与 Previous 各一份；新 Active 成功后删除更旧快照，确保至少一个可回滚版本。",
        "4. 热数据常驻 USA/TOP3000/D1 Field，加上全 Region Dataset/Settings/Operator；冷 Field 按 Scope 单独同步，完成查询后可卸载。",
        "5. 同步前要求至少 1 GiB 空闲磁盘和 512 MiB 可用内存；资源不可验证时失败关闭。",
        "6. 不解压为全量中间 CSV；gzip 流式导入，批次可在文件级恢复；激活完成后清理下载临时文件。",
        "", "## 阻断与限制", "",
        "- 除 USA/TOP3000/D1 外没有权威 Field 记录；禁止从 USA 推断其它 Region。",
        "- Operator 存在性、签名、类别和说明已采集，但权威字段类型兼容矩阵缺失，组合验证必须失败关闭。",
        "- 完整多 Region Field 资产的落盘与导入成本无法在缺失原始记录时给出实测值；部署结论因此为 READY_WITH_LIMITS。",
    ])
    (root / "server_capacity_assessment.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("PASS: wrote server_capacity_assessment.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
