---
name: film-shots
description: Shoot a film's shots as runs - narrowing the video models a film can use, packing shot cards into multi-shot generations against the model's ceiling, joining runs, the scene pictures a run opens on, the key frames any generated video is drafted as before its footage is bought, compiling and verifying every prompt on the server and passing it verbatim, the reference images a run carries, following async jobs, splitting takes at their real cuts, and routing notes to an edit, an extend or a re-roll. Use when a film's video models are narrowed, or its shots are planned into runs, pictured, generated, checked or repaired.
user-invocable: false
---

# Film shots

Author every shot on its own; generate them together. The unit of generation is the **run**: as
much of the film as fits one generation at the model's ceiling, scenes included. The model makes
the cuts inside it, and the take is split back into shots at the cuts it actually made. Read these
before the step:

| File | Read it before you… |
|---|---|
| `references/seams.md` | write how one shot meets the next, or where one run meets the next |
| `references/camera.md` | choose or write a shot's camera move |
| `references/realism.md` | write a shot's action, sound and what persists through a run |
| `references/scene-pictures.md` | make a scene's wide, scene picture or room map |
| `references/references.md` | put a run's reference images together |
| `references/takes.md` | split a take, or judge one |
| `references/repairs.md` | act on a note about a take |

## The model

One video model shoots the whole film, and the runs are packed against its ceiling, so choose it
before the shots are planned.

1. Narrow the video models with `picsart_model_catalog`: `mode: "video"`, `purpose: "generate"`,
   `acceptsImage: true`. Keep the rows whose `supportedAspectRatios` hold the film's ratio. Edits,
   extends and upscalers are out.
2. Read `picsart_model_params` on each model that survives. Keep only those that hold
   **several cuts inside one generation** at the finish resolution and take enough reference
   images for a run.
3. For each one kept, find its edit and extend siblings: the `picsart_model_catalog` rows from the
   same provider with `purpose: "edit"` that edit or extend a clip. Repairs use them.

## Runs

**Packing.** Read the model's ceiling and accepted durations with `picsart_model_params`; never
from memory. Pack the ordered shots into the fewest runs that fit. A scene change, a climax, a
close-up or a hunch that a shot works better alone is not a reason to start a run. Merge adjacent
runs that fit together, and say which you merged.

**Durations.** A shot's `sec` is its length in the cut. A run's generation length is the sum of its
shots' `sec`, plus one handle at each end of the run (not between its shots), snapped up to a
duration the model accepts. That is the run's `genSec`. Inside a run, the
silence after a line and a designed tail hold are the only trim room at a shot boundary.

- The ceiling is a packing limit, not a shot length. Never merge several short actions into one
  long shot to fill a run.
- Dramatic shots run three to eight seconds, action shorter. A shot over 8 s carries its reason;
  over 12 s it is a deliberate long take.
- A scene of more than 12 s held in one shot gets a recommendation of two to four shots of
  coverage, with what is lost without it written on its card.

**The cut-by-cut pass.** Walk each scene's neighbouring shots as pairs and write the pair's rule into
both blocks (`references/seams.md`). Then three checks on the cards, fixed on the card before
anything generates:

1. Two shots of the same subject in a row are two sizes apart.
2. Where a look answers something, the gaze and the thing are on opposite sides of frame.
3. Screen direction holds through the scene, unless a shot toward or away from camera turns it.
4. No three shots in a row share both their size and their camera move.

**The run pass.** Give every shot its run and every run its ordered shots, planned cut times (running
sums of `sec` from zero), generation length, join sentence and ordered references. Planned cuts are
requests: the model cuts near them, not on them. If the cards stop fitting the approved plan, or an
edge falls on a rest, propose the fix; never move an approved edge in silence.

A run that changes a place or a person's state makes later runs wait for its accepted take: their
frames of the change replace the clean pictures they contradict.

## Key frames

Any video that buys footage, a film or a single generated shot in another kind of video, is first
seen as stills at its key points, as video-core says. Run `scripts/keyframes.py` on the plan's
beats: it names each key point (the hook, the turn, the payoff, and the opening of every generated
beat), says which of them the user's own footage already shows, and how the video reuses each
still. Run it again with the stills before the video is quoted; `ready` stays false until every
generated beat has an approved still.

- A film's scene pictures are its key frames (`references/scene-pictures.md`).
- Outside a film, make a key frame the way a scene picture is made: at the video's frame, from
  full-size references. A crop of a screen recording is a low-resolution frame, never a reference.
- **An approved key frame is used, not thrown away**: it opens its generation as picture 1 of
  `imageUrls`, or travels as a `FRAME REFERENCE` (`references/references.md`). A still nothing in
  the video will use is not a key frame.

## Compile and verify

Every prompt is compiled on the server and passed to `picsart_generate` **verbatim**. The camera,
lighting and acting language, the house lines and the templates are the compiler's; a paraphrase
renders worse. This holds for one shot made for another use case too, such as a screen video's
generated opening: it goes through these steps like a run.

1. **Compile** with `picsart_film_compile_prompt`: `kind` (`run` for a video, `still` or
   `scene-picture` for a picture, `map`, `edit`), the world's `look` ids (with `look.scheme` and
   `look.hue` when the setup has them), and what only you can write:
   - `scene`, `geography` (one line, identical in every prompt of the scene), and `space`:
     foreground, midground and background, all three named;
   - `cast`, each with a `tell` and the saved `voice`;
   - `images`: every reference numbered, each with its job;
   - `shots[]`: `sec`, `subject`, size, arrangement, angle, `fov`, `aperture`, `move`;
     `performances` for every person in frame (`action`, `emotion` with the intensity film-story's
     peak rule sets, `gaze` on a named target); the shot's own `speech`, beside `performances`
     rather than inside one (`name`, `line`, `delivery`); and the pair's cut rule in its `extra`;
   - anything more in `extra` or `filmConstraints`, in your own words.

   **Pin what the model would re-infer.** It guesses every unstated fact frame by frame, and the
   glitches come from those guesses. In `extra` and the performances:
   - a moving mechanism states its fixed geometry once (the hinge side and swing of a door, the
     grip and stroke of a tool) and every action names its instrument: water pours from the kettle,
     never "she pours" from a bag of beans;
   - list what may move (people, tools, the camera) and pin the rest still; every spark, smoke or
     sound has an owner on frame or a cause off it, or the model invents one, usually the nearest
     person;
   - one primary action per person per shot; a change of tool is its own written step.

   **Every shot passes its `fov` and `aperture`**, whether the card's value was seeded or changed:
   the setup carries no focal length, so a skipped lens leaves the model choosing one. An `auto`
   aperture writes nothing. A light writes a line only when the user changed it, and then every
   shot of its scene carries the scene's colour temperature and dark side in its `extra`, as
   film-story sets them; a palette other than `auto` always does.
2. **Verify** with `picsart_prompt_verify` on the **literal arguments** you are about to send: the
   prompt, the images, the model settings, the audio flag, and the `promptToken`. Its table checks
   what is string matching and arithmetic. It does not judge the writing: read every character's
   action, emotion and gaze, the entrances and exits, the props, the cut motivation and the joins
   yourself.
3. **A palette warning stops the dispatch.** When the compiler's `notes` say a shot's palette
   argues with the film's scheme, nothing is generated from that prompt. Flag the shot with its
   three options: keep the palette, drop it to `auto`, or swap it for one inside the scheme.
4. **A failure is fixed at the source**: the inputs corrected, compiled again, verified again. A
   finding on a user-owned value (a shot's seconds, a line, a lens, a light) goes back to the user,
   never quietly changed. A prompt changed after compiling is compiled again; an old token never
   covers new text.

Never paste a descriptor into a run prompt: the references carry identity, and the prompt names
them by number. Prompts describe what is there, not a list of negatives; a video takes no negative
prompt.

## Voice

- The film keeps the voice its takes are born with. Native audio is on for any run with a line, off
  for a run without one.
- Every speaking block carries the speaker's saved voice line verbatim, repairs and extends
  included. Emotion and loudness go in the delivery.
- Every line has a beat of silence after it inside its shot. A line running into the cut fails.
- A shared run and a voice line do not guarantee one timbre across takes. Listen for it in review.

## Dispatch and follow

- `picsart_generate` is asynchronous, and a batch of runs goes out as video-core says: one call
  per run, all sent before you follow any. Each call passes the model, the `folderUid` the shots
  are filed in, the shared `aspectRatio`, and its run's compiled prompt, `imageUrls`, `duration`,
  and model-specific settings in `extra` as `picsart_model_params` names them. **Every reference
  travels in `imageUrls`**, and no other image parameter is set: a frame travels as picture 1 of
  `imageUrls`.
- **Runs are shot as drafts**: the lowest `resolution`, or the draft switch, that
  `picsart_model_params` offers for the model, never its finish settings. A run keeps its `genSec`.
  The finish settings are bought once, in film-finishing's final-resolution pass, after the user
  calls the cut final. A model with no setting below its finish has no draft: say so in the
  forecast, and its takes are final.
- The batch is followed on one `picsart_render_monitor`, which reports back, as video-core says.
  Label each run's job with the run's shots.
- **A dropped or timed-out call is not a failed generation.** The job is usually still running and
  charging. Check it with `picsart_job_status` on its handle as video-core says, passing the
  `folderUid` again; never submit it again.
- A job still running at the end of a turn: say what is running and that you will pick it up. A
  batch that lands is split, judged and put up for review in that turn (`references/takes.md`).

## Traps

- A run sent at the finish settings before the user calls the cut final.
- Shooting shot by shot, or splitting runs for emphasis when the same shots fit fewer runs.
- Treating the model's ceiling as a reason to make one long shot.
- A prompt typed by hand, or a compiled one edited without compiling again.
- A verification pass read as approval of the footage.
- A panel pointer, a contact-sheet thumbnail or a low-resolution frame sent as a reference.
- A reference passed outside `imageUrls`; an identity or wardrobe view left out; references reordered without
  compiling again.
- The geography line dropped, so people swap sides between shots.
- Readable text asked of a video or a still. Signs and screens are added in the edit.
- Resubmitting after a dropped call instead of checking its job.
