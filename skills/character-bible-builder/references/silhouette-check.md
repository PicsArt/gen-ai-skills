# The silhouette distinction check

Check the cast against itself before writing a single prompt. 2 characters who read the same in
silhouette will be confused by a generator, and the bible is where that gets caught.

## Why the check exists

A generator has no cast list. It has the text of 1 prompt. If 2 characters reduce to the same
shape, then in any shot where the shape is most of the information it will produce whichever it
prefers, or a blend of the 2. The shots where the shape is most of the information are the wide
shots, the night interiors, the backlit ones and every shot with 2 people in frame, which is to
say the shots that carry the story.

**Colour does not settle it.** Colour is the first thing lost to low light, backlight, distance,
weather and any grade the style guide imposes. A cast distinguished only by coat colour is a cast
that works in the reference sheets and fails in the film. So the test is deliberately harsh:
reduce every character to a **flat black shape** and see whether you can still name them.

## The axes

Fill this in for the whole cast before comparing anything. Values are coarse on purpose. A
scale that is too fine will tell you that 2 characters differ when a viewer cannot see it.

| axis | values |
|---|---|
| Height | short, medium, tall, relative to the cast rather than absolute |
| Mass | slight, medium, heavy |
| Shoulder line | narrow, square, sloped, raised |
| Head shape in outline | round, oval, square, long |
| Hair mass | none, close, medium, large, and where the volume sits |
| Hair outline | smooth, ragged, spiked, tied, braided, covered |
| Headwear | none, cap, hat with a brim, hood, scarf, helmet |
| Garment length | cropped, waist, hip, thigh, knee, ankle |
| Garment volume | close fitting, loose, voluminous |
| Leg line | trousers straight, trousers wide, skirt, bare, boots to the knee |
| Attached prop | none, and otherwise anything that changes the outline: a bag on a strap, a rifle, a cane, a violin case |
| Gait | even, heavy, quick, limping, stooped |

Height, mass, hair mass and garment silhouette are the 4 that do the most work. The rest are
useful for breaking a tie.

## The pass rule

For every pair in the cast:

1. Compare the 4 primary axes: height, mass, hair mass, garment silhouette, where garment
   silhouette is length and volume together.
2. **At least 2 of the 4 must differ.** 1 difference is not enough, because 1 difference is
   what a generator loses when the character sits down, turns away or stands in the rain.
3. **At least 1 difference must be visible in a flat black shape.** Skin tone, eye colour, hair
   colour and wardrobe colour do not count towards this.

| result | verdict | what to do |
|---|---|---|
| 3 or 4 primary axes differ | distinct | Nothing. Record it |
| 2 differ, at least 1 in silhouette | distinct | Record which 2, so a later wardrobe change does not remove them both |
| 2 differ, both colour only | too close | Fix it |
| 1 differs, or 0 | too close | Fix it |
| 2 differ but only in a scene specific layer, such as a coat 1 of them takes off | close | Fix it, or state the shots where they will be confused |

Do the check on every pair, not only on the pairs you expect to collide. Principals get checked
against extras too: an extra in the hero's coat in a wide shot is exactly the failure this
prevents.

## Fixes that work

Change 1 primary axis on the **smaller** part. The principal keeps their look. A secondary
character absorbs the change, and a background character absorbs it without discussion.

In rough order of how well they hold up:

| fix | why it holds |
|---|---|
| Change hair mass or hair outline | Survives distance, backlight and monochrome. The strongest single fix in character work |
| Add or remove headwear | Changes the head outline completely, and a generator repeats it reliably |
| Change garment length by 2 steps | Knee to waist is unmistakable at any distance. 1 step is not enough |
| Change garment volume | A voluminous coat and a close fitting jacket are 2 different shapes |
| Add an attached prop that breaks the outline | A bag on a long strap, a cane, an instrument case. Also gives the character something to do |
| Change the leg line | Wide trousers against boots to the knee reads immediately |
| Change posture | A stoop or a raised shoulder line reads even in a flat shape, and it costs nothing |
| Change height band | Effective, and expensive: if the script says they are the same height, this is not available |

Fixes that do not work, and should not be offered:

- **A different colour.** The whole point of the test is that colour is the first casualty.
- **A different face.** Faces are 8 pixels wide in a wide shot, and a generator resolves them
  last.
- **An accessory smaller than a hand.** Glasses, a ring, a badge, an earring. Real to a reader,
  absent in the render.
- **A name.** The generator does not know the names.
- **1 more adjective in the description.** If 2 characters are the same shape, a longer
  description of the same shape does not separate them.

## Reporting it

Present the table in the stage 3 stop, before any prompt is written, because a fix changes the
description and therefore every prompt built from it.

For each pair not marked distinct, give the verdict, the reason, the proposed fix, and which
character absorbs it. Then let the user overrule you. A user who wants 2 characters to look
alike because the story needs it is entitled to that, and in that case the correct response is
to say which shots will need a manual pick and record it under `## Open questions` in both
character files.

Write the final table into `<bible>/CHARACTERS.md` under `## Distinction check` and into
`<bible>/manifest.json` under `distinctionCheck`, and put each character's surviving differences
into `## Distinction` in their own `<bible>/<character-id>.md`.

That last one matters more than it looks. When somebody adds a character to the cast in 3
months, `## Distinction` is what tells them which shapes are already taken.
