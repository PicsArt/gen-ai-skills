# Prompt verification — the step every dispatch passes through

**Nothing generates until its prompt has been verified against the rules, and
the verification is written down.** Still or video, first take or re-roll, edit
or extend, a board's own suggestion or a prompt a human asked for by name: the
call is made after this step, never before it, and never in the same breath.

## Why this is a step and not a checklist

A checklist enumerates the mistakes somebody already paid for. It is always
behind the rules, and it is silent about every rule nobody has broken yet — so
the first time a new one is missed, it costs a take, and only then does it get
a line. And a run can go out with several house rules broken, **every one of
them already written down**, none of them checked, because the prompt was
authored from a memory of what a prompt looks like rather than from the files
that say what one is.

So the step is not "read the list below". **The step is: open the files that
govern this artifact, take the requirements out of them, and check the literal
text of the call against what you just read.** The rule corpus is the files.
This page is only the procedure for sweeping them, and the procedure is what
makes it cover rules this page has never heard of.

## Which files govern what

Open every file on the artifact's row. Not the ones you think you remember, and
not only the one you were writing in.

| Dispatching | Governing files |
|---|---|
| a video run prompt | `prompt-blocks.md` (Part 1, Part 2, Dispatch) · `presets-camera.md` · `presets-lighting.md` · `presets-acting.md` · `seams.md` · `../../picsart-film/references/presets-looks.md` · `../../picsart-film-assets/references/asset-sheets.md` (how views travel) |
| a scene picture or wide | `step-3-scene-pictures.md` step 3 · `prompt-blocks.md` Part 1 (the film lines) · `presets-acting.md` · [presets-looks.md](../../picsart-film/references/presets-looks.md) · [asset-sheets.md](../../picsart-film-assets/references/asset-sheets.md) |
| a room map | `step-3-scene-pictures.md` step 3, the map item |
| a character sheet, portrait, profile or prop plate | [asset-sheets.md](../../picsart-film-assets/references/asset-sheets.md) · `../../picsart-film-assets/references/asset-efficiency.md` (the asset prefix) · [presets-looks.md](../../picsart-film/references/presets-looks.md) |
| an edit or extend call | `prompt-blocks.md` Dispatch · `../../picsart-film-edit/references/join-repair.md` |
| a final-resolution or re-roll pass | whatever the original artifact's row says — a re-roll is a new dispatch, not a repeat of an approved one |

A file that turns out not to govern this artifact costs one read. A file that
governed it and was not opened costs a take.

## The five passes

Run them in order against **the actual tool arguments** — the `prompt` string
about to be sent, with every parameter as it will really go, after any rewrite.
Never against the draft shown in chat, which is a different artifact with
different words in it.

### 1 · Derive

From each governing file, write out what it requires *for this artifact*: the
lines that must be present, the strings that must be verbatim, the values that
must come from a preset table, the things the file says are dispatch errors.
Derive it from the open file. "I read it earlier" is the failure this whole
step exists to prevent, and re-reading costs seconds.

### 2 · Verbatim

The cheapest pass and the highest-yield, because so much of this pipeline is
*paste this exact string*. Every canonical string appears byte-identical, not
paraphrased, not improved, not compressed. **Which strings are required is a
property of the artifact, not a fixed list** — derive it from the row's files,
because a string that belongs on a run and not on a portrait is a failure in
both directions:

*A video run* — the world's compiled `stylePrefix`; the head-count line and its
exclusives; the appearance-only
reference line; the breathing-feel camera line; the no-music line; the
no-subtitles line with the skin clause **and its frame-rate and
shutter-angle ending**; and the cut-list form with the words *hard cuts* and *real time*.

*A scene picture or wide* — the same `stylePrefix`, the same
head-count line and exclusives, the same appearance-only reference line, and the
film's medium line. **The camera-feel line, the frame rate and shutter angle,
the no-music line and the cut list are video-only and must be ABSENT.** A
photograph has no camera movement, no shutter angle, no soundtrack and no cuts;
a still whose prompt carries them is the same defect as a run that lacks them,
and it is what happens when the governing row is read for the run and the
still's row is written from the run's memory.

*A portrait, profile, sheet or prop plate* — `bible.assetStylePrefix`, **not**
the scenic `stylePrefix` ([asset-sheets.md](../../picsart-film-assets/references/asset-sheets.md), *Every image prompt carries the
film*; defined in [asset-efficiency.md](../../picsart-film-assets/references/asset-efficiency.md)), the film's medium line, and the
negative prompt banning the other medium. Pasting the scenic prefix onto a
neutral sheet and asking the model to ignore the staging is named in that file
as the error.

*Every artifact with a camera or a light in it* — every camera and lighting
sentence as `picsart_film_compile_prompt` pasted it, never the bare board word
(`pan`, `handheld`) that the fragment exists to replace, and never a wording
you composed. **The wordings are server-side and this pass cannot be done from
the preset files** — they carry the ids and the judgement about which to
choose, not the text. So the check here is not "does this match the table" but
"did this prompt come out of the compiler, and has anything been edited into
the middle of a sentence it pasted". Adding a sentence beside one is fine;
rewriting one is the failure.

*Every block that speaks* — that character's saved `voice` text, in full,
inside the block itself.

**A paraphrase is a failure even when it reads better.** These strings were
tuned against renders; prose that merely sounds like them has none of that
behind it. If a sentence in the prompt is one you composed, ask which file it
was supposed to come from.

### 3 · Completeness, per shot

For every shot block (or every subject on a still): each tag in the shot's
asset list has its own action, its own emotion from the wheel, and a named
gaze; the speaking blocks carry the voice line; the camera values are stated as
instruction rather than folded into a header; entrances, exits, props and the
beat that motivates the next cut are all actually written. A name that appears
only inside somebody else's sentence has not been directed.

### 4 · Arithmetic

The checks that are numbers, and therefore the ones with no excuse:

- **Spoken line against shot length.** Count the words, divide by ~2.5 per
  second, add the beat of silence the line is required to end on. Over the
  shot's `sec` means it will be gabbled or truncated — and the fix is a board
  change, because `sec` belongs to the user (below).
- **Run length**: Σ shots' `sec`, handles per the film's setting, snapped to a
  duration the model's own `duration` enum actually offers.
- **References**: count against the model's `imageUrls` max; total bytes
  against the budget; every image's short side against the floor.
- **Head count** (`prompt-blocks.md` Part 1, rule 2): `EXACT <N> CHARACTERS —
  NO DUPLICATES.` with N counting everyone who appears at any point, latecomers
  included, plus one exclusive line per person.
  A scene that never says *three people* in a room with an open doorway is a
  scene the model may answer with four — or with the same person twice.
- **Aspect ratio and resolution** against the console's lock and the model's
  enums.

### 5 · Judgement

What no script can answer, and what the take actually lives or dies on:

- Does anything **escalate**? Name what changes state and when. A threat held
  unchanged for the run's whole length stops reading as a threat.
- Was an **intensity chosen**, or did every face default to the top of the
  wheel? Suppression is the cinematic register; maximum volume from frame one
  is noise.
- Does anyone hiding something carry the **mask/leak pair**?
- Does a character who is **not in the opening frame** get a real arrival to
  animate — a door swinging, a step through — rather than appearing between
  cuts, and do they have both a face and a **wardrobe** reference? A person the
  model must invent mid-shot is one of the reliable ways to get a mess
  (`prompt-blocks.md` Part 2, *A character who is not in the opening frame*,
  and Part 1 rule 2 for counting him).
- Do the **references bind to appearance only** (`prompt-blocks.md` Part 1,
  rule 3) — face, clothes, object — and
  not to the pose, light or background they happen to carry?
- Is the shot's **size compatible with its arrangement**
  (`prompt-blocks.md` Part 2, *size and arrangement*)? An extreme close-up
  and an over-the-shoulder are different geometries; a card can hold both and
  nothing upstream refuses it, so the model picks for you.
- Do the **joins** hold (`seams.md`) — internal cuts paired, the video edge on
  a movement, no two adjacent cuts opening on the same still?

## The verdict is the artifact

Write it before preflight, one line per rule that had to be checked: **rule ·
the file it came from · pass or fail · the evidence**. Any fail and nothing
dispatches — the prompt is repaired and the pass runs again from 1.

An unwritten verdict is a skipped step. This is the whole enforcement
mechanism: a check nobody can see is indistinguishable from a check that never
happened.

## The tool does the mechanical half — call it, do not re-derive it

`picsart_prompt_verify` takes `kind`, the approved material, the **literal tool
arguments** about to be dispatched, the film, and the blocks; a model's limits
are optional. Pass the compiler's returned `promptToken` unchanged beside
its exact prompt; recompiling or editing the prompt requires a fresh matching
token.

`kind` is not optional: it is what keeps a still's rules apart from a run's.
The tool accepts `run`, `still` (alias `scene-picture`), `portrait`,
`profile`, `sheet`, `plate`, `map`, and `edit`.
The kind decides which house lines are **required** and which are
**forbidden** — a still that carries the camera-feel line, the shutter angle or
the no-music line fails, because a photograph has none of those.

What it checks, and therefore what you must never check by eye:

- every required house line present **byte-identical** (compared on collapsed
  whitespace, so wrapping is fine and paraphrase is not), and every video-only
  line absent from a still;
- `EXACT <N> CHARACTERS — NO DUPLICATES.` present, with N equal to the approved
  cast — latecomers counted;
- the cut list in canonical form, its shot count and its total matching the
  shots;
- every approved line present, exactly, in the right block, in the right order,
  with no block missing, duplicated or out of order;
- each speaker's saved `voice` written out in full inside the block they speak
  in, and `generateAudio` true wherever there is dialogue;
- each spoken line's word count against its shot's `sec`;
- `imageUrls` within the model's max, no duplicate view, and the `startFrame`
  field empty;
- the performance gate's banned words — the author's own prose only, since one
  house line legitimately contains one.

It returns the verdict table (`rule · source · pass · evidence`), an error list,
and `requestSha256` — a fingerprint of the exact arguments it read. **Paste that
table and that fingerprint; they are the written verdict.** A verdict whose
fingerprint does not match the arguments you then dispatch is a verdict about a
different prompt.

Pass 5 is deliberately not in the tool and must never be faked with one. It
returns `semanticReviewRequired: true` on every call, including a clean one.

## How this is made to run

Three mechanisms, in increasing order of strength:

1. **The step is named at every entry point** — `prompt-blocks.md`'s Dispatch
   section, `step-2-shot-design.md` for runs and for step 3's stills, [asset-sheets.md](../../picsart-film-assets/references/asset-sheets.md)
   for every portrait, sheet and plate, [join-repair.md](../../picsart-film-edit/references/join-repair.md) for edits and extends.
   There is no path to `picsart_generate` in this pipeline that does not pass a
   pointer to this file.
2. **The verdict is a visible artifact.** A check nobody can see is
   indistinguishable from a check that never happened, so the table goes in the
   message before preflight. Its absence is detectable by the user, which is
   the only reason it works at all.
3. **The tool cannot be talked out of it.** It does not hold a typed copy of
   the rules: it compares against the same tables `picsart_film_compile_prompt`
   pastes from, so the checker and the compiler cannot disagree — those tables
   are the only copy that exists, so the rules cannot drift between them.

**None of that is a guarantee.** All three depend on the assistant choosing to
run the step, and the rules can be quoted correctly minutes before they are
broken in a prompt. `picsart_generate` does not refuse an unverified prompt, so
treat a dispatch with no verdict block in front of it as a defect worth
stopping for, not a style lapse.

## Traps

- **Verifying the chat draft instead of the tool arguments.** They diverge:
  the compression that makes a prompt readable in a message — a voice line
  turned into *"(above)"*, camera values folded into a header — is exactly the
  class of defect this step catches, and it is invisible unless the literal
  string is what gets read.
- **Deriving from memory because the file was open recently.** Quoting the
  rules correctly in conversation is no protection against breaking them in a
  prompt minutes later.
- **Silently repairing a value the user owns.** `sec`, the palette, the lens,
  the light, the line itself — a verification failure on one of those is a
  finding to take back to the board or to the user, never something the verify
  step edits on its way past.
- **Running it once per shot list rather than once per dispatch.** Every
  re-roll, every edit, every extend is its own call with its own arguments, and
  an approved prompt that has since been rewritten is an unverified prompt.
