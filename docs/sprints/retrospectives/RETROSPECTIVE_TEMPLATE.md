# Sprint Retrospective: SPRINT-[ID]

> **Sprint Identifier**: `Sprint X.Y (e.g. Sprint 1.1)`  
> **Facilitator**: `sprint-X.Y-tech-lead`  
> **Participants**: `sprint-X.Y-product-manager`, Junior & Senior Engineers, QA, Security, CTO  
> **Date**: `YYYY-MM-DD`

---

## 1. Sprint Summary Metrics

| Metric | Planned | Actual | Variance / Notes |
|:-------|:--------|:-------|:-----------------|
| **Committed Story Points** | *XX pts* | *YY pts* | *Velocity calculation* |
| **Stories Delivered (G4)** | *N stories* | *M stories* | *Completion rate* |
| **Average PR Lead Time** | *X hours* | *Y hours* | *Junior-to-senior review latency* |
| **Quality Gate SG0–SG4 Passes** | *5 / 5* | *5 / 5* | *Zero skipped gates* |
| **Critical/High Defects Detected**| *0* | *0* | *ASVS L2 audit results* |

---

## 2. What Went Well

- *Highlight 1: Successful decoupling of Axum handlers from Lambda runtime.*
- *Highlight 2: Moka L1 cache hit rate exceeded 94% in benchmark tests.*
- *Highlight 3: Zero merge conflicts due to strict agent workdir isolation.*

---

## 3. What Went Wrong / Areas for Improvement

- *Friction 1: Initial fuzz test setup exceeded memory budget on local developer machines.*
- *Friction 2: Ambiguity in carrier rate response types required mid-sprint clarification.*

---

## 4. Root-Cause Analyses of Stalled Gates or Defects

| Issue / Failure | Root Cause (5 Whys) | Corrective Action | Owner |
|:----------------|:--------------------|:------------------|:------|
| *Example: E1 latency spike* | *Cache key serialization invoked unnecessary clone* | *Switched to byte slice borrowing & ArcSwap* | `senior-be-1` |

---

## 5. Action Items & Process Adaptations

| # | Action Item | Target Sprint | Responsible Role | Status |
|:--|:------------|:--------------|:-----------------|:-------|
| 1 | *Update Loom test harness template with bounded preemption flags* | `Sprint X+1` | `system-architect` | *Open* |
| 2 | *Tune cargo-fuzz memory limits to 2048MB in CI* | `Sprint X+1` | `devops-engineer` | *Open* |
