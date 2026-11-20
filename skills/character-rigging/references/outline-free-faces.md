# Faces without outlines

A style that draws no outlines (flat fills that differ only in tone) makes a face from fills and patches. These
rules keep the eyes, lids and brows readable while they move. Each one is a fault a proof showed.

- **A dark pupil that cannot leave its eye.** Make the dark part of a round eye the slice of the circle beyond a
  sliding vertical chord: a closed path whose vertices lie on the circle at angles `-th` to `th`, where
  `th = acos(d / r)` and `d` is the chord's offset from the centre. Slide `d` to look about; the shape stays inside
  the white by construction. For a saved character, key one vertex set per look value (`by` on the look dial).
- **The lid is a patch in the head's colour that slides down over the eye.** When the eye is open, move the patch
  fully clear of the eye, not just thin; a patch left half-overlapping shows its corners outside the head.
- **Brows and lid lines sit above the lid patch.** A lid in skin colour hides whatever is drawn under it, so a brow
  or lid line placed under the patch vanishes at rest and pops in only during a blink. Draw them above, and give a
  lid line an opacity track so it shows only while the lid is down.
- **Short, darker-than-skin brows carry the mood.** A small stroke just above each inner eye corner, in a darker
  skin tone, with the inner ends raised reads as worry. Long black brows read as anger; keep them off a worried
  face.
