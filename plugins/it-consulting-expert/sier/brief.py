"""The structured RFP Brief: 00-rfp-brief.json is canonical, 00-rfp-brief.md is rendered from it.

Every fact is an item with a grounding label:
    {"text": "...", "label": "RFP" | "Proposed" | "RFP+", "citation": "..."}
An item labelled RFP or RFP+ must carry a citation (a NotebookLM reference, or a page/section
reference when the Brief was produced from the source files directly — fallback tier 3).
"""
from __future__ import annotations

import re
from typing import Any

from common import D, Findings, SierError, md_table, parse_date, yen

LABELS = {"RFP", "Proposed", "RFP+"}
PRIORITIES = {"must", "should", "may"}
GAP_PRIORITIES = {"high", "medium", "low"}
NFR_CATEGORIES = {"performance", "availability", "security", "scalability", "usability",
                  "accessibility", "maintainability", "compliance", "operability", "data", "other"}
SKILLS = {"rfp-analysis", "create-proposal", "technical-solution", "effort-estimation", "cost-estimation",
          "team-composition", "project-delivery", "proposal-presentation", "design-presentation",
          "proposal-review", "change-request", "vendor-management", "maintenance-proposal",
          "progress-report", "lessons-learned"}

ID_PATTERNS = {
    "functional_requirements": re.compile(r"^FR-\d{3,}$"),
    "nonfunctional_requirements": re.compile(r"^NFR-\d{3,}$"),
    "integrations": re.compile(r"^INT-\d{3,}$"),
    "gaps": re.compile(r"^Q-\d{3,}$"),
}

# Which Brief fields each downstream skill depends on. Drives `sier brief gaps --for <skill>`
# and the "readiness" table, so a skill knows exactly what it may need to query.
SKILL_INPUTS = {
    "rfp-analysis": ["evaluation.criteria", "evaluation.mandatory_qualifications", "commercial.budget",
                     "timeline.proposal_submission", "risks", "contract_terms"],
    "technical-solution": ["nonfunctional_requirements", "constraints", "integrations", "data_migration"],
    "effort-estimation": ["functional_requirements", "nonfunctional_requirements", "integrations",
                          "data_migration", "timeline.go_live"],
    "team-composition": ["team_process.staffing", "team_process.methodology", "timeline.go_live"],
    "cost-estimation": ["commercial.budget", "commercial.pricing_model", "commercial.payment_terms"],
    "project-delivery": ["team_process.methodology", "team_process.governance", "timeline.milestones"],
    "create-proposal": ["overview.objectives", "overview.scope_in", "evaluation.submission_requirements"],
}


def _item_ok(f: Findings, where: str, item: Any, allow_null_text: bool = False) -> None:
    if not isinstance(item, dict):
        f.error(f"{where}: expected an object with text/label/citation, got {type(item).__name__}")
        return
    if not allow_null_text and not str(item.get("text", "")).strip():
        f.error(f"{where}: missing text")
    label = item.get("label")
    if label not in LABELS:
        f.error(f"{where}: label must be one of RFP / Proposed / RFP+, got {label!r}")
    elif label in ("RFP", "RFP+") and not str(item.get("citation") or "").strip():
        f.error(f"{where}: labelled {label} but has no citation — an uncited fact cannot be [RFP]")


def _items(f: Findings, data: dict, path: str) -> list:
    cur: Any = data
    for part in path.split("."):
        if not isinstance(cur, dict):
            return []
        cur = cur.get(part)
    if cur is None:
        return []
    if isinstance(cur, list):
        for i, it in enumerate(cur):
            _item_ok(f, f"{path}[{i}]", it)
        return cur
    _item_ok(f, path, cur)
    return [cur]


def validate(data: dict) -> Findings:
    f = Findings()
    if not isinstance(data, dict):
        f.error("Brief must be a JSON object")
        return f
    for key in ("schema_version", "client", "project", "generated_at", "source_tier"):
        if data.get(key) in (None, ""):
            f.error(f"missing top-level field: {key}")
    if data.get("source_tier") not in (None, 1, 2, 3, 4):
        f.error("source_tier must be 1 (notebooklm CLI), 2 (notebooklm-web), 3 (direct file read) or 4 (user)")
    if data.get("source_tier") == 4:
        f.warn("source_tier 4: nothing was read from the RFP itself — every [RFP] label must be re-checked")
    if data.get("generated_at"):
        try:
            parse_date(data["generated_at"], "generated_at")
        except SierError as e:
            f.error(str(e))

    seen: set[str] = set()

    def check_ids(section: str, rows: list) -> None:
        pat = ID_PATTERNS[section]
        for i, r in enumerate(rows):
            rid = r.get("id") if isinstance(r, dict) else None
            if not rid or not pat.match(str(rid)):
                f.error(f"{section}[{i}]: id {rid!r} does not match {pat.pattern}")
            elif rid in seen:
                f.error(f"{section}[{i}]: duplicate id {rid}")
            else:
                seen.add(rid)

    frs = data.get("functional_requirements") or []
    check_ids("functional_requirements", frs)
    for i, r in enumerate(frs):
        _item_ok(f, f"functional_requirements[{i}]", r)
        if isinstance(r, dict) and r.get("priority") not in PRIORITIES:
            f.error(f"functional_requirements[{i}] ({r.get('id')}): priority must be must/should/may")
    if not frs:
        f.warn("no functional requirements recorded — effort-estimation will have nothing to trace to")

    nfrs = data.get("nonfunctional_requirements") or []
    check_ids("nonfunctional_requirements", nfrs)
    for i, r in enumerate(nfrs):
        _item_ok(f, f"nonfunctional_requirements[{i}]", r)
        if isinstance(r, dict) and r.get("category") not in NFR_CATEGORIES:
            f.error(f"nonfunctional_requirements[{i}] ({r.get('id')}): category {r.get('category')!r} not in {sorted(NFR_CATEGORIES)}")

    ints = data.get("integrations") or []
    check_ids("integrations", ints)
    for i, r in enumerate(ints):
        _item_ok(f, f"integrations[{i}]", {**r, "text": r.get("system")} if isinstance(r, dict) else r)

    for path in ("overview.background", "overview.objectives", "overview.scope_in", "overview.scope_out",
                 "overview.scope_ambiguous", "overview.success_criteria", "constraints", "data_migration",
                 "commercial.pricing_model", "commercial.payment_terms", "evaluation.submission_requirements",
                 "evaluation.mandatory_qualifications", "team_process.staffing", "team_process.methodology",
                 "team_process.governance", "risks", "contract_terms", "assumptions"):
        _items(f, data, path)

    for i, a in enumerate(data.get("assumptions") or []):
        if isinstance(a, dict) and a.get("label") == "RFP":
            f.error(f"assumptions[{i}]: an assumption cannot be labelled RFP — it is by definition not stated")

    tl = data.get("timeline") or {}
    for k in ("proposal_submission", "contract_start", "go_live"):
        v = tl.get(k)
        if v:
            _item_ok(f, f"timeline.{k}", v, allow_null_text=True)
            if isinstance(v, dict) and v.get("date"):
                try:
                    parse_date(v["date"], f"timeline.{k}.date")
                except SierError as e:
                    f.error(str(e))
    for i, m in enumerate(tl.get("milestones") or []):
        _item_ok(f, f"timeline.milestones[{i}]", {**m, "text": m.get("name")} if isinstance(m, dict) else m)

    budget = (data.get("commercial") or {}).get("budget")
    if budget:
        _item_ok(f, "commercial.budget", budget, allow_null_text=True)
        amt = budget.get("amount") if isinstance(budget, dict) else None
        if amt is not None:
            try:
                if D(amt) <= 0:
                    f.error("commercial.budget.amount must be positive")
            except SierError as e:
                f.error(f"commercial.budget.amount: {e}")
            if budget.get("basis") not in ("tax_excluded", "tax_included"):
                f.error("commercial.budget.basis must be tax_excluded or tax_included when an amount is given")

    crit = (data.get("evaluation") or {}).get("criteria") or []
    weights = []
    for i, c in enumerate(crit):
        _item_ok(f, f"evaluation.criteria[{i}]", {**c, "text": c.get("name")} if isinstance(c, dict) else c)
        if isinstance(c, dict) and c.get("weight") is not None:
            weights.append(D(c["weight"]))
    if weights and len(weights) == len(crit):
        total = sum(weights)
        if abs(total - 100) > D("0.5") and abs(total - 1) > D("0.005"):
            f.warn(f"evaluation criteria weights sum to {total}, not 100% — check the extraction")

    gaps = data.get("gaps") or []
    check_ids("gaps", gaps)
    for i, g in enumerate(gaps):
        if not isinstance(g, dict):
            continue
        if not str(g.get("question", "")).strip():
            f.error(f"gaps[{i}]: missing question")
        if g.get("priority") not in GAP_PRIORITIES:
            f.error(f"gaps[{i}]: priority must be high/medium/low")
        for s in g.get("blocks") or []:
            if s not in SKILLS:
                f.error(f"gaps[{i}]: blocks unknown skill {s!r}")
    return f


def gaps_for(data: dict, skill: str | None) -> list[dict]:
    gaps = data.get("gaps") or []
    if not skill:
        return gaps
    if skill not in SKILLS:
        raise SierError(f"Unknown skill {skill!r}. Known: {', '.join(sorted(SKILLS))}")
    return [g for g in gaps if skill in (g.get("blocks") or [])]


def _get(data: dict, path: str) -> Any:
    cur: Any = data
    for part in path.split("."):
        if not isinstance(cur, dict):
            return None
        cur = cur.get(part)
    return cur


def readiness(data: dict) -> list[list[str]]:
    rows = []
    for skill, fields in SKILL_INPUTS.items():
        missing = [p for p in fields if not _get(data, p)]
        open_gaps = [g["id"] for g in gaps_for(data, skill)]
        status = "✅" if not missing and not open_gaps else "⚠️"
        rows.append([skill, status, ", ".join(missing) or "—", ", ".join(open_gaps) or "—"])
    return rows


def _lbl(it: Any) -> str:
    if not isinstance(it, dict):
        return str(it)
    cite = f" — {it['citation']}" if it.get("citation") else ""
    return f"{it.get('text', '')} `[{it.get('label', '?')}]`{cite}"


def _bullets(items: Any) -> str:
    if not items:
        return "_Not specified in the RFP._"
    items = items if isinstance(items, list) else [items]
    return "\n".join(f"- {_lbl(i)}" for i in items)


def render(data: dict) -> str:
    ov = data.get("overview") or {}
    tl = data.get("timeline") or {}
    com = data.get("commercial") or {}
    ev = data.get("evaluation") or {}
    tp = data.get("team_process") or {}
    tier_names = {1: "NotebookLM CLI", 2: "NotebookLM web", 3: "direct read of source files", 4: "user-provided"}
    out = [
        f"# RFP Brief: {data.get('client')} — {data.get('project')}",
        "# RFPブリーフィング", "",
        f"**Generated:** {data.get('generated_at')}  ",
        f"**Source tier:** {data.get('source_tier')} ({tier_names.get(data.get('source_tier'), '?')})  ",
        f"**Notebook:** `{data.get('notebook_id') or '—'}`  ",
        f"**Sources:** {len(data.get('sources') or [])}", "",
        "> Rendered from `00-rfp-brief.json` by `sier brief render`. Edit the JSON, not this file.", "",
        "## 1. Project Overview (案件概要)", "",
        "### Background & Objectives", _bullets([ov.get("background")] if ov.get("background") else []),
        _bullets(ov.get("objectives")), "",
        "### Scope — in", _bullets(ov.get("scope_in")), "",
        "### Scope — out", _bullets(ov.get("scope_out")), "",
        "### Scope — ambiguous (clarify with client)", _bullets(ov.get("scope_ambiguous")), "",
        "### Success criteria", _bullets(ov.get("success_criteria")), "",
        "## 2. Requirements (要件)", "",
        "### 2.1 Functional", "",
    ]
    frs = data.get("functional_requirements") or []
    out.append(md_table(["ID", "Requirement", "Module", "Priority", "Label", "Source"],
                        [[r.get("id"), r.get("text"), r.get("module", ""), r.get("priority"), r.get("label"),
                          r.get("citation", "")] for r in frs]) if frs else "_None recorded._")
    nfrs = data.get("nonfunctional_requirements") or []
    out += ["", "### 2.2 Non-functional", ""]
    out.append(md_table(["ID", "Category", "Requirement", "Target", "Label", "Source"],
                        [[r.get("id"), r.get("category"), r.get("text"), r.get("target", ""), r.get("label"),
                          r.get("citation", "")] for r in nfrs]) if nfrs else "_None recorded._")
    out += ["", "### 2.3 Constraints", _bullets(data.get("constraints")), "",
            "### 2.4 Integrations", ""]
    ints = data.get("integrations") or []
    out.append(md_table(["ID", "System", "Type", "Protocol", "Label", "Source"],
                        [[r.get("id"), r.get("system"), r.get("type", ""), r.get("protocol", ""), r.get("label"),
                          r.get("citation", "")] for r in ints]) if ints else "_None recorded._")
    out += ["", "### 2.5 Data migration", _bullets(data.get("data_migration")), "",
            "## 3. Timeline (スケジュール)", ""]
    trows = []
    for k, name in (("proposal_submission", "Proposal submission"), ("contract_start", "Contract start"),
                    ("go_live", "Go-live")):
        v = tl.get(k)
        if v:
            trows.append([name, v.get("date") or v.get("text", ""), v.get("label"), v.get("citation", "")])
    for m in tl.get("milestones") or []:
        trows.append([m.get("name"), m.get("date", ""), m.get("label"), m.get("citation", "")])
    out.append(md_table(["Milestone", "Date", "Label", "Source"], trows) if trows else "_No dates stated._")
    b = com.get("budget") or {}
    budget_txt = (f"{yen(b['amount'])} ({b.get('basis', '?').replace('_', ' ')}) `[{b.get('label')}]` — {b.get('citation', '')}"
                  if b.get("amount") is not None else "_Not specified in the RFP._")
    out += ["", "## 4. Commercial (予算・商務)", "", f"- **Budget:** {budget_txt}",
            f"- **Pricing model:** {_lbl(com['pricing_model']) if com.get('pricing_model') else '_Not specified._'}",
            f"- **Payment terms:** {_lbl(com['payment_terms']) if com.get('payment_terms') else '_Not specified._'}",
            "", "## 5. Evaluation & Submission (評価・提出)", ""]
    crit = ev.get("criteria") or []
    out.append(md_table(["Criterion", "Weight", "Label", "Source"],
                        [[c.get("name"), c.get("weight", "—"), c.get("label"), c.get("citation", "")] for c in crit])
               if crit else "_Evaluation criteria not stated._")
    out += ["", "### Submission requirements", _bullets(ev.get("submission_requirements")), "",
            "### Mandatory qualifications", _bullets(ev.get("mandatory_qualifications")), "",
            "## 6. Team & Process (体制・プロセス)", "",
            "### Staffing", _bullets(tp.get("staffing")), "",
            "### Methodology", _bullets(tp.get("methodology")), "",
            "### Governance", _bullets(tp.get("governance")), "",
            "## 7. Risks & Contract (リスク・契約)", "",
            "### Risks", _bullets(data.get("risks")), "",
            "### Contract terms", _bullets(data.get("contract_terms")), "",
            "### Assumptions", _bullets(data.get("assumptions")), "",
            "## 8. Gaps & Clarifications (不明点・要確認事項)", ""]
    gaps = data.get("gaps") or []
    out.append(md_table(["ID", "Topic", "Question", "Priority", "Blocks"],
                        [[g.get("id"), g.get("topic", ""), g.get("question"), g.get("priority"),
                          ", ".join(g.get("blocks") or [])] for g in gaps]) if gaps else "_No open gaps._")
    out += ["", "## 9. Downstream readiness (スキル連携準備)", "",
            md_table(["Skill", "Ready", "Missing fields", "Open gaps"], readiness(data)), ""]
    return "\n".join(out)
