# Material-To-Research Queue Workflow

Goal: turn useful text, PDFs, and chat-shared ideas into research notes, candidate alpha expressions, backtests, and queue optimization.

## 1. Collection Inbox

Use one local inbox as the stable handoff point:

```text
research_memory/inbox/
```

Recommended subfolders:

```text
research_memory/inbox/pdf/      PDF papers, books, screenshots exported as PDF
research_memory/inbox/text/     copied text, article snippets, WeChat exports
research_memory/inbox/reviewed/ material already processed
```

Keep raw material on disk. Do not paste whole books or long PDFs into chat. The research loop should consume concise notes, formulas, and hypotheses.

## 2. Ingest PDFs And Text

For a PDF with a text layer:

```powershell
.\.venv\Scripts\python.exe doc_learning.py ingest "research_memory\inbox\pdf\paper.pdf" --render-scan-preview
```

For plain text or markdown:

```powershell
.\.venv\Scripts\python.exe doc_learning.py ingest "research_memory\inbox\text\wechat_note.md"
```

This updates:

```text
research_memory/doc_index.json
research_memory/learning_notes/*.md
research_memory/doc_extracts/*.txt
research_memory/page_contact_sheets/*.jpg
```

For scanned PDFs, process them chapter by chapter. The current learner creates preview sheets, then you add short manual/OCR notes into `research_memory/learning_notes/*.md`.

## 3. Convert Material Into Research Notes

Each note should produce operational research memory, not a summary for its own sake:

```text
Hypothesis: why this signal may work
Fields: close, volume, returns, fundamentals, analyst, etc.
Operators: rank, ts_rank, ts_delta, ts_mean, group_neutralize, etc.
Template forms: expression skeletons worth testing
Mutation recipes: decay/window/neutralization variants
Failure repairs: what to try if Sharpe/Fitness/Turnover fails
```

If the material contains direct Fast Expression-like formulas, put them in code spans or code blocks so the importer can detect them:

```text
`rank(ts_delta(close, 5))`
`group_rank(ts_mean(volume, 20), subindustry)`
```

## 4. Feed Notes To The Researcher

Create or update `factor_sources.json`:

```json
{
  "sources": [
    {
      "name": "wechat_notes",
      "path": "research_memory/inbox/text/wechat_note.md",
      "tier": "A"
    },
    {
      "name": "doc_learning_notes",
      "path": "research_memory/learning_notes/example.md",
      "tier": "A"
    }
  ]
}
```

Preview extraction:

```powershell
.\.venv\Scripts\python.exe web_factor_researcher.py --sources-file factor_sources.json --dry-run
```

Import candidates into `alpha_store.db`:

```powershell
.\.venv\Scripts\python.exe web_factor_researcher.py --sources-file factor_sources.json --limit 50 --min-score 70
```

Imported candidates enter the store with sources like:

```text
web_research:wechat_notes
web_research:doc_learning_notes
```

Harder or higher-quality ideas receive higher priority and can move ahead of generic generated candidates.

## 5. Optimize The Existing Queue

After new material-driven candidates enter the store:

```powershell
.\.venv\Scripts\python.exe alpha_research.py optimize --limit 120
.\.venv\Scripts\python.exe alpha_research.py rebalance-queue
.\.venv\Scripts\python.exe alpha_research.py list-queue --limit 40
```

Then run backtests with the profile you want:

```powershell
.\.venv\Scripts\python.exe backtest_from_store.py --profile safe
```

or, when the service is already stable:

```powershell
.\.venv\Scripts\python.exe backtest_from_store.py --profile fast
```

## 6. Close The Feedback Loop

After backtests:

```powershell
.\.venv\Scripts\python.exe doc_learning.py update-outcomes
.\.venv\Scripts\python.exe alpha_research.py report --output reports\alpha_research_report.md --limit 200
.\.venv\Scripts\python.exe alpha_dashboard.py
```

Read:

```text
research_memory/doc_outcomes.md
reports/alpha_research_report.md
alpha_dashboard.html
alpha_dashboard_summary.csv
```

Promote material that produces pass/optimize results. Retire or rewrite material that repeatedly produces fail results.

## 7. WeChat / Enterprise WeChat Bridge

Use WeChat as a notification and collection channel, not as the database.

Recommended minimal setup:

```text
Human shares material in WeChat
-> save/export text or file into research_memory/inbox/
-> run doc_learning.py or web_factor_researcher.py
-> candidates enter alpha_store.db
-> backtest/optimize/rebalance
-> send pass/optimize summary back to WeChat
```

For automatic notifications, use the existing notification layer documented in `NOTIFICATION_WORKFLOW.md`. Keep secrets in `.env`, not in chat logs or markdown files.

For direct Enterprise WeChat ingestion, deploy `wecom_material_receiver.py` on the server and configure the self-built app callback URL to:

```text
http://43.108.38.207:8787/wecom/callback
```

The receiver accepts encrypted text messages, saves them into `research_memory/inbox/text/`, updates `factor_sources.json`, runs the researcher, optimizes/rebalances the queue, and restarts `worldquant-backtest`.

## 8. Push Material To Server And Start Running

After saving WeChat text or PDFs into `research_memory/inbox/`, run:

```powershell
.\sync_material_sources_to_server.bat
```

or:

```powershell
.\push_material_to_server.ps1 -Server admin@43.108.38.207
```

This does the full handoff:

```text
upload research_memory/inbox/
upload factor_sources.json
copy researcher scripts to /root/worldquant
ingest PDFs/text on the server
run web_factor_researcher.py
run alpha_research.py optimize
run alpha_research.py rebalance-queue
restart worldquant-backtest
```

If you only want to import and rebalance without restarting the service:

```powershell
.\push_material_to_server.ps1 -NoRestart
```

## 9. Suggested Daily Routine

Morning:

```powershell
.\pull_server_snapshot.bat
.\.venv\Scripts\python.exe doc_learning.py update-outcomes
```

When you see useful material:

```powershell
.\.venv\Scripts\python.exe doc_learning.py ingest "path\to\material.pdf" --render-scan-preview
.\.venv\Scripts\python.exe web_factor_researcher.py --sources-file factor_sources.json --limit 50
```

Before/after backtesting:

```powershell
.\.venv\Scripts\python.exe alpha_research.py optimize --limit 120
.\.venv\Scripts\python.exe alpha_research.py rebalance-queue
.\.venv\Scripts\python.exe backtest_from_store.py --profile fast
```

Evening review:

```powershell
.\.venv\Scripts\python.exe alpha_research.py report --output reports\alpha_research_report.md --limit 200
.\.venv\Scripts\python.exe alpha_dashboard.py
```
