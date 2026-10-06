# Host conventions

Apply these conventions in every `picsart-*` skill and its references. They hold for Claude Code, Cursor, Codex, and any other host that loads SKILL.md skills.

- Discover the connected Picsart tools and use their actual names and schemas.
  The `picsart_*` names in a workflow identify tools, not a fixed host namespace;
  the host may add a prefix. If the connection is missing, explain that the
  `picsart` MCP server must be connected (see [interface map](interface-map.md));
  continue script and shot planning when possible. Never invent tool results or renders.
- Read board decisions from the current user message and attached widget context.
  Use a widget-context reader tool only if the host actually exposes one. Treat a
  board's initial tool result and unsent widget state as previews, never as user
  approval. If a submitted decision has no accessible payload, explain briefly and
  use the text fallback to collect the missing decision; do not guess or repeat
  charged operations.
- Use the host's available question interface, or one concise conversational
  question, for preset choices.
- UI rendering and feedback delivery are the remote MCP server's responsibility.
  If the host cannot render a board, present its relevant options in text and
  record the user's selection using the same documented feedback fields. Do not
  claim that a plugin manifest makes widgets render in a host that lacks them.
- Save the pipeline's state file (`film.json` for the film skills, `motion.json`
  for the motion skills) and artifacts in the user's writable project workspace,
  not the installed plugin or skill directory. If persistent file tools are
  unavailable, keep a structured project checkpoint in the conversation and
  provide it for download when the host supports files. Never claim a file was
  saved without confirmation from a file tool.
- Honor the user's current instructions and already authorized scope. Preserve
  quoted spend limits and production locks; do not infer authorization from a
  preview, a timeout, or an installed connection. A timed-out charged call needs
  a status check before considering a retry.
- The film pipeline is six skills ([picsart-film](../../picsart-film/SKILL.md),
  [picsart-film-development](../../picsart-film-development/SKILL.md),
  [picsart-film-assets](../../picsart-film-assets/SKILL.md),
  [picsart-film-scenes](../../picsart-film-scenes/SKILL.md),
  [picsart-film-edit](../../picsart-film-edit/SKILL.md),
  [picsart-film-finishing](../../picsart-film-finishing/SKILL.md)) and the motion
  pipeline is three ([picsart-motion](../../picsart-motion/SKILL.md),
  [picsart-motion-import](../../picsart-motion-import/SKILL.md),
  [picsart-motion-design](../../picsart-motion-design/SKILL.md)). Route between them directly.
- [Motion import](../../picsart-motion-import/SKILL.md) reads a design's layers through a connected Figma tool. If Figma
  is not connected in this host, use the flat-frame fallback and say so once.

## Motion server compatibility

This section applies to the motion skills. Discover live tool names and schemas
before invoking the pipeline. Updating skill files changes instructions; it does
not deploy new server tools.

`picsart_scene_editor` accepts `scene`, `title` and
`notes` and emits `scene_editor_feedback` v1. Accept without edits or comments
returns `verdict: "approved"`; Submit after edits or comments returns
`verdict: "needs_changes"`. Read the returned `document` when `edited` is true:
frame comments carry `instruction`, and timeline comments carry `text`, `start`
and `end`. Opening the editor is a preview, never approval.

For imports and gradients, use the served tools (`picsart_media_import_svg_path`,
`picsart_media_import_figma_paint`, `picsart_media_apply_gradient`) and the live
recipes (`picsart_media_list_recipes`). If an operation has no served tool or
recipe, explain that before proceeding with that step.
Keep the original editable assets and the current scene intact.
