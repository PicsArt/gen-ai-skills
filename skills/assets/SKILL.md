---
name: assets
description: Open the Picsart Assets panel on what the user made with Picsart - their videos, images, audio, film characters, film props and film projects - newest first, with previews, or on one kind or one film when they name it. Use when the user wants to see what they made ("show my assets", "my film characters", "open the two-sisters film") or asks for the assets panel. Not for browsing Drive folders, and not for choosing a film's references for a generation.
metadata:
  title: Browse assets
  short-description: See your videos, images, audio, characters and films
  argument-hint: '[videos | images | audio | characters | props | a film]'
  starter-prompt: Show my Picsart assets.
argument-hint: '[videos | images | audio | characters | props | a film]'
---

# Browse assets

Read picsart-video-rules first. One job: open the Assets panel on what the user asked to see.
Nothing here charges credits.

| Stage | Gate | Skills |
|---|---|---|
| 1. Open the panel | ASK | — |
| 2. One line | — | — |

## 1. Open the panel

Call `picsart_film_show_assets`, read-only and free:

- **Nothing named:** call it with `{}`. Every kind opens, one tab per kind.
- **One kind named:** call it with `type`: `video`, `image`, `audio`, `character`, `prop`, or
  `project` for their films or projects.
- **A film named:** call it with `{ "type": "project", "pageSize": 128 }` first. Find the film by
  its name among the projects it returns; while none fits and the reply says `hasNext`, call it
  again with the next `page`. Then call it with that project's `uid` as `projectUid`, and with
  `type` too when they asked for one kind of that film ("the characters of the garage film").
  When two films fit the name, ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) which one, with their names as the options. When no page
  has it, say in one line that no film has that name, and stop.

Pass a `projectUid` only as a `type: "project"` reply gave it: the panel refuses any other folder.
When the tool says the user is not signed in, or that Drive is unavailable, say so in one line.

This panel is for looking. Browsing Drive folders is `picsart_drive_list`, reading a film's
assets for a generation is `picsart_film_list_assets`, and showing or picking the user's saved scene
documents (characters, locations, templates, looks…) is `picsart_scene_library_list`: it opens the
picker, and a picked card comes back as `libraryId`, `sceneUrl` and `kind`, to open with the scene tools
or use with `picsart_scene_apply_preset` (`library:<id>`) or `picsart_scene_apply_template`.

## 2. One line

The panel already shows every file. Say in one short sentence what is open ("Your film characters
are open."), and never list the files back, by name or by count.
