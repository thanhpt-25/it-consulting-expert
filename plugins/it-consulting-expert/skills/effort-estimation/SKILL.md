---
name: effort-estimation
description: >
  Estimate project effort using WBS, function points, or story points, grounded
  in customer RFP/RFQ from NotebookLM. Use this skill when the user asks to
  "estimate effort", "create a WBS", "how long will this take", "工数見積",
  "work breakdown", "man-month estimate", "story point estimation", "estimate
  timeline", "how many man-months", or needs to break down a project into tasks
  with duration estimates. Also trigger for "見積もり", "FP法", "function point",
  "COCOMO", and any request to estimate development time or resources.
---

# Effort Estimation

Produce structured effort estimates for IT projects, **grounded in RFP/RFQ scope from NotebookLM**.

## Grounding

This skill reads the engagement's RFP Brief (`00-rfp-brief.json`) and never invents client requirements. Facts carry `[RFP]` / `[RFP+]` / `[Proposed]` labels as defined in `${CLAUDE_PLUGIN_ROOT}/shared/brief-schema.md`.

## Workflow

### Step 0: Load the engagement (Brief first — NotebookLM only for gaps)

Follow the handoff contract in `${CLAUDE_PLUGIN_ROOT}/shared/engagement-workspace.md`:

1. **Find the workspace:** `python3 "${CLAUDE_PLUGIN_ROOT}/sier" status`. None → run `engagement-init` first.
   (For a one-off question with no engagement, skip the workspace and label every assumption `[Proposed]`.)
2. **Read `00-rfp-brief.json`.** If `sier status` says it is missing or **stale**, run `rfp-notebook` first —
   do not extract the RFP yourself.
3. **From the Brief this skill needs:** `functional_requirements`, `nonfunctional_requirements`, `integrations`, `data_migration`, `timeline`.
4. **Upstream files:** `02-architecture.md` if it exists — the architecture determines integration and infrastructure work.
5. **Gaps only:** `python3 "${CLAUDE_PLUGIN_ROOT}/sier" brief gaps --for effort-estimation`. If it reports no gaps, make
   **no** NotebookLM calls. Otherwise query only for those gaps, per `${CLAUDE_PLUGIN_ROOT}/shared/notebooklm-contract.md`
   (`--notebook <notebook_id> --json`, fallback ladder if NotebookLM is unreachable).
6. **Write back** each answer into `00-rfp-brief.json` as a labelled, cited item, remove the gap, then run
   `sier brief validate` and `sier brief render` so the next skill gets it free.

**Gap queries** — starting points when the Brief is missing one of the fields above:

```bash
notebooklm ask "List every feature, module, or functional requirement that needs to be built" --json --notebook <notebook_id>
notebooklm ask "List all non-functional requirements with specific targets (performance, availability, security)" --json --notebook <notebook_id>
notebooklm ask "What integrations with external systems are required? List each integration point" --json --notebook <notebook_id>
notebooklm ask "What data migration or conversion is needed? Describe the data volumes and sources" --json --notebook <notebook_id>
notebooklm ask "What timeline or deadline constraints does the client specify?" --json --notebook <notebook_id>
notebooklm ask "What technology stack is required or preferred?" --json --notebook <notebook_id>
notebooklm ask "What testing or quality requirements does the client specify?" --json --notebook <notebook_id>
```

### Step 1: Additional Inputs from User

After extracting from the RFP, ask for:
- **Team experience level** with the required stack
- **Estimation method preference**: WBS-based, Function Point, Story Point, or analogous
- **Desired granularity**: high-level (phases) or detailed (task-level)

### Step 2: Choose Estimation Method

| Method | Best For | When to Use |
|--------|----------|-------------|
| **WBS-based (工数積み上げ)** | Waterfall, SIer contracts | Fixed-price contracts, detailed proposals |
| **Function Point (FP法)** | Business applications | Early estimation before design |
| **Story Point / T-shirt sizing** | Agile projects | Ongoing sprints, relative sizing |
| **Analogous (類推法)** | Repeat projects | Similar past projects exist |

Default to **WBS-based** for SIer-style proposals.

### Step 3: Build WBS from RFP Requirements

For each requirement extracted from the RFP, decompose into the standard SIer phases:

**Phase 1: Requirements Definition (要件定義) — typically 10-15% of total**
**Phase 2: Basic Design (基本設計) — typically 15-20%**
**Phase 3: Detailed Design (詳細設計) — typically 15-20%**
**Phase 4: Implementation (製造) — typically 20-25%**
**Phase 5: Integration Testing (結合テスト) — typically 10-15%**
**Phase 6: System Testing (総合テスト) — typically 10-15%**
**Phase 7: Deployment & Transition (移行・リリース) — typically 5-10%**
**Project Management (PM工数) — add 10-15% across all phases**

### Step 4: Estimate Each Task

For each WBS item, estimate in man-days (人日). 1 man-month = ~20 working days = ~160 hours.

Read `references/estimation-templates.md` for per-feature-type estimation benchmarks.
Read `references/function-point-guide.md` for FP method details.

### Step 5: Apply Adjustment Factors

| Factor | Range | Notes |
|--------|-------|-------|
| Technical complexity | 0.8 - 1.5x | New technology = higher |
| Team experience | 0.7 - 1.3x | Experienced team = lower |
| Requirements clarity | 0.9 - 1.4x | Vague RFP sections = higher |
| Distributed team | 1.1 - 1.3x | Offshore = higher |
| Regulatory/compliance | 1.1 - 1.5x | Driven by RFP compliance requirements |

### Step 6: Output Format

**WBS Table with RFP Traceability:**
| ID | RFP Req | Phase | Task | Estimate (人日) | Assignee Role | Dependencies |
|----|---------|-------|------|-----------------|---------------|--------------|

The **RFP Req** column links every estimate to the specific requirement it addresses.

**Summary by Phase:**
| Phase | Man-Days | Man-Months | % of Total |
|-------|----------|------------|------------|

**Risk-Adjusted Range:**
- Optimistic (楽観): base × 0.8
- Most likely (最頻): base × 1.0
- Pessimistic (悲観): base × 1.5
- **Recommended estimate for proposals**: use P75 (base × 1.2)

**Estimation Confidence:**
- Items well-defined in RFP → High confidence
- Items vaguely described in RFP → Medium confidence, flag for clarification
- Items not in RFP but recommended → Low confidence, mark as "Proposed"

## Key Principles

- **Ground every estimate in scope**: No WBS item should exist without a corresponding requirement
- **Flag RFP ambiguities**: Where the RFP is vague, call it out and estimate a range instead of a point
- **Pad honestly**: 20% buffer is professional. Underbidding destroys trust
- **Decompose deeply**: Tasks over 5 man-days should be split further
- **Document assumptions**: Link each assumption to the RFP section it interprets

For estimation templates, read `references/estimation-templates.md`.
For Function Point method, read `references/function-point-guide.md`.
