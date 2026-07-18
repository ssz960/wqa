# WQ AI 工作流论坛与 Skill 框架审阅稿

**日期**：2026-07-16（Asia/Shanghai）  
**用途**：交给 GPT 做第二轮审阅，并据此确定下一步实现方案。  
**范围**：Chrome 中当前打开的 4 个 WorldQuant BRAIN 页面、主帖及回复、本地 `D:\aibrain` 已迁移的 Claude skills、当前 `D:\Codex\worldquant` 研究/回测框架。

## 0. 结论先行

论坛中最有价值的共识不是“让 AI 全自动找 Alpha”，而是把工作拆成三种职责：

1. **AI**：提出经济学假设、做字段语义检索、生成裸信号/模板变体、解释回测结果。
2. **代码**：做确定性工作，包括字段和数据类型约束、语法校验、去重、相关性剪枝、批量回测、结果落库、断点恢复和证据汇总。
3. **人**：决定研究目标、识别异常和伪阳性、判断经济学解释是否成立、决定是否进入人工提交审阅。

这与当前项目的主链高度兼容：

`pull_exports -> local self-correlation -> research pack -> GPT -> strict external_candidates CSV -> server queue/backtest -> pull results -> research pack/review`

最值得落地的不是另起一个“全自动 Alpha 旁路”，而是把 `D:\aibrain` 的能力接入现有 research pack 和 external CSV 契约，形成一个受控的“研究候选生成层”。

当前建议：

- 先落地 **字段语义压缩/检索 + 裸信号生成 + 结果诊断** 三个 AI 环节。
- 保留当前 `external_candidates` 12 列契约、现有队列、现有本地 self-corr 和人工审阅边界。
- 暂不把论坛中的 8x10、自动提交、全自动循环作为默认生产行为；论坛经验不是平台能力证明。
- `consultant_multi` 只能在 capability profile、预算 ledger、父子 reconciliation 均有效时使用；`legacy_single` 的 3-slot 回退必须一直可用。
- 所有结果进入“研究/回测/筛选/报告”链，**不得自动提交 Alpha**。

## 1. 本次浏览的论坛页面

### 1.1 主帖

- [【有奖SKILL征文】分享你的AI工作流、提示词、还有它的SOUL](https://support.worldquantbrain.com/hc/zh-cn/community/posts/39225718749591--%E6%9C%89%E5%A5%96SKILL%E5%BE%81%E6%96%87-%E5%88%86%E4%BA%AB%E4%BD%A0%E7%9A%84AI%E5%B7%A5%E4%BD%9C%E6%B5%81-%E6%8F%90%E7%A4%BA%E8%AF%8D-%E8%BF%98%E6%9C%89%E5%AE%83%E7%9A%84SOUL)
- 主帖为置顶征集帖，页面显示 52 票、28 条评论。
- 楼主明确要求：分享 Skill 或代码应放在评论中；不鼓励重复发新帖；拒绝只有感谢的非深度回复。
- 楼主置顶评论列出的优秀内容包括：
  - `MCP 提示词优化 alpha` 全流程提示词。
  - `Community Leader - 因子构造` 零预算持续生成 Alpha 模板。
  - Gemini CLI 因子优化提示词。
  - “跑了几百次回测仍找不到优质信号”经验帖。

### 1.2 三个搜索页

- [`skill` 搜索结果](https://support.worldquantbrain.com/hc/zh-cn/search?utf8=%E2%9C%93&query=skill)：出现 Regular -> Python、批量回测、FieldPer/OpCount 围栏、裸信号 Skill、Gemini 工作流等。
- [`mcp` 搜索结果](https://support.worldquantbrain.com/hc/zh-cn/search?utf8=%E2%9C%93&query=mcp)：出现 MCP 误区、MCP 自动找 Alpha、Trae/Claude/VSCode 配置、本地 LLM、论文到 Alpha 等。
- [`ai` 搜索结果](https://support.worldquantbrain.com/hc/zh-cn/search?query=ai&utf8=%E2%9C%93)：结果 766 条；高相关条目包括 Harness engineering、AI 打工人、AI 教我写模板、自动找 Alpha、AI 排障手册。

搜索页的票数和评论数只用于发现高价值帖子；正文中的平台能力、收益和成功率仍需按“论坛经验”处理，不能当作官方 entitlement 或当前账户能力。

## 2. 主帖及回复总结

### 2.1 主帖建立的是“Skill 注册表”

主帖本身不是一个 Alpha 方法，而是一个社区索引入口。它把 AI 研究经验集中到评论中，并由楼主定期挑选优秀内容。其价值有三点：

- **减少重复搜索**：提示词、Skill、代码和完整工作流集中在一个主题下。
- **暴露实践分歧**：代码对话、MCP、Claude、Gemini CLI、Trae、AI 打工人等路线并存。
- **形成社区优先级信号**：被楼主列为优秀分享、票数高、回复内容具体的帖子，优先级高于普通工具介绍。

### 2.2 高价值回复的内容分层

#### A. 数据集和字段层

`XC96000` 的长回复是主帖最重要的技术内容之一，给出了一条数据驱动的生成链：

`数据集分析 -> 字段精选 -> 主题确立 -> 操作符选择 -> 表达式构建`

具体方法：

- 先读取数据集元数据，不把 895 个字段一次性直接交给模型。
- 让模型输出高密度关键词簇，作为语义检索查询。
- 用向量库双路径检索：核心词路径 + 全量词簇路径，先粗筛约 120 个字段。
- 再让模型精筛为约 50-80 个字段。
- 把字段按 2-4 个交易主题分桶，每个主题限定相关字段和算子类别。
- 主题级别分别生成表达式，减少长上下文导致的主题漂移。
- 后续再做纠错、模拟和优化。

这个流程的核心不是“向量库”本身，而是**先压缩搜索空间，再让模型做局部决策**。

`ZH87224` 的数据集压缩 Prompt 进一步强调：对字段命名模式抽象为正则或模板，例如把同一数据集内的指标、频率、范围、统计量抽象成占位符。它适合把“数千字段”变成“字段族 + 代表字段 + 可替换位置”。

#### B. 表达式与类型约束层

`HA11071` 分享的 Skill 关注 Alpha DSL 的表达式树、基础字段、运算符和参数约束。

`ZZ44620` 的回复更直接：

- `MATRIX` 可直接进入普通算子。
- `VECTOR` 必须先经过 `vec_*` 降维。
- `GROUP` 只能作为 `group_*` 的分组参数。
- 仅靠 Prompt 不能稳定避免类型错误，必须加本地语法/类型拦截。

这和当前项目已有的 expression verifier、field whitelist、operator signature、lane contract 是同一方向。应把类型信息作为结构化元数据和硬校验，不要只写在自然语言 Prompt 中。

#### C. Prompt 和 Skill 工程层

`WX87649` 给出的 Prompt 分层是：

1. 角色锚定。
2. 核心模板引擎。
3. 数据与假设动态注入。
4. 输出格式约束。
5. Few-shot 示例。

`PZ56655` 的 Alpha Factory v3 则把流程概括成：

`硬性指标筛选 -> 语义逻辑构建 -> 信号效能审计 -> 深度诊断优化`

`LL49894` 的 Gemini CLI 工作流强调多阶段检查、强制清单、robust check、regular/powerpool 模式和阻断机制。

这些内容共同说明：Skill 的价值不只是“多一份 Prompt”，而是把每轮输入、输出、停止条件、验证条件和失败处理固定下来。

#### D. 回测结果分析和优化层

`YL27037` 分享了 `brain-alpha-data-analysis` 思路：

- 大表先由脚本转成 LLM 适合读取的 JSON。
- 数据量大时先做统计分析，避免模型只看到表头。
- 输出结构化诊断报告，再由模型解释。

`SP75169` 的优化 Skill 约束很接近当前项目需要的候选循环：

- baseline 核心字段/数据集不变。
- 每轮固定 8 个候选。
- 目标包括 Sharpe、Fitness、Turnover、检查结果和生产相关性。
- 限制迭代轮数，防止模型无限堆叠。

`ZH87224` 的 FieldPer/OpCount 经验指出，AI 很容易把 2 个字段、4 个算子优化成 8 个字段、40 个算子；优化后必须加复杂度围栏和周期上限。

#### E. Harness / 人机协同层

主帖回复和高票帖子反复出现一个判断：AI 适合发散，代码适合收敛，人负责研究判断。

主帖中 `PZ56655`、`LL49894`、`SP75169` 等回复都在尝试把这套思想做成 Skill；其中 `GY62435` 的“每日四槽”工作流体现了 quota、sentinel 和 family abandonment，但它的槽位假设不能直接覆盖当前项目的 P0 生产约束。

## 3. 高票精华帖总结

### 3.1 Harness engineering 下的 AI Quant

- [帖子](https://support.worldquantbrain.com/hc/zh-cn/community/posts/39304762113815-Harness-engineering%E4%B8%8B%E7%9A%84AI-Quant)
- 页面显示 169 票、53 条评论，是本次页面中最重要的高票帖子。

作者的完整流程：

1. 按目标塔和数据集选择字段，让 AI 生成 50-100 个简单、纯粹、有经济学含义的裸信号。
2. 代码做语法检查和 VECTOR 字段降维，不让 AI 参与这些确定性清理。
3. 统一回测后按 Sharpe/Fitness/Margin 多通道排序和相关性剪枝。
4. 通过传统 1/2/3 阶增强；候选不足时谨慎补 robust，强调 robust 更偏检验而不是无限增强。
5. 做本地 self-corr、平台 check、组合 compare、年度表现、PnL/Turnover 形态检查。
6. 对 rank/sign 变体和 robust 做自动化测试。
7. 让 AI 解释经济学含义，但由人判断是否合理和是否进入提交审阅。

关键经验：

- 裸信号应简单，创新放在入口，收敛放在中后段。
- 输入给模型的字段名和描述不宜无限扩张。
- 多通道剪枝比单指标排序更能保留多样性。
- `instant` 与 `thinking` 的选择是作者经验，不是普适平台规则，需要本地 A/B 验证。
- 全 AI 流程的主要风险是偏航后继续高速执行，而不是立即停机。

回复中最有价值的补充不是点赞，而是：

- `XY20037` 明确提炼出“裸信号 -> 多维剪枝 -> 1/2/3 阶 -> robust -> AI 解释”的闭环。
- `CH62432` 指出真正的瓶颈仍是人的研究能力和假设质量。
- `XX27743` 说明模板法效率较高，但对低相关、完美过线和是否加入 group/trade 仍有人工取舍。
- 多个回复询问老 1/2/3 阶和 robust 的定义，说明这套流程对新用户的可复现性仍不足。

### 3.2 `skill` 搜索页的高信号主题

搜索结果中票数较高、且与当前工程直接相关的帖子包括：

| 帖子 | 页面信号 | 可复用内容 | 主要风险 |
|---|---:|---|---|
| `[Python Alpha] Regular to Python Alpha` | 93 票 / 23 评论 | 将 Regular/Fast Expression 语义化转成可审计 Python core | 算子语义、NaN、group、历史窗口容易转错 |
| `基于 skill 的 Python Alpha 迭代工作流` | 18 票 / 12 评论 | batch simulator + Python Alpha 迭代追踪 | 并发和结果归档不能绕过主队列 |
| `FieldPer 拯救计划：Skill 围栏` | 3 票，内容具体 | 限制字段数、算子数、迭代次数 | 过度限制可能压掉真实信号 |
| `OpCount 拯救计划：因子化简` | 内容具体 | 保持表现的表达式简化 | “表现不变”必须由回测证据证明 |
| `把裸信号生成流程做成 Skill 之后，最重要的不是更快，而是更稳` | 16 票 | 将裸信号流程固化为可检查、可迁移的 Skill | Skill 不能替代数据和平台验证 |
| `8x10 并发代码` | 5 票 | 高吞吐批量回测实现经验 | 论坛代码不等于当前账户 entitlement 或生产批准 |

### 3.3 `mcp` 搜索页的高信号主题

| 帖子 | 页面信号 | 可复用内容 | 主要风险 |
|---|---:|---|---|
| `MCP 使用中的最大误区` | 86 票 / 20 评论 | MCP 只是工具层；重试、状态、上下文和工作流约束决定效果 | 需要把经验转成可观测的失败分类 |
| `借助 MCP，让 AI 全自动找 alpha` | 70 票 / 11 评论 | 把字段解释、表达式生成、回测、调试连起来 | “全自动”必须拆成可回滚的阶段，禁止假成功 |
| `Trae 配置使用 MCP` | 66 票 / 49 评论 | 客户端配置和工具接入经验 | 工具接入不代表研究质量提升 |
| `claude code 添加 MCP` | 64 票 / 3 评论 | 多模型路由与 MCP 配置 | 凭据和 API 中转存在泄露/稳定性风险 |
| `MCP 本地 LLM 配置` | 13 票 / 4 评论 | 本地模型用于降低成本和调试工作流 | 本地模型能力、上下文长度和调用稳定性需实测 |
| `MCP 结合论文实践` | 20 票 / 7 评论 | 从论文方程、字段和表达式提取研究候选 | 论文关系不等于可交易信号，需回测验证 |

### 3.4 `ai` 搜索页的高信号主题

| 帖子 | 页面信号 | 可复用内容 |
|---|---:|---|
| `Harness engineering 下的 AI Quant` | 169 票 / 53 评论 | 人机协同、裸信号、剪枝、增强、稳健性和人工终审 |
| `AI 工具：新版 AI 打工人配置指南` | 105 票 / 31 评论 | 工具安装和集成入口 |
| `AI 教我写模板` | 15 票 / 9 评论 | 用模板和数据集让 AI 学字段和结构 |
| `借助 MCP，让 AI 全自动找 alpha` | 70 票 / 11 评论 | MCP 串联字段、表达式、模拟和调试 |
| `MCP WorkFlow：AI 排障手册` | 85 票 / 2 评论 | 把错误记录为可复用的诊断手册 |
| `AI 融入工作流` | 28 票 | 说明社区仍在迭代阶段，不能把个别成功当稳定规律 |

## 4. D:\aibrain 已迁移 skills 的能力盘点

### 4.1 当前存在的关键能力

`D:\aibrain\.claude\skills` 当前包含：

- 数据发现：`brain-dataset-exploration-general`、`brain-datafield-exploration-general`、`brain-data-feature-engineering`。
- 候选生成：`brain-makeSomeGem`、`brain-feature-implementation`、`brain-enhance-template`、`brain-inspectRawTemplate-create-Setting`。
- 回测与追踪：`brain-simAlphasinBatch-and-track`、`brain-deepExplore`。
- 诊断与复核：`brain-improve-alpha-performance`、`brain-alpha-judge`、`brain-explain-alphas`、`brain-calculate-alpha-selfcorrQuick`、`brain-how-to-pass-AlphaTest`、`wq-brain-alpha-optimization-v1`。
- 研究辅助：`brain-nextMove-analysis`、`brain-forum-browse`、`planning-with-files`、`alpha-expression-verifier`。

根目录还有：

- `brain-consultant.md`：BRAIN API、Alpha、金字塔、设置和操作符的领域角色说明。
- `.mcp.json`：配置 `brain-mcp`，由 `platform_functions.py` 提供平台和论坛相关能力。
- `untracked\APP\brain-orchestrator`、`brain-alpha-judge`、`simulator` 等实验/应用目录。

当前 `.claude\skills` 中没有发现论坛帖子提到的 `brain-regular-to-python-alpha` 同名 Skill；Regular 转 Python 可以作为后续补充，但不能在本报告中假设它已可用。

### 4.2 重要边界和冲突

1. `brain-deepExplore` 的描述包含“直到 4 个 submit-ready Alpha”的停止条件；这与本项目“只研究/回测/筛选/审阅、不得自动提交”的硬要求冲突。迁移时必须把终点改成 `manual_review_ready`。
2. `brain-simAlphasinBatch-and-track` 支持 detached、polling、CSV resume，这与当前队列很匹配，但不能直接把它当作第二条生产回测通道。
3. `brain-feature-implementation` 明确只做本地 CSV 和表达式生成，不调用 BRAIN MCP、不提交、不跑平台模拟；适合作为候选构建前置层。
4. `brain-alpha-judge` 是静态本地论坛 corpus + 平台 hard checks 的审阅层，规则上也要求显式确认后才能提交；可直接对接现有人工审阅边界。
5. `brain-forum-browse` 的默认规则要求浏览后进行论坛写入；本次用户请求只是查看和总结，没有进行评论、点赞或发帖，避免了不必要的外部副作用。

## 5. 与当前 worldquant 框架的匹配分析

### 5.1 当前主链能承接什么

当前主链已经具备以下承接点：

- `research_pack_builder.py` 生成 `research_master`、`research_delta`、报告和 GPT 输入。
- `local_self_corr.py` / `query_csv_self_correlation.py` 负责本地 PnL self-corr 和官方 OS 缓存相关证据。
- `EXTERNAL_CANDIDATE_COLUMNS` 固定为 12 列：

```text
expression, decay, source, priority_score, run_intent, family,
notes, universe, delay, neutralization, truncation, nan_handling
```

- `validate_external_candidates_schema.py` 在进入服务器前验证严格列契约。
- `external_csv_sync_helper.py`、BAT 和 PowerShell 脚本负责同步、导入、拉回和归档。
- `alpha_store.py` 保留 expression、family、template signature、parent/source 等研究元数据，并对队列、重复、优先级和 lane contract 做控制。
- `consultant_multi.py` 已有 capability profile、父子批次、预算 ledger、idempotency、import-once 和 recovery 状态；但 multi 只能在能力快照和预算语义已确认时启用。
- `stable_single_backtest.py` 和 `slot_scheduler.py` 保留 legacy 3-slot 回退。
- research pack / WeCom 层可输出研究状态，但不应成为新的回测入口。

### 5.2 最适合的集成位置

建议把 `D:\aibrain` 接在 **research pack 输出和 external CSV 生成之间**：

```text
research_master/research_delta
        |
        v
AI field/theme/candidate worker
        |
local type + syntax + complexity + duplicate gates
        |
external_candidates 12-column CSV
        |
existing sync/import/queue/backtest chain
        |
results pull -> research pack -> self-corr / judge / human review
```

不要让 AI worker：

- 直接写 `alpha_store.db`。
- 直接改变队列状态或 priority。
- 直接创建平台 Alpha 或发送提交请求。
- 绕过 `validate_external_candidates_schema.py`。
- 维护一套与主队列平行的“成功”状态。

### 5.3 论坛方法与现有模块映射

| 论坛方法 | D:\aibrain Skill | 现有框架承接点 | 建议 |
|---|---|---|---|
| 数据集元数据分析 | `brain-dataset-exploration-general` | research pack 的 dataset/field 资料 | 先落地 |
| 六类字段探测 | `brain-datafield-exploration-general` | 回测候选与结果报告 | 先落地，结果入证据 |
| 字段语义压缩/向量检索 | `brain-data-feature-engineering` | research pack 增加 field clusters/theme map | 先做离线原型 |
| GEM / 裸信号生成 | `brain-makeSomeGem`、`brain-feature-implementation` | external CSV 候选层 | 先小批次 |
| 模板增强 | `brain-enhance-template` | `run_intent=NEAR_REPAIR` 或 `MATERIAL_EXPLORE` | 受控启用 |
| 设置解析 | `brain-inspectRawTemplate-create-Setting` | 12 列 settings + schema validation | 先复用 |
| 批量回测 | `brain-simAlphasinBatch-and-track` | 现有 queue / server backtest | 只复用主链 |
| Alpha 结果解释 | `brain-explain-alphas` | research report / GPT review | 先落地 |
| self-corr/PPAC | `brain-calculate-alpha-selfcorrQuick` | local self-corr cache | 先落地 |
| 提交前审阅 | `brain-alpha-judge` | green/manual review gate | 强制人工确认 |
| 复杂度围栏 | `wq-brain-alpha-optimization-v1`、FieldPer/OpCount 经验 | `alpha_store` expression metadata | 先做硬拒绝 |
| Python 转写 | 论坛 Regular-to-Python 帖子 | 当前无同名已迁移 Skill | 后续单独评估 |

## 6. 可以运用哪些方式做 Alpha

以下方式按“适合当前框架”的优先级排序。

### 方式 A：数据集主题驱动的裸信号发现

流程：

1. 从 research pack 选定一个 region/delay/universe/dataset。
2. 读取字段名、描述、类型、覆盖度和更新频率。
3. 用关键词簇和字段族压缩搜索空间。
4. 让 AI 输出简单、单主题、有经济学含义的裸信号。
5. 本地做类型、语法、字段存在性、重复和复杂度检查。
6. 以小批量 external CSV 进入现有回测链。

适用：发现新数据集、新主题和低复杂度 ATOM 候选。  
主要优势：创新性高，容易解释。  
主要风险：裸信号 Sharpe 低，需要后续增强；不能用单次结果证明主题有效。

### 方式 B：字段族/模板的受控组合

流程：

- 将数千字段压缩为字段族、代表字段和替换槽位。
- 先固定 2-4 个经济逻辑模板，再在字段族内组合。
- 每个模板设置字段数、算子数、迭代次数和 family quota。
- 结果用 `template_signature`、`source_key`、`cluster_key` 记录，避免重复扩张。

适用：已有少量有效模板，需要扩大覆盖面。  
主要优势：吞吐高、可复现。  
主要风险：模板相关性和表达式重复，必须使用多通道 corr pruning。

### 方式 C：失败 Alpha 的诊断式修复

流程：

1. 从 research pack 取 IS 通过但 RA/风险检查失败的候选。
2. 将失败原因分成 turnover、sub-universe、weight、corr、fitness、类型/语法等。
3. 冻结原始字段和核心逻辑，只针对一个失败原因生成 8 个变体。
4. 每轮做本地校验、批量回测、指标比较、self/prod corr 复核。
5. 3-5 轮无进展则停止并转入其他 family。

适用：已有信号但不合格的 near/pass 候选。  
主要优势：比从零生成节省额度。  
主要风险：AI 无限堆叠防御性算子，必须设 FieldPer、OpCount 和 cycle limit。

### 方式 D：信号解释和反向审查

对每个候选要求 AI 同时输出：

- 字段的经济学含义。
- 因子值高/低分别代表什么。
- 多空方向的合理性和不合理性。
- 可能的数据泄露、更新频率、覆盖度和行业偏置。

这一步不生成更多候选，而是帮助人工判断“高分是否有合理解释”。建议把它放在回测结果之后，作为 report 字段，不写入 research-only 之外的外部 CSV 主字段。

### 方式 E：独立 Python 镜像审计

论坛的 Regular -> Python Skill 适合用于：

- 检查复杂表达式语义。
- 审计 NaN、group、历史窗口和 vector 降维。
- 让模型不能只凭字符串替换解释 Alpha。

当前 `D:\aibrain\.claude\skills` 未发现该 Skill 的迁移版本，因此应先做一个只读、单 Alpha、离线验证的实验，不要直接接入生产队列。

## 7. 建议的下一步方案

### Phase 0：先确定 GPT 审阅口径

GPT 需要先回答：

- 是否采用“裸信号发现 + 模板受控组合 + 失败诊断修复”的三通道架构。
- 是否把字段语义检索结果作为持久化研究资产。
- 是否把 Alpha 复杂度上限作为硬门槛，还是只作为排序分。
- 是否先只做 Regular/MATRIX，暂不扩大 VECTOR/GROUP 复杂度。
- 是否允许将 local Python mirror 作为审计工具，而不是生成工具。

### Phase 1：离线 field intelligence 原型

不触碰服务器和队列，只生成：

- `dataset_profile.json`
- `field_family_map.json`
- `theme_candidates.json`
- `operator_compatibility.json`
- `field_search_audit.md`

输入来自已有 research pack 或本地字段快照。验证指标：字段覆盖、族内去重、主题可解释性、VECTOR/GROUP 分类准确性。

### Phase 2：候选生成器接入 external CSV 前

新增一个本地候选适配层，职责只有：

- 读取 `research_delta` 和 field intelligence artifacts。
- 调用现有 `D:\aibrain` skills 生成表达式。
- 调用 expression/type/operator/field gates。
- 生成严格 12 列 `external_candidates`。
- 为每行写入 `source`、`family`、`run_intent`、`notes` 和可追溯的 parent/source key。

候选生成数量建议从 8-32 行开始，不直接上 500 或 8x10。

### Phase 3：接入现有回测和研究包

- 只调用现有 `import_external_csv_to_server.bat` 或主链等价入口。
- 回测状态以服务器/队列结果为准，不以 AI 输出为准。
- 拉回结果后更新 research pack、self-corr cache、family/cluster ledger。
- 对每轮候选生成一个可审计 batch manifest。
- 使用 `brain-alpha-judge` 产生 `READY/REVIEW/BLOCK` 研究结论，但 `READY` 仍只代表人工审阅候选，不代表提交。

### Phase 4：受控优化循环

优先做单一失败原因修复：

- 每轮 8 个候选。
- 冻结 baseline dataset/core fields。
- 每轮最多改变 1-2 类变量。
- 3-5 轮无进步自动停止。
- 任何异常状态、未知预算、父子 ledger 不一致时 fail closed 到 legacy 3-slot。

### Phase 5：再评估 multi throughput

只有当 Phase 3 的候选质量和证据链稳定后，才评估 Consultant Multi：

- capability profile 必须有来源、有效期、日界线、daily cap、count basis。
- parent/child ledger 必须完整，import-once 和 idempotency 必须可验证。
- 监控 `worldquant-backtest=active`、`--single-slots 3`、live worker `--parallel-slots 3`、slot refill 和 queue/results timestamp。
- 8x10 只能作为已验证能力下的受控实验，不得因论坛经验自动放大。

## 8. 需要特别防止的失败模式

| 风险 | 表现 | 防护 |
|---|---|---|
| 全自动偏航 | 模型在错误主题上持续生成 | 每阶段有明确输入/输出/停止条件；人保留研究目标 |
| 字段爆炸 | 数千字段直接塞入上下文 | 字段族、关键词簇、双路径检索、分主题处理 |
| 算子/类型错误 | VECTOR 直接进普通算子，GROUP 被当数值 | 本地类型图和签名校验，Prompt 只做辅助 |
| 复杂度爆炸 | 2Field/4Op 变成 8Field/40Op | FieldPer、OpCount、operatorCount、cycle limit |
| 结果幻觉 | AI 宣称成功但无平台结果 | 以 queue/backtest/research pack 为唯一结果源 |
| 高相关污染 | 同一模板/字段族大量重复 | expression hash、template signature、source/cluster corr pruning |
| 失败循环 | 每轮只改参数或不停加 trade_when | 按失败原因分流，3-5 轮无进展停止 |
| 多槽越权 | 论坛 8x10 经验被当成账户能力 | capability profile + budget ledger + legacy 3-slot fallback |
| 自动提交越界 | 研究候选直接进入提交 | external CSV 只进入回测；提交必须人工明确授权 |
| 凭据泄露 | Prompt、仓库或日志包含账号密码 | 不向论坛/模型上传凭据，日志脱敏，使用本地配置 |

## 9. 给 GPT 的审阅问题

请 GPT 按以下顺序审阅本文件：

1. **架构判断**：三职责分工是否比全自动 Agent 更适合当前 P0 约束？哪里需要补充硬门槛？
2. **优先级判断**：Phase 1-3 的顺序是否合理？field intelligence、裸信号和失败修复哪个先做？
3. **数据契约**：12 列 external CSV 是否足以承载 source/family/parent/notes 的追踪？哪些信息必须进入独立 manifest 或 ledger？
4. **验证设计**：怎样设计离线 A/B，证明字段语义检索、Prompt 分层和复杂度围栏真的提高了结果质量，而不是只提高候选数量？
5. **指标设计**：除 Sharpe/Fitness/Turnover 外，如何量化候选质量、主题多样性、字段族覆盖、corr 污染、解释一致性和人工审阅通过率？
6. **Multi 边界**：在 capability profile 不完整时，是否应该完全停用 multi，只保留 legacy 3-slot？预算和失败计数还缺什么证据？
7. **Python mirror**：Regular -> Python 是否值得作为审计层？优先验证哪些 operator 语义？
8. **最小实现**：如果只能实现一个小功能，建议先做 field family/theme artifact、candidate adapter、还是 result diagnosis adapter？

## 10. 本次事实边界

- 本次只读取了用户当前 Chrome 中的 WQ 页面和本地文件。
- 没有在论坛发帖、评论或点赞。
- 没有运行 Alpha 回测、导入队列、服务器部署或 Alpha 提交。
- 论坛票数、评论数、作者经验和成功率均视为社区经验，不视为官方平台能力证明。
- 本报告引用的当前框架事实以 `agents.md`、`ai_memory` 当前要求、最新变更记录和本地代码结构为准。
- `D:\aibrain` 的 `.claude\skills` 是已迁移到本地的能力集合，但不同 Skill 的脚本、凭据、平台接口和生产边界仍需逐项验证。

