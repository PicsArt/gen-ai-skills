# The project record's core keys

Every use case that runs the edit pipeline keeps these keys in its record, beside its own.
`scripts/record.py check <record>` checks them where commands run. The keys are the same wherever
the record is kept: on disk, in Drive or in the conversation.

| Key | Holds |
|---|---|
| `useCase`, `job` | the use case and the job it runs, said back to the user at intake |
| `pipeline` | the stages this job runs, in the core order |
| `stages` | per stage: `status` (`done` or `stale`), `at`, `skipped: "user"` with its `risk` when the user chose to skip the check, the critics or the review (`record.py skip`), and either `reads` (a copy of the keys it read, when marked by hand) or `inputsHash` (from `record.py`), and `artifact` with its `artifactHash` |
| `brief` | `said`, `read` and `assumed`, kept apart |
| `standing` | `text`, `words` (the user's own), `date`, and `reason` when given |
| `approvals` | `what`, `by`, `date`, `scope` (`meaning:<phrase>` for a meaning change, with the `job` chosen; `keeper:<phrase>` for a keeper let go, with its `shot` or `what`; `map`, `moments` or `mapping` for the approved map; `format:<element>` for a plan that leaves the reference's format, `format:pace` for a pace other than the reference's, `format:rhythm` for a shape other than the rhythm's), and when it was relayed, `session` and `words` (the person's own, quoted). Never a SPEND. |
| `rejected` | `what` the user turned down, `date` |
| `cutPace` | `minHold` (s), `density` (cuts per 10 s), `wordAnchor` (`key` or `off`), `length` (s), and `rhythm`: `medianHold` (s), `fastHold` (s) and `maxFastRun`, `holdPerSection` (s), `breaths` (`true`), and `register` (the brief's style words, quoted, when they ask for this shape) |
| `brand` | from the brand guide: `palette` (`name`, `hex`, `text`: false when the guide keeps the colour off text), `neutrals` (false only when the guide forbids plain black, white and see-through colours) and `fonts` (`family`, `role`, `file`). The plan reads it when held, so a change makes the plan and everything after it stale |
| `finish` | `export` (a full-quality export) or `conform` (from originals on the user's computer), and the aspect ratios. An older `proxy` means `export` |
| `footage`, `reference`, `taste` | what the log, the reference stage and the look read; a change here makes them stale |
| `look` | the look stage's choice, as edit-footage's `references/film-look.md` says: `board` (the reference stills it was chosen from, each with its `source` and `url`, or `open` with why; when there is nothing to read, one entry `{ "open": "<why>" }`), `spec` (what the board shows: blacks, highlights, palette, texture, light, captions, the second camera, the ending) and `check` (each item against the board, with a `verdict` of `pass`, `flag` or `open`). Written in the look stage, before it is marked done; a change afterwards makes the plan and everything after it stale. The critics are given its board |
| `format` | the reference's format, when one was read: layout, emphasis, captions, hook, end card, brand and feasibility, as the reel-structure skill's `references/format.md` says. The plan reads it, so a change makes the plan and everything after it stale |
| `sources` | per source: `url` or `file` (the original), `proxy` only for footage on the user's computer, `gyro` (`true` or `false`) with `gyroKind` (`sony-rtmd`, `gopro-gpmf`, `dji` or `insta360`) when its camera recorded motion data, `stabilised` with its `file` (a copy, never the original) `crop` (the zoom, 1 or more, that framing checks allow for) and `ranges`, each used range's choice at the conform (`in`, `out`, `use`: `stabilised` or `original`, and `shake`, the measurements `[plain, stabilised]`) once it is stabilised, which needs an approval with the scope `stabilise:gyro`, as the edit-on-your-computer skill says (the gyro probe's `maybe` is never kept; no stage counts `gyro`, `gyroKind` or `stabilised`, which are written after the log), and `ranges` with `in`, `out`, `verdict` (`pass`, `flag` or `open`), `method`, `confidence` (`high`, `low` or `none`) and `note`; `upright` (`yes`, `rot90`, `rot270`, `rot180` or `open`: which way is up, judged from a still, since some cameras write no rotation; no stage counts it either, so a source found turned after the log is turned with `invalidate <record> build`, never by redoing the log); and `reframe`, the saved and corrected reframe files, as the footage-reframing skill says |
| `takes` | the chosen take of each line |
| `story` | the story stage's beats: for footage with no words and no brief, the arc inferred from it. Never in `brief`, which intake reads: a change there would make every stage stale |
| `locked` | the meaning map: `phrase`, `job` (the picture's job), `shot`. Written when the user approves the map, at review with the first draft, so the approval leaves that draft current. A job changes only with an approval of it; a locked row changed then needs a new plan: `invalidate <record> plan` |
| `keepers` | what worked in a version the user saw: `kind` (`pair` with `phrase` and `shot`, `moment` with `shot`, `praise` with the user's `words`), `what`, `version`, and why it works |
| `versions` | `name`, `parent`, `plan`, `scene`, `render`, `changed`, `gates` |
| `openDecisions`, `pendingReviews`, `pendingSpends` | as `picsart-video-rules` defines them |

## What a stage marked by hand keeps

A stage marked done by hand keeps in its `reads` a copy of these keys: the ones it reads, and the
ones the stages it builds on read or wrote. When one has changed since, the stage is stale, so a revised
story or cut pace makes the plan and everything after it stale. `record.py` computes the same list (`hand_keys`).
A snapshot saved before it kept upstream reads lacks them, so such a stage counts as stale once and is redone.

| Stage | Keeps |
|---|---|
| `intake` | `brief`, `job` |
| `reference` | `reference`, `brief`, `job` |
| `proxies`, `log` | `footage`, `brief`, `job` |
| `takes` | `footage`, `sources`, `brief`, `job` |
| `look` | `taste`, `takes`, `footage`, `sources`, `brief`, `job`, `reference` |
| `story` | `takes`, `footage`, `sources`, `brief`, `job`, `reference` |
| `plan`, `build` | `cutPace`, `standing`, `format`, `brand` and `look` (when held), `taste`, `takes`, `footage`, `sources`, `brief`, `job`, `reference`, `story` |
| `qc`, `critics`, `review` | `standing`, `cutPace`, `format`, `brand` and `look` (when held), `taste`, `takes`, `footage`, `sources`, `brief`, `job`, `reference`, `story` |
| `finish`, `deliver` | `finish`, `locked`, `approvals`, `standing`, `cutPace`, `format`, `brand` and `look` (when held), `taste`, `takes`, `footage`, `sources`, `brief`, `job`, `reference`, `story` |

A job that leaves a stage out keeps what the stages before it read and wrote all the same. A reel or remix
job's stages also write their own keys, and a change to one makes what follows stale, whether the
stage was marked by hand or by `record.py`: `sheet` (reference), `moments` and `mapping` (story),
`route` and, for a job with no takes stage, `takes` (plan): their clip lists only, so the approved scene or render that review writes into a take leaves the build current.

## A record from a merged use case

`client-edit.json`, `cut-footage-into-reel.json` and `remix-reel-structure.json` are edit-footage
records now. `python3 scripts/record.py migrate <old record>` writes `edit-footage.json` beside it:
`useCase` renamed, every key kept (the brief's notes included), and each stage the old record shows
as done marked done by hand, so `status` resumes it where it stopped. Planned takes mark the plan
done, and the build only when every take has a scene or render URL; a remix sheet marks the reference done only
once the user approved it. Without commands, do the same by hand, as edit-footage's
`references/jobs.md` says.

## An example

```json
{
 "useCase": "edit-footage",
 "job": "broll-voiceover",
 "pipeline": ["intake", "reference", "proxies", "log", "takes", "look", "story", "plan", "build", "qc", "critics", "review", "finish", "deliver"],
 "stages": {"intake": {"status": "done", "at": "2026-11-04T10:02:00Z", "inputsHash": "3f1c…"}},
 "brief": {"said": {"format": "9:16", "length": "25-35 s"}, "read": {"voice": "the founder's own take"}, "assumed": {"destination": "Instagram Reels"}},
 "standing": [{"text": "all supplied footage is cleared", "words": "this is material that they give us", "date": "2026-11-03"}],
 "approvals": [{"what": "stabilise the handheld shots with gyro data", "by": "user", "date": "2026-11-03", "scope": "stabilise:gyro"}, {"what": "install the stabiliser", "by": "user", "date": "2026-11-03", "session": "Scope manager", "words": "install it", "scope": "install:stabiliser"}],
 "rejected": [{"what": "option C, the fast cut", "date": "2026-11-03"}],
 "cutPace": {"minHold": 1.4, "density": 3.5, "wordAnchor": "key", "length": 30},
 "finish": "conform",
 "sources": [{"file": "FX3_2394.MP4", "proxy": "proxy/FX3_2394.mp4", "gyro": true, "gyroKind": "sony-rtmd", "stabilised": {"file": "work/FX3_2394.stab.mov", "crop": 1.12, "ranges": [{"in": 0, "out": 4.0, "use": "stabilised", "shake": [2.1, 0.4]}]}, "ranges": [{"in": 0, "out": 4.0, "verdict": "open", "method": "template-track on the letterhead", "confidence": "none", "note": "plain paper, nothing to track"}]}],
 "locked": [{"phrase": "precision", "job": "hands on a keyboard, close", "shot": "FX3_2380 1.2-3.4"}],
 "keepers": [{"kind": "pair", "what": "the keyboard on precision", "version": "v1", "phrase": "precision", "shot": "FX3_2380 1.2-3.4", "why": "fingers on keys read as exactness"}, {"kind": "praise", "what": "the steadied close-ups", "version": "v2", "words": "the stabilization was really good"}],
 "versions": [{"name": "v1", "scene": "https://…/v1.json", "render": "https://…/v1.mp4", "changed": "first draft", "gates": {"qc": "2 major"}}],
 "openDecisions": []
}
```
