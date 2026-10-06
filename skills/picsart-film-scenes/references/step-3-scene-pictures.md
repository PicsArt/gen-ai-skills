# Film scenes — step 3, scene pictures

## Step 3 — the scene's pictures: one board for all scenes

Read `../../picsart-film-assets/references/asset-efficiency.md` for scheduling and changes:
independent ready scene chains advance without waiting for unrelated retries;
an upstream correction triggers a content-impact check, not a blanket rebuild.
Scene pictures still use the full scene style prefix, unlike neutral asset plates.

**Every scene gets its pictures before its run, and nothing else is generated
between the shot list and the run.** A run's picture of a place is never a
clean, empty location panel. The handbook's reason: *the model is
trained on films with actors in them — an empty location renders unreal, so
make the scene first and take the location from it.* A scene's pictures are one
dependency graph: wide first, opening crop and optional map derived from it. They
are what the run's `imageUrls` carries for that scene — the scene picture as
`START FRAME`, the wide and the map as `SPACE` — so the model never has to
guess the room. A `FRAME REFERENCE for cut N` rides along only when a frame
exported from an already-approved run supplies it (step 6); none is authored
ahead of time. Character views ride beside them (step 2).

**Wide first, then cut the scene picture out of it, then the map — one approved batch.** Two generations and one free crop:

1. **The wide is generated first**, at 4K, with the cast in it from their
   identity and wardrobe views; the scene-picture craft below (whose cast
   opens the scene, the prompt lines, the three planes) applies to it.
2. **The scene picture is cut out of the wide** with `picsart_media_export` (the crop
   recipe, `../../picsart-film-assets/references/asset-sheets.md`, *The crop*): a box
   around the opening shot at the film's ratio, no credits, the run's `START
   FRAME`. Its short side must clear the video's resolution (1080 px for
   1080p), else the wide itself is the start frame. In a vertical film a
   two-shot barely zooms, so a scene opening on two usually starts on the wide.
3. **The room map is generated from the wide**, when needed (item 3 below).

Quote the wide and the map as one intended batch. Preflight each concrete
payload, obtain approval for its cost, and use `picsart_generate` asynchronously.
The map waits for the actual wide URL and its visual check; if its exact quote
could not be obtained in advance, show that quote before dispatch. The opening
crop is free to render. Present wide, crop and map together for one scene review.
A scene starts as soon as its own cast is approved. A request to shoot now can
authorize the prerequisite pictures and run together only when their scope and
cost are explicit; preserve all dependency and asset checks.

**The chain, per scene** (a scene = one place at one time of day; a scene that
moves rooms is two chains). **Model: the wide on a model that
renders 4K (for example `gemini-3.1-flash-image` with `resolution: "4K"`; check
the enum with `picsart_model_params`); the room map, square and empty, on the
GPT Image family — ids as recorded in `film.json` (`model.pictures` — `people`,
`map`), read off `picsart_model_catalog` once at Stage 4
(`../../picsart-film/references/pipeline.md`, *Image models are families*).**
Nano Banana loses faces in two-shots made from whole sheets and holds them
from cut single views; Seedream holds both. If a two-shot fails on faces, try
Seedream for that wide and accept the smaller cut. The
order below is the order things are attached, because the handbook's prompts
say *the 2nd photo*. Every prompt opens with the two film lines
(`../../picsart-film-assets/references/asset-sheets.md`, *Every image prompt carries the
film*).

**Before either generation dispatches, run the prompt-verify step
(`prompt-verify.md`) — it is mandatory for a still
exactly as it is for a run, and the still row of its governing-files table
names what to open.** A scene picture, a wide or a
map is still a generation with subjects tagged
in it, and the same failure the gate exists to catch on video happens on
stills just as easily: a character named in the shot but written into the
prompt only as the target of someone else's reaction, with no pose or emotion
of their own. Check the literal text about to be sent, not a recollection that
the rule is known.

1. **The scene picture** — the handbook's *base image*, the scene as its first
   frame. **CUT from the wide** (above): what follows is the
   craft of the wide's prompt and of where the cut falls. Every head in the cut
   at least a tenth of its frame tall.

   **"The scene as its first frame" means the cast of `shots[0].assets` —
   read it, never the scene's dramatic centre.** A scene whose
   cast changes as it plays (someone arrives on a footsteps cue, a knock, a
   door) is *about* the pairing that arrives, but its FIRST shot is whoever
   is already in the room — and the scene picture is the first shot, not the
   scene's throughline. A base image built from the throughline opens the run
   on someone who has not entered yet. Before writing `Subject #1`/`#2`, open the approved shot
   list and copy `shots[0].assets` verbatim; if that list disagrees with
   whichever pairing feels like the scene's centre, the shot list wins.

   Prompt: the handbook's
   thirteen lines, in its order, each filled from the film — *describe only
   what the camera sees*:

   ```
   Visual tone: <bible.stylePrefix, verbatim>. Skin matte and textured with visible pores, no gloss or shine. A frame of live-action film — real people, real fabric, real light; not an illustration, not animation, not a 3D render.
   Subject description: <one distinguisher per present character — "Subject #1 — @cal, worn dark-blue work jacket"; the face comes from the attached view, not from words>
   Shot size: <the card's size fragment>
   Camera angle: <the card's angle fragment; "Eye-level." when the card is neutral>
   Composition: <the card's arrangement or composition fragment, or N/A>
   Pose & action: <the card's action — what each subject is physically doing in frame one>
   Emotion: <the card's feels line, per visible face>
   Gaze: <each visible face's gaze target — in the scene, never at camera>
   Positioning in the frame: <each subject's placement from the location map — left third, right third, centered>
   Visible / Not visible: <what must stay in frame, what may crop>
   Foreground, Midground, Background elements: <all three, named — what sits closest to the lens, the plane the subject is on, what falls away behind them>
   Setting: <the location descriptor's setting line — place, condition, time of day>
   Aspect ratio: <the film's ratio>
   ```

   **The skin clause rides on `Visual tone`, and is ours.** The
   prefix compiles the camera (grain rides in its stock) and the lens family,
   and a camera fragment says how its stock renders skin *colour* — none of them ask
   for skin *texture*, which is the one instruction that most reliably fights
   the render look on faces. The video prompt carries it in its quality line,
   and the still that sets the film's look carries it too. It is appended to
   line one rather than added as a fourteenth line, because the thirteen are
   the handbook's, in its order, and the only deliberate departure from them is
   the aspect-ratio substitution below. **Where the light comes from is not
   asked for here, and that is a decision, not an omission.** Lighting is
   per-shot, so it cannot ride the prefix, and the handbook's thirteen have no
   lighting slot; a scene picture takes its light from the time of day on
   `Setting` and from the plate it was derived from. A named light source is a
   strong realism lever, but adding a lighting line here is the user's call:
   do not add one unasked.

   **The still says what medium it is, and bans the others.**
   Appended to `Visual tone` after the skin clause, and taken word for word
   from what the character sheets already carry, so the two describe the same
   film: *"A frame of live-action film — real people, real fabric, real light;
   not an illustration, not animation, not a 3D render."* A film set up as
   animated says its own medium instead — the line is whatever the film is,
   never a fixed string. Every frame of the scene is derived from this picture,
   so it guards the medium as firmly as the sheets do.

   **They go to the compiler as `space` (`foreground`, `midground`,
   `background`), the same in every prompt of the scene; it refuses a run or
   a scene picture without all three.**

   **All three planes are named, and `N/A` is an argued exception.**
   An escape offered in a template is the value that gets written. The
   sharpest demonstration is a matched pair — same model, same subject, same place — where the only difference is
   whether a foreground, a midground and a background were written down, and the
   version without them renders the person pasted onto the backdrop like a
   sticker. The claim is that the flat look **is** the missing layers, not a
   model weakness, and it is the same reason the handbook's own location plate
   carries the three slots. So the default inverts: a frame nearly always has
   something close to the lens — a shoulder, a doorframe, a railing, steam, the
   edge of a table — and writing `N/A` means claiming it does not, which is
   rare enough to be worth a sentence in the card's notes.

   **This is the near plane only; it is not an instruction to fill the frame.**
   A foreground object sits close to the lens and slightly soft, and it frames
   rather than competes: one already in the location, never a prop invented for
   the shot, and never something that crosses a face. Where the camera travels,
   check it against the warning that a single large near object sweeps
   the whole frame on a lateral or orbital move and drags the subject with it
   (`presets-camera.md`, *If you are generating a start frame too*) —
   many small cues beat one big one. The `Atmosphere` presets in that same file
   are the other half of this: the planes give the eye somewhere to travel,
   atmosphere is what physically separates them.

   **`negativePrompt`, where the image model's schema declares one.** These are
   all image-model work, so the guardrail the sheets already use applies here
   unchanged (`../../picsart-film-assets/references/asset-sheets.md`): for live action, the
   medium ban — the words that rule out drawing, animation, rendering and
   plastic-looking skin. `picsart_film_compile_asset_prompt` returns it in
   `negativePrompt`; take it from there rather than writing it. Never as prose,
   never in a video block. The lettering ban below is scoped more narrowly than
   this one.

   **The lettering ban goes on the scene picture and the wide — NEVER on the
   room map.** The map's prompt asks in as many words for a label
   on each side, *A on the north side, B on the east side*, and those labels are
   the only reason the map exists: they are read off it to write the geography
   line that every prompt of the scene then carries. Banning lettering there
   destroys the artifact. On the three that do take it, the compiler adds the
   lettering ban — every form of on-image text, from signage to watermarks — to
   the medium ban above.

   **A film that needs a sign does NOT ask the model for it.** A story with a readable shop name, a door number, a headline
   on a screen or a figure on a phone still gets the ban — because the model
   cannot hold clean typographic text, which is the same reason
   `picsart-film-finishing` already refuses to generate the film's titles and makes
   them as overlay tracks instead. In-world text is the twin of that rule.
   Keep the words out of the generation and **lay them in as a
   compositor layer over the finished clip** (`../../picsart-film-edit/references/workflow.md`),
   positioned so they read as part of the frame. The ban and the wanted text
   are not in conflict: the ban stops the model inventing lettering, and the
   layer supplies the lettering the film actually wants, clean.

   Never name the exact string on the *Visible* line and let the model render
   it. Numbers and words rendered into a generated shot come back glitched, so
   they are typed out separately and laid over the clip afterwards, where
   nobody can tell they were not always there.

   **Why the lettering ban is worth its own words.** The video prompt carries
   the handbook's no-subtitles line on every generation (`prompt-blocks.md`,
   item 7). A still without an equivalent leaves the model free to invent
   signage, labels and shopfront text in the picture, and the video then
   faithfully reproduces whatever it invented. This is the same shape as the
   medium guard above: a rule that must hold at both ends of the pipeline.
   What it is aimed at is **invented** lettering — the garbled pseudo-text
   a model reaches for when it has to fill a sign it was never told about — and
   not at text the film actually wants, which is why it has the two exceptions
   above. That failure is not hypothetical: **the run QC below already rejects
   "random pseudo-text" as an artifact**, beside hands and teeth. Caught there,
   it costs a paid take; this catches it one step earlier, in the picture the
   take is built from.

   **The wide is the authored source picture.** Its compiler input carries
   the locked medium, skin treatment, lettering constraints and all three
   `space` planes. Its opening crop inherits those pixels. The map uses the
   checked wide as its reference and the compiler's map template. Preserve
   each compiler result's `negativePrompt` and matching `promptToken`.

   Attached: the identity view **and** the wardrobe view of every present
   character — both, always (rule 7, `../../picsart-film/references/overview.md`) — and, for a real
   place, the user's photographs of it. **Nothing else**: no room map, no prop
   plate, no extra still. Extra references in a two-shot outvote the faces;
   the faces alone hold. A prop is named in words with its count on the *Visible* line (*"one flask,
   on a cross-body strap"*). The handbook writes 16:9 or 9:16 here; ours is
   the film's ratio — the one substitution. Recorded on the scene as
   `pictures.scene`. **Looked at as soon as the plan lands**: each face
   against its identity view on the preview URL (`picsart-film` rule 4);
   a wide with one wrong face is regenerated, and its cut and map with it —
   every derived frame inherits the wrong face. **Two failures on faces in a row change
   the reference set or the model, never a third roll of the same call.**
2. **The wide — generated FIRST**, from the cast's views and
   item 1's craft, at the film's ratio and 4K.
   `pictures.wide`.
3. **The room map — only when the scene needs one**: an
   interior, or any scene whose cards cut between two or more walls behind the
   people; a single outdoor place with one background gets no map, its wide is
   the geography (a map of a place that needs none often comes back wrong).
   When needed, from the wide — the handbook's *location
   sheet*. Its prompt asks for a top-down view of the place in the photo with
   every corner and side visible, no people in it, each side lettered A to D
   clockwise from north, the colour and realism of the source kept, 1:1.
   `picsart_film_compile_prompt` pastes it (a typo in the handbook's own
   wording, "one" for "on", is corrected there, once). Attached: the wide. **One map per place and time of day**,
   made from the first scene played there and reused by every later scene at
   that place — the handbook makes one per scene; one per place is what keeps
   the walls the same across scenes, and it is ours, deliberately. When the map
   lands, read it and write its four sides into the location map (the geography line):
   *"Side A — the shelving wall; Side B — the roller door; …"*. Recorded on the
   location as its `map` view.

   **Left and right are read off the scene picture, not off the map.** Who is frame-left and who is frame-right in the scene
   picture goes into the geography line, and the sides never change inside a
   scene (`seams.md`, screen direction). The map says which wall is
   behind each face — **the background side is the wall behind the face of the
   person facing the camera**, read off the map, never copied from an example.
   A reverse that puts a shoulder frame-right when the master has that person
   frame-left costs a round. **What a reverse changes**:
   whose back is in the foreground, the background wall, and the pointing hand
   becomes the other hand — say it in the shot block (*"Subject #2 hand
   pointing should be the other hand"*), because the model confuses hands
   across a reverse.

**Check each picture against the one before it as results land** — with
`picsart_view_image` on the preview URL (`picsart-film` rule 4), beside
showing it (`picsart-film-assets`, *Show it the moment it lands*) — the same faces as the
identity views, the same grain and colour, the same room — and re-dispatch on
drift. No picture becomes a start frame or a reference until its check is
back. On the
wide, the handbook's questions: did the room stay the same room; did the
characters keep their left and right; is anyone looking at the camera.

**When a picture comes back wrong, read it back to the line that made it.**
The rule above says how many times to try — two failures on
faces in a row change the reference set or the model, never a third roll of the
same call. It does not say *what to change*, and a picture that came back
plastic needs a different fix from one that came back generic — never the
same prompt, rolled again. Every roll is a charged generation. Read the defect
back to the line of the thirteen that owns it, change that line, and only then
re-dispatch.

| What came back | The line that owns it | What to change |
|---|---|---|
| the person could be anyone; the face is not theirs | `Subject description`, and the attachments | the exclusive tell is missing or is not exclusive; or the identity and wardrobe views were not both attached (rule 7) |
| the whole frame reads as a render; skin is plastic | `Visual tone`, and `negativePrompt` | check the skin clause and the medium line are on line one **verbatim**, and that the ban field was actually filled. If both were there, this is not a wording problem — it is the reference set or the model |
| the place is a stock backdrop; it is nowhere in particular | `Setting` | thin setting line, or the location's anchor object was never named — a place without its anchor is "somewhere", and somewhere drifts |
| the people look pasted onto the background | `Foreground, Midground, Background elements` | a plane was left unnamed — most often the near one. This is the defect that line exists to prevent |
| the frame is inert; everyone is centred | `Positioning in the frame`, `Composition` | no placement was given, or the frame needed organising and the composition slot was left empty |
| invented lettering, garbled signs and labels | `negativePrompt` | the lettering ban was not added — and check it was not added to a room map, where it destroys the artifact |
| something the shot needs is simply absent | the whole prompt | it is overloaded. **Cut, do not add** — the model drops what it cannot fit, and another clause makes it worse |
| a prop is missing or there are two of it | `Visible / Not visible` | props are named there with their count, and every prop needs its plate |

**Two things this table deliberately does not do.**

- **It does not authorise more rolls.** It sits *inside* the two-failure cap, not
  beside it: it is how you spend the second attempt well. A third roll of a
  changed prompt is still a change of the reference set or the model.
- **It says nothing about where in the prompt a line sits.** Moving an ignored
  detail closer to the *beginning* and relying on the model weighting the *end*
  are both common advice and neither is reliable, so the thirteen lines stay in
  the handbook's order.

**One row left out on purpose.** A common answer to the plastic-render row is
that the light has no named source, fixed with a lighting instruction in the
picture prompt. There is no lighting line here by decision, so the row above
names the levers this pipeline actually owns instead.

The table changes no field and costs no call.

**One board for every scene's pictures at once**, as the cast board:
`picsart_asset_review`, split past 12 tiles, one tile per
picture — `tag` the scene and the picture (`sc03 · scene picture`, `sc03 · OTS
over @cal`, `@garage · map`), `prompt` the picture's prompt, `info` the cuts it
serves, one `judge` line: scene picture *"the scene as the card designs it —
these faces, this room, real."*; wide *"the same room, the people small and
far."*; map *"the room from above, four sides labelled, nobody in it."*. Feedback per
`../../picsart-film/references/widget-feedback.md`: `approved[]` and `changes[]`, nothing
decided by silence. **A change repairs that picture and triggers an impact check
of its dependents** (`../../picsart-film-assets/references/asset-efficiency.md`). Rebuild
only images whose required content became invalid: a facial-expression correction
does not remake an unchanged room map.
Geometry or lighting changes can affect many views; inspect rather than assume
reuse. Record the reuse/repair decision and source versions. Approved pictures are saved with the scene
(`film.json.scenes[].pictures`, the URLs the save hands back) and are what the
run carries; the map and the wide are the location's views
(`../../picsart-film-assets/references/asset-sheets.md`, *The location*), saved through
`picsart_save_asset` as its row. Two adjacent cuts never open on the same
picture (`seams.md`).

**The animatic stays on request** — *"let me see it as stills first"*: the
scene pictures cut in order at each shot's `sec` — a montage bootstrapped
with each picture as a clip (`content.asset.type: "image"`, `duration` = the
shot's `sec`) and opened as `scene` in `picsart_scene_editor` — played at the
film's real length, so the ±10% runtime gate is checked against the reply's
`duration` before anything renders; ask them to watch it once without stopping — playing finds pacing,
scrubbing finds frames. Rendering it to a file is charged and almost never
needed.

**Dialogue durations come from the words, not from a pre-generated line.** A
line's `sec` is its word count at ~2.5 words per second plus the audio line's one
second of silence, snapped to nothing — no line is generated to be measured
(the model treats a cut time as a share of running time, not a frame-accurate
mark, so that precision would not be real). The run's total snaps
to what the model offers; the shots inside it keep their estimates.

**An `END FRAME` stays an editorial tool, on request, per run** — a second
composed image the run arrives on, for a designed transformation or a match cut
into the next run; generated FROM the scene picture (image-to-image), never rolled
fresh, and never on a held look or a line delivered in stillness, where you want
life rather than interpolation.

**Scene-level changes propagate by content.** A weather, light, or time-of-day
change updates the SCENE entity once and recompiles affected headers. Check its
picture dependencies under [asset-efficiency.md](../../picsart-film-assets/references/asset-efficiency.md); remake views whose required
illumination/state changed, not every file solely because it shares a scene ID.
Do not retain a reference whose pixels contradict the new state.
