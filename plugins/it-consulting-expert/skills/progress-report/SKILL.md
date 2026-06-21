---
name: progress-report
description: >
  Generate standardized project progress reports for IT consulting engagements.
  Use this skill when the user asks to "create a status report", "write a weekly
  report", "進捗報告書を作成", "週次報告", "月次報告", "generate a progress
  update", "project status update", "EVM report", or needs to produce recurring
  status reports for client stakeholders. Also trigger for "ステータスレポート",
  "進捗管理", "status meeting preparation", and any request to summarize project
  progress, schedule variance, or defect trends for reporting purposes.
metadata:
  version: "0.1.0"
---

# Progress Report Generator (進捗報告書)

Generate standardized weekly and monthly progress reports for IT consulting projects following Japanese SIer reporting conventions.

## Why This Matters

In Japanese enterprise projects, the 進捗報告 is the primary trust mechanism between vendor and client. A well-structured report that surfaces issues early builds trust. A report that hides problems until they explode destroys it. Experienced PMs know: the report IS the project from the client's perspective.

## Workflow

### Step 0: Connect to NotebookLM (if applicable)

If the original RFP is in NotebookLM, query for reporting requirements:

```bash
notebooklm ask "What reporting format, frequency, or content does the client require?" --json
notebooklm ask "What KPIs or metrics does the client want tracked in status reports?" --json
```

### Step 1: Gather Current Status from User

Ask the user for current project data:

- **Reporting period** (week/month ending date)
- **Current phase** and planned vs. actual progress
- **Completed tasks** this period
- **Planned tasks** next period
- **Open issues** and their status
- **Risks** — new, changed, or resolved
- **Defect counts** (if in testing phase)
- **Team changes** (additions, departures, role changes)
- **Any decisions needed** from the client
- **Budget status** (if monthly report)

### Step 2: Weekly Report Structure (週次報告書)

**Header:**
| Field | Value |
|-------|-------|
| Project Name | |
| Reporting Period | YYYY/MM/DD — YYYY/MM/DD |
| Overall Status | Green / Yellow / Red |
| Report Date | |
| Author | PM Name |

**1. Overall Status Summary (全体サマリー)**

Traffic light dashboard:

| Area | Status | Trend | Comment |
|------|--------|-------|---------|
| Schedule | 🟢/🟡/🔴 | →/↑/↓ | On track / X days behind |
| Quality | 🟢/🟡/🔴 | →/↑/↓ | Defect rate within target |
| Cost | 🟢/🟡/🔴 | →/↑/↓ | Within budget / X% over |
| Risk | 🟢/🟡/🔴 | →/↑/↓ | No new critical risks |
| Scope | 🟢/🟡/🔴 | →/↑/↓ | No changes / CR pending |

**Status criteria:**
- 🟢 Green: On plan, no issues
- 🟡 Yellow: Minor deviation, corrective action in progress
- 🔴 Red: Significant deviation, escalation or replanning needed

**2. Schedule Progress (スケジュール進捗)**

| Phase/Task | Planned Start | Planned End | Actual Start | Actual End | Status | % Complete |
|-----------|--------------|------------|-------------|-----------|--------|------------|

**EVM Metrics (if tracked):**
| Metric | Value | Interpretation |
|--------|-------|---------------|
| SPI (Schedule Performance Index) | | ≥1.0 = on/ahead of schedule |
| CPI (Cost Performance Index) | | ≥1.0 = at/under budget |
| EAC (Estimate at Completion) | | Projected final cost |
| ETC (Estimate to Complete) | | Remaining cost |

**3. This Week's Accomplishments (今週の実績)**
1. [Completed item with result]
2. [Completed item with result]

**4. Next Week's Plan (来週の予定)**
1. [Planned item with target]
2. [Planned item with target]

**5. Issues (課題一覧)**
| ID | Issue | Severity | Owner | Action | Due | Status |
|----|-------|----------|-------|--------|-----|--------|

**6. Risks (リスク一覧)**
| ID | Risk | Probability | Impact | Mitigation | Owner | Status |
|----|------|-------------|--------|------------|-------|--------|
Mark new risks with 【新規】, changed risks with 【変更】.

**7. Decisions Needed (要決定事項)**
| Decision | Options | Recommendation | Deadline | Decision Maker |
|----------|---------|---------------|----------|----------------|

**8. Change Requests (変更依頼)**
| CR# | Description | Status | Impact |
|-----|-------------|--------|--------|

### Step 3: Monthly Report Additions (月次報告書)

Include everything from the weekly report PLUS:

**Budget Tracking (コスト実績):**
| Category | Budget | Actual | Variance | Forecast |
|----------|--------|--------|----------|----------|
| Labor | | | | |
| Infrastructure | | | | |
| Other | | | | |
| **Total** | | | | |

**Quality Metrics (品質指標):**
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Defect density | | | |
| Test coverage | | | |
| Code review completion | | | |
| Build success rate | | | |

**Defect Trend Chart** (describe data for chart generation):
- Open vs. closed defects by week
- Defects by severity over time
- Defect detection rate by phase

**Resource Utilization:**
| Role | Planned Hours | Actual Hours | Utilization % |
|------|-------------|-------------|---------------|

**Milestone Status:**
| Milestone | Planned Date | Forecast Date | Variance | Status |
|-----------|-------------|--------------|----------|--------|

### Step 4: Output

Generate as .docx (using the `docx` skill). Maintain consistent formatting across reports — the client expects the same structure every week.

## Key Principles

- **No surprises**: If something is Yellow or Red, the client should have heard about it before reading the report
- **Action-oriented**: Every issue has an owner and a due date. Don't list problems without actions
- **Trend over snapshot**: Show whether things are getting better or worse, not just current state
- **Honest status**: Never report Green when things are Yellow. Early transparency saves late crises
- **Consistent cadence**: Reports sent on the same day/time every week build predictability and trust

For report templates, read `references/report-templates.md`.
