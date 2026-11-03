
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import unittest
from scripts.documentation.sprint_closeout import TARGETS, HEADING, append_closeout, render, validate_sprint, check_all


class SprintCloseoutTests(unittest.TestCase):
    def test_all_twelve_real_sprints_have_final_tailored_gates(self):
        self.assertEqual(len(TARGETS), 12)
        self.assertEqual(check_all(), [])

    def test_missing_each_test_category_is_rejected(self):
        for number, label in enumerate(('Benchmark tests', 'Integration tests', 'Fuzz tests', 'Loom concurrency tests'), 1):
            with self.subTest(label=label):
                text = render('sprint-1.1').replace(f'**E{number} — {label}:**', '**Removed:**')
                self.assertTrue(any(f'missing E{number}' in e for e in validate_sprint(text, 'sprint-1.1')))

    def test_empty_wrong_scope_and_missing_gate_are_rejected(self):
        self.assertTrue(validate_sprint('', 'sprint-1.1'))
        self.assertTrue(validate_sprint(render('sprint-1.2'), 'sprint-1.1'))
        self.assertTrue(validate_sprint(render('sprint-1.1') + '\n## Later section\n', 'sprint-1.1'))

    def test_refresh_preserves_authored_prefix_and_is_idempotent(self):
        prefix = '# Sprint\n\nAuthored acceptance requirement.\n'
        first = append_closeout(prefix, 'sprint-6.3')
        self.assertTrue(first.startswith(prefix))
        self.assertEqual(append_closeout(first, 'sprint-6.3'), first)
        self.assertEqual(first.count(HEADING), 1)

    def test_sprint_plan_regeneration_restores_the_closeout_gate(self):
        from scripts.documentation import update_sprint_plans as updater
        plan = updater.build_sprint_agent_plan_markdown('sprint-6.3')
        final = updater.append_closeout('# Sprint\n' + plan, 'sprint-6.3')
        self.assertEqual(validate_sprint(final, 'sprint-6.3'), [])


    def test_full_regeneration_is_idempotent_and_preserves_authored_scope(self):
        from scripts.documentation.update_sprint_plans import compose_sprint_plan
        prefix = "# Sprint\n\n## Goal\nKeep this authored acceptance scope.\n"
        plan = "---\n\n## Multi-Agent Sprint Implementation Plan\nGenerated allocations.\n"
        once = compose_sprint_plan(prefix, 'sprint-1.1', plan)
        twice = compose_sprint_plan(once, 'sprint-1.1', plan)
        self.assertEqual(once, twice)
        self.assertIn('Keep this authored acceptance scope.', twice)
        self.assertEqual(twice.count(HEADING), 1)
        self.assertEqual(validate_sprint(twice, 'sprint-1.1'), [])

    def test_generated_sprint_plan_carries_both_directions_and_single_record_contract(self):
        from scripts.documentation.update_sprint_plans import build_sprint_agent_plan_markdown
        for sprint_id in ('sprint-1.1', 'sprint-6.3'):
            with self.subTest(sprint=sprint_id):
                plan = build_sprint_agent_plan_markdown(sprint_id)
                self.assertLess(plan.index('| P0 |'), plan.index('| EXECUTE |'))
                self.assertLess(plan.index('| COLLECT |'), plan.index('| VALIDATE |'))
                self.assertLess(plan.index('| VALIDATE |'), plan.index('| RETURN |'))
                self.assertIn('canonical `docs/validation/story-records/US-<id>.md`', plan)
                self.assertIn('not dispatch authorization', plan)

if __name__ == '__main__':
    unittest.main()
