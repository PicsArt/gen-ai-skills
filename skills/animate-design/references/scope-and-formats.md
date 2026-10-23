# Scope and formats

## Scope — phased

- **Phase 1 (now): motion-design static material into an ad/reel.** A Figma design's layers — or
  the user's own uploaded assets — → a composed, animated scene → tuned by eye → rendered. All
  of what follows.
- **Also available: generate footage when the design needs it.** When a beat calls for real
  generated video (a video card/element, or the designer asks to generate a clip with a model of
  their choice), that's supported — but it spends credits, so it runs behind the cost-consent gate
  (see *Video generation*). It's a capability within the flow, not a separate phase.
- **Phase 2 (later): generate a *new* video from a given one.** A video-to-video pass,
  once the server's v2v path is wired. Don't build it yet; keep the hook
  (`motion.json.source` can name a given video, not only a design).

## Formats — scene is the source of truth

Everything is authored and edited as a **scene** — the format the engine natively
supports and the one every `picsart_scene_*` / `picsart_media_*` edit / validate / query tool speaks, and the
one `sceneRef` points at. The **mp4** is *derived* from it at Stage 5 (`export`). The scene
is the single editable source of truth — keep it and edit it; the mp4 is the final
render, never an editing surface.
