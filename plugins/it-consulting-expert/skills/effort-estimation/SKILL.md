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

要件定義 → 基本設計 → 詳細設計 → 製造 → 結合テスト → 総合テスト → 移行・リリース, with PM effort added on top.

The typical share of each phase, and the PM overhead range, live in `shared/policy.json` (`estimation`).
Don't restate them — estimate bottom-up per task, and let the engine flag any phase whose share falls
outside its typical range. A flagged phase is a prompt to check, not an error: explain it or fix it.

### Step 4: Estimate each task in 人日

Estimate each WBS item in man-days (人日), using the benchmarks in `references/estimation-templates.md`.
Split anything over 5 人日. Every item carries the Brief requirement id it implements (`req`), or
`"label": "Proposed"` when it is your recommendation (cross-cutting work such as environments, CI/CD,
documentation, training).

### Step 5: Choose adjustment factors — with a reason for each

| Factor | Bounds | Raise it when |
|---|---|---|
| `technical_complexity` | 0.8–1.5 | new or unproven technology |
| `team_experience` | 0.7–1.3 | below 1.0 for an experienced team; above for a new stack |
| `requirements_clarity` | 0.9–1.4 | Brief has many `scope_ambiguous` items or open gaps |
| `distributed_team` | 1.0–1.3 | offshore / multi-site delivery |
| `regulatory` | 1.0–1.5 | the Brief's compliance NFRs (金融, 医療, 官公庁) |
| `integration_complexity` | 1.0–1.5 | many or legacy integrations in `integrations` |

Bounds are enforced by the engine (`shared/policy.json`). Factors **multiply** — 1.1 × 1.1 × 1.1 is
1.33, not 1.3 — which is exactly the arithmetic the engine exists to get right.

### Step 6: Compute with the engine — never by hand

Write `inputs/estimate.json` in the workspace (format: `${CLAUDE_PLUGIN_ROOT}/shared/engine.md`), then:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/sier" estimate
```

It writes `03-estimate.json` / `03-estimate.md` with the phase table, PM overhead, the factor product,
the three-point range, the **recommended figure for the proposal**, the allocation by role that
team-composition and cost-estimation consume, and findings: untraced items, oversized tasks, phases
outside their typical share. **Do not type any of these numbers yourself, and do not "tidy" them.**
To change a result, change an input and re-run.

Address every finding before handing over — trace or relabel untraced items, split oversized tasks,
and explain any phase share the engine flags.

For Function Points use `"method": "fp"` (counting rules in `references/function-point-guide.md`).
FP covers design, build and unit test; add WBS items for 移行 and anything else outside that scope.

**Your track record.** If `_firm/calibration.json` has closed projects of the same `project_type`, the
output shows how they ran against their estimates. Show it to the user. Applying it
(`"apply_calibration": true`) is their call, not yours.

**Spreadsheet.** If the user wants the WBS as Excel, build `artifacts/estimate.xlsx` with the `xlsx`
skill *from `03-estimate.json`* — the workbook mirrors the engine's numbers; it does not recompute them.

## Key Principles

- **Ground every estimate in scope**: No WBS item should exist without a corresponding requirement
- **Flag RFP ambiguities**: Where the RFP is vague, call it out and estimate a range instead of a point
- **Pad honestly**: the recommended figure already applies the policy multiplier (`shared/policy.json`); don't add a second buffer on top
- **Decompose deeply**: Tasks over 5 man-days should be split further
- **Document assumptions**: Link each assumption to the RFP section it interprets

For estimation templates, read `references/estimation-templates.md`.
For Function Point method, read `references/function-point-guide.md`.
