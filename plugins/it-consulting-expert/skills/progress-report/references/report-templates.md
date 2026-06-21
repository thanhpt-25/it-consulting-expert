# Report Templates

## Status Color Decision Guide

### Schedule Status
| Condition | Color |
|-----------|-------|
| ≤ 2 days behind plan AND recovery plan exists | 🟢 Green |
| 3-5 days behind OR behind but recoverable this phase | 🟡 Yellow |
| > 5 days behind OR affects milestone date | 🔴 Red |

### Quality Status
| Condition | Color |
|-----------|-------|
| Defect density within target, test progress on track | 🟢 Green |
| Defect density 10-20% over target OR minor test delays | 🟡 Yellow |
| Critical defects open > 48h OR defect density > 20% over target | 🔴 Red |

### Cost Status
| Condition | Color |
|-----------|-------|
| Within ±5% of budget | 🟢 Green |
| 5-10% over budget OR trending over | 🟡 Yellow |
| > 10% over budget OR forecast exceeds approved budget | 🔴 Red |

## EVM Quick Reference

| Metric | Formula | Good | Warning |
|--------|---------|------|---------|
| SPI | EV / PV | ≥ 0.95 | < 0.85 |
| CPI | EV / AC | ≥ 0.95 | < 0.85 |
| EAC | BAC / CPI | ≤ BAC × 1.1 | > BAC × 1.2 |
| TCPI | (BAC - EV) / (BAC - AC) | ≤ 1.1 | > 1.2 |

Where:
- EV = Earned Value (value of completed work)
- PV = Planned Value (value of work planned to be complete)
- AC = Actual Cost (actual cost spent)
- BAC = Budget at Completion (total budget)
- EAC = Estimate at Completion (projected total cost)
- TCPI = To-Complete Performance Index (required efficiency to finish on budget)

## Escalation Language Guide

**For Yellow items (client report):**
"[Issue] が発生しておりますが、[mitigation action] を実施中であり、[target date] までに解消見込みです。"

**For Red items (client report):**
"[Issue] により [impact] が見込まれます。対策として [options] をご検討いただきたく、[date] までにご判断をお願いいたします。"

**For internal escalation:**
"[Issue] — Impact: [schedule/cost/quality impact]. Current mitigation: [action]. Escalation needed because: [why current plan isn't sufficient]. Recommended action: [specific ask]."
