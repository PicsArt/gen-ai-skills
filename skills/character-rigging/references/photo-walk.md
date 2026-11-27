# Color keys and the side-photo walk

## Contents

- [Color keys](#color-keys)
- [A side-view photo, step by step](#a-side-view-photo-step-by-step)

## Color keys

Use `picsart_scene_cut_parts` to cut a photo, painting or drawing from keyed edits. Keep the base
picture as `image`. Paint a part flat in a distinct color in an aligned edit, then pass
`labels.masks.<part>: { mask: <edit URL>, color: [255, 0, 255] }`. Pixels must newly match the edit
within `tolerance` on every channel (default 100). One edit can mark several parts in different
colors. It may be another size at the same aspect ratio. A changed aspect is refused as `mask_size`.

| Picture | First cut | If it fails |
|---|---|---|
| A simple character drawn as named SVG parts | Build its groups with `picsart_scene_build_model`. | |
| A photo, painting or drawing | Key the parts. Add `ink: true` on moving parts of drawn art to keep their outlines. | Ask for the key again with its edges named. For a drawing with outlines, try seeds and seams; for a side rig use aligned sheets. |
| A place with far and near scenery | Use `bands.depthMap` or `bands.depth: true`. | On `depth_unavailable` or `depth_far_unclear`, use a keyed `bands.layers` mask for each near object. |
| An object in a place | Use a keyed band layer. | Give its polygon. |
| Glass, water or smoke | Cut the object behind the see-through layer separately. | |

**The gate on a key.** Look at the key beside the picture before cutting: one shape per colour, on the
part, nothing else painted. If no pixel newly matches the key, the cut refuses `key_color_missing`.
Ask for a new key or go down a rung. The cut excludes pixels that already matched in the picture
and warns if they account for at least a quarter of the matches. Choose a more distinct colour or lower
`tolerance` if the part has holes. The cut also warns when a key lost a quarter of its px off the figure
(the edit painted something else too: ask again). A key in several pieces is normal: a shoe's straps
part its paint. A key for a plate or a `noarms` edit is different: there the edit's own pixels are
used, so also check that nothing changed outside the painted area.

**Key prompts that worked.** Name the part by what it looks like, give its edges, and say what stays.

- Two parts in one edit: "Paint two shapes flat, and nothing else. Shape 1, flat magenta #FF00FF:
  the dark leafy bush in the lower left corner, keeping its exact outline. Shape 2, flat cyan
  #00FFFF: the big tree at the right edge, trunk and branches, keeping its exact outline. Leave the
  grass, the path and the sky unpainted. Change nothing else in the picture."
- Legs of shorts: "...flat magenta #FF00FF: her left leg from the hip down, with its half of the navy
  shorts below the waistband...". A garment spanning two parts must be split in words, or one key takes
  it all.
- A head, as one silhouette rather than a list of features: "Turn the man's head into a flat magenta #FF00FF
  silhouette, like a cut-out shadow. The silhouette is everything inside the outline of his head and neck..." (in full
  under *A side-view photo, step by step*). A shoe: its own colour, "the whole shoe, sole and laces".

**Ink on drawn art.** Set `ink: true` on moving parts so their lines and soft edges travel with them.
When every part is keyed, the nearest part takes the remaining outline. The body can have just a
key and keep its own line. If the check still shows a hole in a keyed part, repaint its key over
the missing fill.

**The shoulder notch.** Keys and seeds alike leave a notch where an arm crossing the body comes off:
the picture never showed the shoulder under it. A `noarms` edit (the figure without arms, which the
sheets route cuts the torso from) is what fills it.

## A side-view photo, step by step

For side photos in shirts, jackets, hoodies, cardigans and dresses, each Gemini 3.1
Flash Image call asks one small thing as an edit of a picture already made, so every key lines up with the photo; a
character takes about 10 calls. `{who}` gives build, hair, top, trousers and shoes: clothes away from magenta, cyan and
pure red, green or blue, trousers with the shoes showing, hair off the shoulder.

**Five prompt rules.** Most redos came from loose wording.
1. Name a part by what can be seen: "the arm that hangs straight down along his side nearest the camera, its hand by
   his thigh", never just "the arm" or "the other arm".
2. Say what is covered as one outline ("a flat silhouette: everything inside the outline of his head and neck"), not as
   a list of features: Gemini keeps a feature it can see (an ear stayed skin).
3. Count exactly: "two shapes", "exactly three dots, one of each colour".
4. Say what stays: "Do not move, bend or redraw the legs."
5. Forbid only what the picture shows: naming a missing thing draws it ("no floor line" drew one).

**The calls.** These prompts use a navy blue hoodie and grey jogger trousers. Put your character's clothes in their place.
1. The picture: "Full-body photo of {who}, seen exactly from the side (profile facing right), standing on a plain light
   grey studio backdrop. Both legs straight, both feet side by side, the far foot hidden behind the near one except its
   toe. The arm nearest the camera hangs straight down by the side. The far arm reaches well forward and a little down,
   clear of the body, its open hand showing the palm. Whole figure in frame with space around it, even soft light."
   Ask again on doubled or staggered legs, a floor line, or anything touching the frame.
2. Arms: one two-colour key of both arms on the photo, then the figure without arms as an edit of that key.
   - The arms key: "Paint two shapes flat, and nothing else. Shape 1, flat magenta #FF00FF: the arm that hangs straight
     down along the man's side nearest the camera: its whole sleeve from the shoulder seam down to the cuff, and the hand
     by his thigh, palm and every finger. Shape 2, flat cyan #00FFFF: the other arm, which reaches forward to the right:
     the visible part of its sleeve from where it comes out from the front of his chest, and the whole open hand, palm and
     every finger. Each shape is one solid flat colour with no shading, texture or skin showing inside, keeping the arm's
     exact outline. Do not paint the body or the legs. Change nothing else in the picture."
   - The armless edit, on the arms key: "The flat magenta and flat cyan shapes mark the man's two arms and hands, which
     must be deleted, so that after the edit the man has no arms and no hands at all. Where the magenta shape lies over
     his body, from the shoulder down to the hem, paint the side of the navy blue hoodie itself: the same closed fabric as
     the rest of the navy blue hoodie, its folds and soft light continuing across and joined smoothly to the fabric around
     it, from the hood down to the ribbed hem. Where a shape reaches below the navy blue hoodie's ribbed hem, draw only the
     grey jogger trousers and the grey backdrop there. Where a shape lies over the backdrop, paint the grey backdrop. Do
     not draw any sleeve, arm or hand. Change nothing else." On a jacket or a shirt, "from the collar down". Ask again
     when a sleeve, a hand or an armhole shows.
3. Keys on the photo, one edit each:
   - The head: "Turn the man's head into a flat magenta #FF00FF silhouette, like a cut-out shadow. The silhouette is
     everything inside the outline of his head and neck: the hair, the face, the beard, the ear and the neck down to the
     navy blue hoodie's neckline. Fill all of it with the same flat magenta, with no features, lines, shading or skin left
     inside, not even on the ear. Leave the hood behind his neck unpainted. Keep the outline exactly where it is. Change
     nothing else in the picture." Name a beard only when there is one. With no hood or high collar, "down to the
     shirt's collar" and no hood sentence.
   - The legs: "Paint two shapes flat, and nothing else. Shape 1, flat magenta #FF00FF: the man's leg nearest the camera,
     the one in front whose shoe is the lower of the two: its trouser leg from the hip, where it meets the navy blue
     hoodie's hem, down to the cuff above the shoe. Shape 2, flat cyan #00FFFF: the other leg behind it, only the part of
     its trouser leg that can be seen. Each shape is one solid flat colour with no shading or texture, keeping the trouser
     leg's exact outline. Leave the hand on the thigh, the navy blue hoodie, the ankles and the shoes unpainted. Do not
     move, bend or redraw the legs. Change nothing else in the picture." The same again on the armless edit, without "the
     hand on the thigh,", gives the leg under the hand. Where that edit shows no far leg, Gemini makes one up: keep only
     its magenta.
   - The shoes: "Paint two shapes flat, and nothing else. Shape 1, bright flat magenta #FF00FF: the whole shoe nearest
     the camera, the lower one in front, sole and heel included. Shape 2, bright flat cyan #00FFFF: the other shoe behind
     it, only the part that can be seen. Each shape is one solid flat colour with no shading or texture, keeping the
     shoe's exact outline. Leave the ankles, the socks and the trousers unpainted. Change nothing else in the picture."

   The torso needs no key: it is the armless edit's figure minus the head, legs and shoes. Key or dot an arm only on the
   photo, never on a removal edit: after one, Gemini takes the emptied near shoulder for the far arm's.
4. Joints: read the shoulder, elbow, wrist, hip, knee and ankle off the photo by eye, on a crop with a pixel grid.
   Gemini's dots ("draw exactly three small solid round dots, one of each colour: pure red on the centre of its shoulder
   joint, pure green on its elbow, pure blue on its wrist. Draw no dot anywhere else") put the wrist on the cuff or the
   shoulder 32 px low; use them only for a picture you cannot read.

**Why each wording.** Change a wording only when a run shows a defect, and add a row with the defect it answers.

| Call | Wording | Defect it answers |
|---|---|---|
| Picture | "both feet side by side" | "feet together" gave man8 a staggered stance |
| Picture | no "floor" anywhere in the prompt | "no floor line" drew one on woman9, and "curves into the floor" drew a rolled backdrop edge |
| Picture | the far arm "well forward and a little down" | "angled down" took woman9's arm off the body at the hem, too steep to rig |
| Arms key | keyed on the photo, never on a removal edit | a key on a removal edit put man4's far shoulder where the near arm had been |
| Armless edit | what fills each area: the closed fabric "from the hood down to the ribbed hem" | "draw only the plain side of the jacket" gave man10 a vest with an open armhole |
| Armless edit | "Where a shape reaches below the ... ribbed hem, draw only the ... trousers and the grey backdrop there." | without it man11's near sleeve came back, its cuff hanging below the hem |
| Armless edit | not shortened to "remove everything painted magenta and cyan" | the short version painted new arms into the shapes |
| Head | one silhouette, "not even on the ear" | a list of the head's features left the ear as skin |
| Head | "Leave the hood behind his neck unpainted." | the hood lies inside the head's outline; with this sentence man11's head kept it out |
| Shoes | "bright flat magenta" | man5's shoes came back dark magenta, which read as no key |

**Gate, then cut.** Check each key beside the photo. The near arm includes the wrist and hand, and each joint is inside
its limb. Redraw a wrong part on the plain backdrop. A side rig takes `sheets` and refuses `labels.masks` with them.
Prepare each part's sheet from the photo or edit pixels inside its key on one shared blank picture (a flat color absent
from the figure, with a little grain). Prepare the torso by subtraction, the ankle between cuff and shoe, round hip and
shoulder caps, the near arm hung straight and the far arm drawn whole before calling the cutter.

Give the blank and the part sheets as hosted picture URLs. Set `rig: "humanoid-side"`, `labels.regions.edge: "fill"`,
`labels.regions.seeds.<part>: { sheet: "<part>" }` with no points, and `minus: "blank"` on every part. This prepared
cut retries up to six joint moves. Write each returned `moved` entry's `to` back into the part. If a refusal still
names a pivot, take the joint there and check both drawings cover it.

**Walk it.** Apply `motionPreset:walk_cycle` with `picsart_scene_apply_preset`. Set `stride` 240 (about 0.75 of a
photo cut-out's 320 rig-px leg), `lift` 20, `bob` 0.3, `elbow` 0.12, `from: "rest"` and `distance` to the mark.
The swing eases on the floor and a measured rig's stride is capped at its own leg. At `stepDuration` 0.5, 1450 px
takes six steps and stops at 3.6 s in a 4 s clip. Leave about 0.4 s after the last step. At stride 300 the hips bob
70% more to keep the feet planted.
