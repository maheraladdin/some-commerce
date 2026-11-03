# Tasks Template: [Feature / Story Name]

## Phase 1: Core Domain Logic, Types & Constants
- [ ] Task 1.1: Define strongly typed models in `behaviours/<name>/types/`
- [ ] Task 1.2: Define routes, error keys, and limits in `behaviours/<name>/constants/`
- [ ] Task 1.3: Implement pure domain logic & state machines in `behaviours/<name>/logic/`
- [ ] Task 1.4: Write unit and property tests verifying domain invariants

## Phase 2: Services & Infrastructure Adapters
- [ ] Task 2.1: Implement API client / repository adapters in `behaviours/<name>/services/`
- [ ] Task 2.2: Implement RFC 9110 ETag headers and caching integration
- [ ] Task 2.3: Integrate WatermelonDB local-first persistence or server sync
- [ ] Task 2.4: Write service integration and mock-free contract tests

## Phase 3: Designs & Platform-Adaptive UI
- [ ] Task 3.1: Build platform-adaptive UI screens / components in `behaviours/<name>/designs/`
- [ ] Task 3.2: Connect Headless Hooks from `logic/` to UI components in `designs/`
- [ ] Task 3.3: Implement RTL/LTR bidirectional styling and localized fonts
- [ ] Task 3.4: Write component tests for loading, empty, error, and offline states

## Phase 4: Security Gateway & Verification (G0–G4)
- [ ] Task 4.1: Execute security audit abuse tests (rate limits, IDOR, tampering)
- [ ] Task 4.2: Verify zero-trust tenant isolation on all queries and mutations
- [ ] Task 4.3: Execute SAST / secret scanning / dependency checks
- [ ] Task 4.4: Complete G2 Security Gateway sign-off and compile integrated evidence
