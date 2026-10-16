# Contributing

Thanks for your interest in contributing to `gen-ai-skills`. Contributions that add new skills, improve existing skill documentation, fix compliance issues, or strengthen tooling are all welcome. Please read this guide before opening a pull request.

## Repository structure

| Path | Description |
|---|---|
| `skills/` | One directory per skill, named in kebab-case |
| `scripts/` | Compliance checker, security scanner, and other dev utilities |
| `.claude-plugin/` | Plugin manifest (`marketplace.json`) consumed by the Claude agent harness |
| `.cursor-plugin/`, `.codex-plugin/`, `.agents/plugins/` | Equivalent plugin manifests for Cursor, Codex, and other OpenClaw-compatible agents |
| `.mcp.json` | The MCP server declaration (`picsart-gen-ai`), referenced by relative path from every plugin manifest above |
| `generated.json` | The skill folders that are generated rather than hand-written; see [Generated skills](#generated-skills) |
| `.github/workflows/` | CI workflows; `skill-compliance.yml` blocks merge on any compliance failure |
| `VERSION` | Single source of truth for the current release version |

## MCP servers

`.mcp.json` at the repo root is the one place MCP servers are declared. `.claude-plugin/plugin.json`,
`.cursor-plugin/plugin.json`, and `.codex-plugin/plugin.json` all point at it via
`"mcpServers": "./.mcp.json"` — don't inline a server config into any of those manifests, and don't
duplicate an entry's JSON body elsewhere (a skill's `SKILL.md` may *document* how to reach a server, but
should link to or mirror `.mcp.json`, not fork it).

The one server is `picsart-gen-ai`; skills here use its tools and no other server's. Keep each entry
to transport and URL only — `type` and `url`. Do not add client-specific auth
configuration (e.g. Claude Code's `oauth` block): the same `.mcp.json` is read by Claude Code, Cursor,
and Codex, and a server that implements the MCP authorization spec correctly — free tools answering
anonymously, gated tools returning a `401` with a `WWW-Authenticate` challenge — needs nothing more than
that to work across all of them. Before removing what looks like a "duplicate" server, confirm by
endpoint (not name) whether it's actually redundant with something every user already has, or whether
it's the only route external users have to that server — see PR #10 for a case where that distinction
was gotten wrong the first time.

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

2. Add a `SKILL.md` at the root of that directory. It follows the open
   [Agent Skills specification](https://agentskills.io/specification): `name` and `description` are
   required, and the body is free-form Markdown.

   ```markdown
   ---
   name: picsart-upscale
   description: Upscale an image with the Picsart gen-ai MCP. Use when the user wants a photo larger or sharper.
   license: MIT
   ---

   # Picsart Upscale

   The instructions, in whatever sections help the agent most.
   ```

   Optional fields: `license`, `compatibility`, `metadata`, `allowed-tools` from the spec. Hosts'
   own fields are allowed but never required: Hermes Agent's `version`, `author`, `platforms` and
   `metadata.hermes`, and Claude Code's `user-invocable`, `disable-model-invocation`,
   `argument-hint` and `model`.

3. Put supporting files inside the skill's own directory:
   - `references/` — supplementary docs (FLAGS, EXAMPLES, etc.)
   - `scripts/` — helper scripts the skill invokes
   - `templates/` — output templates
   - `assets/` — fixtures, sample images, etc.

4. No manifest change is needed: every plugin manifest reads the whole `skills/` folder. Add a row for
   the skill to the README's hand-written table.

5. Bump the `version` in `VERSION` if this is a release-worthy change.

## Generated skills

The folders listed in [`generated.json`](./generated.json) are generated, and the next generation
overwrites them. Don't edit them in a pull request here; open an issue describing the change
instead. A hand-written skill must not reuse a generated folder's name.

## Compliance rules (CI-enforced)

Every skill must pass `python3 scripts/check-skill-compliance.py` before merge. It checks the open
[Agent Skills specification](https://agentskills.io/specification) and Anthropic's
[skill-authoring rules](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices),
which are what Claude Code, Codex, Cursor and OpenClaw read.

Errors block the merge:

| Rule | What it checks |
|---|---|
| **name** | Required. 1–64 lowercase letters, digits and single hyphens; equals the folder name; no "anthropic" or "claude". |
| **description** | Required, 1–1024 characters. Say what the skill does and when to use it, with the words a user would say: the agent picks a skill from its description alone. |
| **xml-tags** | No XML tag in `name` or `description`; hosts refuse the upload. |
| **fields** | `compatibility` is a string of at most 500 characters, `metadata` is a mapping, `allowed-tools` is a string. |
| **links** | Every relative link in the skill's Markdown files resolves. |
| **paths** | File paths use forward slashes. |

Warnings are printed but never block:

| Rule | What it checks |
|---|---|
| **size** | `SKILL.md` stays under 500 lines; move detail into `references/`. |
| **references** | References sit directly under `references/`, one level deep. |
| **reference-toc** | A reference over 100 lines opens with a `## Contents` list of its sections. |
| **leaves-skill** | No link out of the skill's folder; each skill installs on its own, so name another skill instead. |
| **unknown-field** | A frontmatter field that is neither in the spec nor a known host extension. |

Run the check locally:

```bash
python3 scripts/check-skill-compliance.py            # all skills
python3 scripts/check-skill-compliance.py skills/foo # one skill
python3 -m unittest discover -s scripts -p 'test_*.py'  # the checker's own tests
```

The CI workflow (`.github/workflows/skill-compliance.yml`) runs the same check on every PR and blocks merge on failure.

## Skill conventions

- One skill = one directory under `skills/`. Don't nest skills inside skills.
- `description` is the single most important field — agents use it to decide whether to invoke the skill. Say what the skill does and when to use it, in the words a user would say.
- Keep `SKILL.md` self-contained. Long references go in `references/` and link from `SKILL.md`.
- Don't shell out to anything that requires interactive input.
- Name MCP tools by their exact server names (`picsart_media_upload`, `picsart_generate`, ...), and only tools the gen-ai MCP serves.
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