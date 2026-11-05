---
name: asset-audit
description: Audit media assets BEFORE they enter scene cards, boxes or looks - alpha padding, dimensions, aspect, video properties, URL-reuse hazards, and whether a photo in a reference is a masked view of a larger one. Use before authoring scenes with new assets or when a styled card renders with mysterious edges or misalignment.
metadata:
  category: workflow
  version: '1'
  ported-from: asset-audit 1 at 55.75.0
user-invocable: false
---

# Asset audit - check the media before blaming the scene

Most "the mask is broken / content is misaligned / corners aren't rounded" reports are ASSET
problems. Audit first; it takes a minute and saves a debugging afternoon.

## The checklist

1. **Alpha padding (the #1 trap).** Sticker-style PNGs bake transparent margins into the canvas:
   `fit: cover` covers the box with the FULL canvas, so the visible content sits inset and any
   rounding or mask lands in the transparent margin - the visible edge is the asset's own square
   boundary. Check it by looking: build a one-layer scene whose composition is the asset's own size
   (from `picsart_media_probe`), `background: "#ff00ffff"`, the asset with `fit: "contain"`, and
   look at it with `picsart_scene_contact_sheet` (`resolution` set to the composition size). No
   magenta inside the frame: clean. Magenta around the subject: a padded sticker; trim it, or use
   it deliberately as a decal with no look.
2. **Dimensions and aspect:** `picsart_media_probe` (no download; EXIF-corrected width and height,
   duration for video). Cover-fit crops from decoded dimensions - a 4:3 photo in a 9:16 card loses
   its sides; check the subject survives the crop. Also compare the asset's size with its largest
   placement box: `scale = max(box_w / own_w, box_h / own_h)`, and a scale above 1 is an upscale. A
   585x1024 photo in a 1080x1920 full-bleed box is stretched to nearly double. Rendering can decode
   an asset whose dimensions are omitted, but query and selection geometry cannot invent them: for
   `fit: "none"`, declare both `width` and `height` when the layer must be selectable or
   queryable, or use its intrinsic centre as the default transform anchor. Without them the source
   still renders at natural size, but `picsart_scene_query_layout` returns no bounds and the
   fallback pivot is the content origin. Do not add `content.bounds` as a workaround: `fit: "none"`
   has no destination box and rejects `bounds` and `align`. When a scene already declares an
   asset's `width`/`height`, compare them with the probe: a mismatch means the document describes
   a different file than the one that will load.
3. **Video specifics:** duration against the trim window you plan (a trim beyond the end freezes
   the last frame); first frames may decode dark or blank, so don't trim in exactly at 0 or at a
   scene cut; embedded audio (mute it unless wanted); reversed playback does NOT reverse audio.
4. **URL reuse:** fine. The same media URL in two different boxes renders correctly. Do NOT add a
   distinct `#fragment` per instance: it defeats content dedup, and it silently rewrites a URI that
   already carries a fragment of its own.
5. **SVG data-URIs:** encode only `< > space`; raw spaces in interpolated text are tolerated, raw
   `#` is not (colours as hex-without-# interpolated after `%23`). Declared width and height on the
   asset matter - undeclared dimensions break mask plus bounds combinations.
6. **Content vs box semantics:** an asset that is itself a full-bleed photo behaves under any fit;
   UI screenshots and renders with baked-in margins do not - measure where the content actually
   starts.

## Is the reference element MASKED?

When sourcing assets for a recreation of a reference video, decide for every photographic element
whether you are looking at a WHOLE asset or a MASKED VIEW of a larger one. Baking the mask into the
bitmap gives the right pixels and the wrong scene: the photo can no longer be swapped, the mask
cannot animate, and the "asset" is a screenshot of someone else's render. Narrow slivers cut from
the visible part of a card, or a full frame grabbed as a "photo", are this mistake.

How to tell, cheapest test first:

1. **Does content continue past the edge across frames?** A masked view is a WINDOW: as the card
   moves, grows, or the mask animates, NEW parts of the same photo appear at the edge while the
   rest stays registered. Sample the element at 3-4 timestamps in its own span
   (`picsart_media_video_stills`) and check whether its content translates WITH the box (a whole
   asset moving) or STAYS PUT while the box reveals more of it (a mask sliding over a fixed
   image). The second is a mask, always.
2. **Is a feature cut mid-stride?** A hard straight edge slicing a face, a hand, or a horizon
   mid-feature is a mask boundary; a real asset's edge lands where the photographer put it.
3. **Does the aspect ratio look impossible?** 238x1095 (1:4.6) is not a photograph anyone shot; it
   is a viewport. Compare the element's aspect against plausible source aspects (3:2, 4:3, 1:1,
   9:16).
4. **Corner geometry:** `picsart_media_inventory_diff` (reference as `a`, your candidate as `b`,
   same frame size, `times` of interest; it spends credits) reports whether corners are rounded
   against the local surround. A rounded photographic corner means a mask or a `rounded_corners`
   look, not a rounded photo. Leave `plate` at `auto` for cards over a uniform background; with it
   off, a pale-topped card can split into two invented elements.

What to author once identified: the FULL asset plus a `mask` (or the look that owns the shape),
never a pre-cut bitmap. The mask can then animate and the photo can be replaced. Source ONE
full-size asset, not a sliver cut to the mask's current opening: two slots showing one photo at two
scales bind the SAME URL, differing only by the host layer's scale.

Never take pixels from the reference clip itself as an asset; use what the user supplied, and a
stand-in only when none was.

## Debug heuristic

A styled card shows square edges but sibling cards are fine: suspect THIS asset's alpha (swap the
photo first, the scene second). A masked thing renders tiny or misplaced: mask plus explicit
bounds on one layer (use a boxed aux composition with a bounds-less masked layer inside). Content
invisible at layer start: fade-in or decode timing, start later.
