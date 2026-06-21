---
name: lessons-learned
description: >
  Conduct structured post-project reviews and generate lessons learned documents
  for IT consulting engagements. Use this skill when the user asks to "create a
  lessons learned report", "案件振り返り", "project retrospective", "post-mortem",
  "振り返り会", "KPT analysis", "what went well / what didn't", "プロジェクト完了報告",
  "project close-out report", or needs to formally review project outcomes
  against original plans. Also trigger for "反省会", "改善提案", "ふりかえり",
  "planned vs actual analysis", and any request to capture and document
  project learnings for organizational improvement.
metadata:
  version: "0.1.0"
---

# Lessons Learned (案件振り返り)

Conduct structured post-project reviews with planned vs. actual analysis, root cause identification, and actionable improvement recommendations.

## Why This Matters

Japanese SIer culture values continuous improvement (改善). A thorough lessons learned session transforms project pain into organizational knowledge. Without it, the next project repeats the same mistakes. The best PMs treat this as seriously as the project kickoff — it's the investment that pays off on every future engagement.

## Workflow

### Step 0: Connect to NotebookLM

Query the original RFP and project documentation for baseline data:

```bash
notebooklm ask "What were the original project objectives, scope, and success criteria?" --json
notebooklm ask "What was the original timeline with milestones and delivery dates?" --json
notebooklm ask "What was the original budget and effort estimate?" --json
notebooklm ask "What were the key technical requirements and architecture decisions?" --json
notebooklm ask "What team structure and staffing was originally proposed?" --json
notebooklm ask "What were the identified risks in the original proposal?" --json
```

### Step 1: Gather Project Outcome Data

Ask the user for actual results:

- **Final delivery date** vs. planned
- **Final cost** vs. budget
- **Final effort** (人月) vs. estimate
- **Scope changes**: CRs approved, features deferred
- **Quality metrics**: Defect counts by severity, test pass rates
- **Team**: Actual staffing vs. plan, turnover
- **Client satisfaction**: Formal feedback, informal signals
- **Major incidents**: What went wrong and how it was handled

### Step 2: Planned vs. Actual Analysis (計画実績対比)

**Schedule Analysis:**

| Phase | Planned Duration | Actual Duration | Variance | Root Cause |
|-------|-----------------|-----------------|----------|------------|
| 要件定義 | X weeks | Y weeks | +Z weeks | [reason] |
| 基本設計 | X weeks | Y weeks | +Z weeks | [reason] |
| 詳細設計 | X weeks | Y weeks | +Z weeks | [reason] |
| 製造 | X weeks | Y weeks | +Z weeks | [reason] |
| 結合テスト | X weeks | Y weeks | +Z weeks | [reason] |
| 総合テスト | X weeks | Y weeks | +Z weeks | [reason] |
| 移行・リリース | X weeks | Y weeks | +Z weeks | [reason] |
| **Total** | **X months** | **Y months** | **+Z months** | |

**Effort Analysis:**

| Role | Planned (人月) | Actual (人月) | Variance | Root Cause |
|------|---------------|--------------|----------|------------|
| PM | | | | |
| Architect | | | | |
| SE | | | | |
| PG | | | | |
| Tester | | | | |
| Infra | | | | |
| **Total** | | | | |

**Cost Analysis:**

| Category | Budget (¥) | Actual (¥) | Variance | Variance % |
|----------|-----------|-----------|----------|------------|
| Labor | | | | |
| Infrastructure | | | | |
| Software licenses | | | | |
| Subcontractor | | | | |
| Travel/Other | | | | |
| **Total** | | | | |

**Profitability:**

| Metric | Planned | Actual |
|--------|---------|--------|
| Revenue | | |
| Total cost | | |
| Gross profit | | |
| Gross margin % | | |

### Step 3: Quality Analysis (品質分析)

**Defect Analysis:**

| Metric | Target | Actual | Assessment |
|--------|--------|--------|------------|
| Total defects found | — | X | — |
| Defects by severity: S1 | 0 | X | |
| Defects by severity: S2 | ≤ Y | X | |
| Defects by severity: S3 | ≤ Y | X | |
| Defects by severity: S4 | ≤ Y | X | |
| Defect density (per KLOC) | ≤ Y | X | |
| Post-release defects (warranty) | 0 critical | X | |
| Test case pass rate (final) | 100% | X% | |

**Defect Origin Analysis:**
Where were defects injected vs. detected?

| Injected In → | Detected in 要件 | 基本設計 | 詳細設計 | 製造 | テスト | 本番 |
|---------------|----------------|---------|---------|------|-------|------|
| 要件定義 | ✓ (ideal) | | | | ✗ (costly) | ✗✗ (very costly) |
| 基本設計 | | ✓ (ideal) | | | ✗ | ✗✗ |
| 詳細設計 | | | ✓ (ideal) | | ✗ | ✗✗ |
| 製造 | | | | ✓ (ideal) | OK | ✗ |

Goal: Most defects should be caught in the same or next phase.

### Step 4: KPT Analysis (Keep / Problem / Try)

Facilitate a structured retrospective:

**Keep (良かったこと — continue doing):**
What practices, decisions, or behaviors contributed to success?
- [Practice] — Why it worked — Evidence
- [Practice] — Why it worked — Evidence

**Problem (問題だったこと — stop doing or fix):**
What caused difficulties, delays, or quality issues?
- [Problem] — Impact — Root cause
- [Problem] — Impact — Root cause

**Try (次に試したいこと — improvements for next time):**
Specific, actionable improvements — not vague aspirations.
- [Action] — Expected benefit — Owner — When to apply

**Categorize by theme:**
- Estimation accuracy (見積精度)
- Requirements management (要件管理)
- Design quality (設計品質)
- Development process (開発プロセス)
- Testing effectiveness (テスト効率)
- Communication (コミュニケーション)
- Vendor management (協力会社管理)
- Risk management (リスク管理)
- Client relationship (顧客関係)
- Tools and infrastructure (ツール・インフラ)

### Step 5: Risk Register Review

Review risks from the original proposal:

| Risk ID | Original Risk | Probability | Impact | Did It Occur? | Actual Impact | Mitigation Effective? |
|---------|--------------|-------------|--------|---------------|--------------|----------------------|
| R-001 | | H/M/L | H/M/L | Yes/No | [actual] | Yes/Partial/No |
| R-002 | | H/M/L | H/M/L | Yes/No | [actual] | Yes/Partial/No |

**Unidentified Risks (想定外リスク):**
Risks that actually occurred but were NOT in the original risk register.

| Risk | When Occurred | Impact | How Handled | Could We Have Predicted It? |
|------|--------------|--------|-------------|---------------------------|

### Step 6: Estimation Accuracy Assessment

For organizational learning, track estimation accuracy over time:

| Metric | Estimated | Actual | Accuracy Ratio | Assessment |
|--------|-----------|--------|----------------|------------|
| Total effort (人月) | | | Actual/Estimated | |
| Duration (months) | | | | |
| By phase: 要件定義 | | | | |
| By phase: 設計 | | | | |
| By phase: 製造 | | | | |
| By phase: テスト | | | | |

**Accuracy benchmarks:**
- 0.9–1.1: Excellent estimation
- 0.8–0.9 or 1.1–1.2: Good, minor calibration needed
- 0.7–0.8 or 1.2–1.5: Needs improvement, analyze causes
- < 0.7 or > 1.5: Significant estimation failure, deep-dive required

**Estimation improvement recommendations:**
Based on the variance analysis, suggest calibration factors for future projects of similar type/scale.

### Step 7: Client Feedback Summary

**Formal feedback (if available):**
- Client satisfaction score
- Evaluation comments
- Areas praised
- Areas for improvement

**Informal signals:**
- Was there follow-on work? (strongest positive signal)
- Did the client recommend us to others?
- Were there escalations to executive level?
- How was the final acceptance meeting tone?

### Step 8: Action Items & Organizational Recommendations

Convert learnings into actionable improvements:

| # | Action Item | Category | Priority | Owner | Target Date | Applies To |
|---|-----------|----------|----------|-------|-------------|------------|
| 1 | | Estimation | H/M/L | | | Future projects of type X |
| 2 | | Process | H/M/L | | | All projects |
| 3 | | Tools | H/M/L | | | Team/department |

**Organizational recommendations:**
- Process changes to adopt company-wide
- Training needs identified
- Tool improvements needed
- Template/checklist updates
- Knowledge base articles to create

### Step 9: Output

Generate as .docx (using the `docx` skill):
1. Project close-out report (プロジェクト完了報告書) — formal document for management
2. Lessons learned document (振り返り報告書) — detailed analysis
3. Action items tracker — for follow-up

## Key Principles

- **Blameless**: Focus on processes and systems, not individuals. "The code review process missed this" not "Tanaka missed this"
- **Specific and actionable**: "Improve testing" is useless. "Add API integration tests for external services in 結合テスト phase" is actionable
- **Timely**: Conduct within 2 weeks of go-live while memories are fresh
- **Inclusive**: Include all team members, including subcontractors. Junior members often see things seniors miss
- **Follow through**: The action items are worthless if nobody tracks them. Assign owners and deadlines
- **Celebrate success**: Don't make it all about problems. Recognize what went well and WHO made it happen

For retrospective facilitation guides and templates, read `references/retrospective-guide.md`.
