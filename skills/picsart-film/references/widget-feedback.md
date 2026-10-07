# Reading the film boards' feedback

Read the submitted decision from the current message and attached widget context; use a context-reading tool only when exposed by the host. Follow the [host conventions](../../picsart-workflows/references/host-conventions.md). After opening a board, wait for the user's decision. If the payload is inaccessible, use the text fallback and preserve the feedback fields documented below.

The same silent channel also carries **work-in-progress state** while the user
is still marking things up, so a typed "go with the second one" can usually be
resolved without a send. In-progress state is never a decision. It stops
updating once a board is sent, so the payload of a send is never overwritten by
a half-finished markup behind it.

**A board is the whole turn. Send no prose with it — none above, none below.**
Not a preamble, not a summary of what is on it, not "let me know what you
think". Every board states its own ask: it has a header, a count, a hint line
and one button. Prose repeating that ask puts a second call to action beside the
first — the user is now looking at a text box and a button that want the same
decision, and the usual outcome is that they type what the board was built to
collect, which is the one thing this doc already tells you not to invite.

Anything the user genuinely needs to know before deciding belongs **inside** the
board, in the field that exists for it (`note` on the shot list, `purpose` and
`notes` on the scene editor, `judge` where a board has one) — never in a chat
message wrapped around it.

**Speak after they act.** Their feedback message is the cue: the readback, what
it changed, the cost, the next step all go there. That is also the only place a
readback is worth anything, because until they press the button there is nothing
to read back.

The single exception is a hard blocker: if the board cannot be rendered at all,
say so in one line and fall back.

**One board per decision set — and queue discipline when there are several.**
Things decided together go on ONE board (a batch of takes = one scene editor
carrying the whole film; a planning pass = one shotlist board with all scenes). Never open parallel boards that each demand
a send: the first send moves the conversation forward and the other boards die
unanswered. When several
boards ARE legitimately open (a review queue), one board's feedback is **one
item, not a green light** — act on it, return to the queue, and advance the
pipeline only when the queue is empty or the user says move on.

**Suggested prefills.** `picsart_film_setup` takes a `suggested` input:
your inferences from the material, with a one-line why each. Fill it before
every call with what the script already answers, so the console opens on the
material rather than on its defaults. `current` (previously locked state) always
wins over `suggested`. The film-setup console **applies suggestions silently**
and validates every id against its own options, dropping what it does not
recognise — so pass only what the material really decides: a wrong prefill reads
to the user as a decision someone already made. The feedback payloads below are
unchanged by this: what comes back is what the user confirmed, however it was
seeded.

Every payload carries `type` and `version`. If `version` differs from the one
in the example below, read the block on its own terms. The contracts for
`model_choice_feedback` (the Stage 1 model pick) and `asset_review_feedback`
are documented in `review-feedback.md` beside this file and used unchanged here,
with one film-only addition: an `approved` asset is archived with
`picsart_save_asset`, carrying `projectFolderUid`, as **`locked`, with no
`stressTest`** — the approval is the lock. See `picsart-film-assets` step 4.

## `scene_editor_feedback`

The scene editor (`picsart_scene_editor`) is where takes and cuts are
reviewed. It opens on the scene document you pass as `scene` (a film with
exactly one video may pass `videoUrl` instead), plays it in the user's browser,
and lets them trim, split, delete, duplicate, adjust, change speed, effects,
volume and size, pin comments on the picture and mark stretches of the
timeline. **It is free and renders nothing** — no file, no credits, no
`videoUrl` in the reply. It has one send button, labelled **Accept** until the
user edits or comments and **Submit** once they do, and it sends this when they
press it:

```json
{
  "type": "scene_editor_feedback",
  "version": 1,
  "title": "Cully Hill Boys — sc01 to sc03",
  "duration": 21.4,
  "verdict": "needs_changes",
  "edited": true,
  "stateHash": "9f2c41d0",
  "document": { "…": "the whole scene document, as the user left it" },
  "comments": [
    { "id": "c1", "instruction": "five fingers on his left hand here", "time": 14.6,
      "scenePoint": { "x": 312, "y": 260 }, "layerId": "clip-3",
      "layerPoint": { "x": 0.41, "y": 0.62 },
      "createdAt": 1790000000000, "updatedAt": 1790000000000 }
  ],
  "timelineComments": [
    { "id": "t1", "text": "the push-in is too fast here, make it a slow creep",
      "start": 8.2, "end": 11.0,
      "createdAt": 1790000000000, "updatedAt": 1790000000000 }
  ]
}
```

Every field:

- **`type`** / **`version`** — `scene_editor_feedback`, `1`.
- **`title`** — echoes the `title` you opened it with.
- **`verdict`** — `approved` | `needs_changes`.
- **`edited`** — whether the user committed any edit at all.
- **`document`** — the scene as they left it, their edits applied. When
  `edited` is true it supersedes the scene you opened.
- **`stateHash`** names the committed edit. Record it beside the cut in
  `film.json`: reopening the same state round-trips as the same edit, not a new
  one.
- **`duration`** is the scene's length as the engine resolved it — the cut's
  real running time, and what the ±10% runtime gate reads.
- **`comments`** are pins on the picture: `instruction` (the user's words),
  `time` (seconds on the scene's timeline), `scenePoint`, and `layerId` — the
  clip under the pin, `null` on a bare frame spot — with `layerPoint` inside it.
  A comment with several spots also carries `targets`, every spot in order.
- **`timelineComments`** are marked stretches: `text` (the user's words) and
  `start`/`end` in seconds on the scene's timeline. `start === end` is a note on
  one frame.
- There is no general comment field. The comment sets are the whole of what
  the user wrote.

How to act on it — the verdict, the spend rules, the camera-change retake, kept
frames and mapping a time back to a shot — is in `review-feedback.md`
(`scene_editor_feedback`). The film's deltas:

- **`document` is the cut the user already made.** Its clips, in playback order —
  the clips of the montage's `track` layer, or top-level media layers in a scene
  built by hand — are the pieces: each over a source file with `content.trim`
  in that file's seconds. Write each window to its shot's `trim` with
  `trimSource: "user"`, record `stateHash` beside the cut, and carry `document`
  forward as the film's scene. Nothing is rendered to realise it: the next
  round reopens the editor on `document` itself, whose clips still reach into
  the whole source, so a shot trimmed a second too short can still be opened
  back up. Render with `picsart_media_export` only when a file is wanted — the
  settled cut, not every round. The originals in `Shots/` are never moved,
  overwritten or deleted. `picsart-film-edit` carries the sequence.
- **One editor carrying the whole film, not one per piece.** The
  user has just watched this picture and cut it themselves; opening the editor
  for each resulting piece shows them their own edit N times over. Record the
  cut, say in one line what changed, and open the editor again only when the
  picture contains something they have **not** seen — a regenerated shot
  spliced in, an edit or extend that came back. Then it is one editor on the
  **whole cut** in playback order, never a single clip and never several at
  once.
- **Every retake is seen inside the cut.** A retake — like an edit or extend
  return — goes **into the cut**, the scene is rebuilt, and the whole cut goes
  back up with the changed seconds said in a line. The scene is one timeline,
  never several takes side by side. Every superseded url stays in the log, so
  going back to an earlier take is one call and no credits. `picsart-film-scenes` step 6
  carries the routing.

## `film_setup_feedback`

The console runs before the story and shot list. Its submitted v3 payload is:

```json
{
  "type": "film_setup_feedback", "version": 3,
  "world": "main",
  "selections": {
    "genre": "drama", "tone": "auto", "palette": "auto",
    "scheme": "analogous", "hue": "amber", "hueDegrees": 60,
    "ratio": "169", "duration": "90", "camera": "35mm", "lens": "ana"
  },
  "stylePrefix": "<the compiled prefix, verbatim>",
  "summary": "Drama · analogous around amber — 35mm film, Anamorphic, 16:9 · 1 min 30 sec.",
  "verdict": "locked"
}
```

- Store `stylePrefix` verbatim in `bible.stylePrefix`, selections in `bible.setup`,
  and `Number(selections.duration)` in `film.json.target.duration`. Keep the
  returned summary for readback. The submitted `locked` verdict is the look's
  lock; an initial tool result or unsent widget state is only a preview.
- If the prefix is empty, compile the accepted selections with
  `picsart_film_compile_prompt`, `kind: "look"`; map `ratio` to `look.frame`.
- Colour is `scheme` plus the optional hue. `palette` is always `auto` here;
  each shot may choose its own palette. With scheme Auto, the console omits
  `scheme`, `hue` and `hueDegrees`. With a scheme selected but no hue selected,
  keep the scheme without inventing a hue. Preserve both hue fields exactly
  when present: `green` + `130` reopens at 130°, not at green's 120° anchor.
- Pass `look.scheme` / `look.hue` inside `look` to
  `picsart_film_compile_prompt`. Pass top-level `scheme` / `hue` to
  `picsart_film_compile_asset_prompt`, which has no `look` object and silently
  drops one. Neither compiler consumes `hueDegrees`.
- A tone is `auto`, `italian60`, `american80`, `summer80`, `hongkong80`,
  `neonhk90`, `american90`, `imax`, or `custom`. It seeds camera and lens only.
  Changing camera or lens resets tone to Auto; changing colour does not.
  Seed tone before any explicitly requested rig values.
- A custom genre is `genre: "custom"` plus `customGenre` on the console.
  For the scene/look compiler, pass `look.customGenre` and omit `look.genre`;
  its enum does not accept `custom`. A custom tone uses `look.tone: "custom"`
  plus `look.customTone`. Use each tool's own exposed schema; the asset tool
  has a separate top-level contract.
- Colour reference images are handled from chat, outside the console. Inspect
  them for colour only; keep the durable URL with the bible, and pass
  `look.paletteReference: true` plus `look.customPalette` when there is wording
  to the scene/look compiler. Supply the image to generation only when the
  model supports a colour reference distinct from identity. Reuse a confirmed
  Drive copy; removing the reference from the look does not delete that file.
- Focal length, aperture, light, shot length and camera move are per shot.
  The console sends no `focal`, `aperture`, `light`, `shotlen`, `move`,
  `grain`, `shot` or `pace` keys; grain rides in camera stock. The console
  also sends no `handles`; preserve the film's existing handle policy
  independently of this feedback.
- `ratio` is `169`, `43`, `sq`, `34` or `vert`; filter models against it.
  Suggested ratios also accept labels and words (`9:16`, `vertical`, `tiktok`).
- Reopen with `current.selections`, which wins over suggestions. One setup is
  stored per world. Decide what carries the accent when designing assets;
  the scheme determines hue relationships, not objects. Resolve `bible.palette`
  per `presets-looks.md`; with scheme Auto use each location's own colours.
- Keep a locked `bible.stylePrefix` verbatim until the user reopens the
  console and changes the look.

## `asset_review_feedback`

Shape and rules in `review-feedback.md` beside this file:
`total`, `approved[]`, `changes[]`, no `verdict`, and the invariant
`approved.length + changes.length === total`. The film-only parts:

- **Each `approved` entry is LOCKED immediately** —
  `picsart_save_asset`, one call per asset, `status: "locked"`, no
  `stressTest`. The approval is the lock for every asset, and there is no
  further review step. Batch the calls into one report, not
  one message per asset, and read `locked` in each result.
- **The tile carries the descriptor.** Pass it as `prompt` and its key lines as
  `info`, so a note on a tile is a note on one descriptor line or one panel.
- **Each `changes` entry is one regeneration, its `note` folded into that asset's
  own prompt and nothing else touched.** Then a fresh board with only those,
  `version` bumped and `previousUrl` set. Approved assets never reappear on a
  board.
- One board carries a whole scene block's assets, deduped — so one send settles
  a batch, and a lead is reviewed once rather than once per scene.
- **A user's own photo is never a tile.** They gave it; it is locked on save.
  Only a sheet generated *from* the photo comes to the board, with the judge
  line *"the same person as the photo — face, build. Ignore the pose."*
- **This is the film's only asset board.** Descriptor edits, a narrator's
  voice pick and any "show me the face again" happen in chat.

## `shotlist_board_feedback`

```json
{
  "type": "shotlist_board_feedback", "version": 3,
  "scope": ["sc01"], "verdict": "approved",
  "scenes": [
    { "scene": "sc01", "slug": "INT. GARAGE — DAY",
      "order": ["12A", "12C", "12A′"], "cut": ["12B"], "reordered": true,
      "shots": [
        { "id": "12A", "action": "Cal stops on the threshold.",
          "tags": "@cal @garage_day",
          "values": { "size": "WS", "move": "locked off", "lens": "54°",
                      "aperture": "auto", "light": "window", "palette": "slate",
                      "sec": "8" },
          "recap": "Wide · Locked off · 35mm · 8s" },
        { "id": "12B", "action": "…", "values": { }, "recap": "…", "cut": true },
        { "id": "12C", "action": "Tobin goes still before he answers.",
          "values": { }, "recap": "…", "edited": true },
        { "id": "12A′", "action": "", "values": { }, "recap": "…", "added": true }
      ] }
  ]
}
```

- **Each scene's `shots` is the FINAL list** — every shot, every one of its seven
  values, in `order`. **Replace what the board owns with it wholesale — `action`,
  `line`, `tags`, `values`, `order`, `cut` / `added` / `edited` — never merge
  those field by field.** The board is where the plan is written rather than
  annotated, so it sends the finished list. What the board never carried stays on the shot by id: `design`,
  `refs`, `run`, `trim`. A changed `action` that tells a different story than
  the story's paragraph is a story note: the paragraph in `docs/story.md` is
  rewritten and shown for the yes, then the cards are rebuilt from it — never a
  prompt edit, and never another board in reply (`picsart-film-development`).
- **`scope` is the law of the payload**: the approval covers exactly the scenes
  it names — all of them, none beyond. It approves the **list**, not the spend:
  each dispatch is quoted with `picsart_preflight` in chat and waits for its own
  yes (`picsart-film-scenes`).
- One board carries **all scenes of a planning pass** (`scenes` on the tool
  call), so one approval covers the set.
- `verdict` is always `approved` — the board has one button. Edits are not
  objections, they are the plan.
- **Every shared vocabulary is one library.** The board's moves, sizes, lens
  anchors and lights are the same lists `picsart_film_compile_prompt` compiles,
  and the same ones [presets-camera.md](../../picsart-film-scenes/references/presets-camera.md),
  [presets-lighting.md](../../picsart-film-scenes/references/presets-lighting.md) and
  [presets-acting.md](../../picsart-film-scenes/references/presets-acting.md) define — so a plan and the board that renders it mean the same thing by the
  same word. Send the ids the board's own schema lists (`top-down` is accepted
  for the `overhead` height); what comes back is always the canonical id.

  `ots` as a *size* does **not** resolve, on purpose: it names an arrangement,
  and `arrangement` is where it goes.
- **Every shot carries TWO durations, and they are different numbers.**
  `values.sec` is the CUT length — what the animatic holds and what the ±10%
  runtime gate measures. `genSec` is the GENERATION length — `sec` plus a handle
  at each end, snapped **up** to a duration the model offers. **Generate at
  `genSec`, then trim to `sec`.** Two numbers are what make "generate long, cut
  short" possible: lengthening a take to buy trim room leaves the animatic and
  the runtime gate untouched.

  `genSec === sec` means this shot has no handles — either the film turned them
  off (`handles: "off"` on the tool call) or the card did (`values.handles`).
  Never assume the handle is 2s: snapping to the model's ladder can give more,
  and at the ceiling it gives less. Derive it as `(genSec − sec) / 2`.
- **A preset id is a KEY, not prose.** Every id below names one line of
  compiled text in a reference file, and that line is the hint you were waiting
  for: **look it up and paste it into the block verbatim**, resolving only its
  `<placeholders>` from the scene. Do not paraphrase it, do not "improve" it,
  and do not write your own sentence about the light or the move because the id
  reads self-explanatory. The whole point of the console is that what the user
  saw is what gets compiled — `light: 'firelight'` means one specific sentence
  about a low flickering source below the eyeline and what it does to the far
  side of the face, and nothing else. The user picked it from a picture of that
  sentence. `picsart_film_compile_prompt` is what turns the id into it.
- `values` are preset ids, the **seven the board asks** always present:
  `size` establishing|EWS|WS|MWS|MS|MCU|CU|ECU|detail — a DISTANCE only ·
  `move` a camera-move id from
  `../../picsart-film-scenes/references/presets-camera.md` (`locked off`, `slow push-in`,
  `orbit`, `whip pan`, `time-lapse`, …) ·
  `lens` as its field of view, eleven anchors
  10°|15°|20°|24°|31°|40°|54°|65°|74°|90°|104° (200mm down to 14mm) ·
  `aperture` auto|f/1.4|f/4|f/11, set per shot (`auto` compiles to nothing) ·
  `light` any of the **seventeen setups** in `../../picsart-film-scenes/references/presets-lighting.md`
  (auto|window|practicals|night practical|work light|firelight|silhouette|
  contre-jour|overhead fall|soft cross|overcast|golden hour|blue hour|
  open shade|dappled shade|street light|moonlight — the last six are the
  exterior row), or `custom` with up to three positioned `lights` ·
  `palette` one of the **seventeen palette preset ids** (slate…ink, in
  `presets-looks.md`), opening on the `filmPalette` you pass ·
  `sec` one of the durations the `model` you passed accepts — pass `model` on
  the call so a card cannot hold a length the model refuses. There is no
  `pace`: a value passed under that key is dropped, not displayed.
  A value you passed that the board has no preset for **comes back unchanged** —
  it is displayed verbatim and never snapped to a neighbour.
- `arrangement`, `height` and `handles` are **pass-throughs, not controls.** The
  board has no pills for them — an arrangement and a camera height are decisions
  the plan makes, not adjectives a card carries — so they come back only if you
  sent them, resolved through their alias maps (`top-down` → `overhead`) but
  never asked about. Absent means the user was never given the chance to change
  what you sent, not that they cleared it.
- **The board lists only the camera moves that have a preview clip** — a tile
  that plays the move teaches it, a 30px arrow does not. The vocabulary is all
  50 ids: every one resolves, a plan written against one of the unpreviewed
  moves comes back carrying it, and
  the pill shows an unknown value as itself. So do not read a short move list as
  the library having shrunk, and do not rewrite a shot's move because the board
  could not offer it back.
- Per-shot flags, at most one each: **`cut`** — dropped from the scene, generate
  nothing for it, and it stays out of `order`. **`added`** — created on the board,
  so it has no prompt history and needs one written from scratch. **`edited`** —
  differs from what you passed.
- `recap` is the board's own one-line readback of the five decisions that matter
  at a glance. Quote it back rather than reassembling it from ids.
- `reordered` compares only the shots that survived, so cutting a middle shot is
  reported as a cut and not also as a move.

**Take review is not on this board.** This board plans; a take is judged in
the scene editor (`picsart_scene_editor`), which owns the verdict, the user's own
trims and splits, and the comments that direct another take. Do not look for a take verdict here.

## `render_monitor_feedback`

```json
{
  "type": "render_monitor_feedback", "version": 1,
  "title": "sc01 drafts",
  "done": [
    { "label": "1A", "model": "<the film's video model>", "url": "https://…", "jobId": "job_…" }
  ],
  "failed": [
    { "label": "1B", "model": "<the film's video model>", "error": "FAILED" }
  ],
  "generalComment": null
}
```

- The monitor polls `picsart_job_status` itself and sends this **automatically
  when every job reaches a terminal state** (the user can also send early).
  Do not ask the user to ping you when it is done — the message wakes you; act
  on it: log `done[]` takes into the plan (URLs expire — Drive what matters),
  and regenerate only `failed[]`.
- A monitor left open with jobs still running publishes silent progress
  context; as everywhere, that is awareness, not a decision.

## When the boards are not available

Every board has a working text form and the flow must not stall without widgets:
the shotlist renders as a markdown table (so does the pipeline map, which has no
board); setup, shot design, and acting
run as the host's question interface menus built from the `presets-*.md` files (previews = the
compiled fragment text); asset sheets show reference images inline with the
descriptor as a numbered list so edits can name a line. Keep the same JSON
bookkeeping in `film.json` either way — the state schema does not know whether a
widget or a question produced the decision.
