---
name: gen-ai-local-files
description: Renamed — use picsart-add-media instead.
version: 2.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, upload, local-files, redirect]
---

# Moved

This skill has been renamed to **[`picsart-add-media`](../picsart-add-media/SKILL.md)**. Local
files now become URLs via a browser upload widget (`picsart_upload_widget` / `mp_upload`) instead
of the CLI/`data:`-URI routes this skill used to document. This stub exists only so old
references don't 404 — the sections below just point onward.

## When to Use

Never — this slug is retired. Use [`picsart-add-media`](../picsart-add-media/SKILL.md) for any
local-file-to-URL task.

## Prerequisites

None here — see [`picsart-add-media`](../picsart-add-media/SKILL.md).

## How to Run

Load [`picsart-add-media`](../picsart-add-media/SKILL.md) instead of this skill.

## Quick Reference

| Old | New |
|---|---|
| `gen-ai-local-files` | [`picsart-add-media`](../picsart-add-media/SKILL.md) |

## Procedure

1. Stop using this skill.
2. Use [`picsart-add-media`](../picsart-add-media/SKILL.md).

## Pitfalls

- Don't add new references to this slug — point at `picsart-add-media` directly.

## Verification

N/A — this is a redirect stub, not an executable skill.
