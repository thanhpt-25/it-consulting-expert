# Quality Metrics & KPIs

## Project Health Metrics

| Metric | Formula | Target | Red Flag |
|--------|---------|--------|----------|
| Schedule Performance Index (SPI) | Earned Value / Planned Value | ≥ 0.95 | < 0.85 |
| Cost Performance Index (CPI) | Earned Value / Actual Cost | ≥ 0.95 | < 0.85 |
| Scope Change Rate | # Change Requests / Month | ≤ 2/month | > 5/month |
| Risk Exposure | Σ (Probability × Impact) | Decreasing trend | Increasing |
| Team Velocity (Agile) | Story Points / Sprint | Stable ± 15% | > 30% variance |

## Code Quality Metrics

| Metric | Target | Measurement Tool |
|--------|--------|-----------------|
| Unit test coverage | > 80% | JaCoCo, Istanbul, coverage.py |
| Code complexity (cyclomatic) | < 10 per function | SonarQube, ESLint |
| Code duplication | < 3% | SonarQube, jscpd |
| Static analysis issues (critical) | 0 | SonarQube, Checkmarx |
| Technical debt ratio | < 5% | SonarQube |
| Build success rate | > 95% | CI/CD pipeline |
| Mean time to fix build | < 1 hour | CI/CD pipeline |

## Testing Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Test case pass rate | Passed / Total × 100 | > 95% per phase |
| Defect detection rate | Defects found / Total defects | > 85% before UAT |
| Defect density | Defects / KLOC or FP | < 5 per KLOC |
| Defect removal efficiency | Defects removed / Defects introduced | > 90% |
| Test execution progress | Executed / Planned × 100 | On schedule |
| Regression test pass rate | | 100% |

## Defect Severity Classification

| Severity | Japanese | Definition | Fix SLA |
|----------|---------|------------|---------|
| Critical (S1) | 致命的 | System down, data loss, security breach | 4 hours |
| Major (S2) | 重大 | Core function broken, no workaround | 1 business day |
| Minor (S3) | 軽微 | Function impaired but workaround exists | 3 business days |
| Cosmetic (S4) | 外観 | UI issues, typos, minor usability | Next release |

## Delivery Performance

| Metric | Target |
|--------|--------|
| On-time delivery rate | > 90% of milestones |
| Budget variance | Within ± 10% |
| Client satisfaction (CSAT) | ≥ 4.0 / 5.0 |
| Post-go-live incidents (first month) | < 5 critical |
| Warranty defects | Decreasing trend |
