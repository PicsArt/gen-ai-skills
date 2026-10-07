# Film scenes — steps 6 and 7, selects

## Step 6 — select and accept takes

**The board opens on the run as delivered — split at its cuts, untrimmed.**
When the batch lands, **split every run's take at its delivered cuts**: look at
the frames either side of each declared time (`picsart_media_contact_sheet`, or
the scene editor's own playhead), place a compositor split where the picture
actually changed, write the result to `runs[].cutTimesActual`, and treat a cut
count that disagrees with the cut list as a failed take before anything else is
judged. The split is bookkeeping over one source file and costs nothing; it is
what makes every shot of the run a clip again. Then open the board on exactly
that: every shot a cell bounded by the model's cut, no trims derived, nothing
shaved. **There is no automatic rough cut** — the model already made
the cuts, and a video edge is joined by the handbook's angle change
(`seams.md`), so there is nothing to align. Trims are the user's,
made in the scene editor, and land as `trim` with `trimSource: "user"`. With
several takes competing for a run, you pick the stronger, splice it in and name
the other in a clause (below): the scene is one timeline and cannot hold two
versions of the same shot. Say nothing about cutting
before the board opens — there was no cut; say what came back, and open it.

### A batch that lands opens a board. Every time, without being asked.

**Generations coming back IS the trigger** — not the user asking to see them,
not the takes being good, not the batch being small. First pass, retake, single
shot, a re-roll after a model swap: material arrived, so a board opens in that
same turn. There is no state of the world in which the right response to a
finished generation is a paragraph about it.

When takes land, three rules hold at once:

- **Open the board**, so everything that landed is reviewable.
- **Never self-certify a take in prose.** "Matching its beat, no issues" is a
  taste verdict on material the user has not watched. It is the same class as
  the asset-sheet rule in `picsart-film-assets` ("never self-certify identity in
  prose while the user has seen none of the frames"), and it matters more here,
  because a take is what they are paying for. **You may say what you observed;
  you may not say it passed.** "4A drifts the same way on a third model" is an
  observation and belongs in the message. "1A, 2A and 3A check out clean" is an
  approval, and approval is theirs.
- **Never end the turn on a menu of repairs.** A take that keeps drifting the
  same way across models is not a model problem and not a wording problem —
  step 5's rule is that a shot which will not land is *simplified*, split in two
  or reduced to one action. Do that, say you did it, and put it on the board. A
  question is for a decision that is genuinely the user's; "which of these two
  repairs should I try" is your job.

So the turn is: open the board with every take, say in one line which shot is
being split rather than re-worded and why, and let the user verdict the rest.

Review takes in **one `picsart_scene_editor` that carries the whole film,
by default** (rule 8, `../../picsart-film/references/overview.md`). Focused join comparisons follow
`../../picsart-film-edit/references/join-repair.md` instead, without promoting their preview
to the accepted cut. For ordinary review, not the batch that was just
dispatched — the film: every accepted take plus the new one, in playback order,
bootstrapped into one montage scene (`../../picsart-film-edit/references/assembly.md`) and
passed as `scene`. Two accepted videos and a third just delivered is a scene of
three, the new one in its story position. `videoUrl` is for a film that has
exactly one video and nothing else to play beside it.
On a run the scene's clips are the run's cuts, so a comment maps straight back
to the header that produced it — by the pin's `layerId`, or by its time
(`../../picsart-film/references/review-feedback.md`, *Mapping a comment back to a shot*).
The editor carries no prompt or model, so keep that link in `film.json`. The
scene is **one** timeline, and that timeline is the film.
**Never one view per take**: three takes on three boards means three separate sends, and the
first send moves the conversation forward while the other two boards die
unanswered. One board, one send,
verdicts for the whole batch. The same rule covers the editor's own edits: when
the user trims or splits in it, that cut is theirs and already seen — record it
from the returned `document` and say so, never an editor per piece
(`picsart-film-edit`). If several boards are ever genuinely open at
once, one board's feedback is one item of the queue: act on it, return to the
queue, and advance nothing until the queue is empty or the user says move on.

**Every retake is seen before it becomes the cut — and the surface it goes on is
the scene editor.** One surface judges picture: `picsart_scene_editor` for
takes in the cut, `picsart_asset_review` for stills. The user sees **every**
retake, not just the first, and nothing becomes the cut behind their back. A
shot run through two models and a third generation without the user seeing any
of them turns "still needs work" into something only the agent knows.

- **A retake goes INTO the cut, and the cut goes up.** Swap the new take in,
  rebuild the scene, open the editor on the whole thing, and say in one line
  what changed. Two versions of one shot are never both in the scene: it is the
  timeline, so they would lay out end to end as two different shots of twice the
  real length, with no way to say which wins.
  This ordinary-review rule does not forbid explicitly labelled join comparison
  previews under [join-repair.md](../../picsart-film-edit/references/join-repair.md); those are not the accepted movie timeline.
- **With two takes of one shot in hand, you pick — and say so.** Which of two
  candidates is stronger is a craft call, like which repair to try; make it,
  splice it in, and name the other in a clause: it is in the log, one word away.
  Never ask the user to choose blind between two files; when they want to
  choose themselves, put the takes one after another in the scene editor or
  talk it through with them.
- **An edit or extend return is the same path** — into the cut, the whole cut
  back on the board, one line naming the seconds that changed. That is where an
  edit which fixed the hand and lost the light actually shows.
- **Going back stays free.** Every superseded url stays in the log, so "use the
  first one" is one call and no credits. The comparison happens in sequence,
  inside the cut, and the old take is a word away.
- **A re-rolled run** replaces the run's take the same way: the new take split
  at its own cuts, its shots as the scene's clips, and one line on what you
  changed between the takes.
- If a shot is on its third attempt, say the attempts are converging on nothing
  and that the shot needs splitting. The board is where that gets said.

Contract in `../../picsart-film/references/review-feedback.md`.

**Frames the model reads are exported at full size, never thumbnailed.**
`picsart_media_contact_sheet` renders thumbnails — 480 px wide by default — for
*looking*; fed to the model as a frame, a 480×270 thumbnail is rejected
(Seedance refuses a picture with **either side** under 300 px — width counts
as much as height — and a small frame that is accepted anchors a small, soft
composition). A frame that will
travel in `imageUrls` is extracted with `picsart_media_export`: a one-layer
scene of the run, `mediaType: "png"`, `startTime` at the wanted second, at the
run's native size (`picsart_media_probe_media` the run first for width, height
and fps). Then **probe the exported frame**: if its width or its height is below the
run's, you have a thumbnail — stop and re-extract; **and neither side may be
under 300 px** — a narrow crop fails on its width. It is an export (a render wait, a
Drive file, and it counts against the reference byte budget), and it is the
only way a frame from a take becomes a `START FRAME`, `END FRAME` or `FRAME
REFERENCE`.

**Kept frames are anchors, not notes.** The scene editor has no keep-frame
button: a pin whose `instruction` asks to keep what is on screen (*"keep this
face"*, *"this frame is right"*) is a kept frame at its `time` — a second on
the scene's timeline, so map it to the take's own second first
(`../../picsart-film/references/review-feedback.md`). Each one survives pixel-for-pixel:
export that frame
from the take at native size (above — never a re-render, never a thumbnail) and
feed it back. On a run it
goes into the re-roll's `imageUrls` labelled as that cut's frame (*"IMAGE 9 —
FRAME REFERENCE for cut 3: shot 3 as approved, hold this face and this
framing"*), named in the references header and in that cut's header, or as the identity
reference for an edit pass on that stretch; two kept frames in one cut label as
its opening and closing frames. A user who wants a clean rebuild says so, or
removes the pin before sending: if a keep pin is there, honour it. Kept frames
can also ride on an approved cut, where they are simply on the record for
whatever gets regenerated later.

**When the face is right but the shot is wrong, keep the frame.** Do not throw
away an identity the model just got right: save the best frame of that take and
carry it into the re-roll as that cut's labelled `FRAME REFERENCE`, with the
header's motion rewritten and nothing else — the action, the camera, the
progression, and nothing that re-describes what the frame already shows. This
is the handbook's own frame-reuse technique, and it is also how a good frame
from one shot becomes the `FRAME REFERENCE` of a later one.

**When a run changes a place, its frames become the next run's pictures of
that place — automatically (the handbook's continuity rule).** The
written prompt cannot carry state: a room wrecked in run A, a character covered
in dust, exists only in run A's frames, and the approved scene pictures now
show a clean room that *fights* them. So: the story says where the
story changes a place (the fire, the fight, the flood); every later run at that
place is **dependent** and waits for run A's accepted take, and every other run
dispatches together as usual. When run A's take is accepted, pull the frames
without a stop: list every angle the dependent run will see; for each,
`picsart_media_contact_sheet` at the times of run A's last beat on that angle
(up to eight thumbnails, free) and pick the frame that is sharp, mid-action
where the next run continues the movement, and shows the place in its new
state; export each pick at native size (`picsart_media_export`, above) and
probe it. **One frame per angle** — a frame is one camera angle and carries the
state of the scene, not the geography of the room; an angle with no usable
frame means run A holds that angle for a beat (an extend) or the dependent run
is not ready. The exported frames **replace** that place's pictures for the
dependent run — scene picture, and the map when the room's shape
changed (a new map from the widest frame with the handbook's map prompt) —
never attached beside them: two versions of one room is exactly the
contradiction the rule removes. **The same for a person the earlier run
changed**: the frame that shows the state becomes that person's state view and
replaces their wardrobe view in the dependent run (rule 7) — a
clean coat beside a torn one is the same contradiction. Record them as `pictures.<state>` on the scene,
name them in the `notes` line when run A's scene opens in the scene editor so
the user sees which were chosen and can swap one, and dispatch the dependent run — its charge was quoted
with run A's in one batch and approved once, so nothing waits on a second yes.

A take is accepted against the checklist, not vibes:

- Characters and location match their references — face, costume, space.
- No artifacts: hands, teeth, extra fingers, drifting objects, random pseudo-text.
- **Every declared cut landed as a cut** — the right count, each near its
  time, a hard cut and not a whip pan, a morph or a dissolve. A run that made
  the wrong cuts is rejected whole, whatever else it got right: its shot
  boundaries are not where the plan says, so nothing downstream lines up.
- Camera movement is what the shotlist ordered. **When the camera is wrong, it
  is a camera-change retake — and an ANCHORED one.** Swap exactly the move
  preset (one block-7 recompile of that shot's header) and never re-prompt the
  whole shot over a camera verdict. On a run this is a re-roll with one header
  changed — a camera move is motion, which an edit pass does not change — and
  the anchoring is the same numbered references, so nothing else in the call
  moves.
  - The order arrives as a comment that asks for a different camera move and
    nothing else. The editor has no preset panel, so read the words; a move
    named in them is the shotlist board's own vocabulary, so it recompiles to
    exactly one block.
  - **Anchor it.** Take a frame from the start of that shot's source (the
    commented clip's source url) and
    send it as a *reference image* beside the shot's locked asset references —
    all of them as references together — then name the opening frame in the
    prompt. Cast, wardrobe, set and light survive as pixels; only the camera
    changes. Not a first-frame role (a frame role and reference images are
    alternatives, and the pair is refused), and never the old
    take as a reference video (a reference video supplies camera motion, so it
    reinstates the move being changed).
  - A note that moves the camera **and** something else is an ordinary
    regeneration — an opening-frame anchor would fight a new lighting note.
  - **For a user-requested join repair, distinguish a crop from a new camera
    move.** Existing-pixel reframing follows `picsart-film-edit`'s compositor guidance
    after checking the live operation; it is not a generative camera change.
    Genuine new camera motion still needs a generative repair.
- The performance fits the task; the line reads; lip-sync holds. **"The line
  reads" has a method**: `picsart_media_transcribe` the take and diff against
  the scripted line — it catches lip-sync saying the wrong words and verifies
  the one-second silence tail.
- **Look INSIDE accept candidates before promoting**: a take's first frame
  hides mid-clip morphs. On the takes you intend to accept (only those —
  contact sheets cost render time, not generation credits), render 3–4 frames across the take
  (~25/50/75%), view them in one batched `picsart_view_image` call, and check
  identity and artifacts at each.
- It will cut with its neighbours: a movement written to carry across a cut
  ends mid-move and is picked up; a look that answers a thing leaves frame on
  the right side; the cause is shown before the answer. At a video edge, the
  last shot ends in the middle of its movement and the next video's first shot
  is a clearly different angle (`seams.md`). If a join fails, inspect
  whether existing footage can be recut before deciding it needs new material
  (`../../picsart-film-edit/references/join-repair.md`).
- Palette and light match the world.

Accepted: the run's URL and its `cutTimesActual` into `selects/scNN/` (and
`picsart_drive` — CDN links expire), its prompt saved as the final version,
every shot in it status `final`.

## Step 7 — run it as a conveyor

Work in scene batches, never scattered shots — a scene keeps light and continuity
in one head. A run at a place an earlier run changed is dependent and waits for
that run's frames (step 6); every other run goes out together. While scene N iterates, shotlist N+1 and hand scene N−1 to
`picsart-film-edit` for parallel assembly (that is where reshoot orders come from). Track
daily output in shots-final-per-day against the target and say so when the pace
will not make it.

Gate out (per scene block): every run's take accepted and split at its delivered
cuts · all shots `final` in selects · final prompts versioned · log complete ·
the run watched on the board at its cuts and its run edges (the ten-second
version of the edit's join QC, before problems compound).
