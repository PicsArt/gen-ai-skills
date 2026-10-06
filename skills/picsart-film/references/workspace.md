# Film — workspace and project folder

## The workspace — disk when you have it, the plan block always

When a filesystem is available, create a project directory (ask where, default CWD):

```
<film-slug>/
  film.json            the source of truth — see schema below
  docs/                story.md (the story document — ten lines, then every scene), breakdown.md, the shot list, generation log, DISCLOSURE.md at the end
  assets/              descriptor + reference-image records per asset
  prompts/             final prompt per video, versioned: r1_v3.md
  selects/scNN/        accepted take URLs + their prompts
  edit/  master/       cut records, export URLs, archive manifest
```

`docs/brief.md` is the **living project brief** — the one page a stranger (or a
fresh session) reads to direct this film correctly: logline, the world in three
sentences, the style prefix, who the characters are *as people*, the current
production block, and the standing decisions with their reasons ("hard cuts
only — the film is about abruptness"). Update it whenever a decision would
surprise someone reading only the script; on resume, read it before you say
where things stand. `film.json` holds the state; the brief holds the *intent*.

## The project folder — one film, one tree

**A film is a folder in the user's Drive, provisioned before anything is
generated.** Everything the project makes is persisted into it as it is made, so
nothing ever lives only on a CDN and the whole film is one folder to archive or
hand off. This is the first thing that happens after the idea is agreed — not a
cleanup step at the end:

```
Picsart Films/<film-slug>/
  Library/   locked asset sheets only — what the film is built from
  Assets/    every asset render and every iteration
  Shots/     takes, drafts, finals
  Exports/   masters
```

**Provision it in ONE call**, then never look it up again:

```
picsart_drive action=create_folder
  path: "Picsart Films/<film-slug>"
  children: ["Library", "Assets", "Shots", "Exports"]
```

`result.createdUid` is the project folder and `result.createdUids` maps each
child name to its uid — store all five in `film.json.drive` immediately. Missing
folders are created and existing ones reused, so re-running it after a resume
completes a half-built tree instead of duplicating it. From then on
`picsart_drive action=upload` goes straight into the right uid — never a
browse-`list` first "to find the folder" (each Drive call renders a UI block; a
save should render one receipt, not two stacked browsers). `action=list` is for
when the user actually wants to browse.

**Never show the whole Drive.** No `action=list` without a
`folderUid`, anywhere in the process — the root listing is the user's entire
Drive painted into the chat, and nothing in a film needs it. The provisioning
receipt renders the project folder itself with its four children (the tool
re-lists the folder it created, never its parent — a project folder's parent
IS the root); every
later Drive call renders the one folder the file landed in. Browsing is the
user's request, never a step.

**Then pass the uid on EVERY generation.** `picsart_generate` and
`picsart_job_status` both take `folderUid`, and it is the only thing that files
a render under its own film:

```
picsart_generate  … folderUid: <film.json.drive.shotsUid>   takes
picsart_generate  … folderUid: <film.json.drive.assetsUid>  asset renders
```

**Without it the render lands in a shared default folder outside the
project**, where every generation from every project piles up together — that
default exists for generations with no project to belong to, and a film
take is not one of them. This is the one place "provision once, never look it up
again" does not mean "never mention it again": the uid is in `film.json`, so it
costs nothing to read, and a call that omits it saves to the wrong place
silently.

**Video defaults to async, so the `folderUid` must be passed AGAIN to
`picsart_job_status`.** The job carries no memory of it. A take generated with a
folder and collected without one lands at the root anyway, and since takes are
video, that is the call that actually files most of a film.

**Persistence is silent, with exactly one exception.** Saving is your job, not a
topic. Never narrate the plumbing: no CDN hostnames, no "the result has no
`drive` block", no "`saveToDrive` was set but I'm not assuming it persisted", no
live-testing a path in front of the user. Do the save, verify it yourself, and
move on. If a file genuinely did not persist durably, the user hears one sentence
about the *consequence* — "this link expires, so I'm keeping the prompt to
re-make it" — and never the mechanism. A save that worked is worth zero words.

**The exception is the folder itself, said once.** Creating the project folder is
not plumbing — it is a new folder in *their* Drive, holding *their* film, and
where the work lives is theirs to know. So the provisioning call's receipt is
shown and left to speak for itself ("Created "Picsart Films/hold-it" in your
Picsart Drive. It has Library, Assets, Shots and Exports inside — everything
this project makes gets filed in them."), and if anything is added it is one
plain line at most: they can open it any time, and nothing else will be said
about saving again. Never repeat it per asset, per take, or per stage.

**Two destinations, and the difference is not durability — it is curation.**
Persistence happens at *generation*: every render lands in `Assets/` or `Shots/`
as it comes back — **because you passed `folderUid`**, which is what makes that
sentence true rather than aspirational. Promotion happens at *lock*: `picsart_save_asset` with
`status: "locked"` and the project uid files the sheet in `Library/`, which is
the index of what the film is actually built from. Earlier versions stay in
`Assets/`; the library is not a backup, and nothing is ever moved out of the
project.

One exception to plain uploads: **asset sheets save via `picsart_save_asset`,
never a plain upload** — that call writes the registry the library views read; a
sheet uploaded as a plain file is invisible to them (see `picsart-film-assets`).

Keep the film state in **`film.json`** — written to the workspace when there is
a disk, and updated whole (never a diff) at every milestone: gate passed, asset
locked, batch generated, review round, picture lock, export.

**Never print it in the conversation.** A screenful of fenced JSON is not a
status report — it is your bookkeeping, and it buries the one line the user
needed under sixty they cannot act on. It is also not how anything gets shown:
the shot list is shown by opening the shot list board, an asset by opening its
sheet, a cut by opening the scene editor. **A request to SEE something is a
request to open its board, never to print its data** — including the second
time, when the board has already been open once this session.

**And generated material arriving is itself the request.** A batch of takes
coming back, a sheet rendering, a retake completing — none of them waits to be
asked about. The board opens in the turn the material lands, because the
alternative is describing pixels the user could have been looking at, and a
description is where a verdict gets quietly self-issued: *"three of the four
check out clean"* is an approval nobody granted, written about frames nobody
saw. Say what you observed, open the board, and let the approval come from
them. The full routing is in `picsart-film-scenes` step 6.

There are exactly two moments the state may appear as JSON in chat:

- **On a surface with no disk, at the end of a working session** — once, so the
  next session can resume. Say what it is in one line ("paste this back to pick
  this film up") and never repeat it mid-flow.
- **When the user asks for it** — "show me the state", "give me the json".

Mid-flow, "where are we?" is answered by the map: the stage list with its gates
and the scene×assets matrix, as markdown tables, in the user's own vocabulary.
Everything a fresh session needs to rebuild the concrete work — every render,
every locked sheet, every take — is in the project's Drive folder already, so
what is lost without a state block is the narrative, not the film.

```json
{
  "film": "cully-hill-boys", "phase": "C", "stage": 6,
  "drive": { "projectUid": "<Picsart Films/cully-hill-boys — provisioned before anything is generated>",
             "libraryUid": "<Library — locked asset sheets land here>",
             "assetsUid": "<Assets — every asset render and iteration>",
             "shotsUid": "<Shots — takes>",
             "exportsUid": "<Exports — masters>" },
  "target": { "duration": 120, "aspectRatio": "16:9", "finalResolution": "1080p" },
  "story": { "who": "Cal, who owes; Tobin, who holds the deed", "where": "the garage, closing time",
             "wants": "Cal: Tobin's signature. Tobin: to keep working", "against": "the buyer comes tomorrow",
             "happens": ["Cal accuses", "Tobin keeps working", "Tobin sets the wrench down"],
             "peak": "Tobin sets the wrench down",
             "ends": "the deed signed on the bench",
             "says": "the thing they nearly split over was never the point",
             "fixed": ["both keep the garage"], "genre": "drama" },
  "shoot": { "ceilingSec": 30, "editModel": "<the picked model's edit sibling>",
             "extendModel": "<the picked model's extend sibling>" },
  "runs": [
    { "id": "r1", "scenes": ["sc01", "sc02"], "shots": ["12A", "12B", "12C", "13A"],
      "genSec": 28, "join": "ends as Cal's hand closes on the wrench; r2 opens on the wrench from close in",
      "cutTimes": [5, 13, 19], "cutTimesActual": [5.2, 12.8, 19.1],
      "refs": ["https://…sc01_12A_start.jpg",
               "https://…view_cal_identity_v1.jpg", "https://…view_cal_wardrobe_v1.jpg",
               "https://…view_tobin_identity_v1.jpg", "https://…view_tobin_wardrobe_v1.jpg",
               "https://…plate_wrench_v1.jpg",
               "https://…sc01_scene.jpg", "https://…garage_day_map.jpg", "https://…sc01_wide.jpg"],
      "refRoles": ["START FRAME", "IDENTITY @cal", "WARDROBE @cal", "IDENTITY @tobin", "WARDROBE @tobin",
                   "PROP the wrench", "SCENE PICTURE", "SPACE map", "SPACE wide"],
      "promptVersion": "v3", "takes": 2, "editPasses": 1, "extends": 1,
      "pieces": [
        { "url": "https://…run-r1-take2-edit1.mp4", "from": 0, "to": 28, "promptVersion": "v3",
          "call": "edit", "note": "cut 3: mug is white ceramic" },
        { "url": "https://…run-r1-extend1.mp4", "from": 28, "to": 34, "promptVersion": "v4",
          "call": "extend", "note": "13A holds two more seconds on Tobin" }
      ],
      "select": { "url": "https://…", "jobId": "job_…" } }
  ],
  "model": { "id": "<the video model the user picked on picsart_model_choice — a version id, recorded once>",
             "draftResolution": "480p",
             "pictures": { "people": "<live 4K-capable scene-image model id selected at Stage 4>",
                           "map": "<newest GPT Image id>", "vintage": "<newest GPT Image id>",
                           "modern": "<newest Nano Banana id>" } },
  "banDictionary": { "dark": "low key", "jolting": "rapid motion" },
  "gates": { "1": "passed", "2": "passed", "3": "passed", "4": "passed",
             "5": "passed", "6": null },
  "voicePolicy": "native",
  "blocked_on": null, "attempts": {},
  "bible": { "stylePrefix": "<verbatim — pasted into every prompt of this world>",
             "palette": { "dominant": "amber lamplight on old plaster",
                          "secondary": "burnt-orange rust and oiled timber",
                          "accent": "lime-green enamel",
                          "accentBelongsTo": "the brothers' car" },
             "setup": { "genre": "drama", "tone": "auto", "palette": "auto",
                        "scheme": "analogous", "hue": "amber", "hueDegrees": 60,
                        "ratio": "169", "camera": "35mm", "lens": "ana" } },
  "assets": [
    { "tag": "@cal", "type": "character", "version": "v1", "status": "locked",
      "descriptor": "<verbatim — the sheet's prompt and this record; never pasted into a video prompt>",
      "portrait": "https://…portrait_cal_v1.jpg", "profile": "https://…profile_cal_v1.jpg",
      "sheet": "https://…sheet_cal_v1.jpg",
      "grid": "T-cut triptych at the model's top resolution: left column two stacked face panels, right tall full-body panel; a states row below",
      "panels": ["1 front face (top-left)", "2 side face (bottom-left)", "3 full body front (right tall)",
                 "4 @cal_wet (states row)"],
      "views": [
        { "id": "identity", "source": "portrait, head to neck", "box": [512, 0, 1024, 1536], "delivered": [1024, 1536],
          "url": "https://…view_cal_identity_v1.jpg", "bytes": 291204 },
        { "id": "profile", "source": "profile, head to neck", "box": [512, 0, 1024, 1536], "delivered": [1024, 1536],
          "url": "https://…view_cal_profile_v1.jpg", "bytes": 240310 },
        { "id": "wardrobe", "panel": "3 full body front", "position": "right tall",
          "box": [1024, 0, 1024, 2048], "delivered": [1024, 2048],
          "url": "https://…view_cal_wardrobe_v1.jpg", "bytes": 188440 },
        { "id": "wet", "panel": "4 @cal_wet", "position": "states row",
          "box": [0, 2048, 1024, 1024], "delivered": [1024, 1024],
          "url": "https://…view_cal_wet_v1.jpg", "bytes": 164880 }],
      "variants": ["@cal_wet"], "scenes": ["sc01", "sc02"],
      "blocking": { "asOf": "sc01",
                    "left": "on foot, frame-right, walking away from the bench",
                    "exit": "frame-right" },
      "voice": "low, unhurried, faint valley accent" },
    { "tag": "@maya", "type": "character", "source": "user", "version": "v1", "status": "locked",
      "original": "https://…maya_portrait.jpg",
      "sheet": "https://…sheet_maya_v1.jpg",
      "grid": "2046×1024; 1 row × 3 equal cols",
      "panels": ["profile (leftmost)", "back (centre)", "@maya_coat_off (rightmost)"],
      "views": [
        { "id": "coat_off", "panel": "@maya_coat_off", "position": "panel 3 of 3, rightmost",
          "box": [1364, 0, 682, 1024], "url": "https://…view_maya_coatoff_v1.jpg", "bytes": 64200 }],
      "derived": [{ "url": "https://…maya_portrait_q85.jpg", "op": "jpeg q85 — run budget" }],
      "descriptor": "<minimal — written from the photo; costume only where a scene departs from it>",
      "scenes": ["sc02"] },
    { "tag": "@garage", "type": "location", "version": "v1", "status": "locked",
      "descriptor": "<verbatim — architecture, materials, the anchor object, one light, the palette line>",
      "views": [
        { "id": "map", "url": "https://…garage_day_map.jpg", "madeFrom": "sc01.pictures.wide",
          "sides": { "A": "shelving wall", "B": "roller door", "C": "bench wall", "D": "tarp wall" } },
        { "id": "wide", "url": "https://…sc01_wide.jpg" }],
      "scenes": ["sc01", "sc02"] }
  ],
  "scenes": [
    { "id": "sc01", "slug": "EXT. GARAGE — DAY", "status": "selects-complete",
      "locationMap": "<verbatim spatial map, pasted into every prompt of the scene — with the room map's sides: Side A the shelving wall, …>",
      "pictures": { "scene": "https://…sc01_scene.jpg", "wide": "https://…sc01_wide.jpg",
                    "wrecked": [{ "angle": "WS", "fromRun": "r1", "at": 27.4, "url": "https://…r1_f27.4.png" }] },
      "shots": [
        { "id": "12A", "status": "final", "duration": 5, "run": "r1",
          "refs": [1, 2, 3, 4, 5, 6, 7, 8, 9],
          "design": { "move": "slow push-in", "size": "MS", "fov": "40°",
                      "aperture": "f/4", "lighting": "window",
                      "tailHold": 1.2, "slowReason": "emotional pause",
                      "acting": { "@cal": "anger·2, hides fear, gaze on Tobin" } },
          "picture": "scene",
          "trim": { "in": 0.6, "out": 5.1 }, "trimSource": "user" }
      ] }
  ],
  "review": { "round": 1, "lastFeedbackSummary": "…" },
  "credits": { "spentEstimate": 320, "nextActionQuote": 45 }
}
```

Why the awkward fields: `descriptor` and `stylePrefix` are **verbatim** because
consistency dies the day someone shortens them; `bible.setup` holds the console's
**preset ids** (what the user chose) while `bible.palette` holds the *resolved*
colours — the scheme and hue written as colours plus what carries them
(`presets-looks.md`, *Colour*), absent when the scheme is Auto — plus
`accentBelongsTo` — the one thing that owns the accent, which the
console does not ask and you decide while designing the assets; `trim` is an
**edit-time fact recorded on the shot** — a keep-window in source seconds, and
for a shot inside a run the source is its **piece** — the run's file, or the
regenerated segment that replaced part of it (`runs[].pieces`) — so
the window is in that file's seconds (12B's is `{in: 5.4, out: 12.6}` on the run
file, not `{0.2, 7.4}`): every shot of a piece is a clip in the scene sharing one
url with a different window, which is how the scene editor
already works — so a
trim does not lose itself between the scene editor and the assembly, and
**`trimSource` says where the window came from** — the only value written is
`user` (they moved it in the scene editor), because a run arrives already cut by
the model and there is no automatic rough cut. Nothing automatic touches a
window: recomputing over somebody's own edit is how a helpful default becomes an
argument. A camera change is a retake, never a trim;
`shoot.ceilingSec` is
the model's live max duration, read from `picsart_model_params` once at the model
pick so the run pass has a number to close runs against, and `shoot.editModel` /
`shoot.extendModel` are the siblings an edit or an extend call goes to
(`picsart-film-scenes` step 5); `runs[]` is top-level because a
run spans scenes (as much of the film as fits the ceiling is one
multi-shot generation, and there are no per-shot exceptions) and it is what
actually got bought: which shots, the planned `cutTimes` and the
`cutTimesActual` the delivered take was split at (the model cuts near the plan,
not on it, and every trim downstream hangs off the real numbers), `refs` — the
ordered images the call carried in `imageUrls`, with `refRoles` saying what
the tagging header told the model each one is (a face, an outfit, `START FRAME`,
`FRAME REFERENCE for shot N`, `SPACE` — the `startFrame` field stays empty and
the role travels in words), which every shot block numbers against, so a shot's
`refs` are indices into it — one `promptVersion`, `takes`
and `editPasses` per run, and one `select`; each shot points back with `run`,
keeps its composed `still` when one was requested (an animatic panel if one
was watched, and in `refs` its labelled `START FRAME` or `FRAME REFERENCE`); `locationMap` lives on the scene
because it is written once and pasted into every prompt unchanged; `design` stores
preset names, not prose, so a change is one field and the recompiled prompt differs
in exactly one block. A shot over 8 s carries its reason in `design.durationReason`, one line.
**`blocking` is the one piece of character state that
crosses a scene boundary** — where they were left and which side of frame they
went out — because `locationMap` fixes geography only *within* a scene and
nothing else carries a heading out of one: a character who exits frame-right and
enters the next scene frame-right has quietly broken the geography, and it is
the continuity error viewers feel without being able to name. Note what it is
NOT: wardrobe, damage and wetness are **not** recorded here, because a state
change is a tagged panel with its own view (`overview.md`, rule 2) and a field
holding "now soaked" would compete with `@cal_wet` for the truth. `stressTest`
is not required: the save tool locks on the review-board approval, and no row
carries a battery. Statuses: assets
`draft → review → locked`; shots
`planned → drafting → iterating → final`; a shot regenerated after picture lock gets
a new `promptVersion`, never an edit in place. **`story` is the ten lines the user said yes to, and `docs/story.md` holds
every scene as what we see and hear**
(`../../picsart-film-development/references/dramaturgy.md`); `runs[]` is seeded by the Stage 1
video plan (`id`, `scenes`, `genSec`, `join`) and filled in Stage 6. The shotlist board
owns a card's action, line, tags, values and order; `design`, `refs`, `run` and
`trim` stay on the shot by id (`widget-feedback.md`).
