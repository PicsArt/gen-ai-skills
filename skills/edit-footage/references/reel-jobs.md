# The jobs

The footage and the request decide the job. Infer it ("highlights from my game" is `highlight`,
photos alone are `slideshow`, a how-to filmed to camera is `lesson`), say it back in one line, and
keep it in the record's `job`. Ask only when two jobs fit equally. Anything the user says wins over
a job's default.

| Job | Footage | Moments picked by | Output | Music | Captions |
|---|---|---|---|---|---|
| `reel` | talking footage | the transcript, as the speech-aware-cutting skill says | one short that tells one story | offered once the picture is settled | highlights offered |
| `podcast-clips` | a long podcast or interview, one to three speakers | the transcript, each moment ranked to stand on its own | several shorts (three unless the user names a number), no moment used twice, the speaker kept in frame | none | word-timed, on |
| `split` | a podcast or interview with two people on screen, and a split-screen reference (often the channel's own) | as `podcast-clips` | as `podcast-clips`, each short two stacked halves with full-frame moments, as the format sets: the footage-reframing skill's split layout | none | word cards on the seam, and the hook card, as the format sets |
| `highlight` | an event, a game, a trip: action with little speech | the picture (the footage-analysis skill's watch) and the beat | one music-led cut of the best moments | first: the bed sets the cut | off |
| `montage` | many short clips and photos | the user's order, else the picture | one music-led join | first | off |
| `slideshow` | photos only | the user's order | one titled slideshow, built as the photo-slideshow skill says (on Vibe Cut, in the style the agent picks), every photo moving | a bed, each photo held to its beats | the title only |
| `lesson` | a routine done to camera, each product held to the lens | the transcript, one stretch per product, kept in order of application | one short of 60-180 s (or the length asked), cold-opened on the finished look | none | the hook line only |
| `channel-clips` | one long video, as a file or a link from elsewhere, with a short whose look the clips take (the user's own channel's, else any reel) | the transcript, each moment ranked to stand on its own, as `podcast-clips`; a campaign brief's rules first | several clips (three unless the user or a brief names a number), each in the look: the layout, the hook card, the captions and the end card the short has, with a cover and post copy, in one Drive folder; `references/clips-flow.md` | none | as the look sets |

## The interview, per job

Stage 2's questions (`references/reel-interview.md`) are asked or skipped per job. Skipped means
answered by the job's default, said back in the brief.

| Question | reel | podcast-clips, split | highlight | montage | slideshow | lesson | channel-clips |
|---|---|---|---|---|---|---|---|
| 1. Destination | state | state | state | state | state | state | state: the look's platform, or the brief's (`references/clip-briefs.md`) |
| 2. Goal | ask | ask | skip | skip | skip | skip: teach the routine | skip: grow the audience |
| 3. Audience | ask | ask | skip | skip | skip | skip: the creator's followers | skip: the channel's followers |
| 4. Message | ask | skip: each clip's own | skip | skip | ask: the title, in words | ask: the hook line, in words | skip: each clip's own |
| 5. Length | as interview.md | as interview.md, per clip | as interview.md | as interview.md | as interview.md | as interview.md, the range 60-180 s | skip: 30-60 s, the look's or the brief's when they say |
| 6. How many | ask | ask the number (three recommended) | skip: one | skip: one | skip: one | skip: one | in the plan message, with the go: three unless given |
| 7. Ending | ask | skip: each clip ends on a closed thought | skip | skip | skip | ask: the finished look again, or the creator's sign-off | skip: each clip ends on a closed thought |

On Story Cut, `highlight` and `montage` ask question 4 as `slideshow` does: the title, in words;
its key moments also get a short line each (`references/reel-flow.md`, Which cut).
`montage` also asks whether to keep the user's order, when they gave one. For `highlight`,
`montage` and `slideshow` the bed is chosen before the cut, since its beats set the cuts. After
stage 3 and before stage 4, it is one of:

- background-music's: load it, ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) its brief (in a style, from the
  style's Music line: its mood and tempo), and SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) on its
  generation (a little longer than the brief's length), then measure its beat grid;
- the user's own track, received with `picsart_drive_upload_ask`, its beat grid measured with
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
- **`channel-clips`**: the look is the job, so the reference is read before anything is picked,
  and the interview is not held: its answers are the look's and the defaults above, said in the
  plan message. Express pace throughout. Its steps are `references/clips-flow.md`: two questions
  at most, one plan message, every clip built in the look, the first clip checked and reviewed,
  then all of them delivered with covers and post copy, and the offer to post them.
