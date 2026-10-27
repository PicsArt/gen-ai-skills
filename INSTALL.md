# Install Picsart GenAI & Video

Skills shipped in this repo are listed in [README.md](./README.md). Each skill is a directory under `skills/` containing a `SKILL.md`.

Install them all. A use case such as `screen-promo` loads other skills by name (`video-core`, `layouts`, `screen-zoom` and more), so a use case installed on its own is missing its steps. Every option below except a single-skill Hermes install takes the whole set.

## Prerequisites

The skills call the Picsart gen-ai MCP server (`picsart`, `https://api.picsart.com/gen-ai/mcp`), declared in [`.mcp.json`](./.mcp.json). The plugin installs (Claude Code, Cursor, Codex, OpenClaw bundle) connect it for you; with a skills-only install, add that server to your agent yourself. You need a Picsart account: the server asks you to sign in the first time a step needs it, and every paid step is quoted before anything is charged.

## Option 1 — `npx skills` (recommended, cross-agent)

Works with Claude Code, Cursor, Codex, and any agent that picks up `~/.<agent>/skills/<name>/SKILL.md`. Requires Node.js.

```bash
npx skills add PicsArt/gen-ai-skills
```

The `skills` CLI auto-detects the host agent, walks the repo for directories containing `SKILL.md`, and installs each one to the agent's skills folder.

## Option 2 — `gh skill install`

GitHub CLI v2.90+ extension. Same coverage as `npx skills`.

```bash
gh skill install PicsArt/gen-ai-skills
```

## Option 3 — Claude Code marketplace

Claude Code only. Inside Claude Code:

```
/plugin marketplace add PicsArt/gen-ai-skills
/plugin install picsart@picsart
```

This pulls the plugin manifest from `.claude-plugin/marketplace.json` and registers the skills declared there.

## Option 3b — Codex plugin

Inside a terminal:

```bash
codex plugin marketplace add PicsArt/gen-ai-skills
codex plugin add picsart@picsart
```

Or open `/plugins` inside Codex and install **picsart** from the Picsart marketplace. This reads `.agents/plugins/marketplace.json` and the `.codex-plugin/plugin.json` manifest, and connects the Picsart MCP server for you.

## Option 4 — Setup script

Universal fallback. Clones the repo locally and symlinks each skill into the agent's expected directory.

```bash
git clone --depth 1 https://github.com/PicsArt/gen-ai-skills.git
cd gen-ai-skills
./setup
```

The script auto-detects Claude Code / Cursor / Codex (override with `--host <agent>`) and symlinks each skill subdirectory into place. Idempotent.

## Option 5 — Hermes Agent

For [Hermes Agent](https://hermes-agent.nousresearch.com/) by Nous Research. Install a single skill directly, or subscribe to the whole repo as a tap to browse and search all skills.

```bash
# Install one skill (note the skills/ path)
hermes skills install PicsArt/gen-ai-skills/skills/picsart-add-media

# Or add the repo as a tap (recommended — surfaces every skill in `hermes skills browse`)
hermes skills tap add PicsArt/gen-ai-skills
hermes skills search picsart
hermes skills install picsart-add-media
```

The tap layout uses `skills/` as the root path (Hermes' default), so adding the tap discovers every skill automatically. Skills install through Hermes' security scanner; trust level defaults to `community`.

## Option 6 — OpenClaw

For [OpenClaw](https://openclaw.ai/). Two ways to consume this repo.

Install the skills directly from GitHub:

```bash
# Active workspace only
openclaw skills install git:PicsArt/gen-ai-skills@main

# All agents (writes to ~/.openclaw/skills)
openclaw skills install git:PicsArt/gen-ai-skills@main --global
```

Or install the whole thing as a bundle (skills + the Picsart gen-ai MCP server), reading
this repo's Claude-style `marketplace.json`:

```bash
openclaw plugins marketplace list https://github.com/PicsArt/gen-ai-skills   # inspect first
openclaw plugins install picsart --marketplace https://github.com/PicsArt/gen-ai-skills
```

There is no `openclaw plugins marketplace add` step — point `install` directly at
the source. The MCP server's tools surface as `picsart__<tool>` under OpenClaw's
built-in `bundle-mcp` plugin.

Once published to ClawHub (see [OPENCLAW_PUBLISH_TODO.md](./OPENCLAW_PUBLISH_TODO.md)), skills install by slug instead:

```bash
openclaw skills install @PicsArt/<slug>
```

## Updating

| Method | Update command |
|---|---|
| `npx skills` | re-run `npx skills add PicsArt/gen-ai-skills` |
| `gh skill install` | `gh skill update PicsArt/gen-ai-skills` |
| Claude Code marketplace | `/plugin update picsart@picsart` |
| Codex plugin | `codex plugin marketplace upgrade picsart` |
| Setup script | `cd gen-ai-skills && git pull && ./setup` |
| Hermes Agent | `hermes skills update picsart-add-media` |
| OpenClaw | `openclaw skills update --all` (or `openclaw plugins update picsart`) |
