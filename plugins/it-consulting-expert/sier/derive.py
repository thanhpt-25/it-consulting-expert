"""Tier-2 harness: run a model-generated analysis script under guardrails.

Rules (shared/harness.md explains why):
  1. The script lives in <ws>/_state/derived/ and stays there next to its output — auditable, re-runnable.
  2. It must contain at least one `assert` (a self-check).
  3. It prints exactly one JSON object to stdout.
  4. That JSON may not contain any key Tier-1 engines own (policy.harness.contractual_keys):
     generated code answers new questions; it never restates a contractual number.
"""
from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

from common import SierError, dump_json, md_table, policy, sha256_file


def _forbidden_keys(obj, banned: set, path: str = "") -> list[str]:
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}.{k}" if path else k
            if k in banned:
                hits.append(p)
            hits += _forbidden_keys(v, banned, p)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits += _forbidden_keys(v, banned, f"{path}[{i}]")
    return hits


def _has_assert(src: str) -> bool:
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        raise SierError(f"derived script does not parse: {e}") from None
    return any(isinstance(n, ast.Assert) for n in ast.walk(tree))


def run(ws: Path, script: Path, timeout: int | None = None) -> dict:
    derived = (ws / "_state" / "derived").resolve()
    script = script.resolve()
    if derived not in script.parents:
        raise SierError(f"derived scripts must live in {derived} (got {script})")
    if script.suffix != ".py":
        raise SierError("derived scripts must be .py files")
    src = script.read_text(encoding="utf-8")
    if not _has_assert(src):
        raise SierError("derived script has no `assert` — every generated analysis must check itself")
    cfg = policy()["harness"]
    try:
        proc = subprocess.run([sys.executable, str(script)], cwd=str(ws), capture_output=True, text=True,
                              timeout=timeout or cfg["timeout_seconds"])
    except subprocess.TimeoutExpired:
        raise SierError(f"derived script exceeded {timeout or cfg['timeout_seconds']}s") from None
    if proc.returncode != 0:
        tail = (proc.stderr or "").strip().splitlines()[-8:]
        raise SierError("derived script failed (exit %d):\n    %s" % (proc.returncode, "\n    ".join(tail)))
    try:
        out = json.loads(proc.stdout)
    except json.JSONDecodeError:
        raise SierError("derived script must print exactly one JSON object to stdout") from None
    banned = set(cfg["contractual_keys"])
    hits = _forbidden_keys(out, banned)
    if hits:
        raise SierError("derived output restates numbers owned by Tier-1 engines: " + ", ".join(hits)
                        + ". Read them from 03-estimate.json / 05-cost.json instead of re-emitting them.")
    out_path = script.with_suffix(".out.json")
    rec = {"script": script.name, "script_sha256": sha256_file(script), "output": out}
    dump_json(rec, out_path)
    return {"script": script, "output_path": out_path, "result": out}


def listing(ws: Path) -> str:
    d = ws / "_state" / "derived"
    rows = []
    for s in sorted(d.glob("*.py")):
        o = s.with_suffix(".out.json")
        ok = "—"
        if o.exists():
            try:
                rec = json.loads(o.read_text(encoding="utf-8"))
                ok = "✅ current" if rec.get("script_sha256") == sha256_file(s) else "⚠️ script changed since last run"
            except json.JSONDecodeError:
                ok = "❌ unreadable output"
        rows.append([s.name, ok])
    return md_table(["Derived script", "Output"], rows) if rows else "_No derived analyses yet._"
