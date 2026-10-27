<div align="center">

<img src="./assets/logo.svg" width="72" height="72" alt="Picsart">

# Picsart Video for AI agents

**Movies, micro dramas, motion design, reels and tutorials, made in the chat with your agent.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-8A2BE2)](https://agentskills.io/specification)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-D97757)](#claude-code)
[![Codex](https://img.shields.io/badge/Codex-plugin-111111)](#codex-cursor-openclaw-and-hermes)
[![Cursor](https://img.shields.io/badge/Cursor-plugin-555555)](#codex-cursor-openclaw-and-hermes)

<img src="https://pcdn.picsart.com/cms-uploads/cd0a4ff1-93d3-4552-9e36-cf86d9067404.webp" height="120" alt="A rider on a desert road">
<img src="https://pcdn.picsart.com/cms-uploads/9bdc2bbf-e3fd-4105-8c5b-aa28f33714af.webp" height="120" alt="A micro drama episode">
<img src="https://pcdn.picsart.com/cms-uploads/c1adcb08-a248-4444-a788-d019a747245d.webp" height="120" alt="An animated cartoon character">
<img src="https://pcdn.picsart.com/cms-uploads/15fea4c2-5249-4041-b409-129d19f9ba5f.webp" height="120" alt="A photo promo made from a screen recording">

[What you can make](#what-you-can-make) · [Get started](#get-started-in-a-minute) · [Start a use case](#start-a-use-case) · [Skills library](#the-skills-library)

</div>

---

Picsart Video gives your AI agent a creative studio. Describe what you want, and the agent plans it with you, shows you a preview, and makes it with Picsart's AI models and editing tools, all through Picsart's gen-ai MCP server (`picsart`, `https://api.picsart.com/gen-ai/mcp`).

It ships as a plugin for **Claude Code, Codex and Cursor**, and the skills work in any agent that reads `SKILL.md` files. You need a Picsart account, and **every paid step is quoted before anything is charged.**

## What you can make

<table>
<tr>
<td width="50%" valign="top">
<img src="https://pcdn.picsart.com/cms-uploads/08be72c8-acdc-4411-826d-8a0d78c67460.webp" width="100%" alt="A cinematic AI movie shot">

### Direct your own AI movie
Pick a genre. Call action. You’re the director.<br>
A short film from your story, with recurring characters and one look.

> *Make a short film from my story.*<br>
> `/movie-producer [story idea or script]`
</td>
<td width="50%" valign="top">
<img src="https://pcdn.picsart.com/cms-uploads/48633962-fa38-48d6-969b-0d529c0b2121.webp" width="100%" alt="A lesson cut from a screen recording">

### Tutorials from your screen
Lessons, how-to shorts and promos from one recording.<br>
A screen recording of your app or website becomes a step-by-step tutorial or a vertical promo.

> *Turn my screen recording into short how-to videos.*<br>
> `/make-screen-videos [screen recording and the video you want]`
</td>
</tr>
<tr>
<td width="50%" valign="top">
<p align="center">
<img src="https://pcdn.picsart.com/cms-uploads/9bdc2bbf-e3fd-4105-8c5b-aa28f33714af.webp" width="31%" alt="Micro drama, episode still">
<img src="https://pcdn.picsart.com/cms-uploads/fcafb38a-4bfb-4abb-96fc-0e7e7266950f.webp" width="31%" alt="Micro drama, episode 1">
<img src="https://pcdn.picsart.com/cms-uploads/7b119b1e-5116-4df3-9fa7-ca9f5d3ad34e.webp" width="31%" alt="Micro drama, episode 3">
</p>

### Micro dramas, made to binge
Your series, cast and cliffhangers, episode by episode.<br>
A vertical drama series, pilot or episode with a recurring cast.

> *Make a short drama series from my idea.*<br>
> `/make-short-drama [series idea or the next episode]`
</td>
<td width="50%" valign="top">
<p align="center">
<img src="https://pcdn.picsart.com/cms-uploads/695e7b7e-79ac-4b66-97c4-8fbec301277b.webp" width="40%" alt="Reference edit">
<img src="https://pcdn.picsart.com/cms-uploads/ce009f3c-5bde-4646-8846-9b84f1394fba.webp" width="40%" alt="The same edit with new photos">
</p>

### Same edit. Your footage.
Copy a video’s cuts, timing and motion, then drop in your own photos and text.<br>
A reference video rebuilt as an editable scene that moves and looks like it.

> *Recreate this reference video with my own photos and text.*<br>
> `/recreate-video [reference video, your photos and text]`
</td>
</tr>
<tr>
<td width="50%" valign="top">
<img src="https://pcdn.picsart.com/cms-uploads/407591f8-5766-441e-a729-b00ad5d924d0.webp" width="100%" alt="A motion-designed loop">

### Design that moves
Turn text and logos into scroll-stopping loops.<br>
A Figma design or your own images, photos and logos become a motion-designed ad or reel.

> *Animate my design into a short motion video.*<br>
> `/animate-design [Figma link, design or assets]`
</td>
<td width="50%" valign="top">
<p align="center">
<img src="https://pcdn.picsart.com/cms-uploads/fe93e265-7ea6-4ed1-bf5d-dd26084802fa.webp" width="21%" alt="Reel shot: beach">
<img src="https://pcdn.picsart.com/cms-uploads/1a3566ac-b7bf-4369-ae5c-04d1781de03f.webp" width="21%" alt="Reel shot: mountain">
<img src="https://pcdn.picsart.com/cms-uploads/33e27213-2231-4ad6-a174-31929bde00f2.webp" width="21%" alt="Reel shot: street">
<img src="https://pcdn.picsart.com/cms-uploads/cb0b4ef2-1dc0-43b1-87c6-0ccef9f2b396.webp" width="21%" alt="Reel shot: train">
</p>

### Drop footage. Get a reel.
Beat-synced cuts, transitions and music, done for you.<br>
An interview, podcast, vlog or clips cut into a tight vertical short, with captions and music if you want them.

> *Cut my footage into a 30-second vertical reel.*<br>
> `/cut-footage-into-reel [your footage and the length you want]`
</td>
</tr>
</table>

### And everyday edits

Ask for these in your own words. [`generate-media`](./skills/generate-media) and the Picsart tools handle them directly.

| | What you get |
|---|---|
| **Create and edit videos** | Create and edit videos with a prompt. |
| **Create and edit images** | Create and edit images with a prompt: remove or replace a background, enhance, upscale or vectorize. |
| **Bring your cartoon to life** | Dream up a character. Watch it bounce, blink and wave. |
| **Captions that pop** | Auto-captions in bold styles, timed to every word. |
| **Speak every language** | Natural voiceovers and lip-synced dubs. |
| **One video, every size** | Reframe for vertical, square or wide. The subject stays in frame. |

## Get started in a minute

### Claude Code

Inside Claude Code:

```
/plugin marketplace add PicsArt/gen-ai-skills
/plugin install picsart@picsart
```

The plugin connects the Picsart MCP server for you. Then ask *"Show me what Picsart can do."* to sign in and check your credits.

### Any agent that reads skills

```bash
npx skills add PicsArt/gen-ai-skills
```

The `skills` CLI detects your agent and installs every skill into its skills folder. `gh skill install PicsArt/gen-ai-skills` works the same way. With a skills-only install, add the MCP server below to your agent yourself.

### Codex, Cursor, OpenClaw and Hermes

Codex and Cursor take the skills through `npx skills`, `gh skill install` or the `./setup` script; OpenClaw installs the skills or the whole bundle with the MCP server; Hermes adds the repo as a tap. Every command, and how to update, is in [INSTALL.md](./INSTALL.md).

### Claude.ai, ChatGPT and other MCP clients

Add a custom connector with the Picsart MCP server URL:

```
https://api.picsart.com/gen-ai/mcp
```

Sign in with your Picsart account when the connector asks. Then start with any of the prompts below.

## Start a use case

**In Claude Code**, type the use case's command followed by your brief:

```
/make-short-drama a heist series set in a night market
```

Installed as the plugin, the commands are namespaced: `/picsart:make-short-drama`.

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

A use case loads other skills by name (every one reads [`picsart-video-rules`](./skills/picsart-video-rules) first), so install the whole repo rather than a single use case.

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
