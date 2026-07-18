# WorldQuant Forum Template Collection

Date: 2026-07-16
Source: Chrome session, WorldQuant BRAIN-CN template search and linked posts
Status: REVIEW_ONLY

This file contains external forum material. It is a research input, not a claim that
the expressions are currently valid, available, profitable, or approved for
submission. Validate field type, operator permissions, syntax, coverage, checks,
correlation, and market settings before any local backtest.

## Scope

- Read the visible first page of the forum search for `模板` (778 community results were shown).
- Read the pinned AI workflow post and its 28 comments.
- Read the visible high-signal template posts linked from the search page.
- No forum write, Alpha simulation, queue import, deployment, or Alpha submission was performed.

## Expression Templates

### 1. Quality / Stability Ratio

Source: [AI教我写模板](https://support.worldquantbrain.com/hc/zh-cn/community/posts/38989280956951-AI%E6%95%99%E6%88%91%E5%86%99%E6%A8%A1%E6%9D%BF)

Economic idea: a quality field divided by its time-series dispersion.

```text
rank({datafield}) / ts_std_dev({datafield}, {window})
```

Roles:

- `datafield`: quality, profitability, or stability field
- `window`: positive lookback, original example used 504 and discussed 1024/2048

Review notes: the post later adds valuation and group conditions. Check the actual
operator spelling (`ts_std_dev` versus the current platform catalog) before use.

### 2. Conditioned Short-Squeeze Risk

Source: [AI教我写模板](https://support.worldquantbrain.com/hc/zh-cn/community/posts/38989280956951-AI%E6%95%99%E6%88%91%E5%86%99%E6%A8%A1%E6%9D%BF)

```text
if_else(
    volume > ts_mean(volume, {window}) * {threshold},
    ts_decay_linear(
        group_neutralize(
            rank(vec_avg({field})),
            {group}
        ),
        {decay}
    ),
    NaN
)
```

Suggested field family from the post: `rsk59_squeeze_risk`,
`rsk59_crowded_score`, or `rsk59_shortinterestpct`.

Review notes: the source example uses `sector`, `volume`, and a VECTOR field.
Confirm the field type and whether `NaN` is accepted in the current expression
context. The source also lists `bucket(rank(cap), ...)` and `industry_group` as
alternative grouping choices.

### 3. Sentiment Minus Monthly Return Quantile

Source: [基于情感数据的IND模板](https://support.worldquantbrain.com/hc/zh-cn/community/posts/36876447664023--Alpha-%E6%A8%A1%E6%9D%BF-%E5%9F%BA%E4%BA%8E%E6%83%85%E6%84%9F%E6%95%B0%E6%8D%AE%E7%9A%84IND%E6%A8%A1%E6%9D%BF)

Original parameterization:

```text
S1 = ts_mean(ts_backfill({sentiment}, 250), 22);
R1 = ts_product(1 + returns, 22);
alpha = ts_quantile(S1 - R1, 5, driver='cauchy');
```

Generalized placeholder form:

```text
S1 = ts_mean(ts_backfill({sentiment}, {backfill_window}), {mean_window});
R1 = ts_product(1 + returns, {return_window});
alpha = ts_quantile(S1 - R1, {quantile_window}, driver='cauchy');
```

Review notes: the post says the template commonly needs two datasets and reports
IND use. Validate unit compatibility before subtracting sentiment and return
series. The source also mentions `gaussian` as an alternative driver.

### 4. Macro Robust Quantile Preprocessing

Source: [基于labs分析macro做出可泛化的模板](https://support.worldquantbrain.com/hc/zh-cn/community/posts/34584423754263--Alpha%E6%A8%A1%E6%9D%BF-%E5%9F%BA%E4%BA%8Elabs%E5%88%86%E6%9E%90macro%E5%81%9A%E5%87%BA%E5%8F%AF%E6%B3%9B%E5%8C%96%E7%9A%84%E6%A8%A1%E6%9D%BF)

The post recommends zero-to-NaN cleanup, backfill, and robust quantile handling:

```text
ts_quantile(ts_backfill(to_nan({datafield}), 60), 5, driver='gaussian')
```

It also gives these macro examples:

```text
ts_quantile(ts_zscore({field}, 22), 22, driver='gaussian')
ts_delta(ts_rank({field}, 66), 5)
rank(ts_std_dev({field}, 120))
group_rank(ts_mean({field}, 22), densify(sector))
```

Review notes: the source example uses `mcr27` and explicitly says macro fields may
be VECTOR. A VECTOR field must be reduced with an authorized vector operator before
scalar operators. The four examples are therefore review examples, not ready-to-run
expressions.

### 5. Analyst Coverage / PV Blend

Source: [虎哥模板分享](https://support.worldquantbrain.com/hc/zh-cn/community/posts/33036230902679-%E8%99%8E%E5%93%A5%E6%A8%A1%E6%9D%BF%E5%88%86%E4%BA%AB)

```text
A = ts_backfill(log({datafield} + 1), 63);
B = log(cap);
C = ts_sum(returns, 63);
signal = vector_neut(A, B * C);
```

The post says `B` and `C` can be replaced by other fundamental or price/volume
fields, and that the data field should represent analyst coverage. `vector_neut`
and all field types require current-catalog verification.

### 6. Standard Group-over-Time Template

Source: [新顾问手搓模板三部曲](https://support.worldquantbrain.com/hc/zh-cn/community/posts/36770332492951-%E6%96%B0%E9%A1%BE%E9%97%AE%E6%89%8B%E6%90%93%E6%A8%A1%E6%9D%BF%E4%B8%89%E9%83%A8%E6%9B%B2)

```text
Group_op(ts_op({datafield}, {day}), {group})
```

The post describes this as a broad standard template for a time-series signal with
cross-sectional grouping. It also gives these construction primitives:

```text
<time_series_op>(<profit_field> / <size_field>, <days>)
<group_op>(<put_greek> - <call_greek>, <grouping_data>)
Rank_op({datafield_1} - {datafield_2})
Zscore_op({datafield_1} / {datafield_2})
ts_delta({datafield_1}, {day})
ts_regression({datafield_1}, {datafield_2}, {day}, rettype=0)
```

Review notes: `Group_op`, `ts_op`, `Rank_op`, and `Zscore_op` are placeholders, not
literal operator names. The post warns that VECTOR/Event fields can fail under
ordinary rank/backfill operators and should be type-detected first.

## Supporting Research Templates

These are workflow or field-family templates rather than direct Alpha expressions.
They are retained because they explain how the forum authors use the expressions.

### Field-Family Compression Prompt

Source: ZH87224 comment in the pinned [AI workflow post](https://support.worldquantbrain.com/hc/zh-cn/community/posts/39225718749591--%E6%9C%89%E5%A5%96SKILL%E5%BE%81%E6%96%87-%E5%88%86%E4%BA%AB%E4%BD%A0%E7%9A%84AI%E5%B7%A5%E4%BD%9C%E6%B5%81-%E6%8F%90%E7%A4%BA%E8%AF%8D-%E8%BF%98%E6%9C%89%E5%AE%83%E7%9A%84SOUL)

```text
{dataset_id}_{indicator}_{frequency}_{scope}_{metric}_{stat}
```

The source asks the model to emit mutually exclusive regular-expression families,
enumerated economic meanings, representative examples, and a `specials` list for
fields that cannot be compressed. This is a field-intelligence asset, not an Alpha
template.

### Template Group Management

Source: [模板群管理——动态优化淘汰低效模板](https://support.worldquantbrain.com/hc/zh-cn/community/posts/37285699644823--Alpha%E6%A8%A1%E6%9D%BF-%E6%A8%A1%E6%9D%BF%E7%BE%A4%E7%AE%A1%E7%90%86-%E5%8A%A8%E6%80%81%E4%BC%98%E5%8C%96%E6%B7%98%E6%B1%B0%E4%BD%8E%E6%95%88%E6%A8%A1%E6%9D%BF)

The author recommends tracking each generated Alpha back to its template, measuring
template-level output and pass rates, and removing persistently low-yield templates.
The post is methodology only; no standalone expression was published.

### Forum Template Evaluation Workflow

Source: [MCP 工作流：论坛模板评估](https://support.worldquantbrain.com/hc/zh-cn/community/posts/34310411227799--MCP-%E5%B7%A5%E4%BD%9C%E6%B5%81-%E8%AE%BA%E5%9D%9B%E6%A8%A1%E6%9D%BF%E8%AF%84%E4%BC%B0)

The workflow is: discover posts, extract expressions, check field/operator availability,
convert placeholders, run at most three syntax/backtest retries, score quality, then
monitor long-term results. Its example expressions include:

```text
ts_rank(close, 10) - 0.5
-ts_corr(close, volume, 20)
```

The forum workflow is retained as review guidance only. The local project must use
the existing external-candidate contract and human review boundary.

## Intake Rules

- Keep every entry `REVIEW_ONLY` until current field/operator validation and local checks pass.
- Treat forum claims, pass rates, and market results as community evidence, not platform guarantees.
- Do not auto-submit Alpha. Any future candidate must enter the existing research/backtest/review chain.
- Preserve the source URL and template placeholders when creating derived variants.
- Record field type, region, universe, delay, neutralization, source dataset, and validation evidence separately.
