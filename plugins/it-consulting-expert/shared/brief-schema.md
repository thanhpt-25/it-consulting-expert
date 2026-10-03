# RFP Brief schema — `00-rfp-brief.json`

The Brief is the canonical extraction of the client's RFP/RFQ. `rfp-notebook` writes it; every other
skill reads it. `sier brief validate` enforces the rules below; `sier brief render` produces the
human-readable `00-rfp-brief.md`.

## Items and labels

Almost every fact is an **item**:

```json
{"text": "可用性 99.9%", "label": "RFP", "citation": "RFP §4.1 p.18"}
```

| Label | Meaning | Citation |
|---|---|---|
| `RFP` | Stated in the client's documents | **Required** |
| `RFP+` | Client requirement plus our extension | **Required** (for the client part) |
| `Proposed` | Our assumption or recommendation; the RFP is silent | Not required |

Citation format: the NotebookLM reference text when extracted at tiers 1–2; `RFP §x.y p.N` (or the
appendix/Q&A document name) when read directly at tier 3. An uncited fact cannot be `[RFP]` —
validation fails. An assumption can never be `RFP`.

## Top level

| Field | Type | Rule |
|---|---|---|
| `schema_version` | 1 | required |
| `client`, `project` | string | required |
| `generated_at` | `YYYY-MM-DD` | required |
| `source_tier` | 1–4 | required — see `notebooklm-contract.md` §4 |
| `notebook_id` | string \| null | |
| `sources` | `[{id, title, type}]` | every document loaded |

## Sections

| Section | Shape |
|---|---|
| `overview.background` | item |
| `overview.objectives`, `scope_in`, `scope_out`, `scope_ambiguous`, `success_criteria` | item[] |
| `functional_requirements` | `[{id: "FR-001", text, module, priority: must\|should\|may, label, citation}]` |
| `nonfunctional_requirements` | `[{id: "NFR-001", category, text, target, label, citation}]` — category ∈ performance, availability, security, scalability, usability, accessibility, maintainability, compliance, operability, data, other |
| `constraints`, `data_migration` | item[] |
| `integrations` | `[{id: "INT-001", system, type, protocol, label, citation}]` |
| `timeline.proposal_submission`, `contract_start`, `go_live` | item with optional `date` |
| `timeline.milestones` | `[{name, date, label, citation}]` |
| `commercial.budget` | `{amount, basis: tax_excluded\|tax_included, label, citation}` — `amount: null` when unstated |
| `commercial.pricing_model`, `payment_terms` | item |
| `evaluation.criteria` | `[{name, weight, label, citation}]` — weights should sum to 100 |
| `evaluation.submission_requirements`, `mandatory_qualifications` | item[] |
| `team_process.staffing`, `governance` | item[] |
| `team_process.methodology` | item |
| `risks`, `contract_terms`, `assumptions` | item[] |
| `gaps` | `[{id: "Q-001", topic, question, priority: high\|medium\|low, blocks: [skill names]}]` |

IDs are unique across the Brief. `blocks` names the skills that cannot finish without the answer —
`sier brief gaps --for <skill>` reads it, so downstream skills query NotebookLM only when blocked.

## Minimal valid example

```json
{
  "schema_version": 1, "client": "ABC製造株式会社", "project": "CRMクラウド移行",
  "generated_at": "2026-07-01", "source_tier": 1, "notebook_id": "3f2a…", "sources": [{"id": "S1", "title": "RFP.pdf", "type": "pdf"}],
  "functional_requirements": [
    {"id": "FR-001", "text": "顧客・商談管理", "module": "CRM", "priority": "must", "label": "RFP", "citation": "[1] 顧客情報および商談情報を一元管理すること"}
  ],
  "commercial": {"budget": {"amount": 200000000, "basis": "tax_excluded", "label": "RFP", "citation": "[4] 予算上限2億円（税抜）"}},
  "assumptions": [{"text": "EDI形式は2種類", "label": "Proposed"}],
  "gaps": [{"id": "Q-001", "topic": "EDI", "question": "EDIパートナー数と形式は？", "priority": "high", "blocks": ["effort-estimation"]}]
}
```

A complete example: `tests/fixtures/abc-manufacturing/00-rfp-brief.json` in the repository.
