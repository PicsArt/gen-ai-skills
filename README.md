# gen-ai-skills

Shared skills for Picsart's gen-ai MCP server (`picsart-gen-ai`, `https://api.picsart.com/gen-ai/mcp`), packaged as a plugin for Claude Code, Cursor and Codex.

Skills here are consumable by any agent that reads `SKILL.md` files. Every skill uses the gen-ai MCP server's tools; the plugin manifests connect it through [`.mcp.json`](./.mcp.json).

## Install

```bash
npx skills add PicsArt/gen-ai-skills
```

See [INSTALL.md](./INSTALL.md) for `gh skill install`, the Claude Code marketplace, and the `./setup` script alternatives.

## Repository layout

```
gen-ai-skills/
├── .claude-plugin/      # Claude Code plugin + marketplace manifests
├── .codex-plugin/       # Codex plugin manifest
├── .cursor-plugin/      # Cursor plugin manifest
├── .github/workflows/   # CI (security scan, lint)
├── scripts/             # Repo tooling (scan-skill.py, ...)
├── skills/              # All skills live here, one directory each
│   ├── picsart-add-media/
│   │   └── SKILL.md
│   ├── video-prompt-engineer/
│   │   └── SKILL.md
│   └── ...
├── INSTALL.md
├── CONTRIBUTING.md
├── VERSION
├── .mcp.json            # the picsart-gen-ai MCP server, shared by every manifest
├── setup                # universal symlink installer
└── README.md
```

Each skill lives in its own directory under `skills/`. The directory name is the install name. The directory must contain a `SKILL.md` with YAML frontmatter (`name`, `description`, optional `argument-hint`, optional `allowed-tools`) followed by the skill body.

## Skills

| Skill | Description |
|---|---|
| [`picsart-add-media`](./skills/picsart-add-media) | Turn the user's own files into hosted URLs with the gen-ai MCP's upload tools. |
| [`style-guide-builder`](./skills/style-guide-builder) | Build a reusable visual style guide from reference images. |
| [`video-prompt-engineer`](./skills/video-prompt-engineer) | Write and fix prompts for AI video generation. |

More skills are welcome — see [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

[MIT](./LICENSE)
