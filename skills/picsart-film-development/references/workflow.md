# Development — look, story, model, video plan, shot list

Everything in this skill is **free** (except optional candidate stills, which are
image-cheap). It is also where the film is actually made: a director who walks
out of Stage 1 with a tight bible spends half as much in Stage 6. Do not rush
it because nothing here renders.

## Stage 1 — six steps, in this order, always

The order is the rule. Say where you are in it when a step opens — *"Stage 1 ·
step 3 of 6 — the story, for your yes"* — and when the user asks about the
order, quote the step, never answer from memory.

1. **The idea.** Ask for a premise only if none was supplied. Pre-set duration
   and frame on the look console from the user's words or stated destination;
   otherwise use 90 seconds at 16:9. The user
   changes them on the console. Propose the ending in the story rather than
   asking another intake question.

2. **The look console — before a word of story is written.** Open
   `picsart_film_setup` with `suggested.selections`: genre, tone, `palette: "auto"`,
   ratio and duration from step 1, camera and lens family. Choose a colour scheme
   and hue only when the idea names a colour; otherwise leave `scheme`, `hue`
   and `hueDegrees` out. When pre-setting a hue, include its wheel angle from
   `../../picsart-film/references/presets-looks.md`. Give one line of why per inference.
   Focal length, aperture, light and an individual shot's palette belong on
   the shot list. The setup locks the style prefix, lens family and colour
   scheme before the story or shot list is written. A tone seeds only camera
   and lens; colour changes preserve the tone.
   The user's submitted Lock is the look's lock. Store the compiled prefix
   verbatim in `bible.stylePrefix` and the selections in `bible.setup`, keeping
   `hue` and `hueDegrees` exactly as returned. The feedback and per-tool compile
   mappings are in `../../picsart-film/references/widget-feedback.md`.

3. **The story — one plain document, shown in chat, for the yes.** Written for
   the locked genre, in the viewer's words (`dramaturgy.md`, *The
   story*): ten lines at the top — who, where, what each wants, what stands
   in the way, what happens, which beat the film is built toward, how it ends,
   the one thing the viewer is left with, what the user's brief fixed (quoted,
   never assumed), the genre — and then **every scene as what we see and hear,
   in order**: one plain paragraph per scene, the lines in quotes, ending with
   its length in seconds. No camera words, no film vocabulary, no production
   notes: a reader who knows nothing about film reads it as the film. Inside a
   stated identity budget ("this fits two faces and one place — here it is
   inside that"), inferred from the idea, never asked. The user says yes, or
   says what to change; a change is a rewritten paragraph in the next message,
   and the yes comes on the rewritten text. Recorded: the ten lines as
   `film.json.story`, the scenes as `docs/story.md`. Never write the story to
   a file the user has not seen: a story shown as plain paragraphs draws real
   notes at once, while one filed unshown is first read after the pictures
   exist.
4. **The video model.** Read `picsart_model_catalog` (`mode: "video"`,
   `purpose: "generate"`), filter by the console's ratio and by native
   multi-shot at the finish resolution, and put two or three survivors on
   `picsart_model_choice` with exactly one badged `recommended` (the `picsart-film`
   model policy carries the filter). Record `film.json.model.id`,
   `shoot.ceilingSec` and `shoot.editModel`. The pick belongs here because the
   video plan cannot be written without it: the model's ceiling is what fills
   each video, its `imageUrls` max is the reference budget, and its video-edit
   sibling is the repair path.
5. **The video plan — reviewed with the shot list.** Against the selected
   model's live ceiling, assign each shot to a run and write one sentence
   explaining each run boundary, including boundaries inside a scene. Save
   the run ids, scenes, `cutSec`, `genSec` and `join` in `film.json.runs[]`.
   Present the plan once on `picsart_shotlist_board`: each shot carries `run`
   and the opening shot carries `join`; use the board's `note` for the concise
   run-length summary. This tool has no top-level `runs` input. The board's
   submission approves the plan and shot list together. Text fallback shows
   the same grouping and asks one lock/change question.

6. **The shot list — one board, all scenes, camera only.** Below.

**Combine story approval and model selection where the host allows it.**
Show the story and `picsart_model_choice` in the same response, with two or
three live-catalog candidates. Say explicitly that choosing one accepts this
story and selects the model; a story note reopens the paragraph first. If the
host does not deliver a combined decision, collect the missing approval
explicitly. This reduces turns without inferring consent from a preview.

**One rule with the order: if the genre changes at any point** — the user
re-opens the console, or says "make it an action film" — **the story is
rewritten first**, before any picture or shot list moves. A drama story under
an action lock is two films, and everything built on it is rebuilt.

**A story note is answered with a paragraph, never a board.** When
the user's note is about what happens — who does what, who has what, where
they are, what is said — rewrite that scene's paragraph in the story, show it,
get the yes, then rebuild the cards it touches and re-open the board once.
This holds at every stage: on the board, after a picture, after a video. A
note like "Nen goes and grabs the water" answered with shot-list boards costs a
board per round and drifts into the wrong scene; the same note is a one-minute
rewrite of one paragraph.

**The identity budget never buys silence.** Do not offer a mute character, a
wordless treatment, or a voice-over-instead-of-dialogue version as a saving or a
safety measure: the film's video model does native lip-synced dialogue in-shot,
so people talk. Silence is a directing choice the story earns, and if the user
asks for it, give it to them gladly.

**Action is not a cost flag, and neither is anything else in the story.** Never
flag action, crowds, water or fire as "complex" or propose a cheap rewrite
beside them: that is how a film about two women fighting for water gets
written as "grip and weight, never blows". The video model was chosen for the film's genre; the
story decides what is in it. The one thing still written around is in-frame
text (signs, letters) — models write text poorly, so it is added in the edit,
never generated in-shot.

**When the user brings their own script**, keep it: it is the story document,
and step 3 is already done. Read it once for the two things the medium cannot
do — in-frame text, a character's age as a number — and say them in one line
each as suggestions. Nothing else is reviewed; the video model and the video
plan follow.

## The shot list

**The board approves camera.** It opens once, after the story and
the selected model are approved; this board also approves the video plan. What the user changes on it is camera — size,
movement, lens, light, colour — and seconds, and whatever they change is
written into that shot's block, never lost
(`../../picsart-film-scenes/references/prompt-blocks.md`, Part 2, *The card's own picks*);
a card's action and line are copied from
the story's paragraph and are never rewritten on the card. A note about what
happens is a story note (above): the paragraph first, then the board rebuilt
from it. Never open a board to show a story — when the board is where the user
reads the story, every story change costs a board.

Turn the story into two lists, per `breakdown.md` (load it when
actually breaking down):

1. **The shot cards** — every shot as a card: scene and shot id, location, time
   of day, who is in frame by tag, props, the action in one to three
   sentences, the line verbatim or a dash, seconds; who stands where relative
   to the camera; what the character feels; the camera — size, movement, lens,
   angle. These are not notes for a DP — they are future prompt lines.
2. **The asset list** — people, places, props: every character, every place
   the film plays in, the props the story is about, each with a future `@tag`.
   A durable change the story does to a place or a person — the room after the
   fire, the shirt once it is bloodied — is a row too, because the model
   generates the clean version otherwise; anything that resets between scenes
   is not. Nothing is tiered and nothing is flagged: every character gets the
   handbook's three pictures, every prop a plate, every place its pictures
   from the scene (`picsart-film-assets`, `picsart-film-scenes` step 3).

**Shot length is a habit, not a gate.** Dramatic shots run 3–8 seconds, action
shorter, a reaction shorter still — the handbook's *"Use the duration based on
what the shot needs."* A shot over 8 seconds carries its reason in one line on
the card and nothing else. Never lengthen a card to fill a video; the video is
filled with short shots (`picsart-film-scenes`, *The run pass*).

Present the shotlist through `picsart_shotlist_board` — **one call carrying
ALL scenes** (`scenes: [{id, slug, shots}, …]`), never one board per scene:
the board's single approval covers exactly the scenes passed (its feedback
names them in `scope`), which makes "one confirmation covers a set" mechanical
instead of a guess. Pass `model`. Seed every pill from what is already decided
— the scene's light, the focal length the shot size calls for, and the camera
move. Seed `palette: "auto"` unless the shot needs its own colour; any selected
palette must fit the film's scheme and hue. Surface compiler conflict notes
before dispatch. Pass every shot's lens as `fov` and its aperture to the prompt
compiler, whether seeded or changed, and include each non-auto palette's Colour
line. The user touches only what they disagree with. Without the server board, a
markdown table per scene with one "anything to change in any scene?" at the
end.

**Call the board and say nothing.** It already carries its own instruction —
each scene's header reads "N shots · Xs — type straight into any shot" — and the
preset chips are visible pickers that show film language rather than asking for
it. If a pass genuinely needs framing the board does not already give, pass it
as the board's `note`, not as a message. Feedback per
`../../picsart-film/references/widget-feedback.md` — an `approved` verdict may carry
staged edits (apply them first), cell edits apply to the cards, `removed`
shots leave the scene. The board returns the fields it owns — action, line,
tags, values, order, cuts — and those replace yours wholesale; what it never
carried (`design`, `refs`, `run`, `trim`) stays on the shot by id. A changed
action that tells a different story than the story's paragraph is a story note:
the paragraph is rewritten and shown first, never straight into a prompt, and
never answered with another board.

Sum running time by the cards' seconds. A script page is roughly a minute, but
the seconds column is the number that counts.

## References and the visual bible — part of Stage 1

Stage 1 also covers references and the visual bible; the next stage is Stage 4,
`picsart-film-assets`.

**References are optional inspiration, not a stage.** The look is locked on the
console at Stage 1 step 2, and nothing gathered afterwards reopens it. When
the user has images — their own uploads (`picsart_media_upload` opens the
upload panel), film stills they name — **look at each one before captioning
it**: export a 1280 px JPEG with `picsart_media_export` and view it
(`picsart_view_image`, free); a URL is a link, not pixels; never web-fetch an
image URL and never caption a reference you have not seen. Every image gets a
caption, *what exactly we take from it* ("light from the window", "jacket
fit"), and the captions feed the descriptors at `picsart-film-assets` step 1.
Anti-references — "like this: never" — become bans written into prompts in
positive form. Counts and categories, for the user who wants a board, are in
`visual-bible.md`. **This spends nothing**: a generated moodboard
is never an automatic charge, and the first scene picture doubles as the tone
moodboard.

**A photo of the thing itself is not a reference — it is the asset.** When the upload is the real person, the real product, the real
place the film is about, save it exactly as sent (a Drive copy, probe-matched
byte for byte) the moment it arrives; it registers locked at Stage 4 without
a board, and goes to the video model untouched as IMAGE 1 — `picsart-film-assets`,
*When the user brings the asset*. Decide by looking: film stills, artwork and
mood photos are references and never reach `imageUrls`; a person, product or
place is identity. Ask only when an image genuinely reads both ways, one short
question.

**The visual bible is the console's output, and the console's Lock is its
lock.** `bible.stylePrefix` is compiled by `picsart_film_setup` at step 2 and
stored verbatim; there is no later lock and no prose put in front of the user
to approve — they see the prefix's effect on the sheets. The text portraits
(appearance, age, build, costume by item, movement, posture) and the location
descriptions (architecture, textures, light, condition, atmosphere, palette)
are written at `picsart-film-assets` step 1, when the sheets are about to be
generated, and approved with the sheets. Design so the look **rhymes with the
character**: every visual choice — scar, fabric, colour, the state of the shoes
— restates who this person is and what the story does to them; a detail that
says nothing is a detail the model will vary freely, and a detail with two
readings ("dark, bleached at the crown") is resolved by the model inventing a
third. If the genre moves later, the story is rewritten first (Stage 1's rule)
and the console is re-run. The story's period is **not** one of the console's
controls — it lives in the location descriptors and the scene context, never
in a look preset. A film with two visual worlds runs the setup once per world.
The look locks once, at step 2; no later gate locks it again.

**The voice policy is `native`, and there is nothing to decide.**
Each shot's generated voice is the performance. Record
`film.json.voicePolicy: "native"`. Every speaking character also gets a canonical
voice description on its asset sheet, chosen without an extra user question and
copied verbatim into every speaking prompt; see
`../../picsart-film-assets/references/asset-sheets.md`. Native does not mean unspecified.
Description consistency reduces drift but does not guarantee an identical voice.
Review recurring speakers across video edges; a finishing bed can smooth room
tone and level changes, not a changed speaker identity. Where a recurring voice
drifts too far, retake the worse clip; finishing does not re-voice dialogue.

**Optional gate-out deliverable: the pitch package.** Everything a pitch needs
already exists at this lock — assemble `docs/pitch.md` (logline, the bible's
tone and style prefix, cast portraits, key boards, planned runtime and budget
range) referencing the Drive-saved copies of the boards, never bare CDN links
(they expire). One free assembly step; offer it, don't push it.

On a short film **one batch is the whole asset list**: stills are cheap, so
Stage 4 generates every picture in a single pass and the user approves all of
them on one board (see `picsart-film-assets`). Splitting into production blocks is for
genuinely large lists (≳15 assets) or when the user asks — never the default.

## Gate out (to `picsart-film-assets`)

The look locked on the console · the story and the video plan with their yes ·
the video model recorded · the shot list approved. Update `film.json`
(`bible`, `gates`) silently and route straight on to `picsart-film-assets`, in the
same turn.

## Costs

| Free | Charged |
|---|---|
| interview, console, story, video plan, shotlist board, captions, all text | candidate stills via `picsart_generate` (image rates — a fraction of video; still preflight and mention it) |

## Traps

- **Front-loading the story before the console.** A story written as a drama,
  then locked as action, is two films; the order above prevents it.
- **A story the user never read.** A one-word yes on a table of beats is not a
  yes on the film; the story is shown as paragraphs and the yes comes on those.
- **Answering an order question from memory.** Quote the numbered step.
- **Answering a story note with a board.** The paragraph is rewritten first;
  the board is rebuilt from it once.
- **Writing the story in film words** — "turn", "payoff", "beat", "OTS", "grip
  and weight, never blows". The story is the one artifact that exists to be
  judged as a film by someone who is not making it; camera belongs on the
  card and production notes in `film.json`, so a story written in production
  terms cannot be judged for what it is.
- **Writing the fight soft to protect the render.** Nobody measured that; the
  genre decides, and the model was chosen for it.
- Skipping the durable-change rows ("we'll handle the wrecked room later") —
  the missing picture surfaces mid-production.
- References without captions, or all beauty and no light/optics — light and
  optics are what the model follows best.
- Filing the user's photo of the actual person as one more mood reference and
  generating a lookalike from a descriptor. The photo is the asset, saved
  untouched, first in every run.
- Writing the visual system as taste ("moody, cinematic") instead of prompt-ready
  words. If it cannot be pasted into a prompt, it is not locked yet.
