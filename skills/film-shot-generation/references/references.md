# A run's reference images

Every video call carries its references in `imageUrls` only, and no other image parameter is set:
an exact frame passed on its own shuts the references out, and a frame shows only the people in it.

## What a run carries

- **Every person who appears at any point in the run**, even one not in its first frame: their
  identity view and their wardrobe view. A person carried by words alone is drawn from the model's
  habits. Add a profile, back or state view only where a shot needs it. A photographed person's
  original goes first and untouched; generated views follow it.
- **Every prop the film gave a plate**, as its own image, named by number where it appears. Every
  object is named once, in one place: a flask on her strap and in her hand in one prompt is two
  flasks.
- **The place:** its map, always, and its wide whenever a cut opens wider than a tight frame. An edit
  that reveals more of the setting than the clip showed adds them too.
- **The scene picture**, as `START FRAME`, on the scene's first run only.
- **An approved still or a carried frame**, as `FRAME REFERENCE for shot N`, only for the cut that
  uses it.

Each entry is a single view of one thing. Never a sheet, a composite or a contact sheet.

## The header

The prompt's header names every image by number and role, once, in the order of `imageUrls`:
`IMAGE 1 — START FRAME`, `IDENTITY @cal`, `WARDROBE @cal`, `PROP: the wrench`, `SCENE PICTURE`,
`SPACE map`, `SPACE wide`. After the header, people are called by name, never re-described. The
compiler writes the header from `images`; record the ordered list and the roles, since every shot's
references are numbers into it.

## Budget

Read the model's image count and size limits with `picsart_model_params`, and check the set with
`picsart_preflight`: it measures every picture and refuses one under the floor, with the fix. Only
when a measured limit binds, in this order:

1. drop an optional still;
2. drop the wide, only if the map stays and no cut opens wider;
3. re-encode a PNG view as JPEG, same pixels;
4. last, a smaller copy of a view, never softening an identity view past what holds a face.

**Never drop the map, an identity view or a wardrobe view** to fit. A smaller copy of a view becomes
that view for every run after it (film-cast-design).

## Frames from a take

A frame used as a reference is exported at the take's native size with `picsart_scene_export`
(`mediaType: "png"`, `startTime`) and probed. A contact-sheet thumbnail is for choosing a frame,
never for sending one.
