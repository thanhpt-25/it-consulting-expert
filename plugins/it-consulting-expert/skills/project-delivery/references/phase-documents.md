# Phase Document Templates

## Phase Gate Checklist

Each phase transition requires these checks:

### Requirements → Basic Design Gate
- [ ] All business requirements documented and signed off
- [ ] Non-functional requirements defined with measurable targets
- [ ] Scope boundary clearly defined (in/out of scope)
- [ ] Stakeholder sign-off obtained
- [ ] Requirements traceability matrix created
- [ ] Risk register initialized

### Basic Design → Detailed Design Gate
- [ ] System architecture approved by client technical team
- [ ] Screen designs reviewed with end users
- [ ] Database logical design reviewed
- [ ] Interface specifications agreed with external system owners
- [ ] Basic design documents version-controlled
- [ ] Updated effort estimate reflects design decisions

### Detailed Design → Implementation Gate
- [ ] All program specifications written
- [ ] Coding standards documented and shared
- [ ] Development environment fully set up
- [ ] CI/CD pipeline operational
- [ ] Team onboarding complete
- [ ] Unit test strategy defined

### Implementation → Testing Gate
- [ ] All code committed and passing unit tests
- [ ] Code coverage meets threshold (typically > 80%)
- [ ] Code review completed for all modules
- [ ] Integration test environment ready
- [ ] Test data prepared
- [ ] Test cases reviewed and approved

### Testing → Deployment Gate
- [ ] All test phases complete with acceptable pass rate
- [ ] Critical and major defects resolved
- [ ] Performance test results meet NFR targets
- [ ] Security assessment passed
- [ ] UAT sign-off obtained
- [ ] Migration plan tested (dry run complete)
- [ ] Rollback procedure documented and tested
- [ ] Operations team trained
- [ ] User documentation delivered

## Weekly Status Report Template (週次報告書)

```
# Weekly Status Report - Week of [DATE]

## Summary
- Overall Status: [Green/Yellow/Red]
- Schedule: [On Track / X days behind]
- Budget: [Within budget / X% over]

## This Week's Accomplishments
1. [Completed item]
2. [Completed item]

## Next Week's Plan
1. [Planned item]
2. [Planned item]

## Issues & Risks
| ID | Description | Severity | Owner | Action | Due |
|----|-------------|----------|-------|--------|-----|

## Decisions Needed
| Decision | Options | Recommendation | Deadline |
|----------|---------|---------------|----------|

## Metrics
- Tasks completed: X/Y
- Defects: X open (Y critical)
- Test progress: X% complete
```

## Change Request Template (変更依頼書)

```
# Change Request #[NUMBER]

## Request Details
- Requested by: [Name]
- Date: [DATE]
- Priority: [Critical/High/Medium/Low]

## Description of Change
[What needs to change and why]

## Impact Analysis
- Schedule impact: [+X days/weeks]
- Cost impact: [+¥X,XXX,XXX]
- Quality impact: [Description]
- Scope impact: [What's added/removed]

## Affected Deliverables
- [Document/module affected]

## Recommendation
[Approve / Reject / Defer with rationale]

## Approval
| Role | Name | Decision | Date |
|------|------|----------|------|
| Client PM | | | |
| Project PM | | | |
| Sponsor | | | |
```
