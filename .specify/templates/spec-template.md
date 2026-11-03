# Spec Template: [Feature / Story Name]

## 1. Specification Metadata
- **Identifier**: [STORY-ID / SPEC-ID]
- **Feature**: [Feature Name]
- **Module**: [Module Name]
- **Behaviour**: [Behaviour Name]
- **Sprint / Milestone**: [Sprint X.Y]
- **Status**: [Draft | In Review | Approved | In Progress | Done]

## 2. User Story & Domain Narrative
**As a** [Persona / Role],  
**I want to** [Action / Capability],  
**So that** [Business Value / Benefit].

### 2.1 Preconditions
- [Precondition 1]
- [Precondition 2]

### 2.2 Postconditions
- [Postcondition 1]
- [Postcondition 2]

## 3. Acceptance Criteria (Gherkin)
```gherkin
Feature: [Feature Name]

  Scenario: [Scenario 1 Title]
    Given [Initial context]
    When [Action occurred]
    Then [Expected outcome]
```

## 4. Non-Functional & Performance Budgets
- **Latency Budget**: [e.g. p95 < 200ms]
- **Offline / Caching SLA**: [e.g. 0ms render from local WatermelonDB]
- **Error Budget**: [e.g. < 0.01% server failure rate]
