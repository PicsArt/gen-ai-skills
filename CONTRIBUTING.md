# Contributing

Thanks for your interest in contributing to `gen-ai-skills`.

## Adding a skill

1. Create a top-level directory named after your skill (kebab-case, e.g. `picsart-upscale`). The directory name is what users will see installed at `~/.claude/skills/<name>/`.
2. Add a `SKILL.md` at the root of that directory with YAML frontmatter:

   ```markdown
   ---
   version: 0.1.0
   name: picsart-upscale
   description: |
     One-paragraph description. Lead with what the skill does, then list the
     trigger phrases an agent should match on ("upscale this image",
     "increase resolution", …). Mention what the skill is NOT for and any
     skills it chains with.
   argument-hint: "[image-path] [--scale 2|4]"
   allowed-tools: Bash
   ---

   # Picsart Upscale

   Body of the skill: instructions, examples, edge cases.
   ```

3. Put any supporting files (references, examples, prompt fragments) inside the skill's own directory.
4. If the skill should appear in the Claude Code marketplace, add an entry to `.claude-plugin/marketplace.json` under `plugins[0].skills`:

   ```json
   {
     "name": "upscale",
     "path": "picsart-upscale",
     "invoke": "/picsart:upscale"
   }
   ```

5. Bump the `version` in `VERSION`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`, and `.cursor-plugin/plugin.json` together.

## Skill conventions

- One skill = one directory. Don't nest skills inside skills.
- Frontmatter `description` is the single most important field — agents use it to decide whether to invoke the skill. Be explicit about trigger phrases and exclusions.
- Keep `SKILL.md` self-contained. If a skill needs long references, put them in `<skill>/references/` and link from `SKILL.md`.
- Don't shell out to anything that requires interactive input.

## Pull request flow

1. Fork the repository and create a feature branch from `main`.
2. Run `./setup` locally and verify the new skill loads in your agent.
3. Open a pull request describing the skill and its motivation.
4. Be kind in code review.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](./LICENSE).



 can you chekc our skill agains this /Users/sargis/Desktop/skills/higgsfield-generate and lets understand which one is better acroding to claudebest practices to wrigin
  skills'/Users/sargis/job/ai-toolkit/.claude/skills/gen-ai-use'   