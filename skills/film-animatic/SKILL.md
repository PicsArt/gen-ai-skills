---
name: film-animatic
description: Draft a film or drama episode as a voiced storyboard animatic before any video is bought, with a still per shot, app screens built as scenes, every line voiced at its shot's time, cut with captions and watched until the user says yes. Use when a film's story and shots are worked on stills and sound first.
user-invocable: false
---

# Film animatic

The animatic is the film before video: one picture per shot, the real voices at the shot's
timing, cut together and watched. Stills and sound are cheap and video is not, so the story and
the cinematics are settled here, and the user's yes to the animatic is what opens shooting. A
first paid video is never where anyone first sees the movement or hears a voice.

The use case owns the gates; this skill owns the method. Every paid call below is a SPEND as
picsart-video-rules says, quoted with `picsart_preflight` and bought on a yes (or a stated spend
limit that covers it). Building, checking, the editor and the export are free.

## 1. Cards that can be drawn

Before a panel is bought, every shot card carries what film-story-writing's breakdown asks for,
with two fields the animatic depends on: the **mode** (the camera's relation: lens, observed,
point of view or voice-over) and the **eyeline** (who or what the person on screen looks at or
speaks to). One action per shot, one feeling per face, one peak. Why someone decides is not a card
field: it is a must-know in the film's viewer track, and the cold watch tests whether the picture
gives it.

From this skill's folder, run `python3 scripts/animatic_plan.py <file>` on the cards (its header
has the input). It fails a card with no mode or eyeline, a change of mode the picture does not
show, and a film without exactly one peak, and warns an opening shorter than 1.5 s. Fix an error
on the card before any picture; a fix that changes what happens is a story note, answered as
film-story-writing says. A clean plan says the cards are complete, never that a viewer will follow
them.

## 2. Panels

One panel per shot, at the film's frame:

- **Each scene's opening panel is its scene picture**, made as film-shot-generation says. Every
  other shot gets a still compiled from its card with `picsart_film_compile_prompt`
  (`kind: "still"`), with the present people's locked views and the scene picture as references,
  checked as the compiler's `check` says, and sent verbatim to `picsart_generate`.
- **One quote for every panel of the film or episode**, and one batch on the yes (at most 10 a
  call), filed in the project's Assets folder before you look at them.
- **Continuity against the master.** Look at each panel beside its scene picture before it goes on
  a board: the same faces and wardrobe as the locked views, the same light and set, the eyeline and
  screen direction the card says. Put them on `picsart_film_review_assets`, 12 tiles a board, with
  "continuity with the scene picture" as its `judge`. A changed panel is its own SPEND.
- **A real app's screen is built, never generated.** A phone or a computer screen in a shot is a
  scene layer built from the user's own screenshots or recording (stills with
  `picsart_media_video_stills`), laid into the panel's screen area, one state per beat. A
  generated picture of an interface is not used, and a screen the user has not supplied is asked
  for, not invented.

## 3. Sound

Every line is voiced as the voice-over-generation skill says, but in each person's own locked
voice (the cast's saved voice notes), one line per clip. Ambience is one bed per scene, and an
effect goes where a card's action makes a sound (a tap, a shutter, a door). Quote the voices, the
beds and the effects as **one batch**, then probe every voice line's real length with
`picsart_media_probe`. A sound the user supplies is used as it came.

Run `animatic_plan.py` again with each line's probed `sec`: it re-times every shot so the line
fits, and gives each line its start in the animatic. A line's real length moves its still, never
its words.

## 4. The animatic scene

Build it as scene-building-basics says, from the plan's timeline:

- each panel an image layer for its shot's seconds, hard cuts between shots;
- a move only where the card's camera moves (a slow push-in on a push-in card), eased in and out;
  a static card stays still. Never add a move to pass a motion check;
- a code-built screen as its own layer over its panel, changing state on its beat;
- every voice line an audio layer at its planned start, the scene's bed under it, each effect on
  its action;
- the captions and on-screen text in the house style the user gave, otherwise as the
  spoken-captions skill says. A caption carries only what is said: never a speaker's name the
  viewer has not heard, a card's id or a stage direction. The viewer reads them as the film.

Then `picsart_scene_validate`, and fix every error. From quality-review's folder run
`python3 scripts/cut_check.py --slides <file>` on it, as quality-review says: the joins, overlays and
screens are checked, and the motion rules wait for the cut. Look at
`picsart_scene_contact_sheet` with `times` at the middle of each shot (8 at most per sheet).

Without code execution, time the shots by hand the same way and say the scripts were not run.

## 5. Review as watched

- **A cold watch first.** Run quality-review's cold watch on the animatic against the film's
  viewer track, with the cast's voice lines as its `voices`, quoted first as its reference says: a
  SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) before round 1 unless every call is quoted at 0 credits. You wrote the story, so you can't tell whether a
  stranger follows it; nor can a critic who reads the cards. Fix what falls under its floor, the
  earliest gap first, by changing what is seen or heard, and watch again with fresh viewers, a round
  the yes did not cover quoted again. If the user says no, the review line says "no cold watch yet".
- **Then the critics, with the gap list.** Where quality-review's critic panel runs, it judges the
  contact sheet and the gap list, never the cards or the timed script. Each critic says what it
  could not see or hear (the voices, the timing at speed): a thing it could not judge is not a pass.
- **Then the user watches it, cold.** REVIEW the animatic in `picsart_scene_editor`, with its
  sound, as picsart-video-rules says: a draft opens cold.
- **An MP4 only when asked.** `picsart_scene_export` (free) when the user wants a file to watch or
  share, or when the host cannot show the editor; give its `downloadUrl`.

**Notes route by meaning.** A note on what happens is a story note: film-story-writing rewrites
the paragraph, the cards follow, and only the panels and lines it changes are made again, under
their own SPEND. A note on one shot (the framing, a face, a line's reading) goes to that panel or
that line alone. A note on timing or a cut is a free re-time or re-cut. Build it again, check it,
and REVIEW again, until the user says yes. Keep each round's notes and changes in the record.

## 6. After the yes

The approved animatic is the film's plan for everything after it:

- **Its timing is the cut's reference**, and each approved panel is that shot's key frame: it opens
  the shot's run as film-shot-generation says. An approved voice line can be the run's reference
  audio where the model takes one.
- **The user picks which shots go to video.** Quote the picked shots only; a shot the user keeps
  as a panel stays in the cut as it was approved, a choice the user made, not a still played to
  fill a gap.
- An animatic the user calls final for its own sake (a pitch, a table read) is delivered as it
  is, with no video.

## Traps

- Buying video before the animatic is approved, or calling the scene pictures alone an animatic.
- A silent animatic called reviewed: the user has not heard the voices yet.
- An animatic called reviewed with no cold watch, or a cold watch given the cards, the story or the
  track: whoever knows the story fills in what the picture never shows.
- Captions carrying speaker names, card ids or stage directions.
- A generated interface on a screen.
- A move added to a still to pass a motion check, or to make the draft look busy.
- Re-making every panel for one note.
