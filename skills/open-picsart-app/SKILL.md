---
name: open-picsart-app
description: Open Picsart beside the conversation - the user's recent files, their Picsart Drive, the AI tools, and where to start a film or a motion design video - on a yes to one closed question. Use when a use case offers to open Picsart, such as during setup.
user-invocable: false
---

# Open Picsart

Picsart opens beside the conversation: the user's recent files, their Picsart Drive, the AI tools,
and where to start a film or a motion design video. It shows nothing until they say yes.

ASK: "1. Open Picsart" / "2. Not now".

- **On 1:** call `picsart_workspace_open` with `{}`. It takes no input and charges nothing. Say in
  one line what they can do there.
- **On 2:** go on with the use case.
- **The call fails:** say in one line that Picsart could not open right now, and go on. Never
  retry it in the same turn.
