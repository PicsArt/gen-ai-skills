---
name: picsart-film-development
description: "Develop a film from an idea or script until its pictures can be made. Fixed order: look console, story in the viewer's words, video model, video plan, then the shot list board. Use for Stage 1, which also covers references and the visual bible, when nothing is locked yet. Routed from picsart-film. Not for generating shots; use picsart-film-scenes."
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, film, development]
---

# Film development

Develop a film from an idea or script until its pictures can be made.

## When to Use

- Stage 1 of the film pipeline, including references and the visual bible, when nothing is locked yet.
- Not for generating shots; use [picsart-film-scenes](../picsart-film-scenes/SKILL.md).

## Prerequisites

The `picsart` MCP server is connected.
Read [host conventions](../picsart-workflows/references/host-conventions.md) first. They apply to this skill and its references.
Read [the interface map](../picsart-workflows/references/interface-map.md) before tool calls and cost checks.

## How to Run

Read [the workflow](references/workflow.md) in full when this skill starts.
Read each file below in full before its step.

## Quick Reference

| When | Read |
| --- | --- |
| Writing the story from an idea, or preparing a supplied script (step 3) | [Dramaturgy](references/dramaturgy.md) |
| Same moment, for what the medium can afford | [Screenwriting](references/screenwriting.md) |
| Breaking the story into shot cards and the asset list | [Breakdown](references/breakdown.md) |
| The user wants a reference board or moodboard | [Visual bible](references/visual-bible.md) |
| Choosing the video model (step 4) | [Model policy](../picsart-film/references/model-policy.md) |

## Procedure

Routed from [picsart-film](../picsart-film/SKILL.md).
At the gate, continue to [picsart-film-assets](../picsart-film-assets/SKILL.md) in the same turn.

## Pitfalls

- Lock the look on `picsart_film_setup` before writing a word of story.
- Show the story as plain paragraphs in chat for the yes. Never open a board to show a story.
- Answer a story note by rewriting the paragraph first. Rebuild the board from it once.
- Store the compiled style prefix verbatim.
- A user's photo of the real person is the asset, not a mood reference. Save it untouched.

## Verification

- Approval is the user's actual decision: a submitted verdict, or an explicit text answer when the board is unavailable.
- Opening or previewing a board is never approval.
