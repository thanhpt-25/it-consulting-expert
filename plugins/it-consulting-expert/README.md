# IT Consulting Expert Plugin

Full-lifecycle IT consulting expert for Japanese SIer (System Integrator) engagements. This plugin covers every phase of a consulting engagement — from initial RFP assessment through proposal creation, project execution, and post-delivery — following Japanese enterprise conventions with bilingual (Japanese/English) support.

All skills integrate with **Google NotebookLM** as the single source of truth. Customer RFP/RFQ documents are uploaded to NotebookLM, and every skill queries it before generating content. This prevents hallucination and ensures all outputs are grounded in actual client requirements.

---

## Table of Contents

1. [Installation](#installation)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Engagement Lifecycle](#engagement-lifecycle)
5. [Skills Reference](#skills-reference)
6. [NotebookLM Integration](#notebooklm-integration)
7. [Grounding Rules](#grounding-rules)
8. [Workflow Examples](#workflow-examples)
9. [Output Formats](#output-formats)
10. [Supported Engagement Types](#supported-engagement-types)
11. [Tips & Best Practices](#tips--best-practices)

---

## Installation

1. Open Claude Desktop → **Settings** → **Capabilities**
2. Click **Install Plugin** and select the `it-consulting-expert.plugin` file
3. The 13 skills will appear in your skill list

To verify installation, ask Claude: "List my skills" — you should see all 13 skills prefixed with `it-consulting-expert:`.

---

## Prerequisites

**Required:**

- **Claude Desktop** with Cowork mode enabled
- **NotebookLM skill** installed (either `notebooklm` API skill or `notebooklm-web` browser skill) — this plugin depends on NotebookLM for RFP data extraction
- Customer RFP/RFQ document uploaded to a Google NotebookLM notebook

**Recommended:**

- **docx skill** — most deliverables output as Word documents
- **pptx skill** — the proposal-presentation skill generates PowerPoint decks
- **xlsx skill** — useful for detailed estimation spreadsheets

---

## Quick Start

The fastest path from "we received an RFP" to "proposal submitted":

**Step 1 — Upload the RFP to NotebookLM**

Tell Claude: *"Create a NotebookLM notebook for [Client Name]'s RFP and add this document"*

Or upload manually at [notebooklm.google.com](https://notebooklm.google.com) and tell Claude which notebook to use.

**Step 2 — Assess the opportunity**

> "Analyze this RFP and give me a Go/No-Go recommendation"

This triggers the `rfp-analysis` skill, which scores the deal across 6 dimensions and flags red flags before you invest proposal effort.

**Step 3 — Generate the proposal**

> "Create a proposal for this RFP"

This triggers `create-proposal`, which orchestrates queries to NotebookLM, extracts all requirements, and generates a full proposal document. It will call the other proposal-phase skills (team, effort, cost, technical, delivery) as needed.

**Step 4 — Prepare the presentation**

> "Create a presentation deck for this proposal"

Generates a 15-slide pitch deck and Q&A preparation document for the proposal defense meeting.

---

## Engagement Lifecycle

The 15 skills map to four phases of a consulting engagement, plus a cross-cutting quality gate. Use them in order, or independently as needed.

```
┌─────────────────────────────────────────────────────────────────┐
│                    ENGAGEMENT LIFECYCLE                         │
├──────────┬──────────────┬───────────────┬──────────────────────┤
│  PRE-    │   PROPOSAL   │  EXECUTION    │  POST-DELIVERY       │
│  PROPOSAL│   PHASE      │  PHASE        │  PHASE               │
├──────────┼──────────────┼───────────────┼──────────────────────┤
│          │              │               │                      │
│ rfp-     │ create-      │ progress-     │ maintenance-         │
│ analysis │ proposal     │ report        │ proposal             │
│          │              │               │                      │
│          │ team-        │ change-       │ lessons-             │
│          │ composition  │ request       │ learned              │
│          │              │               │                      │
│          │ effort-      │ vendor-       │                      │
│          │ estimation   │ management    │                      │
│          │              │               │                      │
│          │ cost-        │               │                      │
│          │ estimation   │               │                      │
│          │              │               │                      │
│          │ technical-   │               │                      │
│          │ solution     │               │                      │
│          │              │               │                      │
│          │ project-     │               │                      │
│          │ delivery     │               │                      │
│          │              │               │                      │
│          │ proposal-    │               │                      │
│          │ presentation │               │                      │
│          │              │               │                      │
│          │ design-      │               │                      │
│          │ presentation │               │                      │
│          │              │               │                      │
├──────────┴──────────────┴───────────────┴──────────────────────┤
│  CROSS-CUTTING QUALITY GATE                                    │
│  proposal-review — 6-persona AI review board with debate       │
└────────────────────────────────────────────────────────────────┘
```

---

## Skills Reference

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

#### `create-proposal` — Proposal Generator (提案書作成) ⭐ Orchestrator

**Purpose:** Generate a complete consulting proposal grounded in the client's RFP.

**Trigger phrases:**
- "Create a proposal", "提案書を作成", "Draft a quotation"
- "Prepare an RFP response", "Make a bid"

**What it produces:**
- 12-section proposal document following Japanese SIer conventions
- Compliance Matrix (RFP対応表) tracing every requirement to proposal sections
- [RFP] / [Proposed] / [RFP+] labeling for full traceability
- Output as .docx

**How it works:** This is the orchestrator skill. It runs 11 extraction queries against NotebookLM, then calls the other proposal-phase skills (team, effort, cost, technical, delivery) to build each section. You can run it standalone and it will produce everything, or run the component skills individually for focused work.

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

**Purpose:** Assemble an AI review board of 6 specialist personas that independently review all artifacts, debate conflicts, and produce a consensus assessment before client submission.

**Trigger phrases:**
- "Review the proposal", "提案レビュー", "Quality check the deliverables"
- "Review from multiple perspectives", "多角的レビュー", "Red team the proposal"
- "Final check before submission", "提出前最終確認", "品質ゲートレビュー"

**The 6 Reviewer Personas:**

| Persona | Japanese | Focus | Key Question |
|---------|----------|-------|-------------|
| Business Strategist | 事業戦略レビューア | ROI, margins, competitive positioning, account strategy | "Does winning this make us stronger?" |
| Technical Architect | 技術アーキテクトレビューア | Architecture soundness, technology choices, NFR coverage, feasibility | "Can we actually build this as specified?" |
| QCD Controller | 品質・コスト・納期レビューア | Estimation accuracy, cost balance, timeline feasibility, quality targets | "Will we deliver on time, on budget, at quality?" |
| Risk & Compliance Officer | リスク・コンプライアンスレビューア | RFP compliance, contractual risk, regulatory, assumptions | "What's the worst that can happen?" |
| Client Advocate | 顧客視点レビューア | Evaluation criteria alignment, communication quality, trust signals | "Would the client feel confident choosing us?" |
| Delivery PM | デリバリーPMレビューア | Team feasibility, methodology fit, vendor management, operational readiness | "Could I actually run this project from day one?" |

**How it works:**
1. **Independent Reviews** — Each persona reviews all artifacts alone (prevents groupthink)
2. **Conflict Detection** — Identifies where personas disagree (priority, feasibility, scope, risk tolerance)
3. **Structured Debate** — Conflicting personas present arguments with evidence, rebut, and a mediator synthesizes
4. **Consensus Report** — 6-dimension scorecard, must-fix items, debate resolutions, strengths to preserve

**Verdict thresholds:** ✅ READY (≥4.0) | ⚠️ CONDITIONAL (3.0–3.9) | ❌ NOT READY (<3.0)

**Supports revision tracking:** After fixing issues, re-run targeted review on changed artifacts only.

**Extensible:** Add specialized personas (Security Specialist, Industry Expert, Legal Counsel, UX Reviewer, Data/AI Specialist, Financial Controller) for domain-specific engagements.

**Example:**
> "Review all proposal artifacts before submission. We're bidding on a ¥200M financial system project with a tight timeline. I want the full review board with an extra Security Specialist persona."

---

## NotebookLM Integration

### How It Works

Every skill follows the same pattern:

1. **Step 0**: Query NotebookLM with targeted questions (`notebooklm ask "..." --json`)
2. **Extract**: Parse the JSON response, which includes cited text from the source document
3. **Ground**: Use cited information to populate proposal sections
4. **Label**: Mark every fact with its origin — `[RFP]`, `[Proposed]`, or `[RFP+]`

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

1. Query NotebookLM first before writing any section
2. Use `--json` flag on all queries to get traceable citations
3. Attribute all client-specific facts to the source document
4. Mark assumptions explicitly: "Not specified in RFP — proposed based on industry practice"
5. Verify numbers — if the RFP states a budget, timeline, or metric, use that exact number

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
You:  "I received an RFP from Sumitomo Mitsui for a core banking API platform.
       I've uploaded it to NotebookLM as 'RFP - SMBC API Platform'."

Step 1 → "Analyze this RFP and give me a Go/No-Go"
         → rfp-analysis produces: Score 4.2 — Strong GO

Step 2 → "Create the full proposal"
         → create-proposal orchestrates all sub-skills, outputs .docx

Step 3 → "Create the presentation deck for a 30-minute slot"
         → proposal-presentation outputs .pptx + Q&A prep doc

Step 4 → "Review everything before we submit"
         → proposal-review runs 6-persona review board, produces consensus report
         → Fix must-fix items → re-review changed sections → ✅ READY

Step 5 → [Win the bid, start the project]

Step 6 → "Generate this week's status report"
         → progress-report outputs weekly 進捗報告書

Step 7 → "The client wants to add real-time notifications. Create a CR."
         → change-request outputs CR document + updated cumulative tracker

Step 8 → [Project completes]

Step 9 → "Create a maintenance proposal for 24/7 support"
         → maintenance-proposal outputs SLA + pricing + transition plan

Step 10 → "Run a retrospective on this project"
         → lessons-learned outputs close-out report + KPT + action items
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

| Skill | Primary Output | Format |
|-------|---------------|--------|
| rfp-analysis | Go/No-Go assessment report | .docx |
| create-proposal | Full consulting proposal | .docx |
| team-composition | Organization chart + staffing plan | .docx |
| effort-estimation | WBS + effort breakdown | .docx |
| cost-estimation | Cost breakdown + pricing | .docx |
| technical-solution | Architecture document | .docx |
| project-delivery | Project plan + governance | .docx |
| proposal-presentation | Slide deck + Q&A prep | .pptx + .docx |
| design-presentation | Visual slides via Claude Design | .html → Claude Design → .pptx |
| progress-report | Weekly/monthly status report | .docx |
| change-request | CR document + cumulative tracker | .docx |
| vendor-management | Governance plan + RACI | .docx |
| maintenance-proposal | Support contract proposal + SLA | .docx |
| lessons-learned | Close-out report + KPT | .docx |
| proposal-review | Review report + scorecard + revision checklist | .docx |

All skills use the `docx` skill for Word output and the `pptx` skill for PowerPoint. Ensure these skills are installed.

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

**Start with rfp-analysis.** Even when you're confident about a bid, the structured scoring often reveals risks you'd otherwise miss. A 15-minute Go/No-Go saves weeks of wasted proposal effort on bad deals.

**Let create-proposal orchestrate.** Rather than running each skill separately, start with create-proposal. It queries NotebookLM comprehensively and calls the sub-skills in the right order. Run individual skills only when you need to iterate on a specific section.

**Upload all RFP attachments.** Add the main RFP document plus all appendices, Q&A responses, amendments, and clarification documents to the same NotebookLM notebook. More source material = more accurate extraction.

**Use the Compliance Matrix.** The create-proposal skill generates an RFP対応表 (compliance matrix) that maps every client requirement to your proposal section. Japanese evaluators check this systematically — a missing entry is a lost point.

**Track changes cumulatively.** Individual CRs look harmless. The change-request skill's cumulative tracker reveals scope creep that's invisible one CR at a time. Show clients the dashboard regularly.

**Run lessons-learned within 2 weeks of go-live.** Memories fade fast. The estimation accuracy data from retrospectives is gold — it calibrates your future effort-estimation results.

**Language defaults to Japanese** for all formal documents (keigo style). Add "in English" to your prompt to switch. The plugin supports bilingual output for international engagements.

---

## Version

- Plugin version: 1.2.0
- Skills: 15
- Author: Neo
