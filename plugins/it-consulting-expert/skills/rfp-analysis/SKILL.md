---
name: rfp-analysis
description: >
  Analyze an RFP/RFQ and produce a Go/No-Go recommendation before committing to
  proposal writing. Use this skill when the user asks to "analyze this RFP",
  "should we bid on this", "案件評価", "Go/No-Go判断", "evaluate this opportunity",
  "RFP assessment", "is this deal worth pursuing", "案件判断", "bid/no-bid
  decision", or needs to assess whether an RFP is worth the effort of responding.
  Also trigger for "win probability", "competitive analysis for this bid",
  "提案可否判断", and any request to evaluate an RFP before committing resources.
  This skill should run BEFORE create-proposal — it's the gatekeeper that prevents
  wasting effort on unwinnable or unprofitable bids.
---

# RFP Analysis & Go/No-Go Assessment (案件評価・提案可否判断)

Analyze a customer RFP/RFQ and produce a structured Go/No-Go recommendation. This skill runs BEFORE any proposal work begins — it's the gatekeeper that saves your team from investing weeks on bids you can't or shouldn't win.

## Why This Matters

In Japanese SIer consulting, proposal effort is expensive — a serious bid can consume 2-6 weeks of senior staff time. Experienced firms win 20-40% of bids they pursue. The difference between profitable and unprofitable firms is often the quality of their Go/No-Go process, not the quality of their proposals.

## Workflow

### Step 0: Load the engagement

Follow `${CLAUDE_PLUGIN_ROOT}/shared/engagement-workspace.md`: run `python3 "${CLAUDE_PLUGIN_ROOT}/sier" status`;
no workspace → `engagement-init`; Brief missing or stale → `rfp-notebook` first. Do not extract the RFP here.

### Step 1: Read the assessment inputs from the Brief

Everything the Go/No-Go needs is already in `00-rfp-brief.json`:

| Assessment input | Brief field |
|---|---|
| Deal basics, deadline | `client`, `project`, `timeline.proposal_submission`, `commercial.budget` |
| Scope and complexity | `overview.scope_in`, `functional_requirements`, `integrations`, `data_migration` |
| Mandatory qualifications | `evaluation.mandatory_qualifications` |
| Evaluation criteria and weights | `evaluation.criteria` |
| Technology requirements | `constraints`, `nonfunctional_requirements` |
| Contract structure | `commercial.pricing_model`, `commercial.payment_terms`, `contract_terms` |
| Penalties and unusual risk | `contract_terms`, `risks` |

Then `python3 "${CLAUDE_PLUGIN_ROOT}/sier" brief gaps --for rfp-analysis`. One signal is rarely in the
Brief and is worth a direct query when the notebook is set — incumbency:

```bash
notebooklm ask "Are there any references to an incumbent vendor, current system provider, or signals about competitive landscape?" --json --notebook <notebook_id>
```

Write whatever you learn back into the Brief (Step 6 of the handoff contract).

### Step 2: Score Each Dimension

**Weights are defined once, in `shared/policy.json` (`rubric`). Do not hardcode weights here or in any worked example.**

Evaluate on a 1-5 scale across these dimensions:

**A. Strategic Fit (戦略適合性)**
- Does this align with our target industries and growth strategy?
- Does winning this open doors to follow-on work?
- Does the client represent a strategic account we want to develop?

**B. Capability Match (技術適合性)**
- Do we have the required technology expertise?
- Can we meet mandatory qualifications (certifications, past performance)?
- Do we have enough bench strength to staff this?

**C. Win Probability (受注確度)**
- Is there an incumbent with advantage?
- Do we have prior relationship with this client?
- Are the evaluation criteria favorable to our strengths?
- Is this a "checkbox RFP" (client already chose, just needs paperwork)?

**D. Profitability (収益性)**
- Is the deal size worth the proposal effort?
- Can we deliver within the client's budget at acceptable margins?
- Are the contract terms commercially reasonable?
- Are penalty/warranty clauses manageable?

**E. Delivery Risk (デリバリーリスク)**
- Is the timeline realistic for the scope?
- Are requirements clear enough to estimate?
- Are there integration or migration complexities?
- Are there regulatory or compliance risks?

**F. Resource Availability (リソース確保)**
- Can we staff key roles (PM, TL) from our current bench?
- Do we need to hire or subcontract, and can we do that in time?
- Does this conflict with other active proposals or projects?

### Step 3: Produce the Assessment Sheet (案件評価シート)

**Header:**
| Field | Value |
|-------|-------|
| RFP Title | [from RFP] |
| Client | [from RFP] |
| Estimated Value | [from RFP or estimated] |
| Submission Deadline | [from RFP] |
| Project Duration | [from RFP] |
| Assessment Date | [today] |
| Assessed By | [user] |

**Scoring — computed, not typed.** Write `inputs/go-nogo.json` with a 1–5 score *and a one-line rationale*
for each of the six dimensions, every mandatory qualification from the Brief with `met: true | false |
"workaround"` and its evidence, and the conditions a conditional GO depends on:

```json
{"scores": {"strategic_fit": 4, "capability_match": 4, "win_probability": 3,
            "profitability": 3, "delivery_risk": 3, "resource_availability": 3},
 "rationale": {"strategic_fit": "製造業はターゲット業界", "capability_match": "…", "win_probability": "…",
               "profitability": "…", "delivery_risk": "…", "resource_availability": "…"},
 "mandatory": [{"requirement": "ISMS認証取得", "met": true, "evidence": "ISO27001 cert no. …"}],
 "conditions": ["EDIパートナーの稼働確認"]}
```

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/sier" score
```

The engine applies the canonical weights and thresholds from `shared/policy.json`, forces
DEFINITE_NO_GO when any mandatory requirement is unmet, and writes `01-go-nogo.json` / `.md`. Paste
its matrix into the assessment sheet; never retype or adjust the total. If you disagree with the
verdict, change a *score* and its rationale — not the arithmetic.

"Profitability" must reflect real numbers when they exist: if `05-cost.json` has been computed, score
it from that file's `gross_margin` and `budget_fit`, not from an impression.

### Step 4: Risk and Opportunity Analysis

**Top Risks (if we bid):**
| Risk | Impact | Mitigation Possible? |
|------|--------|---------------------|

**Top Opportunities (if we win):**
| Opportunity | Value | Probability |
|-------------|-------|-------------|

**Red Flags (deal-breakers to watch for):**
- Unrealistic timeline relative to scope
- Budget that can't cover the required team
- Penalty clauses with uncapped liability
- "Wired" RFP signals (evaluation criteria perfectly matching one vendor)
- Client history of late payments or difficult relationships

### Step 5: Recommendation

Produce a clear recommendation:

**GO** — with estimated proposal effort and key staffing needs for the bid team
**CONDITIONAL GO** — with specific conditions that must be resolved before committing
**NO-GO** — with a polite decline message template

If GO, estimate the proposal effort:
| Activity | Who | Days |
|----------|-----|------|
| RFP analysis (done) | | |
| Solution design | TL/Architect | |
| Estimation | PM/TL | |
| Proposal writing | PM/BA | |
| Review & polish | Management | |
| Presentation prep | PM/Sales | |
| **Total proposal cost** | | |

### Step 6: Output

Generate as a .docx document (using the `docx` skill) for circulation to the Go/No-Go decision meeting. This is an internal document — it should be frank and direct, not client-facing.

## Key Principles

- **Be brutally honest**: This document protects the company from bad bids. Optimism here costs real money downstream.
- **Mandatory requirements are binary**: You either meet them or you don't. "We can probably get that certification in time" is not meeting the requirement.
- **Consider the opportunity cost**: Every bid you pursue is time NOT spent on other opportunities.
- **Factor in proposal fatigue**: If your team is already writing 3 proposals, a 4th one will suffer in quality.
- **Incumbents win ~60% of rebids**: If there's an incumbent and you're the challenger, your win probability starts low.

For the Go/No-Go scoring template, read `references/scoring-template.md`.
