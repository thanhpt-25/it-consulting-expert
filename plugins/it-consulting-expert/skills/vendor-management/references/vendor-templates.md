# Vendor Management Templates (協力会社管理テンプレート)

## Contract Checklist for Subcontractor Agreements

### Essential Contract Clauses

| Clause | Japanese | Purpose |
|--------|----------|---------|
| Scope of Work | 業務委託内容 | Define exactly what work is delegated |
| Deliverables | 成果物一覧 | List all expected outputs with acceptance criteria |
| Term & Schedule | 契約期間・スケジュール | Start/end dates, milestone deadlines |
| Pricing & Payment | 委託費・支払条件 | Unit prices, payment schedule, invoice process |
| Personnel | 要員 | Key personnel names, replacement approval process |
| Re-delegation | 再委託 | Whether sub can further delegate (usually prohibited) |
| Confidentiality | 秘密保持 | NDA scope, duration (typically 3-5 years post-contract) |
| IP Ownership | 知的財産権 | Work-for-hire: all IP belongs to prime contractor |
| Security | セキュリティ | Data handling, access controls, incident reporting |
| Quality Standards | 品質基準 | Coding standards, testing requirements, review process |
| Warranty | 瑕疵担保 | Defect liability period (typically 1 year post-delivery) |
| Liability | 損害賠償 | Cap (typically contract value), exclusions |
| Termination | 解約 | Conditions for early termination, notice period |
| Force Majeure | 不可抗力 | Natural disasters, pandemics, regulatory changes |

### Contract Type Selection

| Type | Japanese | When to Use | Risk Distribution |
|------|----------|-------------|-------------------|
| Deliverable-based (請負) | 請負契約 | Clear scope, defined deliverables | Vendor bears delivery risk |
| Time & Materials (準委任) | 準委任契約 | Advisory, ongoing support, unclear scope | Client bears scope risk |
| SES (技術者派遣) | 派遣契約 | Staff augmentation, client-directed work | Client bears management responsibility |

## Vendor Onboarding Checklist

### Week 1: Administrative Setup
- [ ] Contract signed (押印済み)
- [ ] NDA executed
- [ ] Key personnel identified and CVs received
- [ ] Security training completed
- [ ] Development environment access provisioned
- [ ] Communication tools setup (email, chat, ticket system)
- [ ] Project materials shared (design docs, coding standards)

### Week 2: Technical Alignment
- [ ] Architecture overview session conducted
- [ ] Coding standards and naming conventions reviewed
- [ ] Development workflow walkthrough (branch strategy, review process)
- [ ] CI/CD pipeline explained and access verified
- [ ] Test environment confirmed working
- [ ] First task assigned as proof of setup

### Ongoing
- [ ] Weekly status meeting scheduled
- [ ] Quality review process confirmed
- [ ] Escalation contacts exchanged
- [ ] First deliverable reviewed with detailed feedback

## Vendor Exit Checklist

When a subcontractor engagement ends:

- [ ] All source code committed and merged
- [ ] Knowledge transfer sessions completed (recorded)
- [ ] Documentation updated to reflect current state
- [ ] Access revoked (all systems, VPN, tools)
- [ ] Company equipment returned
- [ ] Confidential documents returned or certifiably destroyed
- [ ] Final invoice received and processed
- [ ] Performance review completed and filed
- [ ] Post-engagement NDA obligations confirmed
- [ ] Client notified of team change (if required)

## Offshore Quality Assurance Checklist

### Before Sending Work Offshore
- [ ] Requirements documented in English (not just Japanese meeting notes)
- [ ] Acceptance criteria defined per deliverable
- [ ] Sample/reference deliverables provided
- [ ] Coding standards document translated
- [ ] Bridge SE briefed and aligned

### During Offshore Development
- [ ] Daily standup happening (Bridge SE confirms)
- [ ] Code committed daily (visible in repository)
- [ ] Questions logged and answered within 24h
- [ ] Weekly deliverable review by prime contractor

### Before Accepting Offshore Deliverables
- [ ] Bridge SE pre-review completed
- [ ] Code review by prime contractor engineer
- [ ] Unit test coverage meets threshold
- [ ] Integration test in combined environment passed
- [ ] Documentation in Japanese (or translated by Bridge SE)

## Communication Escalation Matrix

| Issue Type | First Contact | Escalation 1 | Escalation 2 | Max Resolution |
|-----------|--------------|--------------|--------------|----------------|
| Technical question | Sub-engineer → Bridge SE | Sub-PM → Prime Tech Lead | — | 4 hours |
| Task blocker | Sub-PM → Prime PM | — | — | 1 business day |
| Quality issue | Prime QA → Sub-PM | Prime PM → Sub Director | Prime Director → Sub Exec | 1 week |
| Resource issue | Sub-PM → Prime PM | Sub Director → Prime Director | — | 2 weeks |
| Contract dispute | Prime PM → Sub-PM | Prime Director → Sub Director | Legal → Legal | 1 month |
| Security incident | Immediate: Sub-PM → Prime PM → Client | All levels simultaneously | — | Immediate |
