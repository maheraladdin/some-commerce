#!/usr/bin/env python3
"""
Updates all 12 sprint markdown files with:
1. Multi-Agent Implementation Plan dependent on the 3 core execution profiles:
   - backend-engineer (junior author + senior reviewer)
   - client-engineer (junior author + senior reviewer)
   - qa-security-auditor (junior tester + senior auditor)
2. The 6-Layer Governance Ladder (Junior Author -> Senior Reviewer -> Security/Architect -> Tech Lead -> PM -> CTO Agreement).
3. Agent Profile Load Balancer Allocation Matrix and Dedicated Workdirs.
4. Story-by-story 10-PR Vertical Slicing Pipeline with explicit Junior Author & Senior Reviewer pairings.
5. Sprint Quality Gates Execution Matrix (SG0–SG4, Gate A1, Gate A2, Gate M1).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


REPO_ROOT = Path(__file__).resolve().parents[2]
from scripts.agents.agent_load_balancer import AgentProfileLoadBalancer, parse_sprint_stories, PR_SPECS, COMPANY_PIPELINE
from scripts.documentation.sprint_closeout import append_closeout

SPRINT_FILES = sorted((REPO_ROOT / "docs" / "sprints").glob("sprint-*.md"))


def _build_execution_plan_markdown(sprint_id: str) -> str:
    """Builds the comprehensive multi-agent implementation plan for a sprint."""
    if sprint_id == "sprint-6.3":
        return f"""
---

## Multi-Agent Hardening & Launch Orchestration Plan (6-Layer Governance)

Sprint 6.3 is the final hardening and launch verification milestone. Engineering tasks are distributed across the junior-senior agent hierarchy and governed by the 6-Layer Validation Ladder:

### 1. Agent Roster & Load Balancer Allocation
| Worker ID | Profile | Seniority | Specialized Role | Primary Focus & Verification | Dedicated Workdir |
|:----------|:--------|:----------|:-----------------|:-----------------------------|:------------------|
| `{sprint_id}-junior-be-1` | `backend-engineer` | `junior` | `backend-builder` | DynamoDB Capacity, GSI index optimization, hot partition mitigation | `.agents/workspaces/{sprint_id}/{sprint_id}-junior-be-1` |
| `{sprint_id}-junior-be-2` | `backend-engineer` | `junior` | `backend-tester` | Chaos injection tests (KMS outage, carrier timeout, Redis failover) | `.agents/workspaces/{sprint_id}/{sprint_id}-junior-be-2` |
| `{sprint_id}-senior-be-1` | `backend-engineer` | `senior` | `reviewer` | Peer code review, zero-clone borrowing audit, Gate M1 certification | `.agents/workspaces/{sprint_id}/{sprint_id}-senior-be-1` |
| `{sprint_id}-junior-fe-1` | `client-engineer` | `junior` | `client-builder` | CloudFront cache policies, client bundle size optimization (<2.5MB) | `.agents/workspaces/{sprint_id}/{sprint_id}-junior-fe-1` |
| `{sprint_id}-junior-fe-2` | `client-engineer` | `junior` | `client-tester` | Offline reconnect drills, RTL layout stress testing on physical devices | `.agents/workspaces/{sprint_id}/{sprint_id}-junior-fe-2` |
| `{sprint_id}-senior-fe-1` | `client-engineer` | `senior` | `reviewer` | Peer code review, LoB compliance audit, WCAG 2.1 AA certification | `.agents/workspaces/{sprint_id}/{sprint_id}-senior-fe-1` |
| `{sprint_id}-junior-qa-1` | `testing-qa-engineer` | `junior` | `tester` | E2E test runs across mobile & web platforms | `.agents/workspaces/{sprint_id}/{sprint_id}-junior-qa-1` |
| `{sprint_id}-senior-qa-1` | `security-engineer` | `senior` | `auditor` | Final OWASP ASVS L2 audit, penetration testing, Gate M1/A1/A2 sign-off | `.agents/workspaces/{sprint_id}/{sprint_id}-senior-qa-1` |
| `{sprint_id}-tech-lead` | `tech-lead` | `lead` | `lead` | Sprint integration, Gate G1/G4 verification, PR merge coordination | `.agents/workspaces/{sprint_id}/{sprint_id}-tech-lead` |
| `{sprint_id}-product-manager` | `product-manager` | `lead` | `pm` | Product acceptance sign-off across all user stories | `.agents/workspaces/{sprint_id}/{sprint_id}-product-manager` |
| `{sprint_id}-cto` | `chief-technology-officer` | `executive` | `cto` | Executive architectural agreement & final SG4 production release authorization | `.agents/workspaces/{sprint_id}/{sprint_id}-cto` |

### 2. The 6-Layer Governance Ladder
1. **Layer 1 (Junior Execution)**: Implements capacity tuning, chaos suites, and bundle optimization.
2. **Layer 2 (Senior Peer Review)**: Audits code against zero-clone laws, memory limits, and LoB rules.
3. **Layer 3 (Security & Architect Gate)**: Verifies Gate G2 (ASVS L2), Gate A1 (system arch), Gate A2 (folder layout), Gate M1 (microkernel).
4. **Layer 4 (Tech Lead Integration)**: Verifies monorepo regression suites pass with 0 failures.
5. **Layer 5 (Product Manager Acceptance)**: Confirms product readiness across all customer and admin flows.
6. **Layer 6 (CTO Agreement)**: Grants final executive agreement and authorizes production release.

### 3. Sprint Quality Gates Sign-Off (SG0 — SG4)
- [ ] **SG0 (Readiness)**: Hardening backlogs, chaos injection parameters, and benchmark targets approved.
- [ ] **SG1 (Integration)**: Full platform end-to-end regression test suite passes (0 failures).
- [ ] **SG2 (Security Audit)**: Monorepo ASVS L2 verification; zero critical/high CVEs; 0 cross-tenant leaks.
- [ ] **SG3 (Architecture & Gate M1/A1/A2)**: Gate M1 (zero-clone), Gate A1 (system arch), and Gate A2 (folder layout) verified.
- [ ] **SG4 (Production Release Candidate)**: p99 search latency < 50ms under 1,000 concurrent virtual users; production rollback drill verified; **CTO Agreement Granted**.
"""

    balancer = AgentProfileLoadBalancer(
        sprint_id,
        junior_be_workers=2,
        junior_fe_workers=2,
        junior_qa_workers=1,
    )
    plan = balancer.balance_sprint()

    md = f"""
---

## Multi-Agent Sprint Implementation Plan (6-Layer Governance)

Engineering delivery for **{sprint_id.upper()}** is executed by autonomous agent instances organized into **Junior Implementer / Senior Reviewer pairs** and governed by the **6-Layer Validation Ladder** leading up to **Product Manager Acceptance** and **CTO Agreement**.

Every agent operates inside an isolated working directory (`workdir`) with whitelisted write paths to guarantee **zero file conflicts**.

```mermaid
flowchart TD
    subgraph "Sprint Backlog: {sprint_id.upper()}"
        STORIES["{plan['total_stories']} User Stories × 10 PR Slices<br/>({plan['total_prs']} Discrete Vertical Tasks)"]
    end

    subgraph "The 6-Layer Validation Ladder"
        L1["<b>Layer 1: Junior Author</b><br/>Writes PR 1–10 in isolated workdir"]
        --> L2["<b>Layer 2: Senior Reviewer</b><br/>Audits Zero-Clone, LoB & ASVS (APPROVE)"]
        --> L3["<b>Layer 3: Security & Architect</b><br/>Gate G2 & Gates A1, A2, M1"]
        --> L4["<b>Layer 4: Tech Lead & Gatekeeper</b><br/>Cross-PR Integration & G1/G4 Sign-Off"]
        --> L5["<b>Layer 5: Product Manager (PM)</b><br/>Gherkin AC Acceptance Sign-Off"]
        --> L6["<b>Layer 6: Chief Technology Officer (CTO)</b><br/>Executive Agreement & SG4 Release"]
    end

    STORIES --> L1
```

### 1. Agent Roster & Load Balancer Allocation
| Worker ID | Core Profile | Seniority | Specialized Role | Assigned Tasks / Reviews | Dedicated Sprint Workdir |
|:----------|:-------------|:----------|:-----------------|:-------------------------|:-------------------------|
"""
    for wid, wdata in plan["workers"].items():
        workdir_rel = f".agents/workspaces/{sprint_id}/{wid}"
        if wdata["seniority"] == "junior":
            activity = f"{wdata['total_tasks']} implementation tasks"
        else:
            activity = f"{wdata['total_reviews']} peer reviews"
        md += f"| `{wid}` | `{wdata['profile']}` | `{wdata['seniority']}` | `{wdata['role']}` | {activity} | `{workdir_rel}` |\n"

    # Add leadership entries
    md += f"| `{sprint_id}-tech-lead` | `tech-lead` | `lead` | `lead` | Cross-story integration & G1/G4 sign-off | `.agents/workspaces/{sprint_id}/{sprint_id}-tech-lead` |\n"
    md += f"| `{sprint_id}-product-manager` | `product-manager` | `lead` | `pm` | Layer 5 Product Acceptance Sign-Off | `.agents/workspaces/{sprint_id}/{sprint_id}-product-manager` |\n"
    md += f"| `{sprint_id}-cto` | `chief-technology-officer` | `executive` | `cto` | Layer 6 Executive Agreement & SG4 Sign-Off | `.agents/workspaces/{sprint_id}/{sprint_id}-cto` |\n"

    md += f"""
### 2. Non-Conflicting Concurrency & Directory Whitelisting
To ensure conflict-free parallel execution across agents working on the same user story:
- **Backend Track (`backend-engineer`)**: Writes exclusively to `crates/**` and `backend/**`. Operates under the **Rust Zero-Clone Law** and pure microkernel trait contracts. Junior authors submit PRs to `{plan['story_allocations'][0]['prs'][0]['senior_reviewer']}` for code review.
- **Client Track (`client-engineer`)**: Writes exclusively to `apps/storefront/src/features/**` and `packages/**`. Operates under **Locality of Behavior (LoB)** and `@expo/ui` native guidelines. Junior authors submit PRs to `{plan['story_allocations'][0]['prs'][6]['senior_reviewer']}` for code review.
- **Security & Quality Track (`qa-security-auditor`)**: Writes exclusively to `docs/validation/**` and test execution runners. Junior testers submit test suites to `{plan['story_allocations'][0]['qa_auditor']['senior_reviewer']}`.
- **Contract Synchronization**: Once PR 2 merges schema definitions and generates TypeScript types via `ts-rs`, Backend (PR 3–6) and Client (PR 7–10) execute simultaneously without blocking.

### 3. Story-by-Story 10-PR Slicing Pipeline with Junior Author & Senior Reviewer Pairings
Every story in this sprint is decomposed into the standardized 10 PRs (aligned with the 10-Pillar System Architecture) with assigned Junior Authors and Senior Reviewers:
"""

    gate_req_map = {
        1: "Gate M1 + Proptest (Pillar 1)",
        2: "Polyglot Schema Codegen (Pillar 2)",
        3: "Repository & TransactWrite (Pillar 3)",
        4: "Redis L2 + Invalidation (Pillar 4)",
        5: "Moka L1 TinyLFU + Coalescing (Pillar 5)",
        6: "BLAKE3 ETag + Pure Axum (Pillar 6)",
        7: "TanStack Query + ETag Client (Pillar 7)",
        8: "WatermelonDB Delta Sync (Pillar 8)",
        9: "Headless Hooks State Machine (Pillar 9)",
        10: "@expo/ui Native + RTL Parity (Pillar 10)",
    }

    for s in plan["story_allocations"]:
        md += f"\n#### Story [{s['story_id'].upper()}]: {s['title']} ({s['points']} Story Points)\n"
        md += f"- **Layer 5 Product Manager Acceptance**: `{s['governance']['layer_5_product_manager']}`\n"
        md += f"- **Layer 6 CTO Executive Agreement**: `{s['governance']['layer_6_cto_agreement']}`\n\n"
        md += "| PR # | Architectural Slice | Target Layers | Junior Author (Layer 1) | Senior Reviewer (Layer 2) | Gate Requirement |\n"
        md += "|:-----|:--------------------|:--------------|:------------------------|:--------------------------|:-----------------|\n"
        for pr in s["prs"]:
            pr_info = PR_SPECS[pr["pr_num"]]
            target_layers = ", ".join([f"`{l}`" for l in pr_info["layers"]])
            gate_req = gate_req_map.get(pr["pr_num"], "Quality Gate Pass")
            md += f"| **PR {pr['pr_num']}** | {pr['pr_name']} | {target_layers} | `{pr['junior_author']}` | `{pr['senior_reviewer']}` | {gate_req} |\n"

    md += f"""
### 4. Sprint Quality Gates Progression
- [ ] **SG0 (Planning Readiness)**: 100% of backlog stories pass Gate G0; microkernel ports and crate boundaries mapped.
- [ ] **SG1 (Cross-Story Integration)**: End-to-end integration flows across all {plan['total_stories']} stories pass under concurrent load.
- [ ] **SG2 (Security & Tenant Isolation)**: Synthetic multi-tenant penetration testing confirms 0 data leaks across sprint endpoints.
- [ ] **SG3 (Architecture & Gate M1/A1/A2)**:
  - Gate M1: `python3 scripts/validation/validate_microkernel.py` passes (zero cloud SDKs in pure crates, zero-clone compliance).
  - Gate A1: `python3 scripts/validation/validate_system_architecture.py` passes (10-layer architectural contracts verified).
  - Gate A2: `python3 scripts/validation/validate_folder_architecture.py` passes (framework-scoped LoB folder layout verified).
- [ ] **SG4 (Release Candidate & Operations)**: Staging smoke tests pass across mobile and web; p95 latency < 150ms; **Product Manager Acceptance (Layer 5)** and **CTO Agreement (Layer 6)** granted.
"""
    return md


def build_sprint_agent_plan_markdown(sprint_id: str) -> str:
    execution = _build_execution_plan_markdown(sprint_id)
    first_heading_end = execution.index("\n", execution.index("## Multi-Agent"))
    contract = "\n\n### Company planning → role execution → upward validation\n\n"
    contract += "**Status: allocation proposal, not dispatch authorization.** Leadership planning precedes the junior roster; the L1–L6 ladder below is the upward review path. Approve P0–P4 and the company master-plan revision before implementation.\n\n"
    contract += "| Stage | Accountable role | Required output |\n|:------|:-----------------|:----------------|\n"
    contract += "\n".join(f"| {stage['phase']} | `{stage['owner']}` | {stage['output']} |" for stage in COMPANY_PIPELINE)
    contract += "\n\nUse the [company plan template](../../.specify/templates/company-plan-template.md). Every task references its master-plan parent and canonical `docs/validation/story-records/US-<id>.md`; log each action/result and next-role receipt there. Collect all expected children, verify the exact assembled candidate and closeout suites, then return product acceptance and the full dossier to CTO. Missing children, action history or required checks block parent acceptance.\n"
    return execution[:first_heading_end] + contract + execution[first_heading_end:]


def compose_sprint_plan(content: str, sprint_id: str, plan_md: str) -> str:
    """Replace generated sections, preserve authored prefix, and keep closeout last."""
    for heading in ("## Multi-Agent Sprint Implementation Plan", "## Multi-Agent Hardening & Launch Orchestration Plan", "## End-of-Sprint Test Gate"):
        content = content.split(heading, 1)[0].rstrip()
    while content.endswith("\n---"):
        content = content[:-4].rstrip()
    return append_closeout(f"{content}\n\n{plan_md.strip()}\n", sprint_id)


def main():
    print("Updating implementation plans across all 12 sprint markdown files with 6-layer governance...")
    updated_count = 0

    for sprint_file in SPRINT_FILES:
        sprint_id = sprint_file.stem
        content = sprint_file.read_text(encoding="utf-8")

        plan_md = build_sprint_agent_plan_markdown(sprint_id)
        new_content = compose_sprint_plan(content, sprint_id, plan_md)
        sprint_file.write_text(new_content, encoding="utf-8")
        print(f"  - Updated: {sprint_file.name}")
        updated_count += 1

    print(f"\nSUCCESS: Successfully updated {updated_count} sprint implementation plans with 6-layer governance!")


if __name__ == "__main__":
    main()
