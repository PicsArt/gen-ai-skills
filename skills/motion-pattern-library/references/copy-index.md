# Copies by count, and the copy index

N copies of art in one layer: `repeater`; N layers that each move on their own: `$each` over a count.

`$each` over a `number` parameter makes that many copies; each copy's item is its index, 0 to
N − 1. The count is read only from a `number` parameter named bare (`"$each": "tiles"`). A count
that is not a whole number from 0 up is refused (`invalid_each`). A field reads the copy through
`$eval` (`"crate"`, `"crate.@index"`); an `expression` reads it through `{...}`: a group that reads a
loop name (`{crate.@index}`, `{crate}`) is filled for each copy, nested loops included
(`{row.@index * cols + col.@index}`). The loop's length is the count parameter itself (`{crates}`),
or `{cards.@count}` for a list.

**Grid mosaic.** One count, laid out in rows and columns, each tile arriving a beat after the one
before it. `$eval` has no `%`, so the column is `i - cols * floor(i / cols)` and the
row is `floor(i / cols)`:

```json
"parameters": { "tiles": { "type": "number", "default": 12 }, "cols": { "type": "number", "default": 4 } },
"layers": [{ "$each": "tiles", "as": "i", "body": {
    "id": "tile", "content": { "kind": "shape", "items": [{ "type": "rect", "size": [200, 200] }, { "type": "fill", "color": "#2d6cdf" }] },
    "transform": { "position": [
      { "$eval": "120 + 220 * (i - cols * floor(i / cols))" },
      { "$eval": "200 + 220 * floor(i / cols)" } ] },
    "animations": { "opacity": { "keyframes": [
      { "time": { "$eval": "i * 0.06" }, "value": 0 },
      { "time": { "$eval": "i * 0.06 + 0.25" }, "value": 1 } ] } } } }]
```

**Table of cells from a list.** Rows come from a `list` parameter and the cells from each row's
own list; nest the loops, and a cell's id is suffixed with both indices:

```json
{ "$each": "rows", "as": "row", "body": { "id": "row", "content": { "kind": "composition", "layers": [
    { "$each": "row.cells", "as": "cell", "body": { "id": "cell",
        "content": { "kind": "text", "text": { "$eval": "cell" } },
        "transform": { "position": [ { "$eval": "160 + 240 * cell.@index" }, 0 ] } } } ] } } }
```

**One expression on every copy.** When the motion lives in an expression rather than in
keyframes, write it once and let each copy splice its own index:

```json
{ "$each": "crates", "as": "crate", "body": { "id": "crate",
    "content": { "kind": "shape", "items": [{ "type": "rect", "size": [120, 120] }, { "type": "fill", "color": "#8a5a2b" }] },
    "animations": { "position": { "expression":
      "local i = {crate.@index}\nreturn Vec.v2(140 + 800 * i / math.max(1, {crates} - 1), 900 - 40 * math.abs(math.sin(time * 3 + i)))" } } } }
```

In an expression, as in `$eval`, the column of a grid is `{i - cols * floor(i / cols)}` and the row
`{floor(i / cols)}`. A group naming nothing in scope (`{crat}`) is refused (`invalid_expression`).
A nested composition inside a copy is part of it: its fields and expressions read the copy the same
way, as the shipped `cell-cycle-grid` and `framed-window-slideshow` read `<as>.@index` there. A
`scene_ref` is its own document: pass it the index as a parameter,
`"parameters": { "slot": { "$eval": "crate.@index" } }`.
