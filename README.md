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
├── .github/workflows/   # CI (security scan, lint)
├── scripts/             # Repo tooling (scan-skill.py, ...)
├── skills/              # All skills live here, one directory each
│   ├── gen-ai-use/
│   │   └── SKILL.md
│   ├── marketer-campaign-kit/
│   │   └── SKILL.md
│   └── ...
├── INSTALL.md
├── CONTRIBUTING.md
├── VERSION
├── setup                # universal symlink installer
└── README.md
```

Each skill lives in its own directory under `skills/`. The directory name is the install name. The directory must contain a `SKILL.md` with YAML frontmatter (`name`, `description`, optional `argument-hint`, optional `allowed-tools`) followed by the skill body.

## Skills

This bundle ships **19 skills**. Several skills are mode-routers — one entry point with `references/modes/` for variants — to keep the catalog small and trigger-friendly.

### Core CLI

| Skill | Description |
|---|---|
| [`gen-ai-use`](./skills/gen-ai-use) | Generate AI images, videos, audio via the Picsart `gen-ai` CLI. |
| [`gen-ai-persona-creation`](./skills/gen-ai-persona-creation) | Create AI influencers, branded characters, or pet personas from a brief or reference. |
| [`motion-studio`](./skills/motion-studio) | End-to-end AI video production: references, clips, scene assembly, audio. |

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

More skills are welcome — see [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

[MIT](./LICENSE)
