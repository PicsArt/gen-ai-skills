# Pictures for a character cut from pictures

The pictures a side-view character needs before `picsart_scene_cut_parts` cuts it
([cut-from-one-picture.md](cut-from-one-picture.md)): one base picture, the sheets its base actions need, and a
drawn pose for each beat of the plot that the cut parts cannot bend into. Every picture after the base is an
edit of the base, so all of them line up at 0 px and share one hand.

Model: Nano Banana 2 (`gemini-3.1-flash-image`), 9:16, 2K, `extra.thinkingLevel: "high"`, 4 credits a picture.
Quote every batch with `picsart_preflight` and SPEND (quote it in one line, then get the yes with `picsart_ask`, found as picsart-video-rules says, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", else your host's own question tool, such as AskUserQuestion; never as a typed question unless both fail; only then those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) before generating.

## Contents

- [Order of work](#order-of-work)
- [The base picture](#the-base-picture)
- [Base actions and their sheets](#base-actions-and-their-sheets)
- [Plot poses](#plot-poses)
- [Edits that fail](#edits-that-fail)
- [Habits](#habits)

## Order of work

1. The plan is approved first (cartoon-film §1), with its beats per character.
2. **The pose list.** For each beat, one row per character: the move, whether it stays in the picture plane, the
   picture it needs. A move in the plane (a step, a point, a reach, a held prop, a nod) needs no picture. A move
   out of the plane needs a drawn pose: sitting, a palm or the back of the hand turned to the camera, a head
   turned toward the viewer, a wing at each stroke. ASK (with `picsart_ask`, found as picsart-video-rules says, for any closed choice, a multi-select included, so the options are buttons the user taps, the recommended one first; then your host's own question tool, such as AskUserQuestion; only where all fail, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) the story questions that pick a drawing (who is waved
   to, which way they face, who sits) and agree the list, with each prompt and its cost, together with the plan.
3. The base picture first, alone. Read its edge first ([cut-any-edge.md](cut-any-edge.md#read-the-edge-first)).
   - **A dark outline or a light rim** (paper craft, felt: pass `labels.regions.edge: "light"`): before any
     sheet, run `picsart_scene_cut_parts` with `seedMap: "base"` on it and look at the numbered areas and the
     magenta walls between them. Each part (hair, face, jumper, each arm piece, each leg piece, each shoe) must
     be its own area. A short gap in a wall (a hand lying on the thigh) is closed later by a seam. A base whose
     figure comes back as one or two big areas cannot be cut: draw the base again (a clearer outline or rim
     round every piece) before ordering anything else.
   - **Any other edge** (a coloured line, no line): the tool returns one big area, so do not draw the base
     again for that. Cut it by hand as [cut-any-edge.md](cut-any-edge.md) says.
4. Then the base-action sheets and the poses on the list, in one batch.
5. Look at every result before building on it: a sheet that moved, changed the face or the clothes, or came back
   on a grey background is drawn again, never used. The cut's `alignment` names a shifted sheet
   (`sheet_misaligned`).
6. Cut, check, save the character with every picture in `referenceImages`. A later film that needs a new pose
   adds one edit of the same base and cuts again; it never draws the character again.

## The base picture

Draw it twice and keep the one with the pure white background and the cleanest lines:

> Same drawing style as this <first character>: <who, in a few words: age, build, hair, clothes>, full body,
> side view facing right, standing straight, legs straight, the near arm hanging with the hand beside the
> thigh, the top's hem a clear edge over the trousers, slim thighs and a rounded hip behind them, plain
> clothes with no folds, plain white background. For a cut-out animation rig.

- The first character of a film names the drawing style in words; every later one passes the first one's base
  picture as the reference ("Same drawing style as this boy").
- Plain clothes with no folds; a hem, a sleeve seam, a waistband and a shoe top drawn as lines; hair short, tied
  back or under headwear. A loose scarf, a stick or a bag is a prop, drawn on its own.
- A character bent by age stands "a little bent forward", never leaning on anything.
- No cast shadow under the feet.
- Each thigh at most about two thirds as wide as the hip is deep, with the hip rounded behind it. A thigh as
  wide as the hip (blocky paper-craft legs) swung back comes out behind the cloth over the hip. Look for it in
  the base and draw it again before ordering sheets.

## Base actions and their sheets

Look at the base picture first. A sheet is ordered only when, in this picture, something lies over the part AND
a move in the plot shows what is under it; write that reason beside each prompt in the plan. A side rig always
gets the sheet without the top: its seat (the trousers or skirt over the hip) is cut from it, stays rigid, and
the thigh turns under it. Without it, the top over the hip is fitted as a garment, which blocky thighs fail.
A rolled trouser cuff that already covers the ankle needs no socks sheet; a character who never speaks needs no
mouth sheets.
What each sheet can give:

| Base action | Sheet prompt | Gives |
|---|---|---|
| stand, idle, breathe | `Same picture without arms.` | the torso and both legs, drawn whole where the arm lay |
| any side rig | `Same picture without the jumper: a plain white vest tucked in, the trousers drawn whole up to the waist.` (name the top it has; a vest colour unlike the trousers; for a skirt, `the skirt drawn whole up to the waist`) | the seat, cut across the hip below the hip pivot by a seam on this sheet |
| walk | `Same picture, with white socks instead of shoes.` | the foot under the shoe |
| walk, in a skirt or long dress | `Same picture, with skin-coloured leggings instead of the skirt.` (a colour unlike the skirt; for a dark dress `dark grey leggings`), then on that sheet `Same picture without arms.` and `Same picture, with white socks instead of shoes.` | the legs to the hips; the skirt is the base minus the legs |
| head moves | `Same picture without hair.`; under headwear `Same picture without the headscarf, her thin grey hair in a small bun.` | the head and neck; the hair or headwear is the base minus that sheet |
| blink | `Same picture with eyes closed.` | the blink swap |
| talk | `Same picture with mouth open.` and `Same picture with mouth in a small o.` | the mouth swaps |
| a covered limb drawn differently from the base (a rolled sleeve, a tall boot) | `Same picture, only his near arm in its rolled-up shirt sleeve, nothing else, plain white background.`, `Same picture, only his near boot, everything else removed.`, `Same picture, only his trousers and belt, everything else removed.` | the whole piece |

A base set is about 8 to 11 pictures with the two base candidates. When a plain `without arms` edit keeps a
piece of the arm, an Ideogram precise edit (`ideogram-4-5`, `extra.mask` black over the arm, `magicPrompt`
`off`) with `Same picture without the arm: the plain green dress, the white waist tie and the white apron
continue there.` paints it out.

## Plot poses

One edit of the base per pose on the list:

> Same picture, <he/she> <the pose, in plain words>. Everything else unchanged. For animation.

| Pose | Prompt |
|---|---|
| sit on a stool, trousers | `Same picture, he sits on a low stool, thighs level, shins straight down, hands on his knees. For animation.` |
| sit on a stool, skirt | `Same picture, she sits on a low stool, skirt draping over her knees, hands in her lap. For animation.` |
| sit lower | `Same picture, she sits on a low stool, her head lower, skirt draping over her knees, hands in her lap. For animation.` |
| beckon | `Same picture, she holds her near hand out in front of her at chest height, palm up, curling one finger to beckon. Everything else unchanged. For animation.` |
| look at the viewer | `Same picture. The child turns only his head to look at the viewer: a three-quarter view of the face, both eyes visible, a small smile. Body, arms, legs, clothes, colours, outline and paper texture unchanged.` |
| glance a little toward the viewer | `Same picture. The child turns his head only slightly toward the viewer, about a quarter of the way from profile: the face still mostly in profile, the far eye just showing beside the nose. Body, arms, legs, clothes, colours, outline and paper texture unchanged.` |
| wave, near arm | `Same picture, he raises his near arm and waves, open hand up beside his head, everything else unchanged.` |
| a bird in flight, one picture per stroke | `Same picture. The bird is flying: both wings raised high above its back, spread wide with the feathers fanned, legs tucked up under the belly so the feet do not show. Body, head, colours, outline and paper texture unchanged.` and the same with the wings `spread straight out level with its back`, `swept down below its belly`, `folded tight against its body` |
| a character riding an animal | the seated pose first, then `Same girl, same seated pose and same skirt, sitting on the back of this white duck, side view, facing left. Transparent background.` (`gpt-image-2.6-flare`, the seated pose and the animal as references) |

Try the move with the rig before proposing a pose picture, and show the frame where the bent parts fail. Each pose
goes to the cut in `poses` and is swapped in mid-move (character-rules §6).

## Edits that fail

| Prompt | What happened |
|---|---|
| `... with grey leggings instead of the skirt` on a grey skirt | same colour as the skirt: the skirt's middle was lost |
| `... with short white shorts ...` | came back on a grey background |
| `Same picture, only her arms ...` in profile | two bent arms, not aligned with the pose |
| `Same picture, only her legs without shoes, nothing else ...` | zoomed in, socks gone, bare feet with toes |
| `Same picture, she raises her hand and waves.` in profile | waves with the far arm and draws a different hand: a pose reference only |
| `her hair in a few separate locks` | barely changed, grey background |
| a leggings prompt in profile | refused by moderation once; the same prompt went through on retry |

## Habits

- One change per edit; "Same picture ..." keeps the framing. "Only her legs" and other crops change it.
- Chain an edit on an edit (the leggings sheet, then without arms) rather than asking for two changes at once.
- Replace clothing, never remove it.
- An edit changes more than it was asked to (a smile on the closed-eyes sheet): take only the part you need.
- An edit that draws a part in another hand (fingers on a mitten hand) is a reference, not art.
