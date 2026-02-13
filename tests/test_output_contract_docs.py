import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class OutputContractDocTests(unittest.TestCase):
    def test_validator_script_exists(self):
        validator = ROOT / "scripts/spec/validate_output_contract_docs.py"
        self.assertTrue(validator.exists())

    def test_commands_define_output_contract_section(self):
        required = [
            ROOT / "aria/commands/chat.md",
            ROOT / "aria/commands/assess.md",
            ROOT / "aria/commands/project.md",
            ROOT / "aria/commands/report.md",
        ]
        for path in required:
            text = path.read_text(encoding="utf-8")
            self.assertIn("## Output Contract", text, f"Missing in {path.name}")

    def test_chat_declares_response_modes(self):
        text = (ROOT / "aria/commands/chat.md").read_text(encoding="utf-8")
        self.assertIn("response_mode", text)
        self.assertIn("skill_invoked", text)
        self.assertIn("general_qa", text)

    def test_export_commands_define_format_fallback(self):
        for name in ["assess.md", "project.md", "report.md"]:
            text = (ROOT / "aria/commands" / name).read_text(encoding="utf-8")
            self.assertIn("graceful fallback", text.lower(), name)
            self.assertIn("markdown", text.lower(), name)

    def test_all_commands_preserve_regulatory_facts_flag(self):
        for name in ["chat.md", "assess.md", "project.md", "report.md"]:
            text = (ROOT / "aria/commands" / name).read_text(encoding="utf-8")
            self.assertIn("preserve_regulatory_facts", text, name)

    def test_humanized_writing_skill_is_internal_only(self):
        path = ROOT / "aria/skills/humanized-writing/SKILL.md"
        text = path.read_text(encoding="utf-8")
        self.assertIn("name: aria-humanized-writing", text)
        self.assertIn("user-invocable: false", text)
        self.assertIn("preserve_regulatory_facts", text)
        self.assertIn("preserve_numeric_values", text)
        self.assertIn("preserve_disclaimer_strength", text)


if __name__ == "__main__":
    unittest.main()
