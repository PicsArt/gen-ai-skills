---
name: picsart-connect
description: Choose and check the Picsart interface before a media workflow. The picsart MCP server is the default; the gen-ai CLI and @picsart/ai-sdk are fallbacks when no MCP host is available. Use at the start of any Picsart task or when tools or sign-in are missing.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, connect, routing, auth]
---

# Connect and Route

Pick one Picsart interface for the task and confirm it works before any paid call.
Use the `picsart` MCP server first. Use the CLI or SDK only when the host cannot run MCP.

## When to Use

- At the start of a Picsart task, to pick the interface and the route for the requested change.
- When Picsart tools are missing, sign-in fails, or the user asks which interface to use.

## Prerequisites

- For MCP: the host can add a remote MCP server. Read the [interface map](../picsart-workflows/references/interface-map.md).
- For CLI or SDK: a shell with Node.js, and existing Picsart credentials.

## How to Run

1. Look for `picsart_*` tools in the current tool list.
2. If they are missing, add the `picsart` server at `https://api.picsart.com/gen-ai/mcp`. The host opens Picsart sign-in (OAuth) on first connect. No API key is needed.
3. Test with a free read: `picsart_model_catalog` or `picsart_model_params`. Do not test with generation.
4. Only if MCP is not possible, use the CLI or SDK (see Quick Reference).

## Quick Reference

| Interface | Check | Discover | Run |
| --- | --- | --- | --- |
| `picsart` MCP (default) | free read succeeds | `picsart_model_catalog`; `picsart_list_models` for the picker | `picsart_generate`, `picsart_media_*`, edit tools |
| gen-ai CLI (fallback) | `gen-ai --version`, `gen-ai whoami` | `gen-ai models`, `gen-ai models info MODEL --json` | `gen-ai generate ... --no-input --json` |
| `@picsart/ai-sdk` (fallback) | installed version | `catalog`, `Model(id).meta()` | `ai.generate`, `ai.submit` + `ai.result` |

| Need | Route |
| --- | --- |
| Create missing imagery, video, or sound | [model choice](../picsart-model-choice/SKILL.md), then [generate](../picsart-generate/SKILL.md) |
| Cut out, replace background, upscale, vectorize | `picsart_remove_bg`, `picsart_change_bg`, `picsart_enhance`, `picsart_vectorize` |
| Trim, merge, layer, caption, resize, or revise a scene | `picsart_media_*` scene tools; see [scene design](../picsart-scene-design/SKILL.md) |
| Reuse characters, props, locations, brands | [asset reuse](../picsart-asset-reuse/SKILL.md) |
| Store and reuse project resources | [resource library](../picsart-resource-library/SKILL.md) |

## Procedure

1. Start from the supplied media and the requested change. Find existing assets with [asset reuse](../picsart-asset-reuse/SKILL.md). Keep their IDs and versions.
2. Choose the route from the table. Use the scene route when later revisions need separate clips, text, logos, or sound.
3. For MCP, let the host manage sign-in. If sign-in fails, ask the user to connect Picsart.
4. For CLI, use existing credentials or operator-supplied `PICSART_ACCESS_TOKEN` and `PICSART_USER_ID`. Do not read credential files into chat. Do not show account identifiers.
5. For SDK, use `createClient` with the project's established API URL and credentials from the environment, or an existing authenticated `fetch`.
6. Check credits with `picsart_credits` only when the task needs it.
7. Generate only material the workflow still needs.

## Pitfalls

- Keep model IDs, job handles, and scene revisions separate. Do not pass one as another.
- `gen-ai login` opens an external browser. Do not run it where the host forbids that. Report the limit.
- CLI `video-edit` transforms footage through a model. It does not give deterministic trim or merge. Use the scene tools for that.
- Do not invent SDK methods, CLI flags, or tool names to bridge interfaces. Check actual schemas and installed help first.

## Verification

- Report the chosen interface, the route, and the free read that proved access.
- Carry the brief, asset references, scene revision, output targets, and job receipts to the next skill.
- If access is missing, report the required connection and keep the prepared inputs. Do not treat a prepared request as a run.
- Use [production guidance](../picsart-workflows/references/media-production.md) for the chosen composition workflow.
