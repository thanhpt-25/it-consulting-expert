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

### Step 1: Gather Additional Inputs from User

After extracting from the RFP:
- **Effort estimate** (from `effort-estimation` skill or user-provided)
- **Team composition** (from `team-composition` skill or user-provided)
- **Your company's rate card** — use internal rates, not just market benchmarks
- **Currency**: JPY, USD, or other

### Step 2: Labor Cost Calculation

Read `references/rate-cards.md` for market rate benchmarks. Use the user's actual rates when provided — market rates are for sanity-checking only.

**Calculation:**
```
Labor Cost = Σ (Role Rate × Man-Months per Role)
```

| Role | Seniority | Monthly Rate | Man-Months | Subtotal | RFP Constraint |
|------|-----------|-------------|------------|----------|----------------|

The **RFP Constraint** column notes if the RFP caps rates, mandates seniority levels, or dictates team size.

### Step 3: Non-Labor Costs

**Infrastructure** (estimate monthly): Cloud services, dev/staging environments, CI/CD, monitoring

**Licenses**: Dev tools, third-party APIs, security tools, database licenses

**Other**: Travel (出張費), training, hardware, data migration tools

Note which costs the RFP says the client provides vs. expects from the vendor.

### Step 4: Cost Structure by Phase

| Phase | Labor | Infra | License | Other | Phase Total |
|-------|-------|-------|---------|-------|-------------|

### Step 5: Apply Pricing Model

Use the model the RFP specifies. If unspecified, recommend with rationale.

**Fixed Price (一括請負):**
- Add risk premium: 15-25% on cost estimate
- If RFP states a ceiling → work backward from it
- Payment schedule: match RFP milestones if stated

**T&M (準委任):**
- Bill at agreed rates
- Set budget caps if RFP requires
- Include minimum commitment period

**Hybrid:**
- Fixed for well-defined phases, T&M for evolving scope

### Step 6: Budget Fit Check

**Critical**: Compare your total against the RFP's stated budget:
- **Within budget**: Proceed normally
- **Over budget**: Flag the gap, propose scope reductions or phasing options
- **Under budget**: Verify you haven't missed scope items; the gap may indicate missed requirements

### Step 7: Output

**Cost Summary:**
| Category | Amount | Notes |
|----------|--------|-------|
| Labor | ¥XX,XXX,XXX | X man-months total |
| Infrastructure | ¥X,XXX,XXX | |
| Licenses | ¥X,XXX,XXX | |
| Other | ¥XXX,XXX | |
| **Subtotal** | | |
| Management Fee (10%) | | |
| Risk Buffer (15%) | | |
| **Grand Total** | | |
| *RFP Budget* | *¥XX,XXX,XXX* | *Client's stated range* |

**Payment Schedule** aligned to RFP milestones if stated.

**TCO Analysis** (for infrastructure projects): 3-year and 5-year projection.

## Key Principles

- **Respect the budget**: If the RFP states a range, design within it or explain why it's insufficient
- **Transparency**: Every line item traceable to scope
- **No hidden costs**: Call out the risk buffer explicitly
- **Scope linkage**: Every cost traces to a WBS task which traces to an RFP requirement

For rate card references, read `references/rate-cards.md`.
