# Film scenes — steps 4 and 5, runs

## Step 4 — one run before the rest

**With the shot list approved, the sheets locked and the scenes' pictures
approved, buy ONE run before dispatching the rest.** Not a sample of the batch — a test of the path. It answers, for the
price of a single generation, what a whole-film dispatch would answer
expensively and all at once: does the video path work end to end on this
connection, does the chosen model hold the locked identity across its own cuts,
does it make the cuts it was told to (count and approximate times), does
lip-sync land on a spoken line, and is the recipe (model, resolution, run
length, the reference order, block order, how the cut list is phrased)
worth saving and reusing.

- **On a film that fits one run, the test run IS the film.** There is nothing
  to hold back; buy it with care, judge it on the board, and the "recipe" you
  save is the film's own prompt. On a longer film, pick the riskiest run — the
  one with a *line* in it and the most cuts, since lip-sync and the cut count
  are the two variables with the most ways to be wrong — never a throwaway.
- **Say the arithmetic once, in credits, not in theory**: "the film is one run
  at ~120; a re-roll costs the same again" — or, on a longer film, "one run at
  ~100 instead of the whole film at ~400 — if it holds, the rest go out in one
  batch." Then ask, and wait for the yes — the plan is yours, the purchase is
  theirs. A run is never dispatched unquoted.
- **Then the conveyor.** A pass unblocks the whole batch — which is quoted and
  confirmed like any other dispatch; a fail has cost one
  run, and what it teaches (wrong model, a cut the model will not make, a
  header it ignores, a descriptor too loose in motion) applies to every run
  before any of them are bought.
- **This is not the "quick test shot" in *Traps*.** That one is a test *before
  the assets lock*, which is the gate itself. This is after the lock — the last
  cheap question before the expensive pass.

Save the winning recipe in `film.json`, per the handbook's own step for
this ("Generation tests: choose model/method per shot; save recipes"), and reuse
it for the batch rather than re-deciding per shot.

## Step 5 — iterations: edit, extend, or re-roll

For a note about the join between clips, route first to
`../../picsart-film-edit/references/join-repair.md`. Its diagnosis may select a deterministic
edit or a separate connecting insert; the model-routing table below is not a
reason to regenerate accepted footage. Run the prompt-verify step before
dispatching the selected generative repair.

**The note's meaning is the route, and the route is a model call — never a
regeneration by reflex.** A note arrives with a selection — a stretch marked
on the scene editor's timeline (`scene_editor_feedback.timelineComments`, with
its seconds), a pin on a clip (`comments`, with its `layerId`), or a sentence in
chat about a shot — and the two together say
which of three things is being asked. Derive it; do not wait for the word
"edit" or "extend":

| What was selected + what the note asks | It means | The call |
|---|---|---|
| a **stretch** or a clip, and the note is about **how what is there plays** — *"make this more dynamic"*, *"he should look angrier here"*, *"slower"*, *"the mug should be white"*, *"the last 10 seconds are wrong"* | change what exists, inside its seconds | **edit** |
| a clip, and the note asks for **something that has not happened yet** and needs seconds the clip does not have — *"in this scene the copter must land"* when the clip ends with it still in the air, *"let him finish the sentence"*, *"hold on her a beat longer"* | continue the clip | **extend** |
| a clip, and the note asks for the event **instead of** what is there in the same seconds — *"the copter should land here, not hover"* | change what exists | **edit** |
| a note about the **whole run** — light, cast, the cut count — or the words *regenerate / redo / new take* | a different take | **re-roll** |

The test between the first two rows: **does the note ask for something after
the clip's last frame, or in place of what the frames show?** After → extend;
in place → edit. A range selection is almost always an edit (they marked *this*
stretch); a clicked clip with a new event is almost always an extend.

**When the intent is clear, go — no confirmation.** Asking "did you mean edit
or extend?" on a note that already says which is the ceremony this pipeline
keeps removing. **Ask only when the note genuinely reads both ways** — *"make
the ending better"* on a whole clip could be either — and then one short
question naming the two readings in the user's own terms (*"change how the
landing plays, or add the landing after what's there?"*), then the call. Never
two questions, never a menu of models.

The three calls:

| The user says | The call | What goes in |
|---|---|---|
| **edit · change · fix · replace · remove · "the last 10 seconds are wrong"** — anything about what is *in* the clip | **the edit sibling (`shoot.editModel`)** | `videoUrl` = the clip (the run's file, or the piece the shot lives in); `prompt` = the change and *only* the change, naming the shot and its seconds; `imageUrls` = the same numbered views and frames the run had, so identity does not move; `generateAudio` as the run had it |
| **extend · expand · longer · continue · "add a beat at the end"** — anything about *more* clip | **the extend sibling (`shoot.extendModel`)** | `videoUrls` = [the clip]; `prompt` = what happens in the added seconds, written as one more cut header (positions restated, the same references named by number); `duration` per the model's own definition — read `picsart_model_params` and preflight before the first use, and record which it is |
| **regenerate · redo · new take · "roll it again"** — or a note about the whole run: light, cast, the cut count | **a fresh roll of the run** | one header or block changed, the rest byte-identical; it costs the run, said in credits before it goes, and every other shot comes back different — a fresh roll is a fresh roll |

### Extend input gate — probe before preflight

The Seedance 2.5 extend path has provider checks that `picsart_preflight` does
not catch. Before dispatching that sibling, probe every distinct input video
(`picsart_media_probe_media`) and enforce both limits yourself:

- every input video is at least **1.8 seconds** long;
- the **sum of all input-video durations is at most 30.2 seconds**.

These are provider limits the catalog does not state: read
`picsart_model_params` first and treat the live schema or a provider
diagnostic as authoritative. Preflight still runs after
this gate for payload validity and price, but a green preflight alone is not
evidence that these two duration checks pass.

For a two-sided seam repair, never send the whole following run merely to show
the target pose. Make a deterministic excerpt of its opening, normally **2.0
seconds**: `picsart_media_apply_scene_template` with `mpscene://montage`, one
clip and the required trim → `picsart_media_validate_scene` →
`picsart_media_export` as mp4 → probe the exported excerpt again. If the source
side plus that excerpt still exceeds the total ceiling, trim the source input to
the shortest motion-bearing tail that the model accepts; keep the original
takes untouched.

The extend schema accepts `videoUrls` and no `imageUrls`. Do not attach
reference pictures when the live schema omits them. On hosts whose generic
`picsart_generate` surface exposes only singular `videoUrl`, put the model's
multi-video field in `extra: { videoUrls: [...] }`; the generate tool flattens
`extra` before model validation. Pass `videoUrls` directly to
`picsart_preflight`. `duration` is the requested generated continuation, not
the sum or trim length of the source videos.

Every retry gets a fresh returned job handle. Put that exact handle on the new
render monitor row; never reopen a failed handle or let an old monitor stand in
for the retry.

**Regenerating a clip the user wanted kept is the failure this section exists
for.** A selected clip with the note "expand" answered with a new prompt and a
fresh roll throws away the footage they liked and pays a run's price for a
beat's worth of new seconds. The note says what to do; the selection says
where; nothing in it asks for a new take.

**What each call must carry so nothing breaks:**

- **The same references, the same numbers.** `imageUrls` for an edit is the
  run's list verbatim — same sheets, same order, same roles in the prompt — so
  the edited clip's faces are anchored by the same pixels the run was. Never a
  fresh selection, never a re-ordering.
- **Verbatim is the floor, not the ceiling: an edit that opens the frame up
  needs the place's pictures ADDED.** The run's list anchors what
  the clip already showed. The moment the edit changes what is *visible* — a
  pull-back, a wider reframe, a camera move that reveals a skyline, a street, a
  far wall — the newly revealed area is anchored by nothing, and the model
  invents it. So before an edit like that goes out, ask what the new framing
  will show that the old one did not, and put the **map and the wide** of that
  place in `imageUrls` (appended, so the existing numbers do not move) with the
  geography line in the prompt. **The failure it prevents:** a clip that
  carries only a tight frame of its setting, edited into a pull-back without
  the map and the wide, reveals a skyline that is a new place. Rule 10.
- **The change alone, named to the second.** An edit prompt is *"cut 3
  (13.0–19.0s): the mug on the bench is white ceramic, not steel; everything
  else unchanged"* — not a re-description of the shot. A re-described shot is a
  re-rolled shot wearing an edit's price.
- **An extension is a header.** The added seconds are written like any cut
  header of the run — positions restated, the action in beats, the line in
  quotes with its silence, the references by number — because the model reads
  the continuation the same way it read the run.
- **Frames as references are exported at full size** (step 6, *Frames the model
  reads*); a thumbnail is rejected or anchors a soft frame.
- **Preflight, quote, then wait.** Each sibling has its own rate; the number
  goes to the user before the call and the call waits for the yes. A repair is
  a purchase like any other.

**After the call:** a focused join candidate stays separate from the accepted
cut and follows `../../picsart-film-edit/references/join-repair.md`'s comparison workflow.
Otherwise, the result goes into the cut and the whole cut goes back into
`picsart_scene_editor`, with one line naming the stretch that changed; an edit
replaces the clip's
url in `runs[].pieces` (the shots re-point to it, trims re-derived by the user
only), an extension appends a piece. Split the result at its actual cuts before
anyone judges it — an edit that changed the cut count is a failed take like any
other. Log which call it was, with its prompt and rate.

**Rules that hold across all three:**

- One change per call: one thing edited, one beat extended, one header
  re-rolled. Two changes at once and you will not know which one worked.
- **Log every generation**: run or piece, which call, prompt version, what
  changed, result URL, verdict per cut. `film.json` runs carry `promptVersion`,
  `takes`, `editPasses`, `extends` and `pieces`; the prose log lives in
  `docs/log.md` when there is a disk.
- A clip that will not take an edit in **two** tries, or a run that will not
  land in **four or five** rolls, has a wording problem exactly never. Simplify
  the header that keeps failing: drop an action, change the angle, lengthen
  the beat.
