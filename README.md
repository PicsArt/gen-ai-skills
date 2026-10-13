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

Use cases, the entry points a user asks for:

| Skill | Description |
|---|---|
| [`motion`](./skills/motion) | Turn static material into a real motion-designed video. |
| [`picsart-onboarding`](./skills/picsart-onboarding) | Get started with Picsart Video. |
| [`screen-promo`](./skills/screen-promo) | Turn a screen recording of an app or website into a short vertical promo. |
| [`screen-tutorial`](./skills/screen-tutorial) | Turn a screen recording of an app or website into a 16:9 step-by-step tutorial with chapters. |
| [`short-film`](./skills/short-film) | Make a short narrative film from a story. |
| [`short-reel-maker`](./skills/short-reel-maker) | Cut the user's own footage into a tight vertical short for TikTok, Reels or Shorts. |

Skills the use cases load:

| Skill | Description |
|---|---|
| [`captions`](./skills/captions) | Put spoken words on screen from the transcript. |
| [`evaluate`](./skills/evaluate) | Check a scene before the user sees it. |
| [`film-cast`](./skills/film-cast) | Make a film's people, props and places consistent on pictures. |
| [`film-edit`](./skills/film-edit) | Cut a film's accepted takes into one scene. |
| [`film-finishing`](./skills/film-finishing) | Finish a film after picture lock. |
| [`film-shots`](./skills/film-shots) | Shoot a film's shots as runs. |
| [`film-story`](./skills/film-story) | Write a short film's story and break it down. |
| [`layouts`](./skills/layouts) | Lay a screen recording out in a 1080x1920 vertical frame. |
| [`media-analysis`](./skills/media-analysis) | Watch the user's own talking footage and turn it into facts you can build on. |
| [`motion-design`](./skills/motion-design) | The craft of adding motion to any MP Scene, whatever the video. |
| [`motion-import`](./skills/motion-import) | Bring a design or static assets into a scene as LAYERS, not flat frames, whenever they are going to move. |
| [`open-picsart`](./skills/open-picsart) | Open Picsart beside the conversation, where the host can. |
| [`music-bed`](./skills/music-bed) | Draft, generate and lay an instrumental music bed under a finished video's speech. |
| [`reframe`](./skills/reframe) | Put the user's own footage in a frame of another shape. |
| [`scene-compose`](./skills/scene-compose) | Build and edit an MP Scene with the scene tools. |
| [`screen-analysis`](./skills/screen-analysis) | Read a screen recording from its pixels. |
| [`screen-zoom`](./skills/screen-zoom) | The house zoom for screen footage in a panel. |
| [`speech-cuts`](./skills/speech-cuts) | Choose the moments of talking footage worth keeping and cut them so no one is clipped mid-sentence. |
| [`talking-head`](./skills/talking-head) | Put a generated presenter on screen and keep them honest. |
| [`video-core`](./skills/video-core) | The rules every Picsart Video use case follows. |
| [`voice-over`](./skills/voice-over) | Generate a voice-over from written lines. |

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
