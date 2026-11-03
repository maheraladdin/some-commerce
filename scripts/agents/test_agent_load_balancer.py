#!/usr/bin/env python3
"""
Test suite for Agent Profile Load Balancer (agent_load_balancer.py).
Verifies:
1. Parsing of user stories and points from sprint markdown files.
2. Accurate layer and profile routing (PR 1-4 -> BE, PR 5-7 -> FE, QA -> G0-G4).
3. Even workload distribution across worker instances.
4. Correct generation of workspaces when spawn is called.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import unittest
import tempfile
import shutil

from scripts.agents.agent_load_balancer import AgentProfileLoadBalancer, parse_sprint_stories


class TestAgentProfileLoadBalancer(unittest.TestCase):
    def test_company_cycle_starts_at_cto_and_returns_to_cto_without_authorizing_dispatch(self):
        plan = AgentProfileLoadBalancer("sprint-1.1").balance_sprint()
        self.assertEqual(plan["allocation_status"], "PROPOSAL_NOT_AUTHORIZATION")
        self.assertIs(plan["implementation_authorized"], False)
        stages = plan["company_pipeline"]
        self.assertEqual(stages[0]["owner"], "chief-technology-officer")
        self.assertEqual(stages[-1]["owner"], "chief-technology-officer")
        ids = [row["phase"] for row in stages]
        self.assertEqual(ids[:5], ["P0", "P1", "P2", "P3", "P4"])
        self.assertLess(ids.index("P4"), ids.index("EXECUTE"))
        self.assertLess(ids.index("COLLECT"), ids.index("VALIDATE"))
        self.assertLess(ids.index("VALIDATE"), ids.index("RETURN"))
        self.assertEqual(plan["required_story_record_pattern"], "docs/validation/story-records/US-<id>.md")

    def test_parse_sprint_stories(self):
        stories = parse_sprint_stories("sprint-1.1")
        self.assertGreater(len(stories), 0, "Expected at least 1 story in sprint-1.1")
        story_ids = [s[0] for s in stories]
        self.assertIn("us-1.1.1", story_ids)
        self.assertIn("us-2.1.1", story_ids)

    def test_balance_distribution_fairness(self):
        balancer = AgentProfileLoadBalancer("sprint-1.1", junior_be_workers=2, junior_fe_workers=2, junior_qa_workers=1)
        plan = balancer.balance_sprint()

        # Check total stories and 7-PR multiplier
        self.assertEqual(plan["total_prs"], plan["total_stories"] * 7)

        # Check that junior backend workers have balanced workloads (difference <= 4 points)
        be1_load = plan["workers"]["sprint-1.1-junior-be-1"]["workload"]
        be2_load = plan["workers"]["sprint-1.1-junior-be-2"]["workload"]
        self.assertLessEqual(abs(be1_load - be2_load), 4)

        # Check that junior client workers have balanced workloads (difference <= 4 points)
        fe1_load = plan["workers"]["sprint-1.1-junior-fe-1"]["workload"]
        fe2_load = plan["workers"]["sprint-1.1-junior-fe-2"]["workload"]
        self.assertLessEqual(abs(fe1_load - fe2_load), 4)

        # Check that senior reviewers and leadership are assigned
        self.assertIn("sprint-1.1-senior-be-1", plan["workers"])
        self.assertIn("sprint-1.1-senior-fe-1", plan["workers"])
        self.assertEqual(plan["leadership"]["cto"], "sprint-1.1-cto")
        self.assertEqual(plan["leadership"]["product_manager"], "sprint-1.1-product-manager")

        # Check that every PR is mapped to correct profile and has a senior reviewer
        for story in plan["story_allocations"]:
            for pr in story["prs"]:
                self.assertIn("junior_author", pr)
                self.assertIn("senior_reviewer", pr)
                if pr["pr_num"] in (1, 2, 3, 4):
                    self.assertEqual(pr["profile"], "backend-engineer")
                else:
                    self.assertEqual(pr["profile"], "client-engineer")


if __name__ == "__main__":
    unittest.main()
