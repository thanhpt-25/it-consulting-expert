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
metadata:
  version: "0.2.0"
---

# Technical Solution Design

Create technical solution documents for IT consulting proposals, **grounded in RFP/RFQ technical requirements from NotebookLM**.

## NotebookLM-First Rule

The RFP defines what the client needs technically. Query NotebookLM for every technical constraint, integration requirement, NFR target, and platform mandate before designing anything. A beautiful architecture that ignores the RFP's technology constraints is a rejected proposal.

## Workflow

### Step 0: Extract Technical Requirements from NotebookLM

```bash
notebooklm ask "What technology stack, platform, or framework requirements does the client specify or prefer?" --json
notebooklm ask "List all system integration requirements — what external systems must this connect to and how?" --json
notebooklm ask "What are the specific non-functional requirements with targets: performance (response time, throughput), availability (SLA %), scalability (user count), security standards?" --json
notebooklm ask "What is the client's current IT infrastructure and technology landscape?" --json
notebooklm ask "What security, compliance, or regulatory standards must the solution meet?" --json
notebooklm ask "What data migration, conversion, or compatibility requirements exist?" --json
notebooklm ask "Does the client specify any architectural preferences — microservices, cloud-native, on-premise, hybrid?" --json
notebooklm ask "What are the disaster recovery, backup, or business continuity requirements?" --json
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

Generate as a structured document section or standalone technical proposal. Include mermaid diagrams for architecture views.

## Key Principles

- **RFP constraints are non-negotiable** unless you explicitly propose alternatives with risk analysis
- **Simplicity**: Recommend the simplest architecture that meets RFP requirements
- **Client capability**: Consider the client's stated current infrastructure and team skills
- **Cost-aware**: Note operational cost implications of architecture choices
- **Traceability**: Every design decision links to an RFP requirement

For technology references, read `references/tech-reference.md`.
