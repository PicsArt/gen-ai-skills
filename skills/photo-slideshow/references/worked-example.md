# Worked example: a four-photo promo

## Contents

- The scene
- What each part is doing

Four photos, 3s each, on a 1080x1920 frame at 30 fps. Seams: `crossfade`, then `slide` (left),
then `crossfade`, each 0.6s. Clip 2 is a square photo on a `blur_fill`. A title reveals over the
first photo on a gradient scrim. It is an opening card by choice: title and scrim leave before
the first seam's window opens at 2.7s. For a title that stays up for the whole promo, give both
the reel's window. It validates clean, and every frame of the section 8 sweep in the recipe was
rendered from it.

Adapt it by patching, not by re-sending it: swap an `assets` URI (with the probed `width`/`height`),
a clip's `duration`, a transition's `id`/`params`, or the title's `content/text`.

## The scene

```json
{
  "version": "1.0",
  "composition": {"width": 1080, "height": 1920, "fps": 30, "duration": 12, "background": "#000000"},
  "assets": {
    "p1": {
      "type": "image",
      "uri": "https://cdn-template.picsart.com/templates-cdn/37418ba1-c78a-4efe-bc40-879fa243a9cc.jpg",
      "width": 1080,
      "height": 1920
    },
    "p2": {
      "type": "image",
      "uri": "https://cdn271.picsart.com/eeb0e80a-922e-4fa5-8a62-098ccb60b369/507090463024201.jpg",
      "width": 2494,
      "height": 2560
    },
    "p3": {
      "type": "image",
      "uri": "https://cdn271.picsart.com/cb4e8a70-c67a-426c-b4b3-29c8ba6e296f/510780436010201.jpg",
      "width": 2296,
      "height": 4080
    },
    "p4": {
      "type": "image",
      "uri": "https://cdn271.picsart.com/ae9038f4-bb9e-4f67-99b1-2f8b21aaaa80/493136808021201.jpg",
      "width": 2308,
      "height": 3462
    }
  },
  "layers": [
    {
      "id": "reel",
      "start": 0,
      "duration": 12,
      "content": {
        "kind": "track",
        "clips": [
          {"id": "c1", "duration": 3, "content": {"kind": "media", "assetId": "p1", "fit": "cover"}},
          {
            "id": "c2",
            "duration": 3,
            "content": {"kind": "media", "assetId": "p2"},
            "looks": [{"look": "blur_fill", "params": {"blur": 8, "resFactor": 10, "dim": 0.25}}]
          },
          {"id": "c3", "duration": 3, "content": {"kind": "media", "assetId": "p3", "fit": "cover"}},
          {"id": "c4", "duration": 3, "content": {"kind": "media", "assetId": "p4", "fit": "cover"}}
        ],
        "transitions": [
          {"between": 0, "id": "crossfade", "duration": 0.6},
          {"between": 1, "id": "slide", "duration": 0.6, "params": {"direction": "left"}},
          {"between": 2, "id": "crossfade", "duration": 0.6}
        ]
      }
    },
    {
      "id": "scrim",
      "start": 0.5,
      "duration": 2.1,
      "transform": {"position": [540, 1420]},
      "animations": {
        "opacity": {
          "keyframes": [
            {"time": 0.5, "value": 0},
            {"time": 0.8, "value": 1},
            {"time": 2.3, "value": 1},
            {"time": 2.6, "value": 0}
          ]
        }
      },
      "content": {
        "kind": "shape",
        "items": [
          {"type": "rect", "position": [0, 0], "size": [1080, 1000]},
          {
            "type": "gradientFill",
            "gradientType": "linear",
            "startPoint": [0, -500],
            "endPoint": [0, 500],
            "colorStops": [{"offset": 0, "color": "#000000"}, {"offset": 1, "color": "#000000"}],
            "alphaStops": [{"offset": 0, "alpha": 0}, {"offset": 0.5, "alpha": 0.6}, {"offset": 1, "alpha": 0.6}]
          }
        ]
      }
    },
    {
      "id": "title",
      "start": 0.5,
      "duration": 2.1,
      "transform": {"position": [540, 1400]},
      "animations": {"opacity": {"keyframes": [{"time": 2.3, "value": 1}, {"time": 2.6, "value": 0}]}},
      "content": {
        "kind": "text",
        "text": "OUR WINTER",
        "font": {"family": "gilroy-bold", "size": 132},
        "color": "#ffffff",
        "alignment": "center",
        "animations": [{"preset": "fade_in_chars", "params": {"duration": 0.8, "stagger": 0.4}}]
      },
      "effects": [{"id": "drop_shadow", "params": {"offset": [0, 6], "blur": 24, "color": "#000000b3"}}]
    }
  ]
}
```

## What each part is doing

| Layer | Role | Window |
|---|---|---|
| `reel` | the photos, as a track of clips with three seam transitions | 0–12s |
| `scrim` | black gradient under the title, 0 → 0.6 alpha, fading in and out | 0.5–2.6s |
| `title` | `fade_in_chars` entrance from its own start, opacity exit at the end | 0.5–2.6s |

Paint order is array order, later on top, so the scrim sits over the photos and under the title.
