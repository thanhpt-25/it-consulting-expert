---
name: vendor-management
description: >
  Manage subcontractors, offshore partners, and multi-vendor project structures
  for IT consulting engagements. Use this skill when the user asks to "manage
  subcontractors", "協力会社管理", "vendor management", "create a RACI matrix",
  "multi-vendor org chart", "offshore management", "オフショア管理",
  "パートナー管理", "subcontractor evaluation", "協力会社評価", or needs to
  structure and govern relationships with external development partners.
  Also trigger for "再委託管理", "外注管理", "vendor onboarding",
  "partner selection", and any request to organize multi-company project teams.
metadata:
  version: "0.1.0"
---

# Vendor Management (協力会社管理)

Manage subcontractors, offshore partners, and multi-vendor project structures with RACI matrices, performance tracking, and governance frameworks.

## Why This Matters

Most Japanese SIer projects involve subcontractors (協力会社) — sometimes 50%+ of the team. Poor vendor management is the #1 hidden cause of project failure. The prime contractor is accountable to the client for everything, including subcontractor quality. Managing this well means clear boundaries, measurable quality gates, and governance that catches problems before they reach the client.

## Workflow

### Step 0: Connect to NotebookLM

Query the RFP for vendor-related requirements:

```bash
notebooklm ask "Does the RFP restrict or require specific subcontracting arrangements, including re-delegation (再委託) rules?" --json
notebooklm ask "Are there data residency, security clearance, or location requirements that affect vendor selection?" --json
notebooklm ask "Does the client require approval of subcontractors or key personnel?" --json
notebooklm ask "What are the contractual terms around liability, IP ownership, and confidentiality for subcontractors?" --json
notebooklm ask "Are there requirements for on-site presence, co-location, or specific work locations?" --json
```

### Step 1: Vendor Structure Design

Ask the user:

- **Project scale**: Total team size and budget
- **In-house capacity**: Which roles/skills are available internally
- **Gaps to fill**: Specific skills, capacity, or cost optimization needs
- **Delivery model**: Full onshore, nearshore, offshore, hybrid
- **Client constraints**: Security clearances, location requirements, language needs
- **Existing partners**: Preferred vendors with track record

### Step 2: Multi-Company Organization Chart

Design the project organization showing all companies:

```
[Client Organization]
├── Client PM / Sponsor
├── Client Technical Lead
└── Client Business Users (UAT)

[Prime Contractor (Your Company)]
├── Project Director (統括責任者)
├── Project Manager
├── PMO
├── Technical Architect
└── QA Lead

[Subcontractor A — Development Partner]
├── Sub-PM (A社窓口)
├── SE × N
└── PG × N

[Subcontractor B — Infrastructure Partner]
├── Sub-PM (B社窓口)
└── Infrastructure Engineers × N

[Offshore Center (if applicable)]
├── Bridge SE (ブリッジSE)
├── Offshore PM
└── Offshore Development Team × N
```

**Key rules:**
- Every company has exactly ONE contact point (窓口) to the prime contractor
- No direct communication between client and subcontractors without prime contractor involvement
- Bridge SE is mandatory for offshore — they translate requirements, culture, and quality standards

### Step 3: RACI Matrix

Define responsibility across companies for key activities:

| Activity | Client | Prime PM | Prime Tech | Sub-A | Sub-B | Offshore |
|----------|--------|----------|------------|-------|-------|----------|
| Requirements definition | A | R | C | I | I | I |
| Basic design | C | A | R | C | I | I |
| Detailed design | I | A | R | R | R | C |
| Development | I | A | C | R | R | R |
| Unit testing | I | A | C | R | R | R |
| Integration testing | C | A | R | C | C | I |
| System testing | A | R | C | I | I | I |
| UAT support | R | A | C | I | I | I |
| Infrastructure setup | C | A | I | I | R | I |
| Deployment | A | R | C | I | R | I |
| Deliverable review | A | R | R | I | I | I |
| Quality assurance | I | A | R | I | I | I |

Legend: R=Responsible, A=Accountable, C=Consulted, I=Informed

### Step 4: Vendor Evaluation & Selection

**Selection Criteria Matrix:**

| Criterion | Weight | Vendor A | Vendor B | Vendor C |
|-----------|--------|----------|----------|----------|
| Technical capability | 25% | | | |
| Past performance with us | 20% | | | |
| Cost competitiveness | 20% | | | |
| Resource availability | 15% | | | |
| Communication quality | 10% | | | |
| Financial stability | 10% | | | |
| **Weighted Score** | **100%** | | | |

**Due Diligence Checklist:**
- [ ] Company registration and financial statements reviewed
- [ ] NDA (秘密保持契約) executed
- [ ] Security audit / ISMS certification confirmed
- [ ] Reference check with other clients
- [ ] Sample deliverable quality reviewed
- [ ] Key personnel CV and interview completed
- [ ] Conflict of interest check (not working for competitor on same client)
- [ ] Insurance coverage confirmed

### Step 5: Governance Framework

**Meeting Cadence:**

| Meeting | Participants | Frequency | Purpose |
|---------|-------------|-----------|---------|
| Steering Committee | Client + Prime Director | Monthly | Strategic decisions |
| Project Status | Prime PM + Sub-PMs | Weekly | Progress, issues, risks |
| Technical Sync | Prime Architect + Sub Leads | Weekly | Design alignment, tech decisions |
| Quality Review | Prime QA + Sub QA | Bi-weekly | Deliverable quality, defect trends |
| Offshore Standup | Bridge SE + Offshore PM | Daily | Task progress, blockers |

**Quality Gates for Subcontractor Deliverables:**

| Gate | Criteria | Action if Failed |
|------|----------|-----------------|
| Design Review | Compliance with base design, naming conventions, standards adherence | Return with specific correction items |
| Code Review | Coding standards, security checklist, performance baseline | Block merge, return for fixes |
| Unit Test | Coverage ≥ 80%, all tests pass, no critical Sonar issues | Return for additional coverage |
| Deliverable Acceptance | Template compliance, content completeness, review comments addressed | Return with checklist of gaps |

**Escalation Path:**
1. Sub-PM ↔ Prime PM (operational issues, 1-2 day resolution)
2. Sub Director ↔ Prime Director (contractual, resource, quality issues)
3. Sub Executive ↔ Prime Executive (contract disputes, termination)

### Step 6: Performance Tracking

**Monthly Vendor Scorecard:**

| KPI | Target | Actual | Status |
|-----|--------|--------|--------|
| Deliverable on-time rate | ≥ 90% | | 🟢/🟡/🔴 |
| Defect density (per KLOC) | ≤ X | | 🟢/🟡/🔴 |
| Rework rate | ≤ 10% | | 🟢/🟡/🔴 |
| Resource turnover | ≤ 5%/quarter | | 🟢/🟡/🔴 |
| Communication responsiveness | Response within 4h | | 🟢/🟡/🔴 |
| Security incident count | 0 | | 🟢/🟡/🔴 |

**Scoring:**
- 🟢 Meets or exceeds target
- 🟡 Within 10% of target
- 🔴 More than 10% below target — corrective action required

**Corrective Action Process:**
1. Issue identified → documented in scorecard
2. Discuss with Sub-PM → agree corrective action and timeline
3. If not resolved in 2 weeks → escalate to Director level
4. If pattern continues → formal warning letter (改善要求書)
5. If no improvement → consider replacement (last resort)

### Step 7: Offshore-Specific Management

**Bridge SE Responsibilities:**
- Translate requirements from Japanese to offshore team's language
- Ensure cultural alignment (reporting style, quality expectations, work hours overlap)
- Review all deliverables before submission to prime contractor
- Daily standup with offshore team, weekly report to prime PM
- On-site presence at prime contractor during critical phases

**Time Zone Management (Japan-centric):**
| Offshore Location | Overlap with JST (9-18) | Recommended Sync Window |
|-------------------|------------------------|------------------------|
| Vietnam (UTC+7) | 7 hours (10-17 JST) | 10:00-12:00 JST |
| India (UTC+5:30) | 5.5 hours (11:30-17 JST) | 13:00-15:00 JST |
| China (UTC+8) | 8 hours (10-18 JST) | 10:00-12:00 JST |
| Philippines (UTC+8) | 8 hours (10-18 JST) | 10:00-12:00 JST |

**Communication Protocol:**
- All formal communication in writing (email or ticket system)
- Verbal discussions followed by written confirmation within 24h
- Shared project management tool (Backlog, Redmine, Jira) — single source of task truth
- Document language: Japanese ↔ English via Bridge SE; never rely on machine translation for requirements

### Step 8: Output

Generate as .docx (using the `docx` skill):
1. Multi-company organization chart
2. RACI matrix
3. Vendor governance plan
4. Vendor scorecard template

## Key Principles

- **Prime contractor accountability**: You own everything the client sees. Subcontractor failures are YOUR failures
- **One window (一窓口)**: Every company has one point of contact. No side channels
- **Quality at the gate**: Catch subcontractor quality issues before they reach client deliverables
- **Relationship over contract**: Good vendor relationships are built over multiple projects. Invest in them
- **Transparency up, protection down**: Be transparent with your client about structure. Protect your subcontractors from direct client pressure
- **Fair terms**: Pay vendors fairly and on time. Squeezing margins creates quality problems

For vendor evaluation templates and contract checklists, read `references/vendor-templates.md`.
