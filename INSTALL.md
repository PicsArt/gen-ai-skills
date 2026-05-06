# Install Picsart Gen-AI Skills

Skills shipped in this repo are listed in [README.md](./README.md). Each skill is a top-level directory containing a `SKILL.md` manifest.

## Prerequisites

Most skills assume the Picsart `gen-ai` CLI is installed and authenticated. See the per-skill `SKILL.md` for the exact commands a skill expects.

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

## Option 4 — Setup script

Universal fallback. Clones the repo locally and symlinks each skill into the agent's expected directory.

```bash
git clone --depth 1 https://github.com/PicsArt/gen-ai-skills.git
cd gen-ai-skills
./setup
```

The script auto-detects Claude Code / Cursor / Codex (override with `--host <agent>`) and symlinks each skill subdirectory into place. Idempotent.

## Updating

| Method | Update command |
|---|---|
| `npx skills` | re-run `npx skills add PicsArt/gen-ai-skills` |
| `gh skill install` | `gh skill update PicsArt/gen-ai-skills` |
| Claude Code marketplace | `/plugin update picsart@picsart` |
| Setup script | `cd gen-ai-skills && git pull && ./setup` |
