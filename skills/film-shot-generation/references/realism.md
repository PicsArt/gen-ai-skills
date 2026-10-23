# Realism: what makes a shot read as filmed

A prompt that reads as filmed names how bodies, cloth, light, sound and objects behave. The
compiler already writes the house lines (the frame rate and shutter, the skin, no music, the
silence after a line). What follows is what only the shot knows, written into the fields the shot
already passes: the performances, `setting`, `audio` and `extra`, plus the call's top-level
`filmConstraints`, the whole lines the film imposes on every prompt.

These are physical rules, true of any camera. Devices that imitate a cheap one (autofocus hunting,
exposure breathing, uneven zooms, tape texture) are not realism: they fight the look the film
locked. A camera artefact the film wants is picked in the shot's `artefact`, never written in.

## Physical consequence: the action lands on something

**Write what the action does to something else in frame, as the same event.** The card's action
stays word for word; the effect is appended to it in the performance's `action`:

- "She sets the plate down, and the candle flames flutter."
- "He exhales, and the candle flames tremble but stay lit."
- "Water drips from her hair onto her robe, leaving dark spots that spread into the cloth."

One event, two objects. "She sets the plate down and straightens the candles" is two actions, and
one primary action per person per shot still holds. Write a consequence only on a shot with a
physical event; a shot of someone listening has none.

When the camera itself reacts to a force (a slam, a blast, a passing train), the event comes first
and the frame jolts only when the force reaches it. A camera that shakes before the cause reads as
fake.

## Sound: name what plays

The compiler bans music; it cannot say what the room sounds like. Name it:

- **Room tone**, in each shot's `audio`, as a short list of real sources: "the fridge hum, rain on
  the skylight, a radio two rooms away". Keep it word for word through every shot of the scene,
  like the geography line, so the takes match.
- **Each physical event's sound**, in the sentence of the event: "the door slams, the latch
  rattling", "her keys clink on the tile". Its owner is the thing that made it.
- **Only what the room makes.** Say so once in the top-level `filmConstraints`: "Only sounds the
  scene's own sources make; no designed whooshes or transition sounds." A designed whoosh announces
  the cut the blocks were written to hide.

## Mouths and invented speech

The compiler closes the speaker's line with silence. It does not cover the others in frame.

- **Every person in frame who is not speaking** carries it in their performance `note`: "mouth
  closed, listening". In a two-shot, a listener who mouths along is a defect anyone sees.
- **Only the scripted lines are spoken.** Say so once in the top-level `filmConstraints`: "Only the
  scripted lines are spoken: no ad-libs, mumbling, extra words or off-screen voices."

## Hands, teeth, hair and cloth, stated as behaviour

A take is checked for hands and teeth after it lands (`references/takes.md`); this is the other
side, asked for before. State each as what it does, in `extra` or the performance it belongs to:

- **Hair** answers to fingers, gravity and the shoulders it touches: "her hair falls back as she
  straightens".
- **Cloth** creases where the body bends and settles when it stops; a coat swings with the turn.
- **Jewellery and straps** hang and settle with the body: "the chain swings and settles against
  her collar".
- **Hands** have a named job (`references/repairs.md`); a hand that holds something says what.
- **Teeth** show only when the performance opens the mouth: a smile, a line, a grimace.

Name the objects that touch: "her fingers press into the sleeve", never "she holds him". A contact
named is one the model keeps from clipping through.

## Reflections

When a shot holds a mirror, a dark window, a screen, still water or polished metal, or uses the
`mirror/insert POV` move, the reflection is part of the frame. Say in `extra` who it shows, from
the mirrored angle, moving with them in the same instant: "the mirror shows Ana's face from the
front, matching her every movement". Left unsaid, the model invents a reflection of its own, late
or of someone else.

## Continuity written as persistence

One generation holds clothes and light through its cuts. It does not reliably hold a detail the
film has just shown: a sleeve rolled up, a necklace fastened, a glass half emptied, an object picked
up.

- **Every detail shown persists after it is shown.** Write it into each later shot of the run where
  it is visible: "the sleeve stays rolled to the elbow", "the letter is still in his left hand".
  Nothing resets between shots.
- **The light holds.** For a run of several shots, say once in `extra`: "the light and the time of
  day hold through every shot". One generation can jump from day to dusk between its own cuts.
- Across runs, a changed state has its own tag, and a run that changes it makes later runs wait for
  its accepted take (Runs, in this skill). This is the same rule inside one run.
