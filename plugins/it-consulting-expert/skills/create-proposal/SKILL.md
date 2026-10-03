---
name: create-proposal
description: >
  Create IT consulting proposals and quotation documents grounded in customer
  RFP/RFQ uploaded to NotebookLM. Use this skill whenever the user asks to
  "create a proposal", "write a proposal", "draft a quotation", "make a bid",
  "prepare an RFP response", "提案書を作成", or needs to produce a formal
  consulting proposal for software development, infrastructure, or digital
  transformation projects. Also trigger when the user mentions "proposal",
  "quotation", "見積書", "提案", or wants to put together a client-facing
  project offer document — even if they don't say "proposal" explicitly.
---

# IT Consulting Proposal Generator

Generate professional IT consulting proposals following Japanese SIer (System Integrator) standards, **grounded in customer RFP/RFQ documents stored in NotebookLM**.

## Critical rule: the Brief is the single source of truth

Every client-specific fact in the proposal comes from the engagement's RFP Brief
(`00-rfp-brief.json`), which `rfp-notebook` extracted from NotebookLM with citations. Every number
comes from an engine artifact (`03-estimate`, `05-cost`, `01-go-nogo`). Do not invent requirements,
dates, budgets or constraints, and do not retype a computed figure. Where the RFP is silent, say so
and label the content `[Proposed]`.

**Running the whole presale cycle?** Use the `presale-team` skill. It runs the architect, estimator,
staffing planner and cost controller as parallel agents, then calls this skill to write — and the
review board after it. Use this skill directly to write or revise the proposal document itself.

## Workflow

### Step 0: Load the engagement

Follow `${CLAUDE_PLUGIN_ROOT}/shared/engagement-workspace.md`. Run `python3 "${CLAUDE_PLUGIN_ROOT}/sier" status`:

- No workspace → `engagement-init`. Brief missing or stale → `rfp-notebook`. Do not extract the RFP here.
- Read what exists: `00-rfp-brief.json`, `01-go-nogo.json`, `02-architecture.md`, `03-estimate.json`,
  `04-team.json`, `05-cost.json`, `06-delivery-plan.md`.
- For each missing section input, run the owning skill first (see "Where each section's content comes from" below) — or, if the user wants a
  draft now, write that section from the Brief and mark it `【未確定 — <skill> 未実行】` so nobody mistakes
  it for a computed figure.
- `python3 "${CLAUDE_PLUGIN_ROOT}/sier" brief gaps --for create-proposal` — query NotebookLM only for those.

### Step 1: Confirm the deliverables the client asked for

From the Brief: `evaluation.submission_requirements` (format, page limit, mandatory sections, copies,
delivery method), `evaluation.criteria` (the order evaluators read in — mirror it), and the
requirement ids (`FR-*`, `NFR-*`, `INT-*`) the compliance matrix must cover. A missing mandatory
section or an over-length document can disqualify a bid before anyone reads it.

### Step 2: Gather Additional Inputs from User

After extracting from the RFP, ask the user only for what's missing:

- **Your company name** (for cover page)
- **Proposal format**: .docx or .pdf (default: .docx)
- **Language**: Japanese, English, or bilingual
- **Any additional context** not in the RFP (e.g., prior relationship with client, internal rate cards, competitive intelligence)

### Step 3: Research Phase (Supplement, Don't Replace)

If web search is available, research to **supplement** RFP data:
- Client's industry trends (for the executive summary context)
- Technology benchmarks relevant to the proposed solution
- Competitive landscape for pricing sanity-check

**Important**: Research supplements the RFP — it never overrides it. If the RFP says "must use Azure" and your research suggests AWS is better, note the recommendation but respect the constraint.

### Step 4: Generate Proposal

Write each section using this structure. For every section, the source of each claim must be clear:

**Cover Page**
- Proposal title, client name, date, your company name

**1. Executive Summary (エグゼクティブサマリー)**
- 1-page overview synthesizing: client's stated problem (from RFP), proposed solution, expected outcomes, investment summary
- Every business need referenced here must trace to an RFP citation

**2. Background & Current State Analysis (背景・現状分析)**
- Client's business context (from RFP extraction)
- Current IT landscape and pain points (from RFP "current state" query)
- Opportunity analysis (your professional interpretation, marked as such)

**3. Proposed Solution (提案ソリューション)**
- Solution architecture overview addressing each requirement extracted from the RFP
- Technology stack: respect RFP constraints, propose alternatives only where RFP is open
- Map each feature to the specific RFP requirement it addresses
- Reference the `technical-solution` skill for deep architecture design

**4. Project Scope (プロジェクトスコープ)**
- In-scope: directly from RFP extraction
- Out-of-scope: directly from RFP extraction + your recommended exclusions (marked as "Proposed")
- Assumptions and prerequisites: extract from RFP + add professional assumptions

**5. Project Approach & Methodology (開発手法・プロジェクトアプローチ)**
- If RFP specifies methodology → use it
- If RFP is silent → propose with rationale, marked as "Proposed"
- Reference the `project-delivery` skill for detailed methodology

**6. Team Structure (体制図)**
- From `04-team.json` / `04-team.md`; RFP staffing requirements (`team_process.staffing`) addressed explicitly
- Org chart: use the `drawio` skill when available, otherwise mermaid

**7. Schedule (スケジュール)**
- Anchor to any RFP-stated deadlines or milestones
- Build timeline around RFP constraints, not generic defaults

**8. Cost Estimation (費用見積)**
- Copy the tables from `05-cost.md` verbatim — price 税抜/税込, payment schedule, assumptions. Never retype or round them.
- If `05-cost.json` → `budget_fit.status` is `over`, stop and tell the user before writing: a proposal over the
  RFP budget needs a decision (scope reduction, phasing, or a deliberate overrun with justification), not prose

**9. Deliverables List (納品物一覧)**
- Start with RFP-required deliverables
- Add standard SIer deliverables as "Proposed additions"
- See `references/deliverables-template.md`

**10. Risk Analysis (リスク分析)**
- Risks derived from RFP complexity and constraints
- Do NOT invent risks not grounded in the actual project scope

**11. Terms & Conditions (契約条件)**
- Address any RFP-stated contract terms
- Propose standard terms for anything not specified

**12. Compliance Matrix (RFP対応表)** — IMPORTANT
- One row per requirement id in the Brief (`FR-*`, `NFR-*`, `INT-*`, mandatory qualifications) — every id, no exceptions
- Before finishing, check coverage: every id in the Brief appears in the matrix, and every matrix row names a section
  that exists. Japanese evaluators check this table line by line; a missing id is a lost point

| RFP Requirement ID | Requirement | Proposal Section | How Addressed |
|--------------------|-------------|-----------------|---------------|

**Appendices**
- Detailed WBS (reference `effort-estimation` skill)
- Technology comparison matrix
- Team member profiles
- Company profile and past projects

### Step 5: Output

Generate the proposal as a .docx file using the `docx` skill, or as a .pdf using the `pdf` skill. Default to .docx.

## Labeling Convention

Throughout the proposal, use these labels to distinguish source vs. recommendation:

- **[RFP]** — directly stated in the client's RFP/RFQ
- **[Proposed]** — your professional recommendation where the RFP is silent
- **[RFP+]** — extends an RFP requirement with additional professional recommendation

These labels appear in internal drafts. Remove them from the final client-facing document, but retain the compliance matrix (section 12) which serves the same traceability purpose in polished form.

## Where each section's content comes from

| Section | Source file | Owning skill |
|---|---|---|
| 1–2 Summary, background | `00-rfp-brief.json`, `01-go-nogo.json` (win themes) | rfp-notebook, rfp-analysis |
| 3 Solution | `02-architecture.md` | technical-solution |
| 5, 7 Approach, schedule | `06-delivery-plan.md` | project-delivery |
| 6 Team | `04-team.json` | team-composition |
| 8 Cost | `05-cost.md` (engine output) | cost-estimation |
| Appendix WBS | `03-estimate.md` (engine output) | effort-estimation |
| 12 Compliance matrix | requirement ids in the Brief | this skill |

Save the document to `artifacts/proposal.docx` (docx skill) so `sier status` and the review board find it.
Before submission, run the `proposal-review` skill and `python3 "${CLAUDE_PLUGIN_ROOT}/sier" verify`.

For the NotebookLM integration guide, read `references/notebooklm-integration.md`.
For deliverable templates, read `references/deliverables-template.md`.
For proposal formatting guidelines, read `references/proposal-format.md`.
