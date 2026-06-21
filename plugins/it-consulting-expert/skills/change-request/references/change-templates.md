# Change Request Templates (変更管理テンプレート)

## CR Numbering Convention

Format: `CR-[Project Code]-[YYYY]-[NNN]`
- Sequential within project
- Never reuse numbers, even for rejected CRs
- Example: CR-PROJ01-2024-001

## Change Category Classification

| Category | Japanese | Typical Impact | Approval Level |
|----------|----------|---------------|----------------|
| Scope Addition | スコープ追加 | High cost/schedule | Director+ |
| Scope Modification | 仕様変更 | Medium cost/schedule | PM or Director |
| Scope Removal | スコープ削除 | Schedule benefit, potential quality risk | PM |
| Technical Change | 技術変更 | Variable | PM or Director |
| Process Change | プロセス変更 | Usually low | PM |
| Timeline Change | スケジュール変更 | Schedule only | Director+ if go-live affected |

## Effort Estimation Quick Guide for Changes

When estimating additional effort for a change, use these multipliers:

**Design phase changes (要件定義・基本設計中):**
- Effort = Base effort × 1.0 (cheapest time to change)
- Impact: Low — design documents updated, no rework

**Development phase changes (詳細設計・製造中):**
- Effort = Base effort × 1.5–2.0 (redesign + rework)
- Impact: Medium — code rework, test case updates

**Testing phase changes (テスト中):**
- Effort = Base effort × 2.5–4.0 (rework + retest + regression)
- Impact: High — potential test cycle reset

**Post-deployment changes (リリース後):**
- Effort = Base effort × 5.0+ (full cycle impact)
- Impact: Very High — emergency release process

## Communication Templates

### CR Submission Email (to Client)

```
件名: 【変更依頼】[Project Name] CR-YYYY-NNN: [Change Title]

[Client Name] 御中

いつもお世話になっております。
[Your Company] [Your Name]です。

下記の変更依頼書を提出いたします。

■ 変更依頼番号: CR-YYYY-NNN
■ 変更概要: [1-2 sentence summary]
■ 影響概要: スケジュール [+X日] / コスト [+¥X]
■ 回答期限: [Date] — この日までにご判断いただけますと、
  現行スケジュールへの影響を最小限に抑えられます。

詳細は添付の変更依頼書をご確認ください。
ご不明な点がございましたら、お気軽にお問い合わせください。

よろしくお願いいたします。
```

### CR Approval Confirmation (from Client)

```
件名: 【承認】CR-YYYY-NNN: [Change Title]

[Your Company] 御中

CR-YYYY-NNN について、Option [A/B] にて承認いたします。
変更後のスケジュール・コストについて、了承いたしました。

承認者: [Name], [Title]
承認日: [Date]
```

### CR Rejection Notification

```
件名: 【CR却下のご連絡】CR-YYYY-NNN

[Client Name] 御中

CR-YYYY-NNN について、ご検討の結果、却下とのご判断を承りました。
当該変更は実施せず、現行スコープにて進行いたします。

なお、本件に関連する潜在リスクとして [risk] がございますので、
今後の進行において注視してまいります。

よろしくお願いいたします。
```

## Change Control Board (CCB) Meeting Agenda

For projects with formal CCB governance:

1. **Review pending CRs** — Present each CR with impact summary
2. **Cumulative impact review** — Show dashboard of total baseline deviation
3. **Priority ranking** — If multiple CRs compete for budget/timeline
4. **Decision recording** — Document approved/rejected/deferred with rationale
5. **Action items** — Assign next steps for approved CRs

Typical CCB cadence: Bi-weekly for large projects, ad-hoc for smaller ones.

## Dispute Resolution

When client and vendor disagree on whether something is "in scope":

1. **Reference the RFP**: Quote the specific section. If ambiguous, acknowledge it
2. **Check meeting minutes**: Was this discussed and clarified during requirements?
3. **Propose compromise**: Split the cost, defer to Phase 2, or reduce scope elsewhere
4. **Escalate gracefully**: If unresolved, escalate to steering committee with both positions documented
5. **Never burn the relationship**: Being right about scope matters less than keeping the client

## Integration with Other Skills

- **effort-estimation**: Use for calculating additional effort in the CR
- **cost-estimation**: Use for pricing the change with proper rate cards
- **progress-report**: CRs appear in the weekly report's Change Request section
- **create-proposal**: Original baseline comes from the proposal
