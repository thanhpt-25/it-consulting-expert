# The sier engine — command reference for skills and agents

`sier` computes every contractual number in this plugin. **Skills and agents must not do this
arithmetic in prose.** Prepare a JSON input, run the command, and paste the Markdown it prints.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/sier" <command> [options]
```

Python 3.7+ standard library only — nothing to install. Every command prints Markdown. Inside an
engagement workspace it also saves JSON + Markdown artifacts, copies its input to `inputs/`, and
writes an audit record to `_state/runs/`. Exit codes: `0` ok · `1` verify found problems ·
`2` bad input · `3` warnings under `--strict`.

All policy numbers (rubric weights, phase ranges, factor bounds, fees, premiums, EVM thresholds,
CR gates, SLA windows) live in `${CLAUDE_PLUGIN_ROOT}/shared/policy.json`. Never restate them.

## Workspace

| Command | Does |
|---|---|
| `sier init --client X --project Y [--notebook ID] [--root DIR]` | Create the engagement folder |
| `sier status` | Pipeline, deadlines, stale Brief warning, next step |
| `sier verify` | Recompute every artifact from its inputs; cross-check estimate ↔ team ↔ cost ↔ budget |
| `sier runs` | Audit trail of engine runs |

## RFP Brief

| Command | Does |
|---|---|
| `sier brief validate` | Schema check: labels, citations, ids, dates, budget basis |
| `sier brief render` | Write `00-rfp-brief.md` from the JSON; updates `engagement.json` |
| `sier brief gaps --for <skill>` | Open questions that block that skill (and only those) |

Schema: `shared/brief-schema.md`.

## Computations

Each reads `inputs/<name>.json` by default, or `--in FILE`. Use `--no-ws` to just print.

### `sier score` — Go/No-Go → `01-go-nogo.*`
```json
{"scores": {"strategic_fit": 4, "capability_match": 4, "win_probability": 3,
            "profitability": 3, "delivery_risk": 3, "resource_availability": 3},
 "rationale": {"strategic_fit": "why", "...": "one line per dimension"},
 "mandatory": [{"requirement": "ISMS認証", "met": true, "evidence": "cert no."}],
 "conditions": ["condition for a conditional GO"]}
```
`met` is `true`, `false` or `"workaround"`. Any `false` forces DEFINITE_NO_GO.

### `sier estimate` — effort → `03-estimate.*`
```json
{"project_type": "crm_migration", "method": "wbs", "pm_overhead": 0.12,
 "factors": {"technical_complexity": 1.1, "team_experience": 0.95, "requirements_clarity": 1.1,
             "distributed_team": 1.15, "regulatory": 1.0, "integration_complexity": 1.1},
 "items": [{"id": "W-001", "req": "FR-001", "phase": "基本設計", "task": "画面設計",
            "days": 4, "role": "SE", "confidence": "high", "label": "RFP"}]}
```
Phases accept the id (`basic_design`) or Japanese name (`基本設計`). Every item needs a `req` from the
Brief, or `"label": "Proposed"`. Function points: `"method": "fp"` plus
`"fp": {"counts": {"EI": {"low": 2, "avg": 3, "high": 1}, ...}, "gsc": [14 ratings 0–5], "hours_per_fp": 10}`.
If `_firm/calibration.json` has history for `project_type`, the output shows your track record;
`"apply_calibration": true` uses it.

### `sier cost` — price → `05-cost.*`
```json
{"labor": [{"role": "SE", "seniority": "mid", "mm": 24}, {"role": "PM", "seniority": "senior", "mm": 6, "rate": 1300000}],
 "non_labor": [{"category": "infra", "item": "AWS", "monthly": 300000, "months": 12},
               {"category": "travel", "item": "出張費", "one_time": 500000},
               {"category": "license", "item": "client-supplied DB", "one_time": 0, "provided_by": "client"}],
 "pricing": {"model": "fixed", "risk_premium": 0.15},
 "payment_schedule": [{"milestone": "契約時", "pct": 30}, {"milestone": "検収", "pct": 70}],
 "tco": {"years": [3, 5], "annual_run_cost": 3600000}}
```
Rates come from the line, else `_firm/rate-card.json` (`sier ratecard init` creates a benchmark one).
The budget comes from the Brief automatically; the estimate from `03-estimate.json` automatically —
the output says whether team 人月 reconciles with it. Models: `fixed`, `tm`, `hybrid` (+ `fixed_share`).

### `sier evm` — earned value → `progress/evm-<date>.*`
`{"status_date": "2026-10-31", "bac": 100000000, "pv": 40000000, "ev": 36000000, "ac": 41000000}`
or `"tasks": [{"id", "planned_value", "planned_pct", "pct_complete", "actual_cost"}]`.

### `sier sla` — downtime and maintenance fee → `07-sla.*`
`{"project_cost": 197796000, "maintenance_rate": 0.15, "support_24x7": false, "contract_years": 3,
  "availability_tiers": [{"id": "enhanced", "target": 99.9, "window": "24x7"}]}`

### `sier cr add --in cr.json` / `sier cr report` — change ledger → `progress/cr-report.*`
`{"id": "CR-001", "title": "...", "status": "proposed|approved|rejected|deferred",
  "cost_delta": 4500000, "effort_delta_mm": 4, "schedule_delta_days": 10, "go_live_changes": false}`
Baseline comes from `engagement.json` → `baseline`. Report shows cumulative deviation gates and the
approval authority each CR needs.

## Firm data

| Command | Does |
|---|---|
| `sier ratecard init` / `show` | Create (benchmark) / show `_firm/rate-card.json` |
| `sier calibrate add --in rec.json` / `show` | Record a closed project's estimate vs actual |

Calibration record: `{"project": "ABC-CRM", "project_type": "crm_migration", "estimated_mm": 132,
"actual_mm": 168, "estimated_cost": 198000000, "actual_cost": 231000000, "closed": "2027-12-20"}`.

## Tier-2 generated analysis

`sier derive run _state/derived/<name>.py` runs a script you wrote for a question the engines don't
cover. Rules in `shared/harness.md`.
