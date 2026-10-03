"""Engagement workspace: the shared blackboard every skill and agent reads and writes.

Layout (see shared/engagement-workspace.md for the contract):

    <root>/
      _firm/                      rate-card.json, calibration.json  (shared across engagements)
      <slug>/
        engagement.json           identity, notebook, deadlines, baseline
        00-rfp-brief.json/.md     canonical RFP extraction (rfp-notebook is the only writer)
        01-go-nogo.json/.md       rfp-analysis
        02-architecture.md        technical-solution
        03-estimate.json/.md      effort-estimation  (computed by `sier estimate`)
        04-team.json/.md          team-composition
        05-cost.json/.md          cost-estimation    (computed by `sier cost`)
        06-delivery-plan.md       project-delivery
        inputs/                   human-editable inputs for every computed artifact
        artifacts/                client-facing files (proposal.docx, deck.pptx, estimate.xlsx)
        _state/runs/              one JSON record per engine run
        _state/derived/           Tier-2 generated scripts and their outputs
        _state/review/            one report per review-board persona
        _state/cr-ledger.json     change-request ledger
"""
from __future__ import annotations

import os
import re
import unicodedata
from pathlib import Path

from common import (SierError, dump_json, engine_version, load_json, md_table, now_iso,
                    parse_date, policy_sha256, sha256_file, today)

ENGAGEMENT_FILE = "engagement.json"
SCHEMA_VERSION = 1

# Pipeline order — drives `sier status` "next step" and the presale DAG.
PIPELINE = [
    ("00-rfp-brief.json",    "rfp-notebook",       "Extract the RFP into the Brief"),
    ("01-go-nogo.json",      "rfp-analysis",       "Score the bid (Go/No-Go)"),
    ("02-architecture.md",   "technical-solution", "Design the solution"),
    ("03-estimate.json",     "effort-estimation",  "Estimate effort"),
    ("04-team.json",         "team-composition",   "Plan the team"),
    ("05-cost.json",         "cost-estimation",    "Price the bid"),
    ("06-delivery-plan.md",  "project-delivery",   "Plan delivery and governance"),
    ("artifacts/proposal.docx", "create-proposal", "Write the proposal"),
    ("_state/review/consensus.md", "proposal-review", "Run the review board"),
]

SUBDIRS = ["inputs", "artifacts", "_state/runs", "_state/derived", "_state/review"]


def default_root() -> Path:
    env = os.environ.get("SIER_HOME")
    return Path(env).expanduser() if env else Path.cwd() / "consulting"


def slugify(*parts: str) -> str:
    raw = "-".join(p for p in parts if p)
    raw = unicodedata.normalize("NFKC", raw)
    raw = re.sub(r"[\\/:*?\"<>|\s]+", "-", raw.strip())
    raw = re.sub(r"-{2,}", "-", raw).strip("-.")
    if not raw:
        raise SierError("Cannot build a folder name from an empty client/project name")
    return raw[:80]


def init(client: str, project: str, root: Path | None = None, notebook_id: str | None = None,
         currency: str = "JPY", rfp_ref: str | None = None, slug: str | None = None) -> Path:
    if not client or not project:
        raise SierError("Both --client and --project are required")
    root = (root or default_root()).expanduser().resolve()
    ws = root / (slug or slugify(client, project))
    if (ws / ENGAGEMENT_FILE).exists():
        raise SierError(f"An engagement already exists at {ws}. Use it, or pass a different --slug.")
    for sub in SUBDIRS:
        (ws / sub).mkdir(parents=True, exist_ok=True)
    (root / "_firm").mkdir(parents=True, exist_ok=True)
    eng = {
        "schema_version": SCHEMA_VERSION,
        "client": client,
        "project": project,
        "slug": ws.name,
        "created": today().isoformat(),
        "currency": currency,
        "rfp_ref": rfp_ref,
        "notebook_id": notebook_id,
        "sources_updated_at": None,
        "deadlines": {"proposal_submission": None, "presentation": None, "go_live": None},
        "baseline": {"effort_mm": None, "cost": None, "schedule_days": None, "requirements_count": None},
        "brief": {"generated_at": None, "source_tier": None},
    }
    dump_json(eng, ws / ENGAGEMENT_FILE)
    return ws


def find(ws_arg: str | None = None, required: bool = True) -> Path | None:
    """Resolve the workspace: explicit arg > $SIER_WORKSPACE > nearest engagement.json above cwd."""
    candidates = []
    if ws_arg:
        candidates.append(Path(ws_arg).expanduser())
    elif os.environ.get("SIER_WORKSPACE"):
        candidates.append(Path(os.environ["SIER_WORKSPACE"]).expanduser())
    else:
        here = Path.cwd().resolve()
        candidates.extend([here, *here.parents])
    for c in candidates:
        if (c / ENGAGEMENT_FILE).exists():
            return c.resolve()
    if required:
        hint = f" at {candidates[0]}" if ws_arg else ""
        raise SierError(f"No engagement workspace found{hint}. Create one with: sier init --client ... --project ...")
    return None


def load(ws: Path) -> dict:
    return load_json(ws / ENGAGEMENT_FILE)


def save(ws: Path, eng: dict) -> None:
    dump_json(eng, ws / ENGAGEMENT_FILE)


def firm_dir(ws: Path | None) -> Path:
    """Firm-wide data lives next to the engagements: <root>/_firm."""
    if ws is not None:
        return ws.parent / "_firm"
    return default_root() / "_firm"


def record_run(ws: Path | None, command: str, input_path: Path | None, outputs: list[Path],
               summary: dict) -> Path | None:
    """Write an auditable record of one engine run. Returns the record path (None without a workspace)."""
    if ws is None:
        return None
    stamp = now_iso().replace(":", "")
    rec = {
        "command": command,
        "at": now_iso(),
        "engine_version": engine_version(),
        "policy_sha256": policy_sha256(),
        "input": str(input_path) if input_path else None,
        "input_sha256": sha256_file(input_path) if input_path and Path(input_path).exists() else None,
        "outputs": [str(o) for o in outputs],
        "summary": summary,
    }
    runs = ws / "_state" / "runs"
    runs.mkdir(parents=True, exist_ok=True)
    path = runs / f"{stamp}-{command.replace(' ', '-')}.json"
    n = 1
    while path.exists():
        n += 1
        path = runs / f"{stamp}-{command.replace(' ', '-')}-{n}.json"
    dump_json(rec, path)
    return path


def brief_is_stale(eng: dict) -> bool | None:
    gen = (eng.get("brief") or {}).get("generated_at")
    src = eng.get("sources_updated_at")
    if not gen:
        return None
    if not src:
        return False
    return parse_date(src, "sources_updated_at") > parse_date(gen, "brief.generated_at")


def status(ws: Path) -> str:
    eng = load(ws)
    lines = [f"# {eng['client']} — {eng['project']}", "",
             f"- Workspace: `{ws}`",
             f"- Notebook: `{eng.get('notebook_id') or 'not set'}`",
             f"- Created: {eng.get('created')}"]
    stale = brief_is_stale(eng)
    tier = (eng.get("brief") or {}).get("source_tier")
    if stale is None:
        lines.append("- RFP Brief: **not generated yet**")
    else:
        lines.append(f"- RFP Brief: generated {eng['brief']['generated_at']} (source tier {tier})"
                     + (" — ⚠️ **STALE: sources changed after it was generated; re-run rfp-notebook**" if stale else ""))

    dl_rows = []
    for k, v in (eng.get("deadlines") or {}).items():
        if v:
            days = (parse_date(v, k) - today()).days
            flag = "🔴" if days <= 3 else "🟡" if days <= 7 else "🟢"
            dl_rows.append([k.replace("_", " "), v, f"{flag} {days} days" if days >= 0 else f"passed {-days} days ago"])
    if dl_rows:
        lines += ["", "## Deadlines", "", md_table(["Milestone", "Date", "Remaining"], dl_rows, "llr")]

    rows, next_step = [], None
    for rel, skill, label in PIPELINE:
        p = ws / rel
        if p.exists():
            rows.append(["✅", label, f"`{rel}`", skill])
        else:
            rows.append(["·", label, f"`{rel}`", skill])
            if next_step is None:
                next_step = (label, skill)
    lines += ["", "## Pipeline", "", md_table(["", "Step", "File", "Skill"], rows, "clll")]
    if next_step:
        lines += ["", f"**Next step:** {next_step[0]} → `{next_step[1]}`"]
    else:
        lines += ["", "**All pipeline artifacts exist.** Run `sier verify` before submission."]

    ledger = ws / "_state" / "cr-ledger.json"
    if ledger.exists():
        n = len(load_json(ledger).get("crs", []))
        lines += ["", f"- Change requests on file: {n} (see `sier cr report`)"]
    runs = sorted((ws / "_state" / "runs").glob("*.json"))
    if runs:
        lines += [f"- Engine runs recorded: {len(runs)} (latest: `{runs[-1].name}`)"]
    return "\n".join(lines)
