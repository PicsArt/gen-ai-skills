# gen-ai-skills

Shared skills, prompts, and tooling for working with Picsart's generative-AI stack: the `picsart` MCP server and the `gen-ai` CLI.

This repository is a public, community-friendly home for reusable skills and recipes. It is **not** the source of the `gen-ai` CLI or the `picsart` MCP server itself — it complements them.

Skills here are consumable by any agent that reads `SKILL.md` files: Claude Code, Cursor, Codex, and others.

## Install

```bash
npx skills add PicsArt/gen-ai-skills
```

The `picsart-*` skills use the bundled `picsart` MCP server (`https://api.picsart.com/gen-ai/mcp`, declared in [`.mcp.json`](./.mcp.json)) and sign in with OAuth on first connect.

See [INSTALL.md](./INSTALL.md) for `gh skill install`, the Claude Code marketplace, and the `./setup` script alternatives.

## Repository layout

```
gen-ai-skills/
├── .claude-plugin/      # Claude Code plugin + marketplace manifests
├── .codex-plugin/       # Codex plugin manifest
├── .cursor-plugin/      # Cursor plugin manifest
├── .github/workflows/   # CI (security scan, skill compliance)
├── .mcp.json            # the single `picsart` MCP server declaration
├── scripts/             # Repo tooling (check-skill-compliance.py, picsart-mcp-tools.json, ...)
├── skills/              # All skills live here, one directory each
│   ├── gen-ai-use/
│   │   └── SKILL.md
│   ├── picsart-workflows/
│   │   ├── SKILL.md
│   │   └── references/  # shared Picsart references linked by every picsart-* skill
│   └── ...
├── tests/               # unittest suite for the compliance checker
├── INSTALL.md
├── CONTRIBUTING.md
├── VERSION
├── setup                # universal symlink installer
└── README.md
```

Each skill lives in its own directory under `skills/`. The directory name is the install name. The directory must contain a `SKILL.md` with YAML frontmatter followed by the skill body; see [CONTRIBUTING.md](./CONTRIBUTING.md) for the required fields and sections. Shared Picsart references (interface map, Drive library, media production, remote resources, host conventions) live in [`skills/picsart-workflows/references/`](./skills/picsart-workflows/references/).

## Skills

This bundle ships **68 skills**. Several skills are mode-routers — one entry point with `references/modes/` for variants — to keep the catalog small and trigger-friendly.

### Core CLI

| Skill | Description |
|---|---|
| [`gen-ai-use`](./skills/gen-ai-use) | Generate AI images, videos, audio via the Picsart `gen-ai` CLI. |
| [`gen-ai-persona-creation`](./skills/gen-ai-persona-creation) | Create AI influencers, branded characters, or pet personas from a brief or reference. |
| [`gen-ai-explainer`](./skills/gen-ai-explainer) | Produce a short animated explainer video: research → script → assets → render. |

### Prompts and style

| Skill | Description |
|---|---|
| [`style-guide-builder`](./skills/style-guide-builder) | Build a reusable visual style guide from reference images. |
| [`video-prompt-engineer`](./skills/video-prompt-engineer) | Write and fix prompts for AI video generation. |

### MCP

| Skill | Description |
|---|---|
| [`picsart-add-media`](./skills/picsart-add-media) | Turn a user's local file into a hosted URL via the `picsart` MCP server's upload widget. |

### Multi-mode skills

| Skill | Description |
|---|---|
| [`product-photo-studio`](./skills/product-photo-studio) | Transform product photos. Modes: bulk-restyle, compose, seasonal, variants, reshoot, mockups. |
| [`text-to-visual`](./skills/text-to-visual) | Generate visuals from text. Modes: single image, article-set, OG image. |
| [`multi-channel-bundle`](./skills/multi-channel-bundle) | Ship a coordinated multi-format bundle. Modes: campaign, launch. |

### Agency

| Skill | Description |
|---|---|
| [`agency-brand-scoping`](./skills/agency-brand-scoping) | Five on-direction visual variations for new-brand or pitch discovery. |
| [`agency-client-handoff`](./skills/agency-client-handoff) | White-label deliverable export as a zip. |
| [`agency-multi-brand-pack`](./skills/agency-multi-brand-pack) | Per-client asset templates scoped by workspace. |
| [`agency-pitch-mockups`](./skills/agency-pitch-mockups) | Client-branded pitch mockups (hero + tiles + quote slides). |

### Dev

| Skill | Description |
|---|---|
| [`dev-app-assets`](./skills/dev-app-assets) | Consistent app asset set: icons, empty states, onboarding illustrations. |
| [`dev-avatar-service`](./skills/dev-avatar-service) | Deterministic default-avatar generator per user seed. |
| [`dev-screenshot-beautifier`](./skills/dev-screenshot-beautifier) | Turn a raw product screenshot into an LP-ready hero. |

### Enterprise

| Skill | Description |
|---|---|
| [`enterprise-brand-governor`](./skills/enterprise-brand-governor) | Gate every generation through a `brand.md` policy file. |
| [`enterprise-pinned-registry`](./skills/enterprise-pinned-registry) | Pin exact model versions for reproducible output across teams. |
| [`enterprise-press-batch`](./skills/enterprise-press-batch) | Process press photos into wire / web / print / social packs. |

### Marketer

| Skill | Description |
|---|---|
| [`marketer-ad-variant-factory`](./skills/marketer-ad-variant-factory) | Fan out 50+ platform-native ad variants from one hero image. |
| [`marketer-localize-campaign`](./skills/marketer-localize-campaign) | Localize a campaign across N markets (copy + visuals). |

### Prosumer

| Skill | Description |
|---|---|
| [`prosumer-headshot-studio`](./skills/prosumer-headshot-studio) | Selfie → four polished headshots (LinkedIn / ID / editorial / casual). |

### Picsart MCP workflows

Start at the hub: it routes a request to the right `picsart-*` skill and holds the shared references every one of them links.

| Skill | Description |
|---|---|
| [`picsart-workflows`](./skills/picsart-workflows) | Route Picsart MCP media work to the right `picsart-*` skill; holds the shared references. |

**Connection and generation**

| Skill | Description |
|---|---|
| [`picsart-connect`](./skills/picsart-connect) | Choose and check the Picsart interface (MCP first; CLI or SDK fallback) before a media workflow. |
| [`picsart-model-choice`](./skills/picsart-model-choice) | Select a Picsart model for required inputs, output format, and cost. |
| [`picsart-generate`](./skills/picsart-generate) | Generate image, video, audio, or text with a verified Picsart model and keep its receipt. |
| [`picsart-job-recovery`](./skills/picsart-job-recovery) | Recover a generation result after a timeout or interruption without a duplicate job. |

**References**

| Skill | Description |
|---|---|
| [`picsart-library`](./skills/picsart-library) | Browse the shared Picsart Drive Library and resolve characters, props, locations, and cast. |
| [`picsart-asset-reuse`](./skills/picsart-asset-reuse) | Reuse characters, props, locations, and cast from the Drive Library or an existing film. |
| [`picsart-resource-library`](./skills/picsart-resource-library) | Publish or version reusable resources in remote storage with verified receipts. |
| [`picsart-brand-kit`](./skills/picsart-brand-kit) | Define or apply a brand kit: colors, type, logo use, and consistent layouts. |

**Creative output**

| Skill | Description |
|---|---|
| [`picsart-storyboard`](./skills/picsart-storyboard) | Plan image or video scenes as a storyboard with shot purpose, framing, timing, and action. |
| [`picsart-character-continuity`](./skills/picsart-character-continuity) | Keep a character consistent across images or scenes with references and a continuity record. |
| [`picsart-social-ad`](./skills/picsart-social-ad) | Produce social ad creative with a clear opening, product evidence, and call to action. |
| [`picsart-product-shoot`](./skills/picsart-product-shoot) | Create product images for catalogs and campaigns, preserving supplied product details. |
| [`picsart-product-mockup`](./skills/picsart-product-mockup) | Place supplied artwork onto a photographed product with an image-edit model. |
| [`picsart-image-edit`](./skills/picsart-image-edit) | Edit a supplied image: background removal or replacement, enhancement, or a verified edit model. |
| [`picsart-image-finishing`](./skills/picsart-image-finishing) | Exact crops, sizes, rotations, formats, and upscale for delivery derivatives of an accepted image. |
| [`picsart-batch-variants`](./skills/picsart-batch-variants) | Create and compare controlled asset variants within an authorized generation budget. |
| [`picsart-thumbnail`](./skills/picsart-thumbnail) | Create a video thumbnail or cover that stays readable at a small size. |
| [`picsart-explainer`](./skills/picsart-explainer) | Create an explainer from supplied material with narration, visuals, and verified delivery. |
| [`picsart-presenter`](./skills/picsart-presenter) | Create a talking-head presenter clip from an avatar, portrait, script, or recording. |
| [`picsart-3d-cartoon`](./skills/picsart-3d-cartoon) | Create 3D cartoon characters, stylized portraits, and animated scenes. |

**Sound**

| Skill | Description |
|---|---|
| [`picsart-voiceover`](./skills/picsart-voiceover) | Create a voiceover from an approved script: voice selection and speech timing. |
| [`picsart-music-bed`](./skills/picsart-music-bed) | Generate and place an instrumental music bed for mood and pacing. |
| [`picsart-sound-effects`](./skills/picsart-sound-effects) | Generate and place sound effects for actions, transitions, and atmosphere. |
| [`picsart-audio-mix`](./skills/picsart-audio-mix) | Arrange and balance voice, music, and sound: levels, trims, fades, and timing. |

**Scene and video**

| Skill | Description |
|---|---|
| [`picsart-scene-design`](./skills/picsart-scene-design) | Build title cards, overlays, and product cards with editable text, shapes, media, and motion. |
| [`picsart-scene-revision`](./skills/picsart-scene-revision) | Revise selected parts of an existing scene while preserving accepted footage and timing. |
| [`picsart-scene-variants`](./skills/picsart-scene-variants) | Adapt an accepted scene to new ratios, copy, languages, products, or brand treatments. |
| [`picsart-variable-data`](./skills/picsart-variable-data) | Export personalized assets from structured rows and one scene template. |
| [`picsart-video-edit`](./skills/picsart-video-edit) | Assemble or change an existing video scene: trim, sequence, crop, speed, and transitions. |
| [`picsart-video-repurpose`](./skills/picsart-video-repurpose) | Turn long or wide footage into short edits with subject framing and synced captions. |
| [`picsart-video-cutout`](./skills/picsart-video-cutout) | Remove or replace a footage background and verify the alpha or composite. |
| [`picsart-beat-edit`](./skills/picsart-beat-edit) | Sequence photos or video to measured music beats with verified audio sync. |
| [`picsart-captions`](./skills/picsart-captions) | Add or correct timed captions: transcripts, speaker labels, and caption styles. |

**Delivery**

| Skill | Description |
|---|---|
| [`picsart-delivery-check`](./skills/picsart-delivery-check) | Check and export a finished scene with confirmed file links. |
| [`picsart-ctv-delivery`](./skills/picsart-ctv-delivery) | Render an approved ad for a named CTV destination and check it against the spec. |
| [`picsart-scene-portability`](./skills/picsart-scene-portability) | Package an editable scene for handoff or archival, or translate it to Replay or Jet. |

### Film pipeline

| Skill | Description |
|---|---|
| [`picsart-film`](./skills/picsart-film) | Make a narrative AI film with recurring characters through the 11-stage pipeline. |
| [`picsart-film-development`](./skills/picsart-film-development) | Stages 1-3: look, story, video model, video plan, and the shot list board. |
| [`picsart-film-assets`](./skills/picsart-film-assets) | Stages 4-5: produce, review, and lock character sheets and prop plates. |
| [`picsart-film-scenes`](./skills/picsart-film-scenes) | Stage 6: generate the film's shots and select takes. |
| [`picsart-film-edit`](./skills/picsart-film-edit) | Stages 7-8: assemble, repair joins, reshoot, and reach the final cut. |
| [`picsart-film-finishing`](./skills/picsart-film-finishing) | Stages 9-11: grade, final-resolution pass, soundtrack, masters, and archive. |

### Motion pipeline

| Skill | Description |
|---|---|
| [`picsart-motion`](./skills/picsart-motion) | Turn Figma layers or uploaded assets into a motion-designed ad or reel. |
| [`picsart-motion-import`](./skills/picsart-motion-import) | Stage 1: bring a Figma design in as hosted layers and set formats and sizes. |
| [`picsart-motion-design`](./skills/picsart-motion-design) | Stage 3: choose motion per element and author smart-animate between frames. |

More skills are welcome — see [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

[MIT](./LICENSE)
