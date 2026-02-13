import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class OutputContractDocTests(unittest.TestCase):
    def test_validator_script_exists(self):
        validator = ROOT / "scripts/spec/validate_output_contract_docs.py"
        self.assertTrue(validator.exists())


if __name__ == "__main__":
    unittest.main()
