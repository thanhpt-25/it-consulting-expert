"""Shared helpers for the sier engine.

Stdlib only, so the engine runs anywhere `python3` (3.8+) exists, with nothing to install.
Money is handled with Decimal and rounded half-up to whole yen.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from typing import Any, Iterable, Sequence

ENGINE_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = ENGINE_DIR.parent
POLICY_PATH = PLUGIN_ROOT / "shared" / "policy.json"
MANIFEST_PATH = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"


class SierError(Exception):
    """A user-facing error: bad input, missing file, failed validation."""


# --------------------------------------------------------------------------- io

def load_json(path: Path | str) -> Any:
    p = Path(path)
    if not p.exists():
        raise SierError(f"File not found: {p}")
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SierError(f"{p} is not valid JSON (line {e.lineno}, column {e.colno}): {e.msg}") from None


def dump_json(obj: Any, path: Path | str) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False, default=_json_default) + "\n", encoding="utf-8")
    return p


def write_text(text: str, path: Path | str) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
    return p


def _json_default(o: Any) -> Any:
    if isinstance(o, Decimal):
        # Integers stay integers; everything else becomes a float rounded for readability.
        return int(o) if o == o.to_integral_value() else float(round(o, 6))
    if isinstance(o, (_dt.date, _dt.datetime)):
        return o.isoformat()
    if isinstance(o, Path):
        return str(o)
    raise TypeError(f"Not JSON serializable: {type(o).__name__}")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(path: Path | str) -> str:
    return sha256_bytes(Path(path).read_bytes())


# ----------------------------------------------------------------------- policy

_POLICY_CACHE: dict | None = None


def policy() -> dict:
    global _POLICY_CACHE
    if _POLICY_CACHE is None:
        _POLICY_CACHE = load_json(POLICY_PATH)
    return _POLICY_CACHE


def policy_sha256() -> str:
    return sha256_file(POLICY_PATH)


def engine_version() -> str:
    try:
        return str(load_json(MANIFEST_PATH).get("version", "unknown"))
    except SierError:
        return "unknown"


# ------------------------------------------------------------------------ maths

def D(x: Any) -> Decimal:
    """Exact decimal from int/float/str. Floats go through str() to avoid binary noise."""
    if isinstance(x, Decimal):
        return x
    if x is None:
        raise SierError("Expected a number, got null")
    if isinstance(x, bool):
        raise SierError(f"Expected a number, got boolean {x}")
    try:
        return Decimal(str(x))
    except Exception:
        raise SierError(f"Expected a number, got {x!r}") from None


def q(x: Any, places: int = 2) -> Decimal:
    """Round half-up to a fixed number of decimal places."""
    exp = Decimal(1).scaleb(-places)
    return D(x).quantize(exp, rounding=ROUND_HALF_UP)


def round_yen(x: Any) -> int:
    return int(D(x).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def round_to(x: Any, unit: int) -> int:
    """Round half-up to a multiple of `unit` (e.g. 1000 for 千円単位)."""
    if not unit or unit <= 1:
        return round_yen(x)
    u = Decimal(unit)
    return int((D(x) / u).quantize(Decimal(1), rounding=ROUND_HALF_UP) * u)


def safe_div(a: Any, b: Any) -> Decimal | None:
    b = D(b)
    if b == 0:
        return None
    return D(a) / b


def product(values: Iterable[Any]) -> Decimal:
    out = Decimal(1)
    for v in values:
        out *= D(v)
    return out


# ------------------------------------------------------------------- formatting

def yen(n: Any) -> str:
    v = round_yen(n)
    sign = "-" if v < 0 else ""
    return f"{sign}¥{abs(v):,}"


def num(x: Any, places: int = 1) -> str:
    if x is None:
        return "—"
    v = q(x, places)
    return f"{v:,.{places}f}"


def pct(x: Any, places: int = 1) -> str:
    if x is None:
        return "—"
    return f"{q(D(x) * 100, places):.{places}f}%"


def md_table(headers: Sequence[str], rows: Iterable[Sequence[Any]], align: str | None = None) -> str:
    """Render a GitHub-flavoured markdown table. `align` is a string of l/r/c per column."""
    headers = [str(h) for h in headers]
    align = align or ("l" * len(headers))
    sep = {"l": "---", "r": "---:", "c": ":---:"}
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(sep.get(a, "---") for a in align) + "|"]
    for r in rows:
        lines.append("| " + " | ".join("" if c is None else str(c).replace("|", "\\|") for c in r) + " |")
    return "\n".join(lines)


def today() -> _dt.date:
    return _dt.date.today()


def now_iso() -> str:
    return _dt.datetime.now().replace(microsecond=0).isoformat()


def parse_date(s: Any, field: str = "date") -> _dt.date:
    if isinstance(s, _dt.date):
        return s
    try:
        return _dt.date.fromisoformat(str(s).replace("/", "-"))
    except ValueError:
        raise SierError(f"{field}: expected a date like 2026-07-31, got {s!r}") from None


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SierError(msg)


class Findings:
    """Collects warnings and errors so a run can report all problems at once."""

    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def raise_if_errors(self, what: str) -> None:
        if self.errors:
            bullet = "\n  - ".join(self.errors)
            raise SierError(f"{what} failed with {len(self.errors)} error(s):\n  - {bullet}")

    def as_dict(self) -> dict:
        return {"errors": list(self.errors), "warnings": list(self.warnings)}


def findings_md(f: Findings | dict) -> str:
    d = f.as_dict() if isinstance(f, Findings) else f
    out = []
    for e in d.get("errors", []):
        out.append(f"- ❌ {e}")
    for w in d.get("warnings", []):
        out.append(f"- ⚠️ {w}")
    return "\n".join(out) if out else "- ✅ No warnings."
