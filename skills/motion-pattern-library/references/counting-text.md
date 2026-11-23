# Text that counts or swaps words

A text layer's `text` animates like any other property: it takes the usual track `{ keyframes, expression }`, with string values. A counter, a countdown, a timecode or a word swap is one text layer, not a stack of step layers. An animatable `text` parameter's default takes the same track.

## The two arms

- **Keys** `{ "keyframes": [{ "time", "value" }] }`: each string shows from its key until the next. A key's `easing` is absent or `"step"`, because a string does not ramp.
- **An expression** `{ "expression": "…" }`: it returns the frame's string. It writes a number with `picsart.formatNumber(n, {…})`. A bare returned number fails the frame by name, because Lua would write `12450.0`.

Key times and the expression's `time` follow the layer rail: composition seconds, unless the layer sets `"timeMode": "layer"`. A counter on a layer that starts later sets `"timeMode": "layer"`, so it counts from its own start.

## A word swap

```json
"text": { "keyframes": [{ "time": 0, "value": "READY" }, { "time": 1.2, "value": "SET" }, { "time": 2.4, "value": "GO!" }] }
```

## An eased counter: a price or a score

```json
"text": { "expression": "local p = math.min(time / 2, 1)\nreturn picsart.formatNumber(12450 * (1 - (1 - p)^3), {grouping = ',', prefix = '$'})" }
```

`picsart.formatNumber` options, all optional:

| Option | Default |
|---|---|
| `decimals` | 0 |
| `grouping` | "" |
| `decimalMark` | "." |
| `prefix` | "" |
| `suffix` | "" |
| `minDigits` | 1 |

How it writes a number:
- Rounding is half away from zero, on the number as written: 10.075 rounds to 10.08.
- A minus sign comes before `prefix` (`-$12`).
- `minDigits` zero-pads the whole part.
- Separators are written out; there is no locale. `{grouping = '.', decimalMark = ','}` writes `12.450,00`.
- An unknown option fails by name.

The result is a string, so it composes:

```lua
'Lv 3 · ' .. picsart.formatNumber(score, {grouping = ','}) .. ' pts'
```

You can also write `SOLD OUT` once a count reaches zero, or a plural after a number.

## A countdown

On a layer that starts at 4 s, counting 10 s from there:

```json
{ "id": "countdown", "start": 4, "duration": 10, "timeMode": "layer",
  "content": { "kind": "text", "text": { "expression": "local left = math.max(0, math.ceil(10 - time))\nreturn string.format('%02d:%02d', left // 60, left % 60)" } } }
```

## A VHS timecode

Counting from the layer's own start:

```json
{ "id": "timecode", "start": 2, "duration": 8, "timeMode": "layer",
  "content": { "kind": "text", "text": { "expression": "local f = math.floor(time * 30)\nreturn string.format('PLAY  %02d:%02d:%02d', f // 1800, (f // 30) % 60, f % 30)" } } }
```

## Font and alignment

- Name a face whose digits are tabular, so the width holds while the digits change. In `jetbrains-mono-600`, every digit measures the same.
- Align a counter `left` or `right`, never `center`, because centred digits walk as the number grows. A fixed `minDigits` keeps the width steady.

## What a track does not take

`picsart_scene_validate` names each of these by its code:
- `textCase` (`text_case_on_text_track`): return the string already in its case, with `string.upper`.
- `textPath` (`text_path_on_text_track`).
- A text-animation preset that counts the text's characters, such as `fade_in_chars` or `ink_write` (`character_preset_on_text_track`). The count changes every frame.
