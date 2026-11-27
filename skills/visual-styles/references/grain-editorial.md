# Grain editorial

A quiet painted-page explainer: flat gouache colour with no black outlines, paper grain over everything, calm
deadpan people with side-glancing eyes, and one hand-lettered word that carries the idea of the beat.

## Palette

Wall `#a6cdd8`; board `#3a3d40` filling most of the frame, in a bright mustard frame `#eaa92a`; chalk
`#f4f1e8`. Cast colours: mustard, coral red `#e0573f`, teal `#2f8f7f`, cream, warm browns. **The hero colour is
coral**, kept for one accent (a headband, a ribbon, the mark the beat is about). No pure black, no pure white.

## The medium

- **No outlines.** Colour meets colour; detail is thin same-hue darker lines inside a shape (curl lines in hair,
  cheek lines, a nose line), never a dark contour round it.
- **Paper grain over the whole page:** build the scene inside a `scene` asset and put `analog_film_finish`
  (`grain` about 0.08, `paper` about 0.12, `dust` 0: a faint tooth, never a visible noise; colours stay clean and bright) on its one `scene_ref`. The grain then sits inside every fill,
  the people included.
- **Dry-brush edges** on large set pieces: a `brush` on the piece's fill, `{"tip": "bristle", "size": 10,
  "angle": 0, "coverage": 0.97, "streaks": 0.45}`. Drag marks run along the frame like a loaded dry brush;
  `coverage` 1 keeps the edge solid and `streaks` sets how much bristle shows. Never dissolve a piece: the
  speckle reads as noise, not paint.
- **Brush lettering:** a tall hand font in solid chalk white with a 0.7 px blur only. Keep the chalk `brush` off a
  thin hand font: at any `coverage` that shows texture it cuts dark slashes across the letters and dashes the
  underline, and at 1 it shows nothing; dotted letters read as a font effect too. It writes itself left to right
  through a `mask.clip` rect anchored at its left edge, scale x `0 → 1` (`linear`) over about 1.8 s.
- **Chalk smear on the board:** a chalk `brush` on the board's fill, `{"tip": "chalk", "size": 40, "angle": -24,
  "streaks": 0.14}`, a rubbed-in slanted smear.

## Painted texture

For a page that must read as brushwork, not just grain, add these, all in the `scene` asset (no generated pictures; the brush lives on the fills and text above):

- **Ink lines that swell.** Every thin detail line (lids, brows, nose, cheek, glasses, curl strokes) is a stroke with a
  `taper` (`startLength`/`endLength` about 0.28, `startWidth` 0.35, `endWidth` 0.1) plus a `wave` (`units` `cycles`,
  about 1.5 cycles, `amount` 0.5, a different `phase` per line), width 3-5 px. On a short line keep the taper
  lengths under 0.3 or it vanishes; a closed ring takes the wave only (a taper pinches it at the seam).
  Noise-driven pressure is not available: `wave` is periodic, so vary `phase` and `cycles` per line.
- **A line boil:** `turbulent_displace` (`amount` 1.1-1.6, `size` 26, `complexity` 2) on every painted layer, its
  `evolution` held to 8 fps with `return math.floor(time*8)*97+<a different number per layer>`. The edges shiver
  like repainted gouache; keep `amount` under 2, or the shapes look torn.
- **Chalk dust:** one shape layer of about 45 slanted white ellipses (as smooth paths), fill opacity 0.08-0.2,
  `gaussian_blur` 5, above the board and its smear.

Not available yet: a brush that follows a moving or deforming shape (a `brush` is static, so a swaying head slides
under its bristles), and real pressure-from-noise on a line.

## Characters

One part sheet through the SVG part-sheet flow (`character-rigging`), built as the three-quarter view. Fill the
description slot with:

> {subject} drawn in a hand-painted editorial picture-book style: about 7 heads tall, long neck, long slim limbs of
> even width, narrow sloping shoulders, small hands with thin fingers, simple flat shoes; a calm deadpan face:
> almond eyes drawn as a white eye shape with a small dark pupil resting near one corner, a thin dark upper lid
> line over each eye, thin arched dark eyebrows, a long simple nose drawn as one thin darker-skin line, small lips,
> two short thin darker-skin cheek lines; {hair}; {outfit}; NO black outlines anywhere: every shape is flat colour
> meeting flat colour, with only thin same-hue darker detail lines inside shapes; flat shading: at most ONE slightly
> darker flat shade shape of the same hue per part, away from a light at the upper left (no highlights, no
> gradients); {skin}; a muted palette of mustard, coral red, teal, cream and warm browns, quiet and gentle like a
> hand-painted gouache illustration

- Frame people large and cut them at the thigh or waist, like a page: feet below the frame.
- They act little: a point, `breath` and a slow `headTilt` sway (about 0.06), nothing else.
  **Leave out `headTurn`, `lookLeft`/`lookRight`, `blink` and `happy`:** a cut-out rig turns and blinks badly, and
  the style does not need them. The side glance is drawn into the sheet and held for the whole shot; the held
  deadpan face is the joke. Never write a line that has the character blinking, glancing about or turning her head.
- **The arm bends.** Point with the rig's two-bone arm, a soft elbow at a natural reach (`UpperArmRaise` about
  0.55, `LowerArmSwing` about 0.4, the pointing hand `HandPoint` 1), not a straight rod. Never stretch the arm to
  reach: move the word closer to the person.
- **The character is swappable.** The recipe fixes the look (flat gouache, no outlines, deadpan glance, cut at the
  thigh), not one person: a new part sheet from the prompt above replaces her with the same acting and the same
  controls.

## Motion habits

- One idea per beat: the word writes itself, an underline draws under it (`trim`), then one small mark (a tick, a
  circle) lands.
- The person points before the word appears, so the eye travels from the face to the hand to the word.
- **The hand stops short of the word.** Bring it in from below and to the left, the fingertip about a finger
  width from the first letter, and start the underline clear of the hand, so no letter and no part of the line is
  covered.
- Holds are long and calm; nothing pops or overshoots.

## Type

A hand-lettered face (`just-another-hand-regular-8b981e4f2e80`) at about 230 px for the word of the beat, chalk
white on the board.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. No black outline anywhere; detail lines are a darker tone of the shape's own colour.
2. Paper grain is visible inside the fills, on the people too, at 1x.
3. One hand-lettered word per beat, and the person's point or glance leads to it.
4. Coral appears on one accent only.
5. The people are cut by the frame edge, never shown small and whole in the middle.
6. The pointing hand stops short of the word; no letter is covered, and the word reads whole at every moment
   after it has been written. The elbow is softly bent.

## Build with the tools

Wall, board and frame are shape layers; the word is a text layer with a mask clip; the person is a `scene_ref` of a
part-sheet rig; all of it sits in one `scene` asset whose `scene_ref` carries the grain look.

## Do / don't

- **Do** keep the camera still and the acting small.
- **Don't** add outlines, glows, gradients, bouncy pops or a second hot colour.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - **Finish.** the tooth, brush marks and chalk dust all live inside the one `scene` asset; the camera is still, so nothing pans; the grain is added once on the one `scene_ref`, held steady (render two frames and compare the grain); the painted chalk word takes the tooth as paint on the board.

## Originality guard

Invent the people, the words and the setting. Never imitate a known channel's characters, title cards or logo,
and never name one in a prompt. Flat painted colour, paper grain, deadpan side glances and a lettered word are the
style.

## Proven on

A chalkboard beat (8 s, 16:9): a teacher points with a bent arm, "Patience" writes itself and is underlined,
and a tick lands. The texture method above was proven on a 6 s 16:9 chalkboard page: a teacher points at
"Patience", a second figure holds a rosette; against the flat version the paper, brush ink, dry-brush word and
chalk dust read as paint.
