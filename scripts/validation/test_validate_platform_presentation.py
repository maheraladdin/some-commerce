#!/usr/bin/env python3
"""
Unit tests and negative controls for validate_platform_presentation.py (Gate F1 / G-UI).
Verifies that:
- Custom hooks in designs/ are caught.
- Direct mutations/queries in designs/ are caught.
- JSX markup in logic/ is caught.
- Raw web DOM elements in mobile components are caught.
- Missing Tailwind classes in web components are caught.
- Missing {story_id}-G-UI in user stories is caught.
- Valid mobile (@expo/ui) and web (HTML + Tailwind) structures pass.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import tempfile
import unittest
from scripts.validation import validate_platform_presentation


class TestValidatePlatformPresentation(unittest.TestCase):

    def test_custom_hook_in_designs_caught(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            designs_dir = tmp_path / "designs"
            designs_dir.mkdir(parents=True)
            bad_design = designs_dir / "Button.tsx"
            bad_design.write_text(
                "import React from 'react';\n"
                "export function useButtonState() {\n"
                "    return { count: 0 };\n"
                "}\n"
                "export const Button = () => null;\n",
                encoding="utf-8"
            )
            errors = validate_platform_presentation.validate_designs_directory(designs_dir)
            self.assertEqual(len(errors), 1)
            self.assertIn("Gate F1 Violation", errors[0])
            self.assertIn("Custom hook 'useButtonState' defined inside 'designs/'", errors[0])

    def test_query_mutation_in_designs_caught(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            designs_dir = tmp_path / "designs"
            designs_dir.mkdir(parents=True)
            bad_design = designs_dir / "Card.tsx"
            bad_design.write_text(
                "import React from 'react';\n"
                "export const Card = () => {\n"
                "    const { data } = useQuery('items', fetchItems);\n"
                "    return null;\n"
                "};\n",
                encoding="utf-8"
            )
            errors = validate_platform_presentation.validate_designs_directory(designs_dir)
            self.assertEqual(len(errors), 1)
            self.assertIn("Direct query/mutation 'useQuery' called inside 'designs/'", errors[0])

    def test_jsx_in_logic_caught(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            logic_dir = tmp_path / "logic"
            logic_dir.mkdir(parents=True)
            bad_logic = logic_dir / "useAuth.ts"
            bad_logic.write_text(
                "import React from 'react';\n"
                "export function useAuth() {\n"
                "    const errorView = <div>Error</div>;\n"
                "    return { errorView };\n"
                "}\n",
                encoding="utf-8"
            )
            errors = validate_platform_presentation.validate_logic_directory(logic_dir)
            self.assertEqual(len(errors), 1)
            self.assertIn("JSX presentation markup found inside 'logic/'", errors[0])

    def test_web_dom_in_mobile_component_caught(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            mobile_file = tmp_path / "Card.native.tsx"
            mobile_file.write_text(
                "import React from 'react';\n"
                "export const Card = () => (\n"
                "    <div>\n"
                "        <span>Native Title</span>\n"
                "    </div>\n"
                ");\n",
                encoding="utf-8"
            )
            errors = validate_platform_presentation.validate_mobile_component_presentation(mobile_file)
            self.assertEqual(len(errors), 1)
            self.assertIn("Forbidden web DOM element '<div>' found in mobile component", errors[0])

    def test_missing_tailwind_in_web_component_caught(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            web_file = tmp_path / "Header.web.tsx"
            web_file.write_text(
                "import React from 'react';\n"
                "export const Header = () => (\n"
                "    <header>\n"
                "        <h1>Some Commerce</h1>\n"
                "    </header>\n"
                ");\n",
                encoding="utf-8"
            )
            errors = validate_platform_presentation.validate_web_component_presentation(web_file)
            self.assertEqual(len(errors), 1)
            self.assertIn("Web component missing Tailwind CSS 'className' styling", errors[0])

    def test_valid_web_and_mobile_components_pass(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            mobile_file = tmp_path / "Banner.native.tsx"
            mobile_file.write_text(
                "import React from 'react';\n"
                "import { View, Text } from '@expo/ui/components';\n"
                "export const Banner = ({ title }: { title: string }) => (\n"
                "    <View>\n"
                "        <Text>{title}</Text>\n"
                "    </View>\n"
                ");\n",
                encoding="utf-8"
            )
            web_file = tmp_path / "Banner.web.tsx"
            web_file.write_text(
                "import React from 'react';\n"
                "export const Banner = ({ title }: { title: string }) => (\n"
                "    <section className=\"p-4 bg-white rounded-lg shadow-sm\">\n"
                "        <h2 className=\"text-lg font-bold text-gray-900\">{title}</h2>\n"
                "    </section>\n"
                ");\n",
                encoding="utf-8"
            )
            self.assertEqual(len(validate_platform_presentation.validate_mobile_component_presentation(mobile_file)), 0)
            self.assertEqual(len(validate_platform_presentation.validate_web_component_presentation(web_file)), 0)

    def test_missing_story_g_ui_gate_caught(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            story_file = tmp_path / "us-1.1.1-auth.md"
            story_file.write_text(
                "# US-1.1.1: Customer Authentication\n"
                "### 6. Validation Gates & Acceptance Sign-Off\n"
                "- [ ] **US-1.1.1-G-Review:** pass\n",
                encoding="utf-8"
            )
            errors = validate_platform_presentation.validate_stories_ui_gate(tmp_path)
            self.assertTrue(any("Missing UI/UX validation gate 'US-1.1.1-G-UI'" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
