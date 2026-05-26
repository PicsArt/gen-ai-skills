#!/usr/bin/env python3
"""
Skill Compliance Checker

Verifies every SKILL.md under skills/ meets the standards we enforce on
this repo (sourced from the Hermes Agent HARDLINE rules plus our own
catalog conventions):

  1.  description ≤ 60 characters, one sentence, ends with a period
  2.  Full frontmatter:
        name, description, version, author, license, platforms,
        metadata.hermes.{category, tags}
  3.  Canonical ## section order:
        When to Use → Prerequisites → How to Run → Quick Reference →
        Procedure → Pitfalls → Verification
      (extras allowed after the canonical seven)
  4.  Every relative-link target inside SKILL.md exists
        (catches stale references/ moves, renamed sibling skills, etc.)

Usage:
    python scripts/check-skill-compliance.py                # all skills
    python scripts/check-skill-compliance.py skills/foo     # one skill dir
    python scripts/check-skill-compliance.py path/to/SKILL.md  # one file
    python scripts/check-skill-compliance.py --files-from /tmp/changed.txt

Exit codes:
    0 — all checked skills pass
    1 — one or more skills failed
    2 — usage error

CI integration: GitHub Actions calls this with a --files-from list of
SKILL.md paths that changed in the PR. On main pushes it runs against the
whole skills/ tree.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from dataclasses import dataclass, field

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

REQUIRED_TOP_LEVEL = ["name", "description", "version", "author", "license", "platforms"]
REQUIRED_HERMES    = ["category", "tags"]

CANONICAL_SECTIONS = [
    "When to Use",
    "Prerequisites",
    "How to Run",
    "Quick Reference",
    "Procedure",
    "Pitfalls",
    "Verification",
]

DESC_MAX = 60


@dataclass
class SkillReport:
    path: pathlib.Path
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


# ──────────────────────────────────────────────────────────────────────
# Frontmatter parsing (stdlib-only, no yaml dependency)
# ──────────────────────────────────────────────────────────────────────
def split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter_text, body). Empty frontmatter if missing."""
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not m:
        return "", text
    return m.group(1), m.group(2)


def top_level_keys(fm: str) -> set[str]:
    return {
        m.group(1)
        for m in re.finditer(r"^([a-zA-Z_][a-zA-Z0-9_-]*):", fm, re.MULTILINE)
    }


def hermes_subkeys(fm: str) -> set[str]:
    # Look for the hermes: block and capture its first-level subkeys.
    m = re.search(r"^\s*hermes:\s*\n((?:[ \t]+[^\n]*\n?)+)", fm, re.MULTILINE)
    if not m:
        return set()
    block = m.group(1)
    return {
        m.group(1)
        for m in re.finditer(r"^\s+([a-zA-Z_][a-zA-Z0-9_-]*):", block, re.MULTILINE)
    }


def get_description(fm: str) -> str | None:
    # Inline form
    m = re.search(r"^description:\s*(.+)$", fm, re.MULTILINE)
    if m:
        return m.group(1).strip()
    # Block-scalar (|, >) form — rare here after normalization, but handle it
    m = re.search(r"^description:\s*\|?\s*\n((?:[ \t]+.*\n)+)", fm, re.MULTILINE)
    if m:
        return " ".join(line.strip() for line in m.group(1).splitlines() if line.strip())
    return None


# ──────────────────────────────────────────────────────────────────────
# Per-rule checks
# ──────────────────────────────────────────────────────────────────────
def check_description(desc: str | None, r: SkillReport) -> None:
    if desc is None:
        r.failures.append("description: missing")
        return
    if len(desc) > DESC_MAX:
        r.failures.append(f"description: {len(desc)} chars (max {DESC_MAX})")
    if not desc.endswith("."):
        r.failures.append("description: must end with a period")
    # very rough one-sentence heuristic: no embedded periods other than the terminator
    if desc.count(".") > 1:
        r.failures.append("description: looks like more than one sentence")


def check_frontmatter_fields(fm: str, r: SkillReport) -> None:
    top = top_level_keys(fm)
    for key in REQUIRED_TOP_LEVEL:
        if key not in top:
            r.failures.append(f"frontmatter: missing top-level `{key}`")
    if "metadata" not in top:
        r.failures.append("frontmatter: missing `metadata.hermes.{category,tags}`")
        return
    hsub = hermes_subkeys(fm)
    for key in REQUIRED_HERMES:
        if key not in hsub:
            r.failures.append(f"frontmatter: missing `metadata.hermes.{key}`")


def check_section_order(body: str, r: SkillReport) -> None:
    headings = [m.group(1).strip() for m in re.finditer(r"^##\s+(.+)$", body, re.MULTILINE)]
    canonical_seen: list[str] = []
    seen = set()
    for h in headings:
        if h in CANONICAL_SECTIONS and h not in seen:
            canonical_seen.append(h)
            seen.add(h)
    missing = [c for c in CANONICAL_SECTIONS if c not in seen]
    if missing:
        r.failures.append(f"sections: missing {', '.join(missing)}")
    expected_order = [c for c in CANONICAL_SECTIONS if c in seen]
    if canonical_seen != expected_order:
        r.failures.append(
            f"sections: out of order — got {canonical_seen}, expected {expected_order}"
        )


def check_local_links(body: str, skill_dir: pathlib.Path, r: SkillReport) -> None:
    # Find [text](path) where path is relative and not http(s)/mailto/#anchor
    for m in re.finditer(r"\[[^\]]*\]\(([^)\s#]+)(?:\s+\"[^\"]*\")?\)", body):
        target = m.group(1)
        if target.startswith(("http://", "https://", "mailto:", "tel:")):
            continue
        # Strip query/fragment
        target = target.split("#", 1)[0].split("?", 1)[0]
        if not target:
            continue
        # Resolve relative to skill directory
        resolved = (skill_dir / target).resolve()
        if not resolved.exists():
            r.failures.append(f"broken link: {target}")


# ──────────────────────────────────────────────────────────────────────
# Driver
# ──────────────────────────────────────────────────────────────────────
def check_skill(skill_md: pathlib.Path) -> SkillReport:
    r = SkillReport(path=skill_md)
    if not skill_md.is_file():
        r.failures.append("SKILL.md not found")
        return r
    text = skill_md.read_text()
    fm, body = split_frontmatter(text)
    if not fm:
        r.failures.append("frontmatter: missing or malformed `--- ... ---` block")
        return r

    check_description(get_description(fm), r)
    check_frontmatter_fields(fm, r)
    check_section_order(body, r)
    check_local_links(body, skill_md.parent, r)
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
            p = (REPO_ROOT / p).resolve()
        if p.is_file() and p.name == "SKILL.md":
            targets.append(p)
        elif p.is_dir():
            # Treat as a single skill dir, or as skills/ root
            if (p / "SKILL.md").is_file():
                targets.append(p / "SKILL.md")
            else:
                for s in sorted(p.glob("*/SKILL.md")):
                    targets.append(s)
        else:
            print(f"warn: skipping unknown target {raw}", file=sys.stderr)
    if not targets:
        for s in sorted(SKILLS_DIR.glob("*/SKILL.md")):
            targets.append(s)
    # De-duplicate while preserving order
    seen: set[pathlib.Path] = set()
    uniq: list[pathlib.Path] = []
    for t in targets:
        if t not in seen:
            uniq.append(t)
            seen.add(t)
    return uniq


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "targets", nargs="*",
        help="SKILL.md files, skill directories, or skills/ root (default: scan all)",
    )
    parser.add_argument(
        "--files-from",
        help="path to a file listing SKILL.md paths (one per line, used by CI)",
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true",
        help="only print failures",
    )
    args = parser.parse_args()

    targets = discover_targets(args)
    if not targets:
        print("error: no SKILL.md files found to check", file=sys.stderr)
        return 2

    reports = [check_skill(t) for t in targets]
    failed = [r for r in reports if not r.ok]
    passed = [r for r in reports if r.ok]

    # Output
    if not args.quiet:
        for r in passed:
            rel = r.path.relative_to(REPO_ROOT)
            print(f"  ✓ {rel}")
    for r in failed:
        rel = r.path.relative_to(REPO_ROOT)
        print(f"  ✗ {rel}")
        for f in r.failures:
            print(f"      - {f}")

    print()
    print(f"  {len(passed)} pass, {len(failed)} fail")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
