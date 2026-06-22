# Extraction Query Catalog & Notebook Management Templates

## Standard Extraction Query Set (標準抽出クエリセット)

The 26 standard queries are organized into 8 categories. Each query is designed to extract specific, cited information from the RFP.

### Query Design Principles

1. **One topic per query** — don't ask compound questions ("What is the budget AND timeline?")
2. **Specificity over breadth** — "List all functional requirements organized by module" beats "What are the requirements?"
3. **Ask for structure** — "List with priority levels" produces more usable output than "Tell me about requirements"
4. **Request negatives** — "What is explicitly out-of-scope?" catches boundaries that broad questions miss
5. **Follow up on gaps** — if a standard query returns thin results, ask a targeted follow-up

### Category 1: Project Overview (案件概要) — 3 queries

| # | Query | Expected Output | Follow-up If Thin |
|---|-------|----------------|-------------------|
| Q-01 | "What is the project name, objective, and background? Why is the client undertaking this project now?" | Project context, business drivers, urgency | "What business problems or pain points does the client describe?" |
| Q-02 | "What is the project scope? What is explicitly in-scope and out-of-scope?" | Scope boundaries | "Are there any modules, systems, or locations explicitly excluded?" |
| Q-03 | "What are the key success criteria or KPIs the client defines for this project?" | Measurable targets | "What does the client consider a successful outcome?" |

### Category 2: Requirements (要件) — 4 queries

| # | Query | Expected Output | Follow-up If Thin |
|---|-------|----------------|-------------------|
| Q-04 | "List all functional requirements mentioned in the RFP, organized by business area or module" | FR catalog | "For each business function mentioned, what specific capabilities are needed?" |
| Q-05 | "List all non-functional requirements: performance targets, security requirements, availability SLA, scalability needs, and accessibility standards" | NFR catalog | "What response time, uptime, or concurrent user targets are specified?" |
| Q-06 | "What are the mandatory technology constraints, platform requirements, or integration standards?" | Tech constraints | "Does the client specify any preferred vendors, languages, or frameworks?" |
| Q-07 | "What data migration or conversion requirements are specified?" | Migration scope | "How much historical data needs to be migrated and from which systems?" |

### Category 3: Timeline & Milestones (スケジュール) — 3 queries

| # | Query | Expected Output | Follow-up If Thin |
|---|-------|----------------|-------------------|
| Q-08 | "What is the overall project timeline? Start date, end date, and any intermediate deadlines?" | Date range | "Is there a hard deadline driven by regulatory, fiscal year, or business event?" |
| Q-09 | "What are the key milestones, phase gates, or checkpoint dates the client expects?" | Milestone list | "Does the client expect phased delivery or a single go-live?" |
| Q-10 | "What is the proposal submission deadline and format requirements?" | Submission logistics | "What is the expected timeline from submission to contract award?" |

### Category 4: Budget & Commercial (予算・商務) — 3 queries

| # | Query | Expected Output | Follow-up If Thin |
|---|-------|----------------|-------------------|
| Q-11 | "Is there a stated budget range, budget ceiling, or budget constraints?" | Budget info | "Are there any cost-related evaluation criteria or weighting?" |
| Q-12 | "What pricing model does the client prefer: fixed price, time and materials, or other?" | Pricing preference | "Does the RFP discuss risk-sharing or gain-sharing arrangements?" |
| Q-13 | "What payment terms, invoicing schedule, or financial conditions are specified?" | Payment terms | "Are milestone-based payments mentioned?" |

### Category 5: Technical Environment (技術環境) — 4 queries

| # | Query | Expected Output | Follow-up If Thin |
|---|-------|----------------|-------------------|
| Q-14 | "Describe the client's current IT systems, infrastructure, and technology stack" | As-is landscape | "What databases, middleware, or cloud services does the client currently use?" |
| Q-15 | "What integrations with existing systems are required? List each system and the integration type" | Integration map | "For each integration, what data flows between systems?" |
| Q-16 | "What security, compliance, or regulatory requirements are mentioned?" | Compliance needs | "Does the client require specific certifications (ISO 27001, SOC 2, PCI-DSS)?" |
| Q-17 | "What are the hosting, deployment, or infrastructure requirements?" | Infra requirements | "On-premises, cloud, or hybrid? Any specific cloud provider preference?" |

### Category 6: Team & Process (体制・プロセス) — 3 queries

| # | Query | Expected Output | Follow-up If Thin |
|---|-------|----------------|-------------------|
| Q-18 | "What team structure, roles, or staffing requirements does the client specify?" | Staffing needs | "Does the client require on-site presence or accept remote work?" |
| Q-19 | "Does the client prefer a specific development methodology?" | Methodology | "What project management tools or processes does the client use internally?" |
| Q-20 | "What reporting, communication, or meeting cadence does the client expect?" | Governance | "Who are the key stakeholders on the client side?" |

### Category 7: Evaluation & Submission (評価・提出) — 3 queries

| # | Query | Expected Output | Follow-up If Thin |
|---|-------|----------------|-------------------|
| Q-21 | "What evaluation criteria will the client use to assess proposals? List with weights if provided" | Scoring criteria | "Is there a separate technical and commercial evaluation?" |
| Q-22 | "What are the mandatory submission requirements: format, page count, sections, copies, delivery method?" | Format rules | "Is there a mandatory proposal template or structure to follow?" |
| Q-23 | "Are there mandatory qualifications, certifications, or references required from the vendor?" | Vendor gates | "What past project experience does the client require?" |

### Category 8: Risks & Constraints (リスク・制約) — 3 queries

| # | Query | Expected Output | Follow-up If Thin |
|---|-------|----------------|-------------------|
| Q-24 | "What risks, constraints, or assumptions does the RFP mention or imply?" | Risk register seed | "Are there organizational change or business process risks mentioned?" |
| Q-25 | "Are there penalty clauses, liquidated damages, or SLA breach consequences?" | Penalty terms | "What is the liability cap or limitation of liability mentioned?" |
| Q-26 | "What are the contract terms for IP ownership, warranty, and liability?" | Contract terms | "What warranty period does the client expect post-delivery?" |

---

## Advanced Extraction Queries (上級抽出クエリ)

Use these for complex or specialized RFPs:

### Multi-Turn Deep Dive

```bash
# Initial broad query
notebooklm ask "What are the main functional modules in this system?" --json -n <notebook_id>
# → returns conversation_id

# Follow up on each module
notebooklm ask "For the [module name] module, what are the detailed functional requirements?" --json -n <notebook_id> -c <conversation_id>
```

### Comparison Queries (for replacement/migration projects)

```bash
notebooklm ask "Compare what the current system does vs. what the new system is expected to do. What are the gaps?" --json -n <notebook_id>
notebooklm ask "What functionality from the current system should NOT be carried over to the new system?" --json -n <notebook_id>
```

### Hidden Requirements Detection

```bash
notebooklm ask "Are there any implied requirements that are not explicitly stated but can be inferred from the context?" --json -n <notebook_id>
notebooklm ask "What does the RFP assume the vendor already knows or has experience with?" --json -n <notebook_id>
notebooklm ask "Are there contradictions or inconsistencies between different sections of the RFP?" --json -n <notebook_id>
```

### Competitive Intelligence

```bash
notebooklm ask "Does the RFP hint at the client's previous vendor, current dissatisfaction, or reason for re-procurement?" --json -n <notebook_id>
notebooklm ask "Are there requirements that seem tailored to a specific vendor's capabilities?" --json -n <notebook_id>
```

---

## Notebook Management Templates

### Source Checklist (ソースチェックリスト)

Before running extraction, verify all sources are loaded:

```
□ Main RFP document (本体)
□ Technical specifications appendix (技術仕様書別紙)
□ System architecture diagrams (システム構成図)
□ Data volume / data dictionary (データ量・データ定義書)
□ Current system documentation (現行システム資料)
□ Q&A responses from client (質疑応答回答書)
□ Amendment documents (修正通知書)
□ Evaluation criteria details (評価基準詳細)
□ Contract terms / draft contract (契約条件・契約書案)
□ Client organization chart (組織図)
```

### Extraction Progress Tracker

Track which queries have been run and their result quality:

```
Extraction Progress: [Client] - [Project]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Category              │ Queries │ Rich │ Thin │ Empty
──────────────────────┼─────────┼──────┼──────┼──────
Project Overview      │ 3/3     │ 2    │ 1    │ 0
Requirements          │ 4/4     │ 4    │ 0    │ 0
Timeline              │ 3/3     │ 2    │ 0    │ 1
Budget & Commercial   │ 3/3     │ 1    │ 1    │ 1
Technical Environment │ 4/4     │ 3    │ 1    │ 0
Team & Process        │ 3/3     │ 1    │ 2    │ 0
Evaluation            │ 3/3     │ 3    │ 0    │ 0
Risks & Constraints   │ 3/3     │ 2    │ 1    │ 0
──────────────────────┼─────────┼──────┼──────┼──────
Total                 │ 26/26   │ 18   │ 6    │ 2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Rich: 3+ cited facts | Thin: 1-2 cited facts | Empty: no relevant info found

⚠️ Empty categories require [Proposed] assumptions in the RFP Brief
```

### Amendment Tracking Template

```
Amendment Log: [Client] - [Project]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  │ Date       │ Type          │ Impact   │ Brief Updated
───┼────────────┼───────────────┼──────────┼─────────────
1  │ 2024/06/15 │ Amendment     │ High     │ ✅ Yes
2  │ 2024/06/20 │ Q&A Round 1   │ Medium   │ ✅ Yes
3  │ 2024/07/01 │ Q&A Round 2   │ Low      │ ⏳ Pending
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Notebook Archival Checklist

When an engagement concludes (win or lose):

```
□ Final RFP Brief saved to engagement folder
□ All amendment impact reports saved
□ Gaps & Questions list archived with resolution status
□ Notebook renamed with outcome: "RFP - [Client] - [Project] [WON/LOST]"
□ Lessons learned extracted (feed to lessons-learned skill)
□ If WON: notebook kept active for delivery phase reference
□ If LOST: notebook archived, debrief notes added as source
```

---

## Citation Quality Assessment

After extraction, assess citation quality:

| Quality Level | Definition | Action |
|--------------|-----------|--------|
| Strong | Direct quote from RFP with page/section reference | Use as [RFP] with confidence |
| Moderate | Paraphrased from RFP, source identifiable | Use as [RFP], verify wording |
| Weak | Inferred from context, no direct quote | Mark as [RFP+] with caveat |
| None | No citation returned | Mark as [Proposed] or add to Gaps list |

**Rule:** If >30% of a category has Weak/None citations, the RFP likely doesn't cover that topic well. Flag it in the Gaps section and prepare clarification questions for the client.
