---
name: change-request
description: >
  Manage formal scope change requests for IT consulting projects following
  Japanese SIer change management conventions. Use this skill when the user asks
  to "create a change request", "変更管理", "スコープ変更", "scope change",
  "change order", "CR作成", "変更依頼書を作成", "impact analysis for a change",
  "変更影響分析", "assess scope change impact", or needs to formally document,
  evaluate, and track project changes against the original RFP baseline.
  Also trigger for "追加要件", "仕様変更", "additional requirements",
  "change control board", "CCB", and any request to manage scope creep
  or formal change processes.
metadata:
  version: "0.1.0"
---

# Change Request Management (変更管理)

Manage formal scope change requests with impact analysis, approval workflows, and cumulative tracking against the original RFP baseline.

## Why This Matters

Scope creep kills SIer projects. Japanese enterprise clients expect formal change management — every deviation from the original RFP scope must be documented, impact-analyzed, and approved before work begins. Without this discipline, you absorb cost overruns silently until the project is underwater. Experienced PMs know: "No CR, no work" is the rule that saves projects.

## Workflow

### Step 0: Connect to NotebookLM

Query the original RFP for baseline scope and change management expectations:

```bash
notebooklm ask "What is the original project scope, deliverables list, and acceptance criteria?" --json
notebooklm ask "Does the RFP specify a change management process, approval authority, or change control procedures?" --json
notebooklm ask "What are the contractual terms regarding scope changes, additional costs, and timeline extensions?" --json
notebooklm ask "What is the original project timeline with milestones and deadlines?" --json
notebooklm ask "What is the original budget and pricing structure (fixed price, T&M, hybrid)?" --json
```

### Step 1: Change Request Identification

Ask the user:

- **Change origin**: Client request, internal discovery, regulatory change, defect-driven redesign
- **Change description**: What specifically is being added, modified, or removed
- **Affected deliverables**: Which phases, documents, or components are impacted
- **Requester**: Who initiated this change and when
- **Priority**: Critical (blocks progress) / High / Medium / Low
- **Current project status**: Phase, % complete, budget consumed

### Step 2: Impact Analysis (影響分析)

Analyze impact across 5 dimensions:

**Schedule Impact (スケジュール影響):**

| Item | Original | After Change | Delta |
|------|----------|-------------|-------|
| Phase duration | | | +X days |
| Milestone dates | | | Shift by X |
| Go-live date | | | +X days |
| Dependencies affected | | | List |

**Cost Impact (コスト影響):**

| Category | Additional Effort | Unit Rate | Additional Cost |
|----------|------------------|-----------|-----------------|
| Design | +X 人月 | ¥XXX | ¥XXX |
| Development | +X 人月 | ¥XXX | ¥XXX |
| Testing | +X 人月 | ¥XXX | ¥XXX |
| Infrastructure | — | — | ¥XXX |
| **Total** | | | **¥XXX** |

**Quality Impact (品質影響):**
- Additional test cases required
- Regression testing scope expansion
- Impact on existing test results (invalidation)
- Risk of introducing new defects

**Scope Impact (スコープ影響):**
- New requirements added vs. original RFP baseline
- Existing requirements modified
- Requirements removed or deferred
- Impact on other in-scope features (ripple effects)

**Risk Impact (リスク影響):**
- New risks introduced by the change
- Existing risks amplified
- Mitigation actions required
- Impact on overall project risk profile

### Step 3: Change Request Document (変更依頼書)

Generate the formal CR document:

**Header:**
| Field | Value |
|-------|-------|
| CR Number | CR-YYYY-NNN |
| Project Name | |
| Date Submitted | |
| Requested By | |
| Priority | Critical / High / Medium / Low |
| Status | Draft → Submitted → Under Review → Approved / Rejected / Deferred |

**1. Change Description (変更内容)**
Clear, unambiguous description of what is changing. Reference specific RFP sections or requirement IDs where applicable. Label with [RFP] for client-originated changes or [Internal] for vendor-discovered changes.

**2. Reason for Change (変更理由)**
Business justification. Categories:
- Client requirement change (お客様要件変更)
- Requirement clarification (要件明確化) — was ambiguous in RFP
- Technical discovery (技術的発見) — unforeseen constraint
- Regulatory/compliance (法規制対応)
- Defect-driven redesign (不具合起因の設計変更)

**3. Impact Summary (影響サマリー)**

| Dimension | Impact Level | Details |
|-----------|-------------|---------|
| Schedule | None / Low / Medium / High | +X days to milestone Y |
| Cost | None / Low / Medium / High | +¥X,XXX,XXX |
| Quality | None / Low / Medium / High | +X test cases, regression needed |
| Scope | None / Low / Medium / High | X requirements added/modified |
| Risk | None / Low / Medium / High | New risk: [description] |

**4. Options Analysis (対応案)**
Present 2-3 options whenever possible:

| Option | Description | Schedule | Cost | Risk | Recommendation |
|--------|-------------|----------|------|------|---------------|
| A | Full implementation | +X days | +¥X | Low | ★ Recommended |
| B | Partial / phased | +Y days | +¥Y | Med | Alternative |
| C | Defer to Phase 2 | None | None | Low | If budget constrained |

**5. Approval (承認)**

| Role | Name | Decision | Date | Signature |
|------|------|----------|------|-----------|
| Client PM | | Approve / Reject / Defer | | |
| Client Sponsor | | Approve / Reject / Defer | | |
| Vendor PM | | Approve / Reject / Defer | | |
| Vendor Director | | Approve / Reject / Defer | | |

Approval authority thresholds (typical):
- PM approval: < ¥1M and < 5 days schedule impact
- Director approval: ¥1M–¥5M or 5–15 days impact
- Executive approval: > ¥5M or > 15 days or go-live date change

### Step 4: Cumulative Change Tracker (変更累積管理表)

Maintain a running ledger of all changes against the original baseline:

**Cumulative Impact Dashboard:**

| Metric | Original Baseline | Cumulative Changes | Current Forecast | Variance |
|--------|-------------------|-------------------|-----------------|----------|
| Timeline | X months | +Y days | X months + Y days | +Z% |
| Budget | ¥XX,XXX,XXX | +¥X,XXX,XXX | ¥XX,XXX,XXX | +Z% |
| Scope (requirements) | N items | +X / -Y | N+X-Y items | +Z% |
| Effort (人月) | XX 人月 | +X 人月 | XX+X 人月 | +Z% |

**Change Log:**

| CR# | Date | Description | Status | Schedule | Cost | Requester |
|-----|------|-------------|--------|----------|------|-----------|
| CR-2024-001 | | | Approved | +3 days | +¥500K | Client |
| CR-2024-002 | | | Rejected | — | — | Internal |
| CR-2024-003 | | | Pending | +5 days | +¥1.2M | Client |

**Warning Thresholds:**
- 🟡 Yellow: Cumulative changes exceed 10% of original baseline (budget or timeline)
- 🔴 Red: Cumulative changes exceed 20% — trigger contract amendment discussion
- ⚠️ Critical: Cumulative changes affect go-live date — executive escalation required

### Step 5: Scope Creep Prevention

For each change request, verify:

1. **Is this truly new?** — Check if the requirement was already in the original RFP (query NotebookLM)
2. **Is this a clarification or a change?** — Clarifications of ambiguous RFP items may not warrant a CR
3. **Was this foreseeable?** — If yes, why wasn't it in the original estimate? (lessons learned input)
4. **Can it be deferred?** — Phase 2 is a valid answer for non-critical changes
5. **Is the client aware of the cumulative impact?** — Show the dashboard, not just this CR

### Step 6: Output

Generate as .docx (using the `docx` skill):
1. Individual CR document (変更依頼書)
2. Updated cumulative change tracker (変更累積管理表)

## Key Principles

- **"No CR, no work"**: Never start work on a change without formal approval, regardless of how small
- **Baseline is sacred**: The original RFP scope is the reference point. All changes are measured against it
- **Options, not ultimatums**: Always present alternatives. "We can do A at cost X or B at cost Y" is better than "This costs ¥2M more"
- **Cumulative visibility**: Individual CRs look small. The cumulative tracker reveals scope creep
- **Speed of response**: A fast, professional CR response builds trust. Delays signal incompetence
- **Formal Japanese keigo**: CR documents are contractual — use proper business language

For change request templates and approval workflow details, read `references/change-templates.md`.
