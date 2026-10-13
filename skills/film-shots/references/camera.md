# The camera: a move per shot, written so the model makes it

A shot's `move` is an id from the compiler's movement vocabulary, and the compiler writes the
sentence. What it cannot write is what only the shot knows: where the camera ends, what starts it,
and whether this move suits this size. Those go in the fields the shot already passes: `subject`,
`slots`, `framing`, the performances and `extra`. What the camera moves past is the scene's, not
the shot's: the top-level `space`, one foreground, midground and background identical in every
prompt of the scene.

## Contents

- Name where the camera ends, never how far it moves
- Big face, simple move
- What the model will and will not do
- The frame the run opens on decides what is possible
- Per move: what goes wrong, and what to write

## Name where the camera ends, never how far it moves

A model renders a picture, not a quantity. "Orbit through 90 degrees", "push in two metres" or "a
little to the left" each come back as a fraction of the move or none of it. "Her face square to the
lens" is a frame the model can make.

- **An arrival move** (push-in, pull-back, tilt, pan, crane, pedestal, orbit, the zooms, a reveal)
  ends on a destination written as an image: fill `subject`, and the move's `slots` where it has
  them (a side, a target; a compile error names a missing one), with what the last frame shows.
  "Ending on the deed in her hand", not "ending closer".
- **A tilt or a pan names both ends**: where it starts and where it lands ("from his boots to his
  eyes"). The scene picture or the frame the run opens on already fixes the start, so the two must
  agree.
- **A constant move** (tracking, follow, chase, a vehicle or drone track) has no arrival; its
  identity is what it holds the whole shot. Write that constant in `framing`: "her face held
  centre-frame at the same size", "the car's side filling the left half".
- **Every move has a trigger** in the shot: a sound, a look, a word, an entrance. Write it in the
  action or `framing` ("as the phone buzzes, the camera begins to push in"). A move with no cause
  reads as drift.

## Big face, simple move

**The tighter the frame on a face, the simpler the move.** A wide absorbs a sweep, a rise or a
circle, because no part of the frame is under scrutiny. Once a face fills the frame, every frame
of the move has to hold the likeness, and that is where identity drifts and features warp.

| Size | Moves that hold | Moves to keep for the wides |
|---|---|---|
| CU, ECU, detail of a face | `locked off`, `handheld settle`, a short `slow push-in`, `slow zoom in`, `rack focus` | `orbit`, `crane up`, `roll`, `whip pan`, `pass through`, `push through`, the drone moves |

The camera on an approved card is the user's choice. A kinetic move on a face at close-up or
tighter is the risky case: the likeness drifts and the features warp. It has two safer versions,
the simple move at the same size or the same move on a wider shot, and the shot is flagged with
both. Never swap it quietly. A wide on a simple move is not flagged.

## What the model will and will not do

- **It renders the result, not the mechanism.** An optical zoom and a dolly-in both come back as
  "the frame got tighter"; a pivot and a short truck both as "the frame swung". Choose the move by
  the frame it ends on, and spend no words defending a difference the picture cannot show.
- **Rotation and travel are two different requests.** When a shot wants another angle on the same
  moment, say which: the camera turns where it stands (a pan or tilt that reveals what was beside
  or above it, named), or the camera moves to a new position (named against the geography line:
  "from behind Cal's right shoulder"). Left open, the model decides whether the camera travelled,
  and invents the geometry it travelled through.
- **Motion written as a property of the camera is smoothed away.** Shake, sway and a footfall bob
  come back flat. What the model animates reliably is a body: give the rhythm to a person in the
  action (arms swinging, a head turning with each step). If the shot truly needs an operator's
  shake, it is added in the edit.
- **The camera does the turning, not the actor.** A move that ends on a new side of a person (an
  orbit, a crane down to the face) is cheaply faked by turning the person. Their performance says
  they hold their facing and never turn toward the lens.

## The frame the run opens on decides what is possible

- **It pins the camera's height.** A low tracking shot starts low; a tilt up starts on the feet. A
  prompt cannot move the height mid-shot.
- **Its geometry decides which moves are easy.** A street of straight facades running to a
  vanishing point offers one axis, down the street, and the model takes it whatever the words say.
  Before choosing a move, ask what the frame makes easy.
- **An empty region is an invitation to invent.** A flat far field gets rebuilt frame to frame.
  Fill the scene's top-level `space` with rigid, named structure; many small parallax cues hold
  better than one large foreground object, which sweeps the frame on any lateral move. A move that
  depends on a layer (a slider's foreground, a lateral track's background) needs that layer in the
  scene's `space`, since a shot carries none of its own.

## Per move: what goes wrong, and what to write

Most of these failures are the model filling a field left empty. Check the row before a run is
compiled.

| Move | Goes wrong when | Write |
|---|---|---|
| `slow pan` | it has no destination and becomes aimless drift | name what it lands on in `framing` |
| `slow tilt` | it is mixed with a pan, which warps geometry, worst on a face | one axis only, both ends named |
| `slow push-in` | nothing triggers it, so it reads as drift | a short push that begins on a visible trigger and ends on a named held frame |
| `slow pull-back` | the space behind the subject was never described, so the reveal arrives empty | open on one clear subject; reveal exactly one new layer, already named in the scene's `space` |
| `slow zoom in` | — | the safest move on a face: no camera travel, so no parallax and nothing warps |
| `crash zoom` | it lands on nothing in particular and reads as a glitch | land it on one named feature: the eyes, the hands, one object |
| `crash zoom out` | the wide it arrives at was never described | say what the wide reveals; the reveal is the shot |
| `slider` | nothing sits near the lens, so it degrades into a small pan | a named object in `space.foreground`: the parallax is the move |
| `push through`, `through glass`, `pass through` | the barrier is only half crossed | the barrier fully passed, and the space beyond it named |
| `orbit` | a full circle drifts both the face and the room; with nothing changing during it, it is decoration | a part turn ending on a named side (`slots`), on a wide; never a number of degrees |
| `tracking lateral` | the background was never described, and that is where speed lives | name the layers that stream past in `space.background` |
| `low tracking` | the face creeps into frame | say the face is never shown |
| `vehicle track` | the camera floats free of the vehicle | name what it rides: a parallel car, a rig on the door |
| `chase`, `handheld run` | the shake is constant and uncaused, which reads as an effect | give each correction a cause: a turn, an obstacle, a stumble |
| `crane up` | the high frame was never designed, so the rise lands on nothing | start close enough to establish the person, end on one named wide; they stay in frame as it climbs |
| `crane down` | the descent has no landing and drifts to a stop | name the one face, window or object it arrives on |
| `drone establish`, `drone track` | the flight has no line, so the drone wanders | give it a road, a river, a coastline or a wall to follow |
| `whip pan` | it whips toward nothing; busy content inside the blur reads as noise | always whip to a named target in `slots.target` |
| `pass-by reveal` | what it arrives at matters less than what it left | make the destination clearly the more important thing |
| `roll` | the space has no strong lines to read the roll against | firm horizontals and verticals in frame |
| `rack focus` | the first plane was never established, or focus and a move start together | establish the first plane, land the focus change, keep the frame still |

A whip pan is a move inside one shot. It is never a join between shots: inside a run the only join
is a hard cut (`references/seams.md`).
