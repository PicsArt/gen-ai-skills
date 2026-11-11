# A character picture for a cut-out puppet (drawn as SVG)

Part of [character-rigging](../SKILL.md) "Named SVG cut-outs" and the [cut-out puppet reference](cut-out-puppet.md).
An image model
(GPT Image) drawing SVG directly gives every part its own group, so the picture needs no vectorizing; `picsart_image_vectorize`
of a part-sheet PNG stays as the alternative.
A sheet the user draws follows the same layout.

## Contents

- [Flow](#flow)
- [The turnaround sheet](#the-turnaround-sheet)
- [What the builder owns](#what-the-builder-owns)
- [What not to put in the prompt](#what-not-to-put-in-the-prompt)
- [The picture check](#the-picture-check)
- [The builder contract](#the-builder-contract)
- [Prompt to walk](#prompt-to-walk-tool-calls-only)
- [Hands and mouths](#hands-and-mouths-separate-sets)
- [Review the body picture](#review-the-body-picture-before-the-user-sees-it)

## Flow

brief → turnaround sheet → picture check → review → the user approves → hand and mouth sets → review → rig build.

- The brief names the style in words and numbers (hand length, leg length, proportions). Proportions are the style's: chibi,
  animal, robot and stylised adult each differ.
- Every
  generated
  sheet passes the picture check before any rig build, and a defect is fixed on the drawing, not worked
  round in the rig.
- The first iteration need not be perfect, but it has no bad mistakes. Fix, and never forward, a stated rule broken (a hand
  over cloth, parts disjoined or torn, a gap, ledge or seam at a join, the original drawing altered to fit a part such as
  shorts reshaped instead of legs moved, feet or limbs pointing the wrong way, a missing part) and any defect visible at
  normal viewing size. Forward a minor one (a small wobble, slight line-weight or colour drift, an offset seen only when
  zoomed) with a one-line note.
- The approved picture is the reference. A later change that moves a part's length or width by more than 5% is shown to the
  user before and after, and asked.
- Compare
  prompt or
  picture variants by blind A/B picks by the user, not by a metric sheet. Judge a new approach's first
  draft against the old approach's first draft, or count the old one's rounds.

## The turnaround sheet

One request draws the front, three-quarter and side views of the same character in one SVG, so the three share
proportions, colours and line weight; it beat views generated one at a time. Generate it with `picsart_generate`, model
`gpt-image-2.6-sunburst`, aspect ratio 3:2, `extra` `{"outputFormat": "svg", "complexity": "medium"}`, with the frozen
template below and only the character description filled in; the result is an SVG file. The old long
rule-by-rule block is retired: a long prompt failed upstream, and the rules it carried belong to the builder.
The sheet has front, three-quarter and side views of the same character in one SVG, sharing proportions, colours and line weight.

Use this layout for the sheet:

**Template v2.8 (2026-11-10) is current.** It is v1 plus the hold sockets: the grip markers say where a handle passes through the
hand, and an animal or a creature that carries things in its mouth adds `socket_mouth`. Sheets drawn from v1 build exactly as
before. Fill the `{mouth socket}` slot with the clause below for such a character, and delete the whole slot, braces
included, for everyone else.

**Versions.** Tune the template only when a render shows a defect, and add a row here with the defect it answers.

| Version | Date | Change | Defect it answers |
|---|---|---|---|
| v1 | 2026-11-09 | Frozen turnaround template | |
| v2 | 2026-11-10 | Grip sockets; optional `{mouth socket}` slot; face always visible | Held props had no hand point; hats covered faces |
| v2.1 | 2026-11-10 | Side view: far arm hangs behind the near arm, hand a finger width off; each hand a clean open hand, handL/handR mirrored | Grandma sheet: merged-finger hand in front view, far hand drawn beside the body in side view |
| v2.2 | 2026-11-10 | The frozen template gets the face sentence (brim above the eyebrows, both eyes visible); long garments: legs drawn complete under a separate garment group, hip/knee markers on the leg centrelines; every marker inside the part it names | Describe-to-walk eval, 12 sheets: 5 of 6 ankle-length garments refused (knees at the hem, no thighs under the garment), wizard's brim hid both eyes on both sheets, chef and flat-cap markers outside their parts |
| v2.3 | 2026-11-10 | Hat sits high and tilted back, brim tipped up and clear of the eyes; shorts and any garment above the knee drawn inside the upperLeg groups | v2.2 re-run: wizard brim still covered both eyes (both sheets), boy's 3/4 view refused for loose shorts under the UpperLeg piece. Long-garment refusals were a builder fault (a hem-fold subpath), fixed in the builder |
| v2.5 | 2026-11-10 | Shorts, trunks and any above-knee lower garment are ONE `shorts` group in front of the legs (waistband to hem, one solid closed shape with no line or slit between the legs, a tenth of the thigh width clear of each thigh); the upperLeg groups hold only complete skin legs; the shirt hem overlaps the shorts' top edge; front-view A-pose hands held at hip height with a visible gap to the thigh | kid walk: thigh skin beside the shorts, a white gap under the shirt hem, and the crotch opening when each thigh carried its own shorts; the v2.2 refusal of loose shorts behind the thighs is gone now that the builder skins a `shorts` group across hips and both thighs |
| v2.6 | 2026-11-10 | Shorts are a waistband and two leg tubes joined at an inverted-V crotch, each tube covering its own thigh to its own hem, skin between the hems; each thigh lies inside the shorts above the hem; no headwear unless the description names it; the groups are written in paint order (hairBack, legs, far arm, neck, torso, garment, arms, head, cap last) | v2.5's one solid shape with no line between the legs read as a skirt; the boy's cap came before his head, so the head painted over the hat; the girl's thigh tops stuck out past the shorts' outline beside the hips; both got a cap the description never asked for |
| v2.7 | 2026-11-10 | Tight clothing is drawn inside the part it fits, loose clothing is its own group; so shorts are drawn again inside each upperLeg group (each shorts leg over its own thigh, covering its top and outer side); the builder adds a seat in the shorts' colour behind both thighs, so a stride shows fabric between the legs; the cap is always drawn over the head whatever the file order | v2.6's separate shorts group still showed skin at the hip in the 3/4 walk and the owner judged the result not good; per-thigh shorts move with the thigh, so the hip is covered by construction, and v2.3's crotch gap is closed by the builder's seat |
| v2.8 | 2026-11-10 | The face is drawn at rest: a neutral closed mouth (lips together, level, no teeth, neither smiling nor frowning) drawn as a filled lip shape about a fifth of the head wide, never a line, and level brows, browL and browR always drawn and named in every view that shows the eyes | The film's Leo and Sam were drawn with an open smile: neutral read as happy, happy as a bigger smile, every line spoken through the same grin, and angry was only brows over that smile. A first v2.8 sheet that asked only for a closed mouth drew a line, which a viseme only bows: she never opened her mouth to speak. A second roll drew a lip shape an eighth of the head wide: open, it added 0.15% of the head (Leo and Sam 0.58-0.94%) and read as closed |

**Order of use.** The builder accepts a `socket_mouth` group (a marker inside the head) once the SVG mouth-carrier change (!10872) is on master; before that it refuses the name (`unknown_part`). A sheet without the marker has no mouth carrier. Use the `{mouth socket}` slot only for a character that carries things in its mouth.

```text
Draw a character model sheet (turnaround) of ONE {character description}, in a single SVG, viewBox 0 0 1536 1024, white page, three full-body views side by side, left to right: front view, three-quarter view facing right, side view facing right. No hat, cap or other headwear unless the character description names one. The face is always fully visible: a named hat or cap sits high and tilted back on the head, its brim above the eyebrows and clear of the eyes, so both eyes are fully visible in the front and three-quarter views (a wide brim is tipped up, never pulled down over the face). It is the SAME character with the SAME outfit details in all three views, like a model sheet: same proportions, colours and line weight in every view. Front view: A-pose (arms about 30 degrees away from the body, slight elbow bend, hands open and held at hip height well clear of the body and of any shorts or skirt, with a visible gap of background between each hand and the thigh, feet at hip width). Three-quarter view: the whole body turned about 40 degrees to the right, near (ear-side, viewer's left) arm over the torso edge, far arm at full width, hair one closed mass; A-pose. Side view: strict relaxed profile facing right, arms hanging; the far arm is drawn complete and hangs directly behind the near arm, its hand offset from the near hand by only about one finger width (never beside the body). Structure: three top-level groups with ids view_front, view_threeQuarter, view_side; inside each, every body part is its own group with the view prefix f_, q_ or s_ plus the part name: head, neck, torso, upperArmL, lowerArmL, handL, upperArmR, lowerArmR, handR, upperLegL, lowerLegL, footL, upperLegR, lowerLegR, footR (example f_upperArmL); a part the design has beyond these (skirt, coat, tail, backpack, cap) is also its own group with the same prefix. Hair that falls behind the shoulders (long hair, ponytail) is NOT in the head group: it is its own group hairBack, drawn complete behind the torso, and the head group keeps only the head shapes and the front hair. The head group holds every head shape (front hair, face, ears, eyes, nose, mouth). Inside each head group, name the sub-groups with the view prefix: eyeL, eyeR, pupilL, pupilR, browL, browR, mouth, hairFront; keep the face shapes complete (closed eye whites under the pupils). The face is drawn at rest, with no expression: the mouth is a neutral closed mouth, lips together, level, no teeth, neither smiling nor frowning, drawn as one closed shape filled dark red and outlined, about a fifth as wide as the head and a third as tall as it is wide, never a single line or a small dot, and the eyebrows are level, each its own browL or browR group, drawn in every view that shows the eyes. L = limbs on the viewer's left, R = viewer's right. Per view also one group per joint marker with the view prefix (jointNeck, jointShoulderR, jointShoulderL, jointElbowR, jointElbowL, jointWristR, jointWristL, jointHipR, jointHipL, jointKneeR, jointKneeL, jointAnkleR, jointAnkleL), each ONE magenta circle r=5 fill #ff00ff at the rotation point inside both parts it joins; and socket marker groups with the view prefix (socket_head, socket_chin, socket_chest, socket_rightHand, socket_rightGrip, socket_leftHand, socket_leftGrip, socket_leftFoot, socket_rightFoot{mouth socket}), each ONE circle r=6 fill #00aaff on the part it names; a grip socket sits at the middle of the palm, where the handle of a held stick or tool would pass through a closed hand. Plain <path>, <circle>, <ellipse>, <rect> only; solid colours or gradients; no clip-path, mask, filter, use or transform; strokes round joins and caps. Every part drawn COMPLETE as if nothing covers it, ends rounded and extending past the joint into the part it attaches to. A long garment (coat, dress, robe, tabard, cardigan to the shin) is its own group in front of the body, and the legs under it are still drawn complete, upper and lower, down to the feet; the hip and knee markers go on the leg centrelines inside the leg shapes, never on the garment. Clothing that fits tight to a body part is drawn inside that part's group, so it moves with its joint (a sleeve in its arm groups, a sock in its lowerLeg group, a glove in its hand group); only loose clothing that hangs free of the body (a skirt, coat, dress or robe) is a group of its own. So shorts, trunks and any garment that ends above the knee are NOT a separate group: each shorts leg is drawn inside its own upperLegL or upperLegR group, painted over that thigh's complete skin leg, from the waistband down to its own hem, wide enough to cover the whole top and outer side of the thigh; the two shorts legs meet at the crotch between the thighs, and the shirt hem hangs a thumb's height below the shorts' top edge. The groups of each view are written in paint order, back to front: hairBack, the legs and feet, in the three-quarter and side views the far arm, neck, torso, the long garment, the arms (in the three-quarter and side views only the near arm), head (its face and hairFront inside it), then the cap last, after the head. Every marker lies inside the part it names (socket_head inside the head shapes, a hip marker inside both the torso and the thigh). Keep each shape simple (few path points) so the file stays small. Each hand is a clean open hand: a palm, one thumb and four separate fingers of even length, no merged or overlapping fingers; handL and handR are mirror images of each other in the front view.
```

- `{mouth socket}` for an animal or any character that carries things in its mouth: `, socket_mouth` (the list's last item,
  one circle on the head at the middle of the closed mouth shape, where a held stick or ball would sit between the lips). It
  is filled in the prompt, never left in braces, and only once the builder accepts it (see Order of use).
- Leave every other generation setting at its default (`complexity` medium, effort auto, quality high). A setting passed in
  the wrong field silently falls back to a 1:1 PNG, so read the aspect ratio and the format in the job result before
  building anything from it. Draw the sheet with the generation call, never by writing the SVG by hand (flat art, broken
  side views).
- The side view is the walking view: a strict relaxed profile with the far arm at full width. The three-quarter view keeps
  a real body turn (about 40°).
- Gradients are allowed; the template bans only clip-path, mask, filter, use and transform.
- A generation can fail upstream: the job status says only that the job failed and will not finish, with no cause. Most
  likely it hit the generation time limit, so a failure shows up only after about four minutes of polling; expect that
  wait. Retry once with a simpler description (fewer props and details) so the SVG is smaller and finishes faster. If the
  retry also fails, stop and report the two job ids: do not loop, and do not change `complexity` (low is untested for art
  quality).

## What the builder owns

The builder handles these, not a change to the picture.
The picture is never regenerated for these, only for broken art, and then once at most.

- **Left and right:**
  GPT names a part by the side of the image it is on, so
  the builder works out which limbs are the
  character's left and right, near and far, from the geometry and the view.
- **Draw order.** Near limbs over the torso, the cuff over the wrist, the far limbs behind, headwear above the head and the
  front hair: the builder orders the parts by role from their names, never from
  GPT's
  document order.
  (wrong on every earlier sheet).
  A top over shorts keeps the source order.
  A wrong order is fixed in the builder, never refused or regenerated.
- **The head group.** The builder takes the unnamed head shapes into the head.
- **Face draw order and visibility.** Brows draw above `hairFront`; in the side view the far eye and brow are hidden;
  pupils may be nested inside the eye groups.
- **Joint tolerance.** The builder absorbs a marker a few pixels off its joint.

## What not to put in the prompt

- **Joint-end sentences** ("no outline at the joint end", "flat end, no caps"). GPT ignores them and the whole picture gets
  worse (shoulder domes, broken draw order, caps on socks, a mouth outside the face, a longer neck). The template only asks
  for parts drawn complete, rounded and extending past the joint into the part they attach to.
- **Layer order and left or right rules.** The builder checks them.
- **A three-quarter body turn in numbers.** "The torso narrows to 0.75" is not obeyed; the template asks for the turn in
  words, and the user judges the turn on the sheet.
- **"Young" or "girl" in a description.** Picsart's content filter rejected "young princess" twice (HTTP 422); say "a princess in a pink gown" and leave the age out.
- **A four-legged animal.** The sheet prompt draws bipeds: a "four-legged fox" came out upright on both sheets and walked as a biped. Describe an animal as an upright character, or use the quadruped template instead.
- **A hand length.** Hands come out 5–20% long, and open hands longest.


## The picture check

Before any rig build, run `picsart_scene_build_model` with `character: {svg, check: true}` on the sheet. It builds nothing and returns
`pictureCheck` (its `path` names the image): an image of each view split into three columns (the body, the near limbs alone, the far limbs alone) and a
pass or fail per check:

- every part present and complete;
- every joint marker inside a part, or inside the garment covering it;
- the far arm's width against the near arm's;
- the hair and `hairBack` closed;
- the head group found.

Open the image and look at it; the checks do not replace the look. A wrong near or far split, a limb in the wrong place, or
a missing part shows at once. A failed check is fixed on the drawing
(regenerate the sheet once for broken art),
then the check is run again.

## The builder contract

Build one view straight from the whole sheet with `picsart_scene_build_model({character: {svg, view: "front"|"threeQuarter"|"side", duration}})`; the builder splits the view groups and strips the `f_`/`q_`/`s_` prefixes itself, and a multi-view sheet without `view` is refused by name. The builder assigns character sides from geometry: front character-right is image-left; facing right the image-left ear-side limb is character-right/near; facing left the image-right ear side is character-left/near. Names on parts, joints and sockets do not override that assignment. Three-quarter art has the whole body turned; near side = ear side.
GPT SVG 3/4: whole body must be requested turned; near side = ear side.

The builder accepts skirt, coat, coatBack, tail, scarf, backpack, cap, straps, strapL, strapR and hairBack in addition to the named body parts. hairBack follows the head behind the torso; a named skirt keeps its hem rigid on the hips, while coat/coatBack stay on the spine above the waist and share the hip/thigh clothing skin below it. A joint must lie in the union of its two adjacent parts or covering garment (hip in skirt/coat, ankle in shin or foot, neck in neck or head). Edge tolerance is four source px, twelve on hidden far limbs. Within 8% paired lengths normalize to the mean; side-view projection may use independent measured links. One unnamed top-level non-marker group is the head only when the named head is absent.

Role order is stable throughout motion: far hand < lowerArm < upperArm < torso; torso < near upperArm < hand < lowerArm. Head is above neck and torso; neck is beneath the collar. Document order and z prefixes do not override roles. Rest is measured from the source joint markers; presets use absolute targets and lower A-pose arms into their swing. Shoes stay rigid at the ankle.

Named eyeL/R, pupilL/R (including nested pupils), browL/R and mouth inside head become standard blink, look, brow and mouth controls, and the mood dials `happy`, `sad`, `angry` and `surprised`, which bend the drawn mouth and each viseme. Draw the rest face neutral (a level closed mouth, level brows): it is what neutral shows, and every mood starts from it. Without browL/browR the moods show only in the mouth and eyes, and the build notes it. Brows draw above hairFront. A profile hides the far eye/brow. Closed mouth artwork is deformed for visemes; no open-mouth drawing is invented. Unnamed face art stays static.

## Prompt to walk, tool calls only

1. `picsart_scene_build_model({character: {svg, view, duration}})` → `sceneUrl` (the rig, saved to Drive) and its `sockets`.
2. Host it: a document with `assets: [{id:"rig", type:"scene", uri:<sceneUrl>}]` and one layer `{id:"character", content:{kind:"scene_ref", assetId:"rig", fit:"none", blending:"pass_through"}, transform:{position:[0,0], anchor:[0,0], scale:[1,1]}}`.
3. Frame it: `picsart_scene_query_layout({scene, time:0})`, union the `box` of the visible `character__*` layers, then set the layer's `anchor` to the union's centre, `position` to the frame centre and `scale` to `min(0.6·width/unionWidth, 0.7·height/unionHeight)`.
4. `picsart_scene_apply_preset({scene, layerId:"character", preset:"motionPreset:walk_cycle", params:{travel:"in_place"}})`; the view's stride, lift and arm swing come from the rig.
5. `picsart_scene_validate`, then `picsart_scene_export({scene, format:"video"})`.

Walk the side and three-quarter views; the front view is for idle, gestures and face shots (no front walk).

Hands remain rigid unless an independent full Spread/Point/Fist/Grip/ThumbsUp set has matching topology and paint at the same wrist. Gradients are allowed; unsupported patterns, masks, filters, use, nested clips and unsupported paint transforms refuse by name. The importer can flatten supported simple clips in existing art.
Do not ask the image model for them.

## Hands and mouths: separate sets

A finger pose cannot be made by deforming one hand, so each hand pose and each mouth shape is its own drawing,
generated
after the body picture is approved and swapped by the rig per action.

- Hand poses: relaxed (back, palm), open (palm, back), fist, point, wave, hold, thumbs-up; the point pose angles the
  index finger forward (a lone upright index finger can read as rude). Mouth shapes: closed, the vowel and consonant
  shapes the speech needs (A, E, O, U, F, M, L), smile, surprise.
- Same style, line weight and colours as the approved body. Each hand starts at the wrist point of the approved hand,
  its wrist end no wider than the forearm's end and cut flat; give each pose its own length against the approved hand
  (open hands longer, a fist shorter) and check it.
- A hand set has a wrist marker per hand and a mouth set a marker at each mouth's centre; every drawing is its own group.
- The rig blends the hand drawings as path morphs on one hand: it takes five poses (spread: the open hand and the wave; point; fist; grip: the hold; thumbs-up),
  each registered to the base hand's wrist pivot, and refuses by name a set with a missing pose, a wrist that does not
  line up, or drawings whose path counts, vertex counts, grouping or paint differ.
- Draw the set from a multi-path template: a palm path plus one path per finger, the thumb a separate bump (not a line
  loop), each path in its own group (path, fill and stroke), every path ending at the wrist.
  Ask for "five edited copies, same commands, move the numbers only".
  A one-path hand matched the topology on one of two tries and crossed itself
  mid-blend; the multi-path template matched on the first try with no self-crossing in any pose or any 25, 50 and 75%
  blend.
- Check the topology before the build, and look at the interpolated silhouettes before the user approves the set. When a
  pose fails, ask again for that pose only, with the same template.
- The far hand is the near hand darkened, not a second drawing.

## Review the body picture before the user sees it

Fix every high defect first:

- every part present and non-empty, no id outside the brief;
- every marker present and inside both parts it joins;
- each limb's drawn axis along its two markers, its length between one and about one and a half marker distances;
- landmarks within ±0.03 of the brief, the same across views;
- no shape drawn twice: two parts painting the same colour away from their joint;
- the three-quarter shoulders clearly narrower than the front's;
- the picture check's near and far split reads right: near limbs over the torso, far limbs behind, the closed mouth inside the head;
- the limb ends at the wrist, never past it;
- background between a limb and the body is not a gap (a jacket's open space is its silhouette): a gap is a defect only where the original drawing shows cloth or skin, and nothing is added to fill one;
- size against the approved picture (see the flow).

Judge ink relative to the part's own fill, never an absolute darkness (a dark coat is not outline). A metric that passes
on the picture at rest can still fail the lifted arm: check any new geometry rule with the arm raised and by eye.
