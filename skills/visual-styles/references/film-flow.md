# Styled film flow

The order of work for a short film in one of the styles here. Cast, scene table and sound follow
the `character-rigging` skill's `references/cartoon-film.md`; this page is where the style
comes in and how a film is assembled and saved.

## 1. The picker

1. Offer the styles as tiles, one per row of [the style index](style-index.md) whose `use` is `film`: its
   `label`, its `notes` line and its preview clip, and put it on a card. Set the card's `category` to the chip named
   in the use case's column of "Category chips each use case shows" in [the style index](style-index.md), else
   `Other styles`, and mark 4 to 6 cards `recommended` (the picker opens on its `Recommended` chip; a request that names
   a style puts that style first). The chip rules, the minimum of 4 cards and the card order (chip order, `Other styles`
   last) are stated once there. The classic cartoon comes first and is the default when the user does not pick.
   Offer every film row, so the user can see what exists; never shorten the list on
   your own judgement (the tool takes up to 100 tiles). Rows whose `use` is `graphic` are for a graphic or
   explainer request, not a film or cartoon.
2. Ask the rest in the ask panel in one go: palette (take the style's own or the user's brand colours,
   keeping the style's one hero colour), length, and the facts the film must state (names, numbers,
   places). Do not start drawing before these are answered.

## 2. The rough cut

1. Write the shot list: one line per shot with its place, who acts, what happens and its length.
2. Make every shot an ordinary scene that holds a **name card**: a plain card reading the shot's name and
   number, at the shot's final length. A card marks a shot not yet drawn.
3. Write the joiner scene last: it places each shot (a `scene_ref` to the shot's saved scene) in order, with
   the cuts and any shared sound. Play the rough cut to judge pacing and length before drawing anything.
4. The final export refuses while a card remains in any shot.

## 3. The shots

Draw one shot at a time with the style's reference and [FRAME.md](FRAME.md). A hosted scene URL never
changes, so a finished shot does not replace its card at the same address. Each landing is:

1. save the finished shot (a new URL);
2. re-save the joiner pointing at that new URL (a new URL too);
3. post the fresh joiner link to the user.

A character drawn for a shot comes through the part-sheet flow (the `character-rigging` skill). Every arm and leg is two pieces, upper and lower, in every style; read the style's "On a part sheet" before drawing, because a limb drawn as one tube or line is refused. Lip-sync needs a `rig` cast, or a `shapes` character that has a face and a `mouth` chart ([shapes-character](shapes-character.md)); a face-less `shapes` figure (silhouette, stick, woodcut, stained glass, pixel) cannot talk.

Never describe a landing as overwriting the card's file, and never reuse an old link after a landing.

When a style is built from a reference film or a reference frame set, measure it first (palette, sizes, positions
and step rate: the `reference-fragment-matching` skill, "Measure the reference before drawing anything") before the
first shot is drawn.

## 3b. The style's finish

The chosen style's finish goes into the first scene you write, never as an extra afterwards: its stepped rate (a divisor of
the root fps), its film or paper look on the `scene_ref`, and its title card or iris. Each recipe names it in its
"Finish" section; follow that section and do not restate it. A style whose "Finish" says no finish needs none.

## 4. Score last

The style's `score` says when. `last` (the default): music and sound effects go in after the picture is locked,
cut to its final lengths, as in
the `scene-video-edits` recipe. `first`: the beat
table is written before the shots and the picture is keyed to it.
