# Scene tools

Read before the first `picsart_scene_*` call.

**`picsart_scene_capabilities` answers by section, and only to exact section names.** Called
with no arguments, it returns just the index: every section name, and the size of the large ones.
Pass `sections` with names from that index, or the ones a skill gives: `easing`, `motionPresets`,
`textAnimations`, `transitions`, `effects`, `mask`, `limits`, and `looksCompact` to choose a look,
then `look:<id>` for that one look in full. Never make a name from a word in the text: `easings`
and `presets` are refused, and one wrong name fails the whole call. Never pass `["all"]`, because
the whole document overflows the context; ask for a large section (`effects`, `looks`, `supports`)
in a call of its own. When a call is refused, its error lists the valid names: take the name from
there. Pass `detail: "full"` when reading catalog parameter prose.

**Probe a source before sizing around it.** `picsart_media_probe` gives a source's size and
duration to size a composition, choose `fit`, set clip windows or check that an asset matches the
scene. It reads PNG/JPEG/GIF/WebP/HEIC/AVIF/SVG/TIFF dimensions, mp4/mov/m4a dimensions and
duration (moov-at-end files too), and a Lottie's frames and length up to 256 KiB. A fragmented MP4
or streaming upload has no duration in its header; the probe walks its fragments with a few more
small reads and usually recovers it. Skip the probe when an earlier result (a generation's own
response, say) already gave the exact numbers.

**Look with a contact sheet at moments you choose.** Pass `times` at the moments that matter:
clip seams, animation midpoints, entrance ends. Use `frames` only for an even pass over the whole
timeline. Every frame is a real render, so never sample frames to find a clip's duration unless
`picsart_media_probe` could not determine it.

**What `picsart_scene_expand_ref` brings across.** A caller asset or composition bound into the
ref's scene arrives as a copy of the caller's declaration, never its id: inline (`content.asset`)
for a clip, a prefixed entry for an `asset_*` parameter. The caller's own assets stay; a scene
asset nothing names any more is dropped. A ref that stays a layer keeps the scene's size, `fps`,
`duration` and sample count on `content.composition` (`bounds` stays on `content`), and its
layers keep their own times. Track clips stay as they are. Only what the call reads must be valid:
the ref layer, its scene, what is bound into it, and the compositions holding it.

**A scene can travel by URL.** `picsart_scene_patch`, `picsart_scene_expand_ref` and
the three `apply_*` tools take `returnSceneUrl: true`: the result then names the edited scene by its
`sceneUrl` instead of carrying it. Pass that URL on as the next call's `scene` where its schema
takes a URL, and as `sceneUrl` to `picsart_scene_editor`. Leave it off when you need to read the
scene yourself, or when the next tool takes only the document.
