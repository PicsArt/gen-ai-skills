# Exploded view

A product teardown: a small motor (casing, rotor, coils, shaft, end caps) hangs assembled, separates along its
axis in staggered steps, each part gets a thin leader and a name, and the parts slide home again.

## Palette

Light grey backdrop `#eceff1`, casing `#b0bec5` with shade `#90a4ae`, dark parts `#37474f`, white highlights.
**The hero colour is the motor amber `#e0a63a`, reserved for the part the viewer is meant to study** (the coils);
everything else stays in cool greys.

## The medium

- Parts are flat shapes with one highlight band and one shade band each, no outline, drawn side-on along one
  horizontal axis.
- **Axis guide:** a dashed hairline (length 10, gap 8) through the centre, visible only while the parts are apart.
- **Leaders:** a 2 px line from each part to a label placed above or below, ending in a small dot on the part.
- **Labels:** a condensed face in capitals, dark grey; the studied part's label is amber.

## Motion habits

- **Stagger the pull:** parts leave the centre outwards, each delayed 0.12 s from its neighbour, moving a whole
  multiple of one gap with an ease-in-out (`[0.65, 0, 0.35, 1]`) over 0.9 s, with a slight overshoot at the end.
- **Hold, then label:** dots pop, leaders draw with `trim`, labels are written on with `typewriter`, 0.15 s apart from the centre out.
- **Spin the rotor** while apart: rotation keys looped with `ctx:loopOut("cycle")`, slow, so it reads as a part
  not a blur.
- **Return** in reverse order, leaders and labels leaving first.
- Cued layers use `timeMode: "layer"`.

## Type

A condensed display face in capitals for labels; a title in the top-left corner.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every part moves on the one axis only.
2. Parts keep the same order at every moment.
3. One part is amber and the rest cool grey.
4. Leaders never cross each other.
5. The assembled frame and the fully exploded frame both read.

## Build with the tools

One shape layer per part with position keys that share the same timing offsets; leaders with `trim`; labels as
text layers. Check the exploded frame with `picsart_scene_contact_sheet`.

## Do / don't

- **Do** let later parts start from the exact rest position the earlier ones left.
- **Don't** add perspective, cast shadows or colour on the non-studied parts.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Arrivals: parts slide along the axis, leaders draw on with `trim`, dots pop in by `scale`; labels are written on with `typewriter` 0.15 s apart (the hold-then-label line); hard cuts only.
  - Easing: `[0.65, 0, 0.35, 1]` for the pulls and returns (the return is the same ease reversed), linear for leader
    draw-on and the rotor loop; nothing bounces.
  - True data: the part count equals the label count, one part is one label and one leader that ends on that part;
    the machine is invented, so a small "schematic" tag stays in frame; check leader ends with `picsart_scene_query_layout`.

## Originality guard

Design your own machine. It must not copy a real manufacturer's exploded diagram, a named product teardown
channel's graphics or a patent figure. The one axis, the stagger and the single amber part are the style.

## Proven on

The exploded-view-teardown film (a motor pulling apart along its axis in steps, labelled parts, one amber
coil, the parts returning).

**Not proven:** the written-on labels were shown on three dots, not on an exploded assembly.