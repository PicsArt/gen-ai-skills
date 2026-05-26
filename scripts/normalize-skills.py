#!/usr/bin/env python3
"""
Skill Frontmatter & Structure Normalizer

Brings every skill under skills/ to a consistent baseline that satisfies:
  - Anthropic agentskills.io spec (https://agentskills.io/specification)
  - HermesHub submission requirements
  - Most Hermes Agent HARDLINE rules from CONTRIBUTING.md:
      * description ≤ 60 chars, one sentence, ends with a period
      * full frontmatter (version, license, author, metadata.hermes.{tags, category})
      * canonical section order: When to Use → Prerequisites → How to Run →
        Quick Reference → Procedure → Pitfalls → Verification
      * platforms: [macos, linux] for CLI-dependent skills

What this script does NOT do (out of scope for batch processing):
  - Write per-skill test files (need domain knowledge)
  - Rewrite prose to swap shell-utility names for Hermes tool names
  - Restructure prose CONTENT within a section

Usage:
  python scripts/normalize-skills.py            # apply changes in place
  python scripts/normalize-skills.py --dry-run  # show what would change
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

SKILLS_DIR = pathlib.Path(__file__).resolve().parent.parent / "skills"

# ────────────────────────────────────────────────────────────────────────
# Per-skill short descriptions (≤60 chars, one sentence, period-terminated).
# Hand-curated from the existing long-form descriptions.
# ────────────────────────────────────────────────────────────────────────
SHORT_DESCRIPTIONS: dict[str, str] = {
    "gen-ai-use":                    "Generate AI images, videos, audio via Picsart gen-ai CLI.",
    "gen-ai-persona-creation":       "Create AI influencer or branded character personas.",
    "motion-studio":                 "End-to-end AI video production with Picsart gen-ai.",
    "agency-brand-scoping":          "Five brand direction variations for pitch discovery.",
    "agency-client-handoff":         "Export a white-label client deliverable as a zip.",
    "agency-multi-brand-pack":       "Per-client asset templates scoped by workspace.",
    "agency-pitch-mockups":          "Client-branded pitch mockups: hero, tiles, slides.",
    "dev-app-assets":                "Generate icons, empty states, onboarding for apps.",
    "dev-avatar-service":            "Deterministic default-avatar generator per user.",
    "dev-og-image-service":          "Serverless dynamic OG image generator for URLs.",
    "dev-screenshot-beautifier":     "Polish raw screenshots into LP-ready heroes.",
    "ecommerce-catalog-styling":     "Replace catalog backgrounds with lifestyle scenes.",
    "ecommerce-lifestyle-compose":   "Composite a product into a lifestyle scene.",
    "ecommerce-seasonal-refresh":    "Re-skin the catalog for a holiday or season.",
    "ecommerce-variant-fan-out":     "N color or material variants from one product photo.",
    "enterprise-brand-governor":     "Gate every generation through a brand policy file.",
    "enterprise-catalog-reshoot":    "Batch reshoot N SKU variants with brand rules.",
    "enterprise-pinned-registry":    "Pin exact model versions for reproducible output.",
    "enterprise-press-batch":        "Press photos into wire, web, print, social packs.",
    "marketer-ad-variant-factory":   "Fan out 50+ ad variants from one hero image.",
    "marketer-blog-to-visuals":      "Hero, inline illustrations, OG from a blog post.",
    "marketer-campaign-kit":         "Multi-channel campaign asset bundle generator.",
    "marketer-localize-campaign":    "Localize a campaign across N markets.",
    "prosumer-content-visual-pair":  "One matching inline visual for any paragraph.",
    "prosumer-headshot-studio":      "Selfie to four polished headshots for any use.",
    "prosumer-launch-kit":           "Full product launch kit: hero, socials, reel, audio.",
    "prosumer-product-mockups":      "POD, Etsy, Shopify product mockups from artwork.",
}

# Category for metadata.hermes.category
CATEGORY: dict[str, str] = {
    "gen-ai-use":                    "creative",
    "gen-ai-persona-creation":       "creative",
    "motion-studio":                 "creative",
    "agency-brand-scoping":          "agency",
    "agency-client-handoff":         "agency",
    "agency-multi-brand-pack":       "agency",
    "agency-pitch-mockups":          "agency",
    "dev-app-assets":                "dev",
    "dev-avatar-service":            "dev",
    "dev-og-image-service":          "dev",
    "dev-screenshot-beautifier":     "dev",
    "ecommerce-catalog-styling":     "ecommerce",
    "ecommerce-lifestyle-compose":   "ecommerce",
    "ecommerce-seasonal-refresh":    "ecommerce",
    "ecommerce-variant-fan-out":     "ecommerce",
    "enterprise-brand-governor":     "enterprise",
    "enterprise-catalog-reshoot":    "enterprise",
    "enterprise-pinned-registry":    "enterprise",
    "enterprise-press-batch":        "enterprise",
    "marketer-ad-variant-factory":   "marketing",
    "marketer-blog-to-visuals":      "marketing",
    "marketer-campaign-kit":         "marketing",
    "marketer-localize-campaign":    "marketing",
    "prosumer-content-visual-pair":  "prosumer",
    "prosumer-headshot-studio":      "prosumer",
    "prosumer-launch-kit":           "prosumer",
    "prosumer-product-mockups":      "prosumer",
}

# Tag presets by skill-name prefix.
TAG_BY_PREFIX: list[tuple[str, list[str]]] = [
    ("gen-ai-use",      ["picsart", "cli", "image-generation", "video-generation", "audio-generation"]),
    ("gen-ai-persona",  ["picsart", "personas", "character-design", "creative"]),
    ("motion-studio",   ["picsart", "video", "motion-graphics", "creative"]),
    ("agency-",         ["picsart", "agency", "creative", "client-work"]),
    ("dev-",            ["picsart", "dev", "developer-tools", "automation"]),
    ("ecommerce-",      ["picsart", "ecommerce", "product-photos", "catalog"]),
    ("enterprise-",     ["picsart", "enterprise", "governance", "scale"]),
    ("marketer-",       ["picsart", "marketing", "campaigns", "creative"]),
    ("prosumer-",       ["picsart", "prosumer", "creator", "social"]),
]

# Canonical HARDLINE section order. Sections in the source that map to these
# canonical names will be renamed. Anything not in this mapping is preserved
# verbatim and appended after the canonical sections.
SECTION_RENAMES: dict[str, str] = {
    # case-insensitive lookup keys are stored lowercase
    "when to use":               "When to Use",
    "when to use it":            "When to Use",
    "when to use this":          "When to Use",
    "inputs / interview":        "Prerequisites",
    "inputs":                    "Prerequisites",
    "prerequisites":             "Prerequisites",
    "workflow":                  "How to Run",
    "how to run":                "How to Run",
    "how to use":                "How to Run",
    "manifest pattern":          "Quick Reference",
    "model selection":           "Quick Reference",
    "quick reference":           "Quick Reference",
    "command groups":            "Quick Reference",
    "best practices":            "Procedure",
    "procedure":                 "Procedure",
    "common pitfalls":           "Pitfalls",
    "pitfalls":                  "Pitfalls",
    "common mistakes":           "Pitfalls",
    "verification":              "Verification",
}

CANONICAL_ORDER = [
    "When to Use",
    "Prerequisites",
    "How to Run",
    "Quick Reference",
    "Procedure",
    "Pitfalls",
    "Verification",
]


def parse_frontmatter(text: str) -> tuple[dict, str, str]:
    """Return (frontmatter_dict, raw_frontmatter_block, body)."""
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not m:
        return {}, "", text
    raw = m.group(1)
    body = m.group(2)

    # Minimal YAML-ish parser sufficient for our generated files.
    # We don't import yaml to keep the script stdlib-only.
    fm: dict[str, object] = {}
    lines = raw.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if ":" in line and not line.startswith(" "):
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            # Block scalar (|, >)
            if val in ("|", ">"):
                buf: list[str] = []
                i += 1
                while i < len(lines) and (lines[i].startswith(" ") or not lines[i].strip()):
                    buf.append(lines[i].strip())
                    i += 1
                fm[key] = " ".join(b for b in buf if b)
                continue
            fm[key] = val
        i += 1
    return fm, raw, body


def split_sections(body: str) -> tuple[str, list[tuple[str, int, str]]]:
    """Return (preamble, sections) where sections is [(heading_text, heading_level, body), ...]."""
    # Find all ## or ### headings. We treat the # title as separate.
    parts: list[tuple[str, int, str]] = []
    # Strip leading top-level title (we'll keep it in preamble)
    section_re = re.compile(r"^(#{2,3})\s+(.+?)\s*$", re.MULTILINE)
    matches = list(section_re.finditer(body))
    if not matches:
        return body, []
    preamble = body[: matches[0].start()]
    for idx, m in enumerate(matches):
        level = len(m.group(1))
        heading = m.group(2).strip()
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
        section_body = body[start:end].lstrip("\n")
        parts.append((heading, level, section_body))
    return preamble, parts


def normalize_skill(skill_dir: pathlib.Path, *, dry_run: bool) -> list[str]:
    """Normalize one skill's SKILL.md. Returns a list of human-readable changes."""
    name = skill_dir.name
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"  ! no SKILL.md in {skill_dir}"]

    original = skill_md.read_text()
    fm, _, body = parse_frontmatter(original)
    changes: list[str] = []

    # ── 1. Short description ────────────────────────────────────────────
    new_desc = SHORT_DESCRIPTIONS.get(name)
    if new_desc is None:
        changes.append(f"  ! no short description registered for '{name}'")
        new_desc = fm.get("description", "")
    if new_desc and len(new_desc) > 60:
        changes.append(f"  ! short description still too long ({len(new_desc)} chars)")
    if fm.get("description") != new_desc:
        changes.append(f"  ~ description: {len(str(fm.get('description', '')))} → {len(new_desc)} chars")
        fm["description"] = new_desc

    # ── 2. Required frontmatter fields ──────────────────────────────────
    if "version" not in fm:
        fm["version"] = "1.0.0"
        changes.append("  + version: 1.0.0")
    if "license" not in fm:
        fm["license"] = "MIT"
        changes.append("  + license: MIT")

    # author: keep existing if present, else Picsart
    has_author_top = any(
        ln.startswith("author:") for ln in original.splitlines()
    )
    has_author_nested = re.search(r"^\s+author:", original, re.MULTILINE)
    if not (has_author_top or has_author_nested):
        # We'll inject author at the top level when we re-emit.
        fm["author"] = "Picsart"
        changes.append("  + author: Picsart")
    elif has_author_nested and not has_author_top:
        # Promote metadata.author to top level for HARDLINE consistency.
        nested = re.search(r"^\s+author:\s*(.+)$", original, re.MULTILINE)
        if nested:
            fm["author"] = nested.group(1).strip()
            changes.append(f"  ~ author promoted to top level: {fm['author']}")

    # tags + category
    cat = CATEGORY.get(name, "creative")
    tags = next(
        (tags for prefix, tags in TAG_BY_PREFIX if name.startswith(prefix)),
        ["picsart", "creative"],
    )
    fm["__hermes_tags"] = tags
    fm["__hermes_category"] = cat

    # platforms — most Picsart CLI skills work on macos + linux
    if "platforms" not in fm:
        fm["platforms"] = "[macos, linux]"
        changes.append("  + platforms: [macos, linux]")

    # ── 3. Section normalization ────────────────────────────────────────
    preamble, sections = split_sections(body)
    seen_canonical: set[str] = set()
    canonical_buckets: dict[str, list[tuple[str, int, str]]] = {n: [] for n in CANONICAL_ORDER}
    extra_sections: list[tuple[str, int, str]] = []
    renamed_count = 0

    for heading, level, sec_body in sections:
        key = heading.lower().strip()
        canon = SECTION_RENAMES.get(key)
        if canon and canon in canonical_buckets:
            if heading != canon:
                renamed_count += 1
            canonical_buckets[canon].append((canon, level, sec_body))
            seen_canonical.add(canon)
        else:
            extra_sections.append((heading, level, sec_body))

    if renamed_count:
        changes.append(f"  ~ renamed {renamed_count} section header(s) to canonical form")

    # Inject missing canonical sections with a placeholder so the order is complete.
    for sec_name in CANONICAL_ORDER:
        if not canonical_buckets[sec_name]:
            placeholder = {
                "When to Use":     "_See the description above._\n",
                "Prerequisites":   "Picsart `gen-ai` CLI installed and authenticated (`gen-ai login`).\n",
                "How to Run":      "_Use the agent's `terminal` tool to invoke `gen-ai` commands as described in the Procedure below._\n",
                "Quick Reference": "_See the Procedure for canonical commands._\n",
                "Procedure":       "_See sections below for the detailed walkthrough._\n",
                "Pitfalls":        "_See Common Pitfalls below._\n",
                "Verification":    "Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.\n",
            }[sec_name]
            canonical_buckets[sec_name].append((sec_name, 2, placeholder))
            changes.append(f"  + added placeholder ## {sec_name}")

    # ── 4. Re-emit ──────────────────────────────────────────────────────
    out_lines: list[str] = ["---"]
    # Emit frontmatter in a deterministic, HARDLINE-friendly order.
    out_lines.append(f"name: {name}")
    desc = fm.get("description", "")
    out_lines.append(f"description: {desc}")
    out_lines.append(f"version: {fm.get('version', '1.0.0')}")
    out_lines.append(f"author: {fm.get('author', 'Picsart')}")
    out_lines.append(f"license: {fm.get('license', 'MIT')}")
    if "allowed-tools" in fm:
        out_lines.append(f"allowed-tools: {fm['allowed-tools']}")
    out_lines.append(f"platforms: {fm.get('platforms', '[macos, linux]')}")
    out_lines.append("metadata:")
    out_lines.append("  hermes:")
    out_lines.append(f"    category: {fm['__hermes_category']}")
    out_lines.append(f"    tags: [{', '.join(fm['__hermes_tags'])}]")
    out_lines.append("---")
    out_lines.append("")
    out_lines.append(preamble.strip())
    out_lines.append("")

    # Canonical sections in order — always emitted at level 2 (##),
    # even if the source had them deeper (e.g. ### Quick Reference).
    for sec_name in CANONICAL_ORDER:
        for heading, level, sec_body in canonical_buckets[sec_name]:
            out_lines.append(f"## {sec_name}")
            out_lines.append("")
            out_lines.append(sec_body.rstrip())
            out_lines.append("")

    # Extras at the end, preserving original headings.
    for heading, level, sec_body in extra_sections:
        hashes = "#" * level
        out_lines.append(f"{hashes} {heading}")
        out_lines.append("")
        out_lines.append(sec_body.rstrip())
        out_lines.append("")

    new_text = "\n".join(out_lines).rstrip() + "\n"

    if new_text != original:
        if not dry_run:
            skill_md.write_text(new_text)
        changes.insert(0, f"  → {'(dry-run) ' if dry_run else ''}rewrote SKILL.md")
    else:
        changes.append("  ✓ no changes needed")

    return changes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="show changes without writing")
    parser.add_argument("--only", help="normalize only the named skill", default=None)
    args = parser.parse_args()

    if not SKILLS_DIR.is_dir():
        print(f"skills/ not found at {SKILLS_DIR}", file=sys.stderr)
        return 1

    skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())
    if args.only:
        skill_dirs = [p for p in skill_dirs if p.name == args.only]

    print(f"Normalizing {len(skill_dirs)} skill(s){' (dry-run)' if args.dry_run else ''}\n")
    total_changed = 0
    for d in skill_dirs:
        print(f"{d.name}")
        for line in normalize_skill(d, dry_run=args.dry_run):
            print(line)
            if "rewrote" in line:
                total_changed += 1
        print()

    print(f"Done. {total_changed} of {len(skill_dirs)} SKILL.md file(s) modified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
