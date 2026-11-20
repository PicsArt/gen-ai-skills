# Reveal on a spoken word

A part of a diagram appears as the narration says its word. The cue is a number the scene reads, so the same scene plays to any voice.

## The scene

One `number` parameter per cue. Its default is the cue's time in the scene, so the scene previews alone. Each revealed layer's `start` reads it, with a small lead so the entrance lands on the word:

```json
{
  "parameters": {
    "moon": { "type": "number", "default": 0.25 },
    "sun": { "type": "number", "default": 1.25 }
  },
  "layers": [
    { "id": "moonDisc", "start": { "$eval": "moon - 0.1" }, "duration": 3, "…": "…" },
    { "id": "sunRays", "start": { "$eval": "sun - 0.1" }, "duration": 3, "…": "…" }
  ]
}
```

A new voice changes the parameter values only: in the join's `scene_ref` `parameters`, or in the defaults. Every cue is a named parameter, so a part with no cue can be found. Do not reference composition markers from `start`, and do not bind to the transcript while playing.

## Resolving the cues

The script is known, so align it to the transcript; never search the transcript for a word string, which misses or mishears short lines:

1. Mark each cue as phrase k, word j of the approved script, and take the transcript's words and their times from `picsart_media_transcribe`.
2. Align the script's words to the transcript's in order. A word the transcript heard slightly differently is still that word; one it did not hear at all has no time: fix the script or the transcript, never guess one.
3. The cue time is the start of that transcript word. Subtract the scene's start (its first spoken word) so the time is in the scene's own clock.
4. That time is the cue parameter's `default`; the layer's `start` is `{"$eval": "<cue> - <lead>"}`.

The engine's cue resolver, which does steps 2 to 4 and the checks below in one pass, runs only on a local checkout and is not served here: follow the steps above.

## Checks

Each can be made from the cue times, with no render:

- Words per second of each scene: MINOR above about 2.3. Trim the script; never stretch the motion.
- An entrance still building when its phrase ends.
- Every cue in the scene's first quarter: the diagram is all on screen early.
- A part with no cue: it is not revealed on a word.
- Each cued part is not drawn before its word less 0.3 s and is drawn by its word plus 0.3 s: `picsart_scene_check_contracts` on the built scene, with a `motion_range` contract on `effectiveOpacity` for each part (0 before, 1 after).

## Reading the captions

`picsart_scene_lint_layout` reads caption groups in the time they are shown (`captionReading`, MINOR): more than 2 lines, over 20 characters per second, or shown under 0.8 s. The shown time counts the style's `hold`. The served lint takes no audience: for children, hold each group to 17 characters per second yourself. Group by energy in the script that writes the transcript, not in the lint.
