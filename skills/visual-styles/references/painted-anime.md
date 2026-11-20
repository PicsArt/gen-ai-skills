# Painted anime

A hand-painted anime film background with part-sheet characters walking through it: one painted plate (or
painted depth bands), cel-shaded characters from the SVG part-sheet flow, and a soft finishing pass.

Shared with [cel anime](cel-anime.md): the [palette habits](cel-anime.md#palette), the
[motion habits](cel-anime.md#motion-habits), [motion on threes](cel-anime.md#motion-on-threes) with its one-frame
smear, the [impact frame](cel-anime.md#impact-frame), the [expressions note](cel-anime.md#expressions), the type,
the frame checklist and the originality guard.

**Every background starts from the SVG band layout** (step 1 of *Painted place with depth*). The single-plate
variant below is that layout painted over once (steps 1 and 2) and placed as one media layer, never a text-to-image
background: a place the agent generates without a layout has no bands, no floor line and nothing to pass behind.

## Painted background plate

A painted place can be one plate: the SVG band layout painted over once (steps 1 and 2 of *Painted place with
depth*), placed as a media layer scaled to about 1.6 so a held
pan and tilt never shows an edge (hold on `step` keys, move on `ease_in_out` / `ease_out`). Put the actors in an
empty `world` layer that takes the same moves, and a near layer (blurred grass, `gaussian_blur` 4) on the same
keys but about 1.6 times as far, so it slides faster than the plate. Keep the camera zoom to one slow push.

## Painted place with depth

A held pan over one painted plate reads flat once characters walk through it: nothing passes in front of them.
Paint the place in depth bands instead, and the near pieces slide past faster than the far ones.

**What runs on stage today.** Steps 1, 2 and 5 to 7 run on stage today: the layout and the paint-over through
`picsart_generate`, and the compose, the parallax and the walkers through the scene tools. Steps 3 and 4 (cut
the painting into band plates, fill what each band hides) wait for the queued `paintUrl` input on
`picsart_scene_build_place`. Until it lands, the stage route is the painted plate as one layer, plus a separate
foreground layer for the near pieces (step 7).

1. **Band layout (`picsart_generate`, SVG).** Ask an image model that outputs SVG (pick it with
   `picsart_model_choose`) for a 2D background layout with **exactly five top-level groups, back to front: `sky`, `far`, `mid`,
   `ground`, `front`**. Give each band a y range that overlaps the next one, and say "every band is drawn
   complete as if nothing covers it, extending under the band in front of it, and spans the full width". Put a
   `data-floor` y on `ground` where the feet go. Keep `front` sparse: one or two tall pieces (a lamp post, a
   platform pillar, a bench), nothing in the middle of the walk. Flat colours with hard cel shade shapes; plain
   path, rect, circle, ellipse and linearGradient only. The model draws it about 1.8 times as wide as it is high,
   which leaves room to pan.
2. **One paint-over (`picsart_generate`, PNG).** Rasterize the layout and give it to an image model that
   takes reference images, as `imageUrls[0]`, with a style reference painting as `imageUrls[1]` (16:9). The prompt has this shape:
   "Repaint IMAGE 1 as a hand-painted anime film background, in the painting style, brushwork and colour of
   IMAGE 2 [, but at dusk / on a summer afternoon]. Keep IMAGE 1's layout exactly: every shape stays at the same
   position and size, [list the shapes]. Do not move, add or remove any large shape and do not change the edges
   between [the floor and the front pieces]. Add painted detail only inside each shape: [textures, light spill].
   No people, no text." Listing the shapes by name is what holds the edges in place. Reuse one painting as the
   style reference for every place in a film, so the places share a hand.
3. **Cut into band plates (waits for `paintUrl`).** Each band's plate is the painting inside that band's layout
   shape. The painting drifts a few pixels from the layout at the edges, so grow each band's shape by about 3 px
   before cutting, or a thin line of the band behind shows along every edge.
4. **Fill what each band hides (waits for `paintUrl`).** A plate has holes where a nearer band covered it. Fill
   them with that band's own paint, one edit per covered band. A smear of neighbouring colour shows during the
   pan as a light strip beside the near piece (measured on the street and station films; see the limits below).
5. **Parallax.** One layer per band, each panning by its factor times the camera move, all on the same keys:
   `sky` 0.1, `far` 0.25 to 0.5, `mid` 0.5 to 0.6, `ground` 1, `front` 1.3. Parts of one building (upper and
   lower storeys of a shop row) take the same factor, or the building shears; the street used 0.5 for both
   `far` and `mid`. A pan of 40 to 50 px each way over 8 s is enough.
6. **Walkers planted on the floor.** Put the camera move on an empty `world` layer. Parent `ground` and an empty
   `cast` layer to it, then parent each walker to `cast`. A walk that travels on its own refuses a parented
   layer (`travel_needs_plain_layer`), so apply `walk_cycle` with `travel` `in_place` and let `cast` carry the
   walkers: move `cast` at the walk's pace, `stride × scale / stepDuration` stage px per second (the walker's
   scale times `cast`'s), so the feet don't slide. Walkers at different paces each need their own carrier.
   Scale `cast`, not the walkers. Set `cast`'s y so the feet land on the floor line: the
   `data-floor` y when the layout has it. The model often drops the attribute. Without it, read the top edge of
   the `ground` band where the path runs from the layout, and scale it to the plate.
   Each walker carries a soft contact shadow as a child layer at its anchor.
7. **Passing behind a front piece.** List the `front` band layer after the walkers. A walker then disappears
   behind the lamp post or the pillar and comes out the other side. On stage today the plate cannot be cut, so the
   near piece must not be painted into it. Paint the plate from a layout with an empty `front` band, then
   generate the near piece on its own (`background: "transparent"`, the same style reference). This route has not
   been proven on a film yet. The three walk-throughs below used cut bands.

```json
[
  { "id": "sky", "content": { "kind": "media", "assetId": "p_sky", "fit": "none" },
    "animations": { "position": { "keyframes": [
      { "time": 0, "value": [645, 360], "easing": "ease_in_out" }, { "time": 8, "value": [635, 360] }] } } },
  { "id": "far", "content": { "kind": "media", "assetId": "p_far", "fit": "none" },
    "animations": { "position": { "keyframes": [
      { "time": 0, "value": [652.5, 360], "easing": "ease_in_out" }, { "time": 8, "value": [627.5, 360] }] } } },
  { "id": "world", "content": { "kind": "empty" },
    "animations": { "position": { "keyframes": [
      { "time": 0, "value": [50, 0], "easing": "ease_in_out" }, { "time": 8, "value": [-50, 0] }] } } },
  { "id": "ground", "parentId": "world", "transform": { "position": [640, 360] },
    "content": { "kind": "media", "assetId": "p_ground", "fit": "none" } },
  { "id": "cast", "parentId": "world", "transform": { "position": [120, 217], "scale": [0.7, 0.7] },
    "content": { "kind": "empty" } },
  { "id": "front", "content": { "kind": "media", "assetId": "p_front", "fit": "none" },
    "animations": { "position": { "keyframes": [
      { "time": 0, "value": [705, 360], "easing": "ease_in_out" }, { "time": 8, "value": [575, 360] }] } } }
]
```

The walkers (each with `"parentId": "cast"`) go between `cast` and `front`. Run the [finishing pass](#finishing-pass) over a
`scene_ref` of the whole place.

**Measured limits.**

- The paint-over registers to the layout within a few pixels, never exactly. Grow every cut by about 3 px.
- Until each band's hidden area is filled from its own paint, a faint light strip shows beside a front piece
  while the camera moves. It is visible at 1x on the street lamp post and the station pillar. Keep camera moves
  small (under 50 px) and slow until the fill lands.
- A walker that should pass behind something must be in front of the band that holds it. A pillar painted into
  the `ground` plate can never cover anyone.

## Character note

A character hand-drawn as shape groups looks blocky against a painted plate: the joints have no shape and the
face proportions read as drawn. Make the character through the SVG part-sheet flow, then rig it as usual
(`character-rigging`): fill only the description slot of the frozen part-sheet template with the text below.
If there is no sheet, keep the background flat to match flat characters.

**The description.** Start from this text and fill `{subject}` (who it is, e.g. "slim girl violinist") and
`{outfit}`:

> {subject} drawn in Japanese TV-anime cel style: about 6.5 heads tall, long slim legs, narrow
> shoulders; large anime eyes (each eye a tall rounded shape under a thick dark upper lash line, a deep-blue iris
> lighter at the bottom, two small white highlight dots), a tiny nose drawn as one short line, small pointed chin;
> spiky dark-brown hair as one mass of 7 sharp pointed clumps with three pointed strands over the forehead; thin
> dark-brown outlines (never black) of even weight; {outfit}; cel shading: every part has flat base colour plus ONE
> hard-edged darker shadow shape of the same hue (no gradient, no soft edge) on the side away from a light at the
> upper left, and the hair has one pale highlight band

The proportions (6.5 heads, slim legs, narrow shoulders) suit a teen or an adult; adjust them for a child or a
mascot.

What carries the look: the height in heads, large eyes with a lash line and two highlight dots, a one-line nose,
hair as one mass of sharp clumps, thin dark-brown outlines, and the cel clause (one hard shadow per part, away
from the upper-left light, plus one hair highlight band). Leave the cel clause out and the parts come back flat.

- The cel shadows are painted on the parts, so they turn with the limbs; that is accepted for anime.
- Add a contact shadow under the feet (a flat dark ellipse on the plate, at the cel shade tone).
- When the plate's path recedes, walk the character along that path (position and scale together), not flat
  across the frame.

Other anime looks are other fills of the same slot, used only when the user's words ask for one: see
[painted anime looks](painted-anime-looks.md).

**A second character from the same text.** Change only the face, hair and outfit clauses, and keep the cel
clause and the proportions word for word. A girl variant (amber eyes with one lash flick at the outer corner,
side-swept bangs of 5 pointed locks, a high ponytail tied with a band) passed every sheet check on its first
generation. Name long hair as `hairBack` in the description itself ("the ponytail is hairBack"); the rig then
keeps it behind the torso and it swings with the walk. Give two walkers different `stepDuration` (0.42 and
0.47 s) so they never fall into step.

## Lo-fi loop

A painted place held still while small things repeat: a seamless loop to play under music. It is a scene in this
style, not a style of its own. Use it when the user's words ask for a "lo-fi", "chill" or "study" loop.

- **Pick the loop length first** (8 s) and give every motion a period that divides it: written as
  `math.sin(2*math.pi*n*time/L)` with a whole `n`, or as `(time/p) % 1` with `p` a divisor of `L`. Keys go back
  to their first value by `L`. The last frame then flows into the first.
- **The camera is locked** and nothing enters or leaves the frame. Reuse a painted plate (or the depth bands)
  with their pan keys removed.
- **The character is the subject, close and cozy:** at least 40 % of the frame height (about two thirds works),
  feet near the bottom edge, in a third of the frame. A small figure in a wide street turns the scene into an
  empty place, and its breathing and blinks vanish. Bring the character forward rather than cropping the plate:
  keep the plate at its own size and blur it a little (`gaussian_blur` about 5 on each plate layer) so it sits
  behind them like a lens's depth of field; enlarging a plate only softens it.
- **One character at rest**, not walking: a part-sheet rig with no walk, `relaxed`, a hand to the chin
  (`rightHandToChin` 1 with `rightHandIk` 1), a little `lookUp`, and `breath`, `headNod` and `spineLean` on slow
  sines, all read through `local t = math.floor(time*8)/8` so the character moves on threes. Two keyed `blink`s
  on `step` keys, far apart.
- **Three to five small loops around them:**
  - Rain: one tile of slanted streaks drawn twice, one tile height apart, moved one tile per period.
  - Ripples: small stroked ellipses on the floor that grow and fade, each with its own phase. List them
    before the character's layer (the first layer listed draws at the bottom), so none is drawn over them.
  - Lights: lantern glows that pulse on `opacity`. Squash or place a glow on the layer transform, never a group's.
  The rain moves smoothly; only the character steps.
- **Grade it a little darker and cooler** than the plate (`adjust` `brightness` about -0.12, `temperature` about
  -0.12) under the finishing pass.
- **Check the seam:** with the frames rendered, the mean difference from the last frame to the first should match
  the difference between any two neighbouring frames.

## Finishing pass

All 2D, in layers over a `scene_ref` of the drawn scene (below, top to bottom):

- **Diffusion:** the scene again through `scene_ref`, `gaussian_blur` `blur` 16, blend `screen`, opacity 0.38.
- **Colour wash:** a full-frame rectangle with a warm-to-blue `gradientFill` (`#ffb070`, `#ffd9b0`, `#3a4f9a`),
  blend `soft_light`, opacity 0.55.
- **Grade:** one adjustment layer with `adjust`, `channel_shift` `horizontal` 1.5 (`mode` `rb`), `vignette` and
  `film_grain` `intensity` 0.12. Effect params are ranges, not percentages: `adjust` takes `saturation`,
  `highlights` and `temperature` in [-1, 1] (`0.08`, `-0.12`, `0.06`), never 0..100.

```json
[
  { "id": "diffusion", "transform": { "position": [640, 360], "opacity": 0.38 }, "content": { "kind": "scene_ref", "assetId": "film" },
    "blendMode": "screen", "effects": [{ "id": "gaussian_blur", "params": { "blur": 16 } }] },
  { "id": "warmWash", "transform": { "position": [0, 0], "opacity": 0.55 }, "blendMode": "soft_light",
    "content": { "kind": "shape", "items": [{ "type": "group", "contents": [
      { "type": "rect", "position": [640, 360], "size": [1280, 720], "roundness": 0 },
      { "type": "gradientFill", "startPoint": [0, 0], "endPoint": [1280, 720],
        "colorStops": [{ "offset": 0, "color": "#ffb070" }, { "offset": 0.55, "color": "#ffd9b0" }, { "offset": 1, "color": "#3a4f9a" }] }] }] } },
  { "id": "grade", "adjustmentLayer": true, "content": { "kind": "color", "color": "#000000" },
    "effects": [{ "id": "adjust", "params": { "saturation": 0.08, "highlights": -0.12, "temperature": 0.06 } },
                { "id": "channel_shift", "params": { "horizontal": 1.5, "vertical": 0, "mode": "rb" } },
                { "id": "vignette", "params": {} }, { "id": "film_grain", "params": { "intensity": 0.12 } }] },
  { "id": "impact", "adjustmentLayer": true, "start": 3.125, "duration": 0.0833, "content": { "kind": "color", "color": "#000000" },
    "effects": [{ "id": "black_white", "params": {} }, { "id": "negative", "params": {} }] }
]
```

The diffusion layer renders the scene a second time; use it once, on the finished film.

## Proven on

- A riverbank kick on one painted plate (an earlier run; new plates start from the SVG layout): held pan, near-grass parallax, motion on threes, an impact
  frame and the finishing pass.
- Three painted-depth walk-throughs with two part-sheet characters (8 s each): a riverbank path, a shopping
  arcade at dusk where they pass behind a lamp post, and a summer station platform where they pass behind a
  pillar and a bench.
- A lo-fi loop (8 s, seamless): the painted arcade at dusk in the rain behind a girl who stands close, at two
  thirds of the frame height, at rest with her chin on her hand, breathing and blinking on threes, with ripples
  and pulsing lanterns.
