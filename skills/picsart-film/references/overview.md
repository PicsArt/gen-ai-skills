# Film — the production pipeline, orchestrated

A film is not a long video. The model has no memory between generations: describe a
character loosely and he arrives in every shot with a different face, jacket, and age.
The whole pipeline exists to beat that one problem — **consistency** — and it runs on
one economic law: **stills are cheap, video is expensive.** Every decision that can be
made on text or images is made there, before a single charged video call.

Plan free → one approved sheet per asset → native draft when supported, otherwise a price-saving resolution draft (see `../../picsart-film-scenes/references/step-2-shot-design.md`, *Native draft to final*) →
pay full price exactly once, at the final pass. The same law,
stretched across a production.

## 0. Triage — route before anything else

| User brings | Route |
|---|---|
| One clip's worth of idea ("a video of a boot on scree") | **not this pipeline** — one `picsart_generate` video call, quoted and approved first; the eleven stages exist for recurring identity, and a single clip needs none of them |
| Footage to stitch | **not this pipeline** — the scene tools direct: probe → author → validate → `picsart_scene_editor` on the built scene → `picsart_media_export`, written out in `../../picsart-film-edit/references/assembly.md` |
| A story: scenes, characters that recur, dialogue | **this skill** |
| An existing film project (a `film.json` or a workspace dir) | resume — read it, say where the film stands, continue at `phase` |

A 30-second ad with one recurring product is a single generate call with a
reference image. A 90-second story with two brothers who must look like themselves
in every scene is a film. The dividing line is *recurring identity across scenes*.

## Pace — director by default

Default to **director pace**: keep the user involved at each stage gate, show
the key craft decisions before progressing, and preserve the full production
ceremony. Mention once at project start that **express pace** is available if
they want you to make the routine craft decisions and bring them in only for
taste verdicts on boards, the three locks that shape everything (the story
and the video plan, the look, the assets), every charged video dispatch, and any spend beyond
the quoted plan. Switch to express only when the user asks.

Pace changes approval cadence, never safeguards: express pace still uses every
required board, respects all three locks, and asks before any
spend that requires confirmation — including **every charged video dispatch,
quoted with `picsart_preflight` and dispatched only on the user's yes**,
whatever the pace.

## How you talk to the user

Conversation rules:

- **Read submitted widget feedback before acting.** Follow the host conventions above and `widget-feedback.md`; never treat the board's initial result as user approval.

- **Say only what the user needs in order to decide.** The pipeline is your
  bookkeeping, not theirs. It lives in `film.json`; a chat turn is for the
  decision in front of them. Four things that keep leaking into prose and should
  not:
  - **retrospective accounting** — "Stage 2 spent nothing, which is the
    short-film default". They did not ask what the last stage cost. Quote what
    the *next* thing costs, when it costs something.
  - **how the machine works** — "the tone moodboard isn't a separate purchase,
    it's the booth's first plate at Stage 4 doing two jobs". True, internal,
    and nothing they can act on.
  - **editorial subtitles on a stage** — "the last free stage before anything
    renders". A stage name is a locator, not a headline needing a subhead.
  - **standing offers nobody asked for** — "if you have reference images, drop
    them in at any point". Say it when it is relevant to the choice being made,
    once, not as a footer.

  A turn that is two sentences and one question is doing its job. If a paragraph
  is explaining the pipeline to justify what you are about to do, delete the
  paragraph and do it.

- **One decision per turn.** End a turn with at most one question the user must
  answer *now*; park everything non-blocking in `film.json`'s
  `openDecisions` and raise each only when it actually blocks. "Three things I
  need from you" is how users get stuck — they answer one, and the rest dangle
  into re-asks.
- **One confirmation covers a set.** Things presented together get one
  "anything to change?" — never per-item sign-offs (five scene shotlists is one
  approval, not five). Boards exist for targeted edits, not sequential
  ceremony.
- **Free work never asks permission.** Opening a board, drafting descriptors,
  drafting the run's prompt, updating `film.json` — do it; never end a turn
  with "want me to open them as review boards?". Permission questions are for
  money: every charged video dispatch — its own preflight number in front of
  the user, then their yes (`picsart-film-scenes`) — and any spend beyond the quoted
  plan. The optional next-video recap below is a navigation choice, not a
  permission request or another approval gate.
- **Offer a memory refresh after a long video iteration.** When moving to the
  next video after substantial time spent generating, reviewing or editing the
  previous one, or resuming that handoff in a later session, briefly offer once:
  "I can open the shotlist to refresh what comes next and check how it connects
  to the approved edit, or we can go straight to shooting." Use the actual video
  numbers when known. Do not automatically open the board or turn this into a
  mandatory sign-off. If the user already chose straight to shooting, honor it
  without repeating the offer; a routine uninterrupted handoff needs no recap.
  If they choose the recap, reopen the existing shotlist board with the next
  video's shots and explain the join from the **latest approved edited ending**
  of the previous video, not an obsolete script endpoint or untrimmed source.
  Preserve approved dialogue and shot decisions unless the user requests a
  change. If they skip the recap, continue preparation without reopening it;
  continuity checks, reference checks and charged-dispatch approval still apply.
  Record the offer and their choice in the project checkpoint so a new session
  does not ask again for the same handoff.
- **Progress is never damage — and say it without the shop talk.** Mid-stage
  state is "not yet", never failure language: an empty coverage table during
  Stage 4 is normal, not an alarm. But reassurance in jargon reassures nobody.
  *"Scene × assets — every cell is a hole right now, and that's Tuesday
  afternoon, not an alarm. Holes only bite at generation time"* is four internal
  metaphors in two sentences, and a user who cannot parse it cannot be calmed by
  it. Say the plain version: **"nothing here is ready yet — that's expected at
  this stage, and it only matters once we start shooting."** Call the table what
  it shows — which scenes have everything they need — not "the matrix", and an
  empty cell "not ready yet", not "a hole". Alarm words are reserved for a real
  gate violation (charged video attempted through a missing asset). A user told
  "zero locked assets" in a grave voice hears "you wasted an hour", and nothing
  was wasted.

## Ten rules that never bend

1. **Generate nothing for the film until its scene's assets are locked.** The
   scene×assets matrix — read off `film.json` — is the gate, and a hole is a
   stop.
2. **One asset — one approved sheet; one reference image — one view.** Each
   character, location, and prop has a single approved sheet (descriptor + one
   image). The descriptor is the sheet's prompt and the asset's record; it
   is **never pasted into a video prompt** — the pictures carry
   identity and the prompt names them by number
   (`../../picsart-film-scenes/references/prompt-blocks.md`, the one home of the prompt's
   shape). A state
   change (wet, bloodied, new costume) is a **panel on that sheet with its own
   tag** (`@cal_wet`; a panel, not a second sheet) — a tag,
   never a note in the shot prompt. What reaches the model is not the sheet:
   each panel the film uses is **cut out as its own image**,
   and a run's `imageUrls` carries those views, one thing per image. A
   multi-panel picture with the right panel named in words makes the model
   guess, and it puts the wrong face in the shot.
3. **Edits are surgical.** One preset, one line, one block at a time. A rewritten
   prompt loses whatever was working.
4. **Show promptly; inspect before use.** A finished image may be shown
   immediately while its visual check is performed with `picsart_view_image`.
   Explain any defect under it. Approval, reference use, cropping and dependent
   generations wait for the check to pass. Pass the returned URL to
   `picsart_view_image` exactly as given and inspect the returned pixels, not
   the URL. If the image is too large for it, export a small JPEG with
   `picsart_media_export` and inspect that. Previews are for viewing only:
   reference inputs, crops and start frames keep the full-resolution original.
   Video checks use extracted frames. A tool error means the check has not
   happened; use the documented fallback or explain the block.
5. **Everything is logged, lightly.** One prompt per video, the take's link and
   the verdict. Without that a good shot cannot be reproduced.
6. **A dropped call is never a failed generation.** "Server isn't responding" is
   a *response* failure: the render usually completed, charged, and (with
   `saveToDrive`) landed in Drive — a blind retry pays twice for an image
   already owned, and writes finished assets off as "blocked". So every charged
   `picsart_generate` in this pipeline — sheets, stills, video — passes
   `async: true` (a handle always exists to poll),
   and recovery from any drop is **check first, never resubmit**:
   `picsart_job_status` on the handle, or list recent Drive files for a sync
   call that slipped through.
7. **Nobody is in a video without their picture.** Every video
   call — a 30-second run, a five-second bridge, an insert, a one-shot reshoot,
   whatever the clip is called — carries in `imageUrls` the identity view and
   the wardrobe view of every person who appears in it (the two pictures the
   lock step cuts from the sheet, `picsart-film-assets`), and the scene's
   pictures. A person carried by words alone is drawn from the model's habits
   (a wasteland in words puts a long coat on her), so words-only is a failed
   take before it is sent. It follows that the `startFrame` field is never
   filled, on any clip: an exact frame shuts every reference out, and a frame
   shows only the people in it. The frame a video
   must open on is picture 1 in `imageUrls`, labelled `START FRAME` in the
   tagging header, beside the others. A bridge sent with a last frame in the
   `startFrame` field and no picture of a person who is in the shot but not in
   that frame brings that person back in different clothes, and puts a
   wardrobe jump on both of its joins. One habit rides with this rule: every
   object is named in one place with one position — a flask *on her strap*
   and *in her hand* in the same prompt is two flasks. Three cases the rule
   settles: **a person the user photographed** — the photograph
   is the identity view and, when it shows the outfit the story dresses them
   in, the wardrobe view too; when it does not, ask for one more photograph
   that does, and never generate a lookalike to fill the slot. **A state** —
   when a dependent run takes frames from an earlier run because a person
   changed (dusty, torn, wet), the frame that shows it becomes that person's
   state view and **replaces** their wardrobe view in the dependent run; a
   clean coat beside a torn one makes the model average them. **A prop** —
   every object the film gave a plate to rides beside the people as `IMAGE n —
   PROP: <name>` and is named by that number where it appears; an object
   described only in words comes back as whatever the model expects.

8. **Default review carries the whole film.** Every `picsart_scene_editor` call opens on a `scene` that
   plays every accepted take plus the new one, in playback order — the montage
   built by `../../picsart-film-edit/references/assembly.md`. A film with two videos and a
   third just delivered opens as a scene of **three**, the new one in its story
   position — never a scene holding only what was just generated. `videoUrl` is
   for a film that genuinely has one video. **Why:** the
   only question worth asking about a new take is whether it *joins* — the seam
   into it and the seam out of it are the thing that fails, and a clip played on
   its own hides exactly that. A take that looks right alone and jumps in the
   film is the normal case, not the rare one, and it gets approved when
   nobody sees the join. Watching
   the whole film costs nothing: the scene is windows over the source clips, and
   the editor plays it in the browser — it never renders and it never exports. **Focused join diagnosis/comparison is
   the exception** (`../../picsart-film-edit/references/join-repair.md`): review both sides
   of the boundary, including a proposed insert, as a labelled preview separate
   from the accepted cut. Never approve a bridge from watching it alone.
9. **The join between two videos is an angle change; a copied frame is the
   exception and must be named.** This is the default for planning
   new runs, not an automatic repair for existing clips. User-requested join
   repairs follow `../../picsart-film-edit/references/join-repair.md`, including motivated
   inserts and reference choices based on inspected boundary states. Two videos meet the handbook's
   way — the camera changes, the action carries, no pixels copied — which is what
   lets every video of the film dispatch in parallel. Taking video A's last frame
   into video B is permitted **only** when a physical state exists in A's pixels
   and in none of the approved pictures (a torn coat, a wrecked room, dust on a
   face); before dispatch, that state is named out loud in one sentence, and if
   the sentence names nothing, there is no exception and the angle change carries
   the join. The `startFrame` *field* stays empty either way (rule 7) — a frame
   travels as picture 1 of `imageUrls`, labelled `START FRAME`. **Why:** a copied
   frame makes B wait for A, and it carries only the composition and the people
   visible in it — everyone else regenerates from words and comes back changed
   (rule 7). The angle change hides the seam without paying that.

10. **No place is in a video without its picture, and the picture has to cover
    what the frame will show.** Rule 7 protects the people; this is
    the same law for the place. Every
    video and every edit set in a place carries that place's **map** — the
    geometry — and carries the **wide** as well whenever the framing opens up
    beyond a tight frame. The budget ladder may drop the wide only when the map
    is present *and* no cut pulls back; **the map is never dropped**, exactly as
    the identity and wardrobe views are never dropped. An edit inherits the
    run's reference list verbatim, so a hole in the run becomes a hole in the
    edit — and an edit that reveals more of the setting than the clip showed
    must **add** the map and the wide, because the run's list only anchors what
    was already visible. **Why:** a tight frame constrains a doorway and nothing
    else; ask for a pull-back and the skyline, the street and the far wall are
    drawn from the model's habits, so the place changes while every face stays
    right. A clip sent with only a tight frame of its setting, then edited
    to pull back, reveals a skyline from somewhere else.

## Traps

- Starting generation "just for one scene" before its assets pass the gate. That is
  the trap the whole pipeline exists to prevent.
- Dispatching video on the forecast. A forecast is a plan; the purchase needs a
  preflight number in front of the user and a yes after it — per dispatch, at
  any pace (`picsart-film-scenes`).
- Shortening a descriptor "for brevity" inside a prompt. Consistency dies right there.
- Building a state variant as its own asset with its own approval.
  `@cal_wet` is a panel on @cal's sheet, and a
  view cut from it and numbered in the references header like any other image — a separate
  *sheet* only when the change lasts most of the film.
- Handing the video model a multi-panel sheet, or a composite the user
  supplied, with the wanted panel named in words. Cut it into views at lock.
  No pointer works: the same correct prompt can return two different people,
  or one frame blending two panels into a face not in the cast. A prompt that names a panel is a dispatch error (`picsart-film-assets`).
- Letting the registry go stale — two weeks later it lies, and consistency rests on
  one person's memory.
- Losing the project to an expired CDN link because nothing was saved to Drive
  — or, for a locked asset, recording the export's URL instead of the one
  `picsart_save_asset` handed back: the save re-hosts, the export URL expires
  (`picsart-film-assets`, step 4).
- Altering a user's own photo on the way in, or asking them to approve it on a
  board. The original is saved byte-for-byte (probe-matched)
  and is IMAGE 1 in every run; changed copies are derived files with the
  reason recorded, and a sheet is generated *from* the photo only when a card
  needs an angle it lacks (`picsart-film-assets`).
