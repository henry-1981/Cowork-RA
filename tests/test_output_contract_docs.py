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


if __name__ == "__main__":
    unittest.main()
