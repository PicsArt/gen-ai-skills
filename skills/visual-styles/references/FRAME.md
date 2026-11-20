# Frame checklist (every style)

Run this on a contact sheet of the finished shot, frame by frame, before showing it. Each style's own
checklist adds to it; none replaces it. A frame that fails an item is redrawn, not explained.

1. **A subject with a face that acts.** A character, an animal or an object with eyes, and something
   happens to it that it reacts to. A face that only sits there is a prop. A silhouette style keeps this
   with a pose and a head turn instead of a face.
2. **A full-bleed world.** The picture is filled edge to edge: sky, wall, table, colour card. A subject
   floating on blank ground is allowed only when blank is the stage on purpose.
3. **Three or more details of background life** that do not carry the plot and keep moving or changing:
   a bird on a wire, steam, a flag, a sleeping cat, falling petals, a clock hand.
4. **The medium is visible.** The style's texture reads at the size the viewer sees: paper edge and
   shadow, tone dots, off-register print, a lit screen. If it needs zooming in to be seen, it is not
   there.
5. **One light, one outline weight, one palette.** Characters and place share them. A hero colour
   (the one the style reserves) appears on the subject and nowhere else.
6. **Readable at phone size.** The subject is a third of the frame or more in a hero shot, text is at least
   40 px at 1080 wide, nothing important sits in the outer 5%.
7. **Every layer moves or is held on purpose.** Idle motion runs on the style's own time step (see its
   motion habits); a layer that should be still is still, not almost still.
8. **Hand-made type.** Words sit on a tag, a strip or a panel in the style's face, never bare default type.
9. **Not a look-alike.** Read the style's originality guard against what you drew. If anyone could name
   the character or the shot it resembles, change the silhouette, costume and composition.
10. **Two pieces per limb on a part sheet.** Every arm and leg is an upper and a lower piece overlapping at the joint, in every style; the recipe's "On a part sheet" says how to hide the joint. For an outlined style the builder caps the joint; draw nothing extra there. A one-piece limb is refused by the builder and the credits are lost.
11. **The style's finish is applied.** Its stepped rate, its film or paper look and its card or iris (the recipe's "Finish" section) are in the first scene; a frame without them is not finished.

Checks the tools can do (run them, then look): `picsart_scene_validate`, `picsart_scene_lint_layout` for crowding and
off-frame pieces, `picsart_scene_contact_sheet` across the whole clip, and the motion checks in
the `quality-review` recipe.
