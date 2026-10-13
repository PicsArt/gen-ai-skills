#!/usr/bin/env python3
"""
Skill Compliance Checker

Checks every skill under skills/ against the open Agent Skills specification
(https://agentskills.io/specification) and Anthropic's skill-authoring rules
(https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).
Those are what Claude Code, Codex, Cursor and OpenClaw read, so a skill that
passes here loads on all of them.

Errors (block the merge):
  name         required; 1-64 chars of a-z, 0-9 and single hyphens, no leading
               or trailing hyphen; equals the folder name; no "anthropic" or
               "claude"
  description  required; 1-1024 chars; says what the skill does and when to use it
  xml-tags     no XML tag in name or description (hosts refuse the upload)
  fields       compatibility is a string of at most 500 chars; metadata is a
               mapping; allowed-tools is a string
  links        every relative link in a markdown file resolves
  paths        file paths use forward slashes

Warnings (printed, never block):
  size           SKILL.md is over 500 lines
  references     a reference sits more than one level below references/
  reference-toc  a reference over 100 lines has no "## Contents" list near the top
  leaves-skill   a link points outside the skill's folder, which breaks when the
                 skill is installed on its own
  unknown-field  a frontmatter field that is neither in the spec nor a known
                 host extension (Hermes: version, author, platforms; Claude Code:
                 user-invocable, disable-model-invocation, argument-hint, model)

Hermes Agent's fields (version, author, platforms, metadata.hermes) are optional.
The body has no required sections: the spec sets "no format restrictions".

Usage:
    python scripts/check-skill-compliance.py                # all skills
    python scripts/check-skill-compliance.py skills/foo     # one skill dir
    python scripts/check-skill-compliance.py path/to/SKILL.md  # one file
    python scripts/check-skill-compliance.py --files-from /tmp/changed.txt

Exit codes:
    0 — no errors (warnings allowed)
    1 — one or more skills have errors
    2 — usage error

Standard library only.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from dataclasses import dataclass, field

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

NAME_MAX = 64
DESCRIPTION_MAX = 1024
COMPATIBILITY_MAX = 500
SKILL_LINES_MAX = 500
REFERENCE_LINES_WITHOUT_CONTENTS = 100
CONTENTS_WITHIN = 20

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RESERVED_WORDS = ("anthropic", "claude")
# A tag such as <b> or </example>; "<= 3" and "a < b" are not tags.
XML_TAG_RE = re.compile(r"</?[A-Za-z][\w:-]*(?:\s[^<>]*)?/?>")
LINK_RE = re.compile(r"\[[^\]\n]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SCHEME_RE = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)
BACKSLASH_PATH_RE = re.compile(r"[\w.-]+(?:\\[\w.-]+)+\.(?:md|py|json|ya?ml|sh|js|ts|txt)\b")
CONTENTS_RE = re.compile(r"^#{1,6}\s*(?:table of\s+)?contents\b", re.IGNORECASE)

SPEC_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
HOST_EXTENSION_FIELDS = {
    # Hermes Agent
    "version", "author", "platforms",
    # Claude Code
    "user-invocable", "disable-model-invocation", "argument-hint", "model",
}


@dataclass
class SkillReport:
    path: pathlib.Path
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


# ──────────────────────────────────────────────────────────────────────
# Frontmatter parsing (a YAML subset, stdlib only)
# ──────────────────────────────────────────────────────────────────────
def split_frontmatter(text: str) -> tuple[str, str, int] | None:
    """Return (frontmatter, body, body's first line number), or None when missing."""
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not m:
        return None
    return m.group(1), m.group(2), m.group(1).count("\n") + 3


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        inner = value[1:-1]
        return inner.replace("''", "'") if value[0] == "'" else inner.replace('\\"', '"')
    return value


def parse_frontmatter(fm: str) -> dict[str, object]:
    """Top-level keys only. A scalar becomes a string (plain, quoted, folded or
    literal, continuation lines joined); an indented `key:` block becomes a dict;
    a `- item` block or `[a, b]` becomes a list."""
    out: dict[str, object] = {}
    lines = fm.split("\n")
    i = 0
    while i < len(lines):
        m = re.match(r"^([A-Za-z_][\w-]*):(?:\s+(.*))?$", lines[i])
        i += 1
        if not m:
            continue
        key, inline = m.group(1), (m.group(2) or "").strip()
        block: list[str] = []
        while i < len(lines) and (lines[i].startswith((" ", "\t")) or lines[i].strip() == ""):
            block.append(lines[i])
            i += 1
        while block and block[-1].strip() == "":
            block.pop()
        stripped = [b.strip() for b in block if b.strip()]
        if inline in ("|", "|-", ">", ">-", "|+", ">+"):
            joiner = "\n" if inline.startswith("|") else " "
            out[key] = joiner.join(stripped)
        elif inline.startswith("[") and inline.endswith("]"):
            out[key] = [_unquote(v.strip()) for v in inline[1:-1].split(",") if v.strip()]
        elif inline:
            out[key] = _unquote(" ".join([inline, *stripped]))
        elif stripped and all(s.startswith("- ") for s in stripped):
            out[key] = [_unquote(s[2:].strip()) for s in stripped]
        elif stripped:
            nested = {}
            for s in stripped:
                sub = re.match(r"^([A-Za-z_][\w-]*):", s)
                if sub:
                    nested[sub.group(1)] = s
            out[key] = nested
        else:
            out[key] = ""
    return out


# ──────────────────────────────────────────────────────────────────────
# Rules
# ──────────────────────────────────────────────────────────────────────
def check_name(fields: dict[str, object], skill_dir: pathlib.Path, r: SkillReport) -> None:
    name = fields.get("name")
    if not isinstance(name, str) or not name.strip():
        r.errors.append("name: required")
        return
    if len(name) > NAME_MAX:
        r.errors.append(f"name: {len(name)} chars (max {NAME_MAX})")
    if not NAME_RE.match(name):
        r.errors.append(f'name: "{name}" must be lowercase letters, digits and single hyphens')
    for word in RESERVED_WORDS:
        if word in name:
            r.errors.append(f'name: "{name}" contains the reserved word "{word}"')
    if name != skill_dir.name:
        r.errors.append(f'name: "{name}" must equal the folder name "{skill_dir.name}"')


def check_description(fields: dict[str, object], r: SkillReport) -> None:
    desc = fields.get("description")
    if not isinstance(desc, str) or not desc.strip():
        r.errors.append("description: required")
        return
    if len(desc) > DESCRIPTION_MAX:
        r.errors.append(f"description: {len(desc)} chars (max {DESCRIPTION_MAX})")


def check_xml_tags(fields: dict[str, object], r: SkillReport) -> None:
    for key in ("name", "description"):
        value = fields.get(key)
        tag = XML_TAG_RE.search(value) if isinstance(value, str) else None
        if tag:
            r.errors.append(f"xml-tags: {key} holds the XML tag {tag.group(0)}; hosts refuse it")


def check_fields(fields: dict[str, object], r: SkillReport) -> None:
    compatibility = fields.get("compatibility")
    if compatibility is not None and (not isinstance(compatibility, str) or len(compatibility) > COMPATIBILITY_MAX):
        r.errors.append(f"fields: compatibility must be a string of at most {COMPATIBILITY_MAX} chars")
    if "metadata" in fields and not isinstance(fields["metadata"], dict):
        r.errors.append("fields: metadata must be a mapping")
    if "allowed-tools" in fields and not isinstance(fields["allowed-tools"], str):
        r.errors.append("fields: allowed-tools must be a space-separated string")
    for key in fields:
        if key not in SPEC_FIELDS and key not in HOST_EXTENSION_FIELDS:
            r.warnings.append(f'unknown-field: "{key}" is not in the Agent Skills spec; strict hosts may refuse it')


def line_count(text: str) -> int:
    return text.count("\n") + (0 if text.endswith("\n") or text == "" else 1)


def check_size(text: str, r: SkillReport) -> None:
    lines = line_count(text)
    if lines > SKILL_LINES_MAX:
        r.warnings.append(f"size: SKILL.md is {lines} lines; keep it to {SKILL_LINES_MAX} and move detail to references/")


def check_markdown(skill_dir: pathlib.Path, r: SkillReport) -> None:
    """Links and paths in every markdown file of the skill."""
    for md in sorted(skill_dir.rglob("*.md")):
        rel = md.relative_to(skill_dir).as_posix()
        text = md.read_text(encoding="utf-8")
        for m in BACKSLASH_PATH_RE.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            r.errors.append(f"paths: {rel}:{line} {m.group(0)} uses backslashes; write {m.group(0).replace(chr(92), '/')}")
        for m in LINK_RE.finditer(text):
            target = m.group(1).split("#", 1)[0].split("?", 1)[0]
            if not target or SCHEME_RE.match(target) or "\\" in target:
                continue
            line = text.count("\n", 0, m.start()) + 1
            if target.startswith("/"):
                r.errors.append(f"links: {rel}:{line} absolute link {target}; link relative to the file")
                continue
            resolved = (md.parent / target).resolve()
            if not resolved.exists():
                r.errors.append(f"links: {rel}:{line} broken link {target}")
            elif skill_dir.resolve() not in resolved.parents and resolved != skill_dir.resolve():
                r.warnings.append(f"leaves-skill: {rel}:{line} {target} is outside the skill; name the other skill instead")


def check_references(skill_dir: pathlib.Path, r: SkillReport) -> None:
    refs = skill_dir / "references"
    if not refs.is_dir():
        return
    for f in sorted(refs.rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(skill_dir).as_posix()
        if len(f.relative_to(refs).parts) > 1:
            r.warnings.append(f"references: {rel} is nested; keep references one level deep")
        if f.suffix != ".md":
            continue
        text = f.read_text(encoding="utf-8")
        lines = line_count(text)
        head = text.split("\n")[:CONTENTS_WITHIN]
        if lines > REFERENCE_LINES_WITHOUT_CONTENTS and not any(CONTENTS_RE.match(l) for l in head):
            r.warnings.append(f'reference-toc: {rel} is {lines} lines; open it with a "## Contents" list of its sections')


# ──────────────────────────────────────────────────────────────────────
# Driver
# ──────────────────────────────────────────────────────────────────────
def check_skill(skill_md: pathlib.Path) -> SkillReport:
    r = SkillReport(path=skill_md)
    if not skill_md.is_file():
        r.errors.append("SKILL.md not found")
        return r
    text = skill_md.read_text(encoding="utf-8")
    split = split_frontmatter(text)
    if split is None:
        r.errors.append("frontmatter: missing or malformed `--- ... ---` block")
        return r
    fields = parse_frontmatter(split[0])
    skill_dir = skill_md.parent
    check_name(fields, skill_dir, r)
    check_description(fields, r)
    check_xml_tags(fields, r)
    check_fields(fields, r)
    check_size(text, r)
    check_markdown(skill_dir, r)
    check_references(skill_dir, r)
    return r


def discover_targets(args: argparse.Namespace) -> list[pathlib.Path]:
    targets: list[pathlib.Path] = []
    if args.files_from:
        for line in pathlib.Path(args.files_from).read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            p = (REPO_ROOT / line) if not pathlib.Path(line).is_absolute() else pathlib.Path(line)
            if p.suffix == ".md" and p.name == "SKILL.md":
                targets.append(p)
    for raw in args.targets:
        p = pathlib.Path(raw)
        if not p.is_absolute():
            p = (pathlib.Path.cwd() / p).resolve()
        if p.is_file() and p.name == "SKILL.md":
            targets.append(p)
        elif p.is_dir():
            # A single skill dir, or a folder of skills such as skills/
            if (p / "SKILL.md").is_file():
                targets.append(p / "SKILL.md")
            else:
                targets.extend(sorted(p.glob("*/SKILL.md")))
        else:
            print(f"warn: skipping unknown target {raw}", file=sys.stderr)
    if not targets and not args.files_from and not args.targets:
        targets.extend(sorted(SKILLS_DIR.glob("*/SKILL.md")))
    seen: set[pathlib.Path] = set()
    return [t for t in targets if not (t in seen or seen.add(t))]


def display(path: pathlib.Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("targets", nargs="*", help="SKILL.md files, skill directories, or skills/ root (default: scan all)")
    parser.add_argument("--files-from", help="path to a file listing SKILL.md paths (one per line, used by CI)")
    parser.add_argument("--quiet", "-q", action="store_true", help="only print skills with errors or warnings")
    args = parser.parse_args()

    targets = discover_targets(args)
    if not targets:
        print("error: no SKILL.md files found to check", file=sys.stderr)
        return 2

    reports = [check_skill(t) for t in targets]
    for r in reports:
        if r.errors:
            mark = "✗"
        elif r.warnings:
            mark = "!"
        elif args.quiet:
            continue
        else:
            mark = "✓"
        print(f"  {mark} {display(r.path)}")
        for e in r.errors:
            print(f"      error   {e}")
        for w in r.warnings:
            print(f"      warning {w}")

    failed = sum(1 for r in reports if not r.ok)
    warnings = sum(len(r.warnings) for r in reports)
    print()
    print(f"  {len(reports) - failed} pass, {failed} fail, {warnings} warnings")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
