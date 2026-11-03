#!/usr/bin/env python3
"""
Tests negative controls for validate_docs.py to ensure it properly catches missing sections,
invalid story titles, missing security gateways, or missing folder architecture references.
"""

import unittest
import sys
from unittest.mock import patch, mock_open
import validate_docs

class TestValidateDocsNegativeControls(unittest.TestCase):

    def test_missing_security_gateway(self):
        sample_invalid_content = """# US-1.1.1: Phone OTP Passwordless Sign-In
## 1. Spec Kit Specification
### 1.1 User Story Narrative
### 1.2 Acceptance Criteria (Gherkin Scenarios)
[AC-US-1.1.1-01]
### 1.3 Test Cases & Traceability Matrix
## 2. Behavior-Centric Architecture & Folder Blueprint
### 2.1 Colocated Behaviour Directory Tree
features/identity/modules/auth/behaviours/phone-otp
### 2.2 Scoping & Promotion Blueprint
## 3. Technical Implementation Plan
### 3.1 Domain Invariants & Storage Schema
### 3.2 Activity & Interaction Diagram
## 4. Granular Implementation Tasks
## 6. Validation Gates & Acceptance Sign-Off
### G1 — Test coverage
### G2 — Security audit
### G3 — Architecture and maintainability
### G4 — Integrated acceptance
"""
        with patch("os.walk") as mock_walk, \
             patch("builtins.open", mock_open(read_data=sample_invalid_content)), \
             patch("os.path.exists", return_value=True):
            mock_walk.return_value = [
                ("docs/user-stories/01-auth-and-onboarding", [], ["us-1.1.1-sample.md"])
            ]
            count, errors = validate_docs.validate_all_stories()
            self.assertTrue(any("Missing section '## 5. Security Gateway" in e for e in errors))

    def test_missing_behavior_blueprint(self):
        sample_invalid_content = """# US-1.1.1: Phone OTP Passwordless Sign-In
## 1. Spec Kit Specification
### 1.1 User Story Narrative
### 1.2 Acceptance Criteria (Gherkin Scenarios)
[AC-US-1.1.1-01]
### 1.3 Test Cases & Traceability Matrix
## 2. Behavior-Centric Architecture & Folder Blueprint
### 2.1 Colocated Behaviour Directory Tree
### 2.2 Scoping & Promotion Blueprint
## 3. Technical Implementation Plan
### 3.1 Domain Invariants & Storage Schema
### 3.2 Activity & Interaction Diagram
## 4. Granular Implementation Tasks
## 5. Security Gateway (Powered by security-audit)
### 5.1 Trust Boundaries & Security Actors
### 5.2 Threat Modeling & Abuse Matrix
Spoofing & Impersonation
### 5.3 Cryptographic & Data Protection Controls
### 5.4 Automated Security Verification Checklist
### 5.5 Security Gateway (G2) Sign-Off Checklist
## 6. Validation Gates & Acceptance Sign-Off
### G1 — Test coverage
### G2 — Security audit
### G3 — Architecture and maintainability
### G4 — Integrated acceptance
"""
        with patch("os.walk") as mock_walk, \
             patch("builtins.open", mock_open(read_data=sample_invalid_content)), \
             patch("os.path.exists", return_value=True):
            mock_walk.return_value = [
                ("docs/user-stories/01-auth-and-onboarding", [], ["us-1.1.1-sample.md"])
            ]
            count, errors = validate_docs.validate_all_stories()
            self.assertTrue(any("Missing behaviour folder blueprint path" in e for e in errors))

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestValidateDocsNegativeControls)
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    if result.wasSuccessful():
        print("VALIDATOR NEGATIVE CONTROLS PASSED")
        sys.exit(0)
    else:
        sys.exit(1)
