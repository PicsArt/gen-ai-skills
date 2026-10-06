# Film — model policy

## Model policy

The pipeline is model-agnostic; the current fit is checked, not remembered.
**The video model is chosen in Stage 1, right after the story and before the
video plan is written**: the shot
list needs its duration ladder, the run pass needs its ceiling, the reference
budget is its `imageUrls` max, and the edit sibling is its repair path — nothing
downstream of the console can be planned model-blind. Read
`picsart_model_catalog` (`mode: "video"`, **`purpose: "generate"`**) and
`picsart_model_params` live. Pass `purpose` every
time: `mode` and `inputType` say which media go in and out, never what a model is
FOR, so without it the shortlist arrives salted with upscalers, reframes,
video-extend and preset-effect models. `edit` is for changing a clip you already
have; `utility` is upscale/reframe/lip-sync/preset — ask for it by name when that
is genuinely the question. What a film needs from its one video model: **native
multi-shot** — a declared cut count and cut times honoured inside one generation,
at the finish resolution, for the run lengths the shot list needs (the
unit of generation is the run — as much of the film as fits the
ceiling, scenes included; `picsart-film-scenes` has the finding and the rules) — plus
**reference images in** (`imageUrls`, enough slots for every view, plate and
approved still the run uses — views, never sheets — each named by index and role in the prompt —
the start frame travels as one of them, labelled `START FRAME`, since the
`startFrame` field would lock the references out), native audio with
lip-sync for dialogue, and **edit and extend siblings** (`purpose: "edit"`, v2v
— the edit one takes the clip + a change + the same references, the extend one
takes the clip + what happens next) so a fix or a longer shot never re-rolls the
run (`picsart-film-scenes` step 5). The multi-shot line is a hard filter, not a preference: a model that
caps resolution on long takes, or will not hold a cut list, is a model that
shoots the film shot by shot, which is the weaker path. Check the
ceiling, the `imageUrls` max and the resolution enum in `picsart_model_params`
before the board opens. Put the shortlist through `picsart_model_choice` and let the user pick —
the same habit throughout. One model for the whole film unless a
world-switch demands otherwise.

**The choice board is the only model UI this pipeline opens, and it is short.**
Never `picsart_list_models`: that widget is the catalogue shelf — every match,
unranked — and opening a card there puts the user in front of a full parameter
form with its own generate button, a second production flow running beside this
one and spending credits outside the plan. What the board carries instead is a
decision already made: **your recommendation plus the one or two alternatives
whose trade-off a director could genuinely prefer** (three cards is the target,
four the ceiling), exactly one badged `recommended`, each `bestFor` written as
the trade — "one continuous 30s take, but tops out at 720p" — not as a spec
sheet. Narrowing eight candidates to three is your job, not theirs; a long board
is the catalogue handed back with extra steps.

The same rule binds **image** models for asset work: the film's target format
is a hard constraint. Filter the catalog by `supportedAspectRatios` containing
the film's aspect ratio *before* comparing anything else — never settle for a
model whose ratio enum lacks the finish format and let it "cap" the stills at
the nearest ratio it has.

**Image models are families, not ids.** The docs name the family
the handbook uses for each job; the id is read off `picsart_model_catalog`
once, at Stage 4's first call, and recorded in `film.json.model.pictures` so
one film never changes model midway while the next film picks up a newer
version the day it lands (`pipeline.md`, Stage 4, *Image models
are families*):

- **`people`** — the 4K wide's model, selected from the live catalog and
  schema; Nano Banana is the first choice. Seedream Pro is an
  alternate after identity failures, with any smaller crop disclosed;
- **`map`** — the room map, and a prop's plate: the GPT Image family
  (`gpt-image-*`; where a version ships in tiers, the fast one);
- **`vintage`** — the era tones' portrait and sheet: the GPT Image family (the
  premium tier where there is one — a face is cut from it);
- **`modern`** — the modern path and every profile: Nano Banana (Google's
  `gemini-*-flash-image`, never the `-lite`);
- a point fix on a sheet goes to an image **edit** model (`purpose: "edit"`,
  the newest that takes a mask); signs, letters and labels go to the model that
  can spell, as a separate task, never generated inside a shot.

A model id written anywhere in these docs is an example, not the
rule. One video model for the whole film still stands, chosen by the user on
`picsart_model_choice` and recorded with its edit and extend siblings.
