"""Change-request ledger: cumulative deviation from the contract baseline, and approval authority."""
from __future__ import annotations

from pathlib import Path

from common import D, Findings, SierError, dump_json, findings_md, load_json, md_table, num, pct, policy, yen

STATUSES = ("proposed", "approved", "rejected", "deferred")
LEDGER = Path("_state") / "cr-ledger.json"


def authority(cost: D, days: D, go_live_changes: bool) -> str:
    a = policy()["change_control"]["authority"]
    if go_live_changes and a.get("executive_if_go_live_changes"):
        return "executive"
    if cost > D(a["director"]["max_cost_inclusive"]) or days > D(a["director"]["max_days_inclusive"]):
        return "executive"
    if cost >= D(a["pm"]["max_cost_exclusive"]) or days >= D(a["pm"]["max_days_exclusive"]):
        return "director"
    return "pm"


def load_ledger(ws: Path, baseline: dict | None) -> dict:
    p = ws / LEDGER
    if p.exists():
        return load_json(p)
    return {"baseline": baseline or {}, "crs": []}


def add(ws: Path, cr: dict, baseline: dict | None) -> dict:
    led = load_ledger(ws, baseline)
    if not led.get("baseline") and baseline:
        led["baseline"] = baseline
    for k in ("id", "title", "status"):
        if not cr.get(k):
            raise SierError(f"change request needs {k}")
    if cr["status"] not in STATUSES:
        raise SierError(f"status must be one of {', '.join(STATUSES)}")
    if any(x["id"] == cr["id"] for x in led["crs"]):
        # Updating an existing CR (e.g. proposed -> approved) replaces it.
        led["crs"] = [x for x in led["crs"] if x["id"] != cr["id"]]
    for k in ("cost_delta", "effort_delta_mm", "schedule_delta_days", "requirements_delta"):
        cr[k] = cr.get(k, 0) or 0
        D(cr[k])  # validates numeric
    led["crs"].append(cr)
    led["crs"].sort(key=lambda x: str(x["id"]))
    dump_json(led, ws / LEDGER)
    return led


def report(led: dict) -> dict:
    gates = policy()["change_control"]["gates"]
    f = Findings()
    base = led.get("baseline") or {}
    dims = {"cost": "cost_delta", "effort_mm": "effort_delta_mm", "schedule_days": "schedule_delta_days",
            "requirements_count": "requirements_delta"}
    rows, cum = [], {}
    for d, key in dims.items():
        approved = sum((D(c.get(key, 0)) for c in led["crs"] if c["status"] == "approved"), D(0))
        pending = sum((D(c.get(key, 0)) for c in led["crs"] if c["status"] == "proposed"), D(0))
        b = base.get(d)
        ratio = (approved / D(b)) if b else None
        exposure = ((approved + pending) / D(b)) if b else None
        gate = "n/a"
        if ratio is not None:
            gate = "red" if ratio > D(gates["red_above"]) else "yellow" if ratio > D(gates["yellow_above"]) else "green"
            if gate == "red":
                f.warn(f"cumulative approved {d} change is {pct(ratio)} of baseline — above {pct(gates['red_above'], 0)}: "
                       f"open a contract amendment discussion")
            elif gate == "yellow":
                f.warn(f"cumulative approved {d} change is {pct(ratio)} of baseline — above {pct(gates['yellow_above'], 0)}")
        elif approved or pending:
            f.warn(f"no baseline for {d} — set engagement.json baseline to track deviation")
        cum[d] = {"baseline": b, "approved": approved, "pending": pending, "ratio": ratio,
                  "exposure_ratio": exposure, "gate": gate}
    for c in led["crs"]:
        c["authority"] = authority(abs(D(c.get("cost_delta", 0))), abs(D(c.get("schedule_delta_days", 0))),
                                   bool(c.get("go_live_changes")))
        rows.append(c)
    return {"kind": "cr_report", "baseline": base, "cumulative": cum, "crs": rows, "findings": f.as_dict()}


def render(r: dict) -> str:
    icon = {"green": "🟢", "yellow": "🟡", "red": "🔴", "n/a": "⚪"}
    fmt = {"cost": yen, "effort_mm": lambda v: f"{num(v, 1)} 人月", "schedule_days": lambda v: f"{num(v, 0)} days",
           "requirements_count": lambda v: num(v, 0)}
    cum_rows = []
    for d, c in r["cumulative"].items():
        b = c["baseline"]
        cum_rows.append([d.replace("_", " "), fmt[d](b) if b else "—", fmt[d](c["approved"]), fmt[d](c["pending"]),
                         pct(c["ratio"]) if c["ratio"] is not None else "—",
                         pct(c["exposure_ratio"]) if c["exposure_ratio"] is not None else "—", icon[c["gate"]]])
    cr_rows = [[c["id"], c.get("title", ""), c["status"], yen(c.get("cost_delta", 0)),
                f"{num(c.get('effort_delta_mm', 0), 1)}", f"{num(c.get('schedule_delta_days', 0), 0)}",
                c["authority"]] for c in r["crs"]]
    return "\n".join([
        "# Change Request Ledger (変更累積管理表)", "",
        "> Computed by `sier cr report`. Gates and approval authority from shared/policy.json (change_control).", "",
        "## Cumulative deviation from baseline", "",
        md_table(["Dimension", "Baseline", "Approved", "Pending", "Approved %", "If pending approved", "Gate"],
                 cum_rows, "lrrrrrc"), "",
        "## Change requests", "",
        md_table(["CR", "Title", "Status", "Cost Δ", "人月 Δ", "Days Δ", "Approval authority"], cr_rows, "lllrrrl")
        if cr_rows else "_No change requests recorded._", "",
        "## Findings", "", findings_md(r["findings"]), ""])
