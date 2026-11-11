# The project record

One record per film. Write it whole at every milestone, never as a diff. It is read back, never
remembered: "locked" is true when the asset's row says so, not when you recall saving it.

## Contents

- The record (below)
- Why the awkward fields
- Resuming older films

```json
{
  "film": "the-garage",
  "workflowVersion": 2,
  "stage": 6,
  "brief": {
    "logline": "Two brothers split over a garage neither can afford to lose.",
    "world": "<three sentences>",
    "people": { "@cal": "owes, and hides it", "@tobin": "holds the deed, keeps working" },
    "decisions": [{ "what": "hard cuts only", "why": "the film is about abruptness" }]
  },
  "drive": { "project": "<uid>", "library": "<uid>", "assets": "<uid>", "shots": "<uid>", "exports": "<uid>" },
  "look": {
    "stylePrefix": "<verbatim from film_setup_feedback>",
    "selections": { "genre": "drama", "tone": "auto", "palette": "auto", "ratio": "169", "duration": "90", "camera": "35mm", "lens": "ana" },
    "scheme": null, "hue": null,
    "palette": "<with a scheme: its colours, each named with what carries it; null with scheme Auto>",
    "accentBelongsTo": "<the one thing that owns the accent colour>"
  },
  "story": {
    "who": "…", "where": "…", "wants": "…", "against": "…", "happens": ["…", "…", "…"],
    "peak": "…", "ends": "…", "says": "…", "fixed": ["…"], "genre": "drama",
    "scenes": [{ "id": "sc01", "text": "<the scene paragraph the user approved>", "sec": 40 }]
  },
  "model": {
    "video": "<the id model_choice_feedback returned>",
    "ceilingSec": 0,
    "edit": "<its edit sibling>", "extend": "<its extend sibling>",
    "pictures": "<the image model, chosen once for the film>"
  },
  "assets": [
    { "tag": "@cal", "type": "character", "source": "generated", "version": "v1", "status": "locked",
      "assetId": "<picsart_asset_save result>", "identityReferences": [],
      "descriptor": [{ "line": "face", "text": "…" }],
      "voice": "<verbatim, frozen once saved>",
      "sheet": "<url>", "grid": "<as declared>",
      "views": [{ "id": "identity", "box": [0, 0, 0, 0], "delivered": [0, 0], "url": "<url>" }],
      "scenes": ["sc01", "sc02"],
      "blocking": { "asOf": "sc01", "left": "frame-right, walking away from the bench", "exit": "frame-right" } }
  ],
  "rejectedAssets": [
    { "tag": "@cal", "version": "v0", "fileUid": "<rejected file uid>", "url": "<rejected sheet URL>",
      "views": ["<every extracted view/panel URL>"], "reason": "profile is not ok", "exception": null }
  ],
  "scenes": [
    { "id": "sc01", "slug": "INT. GARAGE — NIGHT", "status": "selects-complete",
      "geography": "<the one line pasted into every prompt of the scene>",
      "pictures": { "wide": "<url>", "scene": "<url>", "map": "<url>" },
      "shots": [
        { "id": "1A", "status": "final", "run": "r1", "values": { }, "refs": [1, 2, 3],
          "trim": { "in": 0.4, "out": 5.1 }, "trimSource": "user" }
      ] }
  ],
  "runs": [
    { "id": "r1", "shots": ["sc01:1A", "sc01:1B"], "scenes": ["sc01"], "genSec": 0,
      "join": "ends as Cal's hand closes on the wrench; r2 opens on the wrench from close in",
      "cutTimes": [5, 13], "cutTimesActual": [5.2, 12.8],
      "refs": ["<url>", "<url>"], "refRoles": ["START FRAME", "IDENTITY @cal"],
      "promptVersion": "v3", "promptToken": "<from the compiler>",
      "takes": [{ "job": { "workflow": "…", "id": "…" }, "url": "<url>", "verdict": "accepted" }],
      "pieces": [{ "url": "<url>", "from": 0, "to": 28, "call": "run" }] }
  ],
  "spend": [{ "what": "r1 take 1", "quoted": 0, "yes": true, "job": { "workflow": "…", "id": "…" } }],
  "gates": { "2": "passed", "3": "passed", "4": "passed", "5": "passed", "6": null },
  "overrides": [{ "gate": "5", "line": "…", "why": "the user asked to shoot sc02 first" }],
  "openDecisions": [],
  "blockedOn": null,
  "attempts": {},
  "requestedPreview": null,
  "cut": { "scene": "<the last scene document the user approved>", "final": false },
  "disclosure": null
}
```

## Why the awkward fields

- `stylePrefix`, `descriptor` and `voice` are **verbatim**. Consistency dies the day one is
  shortened. `look.selections` holds the preset ids the user chose.
- `look.palette` is written once the scheme is locked: the scheme's colours, each named with what
  carries it, and it goes into every place's descriptor. The scheme says how the hues relate, never
  what carries them, so `accentBelongsTo` is your design call: the one thing that owns the accent.
- `identityReferences` retains supplied original photo URLs across every scene and later shot.
  `[]` means an entirely generated identity; an absent field means legacy unknown provenance,
  which must be resolved from supplied media. Generated sheets and `views` supplement these
  originals; copy the originals into each relevant generation or plan item's `imageUrls`.
  Rejecting a generated sheet does not reject its source photos; every replacement retains them.
- `descriptor` is line-keyed, so a change is one line and a sheet redo changes one thing.
- `rejectedAssets[]` persists each rejected tag, version and file (uid and URL), every derived view
  or panel, the user's reason and any explicit exception. Save that version with
  `picsart_asset_save`, `status: "rejected"`, before regenerating, and mark its asset row
  `rejected`. Keep this list across replacements and resumed turns; check it before showing any
  picture or choosing any reference. No rejected sheet or part of it is shown or used again.
  One rejected view rejects the whole sheet unless the user explicitly said otherwise.
- `views[]` holds the box in sheet pixels and the delivered size, the first two numbers to read when
  a face drifts.
- `blocking` is the one piece of a person's state that crosses a scene: where they were left and
  which side of frame they went out. Wardrobe and damage are never here: a changed state is its own
  tag with its own view.
- `runs[]` is top level because a run spans scenes. Before quoting, recheck its packing against
  current model durations and reference limits; record any required short-run constraint or
  explicit user split. A prior grouping alone is not proof that the model capacity was used. `cutTimes` are the plan; `cutTimesActual` are
  where the take really cut: a check, never an edit point. `refs` are the ordered `imageUrls`,
  `refRoles` what the prompt called each one, and each shot's `refs` are indices into them.
- `pieces[]` are the files a run's picture comes from: the take, then any edit or extend that
  replaced or added seconds. A shot's `trim` is in its piece's seconds.
- `trimSource` is `user` or absent. Nothing automatic writes a trim.
- `spend[]` keeps every quote beside the yes and the job handle it bought, so a dropped call is
  checked on its handle and never paid twice.
- `scenes[].pictures` retains the wide, opening scene picture and room map (`map` is null when
  no room map is needed). `geography` is the location line shared by the scene's prompts. These
  are stage 5's location references, independent of any storyboard or animatic.
- `requestedPreview` is null by default. Only an explicit user request sets its `kind` to
  `storyboard` or `animatic`, with `status: "requested"` until its review is approved. Preserve an
  unfinished explicit request on resume; an old automatically required animatic is not one.
- `attempts` counts per tool and failure, so a one-retry rule is kept by bookkeeping, not memory.

Statuses: assets `draft → review → locked`, with `draft`, `review` or `locked` able to become
`rejected`. A rejected version cannot lock again; its replacement has a new version. Shots `planned → drafting → iterating → final`; a shot
changed after picture lock gets a new `promptVersion`, never an edit in place.


## Resuming older films

New records use `workflowVersion: 2` and nine stages. An absent version is the previous ten-stage
flow. Migrate once before changing its stage: keep 1–5; old 6 (storyboard/animatic) resumes at 6
(shooting) when the cast and location references are ready, otherwise at 5 for only the missing
references; old 7–10 become 6–9. Remap gate and override keys 7–10 the same way. Archive the old
stage-6 gate and overrides as `legacyStoryboardGate` and `legacyStoryboardOverrides`; never count
animatic approval as shooting completion. A previous stage-5 pass is checked for the location
references now owned by that stage before buying any video.

Keep every approved asset, scene picture, map, job handle, quote, accepted take, cut and user edit.
An existing `animatic`, per-scene `panels` or `voice` may stay as historical material, and approved
images can be reused as references. Preserve explicit shot exclusions and any user-approved held
images from the old `toVideo`/`keptAsPanel` decisions; do not regenerate them or reopen their approval.
Create a missing storyboard or animatic only on an explicit user request; never ask permission
to skip one. Write
`workflowVersion: 2` after migrating, so a later resume cannot renumber the stages twice.
