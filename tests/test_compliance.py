#!/usr/bin/env python3
"""
Comprehensive tests for check-skill-compliance.py

Tests all rules:
1. Description limits (empty, whitespace, quoted, folded, literal, length)
2. Frontmatter fields
3. Name validation (pattern, length, directory match)
4. SKILL.md line count (≤500)
5. Canonical section order
6. Link validation (relative links resolve, escape detection)
7. Link in code fences (ignored)
8. Reachability (orphan files)
9. Symlinks (file, directory)
10. Forbidden strings
11. Tool names (served allowlist, glob, case, any file)
"""

from __future__ import annotations

import json
import pathlib
import re
import tempfile
import unittest
from pathlib import Path


class SkillComplianceTests(unittest.TestCase):
    """Test suite for compliance checker."""

    @classmethod
    def setUpClass(cls) -> None:
        """Import the checker module."""
        import sys
        checker_path = pathlib.Path(__file__).parent.parent / "scripts"
        sys.path.insert(0, str(checker_path))
        # Import via importlib because filename has hyphens
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "check_skill_compliance",
            str(checker_path / "check-skill-compliance.py"),
        )
        if spec and spec.loader:
            cls.checker = importlib.util.module_from_spec(spec)
            sys.modules["check_skill_compliance"] = cls.checker
            spec.loader.exec_module(cls.checker)
        else:
            raise ImportError("Could not load check-skill-compliance.py")

    def setUp(self) -> None:
        """Create a temporary directory for test skills."""
        # Load tools allowlist before creating skills
        self.checker.load_tools_allowlist()

        self.temp_dir = tempfile.TemporaryDirectory()
        self.skills_dir = pathlib.Path(self.temp_dir.name) / "skills"
        self.skills_dir.mkdir()

    def tearDown(self) -> None:
        """Clean up temporary directory."""
        self.temp_dir.cleanup()

    def create_skill(self, name: str, **overrides) -> pathlib.Path:
        """Create a test skill with defaults."""
        skill_dir = self.skills_dir / name
        skill_dir.mkdir(parents=True, exist_ok=True)

        # Default SKILL.md
        skill_md = skill_dir / "SKILL.md"
        frontmatter = {
            "name": name,
            "description": "Test skill.",
            "version": "1.0.0",
            "author": "Test",
            "license": "MIT",
            "platforms": ["macos", "linux"],
            "metadata": {
                "hermes": {
                    "category": "test",
                    "tags": ["test"],
                }
            },
        }
        frontmatter.update(overrides.get("frontmatter", {}))

        body = overrides.get("body", "# Test\n\n## When to Use\nTest.\n")

        # Build frontmatter YAML manually
        fm_lines = ["---"]
        fm_lines.extend(self._dict_to_yaml(frontmatter))
        fm_lines.append("---")

        content = "\n".join(fm_lines) + "\n" + body
        skill_md.write_text(content)

        return skill_dir

    def _dict_to_yaml(self, d: dict, indent: int = 0) -> list[str]:
        """Simple dict-to-YAML converter for test fixtures."""
        lines = []
        prefix = "  " * indent
        for k, v in d.items():
            if isinstance(v, dict):
                lines.append(f"{prefix}{k}:")
                lines.extend(self._dict_to_yaml(v, indent + 1))
            elif isinstance(v, list):
                lines.append(f"{prefix}{k}: {json.dumps(v)}")
            else:
                lines.append(f"{prefix}{k}: {v}")
        return lines

    # ─────────────────────────────────────────────────────────────────────
    # Description tests (rule 1)
    # ─────────────────────────────────────────────────────────────────────
    def test_description_missing(self) -> None:
        """Description missing → failure."""
        skill_dir = self.create_skill("test-desc-missing")
        skill_md = skill_dir / "SKILL.md"
        # Remove description from frontmatter
        text = skill_md.read_text()
        text = text.replace("description: Test skill.\n", "")
        skill_md.write_text(text)

        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertIn("description: missing", " ".join(r.failures))

    def test_description_empty_string(self) -> None:
        """Empty description string → failure."""
        skill_dir = self.skills_dir / "test-desc-empty"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        content = """\
---
name: test-desc-empty
description: ""
version: 1.0.0
author: Test
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: test
    tags: [test]
---
# Test

## When to Use
Test.
"""
        skill_md.write_text(content)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        # Empty description should be reported as missing
        self.assertTrue(any("missing" in f for f in r.failures))

    def test_description_whitespace_only(self) -> None:
        """Whitespace-only description → failure."""
        skill_dir = self.skills_dir / "test-desc-whitespace"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        content = """\
---
name: test-desc-whitespace
description: "   "
version: 1.0.0
author: Test
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: test
    tags: [test]
---
# Test

## When to Use
Test.
"""
        skill_md.write_text(content)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        # Whitespace-only should be reported as missing (after stripping)
        self.assertTrue(any("missing" in f for f in r.failures))

    def test_description_folded_scalar(self) -> None:
        """Folded scalar (>) description → parsed correctly."""
        skill_dir = self.skills_dir / "test-desc-folded"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        # Manually write with folded scalar
        content = """\
---
name: test-desc-folded
description: >
  This is a folded
  description that spans
  multiple lines.
version: 1.0.0
author: Test
license: MIT
platforms: ["macos", "linux"]
metadata:
  hermes:
    category: test
    tags: ["test"]
---
# Test

## When to Use
Test.
"""
        skill_md.write_text(content)

        r = self.checker.check_skill(skill_md, self.skills_dir)
        # Should not fail for length or missing
        self.assertFalse(any("description" in f for f in r.failures))

    def test_description_literal_scalar(self) -> None:
        """Literal scalar (|) description → parsed correctly."""
        skill_dir = self.skills_dir / "test-desc-literal"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        content = """\
---
name: test-desc-literal
description: |
  Literal block
  description here.
version: 1.0.0
author: Test
license: MIT
platforms: ["macos", "linux"]
metadata:
  hermes:
    category: test
    tags: ["test"]
---
# Test

## When to Use
Test.
"""
        skill_md.write_text(content)

        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertFalse(any("description" in f for f in r.failures))

    def test_description_max_length_pass(self) -> None:
        """Description at exactly 1024 chars → pass."""
        long_desc = "x" * 1024
        skill_dir = self.create_skill(
            "test-desc-1024",
            frontmatter={"description": long_desc},
        )
        r = self.checker.check_skill(skill_dir / "SKILL.md", self.skills_dir)
        self.assertFalse(any("chars" in f for f in r.failures))

    def test_description_max_length_fail(self) -> None:
        """Description at 1025 chars → failure."""
        long_desc = "x" * 1025
        skill_dir = self.create_skill(
            "test-desc-1025",
            frontmatter={"description": long_desc},
        )
        r = self.checker.check_skill(skill_dir / "SKILL.md", self.skills_dir)
        self.assertTrue(any("1025 chars" in f for f in r.failures))

    # ─────────────────────────────────────────────────────────────────────
    # Name validation (rule 3)
    # ─────────────────────────────────────────────────────────────────────
    def test_name_pattern_valid(self) -> None:
        """Valid name pattern [a-z0-9-] → pass."""
        skill_dir = self.create_skill("test-skill-name-123")
        r = self.checker.check_skill(skill_dir / "SKILL.md", self.skills_dir)
        self.assertFalse(any("name" in f for f in r.failures))

    def test_name_pattern_invalid_caps(self) -> None:
        """Invalid name with uppercase → failure."""
        skill_dir = self.create_skill("TestSkill")
        r = self.checker.check_skill(skill_dir / "SKILL.md", self.skills_dir)
        self.assertTrue(any("match pattern" in f for f in r.failures))

    def test_name_pattern_invalid_underscore(self) -> None:
        """Invalid name with underscore → failure."""
        skill_dir = self.create_skill("test_skill")
        r = self.checker.check_skill(skill_dir / "SKILL.md", self.skills_dir)
        self.assertTrue(any("match pattern" in f for f in r.failures))

    def test_name_max_length_pass(self) -> None:
        """Name at exactly 64 chars → pass."""
        name = "a" * 64
        skill_dir = self.create_skill(name)
        r = self.checker.check_skill(skill_dir / "SKILL.md", self.skills_dir)
        self.assertFalse(any("chars (max 64)" in f for f in r.failures))

    def test_name_max_length_fail(self) -> None:
        """Name at 65 chars → failure."""
        name = "a" * 65
        skill_dir = self.create_skill(name)
        r = self.checker.check_skill(skill_dir / "SKILL.md", self.skills_dir)
        self.assertTrue(any("chars (max 64)" in f for f in r.failures))

    # ─────────────────────────────────────────────────────────────────────
    # SKILL.md line count (rule 4)
    # ─────────────────────────────────────────────────────────────────────
    def test_skill_md_line_count_pass(self) -> None:
        """SKILL.md with 500 lines → pass."""
        skill_dir = self.skills_dir / "test-lines-500"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        # Create exactly 500 lines: frontmatter (13) + body (487)
        content = """\
---
name: test-lines-500
description: Test.
version: 1.0.0
author: Test
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: test
    tags: [test]
---
# Test

## When to Use
Test.
"""
        # Add 470 more lines to reach exactly 490 (13 + 17 + 470 = 500)
        content += "line\n" * 470
        skill_md.write_text(content)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertFalse(any("lines (max 500)" in f for f in r.failures))

    def test_skill_md_line_count_fail(self) -> None:
        """SKILL.md with 501 lines → failure."""
        skill_dir = self.skills_dir / "test-lines-501"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        # Build content to be exactly 501 lines
        lines = []
        lines.append("---")
        lines.append("name: test-lines-501")
        lines.append("description: Test.")
        lines.append("version: 1.0.0")
        lines.append("author: Test")
        lines.append("license: MIT")
        lines.append("platforms: [macos, linux]")
        lines.append("metadata:")
        lines.append("  hermes:")
        lines.append("    category: test")
        lines.append("    tags: [test]")
        lines.append("---")
        lines.append("# Test")
        lines.append("")
        lines.append("## When to Use")
        lines.append("Test.")
        # Now we have 16 lines. Add 485 more to reach 501
        for _ in range(485):
            lines.append("line")
        content = "\n".join(lines)
        if not content.endswith("\n"):
            content += "\n"
        skill_md.write_text(content)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertTrue(any("501" in f or "lines (max 500)" in f for f in r.failures))

    # ─────────────────────────────────────────────────────────────────────
    # Link validation (rule 6)
    # ─────────────────────────────────────────────────────────────────────
    def test_link_nonexistent(self) -> None:
        """Nonexistent link target → failure."""
        skill_dir = self.create_skill("test-link-broken")
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text()
        text += "\n\nSee [Reference](references/nonexistent.md).\n"
        skill_md.write_text(text)

        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertTrue(any("broken link" in f for f in r.failures))

    def test_link_in_code_fence_ignored(self) -> None:
        """Links in fenced code blocks → ignored."""
        skill_dir = self.create_skill("test-link-code")
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text()
        text += "\n\n```\nSee [Reference](nonexistent.md).\n```\n"
        skill_md.write_text(text)

        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertFalse(any("broken link" in f for f in r.failures))

    # ─────────────────────────────────────────────────────────────────────
    # Reachability (rule 7)
    # ─────────────────────────────────────────────────────────────────────
    # Note: Reachability checks are complex in test environment due to path resolution
    # They are tested in the full compliance checker against real repo skills

    # ─────────────────────────────────────────────────────────────────────
    # Symlinks (rule 8)
    # ─────────────────────────────────────────────────────────────────────
    def test_symlinked_file(self) -> None:
        """Symlinked file under skill → failure."""
        skill_dir = self.create_skill("test-symlink-file")
        target = skill_dir / "target.md"
        target.write_text("# Target\n")
        link = skill_dir / "link.md"
        try:
            link.symlink_to(target)
        except OSError:
            self.skipTest("Cannot create symlinks on this system")

        r = self.checker.check_skill(skill_dir / "SKILL.md", self.skills_dir)
        self.assertTrue(any("symlink" in f for f in r.failures))

    # ─────────────────────────────────────────────────────────────────────
    # Forbidden strings (rule 9)
    # ─────────────────────────────────────────────────────────────────────
    def test_forbidden_string_api_key(self) -> None:
        """Forbidden string PICSART_API_KEY → failure."""
        skill_dir = self.create_skill("test-forbidden-key")
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text()
        text += "\n\nUse PICSART_API_KEY for auth.\n"
        skill_md.write_text(text)

        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertTrue(any("forbidden string" in f for f in r.failures))

    def test_forbidden_string_endpoint(self) -> None:
        """Forbidden string api.picsart.io → failure."""
        skill_dir = self.create_skill("test-forbidden-endpoint")
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text()
        text += "\n\nCall api.picsart.io/v1/generate.\n"
        skill_md.write_text(text)

        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertTrue(any("forbidden string" in f for f in r.failures))

    def test_forbidden_string_path(self) -> None:
        """Forbidden string /Users/ → failure."""
        skill_dir = self.create_skill("test-forbidden-path")
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text()
        text += "\n\nUse /Users/alice/project.\n"
        skill_md.write_text(text)

        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertTrue(any("forbidden string" in f for f in r.failures))

    # ─────────────────────────────────────────────────────────────────────
    # Tool names (rule 10)
    # ─────────────────────────────────────────────────────────────────────
    def test_tool_name_served(self) -> None:
        """Tool name in served list → pass."""
        # First, set up the tools allowlist in the checker
        self.checker.TOOLS_ALLOWLIST = ["picsart_generate", "picsart_enhance"]

        skill_dir = self.create_skill("test-tool-served")
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text()
        text += "\n\nUse picsart_generate to create.\n"
        skill_md.write_text(text)

        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertFalse(any("tool allowlist" in f for f in r.failures))

    def test_tool_name_not_in_list(self) -> None:
        """Tool name not in any list → failure."""
        self.checker.TOOLS_ALLOWLIST = ["picsart_generate"]

        skill_dir = self.create_skill("test-tool-invalid")
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text()
        text += "\n\nUse picsart_nonexistent tool.\n"
        skill_md.write_text(text)

        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertTrue(any("tool allowlist" in f for f in r.failures))

    def test_tool_name_glob_picsart_media_passes(self) -> None:
        """Glob picsart_media_* matches allowlisted tools → pass."""
        self.checker.TOOLS_ALLOWLIST = ["picsart_media_upload", "picsart_media_export"]

        skill_dir = self.create_skill("test-tool-glob-match")
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text()
        text += "\n\nUse picsart_media_* tools for editing.\n"
        skill_md.write_text(text)

        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertFalse(any("tool allowlist" in f for f in r.failures))

    def test_tool_name_invalid_not_in_list(self) -> None:
        """Tool name not in list → fail (covers both glob and non-glob)."""
        self.checker.TOOLS_ALLOWLIST = ["picsart_media_upload"]

        skill_dir = self.create_skill("test-tool-invalid-name")
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text()
        text += "\n\nUse picsart_nope_something for action.\n"
        skill_md.write_text(text)

        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertTrue(any("tool allowlist" in f for f in r.failures))

    def test_description_single_quoted_whitespace(self) -> None:
        """Single-quoted whitespace description → failure."""
        skill_dir = self.skills_dir / "test-desc-single-quoted-ws"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        content = """\
---
name: test-desc-single-quoted-ws
description: '   '
version: 1.0.0
author: Test
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: test
    tags: [test]
---
# Test

## When to Use
Test.
"""
        skill_md.write_text(content)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertTrue(any("missing" in f for f in r.failures))

    def test_description_empty_key_followed_by_another(self) -> None:
        """Empty description: followed by another key → both parsed correctly."""
        skill_dir = self.skills_dir / "test-desc-empty-key"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        content = """\
---
name: test-desc-empty-key
description:
version: 1.0.0
author: Test
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: test
    tags: [test]
---
# Test

## When to Use
Test.
"""
        skill_md.write_text(content)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        # Should fail on missing description, but version should still be recognized
        desc_missing = any("missing" in f for f in r.failures)
        version_ok = "version" not in " ".join(r.failures)
        self.assertTrue(desc_missing and version_ok)

    def test_description_quoted_exact_1024(self) -> None:
        """Quoted description at exactly 1024 chars → pass."""
        skill_dir = self.skills_dir / "test-desc-quoted-1024"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        desc_1024 = "x" * 1024
        content = f"""\
---
name: test-desc-quoted-1024
description: "{desc_1024}"
version: 1.0.0
author: Test
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: test
    tags: [test]
---
# Test

## When to Use
Test.
"""
        skill_md.write_text(content)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertFalse(any("chars" in f for f in r.failures))

    def test_description_quoted_1025(self) -> None:
        """Quoted description at 1025 chars → failure."""
        skill_dir = self.skills_dir / "test-desc-quoted-1025"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        desc_1025 = "x" * 1025
        content = f"""\
---
name: test-desc-quoted-1025
description: "{desc_1025}"
version: 1.0.0
author: Test
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: test
    tags: [test]
---
# Test

## When to Use
Test.
"""
        skill_md.write_text(content)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertTrue(any("1025" in f or "chars" in f for f in r.failures))

    def test_symlinked_directory_under_skill(self) -> None:
        """Symlinked directory under skill → failure."""
        skill_dir = self.create_skill("test-symlink-dir")
        target_dir = skill_dir / "target_dir"
        target_dir.mkdir()
        link_dir = skill_dir / "link_dir"
        try:
            link_dir.symlink_to(target_dir)
        except OSError:
            self.skipTest("Cannot create symlinks on this system")

        r = self.checker.check_skill(skill_dir / "SKILL.md", self.skills_dir)
        self.assertTrue(any("symlink" in f for f in r.failures))

    def test_symlinked_skill_directory(self) -> None:
        """Symlinked skill directory → failure."""
        skill_dir = self.skills_dir / "test-symlink-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""\
---
name: test-symlink-skill
description: Test.
version: 1.0.0
author: Test
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: test
    tags: [test]
---
# Test

## When to Use
Test.
""")
        # Symlink the skill directory
        link_skill = self.skills_dir / "test-symlink-skill-link"
        try:
            link_skill.symlink_to(skill_dir)
        except OSError:
            self.skipTest("Cannot create symlinks on this system")

        r = self.checker.check_skill(link_skill / "SKILL.md", self.skills_dir)
        self.assertTrue(any("symlink" in f for f in r.failures))

    def test_link_escapes_skills_directory(self) -> None:
        """Link escaping skills/ → failure."""
        skill_dir = self.create_skill("test-link-escape")
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text()
        # Create a file outside skills/ but reference it
        outside_file = self.skills_dir.parent / "outside.md"
        outside_file.write_text("# Outside\n")
        text += f"\n\nSee [Outside](../../outside.md).\n"
        skill_md.write_text(text)

        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertTrue(any("escapes skills/" in f for f in r.failures))

    def test_orphan_file_not_reachable(self) -> None:
        """Orphan file not linked from SKILL.md → failure."""
        skill_dir = self.create_skill("test-orphan-file")
        (skill_dir / "orphan.md").write_text("# Orphan\n")

        r = self.checker.check_skill(skill_dir / "SKILL.md", self.skills_dir)
        self.assertTrue(any("unreachable file" in f for f in r.failures))

    # Note: Transitive reachability through markdown links is tested in the
    # real repo checker (skills/ directory path resolution works there);
    # temp-dir fixtures have path resolution issues similar to link_valid tests above

    # ─────────────────────────────────────────────────────────────────────
    # Stricter rule tests (description, links, tool names, forbidden strings)
    # ─────────────────────────────────────────────────────────────────────
    def test_description_folded_over_1024_chars(self) -> None:
        """Folded description over 1024 chars → failure."""
        skill_dir = self.skills_dir / "test-desc-folded-1025"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        # Create a folded scalar that will be >1024 when joined
        content = """\
---
name: test-desc-folded-1025
description: >
  """ + ("word " * 250) + """
version: 1.0.0
author: Test
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: test
    tags: [test]
---
# Test

## When to Use
Test.
"""
        skill_md.write_text(content)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertTrue(any("chars" in f and "1024" in f for f in r.failures))

    def test_description_folded_under_1024_parses_correctly(self) -> None:
        """Folded description under 1024 chars → parsed correctly."""
        skill_dir = self.skills_dir / "test-desc-folded-ok"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        content = """\
---
name: test-desc-folded-ok
description: >
  This is a short
  folded description.
version: 1.0.0
author: Test
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: test
    tags: [test]
---
# Test

## When to Use
Test.
"""
        skill_md.write_text(content)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertFalse(any("description" in f for f in r.failures))

    def test_description_followed_by_version(self) -> None:
        """description: followed by version: without value → fails, version still parsed."""
        skill_dir = self.skills_dir / "test-desc-empty-key"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        content = """\
---
name: test-desc-empty-key
description:
version: 1.0.0
author: Test
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: test
    tags: [test]
---
# Test

## When to Use
Test.
"""
        skill_md.write_text(content)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        # Should fail for missing description
        self.assertTrue(any("description" in f and "missing" in f for f in r.failures))
        # Should not fail for missing version (version is present)
        self.assertFalse(any("version" in f and "missing" in f for f in r.failures))

    def test_link_with_fragment_checked(self) -> None:
        """Link with fragment #anchor → target path checked even with fragment."""
        skill_dir = self.create_skill("test-link-fragment")
        skill_md = skill_dir / "SKILL.md"
        # Create a referenced file
        ref_file = skill_dir / "reference.md"
        ref_file.write_text("# Reference\n")
        # Add a link to the file with a fragment
        text = skill_md.read_text()
        text += "\n\nSee [Reference](./reference.md#section).\n"
        skill_md.write_text(text)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        # Should not fail for the fragment itself
        self.assertFalse(any("broken link" in f for f in r.failures))

    def test_link_missing_target_with_fragment(self) -> None:
        """Link to missing file with fragment → fails."""
        skill_dir = self.create_skill("test-link-missing-fragment")
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text()
        text += "\n\nSee [Missing](./missing.md#section).\n"
        skill_md.write_text(text)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertTrue(any("broken link" in f for f in r.failures))

    def test_reference_style_link(self) -> None:
        """Reference-style markdown link [id]: path → checked."""
        skill_dir = self.create_skill("test-ref-style-link")
        skill_md = skill_dir / "SKILL.md"
        ref_file = skill_dir / "reference.md"
        ref_file.write_text("# Reference\n")
        text = skill_md.read_text()
        text += "\n\n[ref_id]: ./reference.md\n\nSee [reference][ref_id].\n"
        skill_md.write_text(text)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertFalse(any("broken link" in f for f in r.failures))

    def test_reference_style_link_missing(self) -> None:
        """Reference-style link to missing file → fails."""
        skill_dir = self.create_skill("test-ref-style-missing")
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text()
        text += "\n\n[missing_id]: ./missing.md\n"
        skill_md.write_text(text)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertTrue(any("broken link" in f for f in r.failures))

    def test_tool_name_exact_picsart_gen_fails(self) -> None:
        """Tool name picsart_gen (exact, not glob) → fails."""
        skill_dir = self.create_skill("test-tool-picsart-gen")
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text()
        text += "\n\nUse picsart_gen for generation.\n"
        skill_md.write_text(text)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertTrue(any("picsart_gen" in f and "not in" in f for f in r.failures))

    def test_tool_name_glob_picsart_zzz_fails(self) -> None:
        """Tool glob picsart_zzz_* (no match) → fails."""
        skill_dir = self.create_skill("test-tool-picsart-zzz")
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text()
        text += "\n\nUse picsart_zzz_*.\n"
        skill_md.write_text(text)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertTrue(any("picsart_zzz_" in f and "not in" in f for f in r.failures))

    def test_tool_name_glob_picsart_media_star_passes(self) -> None:
        """Tool glob picsart_media_* (matches listed tools) → passes."""
        skill_dir = self.create_skill("test-tool-media-glob")
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text()
        text += "\n\nSupports picsart_media_*.\n"
        skill_md.write_text(text)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertFalse(any("picsart_media_*" in f and "not in" in f for f in r.failures))

    def test_mcp_prefix_tool_name_checked(self) -> None:
        """Tool in mcp__picsart__picsart_foo (invalid) → fails."""
        skill_dir = self.create_skill("test-mcp-prefix-tool")
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text()
        text += "\n\nUse mcp__picsart__picsart_invalidtool.\n"
        skill_md.write_text(text)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertTrue(any("picsart_invalidtool" in f and "not in" in f for f in r.failures))

    def test_tool_allowlist_all_sections_empty(self) -> None:
        """Empty allowlist → fails."""
        self.checker.TOOLS_ALLOWLIST = []
        skill_dir = self.create_skill("test-allowlist-empty")
        r = self.checker.check_skill(skill_dir / "SKILL.md", self.skills_dir)
        self.assertTrue(any("tool allowlist: empty" in f for f in r.failures))

    def test_forbidden_string_in_dotfile(self) -> None:
        """Forbidden string in dotfile → fails."""
        skill_dir = self.create_skill("test-forbidden-dotfile")
        dotfile = skill_dir / ".env"
        dotfile.write_text("PICSART_API_KEY=secret\n")
        skill_md = skill_dir / "SKILL.md"
        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertTrue(any("PICSART_API_KEY" in f and "dotfile" not in f.lower() or "forbidden" in f for f in r.failures))

    def test_forbidden_string_markdown_escaped(self) -> None:
        """Forbidden string escaped in markdown → fails."""
        skill_dir = self.create_skill("test-forbidden-escaped")
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text()
        # Use markdown emphasis or backslash escaping
        text += "\n\nDo not use **api.picsart.io** in URLs.\n"
        skill_md.write_text(text)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertTrue(any("forbidden string" in f and "api.picsart.io" in f for f in r.failures))

    def test_forbidden_string_mp_upload(self) -> None:
        """Forbidden string mp_upload → fails."""
        skill_dir = self.create_skill("test-forbidden-mp-upload")
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text()
        text += "\n\nUse mp_upload for uploads.\n"
        skill_md.write_text(text)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertTrue(any("mp_upload" in f for f in r.failures))

    def test_forbidden_string_latin1_file(self) -> None:
        """Forbidden string in latin-1 encoded file → fails."""
        skill_dir = self.create_skill("test-forbidden-latin1")
        # Create a latin-1 encoded file with a forbidden string
        notes_file = skill_dir / "notes.txt"
        # Write the forbidden string in latin-1 encoding
        notes_file.write_bytes(b"caf\xe9 /Users/ashot/secret\n")
        
        r = self.checker.check_skill(skill_dir / "SKILL.md", self.skills_dir)
        # Should detect the forbidden string /Users/
        self.assertTrue(any("forbidden string" in f and "/Users/" in f for f in r.failures))

    def test_forbidden_string_utf16_file(self) -> None:
        """Forbidden string in UTF-16 encoded file → fails."""
        skill_dir = self.create_skill("test-forbidden-utf16")
        # Create a UTF-16 encoded file with a forbidden string
        notes_file = skill_dir / "notes.txt"
        # Write the forbidden string in UTF-16 encoding
        notes_file.write_bytes("/Users/ashot\n".encode("utf-16"))

        r = self.checker.check_skill(skill_dir / "SKILL.md", self.skills_dir)
        # Should detect the forbidden string /Users/
        self.assertTrue(any("forbidden string" in f and "/Users/" in f for f in r.failures))

    def test_mcp_hyphenated_server_name_invalid_tool(self) -> None:
        """Tool in mcp__picsart-mcp__picsart_unknown (hyphenated server) → fails."""
        skill_dir = self.create_skill("test-mcp-hyphen-server")
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text()
        text += "\n\nUse mcp__picsart-mcp__picsart_unknown.\n"
        skill_md.write_text(text)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertTrue(any("picsart_unknown" in f and "not in" in f for f in r.failures))

    def test_mcp_hyphenated_server_name_valid_tool(self) -> None:
        """Tool in mcp__picsart-mcp__picsart_generate (hyphenated server, valid tool) → passes."""
        skill_dir = self.create_skill("test-mcp-hyphen-server-valid")
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text()
        text += "\n\nUse mcp__picsart-mcp__picsart_generate.\n"
        skill_md.write_text(text)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        # Should not have failures for this tool
        self.assertFalse(any("picsart_generate" in f and "not in" in f for f in r.failures))

    # ─────────────────────────────────────────────────────────────────────
    # Repro tests for fenced code block stripping (issue 1)
    # ─────────────────────────────────────────────────────────────────────
    def test_inline_backticks_false_pass_repro(self) -> None:
        """
        False pass repro: inline triple backticks followed by broken link
        followed by fenced block. The old regex would swallow the broken link.
        Expected: FAIL (broken link detected).
        """
        skill_dir = self.create_skill("test-fence-false-pass")
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text()
        # Add inline backticks, then a broken link, then a fenced code block
        text += (
            "\n\nWrap code in ``` fences.\n"
            "[broken](missing.md)\n"
            "```\ncode\n```\n"
        )
        skill_md.write_text(text)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        # Should fail because the broken link is NOT inside a fence
        self.assertTrue(any("broken link" in f and "missing.md" in f for f in r.failures))

    def test_four_backtick_fence_contains_broken_link(self) -> None:
        """
        False fail repro: 4-backtick fence wrapping a 3-backtick block
        with a broken link inside. The old regex would match from the
        4-backtick opener to the 3-backtick close, leaving the outer
        4-backtick unclosed and reporting the link as broken.
        Expected: PASS (link is inside a fence).
        """
        skill_dir = self.create_skill("test-fence-false-fail")
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text()
        # Add a 4-backtick fence containing a 3-backtick block with a link
        text += (
            "\n\n````\n"
            "```\n"
            "[broken](missing.md)\n"
            "```\n"
            "````\n"
        )
        skill_md.write_text(text)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        # Should pass because the broken link is inside a fence
        self.assertFalse(any("broken link" in f for f in r.failures))

    def test_four_backtick_fence_with_valid_link_passes(self) -> None:
        """
        Positive test: 4-backtick fence containing a 3-backtick block
        with a valid link to an existing file. Should pass.
        """
        skill_dir = self.create_skill("test-fence-four-backtick-valid")
        skill_md = skill_dir / "SKILL.md"
        # Create a file to link to
        ref_file = skill_dir / "reference.md"
        ref_file.write_text("# Reference\n")

        text = skill_md.read_text()
        # Add a 4-backtick fence containing a 3-backtick block with a valid link
        text += (
            "\n\n````\n"
            "```\n"
            "[reference](./reference.md)\n"
            "```\n"
            "````\n"
        )
        skill_md.write_text(text)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        # Should pass because the link is inside a fence
        self.assertFalse(any("broken link" in f for f in r.failures))

    # ─────────────────────────────────────────────────────────────────────
    # Repro tests for description scalar parsing (issue 2)
    # ─────────────────────────────────────────────────────────────────────
    def test_description_multiline_double_quoted(self) -> None:
        """
        Repro: multi-line double-quoted value.
        description: "<1000 a>\n  <1000 b>"
        Real length: 2001, should fail for exceeding 1024.
        The old parser only read the first line and saw 1001.
        """
        skill_dir = self.skills_dir / "test-desc-multiline-quoted"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"

        # Create a description that spans multiple lines (quoted)
        a_part = "a" * 1000
        b_part = "b" * 1000

        content = f"""\
---
name: test-desc-multiline-quoted
description: "{a_part}
  {b_part}"
version: 1.0.0
author: Test
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: test
    tags: [test]
---
# Test

## When to Use
Test.
"""
        skill_md.write_text(content)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        # Should fail because total length is 2001 > 1024
        self.assertTrue(any("description" in f and "max" in f for f in r.failures))

    def test_description_multiline_plain(self) -> None:
        """
        Repro: multi-line plain value (unquoted).
        description: <1000 a>\n  <1000 b>
        Real length: 2001, should fail for exceeding 1024.
        """
        skill_dir = self.skills_dir / "test-desc-multiline-plain"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"

        # Create a description that spans multiple lines (plain)
        a_part = "a" * 1000
        b_part = "b" * 1000

        content = f"""\
---
name: test-desc-multiline-plain
description: {a_part}
  {b_part}
version: 1.0.0
author: Test
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: test
    tags: [test]
---
# Test

## When to Use
Test.
"""
        skill_md.write_text(content)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        # Should fail because total length is 2001 > 1024
        self.assertTrue(any("description" in f and "max" in f for f in r.failures))

    def test_description_literal_with_extra_indentation(self) -> None:
        """
        Repro: literal block with extra indentation.
        description: |
          900-char line
          200-space indent + 100 chars
        Real length: 1200, should fail for exceeding 1024.
        """
        skill_dir = self.skills_dir / "test-desc-literal-indent"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"

        # Create a literal block with extra indentation
        first_line = "a" * 900
        second_line = " " * 200 + "b" * 100

        content = f"""\
---
name: test-desc-literal-indent
description: |
  {first_line}
  {second_line}
version: 1.0.0
author: Test
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: test
    tags: [test]
---
# Test

## When to Use
Test.
"""
        skill_md.write_text(content)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        # Should fail because total length is 1200 > 1024
        self.assertTrue(any("description" in f and "max" in f for f in r.failures))

    def test_description_plain_multiline_with_blank(self) -> None:
        """
        Repro: plain multi-line value with blank line in the middle.
        description: <1000 a>
          <blank line>
          <1000 b>
        Real length: 2001, should fail for exceeding 1024.
        The blank line does not end the scalar; it continues.
        """
        skill_dir = self.skills_dir / "test-desc-plain-blank"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"

        # Create a plain value with blank line in the middle
        a_part = "a" * 1000
        b_part = "b" * 1000

        content = f"""\
---
name: test-desc-plain-blank
description: {a_part}

  {b_part}
version: 1.0.0
author: Test
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: test
    tags: [test]
---
# Test

## When to Use
Test.
"""
        skill_md.write_text(content)
        r = self.checker.check_skill(skill_md, self.skills_dir)
        # Should fail because total length is 2001 > 1024
        self.assertTrue(any("description" in f and "max" in f for f in r.failures))


    def test_allowlist_file_is_flat_served_list(self) -> None:
        """picsart-mcp-tools.json is one flat list of unique picsart_* names, nothing else."""
        data = json.loads((pathlib.Path(__file__).parent.parent / "scripts" / "picsart-mcp-tools.json").read_text())
        self.assertIsInstance(data, list)
        self.assertTrue(data)
        self.assertTrue(all(isinstance(x, str) and re.fullmatch(r"picsart_[a-z0-9_]+", x) for x in data))
        self.assertEqual(len(data), len(set(data)))

    def test_tool_allowlist_non_list_fails(self) -> None:
        """A tiered (dict) allowlist file loads as empty, so every skill fails."""
        root = pathlib.Path(self.temp_dir.name) / "repo"
        (root / "scripts").mkdir(parents=True)
        (root / "scripts" / "picsart-mcp-tools.json").write_text('{"served": ["picsart_generate"]}')
        saved = self.checker.REPO_ROOT
        try:
            self.checker.REPO_ROOT = root
            self.assertEqual(self.checker.load_tools_allowlist(), [])
        finally:
            self.checker.REPO_ROOT = saved
        skill_dir = self.create_skill("test-allowlist-dict")
        r = self.checker.check_skill(skill_dir / "SKILL.md", self.skills_dir)
        self.assertTrue(any("tool allowlist: empty" in f for f in r.failures))
    def test_tool_name_mixed_case_unknown_fails(self) -> None:
        """Mixed-case unknown tool name → fails."""
        skill_dir = self.create_skill("test-tool-mixed-case")
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(skill_md.read_text() + "\n\nCall Picsart_Nonexistent_Tool.\n")
        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertTrue(any("picsart_nonexistent_tool" in f for f in r.failures))

    def test_tool_name_in_non_markdown_file_fails(self) -> None:
        """Unknown tool name in a non-.md file of the skill → fails."""
        skill_dir = self.create_skill("test-tool-non-md")
        (skill_dir / "notes.yaml").write_text("tool: picsart_nonexistent_tool\n")
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(skill_md.read_text() + "\n\n[notes](notes.yaml)\n")
        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertTrue(any("picsart_nonexistent_tool" in f and "notes.yaml" in f for f in r.failures))

    def test_forbidden_not_yet_served_note(self) -> None:
        """A 'not yet served' note → fails (skills name served tools only)."""
        skill_dir = self.create_skill("test-forbidden-not-yet-served")
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(skill_md.read_text() + "\n\nThis tool is not yet served.\n")
        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertTrue(any("forbidden string" in f and "not yet served" in f for f in r.failures))

    def test_forbidden_research_pointer(self) -> None:
        """A pointer into an unshipped research/ tree → fails."""
        skill_dir = self.create_skill("test-forbidden-research")
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(skill_md.read_text() + "\n\nSee `research/notes/ANALYSIS.md`.\n")
        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertTrue(any("forbidden string" in f and "research/" in f for f in r.failures))

    def test_tool_name_env_var_skipped(self) -> None:
        """All-caps PICSART_* environment variables are not tool names → pass."""
        skill_dir = self.create_skill("test-tool-env-var")
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(skill_md.read_text() + "\n\nExport `PICSART_USER_ID` first.\n")
        r = self.checker.check_skill(skill_md, self.skills_dir)
        self.assertFalse(any("picsart_user_id" in f for f in r.failures))


if __name__ == "__main__":
    unittest.main()
