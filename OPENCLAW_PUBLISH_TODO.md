# Publish to OpenClaw (ClawHub) — TODO

Goal: get this repo's skills (and optionally the full bundle) into OpenClaw's
registry, ClawHub, so OpenClaw users can find and install them.

This repo contains two publishable things:
- **Skills** — the 20 `skills/<name>/SKILL.md` packs.
- **Bundle** — the Claude-style `marketplace.json` + `.mcp.json` (the Picsart MCP server).

They publish by different commands. The skills path is confirmed and low-risk;
the bundle path needs a dry-run check first.

> Note: every command below needs YOUR `clawhub login` (your credentials). None
> of this can be automated from the editor.

## Step 0 — Prerequisites
- [ ] Install the ClawHub CLI (`clawhub`). Confirm install method at clawhub.ai docs.
- [ ] GitHub account is **≥ 1 week old** (hard requirement to publish).
- [ ] At repo root: `cd /Users/sargis/job/gen-ai-skills`
- [ ] Authenticate:
      ```bash
      clawhub login
      ```

## Step 1 — Publish the skills (confirmed path, no wrapper needed)
Each skill folder publishes as its own versioned package. Publish all 20 in a loop:

```bash
for d in skills/*/; do
  slug=$(basename "$d")
  clawhub skill publish "$d" --slug "$slug" --name "$slug" --version 1.0.0
done
```

- `--slug` becomes the install name → `openclaw skills install @PicsArt/<slug>`.
- Refine `--name` to human titles later if desired (optional).
- UNCERTAIN: whether one command can publish all 20 at once. The loop publishes
  per-skill, which is the safe/confirmed behavior.

- [ ] All skills published.
- [ ] Verify: `openclaw skills search picsart`

## Step 2 — Publish the bundle (skills + MCP) — DRY-RUN FIRST
```bash
clawhub package publish PicsArt/gen-ai-skills --dry-run
```
- [ ] Read the dry-run output. It reveals whether the Claude-style bundle publishes
      as-is or needs an extra manifest (the one unverified point).
- [ ] Only if dry-run is clean, publish for real:
      ```bash
      clawhub package publish PicsArt/gen-ai-skills
      ```

## Step 3 — Verify it's live
- [ ] `openclaw skills search picsart` shows the skills.
- [ ] Install by slug works: `openclaw skills install @PicsArt/gen-ai-use`

## No-registry fallback (works today, nothing to publish)
Users can already install straight from GitHub:
```bash
openclaw skills install git:PicsArt/gen-ai-skills@main
openclaw plugins install picsart --marketplace https://github.com/PicsArt/gen-ai-skills
```

## Open risks to verify live
1. Bundle manifest requirements for ClawHub — resolve with `--dry-run` before publishing.
2. Multi-skill single-publish vs per-skill — assume per-skill (loop handles it).
3. ClawHub CLI install method — confirm from clawhub.ai docs.

## Notes
- The MCP server's tools surface in OpenClaw as `picsart__<tool>` under the
  built-in `bundle-mcp` plugin.
- There is no `openclaw plugins marketplace add` step — install points directly at
  the source.
