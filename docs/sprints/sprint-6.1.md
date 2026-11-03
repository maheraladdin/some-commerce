# Sprint 6.1 — SDUI Visual Studio + Dual-Edition Toggle

> **Slice**: v6.0 · **Duration**: Weeks 19–20 · **Story Points**: 29

## Goal

Build the visual drag-and-drop SDUI Studio with dual-viewport preview, version history, and implement the dual-edition deployment toggle (Standard vs. Managed Instances).

## User Stories

| Priority | Story | Module | Points | Description |
|:---------|:------|:-------|:-------|:------------|
| P0 | [US-12.1.1](../user-stories/12-admin-and-sdui-studio/us-12.1.1-visual-drag-and-drop-sdui-studio.md) | Admin | 13 | Visual SDUI Studio |
| P0 | [US-12.1.2](../user-stories/12-admin-and-sdui-studio/us-12.1.2-dual-edition-deployment-standard-vs-managed-instances.md) | Admin | 8 | Dual-edition deployment |
| P1 | [US-8.1.2](../user-stories/08-webmcp-and-ai/us-8.1.2-admin-webmcp-store-copilot.md) | WebMCP | 5 | Admin AI copilot integration with studio |
| P2 | Cache telemetry | Observability | 3 | L1/L2/ETag cache hit ratio dashboard |

## Definition of Done

- [ ] Drag-and-drop blocks work in SDUI studio
- [ ] Dual-viewport (ar-EG RTL + en-US LTR) previews render correctly
- [ ] Draft → Publish flow evicts all caches
- [ ] Version history rollback works
- [ ] computeMode toggle deploys correct Lambda configuration

## Mandatory Story Validation

- [ ] Every story delivered in this sprint passes [G0–G4](../QUALITY_GATES.md), including its tailored test, security and architecture checks; attach a [story evidence record](../validation/STORY_EVIDENCE_TEMPLATE.md).
- [ ] Resolve relevant [design and dependency blockers](../DOCS_STRESS_TEST.md) before commitment/release. Partial story work remains In Progress; P1/P2 priority does not exempt it from gates.
- [ ] Non-story tasks that change production behavior use the same gates and have an accountable owner and evidence record.
