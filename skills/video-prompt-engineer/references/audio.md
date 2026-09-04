# Audio

Some generators produce an audio track from the same prompt and some produce none at all.
Which one you are writing for decides whether this file applies, and that is settled in stage 0
of `SKILL.md`.

**On a model that generates audio, saying nothing is a choice you did not make.** The model fills
the silence: a music bed nobody asked for, a room tone that does not match the room, or a voice.
So the prompt always carries an audio line, even when that line is `no audio, silent clip`.

On a model with no audio track, drop every clause on this page. They cost tokens, and a request
for narration on a silent model sometimes lands in the picture instead as on-screen text or a
mouth that starts moving.

**The audio clause goes inside the prompt**, in the clause position immediately before the
exclusion line, or as an `AUDIO:` line directly above `NEGATIVE:` in the labelled block form. It is
not a note handed to the user alongside the prompt. A model that generates sound generates it from
the prompt text, so audio delivered separately is an instruction nothing reads.

## The parts

Write them in this order, in one line or one labelled block. Speech has its own section below,
because it is the part that decides what you can still fix afterwards.

| part | what to say |
|---|---|
| Ambience | The sound the location makes with nothing happening in it. Room tone, wind, traffic, the hum of a fridge |
| Effects | The sound of the action itself. Footsteps, a latch, fabric, a mechanism. Diegetic: it comes from something in frame |
| Music | Whether there is any, then instruments. Never a genre |
| Speech | Whether anyone speaks at all, and whether it is generated here or laid over afterwards |

**Name instruments, not genres.** `Warm ukulele and marimba with light percussion` is a
description a model can act on. `Upbeat indie` is a category, and categories average out into
stock music.

**Ambience is the part that sells the shot and the part most often missing.** A clip with clean
effects and no room tone sounds synthetic even when the picture is good.

## Theme music, across the whole piece

Per-scene sound is the room and the action. A **theme** is the one piece of music that runs under
the entire storyline, and it is decided once for the composition rather than per scene.

Four fields, then reuse the resulting string exactly:

| field | example |
|---|---|
| Instruments | `solo piano, low string pad, light brushed snare` |
| Tempo | `92 BPM` |
| Key or mode | `minor` |
| Role | `sitting under the action, never leading it` |

`Solo piano with a low string pad and a light brushed snare, 92 BPM, minor, sitting under the
action.` That string is the theme. Every scene that carries music carries those words and no
others.

### It cannot be continuous across separate generations

Two clips generated from the identical music clause come back as two different takes: the tempo
drifts differently, the phrase starts somewhere else, the mix is not the same. Played in sequence
you hear the music restart at every cut. No wording prevents this, because each generation
composes from nothing and has no access to the previous clip.

| how the piece is generated | what to do with the theme |
|---|---|
| One pass, the whole piece in a single generation | Put it in the prompt. It genuinely plays throughout, and this is one of the better reasons to generate a dialogue-free piece in one pass |
| Separate scenes, cut together afterwards | One post track across the joins. Each scene prompt asks for ambience and effects and `no music` |
| Separate scenes and the user wants generated music anyway | Identical instruments, tempo and key in every scene. Vary only the arrangement. Say once that the joins will be audible |

Ambience and effects are per scene in every one of those cases. It is only the music that has the
continuity problem, so a scene under a post track still describes its own room tone and its own
footsteps in the prompt.

### Variations, absence and reprise

- **A variation keeps the instrument list and removes from it.** `Same theme, piano alone` is a
  variation. A different instrument list is a different piece of music, and two pieces of music in
  one short film reads as a mistake.
- **Ask for absence.** The theme dropping out is the strongest single thing music does. If one
  scene is the turn, take the music out of that scene and let it return.
- **A reprise is the theme thinner and slower**, not rewritten. Same instruments, fewer of them,
  a lower tempo if the model takes one.

### Fragments

- `AUDIO: solo piano with a low string pad and a light brushed snare, 92 BPM, minor, sitting under the action. Room tone of a small kitchen underneath.`
- `AUDIO: same theme, piano alone, 92 BPM, minor. No pad, no percussion.`
- `AUDIO: no music in this scene. Room tone and the sound of the door only.`
- `AUDIO: ambience and effects only, no music. The score is being laid over afterwards.`

The last of those is the one to use across a cut-together sequence, and it is worth saying in the
prompt rather than just omitting music, because a model asked for nothing will supply something.

## Speech

The decision with the most consequence, because it changes what you can fix later.

| | |
|---|---|
| Generated with the picture | Lip sync exists but drifts. The delivery is whatever the model chose. Changing a word means regenerating the shot |
| Recorded and laid over | Full control of the performance, and the picture can be regenerated without touching the line. Ask for a clip with no speech and no lip sync |

Prefer laid over whenever the words matter, which is nearly always in commercial work. It also
keeps the shot splittable, since the picture no longer has to run for exactly as long as the line.

**Non-verbal sound is different, and generate it with the picture.** A sigh, a gasp, a laugh, a
hum, an animal noise. None of these needs frame-accurate lip sync, all of them make a clip feel
inhabited, and asking for them is cheap. Say roughly when it happens.

## Silence

Ask for it explicitly. It is a legitimate choice and it will not happen by itself.

- `No audio, silent clip.`
- `No music at all, only the room and the mechanism.`
- `Characters do not speak and do not lip sync.`
- `Ambient sound and effects only, no voice, no dialogue, no narration.`

The third of those matters more than it looks: a face in shot on an audio-capable model will
start talking if nothing says otherwise, and a talking face you did not ask for is unusable even
with the sound off, because the mouth is moving.

## Vocabulary

**Instruments.** percussion, bells, ukulele, xylophone, piano, drums, bass, marimba, strings,
synth, guitar, choir, handclaps, pads, flute, harp, kalimba

**Texture and bed.** low sustained drone, ambient pad, minimal electronic ambience, room tone,
soft mechanical clicks, a soft whisper of falling sand

**Constraints.** no vocals, no voice, no dialogue, no narration, diegetic only, ambient SFX or
music only, no lip sync, silent

Some APIs expose the choice as a parameter rather than as prompt text, `generate_audio` or a
sound on and off toggle. Where one exists, set the parameter **and** write the line: the
parameter decides whether there is a track, and the line decides what is on it.

## Examples

- `Minimal deep electronic ambience with soft mechanical clicks.`
- `Warm ukulele and marimba, light percussion, no vocals.`
- `No music at all, only the room and the mechanism.`
- `AUDIO: ambient SFX and effects only, no voice, dialogue or narration.`
- `AUDIO: low sustained drone and a soft whisper of falling sand, no voice.`
- `Keep clip audio diegetic only. Characters never speak or lip-sync.`
- `Room tone of a small kitchen, a fridge hum, and a latch clicking as the door closes.`
- `A single soft laugh about two seconds in, no other voice.`
- `No audio, silent clip. The sound is being cut separately.`

## What fails

| symptom | cause |
|---|---|
| The music restarts at every cut | Per-clip generated music, which cannot be continuous. Use a post track |
| Each scene has different music | The theme clause was paraphrased between scenes, or never settled |
| The score fights a second bed underneath it | A post track laid over clips that were allowed to generate their own music. Say `no music` in the prompts |
| The audio was ignored entirely | The clause was delivered beside the prompt instead of inside it, or the model has no audio track |
| Stock music appeared over the clip | No audio line. The model filled the gap |
| A narrator started explaining the shot | Speech not ruled out. Say no voice, no narration |
| A character's mouth moves and nothing was written for them | Lip sync not ruled out. Say they do not speak |
| The room sounds wrong | Effects written, ambience left out |
| The music is generic | A genre was named instead of instruments |
| The line does not fit the mouth | Speech generated with the picture. Lay it over instead |
| The audio clauses seem to have been ignored | The model produces no audio track. Check before writing them |
