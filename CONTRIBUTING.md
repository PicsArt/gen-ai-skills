# Contributing

Thanks for your interest in contributing to `gen-ai-skills`.

## Adding a skill

1. Create a directory under `skills/` named after your skill in kebab-case (e.g. `skills/picsart-upscale/`). The directory name is the install name users see at `~/.claude/skills/<name>/`.

2. Add a `SKILL.md` at the root of that directory. **Frontmatter must include every field below** — CI will fail your PR otherwise:

   ```markdown
   ---
   name: picsart-upscale
   description: One-sentence description ending with a period.
   version: 1.0.0
   author: Picsart
   license: MIT
   platforms: [macos, linux]
   metadata:
     hermes:
       category: creative
       tags: [picsart, upscale, image-quality]
   ---

   # Picsart Upscale

   Two-to-three-sentence intro stating what the skill does and what it isn't for.

   ## When to Use
   ## Prerequisites
   ## How to Run
   ## Quick Reference
   ## Procedure
   ## Pitfalls
   ## Verification
   ```

3. Put supporting files inside the skill's own directory:
   - `references/` — supplementary docs (FLAGS, EXAMPLES, etc.)
   - `scripts/` — helper scripts the skill invokes
   - `templates/` — output templates
   - `assets/` — fixtures, sample images, etc.

4. Add an entry to `.claude-plugin/marketplace.json` under `plugins[0].skills`:

   ```json
   { "name": "picsart-upscale", "path": "skills/picsart-upscale", "invoke": "/picsart:picsart-upscale" }
   ```

5. Bump the `version` in `VERSION` if this is a release-worthy change.

## HARDLINE rules (CI-enforced)

Every skill must pass `python3 scripts/check-skill-compliance.py` before merge. The check verifies:

| Rule | What it checks |
|---|---|
| **description ≤ 60 chars** | One sentence, ends with a period. State the capability, not the implementation. No marketing words. |
| **Full frontmatter** | `name`, `description`, `version`, `author`, `license`, `platforms`, `metadata.hermes.{category, tags}` all present. |
| **Canonical section order** | `## When to Use` → `## Prerequisites` → `## How to Run` → `## Quick Reference` → `## Procedure` → `## Pitfalls` → `## Verification`. Extras allowed after the canonical seven. |
| **No broken links** | Every relative link in SKILL.md must resolve to an existing file. |

Run the check locally:

```bash
python3 scripts/check-skill-compliance.py            # all skills
python3 scripts/check-skill-compliance.py skills/foo # one skill
```

If structural issues are flagged, use the normalizer as a starting point — it does what it can mechanically; you still need to write/review the prose:

```bash
python3 scripts/normalize-skills.py --dry-run        # preview changes
python3 scripts/normalize-skills.py                  # apply
```

The CI workflow (`.github/workflows/skill-compliance.yml`) runs the same check on every PR and blocks merge on failure.

## Skill conventions

- One skill = one directory under `skills/`. Don't nest skills inside skills.
- `description` is the single most important field — agents use it to decide whether to invoke the skill. Keep it short, factual, and trigger-friendly.
- Keep `SKILL.md` self-contained. Long references go in `references/` and link from `SKILL.md`.
- Don't shell out to anything that requires interactive input.
- Reference Hermes tool names in prose (`terminal`, `web_extract`, `read_file`, `search_files`, ...) instead of shell utilities (`grep`, `cat`, `curl`, `sed`).

## Pull request flow

1. Fork the repository and create a feature branch from `main` (e.g. `feat/add-upscale-skill`).
2. Run `./setup` locally and verify the new skill loads in your agent.
3. Run `python3 scripts/check-skill-compliance.py` and ensure all checks pass.
4. Open a pull request describing the skill and its motivation.
5. Be kind in code review.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](./LICENSE).   