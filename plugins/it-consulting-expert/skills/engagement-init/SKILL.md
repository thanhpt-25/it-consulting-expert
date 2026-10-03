---
name: engagement-init
description: >
  Create or resume the engagement workspace that every other skill in this plugin reads and writes.
  Use this skill when the user starts a new bid or project — "new engagement", "start a new RFP",
  "set up the workspace", "新規案件", "案件を始める", "案件フォルダを作成", "engagement setup" — or asks
  where an engagement stands: "engagement status", "案件の状況", "what's next on this bid",
  "where are we on the ABC proposal", "次は何をすればいい". Also trigger for "set the deadline",
  "提出期限を設定", "record the contract baseline", "ベースライン設定", and "set up our rate card",
  "単価表を設定". Run it before rfp-notebook when no workspace exists yet.
---

# Engagement Workspace (案件ワークスペース)

Create the single folder an engagement lives in, record its identity and deadlines, and tell the
user what to do next. Every other skill follows the handoff contract in
`${CLAUDE_PLUGIN_ROOT}/shared/engagement-workspace.md`; this skill is where that folder is born.

## Resume first

Always check before creating:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/sier" status
```

If it finds a workspace (it walks up from the current folder, or reads `$SIER_WORKSPACE`), show the
dashboard and stop — the user is resuming, not starting. If the user names a client you can't find,
look under `./consulting/` (or `$SIER_HOME`) before creating a duplicate.

## Create

Ask only for what you can't infer from the conversation or attached RFP:

- **Client** (顧客名) and **project** (案件名) — required
- **NotebookLM notebook id**, if the RFP is already uploaded — optional; `rfp-notebook` can set it later
- **Proposal submission deadline** and **presentation date**, if known

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/sier" init --client "ABC製造株式会社" --project "CRMクラウド移行" \
  [--notebook <notebook_id>] [--root <parent folder>]
```

Then write the known deadlines into `engagement.json` → `deadlines`
(`proposal_submission`, `presentation`, `go_live`, as `YYYY-MM-DD`). Leave unknown values `null` —
never guess a date.

Where it goes: `$SIER_HOME` if set, else `./consulting/` under the current folder. In Cowork that is
the connected folder, so the files land on the user's computer; in Claude Code it is the project.

## Firm data (once per firm, not per engagement)

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/sier" ratecard show
```

If no rate card exists, offer `sier ratecard init`. It writes **market benchmark midpoints** marked
`benchmark_only`, and `sier cost` will warn on every run until the user replaces them with the firm's
real rates. Say this plainly — a bid priced on benchmarks is not a bid.

## After award: set the baseline

When the contract is signed, record the baseline that change-request measures against:

```json
"baseline": {"effort_mm": 175.8, "cost": 233250000, "schedule_days": 540, "requirements_count": 42}
```

Take `effort_mm` from `03-estimate.json` → `recommended_mm`, `cost` from `05-cost.json` →
`price_tax_excluded` (or the signed contract value if it differs), and `requirements_count` from the
Brief. These are copied from engine output, never typed from memory.

## Finish

Show `sier status` and name the next step it reports. For a new engagement that is almost always
`rfp-notebook` — the Brief comes before analysis, estimation or writing. If the user wants the whole
presale cycle run end to end, point them to the `presale-team` skill.

## Optional: reminders

If the user wants deadline reminders, offer a scheduled task that runs `sier status` and reports
deadlines within 14 / 7 / 3 days. Create it only if they say yes.
