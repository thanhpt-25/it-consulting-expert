# NotebookLM Contract

Canonical rules for every skill that touches NotebookLM. Read this instead of
re-deriving CLI usage per skill.

## 1. Flag rules — the two flags are NOT interchangeable

| Flag | Valid on |
|------|----------|
| `-n <notebook_id>` | `artifact wait`, `source wait`, `research wait`, `research status`, `download *` |
| `--notebook <notebook_id>` | every other command, including `ask`, `source add`, `source list`, `status` |

Passing `-n` to `ask` is a **silent failure mode**: it either errors, or falls back to
whatever `notebooklm use` last wrote — possibly another engagement's notebook.

## 2. Never rely on `notebooklm use`

`use` writes to a shared global file (`~/.notebooklm/context.json`). Concurrent agents
overwrite each other's context. **Always pass the notebook explicitly on every command.**
For parallel agents, additionally isolate config: `export NOTEBOOKLM_HOME=/tmp/agent-$ID`.

## 3. Always `--json`

Every `ask` carries `--json` so the answer arrives with `references[].cited_text`.
A fact without a citation cannot be labelled `[RFP]`.

## 4. Fallback ladder — no skill may hard-stop at Step 0

Attempt in order, and record which tier produced the data:

| Tier | Mechanism | When | Grounding quality |
|------|-----------|------|-------------------|
| 1 | `notebooklm` CLI | Authenticated and sources ready | Full — citations available |
| 2 | `notebooklm-web` browser skill | CLI unavailable or unauthenticated | Full — citations available |
| 3 | Direct read of the source files (`pdf` / `docx` skill, `Read`) | NotebookLM unreachable, but the RFP is on disk or attached | Reduced — cite by page/section instead of NotebookLM reference |
| 4 | Ask the user | No sources reachable at all | None — do not fabricate; stop and report |

Record the tier used in the engagement's RFP Brief header. Tier 3 output is still valid
consulting work; it simply carries page citations rather than NotebookLM references.
Never silently degrade — the Brief must state which tier produced it.

## 5. Query budget

`rfp-notebook` is the **only** skill that runs the full extraction. Downstream skills read
the Brief it produces and query NotebookLM only for fields the Brief marks as gaps.
