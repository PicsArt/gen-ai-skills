# Writing a music brief

The generator returns a track for any prompt, so a weak prompt fails quietly: the track is wrong
for the video, and that is only heard under the voice. Fill all five slots, then say what the bed
is for.

## Reading the slots off the video

- **Mood and genre come from what is said.** A story about selling a company can be triumphant or
  exhausted; the words say which. Score the tone, not the topic: a big win told wearily wants
  weary music.
- **Tempo and density come from the picture.** Animated, gesturing, quick cuts: a clearer beat and
  more motion. Still, confessional, long takes: sparse, ambient, little percussion.
- **How far forward the bed sits comes from where it plays.** A vertical short for social feeds
  tolerates a present groove; a talk or a work update wants something nearly subliminal.

## Briefs by kind of video

**A personal story** (confessional, still, slow):
> Warm lo-fi hip-hop, instrumental. Mellow Rhodes piano, upright bass, soft vinyl crackle, brushed
> drums, around 90 BPM, unhurried. Intimate and reflective. Purely instrumental throughout. Sits
> quietly under a speaking voice without competing with it.

**A founder or expert insight** (direct, confident, moderate energy):
> Clean minimal electronic, instrumental. Soft analog pads, a muted plucked arpeggio, a restrained
> kick, around 105 BPM. Focused and quietly confident, not triumphant. Purely instrumental
> throughout. Leaves the midrange clear for a speaking voice.

**Banter or comedy** (animated, quick, laughter):
> Bright playful indie-pop, instrumental. Bouncy muted guitar, hand claps, warm bass, light
> tambourine, around 118 BPM. Cheerful and mischievous. Purely instrumental throughout. Has fun
> under the dialogue without stepping on the punchlines.

**A tense story** (dramatic, building):
> Minimal cinematic, instrumental. Low sustained strings, sparse piano, a soft pulsing sub-bass, a
> slow build, around 80 BPM. Quietly ominous. Purely instrumental throughout. Very sparse in the
> midrange, so a voice cuts through.

**Advice or motivation** (energetic, encouraging):
> Uplifting acoustic-electronic, instrumental. Fingerpicked guitar, a warm pad, soft claps, a light
> kick, around 110 BPM. Optimistic without being sweet. Purely instrumental throughout. Supports a
> speaking voice rather than swelling over it.

## What ruins a brief

- **"Background music."** No genre, instruments or mood: the model picks stock pop.
- **A song or an artist by name.** The model will not reproduce it, and an odd pastiche comes
  back. Describe the qualities instead: breathy, sparse, minor-key.
- **The brief in the lyrics field.** Lyrics are sung, so the brief comes back as a voice reading it.
- **No instrumental line, or only a negation.** Without "purely instrumental" a bed may come back
  sung, the most common reason it is unusable under speech; and a bare "no vocals" can be sung too.
- **Contradictions.** "Energetic but calm": pick one, and let the mix set the level.
- **Length.** Past about 80 words, detail dilutes the brief rather than sharpening it.

## Applying a steer

Apply the steer to the slots it touches and redraft the whole brief; never append it.

- "More upbeat": a higher tempo, more rhythm, brighter mood words; keep the genre if it can carry it.
- "Less busy": fewer instruments, less percussion, a lower tempo.
- "More cinematic": strings and pads over drums, slower, more sustain, sparser.

Keep the new brief as short as the old one, so what changed reads plainly against it.
