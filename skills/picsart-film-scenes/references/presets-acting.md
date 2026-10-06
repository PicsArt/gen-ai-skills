# Acting presets — the emotion wheel, gaze, and eye-life

> **The wordings live on the server.** This file decides *which* preset to
> reach for — that judgement is the part that needs a reader. The sentence each
> id compiles to is not here: those sentences are tuned against real renders,
> and a prompt written from a remembered copy of one renders worse than a prompt
> that pastes it. Pass the id to `picsart_film_compile_prompt` and the server
> pastes the sentence.

The vocabulary behind every performance decision in the pipeline: the review
board's per-character direction controls and the text-choice fallback. What
reaches the model is the shot block's emotion — one or two words per visible
face (`prompt-blocks.md`, Part 2), and **the chat picks them from this wheel
while writing the block; the user is never asked to choose an emotion on a
board or in a menu.** The fuller skeleton below is the chat's own vocabulary
for reading a moment, not prompt text. The skeleton per character: state · what
he wants · what he hides · body rhythm · 2–4 visible habits · what changes
across the shot · one unspoken inner line — plus eye-life. The emotion wheel
fills the *state* and *body rhythm* slots; the direction lane of the shot card
fills wants/hides/change; the inner line is authored fresh per shot.

## The wheel — eight emotions × three intensities

Intensity is how much of it is **visible**, not how much is felt. Intensity 1 is
the most cinematic and the default: the camera is close enough to see suppression.

**One shot in the film is the exception — the peak.** The story head's `Peak`
line (`../../picsart-film-development/references/dramaturgy.md`) names the beat the film
is built toward; the shot whose story paragraph covers that beat plays it. There,
and only there, the visible reaction **is** the point: a viewer catches the
feeling off the character's face, so a face holding it in leaves them nothing to
catch. The peak shot takes **intensity 3**, carries no `hides` slot, and names
the physical sign in plain words — eyes filling, a breath that breaks, a laugh
that gets away, hands that find the other person. Every other shot in the film
keeps intensity 1. Suppression everywhere is right; suppression at the peak
throws away what the whole film was built to deliver.

**This wheel is the only emotion vocabulary.** A state outside it — `tense`,
`wary`, `relief`, `broken` — is a blend rather than a wheel position, and
guessing which position it meant is worse than not having it. A payload carrying
an id that is not on the wheel is an unknown id: the control reads "as
generated" and the user picks again.

A surface with no intensity control of its own uses **intensity 2 (open)** — the
one an audience reads without the camera being close. Only a surface that lets
the user say "hold it in" should be sending intensity 1.

**Ids:** `joy` · `sadness` · `anger` · `fear` · `surprise` · `disgust` · `trust` · `hope`

*(The sentence each id compiles to lives server-side. Pass the id to `picsart_film_compile_prompt` and it pastes the tuned wording; never write that sentence yourself.)*

## Gaze target — always named

Every character's entry names where the eyes live: `gaze locked on <target>` /
`gaze avoiding <target>, finding <substitute>` / `gaze on the task, flicking to
<target> at <beat>`. An unnamed gaze is where generated faces go dead. The
listener in a dialogue shot gets a gaze line too — listening is a performance.

## Eye-life

Standing fragment, appended per character and tuned by ONE word — the blink
rate. Three settings: composed, strained, and a predatory/frozen one to use
rarely. The compiler holds the wordings and picks by the character's state.
Catchlights are always requested, in all three; a face without them reads as
rendered, which is why the fragment is standing rather than optional.

## The living shot — rules that keep frames from dying

Four standing rules, written into the acting block whenever they apply:

- **The reaction starts before the line ends.** The listener's face begins to
  answer while the speaker is still talking — brow, breath, a weight shift.
  Reactions that wait for the line to finish read as turn-taking robots.
- **Hands are always busy.** Every character holds a task — coiling a rope,
  wiping a cup, worrying a strap. Idle hands are where duplicated fingers and
  dead performances live; a task also gives the actor something to *stop doing*
  at the dramatic beat.
- **Micro-life every one to two seconds.** Somewhere in frame, something small
  moves: a blink, steam, a curtain, a background figure shifting weight. A
  frame with no micro-life for two seconds reads as a freeze even when the
  camera moves.
- **Stillness is held tension, never "nobody moves."** Calming phrases freeze
  the render. Write what the stillness *costs*: "he holds himself still, breath
  shallow, knuckles whitening on the rail" — the body working to not move is a
  performance; absence of motion is a bug.

## Hidden intention

The `hides` slot pairs the wheel with its mask: `hides fear` under anger,
`hides relief` under scolding, `hides recognition` under politeness. The mask is
what the face performs; the emotion is what leaks. Write both, in that
relationship: `shame at intensity 1, masked as concentration`.

## Without boards

Nothing changes: no question is asked either way. The chat reads the story's
paragraph for the moment, picks the emotion and its intensity from the wheel,
and writes the one or two words into the shot block.
