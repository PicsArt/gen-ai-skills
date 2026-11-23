# Dark tech explainer

A near-black explainer where one thing at a time glows: a faint dot field, a drifting band of light, a small capsule
at the top, captions in their own band at the bottom, a rail of step capsules along which one amber highlight
walks, and a single hero shape that draws on and glows. Quieter than a sci-fi HUD, closer to a product keynote.

## Palette

Canvas `#07080b`; dot field `#c9d4e6` at 30 % on a 48 px pitch; greys `#7c818c`; white `#f2f4f8`. **The hero colour
is one amber `#ffb020` that marks the current focus only**; nothing else is amber. No purple, no orange.

## The medium

- **The dot field:** a grid of small dots, 48 px apart, built from nested repeaters, with a faint light band
  drifting slowly through it and a soft fog along the bottom edge.
- **The HUD capsule:** top centre, a thin outline capsule holding a section number and title in a mono face
  (JetBrains Mono 600), small and capitalised.
- **Captions:** in a reserved band at the bottom (Gilroy Bold about 30), centred; nothing else enters that band.
- **The rail:** a row of step capsules joined by hairlines; the current step's capsule is outlined in amber and a
  small amber pip travels to the next one.
- **The display word:** one large word in a wide display face (Space Racer) for the big idea.
- **The hero:** one shape per shot (a lens, a node, a cube), line art in white, which glows: the same shape
  duplicated with a `gaussian_blur` and an `add` blend. The glow fades out before the shape does.
- **Every element earns a job.** A few secondary elements and fewer labels; one that does nothing for the shot
  comes out. The background is the dot field and nothing else, no scattered small icons.
- **The hero is big:** at least a third of the frame's height, on screen by the first or second beat. A subject that
  is small by nature (a rail, a table, a timeline) is carried by a large word or number, or by its lit current item
  grown to hero size; a thin rail alone leaves most of the frame empty.
- **Light follows the hero:** only the hero and the current focus glow; capsules, labels and captions never do.

## Motion habits

- **Entrances are soft:** 0.2 to 0.33 s, a fade and a small rise; list items stagger by about 0.07 s.
- **Line art draws on from its root** (`trim`), never fades in whole.
- **The amber focus walks along the rail** with the travelling pip, one step per beat of the narration.
- **Rare effects, a per-film budget:**
  - a glitch (a red and cyan split for about 0.4 s) on a single key word in each film section;
  - a light sweep only on the big idea, clipped to the hero's own shape (a gradient inside the shape); a free bar
    crossing the hero reads as a stick;
  - at most one camera move per shot, and the capsule and captions sit outside the moving shot so they never
    jump at a cut.
- **Leaving and holding:** everything on screen reaches zero before a hard cut, the emphasis going out first. After
  the last element lands, hold for a beat and a half before anything leaves, and make no camera move in that last
  beat.
- **Show/hide keys sit one frame apart** (`1/fps` at least): keys 0.001 s apart land on the same frame and blend
  every window together. This covers the capsule, captions, glow and the rail's pips.

## Type

Mono for the capsule and labels, a bold sans for captions, a wide display face for the one big word. Three faces
at most.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. One hero, glowing; the glow fades before the shape.
2. Amber marks only the current focus.
3. Captions sit in their own band and nothing else enters it.
4. A few secondary elements, fewer labels, and a hero at least a third of the frame high.
5. The capsule and captions do not move with the camera.

## Build with the tools

Build the dot field as nested repeaters on a black background, the capsule, rail and captions as plain
layers outside any camera group, the hero as a shape group with its blurred `add` copy. Key the entrances and the
pip; draw lines with `trim`. Preview the first beat, the rail and the big word, then a contact sheet.

## Do / don't

- **Do** keep amber for the focus, the rest in greys and white.
- **Do** spend a rare effect once per section, not per shot.
- **Don't** reuse another product's palette or its icon set; the palette here is our own.
- **Don't** put captions inside the moving shot, or let a bar cross the hero.

## Originality guard

Invent your own subject, wording and icons. Do not copy a company's keynote graphics, a game's interface or a
named explainer series' look. The dark field, one accent, glowing hero and rail are generic conventions.

## Proven on

The search-ranking film: a glowing lens that asks one question, then a three-capsule rail (crawl, index, rank) with
an amber pip walking it while the current step shows as a big lit word, ending on the display word "RANK" (7 s,
1280×720, checked frame by frame).
