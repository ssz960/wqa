# WQ Consultant / Genius 权限与现有回测框架差距审阅

日期：2026-07-16  
用途：交给 GPT 审阅并更新知识库；下一步由 GPT 输出正式改造方案。  
边界：本轮只浏览、审计和写报告；未触发回测、未导入队列、未修改生产服务、未提交 Alpha。

## 1. 结论先行

账号已经进入正式 Consultant，并处于 BRAIN Genius Gold。变化不只是“3 个单回测槽变成最多 8 个 Multi-Simulation、每批最多 10 个子回测”以及“日上限从 1,800 变成 5,000”，而是研究目标整体变化：

1. 原框架主要解决“稳定跑完、通过平台 IS 提交检查、补齐本地相关性并形成研究包”。
2. Consultant 阶段必须同时优化四件事：单 Alpha 质量、近期提交组合的 OS 表现、跨地区/数据集/字段/操作符的多样性、Genius/Osmosis 组合表现。
3. 现有生产主链仍是硬编码的 3 个单回测槽，单个队列任务对应一次 `/simulations` 请求；它没有 Multi-Simulation 父子任务模型，也没有 5,000/日预算控制。
4. 现有 `failed_submission_rules()` 只检查 Sharpe、Fitness、Turnover，以及部分平台 Weight/Sub-universe/Self-correlation 结果。它没有 Margin、Product Correlation、近期年度趋势、Pyramid、VF/Combined/Osmosis 影响、字段/操作符复杂度和组合多样性。
5. 因此不能只把 `3` 改成 `80`。应先把主链改造成“能力发现 + 日预算 + Multi-Simulation 父子批次 + 组合目标层 + 人工提交审阅”的统一系统。
6. 8×10 是峰值能力，不应当默认 24 小时跑满。按现有 216–246 秒单回测延迟估算：
   - 维持 `150/h` 约需 9–11 个等效并发子回测；
   - 若一天用满 5,000 次，24 小时均匀速率约为 `208/h`，约需 13–15 个等效并发子回测；
   - 两个 10-child 批次在延迟相近时已经可能满足日预算，8×10 更适合故障恢复后的追赶、短时高峰和能力冗余。

## 2. 证据等级

本报告把信息分为四类，GPT 更新知识库时不得混写：

- `LIVE_ACCOUNT`：2026-07-16 在用户已登录 Chrome 中直接读取的当前账号页面。
- `OFFICIAL_DOC`：BRAIN 官方 Help Center / Learn 页面。
- `FORUM_EXPERIENCE`：顾问专属论坛中的经验与实操建议，不等于平台硬规则。
- `USER_CONFIRMED_NEEDS_RUNTIME_PROBE`：用户明确告知，但本轮网页未出现可直接读取的官方计数；实现前必须用只读 API/真实响应再确认。

## 3. 当前账号与 Genius 权限

### 3.1 当前等级和季度状态（LIVE_ACCOUNT）

- 当前等级：Gold。
- 最佳等级：Gold。
- 当前季度：2026-Q3，2026-07-01 至 2026-09-30。
- 当前季度页面显示：Signals `0`、Pyramids Completed `0`、Combined Alpha Performance 待月度计算。
- 当前最大连续模拟天数：`73`。
- Expert 门槛：`20 Signals + 10 Pyramids`。
- Master 门槛：`120 Signals + 30 Pyramids`。
- Grandmaster 门槛：`220 Signals + 60 Pyramids`。
- Combined Alpha Performance 的具体当季数值门槛未在当前空白账号状态中可靠显示，必须动态读取，不能写死。

### 3.2 Gold 权益（OFFICIAL_DOC）

官方权益页当前列出的 Gold 权益：

- 数据字段：约全部可用字段的 `50%`。
- 操作符：约全部操作符的 `45%`。
- 基础研究地区：USA、ASI、EUR、GLB、CHN、IND；页面还列出额外地区/地区组合选择，但表格排版存在歧义，实际权限必须以账号 API 返回为准。
- SuperAlpha：提交 `100+` Alpha 后解锁；Gold 只能使用自己的 Alpha 作为 SuperAlpha 组件。
- 生物识别重新登录间隔：4 小时。

当前 Genius 状态页列出的 Osmosis/Pyramid scope 包括：

- USA/D1、USA/D0、GLB/D1、EUR/D1、EUR/D0、ASI/D1、CHN/D0、CHN/D1、JPN/D1、JPN/D0、IND/D1、MEA/D1。

注意：状态页展示 scope 不必然等于所有 scope 都已开放回测。调度器必须从账号 API/数据接口读取真实 entitlement，不能仅依赖静态页面表格。

### 3.3 当前数据面基线（LIVE_ACCOUNT + LOCAL_AUDIT）

2026-07-16 已有审计记录：

- 本地 canonical 字段表仍只有 USA：8,599 行、20 个 dataset、9 个 category。
- BRAIN Data 页面可见 17 个 category，覆盖 ASI、CHN、EUR、GLB、IND、JPN、MEA、USA 的不同组合。
- 因此本地字段白名单已经不能代表 Consultant Gold 的完整研究空间。

需要建立按 `region/delay/universe/category/dataset` 版本化的权限快照，保留旧 USA 表作为回滚证据，不得直接覆盖后丢失来源。

## 4. 新概念解释

### 4.1 VF 是什么

VF = Value Factor。

官方定义的核心是：VF 衡量近期提交的 Alpha 组合在 OS（Out-of-Sample）阶段的表现，同时考虑：

1. 单 Alpha 表现；
2. 近期提交的多样性；
3. 相对自己历史提交以及其他顾问提交的独特性。

官方文档还明确：

- VF 范围 `0–1`，历史平均值约 `0.5`；
- VF 同时影响 Base Payment 和 Quarterly Payment；
- Quarterly Payment 中，VF 与所有 Alpha/SuperAlpha 的 Weight 影响程度相近。

重要限制：VF 是 OS 组合结果，不能由当前 IS 指标精确预测。现阶段只能用低 PC、低自相关、跨 scope/数据集/字段/模板的多样性、稳定 PnL、合理 Margin/Turnover 等做代理风险控制，然后等待真实 VF 更新验证。

官方 VF 文章存在历史时点表述冲突（季度更新、后续改为月度更新）；论坛新手指南称按近期窗口月度更新。知识库不得硬编码窗口，必须在 Performance 页面或当前官方规则中再次确认。

### 4.2 Pyramid（点塔）是什么

官方定义：一个 Pyramid 是 `region + delay + dataset category` 的组合，例如 `USA-D1-analyst`。

- 在同一 Pyramid 至少提交 3 个 Alpha，才算完成一座塔。
- 从 2025-Q2 起，一个 Alpha 最多贡献 2 座 Genius Pyramid。
- 如果一个 Alpha 涉及超过 2 个 Pyramid，则它对 Pyramid 计数贡献为 0，但仍可计入 Base Payment 和其他 Genius 指标。
- Currency/Country/Exchange/Sector/Industry/Subindustry/Market 等 neutralization 字段不额外计塔。
- 更多 Pyramid 可能通过多样化改善 VF 和 Combined Alpha Performance。

这意味着现有“一个表达式越多字段越丰富越好”的生成思路可能反而破坏点塔效率。生成器应显式计算 `pyramid_count_per_alpha`，通常控制在 1–2。

### 4.3 Genius 六维与组合指标

当前页面的 tie-breaker/活动维度包括：

- Operators per Alpha；
- Operators used；
- Fields per Alpha；
- Fields used；
- Community activity；
- Max simulation streak；
- Simulation activity；
- Submission activity。

论坛高等级经验普遍强调“单 Alpha 少量操作符/字段，但组合总体覆盖更多操作符/字段”。这不是固定硬门槛，框架应把它建成可配置的组合指标，而不是写死为 `5 operators + 2 fields`。

### 4.4 Combined Alpha Performance

Genius 晋级的第三项硬条件是组合 Alpha 的 OS Sharpe，而不是单个 Alpha 的 IS Sharpe。当前页面还分别显示：

- Combined Alpha Performance；
- Combined Selected Alpha Performance；
- Combined Power Pool Alpha Performance；
- Combined Osmosis Performance。

现有研究包主要按单 Alpha 排名/修复，缺少“如果加入这个 Alpha，会让组合更好还是更差”的决策视图。

### 4.5 Osmosis

当前账号页面的硬规则：

- 至少 3 个 qualifying scopes；
- 每个 scope 至少 10 个 Alpha；
- 每个 scope 精确分配 100,000 points；
- 更多 scope 和 Alpha 可能提高分数。

论坛置顶实操帖说明（FORUM_EXPERIENCE）：

- Osmosis 是用户自己选择并配权的 Alpha 组合；
- Daily Osmosis Rank 可能形成 `1–2` 的 Base Payment 乘数；
- Combined Osmosis Performance 参与 Genius 季度评估；
- 分配方案在每周日 23:59 EST 截点，随后延迟进入计算；
- 应跨数据集、特征和操作符分散，不应为凑满 10 个而塞入劣质或逻辑重复 Alpha。

生产系统仍不得自动修改 Osmosis points。可以先生成“建议分配 CSV/报告”，由人审核后手工操作。

## 5. 回测权限变化：已确认与待确认

### 5.1 Multi-Simulation（USER_CONFIRMED + REPO_REFERENCE）

用户确认正式顾问权限为最多 `8 × 10`：最多 8 个并发 Multi-Simulation，每个最多 10 个子 Alpha。

仓库内 ACE 参考实现与此一致：

- `limit_of_concurrent_simulations` 允许 `1..8`；
- `limit_of_multi_simulations` 允许 `2..10`；
- REGULAR Alpha 可走 Multi-Simulation；
- SuperAlpha 不支持同样的 Multi-Simulation 路径，参考实现回退到 3 个 single concurrent simulations。

实现时必须把“batch 并发数”和“每批 child 数”分开建模，不能用一个 `slots=80` 代替。

### 5.2 每日 5,000 上限（USER_CONFIRMED_NEEDS_RUNTIME_PROBE）

用户确认日上限由 1,800 提升至 5,000。本轮在可见页面中没有找到官方计数器，因此：

- 方案可以以 5,000 作为候选 capability；
- 代码不得永久硬编码；
- 首次启用前应通过账号只读能力接口、响应 header 或接近日限时的明确平台响应确认；
- 必须确认平台日界线、REGULAR/SUPER 是否共用预算、失败请求是否计数、Multi-Simulation 是按 parent 还是 child 计数。

## 6. 现有主链与差距

### 6.1 当前主链

生产回测主链：

`worldquant-backtest.service`
→ `autonomous_research_loop.py --single-slots 3`
→ `backtest_from_store.py`
→ `stable_single_backtest.py --parallel-slots 3`
→ `POST /simulations`（单表达式）
→ 轮询 Location
→ 单 Alpha 结果写入 `alpha_store.py`
→ hourly metric / research pack。

当前 P0 约束要求服务和 worker 都必须保持正好 3 槽。没有用户明确切换以及对应 flag 时，不得把生产 worker 直接改成 8×10。

### 6.2 代码级硬编码

- `worldquant-backtest.service`：`--single-slots 3`。
- `backtest_from_store.py`：无条件把 `args.single_slots = 3`，启动参数也写死 `--parallel-slots 3`。
- `stable_single_backtest.py`：`min(3, ...)` 强行截断。
- `pipeline_watchdog.py` 和生产 guardrail 测试：以“必须 3 槽”为成功条件。
- `slot_scheduler.py`：lane/配额模型围绕 3 槽或少量单槽设计，不理解 batch/child。
- `alpha_store.queue_stats_snapshot()`：只统计 running rows 和 total slots，不理解一个 parent 对应多个 child。

### 6.3 任务/恢复语义差距

现有模型是：一个 DB row = 一个平台 simulation URL。Multi-Simulation 需要：

- 一个 parent request 对应 2–10 个 child；
- parent URL 与 child Alpha ID 的映射；
- parent 失败、部分 child 失败、child 完成但写库失败的分别恢复；
- 幂等重试，防止 parent 成功后重复提交整批；
- batch 级 429、单 child invalid、认证失败、超时的不同处理；
- worker 重启时恢复 parent 与全部 child，而不是把整个 batch 重新入队。

### 6.4 当前质量门过窄

`alpha_store.failed_submission_rules()` 当前只包含：

- Delay 1：Sharpe > 1.25、Fitness > 1.0；
- Delay 0：Sharpe > 2.0、Fitness > 1.3；
- `0.01 < Turnover < 0.70`；
- 部分平台 Weight、Sub-universe、Self-correlation fail。

它没有检查或表达：

- Margin；
- Product Correlation（论坛经验通常以 `<0.7` 为关键线，但必须以当前平台检查为准）；
- 与自己近期/历史提交的结构多样性；
- 近 2 年或滚动窗口稳定性、PnL 掉头；
- Pyramid 归属与每 Alpha 的 Pyramid 数；
- 字段/操作符总覆盖与单 Alpha 复杂度；
- 对 VF、Combined、Osmosis 的潜在增量；
- RA / ATOM / PPAC / SA 的差异化门槛。

“Submit 按钮变绿”只能代表平台基础提交检查通过，不能代表适合 Consultant 组合。

### 6.5 吞吐与预算

2026-07-14 的生产证据：3/3 worker 在三个完整小时完成 44、48、48 个回测，平均延迟 246.1、229.6、216.1 秒，实际天花板约 44–50/h。

因此新的容量控制应同时记录：

- `active_batches / max_batches`；
- `active_children / max_children`；
- `simulations_used_today / daily_cap`；
- `child_completed_per_hour`；
- `official_visible_alpha_per_hour`；
- parent/child 429、失败率、P50/P95 延迟；
- 各 scope、dataset category、run_intent 的消耗和产出。

## 7. 建议的目标架构

### 7.1 Capability Contract

每次 worker 启动先生成只读 capability snapshot，例如：

```json
{
  "account_tier": "CONSULTANT_GOLD",
  "regular": {"max_batches": 8, "max_children_per_batch": 10},
  "super": {"max_single_concurrency": 3},
  "daily_simulation_cap": 5000,
  "day_boundary": "DISCOVERED_NOT_HARDCODED",
  "regions": [],
  "operators_snapshot": "...",
  "data_entitlement_snapshot": "..."
}
```

能力读取失败或与批准配置漂移时 fail closed 到安全模式，不猜权限、不自动升并发。

### 7.2 统一主 worker，而不是新增旁路

保留当前 DB 队列、事件、恢复和研究包主链；将 single worker 演进为支持两种 transport：

- `single`：现有单任务路径，兼容 SuperAlpha 和安全回退；
- `multi`：REGULAR Alpha 的 parent/child 批次路径。

不要直接启用 `小工具` 或 skill 目录里的 ACE 代码作为第二套生产 worker。可以借鉴其 payload/progress 解析，但必须移植到当前主链的认证、事件、重试、恢复和 DB 事务模型中。

### 7.3 DB 模型

建议增加而不是破坏现有 row：

- `simulation_batches`：batch_id、platform_location、mode、status、submitted_at、retry_after、capability_snapshot_id。
- child row 增加：batch_id、child_index、platform_alpha_id、child_status、terminal_imported_at。
- `daily_simulation_budget`：平台日、已提交 child、失败是否计费、保留预算、最后权威响应。
- `capability_snapshots`：账号权限和来源证据。

所有迁移必须可回滚，旧 3-slot worker 仍能读取旧 row。

### 7.4 Batch Builder

Batch Builder 从现有 queue reservation 取任务，但要满足：

- 一批最多 10 child；
- REGULAR 与 SUPER 分流；
- 不把已知 invalid/score-zero/cooldown row 取入；
- 保留 run_intent 与质量优先；
- 可按 region/delay/universe 或兼容设置分组，以便诊断和预算归因；
- 低于最小批量时允许 single 回退，不能为了凑 10 个塞入低质量任务。

### 7.5 动态节流

建议不要第一天直接 8×10：

1. Mock/replay：8×10 父子状态、部分失败、重启恢复全部通过。
2. 实盘限量（需用户另行批准）：1×3 或 1×5。
3. 观察稳定后：1×10。
4. 以 150/h 和 5,000/日 pacing 为目标升到 2×10。
5. 只有 backlog、日剩余预算、低 429、低错误和资源余量同时满足时，才允许 4×10、6×10、8×10 的短时 burst。

调度器应算“本日剩余 child / 距离日界线剩余小时”，动态得到目标每小时速率，而不是始终跑满。

### 7.6 Consultant 研究目标层

在“是否值得进入人工提交候选”之前新增 portfolio objective，不得自动提交：

- `is_quality_gate`：当前六检查 + Margin + 稳定性。
- `correlation_gate`：Self Corr、Product Corr、结构/字段相似度。
- `pyramid_impact`：属于哪几座塔、是否超过 2 塔、能否补齐 `2/3 -> 3/3`。
- `diversity_impact`：新地区、dataset category、dataset、field、operator、template 的边际覆盖。
- `vf_proxy`：质量、低相关、独特性、多样性代理分；明确标注不是实际 VF。
- `combined_proxy`：加入候选后组合 IS/可用 OS 代理是否改善。
- `osmosis_candidate`：是否适合进入某个 scope 的至少 10 个组合及建议点数。
- `alpha_type_plan`：RA / ATOM / PPAC / SA 的目标和各自门槛。

### 7.7 数据权限刷新

建立新的版本化布局，例如：

`reports/data_fields/consultant/<snapshot_id>/<region>/<delay>/<universe>/...`

至少保存：dataset id/category、field id/type、region、delay、universe、可见性、抓取时间、账号 tier、hash、源接口。生成器只从最新已认证 snapshot 取字段，过期或缺失时 fail closed，不从旧 USA fallback 假装全量。

### 7.8 GPT 研究包更新

FULL_RESEARCH_PACK 后续应新增或扩展以下决策资产（具体文件名由下一轮方案确定，不能破坏当前 COMPLETE contract）：

- capability snapshot；
- daily budget / batch throughput；
- pyramid progress matrix；
- operator/field six-dimension coverage；
- VF proxy / diversity ledger；
- Combined/Osmosis candidate review；
- scope/dataset/category backlog；
- 人工提交候选清单及 reject reason。

## 8. 必须先解决的政策冲突

当前 `agents.md`、`ACTIVE_REQUIREMENTS.md`、service、watchdog 和 tests 把“正好 3 槽”定义为 P0。正式启用 Consultant multi worker 前，必须由用户明确选择：

1. 修改主系统的 P0 合约，从“3 single slots”升级为“已验证 Consultant capability 下的 batch/child 上限”；或
2. 明确切换到另一个 server-side backtest system，并按现有规则维护 `/root/worldquant/ALTERNATE_BACKTEST_SYSTEM.flag`。

在这个决定发生前，允许做本地/mock/replay 开发和只读能力探测，但不得把生产服务直接升到 8×10。

## 9. 建议实施阶段与验收门

### Phase 0：知识与能力审计

- GPT 更新 Consultant、Gold、VF、Pyramid、Genius、Osmosis、Multi-Simulation 知识。
- 用只读接口确认 8×10、5,000 日限、日界线、计费口径、SUPER 限制、真实 region/operator/data entitlement。
- 输出 capability snapshot 和差异报告。

验收：所有能力都有来源、时间戳和置信度；无回测副作用。

### Phase 1：父子批次数据模型与 mock/replay

- DB migration、batch builder、parent/child polling、幂等导入、重启恢复。
- 覆盖 200/201、Retry-After、429、4xx child invalid、部分完成、父任务超时、认证刷新、写库失败。

验收：8×10 mock 全部 child 精确一次入库；重启不重提；旧 3-slot 路径不回归。

### Phase 2：预算与调度

- 日预算 ledger、动态 pacing、batch/child 指标、scope/intent 配额。
- 保留 pause/resume/score-zero/history 语义。

验收：模拟跨日、失败计数、budget exhausted、backlog catch-up；永不越过 configured cap。

### Phase 3：Consultant 质量与组合目标

- 扩充质量门、Pyramid/diversity/VF proxy/Combined/Osmosis 视图。
- 只产出人工审阅候选，不自动 submit，不自动设置 Osmosis points。

验收：每个候选能解释“为何回测、为何保留、为何提交/不提交、对哪座塔和哪个组合有帮助”。

### Phase 4：有限实盘验证（必须另行批准）

- 从小 batch 开始，逐级放大。
- 每级至少验证服务 active、parent/child 完整、无重复、429/失败率、DB/队列时间戳推进、官方可见结果推进、资源稳定。

验收：达到批准档位并完成 soak；未达到则自动回退，不宣称完成。

### Phase 5：生产切换

- 用户明确更新 P0 合约或启用 alternate system flag。
- 部署、重启激活、服务/worker 命令验证、批次补位、10 分钟以上 live soak。

验收：source、process、DB、平台结果、预算 ledger 五类证据一致。

## 10. 需要 GPT 下一步回答的问题

把本报告交给 GPT 后，要求它先更新知识库，再给方案；不要直接改生产：

1. 当前账号的 8×10 和 5,000/日如何从官方 API/响应只读确认？
2. Multi-Simulation parent 的完整响应结构、child 映射和部分失败语义是什么？
3. SUPER、REGULAR、RA、ATOM、PPAC、SA 的实际回测/提交限制如何分流？
4. 当前 VF 的精确更新窗口与 Performance 页面字段是什么？
5. Product Correlation、Self Correlation、Margin、近年趋势、OS proxy 应如何分层，而不是混成一个 pass？
6. 当前 2026-Q3 Combined Alpha Performance 的等级门槛如何动态取得？
7. Gold 实际开放的 regions、operators、datasets、fields 如何形成版本化 entitlement snapshot？
8. 现有 `stable_single_backtest.py` 如何渐进重构，且保留旧 3-slot 回退和运行中任务恢复？
9. 如何让 5,000/日预算服务于 VF/Pyramid/Combined/Osmosis，而不是无脑堆量？
10. 哪些研究包 CSV/ledger 必须新增，且不破坏 FULL_RESEARCH_PACK 的 COMPLETE-only contract？

建议给 GPT 的明确指令：

> 先把本报告中的 LIVE_ACCOUNT、OFFICIAL_DOC、FORUM_EXPERIENCE、USER_CONFIRMED_NEEDS_RUNTIME_PROBE 分层写入知识库。然后只输出分阶段改造方案、DB schema、状态机、测试矩阵、迁移/回滚方案、政策变更清单和验收门。不要改代码、不要触发回测、不要导入队列、不要部署、不要提交 Alpha。所有未确认权限必须先设计只读 preflight。

## 11. 主要来源

### 当前账号页面

- `https://platform.worldquantbrain.com/genius/`
- `https://platform.worldquantbrain.com/genius/status`
- `https://platform.worldquantbrain.com/simulate`

### 官方文档

- Gold/Expert/Master/Grandmaster 权益：`https://support.worldquantbrain.com/hc/en-us/articles/26715911101719-What-are-the-main-benefits-of-advancing-to-higher-levels`
- 晋级条件：`https://support.worldquantbrain.com/hc/en-us/articles/26715993801879-How-do-I-qualify-for-the-higher-levels`
- Pyramid：`https://support.worldquantbrain.com/hc/en-us/articles/26716012806295-What-are-pyramids`
- Value Factor：`https://support.worldquantbrain.com/hc/en-us/articles/11591947651607-What-is-the-Value-Factor`
- VF/Weight 对 Quarterly Payment：`https://support.worldquantbrain.com/hc/en-us/articles/6161094877079-How-much-impact-do-Weight-and-ValueFactor-OS-performance-have-on-a-Quarterly-Payment`

### 顾问专属论坛

- 顾问专属中文论坛：`https://support.worldquantbrain.com/hc/en-us/community/topics/18910956638743-%E9%A1%BE%E9%97%AE%E4%B8%93%E5%B1%9E%E4%B8%AD%E6%96%87%E8%AE%BA%E5%9D%9B`
- Eligibility/Genius 实战：`https://support.worldquantbrain.com/hc/en-us/community/posts/39922788056343`
- 新顾问入门：`https://support.worldquantbrain.com/hc/en-us/community/posts/27928616328855`
- 近期 VF 实战：`https://support.worldquantbrain.com/hc/en-us/community/posts/41563959159319`
- Osmosis 机制：`https://support.worldquantbrain.com/hc/en-us/community/posts/40604106677271`

### 本地代码与证据

- `worldquant-backtest.service`
- `autonomous_research_loop.py`
- `backtest_from_store.py`
- `stable_single_backtest.py`
- `alpha_store.py`
- `slot_scheduler.py`
- `pipeline_watchdog.py`
- `skills/brain-simAlphasinBatch-and-track/scripts/ace_lib.py`
- `reports/audits/DATA_FIELDS_AND_ROOT_CLEANUP_AUDIT_20260716.md`
- `ai_memory/PIPELINE_CHANGE_LOG_20260714_HOURLY_METRICS_THROUGHPUT_P0.md`

