---
name: lip-sync-lines
description: Make a rigged character's mouth move on its spoken lines - word timings for each line from the voice, one combined transcript per character per scene, one viseme lip-sync preset on that character's rig layer, and a rig without the viseme mouth set named to the user. Use when a character in a scene speaks on screen, in a story or an explainer with a host.
user-invocable: false
---

# Lip-sync a character's lines

Lip-sync comes after the picture is proven: the shots are timed silent from estimated line lengths, and the voice and the lip-sync are made only once the user accepts the first render. When the real line lengths arrive, the slot grows and you say so; a line is never cut to fit.

A speaking character has one voice.
Cast it as voice-over-generation says.

Get each line's word timings with `picsart_media_transcribe`, passing `text` the line you sent to text-to-speech: recognition mishears short lines ("Mine!" as "Nein!") and can return nothing for a one-word line, and with `text` the result is that script on the timing of the speech heard.

Combine all of one character's lines in a scene into one transcript at their scene-relative times, then apply `picsart_scene_apply_preset` once with `preset: "lipSync:visemes"` on that character's rig layer, for its own lines only (`speaker`), with the transcript and the rig's `visemes` in `params`. Applying it again replaces the mouth tracks, so a second line applied alone would erase the first.

Apply it with `audio` naming the scene's voice layer. If the first call answers `status: "pending"` (the audio is still being analysed), call it again with `analysisJob` set to the id it returned.

A rig without the viseme mouth set is named to the user ("X can't lip-sync"), and its lines become narration.

A mouth that does not move on its line is a lip-sync that was not applied: apply it again.
