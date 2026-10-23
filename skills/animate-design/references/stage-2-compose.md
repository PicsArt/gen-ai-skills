**Layered means LIVE, not rasterized — a hard requirement.** Text is always a live `text`
layer (font by file URL), never a baked PNG; solid/gradient rectangles, cards, borders, circles
and masks are `color`/shape layers; icons and logos stay **vectors** where supported; a raster
asset is reserved for **true imagery** (photos, videos, textures, or an effect the engine can't
reproduce — disclosed to the designer when baked in). Never flatten a group whose children carry
text or animate independently into one screenshot: a flattened slab can only fade/scale as a whole,
which forfeits every per-element move Stage 3 exists for. The full kind-triage lives in
`references/AUTHORING-FLOW.md` §5.

- **"Upload every asset" means EXTERNAL MEDIA ONLY — it does NOT mean "turn every visual element
  into an uploaded image."** Drive/`upload` applies only to external media files (photos, videos,
  textures, unavoidable raster). **Native scene shapes, vectors, and live text must remain authored
  elements and must never be converted to raster images merely for upload or CSP compatibility.**
  PNG export is a **fallback** for genuine raster content or a truly unsupported vector — not the
  default, and never a way to make a card/component/screen "uploadable." (This is the exact trap that
  produces a rebuilt-from-screenshots frame that diverges from the design.)
- **A CSP/blob failure is fixed by changing ONLY the affected asset's URL or format — never by
  flattening.** Re-host that one image to a Picsart URL (or convert an unsupported vector to a raster
  *for that element alone*); do **not** rasterize the card, component, or whole screen it sits in to
  make the error go away. Flattening to dodge CSP destroys the layering and is a wrong ad.
- **Audit every node's kind BEFORE composing** — shape / vector / text / photo / video — and author
  each as its native kind (above). This layer-type pass is a required step, not optional; skipping it
  is how shapes and text get wrongly baked.
- **If Figma metadata shows no text but the reference visibly has text, STOP and verify the node/
  frame before authoring — do not proceed on the exported assets.** A `get_metadata` call can land on
  the wrong node (a rectangle, a collapsed instance) or not expand the frame's nested tree, returning
  no text for a frame that clearly contains it. That is a signal to re-inspect the full nested
  structure / correct frame node (`get_metadata` on the right frame, `use_figma` for the tree), never
  to reconstruct from the visible screenshots and omit the text. Missing text in the read = read
  again, don't guess.

- **A composed frame must render identical to the static design — proven by comparison, not
  assumed.** Render one `contact_sheet` frame at the frame's hold start and put it **side by side
  with the source** (`get_screenshot` of the Figma frame). Look specifically for **text that
  clipped, wrapped, or shifted** versus the design (the alignment/box traps above), layers that
  landed off-position, and wrong z-order. Skipping this compare is how a mispositioned or
  wrapped headline ships — it is a wrong ad, cheaply caught now.
- **Compose one frame, PREVIEW it, and wait for the designer before the next — never
  batch-compose the storyboard.** After each frame is composed, actually **render it and show it**
  (the `contact_sheet`/editor still beside the source) and let the designer confirm it before
  you compose the next frame. The preview is a **hard precondition to advancing, not a formality
  you narrate past**: proceeding on your own "it should match" judgment — *without having rendered
  and shown the frame* — is the skipped-preview failure, the same one the pair rhythm below exists
  to prevent. If you catch yourself *describing* a frame instead of *showing* it, stop and render
  it. The designer should never have to ask you to preview — and the reverse holds too:
  **never ask the designer for a go-ahead to render.** A free render (`validate_scene`,
  `contact_sheet`, the editor panel) needs no permission — run it, show the result, and let
  the designer react to what they see. "Approve the render when it pops up" / "say go and I'll
  run it" is a dead turn where the result should already be on screen.
- **You do NOT have to compose the whole storyboard before any motion — compose and motion
  INTERLEAVE per pair.** The stage table lists Compose (2) before Motion (3), but that is the order
  *for a given frame*, not a barrier across the whole reel. The rhythm: **compose frame 1 → animate
  frame 1's opening beat → then, for each pair, compose the next frame only when its pair comes up, and
  motion it.** Composing every frame first and only then starting motion both **delays the motion the
  designer is waiting to see** and contradicts *"open with frame 1's entrance before pair 1→2"* (Stage
  3). Rebuild just-in-time, pair by pair.
- **Matched elements stay one continuous layer across the frames they appear in**, keyed
  by `matchKey` from import — that is what lets Stage 3 smart-animate them rather than
  cross-dissolve. A header present in frames 1–4 is *one* layer with four transform
  states, not four separate headers.
- **Duration is derived by default; an explicit target is opt-in and soft.** By default
  (`duration.mode: "derived"` — the console's checked box) the total is `$sum` of the
  holds, each grown to fit its own motion (a 1.2s type-on needs a hold ≥ 1.2s), so it
  *grows as motion is added*. A designer may instead set `duration.mode: "target"` with a
  length — a **soft budget**: holds scale toward it where there is slack, but never below
  each hold's motion-minimum, so a too-short target **lengthens** the video rather than
  clipping an animation. Never silently clip motion to hit a number; a target the motion
  overflows is shown, not enforced.

- **Every asset URL in the scene must be Picsart-hosted (`pastatic`/`gcdn`) — never a `figma.com`,
  `data:`, or `blob:` URL.** A Figma `get_screenshot` returns a `figma.com/api/mcp/asset/…` URL and
  browsers hand you `blob:` object URLs; **do not author either into the scene.** First lift every
  image to a durable Picsart URL with `picsart_drive_upload_ask` (or `picsart_drive_upload`) and author *that*.
  The catch: server-side `export`/`contact_sheet` **can** fetch `figma.com`, so they render fine and
  hide the problem — but the browser preview's Content-Security-Policy blocks these hosts
  (`csp: blocked connect-src … figma.com`, `csp: blocked img-src … blob:`), so the layer goes blank
  or the engine fails. **Validation and a clean contact-sheet are NOT proof it loads in the preview.**
  Fix a blocked scene by re-uploading the offending assets and `patch_scene`-ing their `uri` to the
  Picsart URLs. (Full detail: `references/AUTHORING-FLOW.md` §5.)
- **A text layer's font is a catalog key, the entry's resolved `.ttf`/`.otf` file URL from `picsart_scene_fonts`
  (or an `assets[]` `{ type: "font", id, uri }` entry carrying it) — never a family name ("Inter").**
  A catalog `key` ("gilroy-semibold") or URL passes `validate_scene` and renders on `export` and
  `contact_sheet`; both also open in the scene editor, where the designer reviews it. A font URL
  must use HTTPS on `picsart.com` or a `*.picsart.com` host to load there. Any other name fails `validate_scene` as `unknown_font_family`; follow its hints.
  If the editor stops on a scene, the panel says so and offers to export the scene as opened. Match
  the design's typeface to a catalog entry, then author that entry's **key or URL**.
- **A text layer carries the design's real horizontal alignment and box behaviour — never a
  guessed one.** Author the `alignment` Figma actually set (`textAlignHorizontal`), because the
  anchor follows it: a **left**-aligned layer's `position.x` is the box's **left edge**, a
  **center**-aligned layer's is the box **center**. Defaulting a headline to `center` (and so to a
  center-of-box x) is the classic tell — it drags left-aligned copy off toward the middle/right.
  And if Figma's text sits in a **fixed-width box that overflows the frame**, it **clips** there;
  a scene text layer with only a point anchor + font size will instead **soft-wrap** the overlong
  line at the space. Carry the box width (so it clips like the design) or drop the font size so the
  single line fits — never let it silently wrap to two lines.
- **A missing font is surfaced, never silently swapped.** For every text layer, check its
  typeface against `picsart_scene_fonts` (the platform's available fonts; its `query` also
  live-searches a font not in the bundled snapshot and returns a `.ttf`/`.otf` URL you author directly). If the
  design's font is **not available from the media tools** — neither tool can find it — do
  **not** quietly substitute a fallback and move on. **Tell the designer plainly**: name
  the missing font, name the fallback you'd otherwise use, and say the text will render in
  that fallback (different metrics → the layout can shift). Let them decide — pick an
  available font, supply/upload the font, or accept the fallback knowingly. A silently
  swapped font is a wrong ad that reads as "close enough" until someone notices.

Then `picsart_scene_validate` — free, catches schema errors before any render is
spent on a broken scene.
