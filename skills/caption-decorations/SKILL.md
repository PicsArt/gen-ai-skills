---
name: caption-decorations
description: Author and validate scene caption decorations, choosing between measured procedural decoration presets and arbitrary scene artwork. Use when adding caption highlights, boxes, stickers, animated artwork, custom decoration assets, or debugging why a caption decorator is missing or timed incorrectly.
metadata:
  category: authoring
  version: '1'
  ported-from: caption-decoration-authoring 1 at 55.128.2
user-invocable: false
---

# Caption decoration authoring

Choose the asset form from the behavior, not the visual appearance.

Read the captions reference by part, not whole: `picsart_scene_capabilities` with `sections: ["captions:decorations"]` (a pick list of the presets, each parameter as `name: type`), then `["decoration:<name>"]` for one preset whole; `["captions:rules"]` for the row, place and window rules; `["captions:styles"]` for the style presets. `["captions"]` is all of them (about 28K, `detail: "full"` 40K).

| Need | Declare | Caption row |
|---|---|---|
| Artwork generated from measured word/line geometry | `type: "decoration"` with a procedural shape definition | `preset: "<asset-id>"` plus `params` |
| Arbitrary editable artwork: shapes, text, media, nested scenes, stickers | `type: "scene"` with a scene body | `content.kind: "scene_ref"` |
| External image/video/Lottie/SVG | its ordinary media asset type | `content.kind: "media"` |

`type: "decoration"` is not a general scene container. It is the measured caption-definition language: its `shape` reads `boxW`, `boxH`, `em` (the caption's font size, for artwork sized by the type: a header label that should not grow with the line count), optional measured `path`, and declared params. `em` is reserved, so a def cannot declare a param of that name. General artwork already has the full scene language through `scene_ref`.

Set the caption size with `style.font.size` (composition pixels); left out, it is the text default, small on a tall frame such as 1080x1920. Caption-row `padding`, `size`, `gap`, and `offset` are multiples of the effective caption font em. Platform text measurement still owns x/width, optical centring, and the advance between wrapped lines. Definition-side `boxW`/`boxH` are the resulting decoration box after those row fields are applied.

**Line wrapping** happens at the style's `wrapWidth` (composition pixels) when it sets one, else at the FULL WIDTH of the composition it renders in (no margin). Either width is fixed in PIXELS, never scaled to font size, so a SMALLER font fits more characters before it wraps: shrinking the font can turn two wrapped lines into one wider one, up to that width.

**Generated decoration/segment layer ids share a stem.** A caption segment/decoration gets a `<layer>__seg<i>__dec<d>` stem, so an id containing `__seg0__dec0` belongs to the first segment's first decoration. It is followed by a form suffix (e.g. `__band`, `__stick`, `__bandreveal`, `__pillw<word>`) that is not part of the contract. Select a decoration by its stem or its structure (target/place/row index), never by its full generated id.

A segment of a stacked style (below) draws one text layer per run instead, `<layer>__seg<i>__run<N>` (N from 0 in reading order), a stressed run `<layer>__seg<i>__run<N>__stressed`, and each run's decorations stem from its own id: `<layer>__seg<i>__run<N>__stressed__dec<d>`.

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
        "font": {"family": "default", "size": 72},
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

**Marks over the words.** `place: "over"` draws the box a `behind` row would draw, under every `behind` rule (`padding`, the windows including `grow`, `lead`, `box`-scope presets), on the plane above the text: a pen circle, strike-through or underline that crosses the glyphs. Rows on that plane stack in array order with the `above`/`below` stickers. An `over` row is never the box a sticker's `gap` measures from; that stays the last `behind` row on the same target.

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
          "content": {"kind": "scene_ref", "sceneRef": "scene://sparkle_badge"},
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

Effect params may be keyframed, and their `time` is the clock of the layer they land on, never the captions composition's: 0 where each segment appears for the style's `effects` and a text row's, 0 where its own layer appears for an artwork row's. One list (a `channel_shift` decaying over 0.4 s) serves every caption; do not shift keys by a segment's start.

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

**Words that enter as they are spoken.** A `highlighted` or `emphasized` text row may name an ENTRANCE text animation with a `window` (`active` or `sustain`), its `params`, and optionally a `color`, `effects` and a `lead`, which ride the same per-word windows. `lead` (seconds, >= 0) opens each word's window that much before its onset, never before the layer, so the entrance is under way as the word is spoken; only the opening moves, and an `active` window still closes on time. A `lead` on a row with no entrance preset is refused, and under `reveal` the led seconds play hidden, so a led row wants `reveal: false`. Colour and effects: each word takes the colour from its onset (an entrance that animates colour composes over it), and the effects' clone holds each word over its own window, so a halo lights with its word. Each word the row treats plays it on its own word selector, its keys moved to that word's onset on the segment layer's clock (a run's own on a stacked segment: a stressed word is keyed from its run's start), never fitted to the segment. `sustain` keeps each word entered; `active` drops it back at rest when its window closes (the next word's onset on `highlighted`, the word's own end on `emphasized`). A selector that takes the whole text (`shape: "square"`, `start` 0, `end` 1) is replaced by the word's, its motion in keyed transforms. A selector that moves within the word (by character or word, shape `square`, `triangle`, `round` or `smooth`, `start`/`end` between 0 and 1, no `offset`, no random order; a ramp, or an absent shape, which is a ramp, would reach past the word), such as `typewriter`, is laid onto that word's own characters and keyed from its onset, so each word types itself out as it is spoken; it needs `window: "sustain"`, since it plays out over its own keys. Anything else is refused (`captions_invalid_decoration`). Before its window a word is at rest, so pair it with `reveal` to hide words until they are spoken; both switch on the same key. A finale spring, declared as the document's own entrance:

```json
{"assets": {"spring_in": {"type": "text_animation", "textAnimation": {"kind": "entrance", "entries": [
   {"transform": {"kind": "scale", "value": {"keyframes": [{"t": 0, "v": 0.4}, {"t": 0.3, "v": 1}]}},
    "selector": {"basedOn": "word", "start": 0, "end": 1, "shape": "square"}},
   {"transform": {"kind": "offset", "x": 0, "y": {"keyframes": [{"t": 0, "v": 40}, {"t": 0.3, "v": 0}]}},
    "selector": {"basedOn": "word", "start": 0, "end": 1, "shape": "square"}},
   {"transform": {"kind": "opacity", "value": {"keyframes": [{"t": 0, "v": 0}, {"t": 0.12, "v": 1}]}},
    "selector": {"basedOn": "word", "start": 0, "end": 1, "shape": "square"}}]}}},
 "style": {"reveal": {"window": "sustain"},
  "decorations": [{"target": "highlighted", "place": "text", "preset": "spring_in", "window": "sustain"}]}}
```

**Stepped lines.** `style.lineStep: [x, y]` (composition px) moves rendered line `i`, counted after wrapping, by `i × lineStep`. Line pills, word boxes and stickers follow the words they decorate.

```json
{"style": {"alignment": "left", "wrapWidth": 560, "lineStep": [56, 0]}}
```

**Tracking.** `style.letterSpacing` (composition px: a number, or keyframes where nothing is measured, below) is each segment's text `letterSpacing`. Lines wrap with it and every box, word rect and sticker is measured with it, so a pill behind widely tracked words widens with them. A variant's value replaces the base's:

```json
{"style": {"letterSpacing": 2}, "styles": {"whisper": {"letterSpacing": 14}}}
```

Tracking may be keyframed (`{"keyframes": [{"time": 0, "value": 0}, {"time": 0.4, "value": 12}]}`) on each segment's own clock, but only where nothing is measured: the effective style of every segment the layer draws (base plus all its tags' variants) may carry `place: "text"` and `place: "frame"` rows and no others, and no `lineStep` (else `captions_invalid_style`). It is layer-wide: the whole segment spreads, so a stressed word that should open out alone is its own segment, or its own run (`emphasized.letterSpacing` on a stacked style, below), judged on the run's own style.

**Alternating captions.** `style.cycle` (base style only) lists `styles{}` variants laid over the segments in turn: segment `i` of the transcript, in authored order, takes `cycle[i % cycle.length]` over the base, and its tags' variants still lay over that. So captions alternate (`"cycle": ["pink", "cyan"]`) with nothing in the transcript asking for it. A name that is no variant is `captions_unknown_style_ref`; a variant setting `cycle` is `captions_invalid_style`.

## Named caption styles: `stylePreset`

A captions content may name a caption style by id instead of writing its look out: a shipped one (the `caption_style` catalog, each `{meta, style, styles?, tagStyles?}`) or a `type: "caption_style"` asset the scene declares (`{"type": "caption_style", "captionStyle": {style, styles?, tagStyles?}}`, its id the asset key). The style lies UNDER the content's own before any segment is styled or measured: its `style` fields first and the content's over them (each field whole, so a content `font` replaces the preset's whole `font`); its `styles` and `tagStyles` beside the content's, the content's entry winning by name. So `{"stylePreset": "sample_bold"}` alone draws the preset, and every field written beside it is an override:

```json
{"kind": "captions", "stylePreset": "sample_bold", "style": {"color": "#FFD400"},
 "styles": {"loud": {"font": {"family": "default", "size": 96}}}, "tagStyles": {"tone:loud": "loud"}}
```

A preset's own `tagStyles` name only its own `styles`. An id nothing answers is refused by name (`captions_unknown_style_preset`); a declared style that collides with a shipped id, or that the catalog's law refuses, is `caption_style_asset_def`. `meta` (`id`, `displayName`, `description`, `category`, nothing else) is the gallery's and takes no part in resolution.

**A style's faces are the document's to declare.** A style names each face by id and carries no file; the listing's `fonts` gives the ids, every `font.family` the style and its variants name. The document using the style declares each as a font asset, `"assets": {"anton": {"type": "font", "uri": "https://…/Anton.ttf"}}`, unless the font catalog already has it (`arial-bold`). An id names one file. A static id carries its weight and style in the id (`jetbrains-mono-600` is JetBrains Mono SemiBold): point it at that static file. A `-variable` id (`inter-variable`, `fraunces-variable-italic`) names a variable font, drawn at the style's numeric `font.weight` and, where pinned, its `font.opticalSize`: point it at the variable file, never a static instance, which draws one weight whatever the style asks. Resolution is strict: a face that resolves nowhere refuses the layer, `captions_preset_font_unresolved`, naming the style, the font and the layer, even when only a variant no segment draws names it. No default face stands in. A shipped style never names a face by URL.

**The shipped signature styles.** `directors_cut` (per segment at most one tag, `tone:lilting|whisper|shout|soft|emphatic|mechanical` or `role:finale`, none for a plain line, and the stressed words in `emphasize`: small plain runs around a stressed run two to five times larger in its own face (`stacked`), frame rows for the lower shade, the whisper's dim and lean-in and the shout/punch flash and shake, a shockwave on the punch, word-onset entrances, exits and a hold; the `role:finale` stressed run draws in front of the person, a gradient and drop shadow on its own `emphasized.effects`), `pop` (`tone:shout|whisper`), `depth` (the read-along line) and `depth_words` (the one emphasized keyword fitted to 92 % of the frame, behind the person through the same backdrop mask, for a second captions layer beneath a `depth` one; its plain runs are `visible: false`; `tone:soft|whisper` turn it to an italic serif). The behind-the-person mask is `remove_segment` with `{"provider": "portrait", "segments": ["person"], "source": "backdrop"}`, never `invert`: where no person segmentation runs it removes nothing and the words draw in front. The mask has two homes on captions and takes the same way in both: a stressed run's own `effects` (the `emphasized` slot under `stacked`: the run stands behind the person) and an `emphasized` text row's `effects` (`{"target": "emphasized", "place": "text", "effects": [...]}`: the marked words stand behind the person inside the line). Either makes the captions layer a size-less pass-through group whose `__text` composition passes through too (a sized one would read an empty canvas), and either is refused as `captions_frame_row_isolated` where the captions layer draws on a canvas of its own (`effects`, `mask`, `looks`, a non-normal `blendMode`, an opacity below 1, motion blur where samples are allotted). A shade beneath it belongs in `"blendMode": "multiply"` (frame rows, below), so it does not thin the cut. Their faces are ids (the listing's `fonts`; `directors_cut` names eleven); the app declares them as font assets whose URLs are Google Fonts and the Picsart CDN
,
.

**The shipped catalog styles.** Faces by id as above; each draws its marks on the segment's `emphasize` words (one contiguous run of one or two) and reads the segment's one `tone:*` / `role:*` tag where it maps one:
- `tape_97` (a worn VHS: a vhs grade and a glitch burst at each caption on a held frame row, `channel_shift` on upper-case VT323 closed captions on black word blocks that build as words are spoken; `tone:shout` glitches harder, `tone:whisper` greys the type)
- `red_pen` (clean Inter Tight that lifts in word by word, then an editor's marks on the stressed words: a 90 % yellow highlighter with dark ink; `tone:shout` a red circle, `tone:emphatic` a red box, `tone:lilting` and `tone:soft` a red underline, `tone:mechanical` a red strike-through, `tone:whisper` lilac dots, `role:finale` the highlighter plus a yellow underline)
- `comic` (upper-case Bangers in a `speech_balloon` with its tail up, each word springing in as it is spoken; `tone:shout` and `tone:emphatic` burst out of a `comic_burst` in red at 112 px, `tone:whisper` dashes the balloon and fades every word but the stressed one)
- `silent_film` (a toned, grainy, weaving black-and-white print on a held frame row; Playfair Display fading up word by word on a fixed black intertitle card with a double cream rule, a frame-row shape; the stressed words in Limelight on a stacked line of their own; no tags)
- `label_maker` (embossed-looking Rubik Mono One typed out onto one label tape that grows with the spoken words, red by default; `tone:shout` black tape, `tone:whisper` blue, `tone:emphatic` green; for 1-3 word captions, as a wrapped caption tapes only its last line)
- `board` (a departures board: Barlow Condensed SemiBold in split-flap `flap_tile`s on a `board_panel` with a header plate sized from `em`, each tile flipping in on its word's onset through a text row's entrance `lead`; `reveal: false` keeps the words up while the flaps lead in; no tags)

**Case.** `style.textCase` `"upper"` / `"lower"` / `"none"` draws and measures every segment in that case (a text layer takes the same field); a variant's replaces the base's. Only the characters change: `words[]` and `emphasize` keep indexing the same words, and the transcript is never rewritten. Unicode full case mapping, one character at a time and locale-free ("ß" → "SS"; no Turkish dotless i).

## Word slams: the glyph pivot

`style.animationPivot` picks what every glyph animation of a segment turns and scales about: `"character"` (the default, each letter on its own centre) or `"word"` (each word as one piece, about its horizontal centre ON the baseline). A text layer takes the same field on its content. A variant with it replaces the base's, and every segment layer and glyph clone carries it.

**Word slam.** Each word lands from 3.2× as one piece. An `anchor` entry nudges the pivot in fractions of the word's box, so `y: -0.35` slams about the word's vertical middle instead of its baseline:

```json
{"style": {"animationPivot": "word", "animation": [
  {"transform": {"kind": "scale", "value": {"keyframes": [{"t": 0, "v": 3.2, "easing": "ease_out"}, {"t": 0.4, "v": 1}]}},
   "selector": {"basedOn": "word"}},
  {"transform": {"kind": "anchor", "x": 0, "y": -0.35}, "selector": {"basedOn": "word"}}]}}
```

**One pivot per glyph.** A `"word"` pivot cannot share a segment with a `place: "text"` row whose preset scales or turns letters about themselves: validation and resolution refuse it as `captions_animation_pivot_conflict`. That is decided by what the row's preset lowers to, not by its name: `throb` (a scale) and `sway` (a turn) always conflict; `transform` conflicts only with non-zero `degrees`, and with only `x`/`y` it just moves glyphs. A document's own ambient preset counts the same way, and so does a word-onset entrance row: a spring that scales each word's glyphs conflicts, a lift that only moves them does not. Put the word slam and the letter wobble on different segments (tag variants), or drop one. The style's own `animation` entries are never refused, but under `"word"` an entry that scales or turns letters one by one (`basedOn: "character"`) turns each letter about its word: use `"character"` for a letter spring. Rows that only recolour, move or fade glyphs (`color`, `hop`, `drift`, `flicker`, …) are fine beside it. The pivot moves glyphs only: the measured segment box, and every artwork row placed from it, is the same either way. On a text layer, a `"word"` pivot does not work along a `textPath`: it is refused as `animation_pivot_on_text_path`.

## Stacked runs: plain and stressed

`style.stacked: true` splits each segment that marks words (`emphasize`) into stacked lines, one per run: each stretch of contiguous marked words is a stressed run, and the words between them form plain runs, so "But a voice is never flat." marking `never flat.` draws "But a voice is" over "never flat.", and two stresses apart draw two stressed lines. Punctuation stays with its word. A segment without `emphasize`, or a style without `stacked`, draws as one line, exactly as before.

The plain runs draw in the style itself (its base fields, a variant's over them). The `emphasized` slot styles the stressed runs: it lays its own `font`, `color`, `letterSpacing`, `effects`, `animation`, `exit`, `stroke`, `wrapWidth`, `textCase` and `reveal` over the style (whole value per field). The split reads the authored words, then each run is cased in its own style.

The runs stack by their measured heights and the block is centred where the one line would be (`offset`), so a stacked caption is always measured. `gap` (composition pixels) is the space below a run, before the next one: the style's `gap` below each plain run, the slot's `gap` below each stressed run, so the space above a stress and the space below it can differ. `visible: false` (on the style for the plain runs, on the slot for the stressed ones) draws nothing and takes no place (no height, no gap, never measured), so a keyword layer drawn beside a read-along one hides its plain runs and its stress stands alone on the offset. A run without a `wrapWidth` wraps, and is measured, at the composition's width.

A plain run spans the segment. A stressed run starts at its first word's onset (`words[]`), so its entrance plays there; the slot's `lead` (seconds, >= 0) opens it that long before the onset, never before the segment, as a decoration row's `lead` is clamped, so a slam is already landing when the word is spoken; its words are still revealed, highlighted and entered at their own onsets, and its exit still runs from its end. The slot's `reveal` replaces the style's on the stressed runs, and `false` lifts it, so their words show for their layer's whole life. A style or `styles{}` variant takes `reveal: false` too: a variant that writes it shows its segments' whole captions at once, under a base style that reveals word by word. A led run needs `reveal: false`, or the style's reveal hides its word until the onset and the slam plays unseen. `emphasized` rows treat the stressed runs; `line` and `highlighted` rows, and `reveal`, treat each run's own words; a segment's `frame` rows are the segment's, drawn once.

`emphasized.fit: "width"` sizes each stressed run so its one line fills its column (the slot's `wrapWidth`, else the composition's width), capped at `maxSize`:

```json
{"style": {"font": {"family": "Inter", "size": 52}, "offset": [0, 420], "stacked": true, "gap": 13,
  "emphasized": {"font": {"family": "Anton", "size": 160}, "color": "#ffe8cf",
                 "fit": "width", "wrapWidth": 972, "maxSize": 320}}}
```

## Exits and hold

`style.exit` takes the same entries as `animation` (preset references or raw entries), keyed from the END of each layer the segment draws (its text layer, every run's, every glyph clone): a key at `t` sits at `end - t`, so an entry whose keys span `[0, d]` runs over `[end - d, end]`, played backwards. An entrance preset leaves the way it came in (`{"preset": "fade_in_chars", "params": {"duration": 0.3}}` fades the characters out, last first); a raw exit is written as the entrance it reverses. Easing is mirrored with each span (`ease_in` and `ease_out` trade places). An exit longer than the layer is compressed to it on its own, never into the entrance, and it composes with the entrance: each exit entry selects no glyph before its own first key, so a fading entrance paired with an opacity exit still fades. It is the captions' counterpart of a look's `role: "out"`. An `expression` or a `step` key cannot be played backwards and is refused (`captions_invalid_style`). Variants and the `emphasized` slot carry their own `exit`, whole value like `animation`.

`style.hold` (seconds, base style only) keeps each segment up through the pause after it: its layers end at the next segment's start, at most `hold` seconds past its own end, never past the captions layer's end. The last segment ends as before. Everything timed to the segment's end reads the held end: the exit runs there, `segment`/`sustain` windows and a highlighted word's box stay up with the text as it was when spoken, `reveal` keeps its shown words, a stressed run ends with the rest. A fade-and-drift exit over a short-gap hold:

```json
{"style": {"hold": 0.6,
  "exit": [{"transform": {"kind": "opacity", "value": 0},
            "selector": {"basedOn": "character", "start": 0, "end": 1, "shape": "square",
                         "offset": [{"t": 0, "v": 0}, {"t": 0.25, "v": 1}]}},
           {"transform": {"kind": "offset", "x": 0, "y": -12},
            "selector": {"basedOn": "character", "start": 0, "end": 1, "shape": "square",
                         "offset": [{"t": 0, "v": 0}, {"t": 0.25, "v": 1}]}}]}}
```

**The whole caption moving as one piece.** `style.motion` moves everything a segment draws (its box and sticker artwork, glyph clones and text, every run of a stacked segment) together, turning about the caption's centre (the composition centre moved by `offset`; `anchor` nudges it, pixels). `in` and `out` key `offset` (`[x, y]` px), `rotation` (degrees clockwise), `scale` (a uniform factor) and `opacity` as `[{"t": seconds, "v": value, "easing"?: ...}]`. `in` is keyed from each segment's start; `out` from its held end, written as the entrance it reverses, as `exit` is. Each is compressed to a short segment on its own, and where they overlap the exit wins. It lowers to one size-less pass-through group per segment (`<seg>__motion`; frame rows stay outside), which draws on a canvas of its own while its opacity is below 1, so the caption fades as one piece. A variant's `motion` replaces the base's; the `emphasized` slot takes none. A label that drops off in its last 0.22 s:

```json
{"style": {"motion": {"out": {
  "offset":   [{"t": 0, "v": [0, 260], "easing": "ease_in_out"}, {"t": 0.22, "v": [0, 0]}],
  "rotation": [{"t": 0, "v": 17.2, "easing": "ease_in_out"}, {"t": 0.22, "v": 0}],
  "opacity":  [{"t": 0, "v": 0, "easing": "ease_in_out"}, {"t": 0.22, "v": 1}]}}}}
```

## The picture under the captions: `place: "frame"`

A `place: "frame"` row draws a full-frame layer beneath every caption's text for its window: the segment on `target: "line"`, a marked word's on `emphasized` (`active` / `sustain` / `segment`), each spoken word's on `highlighted` (`active` / `sustain`). Windows that overlap are drawn as one layer (a two-word `sustain` opens once, at the first word). It takes `content` — `{"kind": "color", "color"}` (a wash) or `{"kind": "shape", "items"}` (items about the frame centre) — or a `preset` with its `params`: a `box`-scope definition fitted to the FRAME as a `behind` row's is fitted to the text box, so a gradient shade fits every resolution (not both). And/or `adjustmentLayer: true` with `effects`, which grade the picture beneath the captions layer. Nothing is measured for it. Effect keyframes read on the row layer's own clock, so a flash decays and a shake settles from the word's onset; `motion_tile` at 104 % hides the edges a shake reveals:

```json
{"styles": {
  "whisper": {"decorations": [{"target": "line", "place": "frame", "adjustmentLayer": true, "effects": [
    {"id": "adjust", "params": {"exposure": -0.45}}, {"id": "vignette", "params": {"size": 70}},
    {"id": "motion_tile", "params": {"tileWidth": 104, "tileHeight": 104}}]}]},
  "shout": {"decorations": [{"target": "emphasized", "place": "frame", "adjustmentLayer": true, "effects": [
    {"id": "motion_tile", "params": {"tileWidth": 104, "tileHeight": 104, "mirror": true,
      "centerX": {"keyframes": [{"time": 0, "value": 0.53}, {"time": 0.1, "value": 0.48}, {"time": 0.8, "value": 0.5}]},
      "centerY": {"keyframes": [{"time": 0, "value": 0.48}, {"time": 0.1, "value": 0.515}, {"time": 0.8, "value": 0.5}]}}}]}]}}}
```

With a frame row on any drawn segment, the captions layer composites as a size-less `blending: "pass_through"` group: the frame layers (`<seg>__dec<d>__frame`, `…__framew<k>` for a window opening on word k), then the captions' own composition (`<layer>__text`). The group shares the layer's transform, so a moved, scaled or turned captions layer moves the frame with it. A stacked segment draws its frame rows once, not per run (an `emphasized` window is the stressed words), and under `hold` a segment-long window runs to the held end, as does `sustain`. A row's own `hold` (seconds) keeps it up through the pause after its segment on the style hold's rule at its own cap, never shorter than the segment is drawn: a style hold of 1.1 s keeps the text through breaths, a shade's `hold: 3` keeps the picture shaded until the next caption. A row's `exit: {"opacity": {"keyframes": [{"t": 0, "v": 0, "easing": "ease_in_out"}, {"t": 0.25, "v": 1}]}}` fades each of its layers out over their last 0.25 s, written as the entrance it reverses in a style exit's own `{t, v}` keys (the style `exit` rule, on the layer's opacity; on an adjustment row it fades the grade). Each segment draws its own frame layers, so a row meant to stay up across captions (a shade) takes no exit: it would dip at every caption change. A frame row takes no box field (`padding`, `size`, `gap`, `offset`, `lead`, `color`). It may take `blendMode`, the layer field's names (default `normal`; it replaces a preset layer's own): a non-normal blend leaves the subject channel unchanged, so a backdrop-masked caption above it still finds the person, where a `normal` shade partly covers the person and the words show through it by its opacity. A black shade is identical in `multiply` and `normal` over the video, so write `"blendMode": "multiply"` on it (the shipped styles' `frame_shade` rows do), and a light leak is `screen`. An adjustment frame row on a captions layer that draws on a canvas of its own (`looks`, `mask`, `effects`, a non-normal `blendMode`, an opacity below 1, `motionBlur` where the composition allots samples), or on a captions clip of a track that does (not `blending: "pass_through"`, or its layer isolates it), is refused as `captions_frame_row_isolated`: it would grade nothing, or only the track. A shade still draws there.

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
