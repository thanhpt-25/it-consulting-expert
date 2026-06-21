---
name: maintenance-proposal
description: >
  Create post-delivery maintenance and support contract proposals for IT systems.
  Use this skill when the user asks to "create a maintenance proposal",
  "保守運用提案", "support contract proposal", "SLA definition", "SLA定義",
  "maintenance plan", "保守計画", "運用設計", "operations proposal",
  "post-go-live support", "create a support plan", or needs to propose ongoing
  maintenance, monitoring, and support services after project delivery.
  Also trigger for "保守見積", "年間保守", "ヘルプデスク提案",
  "incident management plan", and any request to define post-delivery
  support structures, SLAs, or maintenance pricing.
metadata:
  version: "0.1.0"
---

# Maintenance & Support Proposal (保守運用提案)

Create comprehensive post-delivery maintenance and support contract proposals with SLA definitions, support tier structures, and pricing models.

## Why This Matters

In Japanese SIer business, maintenance contracts (保守契約) are the annuity revenue that sustains the company between projects. A well-structured maintenance proposal secures 15-20% of the original project value annually, often for 3-5 years. More importantly, it ensures the system you built continues to work properly — protecting both your client and your reputation.

## Workflow

### Step 0: Connect to NotebookLM

If the original RFP or project documentation is in NotebookLM, query for maintenance-relevant information:

```bash
notebooklm ask "Does the RFP or contract include requirements for post-delivery maintenance, support, or warranty period?" --json
notebooklm ask "What are the system's availability requirements, RPO, and RTO targets?" --json
notebooklm ask "What is the technology stack, infrastructure, and deployment architecture?" --json
notebooklm ask "What are the business-critical functions and peak usage periods?" --json
notebooklm ask "Are there existing maintenance contracts or support structures being replaced?" --json
notebooklm ask "What regulatory or compliance requirements affect system operations?" --json
```

### Step 1: Gather Maintenance Requirements

Ask the user:

- **System overview**: What was delivered, technology stack, user base
- **Criticality**: Business impact if the system goes down
- **Support hours**: Business hours only (9-18 JST) or 24/7/365
- **Current state**: Still in warranty? Existing support in place?
- **Client expectations**: Response time, resolution time, reporting
- **Budget indication**: Client's ballpark for annual maintenance
- **Contract duration**: 1 year, 3 years, 5 years

### Step 2: Service Catalog (サービスカタログ)

Define the maintenance service offerings:

**Category 1: Corrective Maintenance (障害対応)**
- Incident reception and triage
- Root cause analysis
- Bug fixes and emergency patches
- Workaround implementation
- Post-incident reporting

**Category 2: Adaptive Maintenance (環境適応)**
- OS and middleware version upgrades
- Security patch application
- Browser compatibility updates
- Third-party library updates
- Infrastructure scaling adjustments

**Category 3: Preventive Maintenance (予防保守)**
- System health monitoring
- Performance trend analysis
- Capacity planning
- Security vulnerability scanning
- Backup verification and DR testing

**Category 4: Perfective Maintenance (改善保守)**
- Minor enhancements (within included hours)
- Performance optimization
- UX improvements
- Report additions/modifications
- Configuration changes

**Category 5: Operations Support (運用支援)**
- Batch job monitoring
- Data maintenance (master data updates)
- User account management
- Regular reporting
- Helpdesk (問い合わせ対応)

### Step 3: SLA Definition (SLA定義)

**Incident Severity Classification:**

| Severity | Japanese | Definition | Example |
|----------|----------|------------|---------|
| S1 Critical | 重大障害 | System down, all users affected, no workaround | Production server crash, data corruption |
| S2 Major | 重要障害 | Major function unavailable, significant users affected | Payment processing failure, login issues |
| S3 Moderate | 中度障害 | Function degraded, workaround available | Slow performance, report formatting error |
| S4 Minor | 軽微障害 | Cosmetic or low-impact issue | UI alignment, typo in message |

**SLA Targets by Support Tier:**

| SLA Metric | S1 | S2 | S3 | S4 |
|-----------|-----|-----|-----|-----|
| **Standard (9-18 JST, weekdays):** | | | | |
| Response time | 30 min | 1 hour | 4 hours | Next business day |
| Status update frequency | Every 1 hour | Every 2 hours | Daily | On resolution |
| Workaround target | 2 hours | 4 hours | 2 business days | 5 business days |
| Resolution target | 8 hours | 1 business day | 5 business days | 10 business days |
| **Premium (24/7/365):** | | | | |
| Response time | 15 min | 30 min | 2 hours | Next business day |
| Status update frequency | Every 30 min | Every 1 hour | Every 4 hours | On resolution |
| Workaround target | 1 hour | 2 hours | 1 business day | 3 business days |
| Resolution target | 4 hours | 8 hours | 3 business days | 7 business days |

**Availability SLA:**

| Tier | Target | Allowed Downtime/Month | Measurement |
|------|--------|----------------------|-------------|
| Standard | 99.5% | ~3.6 hours | Business hours only |
| Enhanced | 99.9% | ~43 minutes | 24/7 |
| Premium | 99.95% | ~22 minutes | 24/7 |

Exclusions: Planned maintenance windows, force majeure, client-caused issues, third-party service outages (outside our control).

### Step 4: Support Team Structure

**Standard Support Team:**

| Role | Allocation | Responsibility |
|------|-----------|----------------|
| Support Manager (保守責任者) | 0.1-0.2 人月 | Overall governance, escalation point, monthly reporting |
| Application Support Lead | 0.3-0.5 人月 | Incident management, change coordination, knowledge base |
| Application Engineer | 0.5-1.0 人月 | Bug fixes, minor enhancements, investigations |
| Infrastructure Engineer | 0.2-0.3 人月 | Server/network monitoring, patching, capacity management |
| Helpdesk Operator | 0.2-0.5 人月 | Tier 1 support, ticket routing, user communication |

**For 24/7 support, add:**
- On-call rotation (typically 3-4 engineers for continuous coverage)
- On-call allowance: ¥50,000-100,000/month per person
- After-hours incident response rate: 1.25-1.5x standard rate

### Step 5: Pricing Model

**Option A: Fixed Monthly Fee (月額定額)**
Best for: Stable systems, predictable workload

| Item | Monthly | Annual |
|------|---------|--------|
| Base support fee | ¥X,XXX,XXX | ¥XX,XXX,XXX |
| Included enhancement hours | 20 hours/month | 240 hours/year |
| Additional hours rate | ¥XX,XXX/hour | — |

**Option B: Tiered Service Plans**

| Feature | Bronze | Silver | Gold |
|---------|--------|--------|------|
| Support hours | 9-18 weekdays | 9-21 weekdays | 24/7/365 |
| Response SLA (S1) | 1 hour | 30 min | 15 min |
| Included hours | 10h/month | 20h/month | 40h/month |
| Proactive monitoring | — | Basic | Full |
| Monthly report | — | ✓ | ✓ |
| Quarterly review | — | — | ✓ |
| DR testing | — | Annual | Semi-annual |
| Monthly fee | ¥XXX,XXX | ¥X,XXX,XXX | ¥X,XXX,XXX |

**Option C: Incident-Based (従量制)**
Best for: Low-volume, non-critical systems

| Item | Rate |
|------|------|
| Retainer fee (minimum) | ¥XXX,XXX/month |
| S1 incident | ¥XXX,XXX/incident |
| S2 incident | ¥XXX,XXX/incident |
| S3/S4 incident | ¥XX,XXX/incident |
| Enhancement work | ¥XX,XXX/hour |

**Pricing Guidelines:**
- Annual maintenance typically 15-20% of original project cost
- 24/7 support adds 40-60% to base support cost
- Multi-year contracts: 5% discount for 3-year, 10% for 5-year commitment
- Payment: Monthly invoicing, 30-day payment terms typical

### Step 6: Governance & Reporting

**Regular Activities:**

| Activity | Frequency | Deliverable |
|----------|-----------|-------------|
| Incident report | Per incident (S1/S2) | 障害報告書 |
| Monthly report | Monthly | 月次保守報告書 |
| SLA achievement report | Monthly | SLA達成状況レポート |
| Service review meeting | Monthly or Quarterly | 保守定例会議事録 |
| System health assessment | Quarterly | システム健全性レポート |
| Annual maintenance plan | Annually | 年間保守計画書 |

**Monthly Report Contents:**
1. Incident summary (件数, severity distribution, resolution times)
2. SLA achievement rates vs. targets
3. Enhancement work completed (hours used vs. included)
4. System availability metrics
5. Upcoming planned maintenance
6. Risk and improvement recommendations

### Step 7: Transition Plan (移行計画)

**From Project Team to Maintenance Team:**

| Phase | Duration | Activities |
|-------|----------|-----------|
| Parallel Run | 1-2 months | Project team handles incidents with maintenance team shadowing |
| Gradual Transfer | 1 month | Maintenance team takes lead, project team as backup |
| Full Transfer | — | Maintenance team fully responsible, project team disbanded |

**Knowledge Transfer Requirements:**
- Architecture and design document walkthrough
- Operations manual (運用手順書) review
- Incident handling procedure training
- Access credential handover
- Monitoring tool training
- Known issues and workaround documentation

### Step 8: Output

Generate as .docx (using the `docx` skill):
1. Maintenance proposal document (保守提案書)
2. SLA agreement draft (SLA合意書)
3. Service catalog (サービスカタログ)
4. Transition plan (移行計画書)

## Key Principles

- **Maintenance is not an afterthought**: Propose it during the project, not after go-live
- **SLAs must be measurable**: If you can't measure it, don't promise it
- **Right-size the support**: Over-provisioning erodes margins; under-provisioning destroys reputation
- **Knowledge retention**: The biggest risk is losing the people who built the system
- **Proactive > reactive**: Finding problems before clients report them is what separates good support from great
- **Annual review**: Adjust SLAs and pricing annually based on actual incident volumes

For SLA templates and pricing calculation worksheets, read `references/maintenance-templates.md`.
