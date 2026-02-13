# Humanized Writing + Output Contract Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement Gate A (output contract unification) and Gate B (internal humanized writing layer) for ARIA commands/skills while preserving decision safety.

**Architecture:** Gate A establishes a canonical output contract and command-level mapping first. Gate B then introduces an internal-only humanization layer with fact-preservation rules and depth presets (`express/standard/deep`) including optional user override. All changes are validated through lightweight contract tests plus scenario-based golden checks.

**Tech Stack:** Markdown command/skill specs, Python 3 (`unittest`, `re`, `pathlib`) for spec validation scripts, existing ARIA test-scenario markdown convention.

---

## Execution Rules

- Apply `@test-driven-development` for every task (fail -> minimal fix -> pass).
- Apply `@verification-before-completion` before closing each task.
- Keep commits small and focused (one task = one commit).
- Respect gate order: complete all Gate A tasks before Gate B tasks.

---

## Gate A: Output Contract Unification

### Task 1: Create Spec Validator Harness

**Files:**
- Create: `scripts/spec/validate_output_contract_docs.py`
- Create: `tests/test_output_contract_docs.py`

**Step 1: Write the failing test**

```python
# tests/test_output_contract_docs.py
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class OutputContractDocTests(unittest.TestCase):
    def test_validator_script_exists(self):
        validator = ROOT / "scripts/spec/validate_output_contract_docs.py"
        self.assertTrue(validator.exists())


if __name__ == "__main__":
    unittest.main()
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_output_contract_docs.py -v`  
Expected: FAIL because `scripts/spec/validate_output_contract_docs.py` does not exist.

**Step 3: Write minimal implementation**

```python
# scripts/spec/validate_output_contract_docs.py
from pathlib import Path


def command_docs() -> list[Path]:
    root = Path(__file__).resolve().parents[2]
    return sorted((root / "aria" / "commands").glob("*.md"))


if __name__ == "__main__":
    docs = command_docs()
    print(f"Found {len(docs)} command docs.")
```

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_output_contract_docs.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add scripts/spec/validate_output_contract_docs.py tests/test_output_contract_docs.py
git commit -m "test(spec): add output-contract doc validator harness"
```

---

### Task 2: Add Gate A Contract Assertions (Command Layer)

**Files:**
- Modify: `tests/test_output_contract_docs.py`
- Modify: `aria/commands/chat.md`
- Modify: `aria/commands/assess.md`
- Modify: `aria/commands/project.md`
- Modify: `aria/commands/report.md`

**Step 1: Write the failing test**

```python
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
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_output_contract_docs.py -v`  
Expected: FAIL because command docs do not yet contain `## Output Contract`.

**Step 3: Write minimal implementation**

Add `## Output Contract` sections to all 4 command docs with:
- `output_type` mapping per command output
- `language`, `format`, `audience`, `safety_flags`
- `chat`-specific `response_mode` (`skill_invoked | general_qa`)

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_output_contract_docs.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add tests/test_output_contract_docs.py aria/commands/chat.md aria/commands/assess.md aria/commands/project.md aria/commands/report.md
git commit -m "docs(commands): add unified output contract sections"
```

---

### Task 3: Add Gate A Fallback and Safety Assertions

**Files:**
- Modify: `tests/test_output_contract_docs.py`
- Modify: `aria/commands/assess.md`
- Modify: `aria/commands/project.md`
- Modify: `aria/commands/report.md`

**Step 1: Write the failing test**

```python
def test_export_commands_define_format_fallback(self):
    for name in ["assess.md", "project.md", "report.md"]:
        text = (ROOT / "aria/commands" / name).read_text(encoding="utf-8")
        self.assertIn("graceful fallback", text.lower(), name)
        self.assertIn("markdown", text.lower(), name)


def test_all_commands_preserve_regulatory_facts_flag(self):
    for name in ["chat.md", "assess.md", "project.md", "report.md"]:
        text = (ROOT / "aria/commands" / name).read_text(encoding="utf-8")
        self.assertIn("preserve_regulatory_facts", text, name)
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_output_contract_docs.py -v`  
Expected: FAIL for one or more command docs.

**Step 3: Write minimal implementation**

Add explicit fallback and safety-flag wording in command docs:
- connector unavailable -> fallback to markdown
- include contract safety flags (`preserve_regulatory_facts`, `preserve_numeric_values`, `preserve_disclaimer_strength`)

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_output_contract_docs.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add tests/test_output_contract_docs.py aria/commands/assess.md aria/commands/project.md aria/commands/report.md aria/commands/chat.md
git commit -m "docs(commands): define fallback and safety flags in output contract"
```

---

## Gate B: Humanized Writing Layer

### Task 4: Create Internal Humanized Writing Skill Spec

**Files:**
- Create: `aria/skills/humanized-writing/SKILL.md`
- Modify: `tests/test_output_contract_docs.py`

**Step 1: Write the failing test**

```python
def test_humanized_writing_skill_is_internal_only(self):
    path = ROOT / "aria/skills/humanized-writing/SKILL.md"
    text = path.read_text(encoding="utf-8")
    self.assertIn("name: aria-humanized-writing", text)
    self.assertIn("user-invocable: false", text)
    self.assertIn("preserve_regulatory_facts", text)
    self.assertIn("preserve_numeric_values", text)
    self.assertIn("preserve_disclaimer_strength", text)
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_output_contract_docs.py -v`  
Expected: FAIL because skill file does not exist yet.

**Step 3: Write minimal implementation**

Create `aria/skills/humanized-writing/SKILL.md` including:
- metadata and internal-only declaration
- purpose and scope
- hard-fact invariants
- insufficiency behavior (ask 1-3 minimum questions)
- depth presets (`express|standard|deep`)

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_output_contract_docs.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add aria/skills/humanized-writing/SKILL.md tests/test_output_contract_docs.py
git commit -m "feat(skill): add internal aria-humanized-writing specification"
```

---

### Task 5: Add Depth Override and Insufficiency Rules to Commands

**Files:**
- Modify: `tests/test_output_contract_docs.py`
- Modify: `aria/commands/chat.md`
- Modify: `aria/commands/assess.md`
- Modify: `aria/commands/project.md`
- Modify: `aria/commands/report.md`

**Step 1: Write the failing test**

```python
def test_commands_declare_depth_support(self):
    for name in ["chat.md", "assess.md", "project.md", "report.md"]:
        text = (ROOT / "aria/commands" / name).read_text(encoding="utf-8")
        self.assertIn("--depth", text, name)
        self.assertRegex(text, r"express\|standard\|deep")


def test_chat_has_insufficient_info_short_mode(self):
    text = (ROOT / "aria/commands/chat.md").read_text(encoding="utf-8").lower()
    self.assertIn("insufficient", text)
    self.assertIn("1-3", text)
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_output_contract_docs.py -v`  
Expected: FAIL until command docs include `--depth` and insufficiency handling rules.

**Step 3: Write minimal implementation**

Update command docs with:
- optional `--depth express|standard|deep`
- default depth behavior by output type
- insufficient info behavior: concise rationale + 1-3 required questions

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_output_contract_docs.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add tests/test_output_contract_docs.py aria/commands/chat.md aria/commands/assess.md aria/commands/project.md aria/commands/report.md
git commit -m "docs(commands): add depth presets and insufficient-info handling"
```

---

### Task 6: Golden Scenario Pack for Readability + Fact Preservation

**Files:**
- Create: `tests/SPEC-ARIA-005-chat-test-scenarios.md`
- Create: `tests/SPEC-ARIA-005-assess-test-scenarios.md`
- Create: `tests/SPEC-ARIA-005-project-test-scenarios.md`
- Create: `tests/SPEC-ARIA-005-report-test-scenarios.md`
- Modify: `tests/test_output_contract_docs.py`

**Step 1: Write the failing test**

```python
def test_spec_aria_005_scenario_files_exist(self):
    required = [
        ROOT / "tests/SPEC-ARIA-005-chat-test-scenarios.md",
        ROOT / "tests/SPEC-ARIA-005-assess-test-scenarios.md",
        ROOT / "tests/SPEC-ARIA-005-project-test-scenarios.md",
        ROOT / "tests/SPEC-ARIA-005-report-test-scenarios.md",
    ]
    for path in required:
        self.assertTrue(path.exists(), path.name)
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_output_contract_docs.py -v`  
Expected: FAIL because scenario files do not exist.

**Step 3: Write minimal implementation**

Create scenario docs covering:
- insufficient info turn (`express`) behavior
- summary brevity with preserved facts
- full report deep narrative without semantic drift
- override behavior (`--depth`) and expected differences

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_output_contract_docs.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add tests/SPEC-ARIA-005-*-test-scenarios.md tests/test_output_contract_docs.py
git commit -m "test(spec): add SPEC-ARIA-005 golden scenario pack"
```

---

## Final Verification

### Step 1: Run full spec tests

Run: `python3 -m unittest tests/test_output_contract_docs.py -v`  
Expected: PASS.

### Step 2: Verify no unintended file changes

Run: `git status --short`  
Expected: only intentional files changed.

### Step 3: Version policy check (if plugin/commands/skills changed)

Run: `python3 scripts/versioning/check_version_policy.py --base-ref origin/main`  
Expected: PASS, or explicit actionable failures for required patch bumps.

### Step 4: Final commit (if any remaining staged changes)

```bash
git add <remaining-files>
git commit -m "chore: finalize SPEC-ARIA-005 implementation"
```

---

## Notes for Executor

1. Do not start Gate B before Gate A acceptance tests pass.
2. Preserve ARIA core flow in all docs: information sufficiency -> analysis -> next-action question.
3. If any command-level wording conflicts with safety invariants, prioritize invariants and update tests.

