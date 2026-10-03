---
name: cost-estimation
description: >
  Create cost estimations, budget breakdowns, and pricing for IT consulting
  projects, grounded in customer RFP/RFQ from NotebookLM. Use this skill when
  the user asks to "estimate cost", "create a budget", "calculate pricing",
  "費用見積", "コスト計算", "how much will this cost", "rate card", "TCO analysis",
  "total cost of ownership", or needs to produce financial projections for a
  project proposal. Also trigger for "予算", "単価", "pricing model", and any
  request involving project financials, billing structure, or cost-benefit analysis.
---

# Cost Estimation

Generate detailed cost breakdowns for IT consulting engagements, **grounded in RFP/RFQ budget constraints and scope from NotebookLM**.

## Grounding

This skill reads the engagement's RFP Brief (`00-rfp-brief.json`) and never invents client requirements. Facts carry `[RFP]` / `[RFP+]` / `[Proposed]` labels as defined in `${CLAUDE_PLUGIN_ROOT}/shared/brief-schema.md`.

## Workflow

### Step 0: Load the engagement (Brief first — NotebookLM only for gaps)

Follow the handoff contract in `${CLAUDE_PLUGIN_ROOT}/shared/engagement-workspace.md`:

1. **Find the workspace:** `python3 "${CLAUDE_PLUGIN_ROOT}/sier" status`. None → run `engagement-init` first.
   (For a one-off question with no engagement, skip the workspace and label every assumption `[Proposed]`.)
2. **Read `00-rfp-brief.json`.** If `sier status` says it is missing or **stale**, run `rfp-notebook` first —
   do not extract the RFP yourself.
3. **From the Brief this skill needs:** `commercial.budget`, `commercial.pricing_model`, `commercial.payment_terms`, `evaluation.criteria` (is price weighted?).
4. **Upstream files:** `03-estimate.json` (effort to reconcile against) and `04-team.json` (labor lines).
5. **Gaps only:** `python3 "${CLAUDE_PLUGIN_ROOT}/sier" brief gaps --for cost-estimation`. If it reports no gaps, make
   **no** NotebookLM calls. Otherwise query only for those gaps, per `${CLAUDE_PLUGIN_ROOT}/shared/notebooklm-contract.md`
   (`--notebook <notebook_id> --json`, fallback ladder if NotebookLM is unreachable).
6. **Write back** each answer into `00-rfp-brief.json` as a labelled, cited item, remove the gap, then run
   `sier brief validate` and `sier brief render` so the next skill gets it free.

**Gap queries** — starting points when the Brief is missing one of the fields above:

```bash
notebooklm ask "What budget range, cost ceiling, or financial constraints does the client state?" --json --notebook <notebook_id>
notebooklm ask "What pricing model does the client prefer — fixed price, time and materials, or other?" --json --notebook <notebook_id>
notebooklm ask "What payment terms, invoicing schedule, or financial milestones does the client specify?" --json --notebook <notebook_id>
notebooklm ask "Are there any cost-related evaluation criteria? Does the client weight price in proposal scoring?" --json --notebook <notebook_id>
notebooklm ask "What infrastructure, licensing, or third-party costs does the client expect the vendor to cover vs. provide themselves?" --json --notebook <notebook_id>
```

### Step 1: Gather inputs from the workspace, not the user

- **Effort**: `03-estimate.json` (from `sier estimate`). Missing → run `effort-estimation` first.
- **Team**: `04-team.json` — role, seniority and 人月 per line. Missing → run `team-composition`.
- **Rates**: the firm's `_firm/rate-card.json`. Missing → `sier ratecard init` writes benchmark midpoints that
  the engine flags on every run; tell the user a bid priced on benchmarks needs real rates before it goes out.
- **Budget, pricing model, payment terms**: the Brief (`commercial`). The engine reads the budget itself.
- Ask the user only for what none of these hold: non-labor items, a pricing-model preference the RFP left
  open, the risk premium within the policy range.

### Step 2: Write the cost input

`inputs/cost.json` (format: `${CLAUDE_PLUGIN_ROOT}/shared/engine.md`):

- `labor`: one line per `04-team.json` role/seniority with its 人月. Give `rate` only to override the rate card.
- `non_labor`: infrastructure (monthly × months), licenses, travel (出張費), migration tools. Mark items the
  RFP says the client supplies `"provided_by": "client"` — listed, not priced.
- `pricing`: `fixed` (一括請負), `tm` (準委任) or `hybrid` with `fixed_share`; the risk premium for fixed work.
  Use the model the RFP specifies; if it is silent, recommend one and say why.
- `payment_schedule`: match the Brief's `timeline.milestones` when the RFP states them.
- `tco` for infrastructure engagements (3- and 5-year view).

### Step 3: Compute with the engine — never by hand

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/sier" cost
```

It writes `05-cost.json` / `05-cost.md`: labor and non-labor tables, cost subtotal (総原価), management fee,
risk premium, price 税抜 and 税込 (consumption tax from policy), gross margin, payment schedule, TCO, and two
checks no prose estimate ever did reliably:

- **Budget fit** against the Brief's budget, on the right tax basis.
- **Reconciliation**: does the team's total 人月 match the estimate's recommended 人月 (within policy
  tolerance)? If not, the team plan and the estimate describe different projects — fix one of them.

Copy its tables into documents verbatim. **Never type, round or adjust a figure the engine produced.**

### Step 4: Act on the findings

- **Over budget** — do not shave the risk premium below policy to make it fit. Present options: phase the
  scope, cut `should`/`may` requirements (the Brief has priorities), change the pricing model, or propose
  the overrun with justification. That is the user's decision, with numbers for each option (re-run the
  engine per option).
- **Well under budget** — check for missed scope before celebrating.
- **Risk premium or fee outside policy** — the engine says so. Keep it only with a stated reason.

**Spreadsheet.** For an Excel 見積書, build `artifacts/cost.xlsx` with the `xlsx` skill from `05-cost.json`.

## Key Principles

- **Respect the budget**: If the RFP states a range, design within it or explain why it's insufficient
- **Transparency**: Every line item traceable to scope
- **No hidden costs**: Call out the risk buffer explicitly
- **Scope linkage**: Every cost traces to a WBS task which traces to an RFP requirement

For rate card references, read `references/rate-cards.md`.
