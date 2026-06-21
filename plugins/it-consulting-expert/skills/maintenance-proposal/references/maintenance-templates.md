# Maintenance Templates (保守運用テンプレート)

## Incident Report Template (障害報告書)

```
■ 障害報告書

報告日: YYYY/MM/DD
報告者: [Name]
障害管理番号: INC-YYYY-NNN

1. 障害概要
   発生日時: YYYY/MM/DD HH:MM
   復旧日時: YYYY/MM/DD HH:MM (障害時間: X時間Y分)
   重要度: S1 / S2 / S3 / S4
   影響範囲: [affected users/functions]

2. 事象
   [What happened — objective description]

3. 原因
   [Root cause analysis result]
   直接原因: [immediate cause]
   根本原因: [underlying cause]

4. 対応内容
   [Timeline of response actions]
   HH:MM — 障害検知 / 連絡受領
   HH:MM — 調査開始
   HH:MM — 原因特定
   HH:MM — 対策実施
   HH:MM — 復旧確認

5. 再発防止策
   恒久対策: [permanent fix]
   実施予定日: YYYY/MM/DD
   横展開: [similar systems to check]

6. SLA影響
   対応時間: [actual vs SLA target]
   SLA遵守: Yes / No (if No, explain)
```

## SLA Calculation Guide

### Availability Calculation

```
Availability % = (Total Service Time - Downtime) / Total Service Time × 100

Business hours only (9-18 JST, weekdays):
- Monthly service hours ≈ 180 hours (9h × 20 days)
- 99.5% target = max 54 minutes downtime/month

24/7:
- Monthly service hours ≈ 720 hours (24h × 30 days)
- 99.9% target = max 43 minutes downtime/month
- 99.95% target = max 22 minutes downtime/month
```

### SLA Achievement Reporting

| Month | S1 Response | S1 Target | Met? | S2 Response | S2 Target | Met? |
|-------|------------|-----------|------|------------|-----------|------|
| Jan | Average Xm | 30m | ✓/✗ | Average Xm | 60m | ✓/✗ |
| Feb | | | | | | |

**SLA Breach Penalty Calculation (if applicable):**

| Metric | Target | Actual | Breach | Credit |
|--------|--------|--------|--------|--------|
| Availability | 99.9% | 99.7% | 0.2% | 5% of monthly fee |
| S1 Response | 30 min | 45 min | 15 min over | 2% of monthly fee |

Typical penalty caps: 10-20% of monthly maintenance fee per month.

## Pricing Calculation Worksheet

### Step 1: Base Staffing Cost

| Role | Allocation (人月) | Monthly Rate (¥) | Monthly Cost (¥) |
|------|------------------|-------------------|-------------------|
| Support Manager | 0.15 | 1,500,000 | 225,000 |
| App Support Lead | 0.4 | 1,200,000 | 480,000 |
| App Engineer | 0.8 | 1,000,000 | 800,000 |
| Infra Engineer | 0.25 | 1,100,000 | 275,000 |
| Helpdesk | 0.3 | 700,000 | 210,000 |
| **Subtotal** | **1.9** | | **1,990,000** |

### Step 2: Add-ons

| Item | Cost (¥/month) |
|------|----------------|
| On-call allowance (if 24/7) | 200,000 |
| Monitoring tools/licenses | 100,000 |
| Communication tools | 30,000 |
| Knowledge base maintenance | 50,000 |
| **Subtotal** | **380,000** |

### Step 3: Margin & Final Price

| Item | Amount (¥) |
|------|-----------|
| Direct cost | 2,370,000 |
| Overhead (15%) | 355,500 |
| Margin (20-25%) | 545,100 |
| **Monthly fee** | **3,270,600** |
| **Annual fee** | **39,247,200** |

## Maintenance Contract Renewal Checklist

### 3 Months Before Renewal
- [ ] Compile annual SLA achievement data
- [ ] Calculate actual incident volumes vs. projections
- [ ] Assess system stability trends
- [ ] Identify upcoming technology changes (EOL, upgrades needed)
- [ ] Review staffing levels vs. actual workload
- [ ] Prepare renewal proposal with any scope/price adjustments

### 1 Month Before Renewal
- [ ] Present renewal proposal to client
- [ ] Negotiate terms and pricing
- [ ] Confirm key personnel availability
- [ ] Update SLA targets if needed
- [ ] Draft new contract or amendment

### At Renewal
- [ ] Sign new contract
- [ ] Update service catalog if scope changed
- [ ] Communicate changes to support team
- [ ] Update monitoring thresholds if SLAs changed

## Integration with Other Skills

- **effort-estimation**: For sizing enhancement work within maintenance
- **cost-estimation**: For pricing maintenance services with proper rate cards
- **progress-report**: Monthly maintenance reports follow similar format
- **change-request**: Enhancement requests within maintenance use the CR process
- **technical-solution**: For architecture decisions within maintenance scope
