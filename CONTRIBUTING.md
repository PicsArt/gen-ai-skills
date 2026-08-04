# Contributing

Thanks for your interest in contributing to `gen-ai-skills`. Contributions that add new skills, improve existing skill documentation, fix compliance issues, or strengthen tooling are all welcome. Please read this guide before opening a pull request.

## Repository structure

| Path | Description |
|---|---|
| `skills/` | One directory per skill, named in kebab-case |
| `scripts/` | Compliance checker, normalizer, and other dev utilities |
| `.claude-plugin/` | Plugin manifest (`marketplace.json`) consumed by the Claude agent harness |
| `.github/workflows/` | CI workflows; `skill-compliance.yml` blocks merge on any compliance failure |
| `VERSION` | Single source of truth for the current release version |

## Local setup

**Prerequisites:** Python 3.9+. No additional package installation is required for the compliance checker.

```bash
# Clone your fork
git clone https://github.com/<your-username>/gen-ai-skills.git
cd gen-ai-skills

# Run the setup script (installs the plugin into your local Claude agent)
./setup
```

After `./setup` completes, open your Claude agent and confirm the skill registry loads without errors before proceeding.

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
- If your skill requires a third-party CLI tool, API, or Python package, list it in the `## Prerequisites` section of `SKILL.md` with the minimum required version and where to obtain it. Do not assume the tool is installed.
- Do not introduce Python package dependencies in `scripts/` without updating the top-level `README.md` and noting the package name, version, and license.

## Reporting bugs and asking questions

Before opening an issue, check the [existing issue tracker](../../issues) to avoid duplicates.

**To report a bug:**
- Use the `bug` label.
- Include the skill name and version.
- State what you expected to happen and what actually happened.
- Provide a minimal, self-contained reproduction: the exact command you ran, the agent output, and any relevant file contents.

**To ask a question:**
- Use the `question` label.
- Be specific about which skill or part of the system you are asking about.

Keep issues focused on a single topic. One issue, one problem.

## Pull request flow

1. Fork the repository and create a feature branch from `main`. Use the prefixes below:
   - `feat/` for new skills (e.g. `feat/add-upscale-skill`)
   - `fix/` for bug fixes or corrections to existing skills (e.g. `fix/upscale-broken-link`)
   - `chore/` for maintenance tasks (e.g. `chore/update-marketplace-json`)

2. Run `./setup` locally and verify the new or changed skill loads in your agent.

3. Run `python3 scripts/check-skill-compliance.py` and ensure all checks pass.

4. Write clear, scoped commits. One logical change per commit. Commit messages should complete the sentence "This commit will...".

5. Open a pull request with a title that names the skill and the action (e.g. `feat: add picsart-upscale skill`). In the PR description include:
   - What the skill does and why it is useful
   - Any limitations or known gaps
   - How you tested it locally

6. Every pull request requires at least **2 approvals** before merge. At least one approval must come from a repository code owner.

7. Merging is handled by the Picsart maintainer team to protect release stability. Do not merge your own PR.

8. Be kind and constructive in code review. Assume good intent.

## Release cycle

There is no fixed release cadence. Releases are published on demand after meaningful sets of changes accumulate.

Each release:
- Follows [Semantic Versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`).
- Is tagged in GitHub Releases, newest first.
- Has release notes listing all skills added or changed since the prior tag.

Bump the `VERSION` file in your PR only when your change is release-worthy (a new skill or a breaking change to an existing one). Typo fixes and doc-only updates do not require a version bump.

## License

`gen-ai-skills` is provided under the [MIT License](./LICENSE). By using, distributing, or contributing to this project, you agree to the terms and conditions of that license.   