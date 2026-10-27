<div align="center">

<img src="https://pcdn.picsart.com/cms-uploads/7391b2b3-8376-49f0-9374-73ce49941e03.gif" width="100%" alt="Picsart Video for AI agents: make movies, micro dramas, motion design, reels and tutorials">

# Picsart Video for AI agents

**Movies, micro dramas, motion design, reels and tutorials, made in the chat with your agent.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-8A2BE2)](https://agentskills.io/specification)
[![Claude Code plugin](https://img.shields.io/badge/Claude%20Code-plugin-D97757)](#install-the-plugin)
[![OpenClaw bundle](https://img.shields.io/badge/OpenClaw-bundle-555555)](#on-other-agents)

[**Install the plugin**](#install-the-plugin) · [What you can make](#what-you-can-make) · [Start a use case](#start-a-use-case) · [Skills library](#the-skills-library)

</div>

---

Picsart Video gives your AI agent a creative studio. Describe what you want, and the agent plans it with you, shows you a preview, and makes it with Picsart's AI models and editing tools. You need a Picsart account, and **every paid step is quoted before anything is charged.**

## Install the plugin

> [!TIP]
> **The Picsart plugin is the recommended way to install.** One install brings every skill below and connects the Picsart MCP server for you: nothing else to set up.

**In Claude Code**, run:

```
/plugin marketplace add PicsArt/gen-ai-skills
/plugin install picsart@picsart
```

Then ask *"Show me what Picsart can do."*: the plugin signs you in to Picsart and shows your credits.

### On other agents

| Agent | Install |
|---|---|
| **OpenClaw** | `openclaw plugins install picsart --marketplace https://github.com/PicsArt/gen-ai-skills`: the skills and the Picsart MCP server as one bundle. |
| **Codex, Cursor and any agent that reads skills** | `npx skills add PicsArt/gen-ai-skills` (or `gh skill install PicsArt/gen-ai-skills`), then add the MCP server below. |
| **Hermes** | `hermes skills tap add PicsArt/gen-ai-skills` |

Every command, the `./setup` script and how to update are in [INSTALL.md](./INSTALL.md).

<details>
<summary><b>Connect the MCP server directly</b> (Claude.ai, ChatGPT, or a skills-only install)</summary>

<br>

Without the plugin, add a custom connector (or an MCP server) with this URL, and sign in with your Picsart account when it asks:

```
https://api.picsart.com/gen-ai/mcp
```

Its name in [`.mcp.json`](./.mcp.json) is `picsart`. The plugin does this step for you.

</details>

## What you can make

<table>
<tr>
<td width="50%" valign="top">
<img src="https://pcdn.picsart.com/cms-uploads/3fe5a044-1d48-45b6-9fe2-3191e83b7c9e.gif" width="100%" alt="Genre clips from drama to documentary">

### Direct your own AI movie
Pick a genre. Call action. You’re the director.<br>
A short film from your story, with recurring characters and one look.

> *Make a short film from my story.*<br>
> `/picsart:movie-producer [story idea or script]`
</td>
<td width="50%" valign="top">
<img src="https://pcdn.picsart.com/cms-uploads/fed61e96-d343-4980-bc67-15f3dcfaba63.gif" width="100%" alt="Three episodes of a micro drama">

### Micro dramas, made to binge
Your series, cast and cliffhangers, episode by episode.<br>
A vertical drama series, pilot or episode with a recurring cast.

> *Make a short drama series from my idea.*<br>
> `/picsart:make-short-drama [series idea or the next episode]`
</td>
</tr>
<tr>
<td width="50%" valign="top">
<img src="https://pcdn.picsart.com/cms-uploads/3d85b8f7-bbe4-458e-bb1e-a7ddb3e3818f.gif" width="100%" alt="Shapes bouncing in a motion-designed loop">

### Design that moves
Turn text and logos into scroll-stopping loops.<br>
A Figma design or your own images, photos and logos become a motion-designed ad or reel.

> *Animate my design into a short motion video.*<br>
> `/picsart:animate-design [Figma link, design or assets]`
</td>
<td width="50%" valign="top">
<img src="https://pcdn.picsart.com/cms-uploads/0800919d-8288-4a77-977d-f980e6f6921d.gif" width="100%" alt="A lesson and how-to shorts cut from one screen recording">

### Tutorials from your screen
Lessons, how-to shorts and promos from one recording.<br>
A screen recording of your app or website becomes a step-by-step tutorial or a vertical promo.

> *Turn my screen recording into short how-to videos.*<br>
> `/picsart:make-screen-videos [screen recording and the video you want]`
</td>
</tr>
<tr>
<td width="50%" valign="top">
<img src="https://pcdn.picsart.com/cms-uploads/12a52d40-c0f2-4718-8051-7c2e8bc8f662.gif" width="100%" alt="A reference edit and the same edit with new footage">

### Same edit. Your footage.
Copy a video’s cuts, timing and motion, then drop in your own photos and text.<br>
A reference video rebuilt as an editable scene that moves and looks like it.

> *Recreate this reference video with my own photos and text.*<br>
> `/picsart:recreate-video [reference video, your photos and text]`
</td>
<td width="50%" valign="top">
<img src="https://pcdn.picsart.com/cms-uploads/a94eb191-7414-4073-8328-3c2727a4abf3.gif" width="100%" alt="Travel shots cut on the beat into a vertical reel">

### Drop footage. Get a reel.
Beat-synced cuts, transitions and music, done for you.<br>
An interview, podcast, vlog or clips cut into a tight vertical short, with captions and music if you want them.

> *Cut my footage into a 30-second vertical reel.*<br>
> `/picsart:cut-footage-into-reel [your footage and the length you want]`
</td>
</tr>
</table>

### And everyday edits

Ask in your own words: [`generate-media`](./skills/generate-media) and the Picsart tools handle these directly.

<table>
<tr>
<td width="33%" valign="top"><img src="https://pcdn.picsart.com/cms-uploads/0c50bcab-b47e-4f1f-ad93-9f201cb4bf0c.gif" width="100%" alt="A video edited with a prompt"><br><b>Create and edit videos</b><br>Create and edit videos with a prompt.</td>
<td width="33%" valign="top"><img src="https://pcdn.picsart.com/cms-uploads/ca71e12d-85eb-41c0-8678-e21273f07a21.gif" width="100%" alt="A portrait edited step by step"><br><b>Create and edit images</b><br>Restyle, cut out the background, or put it anywhere.</td>
<td width="33%" valign="top"><img src="https://pcdn.picsart.com/cms-uploads/f75797b4-fc8f-487b-a707-e58b868aaf2e.gif" width="100%" alt="An animated cartoon dog"><br><b>Bring your cartoon to life</b><br>Dream up a character. Watch it bounce, blink and wave.</td>
</tr>
<tr>
<td width="33%" valign="top"><img src="https://pcdn.picsart.com/cms-uploads/8b8e1af8-822f-4495-9e78-e7ac00888d57.gif" width="100%" alt="Word-by-word captions on a talking video"><br><b>Captions that pop</b><br>Auto-captions in bold styles, timed to every word.</td>
<td width="33%" valign="top"><img src="https://pcdn.picsart.com/cms-uploads/b5a7297d-e725-4e01-980b-e9590f21c9c2.gif" width="100%" alt="One clip in wide and vertical"><br><b>One video, every size</b><br>Reframe for vertical, square or wide. The subject stays in frame.</td>
<td width="33%" valign="top"><br><b>Speak every language</b><br>Natural voiceovers and lip-synced dubs.</td>
</tr>
</table>

## Start a use case

**In Claude Code**, type the use case's command and your brief:

```
/picsart:make-short-drama a heist series set in a night market
```

With the plugin the commands are namespaced (`/picsart:…`); a skills-only install names them without the prefix (`/make-short-drama`).

**Everywhere else**, open with the use case's starter prompt and add your brief. The agent picks the right use case from it.

| Use case | Starter prompt |
|---|---|
| [`get-started`](./skills/get-started) | *Show me what Picsart can do.* |
| [`generate-media`](./skills/generate-media) | *Make an image, a video or audio from my prompt.* |
| [`movie-producer`](./skills/movie-producer) | *Make a short film from my story.* |
| [`make-short-drama`](./skills/make-short-drama) | *Make a short drama series from my idea.* |
| [`animate-design`](./skills/animate-design) | *Animate my design into a short motion video.* |
| [`make-screen-videos`](./skills/make-screen-videos) | *Turn my screen recording into short how-to videos.* |
| [`recreate-video`](./skills/recreate-video) | *Recreate this reference video with my own photos and text.* |
| [`cut-footage-into-reel`](./skills/cut-footage-into-reel) | *Cut my footage into a 30-second vertical reel.* |

A use case loads other skills by name (every one reads [`picsart-video-rules`](./skills/picsart-video-rules) first), so install the whole plugin rather than a single use case.

## The skills library

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
| [`make-short-drama`](./skills/make-short-drama) | Make a vertical drama series, pilot or episode with a recurring cast. |
| [`movie-producer`](./skills/movie-producer) | Make a short narrative film from a story. |
| [`recreate-video`](./skills/recreate-video) | Rebuild a reference video as an editable animated scene that moves and looks like it. |

Skills the use cases load:

| Skill | Description |
|---|---|
| [`ai-presenter`](./skills/ai-presenter) | Put a generated presenter on screen and keep them honest. |
| [`background-music`](./skills/background-music) | Draft, generate and lay an instrumental music bed under a finished video's speech. |
| [`caption-decorations`](./skills/caption-decorations) | Author and validate scene caption decorations, choosing between measured procedural decoration presets and arbitrary scene artwork. |
| [`design-layer-import`](./skills/design-layer-import) | Bring a design or static assets into a scene as LAYERS, not flat frames, whenever they are going to move. |
| [`drama-series-writing`](./skills/drama-series-writing) | Write a drama series' bible, season arc and episode cliffhangers, from templates or the user's idea. |
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

## How it's built

<details>
<summary>Repository layout</summary>

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
├── .mcp.json            # the picsart MCP server, shared by every manifest
├── generated.json       # the skill folders that are generated, not hand-written
├── setup                # universal symlink installer
└── README.md
```

</details>

Each skill lives in its own directory under `skills/`. The directory name is the install name. The directory holds a `SKILL.md` that follows the open [Agent Skills specification](https://agentskills.io/specification): YAML frontmatter with `name` and `description`, then the instructions. The plugin manifests connect the MCP server through [`.mcp.json`](./.mcp.json).

## Contribute

More skills are welcome. See [CONTRIBUTING.md](./CONTRIBUTING.md) and the [Code of Conduct](./CODE_OF_CONDUCT.md).

## License

[MIT](./LICENSE) · Made by [Picsart](https://picsart.com)
