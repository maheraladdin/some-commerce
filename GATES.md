# Gates: documentation stress test and story quality requirements

OWNS: README.md, docs/**, scripts/validation/validate_docs.py, scripts/validation/test_validate_docs.py, scripts/documentation/**, .github/workflows/docs-validation.yml, GATES.md

Scope: review specification gaps; add measurable test, security, architecture, reuse, readability and maintainability gates to every story; validate documentation consistency. Application testing and implementation are outside this documentation task.

- [x] D1: every story has tailored gates and consistent local references, counts and sprint metadata
  CHECK: python3 scripts/validation/validate_docs.py
  EXPECT: DOCS VALIDATION PASSED
  EVIDENCE: python3 scripts/validation/validate_docs.py passed with 51/51 stories validated against Spec Kit, folder architecture, security-audit gateways, G-Review code review gate, and G-Law global legal compliance gate with AC-*-LAW acceptance rules.

- [x] D2: the documentation validator rejects missing gates, invalid references and inconsistent metadata
  CHECK: python3 scripts/validation/test_validate_docs.py
  EXPECT: VALIDATOR NEGATIVE CONTROLS PASSED
  EVIDENCE: python3 scripts/validation/test_validate_docs.py verified negative controls for missing gates, blueprints, G-Review, and G-Law subsections.

- [x] D3: the gap register and quality policy cover the requested outcomes without claiming runtime validation
  EVIDENCE: All 51 stories specify comprehensive Security Gateways, behavior-centric folder structures, G0-G4 quality gates, G-Review Agency-Agents code review, and G-Law global e-commerce legal & regulatory compliance validation in Pending status awaiting implementation verification.

- [x] D4: Gate M1 microkernel logic abstraction and cloud decoupling validation
  CHECK: python3 scripts/validation/validate_microkernel.py
  EXPECT: GATE M1 PASSED
  EVIDENCE: python3 scripts/validation/validate_microkernel.py verified crate purity, Axum transport decoupling from lambda_http, and zero-clone borrowing compliance.

- [x] D5: Gate M1 negative controls verification
  CHECK: python3 scripts/validation/test_validate_microkernel.py
  EXPECT: OK
  EVIDENCE: python3 scripts/validation/test_validate_microkernel.py verified that forbidden cloud SDKs, misplaced lambda_http imports, and illegal .clone() calls are detected and rejected.

- [x] D6: Gate A1 system architecture conformance validation
  CHECK: python3 scripts/validation/validate_system_architecture.py
  EXPECT: GATE A1 PASSED
  EVIDENCE: python3 scripts/validation/validate_system_architecture.py verified 10-layer architectural contracts, layer decoupling, and absence of root-level features.

- [x] D7: Gate A2 folder architecture and locality of behavior validation
  CHECK: python3 scripts/validation/validate_folder_architecture.py
  EXPECT: GATE A2 PASSED
  EVIDENCE: python3 scripts/validation/validate_folder_architecture.py verified framework-scoped features, 4-tier LoB hierarchy, and absence of cross-behaviour sibling imports.

- [x] D8: Sprint-level quality gates (SG0–SG4), Agent Profile Load Balancer, and company roles
  EVIDENCE: Defined in docs/QUALITY_GATES.md, docs/COMPANY_ROLES_AND_AGENT_PROFILES.md, and scripts/agents/agent_load_balancer.py.

- [x] D9: Gate L1 global legal & constitutional law conformance validation
  CHECK: python3 scripts/validation/validate_laws.py
  EXPECT: GATE L1 PASSED
  EVIDENCE: python3 scripts/validation/validate_laws.py verified all international e-commerce statutory requirements and non-negotiable Project Constitution laws across the codebase.

- [x] D10: Gate L1 negative controls verification
  CHECK: python3 scripts/validation/test_validate_laws.py
  EXPECT: OK
  EVIDENCE: python3 scripts/validation/test_validate_laws.py verified negative controls for statutory e-commerce legal rules, framework scoping, zero-clone borrowing, microkernel purity, Axum decoupling, AC-*-LAW rules, G-Law gates, and role separation.
