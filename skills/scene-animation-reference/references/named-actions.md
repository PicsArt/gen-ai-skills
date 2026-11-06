# Named actions on a placed scene

Use `content.animation` when a scene declares fixed motions in its root `actions` map:
imported Spine bone timelines, Live2D parameter motions, or authored cut-out poses. A
parametric catalog rig's motion presets write host `scene_ref.parameters` bindings;
those are controls, not named actions. Use bindings/presets for live controls, actions for
fixed motions that need mixing, and layer `animations` for the whole rig's travel.

`animations` is a layer field; the action stack is `content.animation`. Root `actions` is
named motions, distinct from `TrackContent.clips`, a sequence of placed content.

An action's `layers[id]` is an `Animations` map. IDs name only the referenced scene's
ROOT layers, never layers inside nested compositions. `parameters[name]` keys a
number, boolean, text, color, vec2 or vec3 parameter declared by that scene. Structural
bindings (paths, assets, lists, animations and clips) are refused as `action_body_invalid`.
Action bodies take time keyframes and the usual easing
and numeric `min`/`max`; no `$eval`, `by` or expressions. Keys start at zero. `duration`
defaults to the last key; give a longer duration for an end hold. Rest is the static
layer transform or the parameter's declared default. If that default is animated,
the action uses its value at time zero as rest: the keyed action replaces the default
track rather than letting it keep running beneath the mix.

`ActionAnimation` (`schema:ActionAnimation`) is the same entry type used by a glTF model: `action`, `trim`, `speed`
(default 1), `loop` (default true), `weight` (default 1, a number or track), `start`,
`duration`, `fade` (default 0, linear ramps at only the explicitly given window edges), and `mode` (`replace` or `aggregate`). A scene_ref with
`animation` refuses its own `trim` OR `speed` (`scene_ref_animation_with_trim`); put
those on each entry. Omitted animation plays the scene's own timeline; an omitted
model animation leaves the model still. Weight keyframes follow the host layer's
`timeMode`, exactly like its other tracks: composition seconds by default on an
ordinary layer, seconds from the effective start with `timeMode: "layer"`. A
sequence clip defaults to layer-local keys; its inherited start is the effective
start. Explicit `timeMode` overrides that default. Weight expressions use the host scope
and host-local time. Entry `start`/`duration` windows and action playback always count
from the host's effective start; `timeMode` changes weight keys, not those clocks.

Per channel, only entries whose actions key it participate. Replace weights normalise
above a sum of 1 within one `tier`; the lower tiers' result fills a sum below 1
(initially static rest). `tier` is a literal integer >= 0, default 0: a tier of the
stack, not a keyframe track. Sparse numbers are fine; tiers evaluate ascending.
After each tier's replace pool, its aggregate entries add their weighted offsets
from their action's pose at `trim.in`, in authored order. The mixed base REPLACES the
layer's own keyframes and `by`/parameter inputs. Its own expression then runs with
that base as `value`, followed by limits, constraints, deformers, skins, draw order
and parenting. Channels no action keys keep playing their own tracks.

For a walking character that aims and shoots without changing its legs, keep the
original full walk action and layer only the keyed arm channels above it:

```json
[{"action":"walk"},
 {"action":"aim","tier":1,"start":3.5,"fade":0.2},
 {"action":"shoot","tier":1,"mode":"aggregate","start":4,"duration":1.9}]
```

A full tier-1 aim replaces only the channels it keys; other channels retain walk.
Crossfade aim→wave together in tier 1. Crossfade walk→idle together in tier 0.
Putting the outgoing and incoming entries in different tiers creates a rest dip:
with weights `1-m` and `m`, the base contribution is `(1-m)^2` and the unwanted
rest contribution is `(1-m)*m`. Put recoil and other aggregates on the top tier
whose replace result they should follow: a full higher replace hides lower
aggregates only on the channels it keys. Do not split walk into derived arm/leg actions.

Numbers, vectors and colours interpolate. `rotation`, `rotationX` and `rotationY`
mix by the shortest arc against the running result, including the rest contribution;
a lone full-weight 0→720 action keeps both turns, and its held end pose does not
unwind during fade-out.
When every action track keying a channel has only `step` segments (including tracks
on currently inactive entries), the channel takes the LAST positive-weight replace entry in ascending tier then
list order immediately: at an explicitly authored start with a positive fade, its weight
is zero, so it does not yet win;
a lone entry at weight 0.25 shows its value fully. Step channels
ignore rest-fill/fade shortfall and skip aggregate entries. The final key's easing
does not affect this classification: it has no following segment. This preserves attachment
swaps and draw-order copies without showing two half-visible attachments.

Two authoring pitfalls: keys closer than one frame merge at the composition fps.
A teleport written as 5.999→6.0 can bend the motion; space keys at least one frame
apart. Place a jumping or reaching rig with `blending: "pass_through"` on its
`scene_ref` to let limbs cross its canvas edge. Under pass_through the frame sizes
and places, it does not clip; fit and bounds still use the scene size. A mask,
effect, content effect, non-normal blend, opacity below 1, motion blur, mesh,
stroke/shadow, adjustment or look on the instance makes it isolated and clipped.
The default remains isolated.

A complete walk→idle authoring pattern (T0 = 2 seconds, fade = 0.25):

```json
{
  "version": "1.0",
  "composition": {"width": 640, "height": 480, "duration": 4},
  "assets": {
    "puppet": {"type": "scene", "scene": {
      "composition": {"width": 640, "height": 480, "duration": 1},
      "layers": [{"id": "hip", "content": {"kind": "empty"}, "transform": {"rotation": 0}}],
      "actions": {
        "walk": {"duration": 1, "layers": {"hip": {"rotation": {"keyframes": [
          {"time": 0, "value": -10}, {"time": 0.5, "value": 10}, {"time": 1, "value": -10}
        ]}}}},
        "idle": {"duration": 1, "layers": {"hip": {"rotation": {"keyframes": [
          {"time": 0, "value": 0}, {"time": 1, "value": 0}
        ]}}}}
      }
    }}
  },
  "layers": [{"id": "actor", "duration": 4, "content": {
    "kind": "scene_ref", "assetId": "puppet", "fit": "none",
    "animation": [
      {"action": "walk", "duration": 2.25, "fade": 0.25},
      {"action": "idle", "start": 2, "fade": 0.25}
    ]
  }}]
}
```

Add painted parts as layers parented to the bones. The outgoing walk keeps advancing
during the overlap. Keep travel keys on `actor.animations.position` and measure the
planted foot. Check it with `picsart_scene_validate`, then render before, inside and after the overlap with `picsart_scene_contact_sheet`.
Unknown names report `action_unknown`, `action_layer_unknown` or `action_parameter_unknown`;
invalid duration reports `action_duration_invalid`. Spine per-vertex deform timelines
are refused as `spine_deform_unsupported`; do not silently discard them.

## Catalog humanoid actions

`scene://rig-humanoid` and `scene://rig-humanoid-front` declare actions: idle, walk (in place), wave, point, talk,
shrug, nod, shake. `rig-face` has none; blink, gaze, breath and follow-through stay drivers. Place the template in
reference mode and play its actions through the `scene_ref`'s `content.animation` as above; the walk stays in
place, so move the body with a host position track (or a ground scroll). A layer that plays its body's actions
stays a reference when `picsart_scene_expand_ref` expands in bulk, and detaching it by layer id is refused as
`detach_plays_actions`.
