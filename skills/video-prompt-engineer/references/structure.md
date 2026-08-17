# Structure

A prompt is read start to finish, and earlier clauses frame the later ones. This order puts the decisions that cannot be undone first, and the exclusions last.

## Clause order

1. Duration
2. Aspect ratio
3. Medium and style
4. Shot size
5. Camera angle
6. Camera movement
7. Lens and focal length
8. Depth of field
9. Lighting
10. Colour and grade
11. Subject motion
12. Mood
13. Audio bed
14. Pacing and cuts
15. Exclusions

One clause per decision, commas between them. A prompt is a list of decisions, not a paragraph of atmosphere. Prefer a number to an adjective wherever a number exists: 8 seconds over short, 85mm over flattering, 116 BPM over upbeat.

Keep a single shot prompt under roughly 120 words. Past that, generators start dropping clauses, and the ones they drop are at the end, which is where the exclusions live.

## More than one shot

Use a labelled block per shot and repeat the shared lines byte identically. Paraphrasing the style line between shots is the single biggest cause of a sequence that will not cut together.

```
STYLE: <one string, identical in every block>
NEGATIVE: <one string, identical in every block>

SHOT 1
SCENE: <what is in frame>
CAMERA: <shot size, angle, one movement>
MOTION: <one action, completed within the shot>

SHOT 2
SCENE: ...
CAMERA: ...
MOTION: ...
```

One action per shot. If a shot needs two things to happen, it is two shots.
