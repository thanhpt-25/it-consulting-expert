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
metadata:
  version: "0.2.0"
---

# IT Consulting Proposal Generator

Generate professional IT consulting proposals following Japanese SIer (System Integrator) standards, **grounded in customer RFP/RFQ documents stored in NotebookLM**.

## Critical Rule: NotebookLM as Single Source of Truth

Every client-specific fact in the proposal MUST come from querying the NotebookLM notebook that contains the customer's RFP/RFQ. Do not invent requirements, timelines, budgets, or technical constraints. If the RFP doesn't address a topic, explicitly mark the section as "Proposed (not specified in RFP)" so the client knows what's your recommendation vs. their stated need.

Read `references/notebooklm-integration.md` for the full integration guide including query patterns, citation rules, and grounding rules.

## Workflow

### Step 0: Connect to NotebookLM (MANDATORY)

Before any proposal work, establish the data source:

1. Ask the user which NotebookLM notebook contains the client's RFP/RFQ
2. List available notebooks:
   ```bash
   notebooklm list --json
   ```
3. Set context to the target notebook:
   ```bash
   notebooklm use <notebook_id>
   ```
4. Verify sources are ready:
   ```bash
   notebooklm source list --json
   ```
   All sources must show `"status": "ready"`. If not, wait with `notebooklm source wait`.

If the user hasn't uploaded the RFP yet, help them:
```bash
notebooklm create "RFP - [Client Name] - [Project Name]" --json
notebooklm source add ./rfp-document.pdf --json
notebooklm source wait <source_id> -n <notebook_id> --timeout 600
```

### Step 1: Extract RFP Requirements from NotebookLM

Run these extraction queries to build a complete picture. Use `--json` on every query to get citations:

```bash
# Project overview
notebooklm ask "What is the project name, client name, and overall objective described in this RFP?" --json

# Scope
notebooklm ask "List all items that are in-scope and out-of-scope for this project" --json

# Functional requirements
notebooklm ask "List all functional requirements, features, or capabilities the client expects" --json

# Non-functional requirements
notebooklm ask "List all non-functional requirements: performance targets, security requirements, availability SLAs, scalability needs, compliance standards" --json

# Technical constraints
notebooklm ask "What technology constraints, platform requirements, or integration needs does the client specify?" --json

# Timeline and milestones
notebooklm ask "What timeline, deadlines, milestones, or phase expectations does the client state?" --json

# Budget
notebooklm ask "What budget range, cost constraints, or pricing expectations are mentioned?" --json

# Evaluation criteria
notebooklm ask "How will the client evaluate proposals? What are the scoring criteria or selection factors?" --json

# Team / methodology preferences
notebooklm ask "Does the client specify team size, roles, development methodology preferences, or delivery model requirements?" --json

# Deliverables
notebooklm ask "What specific deliverables, documents, or artifacts does the client expect?" --json

# Current state
notebooklm ask "Describe the client's current IT systems, infrastructure, or business processes mentioned in the document" --json
```

Store all extracted data before proceeding. Every answer comes with citations — use them.

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
- If RFP specifies team requirements → address them directly
- Reference the `team-composition` skill for full team planning

**7. Schedule (スケジュール)**
- Anchor to any RFP-stated deadlines or milestones
- Build timeline around RFP constraints, not generic defaults

**8. Cost Estimation (費用見積)**
- If RFP states budget → design within it
- Reference the `cost-estimation` skill for detailed breakdown

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
- Create a traceability table mapping EVERY RFP requirement to the proposal section that addresses it
- This demonstrates thoroughness and makes evaluation easier for the client

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

## Cross-Skill Integration

This skill orchestrates other skills in the plugin. When invoking them, pass the NotebookLM notebook ID so they can also query the RFP:

- `team-composition` — pass RFP team requirements
- `effort-estimation` — pass RFP scope and feature list
- `cost-estimation` — pass RFP budget constraints
- `technical-solution` — pass RFP technical requirements and constraints
- `project-delivery` — pass RFP methodology and timeline requirements

For the NotebookLM integration guide, read `references/notebooklm-integration.md`.
For deliverable templates, read `references/deliverables-template.md`.
For proposal formatting guidelines, read `references/proposal-format.md`.
