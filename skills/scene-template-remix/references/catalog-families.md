# Customize the right catalog family

## Contents

- Shared edit and evidence rules
- Looks: retain a reference until structure must change
- Motion presets: baked tracks are the editable result
- Text animations: entrance baking differs from ambient references
- Transitions: customize one seam, not neighboring clip identity
- Effects: edit operation inputs, not imaginary editable shader layers
- Caption decorations: measured shape versus arbitrary scene artwork

Use the current public schemas, not guessed names or remembered ranges. Call
the listed discovery tool (or `picsart_scene_capabilities` with the named sections), then inspect
the chosen entry. Use its `schema:<Name>` sections when authoring fields directly. Tool inputs below
are request shapes, not complete standalone scenes; `scene` is the assembled document.

| Family | Discover with capability sections | Parameter edit | Deeper instance edit |
|---|---|---|---|
| Looks | `picsart_scene_looks` (`facetsOnly:true` first), then `look:<id>` | `picsart_scene_apply_preset` with `look:<id>`; retune an existing entry's params with `picsart_scene_patch` | `picsart_scene_resolve_looks` for one host, then inspect/patch its generated scene assets |
| Motion presets | `motionPresets` | `picsart_scene_apply_preset` with `motionPreset:<id>` | Edit the emitted animations, transforms, effects or looks |
| Text animations | `textAnimations`, `textAnimation:<name>`, `textAnimationAuthoring` | Named `content.animations[]` entry; entrance baking via `picsart_scene_apply_preset` with `textAnimation:<name>` | Edit baked entrance entries, or declare a unique local text-animation definition |
| Transitions | `transitions`, `transition:<id>` | One track `content.transitions[]` entry | Author a unique local `type:"transition"` asset and retarget that seam |
| Effects | `effects`, `effect:<id>`, `effectAuthoring` | `picsart_scene_apply_preset` with `effect:<id>` | Edit parameter tracks, mask, order or supported effect placement; not the renderer's operation body |
| Caption decorations | `captions` | One caption style `decorations[]` row | Unique local `type:"decoration"` definition, or a scene-ref decoration row |

There is no generic “expand catalog item” operation. In particular, public discovery
does not promise extraction of shipped transition, decoration or effect source. A custom
definition is newly authored behavior, not a verified clone of a shipped implementation.

## Shared edit and evidence rules

1. Keep the original source and read the actual host before edits; page a large one with `picsart_scene_inspect`. Reuse parameters while they express the requested change.
2. Make bounded `picsart_scene_patch` edits using known source addresses. A shared definition affects every reference; give an instance-specific definition a unique id and retarget only its intended consumer.
3. Validate the assembled host and query actual ids/root times. Use supported `picsart_scene_lint_layout` relationships and independent explicit comparisons for remaining intent. Run contract records with `picsart_scene_check_contracts`; do not claim syntax validation proves design intent.
4. Inspect full-resolution `picsart_scene_contact_sheet` with `resolution` set to the composition dimensions, frames before, during and after behavior, including delayed hosts, and watch continuous video for pacing.
5. Compare default, changed-parameter and deeper-edited instances. Confirm the intended target changed and unrelated hosts did not. Record numerical, visual and unverified evidence separately.

## Looks: retain a reference until structure must change

Start with `picsart_scene_looks` with `facetsOnly:true`, then filter by exact `category`, `tags` or `appliesTo` (the full `looks` capability section can overflow a result), then request `look:<id>` for a candidate. Read the returned content restrictions, parameters and roles before applying it. Timing roles are distinct: `in`/`out` are selectable roles, `loop` spans the layer and `static` has no motion. An animated look need not support every role. Filters belong to `picsart_scene_looks`; do not invent filters on the capability tool.

Inspect the selected entry with `picsart_scene_capabilities({sections:["look:<id>"]})`
for full parameter/role details before applying. Existing `looksCompact` and `looks`
capability sections remain available for whole-catalog consumers. The scene-template
`referencePolicy` filter does not apply to looks; use their existing reference,
expand and resolve operations below. Filtering does not prove a look fits the host.

`picsart_scene_apply_preset({scene,layerId,preset:"look:<id>",params,mode:"reference"})` stores a `looks[]` entry.
Read applicability and the entry's supported `fade`, `start`, `duration`, roles and
animatable parameters; not every look supports each. Only parameters declared animatable
accept tracks. Retune the existing entry with a bounded `picsart_scene_patch` edit
of its `looks[]` entry. Applying another look is not a synonym for replacing one.

For deeper editing of an already-styled host, call
`picsart_scene_resolve_looks({scene,layerId})`. This detaches that host's look chain into editable
scene assets while leaving other hosts referenced. Inspect the returned structure before
patching; do not guess generated asset IDs. A repeated host ID across scopes is ambiguous,
not authorization to detach every match. A `look:` preset with `mode:"expand"` also supports
eager baking when initially applying a look; do not reapply a referenced look just to detach it.

Check retained host position/lifetime and subject fit numerically. Inspect corners, padding,
shadow, crop, blend and fade in frames. Geometry does not prove a blur or colour treatment.

## Motion presets: baked tracks are the editable result

`picsart_scene_apply_preset({scene,layerId,preset:"motionPreset:slide_in",params:{duration:0.6,distance:80,direction:"up",fade:1}})`
is an example; discover the current preset before changing it. It emits ordinary scene
animation/transform/effect/look fields, not a persistent preset reference. There is no
separate motion “expand” mode. Resolve template inputs to a concrete scene first if required.

Inspect emitted tracks and ordered transform components. Patch those for custom overshoot,
stagger or trajectory; preserve the base placement and unrelated tracks. Reapplying is not
universally idempotent: overlapping property tracks can replace existing animation and look
outputs can append. Compare the returned revision and diagnostics before keeping it.
For a parameter comparison, apply each variant to the saved pre-preset scene. On an already
baked instance, edit/remove the intended emitted fields instead: setting a new `fade:0`, for
example, need not remove an opacity track emitted by the previous application. The tool
cannot infer which existing animation belongs to that earlier preset.

Query the active window at entrance, intermediate/extreme, settle and exit, using root times
and the host's clock correctly. Check companion motion and containment where intended;
inspect frames for overshoot/clipping and playback for easing. Grouping does not resize a card.

## Text animations: entrance baking differs from ambient references

Named entries go in text `content.animations[]` as `{preset,params}`. Caption word/line
animation uses its own style schema; inspect the `captions` capabilities rather than copying text fields.
`picsart_scene_apply_preset({scene,layerId,preset:"textAnimation:typewriter",params:{duration:1}})` bakes an
entrance animation into concrete content animation entries. It appends entries: applying it
twice can double the animation. Remove or edit the intended entries when retuning.

Ambient presets remain named entries; the baking tool deliberately refuses them. For deeper
entrance edits, inspect the baked selectors and per-glyph tracks. For custom named behavior,
inspect `textAnimationAuthoring`, author a unique local `type:"text_animation"` asset and
point only the intended entry at it. Do not invent a delay parameter: content animation time
is layer-local; use the supported timing fields and preserve the host's visible window.

Validate selectors/tracks and measure text containment after copy changes. Inspect early,
partial-word, settled and exit frames, including a delayed/nested host. Whole-layer boxes
cannot show whether the right glyphs are emphasized, revealed in order or actually painted.

## Transitions: customize one seam, not neighboring clip identity

Use a track's `content.transitions[]` entry `{between,id,duration,params}`; `between` is
the zero-based seam between consecutive clips. For example, a discovered `slide` entry can
use `params:{direction:"left"}`. Change only that firing's params/duration. The transition
window is centered on the cut; validate that it fits both neighboring clips.

For structure beyond parameters, fetch `custom-transitions`. Declare a unique local
asset `{type:"transition",transition:{meta,scene}}` following the current schema, with
exactly one source and one destination slot, and retarget only the chosen seam. Do not
claim a built-in's body was extracted. Its source/destination are neighboring boundary
frames, not arbitrary live playback through the transition. Keep live identity carriers
outside the seam when needed; use `motion-scene-continuity` to decide the relationship first.

Validate the seam and query neighboring clip/track placement at root times. The layout
report may show authored clip geometry rather than the animated transition slots; do not
interpret unchanged boxes as a failed transition, or a clean query as proof of its motion.
Inspect rendered frames just before/after plus 0/25/50/75/100% of the window (sample inside the scene end).
Check coverage, unintended background bleed, direction and clean ownership at both ends.
Test two durations/aspects if claiming independence from them; geometry alone cannot prove
the composited blend. Inspect continuous playback before calling the handoff smooth.

## Effects: edit operation inputs, not imaginary editable shader layers

`picsart_scene_apply_preset({scene,layerId,preset:"effect:<id>",params,mask})` reads catalog types/ranges and supports
tracks only for animatable parameters. For example `gaussian_blur` uses `blur`, not `radius`;
its `fade:0` is full strength and `fade:100` bypasses it. Check the chosen effect, not that example,
for supported masks and required providers. Some style effects do not accept masks.

Reapplying the same effect ID rebuilds that entry using defaults for omitted params and
appends it at the end. To preserve other overrides and effect order, patch the existing
entry instead. Deeper customization means parameter keyframes, a supported mask, order, or
`effects` versus `contentEffects` placement—not expanding the renderer operation's body.

Validate schema/provider availability, then inspect before/after and intermediate frames for
strength, alpha, edge coverage and clipping. For animated parameters check the actual interval.
Layout/contract passes cannot establish blur strength or mask paint. Report missing renderer
support or render failures explicitly; never interpret a silent/no-op picture as successful styling.

## Caption decorations: measured shape versus arbitrary scene artwork

Each caption style `decorations[]` row owns its target, placement and source. A measured
example is `{target:"line",place:"behind",preset:"pill",params:{color:"#173B57"},padding:[0.35,0.18]}`.
Discover each preset's params; row padding/size/gap/offset use font-em units, while wrap width
uses pixels. Changing copy or wrapping changes measured boxes. Not every highlight preset
smoothly travels between words; do not promise a motion behavior from a name.

Fetch `caption-decorations` before deeper editing. Use a unique local
`type:"decoration"` asset for a measured procedural shape (`boxW`/`boxH` are resolved after
row geometry), or `type:"scene"` plus row `content:{kind:"scene_ref",sceneRef:...}` for arbitrary
artwork. Follow the row schema: do not paste visual-layer `assetId`, `fit` or `bounds` fields.
Use `preset` OR `content`, not both. Retarget only the intended row; do not mutate a shared
decoration definition to customize one caption.

Validate the assembled captions and query actual generated IDs, not hard-coded suffixes.
Check padding/containment and wrap collisions numerically. Inspect word boundaries, line
wrap changes, highlighted-target movement and first/last visible words in cropped frames.
A measured box cannot prove highlight paint or synchronization; inspect playback when claiming it.
