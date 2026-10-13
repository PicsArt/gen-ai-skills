# gen-ai-skills

Picsart AI video skills for Picsart's gen-ai MCP server (`picsart-gen-ai`, `https://api.picsart.com/gen-ai/mcp`), packaged as a plugin for Claude Code, Cursor and Codex.

- Turn a screen recording into a short vertical promo or a step-by-step tutorial.
- Cut an interview, podcast or vlog into a tight vertical reel, with captions and music if wanted.
- Turn a design or your own images into a motion-designed ad.
- Make a short film from a story, with recurring characters and one look.

Every paid step is quoted before anything is charged. The skills work in any agent that reads `SKILL.md` files; the plugin manifests connect the MCP server through [`.mcp.json`](./.mcp.json). You need a Picsart account.

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
├── generated.json       # the skill folders that are generated, not hand-written
├── setup                # universal symlink installer
└── README.md
```

Each skill lives in its own directory under `skills/`. The directory name is the install name. The directory holds a `SKILL.md` that follows the open [Agent Skills specification](https://agentskills.io/specification): YAML frontmatter with `name` and `description`, then the instructions.

A use case loads other skills by name (every one reads `video-core` first), so install the whole repo rather than a single use case.

## Skills

### Video

Generated; [`generated.json`](./generated.json) lists them. Don't edit these folders by hand: the next generation overwrites them.

<!-- generated-skills:start -->

_The generated skills arrive in their own pull request._

<!-- generated-skills:end -->

### Hand-written

| Skill | Description |
|---|---|
| [`picsart-add-media`](./skills/picsart-add-media) | Turn the user's own files into hosted URLs with the gen-ai MCP's upload tools. |
| [`style-guide-builder`](./skills/style-guide-builder) | Build a reusable visual style guide from reference images. |
| [`video-prompt-engineer`](./skills/video-prompt-engineer) | Write and fix prompts for AI video generation. |

More skills are welcome — see [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

[MIT](./LICENSE)
