---
description: "A vertical story episode, built in stages: slides, voice, video"
argument-hint: "[slides | voice | video] [script or story idea]"
---

Run the `make-short-drama` use case, starting from this preset: one vertical story episode with a recurring cast, a series only when the user asks for one. When the request starts with slides, voice or video, build only that stage, as the use case's Build in stages says.

Anything the user says below wins over the preset. Ask only for what is still missing.

The user's request: $ARGUMENTS
