# ARIA Versioning Policy

This document defines separated version domains and enforcement rules for ARIA.

## 1. Version Domains

### 1.1 Plugin version (ARIA release)

- Source of truth: `aria/.claude-plugin/plugin.json` -> `version`
- Must be synchronized with marketplace entry:
  - `.claude-plugin/marketplace.json` -> `plugins[name=aria].version`

### 1.2 Command versions (independent from plugin version)

- Source of truth: `aria/commands/versions.json`
- Managed per command:
  - `chat`
  - `assess`
  - `project`
  - `report`

### 1.3 Skill versions (independent from plugin version)

- Source of truth: each `aria/skills/*/SKILL.md` -> frontmatter `metadata.version`

## 2. SemVer Rules

All domains use `MAJOR.MINOR.PATCH`.

- `MAJOR` and `MINOR`:
  - MUST NOT change during normal development.
  - May change only with explicit user request.
- `PATCH`:
  - Normal updates use patch increments only.

## 3. Update Rules

### 3.1 Plugin patch rule

- When any commit/PR change exists in the repo, plugin `PATCH` must increase.
- `plugin.json` and `marketplace.json` plugin version must always match.

### 3.2 Command patch rule

- If a command file changes (`aria/commands/<name>.md`), that command's patch in `aria/commands/versions.json` must increase.
- If a command file does not change, its version must not change.

### 3.3 Skill patch rule

- If a skill changes (`aria/skills/<skill>/**`), that skill's `metadata.version` patch must increase.
- If a skill does not change, its version must not change.

## 4. Validation

- Validation script: `scripts/versioning/check_version_policy.py`
- CI workflow: `.github/workflows/version-policy.yml`

Local example:

```bash
python3 scripts/versioning/check_version_policy.py --base-ref origin/main
```

Optional explicit major/minor override (manual use only):

```bash
python3 scripts/versioning/check_version_policy.py --base-ref origin/main --allow-major-minor
```
