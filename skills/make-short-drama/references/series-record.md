# The series record

One record per series, written whole at every milestone. It outranks memory. Where the host gives
you files, keep it as `film.json` in the working folder of the series project. Otherwise keep it
in the conversation and give it once at session end for the user to paste back. Never print it
mid-flow. Save gates, locks, batch dispatch/landing, reviews, picture lock and exports as they
happen. Saving production state does not commit a proposed story delta.

## Project fields

Extend the film project record. Keep `film`, `stage`, `brief`, `drive`, `look`, `story`, `model`,
`assets`, `scenes`, `runs`, `spend`, `gates`, `overrides`, `openDecisions`, `blockedOn`, `attempts`,
`cut` and `disclosure`. At series level, `stage` is the seven-stage workflow; episode production
uses substage ids 5a–5f. Namespace scene, shot and run ids by episode to prevent collisions.

| Field | Preserve |
|---|---|
| `brief` | Logline, world in three sentences, people, standing decisions and reasons; format, episode count/length, language and successor flags |
| `drive` | `project`, `library`, `assets`, `shots`, `exports` uids; one project for the entire series |
| `look` | Verbatim `stylePrefix`, selections, scheme, hue, palette carriers and `accentBelongsTo` |
| `model` | Video id, ceiling seconds, edit/extend siblings and image model |
| `assets` | Tag, type, source, version, status, assetId, line-keyed descriptor, frozen voice, sheet, grid, view boxes and delivered sizes |
| `scenes` | Geography, approved picture URLs, shots with values, status, run, reference indices and trims |
| `runs` | Planned and actual cuts, shot/scene ids, joins, ordered references and roles, prompt versions/tokens, takes and pieces |
| `spend` | Every quote, its yes, and job workflow/id; follow dropped calls by this handle |
| `gates`, `overrides` | Evidence and any user override with gate, line and reason |
| `cut` | Last approved scene document and final flag; user trims/splits stay theirs |
| `attempts`, `blockedOn`, `openDecisions` | Failure counters and outstanding facts or choices |

Descriptors, voices and style prefixes stay verbatim. `blocking` tracks where a person was left
and screen exit; changed wardrobe or damage has its own tag and view. `refs` order and `refRoles`
remain paired. Each shot's reference indices point into that run. `cutTimesActual` holds the real
cuts; `pieces` names original/edit/extend files, and trims are in the piece's seconds. Set
`trimSource: "user"` only for a user trim. A prompt changed after picture lock gets a new version.
Assets progress draft → review → locked; shots planned → drafting → iterating → final.

## Series extension

| Field | Contents |
|---|---|
| `seriesBible` | Locked Story DNA, emotional promise, season question, characters' wants/flaws/secrets, relationship/power graph, recurring sets, reveal bank, theme and caption style |
| `arc` | Every incident outline, proposed ending shape, successor flag and intended continuity delta |
| `castManifest` | Tag, assetId, `sheetVersion`, locked status, descriptor/views, voice notes, superseded versions and episode applicability |
| `committedStory` | Accepted episode/version through which the state is true, relationship/power graph, audience knowledge, per-character knowledge, hidden facts, open threads, spent twists and ending history |
| `episodes` | Number, version, proposed/accepted status, production stage, script, successor flag, ending shape used, proposed and committed story deltas, evidence, verdict, masters and acceptance |

The manifest covers places and props as well as cast. An asset row's `version` mirrors its
`sheetVersion`; retain old rows and explicit supersession. Record voice language, register,
accent and approved notes verbatim, with available sample references. Do not claim a selected
voice was verified merely because notes exist.

A compact episode entry can look like this; replace illustrative values with observed state:

```json
{
  "number": 2,
  "version": "v1",
  "status": "proposed",
  "stage": "5a",
  "hasSuccessor": true,
  "endingShapeUsed": "Reversal",
  "basedOn": { "episode": 1, "version": "v1" },
  "storyDelta": {
    "proposed": {
      "audienceKnowledgeAdded": ["The trustee withheld the letter"],
      "characterKnowledgeAdded": { "@mara": ["The ring belongs to her mother"] },
      "hiddenFactsRemaining": ["Who altered the register"],
      "relationshipPowerChange": "Mara gains leverage over Theo",
      "externalPlotMove": "Mara demands the register before the sale",
      "secretPlotMove": "She traces the ring to her mother",
      "threadsOpened": ["Who ordered the withheld letter?"],
      "threadsClosed": ["Who owned the ring?"],
      "spentTwistsAdded": ["The trustee withheld the letter"]
    },
    "committed": null
  },
  "verdict": null,
  "evidence": [],
  "masterUrls": [],
  "acceptance": null
}
```

Keep full knowledge snapshots alongside deltas: audience knowledge is not character knowledge.
Each hidden fact records who secretly knows it. Open threads have ids, plants, owners and intended
payoffs; spent twists cannot be offered again as new. Keep ending history by accepted episode and
shape, plus the proposed arc, so both the rolling five and whole-season diversity can be checked.

## Commit and resume

On explicit user acceptance of a specific episode version, copy its proposed delta to committed,
apply it once to `committedStory`, record acceptance and mark that episode accepted. Do not apply
it again on resume. Changed canon requires an explicit revision decision and dependency check.
Rejected and superseded versions remain proposals; keep them out of the next episode's baseline.

On resume, read the record before reporting status. Use the last accepted version, then resume an
unfinished proposed episode or start the next one. List assets scoped to the project and reconcile
locked versions against the manifest. Never infer a lock from a `saved` message or a sheet URL.
