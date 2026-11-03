# User story validation gates

## Scope and status

These gates apply to **every user story**, every implementation PR, and every production slice. They replace weaker sprint checklists and blanket claims of “100% test coverage.” Each story contains additional, story-specific requirements. Passing documentation validation means only that the required sections and references exist; it does not mean the application has been tested or audited.

The repository currently contains specifications and documentation utilities, with no application manifests, implementation, or application CI. Application gates below are **required but not implemented**. No story has passed them. The [stress-test register](DOCS_STRESS_TEST.md) lists unresolved design and delivery blockers.

## Gate sequence and ownership

| Gate | Required before | Accountable reviewer | Pass condition |
|:-----|:----------------|:---------------------|:---------------|
| G0 — Ready | Starting implementation | Story owner + domain reviewer | Acceptance criteria and existing TC IDs mapped; affected layers, dependencies, data ownership, threat boundaries, measurable budgets, and linked design blockers resolved. Assign named reviewers and evidence location. |
| G1 — Tests and coverage | Merging each PR | Test reviewer | Relevant automated tests pass, coverage meets the thresholds below, every changed acceptance outcome has an assertion, and story-specific failure scenarios are tested. |
| G2 — Security audit | Merging each PR | Security reviewer | Threat review, applicable scans, and adversarial tests pass; no open critical/high findings; lower-severity findings have an owner and due date. |
| G3 — Architecture and maintainability | Merging each PR | Architecture reviewer | Dependency boundaries, reuse, complexity, readability, and changeability checks pass with a recorded review. |
| G4 — Integrated acceptance | Marking the story Done or releasing it | Story owner + release reviewer | Complete story works across its affected layers/platforms, required provider sandbox checks and operational drills pass, and all G0–G3 evidence refers to the release candidate commit. |

Reviewers must be identified; “reviewed by agent” without an identity and evidence is insufficient. An implementation author cannot be the sole approver of G2 or G3. One qualified independent reviewer may cover multiple roles. Splitting work into several PRs does not defer tests, security, or architecture until the last PR. A partially implemented story stays In Progress and is inaccessible in production until G4 passes.

## G0 — Ready

- Give every Gherkin scenario a stable `AC-<story>-NN` identifier before implementation. Preserve existing `TC-*` identifiers. Map each AC, existing TC, and story gate scenario to test name, path, level, expected assertion, and evidence. Table entries with no executable assertion are unimplemented requirements.
- Record scope: API/routes, events, schemas, supported platforms, tenancy/roles, migrations, external providers, and dependencies. Link an ADR for new boundaries, incompatible contracts, consistency models, or shared business policies. Small changes can use a PR design note.
- Resolve applicable blocking findings in the stress-test register. For every unresolved product choice, record an accountable owner and decision deadline before its dependent story starts. Do not silently select different policies in different stories.
- For each measurable feature, set a numeric latency/error/resource budget and test environment. Specify dataset size, device/browser, cold/warm state, concurrency/arrival rate, run length, percentile, sample count, and dependency latency. “Instant,” “unlimited,” “zero cost,” and “no lag” are not pass criteria.

## G1 — Tests and coverage

The following thresholds are project defaults, not a guarantee of correctness:

| Measurement | Required result |
|:------------|:----------------|
| Acceptance traceability | 100% of this story's ACs, existing TCs, and added gate scenarios mapped to passing tests or explicit reviewed manual evidence where automation is impractical. No unexplained omissions. |
| Changed handwritten production code | At least 90% line and 85% branch coverage in **each** affected Rust/TypeScript package, measured against the PR base. Do not average weak packages into stronger ones. |
| Critical domain modules | At least 95% branch coverage for authorization, money/allocation, stock reservations, payment/refund transitions, license verification, and metering. All identified invariant and deny/error outcomes require tests even if the percentage already passes. |
| Existing baseline | No reduction in total line or branch coverage for an affected package without a documented, time-limited exception. First implementation establishes its baseline and must meet changed-code thresholds. |
| Critical rule mutation tests | At least 90% of non-equivalent mutations killed in changed critical pure-domain rules. Review every survivor; exclude equivalent mutations only with a rationale. CI timeout/crash is a failed run, not a killed mutation. |

Exclude generated files and vendored code only with explicit paths and ownership. Do not exclude handwritten adapters, handlers, error branches, migrations, or UI logic. If branch measurement is unsupported by the chosen toolchain, the gate is Pending until an approved alternative measures the relevant decisions; report no invented percentage.

Tests must include the layers the story changes:

- Pure unit/property tests for invariants and boundaries, using injected clock/randomness/IDs for deterministic failures.
- Repository integration tests for real conditional writes, transactions, pagination, ownership filters, migrations, and cache behavior. Mocks alone cannot prove storage/provider semantics.
- API and provider contract tests for success, malformed requests, version drift, authentication, denial, timeout, retry, replay, and ambiguous outcomes. Use sandbox evidence for actual provider behavior before release.
- Client/component and end-to-end tests for affected web/iOS/Android flows, locale/RTL, keyboard or assistive navigation, loading/empty/error/offline states, and reconnect. An API-only story can mark UI testing N/A with a reason.
- Concurrency/fault tests asserting final state and side-effect counts after retries, reordered/duplicated messages, process restart, and dependency failure. A successful HTTP response alone is insufficient.

Fix newly failing or flaky required tests before merge. Quarantining a failing invariant or dropping assertions to raise coverage does not pass G1. Store commands, seed, environment, logs, and coverage reports with the exact source commit.

## G2 — Security audit

Use a pinned [OWASP ASVS](https://asvs.owasp.org/) version and applicable requirement IDs as a review checklist. ASVS provides verifiable security requirements; a scanner alone does not establish conformance.

For every story, document assets, entry points, trust boundaries, actors, abuse cases, and mitigations. Test unauthenticated access, wrong role, same-role different user/vendor/org/tenant, stale/revoked privilege, and forged object identifiers wherever relevant. Derive authority server-side. Check list/count/export endpoints, storage URLs, search facets, caches, sync, background jobs, and AI tools as well as detail endpoints.

Required CI jobs cover secret scanning, SAST, dependency vulnerability/license audit, and an SBOM for changed deployable artifacts. IaC changes also require policy/configuration scans. Runtime/API changes require authenticated dynamic abuse tests in an isolated environment. Uploads need content/size validation and quarantine; configurable outbound URLs need SSRF controls. Web/native credential storage, CSRF where cookies authenticate, CORS, XSS, log redaction, and retention controls must be reviewed when affected.

Zero unresolved **critical or high** findings is a merge/release requirement. Scanner errors, stale/unavailable vulnerability data, missing artifacts, or untriaged results are Pending/Fail, never Pass. Record scanner/tool and advisory database versions, commit, scope, findings, and remediation evidence. False positives require independent justification and a narrow suppression; never suppress a whole class of vulnerabilities.

Medium/low risk acceptance needs reviewer, rationale, compensating control, issue, and expiry. Tenant isolation, credential exposure, unauthorized money movement, and broken signature checks cannot be waived. Production credentials or customer data must not appear in test fixtures or reports.

## G3 — Architecture and maintainability

### Boundaries and useful abstraction

Dependencies flow from UI to hooks/services, from HTTP/event adapters to application use cases, and from infrastructure adapters to domain-owned ports. Domain rules depend on value types and small interfaces, not on Axum, AWS SDKs, database records, Redis, React, or provider DTOs. Composition roots wire implementations. Inspect the actual import/dependency graph; enforce allowed edges and reject cycles in CI.

Prefer one canonical owner for each rule. A port is justified by an external boundary, multiple concrete consumers/providers, or a testable substitution need. Do not create an interface, generic repository, plugin registry, extra crate, or forwarding service merely to satisfy the seven-layer diagram. Record why a new abstraction reduces the cost of a concrete change. Platform-specific presentation may differ while sharing application policy and view models.

| Concern | Canonical responsibility | Reuse requirement |
|:--------|:-------------------------|:------------------|
| Money, rounding, fees, discounts, deposits, allocations | Domain value types and pricing/allocation policies | Checkout, COD, refunds, B2B, ledger, and metering must consume the same policy or shared conformance fixtures across languages. |
| Authentication and authorization | Identity adapter + shared authorization policy | HTTP, MCP, sync, workers, downloads, and admin actions enforce the same ownership rules. |
| Addresses | Address domain/schema and account use cases | US-3.1.4 and US-7.1.2 share validation, persistence, default selection, and hooks; checkout stores an immutable order snapshot. |
| Order, payment, inventory, shipment, refund, payout | Separate explicit state machines and application services | Adapters translate provider events; they do not invent transitions or edit balances directly. |
| Cache identity, ETags, sync | Shared infrastructure policies with typed scoped keys | No independently assembled tenant/user keys or parallel client sources of truth. |
| MCP/WebMCP/Bedrock | One tool contract and application use case per operation | Transports adapt schemas and context; no copied checkout/admin logic. |
| Carrier/payment providers | Small capability ports and adapter contract suites | Retry/timeout mechanisms are shared; provider-specific idempotency/signature rules stay explicit. |
| License formats and SDKs | Versioned protocol, trusted primitives, shared golden vectors | Rust/TypeScript/LAN implementations agree on encodings, keys, time and revocation semantics. |

### Redundancy, readability, and changeability

- Search existing code before adding a helper or rule; document reused components and removed duplication. **No new duplicated domain policy** without an approved design reason. Generated bindings and intentionally independent test oracles are not duplicate business implementations.
- Run a pinned duplication detector on handwritten production code. Changed-code duplication above 3% triggers a failing review item until it is refactored or a narrow justified exception is approved. A lower number does not excuse repeated business rules.
- Run formatting, strict type checks, lint, unused dependency/export checks, and dependency-boundary checks. No new unexplained suppressions, dead code, unused abstractions, catch-all `any`, unchecked panics in request paths, or swallowed errors.
- Cyclomatic complexity above 10, functions above 50 logical lines, or modules above 400 logical lines trigger a recorded decomposition review. These are review triggers, not a reason to fragment cohesive code into meaningless wrappers.
- Use domain names, small explicit inputs/outputs, typed errors, visible side effects, and comments explaining invariants or decisions. A reviewer must be able to trace a request to the owning rule and its persistence effects without following unrelated utility modules.
- Demonstrate one relevant change exercise: add a provider, a fee rule, a locale, or a consumer in the design/test fixture. Show which files change and why. Avoid editing unrelated modules or copying existing implementations. Do not add an unused feature just for this exercise.
- Document public contracts and migration/version compatibility. Build affected consumers and run shared conformance tests after changing reused code. Keep secrets, mutable global state, clocks, and external clients injectable at boundaries.

## G4 — Integrated acceptance and operations

Verify the complete user outcome across the affected APIs, workers, storage, and clients. Include upgrade/rollback with representative data; restart/retry without lost or duplicated effects; tenant-safe logs/metrics/traces; alert delivery and runbook; and backup/restore when persisted data changes. Record numeric RPO/RTO and demonstrate them before the first production release of a stateful feature.

Performance evidence uses the G0 environment and budgets. Shared-resource stories need noisy-neighbor and rate/cost-limit tests. Financial scenarios reconcile expected and recorded amounts after injected failures. A provider timeout with an unknown outcome requires reconciliation rather than a blind second side effect. Releases cannot depend on a later sprint to implement a security or correctness prerequisite.

## Evidence record and exceptions

Copy the [story evidence template](validation/STORY_EVIDENCE_TEMPLATE.md) to a story-specific review artifact or PR body. Attach immutable CI run links/artifacts, commit, reviewer, result, and date for each gate. Allowed results are **Pending**, **Pass**, **Fail**, and **N/A**. A gate can be N/A only for a demonstrably unaffected sub-check, with reviewer and rationale; the overall test, security, and architecture gates always apply.

No critical/high security waiver, isolation waiver, or financial invariant waiver is allowed. Other exceptions require the affected criterion, reason, compensating evidence, owner, independent approval, expiry, and remediation issue. Expired exceptions fail the gate. An exception cannot turn a failing test into a passing test; report the exception separately.

## CI enforcement contract

The implemented `docs-validation` job runs `python3 scripts/validate_docs.py`. It checks documentation structure and cross-references only. It does not run application audits, validate evidence authenticity, or configure GitHub branch protection.

Before merging the first application implementation, add blocking CI checks named `story-tests`, `story-security`, `story-architecture`, and `story-acceptance`, backed by real commands for the affected packages. Configure branch protection/rulesets to require them and independent review. Conditional jobs must explicitly report reviewed N/A sub-checks; missing reports, skipped required tests, or `continue-on-error` cannot produce a successful gate. A final aggregator must fail when any required job fails, is cancelled, or is unexpectedly skipped.

Tools can include Rust coverage/property tests and dependency audits, TypeScript branch coverage and browser/device tests, dependency graph checks, duplication analysis, IaC/security scanners, and mutation tests. Pin tools and lockfiles after compatibility verification; tool selection is not evidence that a check ran. Maintain path-to-story ownership so a shared module change runs all affected story suites. Re-run required checks on the merge candidate when its dependencies change.
