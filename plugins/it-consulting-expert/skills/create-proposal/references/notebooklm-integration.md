# NotebookLM Integration Guide

## Purpose

NotebookLM serves as the **single source of truth** for all proposal-related data. Customer RFP/RFQ documents are uploaded there, and every skill in this plugin must extract information from NotebookLM rather than generating content from general knowledge. This prevents hallucination and ensures proposals are grounded in actual client requirements.

## Architecture

```
Customer RFP/RFQ → User uploads to NotebookLM → Notebook becomes source of truth
                                                         ↓
                                              Skills query via `notebooklm ask`
                                                         ↓
                                              Cited answers drive proposal content
```

## Setup Flow

### 1. Identify or Create the Notebook

Ask the user which NotebookLM notebook contains the RFP/RFQ. Run:

```bash
notebooklm list --json
```

If the user hasn't uploaded yet, guide them:

```bash
notebooklm create "RFP - [Client Name] - [Project Name]" --json
notebooklm source add ./rfp-document.pdf --json
notebooklm source wait <source_id> -n <notebook_id> --timeout 600
```

### 2. Set Notebook Context

```bash
notebooklm use <notebook_id>
```

Or use `-n <notebook_id>` / `--notebook <notebook_id>` on each command for parallel safety.

### 3. Verify Sources Are Ready

```bash
notebooklm source list --json
```

All sources must show `"status": "ready"` before querying.

## Querying Patterns

### Extraction Queries

Use targeted questions to extract specific information from the RFP/RFQ. Always use `--json` to get citations.

**Requirements extraction:**
```bash
notebooklm ask "List all functional requirements mentioned in the RFP" --json
notebooklm ask "List all non-functional requirements (performance, security, availability, scalability)" --json
notebooklm ask "What are the mandatory technology constraints or platform requirements?" --json
```

**Scope extraction:**
```bash
notebooklm ask "What is the project scope? What is explicitly in-scope and out-of-scope?" --json
notebooklm ask "What are the key deliverables the client expects?" --json
notebooklm ask "What acceptance criteria or success metrics does the client define?" --json
```

**Timeline and budget:**
```bash
notebooklm ask "What timeline or deadline does the client specify?" --json
notebooklm ask "Is there a stated budget range or budget constraints?" --json
notebooklm ask "What are the key milestones or phase gates the client expects?" --json
```

**Technical context:**
```bash
notebooklm ask "Describe the client's current IT systems and infrastructure mentioned in the document" --json
notebooklm ask "What integrations with existing systems are required?" --json
notebooklm ask "What security, compliance, or regulatory requirements are mentioned?" --json
```

**Team and process:**
```bash
notebooklm ask "What team structure, roles, or staffing requirements does the client specify?" --json
notebooklm ask "Does the client prefer a specific development methodology (waterfall, agile, hybrid)?" --json
notebooklm ask "What evaluation criteria will the client use to assess proposals?" --json
```

### Using Citations

The `--json` flag returns citations that trace every answer back to the source document:

```json
{
  "answer": "The client requires 99.9% uptime [1] and response time under 2 seconds [2]",
  "references": [
    {"citation_number": 1, "cited_text": "System availability must be 99.9%..."},
    {"citation_number": 2, "cited_text": "All API responses within 2 seconds..."}
  ]
}
```

**Rules for using citations:**
- Only include requirements, numbers, or constraints that appear in citations
- If NotebookLM's answer lacks a citation for a specific claim, flag it as an assumption
- When the RFP is silent on a topic, explicitly state "Not specified in RFP" and propose a reasonable default

### Multi-Turn Conversations

For complex extraction, use conversation continuity:

```bash
# First query
notebooklm ask "What are the main project objectives?" --json
# → returns conversation_id in JSON

# Follow-up using same conversation
notebooklm ask "For each objective, what specific KPIs does the client mention?" --json -c <conversation_id>
```

## Grounding Rules

These rules apply to ALL skills in this plugin:

### MUST DO
1. **Query NotebookLM first** before writing any proposal section
2. **Use `--json` flag** on all `notebooklm ask` calls to get traceable citations
3. **Attribute all client-specific facts** to the source document
4. **Mark assumptions explicitly** when the RFP doesn't cover a topic: "Not specified in RFP — proposed based on industry practice"
5. **Verify numbers** — if the RFP states a budget, timeline, or metric, use that exact number

### MUST NOT
1. **Do NOT invent client requirements** — if the RFP doesn't mention it, don't claim the client needs it
2. **Do NOT assume technology preferences** unless the RFP states them
3. **Do NOT fabricate evaluation criteria** — extract them from the RFP
4. **Do NOT guess budget ranges** — use what the client states or mark as TBD
5. **Do NOT hallucinate past project references** — only include verifiable information

### SHOULD DO
1. **Augment with industry knowledge** where the RFP is silent, but clearly label it as a recommendation
2. **Propose alternatives** when the RFP's stated approach has known risks
3. **Fill gaps** with professional judgment, always marking these sections as "Proposed" vs "Required"

## Notebook ID Management

Each proposal engagement should have its own notebook. Track the mapping:

```
Client A - Project X → notebook_id: abc123...
Client B - Project Y → notebook_id: def456...
```

When the user says "create a proposal for Client A", ask which notebook contains their RFP, or list notebooks with `notebooklm list` to help them find it.

## Source Types

Common RFP/RFQ document types that can be added as sources:
- PDF documents (most common for formal RFPs)
- Word documents (.docx)
- Web URLs (for online RFPs or client websites)
- Google Docs (if client shares via Google Workspace)
- Text files, Markdown

Multiple sources per notebook are supported — add the main RFP plus any appendices, amendments, or Q&A documents.
