# The look and the user's references

The look is locked on the film setup console before the story. Its style line comes back from the
console verbatim and is stored as it came; nothing here rebuilds it.

## References are inspiration, not a gate

A user may bring images beside the look. None of them reopens it.

1. **Look at each one** (picsart-video-rules, Asset URLs) before you say anything about it. Never describe
   an image you have not seen.
2. **One reference answers one question**, and its caption says which: "light from the window",
   "brick texture", "jacket fit". The caption travels into the descriptor it informs.
3. **An anti-reference** ("not like this") becomes a line written in positive form in the
   descriptor or the shot, never a list of negatives.
4. **A photo of the real person, product or place is not a reference**: it is the asset, used
   untouched. film-cast-design says how.
5. **A colour reference** is for colour only, never subjects or composition. The console has no
   custom palette, so it goes in at compile time: `look.paletteReference: true` on
   `picsart_film_compile_prompt`, plus `look.customPalette` when the user also put the colour into
   words. Keep its URL with the look; a URL in text shows a model none of its pixels.

The densest board belongs to the character in most scenes, not the thinnest: everyone already
"knows" the lead, and that is how the lead drifts.

## Descriptors are prompt-ready words

The descriptors are written when the pictures are prepared (film-cast-design). What they share with the
look:

- **concrete words only**: "stylish" and "moody" are not words a model can hold. If it cannot be
  pasted into a prompt, it is not locked;
- **the look's colour is carried into every place's descriptor**, which is why the grade later
  refines the film instead of inventing it;
- **design rhymes with character**: every visual choice restates who the person is, or what the
  story does to them.

## More than one world

A film with a deliberate second look (a dream, a flashback) opens the console once per world, each
with its own `world` id, and every prompt uses its own world's style line.
