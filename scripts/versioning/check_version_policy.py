#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
from dataclasses import dataclass

ROOT = pathlib.Path(__file__).resolve().parents[2]

PLUGIN_REL = "aria/.claude-plugin/plugin.json"
MARKETPLACE_REL = ".claude-plugin/marketplace.json"
COMMAND_VERSIONS_REL = "aria/commands/versions.json"

COMMAND_FILE_RE = re.compile(r"^aria/commands/([^/]+)\.md$")
SKILL_FILE_RE = re.compile(r"^aria/skills/([^/]+)/")
VERSION_LINE_RE = re.compile(r'^\s*version:\s*"?(\d+)\.(\d+)\.(\d+)"?\s*$')
VERSION_LINE_CONTENT_RE = re.compile(r'^version:\s*"?\d+\.\d+\.\d+"?$')


@dataclass(frozen=True)
class SemVer:
    major: int
    minor: int
    patch: int

    @classmethod
    def parse(cls, raw: str, context: str) -> "SemVer":
        parts = raw.strip().split(".")
        if len(parts) != 3 or not all(p.isdigit() for p in parts):
            raise ValueError(f"{context}: invalid semver '{raw}'")
        return cls(int(parts[0]), int(parts[1]), int(parts[2]))

    def major_minor(self) -> tuple[int, int]:
        return (self.major, self.minor)

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


def run_git(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result


def git_show(base_ref: str, rel_path: str) -> str | None:
    result = run_git(["show", f"{base_ref}:{rel_path}"], check=False)
    if result.returncode != 0:
        return None
    return result.stdout


def resolve_base_commit(base_ref: str) -> str:
    result = run_git(["merge-base", base_ref, "HEAD"])
    return result.stdout.strip()


def changed_files(base_commit: str) -> list[str]:
    result = run_git(["diff", "--name-only", base_commit, "--"])
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def load_json_file(rel_path: str) -> dict:
    return json.loads((ROOT / rel_path).read_text(encoding="utf-8"))


def load_json_from_git(base_ref: str, rel_path: str) -> dict | None:
    content = git_show(base_ref, rel_path)
    if content is None:
        return None
    return json.loads(content)


def plugin_version_from_plugin_json(data: dict) -> SemVer:
    return SemVer.parse(data["version"], PLUGIN_REL)


def plugin_version_from_marketplace(data: dict) -> SemVer:
    for plugin in data.get("plugins", []):
        if plugin.get("name") == "aria":
            return SemVer.parse(plugin["version"], MARKETPLACE_REL)
    raise ValueError("marketplace: plugin 'aria' entry not found")


def load_command_versions_map_from_json(data: dict, context: str) -> dict[str, SemVer]:
    versions: dict[str, SemVer] = {}
    for command_name, raw_version in data.items():
        versions[command_name] = SemVer.parse(str(raw_version), f"{context}:{command_name}")
    return versions


def load_current_command_versions() -> dict[str, SemVer]:
    data = load_json_file(COMMAND_VERSIONS_REL)
    return load_command_versions_map_from_json(data, COMMAND_VERSIONS_REL)


def load_base_command_versions(base_ref: str) -> dict[str, SemVer] | None:
    data = load_json_from_git(base_ref, COMMAND_VERSIONS_REL)
    if data is None:
        return None
    return load_command_versions_map_from_json(data, f"{base_ref}:{COMMAND_VERSIONS_REL}")


def extract_frontmatter(text: str, rel_path: str) -> str:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{rel_path}: frontmatter start '---' not found")

    fm_lines: list[str] = []
    for line in lines[1:]:
        if line.strip() == "---":
            return "\n".join(fm_lines)
        fm_lines.append(line)
    raise ValueError(f"{rel_path}: frontmatter end '---' not found")


def extract_skill_version(text: str, rel_path: str) -> SemVer:
    frontmatter = extract_frontmatter(text, rel_path)
    for line in frontmatter.splitlines():
        match = VERSION_LINE_RE.match(line)
        if match:
            return SemVer(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    raise ValueError(f"{rel_path}: metadata.version not found in frontmatter")


def load_current_skill_versions() -> dict[str, SemVer]:
    versions: dict[str, SemVer] = {}
    for skill_md in sorted((ROOT / "aria/skills").glob("*/SKILL.md")):
        rel = skill_md.relative_to(ROOT).as_posix()
        skill_name = skill_md.parent.name
        versions[skill_name] = extract_skill_version(skill_md.read_text(encoding="utf-8"), rel)
    return versions


def load_base_skill_versions(base_ref: str, skills: list[str]) -> dict[str, SemVer]:
    versions: dict[str, SemVer] = {}
    for skill_name in skills:
        rel = f"aria/skills/{skill_name}/SKILL.md"
        content = git_show(base_ref, rel)
        if content is None:
            continue
        versions[skill_name] = extract_skill_version(content, f"{base_ref}:{rel}")
    return versions


def command_changes(changed: list[str]) -> set[str]:
    names: set[str] = set()
    for rel in changed:
        match = COMMAND_FILE_RE.match(rel)
        if match:
            names.add(match.group(1))
    return names


def skill_md_is_version_only_change(base_ref: str, rel_path: str) -> bool:
    diff = run_git(
        ["diff", "--unified=0", base_ref, "--", rel_path],
        check=False,
    ).stdout

    has_edits = False
    for line in diff.splitlines():
        if line.startswith(("+++", "---", "@@")):
            continue
        if not line.startswith(("+", "-")):
            continue
        has_edits = True
        content = line[1:].strip()
        if not content:
            continue
        if VERSION_LINE_CONTENT_RE.fullmatch(content):
            continue
        return False

    return has_edits


def skill_changes(base_ref: str, changed: list[str]) -> set[str]:
    names: set[str] = set()
    for rel in changed:
        match = SKILL_FILE_RE.match(rel)
        if not match:
            continue
        skill_name = match.group(1)
        if rel.endswith("/SKILL.md") and skill_md_is_version_only_change(base_ref, rel):
            continue
        names.add(skill_name)
    return names


def validate_component_version(
    *,
    label: str,
    old: SemVer,
    new: SemVer,
    should_have_changed: bool,
    allow_major_minor: bool,
    errors: list[str],
) -> None:
    if not should_have_changed:
        if old != new:
            errors.append(f"{label}: changed without file update ({old} -> {new})")
        return

    major_minor_changed = old.major_minor() != new.major_minor()
    if major_minor_changed:
        if not allow_major_minor:
            errors.append(f"{label}: major/minor changed ({old} -> {new})")
        return

    if new.patch <= old.patch:
        errors.append(f"{label}: patch must increase ({old} -> {new})")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate ARIA version policy across plugin, commands, and skills.",
    )
    parser.add_argument("--base-ref", required=True, help="Base git ref (e.g., origin/main or <sha>).")
    parser.add_argument(
        "--allow-major-minor",
        action="store_true",
        help="Allow major/minor changes (use only for explicit user-requested version jumps).",
    )
    args = parser.parse_args()

    try:
        base_commit = resolve_base_commit(args.base_ref)
        changed = changed_files(base_commit)

        current_plugin_json = load_json_file(PLUGIN_REL)
        current_marketplace = load_json_file(MARKETPLACE_REL)
        current_plugin = plugin_version_from_plugin_json(current_plugin_json)
        current_marketplace_plugin = plugin_version_from_marketplace(current_marketplace)

        current_commands = load_current_command_versions()
        base_commands = load_base_command_versions(base_commit)

        current_skills = load_current_skill_versions()
        base_skills = load_base_skill_versions(base_commit, sorted(current_skills.keys()))

        changed_commands = command_changes(changed)
        changed_skills = skill_changes(base_commit, changed)

        errors: list[str] = []
        warnings: list[str] = []

        if current_plugin != current_marketplace_plugin:
            errors.append(
                "plugin version mismatch: "
                f"{PLUGIN_REL}={current_plugin}, "
                f"{MARKETPLACE_REL}=aria:{current_marketplace_plugin}"
            )

        base_plugin_json = load_json_from_git(base_commit, PLUGIN_REL)
        if base_plugin_json is None:
            warnings.append(f"bootstrap: '{PLUGIN_REL}' missing at base commit, plugin delta check skipped.")
        else:
            old_plugin = plugin_version_from_plugin_json(base_plugin_json)
            validate_component_version(
                label="plugin",
                old=old_plugin,
                new=current_plugin,
                should_have_changed=bool(changed),
                allow_major_minor=args.allow_major_minor,
                errors=errors,
            )

        missing_command_versions = changed_commands - set(current_commands.keys())
        for command_name in sorted(missing_command_versions):
            errors.append(f"command:{command_name}: missing version entry in {COMMAND_VERSIONS_REL}")

        if base_commands is None:
            warnings.append(f"bootstrap: '{COMMAND_VERSIONS_REL}' missing at base commit, command delta check skipped.")
        else:
            for command_name in sorted(set(base_commands.keys()) | set(current_commands.keys())):
                old = base_commands.get(command_name)
                new = current_commands.get(command_name)
                if old is None or new is None:
                    warnings.append(f"command:{command_name}: added/removed command detected; delta check skipped.")
                    continue
                validate_component_version(
                    label=f"command:{command_name}",
                    old=old,
                    new=new,
                    should_have_changed=(command_name in changed_commands),
                    allow_major_minor=args.allow_major_minor,
                    errors=errors,
                )

        for skill_name in sorted(changed_skills):
            if skill_name not in current_skills:
                warnings.append(f"skill:{skill_name}: removed skill detected; delta check skipped.")

        for skill_name in sorted(current_skills.keys()):
            old = base_skills.get(skill_name)
            new = current_skills[skill_name]
            if old is None:
                warnings.append(f"skill:{skill_name}: new skill detected; delta check skipped.")
                continue
            validate_component_version(
                label=f"skill:{skill_name}",
                old=old,
                new=new,
                should_have_changed=(skill_name in changed_skills),
                allow_major_minor=args.allow_major_minor,
                errors=errors,
            )

        if errors:
            print("Version policy check failed:")
            for error in errors:
                print(f"- {error}")
            if warnings:
                print("\nWarnings:")
                for warning in warnings:
                    print(f"- {warning}")
            return 1

        print("Version policy check passed.")
        if warnings:
            print("Warnings:")
            for warning in warnings:
                print(f"- {warning}")
        return 0

    except Exception as exc:
        print(f"Version policy check error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
