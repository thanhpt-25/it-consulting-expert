"""sier — the deterministic calculation engine for the it-consulting-expert plugin.

Run it as:   python3 "${CLAUDE_PLUGIN_ROOT}/sier" <command> [options]
Every command prints Markdown to stdout; with a workspace it also writes JSON + Markdown
artifacts and an audit record under _state/runs/.

Exit codes: 0 ok · 1 verification mismatch · 2 input/validation error · 3 warnings under --strict
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import brief as brief_mod  # noqa: E402
import change  # noqa: E402
import cost as cost_mod  # noqa: E402
import derive  # noqa: E402
import estimate as estimate_mod  # noqa: E402
import evm as evm_mod  # noqa: E402
import firm  # noqa: E402
import score as score_mod  # noqa: E402
import sla as sla_mod  # noqa: E402
import workspace  # noqa: E402
from common import (POLICY_PATH, SierError, _json_default, dump_json, engine_version, findings_md,  # noqa: E402
                    load_json, md_table, today, write_text)

# ---------------------------------------------------------------------------- computed artifacts
# name -> (default input, output stem). Every computed artifact keeps its input in inputs/ so that
# `sier verify` can recompute it and prove the stored numbers were not edited by hand.
COMPUTED = {
    "score":    ("inputs/go-nogo.json", "01-go-nogo"),
    "estimate": ("inputs/estimate.json", "03-estimate"),
    "cost":     ("inputs/cost.json", "05-cost"),
    "sla":      ("inputs/sla.json", "07-sla"),
}


def _context_estimate(ws):
    if ws is None:
        return None
    p = ws / "03-estimate.json"
    return load_json(p) if p.exists() else None


def _brief_budget(ws):
    if ws is None:
        return None
    p = ws / "00-rfp-brief.json"
    if not p.exists():
        return None
    b = (load_json(p).get("commercial") or {}).get("budget")
    return b if b and b.get("amount") is not None else None


def compute_named(name: str, inp: dict, ws: Path | None) -> tuple[dict, str]:
    if name == "estimate":
        cal = firm.calibration_factor(workspace.firm_dir(ws), inp.get("project_type"))
        r = estimate_mod.compute(inp, calibration=cal)
        return r, estimate_mod.render(r)
    if name == "cost":
        est = inp.get("estimate") or _context_estimate(ws)
        r = cost_mod.compute(inp, rate_card=firm.ratecard_load(workspace.firm_dir(ws)), estimate=est,
                             brief_budget=_brief_budget(ws))
        return r, cost_mod.render(r)
    if name == "score":
        r = score_mod.compute(inp)
        return r, score_mod.render(r)
    if name == "sla":
        r = sla_mod.compute(inp)
        return r, sla_mod.render(r)
    if name == "evm":
        r = evm_mod.compute(inp)
        return r, evm_mod.render(r)
    raise SierError(f"unknown computation {name}")


def _normalize(obj):
    return json.loads(json.dumps(obj, default=_json_default, ensure_ascii=False))


def cmd_compute(name: str, args) -> int:
    ws = None if args.no_ws else workspace.find(args.ws, required=False)
    if name == "evm":
        default_in = None
    else:
        default_in = (ws / COMPUTED[name][0]) if ws else None
    src = Path(args.input) if args.input else default_in
    if src is None:
        raise SierError(f"no input: pass --in FILE (no workspace found to read {COMPUTED.get(name, ('inputs/…',))[0]} from)")
    inp = load_json(src)
    result, md = compute_named(name, inp, ws)
    outputs = []
    if ws is not None and not args.out:
        if name == "evm":
            stamp = str(inp.get("status_date") or today().isoformat())
            stored_in = ws / "inputs" / f"evm-{stamp}.json"
            stem = ws / "progress" / f"evm-{stamp}"
        else:
            stored_in = ws / COMPUTED[name][0]
            stem = ws / COMPUTED[name][1]
        if src.resolve() != stored_in.resolve():
            stored_in.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, stored_in)
        outputs = [dump_json(result, stem.with_suffix(".json")), write_text(md, stem.with_suffix(".md"))]
        rec = workspace.record_run(ws, name, stored_in, outputs, _summary(name, result))
        md += f"\n_Saved: {', '.join(str(o.relative_to(ws)) for o in outputs)} · run record `{rec.name}`_\n"
    elif args.out:
        outputs = [dump_json(result, Path(args.out))]
        if args.md:
            outputs.append(write_text(md, Path(args.md)))
    print(md)
    warnings = (result.get("findings") or {}).get("warnings") or []
    return 3 if (args.strict and warnings) else 0


def _summary(name: str, r: dict) -> dict:
    if name == "estimate":
        return {"recommended_mm": r["recommended_mm"], "factor_product": r["params"]["factor_product"],
                "warnings": len(r["findings"]["warnings"])}
    if name == "cost":
        fit = r.get("budget_fit") or {}
        return {"price_tax_excluded": r["price_tax_excluded"], "gross_margin": r["gross_margin"],
                "budget_status": fit.get("status"), "warnings": len(r["findings"]["warnings"])}
    if name == "score":
        return {"weighted_score": r["weighted_score"], "verdict": r["verdict"]}
    if name == "evm":
        return {"spi": r["spi"], "cpi": r["cpi"], "overall": r["overall"]}
    if name == "sla":
        return {"annual_fee": (r.get("fee") or {}).get("annual_total")}
    return {}


# ------------------------------------------------------------------------------------- verify

def cmd_verify(args) -> int:
    ws = workspace.find(args.ws)
    rows, problems = [], 0
    for name, (rel_in, stem) in COMPUTED.items():
        p_in, p_json, p_md = ws / rel_in, ws / f"{stem}.json", ws / f"{stem}.md"
        if not p_json.exists() and not p_in.exists():
            continue
        if not p_in.exists():
            rows.append([name, "❌", f"`{stem}.json` exists but its input `{rel_in}` is missing — cannot be reproduced"])
            problems += 1
            continue
        if not p_json.exists():
            rows.append([name, "⚠️", f"input exists but `{stem}.json` was never computed — run `sier {name}`"])
            continue
        try:
            result, md = compute_named(name, load_json(p_in), ws)
        except SierError as e:
            rows.append([name, "❌", f"input no longer computes: {e}"])
            problems += 1
            continue
        same_json = _normalize(result) == _normalize(load_json(p_json))
        same_md = p_md.exists() and p_md.read_text(encoding="utf-8").rstrip() == md.rstrip()
        if same_json and same_md:
            rows.append([name, "✅", "recomputed from inputs: identical"])
        elif same_json:
            rows.append([name, "❌", f"`{stem}.md` differs from what the engine renders — it was edited by hand"])
            problems += 1
        else:
            rows.append([name, "❌", f"`{stem}.json` differs from a fresh computation — inputs, policy, rate card or "
                                     f"calibration changed since it was saved, or it was edited. Re-run `sier {name}`."])
            problems += 1

    checks = []
    bp = ws / "00-rfp-brief.json"
    if bp.exists():
        bf = brief_mod.validate(load_json(bp))
        checks.append(["RFP Brief schema", "✅" if not bf.errors else "❌", f"{len(bf.errors)} error(s), {len(bf.warnings)} warning(s)"])
        problems += 1 if bf.errors else 0
        eng = workspace.load(ws)
        stale = workspace.brief_is_stale(eng)
        if stale:
            checks.append(["RFP Brief freshness", "❌", "sources changed after the Brief was generated"])
            problems += 1
    cp = ws / "05-cost.json"
    if cp.exists():
        c = load_json(cp)
        rc = c.get("reconciliation")
        if rc:
            ok = rc.get("within_tolerance")
            checks.append(["Team 人月 vs estimate", "✅" if ok else "❌",
                           f"labor {rc['labor_mm']} vs estimate {rc['estimate_mm']} 人月"])
            problems += 0 if ok else 1
        else:
            checks.append(["Team 人月 vs estimate", "⚠️", "cost was computed without an estimate to reconcile against"])
        fit = c.get("budget_fit")
        if fit:
            checks.append(["Budget fit", "❌" if fit["status"] == "over" else "✅", fit["status"].replace("_", " ")])
            problems += 1 if fit["status"] == "over" else 0
        ep = ws / "03-estimate.json"
        if ep.exists() and rc and abs(float(rc["estimate_mm"]) - float(load_json(ep)["recommended_mm"])) > 0.005:
            checks.append(["Cost built on current estimate", "❌", "05-cost.json was computed against an older estimate — re-run `sier cost`"])
            problems += 1
    ep = ws / "03-estimate.json"
    if ep.exists():
        tr = load_json(ep)["traceability"]
        n = len(tr["untraced"])
        checks.append(["Estimate traceability", "✅" if n == 0 else "⚠️", f"{n} untraced WBS item(s)"])
    gp = ws / "01-go-nogo.json"
    if gp.exists():
        g = load_json(gp)
        checks.append(["Go/No-Go verdict", "ℹ️", f"{g['verdict']} ({g['weighted_score']})"])

    out = [f"# Verification — {ws.name}", "", f"Engine {engine_version()} · {today().isoformat()}", "",
           "## Recomputation", "", md_table(["Artifact", "", "Result"], rows, "lcl") if rows else "_Nothing computed yet._",
           "", "## Cross-checks", "", md_table(["Check", "", "Detail"], checks, "lcl") if checks else "_No artifacts to check._",
           "", f"**{'PASS' if problems == 0 else f'FAIL — {problems} problem(s)'}**", ""]
    text = "\n".join(out)
    write_text(text, ws / "_state" / "verify.md")
    print(text)
    return 0 if problems == 0 else 1


# ------------------------------------------------------------------------------------- commands

def cmd_init(args) -> int:
    ws = workspace.init(args.client, args.project, Path(args.root) if args.root else None,
                        args.notebook, args.currency, args.rfp_ref, args.slug)
    print(f"Created engagement workspace: {ws}\n\nNext: run rfp-notebook to produce 00-rfp-brief.json, then `sier status`.")
    return 0


def cmd_status(args) -> int:
    print(workspace.status(workspace.find(args.ws)))
    return 0


def cmd_brief(args) -> int:
    ws = workspace.find(args.ws, required=not args.file)
    path = Path(args.file) if args.file else ws / "00-rfp-brief.json"
    data = load_json(path)
    if args.action == "validate":
        f = brief_mod.validate(data)
        print(f"# Brief validation — {path.name}\n\n{findings_md(f)}\n")
        return 2 if f.errors else (3 if args.strict and f.warnings else 0)
    if args.action == "render":
        f = brief_mod.validate(data)
        if f.errors:
            print(findings_md(f))
            raise SierError("fix the Brief before rendering it")
        md = brief_mod.render(data)
        out = path.with_suffix(".md")
        write_text(md, out)
        if ws is not None and path.parent.resolve() == ws.resolve():
            eng = workspace.load(ws)
            eng["brief"] = {"generated_at": data.get("generated_at"), "source_tier": data.get("source_tier")}
            if data.get("notebook_id") and not eng.get("notebook_id"):
                eng["notebook_id"] = data["notebook_id"]
            workspace.save(ws, eng)
            workspace.record_run(ws, "brief render", path, [out], {"warnings": len(f.warnings)})
        print(md)
        return 0
    if args.action == "gaps":
        gaps = brief_mod.gaps_for(data, args.for_skill)
        if not gaps:
            print(f"No open gaps{' for ' + args.for_skill if args.for_skill else ''}. Use the Brief as-is; do not re-query NotebookLM.")
            return 0
        print(md_table(["ID", "Topic", "Question", "Priority"],
                       [[g["id"], g.get("topic", ""), g["question"], g["priority"]] for g in gaps]))
        return 0
    raise SierError(f"unknown brief action {args.action}")


def cmd_cr(args) -> int:
    ws = workspace.find(args.ws)
    eng = workspace.load(ws)
    baseline = {k: v for k, v in (eng.get("baseline") or {}).items() if v is not None}
    baseline = {"cost": baseline.get("cost"), "effort_mm": baseline.get("effort_mm"),
                "schedule_days": baseline.get("schedule_days"), "requirements_count": baseline.get("requirements_count")}
    if args.action == "add":
        if not args.input:
            raise SierError("cr add needs --in FILE")
        led = change.add(ws, load_json(args.input), baseline)
    else:
        led = change.load_ledger(ws, baseline)
        if not led.get("baseline") or not any(led["baseline"].values()):
            led["baseline"] = baseline
    r = change.report(led)
    md = change.render(r)
    outs = [dump_json(r, ws / "progress" / "cr-report.json"), write_text(md, ws / "progress" / "cr-report.md")]
    workspace.record_run(ws, f"cr {args.action}", Path(args.input) if args.input else None, outs,
                         {"crs": len(r["crs"]), "gates": {k: v["gate"] for k, v in r["cumulative"].items()}})
    print(md)
    return 0


def cmd_calibrate(args) -> int:
    ws = workspace.find(args.ws, required=False)
    fd = workspace.firm_dir(ws)
    if args.action == "add":
        if not args.input:
            raise SierError("calibrate add needs --in FILE")
        firm.calibration_add(fd, load_json(args.input))
    print(firm.calibration_render(fd))
    return 0


def cmd_ratecard(args) -> int:
    ws = workspace.find(args.ws, required=False)
    fd = workspace.firm_dir(ws)
    if args.action == "init":
        p = firm.ratecard_init(fd, force=args.force)
        print(f"Wrote benchmark rate card to {p}. Replace the rates with your firm's own before pricing a bid.")
        return 0
    card = firm.ratecard_load(fd)
    if not card:
        print(f"No rate card at {fd / firm.RATE_CARD}. Create one with `sier ratecard init`.")
        return 0
    rows = [[role, sen, f"¥{int(rate):,}"] for role, levels in card["rates"].items() for sen, rate in levels.items()]
    print(f"# Rate card — {card.get('source')}\n\n" + md_table(["Role", "Seniority", "Monthly"], rows, "llr"))
    return 0


def cmd_derive(args) -> int:
    ws = workspace.find(args.ws)
    if args.action == "list":
        print(derive.listing(ws))
        return 0
    if not args.script:
        raise SierError("derive run needs a script path")
    res = derive.run(ws, Path(args.script), args.timeout)
    workspace.record_run(ws, "derive", res["script"], [res["output_path"]], {"keys": sorted(res["result"].keys())[:20]})
    print(json.dumps(res["result"], indent=2, ensure_ascii=False))
    return 0


def cmd_runs(args) -> int:
    ws = workspace.find(args.ws)
    rows = []
    for p in sorted((ws / "_state" / "runs").glob("*.json"))[-args.limit:]:
        r = load_json(p)
        rows.append([r["at"], r["command"], r.get("engine_version"), json.dumps(r.get("summary"), ensure_ascii=False)[:90]])
    print(md_table(["At", "Command", "Engine", "Summary"], rows) if rows else "No runs recorded.")
    return 0


def cmd_policy(args) -> int:
    print(f"Policy file: {POLICY_PATH}\nEngine version: {engine_version()}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="sier", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--version", action="version", version=f"sier {engine_version()}")
    sub = p.add_subparsers(dest="command", required=True)

    def ws_opt(sp):
        sp.add_argument("--ws", help="engagement workspace (default: $SIER_WORKSPACE or nearest engagement.json above cwd)")

    sp = sub.add_parser("init", help="create an engagement workspace")
    sp.add_argument("--client", required=True)
    sp.add_argument("--project", required=True)
    sp.add_argument("--root", help="parent folder (default: $SIER_HOME or ./consulting)")
    sp.add_argument("--notebook", help="NotebookLM notebook id")
    sp.add_argument("--currency", default="JPY")
    sp.add_argument("--rfp-ref", dest="rfp_ref")
    sp.add_argument("--slug", help="folder name override")
    sp.set_defaults(fn=cmd_init)

    sp = sub.add_parser("status", help="engagement dashboard: pipeline, deadlines, next step")
    ws_opt(sp)
    sp.set_defaults(fn=cmd_status)

    sp = sub.add_parser("brief", help="validate / render / list gaps in the RFP Brief")
    sp.add_argument("action", choices=["validate", "render", "gaps"])
    sp.add_argument("--file", help="brief JSON (default: <ws>/00-rfp-brief.json)")
    sp.add_argument("--for", dest="for_skill", help="gaps: only those blocking this skill")
    sp.add_argument("--strict", action="store_true")
    ws_opt(sp)
    sp.set_defaults(fn=cmd_brief)

    for name, helptext in (("estimate", "effort estimate (WBS or FP)"), ("cost", "cost model and pricing"),
                           ("score", "Go/No-Go score"), ("evm", "earned value metrics"),
                           ("sla", "SLA downtime and maintenance fee")):
        sp = sub.add_parser(name, help=helptext)
        sp.add_argument("--in", dest="input", help="input JSON (default: <ws>/inputs/…)")
        sp.add_argument("--out", help="write result JSON here instead of the workspace")
        sp.add_argument("--md", help="with --out: also write Markdown here")
        sp.add_argument("--no-ws", action="store_true", help="ignore any workspace; print only")
        sp.add_argument("--strict", action="store_true", help="exit 3 when there are warnings")
        ws_opt(sp)
        sp.set_defaults(fn=lambda a, n=name: cmd_compute(n, a))

    sp = sub.add_parser("cr", help="change-request ledger")
    sp.add_argument("action", choices=["add", "report"])
    sp.add_argument("--in", dest="input")
    ws_opt(sp)
    sp.set_defaults(fn=cmd_cr)

    sp = sub.add_parser("calibrate", help="estimation calibration from closed projects")
    sp.add_argument("action", choices=["add", "show"])
    sp.add_argument("--in", dest="input")
    ws_opt(sp)
    sp.set_defaults(fn=cmd_calibrate)

    sp = sub.add_parser("ratecard", help="firm rate card")
    sp.add_argument("action", choices=["init", "show"])
    sp.add_argument("--force", action="store_true")
    ws_opt(sp)
    sp.set_defaults(fn=cmd_ratecard)

    sp = sub.add_parser("derive", help="Tier-2: run a generated analysis script under guardrails")
    sp.add_argument("action", choices=["run", "list"])
    sp.add_argument("script", nargs="?")
    sp.add_argument("--timeout", type=int)
    ws_opt(sp)
    sp.set_defaults(fn=cmd_derive)

    sp = sub.add_parser("verify", help="recompute every artifact from its inputs and run cross-checks")
    ws_opt(sp)
    sp.set_defaults(fn=cmd_verify)

    sp = sub.add_parser("runs", help="list recorded engine runs")
    sp.add_argument("--limit", type=int, default=20)
    ws_opt(sp)
    sp.set_defaults(fn=cmd_runs)

    sp = sub.add_parser("policy", help="show where the policy file lives")
    sp.set_defaults(fn=cmd_policy)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.fn(args)
    except SierError as e:
        print(f"sier: error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
