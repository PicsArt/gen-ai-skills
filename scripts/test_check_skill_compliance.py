"""Tests for check-skill-compliance.py. Run: python3 -m unittest discover -s scripts -p 'test_*.py'"""

from __future__ import annotations

import importlib.util
import pathlib
import sys
import tempfile
import unittest

_SPEC = importlib.util.spec_from_file_location(
    "check_skill_compliance", pathlib.Path(__file__).with_name("check-skill-compliance.py"))
checker = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = checker  # dataclasses look the module up by name
_SPEC.loader.exec_module(checker)


def skill(root: pathlib.Path, name: str, frontmatter: str, body: str = "\n# Skill\n", files: dict[str, str] | None = None) -> pathlib.Path:
    d = root / name
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(f"---\n{frontmatter}\n---\n{body}", encoding="utf-8")
    for rel, text in (files or {}).items():
        (d / rel).parent.mkdir(parents=True, exist_ok=True)
        (d / rel).write_text(text, encoding="utf-8")
    return d / "SKILL.md"


GOOD = "name: demo\ndescription: Does demo things. Use when a test needs a demo."


class CheckSkillTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def check(self, frontmatter: str = GOOD, body: str = "\n# Skill\n", files: dict[str, str] | None = None, name: str = "demo"):
        # A fresh folder per call, so one test can check several skills of the same name.
        root = pathlib.Path(tempfile.mkdtemp(dir=self.root))
        return checker.check_skill(skill(root, name, frontmatter, body, files))

    def test_minimal_spec_skill_passes_clean(self) -> None:
        r = self.check()
        self.assertEqual((r.errors, r.warnings), ([], []))

    def test_long_multiline_description_and_any_sections_pass(self) -> None:
        desc = "description: Turn a screen recording into a short vertical promo, with the waiting cut and\n  each request typed out over its result. Use when the user has a screen recording."
        r = self.check(f"name: demo\n{desc}", body="\n# Demo\n\n## Steps\n\n## Notes\n")
        self.assertEqual(r.errors, [])

    def test_hermes_and_claude_code_fields_are_optional_and_allowed(self) -> None:
        fm = GOOD + "\nversion: 1.0.0\nauthor: Picsart\nplatforms: [macos, linux]\nuser-invocable: false\nmetadata:\n  hermes:\n    tags: [a, b]"
        r = self.check(fm)
        self.assertEqual((r.errors, r.warnings), ([], []))

    def test_unknown_field_warns(self) -> None:
        r = self.check(GOOD + "\nflavour: mint")
        self.assertEqual(r.errors, [])
        self.assertIn('unknown-field: "flavour" is not in the Agent Skills spec; strict hosts may refuse it', r.warnings)

    def test_name_rules(self) -> None:
        self.assertIn('name: "other" must equal the folder name "demo"',
                      self.check("name: other\ndescription: x. Use when testing.").errors)
        self.assertIn('name: "claude-demo" contains the reserved word "claude"',
                      self.check("name: claude-demo\ndescription: x.", name="claude-demo").errors)
        self.assertIn('name: "bad--name" must be lowercase letters, digits and single hyphens',
                      self.check("name: bad--name\ndescription: x.", name="bad--name").errors)

    def test_description_rules(self) -> None:
        self.assertIn("description: required", self.check("name: demo").errors)
        self.assertIn("description: 1025 chars (max 1024)", self.check(f"name: demo\ndescription: {'x' * 1025}").errors)

    def test_xml_tags_fail_but_comparisons_do_not(self) -> None:
        self.assertIn("xml-tags: description holds the XML tag <b>; hosts refuse it",
                      self.check("name: demo\ndescription: Does <b>bold</b> things.").errors)
        self.assertEqual(self.check("name: demo\ndescription: Cuts 1080x1920 frames at <= 3 s.").errors, [])

    def test_links_and_paths(self) -> None:
        body = "\nSee [gone](references/missing.md), [ok](references/guide.md) and `scripts\\cut.py`.\n"
        r = self.check(body=body, files={"references/guide.md": "# Guide\n"})
        self.assertIn("links: SKILL.md:6 broken link references/missing.md", r.errors)
        self.assertIn("paths: SKILL.md:6 scripts\\cut.py uses backslashes; write scripts/cut.py", r.errors)
        self.assertEqual(len(r.errors), 2)

    def test_link_out_of_the_skill_warns(self) -> None:
        skill(self.root, "other", "name: other\ndescription: x.")
        r = checker.check_skill(skill(self.root, "demo", GOOD, "\nSee [other](../other/SKILL.md).\n"))
        self.assertEqual(r.errors, [])
        self.assertIn("leaves-skill: SKILL.md:6 ../other/SKILL.md is outside the skill; name the other skill instead", r.warnings)

    def test_reference_contents_and_depth_warn(self) -> None:
        long_ref = "# Guide\n\n" + "line\n" * 110
        r = self.check(files={"references/long.md": long_ref, "references/ok.md": "# Ok\n\n## Contents\n\n- A\n" + "line\n" * 110,
                              "references/deep/x.md": "# x\n"})
        self.assertEqual(r.errors, [])
        self.assertIn('reference-toc: references/long.md is 112 lines; open it with a "## Contents" list of its sections', r.warnings)
        self.assertIn("references: references/deep/x.md is nested; keep references one level deep", r.warnings)
        self.assertEqual(len(r.warnings), 2)

    def test_size_warns(self) -> None:
        r = self.check(body="\n" + "line\n" * 600)
        self.assertEqual(r.errors, [])
        self.assertTrue(any(w.startswith("size: SKILL.md is") for w in r.warnings))

    def test_missing_frontmatter_fails(self) -> None:
        d = self.root / "demo"
        d.mkdir()
        (d / "SKILL.md").write_text("# no frontmatter\n", encoding="utf-8")
        self.assertEqual(checker.check_skill(d / "SKILL.md").errors, ["frontmatter: missing or malformed `--- ... ---` block"])


if __name__ == "__main__":
    unittest.main()
