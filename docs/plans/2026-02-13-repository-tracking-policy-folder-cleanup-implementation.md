# Repository Tracking Policy Cleanup Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Convert `docs/`, `tests/`, and other agreed local artifacts to local-only while keeping deploy/release assets tracked and policy-documented.

**Architecture:** First normalize `.gitignore` so behavior is deterministic. Then run a dry-run tracked-file listing and remove only the approved paths from git index using `git rm --cached` (local files remain). Finally, document the tracking boundary in `README.md` and run verification (`git status`, tracked-file checks, version-policy check).

**Tech Stack:** Git index operations (`git ls-files`, `git rm --cached`), ignore-rule validation (`rg`, `git check-ignore`), Markdown docs (`README.md`), Python policy checker (`scripts/versioning/check_version_policy.py`).

---

### Task 1: Normalize `.gitignore` Rules

**Files:**
- Modify: `.gitignore`
- Test: Shell checks in terminal (no new test file)

**Step 1: Write the failing test**

Run these checks first:

```bash
rg -n '^!docs/' .gitignore
```

```bash
rg -n '^docs/$|^tests/$|^scripts/spec/$|^aria.local.md$|^aria/.mcp.json$' .gitignore
```

**Step 2: Run test to verify it fails**

Expected before edit:
- First command returns one or more `!docs/...` exception lines (failure against new policy).
- Second command may miss one or more required local-only patterns.

**Step 3: Write minimal implementation**

Edit `.gitignore` so it deterministically enforces:

```gitignore
docs/
tests/
scripts/spec/
aria.local.md
aria/.mcp.json
```

Remove conflicting re-include patterns for docs (for example `!docs/`, `!docs/development/`, `!docs/development/**`).

**Step 4: Run test to verify it passes**

Run:

```bash
rg -n '^!docs/' .gitignore
```

Expected: no output.

Run:

```bash
rg -n '^docs/$|^tests/$|^scripts/spec/$|^aria.local.md$|^aria/.mcp.json$' .gitignore
```

Expected: all five patterns present.

**Step 5: Commit**

```bash
git add .gitignore
git commit -m "chore(gitignore): normalize local-only tracking rules"
```

---

### Task 2: Dry-Run and Untrack Approved Local-Only Paths

**Files:**
- Untrack (index only): `docs/**`
- Untrack (index only): `tests/**`
- Untrack (index only): `scripts/spec/**`
- Untrack (index only): `aria.local.md`
- Untrack (index only): `aria/.mcp.json`
- Test: Shell checks in terminal

**Step 1: Write the failing test**

Run:

```bash
git ls-files 'docs/**' 'tests/**' 'scripts/spec/**' 'aria.local.md' 'aria/.mcp.json'
```

**Step 2: Run test to verify it fails**

Expected before untracking: command prints tracked files (non-empty output), which fails the target condition (must be empty).

**Step 3: Write minimal implementation**

1. Save explicit dry-run list:

```bash
git ls-files 'docs/**' 'tests/**' 'scripts/spec/**' 'aria.local.md' 'aria/.mcp.json' > /tmp/local-only-tracked-files.txt
cat /tmp/local-only-tracked-files.txt
```

2. Untrack only files from that list:

```bash
xargs -I{} git rm --cached "{}" < /tmp/local-only-tracked-files.txt
```

**Step 4: Run test to verify it passes**

Run:

```bash
git ls-files 'docs/**' 'tests/**' 'scripts/spec/**' 'aria.local.md' 'aria/.mcp.json'
```

Expected: no output.

Also verify local files still exist:

```bash
test -f README.md && test -d docs && test -d tests && echo "local files preserved"
```

Expected: `local files preserved`.

**Step 5: Commit**

```bash
git add -u
git commit -m "chore(repo): untrack local-only docs tests and spec artifacts"
```

---

### Task 3: Document Repository Tracking Policy in README

**Files:**
- Modify: `README.md`
- Test: Shell checks in terminal

**Step 1: Write the failing test**

Run:

```bash
rg -n '^## Repository Tracking Policy' README.md
```

**Step 2: Run test to verify it fails**

Expected before edit: no match.

**Step 3: Write minimal implementation**

Add `## Repository Tracking Policy` section to `README.md` with:
1. Remote tracked scope (deploy/release essentials)
2. Local-only scope (`docs/`, `tests/`, `scripts/spec/`, `aria.local.md`, `aria/.mcp.json`, etc.)
3. Rule for new files: track only if required for deployment/release operation

**Step 4: Run test to verify it passes**

Run:

```bash
rg -n '^## Repository Tracking Policy|docs/|tests/|scripts/spec/' README.md
```

Expected: section header and policy bullets are found.

**Step 5: Commit**

```bash
git add README.md
git commit -m "docs(readme): add repository tracking policy section"
```

---

### Task 4: Final Verification and Version Policy Compliance

**Files:**
- Possibly modify: `aria/.claude-plugin/plugin.json`
- Possibly modify: `.claude-plugin/marketplace.json`
- Test: policy and status verification commands

**Step 1: Write the failing test**

Run:

```bash
python3 scripts/versioning/check_version_policy.py --base-ref origin/main
```

**Step 2: Run test to verify it fails (if needed)**

If output reports plugin patch not increased, treat as expected failure for this task.
If it already passes, skip directly to Step 4.

**Step 3: Write minimal implementation (only if Step 2 failed)**

Bump plugin patch versions in both files to the next patch:
- `aria/.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`

**Step 4: Run test to verify it passes**

Run all checks:

```bash
python3 scripts/versioning/check_version_policy.py --base-ref origin/main
```

```bash
git ls-files 'docs/**' 'tests/**' 'scripts/spec/**' 'aria.local.md' 'aria/.mcp.json'
```

```bash
git status -sb
```

Expected:
- version policy passes
- local-only paths are not tracked
- status shows only intended branch delta

**Step 5: Commit (if Step 3 changed files)**

```bash
git add aria/.claude-plugin/plugin.json .claude-plugin/marketplace.json
git commit -m "chore(versioning): bump plugin patch for tracking-policy cleanup"
```

---

## Notes for Executor

1. Do not run `git rm` without `--cached` for this migration.
2. Use the dry-run list as the only source of truth for untracking.
3. Keep implementation minimal: no new architecture changes inside `aria/`.
4. Apply `@test-driven-development` and `@verification-before-completion` in every task.

