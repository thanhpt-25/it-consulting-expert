---
name: technical-solution
description: >
  Design and document technical solutions and system architectures for IT
  consulting proposals, grounded in customer RFP/RFQ from NotebookLM. Use this
  skill when the user asks to "design a solution", "propose an architecture",
  "create a technical proposal", "技術提案", "システム構成", "architecture
  diagram", "technology selection", "solution design", or needs to evaluate
  and recommend technology stacks, create system architecture documents, or
  produce technical feasibility assessments. Also trigger for "技術選定",
  "system design for proposal", "infrastructure design", "cloud architecture",
  "solution overview".
---

# Technical Solution Design

Create technical solution documents for IT consulting proposals, **grounded in RFP/RFQ technical requirements from NotebookLM**.

## Grounding

This skill reads the engagement's RFP Brief (`00-rfp-brief.json`) and never invents client requirements. Facts carry `[RFP]` / `[RFP+]` / `[Proposed]` labels as defined in `${CLAUDE_PLUGIN_ROOT}/shared/brief-schema.md`.

## Workflow

### Step 0: Load the engagement (Brief first — NotebookLM only for gaps)

Follow the handoff contract in `${CLAUDE_PLUGIN_ROOT}/shared/engagement-workspace.md`:

1. **Find the workspace:** `python3 "${CLAUDE_PLUGIN_ROOT}/sier" status`. None → run `engagement-init` first.
   (For a one-off question with no engagement, skip the workspace and label every assumption `[Proposed]`.)
2. **Read `00-rfp-brief.json`.** If `sier status` says it is missing or **stale**, run `rfp-notebook` first —
   do not extract the RFP yourself.
3. **From the Brief this skill needs:** `nonfunctional_requirements`, `constraints`, `integrations`, `data_migration`.
4. **Upstream files:** `01-go-nogo.json` for capability gaps flagged at bid time.
5. **Gaps only:** `python3 "${CLAUDE_PLUGIN_ROOT}/sier" brief gaps --for technical-solution`. If it reports no gaps, make
   **no** NotebookLM calls. Otherwise query only for those gaps, per `${CLAUDE_PLUGIN_ROOT}/shared/notebooklm-contract.md`
   (`--notebook <notebook_id> --json`, fallback ladder if NotebookLM is unreachable).
6. **Write back** each answer into `00-rfp-brief.json` as a labelled, cited item, remove the gap, then run
   `sier brief validate` and `sier brief render` so the next skill gets it free.

**Gap queries** — starting points when the Brief is missing one of the fields above:

```bash
notebooklm ask "What technology stack, platform, or framework requirements does the client specify or prefer?" --json --notebook <notebook_id>
notebooklm ask "List all system integration requirements — what external systems must this connect to and how?" --json --notebook <notebook_id>
notebooklm ask "What are the specific non-functional requirements with targets: performance (response time, throughput), availability (SLA %), scalability (user count), security standards?" --json --notebook <notebook_id>
notebooklm ask "What is the client's current IT infrastructure and technology landscape?" --json --notebook <notebook_id>
notebooklm ask "What security, compliance, or regulatory standards must the solution meet?" --json --notebook <notebook_id>
notebooklm ask "What data migration, conversion, or compatibility requirements exist?" --json --notebook <notebook_id>
notebooklm ask "Does the client specify any architectural preferences — microservices, cloud-native, on-premise, hybrid?" --json --notebook <notebook_id>
notebooklm ask "What are the disaster recovery, backup, or business continuity requirements?" --json --notebook <notebook_id>
```

### Step 1: Additional Context

After RFP extraction, ask the user for:
- Your company's technology strengths and preferred stacks
- Any technology partnerships or licensing advantages
- Known technical risks from similar past projects

### Step 2: Solution Architecture Document

**1. Solution Overview (ソリューション概要)**
- Problem statement from RFP
- Solution concept addressing each stated requirement
- High-level architecture diagram (mermaid)

**2. Architecture Design (アーキテクチャ設計)**

Produce these views, anchored to RFP requirements:

- **System Context Diagram**: system and its external actors/systems (from RFP integration list)
- **Container Diagram**: major components
- **Deployment Diagram**: infrastructure topology respecting RFP cloud/on-prem constraints
- **Data Flow Diagram**: how data moves, especially across integration points from the RFP

**3. Technology Stack Selection (技術選定)**

| Layer | RFP Requirement | Selected Technology | Alternatives | Rationale |
|-------|----------------|-------------------|-------------|-----------|

If the RFP mandates a technology → select it, note any risks.
If the RFP is open → propose with comparison matrix.

Read `references/tech-reference.md` for comparison matrices and reference architectures.

**4. Integration Design (連携設計)**
- Address each integration point identified from the RFP
- API design approach (REST, GraphQL, gRPC)
- Authentication between systems
- Data format and protocol for each interface

**5. Non-Functional Requirements (非機能要件)**

Map directly from RFP-extracted NFRs:

| Category | RFP Target | Design Approach | Confidence |
|----------|-----------|-----------------|------------|

If the RFP states "99.9% availability" → design for it and explain how.
If the RFP is silent on a category → propose a reasonable target, marked as "Proposed."

**6. Security Architecture (セキュリティ設計)**
- Address every security/compliance requirement from the RFP
- Authentication, authorization, encryption, network security
- Compliance mapping (ISMS, PCI-DSS, 個人情報保護法 — only what's in the RFP)

**7. Migration Strategy (移行戦略)** (if replacing existing system)
- Based on RFP migration requirements
- Approach, data migration plan, rollback strategy

**8. PoC / Feasibility (技術検証)**
- Flag RFP requirements that need proof of concept before commitment
- Technical risks from RFP scope that require prototyping

### Step 3: Output

Save the solution document as `02-architecture.md` in the engagement workspace — effort-estimation,
team-composition and the proposal writer all read it from there.

- **Diagrams:** use the `drawio` skill when it is available (C4 context/container views, network and
  deployment diagrams; export PNG for the proposal and keep the `.drawio` source in `artifacts/`).
  Otherwise use mermaid.
- **Trace every component to the Brief:** each NFR id (`NFR-*`) and integration id (`INT-*`) appears in the
  NFR compliance table with how the design meets it. An NFR with no answer is a finding, not an omission.
- **Ground cloud claims in vendor documentation.** For Azure designs, check service limits, SLAs and
  Japan-region availability with the Microsoft Learn tools when they are connected; for AWS/GCP, cite the
  provider's documentation. Don't quote an SLA percentage from memory.

## Key Principles

- **RFP constraints are non-negotiable** unless you explicitly propose alternatives with risk analysis
- **Simplicity**: Recommend the simplest architecture that meets RFP requirements
- **Client capability**: Consider the client's stated current infrastructure and team skills
- **Cost-aware**: Note operational cost implications of architecture choices
- **Traceability**: Every design decision links to an RFP requirement

For technology references, read `references/tech-reference.md`.
