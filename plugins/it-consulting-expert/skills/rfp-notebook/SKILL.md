---
name: rfp-notebook
description: >
  Set up and manage NotebookLM notebooks for IT consulting engagements. Use this
  skill when the user asks to "set up a notebook for an RFP", "RFPのノートブックを
  作成", "upload RFP to NotebookLM", "RFP資料をアップロード", "extract requirements
  from the RFP", "要件を抽出", "create engagement notebook", "案件ノートブック作成",
  "add amendment to notebook", "追加資料をノートブックに追加", "which notebook has
  the RFP", "RFPはどのノートブックにありますか", "prepare notebook for proposal",
  "提案準備のノートブック設定", "run RFP extraction", "RFP分析を実行", "briefing
  from RFP", "RFPブリーフィング作成", or any request to create, manage, or query
  NotebookLM notebooks for consulting engagements. Also trigger for "notebooklm
  setup", "notebook管理", "source management", "ソース管理", and requests to
  produce a structured RFP brief from uploaded documents.
metadata:
  version: "0.1.0"
---

# RFP Notebook Manager (RFP ノートブック管理)

Automate the creation, source management, and structured extraction of RFP/RFQ content from NotebookLM — the "Step 0" that grounds every other skill in this plugin.

## Why This Matters

Every skill in the `it-consulting-expert` plugin depends on NotebookLM as the single source of truth. Before any proposal section can be written, the RFP must be uploaded, processed, and systematically queried. This skill automates that entire setup and extraction pipeline, producing a structured **RFP Brief** that all downstream skills consume.

Without this skill, each skill independently asks the user "which notebook?" and runs ad-hoc queries. With this skill, there's one canonical setup process and one structured output that feeds everything else.

```
RFP/RFQ Documents → rfp-notebook → Structured RFP Brief
                                         ↓
                    ┌────────────────────────────────────────┐
                    │ All other skills consume the brief:    │
                    │ rfp-analysis, create-proposal,         │
                    │ technical-solution, effort-estimation,  │
                    │ cost-estimation, team-composition,      │
                    │ project-delivery, proposal-review, ... │
                    └────────────────────────────────────────┘
```

## Workflow

### Step 1: Identify or Create the Engagement Notebook

Ask the user: "Do you already have a NotebookLM notebook for this engagement, or should I create one?"

**If existing:**

```bash
notebooklm list --json
```

Display notebooks and let the user select. Confirm the selection:

```bash
notebooklm use <notebook_id>
```

**If new:**

Ask for:
- Client name (顧客名)
- Project name (案件名)
- RFP reference number (if any)

Create with the naming convention:

```bash
notebooklm create "RFP - [Client Name] - [Project Name]" --json
```

**Naming Convention:**
| Pattern | Example | When |
|---------|---------|------|
| `RFP - [Client] - [Project]` | `RFP - NTT Data - 基幹系統刷新` | Standard engagement |
| `RFP - [Client] - [Project] - Amendment [N]` | `RFP - NTT Data - 基幹系統刷新 - Amendment 2` | When tracking amendment history separately |
| `RFQ - [Client] - [Project]` | `RFQ - MUFG - クラウド移行` | Quote request (simpler scope) |

Record the notebook ID for this engagement:

```
📒 Engagement Notebook Registry
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Client:      [Client Name]
Project:     [Project Name]
Notebook ID: [notebook_id]
Created:     [YYYY/MM/DD]
Sources:     [count] documents
Status:      Active / Archived
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 2: Upload and Process Sources

Guide the user to add all relevant documents:

**Primary RFP document:**
```bash
notebooklm source add ./[filename] -n <notebook_id> --json
```

**Additional sources (add all that apply):**
```bash
# Appendices
notebooklm source add ./appendix-a-technical-specs.pdf -n <notebook_id> --json

# Q&A clarifications
notebooklm source add ./rfp-qa-responses.pdf -n <notebook_id> --json

# Amendments
notebooklm source add ./amendment-1.pdf -n <notebook_id> --json

# Client website (for context)
notebooklm source add "https://client-company.co.jp/about" -n <notebook_id> --json

# Existing system documentation
notebooklm source add ./current-system-overview.pdf -n <notebook_id> --json
```

**Wait for processing:**
```bash
notebooklm source wait <source_id> -n <notebook_id> --timeout 600
```

**Verify all sources ready:**
```bash
notebooklm source list -n <notebook_id> --json
```

All sources must show `"status": "ready"` before proceeding. If any source fails:
- Check file format is supported (PDF, DOCX, TXT, MD, URL, Google Docs)
- Check file size limits
- Retry the upload

Display source summary:
```
📄 Sources Loaded
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# │ Source                        │ Status
──┼───────────────────────────────┼───────
1 │ RFP-2024-XXX.pdf              │ ✅ Ready
2 │ Appendix-A-Technical.pdf      │ ✅ Ready
3 │ QA-Responses-Round1.pdf       │ ✅ Ready
4 │ Amendment-1.pdf               │ ⏳ Processing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 3: Run Structured Extraction (RFP分析抽出)

Execute the standard extraction query set. This is the core value of this skill — a systematic, comprehensive extraction that no manual reading would match.

**Run ALL queries in sequence.** Each query uses `--json` to get cited answers.

#### 3.1 Project Overview (案件概要)

```bash
notebooklm ask "What is the project name, objective, and background? Why is the client undertaking this project now?" --json -n <notebook_id>
notebooklm ask "What is the project scope? What is explicitly in-scope and out-of-scope?" --json -n <notebook_id>
notebooklm ask "What are the key success criteria or KPIs the client defines for this project?" --json -n <notebook_id>
```

#### 3.2 Requirements (要件)

```bash
notebooklm ask "List all functional requirements mentioned in the RFP, organized by business area or module" --json -n <notebook_id>
notebooklm ask "List all non-functional requirements: performance targets, security requirements, availability SLA, scalability needs, and accessibility standards" --json -n <notebook_id>
notebooklm ask "What are the mandatory technology constraints, platform requirements, or integration standards?" --json -n <notebook_id>
notebooklm ask "What data migration or conversion requirements are specified?" --json -n <notebook_id>
```

#### 3.3 Timeline & Milestones (スケジュール)

```bash
notebooklm ask "What is the overall project timeline? Start date, end date, and any intermediate deadlines?" --json -n <notebook_id>
notebooklm ask "What are the key milestones, phase gates, or checkpoint dates the client expects?" --json -n <notebook_id>
notebooklm ask "What is the proposal submission deadline and format requirements?" --json -n <notebook_id>
```

#### 3.4 Budget & Commercial (予算・商務)

```bash
notebooklm ask "Is there a stated budget range, budget ceiling, or budget constraints?" --json -n <notebook_id>
notebooklm ask "What pricing model does the client prefer: fixed price, time and materials, or other?" --json -n <notebook_id>
notebooklm ask "What payment terms, invoicing schedule, or financial conditions are specified?" --json -n <notebook_id>
```

#### 3.5 Technical Environment (技術環境)

```bash
notebooklm ask "Describe the client's current IT systems, infrastructure, and technology stack mentioned in the document" --json -n <notebook_id>
notebooklm ask "What integrations with existing systems are required? List each system and the integration type" --json -n <notebook_id>
notebooklm ask "What security, compliance, or regulatory requirements are mentioned? Include industry-specific regulations" --json -n <notebook_id>
notebooklm ask "What are the hosting, deployment, or infrastructure requirements (on-premises, cloud, hybrid)?" --json -n <notebook_id>
```

#### 3.6 Team & Process (体制・プロセス)

```bash
notebooklm ask "What team structure, roles, or staffing requirements does the client specify or prefer?" --json -n <notebook_id>
notebooklm ask "Does the client prefer a specific development methodology (waterfall, agile, hybrid)? What governance is expected?" --json -n <notebook_id>
notebooklm ask "What reporting, communication, or meeting cadence does the client expect?" --json -n <notebook_id>
```

#### 3.7 Evaluation & Submission (評価・提出)

```bash
notebooklm ask "What evaluation criteria will the client use to assess proposals? List with weights if provided" --json -n <notebook_id>
notebooklm ask "What are the mandatory submission requirements: format, page count, sections, copies, delivery method?" --json -n <notebook_id>
notebooklm ask "Are there mandatory qualifications, certifications, or references required from the vendor?" --json -n <notebook_id>
```

#### 3.8 Risks & Constraints (リスク・制約)

```bash
notebooklm ask "What risks, constraints, or assumptions does the RFP mention or imply?" --json -n <notebook_id>
notebooklm ask "Are there penalty clauses, liquidated damages, or SLA breach consequences specified?" --json -n <notebook_id>
notebooklm ask "What are the contract terms for IP ownership, warranty, and liability?" --json -n <notebook_id>
```

### Step 4: Compile the Structured RFP Brief (RFPブリーフィング)

Compile all extraction results into a single structured document — the **RFP Brief**. This is the canonical reference that all other skills consume.

```markdown
# RFP Brief: [Client Name] - [Project Name]
# RFPブリーフィング

**Generated:** YYYY/MM/DD
**Notebook ID:** [notebook_id]
**Sources:** [N] documents
**Extraction Queries:** 26 standard queries executed

---

## 1. Project Overview (案件概要)

### 1.1 Background & Objectives [RFP]
[Compiled from 3.1 queries, with citations]

### 1.2 Scope [RFP]
**In-Scope:**
- [item] — [citation]

**Out-of-Scope:**
- [item] — [citation]

**Ambiguous (clarification recommended):**
- [item] — [why it's unclear]

### 1.3 Success Criteria [RFP]
[KPIs and acceptance criteria with citations]

---

## 2. Requirements Summary (要件サマリー)

### 2.1 Functional Requirements [RFP]
| # | Requirement | Priority | Source |
|---|------------|----------|--------|
| FR-001 | [description] | Must/Should/May | [citation] |

### 2.2 Non-Functional Requirements [RFP]
| Category | Target | Source |
|----------|--------|--------|
| Performance | [target] | [citation] |
| Availability | [target] | [citation] |
| Security | [standard] | [citation] |
| Scalability | [target] | [citation] |

### 2.3 Technical Constraints [RFP]
[Platform, technology, integration constraints]

### 2.4 Data Migration [RFP]
[Migration scope, volume, constraints]

---

## 3. Timeline & Milestones (スケジュール)

### 3.1 Key Dates [RFP]
| Milestone | Date | Source |
|-----------|------|--------|
| Proposal submission | YYYY/MM/DD | [citation] |
| Contract start | YYYY/MM/DD | [citation] |
| Go-live | YYYY/MM/DD | [citation] |

### 3.2 Phase Expectations [RFP]
[Client-specified phases or milestones]

---

## 4. Budget & Commercial (予算・商務)

### 4.1 Budget [RFP]
- Stated budget: [amount or "Not specified"]
- Pricing preference: [fixed/T&M/hybrid or "Not specified"]
- Payment terms: [terms or "Not specified"]

### 4.2 Financial Constraints [RFP]
[Any financial conditions, caps, or requirements]

---

## 5. Technical Environment (技術環境)

### 5.1 Current Systems [RFP]
[Existing IT landscape the solution must fit into]

### 5.2 Integration Requirements [RFP]
| System | Integration Type | Protocol | Source |
|--------|-----------------|----------|--------|
| [name] | [type] | [protocol] | [citation] |

### 5.3 Security & Compliance [RFP]
[Regulatory requirements, certifications, data handling]

### 5.4 Infrastructure [RFP]
[Hosting, deployment, environment requirements]

---

## 6. Team & Process (体制・プロセス)

### 6.1 Staffing Requirements [RFP]
[Client expectations for team structure]

### 6.2 Methodology Preference [RFP]
[Waterfall/Agile/Hybrid preference]

### 6.3 Governance [RFP]
[Reporting, meetings, communication expectations]

---

## 7. Evaluation & Submission (評価・提出)

### 7.1 Evaluation Criteria [RFP]
| Criterion | Weight | Source |
|-----------|--------|--------|
| [criterion] | [%] | [citation] |

### 7.2 Submission Requirements [RFP]
[Format, deadline, mandatory sections, delivery method]

### 7.3 Vendor Qualifications [RFP]
[Required certifications, references, experience]

---

## 8. Risks & Constraints (リスク・制約)

### 8.1 Identified Risks [RFP]
[Risks mentioned in the RFP]

### 8.2 Contractual Terms [RFP]
[Penalty clauses, IP, warranty, liability]

### 8.3 Assumptions [Proposed]
[Items not specified in RFP that we need to assume]

---

## 9. Gaps & Clarification Needed (不明点・要確認事項)

| # | Topic | Question | Priority |
|---|-------|----------|----------|
| Q-001 | [topic] | [question to ask client] | High/Medium/Low |

---

## 10. Downstream Skill Readiness (スキル連携準備)

| Skill | Key RFP Inputs Available | Gaps |
|-------|-------------------------|------|
| rfp-analysis | ✅ Evaluation criteria, budget, timeline | None |
| create-proposal | ✅ All sections covered | [any gaps] |
| technical-solution | ✅ Tech constraints, integrations, NFRs | [any gaps] |
| effort-estimation | ✅ Requirements list, timeline | [any gaps] |
| cost-estimation | ✅ Budget range, pricing preference | [any gaps] |
| team-composition | ✅ Staffing requirements, methodology | [any gaps] |
| project-delivery | ✅ Methodology, governance, milestones | [any gaps] |
```

### Step 5: Amendment & Update Management (追加資料管理)

When the client issues amendments, Q&A responses, or clarifications after initial setup:

**Add new sources:**
```bash
notebooklm source add ./amendment-2.pdf -n <notebook_id> --json
notebooklm source wait <source_id> -n <notebook_id> --timeout 600
```

**Run delta extraction — query only what the amendment affects:**
```bash
notebooklm ask "What changes does the latest amendment make to the original RFP requirements?" --json -n <notebook_id>
notebooklm ask "Does the amendment change the timeline, budget, or evaluation criteria?" --json -n <notebook_id>
notebooklm ask "Are there new requirements added or existing requirements removed by this amendment?" --json -n <notebook_id>
```

**Produce an Amendment Impact Report:**
```markdown
# Amendment Impact Report
**Amendment:** [Amendment N / Q&A Round N]
**Date Added:** YYYY/MM/DD

## Changes Detected
| Section | Original | Changed To | Impact |
|---------|----------|-----------|--------|
| [section] | [was] | [now] | High/Medium/Low |

## Affected Downstream Skills
- [skill name]: [what needs updating]

## Updated RFP Brief Sections
[List which sections of the RFP Brief were updated]
```

### Step 6: Multi-Engagement Management (複数案件管理)

For consultants handling multiple active engagements:

```bash
notebooklm list --json
```

Display an engagement dashboard:

```
📒 Active Engagement Notebooks
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  │ Client      │ Project          │ Sources │ Status
───┼─────────────┼──────────────────┼─────────┼────────
1  │ NTT Data    │ 基幹系統刷新     │ 5       │ Active
2  │ MUFG        │ クラウド移行     │ 3       │ Active
3  │ Toyota      │ DX推進基盤       │ 8       │ Brief Done
4  │ Sony        │ ECサイト構築     │ 2       │ Archived
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Switch engagement context:
```bash
notebooklm use <notebook_id>
```

### Step 7: Output

The primary output is the **Structured RFP Brief** (markdown document). Additionally:

1. **RFP Brief** (.md) — the canonical structured extraction, grounded in citations
2. **Gaps & Questions List** — items to clarify with the client before proposal writing
3. **Notebook Registry Entry** — engagement-to-notebook mapping for future reference
4. **Amendment Impact Reports** — delta analysis when sources are added

Save the RFP Brief for downstream skill consumption. All other skills should reference this brief rather than re-querying NotebookLM independently.

## Grounding Labels

All content in the RFP Brief uses the standard grounding labels:

| Label | Meaning | Usage |
|-------|---------|-------|
| `[RFP]` | Directly from client document | Cited from NotebookLM with reference |
| `[Proposed]` | Our recommendation | When RFP is silent, we propose based on experience |
| `[RFP+]` | RFP requirement + our enhancement | Client stated X, we recommend X + Y |

## Integration with Other Skills

This skill is **Step 0** — it runs before all other skills:

```
rfp-notebook (Step 0)
    ↓ RFP Brief
rfp-analysis (Go/No-Go)
    ↓ GO decision
create-proposal + technical-solution + effort-estimation + cost-estimation + team-composition + project-delivery
    ↓ All artifacts
proposal-presentation / design-presentation
    ↓ Presentation ready
proposal-review (Quality Gate)
    ↓ Approved
Submit to client
```

When another skill needs RFP data, it should first check if an RFP Brief exists. If not, prompt the user to run `rfp-notebook` first.

## Key Principles

- **One notebook per engagement** — never mix multiple RFPs in one notebook
- **All sources before extraction** — upload everything (RFP + appendices + Q&A) before running queries
- **Citations are mandatory** — every fact in the brief must trace to a source document
- **Gaps are features** — explicitly listing what the RFP doesn't say is as valuable as what it does say
- **Amendments are incremental** — don't re-extract everything; run delta queries on changes
- **The brief is the contract** — downstream skills trust the brief; if the brief is wrong, everything is wrong

For extraction query patterns and notebook management templates, read `references/extraction-catalog.md`.
