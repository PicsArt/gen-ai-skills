# The user's own photos

A photo of the real person, product or place **is** the asset, not inspiration for a lookalike.

## Taking it in

- It comes in through `picsart_media_upload`, or from a link or Drive as video-core's Asset URLs
  say, and is saved as it came.
- Probe the source and the saved file with `picsart_media_probe_media`: bytes, width, height and
  content type match, or it was changed on the way.
- **Never re-encode, crop, enhance, retouch or cut out the original.** Every changed copy is a
  derived file beside it, with the operation and the reason recorded.
- Decide from the picture whether it shows the asset or is inspiration. Inspiration gets a caption
  and never enters a run. When its role cannot be told, flag it as unclear between the two.
- Decide whether it is one view or a composite. A composite is kept as it came, and its views are
  cut from a copy (`references/views.md`). A composite never goes into a run whole.
- For a person, check for a clearly visible, well-lit, sharp face near the front, at a good size.
  A photo that falls short is saved anyway, and flagged with what a better one would show.
- **Never ask the user to approve their own photo.** It is saved, locked and registered as it is.
  Only a sheet generated from it is reviewed.

## When a card needs a view the photo lacks

Flag the missing view, and what would fill it: a photo that shows it (the outfit the story dresses
them in, their profile) beats a generated view, so name both, the generated one with its cost.
Never generate a lookalike to fill a slot the user could fill with a photo. A generated view is a
profile from the photo, then a sheet from the photo, the profile and the outfit, compiled with
`picsart_film_compile_asset_prompt` and its `usePhoto` and `useOutfitImage` inputs.

A photo that already shows every view the cards need gets no generated sheet at all.

## An era the photo does not match

When the film's tone is an era and the photo is plainly modern, flag that an era-adapted portrait
is possible, and that choosing it makes a generated image, not the photograph, the identity in
every run. Never restyle a real person's photo on your own call.

## Allowed derived copies

- a view cut from a composite;
- a format conversion a model requires;
- a smaller copy to fit a run's byte budget;
- an enhanced copy when the source is under a model's size floor (`picsart_enhance`);
- a neutral background cut-out, only after a first run proves the original background leaks into
  the shots.

In every run, the original (or its identity cut) goes first, and any approved generated view
follows it.

## A real place

The user's photos of a real place are its `SPACE` references. Its map is made from the best wide
photo, as film-shots says for any place.
