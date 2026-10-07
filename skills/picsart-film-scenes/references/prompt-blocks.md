# The prompt — the handbook's shape, filled from the film

> **The house lines live on the server.** This file decides the prompt's SHAPE
> and every judgement inside it — what a setup carries, how a block is written,
> what the camera line governs and when it is dropped, how long a spoken line
> may be, what a reference may and may not give. That is the part that needs a
> reader, and it is all here.
>
> The lines themselves are not. Build a prompt with
> `picsart_film_compile_prompt`: it pastes the camera, music, subtitle, quality
> and cut lines in the order below, and returns them with the blocks. Check one
> with `picsart_prompt_verify`, whose verdict rows cite this file's part and
> item numbers — which is why they are kept stable.
>
> The numbering below is the paste order. An item that says *(ours)* is a line
> this pipeline added to the handbook's stack; the rest are the handbook's.

One prompt per video (`overview.md`, *The unit of generation is the run*), in
the handbook's two-part shape: **a setup once, then one short block per shot.**
One shape for every model the pipeline uses: the handbook's Seedance layout —
tagging header, visual tone, breathing feel, no music, no subtitles, the shot
list as a timeline. A model without native multi-shot does not pass the model
policy in the first place, and the start-frame field stays empty (rule 7 in
`../../picsart-film/references/overview.md`).

**Pictures carry identity; words carry the action.** A prompt that pastes every
character's full descriptor and restates every board value in every cut header
runs a seven-shot video to 17,000 letters, the user cannot read it, and it buys
nothing: a prompt describing a cropped haircut and a round canteen on a hip in
full still gets the pictures' bob and flat flask, and a descriptor paragraph
that agrees with the pictures changes nothing visible.

Every line the handbook gives is pasted **verbatim**; what is ours is named as
ours below. The only freshly written text per video is the two scene sentences,
the geography line, and the shot blocks.

## The Seedance shape

### Part 1 — the setup, once per video, in this order

1. **Visual tone** — `bible.stylePrefix`, word for word. The handbook: *"in
   Seedance there are more camera movements and shot changes happening inside
   one prompt, so the model can start making up its own tone between shots."*
2. **The scene, two sentences** (ours) — where and when, and what happens in
   this video, written as if this were the only video that exists: what is in
   the frame now, never what happened in the video before (*Language laws*,
   first law). Then, on its own line: `EXACT <N> CHARACTERS — NO DUPLICATES.`
   with N the number of people in this video (ours — the model adds people the
   moment you let it). Then **one line per person naming the one thing that
   tells them apart, written as an exclusive**:
   `@cal = ONLY the black headband and the beard. @tobin = ONLY the grey
   overall and the shaved head. Never duplicate either, never add a third.`
   **A character who is not in frame at the start is counted anyway, and the
   line says where he is**: `EXACT 3 CHARACTERS — NO DUPLICATES.
   Marcus is outside the room until shot 1B and enters through the doorway.`
   Counting only the people visible in shot 1 is how a run comes back with the
   same man at the doorway and already inside, in the same cut.

   The count and the exclusives guard different failures: the count stops a
   fourth body arriving, and does nothing about the model giving two of the
   three the same face. The exclusive is what holds them apart. Write the tell
   from what the pictures already show — it is a pointer, not a descriptor, so
   it does not reopen *no descriptor in the prompt*.
3. **The tagging header** — the handbook's template verbatim, our image numbers
   where its platform puts an `@`:

   ```
   Main Subjects:
   • [Character name] face and outfit 100% matched based exactly on IMAGE n (face) and IMAGE m (outfit)
   • [Character name] face and outfit 100% matched based exactly on IMAGE k

   [Object/asset name] 100% matched based exactly on IMAGE j

   Scene setting is based on IMAGE p (scene picture), IMAGE q (wide), IMAGE r (room map, when the scene has one)

   Expression of [side character] is [e.g. scared / nervous / confused]
   [Main character(s)] facial expression remains [e.g. calm and cold] throughout. No panic, no fear.
   ```

   Fill these acting examples from the approved story; “calm throughout” and
   “no panic” are not fixed boilerplate. If emotion changes across shots, put
   that progression in their shot blocks instead of a contradictory global state.

   Then one line per picture with its job, in words (ours, user-verified — the
   `startFrame` *field* would lock the references out):
   `IMAGE p — START FRAME: the video opens on exactly this picture.` ·
   `IMAGE s — FRAME REFERENCE for shot 4: shot 4 opens on this framing.` ·
   `IMAGE q — SPACE.` · `IMAGE j — PROP: the flask.` (every prop with a plate,
   rule 7). **After this header, names only.** No descriptor is
   pasted anywhere in the prompt: a face is IMAGE n, a costume is IMAGE m, and
   one short clause names only what no picture shows (*"the flask on a
   cross-body strap"*).

   **Every reference is bound to appearance only** — one line after the
   picture jobs. It says a reference gives appearance and nothing else — the
   face, the garment, the object — and rules out copying its pose, framing,
   lighting, backdrop or catalogue stance. Without it the header tells the
   model what to copy and never what not to: *100% matched based exactly on
   IMAGE n* bounds nothing, and a single-view crop still carries a studio pose
   and a neutral backdrop that can leak into the shot. This does not reopen
   *views, not sheets* — the sheets stay cut, and a prompt that
   points at a panel is still a dispatch error. The two work together: single
   views stop the model *choosing* the wrong panel, and this line stops it
   copying the right panel's pose.
4. **The geography line** (ours) — one line, identical in every prompt of the
   scene: who is left, who is right, what is behind them (by the room map's
   side letter when the scene has a map), and the side of the room the camera
   never crosses. *"Nen frame-left at the pump, Rasa frame-right; the shell
   behind them (Side A); the camera stays on the apron side of the line."*
5. **The camera line** — one of the handbook's two, verbatim, by the film's
   `cameraDefault` (`handheld` or `static`) on `picsart_film_compile_prompt`. Both open `Breathing
   feel:`; one describes a handheld camera that moves with the scene's
   intensity, the other a static one that does not move at all. The compiler
   picks by the film's default move. What is decided HERE is whether it pastes
   either at all:

   **The line is dropped when every block carries its own camera fragment.**
   The handbook needs it because its example blocks say only
   *handheld* or *slow push-in* — a word, not an instruction — so something has
   to govern the camera for the whole video. A block written from
   `presets-camera.md` does not leave that gap: the fragment states what the
   camera does **and** what it does not do: the locked-off fragment says the
   camera is on sticks and then says it does not move at all, for the whole
   shot. Keeping the global line beside it puts two opposite instructions in
   one prompt — the handheld line's constant shake against that fragment's no
   movement of any kind — and the model has to pick. The risk that buys is a video where every shot
   drifts slightly, so the still shots stop reading as still and the moving
   shots stop reading as deliberate.

   So: a run whose shots mix moving and locked-off cameras **omits the camera
   line**, and each block's fragment is the only camera instruction. A run whose
   blocks do not each carry a fragment still needs it. `picsart_prompt_verify`
   enforces exactly that pair — drop the line and any block without a camera
   fragment is a dispatch error.

   This departs from the handbook, which keeps the line: if a take comes back
   weightless or drifting, put the line back.
6. **No music** — the handbook's line, verbatim. It asks for SFX and ambient
   sound and rules music out.
7. **No subtitles** — the handbook's line, verbatim, on every generation,
   followed by our one quality line. That quality line carries three things:
   readable faces and natural motion; a skin clause asking for matte, pored
   skin with no gloss — the one instruction that most reliably fights the
   render look on faces; and the frame rate and shutter angle, which are what
   make movement blur the way a real camera's does and are the most physical
   realism cue a video model takes. Shutter angle is
   **video only** — a still has none — so it lives here and never in
   `stylePrefix`.
8. **The cut list** (ours — the model most reliably honours a count in words).
   It states the shot count, the second each hard cut falls on, and the total
   running time, and it ends by saying the film runs in real time. It must say
   *hard cut*, or the model sometimes dissolves or whips between shots; the
   compiler writes the word and `picsart_prompt_verify` fails a prompt whose
   cut list disagrees with the shot list it was built from.
### Part 2 — one block per shot, the handbook's timeline

The handbook's template, with the six lines its Kling lesson names for every
shot box (shot type and angle · who is visible by name · action and body
language · emotion · the exact line · how it is said):

```
[X]-[Y]s
[Shot type], [camera angle], [camera movement]. [Who is visible, by name, and where in frame]. [Describe what the character(s) are doing — action, position, movement]. [What they feel]. [Name]: "[the line, exactly as it should be heard]" — [how it is said]. [the silence line]
```

- **Always start each beat with the shot type and camera movement** — *"Do not
  expect the model to guess the shot or camera move. Tell it clearly."*
- **One big clear action per shot.** *"Make sure each action can actually
  happen within the time you gave it. If it is a 3-second beat, the action
  should feel natural in 3 seconds. Read the line out loud. If it takes too
  long, shorten it or give it more time."* Action is a charge, a throw, a fall
  — never a flurry.
- **Every visible character gets an individual performance arc.**
  Name what each person physically does, what changes in their face or body,
  and the end state they reach by the cut. A group sentence such as *"they
  watch each other"* is not a performance. Neither is *stands / looks /
  watches / listens* on its own: pair a held position with a readable change
  — a jaw locking, breath catching, eyes breaking away, weight shifting,
  shoulders releasing — that answers the other character's action. This is
  especially strict for a silent listener in a dialogue shot; silence is
  reaction, not inactivity.
- **Run the visible-cast performance lint before dispatch.** For every shot,
  the names in *who is visible* must each appear in both the action/body-
  language sentence and the emotion sentence. Each must have a beginning and
  an end, even if the change is small. A missing name, a static stare with no
  evolving reaction, or an acting note for somebody omitted from *who is
  visible* is a dispatch error — repair the shot block before preflight.
- **Listener coverage must match the picture.** On a dialogue
  retake, compare the requested framing with who actually remains visible in
  the take or its approved framing reference. A prompt saying *only the speaker
  is visible* does not explain or repair a silent listener who is visibly inert.
  Resolve the mismatch: preserve the listener and direct their reaction when
  that is what the user wants, or restore the intended clean single when the
  complaint is framing. Do not silently crop out a requested performance.
  For each visible listener, write a compact **trigger → response → end state**
  in the speaker's block: e.g. at the claim best, the listener raises one brow,
  gives a small head shake, then leans toward the microphone ready to object.
  The response starts during the other person's line; it does not require
  extra dialogue, vocal overlap, constant gesturing or equal intensity.
  Preserve the approved speaker's delivery and keep reactions subordinate to
  the scene's focus. Include the final listening beat after speech ends.
  Verify this visually in the returned take: presence in the prompt is not
  evidence that the listener actually reacted. If viewing is unavailable,
  state that limitation rather than claiming the performance passed.
- **Emotion in every shot**, one or two words per visible face — chosen by you
  from the wheel in `presets-acting.md` (a state and how visible it is), read
  off the story's paragraph for that moment. The user is never asked to pick
  it on a board: acting is the chat's job, and a control for it is a question
  nobody needs.

  **Open that file and copy the compiled tell; do not write the feeling's name.**
  What goes in the block is the table's compiled tell for the
  emotion — for open fear, what the eyes, the weight and the breath are doing —
  a body doing something. What must never
  go in it is *desperate*, *panicked*, *overwhelmed*, *intense*, *emotional*:
  those are summaries of a performance nobody staged, and the model renders a
  generic face because a generic face is all the words describe. The same file
  carries the gaze line, the catchlights, the micro-life and the mask/leak pair
  that the block also needs; the full pre-dispatch list is *Performance gate*
  under **Dispatch**, below.
- **The line exactly, and how it is said as feeling, not as a voice type**:
  *"He says it angrily, breathless, and frustrated."* — never *deep voice /
  soft voice*.
- **The character's voice line is FROZEN. Not one word changes between
  generations (user decision).** Accent, tempo and texture, written
  once on the asset and reproduced **byte for byte** in every block that
  character speaks in: *"light Armenian accent, unhurried, a little rasp."*

  **The discipline is absolute even though the mechanism is not.** Conditioning
  on the same words reduces drift; it is not a guarantee of identical timbre,
  and nothing here should be read as promising one. That is exactly why the text
  is held rigid: it is the one variable we control, so it is held
  fixed. When a voice drifts anyway, the cause is the model, and
  the fix is a retake or the voice-changer pass at finishing — never a reworded
  voice line, which only adds a second cause to the first.

  Things that are **never** allowed to edit it: the scene's emotion, a raised or
  lowered volume, a faster or slower moment, a whisper, a shout, age, drunkenness,
  exhaustion, distance from the microphone, a phone or a radio. Every one of
  those belongs in the delivery clause or the action, beside the line. If you
  find yourself wanting to reword the voice field to fit a moment, that is the
  signal you are writing in the wrong slot.

  **This deliberately qualifies the law above it**, which refuses voice-type
  words — that refusal governs the *delivery* clause, where "deep voice" is a
  limp substitute for a played emotion. The voice line does the other job: it
  names the speaker's stable vocal identity. Feeling changes every line; the
  description never does.

  **Changing it at all is a version bump, not an edit.** If the saved line is
  genuinely wrong, or the character is meant to sound different from some point
  in the story, that is a new version of the asset with the reason recorded —
  and, like a changed look, it **re-opens every shot that character has already
  spoken in**, because half a film on the old line and half on the new is the
  drift this rule exists to prevent. Never a quiet in-place improvement.
- **The voice line survives every rebuild of a prompt.** It belongs
  to the character, not to the shot, so it is **re-read from the asset** every
  time a prompt is written or rewritten — not remembered, not paraphrased, not
  improved. The paths that rewrite a prompt and would otherwise drop it:
  - **a new shot ordered mid-project** (`../../picsart-film-edit/references/workflow.md` — an edit
    order routed back as a shot card) — written fresh, weeks after the rest;
  - **an ordinary regeneration**, where a note changes more than the camera and
    the whole shot is re-prompted;
  - **a note folded into a shot's prompt** at the edit, which rewrites prose
    around the line.

  A rebuilt prompt for a speaking character that carries their voice line in any
  form other than **byte-for-byte identical to the asset** — reworded, trimmed,
  expanded, reordered, or absent — is a defect, and the drift it causes does not show up until the
  clip is watched next to an older one. Anchored retakes are safe by
  construction — a camera-only change recompiles one header and re-prompts
  nothing. Edits and extends do not automatically inherit text from a previous
  API call: explicitly include the saved voice line whenever they generate speech.
  Before dispatch, check each speaker against their asset's `voice` field; fill
  a missing field using the asset-sheet rule, then copy it exactly.
- **Punctuation in the spoken line is delivery direction.** Commas,
  full stops and an ellipsis tell the model where the breath goes; a line typed
  without them comes back read aloud rather than spoken. Write the line as it is
  said — *"Somebody had to… I wasn't going to ask you first."* — rather than as
  clean prose. This is free, it changes no field, and it is the cheapest thing
  in this file.
- **After every spoken line, the handbook's sentence, verbatim** — the one
  that says the speaker has stopped and the room is silent. Without it the
  model fills the tail with mumbling, and the edit has no cut point.
- **A speaker who is not in frame is named**: *"Nen's voice is heard
  off-camera saying, '…'"* — never *"A voice is heard."*
- **The cuts are written as pairs** (`seams.md`, *Internal cuts*): a movement
  that carries ends mid-move in one block and is *already* under way in the
  next; a look is answered on the opposite side of frame; an exit right is an
  entrance from the left.
- **A character who is not in the opening frame gets an arrival, and a
  wardrobe view.** Write the entrance as a physical event in the
  block where it happens — the door swinging, the step across the threshold,
  the other faces turning to it — and carry that character's **wardrobe** view
  in `imageUrls` beside the face, because everything below the chin is
  otherwise invented at the moment of entry. A character who simply exists in
  shot 2 having been absent from shot 1 is the model's invitation to place him
  twice, and a face-only reference is its invitation to dress him twice. The
  head-count line (Part 1, item 2) says where he is until then.
- **The shot's size and its arrangement are two different instructions, and
  they must be compatible.** `size` is how far away the camera is;
  `arrangement` is whose shoulders are in the frame. An over-the-shoulder needs
  enough frame for the near shoulder, so it pairs with a medium close-up or
  wider — write an extreme close-up and an OTS into the same block and the
  model resolves the contradiction for you, differently each take. Nothing
  upstream refuses the pair: the card holds both values happily, so this is
  caught here or not at all.
- **What the film has already shown does not reset.** A detail the
  story changed on screen — a sleeve pushed up, a jacket taken off, a clasp
  fastened, a cup picked up, a cut on a hand, a phone now in a pocket — is true
  from that moment on, and every later block is written as if it happened. The
  doctrine that continuity inside a video is a given because one generation
  authors every cut holds for clothes, light and place; it does **not** reliably
  hold for a state the film created a few seconds earlier, and the model will
  put the cup back on the table.

  The failure is worst **across** videos, where nothing carries it at all: the
  pictures hold identity, and no picture knows the sleeve went up in the video
  before. So when a run ends with a changed state, the next run's blocks carry
  it in their own action sentences — *"the sleeve still pushed above the
  elbow"* — in the words of what is there now, never as a reference to the
  earlier video (*Language laws*, first law).

  **Where the line runs between this and a state variant.** A change big enough
  that the person no longer matches their picture — a bloodied face, a soaked
  coat, a shaved head — is not carried in words at all: it is a second version
  of the asset with its own views, ordered at script time
  (`../../picsart-film-development/references/screenwriting.md`, *Beats must
  photograph*), and from then on the run attaches that version instead. This
  clause is for the smaller things, the ones no picture will ever show and no
  asset should be spent on.

  **This is not a closing state line.** It adds no line to a block:
  it constrains the action sentence a block already has, and it only fires for a
  detail the film actually changed in view of the camera. A state nobody watched
  change is carried by the pictures and gets no words.

- **At a video edge** (`seams.md`, *The video edge*): the last block of a
  video ends with *ends in the middle of the movement — <the movement>*; the
  first block of the next video carries *picks that movement up from this new
  angle*, and is a clearly different shot type — a detail or an extreme
  close-up by preference.
- **When the camera moves through a set, name the set as rigid** in that
  block: *"the pump, the shell wall and the slabs keep their exact shape and
  position; nothing appears or disappears."* Without the clause the model
  invents geometry, such as shelving on every wall.
- **The card's own picks (ours).** A shot
  whose row came back from the shot list with a light or a colour the user
  chose — not the value the row was seeded with — closes its block with one line
  carrying exactly those: *`Light: window. Colour: slate blue dominant, worn
  khaki, signal red accent.`* — the preset fragments from `presets-lighting.md`
  and `../../picsart-film/references/presets-looks.md`, nothing reworded. A light
  the user did not touch writes nothing: the scene picture and the location
  already carry it. **Two values are written on every shot, whoever set them:**
  - **Lens and aperture.** Pass the card's lens as the shot's `fov` and the
    shot's aperture as `aperture` to `picsart_film_compile_prompt`, seeded or
    changed; an `auto` aperture has nothing to say and writes nothing. The setup
    carries no focal length or aperture, so a skipped lens leaves the model with
    no focal length at all, and a close-up the card shows at 85mm is shot at
    whatever the model picks.
  - **A palette other than `auto`.** The setup carries a colour scheme, never a
    palette, so a shot's palette is never already in the prefix.

  This line is ours, not the handbook's — the book's shot box has
  no lens or light — and it exists so that a choice made on the shot list is never
  a choice the model did not hear.

Nothing else goes in a shot block. No restated board values, no closing state
line, no light the user did not choose — the pictures and the setup carry
those. The lens and aperture are not restated setup values: they are the shot's
own, and the setup does not have them.

## Dispatch

### The step: verify the prompt against the rules

**`prompt-verify.md` is the gate, and it runs before every
`picsart_generate` call this skill makes** — still or video, first take or
re-roll, edit, extension, final-resolution pass. It is a *step*, not a
checklist: its first instruction is to open the files that govern the artifact
in front of you and take the requirements out of them, so it covers the rules
nobody has broken yet as well as the ones below. Its verdict — rule, source
file, pass/fail, evidence — is written before preflight, and a fail blocks the
dispatch.

The two gates that follow are the two passes of it that were learned the
expensive way and are therefore spelled out: *is the direction present* and *is
what is present direction at all*. Passing both is not the same as running the
step; the step is opening the files.

### Approved-intent gate — content before format, mandatory for every dispatch

Run this before **every** `picsart_generate` call this skill makes — a still
(scene picture, wide, room map, an asset sheet's portrait/profile/
T-cut) exactly as much as a video take, retake, insert, edit, extension or
final-resolution pass. **Knowing the rules below is not the gate — checking the
literal text about to be sent, against them, is.** Read the latest approved shot
cards/script and submitted chat/widget decisions, plus the affected character
records. Reconcile superseded notes first; do not reconstruct approval from the
draft prompt or memory. Persist the current requirements alongside the prompt
version, with the source decision/revision. An approval snapshot records what
the user already chose; it is not a new form for them to fill in.

**Three misses this gate exists to catch — each already a rule in this file,
each easy to skip in the final text:** a run's voice line written as a
back-reference (`Jake's voice (above)`) instead of repeated byte for byte inside
every block that speaks it; a second character tagged as visible across two
consecutive shots but never given an action or an emotion of his own —
described only through what the *other* characters feel about him — which the
model resolves by rendering him twice; and camera height, lens and light folded
into an ad hoc comma-separated header instead of stated as their own
instruction. Knowing the rules does not prevent these; checking the dispatch
against them does. The gate only closes the gap if it is actually run — against
the real, final text of the call about to be made — every time, not just the
first time a shot is authored.

Check the **actual tool arguments about to be sent**, after any rewriting or
parameter overrides, against those requirements:

- Every required line is verbatim, in the intended shot and order, assigned to
  the correct speaker and addressee (including gaze or off-camera status).
- Each speaking block contains the asset's exact saved voice description,
  written out in full inside that block — never a back-reference (`"(above)"`,
  `"as above"`, `"same voice as 1A"`) to a line stated once elsewhere in the
  prompt, even inside a single multi-shot run where it feels redundant to
  repeat it. Emotion, volume and delivery remain separate and match the
  approved direction.
- Every visible character — every tag in that shot's asset list — has their
  OWN action/body-language clause and their OWN emotion word, not only a
  mention as the target of someone else's reaction (*"Jake reacts to Marcus"*
  is not a line for Marcus). A tagged character with no clause of their own is
  a dispatch error, the same as a missing line of dialogue, whether the artifact
  is a video shot block or a still's Subject description / Pose & action /
  Emotion lines. Entry/exit positions, essential props and the beat motivating
  the next cut remain physically coherent.
- The selected operation and affected source windows match the request. Content
  the user wanted kept, including neighboring accepted clips, is not silently
  removed or regenerated. Any changed story, duration or speech needs agreement,
  not a quieter rewrite to make the payload pass.
- Native speech has `generateAudio: true`. For a visual-only edit preserving
  source speech, keep the source's audio policy and explicitly preserve its lines;
  do not assume an edit or extension inherits a previous prompt's voice text.
- Camera choices — height/angle, lens, light — are stated as their own explicit
  instruction (the closing line below, for a video shot block; the still
  handbook's own labelled `Shot size:` / `Camera angle:` lines, for a still),
  never compressed into a shorthand list written for a human reader's
  convenience. A comma-separated summary is a note to the user in chat; it is
  not the model-facing instruction, and the two must not be conflated.

### Performance gate — is it direction, or is it a description?

The gate above asks whether direction is **present**. This one asks whether what
is present is **direction at all**. Both halves run before every dispatch, still
and video. A prompt can pass every structural check above and still render a cast
of mannequins, because "each character has an emotion clause" is satisfied by a
clause that names a feeling instead of showing a body.

**Open `presets-acting.md` and write each face from the table. Never from
memory.** That file is not background reading for this step — it is the step's
input, and the single most common way this gate fails is never opening it.

- **Every emotion is a wheel position at a named intensity** — one of the eight
  (joy · sadness · anger · fear · surprise · disgust · trust · hope), written as
  the compiled tell, not as a feeling-noun. The table's entry for fury is
  renderable — it names the neck, the distance and the speed of the movement;
  *desperation*, *panicked*,
  *overwhelmed*, *angrily*, *intense*, *emotional* are not — they are summaries
  of a performance nobody staged. An adjective that is not in the table is a
  dispatch error, however vivid it reads in chat.
- **Intensity is a decision, and 1 is the default.** *"Intensity is how much of
  it is visible, not how much is felt"* — suppression is the cinematic register,
  and a man holding something down with a gun in his hand frightens an audience
  more than a man screaming. Check the run end to end: if every face sits at
  the top of the wheel for its whole length, nobody chose an intensity, they
  defaulted into shouting. Maximum volume from the first frame is not tension,
  it is noise — and it contradicts the setup's own `withheld information`.
- **Anyone hiding something carries the mask/leak pair.** `fear at intensity 2,
  masked as anger` — two things fighting in one face. A character with one flat
  layer and nothing underneath has no tension in him to photograph.
- **Every visible face has a named gaze target, listeners included.** An
  unnamed gaze is where generated faces go dead; listening is a performance.
- **Eye-life is requested explicitly** — blink rate plus `live catchlights`.
  A face without catchlights reads as rendered, which is the exact complaint
  "it looks AI" describes.
- **Micro-life is specified at least every one to two seconds of shot length.**
  A five-second block with one static state described in it is four seconds of
  freeze, however much the camera moves.
- **Stillness is written as what it costs.** *"he holds himself still, breath
  shallow, knuckles whitening on the rail"* — never `calm`, `composed`,
  `motionless`, `nobody moves`, `stands there`. Those phrases freeze the render;
  the body working not to move is the performance.
- **Something escalates physically across the run.** Name what changes state
  and when: the grip tightening, the barrel pressing in, the hand's shake
  growing, the voice dropping. A threat established in frame one and held
  unchanged for twelve seconds stops being a threat about two seconds in —
  tension is the *change*, not the situation.

**What failing this gate looks like.** A 12-second run of a man holding a
woman at gunpoint while a third man walks in — a premise that cannot fail to be
tense — comes back flat (*"I didn't feel it. The video does not pass
tension."*) when its entire emotional direction is `overwhelmed desperation`,
`panicked and pleading`, and `he says it angrily, breathless, and overwhelmed`.
Not one of those is a wheel position. No intensity chosen, no gaze named in
three shots, no catchlights, no micro-life, no beat of stillness, and across
twelve seconds nothing tightening by a millimetre. Every one of those mechanisms
is written in `presets-acting.md`. A prompt authored from a memory of what a
prompt looks like, without opening that file, is how a scene with a gun in it
arrives boring.

**Run the deterministic check before preflight.** It is a tool call —
`picsart_prompt_verify`, which takes the approved material, the literal request
about to be dispatched, the film, and the blocks, and returns a verdict row per
rule. Its rows cite this file by part and item, so a failure names the
paragraph that explains it. See `prompt-verify.md` for the arguments and how to
read the verdict.

The approved material is a snapshot from what the user approved, not from the
prompt:

```json
{"revision":"shotlist-v4 + submitted correction","shots":[{"id":"bridge","dialogue":[{"speaker":"@jake","addressee":"@marcus","text":"I can't! Every AI shot comes out different!","delivery":"panicked, shouted at high volume"}],"action":"Jake notices Marcus approaching and recoils","preserve":"Keep both neighboring accepted clips unchanged"}]}
```

Use an explicit empty `dialogue: []` for a silent shot. The request is the
exact tool arguments, with `prompt` and model parameters at top level or in
`extra` as the live tool requires. The blocks map each shot ID to its exact
contiguous shot-block text copied from that actual prompt; for a single shot
they may be omitted. Include every affected shot, including unchanged dialogue in an
edit, so omission cannot disappear from the check. Speaker IDs match asset tags;
voices are read directly from `film.json.assets[]`, never a rewritten voice copy.
Fields such as `addressee`, `delivery`, `action` and `preserve` carry the semantic
requirements for assistant review; the tool does not interpret their meaning.

The tool checks required lines and their order within/across blocks, missing
voice fields, exact voice text per speaking block, and audio enabled when dialogue
is required. It returns a request fingerprint (`requestSha256`) and a failing
verdict when a check fails; it does not dispatch or authorize spending. Keep its
result with the prompt version.
Any change to the prompt, payload or approved requirements invalidates the check;
rerun on the exact request that will be preflighted and sent.

**A mechanical pass is not a semantic pass.** The tool cannot establish that a
quoted line is actually instructed as speech, detect all contradictory prose,
judge speaker/addressee binding, acting, spatial logic or model performance.
Read those checks above before dispatch, and check the delivered take afterward.
When the tool cannot be called, perform the same comparisons explicitly and
record that they were manual; never claim an automatic check ran.

Repair omissions before spending; do not weaken the approved snapshot to pass.
Ask the user only when there is a genuine unresolved creative conflict, not to
repeat an existing approval. This gate supplements schema/price preflight and
the existing credit approval rule; it is not a server-enforced guarantee.

### Format and reference checks

The call carries **`imageUrls` only**, in the order the tagging header
numbers them; the `startFrame` field stays empty; every picture's job is in
the header's words (user-verified). Before dispatch, read the prompt
once against this list — a failure costs a keystroke here and a take after:

- every `IMAGE n` in the prompt exists in `imageUrls` at that position, and
  every picture in `imageUrls` is named once;
- every name in a shot block was assigned in the tagging header;
- every person in any shot block has their identity view and wardrobe view in
  `imageUrls` — a start frame covers only the people visible in it, and a
  person carried by words alone is a failed take before it is sent (a bridge
  sent with one face in the frame brings the other woman back in a long coat
  with two flasks; rule 7, `../../picsart-film/references/overview.md`);
- **and that holds for a person only PART of whom is in frame — a hand, a
  shoulder, the back of a head — which is not an exception to the rule but its
  sharpest case.** A body part is still that person's skin, hair and build, so
  it needs their identity view exactly like a face does. Dropping it "because
  we never see the face" is how a Black character in the foreground of an
  over-the-shoulder gets a white hand and light brown hair: his face view
  pulled from the references to make room, his wardrobe view kept, and the
  words describing him only as a navy jacket sleeve. Reference budget is never freed by removing an identity; it is freed
  by removing a *place* or a *prop* that the words can carry instead. And when
  a part is all that shows, the prompt says which part and whose it is —
  *"the hand and the back of the head in this frame belong to that man"* —
  because the header's default reading of a face view is *the face*;
- every object is named in one place with one position, and with its count
  where the model could double it — *one flask, in her right hand*, not also
  *on her strap*;
- every prop the film gave a plate to (`picsart-film-assets`) rides in `imageUrls` as
  `IMAGE n — PROP: the flask` and is named by that number where it appears —
  the same law as the people: words alone draw a round canteen as a flat
  flask, and the model's thirty slots are for this;
- the picture count and the bytes are under the model's live limits — the
  `imageUrls` max off `picsart_model_params`, the inline total off a probe —
  and when they are not, **nothing is dropped in silence**: the list goes to
  the user with the pictures you would drop marked and the reason (a wide when
  the map is in the set), and the user chooses.
  A person's identity and wardrobe views and the place's map are never on that
  list (rule 7);
- the `startFrame` field is empty, on this and every clip — a bridge or a
  one-shot reshoot included;
- no picture is a preview or a sheet — a contact-sheet frame is never a
  reference (export the frame at full size first), and a multi-panel sheet
  never travels (`picsart-film-assets`);
- the shot seconds sum to the video's length and match the cut list;
- no word in the prompt refers to another video — "previous", "earlier",
  "again", "continuing", "as before" — the model never sees it;
- every spoken line is followed by the ending sentence; every speaker is
  visible or named off-camera;
- the breathing-feel line, the no-music line and the no-subtitles line are
  present, verbatim;
- on a video that is not the film's last, the last block ends mid-movement.

## Language laws — wordings the models punish

Hard-won rules; each exists because shots failed without it:

- **The model never sees the previous video.** Every prompt is read on its
  own, so a prompt never says "continuing from the previous scene", "as
  before", "earlier", "again", "still", "returns to", "the same place as".
  Those words tell the model nothing — a prompt opening *"CONTINUOUS FROM THE
  PREVIOUS SCENE. Rasa has walked a few steps off"* gives it no way to know
  where she has been. Write what is in the frame now
  — *"Rasa stands eight metres from the pump, the flask in her right hand"* —
  and let the joining be done by the same pictures in both videos, the
  geography line, and the movement the first shot picks up (`seams.md`). The
  handbook's director instruction bans the same words: *"Never use the words
  'earlier', 'before', 'previous', 'again', 'return', 'continue', 'as before',
  'last time' … anywhere in any prompt."*
- **Quotation marks are dialogue. The model SPEAKS whatever is inside them.**
  An emphasis word quoted in the ACTION prose is delivered as a spoken word:
  `on the word "four" the forearm tightens once` gives a take that opens with
  Jake saying **"four"** and only then the real line, and every such word has
  to be hand-trimmed out of the cut afterwards. Write the emphasis
  bare — `on the word four the forearm tightens once` — which renders the
  identical gesture and speaks nothing. The same law reaches the **saved voice**:
  a descriptor ending *"...to cut through panic (\"Jake! Look at me!\")"* is
  copied verbatim into every block that character speaks in, so it offers a spare
  line on every one of their shots. Fix that in the ASSET's voice text, never in
  the block — the block must carry the voice byte-for-byte.
  `picsart_prompt_verify` fails the dispatch on both.
- **Never write a character's age, in any language.** Content filters harden
  the moment a number that could read as a minor appears. Carry age through
  role, clothes, and action.
- **Actions only in positive form.** "Does NOT fall on his back" is ignored or
  inverted — write "falls on his stomach". There is no negative block: write
  what IS in the frame.
- **Keep a ban dictionary per film** in `film.json.banDictionary` — words the
  models or filters punish, with their working substitutes ("dark" → "low
  key", "jolting" → "rapid motion"). Check it before writing a shot block.
- **A shot block carries at most three sentences of action.** An overloaded
  block smears; split the shot, not the detail.
- **Calming phrases freeze the frame.** "Nobody moves" produces a freeze;
  write stillness as held tension (`presets-acting.md`).
- **Complex action opens mid-action** — "ALREADY mid-swing, the door ALREADY
  cracking"; the approach is its own shot.
- **Speeds are numbers** — "the car passes at 40 km/h". "Fast" and "slowly"
  are the two words a prompt most reliably loses. No tempo words at all:
  rhythm is the seconds.
- **Describe what a liquid does, never what it looks like** (learned over four
  rolls on one shot of water): *"the water has spread into the creases of her
  palm, the skin under it dark and slick"*, never *"a bead of water with a
  highlight"* — that gives a glass marble. The same for dust, blood, rain:
  what it does to the surface it lands on.
- **One flat colour for hair, one costume, one carry.** "Dark
  brown, sun-bleached at the crown" is two colours the model resolves by
  inventing a third; a headband is "a separate object on her head", or it
  becomes hair.
- **A frame outranks the words.** A picture that shows the old action pulls
  the video back to it however the block reads; a picture that contradicts
  the pictures beside it (a clean room beside a wrecked frame) makes the model
  average them. Attach only pictures that agree with the shot.

## Worked example — sc01 of the garage film, one video, three shots shown

```
STYLE — drama: quiet realism, faces carry the story. analogous colour scheme around amber: … Arri Alexa 35: … framed for 16:9.

INT. GARAGE — DAY. Cal comes to make Tobin sign the deed before the buyer arrives tomorrow; Tobin keeps working and does not look up until the end.
EXACT 2 CHARACTERS — NO DUPLICATES.
Cal = ONLY the dark-blue work jacket and the cropped grey hair. Tobin = ONLY the brown overall and the beard. Never duplicate either, never add a third.

Main Subjects:
• Cal face and outfit 100% matched based exactly on IMAGE 1 (face) and IMAGE 2 (outfit)
• Tobin face and outfit 100% matched based exactly on IMAGE 3 (face) and IMAGE 4 (outfit)

The deed 100% matched based exactly on IMAGE 5

Scene setting is based on IMAGE 6 (scene picture), IMAGE 7 (wide), IMAGE 8 (room map)

Expression of Tobin is closed and unhurried
Cal facial expression remains angry and controlled throughout. No panic, no fear.

IMAGE 6 — START FRAME: the video opens on exactly this picture.
IMAGE 9 — FRAME REFERENCE for shot 3: shot 3 opens on this framing.
IMAGE 7, IMAGE 8 — SPACE.
<the appearance-only line — item 3>

Cal frame-left by the tarp, Tobin frame-right at the bench; the shelving wall behind them (Side A); the camera stays on the roller-door side of the line.

<the camera, music, subtitle and quality lines — items 5 to 7, pasted by the compiler>

<the cut list — item 8, over 6 shots cutting at 4, 9, 14, 19 and 24 seconds, 28 seconds total>

0-4s
Wide shot, eye level, slow push-in. Cal frame-left walks in from the tarp toward the bench; Tobin frame-right sorts bolts and does not look up. Cal is angry and holding it; Tobin is closed. Cal: "You sold the manifolds." — flat, like a fact he has checked twice. <the silence line>

4-9s
Medium shot on Tobin, eye level, handheld. Tobin frame-right keeps sorting, his hands slow but do not stop; Cal's shoulder in the left foreground. Tobin is calm, hiding shame. Tobin: "Somebody had to." — quiet, not looking up. <the silence line>

9-14s
Close-up on Cal, eye level, handheld. Cal frame-left, jaw set, eyes on Tobin's hands; he starts to turn his head toward the door. Cal is furious and about to leave. Ends in the middle of the movement — the head turn.
…
```

The next video's first block, if this were the edge: *"0-4s Extreme close-up
on Cal's hand, three-quarter height, static. Cal's hand closing on the deed on
the bench; picks up the head turn from this new angle — his shadow crosses the
paper as he turns."*

## Iterating on this prompt

"Make the light softer" touches the scene picture and the geography line, not
a shot block. "He should sound angrier" touches how the line is said, not the
line. "Wider" is a new shot type in that block. One change per call; if a
requested change would touch three places, say which three and why before
regenerating — that is usually two iterations pretending to be one.
