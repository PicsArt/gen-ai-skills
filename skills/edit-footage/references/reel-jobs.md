# The jobs

The footage and the request decide the job. Infer it ("highlights from my game" is `highlight`,
photos alone are `slideshow`, a how-to filmed to camera is `lesson`), say it back in one line, and
keep it in the record's `job`. Ask only when two jobs fit equally. Anything the user says wins over
a job's default.

| Job | Footage | Moments picked by | Output | Music | Captions |
|---|---|---|---|---|---|
| `reel` | talking footage | the transcript, as the speech-aware-cutting skill says | one short that tells one story | offered once the picture is settled | highlights offered |
| `highlight` | an event, a game, a trip: action with little speech | the picture (the footage-analysis skill's watch) and the beat | one music-led cut of the best moments | first: the bed sets the cut | off |
| `montage` | many short clips and photos | the user's order, else the picture | one music-led join | first | off |
| `slideshow` | photos only | the user's order | one titled slideshow, built as the photo-slideshow skill says (on Vibe Cut, in the style the agent picks), every photo moving | a bed, each photo held to its beats | the title only |
| `lesson` | a routine done to camera, each product held to the lens | the transcript, one stretch per product, kept in order of application | one short of 60-180 s (or the length asked), cold-opened on the finished look | none | the hook line only |

## The interview, per job

Stage 2's questions (`references/reel-interview.md`) are asked or skipped per job. Skipped means
answered by the job's default, said back in the brief.

| Question | reel | highlight | montage | slideshow | lesson |
|---|---|---|---|---|---|
| 1. Destination | state | state | state | state | state |
| 2. Goal | ask | skip | skip | skip | skip: teach the routine |
| 3. Audience | ask | skip | skip | skip | skip: the creator's followers |
| 4. Message | ask | skip | skip | ask: the title, in words | ask: the hook line, in words |
| 5. Length | as interview.md | as interview.md | as interview.md | as interview.md | as interview.md, the range 60-180 s |
| 6. How many | ask | skip: one | skip: one | skip: one | skip: one |
| 7. Ending | ask | skip | skip | skip | ask: the finished look again, or the creator's sign-off |
| 8. Your numbers | ask, for a channel that posts shorts | skip | skip | skip | ask, for a channel that posts shorts |

On Story Cut, `highlight` and `montage` ask question 4 as `slideshow` does: the title, in words;
its key moments also get a short line each (`references/reel-flow.md`, Which cut).
`montage` also asks whether to keep the user's order, when they gave one. For `highlight`,
`montage` and `slideshow` the bed is chosen before the cut, since its beats set the cuts. After
stage 3 and before stage 4, it is one of:

- background-music's: load it, ASK (with `picsart_ask`, found as picsart-video-rules says, for any closed choice, a multi-select included, so the options are buttons the user taps, the recommended one first; then your host's own question tool, such as AskUserQuestion; only where all fail, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) its brief (in a style, from the
  style's Music line: its mood and tempo), and SPEND (quote it in one line, then get the yes with `picsart_ask`, found as picsart-video-rules says, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", else your host's own question tool, such as AskUserQuestion; never as a typed question unless both fail; only then those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) on its
  generation (a little longer than the brief's length), then measure its beat grid;
- the user's own track, received with `picsart_drive_upload_ask` (`accept: 'audio'`), its beat grid measured with
  `picsart_media_analyze_audio`.

The beats then
drive stages 4 and 7. The mix waits for the scene: the bed is laid under the approved scene, and
its REVIEW comes, at stage 11 as usual. On resume, the record's chosen bed shows the choice is
done.

## Per job, beyond the interview

- **`highlight`, `montage`**: no speech to cut on, so the cut follows the picture and the bed's
  beats: a clip changes on a beat measured with `picsart_media_analyze_audio`. Measure that grid
  before cutting. Say in one line that the cut follows the beat.
- **`slideshow`**: every photo moves (a slow push or a drift; never a still held), each held to a
  whole number of beats, as the photo-slideshow skill sequences them, the beats measured as for
  `highlight`. A static slideshow is a miss.
- **`highlight`, `montage`, `slideshow` on Vibe Cut**: built in the one best-fitting style
  from the reel-structure skill's style library, picked by the agent with no question, as
  `references/reel-flow.md` says (No reference: a style). On Clean Cut and Story Cut, as above.
- **`lesson`**: the short opens cold on the finished look, 1-2 s with the hook line as text, then
  the routine in order of application, one stretch per product while it is held to the lens and
  talked through. Never reorder the steps or cut one out; a long silent stretch of blending may be
  sped up. No step cards and no product names on screen unless the user asks. Keep each product's
  stretch in the record's `steps`, and give the QC inspector each as a locked row: the product as
  `phrase`, the close-up it shows as `job` (the locked row's field, not the record's `job`), its
  range as `shot`. Deliver the product list, in order
  of use, as text for the post's caption, then offer a 30-60 s Reel cut-down. A lesson filmed on
  screen is a screen recording, not this job.
