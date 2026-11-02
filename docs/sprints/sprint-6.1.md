# Sprint 6.1 — SDUI Visual Studio + Dual-Edition Toggle

> **Slice**: v6.0 · **Duration**: Weeks 19–20 · **Story Points**: 30

## Goal

Build the visual drag-and-drop SDUI Studio with dual-viewport preview, version history, and implement the dual-edition deployment toggle (Standard vs. Managed Instances).

## User Stories

| Priority | Story | Module | Points | Description |
|:---------|:------|:-------|:-------|:------------|
| P0 | [US-12.1.1](../user-stories/12-admin-and-sdui-studio/README.md#us-1211-visual-drag-and-drop-sdui-studio) | Admin | 13 | Visual SDUI Studio |
| P0 | [US-12.1.2](../user-stories/12-admin-and-sdui-studio/README.md#us-1212-dual-edition-deployment-standard-vs-managed-instances) | Admin | 8 | Dual-edition deployment |
| P1 | [US-8.1.2](../user-stories/08-webmcp-and-ai/README.md#us-812-admin-webmcp-store-copilot) | WebMCP | 5 | Admin AI copilot integration with studio |
| P2 | Cache telemetry | Observability | 3 | L1/L2/ETag cache hit ratio dashboard |

## Definition of Done

- [ ] Drag-and-drop blocks work in SDUI studio
- [ ] Dual-viewport (ar-EG RTL + en-US LTR) previews render correctly
- [ ] Draft → Publish flow evicts all caches
- [ ] Version history rollback works
- [ ] computeMode toggle deploys correct Lambda configuration
