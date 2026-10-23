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
| [`animate-design`](./skills/animate-design) | Turn static material into a real motion-designed video. |
| [`cut-footage-into-reel`](./skills/cut-footage-into-reel) | Cut the user's own footage. |
| [`generate-media`](./skills/generate-media) | Make an image, a video, a voice line, a sound or a song from a prompt, or edit a picture. |
| [`get-started`](./skills/get-started) | Get started with Picsart Video. |
| [`make-screen-videos`](./skills/make-screen-videos) | Turn a screen recording of an app or website into finished videos. |
| [`movie-producer`](./skills/movie-producer) | Make a short narrative film from a story. |
| [`recreate-video`](./skills/recreate-video) | Rebuild a reference video as an editable animated scene that moves and looks like it. |

Skills the use cases load:

| Skill | Description |
|---|---|
| [`ai-presenter`](./skills/ai-presenter) | Put a generated presenter on screen and keep them honest. |
| [`background-music`](./skills/background-music) | Draft, generate and lay an instrumental music bed under a finished video's speech. |
| [`caption-decorations`](./skills/caption-decorations) | Author and validate scene caption decorations, choosing between measured procedural decoration presets and arbitrary scene artwork. |
| [`design-layer-import`](./skills/design-layer-import) | Bring a design or static assets into a scene as LAYERS, not flat frames, whenever they are going to move. |
| [`film-cast-design`](./skills/film-cast-design) | Make a film's people, props and places consistent on pictures. |
| [`film-cutting`](./skills/film-cutting) | Cut a film's accepted takes into one scene. |
| [`film-finishing`](./skills/film-finishing) | Finish a film after picture lock. |
| [`film-shot-generation`](./skills/film-shot-generation) | Shoot a film's shots as runs. |
| [`film-story-writing`](./skills/film-story-writing) | Write a short film's story and break it down. |
| [`footage-analysis`](./skills/footage-analysis) | Watch the user's own talking footage and turn it into facts you can build on. |
| [`footage-reframing`](./skills/footage-reframing) | Put the user's own footage in a frame of another shape. |
| [`motion-design-craft`](./skills/motion-design-craft) | The craft of adding motion to any scene, whatever the video. |
| [`motion-tracking-from-video`](./skills/motion-tracking-from-video) | Measure what objects visibly do in a video. |
| [`open-picsart-app`](./skills/open-picsart-app) | Open Picsart beside the conversation. |
| [`photo-slideshow`](./skills/photo-slideshow) | Build a photo promo or slideshow in a scene. |
| [`picsart-video-rules`](./skills/picsart-video-rules) | The rules every Picsart Video use case follows. |
| [`quality-review`](./skills/quality-review) | Check work before the user sees it. |
| [`realistic-color-grade`](./skills/realistic-color-grade) | Make a video's colours look more realistic and natural with the ai_realism look. |
| [`reference-fragment-matching`](./skills/reference-fragment-matching) | Rebuild a reference video as a scene one fragment at a time. |
| [`resting-frame-rules`](./skills/resting-frame-rules) | Keep every element whole or gone whenever motion stops. |
| [`retention-hooks`](./skills/retention-hooks) | Keep a short video watched to the end with open loops. |
| [`scene-building-basics`](./skills/scene-building-basics) | Build and edit a scene with the scene tools. |
| [`screen-recording-analysis`](./skills/screen-recording-analysis) | Read a screen recording from its pixels. |
| [`screen-recording-layouts`](./skills/screen-recording-layouts) | Lay a screen recording out in a 1080x1920 vertical frame or a 1920x1080 landscape one. |
| [`screen-recording-zoom`](./skills/screen-recording-zoom) | The house zoom for screen footage in a panel. |
| [`screen-ui-redesign`](./skills/screen-ui-redesign) | Recreate the screens of a recording as designed motion UI. |
| [`speech-aware-cutting`](./skills/speech-aware-cutting) | Choose the moments of talking footage worth keeping and cut them so no one is clipped mid-sentence. |
| [`spoken-captions`](./skills/spoken-captions) | Put spoken words on screen from the transcript. |
| [`visual-style`](./skills/visual-style) | A video's style, chosen by eye and kept. |
| [`voice-over-generation`](./skills/voice-over-generation) | Generate a voice-over from written lines. |

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
