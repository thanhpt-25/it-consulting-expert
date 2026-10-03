"""Earned value management for progress reports.

Inputs are cumulative to the status date: either PV/EV/AC directly, or a task list from which
they are derived (EV = Σ planned_value × pct_complete, PV = Σ planned_value × planned_pct).
"""
from __future__ import annotations

from common import D, Findings, SierError, findings_md, md_table, num, pct, policy, safe_div, yen

RAG_ICON = {"green": "🟢", "yellow": "🟡", "red": "🔴", "n/a": "⚪"}


def _rag_min(v, cfg):
    if v is None:
        return "n/a"
    return "green" if v >= D(cfg["green_min"]) else "red" if v < D(cfg["red_below"]) else "yellow"


def _rag_max(v, cfg):
    if v is None:
        return "red"
    return "green" if v <= D(cfg["green_max"]) else "red" if v > D(cfg["red_above"]) else "yellow"


def compute(inp: dict) -> dict:
    pol = policy()["evm"]
    f = Findings()
    if inp.get("bac") is None:
        raise SierError("evm input needs bac (budget at completion)")
    bac = D(inp["bac"])
    if bac <= 0:
        raise SierError("bac must be positive")
    if inp.get("tasks"):
        pv = ev = ac = D(0)
        for i, t in enumerate(inp["tasks"]):
            pvt = D(t.get("planned_value", 0))
            pc = D(t.get("pct_complete", 0))
            pp = D(t.get("planned_pct", 0))
            if not (0 <= pc <= 1) or not (0 <= pp <= 1):
                f.error(f"tasks[{i}] ({t.get('id')}): pct_complete and planned_pct are fractions between 0 and 1")
            pv += pvt * pp
            ev += pvt * pc
            ac += D(t.get("actual_cost", 0))
        total_pv = sum(D(t.get("planned_value", 0)) for t in inp["tasks"])
        if abs(total_pv - bac) > D("0.5"):
            f.warn(f"task planned values sum to {yen(total_pv)} but BAC is {yen(bac)}")
        source = "tasks"
    else:
        for k in ("pv", "ev", "ac"):
            if inp.get(k) is None:
                raise SierError(f"evm input needs {k} (or a tasks list)")
        pv, ev, ac = D(inp["pv"]), D(inp["ev"]), D(inp["ac"])
        source = "totals"
    f.raise_if_errors("EVM")
    if ev > bac:
        f.warn("EV exceeds BAC — check the % complete figures")

    spi = safe_div(ev, pv)
    cpi = safe_div(ev, ac)
    eac = safe_div(bac, cpi) if cpi else None
    eac_atypical = ac + (bac - ev)
    eac_composite = (ac + (bac - ev) / (cpi * spi)) if cpi and spi else None
    etc = (eac - ac) if eac is not None else None
    vac = (bac - eac) if eac is not None else None
    tcpi = safe_div(bac - ev, bac - ac) if bac - ac > 0 else None
    if bac - ac <= 0 and ev < bac:
        f.warn("actual cost has reached BAC with work remaining — the budget cannot be met (TCPI undefined)")
    if pv == 0:
        f.warn("PV is zero — SPI undefined (status date before any planned work?)")
    if ac == 0:
        f.warn("AC is zero — CPI undefined")

    rag = {
        "spi": _rag_min(spi, pol["spi"]),
        "cpi": _rag_min(cpi, pol["cpi"]),
        "eac": _rag_max(safe_div(eac, bac) if eac is not None else None, pol["eac_over_bac"]) if eac is not None else "n/a",
        "tcpi": _rag_max(tcpi, pol["tcpi"]),
    }
    order = ["green", "yellow", "red"]
    overall = max((v for v in rag.values() if v in order), key=order.index, default="n/a")
    return {
        "kind": "evm", "status_date": inp.get("status_date"), "source": source,
        "bac": bac, "pv": pv, "ev": ev, "ac": ac,
        "sv": ev - pv, "cv": ev - ac, "spi": spi, "cpi": cpi,
        "eac": eac, "eac_atypical": eac_atypical, "eac_composite": eac_composite,
        "etc": etc, "vac": vac, "tcpi": tcpi,
        "pct_complete": ev / bac, "pct_spent": ac / bac,
        "rag": rag, "overall": overall, "findings": f.as_dict(),
    }


def render(r: dict) -> str:
    def ix(v):
        return num(v, 2) if v is not None else "—"
    rows = [
        ["Budget at completion (BAC)", yen(r["bac"]), ""],
        ["Planned value (PV)", yen(r["pv"]), ""],
        ["Earned value (EV)", yen(r["ev"]), f"{pct(r['pct_complete'])} of BAC earned"],
        ["Actual cost (AC)", yen(r["ac"]), f"{pct(r['pct_spent'])} of BAC spent"],
        ["Schedule variance (SV = EV − PV)", yen(r["sv"]), "behind" if r["sv"] < 0 else "on/ahead"],
        ["Cost variance (CV = EV − AC)", yen(r["cv"]), "over cost" if r["cv"] < 0 else "on/under cost"],
        ["SPI (EV / PV)", ix(r["spi"]), RAG_ICON[r["rag"]["spi"]]],
        ["CPI (EV / AC)", ix(r["cpi"]), RAG_ICON[r["rag"]["cpi"]]],
        ["EAC (BAC / CPI)", yen(r["eac"]) if r["eac"] is not None else "—", RAG_ICON[r["rag"]["eac"]]],
        ["EAC if variance is one-off (AC + BAC − EV)", yen(r["eac_atypical"]), ""],
        ["EAC if schedule pressure persists (AC + (BAC − EV) / (CPI × SPI))",
         yen(r["eac_composite"]) if r["eac_composite"] is not None else "—", ""],
        ["ETC (EAC − AC)", yen(r["etc"]) if r["etc"] is not None else "—", ""],
        ["VAC (BAC − EAC)", yen(r["vac"]) if r["vac"] is not None else "—", ""],
        ["TCPI ((BAC − EV) / (BAC − AC))", ix(r["tcpi"]), RAG_ICON[r["rag"]["tcpi"]]],
    ]
    return "\n".join([
        f"# EVM status{(' — ' + str(r['status_date'])) if r.get('status_date') else ''}", "",
        f"**Overall: {RAG_ICON[r['overall']]} {r['overall'].upper()}**", "",
        "> Computed by `sier evm`. Thresholds from shared/policy.json (evm).", "",
        md_table(["Metric", "Value", "Status"], rows, "lrl"), "",
        "## Findings", "", findings_md(r["findings"]), ""])
