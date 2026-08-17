# Extrapolation

How to render something the references never showed.

This is the file that makes a style guide worth having. Describing what is in the references
is the easy half; nearly everything generated later will be something else. A guide built from
twelve frames of a cartoon will be asked for a pig, a bus stop and a rainstorm, none of which
appear in the twelve frames.

## The principle

**Do not extrapolate from the instance. Extrapolate from the construction rule.**

Wrong: the tiger is orange with black stripes, so the pig is orange with black stripes.

Right: what the references show about how this style builds *any four-legged animal* is a head
at one third of body height, eyes with a single highlight and no sclera at rest, limbs as soft
tubes without visible joints, and fur implied by three or four marks at the silhouette edge
only. Apply that to a pig and you get a pig that belongs in the same world.

So for every subject class, the guide records two things: what the examples look like, and the
rules the examples reveal. The second is what generalises.

## Deriving the rules

For each class, ask what the style does about these, and write the answer as an instruction:

| question | why it generalises |
|---|---|
| What proportion is exaggerated, and by how much | Applies to every creature, not just the one drawn |
| How is the eye constructed | The strongest style tell, and identical across characters in most productions |
| Is there an outline, what colour, and does its weight vary | Applies to everything in frame |
| How is surface texture handled: drawn, implied, or omitted | Fur, feathers, scales, bark, fabric and hair all follow one rule |
| Where does detail concentrate | Usually faces and silhouettes. Tells you what to leave bare |
| How many shading steps | Two-tone versus soft gradient decides how a new object reads |
| How is contact with the ground shown | Shadow, or nothing. Very visible when wrong |

## Worked chains

These are the derivations the guide should support. Each moves from something observed to
something absent.

**Tiger to pig.** Observed: oversized head, no sclera, tube limbs, fur at the silhouette only,
two-tone shading, dark brown outline. Derived: a pig with the same head ratio and eye
construction, a snout simplified to one shape with two dots, no fur marks because a pig is
smooth, and the same outline and shading. Palette from the palette rule, not from the tiger.

**Tree to grass.** Observed: the tree is a trunk plus two or three leaf masses, each mass a
flat fill with five or six notches cut into the silhouette, no individual leaves. Derived:
grass is a flat fill with notches at the top edge only, at the same notch scale. Not blades.
The rule is "detail lives at the silhouette", and grass obeys it the same way.

**One character to a crowd.** Observed: the four named characters carry facial detail and
fold-shaded clothing. Background figures in two frames are flat silhouettes with no faces.
Derived: a crowd is silhouettes at one flat value, and the moment a figure needs a face it
becomes a foreground character and takes the full treatment. **The rule is the threshold**,
and it is more useful than either example.

**Day to night.** Observed: all references are warm daylight, shadows the same hue darkened
with a slight blue shift. Derived: night keeps the hue-shift rule, moves the key to a cool
practical source, and holds the same number of shading steps. Say clearly that this is
inferred from zero night references and should be tested.

## Recording confidence

Every derived rule states what it rests on. Use these words consistently:

| label | meaning |
|---|---|
| **Established** | Consistent across most references. Trust it |
| **Provisional** | One or two examples. Likely right, test it |
| **Inferred** | No example. Derived from a related class. Test before committing |
| **Unknown** | No basis. Say so and ask, or let the generator decide and check |

**Unknown is a legitimate answer and the most useful one when it is true.** A guide that
answers everything confidently is a guide that is wrong in places nobody can find. If the
references contain no water at all, `water: unknown` sends the user to add a reference. A
confident invented rule sends them to forty bad renders.

## The interaction with prompt writing

When another skill, typically `video-prompt-engineer`, hits an element the guide does not
cover:

1. Find the nearest covered class. A pig is nearest to the tiger, not to the tree.
2. Apply that class's construction rules.
3. Take colour from the palette rule, never by copying the neighbour's colour.
4. Mark the clause as inferred in what it reports back, so the user knows which part of the
   prompt is a guess.
5. If nothing is near enough, say so and ask, rather than reaching for a generic default. A
   generic default is exactly the thing the style guide exists to prevent.

## What not to extrapolate

- **Identity.** A style guide generalises a look, not a character. Deriving "a tiger in this
  style" from a specific copyrighted tiger is style transfer; reproducing that tiger is not
  yours to do. Keep the construction rules, drop the identity.
- **Anything the audience rules forbid.** `audience.md` outranks every derivation here. If the
  guide is for young children, a derivation that produces a weapon or an injury stops, even
  when the construction rules would happily render it.
- **Aspects the medium does not have.** Do not derive a focal length for a flat vector style
  because a photographic reference elsewhere had one.
