# Film scenes — step 2, shot design

## Step 2 — design the shot on its card, then assemble the prompt

**The card is the design surface, and it arrives filled in.** Every shot's six
decisions — size, camera move, lens, light, colour, length — plus its
arrangement and camera height are pills on its card on `picsart_shotlist_board`,
each opening a picture rather than a list. **A pill the user changes is written
into that shot's block; a light left as seeded writes nothing, but lens and
aperture reach every shot, seeded or changed, and so does a palette other than
`auto`** (`prompt-blocks.md`, Part 2, *The card's own picks*).
A choice made on the board is never a choice the model did not hear. **Seed them before the board opens**,
from what is already decided (the story's action, the scene location's light,
the world defaults' register, the run's model), so the user touches only what they
disagree with; nothing forces a stop, in either pace. Shot design is the board
plus the camera, lighting and acting presets: there is no console behind a row
and no separate design panel to open per scene. Without boards, the same rule: state the
seeded design in one line and the host's question interface only what the card leaves open,
from `presets-camera.md`, `presets-lighting.md`,
`presets-acting.md`. Both paths return preset names plus their compiled text
fragments. World defaults come from the bible's setup; the shot stores only its
deviations (`design` on the shot in `film.json`).

**The scene's pictures are step 3, always.** A shot's frame is not composed
here on request: every scene gets the handbook's set of
pictures before its run — the scene picture the run opens on, the wide, the
room map — on one board for all scenes (step 3).
A user who asks "show me how the opening looks" is shown that board.

**A fragment is the start of the Camera block, not the whole of it.** A model
renders a described *picture* and ignores a stated *quantity*. So paste the
fragment, then make sure the block ends on the arrival as an image, name the set
as rigid if the camera travels through it, and — for any move that ends on a
changed aspect — say that the camera does the turning. `presets-camera.md`'s
"Getting a model to actually do the move" carries the rules and what each one
cost to learn.

**The board holds choices; the numbers behind them are yours.** Several blocks
want a quantity where the card holds a word — the Kelvin behind `warm`, the
km/h behind a moving car, the fog density behind a foggy street, the ratio
between two things of different size. **None of them becomes a pill.** The
console's job is a decision with a picture behind it, and nobody can judge 5200
against 5600 from a chip; a board that asks would be the form this pipeline
keeps trying not to be. Resolve each from what the user already chose plus the
scene's location and time of day, write it into its block, and do not raise it
in chat either unless it is genuinely in question. `prompt-blocks.md` blocks 8,
9 and 10 carry the rules and the tables.

**A slow shot names which kind of slow it is.** There is no tempo setting
anywhere. Models render
described pictures and ignore stated qualities, so rhythm is written, never
stated: the shot block's action and the card's `sec` carry it, and tempo
words (slow, calm, measured, brisk, urgent) do not appear in a header. A shot
that should feel slow has less happening in more seconds, and it records
`design.slowReason`, from four:

| `slowReason` | What it is | How it reaches the shot |
|---|---|---|
| `anti-tempo` | slow *against* the scene around it, for contrast | real time; the neighbours carry the contrast, so it is a cut decision as much as a shot one |
| `hero reveal` | the thing itself deserves the seconds | **not generated slow** — generated at normal speed and ramped at the edit, because a model asked for slow motion smears instead of slowing |
| `breath` | the film needs air after a heavy beat | real time, minimal action, usually paired with a `tailHold` |
| `emotional pause` | a face working, nothing else happening | real time; the seconds go to the acting, not to the action lines |

The value is not decoration: three of the four are real-time shots whose slowness
comes from *having less happen*, and one is a post effect that should never be
asked of the generator. A card that just says "slow" gets whichever the model
guesses.

**Generate one size wide when the shot can afford it.** A take framed one
shot-size wider than the card's intent gives the edit spatial trim room —
virtual reframes, subtle push-ins, and composition fixes are then free crop
moves instead of retakes. Skip this on faces at CU and tighter (resolution is
the budget; a crop spends it).

**Generate one beat long, for the same reason.** Two numbers, not one:

- `sec` is the **cut length** — how long the shot runs in the film. It is what
  the ±10% runtime gate measures and what the dialogue rule computes.
  Unchanged.
- `genSec` is the **generation length**. For a run it is the sum of its shots'
  `sec` plus a handle at each end *of the run*, snapped **up** to a duration the
  model actually offers; for a solo shot it is `sec` plus a handle at each end.
  It is what you pass to `picsart_generate`, and you trim back to the shots'
  `sec` in the assembly.

This is the temporal twin of shooting one size wide, and the same logic: a
generated take has no second take, so the cheapest repair is material you
already paid for. A tail that drifts, an action that lands half a beat late, an
end state the next shot cannot cut to — with handles those are trims; without
them they are re-renders.

**Handles are a per-film policy**, stored independently of setup feedback
(the setup does not send `handles`), because
they are a real and permanent cost: duration is what video models bill. On a run
they are exactly two — one at each end of the run — and they are cheap in
proportion: two seconds on a 28s run, not two on every 5s shot. Skip them
(`handles: "off"`) only when the run is already at the model's ceiling and there
is no room to add. **Inside the run no shot has a handle**, by construction: an
internal boundary is the model's cut, and its only trim room is `tailHold` and
the audio line's silence. That is why the silence is not optional, and why a run whose
line runs into its cut is a failed take rather than a trim — there is no handle
behind the last word.

### Audio: the takes keep the voice they were born with

**Shoot dialogue with `generateAudio: true` and each speaker's saved voice
description.** Read the character's `voice` field and copy it verbatim into every
speaking block, including inserts, retakes, edits and extensions; see
`prompt-blocks.md`. Fill a missing field once using
`../../picsart-film-assets/references/asset-sheets.md`, without an extra user question.
Describe the shot's emotion and volume separately. Native audio is the default;
no separate TTS, cloning or saved audio sample is required for this text rule.

The description improves consistency but does not guarantee identical timbre.
Compare new dialogue with accepted takes before declaring the voice consistent.
Optional reference audio is conditioning, not a deterministic voice lock or a
promise that the supplied waveform will be reproduced. A separate voice workflow
is a distinct production choice; do not silently substitute it or remove dialogue.

Five rules make native audio survivable. They are not optional:

1. **Fewer, longer takes.** Keeping a dialogue scene in one generation reduces
   independent voice decisions. Still check the delivered performances; neither
   a shared run nor the copied description guarantees perfect consistency.
2. **Transcribe every dialogue take and read it against the story's lines.** The model
   paraphrases, drops words, adds filler, and mispronounces names. Cheap to
   check, impossible to fix later without a retake.
3. **Demand silence handles** — a beat before and after each line — and reject a
   take that runs its line into the last frame. Native audio is welded to the
   picture, so the only cut points the edit gets are the silences the model left.
4. **Carry a bed across every scene.** Each take is mastered on its own, so
   levels, EQ and room tone step at every join; a continuous ambience or music
   bed is what hides it. Audiences forgive picture mismatch, not level jumps.
5. **Preserve the scripted dialogue.** Voice drift is a review issue, not a reason
   to replace a requested line with silence or narration. Judge accent, register
   and timbre against the accepted character performance, separately from emotion.

A bed can smooth changes in room tone and level; it cannot repair a changed
speaker identity. Do not automatically accept voice drift under the native policy.

### Frames or references — one way: `imageUrls` only

**Every video call carries `imageUrls` only, and the `startFrame` field stays
empty** — on a run, a bridge, an insert, a one-shot reshoot, whatever the clip
is called (rule 7, `../../picsart-film/references/overview.md`). The frame the video must open on is
picture 1, labelled `START FRAME` in the tagging header; the identity and
wardrobe views of everyone in the video ride beside it, in the order `runs[].refs`
fixes, and the header says which is `FRAME REFERENCE for shot N`, which a face
or an outfit, which `SPACE`; after the header, names only. The model honours
the role stated in words, so one call gets both things the two fields would
otherwise force a choice between.

Why the field is never filled — reasons, not a second recipe:

- **A start frame and reference media cannot travel in the same request**, and
  "reference media" means images, video **and audio** alike: the video model
  routes on which fields you set. A call carrying both `startFrame` and
  `audioUrls` is refused, while the same audio alongside `imageUrls` renders
  fine.
- **A frame shows only the people in it.** A bridge sent with one scene's last
  frame in the `startFrame` field — one person's face — and no picture of the
  second person, who is in the shot but not in the frame, brings that second
  person back in invented wardrobe and puts a wardrobe jump on both joins.
- **Native audio is NOT reference media.** `generateAudio: true` with the
  line in its shot block renders the character speaking the line, so a call
  carries its lines and its images together. That is a fact about audio, not a second way to build an
  anchored shot: the call is still `imageUrls` only.

- **Keep the reference set tight, and every entry a single view.** The
  identity view and the wardrobe view of every character in the video — both,
  always (rule 7, `../../picsart-film/references/overview.md`) — and per scene the run plays its pictures — the scene
  picture, the map and the wide (step 3). A tagged
  state a cut names — `@cal_wet` — is its
  own view, numbered like any other image, never a panel pointer into a sheet.
  For a photo-sourced character the photograph is the identity view and, when
  it shows the outfit the story dresses them in, the wardrobe view too; when it
  does not, the user is asked for one more photograph that does (rule 7) — a view of its angle sheet comes along only when a cut in this
  run needs that angle. Every prop the film gave a plate to rides as `IMAGE n —
  PROP: <name>` (rule 7): the descriptor is not in the prompt, so a picture is
  the only carrier an object has. Every image is inlined and the total has a
  ceiling.
  - **The ceiling is real and it is measured before every dispatch.** Three
    *lossless PNG* references are enough to overflow it;
    a view is a JPEG crop of a max-resolution sheet
    scaled to a **2048 px delivery cap** (the model renders 1080p and declares
    no input pixel limit, so the cap is ours to hold), which puts each one at a
    few hundred KB — **what binds is the image count, not the bytes**. Still: `picsart_media_probe_media` every
    URL (free — `bytes`, `width`, `height`), sum, and stay **under 15 MB** —
    the count follows the scenes the run plays (two characters and one scene
    are seven images; Seedance 2.5 takes 30).

    **The probe returns `width` and `height` for a reason: read the short side
    of every picture, not only the bytes.** `min(width, height)` under 300 px is
    refused before dispatch, so nothing under **320 px on its
    short side** is dispatched — width counts as much as height. A narrow
    wardrobe view (252×508) passes a byte-total check and a *"300 px tall"*
    check and is still refused. The crop that avoids it is in
    `../../picsart-film-assets/references/asset-sheets.md`, *The crop*; this is the gate
    that catches it regardless.

    Over budget, in order: **drop the wide — but only when the map is in the set
    and no cut in the run opens the setting up** (a pull-back, a reframe wider
    than the shot it came from, a move that reveals a skyline or a street: those
    cuts need the wide, and dropping it there lets the location drift);
    **the map never leaves, and neither do the identity
    and wardrobe views** (rules 7 and 10 — no descriptor is in
    the prompt any more, so neither the costume nor the geography has another
    carrier); re-encode any PNG as
    JPEG; downscale a view only as far as keeps
    the identity view ≥ 600 px on its short side — and **a view downscaled once
    becomes that state's file from then on**, recorded in `views[]` and passed
    by every later run, never a one-run copy (one state, one file). There is
    no face panel to split out of a sheet here: that split happens at lock for
    every asset. The method and the export calls are in
    `../../picsart-film-assets/references/asset-sheets.md`, *How an asset reaches the
    run*. Never discover the ceiling after the render.
  - **The panel-pointer lint, run at the same moment.** Read the
    image labels before the prompt goes out — the references header and every cut header's
    image reference. A pointer **into a reference image** — *panel 2*, *the
    leftmost panel*, *the top-right of IMAGE 1*, *the bottom row of the sheet* —
    is a **dispatch error**, not a wording preference: it means one image in
    this set has more than one thing in it, and the fix is a crop (free, at
    boxes `film.json` already holds), never a reworded label. Two runs of one
    correct pointer return two different people; the wording is not the
    variable. **Scope: reference labels only.** Position words describing the
    *frame being made* — the location map, the blocking block, where a
    character stands, where the camera is — are the film's staging and are
    required; the lint never touches them.

**The anchor is compositional, not pixel-exact.** An approved still used as a
start frame returns the same person, wardrobe, room, pose and props, but the
first delivered frame may sit slightly wider with the subject shifted, whatever
the vendor doc's "exactly match" says. The same holds for a run's frames in
`imageUrls` with their role in words, so judge the take on composition, never on
identical pixels.

**Reference audio is a conditioning input, never the film's voice.** The model
performs its own line in its own timing rather than the supplied `audioUrls`
track, so a scratch mix earns its keep for **timing** (see step 3) and the voice
comes from the run's native audio. It is never delivered by attaching a wav.

**Duration = the spoken line + one second, snapped UP the model's list.** Block
11 already requires a second of silence after each line as the editor's cut
point; the duration has to leave room for it. A 5.3s line needs 6.3s, and a
solo clip snaps that **up** to the next length the model's `duration` schema
allows (read off `picsart_model_params` — never a ladder remembered from a
note; on a schema with a one-second step, 6.3s is a 7s clip). Rounding down
runs the dialogue to the final frame with no cut point, the failure the audio
line exists to prevent. **Inside a run the snap moves to the
total.** Cut times are prompt text, so a shot inside a run keeps its exact
`sec` — 6.3s is 6.3s, no ladder — and only the run's `genSec` snaps up to what
the model offers; the slack that snapping adds goes to the run's tail handle,
never to a shot.

A refused payload — a frame mixed with reference media, or references over the
15 MB budget — stays refused. **Change the payload; never re-run the same one**, and say in one line what you
changed.

Every run's prompt is the handbook's two-part shape — see
`prompt-blocks.md` for the template, the shape per model, a worked
example and the pre-dispatch checklist. The assembly is mechanical by design:
the handbook's lines verbatim, the style prefix verbatim from the bible, the
geography line verbatim from the scene; no descriptor is pasted — the pictures
carry identity. There is no negative prompt: every ban is written as what IS in
the frame.

**Before every video dispatch, including edits, extensions and inserts, run the
prompt-verify step — `prompt-verify.md` — not just the format lint.**
It opens the files that govern a run (the blocks reference, the camera, lighting
and acting presets, the seams, the look), derives what they require for this
call, and checks the **literal tool arguments** against them; its verdict is
written before preflight and a fail blocks the dispatch. Use
`picsart_prompt_verify` for the objective half and read the rest yourself. A valid schema and a credit approval do not excuse missing dialogue,
changed story content, or a house line paraphrased on its way into the prompt.

**Price the model before believing the draft rule.** The rule below exists for
ONE reason — keep the iterations cheap so only the keeper is paid for at full
size — and it only works on a model whose price moves with resolution. Prices
change and no number is recorded here: quote both resolutions with
`picsart_preflight` before the first dispatch. If the price moves with
resolution, draft at 480p; if it is the same, draft at the finish resolution and
there is no second pass to pay for. Say which of the two the film is doing, once,
in the forecast.

### Native draft to final

Read `picsart_model_params` for the chosen model before quoting. On Seedance
2.5, when the schema lists `draft`, use `picsart_generate` with
`extra: { "draft": true }` for a native draft, keeping the approved prompt,
references, duration and format. Preflight the same payload including `extra`.
Record the returned result URL exactly in `film.json`.

If the live schema also exposes `fromDraft`, preflight a final request with
`extra: { "fromDraft": "<exact draft result URL>" }`; use the schema's
required envelope only. The tool requires a `prompt` string: use an empty
string for a from-draft request only if preflight accepts it. Re-quote and
obtain approval before the paid final. Do not add the original references,
duration or draft flag unless the live contract requires them.

If `fromDraft` is absent or rejected, it is not available on this connection.
Explain that the final requires a separately quoted rerender and may change
content; follow the normal finishing approval and re-review. Choose a regular
resolution-priced draft instead when that better fits the approved budget.

For models without the native draft path, dispatch drafts at **480p** — where resolution actually changes the price —
with the run's images in `imageUrls`, in exactly the order the prompt numbers
them, and **the `startFrame` field empty** — the start frame is the image the references header
labels `START FRAME`. `generateAudio: true` on any run with a
line in it — the line, its lip-sync, and
the voice block are part of what is being judged; a run with no speech drafts
with audio off. Audio follows the film's **voice policy** (always `native`,
recorded in `film.json.voicePolicy` — nothing to decide) — and *how the approved voice
reaches the picture* is settled before the first dialogue take, not at finishing:
see the next section. **Every video generation is submit-and-poll**:
`async: true` + `picsart_job_status` (the server defaults every media mode to
async, so this holds even if you forget) — a synchronous video call dies at
the host's ~60s tool window while the render keeps running and charging, with
no handle left to recover the result. A host "isn't responding" error is therefore never a failed
generation: poll the job, never re-submit on that signal.
`picsart_preflight` the batch, **give the user the quoted total, and dispatch
only on their yes** (the law at the top of this skill) — surprise spend is the
one unrecoverable mistake.

After dispatching, put the batch's job handles on `picsart_render_monitor`:
it polls the jobs itself, shows live per-shot
progress, and **reports the finished takes back into the conversation
automatically**. Never ask the user to wait, check back, or "ping me in five
minutes" — that is the monitor's job. When the monitor cannot open, poll
`picsart_job_status` yourself; if a render outlives the turn, say plainly
what's running and check it first thing next turn.
