# gen-ai-skills

Shared skills, prompts, and tooling for working with Picsart's `gen-ai` CLI and related generative-AI workflows.

This repository is a public, community-friendly home for reusable skills and recipes. It is **not** the source of the `gen-ai` CLI itself — it complements it.

Skills here are consumable by any agent that reads `SKILL.md` files: Claude Code, Cursor, Codex, and others.

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
├── <skill-name>/        # one directory per skill, each with a SKILL.md
│   └── SKILL.md
├── INSTALL.md
├── CONTRIBUTING.md
├── VERSION
├── setup                # universal symlink installer
└── README.md
```

Each skill lives in its own top-level directory. The directory name is the install name. The directory must contain a `SKILL.md` with YAML frontmatter (`name`, `description`, optional `argument-hint`, optional `allowed-tools`) followed by the skill body.

## Status

Early scaffold. Skills will be added by contributors — see [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

[MIT](./LICENSE)
