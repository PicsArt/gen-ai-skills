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
   (the one the style reserves) appears on the subject and nowhere else. Each recipe's colour table names
   every colour's one job; a colour used outside its job is a defect.
6. **Readable at phone size, and long enough to read.** The subject is a third of the frame or more in a
   hero shot. On a 9:16 frame 1080 wide, content text is at least 100 px, captions at least 50 px, and
   everything that must be read sits in the safe box x 60 to 940, y 250 to 1500, so a caption clears the app's
   own bars (ours, tune by render). Text stays up long enough to be read twice and at least as long as its
   spoken line; a verdict or a comparison stays fully in frame until it has been read; a label leaves before
   the camera moves on; clear the subtitle before a silent beat. A card shorter than reading time is allowed
   only when its words also appear in full elsewhere. Lay out 9:16, 1:1 and 16:9 each on their own, never by
   scaling one into another.
7. **Every layer moves or is held on purpose.** Idle motion runs on the style's own time step (see its
   motion habits); a layer that should be still is still, not almost still.
8. **Hand-made type.** Words sit on a tag, a strip or a panel in the style's face, never bare default type.
9. **Not a look-alike.** Read the style's originality guard against what you drew. If anyone could name
   the character or the shot it resembles, change the silhouette, costume and composition.
10. **Two pieces per limb on a part sheet.** Every arm and leg is an upper and a lower piece overlapping at the joint, in every style; the recipe's "On a part sheet" says how to hide the joint. For an outlined style the builder caps the joint; draw nothing extra there. A one-piece limb is refused by the builder and the credits are lost.
11. **The style's finish is applied.** Its stepped rate, its film or paper look and its card or iris (the recipe's "Finish" section) are in the first scene; a frame without them is not finished.

## The QC pass

Run these in order on every film before it goes out. The first is a viewer's pass at normal speed: watch it once as
a viewer would and fix what reads wrongly within three seconds, then measure.

1. **Dead beats.** Something new happens every few seconds; no flat frame is held long, and a near-empty frame
   is held only while a mark is being made (ours, tune by render).
2. **Per-shot pass table, and the weakest shot named.** One row per shot against this checklist; write down the
   weakest one and fix it before the film is sent.
3. **A phone-size contact sheet at one frame per second.** The style's signature must show in every frame,
   not only the first.
4. **Vary the scale.** Across the film, at least one extreme close-up and one wide.
5. **A small-thumbnail read.** At thumbnail size the subject and the value structure (what is light, what is
   dark) still read.
6. **Determinism.** Randomness is seeded; render one frame twice and compare the pixels.
7. **Palette.** Count the pixels that are not in the style's palette per frame by eye on the contact sheet;
   `picsart_scene_check_pixels` does not count them yet.
8. **Data in space.** For a data style, assert the numbers with `picsart_scene_query_layout`: a bar's length against its
   value, a tick's value, parts adding up to the total.
9. **Text.** Nothing is cut off, overlapping, under a UI band, or low in contrast.

Checks the tools can do (run them, then look): `picsart_scene_validate`, `picsart_scene_lint_layout` for crowding and
off-frame pieces, `picsart_scene_contact_sheet` across the whole clip, and the motion checks in
the `quality-review` recipe.
