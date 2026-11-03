# Shooting on Seedance

Read this when the film's model, or the edit or extend model a repair uses, is a Seedance one: its
id starts with `seedance-`. It adds to the steps in `SKILL.md` and never replaces them. Source: the
Seedance 2.5 prompt guide from BytePlus,
<https://docs.byteplus.com/en/docs/modelark/seedance-2-5-prompt-guide>.

**Load BytePlus's own prompt skill for the model before the first compile**, even when the shots
are already approved: `sd25-pe` for Seedance 2.5, `sd2-pe` for Seedance 2.0. Write each shot's
action, lines and `extra` by it, and every prompt written by hand (an edit or extend). The compiled
run prompt still goes out verbatim.

## What the compiler does for you

Pass the model's id as `model` to `picsart_film_compile_prompt`, and give each `cast` member the
`language` of their saved voice. The compiler then writes the shot blocks the way Seedance reads them:

- a spoken line names its language and puts the delivery before the words, with nothing after
  them. Tone or action hung after a line is what makes Seedance burn the words in as subtitles.
  On 2.5 the words go in braces, `{…}`, as `sd25-pe` writes dialogue;
- whoever is in frame and not speaking keeps their mouth closed, and a shot with no line says so;
- every reference is named `@Image N`, as both BytePlus skills name them;
- on Seedance 2.5, the run leaves out its total duration and the frame-rate line: those are
  `picsart_generate` settings there;
- on Seedance 2.0, each block opens with its shot number as well as its seconds, since 2.0 ignores
  timestamps.

Never write any of this by hand in `extra`: the compiler owns it, and verify checks its text.

## Its notes

Act on them before the quote:

- **No `language` for a speaker:** copy it from their saved voice and compile again. Without it the
  model may answer in another language.
- **A cut between whole seconds** (Seedance 2.5): the shot lengths are the user's. ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) whether to
  round them; 2.5 places cuts on whole seconds.
- **Glowing-eye words** ("fanatical", "eyes blaze"): Seedance can light up the eyes on strong
  emotion words. Write the body instead, in plainer words. If the scene needs the intensity, add
  "normal human eyes, no glowing eyes" to `extra`.
- **Water or echo words with audio on:** they can bring bubbling or whistling into the track. Keep
  them only where the scene needs them.

## References

- Order the people in `images` by when each first appears. Seedance matches references to people
  in that order, and a swapped order swaps faces or voices.
- One subject per image, single views; 1 to 8 people in a run is where it holds.
- Prefer views no larger than the output resolution. An oversized generated still can come back as
  fingerprint-like texture in grass, leaves or fabric.
- Text that must be spelled right travels as a picture of the text, not as words in the prompt.

## Start and end frames

A Seedance start or end frame field cannot travel with reference images, and it locks the output's
aspect ratio to the frame's. A run keeps its frame as `IMAGE 1 — START FRAME` in `imageUrls`, as
`references.md` says, because a run always carries its people. Only a clip with no references at all
(a plain shot animated from one approved still) may use the model's own start frame field, with
`aspectRatio: "adaptive"`. Its end frame must share the start frame's ratio, or it is stretched.

## Edits and extends

The Seedance edit and extend siblings follow the source clip, never a new shape:

- **An edit keeps the clip's ratio and length.** Name the one thing that changes, from what to
  what, and from which second to which second ("from 4 to 6 seconds, his hand sets the cup down
  instead of lifting it"). Close the scope in the same prompt: everything else in the clip stays as
  it is. A moving subject that is swapped takes the old one's place: same entrance, path, speed and
  exit, and the old one no longer appears.
- **A change of ratio or length is not an edit.** It is a new run with the clip as a reference.
- **An extend says which way it goes**, forward from the last frame or back from the first. The
  first new frame continues the clip's posture, props, camera and light. A person stays one person
  through it, never doubled. Going back, nothing from later in the clip appears early.
- **An edit followed by an extend is two calls**: edit first, then extend the edited clip.

Read each sibling's settings with `picsart_model_params`. The ratio and length the source locks
are among them.

## Two Seedance versions in one film

Seedance 2.0 and 2.5 render the same prompt with a visibly different look, so a film keeps one
version. To carry a 2.0 clip's look into 2.5, extend the 2.0 clip on 2.5's extend model rather than
generating fresh.
