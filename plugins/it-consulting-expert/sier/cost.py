"""Cost model and pricing.

Order of operations:
    labor         = Σ round(rate × 人月) per line
    non_labor     = Σ vendor-provided lines (monthly × months + one_time); client-provided lines are listed, not priced
    cost_subtotal = labor + non_labor                         (総原価)
    mgmt_fee      = cost_subtotal × mgmt_fee_rate
    risk_premium  = fixed:  cost_subtotal × rp
                    hybrid: labor × fixed_share × rp
                    tm:     0
    price (税抜)  = round_to(cost_subtotal + mgmt_fee + risk_premium, round_to)
    tax           = round(price × tax_rate)
    price (税込)  = price + tax
Fee and premium are each taken on the subtotal; they do not compound.
"""
from __future__ import annotations

from typing import Any

from common import (D, Findings, SierError, findings_md, md_table, num, pct, policy, round_to,
                    round_yen, safe_div, yen)

MODELS = {"fixed": "一括請負 (fixed price)", "tm": "準委任 (time & materials)", "hybrid": "ハイブリッド (hybrid)"}


def _rate(line: dict, card: dict | None, f: Findings, where: str) -> Any:
    if line.get("rate") is not None:
        return D(line["rate"])
    if not card:
        f.error(f"{where} ({line.get('role')}): no rate given and no rate card available")
        return None
    rates = card.get("rates", {})
    role, sen = line.get("role"), line.get("seniority")
    r = (rates.get(role) or {}).get(sen)
    if r is None:
        f.error(f"{where}: rate card has no rate for role={role!r} seniority={sen!r}")
        return None
    return D(r)


def compute(inp: dict, rate_card: dict | None = None, estimate: dict | None = None,
            brief_budget: dict | None = None) -> dict:
    pol = policy()["commercial"]
    f = Findings()
    card = inp.get("rate_card") or rate_card
    if card and card.get("benchmark_only"):
        f.warn("rates come from market benchmark midpoints, not your firm's rate card — replace them before submission")

    # -- labor
    labor_lines, labor_total, labor_mm = [], D(0), D(0)
    if not inp.get("labor"):
        raise SierError("cost input needs at least one labor line")
    for i, ln in enumerate(inp["labor"]):
        where = f"labor[{i}]"
        try:
            mm = D(ln.get("mm"))
        except SierError:
            f.error(f"{where}: mm must be a number")
            continue
        if mm <= 0:
            f.error(f"{where}: mm must be positive")
            continue
        rate = _rate(ln, card, f, where)
        if rate is None:
            continue
        amount = round_yen(rate * mm)
        labor_total += amount
        labor_mm += mm
        labor_lines.append({"role": ln.get("role"), "seniority": ln.get("seniority"), "label": ln.get("label", ""),
                            "rate": rate, "mm": mm, "amount": amount})

    # -- non-labor
    nl_lines, nl_total, client_provided = [], D(0), []
    for i, ln in enumerate(inp.get("non_labor") or []):
        where = f"non_labor[{i}]"
        monthly, months, one_time = ln.get("monthly"), ln.get("months"), ln.get("one_time")
        if monthly is None and one_time is None:
            f.error(f"{where} ({ln.get('item')}): needs monthly+months or one_time")
            continue
        if monthly is not None and months is None:
            f.error(f"{where} ({ln.get('item')}): monthly given without months")
            continue
        amount = round_yen((D(monthly) * D(months) if monthly is not None else D(0)) + (D(one_time) if one_time is not None else D(0)))
        row = {"category": ln.get("category", "other"), "item": ln.get("item", ""), "monthly": monthly,
               "months": months, "one_time": one_time, "amount": amount,
               "provided_by": ln.get("provided_by", "vendor")}
        if row["provided_by"] == "client":
            client_provided.append(row)
        else:
            nl_total += amount
            nl_lines.append(row)

    f.raise_if_errors("Cost")

    subtotal = labor_total + nl_total
    fee_rate = D(inp.get("mgmt_fee_rate", pol["mgmt_fee_rate"]["default"]))
    lo, hi = (D(x) for x in pol["mgmt_fee_rate"]["range"])
    if not (lo <= fee_rate <= hi):
        f.warn(f"management fee {pct(fee_rate)} is outside the policy range {pct(lo)}–{pct(hi)}")
    mgmt_fee = round_yen(subtotal * fee_rate)

    pricing = inp.get("pricing") or {"model": "fixed"}
    model = pricing.get("model", "fixed")
    if model not in MODELS:
        raise SierError(f"pricing.model must be one of {', '.join(MODELS)}")
    rp_floor, rp_ceiling = (D(x) for x in pol["risk_premium_fixed"]["range"])
    rp = D(pricing.get("risk_premium", pol["risk_premium_fixed"]["default"])) if model != "tm" else D(0)
    if model == "tm" and pricing.get("risk_premium"):
        f.warn("risk_premium ignored for T&M (準委任): the client carries the effort risk")
    if model in ("fixed", "hybrid") and not (rp_floor <= rp <= rp_ceiling):
        f.warn(f"risk premium {pct(rp)} is outside the fixed-price policy range {pct(rp_floor)}–{pct(rp_ceiling)}"
               + (" — this bid carries less contingency than policy requires" if rp < rp_floor else ""))
    if model == "fixed":
        risk_base = subtotal
    elif model == "hybrid":
        share = D(pricing.get("fixed_share", 0))
        if not (0 < share < 1):
            raise SierError("pricing.fixed_share must be between 0 and 1 for hybrid pricing")
        risk_base = labor_total * share
    else:
        risk_base = D(0)
    risk_premium = round_yen(risk_base * rp)

    unit = int(inp.get("round_to", pol["round_to"]))
    raw = subtotal + mgmt_fee + risk_premium
    price_ex = round_to(raw, unit)
    rounding_adj = price_ex - round_yen(raw)
    tax_rate = D(inp.get("tax_rate", pol["tax_rate"]))
    tax = round_yen(D(price_ex) * tax_rate)
    price_inc = price_ex + tax
    margin = safe_div(D(price_ex) - subtotal, price_ex)

    # -- budget fit
    budget = inp.get("budget") or brief_budget
    fit = None
    if budget and budget.get("amount") is not None:
        basis = budget.get("basis", "tax_excluded")
        amount = D(budget["amount"])
        compared = D(price_inc if basis == "tax_included" else price_ex)
        delta = compared - amount
        ratio = compared / amount
        if delta > 0:
            status = "over"
            f.warn(f"price {yen(compared)} is {yen(delta)} ({pct(ratio - 1)}) OVER the RFP budget of {yen(amount)} "
                   f"({basis.replace('_', ' ')}) — propose scope reduction or phasing")
        elif ratio < 1 - D(pol["under_budget_warning"]):
            status = "well_under"
            f.warn(f"price is {pct(1 - ratio)} under the RFP budget — check for missed scope before celebrating")
        else:
            status = "within"
        fit = {"budget": amount, "basis": basis, "source": budget.get("source") or budget.get("citation"),
               "compared_price": compared, "delta": delta, "ratio": ratio, "status": status}

    # -- reconciliation with the effort estimate
    recon = None
    if estimate and estimate.get("recommended_mm") is not None:
        est_mm = D(estimate["recommended_mm"])
        diff = labor_mm - est_mm
        rel = safe_div(diff, est_mm) or D(0)
        tol = D(pol["estimate_reconciliation_tolerance"])
        recon = {"estimate_mm": est_mm, "labor_mm": labor_mm, "diff_mm": diff, "diff_ratio": rel,
                 "within_tolerance": abs(rel) <= tol, "by_role": []}
        # Per role: a matching total can hide a team that is short on testers and long on managers.
        rcfg = pol["role_reconciliation"]
        est_roles = {r["role"]: D(r["recommended_mm"]) for r in estimate.get("roles") or []
                     if not str(r["role"]).startswith(("UNASSIGNED", "UNALLOCATED"))}
        team_roles: dict = {}
        for ln in labor_lines:
            team_roles[ln["role"]] = team_roles.get(ln["role"], D(0)) + ln["mm"]
        for role in sorted(set(est_roles) | set(team_roles)):
            e, t = est_roles.get(role, D(0)), team_roles.get(role, D(0))
            d = t - e
            flag = abs(d) > D(rcfg["min_mm"]) and (e == 0 or abs(d) / e > D(rcfg["tolerance"]))
            recon["by_role"].append({"role": role, "estimate_mm": e, "team_mm": t, "diff_mm": d, "flag": flag})
        short = [x for x in recon["by_role"] if x["flag"] and x["diff_mm"] < 0 and x["estimate_mm"] > 0]
        if short:
            f.warn("team is short against the estimate's role allocation: "
                   + ", ".join(f"{x['role']} {num(x['team_mm'], 1)} vs {num(x['estimate_mm'], 1)} 人月" for x in short)
                   + " — a matching total can hide missing testers or developers; rebalance or explain")
        if abs(rel) > tol:
            f.warn(f"labor plan totals {num(labor_mm, 1)} 人月 but the effort estimate recommends {num(est_mm, 1)} 人月 "
                   f"({'+' if diff > 0 else ''}{pct(rel)}) — the team plan and the estimate do not describe the same project")
    else:
        f.warn("no effort estimate supplied — labor 人月 cannot be reconciled against 03-estimate.json")

    # -- payment schedule
    schedule = None
    if inp.get("payment_schedule"):
        ps = inp["payment_schedule"]
        total_pct = sum(D(x.get("pct", 0)) for x in ps)
        if total_pct != 100:
            raise SierError(f"payment_schedule percentages sum to {total_pct}, not 100")
        schedule, acc_ex, acc_inc = [], 0, 0
        for i, x in enumerate(ps):
            last = i == len(ps) - 1
            ex = price_ex - acc_ex if last else round_yen(D(price_ex) * D(x["pct"]) / 100)
            inc = price_inc - acc_inc if last else round_yen(D(price_inc) * D(x["pct"]) / 100)
            acc_ex += ex
            acc_inc += inc
            schedule.append({"milestone": x.get("milestone", f"#{i + 1}"), "pct": D(x["pct"]),
                             "amount_tax_excluded": ex, "amount_tax_included": inc})

    # -- TCO
    tco = None
    if inp.get("tco"):
        t = inp["tco"]
        mrate = D(t.get("maintenance_rate", pol["maintenance_rate"]["default"]))
        annual_run = D(t.get("annual_run_cost", 0))
        annual = round_yen(annual_run + D(price_ex) * mrate)
        tco = {"maintenance_rate": mrate, "annual_run_cost": annual_run, "annual_total": annual,
               "years": [{"years": int(n), "total": price_ex + annual * int(n)} for n in t.get("years", [3, 5])]}

    result = {
        "kind": "cost",
        "currency": inp.get("currency", pol["currency"]),
        "pricing_model": model,
        "rate_card_source": (card or {}).get("source"),
        "labor": labor_lines,
        "labor_total": labor_total,
        "labor_mm": labor_mm,
        "blended_rate": round_yen(labor_total / labor_mm) if labor_mm else None,
        "non_labor": nl_lines,
        "non_labor_total": nl_total,
        "client_provided": client_provided,
        "cost_subtotal": subtotal,
        "mgmt_fee_rate": fee_rate,
        "mgmt_fee": mgmt_fee,
        "risk_premium_rate": rp,
        "risk_premium": risk_premium,
        "rounding_unit": unit,
        "rounding_adjustment": rounding_adj,
        "price_tax_excluded": price_ex,
        "tax_rate": tax_rate,
        "tax": tax,
        "price_tax_included": price_inc,
        "gross_margin": margin,
        "budget_fit": fit,
        "reconciliation": recon,
        "payment_schedule": schedule,
        "tco": tco,
        "findings": f.as_dict(),
    }
    return result


def render(r: dict) -> str:
    out = ["# Cost Estimate (費用見積)", "",
           f"Pricing model: **{MODELS[r['pricing_model']]}** · Currency: {r['currency']}"
           + (f" · Rates: {r['rate_card_source']}" if r.get("rate_card_source") else ""), "",
           "> Computed by `sier cost`. Do not edit numbers here; edit `inputs/cost.json` and re-run.", "",
           "## Labor (人件費)", "",
           md_table(["Role", "Seniority", "Monthly rate", "人月", "Amount"],
                    [[x["role"], x.get("seniority") or "", yen(x["rate"]), num(x["mm"], 1), yen(x["amount"])]
                     for x in r["labor"]]
                    + [["**Labor total**", "", f"blended {yen(r['blended_rate'])}" if r.get("blended_rate") else "",
                        f"**{num(r['labor_mm'], 1)}**", f"**{yen(r['labor_total'])}**"]], "llrrr"), ""]
    if r["non_labor"] or r["client_provided"]:
        rows = [[x["category"], x["item"], yen(x["monthly"]) if x["monthly"] is not None else "—",
                 x["months"] if x["months"] is not None else "—",
                 yen(x["one_time"]) if x["one_time"] is not None else "—", yen(x["amount"])] for x in r["non_labor"]]
        rows.append(["**Non-labor total**", "", "", "", "", f"**{yen(r['non_labor_total'])}**"])
        out += ["## Non-labor (非人件費)", "", md_table(["Category", "Item", "Monthly", "Months", "One-time", "Amount"], rows, "llrrrr"), ""]
        if r["client_provided"]:
            out += ["Provided by the client (not priced): " + ", ".join(f"{x['item']} ({yen(x['amount'])})" for x in r["client_provided"]), ""]
    rows = [["Labor (人件費)", yen(r["labor_total"])],
            ["Non-labor (非人件費)", yen(r["non_labor_total"])],
            ["**Cost subtotal (総原価)**", f"**{yen(r['cost_subtotal'])}**"],
            [f"Management fee ({pct(r['mgmt_fee_rate'])} of subtotal)", yen(r["mgmt_fee"])],
            [f"Risk premium ({pct(r['risk_premium_rate'])})", yen(r["risk_premium"])]]
    if r["rounding_adjustment"]:
        rows.append([f"Rounding to {r['rounding_unit']:,}", yen(r["rounding_adjustment"])])
    rows += [["**Price, tax excluded (税抜)**", f"**{yen(r['price_tax_excluded'])}**"],
             [f"Consumption tax ({pct(r['tax_rate'], 0)})", yen(r["tax"])],
             ["**Price, tax included (税込)**", f"**{yen(r['price_tax_included'])}**"],
             ["Gross margin (粗利率)", pct(r["gross_margin"])]]
    out += ["## Summary (費用サマリー)", "", md_table(["Item", "Amount"], rows, "lr"), ""]
    fit = r.get("budget_fit")
    if fit:
        icon = {"over": "🔴 OVER", "well_under": "🟡 well under", "within": "🟢 within"}[fit["status"]]
        out += ["## Budget fit (予算適合)", "",
                md_table(["RFP budget", "Basis", "Our price", "Delta", "Status"],
                         [[yen(fit["budget"]), fit["basis"].replace("_", " "), yen(fit["compared_price"]),
                           ("+" if fit["delta"] > 0 else "") + yen(fit["delta"]), icon]], "rlrrl"),
                (f"Budget source: {fit['source']}" if fit.get("source") else ""), ""]
    rc = r.get("reconciliation")
    if rc:
        out += ["## Reconciliation with the effort estimate (工数整合)", "",
                md_table(["Estimate recommends", "Labor plan", "Difference", "OK?"],
                         [[f"{num(rc['estimate_mm'], 1)} 人月", f"{num(rc['labor_mm'], 1)} 人月",
                           f"{'+' if rc['diff_mm'] > 0 else ''}{num(rc['diff_mm'], 1)} ({pct(rc['diff_ratio'])})",
                           "✅" if rc["within_tolerance"] else "❌"]], "rrrc"), ""]
        if rc.get("by_role"):
            out += ["By role (estimate allocation vs team plan):", "",
                    md_table(["Role", "Estimate 人月", "Team 人月", "Difference", ""],
                             [[x["role"], num(x["estimate_mm"], 1), num(x["team_mm"], 1),
                               ("+" if x["diff_mm"] > 0 else "") + num(x["diff_mm"], 1), "⚠️" if x["flag"] else ""]
                              for x in rc["by_role"]], "lrrrc"), ""]
    if r.get("payment_schedule"):
        out += ["## Payment schedule (支払条件)", "",
                md_table(["Milestone", "%", "税抜", "税込"],
                         [[x["milestone"], f"{num(x['pct'], 0)}%", yen(x["amount_tax_excluded"]), yen(x["amount_tax_included"])]
                          for x in r["payment_schedule"]], "lrrr"), ""]
    if r.get("tco"):
        t = r["tco"]
        out += ["## Total cost of ownership (TCO)", "",
                f"Annual run + maintenance: {yen(t['annual_total'])} "
                f"(run {yen(t['annual_run_cost'])} + maintenance {pct(t['maintenance_rate'])} of price)", "",
                md_table(["Horizon", "TCO"], [[f"{y['years']} years", yen(y["total"])] for y in t["years"]], "lr"), ""]
    out += ["## Findings", "", findings_md(r["findings"]), ""]
    return "\n".join(out)
