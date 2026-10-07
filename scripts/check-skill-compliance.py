#!/usr/bin/env python3
"""
Skill Compliance Checker for MCP Consolidation

Verifies every SKILL.md under skills/ meets the consolidated MCP standards:

  1.  description ≤ 1024 characters (YAML scalar parsing: plain, quoted, folded, literal)
  2.  Full frontmatter:
        name, description, version, author, license, platforms,
        metadata.hermes.{category, tags}
  3.  Name equals directory name, ≤64 chars, matches [a-z0-9]+(-[a-z0-9]+)*
  4.  SKILL.md ≤ 500 lines
  5.  Canonical ## section order:
        When to Use → Prerequisites → How to Run → Quick Reference →
        Procedure → Pitfalls → Verification
      (extras allowed after the canonical seven)
  6.  Every relative markdown link resolves inside skills/
  7.  Every file under skill dir is reachable from SKILL.md via .md links
  8.  No symlinks (symlinked file, symlinked skill dir, symlinked skills/ root)
  9.  No forbidden strings (single-surface guard)
  10. Tool names (picsart_*) are served by the picsart MCP (scripts/picsart-mcp-tools.json)

Usage:
    python scripts/check-skill-compliance.py                # all skills
    python scripts/check-skill-compliance.py skills/foo     # one skill dir
    python scripts/check-skill-compliance.py path/to/SKILL.md  # one file
    python scripts/check-skill-compliance.py --files-from /tmp/changed.txt

Exit codes:
    0 — all checked skills pass
    1 — one or more skills failed
    2 — usage error
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from collections import deque
from dataclasses import dataclass, field

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

REQUIRED_TOP_LEVEL = ["name", "description", "version", "author", "license", "platforms"]
REQUIRED_HERMES = ["category", "tags"]

CANONICAL_SECTIONS = [
    "When to Use",
    "Prerequisites",
    "How to Run",
    "Quick Reference",
    "Procedure",
    "Pitfalls",
    "Verification",
]

DESC_MAX = 1024

# Forbidden strings (case-insensitive)
FORBIDDEN_STRINGS = [
    "mcp.picsart.io",
    "api.picsart.io",
    "video-api.picsart.io",
    "vd-api.picsart.io",
    "genai-api.picsart.io",
    "picsart-gen-ai",
    "PICSART_API_KEY",
    "X-Picsart-API-Key",
    "mcp__codex_apps__",
    "/Users/",
    "genai_list_presets",
    "genai_get_preset",
    "genai_run_preset",
    "mp_upload",
    "not yet served",
    "research/",
    "pa-ai-models",
    "SPEC.md",
    "@picsart/replay",
]

# Load tool allowlist: the tools the picsart MCP serves
TOOLS_ALLOWLIST: list[str] = []
def load_tools_allowlist() -> list[str]:
    """Load picsart-mcp-tools.json, a flat JSON list of served tool names."""
    global TOOLS_ALLOWLIST
    TOOLS_ALLOWLIST = []
    tools_file = REPO_ROOT / "scripts" / "picsart-mcp-tools.json"
    try:
        data = json.loads(tools_file.read_text())
    except (json.JSONDecodeError, OSError):
        return TOOLS_ALLOWLIST
    if isinstance(data, list) and all(isinstance(x, str) for x in data):
        TOOLS_ALLOWLIST = data
    return TOOLS_ALLOWLIST


@dataclass
class SkillReport:
    path: pathlib.Path
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


# ──────────────────────────────────────────────────────────────────────
# YAML Frontmatter parsing (stdlib-only, handles block scalars)
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
    """Look for the hermes: block and capture its first-level subkeys."""
    m = re.search(r"^\s*hermes:\s*\n((?:[ \t]+[^\n]*\n?)+)", fm, re.MULTILINE)
    if not m:
        return set()
    block = m.group(1)
    return {
        m.group(1)
        for m in re.finditer(r"^\s+([a-zA-Z_][a-zA-Z0-9_-]*):", block, re.MULTILINE)
    }


def get_description(fm: str) -> str | None:
    """
    Extract description from YAML frontmatter, handling:
    - plain: description: text here
    - single-quoted: description: 'text here'
    - double-quoted: description: "text here"
    - folded: description: > or description: >- or description: >+
    - literal: description: | or description: |- or description: |+
    - multi-line plain scalars
    - multi-line quoted scalars
    - multi-line literal/folded with indentation

    For block scalars (| and >), handles indentation stripping, folding rules,
    and chomping indicators per YAML 1.2 spec.
    For plain/quoted scalars, handles continuation lines with proper folding,
    including blank lines within the scalar.
    """
    # Try block scalar (folded or literal) FIRST
    # Match description: | or description: > (with optional - for strip or + for keep)
    # Must be followed by newline, not just whitespace
    m = re.search(
        r"^description:[ \t]*([|>])([-+]?)[ \t]*\n",
        fm,
        re.MULTILINE,
    )
    if m:
        block_type = m.group(1)  # '|' or '>'
        chomp = m.group(2)  # '-', '+', or ''

        # Find the content lines (all subsequent lines that are indented more than the key)
        start_pos = m.end()
        rest_text = fm[start_pos:]
        lines_iter = rest_text.split("\n")

        content_lines = []
        # Determine the base indentation from the first non-empty content line
        base_indent = None
        for line in lines_iter:
            # Empty line - could be content (blank line in the scalar)
            if not line.strip():
                # Empty line - keep it if we've started collecting content
                if base_indent is not None:
                    content_lines.append("")
                continue

            # Non-empty line
            stripped = line.lstrip(" \t")
            indent_level = len(line) - len(stripped)

            # For the first non-blank line, set base indentation
            if base_indent is None:
                base_indent = indent_level
                content_lines.append(line)
            elif indent_level >= base_indent:
                # Still indented enough, it's content
                content_lines.append(line)
            else:
                # Less indented, end of block
                break

        if not content_lines or not any(l.strip() for l in content_lines):
            return None

        # Process content based on block type
        if block_type == "|":
            # Literal: preserve newlines, strip common indentation
            if base_indent is not None:
                # Strip base indentation from each line
                text_lines = []
                for line in content_lines:
                    if line.strip():  # Non-empty line
                        # Remove base indentation
                        if len(line) > base_indent:
                            text_lines.append(line[base_indent:])
                        else:
                            text_lines.append(line.lstrip())
                    else:
                        # Blank line - preserve it (empty string = blank line)
                        text_lines.append("")
            else:
                text_lines = content_lines

            # Reconstruct with proper newlines
            text = ""
            for i, line in enumerate(text_lines):
                text += line
                if i < len(text_lines):
                    text += "\n"

            # Handle chomping
            if chomp == "-":
                # Strip: remove all trailing newlines
                text = text.rstrip("\n")
            elif chomp == "+":
                # Keep: preserve all trailing newlines
                pass
            else:
                # Clip (default): keep exactly one trailing newline
                text = text.rstrip("\n") + "\n"

            return text if text.strip() else None
        else:
            # Folded: fold lines but preserve newlines for more-indented lines
            if base_indent is not None:
                result = []
                for line in content_lines:
                    if not line.strip():
                        # Blank line
                        result.append("")
                    else:
                        # Non-empty line
                        indent_level = len(line) - len(line.lstrip(" \t"))
                        if indent_level > base_indent:
                            # More-indented line: preserve leading spaces after base indent
                            extra_indent = " " * (indent_level - base_indent)
                            result.append(extra_indent + line.lstrip(" \t"))
                        else:
                            # At base indentation: strip and fold
                            result.append(line[base_indent:] if len(line) > base_indent else line.lstrip())
            else:
                result = content_lines

            # Fold: join lines with spaces (folding single newlines), preserve blank lines as newlines
            text = ""
            for i, line in enumerate(result):
                if not line.strip():
                    # Blank line - contribute a newline
                    if text:
                        text += "\n"
                else:
                    # Non-blank line
                    if text:
                        # Check if previous line was blank or current line is more-indented
                        prev_blank = (i > 0 and not result[i - 1].strip())
                        more_indented = line.startswith(" ")
                        if prev_blank or more_indented:
                            text += "\n"
                        else:
                            text += " "
                    text += line.strip() if not line.startswith(" ") else line

                    # Add newline after non-blank lines (for folded blocks, each line ends with newline)
                    if i < len(result) - 1:
                        text += "\n"

            # Handle chomping
            if chomp == "-":
                # Strip: remove all trailing newlines
                text = text.rstrip("\n")
            elif chomp == "+":
                # Keep: preserve all trailing newlines
                pass
            else:
                # Clip (default): keep exactly one trailing newline
                text = text.rstrip("\n") + "\n"

            return text if text.strip() else None

    # Try inline with empty/quoted empty strings
    m = re.search(r"^description:[ \t]*(['\"])\1[ \t]*$", fm, re.MULTILINE)
    if m:
        # Empty string: "" or ''
        return None

    # Try quoted or plain inline with continuation lines
    # First try to match opening of quoted or plain value
    m = re.search(r"^description:[ \t]*(['\"]?)(.*)$", fm, re.MULTILINE)
    if not m:
        return None

    quote_char = m.group(1)  # '' for unquoted, or ' or "
    first_line_content = m.group(2)

    # If there's a quote character, handle quoted scalar
    if quote_char:
        # For quoted scalars, we need to find the closing quote
        # and handle continuation lines (indented lines are continuations)
        text = first_line_content

        # If the line ends with the closing quote, we're done
        if text.endswith(quote_char):
            text = text[:-len(quote_char)]
        else:
            # Look for continuation lines
            lines = fm.split("\n")
            # Find the line with description
            desc_line_idx = None
            for idx, line in enumerate(lines):
                if line.startswith("description:"):
                    desc_line_idx = idx
                    break

            if desc_line_idx is not None:
                # Look at subsequent lines that are more indented
                for idx in range(desc_line_idx + 1, len(lines)):
                    line = lines[idx]
                    # Check if this is a continuation (more indented) or a new key
                    if line and not line[0].isspace():
                        # New key, end of value
                        break

                    if line.startswith("  ") or line.startswith("\t"):
                        # Continuation line
                        cont = line.lstrip()
                        if not cont:
                            # Blank continuation line - fold to newline
                            text += "\n"
                        else:
                            # Non-empty continuation - fold with space
                            if quote_char == '"':
                                # For double-quoted, merge lines with space
                                text += " " + cont
                            elif quote_char == "'":
                                text += " " + cont

                        # Check if this line has the closing quote
                        if cont.endswith(quote_char):
                            text = text[:-len(quote_char)]
                            break
            else:
                # Didn't find the line, treat as single-line
                if text.endswith(quote_char):
                    text = text[:-len(quote_char)]

        # Unescape quoted strings
        if quote_char == "'":
            text = text.replace("''", "'")
        elif quote_char == '"':
            # For double-quoted, we might need to handle escape sequences
            # but for now, just leave them as-is
            pass

        return text.strip() if text.strip() else None

    # Plain scalar (unquoted)
    # It ends at the first line that is not indented more than the key
    if not first_line_content.strip():
        return None

    text = first_line_content

    # Look for continuation lines
    lines = fm.split("\n")
    desc_line_idx = None
    for idx, line in enumerate(lines):
        if line.startswith("description:"):
            desc_line_idx = idx
            break

    if desc_line_idx is not None:
        # Look at subsequent lines that are more indented
        for idx in range(desc_line_idx + 1, len(lines)):
            line = lines[idx]

            # Check if this is a continuation (more indented) or a new key
            if line and not line[0].isspace():
                # New key or at same level, end of value
                break

            if line.startswith("  ") or line.startswith("\t"):
                # Continuation line - fold with space
                cont = line.strip()
                if not cont:
                    # Blank continuation line - fold to newline
                    text += "\n"
                else:
                    text += " " + cont
            elif not line.strip():
                # Blank line inside value - continue looking for more indented content
                # Keep the blank line but don't end the scalar yet
                text += "\n"

    return text.strip() if text.strip() else None


# ──────────────────────────────────────────────────────────────────────
# Validation checks
# ──────────────────────────────────────────────────────────────────────
def check_description(desc: str | None, r: SkillReport) -> None:
    """Check description: presence, length, whitespace."""
    if desc is None:
        r.failures.append("description: missing")
        return
    if not desc or not desc.strip():
        r.failures.append("description: empty or whitespace-only")
        return
    if len(desc) > DESC_MAX:
        r.failures.append(f"description: {len(desc)} chars (max {DESC_MAX})")


def check_name(fm: str, skill_dir: pathlib.Path, r: SkillReport) -> None:
    """Check name: exists, equals directory, ≤64 chars, valid pattern."""
    m = re.search(r"^name:\s*['\"]?([^'\"\n]+)['\"]?\s*$", fm, re.MULTILINE)
    if not m:
        r.failures.append("name: missing or malformed")
        return
    name = m.group(1).strip()
    dir_name = skill_dir.name
    if name != dir_name:
        r.failures.append(f"name: '{name}' does not match directory '{dir_name}'")
    if len(name) > 64:
        r.failures.append(f"name: {len(name)} chars (max 64)")
    if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name):
        r.failures.append(
            f"name: '{name}' must match pattern ^[a-z0-9]+(-[a-z0-9]+)*$"
        )


def check_frontmatter_fields(fm: str, r: SkillReport) -> None:
    """Check required frontmatter fields."""
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


def check_skill_md_lines(skill_md: pathlib.Path, r: SkillReport) -> None:
    """Check SKILL.md line count ≤500."""
    text = skill_md.read_text()
    lines = text.count("\n") + (1 if text and not text.endswith("\n") else 0)
    if lines > 500:
        r.failures.append(f"SKILL.md: {lines} lines (max 500)")


def check_section_order(body: str, r: SkillReport) -> None:
    """Check canonical section order."""
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


def strip_fenced_code_blocks(text: str) -> str:
    """
    Remove fenced code blocks from text following CommonMark rules.

    An opening fence is a line whose stripped form starts with 3+ backticks
    or 3+ tildes (up to 3 spaces of indent). It closes on a line made of
    the same character, at least as long as the opener, and nothing else.
    An unclosed fence runs to EOF. Inline backticks never open a fence.

    Returns text with all fenced blocks removed.
    """
    lines = text.split("\n")
    result_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip(" \t")

        # Check for fence opener: line starts with 3+ backticks or 3+ tildes
        if stripped.startswith("```") or stripped.startswith("~~~"):
            # Count the fence character and get its count
            fence_char = stripped[0]
            fence_len = 0
            for ch in stripped:
                if ch == fence_char:
                    fence_len += 1
                else:
                    break

            # Only consider it a fence if we have 3+ characters
            if fence_len >= 3:
                # Look for closing fence
                i += 1
                while i < len(lines):
                    close_line = lines[i]
                    close_stripped = close_line.lstrip(" \t")

                    # Check if this line is a valid closing fence
                    # It must start with the same character, have at least as many,
                    # and only contain that character (and spaces/tabs before it)
                    if close_stripped.startswith(fence_char):
                        close_len = 0
                        for ch in close_stripped:
                            if ch == fence_char:
                                close_len += 1
                            else:
                                break

                        # Valid closing if same char, at least as long, and nothing else after
                        if close_len >= fence_len and close_stripped == fence_char * close_len:
                            # Found closing fence, skip to next line
                            i += 1
                            break

                    i += 1
                # After the loop, i points to the line after the closing fence
                # or past EOF if unclosed
                continue

        # Not a fence line, keep it
        result_lines.append(line)
        i += 1

    return "\n".join(result_lines)


def find_markdown_files(skill_dir: pathlib.Path) -> list[pathlib.Path]:
    """Find all .md files under skill_dir, excluding dotfiles and __pycache__."""
    md_files = []
    try:
        for md_path in skill_dir.rglob("*.md"):
            # Skip dotfiles and __pycache__
            parts = md_path.relative_to(skill_dir).parts
            if any(p.startswith(".") or p == "__pycache__" for p in parts):
                continue
            md_files.append(md_path)
    except (OSError, RuntimeError):
        pass
    return md_files


def find_links_in_markdown(md_text: str, md_file: pathlib.Path) -> list[tuple[str, int]]:
    """
    Find all relative markdown links in text.
    Returns list of (target, line_number) tuples.
    Handles:
    - inline links: [text](path#fragment "title")
    - reference-style definitions: [id]: path "title"
    - angle-bracket targets: [text](<path>)

    Ignores:
    - http(s), mailto, tel schemes
    - pure anchors (#only)
    - links inside fenced code blocks (``` or ~~~ blocks)
    - HTML href attributes
    """
    # Remove fenced code blocks using CommonMark-compliant stripper
    text = strip_fenced_code_blocks(md_text)

    links = []
    line_num = 1
    for line in text.split("\n"):
        # Inline links: [text](path) or [text](path#fragment) or [text](path "title")
        for m in re.finditer(r"\[[^\]]*\]\(<?([^)>#\s]+)(?:[>#][^)]*)?(?:\s+['\"]?[^)]*['\"])?\)", line):
            target = m.group(1)
            if target.startswith(("http://", "https://", "mailto:", "tel:")):
                continue
            if target:
                links.append((target, line_num))

        # Reference-style definitions: [id]: path or [id]: <path> or [id]: path "title"
        for m in re.finditer(r"^\s*\[([^\]]+)\]:\s*<?([^>\s#]+)(?:[#>].*)?(?:\s+['\"].*['\"])?", line):
            target = m.group(2)
            if target.startswith(("http://", "https://", "mailto:", "tel:", "scheme:")):
                continue
            if target and not target.startswith("#"):
                links.append((target, line_num))

        line_num += 1
    return links


def check_link_in_md_file(
    md_file: pathlib.Path, target: str, skills_dir: pathlib.Path, r: SkillReport
) -> pathlib.Path | None:
    """
    Resolve a link target from md_file. Return resolved path if it exists and is
    within skills_dir, else record failure and return None.
    """
    resolved = (md_file.parent / target).resolve()
    skills_dir_resolved = skills_dir.resolve()
    try:
        # Check if resolved is within skills_dir
        resolved.relative_to(skills_dir_resolved)
    except ValueError:
        try:
            md_rel = md_file.relative_to(REPO_ROOT)
        except ValueError:
            md_rel = str(md_file)
        r.failures.append(
            f"broken link: {target} (in {md_rel}) escapes skills/ directory"
        )
        return None

    if not resolved.exists():
        try:
            md_rel = md_file.relative_to(REPO_ROOT)
            res_rel = resolved.relative_to(REPO_ROOT)
        except ValueError:
            md_rel = str(md_file)
            res_rel = str(resolved)
        r.failures.append(
            f"broken link: {target} (in {md_rel}) → {res_rel} does not exist"
        )
        return None
    return resolved


def check_links(skill_dir: pathlib.Path, skills_dir: pathlib.Path, r: SkillReport) -> None:
    """Check all relative markdown links in all .md files under skill_dir."""
    md_files = find_markdown_files(skill_dir)
    for md_file in md_files:
        text = md_file.read_text()
        links = find_links_in_markdown(text, md_file)
        for target, line_num in links:
            check_link_in_md_file(md_file, target, skills_dir, r)


def check_reachability(skill_dir: pathlib.Path, r: SkillReport) -> None:
    """
    Check that every file under skill_dir (excluding dotfiles, __pycache__)
    is reachable from SKILL.md via relative links through .md files.
    """
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return  # Will be caught elsewhere

    # BFS: start from SKILL.md, follow .md links, track reachable files
    visited_files: set[pathlib.Path] = set()
    queue: deque[pathlib.Path] = deque([skill_md])
    visited_files.add(skill_md)

    while queue:
        current = queue.popleft()
        text = current.read_text()
        links = find_links_in_markdown(text, current)
        for target, _ in links:
            resolved = (current.parent / target).resolve()
            if resolved.exists() and resolved not in visited_files:
                visited_files.add(resolved)
                if resolved.suffix == ".md":
                    queue.append(resolved)

    # Find all files under skill_dir that should be reachable
    all_files: set[pathlib.Path] = set()
    try:
        for f in skill_dir.rglob("*"):
            if f.is_file():
                parts = f.relative_to(skill_dir).parts
                if not any(p.startswith(".") or p == "__pycache__" for p in parts):
                    all_files.add(f)
    except (OSError, RuntimeError):
        pass

    # Find unreachable files
    unreachable = all_files - visited_files
    for f in sorted(unreachable):
        try:
            rel_path = f.relative_to(REPO_ROOT)
        except ValueError:
            rel_path = f.relative_to(skill_dir.parent.parent)
        r.failures.append(
            f"unreachable file: {rel_path} (not linked from SKILL.md)"
        )


def check_symlinks(skill_dir: pathlib.Path, skills_dir: pathlib.Path, r: SkillReport) -> None:
    """Check for symlinks under skill_dir, at skill_dir itself, or at skills_dir root."""
    # Check skills_dir root
    if skills_dir.is_symlink():
        r.failures.append(f"symlink: skills/ directory is a symlink")

    # Check skill_dir itself
    if skill_dir.is_symlink():
        r.failures.append(f"symlink: {skill_dir.name}/ is a symlink")

    # Check all files/dirs under skill_dir (not following symlinks)
    try:
        for item in skill_dir.rglob("*"):
            if item.is_symlink():
                try:
                    rel_path = item.relative_to(REPO_ROOT)
                except ValueError:
                    rel_path = item.relative_to(skill_dir.parent.parent)
                r.failures.append(f"symlink: {rel_path} is a symlink")
    except (OSError, RuntimeError):
        pass


def normalize_markdown(text: str) -> str:
    """
    Normalize text for forbidden-string checking:
    - Remove ** and * emphasis markers
    - Remove \\ escape sequences
    """
    # Remove markdown emphasis markers
    text = re.sub(r"\*\*", "", text)
    text = re.sub(r"\*", "", text)
    # Remove backslash escapes
    text = text.replace("\\", "")
    return text


def check_forbidden_strings(skill_dir: pathlib.Path, r: SkillReport) -> None:
    """
    Check for forbidden strings in all files under skill_dir.
    Includes dotfiles (which are copied on install).
    Normalizes markdown to catch escaped/emphasized versions.
    Scans files with multiple decoding strategies to detect forbidden strings in non-UTF-8 files.
    """
    forbidden_lower = [s.lower() for s in FORBIDDEN_STRINGS]
    try:
        for f in skill_dir.rglob("*"):
            if f.is_file():
                parts = f.relative_to(skill_dir).parts
                # Skip __pycache__ but include dotfiles (they are copied on install)
                if any(p == "__pycache__" for p in parts):
                    continue
                try:
                    # Try to read as UTF-8 text
                    text = f.read_text()
                    texts_to_check = [text]
                except UnicodeDecodeError:
                    # File is not UTF-8; try reading bytes and decode with replacements
                    try:
                        data = f.read_bytes()
                        # Strategy 1: UTF-8 with replacement characters
                        texts_to_check = [data.decode("utf-8", "replace")]
                        # Strategy 2: UTF-16 ASCII content (remove null bytes)
                        texts_to_check.append(data.replace(b"\x00", b"").decode("utf-8", "replace"))
                    except OSError as e:
                        # Cannot read file at all
                        try:
                            rel_path = f.relative_to(REPO_ROOT)
                        except ValueError:
                            rel_path = f.relative_to(skill_dir.parent.parent)
                        r.failures.append(f"cannot read {rel_path}: {e}")
                        continue
                except OSError as e:
                    # Cannot read file (permission, etc.)
                    try:
                        rel_path = f.relative_to(REPO_ROOT)
                    except ValueError:
                        rel_path = f.relative_to(skill_dir.parent.parent)
                    r.failures.append(f"cannot read {rel_path}: {e}")
                    continue

                # Check all decodings for forbidden strings
                found_forbidden = set()  # Track which forbidden strings we've already reported
                for text in texts_to_check:
                    # Normalize text for markdown emphasis and escapes
                    normalized = normalize_markdown(text)
                    text_lower = normalized.lower()
                    for forbidden, forbidden_low in zip(FORBIDDEN_STRINGS, forbidden_lower):
                        if forbidden_low in text_lower and forbidden not in found_forbidden:
                            try:
                                rel_path = f.relative_to(REPO_ROOT)
                            except ValueError:
                                # Not under REPO_ROOT (e.g., in test temp dir)
                                rel_path = f.relative_to(skill_dir.parent.parent)
                            r.failures.append(
                                f"forbidden string: '{forbidden}' found in {rel_path}"
                            )
                            found_forbidden.add(forbidden)
    except (OSError, RuntimeError):
        pass


def check_tool_names(skill_dir: pathlib.Path, r: SkillReport) -> None:
    """
    Check that every picsart_* tool name in the skill is served by the picsart MCP.

    Matching rules (case-insensitive, every file in the skill; all-caps
    PICSART_* environment variables are skipped):
    - Exact match: picsart_foo must be in scripts/picsart-mcp-tools.json
    - Glob match: picsart_foo_* passes only if a listed name starts with picsart_foo_
    - mcp__<server>__picsart_* tokens: the picsart_* part is checked
    """
    if not TOOLS_ALLOWLIST:
        r.failures.append("tool allowlist: empty or invalid picsart-mcp-tools.json")
        return
    allowed = set(TOOLS_ALLOWLIST)

    def is_served(name: str) -> bool:
        if name.endswith("*"):
            return any(t.startswith(name[:-1]) for t in allowed)
        return name in allowed

    bare = re.compile(r"(?<![A-Za-z0-9_.-])(picsart_[a-z0-9_]*[a-z0-9*])(?![A-Za-z0-9_-])", re.IGNORECASE)
    prefixed = re.compile(r"mcp__[a-z0-9_-]+?__(picsart_[a-z0-9_]*[a-z0-9*])(?![A-Za-z0-9_-])", re.IGNORECASE)

    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        try:
            text = path.read_bytes().decode("utf-8", "replace")
        except OSError:
            continue
        try:
            rel = path.relative_to(REPO_ROOT)
        except ValueError:
            rel = path.relative_to(skill_dir.parent.parent)
        reported: set[str] = set()
        for pattern in (bare, prefixed):
            for m in pattern.finditer(text):
                if m.group(1).isupper():
                    continue  # PICSART_* environment variables, not tools
                name = m.group(1).lower()
                if name in reported or is_served(name):
                    continue
                reported.add(name)
                line_num = text.count("\n", 0, m.start()) + 1
                r.failures.append(
                    f"tool allowlist: '{name}' not in the served tool list ({rel}:{line_num})"
                )


# ──────────────────────────────────────────────────────────────────────
# Driver
# ──────────────────────────────────────────────────────────────────────
def check_skill(skill_md: pathlib.Path, skills_dir: pathlib.Path) -> SkillReport:
    """Run all checks on one skill."""
    skill_dir = skill_md.parent
    r = SkillReport(path=skill_md)

    if not skill_md.is_file():
        r.failures.append("SKILL.md not found")
        return r

    text = skill_md.read_text()
    fm, body = split_frontmatter(text)
    if not fm:
        r.failures.append("frontmatter: missing or malformed `--- ... ---` block")
        return r

    # Frontmatter checks
    check_description(get_description(fm), r)
    check_name(fm, skill_dir, r)
    check_frontmatter_fields(fm, r)

    # Structure checks
    check_skill_md_lines(skill_md, r)
    check_section_order(body, r)

    # Link and reachability checks
    check_links(skill_dir, skills_dir, r)
    check_reachability(skill_dir, r)

    # Content checks
    check_symlinks(skill_dir, skills_dir, r)
    check_forbidden_strings(skill_dir, r)
    check_tool_names(skill_dir, r)

    return r


def discover_targets(args: argparse.Namespace) -> list[pathlib.Path]:
    """Discover target SKILL.md files from CLI arguments."""
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

    # Load allowlist
    load_tools_allowlist()

    targets = discover_targets(args)
    if not targets:
        print("error: no SKILL.md files found to check", file=sys.stderr)
        return 2

    reports = [check_skill(t, SKILLS_DIR) for t in targets]
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
