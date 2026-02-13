# Repository Tracking Policy & Folder Structure Cleanup Design

**Date**: 2026-02-13  
**Status**: Design Approved  
**Scope**: Root-level repository tracking policy, `.gitignore` normalization, tracked/untracked boundary cleanup

---

## 1. Problem Statement

Current repository structure mixes deploy/release assets with local-only development artifacts.  
This causes ambiguity in what should remain in remote tracking and what should stay local.

Additional risk: `.gitignore` includes conflicting patterns for `docs/` and `tests/` (`ignore + re-include`), which can make tracking behavior harder to reason about.

---

## 2. Decision Summary

### 2.1 Primary goal (balanced)

Improve readability, deployment clarity, and development hygiene together:
1. Keep only deploy/release essentials tracked remotely
2. Move local operation artifacts to local-only
3. Normalize ignore rules to remove ambiguity

### 2.2 Chosen strategy

Adopt strict deployment-oriented tracking:

**Keep tracked (remote):**
- `aria/**`
- `.claude-plugin/marketplace.json`
- `.github/workflows/version-policy.yml`
- `scripts/versioning/check_version_policy.py`
- `README.md`
- `CHANGELOG.md`
- `aria/CHANGELOG.md`
- `.gitignore`
- `.gitattributes`
- `aria/LICENSE`
- `aria/README.md`
- `aria/CONNECTORS.md`

**Move to local-only (untrack):**
- `docs/**`
- `tests/**`
- `scripts/spec/**`
- `aria.local.md`
- `aria/.mcp.json`

---

## 3. Approaches Considered

### Approach A (selected): Strict deployment-only remote tracking
- Pros: cleanest boundary, minimal noise in remote, simplest long-term policy
- Cons: design/test artifacts are not shared by default

### Approach B: Keep validation/test artifacts in remote
- Pros: easier collaborative auditing
- Cons: weaker separation between deploy assets and local workflow assets

### Approach C: Gradual migration
- Pros: lower immediate change surface
- Cons: prolonged ambiguity and policy drift

Selected: **Approach A**.

---

## 4. Final Design

## 4.1 Section 1: Target remote structure

Remote repository is defined as deployment/release source only.

Everything outside that objective is local-only.

## 4.2 Section 2: Execution flow (adjusted after user feedback)

### Step 0. Normalize ignore rules first

Update `.gitignore` to remove conflicting `docs/tests` exceptions and keep deterministic rules:
- `docs/`
- `tests/`
- `scripts/spec/`
- `aria.local.md`
- `aria/.mcp.json`

Remove any `!docs/**` style re-include overrides that conflict with the new policy.

### Step 1. Dry-run target confirmation

Before untracking, list currently tracked files under:
- `docs/**`
- `tests/**`
- `scripts/spec/**`
- `aria.local.md`
- `aria/.mcp.json`

Use this explicit list as the final removal set.

### Step 2. Untrack from git index only

Apply `git rm --cached` only to the confirmed set.

Note: this removes remote tracking, but keeps local files physically present.

### Step 3. Policy documentation

Add `Repository Tracking Policy` section to `README.md`:
1. What remains tracked (deployment/release essential)
2. What is local-only
3. Rule for future files: track only if required for deployment/release operation

### Step 4. Validation

Run:
1. `git status` to confirm intended changes only
2. `python3 scripts/versioning/check_version_policy.py --base-ref origin/main`
3. `rg` checks to ensure no conflicting re-include rules remain for `docs/tests`

---

## 5. Success Criteria

1. `.gitignore` contains normalized local-only rules with no conflicting `docs/tests` re-includes.
2. `git ls-files` no longer includes files under:
   - `docs/**`
   - `tests/**`
   - `scripts/spec/**`
   - `aria.local.md`
   - `aria/.mcp.json`
3. `git status` shows only intended index removals and policy-doc updates.
4. Version policy check passes:
   - `python3 scripts/versioning/check_version_policy.py --base-ref origin/main`
5. `README.md` clearly documents the remote/local boundary.

---

## 6. Risks & Mitigations

1. **Risk**: accidental over-removal from index  
   **Mitigation**: enforce dry-run confirmation list before `git rm --cached`

2. **Risk**: future accidental re-tracking of local files  
   **Mitigation**: strict `.gitignore` normalization and README policy section

3. **Risk**: contributor confusion after boundary change  
   **Mitigation**: explicit policy wording with examples in README

---

## 7. Non-Goals

1. Reorganizing `aria/` internal command/skill architecture
2. Changing runtime behavior of ARIA commands/skills
3. Modifying CI logic beyond what is required for policy consistency

---

## 8. Approval Record

Approved by user on 2026-02-13 with explicit adjustments:
1. `.gitignore` normalization must precede untracking
2. dry-run tracked list confirmation is mandatory
3. policy documentation in README is required (not optional)
4. `docs/` and `tests/` must be fully local-only

