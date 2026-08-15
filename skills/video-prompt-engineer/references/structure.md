# Structure

A prompt is read start to finish, and earlier clauses frame the later ones. This order puts the decisions that cannot be undone first, and the exclusions last.

## One prompt, several beats

For a piece with no dialogue that is being generated in one pass, the prompt carries the beat
structure inside it. The shared description sits at the top and applies throughout; each beat
then gets its own duration, action and camera.

```
STYLE: <one string for the whole clip>
CHARACTERS: <every character on screen, once, for the whole clip>
SETTING: <the one location>
AUDIO: <one string for the whole clip, on a model that generates audio. The theme first, then the
        ambience that runs throughout. Omit the line entirely on a model with no audio track>
NEGATIVE: <one string for the whole clip>

BEAT 1, 0 to 6 seconds
ACTION: <one thing happening>
CAMERA: <shot size, angle, movement>

BEAT 2, 6 to 13 seconds
ACTION: ...
CAMERA: <a different shot size or angle from beat 1>
TRANSITION: cut

BEAT 3, 13 to 20 seconds
...
```

Rules that make the difference between a sequence and a drift:

- **Every beat changes the camera.** Two beats at the same shot size and angle read as one
  long shot with activity wandering through it, which is the failure this form exists to avoid.
- **Six to ten seconds per beat.** Shorter and the model will not complete the action; longer
  and it starts inventing.
- **Name the transition** where you want a hard cut. Left unsaid, a generator dissolves or
  glides between beats.
- **State the shared lines once.** Repeating the style, cast and audio per beat wastes the budget
  and invites the model to reinterpret them mid-clip. Where one beat needs a sound the others do
  not, add it to that beat as `SOUND:` rather than rewriting the shared `AUDIO:` line.
- **Keep the running total visible** in the beat headings, as above, so it is obvious whether
  the whole thing fits the model's maximum duration.

If any beat needs a spoken line, this form is the wrong one: go back to separate chunks.

## Clause order

1. Duration
2. Aspect ratio
3. Medium and style
4. Shot size
5. Camera angle
6. Camera movement
7. Lens and focal length
8. Depth of field
9. Lighting
10. Colour and grade
11. Subject motion
12. Mood
13. Pacing and cuts
14. Audio, on a model that generates it. Ambience, effects, music, and whether anyone speaks
15. Exclusions

**Audio sits last before the exclusions, inside the prompt.** On a model that generates sound the
audio clause is part of the prompt, not a note delivered alongside it, and its place is
immediately above the exclusion line so that the exclusions can rule out what the audio clause
did not ask for. Where a sequence has a theme, the theme clause is the first thing in the audio
position and is byte identical in every scene.

Clause 14 is dropped entirely on a model that produces no audio track, and is never left out on
one that does. On an audio-capable model, `no audio, silent clip` is a clause and an omission is
not: see `references/audio.md`.

One clause per decision, commas between them. A prompt is a list of decisions, not a paragraph of atmosphere. Prefer a number to an adjective wherever a number exists: 8 seconds over short, 85mm over flattering, 116 BPM over upbeat.

Keep a single shot prompt under roughly 120 words. Past that, generators start dropping clauses, and the ones they drop are at the end, which is where the exclusions live.

## Two limits, and the smaller one binds

The 120 words above is a **craft limit**: past it a generator loses clauses on its own, whatever
the API allows. On top of it sits the model's **hard character cap**, which truncates from the end
without saying so. Kling 3.0 allows 2500 characters and others are tighter, so establish the real
figure from the model's documentation rather than its name, and write to 1000 characters when it
is unknown.

For a single shot the craft limit binds first and the cap rarely matters. It bites on the two
forms below, where a header plus 6 shots or 4 beats passes 2500 characters without feeling long.
Count the characters on those. Both failure modes take the end of the prompt, which is why the
exclusion clause is the thing you lose, and why the output comes back wrong in a way that never
points at length.

Two things buy back most of the budget:

- **The shared header is stated once.** See below. It is the largest and most common waste.
- **Exclusions move to the negative field** where the API has one, and are then deleted from the
  prompt body. Not both: a repeated ban wastes the budget twice and reads as emphasis on the
  banned thing.

## More than one shot

Use a labelled block per shot, with the shared lines stated **once** in a header above them.

The header is the whole point of the form. Everything that is a decision about the piece rather
than about one shot goes there, once, and no shot block restates it. Restating it wastes the
character budget and invites the model to reinterpret a decision mid-prompt, which is the drift
the header exists to prevent.

**This applies inside one prompt.** When each shot is generated separately, every prompt carries
its own full copy of the shared lines, byte identical, because the next call has no memory of the
last. Paraphrasing between those separate prompts is the single biggest cause of a sequence that
will not cut together. One call: state once. Several calls: repeat in full.

```
STYLE: <one string for the whole prompt, stated here and nowhere else>
CHARACTERS: <one description per character on screen, stated here and nowhere else>
AUDIO: <the theme, stated here and nowhere else, on a model that generates audio>
NEGATIVE: <one string for the whole prompt, stated here and nowhere else>

SHOT 1
SCENE: <what is in frame>
CAMERA: <shot size, angle, one movement>
MOTION: <one action, completed within the shot>
SOUND: <only what this shot adds: its ambience, its effects. Omit when it adds nothing>

SHOT 2
SCENE: ...
CAMERA: ...
MOTION: ...
```

One action per shot. If a shot needs two things to happen, it is two shots.

`AUDIO` is shared and `SOUND` is per shot, and the split matters. The theme belongs at the top
because it is one decision about the whole piece; the room tone and the footsteps belong to the
shot that has them. Restating the theme inside each shot invites the model to reinterpret it, which
is the same failure as restating the style line.

Where the shots are generated separately and cut together, the shared `AUDIO` line reads
`ambience and effects only, no music`, because per-clip generated music restarts at every join. The
theme then goes on as one track afterwards. See `references/audio.md`.

## The CHARACTERS line is not optional

Anything with a recurring character needs it, and it is the line most often left out. A generator has no memory between clips: scene four does not know what the person looked like in scene one, so the only thing carrying a character across a sequence is the same words appearing in every prompt.

Where a character bible exists, this line is the `Verbatim description` from `<bible>/<character-id>.md`, pasted, not summarised. Use the `Short form` for a single clip and the `Long form` when the character has to hold across a sequence. Repeating a slightly different description in each scene is the same as giving the generator a different person each time, and it is the most common cause of a cast that drifts across an episode.

Two practical rules:

- **Only the characters actually on screen.** Listing the whole cast in a shot that holds one person invites the others into frame.
- **Same order every time.** Where two characters appear together, keep them in the same order in the line, because a generator reads position as emphasis.
