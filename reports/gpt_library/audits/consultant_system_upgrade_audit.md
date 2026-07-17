# Consultant Gold / BRAIN Genius 回测主链升级审计与分阶段设计

日期：2026-07-16  
范围：只读审计、设计和验收门；本轮不修改生产代码、不部署、不重启服务、不触发真实回测、不导入队列、不提交 Alpha、不设置 Osmosis points。

## 0. 执行结论

当前生产链仍是“一个 Alpha row 对应一个 `/simulations` URL、一个稳定单回测 worker、正好 3 槽”的系统。Consultant/Genius 目标不能通过把 `3` 改成 `80` 达成：Multi-Simulation 需要 parent/child 数据模型，日预算需要可审计的 reservation ledger，Consultant 需要组合目标和人工候选审阅，权限需要每次只读探测并 fail closed。

推荐最小路径是：保留现有 3-slot single transport 和队列/事件/恢复/research-pack 主链，在同一个 worker 内增加 capability-aware multi transport；先做本地 mock/replay 和 schema，随后在用户单独批准后以 1×3/1×5 小批量观察，再逐级放大。未完成政策切换前，生产 P0 仍是服务 active、配置 `--single-slots 3`、worker `--parallel-slots 3`、补位 `3/3`。

### 证据分类（GPT 知识库必须保留标签）

| 标签 | 含义 | 本报告用法 |
|---|---|---|
| `LIVE_ACCOUNT` | 2026-07-16 已登录 Chrome 页面直接可见 | Gold、2026-Q3、Genius 状态、当前 scopes、Signals/Pyramids 等 |
| `OFFICIAL_DOC` | BRAIN Help Center/Learn 官方页面 | Gold 字段/操作符比例、Pyramid 规则、VF 定义、Genius 资格条件 |
| `FORUM_EXPERIENCE` | 顾问论坛经验或建议 | 低相关/多样性、提交前复核、Osmosis 操作经验；不能变成硬门槛 |
| `USER_CONFIRMED_NEEDS_RUNTIME_PROBE` | 用户已明确报告但未获官方接口/真实响应确认 | `8×10`、日上限 `5,000`、day boundary、计费和 parent/child 计数方式 |

任何 `USER_CONFIRMED_NEEDS_RUNTIME_PROBE` 能力在探测前只能作为候选上限，不能写入硬规则。探测失败时使用安全 3-slot single 模式。

## 1. 当前真实调用链与运行时证据

### 1.1 生产调用链

```text
worldquant-backtest.service
  -> autonomous_research_loop.py --single-slots 3
  -> backtest_from_store.py
  -> stable_single_backtest.py --parallel-slots 3
  -> alpha_store.reserve_next_backtest_items()
  -> POST /simulations (一个表达式/一个任务)
  -> Location 轮询与 fetch_metrics()
  -> alpha_store.alphas + backtests + queue_events
  -> 每小时指标（six checks/PnL/correlation）
  -> run_daily_pull_pc_selfcorr_pack.bat
  -> pipeline_orchestrator.py recent
  -> research_pack_builder.py
  -> FULL_RESEARCH_PACK/COMPLETE 门禁
```

每日 FULL 链路冻结 24h target window，拉取/切片、展开 checks JSON、构建 target IDs、填充 six checks/PnL、合并 self-corr/product-corr、预检 100% 覆盖、打包并做 postflight manifest acceptance。当前资产要求 `COMPLETE`，lane plan 明确 `research_advice_only=true`、`auto_queue=false`。

### 1.2 当前真实运行时与 DB

- 2026-07-16 只读远程证明：`worldquant-backtest=active`，命令包含 `--single-slots 3`，live worker 包含 `--parallel-slots 3`，`active_slots=3/3`，队列约 530、running 3，alternate flag 不存在。该证明来自现有 P0 报告/日志；再次切换或重启不在本轮范围。
- 2026-07-14 三个完整小时为 44、48、48 个终态回测，P50 约 216–246 秒，实际稳定吞吐约 44–50/h；这是 3-slot single 的生产基线，不是 Consultant entitlement。
- `alpha_store.db`（本地，mtime 2026-07-13）有 1,029 个 alpha、5,121 个 queue events、`done=169`、`queued=860`；`alpha_store_server.db`（本地旧快照，mtime 2026-07-03）有 60,635 个 alpha、3,770,921 个 events、`running=3`、`queued=3,203`。两者不是当前远程 DB 的替代品，不能据此宣称实时状态。
- 两个 DB 都没有 `simulation_batches`、`daily_simulation_budget`、`capability_snapshots`；说明父子/预算/权限审计层尚未落地。

### 1.3 单任务数据模型的限制

`alphas` 目前以 `simulation_url`、`platform_alpha_id`、`submitted_at`、`reserved_batch_id` 等字段承载一条平台 simulation。`backtests` 以 `alpha_id` 一对一保存状态和指标，`queue_events` 只记录 alpha 事件。Multi-Simulation 会产生一个 parent Location 与 2–10 个 child Alpha ID：若仍只写一行，会丢失 child 部分失败、parent 超时、child 完成但写库失败、重启幂等和按 child 计费信息。因此必须新增 batch/child 表并保持旧 row 可读。

## 2. “正好 3 槽”硬编码、测试、watchdog 与政策清单

| 位置 | 证据 | 类型 | 改造前处理 |
|---|---|---|---|
| `agents.md:27-29` | P0 exact 3；alternate flag 才可停主服务；部署后验证 3/3 | 政策 | 保持不变，待用户批准后改写为 capability contract |
| `ai_memory/ACTIVE_REQUIREMENTS.md:6-7,26` | exact 3；小时子指标不得增加主链并发 | 政策 | 保留并增加 legacy-safe 条款 |
| `worldquant-backtest.service:2,12` | `--single-slots 3` | service | 只读记录；切换前不得编辑 |
| `worldquant-backtest-watchdog.service/.timer:2` | three-slot 描述 | watchdog policy | 切换前继续报警 |
| `autonomous_research_loop.py:580,634-635,603,998,1000,1519,2214,2386` | parser 默认 3、CURRENT_MAX_BACKTEST_SLOTS/总槽位 | runtime | 拆为 single 与 batch 指标，不直接替换 |
| `backtest_from_store.py:11,18,29,46-47` | 描述/默认 3，强制 `args.single_slots=3`，启动 worker 3 | launcher | 保留 single fallback；新增 capability 参数解析 |
| `stable_single_backtest.py:584-637,784,1186,1196` | 单 payload POST；`min(3, ...)`；active_jobs 与 3-slot stats | transport | 保持 single；新增 multi parent/child transport |
| `pipeline_watchdog.py:166,168-199,389,446-468` | required slots、`--availability-only`、3/3 检查 | guardrail | 设计双态 watchdog 后再改政策 |
| `tests_backtest_availability.py:18,45-73` | required_slots=3、service/worker 命令断言 | test | 先增加 legacy tests，不删除旧断言 |
| `tests_production_guardrails.py:652,1876,3909,4330,4355,4384,4440,4671` | 3/3、daemon command、single slots 3 | test | 迁移为 profile 参数化 |
| `tests_hourly_brief_formatter.py:69-70` | 期待“运行 3/3” | presentation test | 同时支持 `single=3/3; batch=x/y` |
| `resume_3slot_production.py:138,238` | 固定恢复为 3 | recovery | 作为安全回滚入口保留 |
| `scripts/server_tune_150h.sh:20` | server 命令 3 | server helper | 仅在政策批准后另加 multi 参数 |
| `alpha_store.py:3091-3097` | `configured_slots()` 默认 3 | scheduler/export config | 不把它误当成 transport 并发；拆分 batch/child 配置 |
| `alpha_store.py:2558+` | `queue_stats_snapshot(total_slots)` 只数 running rows | observability | 增加 parent/child 维度，保留旧字段 |
| `ai_memory/SERVER_STATE.md`, `HANDOFF_CURRENT.md`, P0 日志 | 当前/历史 3-slot 证据 | policy/evidence docs | 更新时保留历史证据和切换时间 |
| `ai_memory/DAILY_RESEARCH_PACK_PLAYBOOK.md:203`、FULL 报告 | 远程 3-slot healthy 门 | research-pack gate | 改为 profile-aware，但 COMPLETE-only 不变 |

搜索到的“3/3”若只是报告步骤编号、三项指标或 CSV 文本，不应误判为 slot policy；上表只列会控制、守护或断言并发的点。

## 3. 当前恢复、暂停、队列与指标语义

- `reserve_next_backtest_items()` 只从 queued、priority>0、retry cooldown 清除的 alpha 中预留；写入 `reserved_batch_id/reserved_at/reservation_expires_at`。
- `stable_single_backtest.submit()` 为一条表达式提交一个 payload，保存 Location；轮询遇到 `Retry-After/PENDING/RUNNING`，完成后写 platform id 与指标。
- `recover_running_jobs()` 通过 `status='running' AND simulation_url` 恢复单任务；`cleanup_queue_state()` 处理 reservation 15 分钟、无 identity 的 running、最长收集超时并回队列冷却。
- pause 先 drain running 再保留 paused_running 顺序；resume 按顺序继续；score-zero 不硬删除，只排除 `queued_available`/reservation；queue prune 非破坏性。
- SQLite 锁定时 `append_and_import_safely()` 保留 pending import row；`emit_event()` 写入 queue event 并在 error/timeout/rate_limited 更新 last_error。
- `queue_stats_snapshot()` 把 running row 当槽位；Multi-Simulation 后必须同时显示 `active_batches`、`active_children`、`single_active`，不能把 parent 当一个 child 或把 80 个 child 当 80 个 legacy slots。

## 4. Capability Contract（只读、版本化、fail closed）

### 4.1 Snapshot schema 草案

```json
{
  "schema_version": "capability_snapshot.v1",
  "snapshot_id": "uuid",
  "captured_at": "ISO-8601",
  "account": {"account_tier": "CONSULTANT_GOLD", "genius_level": "GOLD", "source": "LIVE_ACCOUNT", "confidence": 1.0},
  "regular": {"max_concurrent_batches": null, "max_children_per_batch": null, "source": null, "confidence": 0.0},
  "super": {"max_single_concurrency": null, "multi_supported": null, "source": null, "confidence": 0.0},
  "daily": {"simulation_cap": null, "day_boundary": null, "failure_counts": null, "count_basis": null, "source": null, "confidence": 0.0},
  "entitlements": {"regions": [], "delays": [], "universes": [], "operators": [], "datasets": [], "fields": [], "source": null, "confidence": 0.0},
  "probe": {"status": "CONFIRMED|PARTIAL|FAILED", "api_version": null, "evidence_refs": [], "expires_at": null, "error_class": null}
}
```

必须记录：REGULAR 最大并发 batch、每 batch 最大 child、SUPER 单回测并发、每日 simulation cap、平台日界线、失败请求是否计费、Multi-Simulation 按 parent 还是 child 计数，以及真实 region/delay/universe/operator/dataset/field entitlement。每个字段单独保存 source、captured_at、confidence、evidence_ref，不能用整份 snapshot 的一个置信度掩盖缺失字段。

### 4.2 探测顺序与关闭规则

1. 读取官方 account/capability API 或受支持的只读响应 header/JSON；其次读取页面上明确的当前账户状态。
2. 对受控的只读 capability endpoint 做 schema 验证；不得用提交 Alpha 的方式试探上限。
3. 将用户的 `8×10` 和 `5,000/day` 作为待确认值写入 evidence ledger，不作为可执行 cap。
4. 任一关键字段（account tier、regular batch/child 上限、daily cap 或计数方式）缺失、过期、响应矛盾或认证失败，`probe.status=FAILED/PARTIAL`，调度 profile 自动回到 `single_slots=3`，multi transport 禁止提交。
5. snapshot 过期时只允许已知安全 profile；不得从旧 USA 字段快照推断 Consultant entitlement。

## 5. DB migration 草案（增量、可回滚）

不修改旧 `alphas/backtests/queue_events` 语义，新增表和 nullable 扩展：

```sql
CREATE TABLE capability_snapshots (
  snapshot_id TEXT PRIMARY KEY, schema_version TEXT NOT NULL, captured_at TEXT NOT NULL,
  account_tier TEXT, genius_level TEXT, payload_json TEXT NOT NULL,
  probe_status TEXT NOT NULL, expires_at TEXT, source_refs_json TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE simulation_batches (
  batch_id TEXT PRIMARY KEY, parent_request_key TEXT UNIQUE NOT NULL,
  platform_location TEXT, request_type TEXT NOT NULL, mode TEXT NOT NULL,
  capability_snapshot_id TEXT, requested_children INTEGER NOT NULL,
  reserved_children INTEGER NOT NULL DEFAULT 0, submitted_children INTEGER NOT NULL DEFAULT 0,
  completed_children INTEGER NOT NULL DEFAULT 0, failed_children INTEGER NOT NULL DEFAULT 0,
  status TEXT NOT NULL, idempotency_key TEXT UNIQUE NOT NULL,
  reserved_at TEXT, reservation_expires_at TEXT, submitted_at TEXT, finished_at TEXT,
  retry_after TEXT, last_error TEXT, metadata_json TEXT,
  FOREIGN KEY(capability_snapshot_id) REFERENCES capability_snapshots(snapshot_id)
);

CREATE TABLE simulation_batch_children (
  child_id TEXT PRIMARY KEY, batch_id TEXT NOT NULL, alpha_id INTEGER NOT NULL,
  child_index INTEGER NOT NULL, platform_alpha_id TEXT, child_status TEXT NOT NULL,
  child_request_hash TEXT NOT NULL, submitted_at TEXT, completed_at TEXT,
  imported_at TEXT, error_class TEXT, error_detail TEXT, metrics_json TEXT,
  UNIQUE(batch_id, child_index), UNIQUE(batch_id, alpha_id),
  FOREIGN KEY(batch_id) REFERENCES simulation_batches(batch_id)
);

CREATE TABLE daily_simulation_budget (
  platform_day TEXT PRIMARY KEY, day_boundary_source TEXT, daily_cap INTEGER,
  reserved_children INTEGER NOT NULL DEFAULT 0, submitted_children INTEGER NOT NULL DEFAULT 0,
  counted_failures INTEGER NOT NULL DEFAULT 0, released_reservations INTEGER NOT NULL DEFAULT 0,
  last_authoritative_response_at TEXT, ledger_version INTEGER NOT NULL DEFAULT 1,
  metadata_json TEXT
);
```

建议给 `alphas` 增加 nullable `batch_id`, `child_index`, `child_status`, `child_request_hash`, `capability_snapshot_id`；给 `backtests` 增加 `batch_id/child_id/parent_status/import_status`。迁移先 `CREATE TABLE`、索引和双写 shadow ledger，旧 single 读取路径不依赖新表；以 `PRAGMA user_version` 和向前/向后迁移脚本保证回滚。

## 6. Parent/child 状态机与恢复

### 6.1 状态

`PLANNED -> RESERVED -> SUBMITTING -> SUBMITTED -> POLLING -> (PARTIAL|COMPLETE|FAILED_RETRYABLE|FAILED_TERMINAL)`；任一阶段可进入 `RECOVERY_REQUIRED`；child 级别可为 `PENDING/RUNNING/SUCCEEDED/FAILED_RETRYABLE/FAILED_TERMINAL/IMPORT_PENDING/IMPORTED`；parent 终态为 `COMPLETE`（全部 child imported）、`PARTIAL`（至少一个 imported 且其余 terminal）、`FAILED_TERMINAL`（无可用 child）或 `ABORTED`。

### 6.2 关键转换和幂等

| 事件 | 处理 |
|---|---|
| parent request accepted | 只写一次 `idempotency_key` 和 platform location；重复 2xx/Location 不得新建 batch |
| parent 429/5xx/网络超时 | 读取 Retry-After；保留 reservation，超过 reservation timeout 才释放；不重复提交已确认的 parent |
| child invalid/4xx | 标记该 child terminal，其他 child 继续；按官方计费响应更新 budget |
| 部分 child 完成 | 逐 child 写指标和平台 Alpha ID；parent 保持 PARTIAL/POLLING，不重发整个 batch |
| child 完成但 DB 写失败 | 写 durable `IMPORT_PENDING`/outbox；重启按 child request hash 和平台 ID 幂等导入 |
| parent 超时 | 对未知 child 先查询 parent/child 状态；查询失败进入 RECOVERY_REQUIRED，而不是盲目重发 |
| worker 重启 | 从 batch/child 表恢复；旧 `simulation_url` row 仍由 single recovery 处理 |
| reservation timeout | 未提交 child 释放预算并回队；已提交 child 不回滚计费 |

Parent 的平台 Location、每个 child 的 Alpha ID 和 request hash 必须可审计；不能用 parent 一行覆盖 child 失败。

## 7. 预算、指标与动态调度

### 7.1 必备实时指标

`active_batches`、`active_children`、`simulations_used_today`、`daily_cap`、`reserved_budget`、`target_children_per_hour`、P50/P95 parent/child latency、parent/child 429、可重试/终态失败率、backlog、server CPU/memory、official-visible-alpha/hour、scope/intent 产出。

### 7.2 安全 pacing 算法

设 `remaining = daily_cap - counted_submitted - reserved_budget`，`hours_left` 来自探测到的平台 day boundary，`backlog` 为兼容且非 score-zero 的候选数，`safe_rate` 为最近窗口按 P95 延迟、429、失败率和服务器资源折减后的 child/h：

```text
target_children_per_hour = min(
  safe_rate,
  remaining / max(hours_left, safety_window_hours),
  backlog / max(hours_left, 1),
  user_goal_rate_if_explicit
)
```

保留 `reserved_budget` 防止多进程超卖；只在 authoritative daily response 确认失败计费语义后计入 `counted_failures`。day boundary 未知时不做跨日追赶，使用保守单槽；429 连续上升、P95 超阈、服务器资源越界或 ledger 不一致时降级/暂停。

### 7.3 升级阶梯

| 阶梯 | 进入条件（全部满足） | 退出/回滚 |
|---|---|---|
| 1×5 | capability snapshot 完整；mock/replay 通过；用户批准有限 live probe；资源与 3-slot single 无冲突 | 任一 parent/child 幂等、429、写库错误回 3-slot |
| 1×10 | 1×5 soak 稳定，P95 和失败率在批准阈值内，预算 ledger 无超卖 | 连续错误/预算未知回 1×5 或 single |
| 2×10 | backlog 足够、剩余预算可覆盖安全窗口、近窗 429 低、server 资源有余量 | 预算/资源/429 任一越界回 1×10 |
| 4×10 | 至少一个日周期历史回放 + 用户批准；parent/child recovery 和 FULL pack 兼容 | 仅在 burst 或故障追赶需要时短暂启用 |
| 8×10 | 官方/真实 runtime 明确确认 entitlement、计数和日 cap；多周期 soak；P0 政策已切换 | 未满足则禁止；8×10 是峰值上限而非默认目标 |

即使用户报告 `5,000/day`，稳定目标也先按日预算和 150 official-visible-alpha/hour 目标反推，不默认跑满 8×10。

## 8. Batch Builder 与恢复设计

从现有 reservation 结果按 `REGULAR/SUPER`、region、delay、universe、run_intent、priority、scope、neutralization/truncation/decay 等兼容设置分组。每组最多 10 child；同一 parent 不混入平台不兼容设置。先按质量、去重、Pyramid 缺口和组合目标排序；低于最小 batch 时允许 single fallback，不为凑 10 条引入低质量候选。

保留 pause/resume、score-zero、history、queue prune、reservation timeout、旧任务恢复。Batch reservation 必须可部分释放：只释放未提交 child，已提交 child 继续轮询。旧 row 的 `simulation_url` 仍是 single source；新增 batch row 不得覆盖它。

## 9. Consultant 质量门与人工候选

将现有 `failed_submission_rules()` 从“一次布尔判断”拆为可解释维度：

1. IS：Sharpe、Fitness、Returns、Drawdown、Nan、six checks；
2. Margin、Weight、Sub-universe、Turnover；
3. Self Corr、Product Corr、同模板/字段/操作符相关；
4. 最近两年或滚动窗口稳定性、PnL 集中、coverage、long/short 平衡；
5. 字段数、操作符数、复杂度、region/delay/dataset category；
6. Pyramid 归属、`pyramid_count_per_alpha`（1–2 座有效，超过 2 座按官方规则计 0）；
7. diversity impact、`vf_proxy`、`combined_proxy`、Osmosis scope fit。

“平台绿灯”仅表示平台基础提交检查通过，不等于适合 Consultant 组合。输出 `consultant_submission_candidate_review`，包含 pass/warn/reject、证据指标、预计 Pyramid 贡献、冲突资产、人工理由；绝不自动提交。

## 10. 组合目标模型

### 10.1 Pyramid

`pyramid_key = region + delay + dataset_category`。矩阵记录已有 Alpha、缺口、每座塔数量和候选贡献；每个 Alpha 最多计入 1–2 座，超过 2 座不计 Genius Pyramid count（官方规则），但仍可进入其他组合指标。dataset category 必须来自认证权限快照，不能从 neutralization 猜。

### 10.2 Diversity、VF proxy、Combined

- `diversity_impact`：region/delay/universe/dataset/category/field/operator/template 的边际覆盖、与现有池的相关惩罚、重复度。
- `vf_proxy`：质量、低 self/product corr、近窗稳定、唯一性和多样性的代理分；明确标注“不是预测真实 VF”，不得用于声称未来 VF。
- `combined_proxy`：将候选加入组合后的加权收益/风险、相关、coverage、Pyramid/Osmosis 贡献；不是官方 Combined Alpha Performance。
- `osmosis_candidate_review`：只生成 scope 覆盖、10-alpha 缺口、质量冲突和建议 points 报告；不写平台 points。
- `alpha_type_plan`：RA/ATOM/PPAC/SA 分类与各自质量/多样性目标；SuperAlpha 的真实限制仍需探测。

## 11. 数据权限刷新方案

建立 `snapshot_id/region/delay/universe/category/dataset` 版本目录，保存 dataset id/category、field id/type、operator id、可见性、账户 tier、来源 API/page、抓取时间、TTL、hash、probe status。当前 USA canonical 8,599 rows/20 datasets/9 categories 与旧 5,905 server snapshot 都保留为证据，不能直接覆盖。

生成器只读取最新且未过期的认证 snapshot；缺失/矛盾/过期则 fail closed，禁止用旧 USA 快照假装全量 Consultant。每次权限变化生成 delta ledger，记录新增、撤销和 hash 变化；数据权限与运行 capability snapshot 通过 snapshot_id 关联。

## 12. FULL_RESEARCH_PACK 升级（保持 COMPLETE-only）

以下是新增/扩展资产建议。每个资产都写入 manifest，空表仍必须有固定 header；只有数据源明确完成或按合同允许的空表规则时，才可 `COMPLETE`。任何缺失必为 `PARTIAL/INCOMPLETE`，不以空文件伪装成功。

| 文件 | 数据源/关键字段 | 空表规则 | ledger/cache 与性能风险 | 门禁 |
|---|---|---|---|---|
| `capability_snapshot.csv` | capability_snapshots；snapshot、tier、limits、source、time、confidence | 探测失败可有一行 FAILED+原因，不可无 header | append-only evidence，按 snapshot cache；低 | 关键能力缺失则 pack 标注 probe_failed，不能启用 multi |
| `daily_simulation_budget.csv` | daily ledger；platform_day、cap、reserved/submitted/count-fail、boundary | 未确认 cap 用 NULL+source，不填 5000 | 每日一行+事件 delta；低 | 不得超卖；计费语义未确认需 warning |
| `multi_simulation_throughput.csv` | batch/child events；active、P50/P95、429、失败率、child/h | 尚未启用可空但必须说明 `transport_not_enabled` | 窗口聚合，避免每 child 全量重复；中 | 与 single 指标分开，不污染 3-slot proof |
| `pyramid_progress_matrix.csv` | alpha metadata + entitlement；key、count、candidate_contribution | 无认证 category 时空表+gap | 增量 ledger；中 | 每 Alpha 1–2 座计数规则可复算 |
| `field_operator_diversity_ledger.csv` | fields/operators/templates + corr | 无新候选可空 | hash/delta cache；中 | 不能越权读取旧快照 |
| `vf_proxy_review.csv` | quality/corr/diversity/proxy | 无真实 VF 时仍可输出代理，必须 `proxy_only=true` | 组合重算窗口 cache；中 | 禁止命名为真实 VF |
| `combined_portfolio_review.csv` | portfolio candidate add/remove、risk/corr/coverage | 无候选可空 | 组合矩阵 cache；高 | 明示非官方 Combined |
| `osmosis_candidate_review.csv` | scope、alpha count、quality、points recommendation | 不足 scope 可列缺口 | 仅建议 ledger；低 | 禁止平台写 points |
| `scope_dataset_backlog.csv` | entitlement gap、region/delay/category/dataset | 无缺口可空 | snapshot keyed；低 | 缺权限不能入队 |
| `consultant_submission_candidate_review.csv` | quality dimensions、green status、manual decision、reason | 无候选可空 | append-only human review；低 | 不自动提交 |
| `research_data_gap_report.csv` | missing checks/fields/corr/permissions | 无 gap 输出 header+`gap_count=0` | 与 manifest 对账；低 | FULL preflight 可解释 |

继续保留 `submit-hunt`、`repair_method_feedback`、`high_corr_asset_review`、`daily_batch_lane_plan`、`batch_research_funnel`、资产台账快照和每日 delta。新增资产不改变现有 `FULL_RESEARCH_PACK/COMPLETE`、100% target coverage、manifest/ZIP 校验和 advice-only 语义；性能高风险资产采用窗口聚合、hash cache、增量 ledger，禁止每次全库笛卡尔积。

## 13. 政策冲突与正式切换

当前 `agents.md`、`ACTIVE_REQUIREMENTS.md`、service、watchdog、availability/production tests 将“正好 3 槽”定义为 P0。两种可回滚选择：

1. **更新主系统 P0 合约**：用户批准后将 P0 改为“经认证 capability profile 下的 batch/child 上限、日预算、资源和 3-slot fallback 均满足”，同时保留 legacy single assertions；修改 service、watchdog、tests、handoff、playbook 和验收证据。
2. **启用 alternate system**：用户明确切换到另一 server-side backtest system 后，创建 `/root/worldquant/ALTERNATE_BACKTEST_SYSTEM.flag`，按既有规则停止 primary；删除 flag 则立即恢复 primary 3-slot。不能用 flag 绕过未批准的 multi transport。

在用户批准前，只允许本地 mock、历史回放和只读 capability probe；不得改 P0、部署、重启、真实回测、队列、Alpha 或 Osmosis。

## 14. 逐文件修改清单（本轮仅设计，不修改）

| 文件/模块 | 未来变更 | 本轮状态 |
|---|---|---|
| `worldquant-backtest.service`, watchdog units | capability profile 注入、双态健康检查 | 未改 |
| `autonomous_research_loop.py` | single/multi transport 路由、budget tick、降级 | 未改 |
| `backtest_from_store.py` | 保留 3-slot fallback，读取 snapshot/profile | 未改 |
| `stable_single_backtest.py` | 抽取 single transport；新增 parent/child client 和幂等 | 未改 |
| `alpha_store.py` | migration、batch/child ledger、事件和旧 row 兼容 | 未改 |
| `slot_scheduler.py` | active batch/child 与 budget pacing | 未改 |
| `pipeline_watchdog.py` | profile-aware checks；legacy 3-slot safety alarm | 未改 |
| `failed_submission_rules` / research actions | 质量维度、人工候选视图 | 未改 |
| `pipeline_orchestrator.py`, `research_pack_builder.py` | 新资产、manifest、COMPLETE 门禁 | 未改 |
| `reports/data_fields/*` | Consultant entitlement snapshots/delta | 未改 |
| tests | mock/replay、迁移、状态机、预算、旧回归、pack 完整性 | 未改 |
| `agents.md`, `ai_memory/*` | 用户批准后的 P0/切换记录 | 未改 |

## 15. 测试矩阵

| 领域 | 必测场景 | 通过证据 |
|---|---|---|
| Capability | 完整、部分、过期、API 429、矛盾响应、认证失败 | snapshot fixture、fail-closed=3-slot |
| Schema | fresh DB、旧 DB、重复 migration、回滚 | schema version、row count、旧查询不变 |
| Parent/child | 2/5/10 child、parent 429、child 4xx、部分失败、超时、重启 | replay event log、无重复提交/无重复入库 |
| Idempotency | 同 idempotency key 重试、DB 写失败后恢复 | unique constraint、outbox/import pending 清零 |
| Budget | 跨日、reserved 超时、失败计费未知/已知、预算耗尽 | ledger 不超卖、保守降级 |
| Scheduler | 1×5→1×10→2×10，429/P95/资源回压 | pacing trace 与阶梯决策 |
| Queue | pause/resume、score-zero、prune、legacy running recovery | 旧行为快照一致 |
| Quality | 六检查+Margin/Weight/SU/Turnover/self/product corr/rolling/coverage | 每候选可解释 reason |
| Portfolio | Pyramid 1–2 座、>2 座、diversity/VF proxy/combined/Osmosis | proxy_only、不可自动提交/配点 |
| Fields | USA 旧快照、Consultant 新 snapshot、撤销字段、过期 | source/hash/TTL、fail closed |
| Research pack | 新资产空表/非空、manifest、ZIP、COMPLETE/INCOMPLETE | package status 与现有 FULL contract 一致 |
| Production guardrail | primary active、3/3、alternate flag absent | 只读 live proof；未经批准不执行切换 |

## 16. 迁移、回滚与风险排序

迁移顺序：先只读 snapshot 与 schema shadow ledger；再 mock/replay parent/child；再 single worker 内 feature-flagged multi transport；再预算/调度；再 Consultant 组合报告；最后才考虑有限 live probe。每步均可关闭 multi flag 回到旧 single，保留旧 `alphas.simulation_url` 恢复逻辑和 `resume_3slot_production.py`。

风险排序：

1. **高**：错误计费/日界线/parent-child 计数导致预算超卖；解决：官方/真实响应确认、reserved ledger、保守 fail closed。
2. **高**：DB 一对一模型丢 child 或重复提交；解决：唯一 idempotency、child request hash、outbox/recovery replay。
3. **高**：政策与 watchdog 误报或失去 3-slot 回滚；解决：双态 profile、保留 legacy tests、先更新政策再切换。
4. **中高**：权限 snapshot 过期造成越权或漏跑；解决：TTL、source/hash、旧快照仅证据。
5. **中**：多样性 proxy 被误认为真实 VF/Combined；解决：字段命名 `proxy_only`、人工审阅和官方结果回填。
6. **中**：FULL pack 变慢或完整性破坏；解决：增量 ledger、窗口聚合、固定 header、COMPLETE-only gate。
7. **中**：低质量候选为凑 batch 进入队列；解决：最小 batch 回退 single、质量/priority 先于 batch size。

## 17. 阶段、协作边界与验收门

- **Phase0 能力探测**：只读 API/page/runtime probe，输出带来源、时间、置信度的 snapshot；无真实回测副作用。
- **Phase1 父子模型和 mock/replay**：migration、状态机、幂等、恢复、旧路径回归；验收为 8×10 replay 全部可重放且无重复入库。
- **Phase2 预算与调度**：daily ledger、pacing、429/P95/资源回压；验收为模拟跨日、预算耗尽、backlog catch-up 永不超 cap。
- **Phase3 Consultant 质量和组合目标**：quality dimensions、Pyramid/diversity/VF proxy/Combined/Osmosis 报告；验收为人工候选可解释且零自动提交/配点。
- **Phase4 有限实盘验证**：用户另行批准后 1×3/1×5、soak、可回滚；验收由用户批准阈值和 live evidence 决定。
- **Phase5 生产切换**：先完成 P0 合约更新或 alternate flag 决策，再逐级扩大；验收含 service/worker、DB、budget、官方可见结果、FULL pack 和回滚证据。

协作边界：Codex 负责工程实现、只读快照、状态机、数据完整性和测试；GPT 负责研究包复盘、repair 方法、高相关资产、每日 batch 路线、Pyramid/VF/Combined/Osmosis 建议；用户保留生产切换、真实并发提升、Alpha 提交和 Osmosis 配点的最终审批权。

## 18. 推荐最小改造路径（立即/需探测/需批准）

**可立即开发（本地/mock/replay）**：schema migration 草案与 fixture、parent/child 状态机、idempotency/outbox、旧 DB 兼容、预算算法离线模拟、profile-aware 指标、FULL pack 空表/manifest 设计、Consultant 候选报告和字段 snapshot 目录。

**必须先完成只读 runtime probe**：REGULAR batch/child 上限、SUPER 并发、日 cap 真实值、day boundary、失败是否计费、parent/child 计数方式、真实 regions/delays/universes/operators/datasets/fields、Multi-Simulation parent/child 响应结构。

**必须等待用户单独批准**：任何真实 Multi-Simulation、1×3 以上并发、生产 service/watchdog/P0 政策修改、停止 primary、创建 alternate flag、Alpha 提交和 Osmosis points 写入。

最小可行目标不是重写系统，而是在同一主 worker 增加第二种 transport，复用当前 DB 队列、事件、恢复和 research pack；3-slot single 永远作为能力探测失败、预算不明、429/资源异常和生产回滚的安全底座。

## 19. 给 GPT 的审阅指令

请先将本报告按四类证据写入知识库，再输出正式实施方案。不得把论坛经验写成官方门槛，不得把 `8×10/5,000` 写成未经探测的硬规则，不得把 `vf_proxy`/`combined_proxy` 写成真实 VF/Combined 预测，不得自动提交 Alpha 或设置 Osmosis points。正式方案必须先给 schema、状态机、测试、迁移/回滚和政策变更清单，再提出任何生产动作。

## 20. 主要来源

官方/账户页面：

- [Genius status](https://platform.worldquantbrain.com/genius/)
- [Simulate](https://platform.worldquantbrain.com/simulate)
- [Gold benefits](https://support.worldquantbrain.com/hc/en-us/articles/26715911101719-What-are-the-main-benefits-of-advancing-to-higher-levels) (`OFFICIAL_DOC`)
- [Genius qualification](https://support.worldquantbrain.com/hc/en-us/articles/26715993801879-How-do-I-qualify-for-the-higher-levels) (`OFFICIAL_DOC`)
- [Pyramids](https://support.worldquantbrain.com/hc/en-us/articles/26716012806295-What-are-pyramids) (`OFFICIAL_DOC`)
- [Value Factor](https://support.worldquantbrain.com/hc/en-us/articles/11591947651607-What-is-the-Value-Factor) (`OFFICIAL_DOC`)
- [VF and Weight](https://support.worldquantbrain.com/hc/en-us/articles/6161094877079-How-much-impact-do-Weight-and-ValueFactor-OS-performance-have-on-a-Quarterly-Payment) (`OFFICIAL_DOC`)

论坛经验：顾问资格/实战、VF 近期经验、Osmosis 操作帖，均只作 `FORUM_EXPERIENCE`，不作硬规则。代码与证据：`worldquant-backtest.service`、`autonomous_research_loop.py`、`backtest_from_store.py`、`stable_single_backtest.py`、`alpha_store.py`、`slot_scheduler.py`、`pipeline_watchdog.py`、`skills/brain-simAlphasinBatch-and-track/scripts/ace_lib.py`、`reports/audits/DATA_FIELDS_AND_ROOT_CLEANUP_AUDIT_20260716.md`、`ai_memory/PIPELINE_CHANGE_LOG_20260714_HOURLY_METRICS_THROUGHPUT_P0.md`、`reports/FULL_RESEARCH_PACK_P0_ASSETS_20260716.md`。
