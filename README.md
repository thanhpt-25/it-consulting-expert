# IT Consulting Expert Plugin

Full-lifecycle IT consulting expert for Japanese SIer (System Integrator) engagements — from the first
read of an RFP through proposal, delivery and maintenance — following Japanese enterprise conventions,
bilingual (Japanese/English).

**What makes 2.0 different**

- **One engagement folder, one RFP extraction.** `rfp-notebook` extracts the client's RFP from NotebookLM
  once into a validated, cited **RFP Brief** (`00-rfp-brief.json`). Every other skill reads it and asks
  NotebookLM only about gaps — ~90 queries per engagement became 26.
- **No arithmetic in prose.** Effort, cost, price, tax, budget fit, Go/No-Go score, EVM, SLA and change gates
  are computed by **`sier`**, a bundled, tested calculation engine. `sier verify` re-derives every number
  from its saved inputs and fails if one was edited by hand or went stale.
- **Agent teams.** A **presale team** (RFP analyst, architect, estimator, staffing planner, cost controller,
  writer) runs the bid wave by wave with human gates, and the **review board** runs as independent
  parallel reviewers.
- **Tested.** 60 engine tests (including a regression of the original dry run, which the engine shows was
  arithmetically wrong), 20 plugin eval cases for routing and engine use, CI.

18 skills · 14 agents · 1 engine. All client facts come from the customer's RFP; all numbers come from code.

---

## Table of Contents

1. [Installation](#installation)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Engagement Lifecycle](#engagement-lifecycle)
5. [Engagement Workspace](#engagement-workspace)
6. [The Calculation Engine (sier)](#the-calculation-engine-sier)
7. [Agent Teams](#agent-teams)
8. [Skills Reference](#skills-reference)
9. [NotebookLM Integration](#notebooklm-integration)
10. [Grounding Rules](#grounding-rules)
11. [Workflow Examples](#workflow-examples)
12. [Output Formats](#output-formats)
13. [Testing](#testing)
14. [Supported Engagement Types](#supported-engagement-types)
15. [Tips & Best Practices](#tips--best-practices)

---

## Installation

1. Open Claude Desktop → **Settings** → **Capabilities**
2. Click **Install Plugin** and select the `it-consulting-expert.plugin` file
3. The 18 skills and 14 agents will appear in your skill list

To verify installation, ask Claude: "List my skills" — you should see all 18 skills prefixed with `it-consulting-expert:`.

---

## Prerequisites

**Required:**

- **Claude Desktop** with Cowork mode enabled
- **NotebookLM skill** installed (either `notebooklm` API skill or `notebooklm-web` browser skill) — this plugin depends on NotebookLM for RFP data extraction
- Customer RFP/RFQ document uploaded to a Google NotebookLM notebook

- **Python 3.7+** (`python3`) for the `sier` calculation engine — standard library only, nothing to install. macOS and the Cowork VM already have it.

**Recommended:**

- **docx skill** — most deliverables output as Word documents
- **pptx skill** — the proposal-presentation skill generates PowerPoint decks
- **xlsx skill** — Excel exports of the estimate and cost (they mirror engine output)
- **drawio skill** — architecture diagrams and 体制図

---

## Quick Start

**Step 1 — Create the engagement**

> "新規案件を始めます。ABC製造のCRMクラウド移行です。" / "Start a new engagement for ABC Manufacturing's CRM migration"

`engagement-init` creates the engagement folder (`./consulting/<client>-<project>/`).

**Step 2 — Extract the RFP once**

> "Set up a notebook for this RFP and run the full extraction"

`rfp-notebook` loads the RFP and attachments into NotebookLM, runs 26 extraction queries, and writes the
validated RFP Brief. If NotebookLM is unavailable it reads the files directly and says so.

**Step 3 — Either run the whole bid…**

> "Run the presale team on this RFP"

`presale-team` runs the agents wave by wave, stopping for your Go/No-Go decision and again if the price is
over budget, and finishes with the review board's verdict.

**…or one skill at a time**

> "Go/No-Go判断をお願いします" → `rfp-analysis` · "工数見積をして" → `effort-estimation` ·
> "費用を計算して" → `cost-estimation` · "提案書を作成して" → `create-proposal` · "提出前にレビューして" → `proposal-review`

At any point: **"案件の状況は？" / "where are we on this bid?"** → `sier status` shows what exists and what's next.

---

## Engagement Lifecycle

```
┌──────────────────────────────────────────────────────────────────────────┐
│  FOUNDATION    engagement-init → rfp-notebook (the RFP Brief)            │
├───────────┬──────────────────┬─────────────────────┬─────────────────────┤
│ PRE-      │ PROPOSAL         │ EXECUTION           │ POST-DELIVERY       │
│ PROPOSAL  │                  │                     │                     │
│ rfp-      │ technical-       │ progress-report     │ maintenance-        │
│ analysis  │   solution       │ change-request      │   proposal          │
│           │ effort-estimation│ vendor-management   │ lessons-learned ─┐  │
│           │ team-composition │                     │  (calibrates the │  │
│           │ cost-estimation  │                     │   next estimate) │  │
│           │ project-delivery │                     │                  │  │
│           │ create-proposal  │                     │                  │  │
│           │ proposal-/design-│                     │                  │  │
│           │   presentation   │                     │                  │  │
├───────────┴──────────────────┴─────────────────────┴──────────────────┼──┤
│  ORCHESTRATION   presale-team — runs the proposal phase with agents   │  │
│  QUALITY GATE    proposal-review — independent review agents + verify │  │
│  ENGINE          sier — every number, every skill  ◀──────────────────┘  │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Engagement Workspace

Every skill and agent reads and writes one folder per engagement — the files are how they hand work to
each other. Full contract: `plugins/it-consulting-expert/shared/engagement-workspace.md`.

```
consulting/
├── _firm/                     rate-card.json · calibration.json  (shared across engagements)
└── abc製造-crmクラウド移行/
    ├── engagement.json        client, notebook, deadlines, contract baseline
    ├── 00-rfp-brief.json/.md  the RFP, extracted once, cited  (rfp-notebook)
    ├── 01-go-nogo.json/.md    sier score                      (rfp-analysis)
    ├── 02-architecture.md                                     (technical-solution)
    ├── 03-estimate.json/.md   sier estimate                   (effort-estimation)
    ├── 04-team.json/.md                                       (team-composition)
    ├── 05-cost.json/.md       sier cost                       (cost-estimation)
    ├── 06-delivery-plan.md                                    (project-delivery)
    ├── inputs/                the inputs behind every computed file
    ├── artifacts/             proposal.docx, decks, xlsx — what the client sees
    ├── progress/              EVM and change-request reports
    └── _state/                runs/ (audit trail) · derived/ · review/ · cr-ledger.json
```

Location: `$SIER_HOME` if set, otherwise `./consulting` under the current folder (in Cowork, the connected
folder; in Claude Code, the project).

---

## The Calculation Engine (sier)

`plugins/it-consulting-expert/sier/` — Python, standard library only. Skills call it as
`python3 "${CLAUDE_PLUGIN_ROOT}/sier" <command>`; you can run it yourself the same way.

| Command | Computes |
|---|---|
| `init`, `status` | Create an engagement; pipeline, deadlines and next step |
| `brief validate / render / gaps` | Schema-check the RFP Brief; render it; list gaps blocking a skill |
| `score` | Go/No-Go against the canonical rubric, with the mandatory-qualification gate |
| `estimate` | WBS or function points, PM overhead, adjustment factors, three-point range, recommended 人月, traceability |
| `cost` | Labor and non-labor, management fee, risk premium, 税抜/税込, margin, budget fit, team-vs-estimate reconciliation (total and per role), payment schedule, TCO |
| `evm` | SPI, CPI, EAC (three forecasts), ETC, VAC, TCPI with RAG status |
| `sla` | Allowed downtime per tier and window, maintenance fee, multi-year totals, service credits |
| `cr add / report` | Change ledger: cumulative deviation gates, approval authority |
| `calibrate`, `ratecard` | Firm-wide calibration from closed projects; the firm rate card |
| `derive run / list` | Run a generated analysis script under guardrails (Tier 2) |
| `verify` | Recompute every artifact from its inputs and cross-check estimate ↔ team ↔ cost ↔ budget |

Every policy number — rubric weights, phase ranges, factor bounds, fees, premiums, EVM thresholds, CR gates,
SLA windows — lives in one file, `shared/policy.json`. Change it there and every calculation, test and
document follows. Command reference: `shared/engine.md`. When to write code and the rules for it:
`shared/harness.md`.

---

## Agent Teams

**Presale team** (`presale-team` skill — you stay in the loop as the bid manager's audience):

| Wave | Agent | Produces |
|---|---|---|
| 0 | `presale-rfp-analyst` | RFP Brief |
| — | *Gate A: your Go/No-Go decision* | |
| 1 | `presale-architect` (opus) | `02-architecture.md` |
| 2 | `presale-estimator` ∥ `presale-writer` (draft) | `03-estimate`, proposal draft |
| 3 | `presale-staffing` | `04-team`, `06-delivery-plan` |
| 4 | `presale-cost` | `05-cost` |
| — | *Gate B: your decision if over budget* | |
| 5 | `presale-writer` (final, opus) | `artifacts/proposal.docx`, compliance matrix |
| 6 | review board, in parallel | `_state/review/*.md` + consensus |

**Review board** (`proposal-review` skill): `review-business`, `review-architect`, `review-qcd`,
`review-risk`, `review-client`, `review-delivery`, plus optional `review-security` and `review-legal-ja`.
Each runs in its own context, read-only, and never sees another reviewer's report; conflicts are mediated
only after all have reported.

---

## Skills Reference

### Foundation Layer

#### `engagement-init` — Engagement Workspace (案件ワークスペース) ⭐ Start here

**Purpose:** Create or resume the engagement folder every other skill uses; record deadlines and the
post-award baseline; set up the firm rate card.

**Trigger phrases:** "New engagement", "新規案件", "案件フォルダを作成", "engagement status", "案件の状況",
"what's next on this bid", "提出期限を設定", "ベースライン設定"

---


#### `rfp-notebook` — RFP Extraction (RFPノートブック管理)

**Purpose:** The only skill that extracts from the RFP. Loads the RFP and attachments into NotebookLM, runs
26 standard extraction queries, and writes the **RFP Brief** — `00-rfp-brief.json`, validated by
`sier brief validate`, rendered to Markdown by `sier brief render`.

**Trigger phrases:** "Set up a notebook for this RFP", "RFPのノートブックを作成", "Extract requirements",
"要件を抽出", "Add amendment to notebook", "追加資料をノートブックに追加", "RFPブリーフィング作成"

**What it produces:** requirements with stable ids (`FR-`, `NFR-`, `INT-`), every fact labelled and cited,
the gaps list (questions for the client, each naming the skills it blocks), and amendment impact reports.
If NotebookLM is unreachable it reads the files directly and records `source_tier: 3`. When sources change,
`sier status` marks the Brief stale for every skill until it is regenerated.

---

### Pre-Proposal Phase

#### `rfp-analysis` — Go/No-Go Assessment (案件評価)

**Purpose:** Evaluate whether an RFP is worth pursuing before investing proposal effort.

**Trigger phrases:**
- "Analyze this RFP", "Should we bid on this?", "案件評価", "Go/No-Go判断"
- "Evaluate this opportunity", "Is this deal worth pursuing?"
- "提案可否判断", "Bid/no-bid decision"

**What it produces:**
- 6-dimension weighted score (Strategic Fit 15%, Capability Match 25%, Win Probability 25%, Profitability 15%, Delivery Risk 10%, Resource Availability 10%)
- Mandatory qualification pass/fail check
- Red flag checklist (10 items)
- Go/No-Go recommendation with thresholds (≥4.0 Strong GO → <2.0 Definite NO-GO)
- Polite decline template in Japanese keigo (if NO-GO)

**Example:**
> "I just received an RFP from Mitsubishi UFJ for a payment system migration. The notebook is set up. Should we bid?"

---

### Proposal Phase

#### `create-proposal` — Proposal Generator (提案書作成)

**Purpose:** Generate a complete consulting proposal grounded in the client's RFP.

**Trigger phrases:**
- "Create a proposal", "提案書を作成", "Draft a quotation"
- "Prepare an RFP response", "Make a bid"

**What it produces:**
- 12-section proposal document following Japanese SIer conventions
- Compliance Matrix (RFP対応表) tracing every requirement to proposal sections
- [RFP] / [Proposed] / [RFP+] labeling for full traceability
- Output as .docx

**How it works:** Writes each section from its workspace file (architecture, estimate, team, cost, delivery
plan), copies engine tables verbatim, and checks that the compliance matrix covers every requirement id in
the Brief. It no longer re-extracts the RFP. For the whole bid end to end, use `presale-team`.

**Example:**
> "Create a proposal for the RFP in my 'NTT Data Cloud Migration' notebook"

---

#### `team-composition` — Team Structure (体制図)

**Purpose:** Design project team structures with roles, seniority mix, and allocation.

**Trigger phrases:**
- "Propose a team", "体制図を作成", "Staffing plan"
- "What team do I need?", "How many developers?"

**What it produces:**
- Organization chart with 8 core roles (PM, Architect, SE, PG, etc.) with Japanese titles
- Seniority mix ratios by project scale
- Allocation table (人月) per phase
- RFP Source column tracing team requirements back to client document

**Example:**
> "What team do I need for a 50人月 web application project with offshore development?"

---

#### `effort-estimation` — Effort Estimation (工数見積)

**Purpose:** Produce WBS-based or function-point effort estimates.

**Trigger phrases:**
- "Estimate effort", "WBS", "工数見積", "Man-month estimate"
- "How long will this take?", "Function point analysis"

**What it produces:**
- WBS breakdown across 7 SIer phases (要件定義 → 基本設計 → 詳細設計 → 製造 → 結合テスト → 総合テスト → 移行)
- Phase distribution percentages by project type
- Risk-adjusted range: Optimistic (0.8x), Most Likely (1.0x), Pessimistic (1.5x), Recommended P75 (1.2x)
- Adjustment factors table (complexity, team experience, technology maturity)
- Function Point method support (EI/EO/EQ/ILF/EIF)

**Example:**
> "Estimate the effort for this RFP. Use function point analysis for the early-stage estimate, then WBS for detailed breakdown."

---

#### `cost-estimation` — Cost Estimation (費用見積)

**Purpose:** Create cost breakdowns, pricing models, and budget fit analysis.

**Trigger phrases:**
- "Estimate cost", "費用見積", "Budget", "Rate card"
- "How much will this cost?", "TCO analysis"

**What it produces:**
- Budget fit check (total vs. RFP ceiling)
- Cost breakdown by category (labor, infrastructure, licenses, travel)
- Pricing model options: Fixed Price, T&M, Hybrid
- Payment schedule options
- Japanese market rate cards by role × seniority (JPY)

**Example:**
> "Create a cost estimate for the proposed team. The client's budget ceiling is ¥80M. Use fixed price with milestone-based payments."

---

#### `technical-solution` — Technical Solution Design (技術提案)

**Purpose:** Design system architecture and recommend technology stacks.

**Trigger phrases:**
- "Design a solution", "技術提案", "Architecture proposal"
- "Technology selection", "System design for proposal"

**What it produces:**
- C4-model architecture views (Context, Container, Component)
- Technology decision matrix with RFP Requirement column
- Cloud platform comparison (AWS/Azure/GCP for Japan market)
- NFR compliance mapping (performance, security, availability, scalability)
- Common stack combinations by project type

**Example:**
> "Design the technical architecture for this cloud migration project. The client requires AWS and has strict data residency requirements in Japan."

---

#### `project-delivery` — Project Delivery Plan (プロジェクト計画)

**Purpose:** Define methodology, governance, quality assurance, and communication plans.

**Trigger phrases:**
- "Project plan", "Delivery methodology", "品質管理計画"
- "How to deliver this project", "Governance structure"

**What it produces:**
- Methodology selection (Waterfall/Agile/Hybrid) based on RFP preference
- Phase gate checklists (5 transitions: 要件定義→基本設計→...→移行)
- Governance meeting cadence with RFP Requirement traceability
- Quality metrics: SPI/CPI targets, code quality, testing metrics
- Defect severity classification (S1-S4 with Japanese names and fix SLAs)
- Change management and communication plans

**Example:**
> "Create a project delivery plan. The client prefers waterfall with phase gate reviews. Total duration is 12 months."

---

#### `proposal-presentation` — Presentation Materials (提案プレゼン)

**Purpose:** Generate slide deck and Q&A preparation for proposal defense meetings.

**Trigger phrases:**
- "Create a presentation", "提案プレゼン資料を作成", "Pitch deck"
- "Prepare for the proposal defense", "プレゼン準備"

**What it produces:**
- 15-slide deck optimized for 20-minute Japanese enterprise presentations
- Design guidelines (white background, Meiryo font, formal keigo)
- Q&A preparation document with 4 question categories (technical, commercial, delivery, competitive)
- 30-second and 2-minute answer formats for each anticipated question
- Output as .pptx

**Important:** Run this AFTER `create-proposal` — it converts the full proposal into a focused presentation.

**Example:**
> "Create a 20-minute presentation for next Tuesday's 提案説明会. The audience is CIO plus 3 department heads."

---

#### `design-presentation` — Visual Presentation via Claude Design (Claude Designプレゼン)

**Purpose:** Create visually polished presentations using Claude Design with Japanese enterprise design conventions. Complements `proposal-presentation` by adding visual polish.

**Trigger phrases:**
- "Design the presentation in Claude Design", "Claude Designでプレゼン作成"
- "Make the presentation look professional", "ビジュアルプレゼン"
- "Polish the proposal deck", "デザインプレゼン"

**What it produces:**
- Self-contained HTML slide deck (1280×720px, 16:9) with inline SVG icons and charts
- Design system setup: color palettes by client industry, Japanese typography, layout grid
- 7 slide templates: Title, Section Divider, Content, Comparison, Architecture Diagram, Timeline/Gantt, Team Org Chart, Cost Summary
- Import into Claude Design via `import-claude-design-from-url` for interactive refinement
- Export to PowerPoint, PDF, or deploy to Vercel

**Workflow:** Run `proposal-presentation` first for content → then `design-presentation` for visual polish → import to Claude Design → refine interactively → export as .pptx for client submission.

**Example:**
> "Take the proposal presentation content and design it in Claude Design. The client is in finance — use the conservative color palette."

---

#### `presale-team` — Presale Agent Team (提案チーム) ⭐ Orchestrator

**Purpose:** Run the proposal phase end to end with specialist agents, wave by wave, with the engine
checking every wave and two human gates (Go/No-Go; over budget).

**Trigger phrases:** "Run the presale team", "提案チームで進めて", "提案書一式を作成", "end-to-end bid",
"rerun the bid after the amendment"

---

### Execution Phase

#### `progress-report` — Progress Reports (進捗報告書)

**Purpose:** Generate standardized weekly and monthly status reports.

**Trigger phrases:**
- "Create a status report", "週次報告", "進捗報告書を作成"
- "Monthly report", "EVM report", "Project status update"

**What it produces:**
- Traffic light dashboard (Schedule/Quality/Cost/Risk/Scope) with trend arrows
- EVM metrics: SPI, CPI, EAC, ETC with interpretation
- Accomplishments / Plans / Issues / Risks / Decisions sections
- Monthly additions: budget tracking, defect trends, resource utilization, milestone status
- Status color decision guide with specific thresholds

**Example:**
> "Generate the weekly status report for the week ending June 20. Schedule is Yellow — we're 3 days behind on 詳細設計 but have a recovery plan."

---

#### `change-request` — Change Management (変更管理)

**Purpose:** Create formal scope change requests with impact analysis and cumulative tracking.

**Trigger phrases:**
- "Create a change request", "変更管理", "スコープ変更", "CR作成"
- "Impact analysis for a change", "変更影響分析"

**What it produces:**
- 5-dimension impact analysis (Schedule, Cost, Quality, Scope, Risk)
- Options analysis table (2-3 alternatives with recommendation)
- Approval workflow with authority thresholds (PM < ¥1M, Director ¥1M-5M, Executive > ¥5M)
- Cumulative change tracker against original RFP baseline
- Warning thresholds (🟡 >10% deviation, 🔴 >20% triggers contract amendment discussion)
- Communication templates in Japanese keigo

**Example:**
> "The client wants to add a mobile app to the scope. Create a CR with impact analysis. The original estimate was 40人月."

---

#### `vendor-management` — Vendor Management (協力会社管理)

**Purpose:** Structure and govern subcontractor and offshore partner relationships.

**Trigger phrases:**
- "Manage subcontractors", "協力会社管理", "RACI matrix"
- "Multi-vendor org chart", "Offshore management", "Partner selection"

**What it produces:**
- Multi-company organization chart with 一窓口 (single contact point) principle
- RACI matrix across all companies for key activities
- Vendor selection criteria matrix (6 dimensions, weighted scoring)
- Governance framework: meeting cadence, quality gates, escalation paths
- Monthly vendor scorecard with KPI targets
- Offshore-specific management: Bridge SE responsibilities, time zone overlap, communication protocols
- Onboarding and exit checklists

**Example:**
> "We're using an offshore team in Vietnam for development and a local partner for infrastructure. Create the governance structure and RACI."

---

### Post-Delivery Phase

#### `maintenance-proposal` — Maintenance Proposal (保守運用提案)

**Purpose:** Create post-delivery maintenance and support contract proposals.

**Trigger phrases:**
- "Maintenance proposal", "保守運用提案", "SLA definition"
- "Support contract", "Post-go-live support plan"

**What it produces:**
- 5-category service catalog (Corrective, Adaptive, Preventive, Perfective, Operations Support)
- SLA definitions: 4 severity levels (S1 Critical → S4 Minor) with response/resolution targets
- Support team structure with allocation (人月)
- 3 pricing models: Fixed Monthly, Tiered Plans (Bronze/Silver/Gold), Incident-Based
- Availability SLA tiers (99.5% / 99.9% / 99.95%)
- Transition plan from project team to maintenance team
- Pricing guideline: annual maintenance = 15-20% of original project cost

**Example:**
> "Create a maintenance proposal for the system we just delivered. The client wants 24/7 support with 99.9% availability. Propose a 3-year contract."

---

#### `lessons-learned` — Lessons Learned (案件振り返り)

**Purpose:** Conduct structured post-project reviews and capture organizational learnings.

**Trigger phrases:**
- "Lessons learned", "案件振り返り", "Project retrospective"
- "KPT analysis", "Post-mortem", "Project close-out report"

**What it produces:**
- Planned vs. actual analysis across schedule, effort, cost, and quality
- Profitability analysis (planned vs. actual margin)
- Defect origin analysis (where injected vs. where detected)
- KPT framework (Keep/Problem/Try) categorized by 10 themes
- Risk register review (did identified risks materialize? what was missed?)
- Estimation accuracy assessment with calibration factors for future projects
- Action items with owners and deadlines

**Example:**
> "The project is complete. Run a full retrospective. Original estimate was 45人月 over 9 months. Actual was 58人月 over 11 months. Let's understand why."

---

### Cross-Cutting Quality Gate

#### `proposal-review` — Multi-Perspective Review Board (多角的レビューボード)

**Purpose:** Independent review by specialist agents before client submission, then structured debate and
a consensus verdict.

**Trigger phrases:** "Review the proposal", "提案レビュー", "多角的レビュー", "Red team the proposal",
"提出前最終確認", "品質ゲートレビュー"

**How it works:**
1. **`sier verify`** — recompute every number from its inputs; cross-check estimate ↔ team ↔ cost ↔ budget.
2. **Independent reviews** — six reviewer agents (plus optional Security and Legal-Japan) dispatched in
   parallel, each in its own context, read-only, never seeing another's report.
3. **Conflict detection and structured debate** — in the main conversation, after all have reported.
4. **Consensus report** — scorecard, must-fix items, debate resolutions, strengths to preserve.

**Verdict thresholds:** ✅ READY (≥4.0) | ⚠️ CONDITIONAL (3.0–3.9) | ❌ NOT READY (<3.0). Revisions re-run only
the affected reviewers.

---

## NotebookLM Integration

### How It Works

1. **Extract once.** `rfp-notebook` queries NotebookLM (`notebooklm ask "…" --json --notebook <id>`) and
   writes every answer into the RFP Brief with its citation.
2. **Read the Brief.** Every other skill starts from `00-rfp-brief.json`.
3. **Ask only for gaps.** `sier brief gaps --for <skill>` lists what blocks a skill; it queries NotebookLM
   only for those, then writes the answers back into the Brief.
4. **Label everything** — `[RFP]`, `[Proposed]`, `[RFP+]` — with citations for anything labelled RFP.

Always pass `--notebook <id>` — never rely on `notebooklm use`, whose global context concurrent agents
overwrite. Full rules and the fallback ladder: `shared/notebooklm-contract.md`.

### Setup

Before using any skill, ensure:

1. The RFP/RFQ document is uploaded to a NotebookLM notebook
2. The source status is "ready" (processing complete)
3. Tell Claude which notebook to use: *"Use the notebook called 'RFP - Client Name'"*

### Supported Source Types

NotebookLM accepts: PDF, Word (.docx), Google Docs, web URLs, text files, Markdown, audio, video, and images. You can add multiple sources per notebook — the main RFP plus appendices, amendments, Q&A responses, etc.

### Citation Format

The `--json` flag returns traceable citations:

```json
{
  "answer": "The client requires 99.9% uptime [1] and response time under 2 seconds [2]",
  "references": [
    {"citation_number": 1, "cited_text": "System availability must be 99.9%..."},
    {"citation_number": 2, "cited_text": "All API responses within 2 seconds..."}
  ]
}
```

---

## Grounding Rules

These rules apply across ALL skills to prevent hallucination:

### Labels

Every piece of information in the output must be labeled:

| Label | Meaning | Example |
|-------|---------|---------|
| `[RFP]` | Directly from the client's document | "99.9% availability [RFP]" |
| `[Proposed]` | Our recommendation, not in the RFP | "We propose Redis for caching [Proposed]" |
| `[RFP+]` | Extends a client requirement | "Client requires HA [RFP]; we add multi-AZ [RFP+]" |

### MUST DO

1. Read the RFP Brief before writing any section; query NotebookLM only for gaps it records
2. Use `--json` flag on all queries to get traceable citations
3. Attribute all client-specific facts to the source document
4. Mark assumptions explicitly: "Not specified in RFP — proposed based on industry practice"
5. Verify numbers — if the RFP states a budget, timeline, or metric, use that exact number
6. Never type a computed number — effort, cost, price, score and SLA figures come from `sier`

### MUST NOT

1. Do NOT invent client requirements
2. Do NOT assume technology preferences unless stated in the RFP
3. Do NOT fabricate evaluation criteria
4. Do NOT guess budget ranges
5. Do NOT hallucinate past project references

---

## Workflow Examples

### Example 1: Complete Proposal Cycle (End-to-End)

```
You:  "I received an RFP from Sumitomo Mitsui for a core banking API platform. Here are the files."

Step 0 → "Start a new engagement"            → engagement-init creates the folder
Step 1 → "Run the presale team on this RFP"  → presale-team:
           W0 rfp-analyst writes the RFP Brief
           Gate A: Go/No-Go with you (sier score: 4.2 — STRONG_GO)
           W1 architect · W2 estimator ∥ writer draft · W3 staffing · W4 cost
           Gate B: price over budget? you choose between priced options
           W5 writer completes proposal.docx · W6 review board + sier verify → ✅ READY
Step 2 → "Create the presentation deck"      → proposal-presentation / design-presentation
Step 3 → [Win] "Set the contract baseline"   → engagement-init records baseline from 03/05
Step 4 → "Generate this week's status report" → progress-report (EVM via sier evm)
Step 5 → "Client wants real-time notifications — create a CR" → change-request (sier cr)
Step 6 → "Maintenance proposal, 24/7"         → maintenance-proposal (sier sla)
Step 7 → "Run a retrospective"                → lessons-learned → sier calibrate add
           (the next CRM estimate shows how this one ran against its estimate)
```

### Example 2: Quick Estimation Only

```
You:  "I need a rough effort estimate for this RFP. Use function point analysis."

      → effort-estimation runs FP analysis, produces 人月 range with risk adjustment
```

### Example 3: Mid-Project Vendor Setup

```
You:  "We just signed a subcontractor for offshore development in Vietnam.
       Set up the governance structure."

      → vendor-management produces org chart, RACI, quality gates, and Bridge SE plan
```

### Example 4: Responding to Scope Creep

```
You:  "The client keeps asking for small changes without CRs.
       Show me the cumulative impact."

      → change-request produces cumulative change tracker showing total baseline deviation
```

---

## Output Formats

| Skill | Primary output |
|-------|----------------|
| engagement-init | `engagement.json`, workspace folders |
| rfp-notebook | `00-rfp-brief.json` (canonical) + `.md` (rendered) |
| rfp-analysis | `01-go-nogo.json/.md` (sier score) + assessment .docx |
| technical-solution | `02-architecture.md` + diagrams (.drawio/.png or mermaid) |
| effort-estimation | `03-estimate.json/.md` (sier estimate); optional .xlsx |
| team-composition | `04-team.json/.md` + 体制図 |
| cost-estimation | `05-cost.json/.md` (sier cost); optional .xlsx |
| project-delivery | `06-delivery-plan.md` |
| create-proposal | `artifacts/proposal.docx` + compliance matrix |
| presale-team | everything above, wave by wave |
| proposal-presentation | .pptx + Q&A prep |
| design-presentation | Claude Design canvas or HTML → .pptx |
| progress-report | weekly/monthly .docx; `progress/evm-<date>.*` (sier evm) |
| change-request | CR .docx; `progress/cr-report.*` (sier cr) |
| vendor-management | governance plan + RACI .docx |
| maintenance-proposal | proposal .docx; `07-sla.json/.md` (sier sla) |
| lessons-learned | close-out .docx; calibration record (sier calibrate) |
| proposal-review | `_state/review/*.md`, `consensus.md`, review .docx |

---

## Testing

```bash
python3 -m unittest discover -s tests -t tests          # 60 engine tests, stdlib only
claude plugin validate plugins/it-consulting-expert --strict
cd plugins/it-consulting-expert && claude plugin eval . --tag smoke --runs 1 --ablation none \
    --allow-tools Bash Write Edit                          # see evals/README.md
```

`tests/fixtures/abc-manufacturing/` turns the original dry run into engine inputs and pins what the engine
found: its adjustment factors multiply to 1.20, not the 1.07 it printed; computed correctly the estimate is
175.79 人月; priced to policy the bid is ¥233.25M, over the ¥200M budget it claimed to fit.

---

## Supported Engagement Types

**Software Development**
Custom applications, web/mobile, API platforms, microservices, SaaS products

**Infrastructure**
Cloud migration (AWS/Azure/GCP), DevOps pipeline, networking, security hardening, disaster recovery

**Digital Transformation**
Legacy modernization, process automation, AI/ML integration, data platform, IoT

**All Client Sizes**
Enterprise (Fortune 500, 大企業), mid-market (中堅企業), and startup engagements. Estimation heuristics and team sizing adjust automatically by project scale.

---

## Tips & Best Practices

**Start with engagement-init, then rfp-notebook.** Before any analysis or proposal work, run the full extraction. The structured RFP Brief it produces is consumed by every other skill, ensuring consistency and preventing each skill from independently re-querying NotebookLM.

**Then run rfp-analysis.** Even when you're confident about a bid, the structured scoring often reveals risks you'd otherwise miss. A 15-minute Go/No-Go saves weeks of wasted proposal effort on bad deals.

**Let presale-team orchestrate.** For a whole bid, run presale-team; it calls the skills in dependency order, checks each wave with the engine and stops for your decisions. Run individual skills to iterate on one artifact.

**Upload all RFP attachments.** Add the main RFP document plus all appendices, Q&A responses, amendments, and clarification documents to the same NotebookLM notebook. More source material = more accurate extraction.

**Use the Compliance Matrix.** The create-proposal skill generates an RFP対応表 (compliance matrix) that maps every client requirement to your proposal section. Japanese evaluators check this systematically — a missing entry is a lost point.

**Track changes cumulatively.** Individual CRs look harmless. The change-request skill's cumulative tracker reveals scope creep that's invisible one CR at a time. Show clients the dashboard regularly.

**Run lessons-learned within 2 weeks of go-live.** It records estimate vs actual with `sier calibrate`, and every later estimate of the same project type shows that track record.

**Replace the benchmark rate card.** `sier ratecard init` writes market midpoints so you can start; the engine warns on every price until you put in your firm's real rates.

**Run `sier verify` before submission.** It is the one check that proves the numbers in the documents are the numbers the engine computed.

**Language defaults to Japanese** for all formal documents (keigo style). Add "in English" to your prompt to switch. The plugin supports bilingual output for international engagements.

---

## Version

- Plugin version: 2.0.0 (see `CHANGELOG.md`)
- Skills: 18 · Agents: 14 · Engine: sier
- Author: Neo
