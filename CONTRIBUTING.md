# Contributing

Thanks for your interest in contributing to `gen-ai-skills`. Contributions that add new skills, improve existing skill documentation, fix compliance issues, or strengthen tooling are all welcome. Please read this guide before opening a pull request.

## Repository structure

| Path | Description |
|---|---|
| `skills/` | One directory per skill, named in kebab-case |
| `scripts/` | Compliance checker, `picsart-mcp-tools.json` tool allowlist, normalizer, and other dev utilities |
| `tests/` | `unittest` suite for the compliance checker |
| `.claude-plugin/` | Plugin manifest (`marketplace.json`) consumed by the Claude agent harness |
| `.cursor-plugin/`, `.codex-plugin/`, `.agents/plugins/` | Equivalent plugin manifests for Cursor, Codex, and other OpenClaw-compatible agents |
| `.mcp.json` | The single MCP server declaration, referenced by relative path from every plugin manifest above |
| `.github/workflows/` | CI workflows; `skill-compliance.yml` blocks merge on any compliance failure |
| `VERSION` | Single source of truth for the current release version |

## MCP servers

`.mcp.json` at the repo root is the one place MCP servers are declared, and it declares exactly one:
`picsart`, at `https://api.picsart.com/gen-ai/mcp`. `.claude-plugin/plugin.json`,
`.cursor-plugin/plugin.json`, and `.codex-plugin/plugin.json` all point at it via
`"mcpServers": "./.mcp.json"` — don't inline a server config into any of those manifests, and don't
duplicate an entry's JSON body elsewhere (a skill's `SKILL.md` may *document* how to reach a server, but
should link to or mirror `.mcp.json`, not fork it).

Keep each entry to transport and URL only — `type` and `url`, nothing else. No `headers`, no API keys,
and no client-specific auth configuration (e.g. Claude Code's `oauth` block): the same `.mcp.json` is
read by Claude Code, Cursor, and Codex. The server implements the MCP authorization spec — an
unauthenticated request gets a `401` whose `WWW-Authenticate` header points at the server's
protected-resource metadata — so an OAuth-capable host discovers the sign-in flow from that and has the
user sign in on first connect, with no extra config. Before adding, removing, or renaming a server
entry, confirm by endpoint (not name) what it actually serves and who depends on it — see PR #10 for a
case where judging a server "duplicate" by name went wrong the first time.

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
   description: Upscale a Picsart image to a higher resolution. Use when an accepted image needs more pixels for print or large displays. Not for generative edits; use picsart-image-edit.
   version: 1.0.0
   author: Picsart
   license: MIT
   platforms: [macos, linux, windows]
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

4. Link shared Picsart references instead of copying them. They live in the `picsart-workflows` hub: link them as `../picsart-workflows/references/<file>` from a `SKILL.md`, or `../../picsart-workflows/references/<file>` from inside your skill's `references/`.

   No manifest entry is needed: skills are discovered from `skills/`. `.claude-plugin/marketplace.json` has no skills array.

5. Bump the `version` in `VERSION` if this is a release-worthy change.

## Compliance rules (CI-enforced)

Every skill must pass `python3 scripts/check-skill-compliance.py` before merge. For each `skills/<name>/SKILL.md` it checks:

| Rule | What it checks |
|---|---|
| **Full frontmatter** | `name`, `description`, `version`, `author`, `license`, `platforms`, and `metadata.hermes.{category, tags}` are all present. |
| **description ≤ 1024 chars** | Present and non-empty. Say what the skill does, when to use it, and what it is not for — and keep it tight. |
| **name** | Equals the folder name, ≤ 64 chars, matches `^[a-z0-9]+(-[a-z0-9]+)*$`. |
| **SKILL.md ≤ 500 lines** | Long material goes in `references/`. |
| **Canonical section order** | `## When to Use` → `## Prerequisites` → `## How to Run` → `## Quick Reference` → `## Procedure` → `## Pitfalls` → `## Verification`, all seven present. Extras allowed after the canonical seven. |
| **Links resolve inside `skills/`** | Every relative link in every `.md` file of the skill (outside fenced code blocks) resolves to an existing file and does not escape `skills/`. |
| **Every file reachable** | Every file in the skill directory is reachable from `SKILL.md` by following relative links through `.md` files. Dotfiles are exempt, but the single-surface guard still scans them. |
| **No symlinks** | No symlinked files or directories in the skill, and neither the skill directory nor `skills/` itself is a symlink. |
| **Single-surface guard** | No file in the skill contains (case-insensitive) `mcp.picsart.io`, `api.picsart.io`, `video-api.picsart.io`, `vd-api.picsart.io`, `genai-api.picsart.io`, `picsart-gen-ai`, `PICSART_API_KEY`, `X-Picsart-API-Key`, `mcp__codex_apps__`, `/Users/`, `genai_list_presets`, `genai_get_preset`, `genai_run_preset`, `mp_upload`, `not yet served`, `research/`, `pa-ai-models`, `SPEC.md`, or `@picsart/replay`. |
| **Tool names served** | Every `picsart_*` tool name in any file of the skill (any case; all-caps `PICSART_*` environment variables excepted) is in `scripts/picsart-mcp-tools.json`, a flat list of the tools `https://api.picsart.com/gen-ai/mcp` serves. A glob such as `picsart_media_*` must match at least one listed name. Skills name only served tools. Regenerate the list from an authenticated `tools/list` of the endpoint. |

Run the check and its tests locally:

```bash
python3 scripts/check-skill-compliance.py            # all skills
python3 scripts/check-skill-compliance.py skills/foo # one skill
python3 -m unittest discover -s tests                # checker test suite
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

3. Run `python3 scripts/check-skill-compliance.py` and `python3 -m unittest discover -s tests` and ensure both pass.

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