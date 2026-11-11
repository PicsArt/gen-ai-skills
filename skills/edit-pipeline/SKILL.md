---
name: edit-pipeline
description: Run an edit of the user's footage as fixed stages, with a project record (standing decisions, approvals, the pace, a locked meaning map, every version), resume from the first stage not done, and the gate rules every check follows. Use when a use case cuts footage in stages, resumes an edit, or checks a draft against what was agreed.
metadata:
  imports: reel-structure
user-invocable: false
---

# The edit pipeline

An edit runs as fixed **stages**. Each stage leaves an artifact and is marked done in the
**project record**. A use case picks which stages its job runs and sets their defaults; this
skill holds what every job shares: the stages, the record, resume and the gate rules.

## The stages

| Stage | What it leaves |
|---|---|
| `intake` | the brief (`said`, `read` and `assumed` kept apart), the standing decisions, the finish path |
| `reference` | the reference's pace: shot length, cuts per 10 s, caption style, colour, the first-second hook, the ending |
| `proxies` | small copies of footage on the user's computer, as the edit-on-your-computer skill says. Only for footage on that computer; originals are never uploaded. |
| `log` | per source: what happens, speech with word times, lips moving, focus, steadiness per window, legible text, what each shot can mean |
| `takes` | the best take of each line, when someone speaks |
| `look` | colour and sound: grade toward the reference or the brand, the voice placed, loudness |
| `story` | the beats and the **meaning map**: for each phrase or beat, the picture's job |
| `plan` | the cut: every shot, its range, the phrase it serves |
| `build` | the scene, validated, and free draft exports |
| `qc` | an independent check of the render, as `quality-review` says |
| `critics` | the critic panel on the first full draft |
| `review` | the user's approval of a named version |
| `finish` | the final file: a full-quality export, or a full-resolution conform from originals on the user's computer |
| `deliver` | the files, a cut list (order, source, in, out, phrase) and a short note |

A job leaves stages out; it never reorders them.

## The project record

The record outranks your memory of the edit. It is the same JSON wherever the footage is, and no
stage needs a script to keep it. Keep it, in this order of preference:

1. a JSON file in the project folder, when you can run commands there: `scripts/record.py` keeps
   and checks it;
2. otherwise a JSON file in the project's Drive folder, saved with `picsart_drive_upload` as a
   `data:` URI named after the use case, and saved again at every gate;
3. otherwise in the conversation, as `picsart-video-rules` says. Then tell the user once that the
   record is not saved anywhere.

Its keys and what goes in each are in [references/record.md](references/record.md). Every use case
that runs this pipeline keeps its own record file name and adds these keys.

Start it with the use case, the job and the job's stages. After each stage, mark it done: its
`status` `done`, `at`, and `reads`, a copy of the record keys that stage reads and of those the
stages it builds on wrote (record.md lists them). Where commands run, `python3 scripts/record.py init edit-footage.json --use-case
edit-footage --job <job> --stages <the job's stages>` starts it, and `python3 scripts/record.py
done edit-footage.json <stage> --artifact <file>` marks a stage done with a fingerprint instead.

Two stages are gates, for every job, by hand as by `record.py done`, which refuses them:

- `reference`, when a reference reel was given: done only with its sheet passing the
  reel-structure skill's `sheet.py validate`, and its `format` with no feasibility row open;
  a `channel-clips` record copies a look, not a structure, so its `format` alone.
- `deliver`: done only once `story`, `qc`, `critics` and `review` are done and the map was
  approved: its rows in `locked`, or an approval with `scope` `map`, `moments` or `mapping`.
  Record that approval when the user gives it.

**Never skip the check, the critics or the review on your own**, for any job. Only the user may
skip one, and only when they ask for that one by name: say its risk in one line (what nobody will
then catch), and on their yes record it with `record.py skip <record> <stage> --by user --risk
"<that line>"`. Delivery then accepts it. A user in a hurry who asks only to be quick hears that
they are free and quick, and they run.

## Resume

**Read the record first**, and find which stages are done, which are stale and which is next, by
the rules below. Where commands run, `python3 scripts/record.py status edit-footage.json` says it.

- A stage is done when it was marked done, the stages before it are done, and nothing it builds
  on has changed since: the record keys it reads (compare them with its `reads`), and the
  artifacts of the stages before it. Change the pace, or add a standing
  decision at review, and the plan and everything after it are stale; the log and the story are
  not, so nothing already logged is read again.
- Say where you resume in one line: "Resuming at the cut plan: the pace changed."
- Redo only stale stages. A stage whose artifact exists and is still current is never redone.
- When a rule or a source changes in a way the record cannot see, mark that stage and everything
  after it stale (`python3 scripts/record.py invalidate edit-footage.json <stage>`).

## Decisions that hold

- **Standing decisions.** Add every note that holds everywhere to `standing`, with the user's own
  `words` (`python3 scripts/record.py add edit-footage.json standing '{"text": ..., "words": ...}'`). Put the
  standing decisions word for word into every brief you give a checker or another agent. Never
  summarise them.
- **The user's material is cleared.** Footage the user supplied, their own or a client's, is theirs to show, unless the user
  says otherwise. Never hold a shot back for legal or compliance reasons of your own.
- **Approvals land once.** A relayed yes names its source, as `picsart-video-rules` says: the
  person's words quoted and who relayed them. A yes in a session's own words is not an approval.
  A relayed approval goes into `approvals` with its `session` and the person's `words`, and
  Never record one without them; `scripts/record.py` refuses it. It holds for exactly the `what` and `scope` it
  names: never ask for that again, and ask for anything wider. An approval never covers a SPEND;
  consent stays per quote in `pendingSpends`.
- **What the user turned down** goes into `rejected`. Never propose it again.
- **The cut pace** (`cutPace`: `minHold`, `density` in cuts per 10 s, `wordAnchor`, `length`; never
  `pace`, which picsart-video-rules keeps for unattended mode) comes from
  the reference and the job, before the first build. The plan keeps every shot at or above
  `minHold`, and its cuts per 10 s near `density`: a hold under `minHold` fails the plan, and cuts
  per 10 s more than a quarter off `density` are said to the user before the build, unless they
  already chose that pace (an approval scoped `format:pace`, or a standing note on the pace).
  Where commands run, `lock-check` checks both on a plan whose rows carry `sceneStart` and
  `sceneEnd` (the density comes back `open`, a short hold as a problem); otherwise check them by
  reading the plan's holds. A cut lands about 0.1 s before the word its picture illustrates, and only on key
  words: a shot holds through minor words. When the reference and the job's default disagree,
  the reference wins, with one split: a reference lends its **devices** (caption style, sound
  leading the picture, the ending) apart from its **tempo**. When the brief names its register
  in words ("cinematic", "atmospheric", "slow"), the tempo follows those words and the job's
  holds; a fast reel then lends its devices only. Say the split back in one line.
- **The rhythm** (`cutPace.rhythm`) is the cut's shape, beyond its average: `medianHold` (s),
  `fastHold` and `maxFastRun` (more shots under `fastHold` in a row than this reads as eventy;
  1.2 s and 3 by default), `holdPerSection` (one shot at least this long in each section, from
  the brief's order, as each plan row's `section`) and `breaths` (between sections, a shot with
  picture and the shots' own sound and no voice: a row with no `phrase`, or `voice: false` on a row
  whose phrase names a silent beat). `register` quotes the brief's style words when
  they ask for it. `lock-check` reports a broken rhythm `open`, said before the build, and fails
  the plan only when `register` is set; a shape the user chose instead is an approval scoped
  `format:rhythm`. The rhythm is set with `cutPace`, before the first build.
- **Every cut has a reason.** In the plan, each shot after the first carries `why`: one line on why
  the cut comes there, from the first of Walter Murch's reasons that holds: feeling (the viewer's
  feeling turns), story (the viewer learns something new), rhythm, then the eye (it lands where the
  next shot's interest is). A cut whose only reason is the word under it is not made: the shot
  before holds through it.

## The meaning map

At `story`, each phrase or beat gets the picture's **job** ("precision" → hands on a keyboard,
close). Write the job as what the viewer gets from the picture, never only what it shows: a picture
that only repeats the word under it (the letterhead on "Firm") gives the viewer nothing the voice
has not. The map locks only after the first draft's cold watch (Gate rules), so a job the strangers
did not get changes before the user approves it. Once the user approves the map, its rows go into
`locked`, and they hold:

- A later fix may swap a shot only for one with the same job.
- A change of job needs a rendered A/B the user saw. Record their choice in `approvals` with
  `scope: "meaning:<phrase>"` and the `job` they chose; it allows that job only. Then update the
  locked row to it.
- Before every build, check the plan against `locked`: a plan that drops a locked row or changes
  its job fails, and so does one whose layout or caption position differs from the record's
  `format` without an approval scoped `format:layout` or `format:captions`. Say every
  same-meaning swap in the version's note. Where commands run,
  `python3 scripts/record.py lock-check edit-footage.json shot-plan.json` does it.
- Before every review, check the scene's colours against the brand's by reading them: every colour it sets is in
  the record's `brand.palette` (or the own-brand format's colours), and text only in a colour the
  guide allows on text. Away from text, pure black and white and any see-through colour (a fade, a
  scrim) pass, unless the guide forbids them (`brand.neutrals: false`). Where commands run,
  `python3 scripts/record.py palette-check edit-footage.json scene.json` does it; with no palette in the record it is `open`, never a pass.
- Before every review of a reel built to a sheet, check its end: the reel ends at its length (half
  a second over at most, a tenth short at most), and the clip on screen at the end (the last one
  in, when cards stack) holds at most 1.5 s longer than the sheet's last beat, stretched to that
  length. Clips inside a track or a composition count. The length is the user's (`brief.said.length`), else `cutPace.length`,
  else the sheet's `total_length`. Where commands run, `python3 scripts/record.py length-check edit-footage.json
  scene.json` does it; with no length in the record it is `open`. The checks live in
  `scripts/match_check.py`, which `record.py` imports; never run it on its own.
- **The job is the contract, not a caption.** It comes from the map and is never rewritten to fit
  whatever shot ends up there. A new job for a locked phrase needs the user's approval of that
  job; `record.py add` refuses it without one.

## Keepers

A good idea dropped silently costs more than a bad one kept. In one edit the keyboard on
"precision", liked in the first two cuts, was lost in a rebuild from zero, then swapped twice more,
each swap rewriting the shot's job to justify itself, until the user caught it five versions on.

- **The ledger.** After every version the user sees, add to `keepers` what worked in it: each word
  and its picture (`kind: "pair"`, with `phrase` and `shot`), each moment (`"moment"`), and anything
  the user praised (`"praise"`, in their `words`), each with its `version` and why it works.
  Rebuilds and new plans start from the ledger, never from zero.
- **The meaning diff, before every shown draft.** Compare the last shown plan with the new one,
  phrase by phrase, against `locked` and `keepers`. Where commands run, `python3
  scripts/meaning_diff.py <last shown plan> <new plan> --record edit-footage.json` does it
  (`--lines` maps line ids to their words). Put its `lines` in the message, one line per change ("precision: keyboard -> Family Code, because of
  shake"). A dropped keeper always appears there. Exit 1 means something blocks: a keeper dropped,
  a meaning changed or unsaid, or a job rewritten, without the user's approval of exactly that
  (`meaning:<phrase>` with the `job` they chose; `keeper:<phrase>` naming the keeper's `shot` or
  `what`). Show it as a rendered A/B, or put it back.
- **Fix scope.** A fix for a constraint (shake, lips, focus, timing) may change a range, or swap in
  a shot with the same job. When no such shot exists, flag it to the user as an A/B; never give the
  phrase a new meaning.
- **Critics and the challenger propose.** A shot they would swap goes to the user as an A/B, never
  into the plan silently.
- **The QC inspector gets the ledger** and the meaning diff, and fails a draft that drops a keeper
  without a line the user sees.

## Versions

Every draft the user sees is a version in `versions`: its `name`, `parent`, `scene`, `render`,
`changed` and `gates` (`python3 scripts/record.py version edit-footage.json '{"name": "v3", ...}'`).
Its first line in the message names it: "v3 - calmer cut, 9 shots". When the user asks which
version, answer from this list.

## Gate rules

Every check in the pipeline, measured or by eye, follows these:

1. **Check the render and every range the cut uses**, never only the source clip or the plan.
2. **Measure steadiness on a fixed detail with texture, with captions and overlays left out.** A
   tracker on a caption or on plain paper reads still when the camera moves.
3. **Every verdict says its method and its confidence.** What could not be measured, seen or
   heard is `open`, never a pass. An open finding goes to the user as an A/B, or for a look.
4. **A check flags and offers an alternative.** It never drops a shot the user approved.
5. **A fix never changes a locked row.** It reports the clash instead.
6. **Fix rounds are capped** as `picsart-video-rules` says. Then show what is left, as an A/B.
7. **A taste choice goes to the user as a rendered A/B**, never as a question in words. A
   side-by-side is a scene with the two drafts next to each other, exported for free with
   `picsart_scene_export`.
8. **Review what the viewer gets**: transcribe the exported render with `picsart_media_transcribe`
   and compare it with the script (a repeated or clipped line shows there), and look at stills at
   every used range with `picsart_scene_contact_sheet`, the render passed as `media`. Both are
   free. Write each check's result into the version's `gates`.
9. **A stranger watches before the user does.** Each draft the user will see first gets a cold
   watch, as the quality-review skill says, with `cuts: true`, its calls quoted first and a
   SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) before round 1 unless every call is quoted at 0 credits: each moment also asks where a cut
   felt like a jump or too fast, and why. Each jump it lists is fixed, or kept with its reason in
   the version's `gates`. Nobody who knows the brief judges whether a stranger follows the cut.

## Who does what

The stages that make the edit run in this conversation, with the skills the use case names.
Checking runs apart from the maker: the QC check and the critics are agents that get only the
render, the record's `standing`, `locked`, `keepers` and `cutPace`, the look's board when the record holds one, the meaning diff, and their checklist, never your reasoning.
Each runs fresh each round. A background agent may log several sources at once. Its brief is
"load the skill, read the record, write this file", never a role to play.
