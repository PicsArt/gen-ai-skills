# Inheritance

What every chunk carries from the scene it came from. This is the reason a split is safe: 4
chunks that each know the whole scene will cut together, and 4 chunks that only know their own
action will not.

## The rule

When a scene is split, **each chunk inherits every attribute of the original scene**, written out
in full inside its own file. No chunk file refers to another chunk file for a fact it needs.

The test is simple. Open 1 chunk file at random, paste its prompt, and generate. If the result
is in the wrong room, the wrong clothes or the wrong light, the inheritance was incomplete.

## What is inherited

| attribute | where it comes from | what happens when it is dropped |
|---|---|---|
| Setting | The scene heading, or the prose | The model puts the subject somewhere else, and undescribed backgrounds fill with objects nobody asked for |
| Characters present | The scene | A character appears or vanishes across the join |
| Wardrobe | The script, the `Wardrobe` heading in `<bible>/<character-id>.md`, or asked | Clothing changes between chunks. This is the most visible failure of the set |
| Time of day | The scene heading | The sun moves between 2 clips that are 1 second apart |
| Lighting | `<guide>/lighting.md`, or the scene | The key light swaps sides |
| Style and medium | `<guide>/rendering.md` | The clips look like they came from different productions |
| Palette and grade | `<guide>/palette.md` | Colour drifts, which is the hardest thing to fix afterwards |
| Camera treatment | `<guide>/camera.md`, or the scene | Shot size and lens character wander |
| Mood | The scene | Small decisions the model makes go different ways per chunk |
| Aspect ratio | Asked in stage 0 | The chunks cannot be edited into 1 timeline |
| Audio | The scene, or asked. Nothing at all when the model produces no audio track | The bed restarts or changes character at every join |
| Theme music | Asked in stage 0, held in `<shots>/shared.md` | Every chunk invents its own music, so the piece has 9 scores instead of 1. See the note below |
| Exclusions | `<guide>/negatives.md` plus the usual artefacts | Text, watermarks and extra limbs arrive in whichever chunk forgot the line |
| Character descriptions | `<bible>/CHARACTERS.md` or `<guide>/characters.md` | The face is not the same face |
| Audience limits | `<guide>/audience.md` | A chunk ships something the user cannot use, and 1 bad chunk fails the set |

Where a style guide and a character bible disagree, `<bible>/CHARACTERS.md` wins on the
character and `<guide>/` wins on everything else. Where `<guide>/audience.md` conflicts with
anything at all, it wins.

**Theme music is the 1 attribute that inheritance cannot save.** Every other row on that table
reproduces from identical words: paste the same style string and you get the same style. Music does
not, because each chunk composes its own take, so identical clauses still give a different tempo
drift, a different point in the phrase and a different mix. The music restarts at every join and no
copying discipline prevents it.

So for a chunked set, carry the theme as `no music` in every chunk and lay 1 track over the cut
afterwards. Keep the theme spec in `<shots>/shared.md` regardless, because that string is what the
composer or the music generator gets. Only a `000-single-pass.md` set can generate a theme that
plays throughout, because there is only 1 generation.

## Byte identical, not equivalent

The shared attributes live once in `<shots>/shared.md` and are copied from there into every chunk
file without edits.

That means:

- No rewording, even when a chunk would read better with a different word.
- No shortening, even when a line feels long for a 5 second chunk.
- No reordering inside a line.
- No fixing a typo in 1 chunk only. Fix it in `<shots>/shared.md` and recopy it everywhere.

A paraphrase is a different prompt. `Warm afternoon light from a low window` and
`low warm afternoon light through a window` produce visibly different light, and the difference
lands exactly at the cut where a viewer is already looking for one.

When a shared line has to change, change `<shots>/shared.md` and then recopy it into every chunk
file, including the ones already written and including any that were already generated. Note in
your report which chunks now need regenerating, because that is a cost the user should know
about.

## What may differ per chunk

The whole point of a chunk is that something in it is specific. These are the fields that are
allowed to vary, and nothing else is:

| field | how it varies |
|---|---|
| Duration | 5 or 10, per the estimate |
| Subject motion | 1 action per chunk, and it is the action of this chunk only |
| Camera movement | 1 move per chunk. A different move in the next chunk is fine, a second move in this one is not |
| Shot size and angle | May change between chunks when the script implies a new shot |
| Dialogue | The line or part of a line this chunk carries |
| Continuity in and out | Specific to the boundary by definition |
| Pacing | Where the beat falls inside this chunk |

Lighting sits on the line between the 2 lists. It is inherited within a scene, and it may change
between scenes. If a scene contains a light change, that change is a chunk boundary, and both
sides state their own lighting in full.

## Handling an attribute the script does not give you

3 options, in order:

1. **Take it from the guide or the bible.** Verbatim. This is why they exist.
2. **Ask.** 1 question covering all the missing attributes across all the scenes is cheaper than
   1 per scene.
3. **Infer it, and mark it.** Only in auto mode, or when the user has said to fill gaps. Record
   the inference in `<shots>/manifest.json` under open questions and list it in your report, so
   the wrong guess is caught before the whole set is generated from it.

Never fill a gap silently. An invented wardrobe copied byte identically into 14 chunk files is
14 clips to regenerate.
