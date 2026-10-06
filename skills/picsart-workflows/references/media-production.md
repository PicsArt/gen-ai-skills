# Editable media production

## Route and reuse

Use generation for missing creative material, scene operations for precise assembly/revision, and the dedicated edit tools for background removal, replacement, enhancement, and vectorization. CLI `video-edit` is model transformation, not evidence of deterministic trim/concat. The [interface map](interface-map.md) defines supported routes.

Start from supplied assets, then the [shared Library](drive-library.md) and project references. Carry stable resource IDs, roles, and selected versions throughout the workflow. Use [remote resources](remote-resources.md) for persistence and shared-library publication. A stored URL is not an approval or continuity guarantee.

## Discover detail only when needed

Call `picsart_media_list_recipes` for the native authoring index, then `picsart_media_get_recipe` for the relevant body. Fetch its named companion references only when the selected operation needs them. Current recipes include video editing, photo promos, Figma storyboards, UI motion, gradients, caption decoration, transitions, and motion intent/mechanics/patterns. Recheck the catalog instead of hard-coding its contents.

Discover template IDs and parameter schemas from the live template tools. For common clip merge, start with `picsart_media_quickstart({ recipe: "concat_videos" })`; its example is a complete payload. Use montage for sequential clips, overlapping layers for simultaneous composition. Keep source trim time separate from composition time.

Inspect relevant capability sections only. `generativeTemplates` means parametric layouts, not AI pixel generation. A by-reference template keeps a reusable scene unit; bootstrap produces an editable standalone document; inline adds editable layers to a parent. Catalog defaults and feature behavior can change; preserve the capability build with project state.

## Revision and interactive return

Scene operations take a document and return its successor; the caller owns persistence. Keep the returned scene for every next operation. Patch by stable layer/asset ID using slash-separated paths. Atomic patch failure does not produce a partially updated scene. `valid:true` on the current patch already establishes validation.

Expand scene references (`picsart_media_expand_scene_ref`) before opening `picsart_scene_editor`. Check `stillReferenced` and continue necessary expansion; report unresolved references if the editor cannot open them. The editor returns user decisions through widget context. If the user committed edits, its returned document supersedes the opened version. Comments identify picture/time or timeline intervals. An editor return is not a media export or a remote save.

Expansion leaves HTTP references and track-clip references in place. Inspect the returned unresolved dependency list rather than claiming a self-contained project. Resolved looks do not embed remote media or fonts.

Preserve the original scene revision and resource IDs. When replacing a resource, record affected layers/shot IDs. Preview affected intervals and joins. Keep the accepted source order and unrelated layers when the requested change is bounded.

## Footage analysis and timing

Probe unknown media properties before computing trim windows. Missing duration is unknown, not zero. Visual description, speech transcription, and acoustic analysis serve different questions; do not substitute one for another. Preserve confidence and missing-data notes.

Transcription output fits a captions layer, but trims, reordering, and speed changes need a time mapping. For positive speed: `source = trim.in + speed * (composition - start)`. Map caption times into the final edit and review dialogue synchronization. Speech cut candidates are useful editorial boundaries, not a complete automatic selection policy.

Subject-following reframe returns an editable scene with crop animation. It uses existing pixels and cannot invent missing frame edges. Inspect subjects and important text through the whole crop track. For an existing scene, use the tool's supported scene/layer attachment contract; do not reframe a different source from the one shown in the layer.

Reframe defaults to 30 fps unless supplied. Preserve the intended frame rate and recheck trim, duration, and source identity after attachment. Beat analysis event lists can be capped and subsampled; a reduced list is not a complete beat grid.

Audio analysis supplies beats/tempo/energy with confidence. Request event series only when needed. For uncertain rhythm, use deliberate manual pacing. Scene audio is an ordinary layer with audio content; fades live on its volume animation. Do not invent automatic loudness normalization, speech ducking, or reverse-audio behavior without a supported contract.

## Design and variants

To animate a supplied design, use supplied design data or an available design connector. Paint/path import tools do not fetch a Figma file. Preserve independent layers and measured geometry. Native paint import reports unsupported treatments; flatten only those treatments that need it. SVG path import accepts path geometry, not an entire arbitrary SVG document.

Choose fonts from the current font catalog or supported font asset contract. Plain system family names can fail. Derive motion from the design's order and pose differences; review each beat and join as motion. Still previews cannot show pacing.

For ratio/localization variants, copy the accepted scene, then adjust geometry, framing, and text. Changing output resolution alone does not create a useful new layout. Check line wrapping, fonts, logos, captions, subjects, and safe placement for each target. Retain the master revision and selected resource versions in the variant manifest.

## Film orchestration

Film setup establishes the look before the shotlist board. Use actual widget return data as the current setup/shotlist state. Keep shared references distinct from a project's locked registry. Film asset review and `picsart_save_asset` establish registry locks; only a returned `locked:true` confirms them.

Use the asset prompt compiler for neutral character references and the film prompt compiler for scenic/shot content. Keep compiler receipts and verify literal final generation arguments. If editing compiled text, preserve that change and read the verifier's result rather than claiming the original receipt verifies altered text. Render Monitor shows async progress; preserve original job handles and classify failures before choosing a retry. A host timeout does not mean generation failed.

## Verify, deliver, and retain

Validate direct edits. Geometry queries establish layout, not decoded pixels or audio. Rendered previews inspect visible output. Contact sheets sample pixels at selected times, with at most eight inline samples per call. Use full resolution when judging precise placement. Do not rerender just to obtain missing inline images from a successful preview.

Use motion playback and listening for timing/audio checks. Follow export receipts with the exact named status tool and original job handle. Use returned normal URLs for tool inputs and download URLs for saving. Confirm storage using the actual save receipt; saves can be best-effort.

Deliver the accepted scene/project, source/dependency records, final output references, and validation status appropriate to the request. If remote persistence was requested, include the confirmed project and asset IDs. Keep schemas, geometry checks, sampled stills, playback, export completion, and storage confirmation as separate evidence.
