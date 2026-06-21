---
name: project-delivery
description: >
  Plan project delivery methodology, milestones, and governance for IT consulting
  engagements, grounded in customer RFP/RFQ from NotebookLM. Use this skill when
  the user asks to "create a project plan", "define delivery methodology", "plan
  project phases", "プロジェクト計画", "開発プロセス", "how to deliver this
  project", "milestone plan", "governance structure", "quality plan", "品質管理計画",
  or needs to define how a project will be executed, managed, and delivered. Also
  trigger for "SDLC", "waterfall plan", "agile delivery", "hybrid methodology",
  "進捗管理", "WBS schedule".
metadata:
  version: "0.2.0"
---

# Project Delivery Planning

Define how an IT consulting project will be executed, **grounded in RFP/RFQ delivery requirements from NotebookLM**.

## NotebookLM-First Rule

The RFP often specifies methodology preferences, milestone expectations, reporting requirements, and governance structures. Extract these before proposing any delivery plan — proposing Agile when the client mandates Waterfall (or vice versa) is a fast path to rejection.

## Workflow

### Step 0: Extract Delivery Requirements from NotebookLM

```bash
notebooklm ask "Does the client specify a development methodology — waterfall, agile, hybrid, or other?" --json
notebooklm ask "What milestones, phase gates, or checkpoint dates does the client expect?" --json
notebooklm ask "What reporting, status updates, or governance meetings does the client require?" --json
notebooklm ask "What quality assurance, testing, or acceptance criteria does the client define?" --json
notebooklm ask "What risk management or escalation procedures does the client expect?" --json
notebooklm ask "What document deliverables does the client require at each phase?" --json
notebooklm ask "What communication channels, frequency, or stakeholder engagement does the client expect?" --json
notebooklm ask "What change management or change request process does the client define?" --json
```

### Step 1: Select Methodology

**If RFP specifies → use it.** Propose modifications only with clear justification.

**If RFP is silent → recommend based on project characteristics:**

| Factor | Waterfall | Agile | Hybrid |
|--------|-----------|-------|--------|
| Requirements stability | Well-defined | Evolving | Mixed |
| Contract type | Fixed-price | T&M | Either |
| Client culture | Traditional/SIer | Startup/modern | Transitioning |
| Regulatory | High compliance | Low compliance | Moderate |
| Japanese enterprise default | Yes | Rare | Growing |

### Step 2: Define Phase Plan

**For Waterfall / Hybrid** (anchored to RFP milestones):

| Phase | Japanese Name | Duration % | RFP Milestone | Gate Criteria |
|-------|-------------|-----------|---------------|---------------|
| Requirements | 要件定義 | 10-15% | [from RFP] | 要件定義書 approved |
| Basic Design | 基本設計 | 15-20% | [from RFP] | 基本設計書 approved |
| Detailed Design | 詳細設計 | 15-20% | [from RFP] | 詳細設計書 approved |
| Implementation | 製造 | 20-25% | [from RFP] | Code complete |
| Integration Test | 結合テスト | 10-15% | [from RFP] | IT report approved |
| System Test | 総合テスト | 10-15% | [from RFP] | UAT sign-off |
| Deployment | 移行・リリース | 5-10% | [from RFP] | Go-live checklist |

### Step 3: Governance Structure

**Match RFP expectations.** If the RFP defines meeting cadence, use it:

| Meeting | Frequency | Participants | Purpose | RFP Requirement |
|---------|-----------|-------------|---------|-----------------|
| Steering Committee | Monthly | PM, Client Sponsors | Strategic decisions | [RFP or Proposed] |
| Progress Meeting | Weekly | PM, TL, Client PM | Status review | [RFP or Proposed] |
| Technical Review | Per phase gate | TL, SE, Client tech | Quality review | [RFP or Proposed] |

**Reporting**: Match RFP format if specified. Otherwise propose:
- Weekly status report (週次報告書)
- Monthly executive report
- Phase completion report (工程完了報告書)

### Step 4: Quality Assurance Plan

Address RFP-stated quality requirements:

| Test Level | Scope | RFP Requirement | Entry Criteria | Exit Criteria |
|-----------|-------|-----------------|----------------|---------------|
| Unit Test | Functions | [RFP or standard] | Code complete | Coverage > 80% |
| Integration Test | Interfaces | [from RFP] | UT complete | All cases pass |
| System Test | End-to-end | [from RFP] | IT complete | All cases pass |
| UAT | Business | [from RFP] | ST complete | Client sign-off |
| Performance | Load/stress | [from RFP NFRs] | ST complete | Meets targets |

### Step 5: Risk Management

Derive risks from the actual RFP scope and constraints:
- RFP ambiguities flagged during extraction → risk of scope creep
- Tight timeline in RFP → risk of quality compromise
- Complex integrations in RFP → risk of interface delays
- New technology in RFP → risk of learning curve

| ID | Risk | Source | Probability | Impact | Mitigation | Owner |
|----|------|--------|-------------|--------|------------|-------|

### Step 6: Output

Produce a project delivery plan containing:
1. Methodology and rationale (respecting RFP preference)
2. Phase plan with milestones (anchored to RFP dates)
3. Governance structure (matching RFP reporting requirements)
4. Quality assurance plan (covering RFP quality requirements)
5. Risk register (grounded in actual project scope)
6. Communication plan (matching RFP stakeholder expectations)
7. Change management process

## Key Principles

- **Fit the client's expectations**: The RFP tells you what governance maturity the client expects
- **Gates catch real issues**: Don't add ceremony the RFP doesn't need
- **Over-communicate early**: More communication in requirements/design prevents rework
- **Document decisions**: Record why, not just what — especially for RFP interpretation choices

For phase document templates, read `references/phase-documents.md`.
For quality metrics, read `references/quality-metrics.md`.
