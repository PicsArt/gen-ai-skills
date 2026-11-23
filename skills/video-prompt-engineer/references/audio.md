# Audio bed

A video prompt can carry its own soundtrack. Describe the desired sound and verify that the selected model supports audio.

## Audio bed

The sound that plays under the picture. Naming instruments, atmosphere and any speech can make the intent clearer; adherence remains model-dependent.

**Vocabulary.** percussion, bells, ukulele, xylophone, piano, drums, bass, marimba, strings, synth, guitar, choir, handclaps, pads, flute, synthesizer, synthetic, harp, synthase, kalimba, ambient SFX or music only, no voice, dialogue, or narration, Low sustained drone, a soft whisper of falling sand

**Examples.**

- `Minimal deep electronic ambience with soft mechanical clicks.`
- `Warm ukulele and marimba, light percussion, no vocals.`
- `No music at all, only the room and the mechanism.`
- `AUDIO: {ambient SFX or music only, NO voice, dialogue, or narration}.`
- `AUDIO: Low sustained drone and a soft whisper of falling sand, no voice.`
- `Keep clip audio diegetic only. Characters never speak or lip-sync.`

Configure audio only through documented fields for the selected endpoint; do not put guessed API flags into prompt prose. Keep separate voiceover, lip-sync and continuous-score work outside the generation prompt when the model cannot supply it.
