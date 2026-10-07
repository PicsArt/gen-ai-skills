# Camera & optics presets — movement, size, FOV, aperture, angle, view, arrangement, placement, composition

> **The wordings live on the server.** This file decides *which* preset to
> reach for — that judgement is the part that needs a reader. The sentence each
> id compiles to is not here: those sentences are tuned against real renders,
> and a prompt written from a remembered copy of one renders worse than a prompt
> that pastes it. Pass the id to `picsart_film_compile_prompt` and the server
> pastes the sentence.

The vocabulary behind the shot-level camera decisions and their text-choice
fallback. Movement, size and angle open every shot block (`prompt-blocks.md`,
Part 2 — *shot type, camera angle, camera movement*); FOV and aperture belong
to each shot and reach its prompt on **every** shot, whether the user changed
them or left them as seeded (*The card's own picks*); arrangement, character
view, placement and composition compile into the scene picture's prompt and the
geography line. Fragments are pasted verbatim; `<subject>`, `<second>`,
`<third>` are replaced with asset tags' names. The tables carry the Zero Shoots
handbook's *Camera Work* vocabulary name for name — its phrases are the
fragments wherever it has one.

Movement, size, lens, aperture, angle and arrangement are picked on the shot
cards of `picsart_shotlist_board`. Character view, placement, composition,
atmosphere and camera artefacts have no control there: you author them by hand
from this file, out of the scene's staging.

## Movement presets — one per shot

**50 moves in six groups, and they are one library.** The same ids, labels and
notes serve the shot list's `Camera move` control, the review board's direction
panel, and the compiler's per-shot `move`. A move means the same thing wherever
the film is discussed, which is the whole reason a note reading
`Camera move → Slow push-in` can be folded into a prompt without asking what the user
meant by it — and why picking one without boards lands on the same fragment the
board would have compiled.

Grouped by energy. Every fragment also states what the camera does NOT do —
models drift without the negative space written positively. Three laws across
the whole table:

- **Every move ends somewhere named.** The fragment's last clause is the END
  STATE — the final frame the move arrives at ("ending composed on…",
  "settling at…"). Models overshoot moves with no destination, and the end
  state is what the next shot's seam inherits. The exception is a move that is
  *defined* by not arriving — a sustained track, a chase, an infinite zoom —
  where the last clause names the constant instead ("constant distance",
  "never leaving frame").
- **Speed is a variant, not a new move.** "Faster" or "slower" modifies the
  chosen preset's fragment in place (one word), never switches presets. Where
  the table does name a speed (slow / fast / crash zoom) those are three
  genuinely different shapes — a settle, an arrival, an overshoot — not three
  dials on one move.
- **Direction is a placeholder, not a preset.** `<left/right>` and `<up/down>`
  are filled at prompt time; a pan left and a pan right are one move pointed
  two ways. Surfaces that cannot ask (the shot list, the world default) drop
  the word rather than guess it.

### At rest (register: SETTLE)

**Ids:** `locked off` · `handheld settle` · `slow push-in` · `slow pull-back` · `slow zoom in` · `slow zoom out` · `slow pan` · `slow tilt` · `pedestal` · `slider`

*(The sentence each id compiles to lives server-side. Pass the id to `picsart_film_compile_prompt` and it pastes the tuned wording; never write that sentence yourself.)*

**`orbit` is the one circling move.** A quarter-circle around a static subject
is an orbit, and a model cannot be asked for a shallower arc: generated as a
deliberately shallow 30° swing, it comes back as plain lateral travel,
indistinguishable from a slider and nothing like a curve around anybody. Write
any circle as `orbit`, ending on a named aspect.

**Slider against pan.** Both move the frame sideways and a model will collapse
them if the fragment lets it: a pan pivots from one spot and has no parallax,
while a slider is a short move that re-frames the same subject.

**Lateral travel is `tracking lateral`, whether or not the subject moves.**
Travel past a *static* subject and travel *alongside a moving one* compile to the
same camera; the difference lives entirely in whether the subject happens to be
walking, which the shot already says.

### In motion (register: kinetic)

**Ids:** `tracking lateral` · `low tracking` · `follow behind` · `front tracking` · `handheld run` · `handheld shaky` · `chase` · `orbit` · `roll` · `dolly counter` · `crane up` · `crane down` · `push through` · `vehicle track` · `pass-by reveal`

*(The sentence each id compiles to lives server-side. Pass the id to `picsart_film_compile_prompt` and it pastes the tuned wording; never write that sentence yourself.)*

**The three tracking moves are named by WHERE THE CAMERA IS**, because that is
the only thing that separates them: `tracking lateral` rides beside the subject,
`front tracking` runs ahead of them facing back, and `follow behind` sits behind
their shoulder. All three match the subject's pace and hold them in the same
place in frame; a viewer tells them apart by which side of the person they are
looking at.

**Chase against handheld run.** `handheld run` is a body carrying the camera —
the operator's effort is the texture. `chase` is about the route and the gap:
it can be a car, a drone or a gimbal, and what it promises is that the subject
stays in frame while the distance keeps changing.

### Punctuation (use sparingly — one per scene at most)

**Ids:** `punch-in` · `whip pan` · `fast zoom in` · `fast zoom out` · `crash zoom` · `crash zoom out` · `snap tilt` · `drop reveal` · `through glass`

*(The sentence each id compiles to lives server-side. Pass the id to `picsart_film_compile_prompt` and it pastes the tuned wording; never write that sentence yourself.)*

**The three zoom speeds are three shapes.** `slow zoom` settles, `fast zoom`
arrives and holds, `crash zoom` overshoots and recovers. That is why the speed
law does not apply to them: writing "faster" onto a slow zoom gets you a fast
zoom's timing with a settle's ending, which is neither.

### Point of view

**Ids:** `POV walk` · `POV vehicle` · `mirror/insert POV` · `snorricam`

*(The sentence each id compiles to lives server-side. Pass the id to `picsart_film_compile_prompt` and it pastes the tuned wording; never write that sentence yourself.)*

### Aerial / remote

**Ids:** `drone establish` · `drone track` · `drone push-in` · `drone pull-back` · `helicopter pull` · `robot arm`

*(The sentence each id compiles to lives server-side. Pass the id to `picsart_film_compile_prompt` and it pastes the tuned wording; never write that sentence yourself.)*

**Drone pull-back against helicopter pull.** The drone move holds its altitude
and its speed; the helicopter move accelerates and is about scale arriving. Ask
which one the shot is doing before picking, because they read differently at the
same distance.

### Specials — the ones that are not really a camera path

| Preset | Register |
| --- | --- |
| rack focus | SETTLE |
| infinite zoom | kinetic |
| earth zoom out | kinetic |
| time-lapse | SETTLE |
| tilt-shift glide | kinetic |
| pass through | kinetic |

*(The sentence each id compiles to lives server-side. Pass the id to `picsart_film_compile_prompt` and it pastes the tuned wording; never write that sentence yourself.)*

Two of these carry their own **register** because the group's does not fit them:
`rack focus` and `time-lapse` are shot on a camera that does not move, and a
Camera block reading `Register: kinetic` over a locked-off frame is a
contradiction the model has to resolve on its own. Every other preset takes its
group's register.

`pass through` is the general case of `through glass`: glass is the one that
works most reliably, so it keeps its own preset and stays in punctuation, and
`pass through` is what you reach for when the barrier is a wall or a hedge.

### Coverage — the aicameramovements.com set

The public list at `aicameramovements.com` is 46 moves in seven categories, and
every one of them lands on a preset above, under the name a crew actually uses.
Directional pairs are one preset with a `<left/right>` placeholder, which is why
46 site entries map onto fewer rows than 46.

| Site category | Site name | Preset here |
|---|---|---|
| Pan/Tilt | Static shot | `locked off` |
| Pan/Tilt | Pan right · Pan left | `slow pan <left/right>` |
| Pan/Tilt | Whip pan right · Whip pan left | `whip pan <left/right>` |
| Pan/Tilt | Tilt up · Tilt down | `slow tilt <up/down>` |
| Zoom/Lens | Slow zoom in | `slow zoom in` |
| Zoom/Lens | Slow zoom out | `slow zoom out` |
| Zoom/Lens | Fast zoom in | `fast zoom in` |
| Zoom/Lens | Fast zoom out | `fast zoom out` |
| Zoom/Lens | Crash zoom in | `crash zoom` |
| Zoom/Lens | Crash zoom out | `crash zoom out` |
| Dolly/Track | Dolly in | `slow push-in` |
| Dolly/Track | Dolly out | `slow pull-back` |
| Dolly/Track | Tracking shot | `front tracking` |
| Dolly/Track | Side tracking | `tracking lateral` |
| Dolly/Track | Follow shot / over-the-shoulder | `follow behind` |
| Dolly/Track | Reverse tracking / walk-and-talk | `front tracking` |
| Dolly/Track | Low tracking | `low tracking` |
| Dolly/Track | Vehicle tracking | `vehicle track` |
| Dolly/Track | Chase shot | `chase` |
| Physical | Truck right · Truck left | `tracking lateral` |
| Physical | Pedestal up · Pedestal down | `pedestal` |
| Physical | Slider right · Slider left | `slider <left/right>` |
| Physical | Push past / pass-by shot | `pass-by reveal` |
| Physical | Arc right · Arc left | `orbit` |
| Physical | Orbit clockwise · counterclockwise | `orbit` |
| Human | Handheld shot | `handheld settle` (running: `handheld run`) |
| Human | Body-mounted camera / Snorricam | `snorricam` |
| Drone/Crane | Crane up | `crane up` |
| Drone/Crane | Crane down | `crane down` |
| Drone/Crane | Drone push in | `drone push-in` |
| Drone/Crane | Drone pull back | `drone pull-back` |
| Drone/Crane | Helicopter shot | `drone establish` (accelerating: `helicopter pull`) |
| Specials | First-person view | `POV walk` |
| Specials | Tilt-shift | `tilt-shift glide` |
| Specials | Infinite zoom | `infinite zoom` |
| Specials | Earth zoom out | `earth zoom out` |
| Specials | Time-lapse | `time-lapse` |
| Specials | Pass-through objects | `pass through` (glass: `through glass`) |

**The site's wording is not what compiles.** Its descriptions have no end state
and no negative space — "pan right. Movement: rotate the camera horizontally
from left to right from one fixed point" — which is exactly what the two laws
above exist to prevent. What the site gives is the *set*: which moves a
director expects to find. The words are this file's.

Five presets here are on no public list: `dolly counter`,
`mirror/insert POV`, `robot arm`, `drop reveal` and `rack focus`.

Always write the canonical ids listed above into a payload.

### Handbook terms (Zero Shoots, *Camera Work*)

The handbook names ten camera movements. Each lands on a preset here, none
approximated:

| Handbook term | Resolves to |
|---|---|
| Circles to the Right / Left | `orbit`, direction in the placeholder |
| Circles Up / Down | `crane up` · `crane down` |
| Camera Rolls Clockwise / Counterclockwise | `roll` |
| Camera Tilts Down / Up | `slow tilt` |
| Camera Pans Right / Left | `slow pan` |
| Camera Pushes In | `slow push-in` |
| Camera Pulls Back | `slow pull-back` |
| Handheld Shaky Camera | `handheld shaky` |
| Static Shot | `locked off` |
| Camera tracks the subject | `tracking lateral` — `follow behind` or `front tracking` when the direction is known |

## Getting a model to actually do the move

These rules apply whenever you are writing the Camera block, not only when
making previews.

### Name the ARRIVAL, never the quantity

`orbit` written as "through roughly 90°" delivers a fraction of the turn.
Written to end on *"their front, their aspect visibly turned"* it delivers the
whole quarter turn.

A number is an abstraction a model cannot render. A picture is not. "90 degrees"
means nothing; "her face square to the lens" is a frame it can make. So the last
clause of a Camera block is a **destination described as an image** — and this
file's first law, that every move ends somewhere named, is not a style
preference. It is the difference between getting the move and getting a fifth of
it.

### Two kinds of move, two kinds of prompt

| The move's identity is | Write it as | Examples |
|---|---|---|
| an **arrival** — you got there or you did not | our fragment, ending on the destination as an image | orbit, tilt, crane, pedestal, push-in, pull-back, punch-in, drop reveal, zooms |
| a **constant** — something is held for the whole shot | `Movement / Speed / Framing / End` slots, with the constant in Framing | tracking, front tracking, follow behind, chase, handheld, vehicle track, snorricam, drone track, time-lapse |

The constant-moves land on the slotted form, and the arrival-moves need the
destination spelled out. Getting this
backwards is how `orbit` under-rotates — the slotted form's End slot says
"complete the intended arc **or full circle**", which is not a destination at
all.

### State what must not move

A model invents geometry unless told not to: without this clause, a room grows
shelving, racking or openings it never had.

> THE ROOM IS RIGID AND MUST STAY PUT: the benches, the shelving and the window
> wall keep their exact shape and position, and nothing appears or disappears.

Name the actual objects. "Keep it consistent" does nothing.

### The camera does the turning, not the actor

The cheap way to satisfy "we end on her face" is to rotate *her*. That reads as
the move in a single frame and is a lie in motion. Any move whose arrival is an
aspect change needs the guard: **they never rotate, never step, never turn
toward the lens.**

### Camera properties get smoothed; the ACTION slot does not

Motion written as a property of the camera gets ironed flat: handheld becomes a
small organic drift, and a `POV walk`'s head-height sway with each footfall
becomes a perfectly smooth dolly.

What it animates reliably is what a body does. So when a move's identity lives
in a small repeating motion, give the motion to a body in the ACTION line — arms
swinging and exchanging, a head turning — rather than asking the camera to shake.

**The camera does not then inherit it, and that is the honest limit.** The body
carries the rhythm and the tile reads as walking; the lens keeps gliding. No
framing or wording produces a footfall bob, so treat handheld sway as something
the model will not give you, and get the motion into the frame some other way.

### What a model cannot be asked to distinguish

It renders the RESULT and is indifferent to the MECHANISM. Each pair below
renders as one move, however carefully the fragment separates them:

- optical zoom against dolly-in — both just "the frame got tighter"
- pivot against short truck — both just "the frame swung right"
- arc against lateral travel — which is why `orbit` is the only circling move
- travel past a static subject against travel alongside a moving one — which
  is why `tracking lateral` covers both

So do not spend a clause defending a distinction the picture cannot carry.
Where two moves differ only in mechanism, the honest move is to keep one
preset for both.

### If you are generating a start frame too

- **The start frame pins the camera height**, and no prompt moves it mid-clip.
  A low tracking shot must START low; asking the camera to descend does nothing.
  Same for a tilt: up starts on the feet, down starts on the face.
- **The start frame also decides which motions are AVAILABLE.** A corridor of
  straight facades running to a vanishing point offers exactly one axis — down
  the street — so `snorricam`'s "the whole world lurches behind them" turns into
  a dolly in and out there, the one thing a snorricam never does. On a crowded
  dance floor, with no straight wall and no vanishing point to travel along, the
  same sentence gives the swing. Before writing the move, ask what the geometry
  in the frame makes easy — the model will do that, whatever the words say.
- **An empty region is not neutral, it is an invitation to invent.** A flat far
  field gets rebuilt frame to frame, so distant objects in it wobble left and
  right. Fill the frame with rigid structure.
- **Many small parallax cues beat one big foreground object.** A lone near
  object sweeps the whole frame on any lateral or orbital move and takes the
  subject with it.
- **Dark subject on a pale ground** reads at tile size; pale on pale does not.

### What goes wrong per move, and what to fall back to

Each row names a move's characteristic failure and its fallback. Treat a row as
a thing to check before dispatch.

**Read the third column as an instruction to the prompt, not to the shot.** Most
of these failures are the model filling a slot we left empty. Where our fragment
already fills it, the row says so — those are worth keeping precisely because a
later edit that "simplifies" the fragment would reopen the hole.

| Preset | Goes wrong when | Fall back to |
|---|---|---|
| `locked off` | anything short of refusing movement outright gets a slow drift added | our fragment already refuses it in as many words — the row exists so that clause is never trimmed |
| `slow pan` | the pan has no destination, so it becomes the same aimless drift a missing instruction produces | name what the pan lands on, not only that it ends composed |
| `slow tilt` | a tilt mixed with any pan warps geometry, worst on a face | one axis only, and name both ends — where it starts, where it lands |
| `slow push-in` | nothing in the scene triggers the move, so it reads as aimless drift; held too long, it stops reading as real time | a short straight push that begins on a visible trigger and ends on a named held frame |
| `slow pull-back` | the thing revealed is vague, or the space behind the subject is underdescribed, so the reveal arrives empty | open on one clear subject and reveal exactly one new layer |
| `slow zoom in` / `slow zoom out` | — | the safest move that exists on a face: no camera travel means no parallax, so nothing warps. Reach for it when a push-in worries you |
| `fast zoom in` / `fast zoom out` | the faster the zoom, the harder the model drags everything else into slow motion | the real-time clause in the shot header is load-bearing here, not decoration |
| `crash zoom` | the snap lands on nothing in particular, so it reads as a glitch rather than emphasis | land it on a named feature — the eyes, the hands, one object |
| `crash zoom out` | the wide arrives but the new information was never described, so the shock has nothing to be about | say what the wide reveals; the reveal *is* the shot |
| `slider` | nothing real sits close to the lens, so there is no parallax and the move degrades into a small pan | put a named object in the near foreground — the parallax is the whole point of the move |
| `pedestal` | the model blends the rise with a tilt into a curve | our fragment already says lens level, no tilt |
| `push through` / `through glass` / `pass through` | the opening is only half crossed — the commonest failure of this whole family | the barrier must be fully passed, and the space beyond it named |
| `orbit` | a full circle drifts both identity and room geometry; and if nothing in the frame changes during the move, the orbit is decoration | a part turn ending on a named aspect — our arrival rule above already fixes the under-rotation half of this |
| `follow behind` | — | tracking legitimately begins already in motion, so its start needs no instruction. Only the ending is still yours to decide, and it still needs deciding |
| `front tracking` | — | the most stable tracking there is for a face: the subject barely moves relative to the lens, so identity holds |
| `tracking lateral` | the background was never described, and the background is where the sense of speed actually lives | name the layers that will stream past behind them |
| `low tracking` | the face creeps into frame because nothing forbade it | "the face is never shown" is an instruction models respect — say it rather than trusting ankle height to imply it |
| `vehicle track` | the camera is not anchored to anything, so the shot floats free of the vehicle | name what it rides — a parallel car, a rig on the door |
| `chase` / `handheld run` | the shake is constant and uncaused, which reads as an effect rather than an operator | every correction needs a cause: a turn, an obstacle, a stumble |
| `handheld shaky` / `handheld settle` | asked for as abstract "shakiness", which models render worse than a described human | our fragments already name the operator's breath and weight — that is the form that works |
| `snorricam` | the rig is not described as rigid, and it returns as an ordinary handheld shot of a face | keep "rigged to the body" explicit; our fragment does |
| `crane up` | the high frame was never designed, so the rise lands on nothing; too fast a rise throws away the intimacy it opened with | start close enough to establish the person, end on one clear wide payoff — and say the subject stays in frame as the camera climbs, or it becomes a fly-away |
| `crane down` | the descent has no named landing, so it drifts to a stop | name the one window, one face, one object it arrives on |
| `drone establish` / `drone track` | the flight has no line to follow, so the drone wanders | give it a road, a river, a coastline, a wall |
| `whip pan` | used as a hidden cut with the blur on either side unmatched in direction, density or brightness — then the cut shows; busy content inside the blur reads as noise | match direction and blur on both sides, and keep the blurred frames empty |
| `pass-by reveal` | the camera leaves the subject without arriving at something that matters, so the move reads arbitrary | make the destination clearly more important than what was left behind |
| `roll` | the space has no strong geometry to rotate against, so there is nothing to read the roll against; past a point the chaos is unreadable | keep firm horizontals and verticals in frame as the reference |
| `rack focus` | focus and camera movement begin at the same instant, muddying the cue; or the first object was never clearly established | land the focus change first, then move — and our fragment already holds the frame still through it |
| `infinite zoom` | more than about two worlds in one clip and the geometry stops holding | two per clip; chain clips for a longer dive |

**Three common fixes that do not hold:**

- **Zoom against dolly.** Naming *"the camera stays in a fixed position"* does
  not stop the model blending them; the two still render indistinguishable,
  because the model renders the RESULT and is indifferent to the MECHANISM
  (above). Keep the clause, keep the expectation low.
- **`orbit`.** *Use fewer degrees* is the quantity form this file's first law
  rejects. The fix is the arrival form.
- **Dolly zoom.** There is no dolly-zoom preset; the nearest move here is
  `slow pull-back`. A line holding the subject's size exactly constant while the
  background moves is not a reason to write one.

### Big face, simple move

**The tighter the frame on a face, the simpler the move has to be.** A wide
shot will absorb almost anything — a sweep, a rise, a circle — because no single
part of the frame is under enough scrutiny for a small error to show. Once a
face fills the frame, the same move has to hold a likeness steady through every
one of its frames, and that is where identity drifts and features warp.

So at close-up and tighter, stay inside: `locked off`, `handheld settle`, a
short `slow push-in`, `slow zoom in`, `rack focus`. Save `orbit`, `crane up`,
`roll`, `whip pan`, `pass through` and the aerials for the wides.

This is `orbit`'s row above — *the wider the shot, the safer the circle* —
stated once as a rule rather than once per preset, because it holds for every
path in the kinetic register and not only the circular ones.

## Shot-size ladder — a DISTANCE, and nothing else

Nine rungs, wide to tight — the handbook's seven plus our `MCU` and `MWS`. A
size says how much of the figure the frame holds
and **nothing about who else is in it or where they stand** — that is the
arrangement below, and keeping the two apart is what stops "OTS" being used as a
distance.

**Ids:** `detail` · `ECU` · `CU` · `MCU` · `MS` · `MWS` · `WS` · `EWS` · `establishing`

*(The sentence each id compiles to lives server-side. Pass the id to `picsart_film_compile_prompt` and it pastes the tuned wording; never write that sentence yourself.)*

**The handbook's seven shot sizes are all rungs.** Establishing
Shot → `establishing`, Extreme Wide Shot → `EWS` (its sentence is the fragment),
Wide Shot → `WS`, Medium Shot → `MS`, Close Up → `CU`, Extreme Close Up → `ECU`,
Detail Shot → `detail`. Two of them lean on the arrangement beside them: a
`detail` is normally shot as `insert` (a thing, no face — a hand may enter), and
an `establishing` opens the scene on its `single` or `group`, first in the
scene, before the action. The size still says only how much the frame holds;
the arrangement says who is in it.

## Arrangement — who is in frame, and how they sit in it

**`OTS` and `insert` are not rungs on the ladder above.** They are not
distances: an over-the-shoulder can be a medium or a close-up, and an insert has
no figure to measure at all. Worse, a size chosen from a single list would
quietly decide the staging too — a plan asking for "OTS" makes a claim about two
bodies holding fixed positions, and a size list checks nothing against the
scene's map.

So arrangement is its own decision, and **anything with a second body is a claim
that gets checked** before a shot renders.

**Ids:** `single` · `two-shot` · `dirty single` · `OTS` · `over the hip` · `triangle 2+1` · `triangle 1+2` · `face to face` · `back to back` · `POV` · `insert` · `group`

*(The sentence each id compiles to lives server-side. Pass the id to `picsart_film_compile_prompt` and it pastes the tuned wording; never write that sentence yourself.)*

`insert` pairs with any tight size; `single` is the default and the only one that
makes no claim about a second person. The five rows from `over the hip` to `back
to back` are the handbook's *Character Blocking*, its wording kept;
`<subject's character view>` is filled from the Character view table below —
the handbook writes the far subject's facing into the blocking line, and so do
we. Anything with a second body is still a claim checked against the scene's
map before it renders.

## FOV ladder — ten anchors, one per shot, locked

FOV changes only on a hard cut. Every shot's degrees go into its prompt — pass
the card's lens as the shot's `fov` to `picsart_film_compile_prompt`, whether the user
changed it or left it as seeded (`prompt-blocks.md`, Part 2, *The card's own
picks*); the lens equivalent is for talking to humans.

| Anchor | ≈ lens (ff) |
| --- | --- |
| 10° | 200mm |
| 15° | 135mm |
| 24° | 85mm |
| 31° | 65mm |
| 40° | 50mm |
| 54° | 35mm |
| 65° | 28mm |
| 74° | 24mm |
| 90° | 18mm |
| 104° | 14mm |

*(The sentence each id compiles to lives server-side. Pass the id to `picsart_film_compile_prompt` and it pastes the tuned wording; never write that sentence yourself.)*

**These degrees are the real ones.** A full-frame 50mm is 39.6° horizontal; the
anchors above round it honestly, so one lens has one number on every surface.

**This ladder is the film's only focal length.** The setup's Lens pill is the
glass *family* (spherical, anamorphic, vintage…), which says how the picture
renders, never how wide it is. The setup carries no aperture either; the table
below is the only one. That is why a seeded lens is never skipped: with no focal
length in the style line, a shot whose lens is not passed reaches the model with
no focal length at all.

## Aperture / depth

**Ids:** `f/1.4` · `f/4` · `f/11`

*(The sentence each id compiles to lives server-side. Pass the id to `picsart_film_compile_prompt` and it pastes the tuned wording; never write that sentence yourself.)*

## Angle / height

**Ids:** `eye level` · `low` · `high` · `overhead` · `drone top-down` · `top-down foreshortening` · `low foreshortening` · `three-quarter` · `dutch`

*(The sentence each id compiles to lives server-side. Pass the id to `picsart_film_compile_prompt` and it pastes the tuned wording; never write that sentence yourself.)*

The `low`, `high` and `dutch` fragments carry the handbook's wording, and
`drone top-down` and the two foreshortening rows are its *Camera Angle* table —
the low foreshortening shot is written there as a five-line spec, and its
fragment is that spec as one clause. Its *Eye Level*, *POV
shot* and *Dutch* were already here; POV lives in Arrangement, since it is a
claim about who is in frame.

## Character view — which way the subject faces the lens

The handbook's axis: the camera's height says nothing about whether we see a
face or a back. Written into the blocking line for every
present character; the handbook's phrases are the fragments.

| Preset | Use it when |
| --- | --- |
| front | the face matters and the audience must read them |
| profile | direction, silhouette, or face-to-face blocking matters |
| three-quarter | both face and side angle visible — the cinematic default |
| three-quarter back | leaving, looking over a shoulder, a partial reveal |
| rear | the face must not be seen; the back and the body's direction matter |

*(The sentence each id compiles to lives server-side. Pass the id to `picsart_film_compile_prompt` and it pastes the tuned wording; never write that sentence yourself.)*

## Placement — where the subject sits in the frame

The handbook's three terms. Centered is direct and confrontational; a third opens
negative space, creates direction and leaves room for the second subject or the
environment. Written into the blocking line, one per shot when it matters.

**Ids:** `centered` · `left third` · `right third`

*(The sentence each id compiles to lives server-side. Pass the id to `picsart_film_compile_prompt` and it pastes the tuned wording; never write that sentence yourself.)*

**Which third is not a free choice — leave the room in front.**
The open side goes where the subject is looking or moving: someone looking
frame-right sits on the *left* third, so the space they look into is in front
of them. Put the empty half behind them instead and the shot reads as trapped,
about to walk into the edge — the frame is composed correctly and still feels
wrong, which is why this one is hard to spot in review. Say it in the blocking
line as the space, not as a rule: *"Rasa on the left third, the length of the
platform open in front of her."*

Not to be confused with the eyeline rule in `seams.md`, which is about two
shots across a cut — A looks off frame-right, and the thing is on frame-left in
B. Lead room is about the space inside one frame. The two are independent:
obeying one says nothing about the other.

## Composition — how the frame is organised

The handbook's five, its wording kept. Written into the blocking line only when
the frame's organisation carries meaning; a shot that names none is composed by the
arrangement and the placement alone.

| Preset | Good for | Use it when |
| --- | --- | --- |
| symmetrical | formal scenes, controlled environments, a centered subject, balanced power | balance, order, ritual, control, a clean centered frame |
| leading lines | hallways, roads, tables, lights, ceiling lines, counters | the environment should guide the eye to the subject |
| separated by distance | emotional distance, threat across the room, foreground/background contrast | distance should create tension, loneliness, power or scale |
| side by side | partnership, comparison, walking together, matching reactions | two subjects share the frame on one plane |
| vanishing point | roads, hallways, long rooms, aisles, streets | the scene should have depth lines pulling toward one point |

*(The sentence each id compiles to lives server-side. Pass the id to `picsart_film_compile_prompt` and it pastes the tuned wording; never write that sentence yourself.)*

## Atmosphere — what is in the air between the camera and the distance

Ours, not the handbook's. The second tool for the job the three planes do: the
planes give the eye somewhere to travel, and atmosphere is what physically
separates them. Air is not empty, so the further away a thing is the more air
sits in front of it — distant things lighten and lose contrast, and the eye
reads that as distance before it reads anything else. Naming it is the fastest
way to stop a frame reading as a subject pasted on a backdrop.

| Preset | Use it when |
| --- | --- |
| haze | a big exterior should feel vast; the background must sit far back |
| low fog | the planes must be unmistakably separate; ground-level menace or cold |
| light shaft | an interior with one strong source; the air should be visible |
| smoke drift | movement and mood on top of depth — a fire, exhaust, a kitchen |

*(The sentence each id compiles to lives server-side. Pass the id to `picsart_film_compile_prompt` and it pastes the tuned wording; never write that sentence yourself.)*

**It belongs to the place, not the shot.** A street that is hazy in one picture
is hazy in all of them, or the location comes apart worse than a moved wall
would break it. So it is decided at the location's plate, carried in the
`Setting` line of every picture made there, and never introduced by a single
shot — *a frame outranks the words* (the language laws), so a shot asking for
fog the plate does not have will fight its own reference and usually lose.

Check it against the locked look before using it: a stock with strong halation
and a haze clause will wash the far plane twice.

## Camera artefacts — the small failures that prove a camera was there

A real camera is a physical object with a lens that has to hunt for focus, a
meter that has to catch up to a changing light, and a front element that things
land on. A generated shot has none of those, and its *absence* is one of the
tells: the image is impossibly clean and impossibly decided, and it reads as a
render for the same reason a face with no pores does.

This is the moving half of the family the video prompt's quality line already
opens with frame rate and shutter angle (`prompt-blocks.md`, Part 1 item 7).
Those two say how motion blurs; these say what the instrument does while it
films.

**They ride the quality line, and never the Breathing feel line.** Breathing
feel is one of the handbook's two camera lines carried *verbatim* (Part 1 item
5) — it is not ours to extend, and appending to it is exactly the failure the
book-fidelity rule exists to prevent. The quality line in item 7 is marked ours
and already carries the skin clause and the frame rate; that is where these
belong. Never into `stylePrefix` either — like shutter angle they are **video
only**, and a still has no focus hunt.

**Ids:** `focus hunt` · `exposure shift` · `lens contact` · `late reframe`

*(The sentence each id compiles to lives server-side. Pass the id to `picsart_film_compile_prompt` and it pastes the tuned wording; never write that sentence yourself.)*

**One per shot at the very most, and not in most shots.** These read as an
accident, and an accident that happens on every shot is a style — at which point
it stops proving a camera and starts proving an effect. The rule for handheld
shake applies unchanged: the moment the viewer notices it as a
technique, it has failed.

**Check against the film's chosen texture first.** A film whose look is formal —
locked-off frames, controlled light, the polished registers — is actively hurt by
a focus hunt, the same way a haze clause hurts a stock with strong halation. The
fragments belong to a film that is pretending to be found or observed, and the
Breathing feel line is where that is already decided.

The related move, a handheld camera snapping into a subject and correcting —
the documentary snap zoom — has **no preset here**, deliberately: it is two
moves in one shot, which the one-move-per-shot law refuses. Where a shot needs
it, design it as a shot, not a fragment.

## Without boards

Offer movement as one question (4 options drawn from the scene's energy, preview =
the fragment), size + FOV + aperture as a second, angle folded into whichever
needs it. Character view, placement and composition are written from the
staging, never asked. Record chosen preset names in the shot's `design`; paste
fragments into the blocking and camera lines unchanged.
