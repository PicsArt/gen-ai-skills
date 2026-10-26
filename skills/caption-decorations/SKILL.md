---
name: caption-decorations
description: Author and validate scene caption decorations, choosing between measured procedural decoration presets and arbitrary scene artwork. Use when adding caption highlights, boxes, stickers, animated artwork, custom decoration assets, or debugging why a caption decorator is missing or timed incorrectly.
metadata:
  category: authoring
  version: '1'
user-invocable: false
---

# Caption decoration authoring

Choose the asset form from the behavior, not the visual appearance.

| Need | Declare | Caption row |
|---|---|---|
| Artwork generated from measured word/line geometry | `type: "decoration"` with a procedural shape definition | `preset: "<asset-id>"` plus `params` |
| Arbitrary editable artwork: shapes, text, media, nested scenes, stickers | `type: "scene"` with a scene body | `content.kind: "scene_ref"` |
| External image/video/Lottie/SVG | its ordinary media asset type | `content.kind: "media"` |

`type: "decoration"` is not a general scene container. It is the measured caption-definition language: its `shape` reads `boxW`, `boxH`, optional measured `path`, and declared params. General artwork already has the full scene language through `scene_ref`.

Caption-row `padding`, `size`, `gap`, and `offset` are multiples of the effective caption font em. Platform text measurement still owns x/width, optical centring, and the advance between wrapped lines. Definition-side `boxW`/`boxH` are the resulting decoration box after those row fields are applied.

**Line wrapping** happens at the style's `wrapWidth` (composition pixels) when it sets one, else at the FULL WIDTH of the composition it renders in (no margin). Either width is fixed in PIXELS, never scaled to font size, so a SMALLER font fits more characters before it wraps: shrinking the font can turn two wrapped lines into one wider one, up to that width.

**Generated decoration/segment layer ids share a stem.** A caption segment/decoration gets a `<layer>__seg<i>__dec<d>` stem, so an id containing `__seg0__dec0` belongs to the first segment's first decoration. It is followed by a form suffix (e.g. `__band`, `__stick`, `__bandreveal`, `__pillw<word>`) that is not part of the contract. Select a decoration by its stem or its structure (target/place/row index), never by its full generated id.

## Procedural measured preset

The asset key is the preset name; `decoration.name` may be omitted. Parameters are declared once and read at their actual shape sites.

```json
{
  "assets": {
    "brand_pill": {
      "type": "decoration",
      "decoration": {
        "scope": ["box"],
        "modes": ["once"],
        "parameters": {
          "color": {"type": "color", "default": "#635bffff"},
          "radius": {"type": "number", "default": 0.42, "min": 0, "max": 0.5}
        },
        "shape": {
          "w": {"$eval": "boxW"},
          "h": {"$eval": "boxH"},
          "items": [{
            "type": "group",
            "name": "pill",
            "contents": [
              {"type": "rect", "size": [{"$eval": "boxW"}, {"$eval": "boxH"}],
               "position": [{"$eval": "boxW / 2"}, {"$eval": "boxH / 2"}],
               "roundness": {"$eval": "radius * boxH"}},
              {"type": "fill", "color": {"$eval": "color"}, "opacity": 1}
            ]
          }]
        }
      }
    }
  },
  "layers": [{
    "id": "captions",
    "content": {
      "kind": "captions",
      "style": {
        "decorations": [{
          "target": "line",
          "place": "behind",
          "preset": "brand_pill",
          "params": {"color": "#ff4d8dff", "radius": 0.35},
          "padding": [0.35, 0.18]
        }]
      },
      "transcript": {"segments": [{"start": 0, "end": 2, "text": "Measured artwork"}]}
    }
  }]
}
```

## Arbitrary scene artwork

Use this for a designer-authored composition, including animated shapes, text, media, or nested scenes. Parameters belong to the scene asset's ordinary scene parameter declarations.

A caption decoration `scene_ref` accepts `sceneRef` and optional `parameters`. Do not use layer-level `assetId`, `fit`, or `bounds` fields inside that content object; place and scale the decoration with its caption-row fields such as `size` and `gap`.

```json
{
  "assets": {
    "sparkle_badge": {
      "type": "scene",
      "scene": {
        "composition": {"width": 120, "height": 80, "duration": 1},
        "layers": [{
          "id": "sparkle",
          "content": {"kind": "shape", "items": []}
        }]
      }
    }
  },
  "layers": [{
    "id": "captions",
    "content": {
      "kind": "captions",
      "style": {
        "decorations": [{
          "target": "highlighted",
          "place": "above",
          "content": {"kind": "scene_ref", "sceneRef": "mpscene://sparkle_badge"},
          "size": 0.7,
          "gap": 0.15
        }]
      },
      "transcript": {"segments": [{"start": 0, "end": 2, "text": "Scene artwork"}]}
    }
  }]
}
```

## Emphasis on the glyphs

A `place: "text"` row treats the words themselves. Three recipes compose on one style:

**Glow on the emphasized word.** `effects` on an `emphasized` or `highlighted` text row apply to those words only; the halo sits under the neighbouring words. An effect on every word is the style's own `effects`, so a `line` text row takes none.

```json
{"target": "emphasized", "place": "text", "color": "#ffa800",
 "effects": [{"id": "glow", "params": {"radius": 24, "threshold": 40, "intensity": 1.4}}]}
```

**Word-timed reveal.** `style.reveal` shows only the spoken words: everything spoken so far with `window: "sustain"` (the default), the current word with `window: "active"`. `fade` (seconds) fades each word in as it is spoken. Nothing shows before the first word. Every text row treats the shown words, so a glowing word appears with its word; artwork rows keep their own windows. A text row's own `fade` is only that treatment's crossfade, so "line builds up + current word glows" is a sustain reveal plus one `highlighted` row:

```json
{"style": {"reveal": {"window": "sustain", "fade": 0.12},
  "decorations": [{"target": "highlighted", "place": "text", "color": "#ffa800", "fade": 0.12,
                   "effects": [{"id": "glow"}]}]}}
```

**Stepped lines.** `style.lineStep: [x, y]` (composition px) moves rendered line `i`, counted after wrapping, by `i × lineStep`. Line pills, word boxes and stickers follow the words they decorate.

```json
{"style": {"alignment": "left", "wrapWidth": 560, "lineStep": [56, 0]}}
```

## Scope law

- Asset IDs are local to the scene that declares them.
- Sibling scene assets may reuse the same local decoration ID with different definitions.
- A `type: "scene"` asset starts an independent asset scope.
- A `type: "scene"` asset cannot read parent or sibling assets implicitly. Declare what it needs locally or pass it through a declared parameter.
- An inline `kind: "composition"` body is part of the enclosing scene: it cannot declare its own asset table, and its layers use the enclosing table.
- A document definition cannot shadow a shipped preset of the same name.

## Timing behavior

Do not assume every highlighted decoration slides continuously.

- Media and `scene_ref` highlighted bands slide continuously between measured stops.
- A path-tracked procedural preset owns one measured path schedule. The shipped colour-box treatment holds, then hops to the next stop.
- An ordinary procedural preset is instantiated per stop unless its definition explicitly owns path tracking.
- Above/below stickers hold at one stop, then hop to the next.
- `mode`, `speed`, and `duration` control a preset's internal animation clock; they do not change a path-tracked definition's measured movement schedule.

## Verify before handing off

Use the scene tools through MCP:

1. Call `picsart_scene_validate` with the complete scene and require `valid: true` with no error diagnostics.
2. Render full-resolution stills of both moments in one call: a representative caption
   time `t1`, and a time `t2` where the decoration's movement should have carried it somewhere
   different. Call `picsart_scene_contact_sheet` with `times: [t1, t2, …]` and `resolution` set to the scene's `composition.width` and `composition.height`. Decoration detail is small; full resolution is what shows it. Without `resolution` the sheet returns downscaled thumbnails, which are not for judging position. The sheet image scales every frame to fit one picture; to judge full-resolution detail, open a frame's `url`.

Treat schema validation and the rendered frames as separate checks: a schema-valid declaration can still land wrong once its text is measured and the artwork placed. Inspect the returned images; a successful tool call alone does not establish correct placement.
