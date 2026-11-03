# Drag, drop and list reflow

Use `scene://cursor-drag-drop` for a coordinated transfer demonstration: approach, carry,
drop, confirmation, departure and source-list gap closure. Discover with category `ui_widget`,
tag `drag`, reference policy `reusable`. Describe before applying.
For ordinary movement of one object use position tracks, not this template.

```json
{
  "uri": "scene://cursor-drag-drop",
  "mode": "bootstrap",
  "parameters": {
    "items": ["Design layout", "Review motion", "Export video"],
    "selectedIndex": 1,
    "cardWidth": 320,
    "cardHeight": 72,
    "style": "hand"
  }
}
```

This independently adapts an upstream interaction idea; no implementation/assets are imported.
It is not a live drag handler, arbitrary target tracker or complete kanban application.
Badges, changing counters and upstream board chrome are outside this adaptation.

## Ownership before checking

The card plate and label share `dragged` as their owner. The cursor's position expression reads
that owner's evaluated position; only its approach/departure offset changes independently.
During carry the offset is `[cardWidth/2 - 28, 0]`. Edit the card path and the pointer follows.
Do not replace that relationship with copied position keyframes. For independent animations
that align only for part of a timeline, use a windowed contract for that phase.
After bootstrap, preserve or coherently rewire this dependency if renaming layers. Reference mode
keeps the template parameterized; use bootstrap for structural/path edits.

`items` is a nonempty literal string list; `selectedIndex` must be an integer in range. The numeric
parameter schema cannot enforce this list-relative bound. Check before applying and require the
selected label after resolving. Count controls height, not three hard-coded rows. Long copy is not
automatically fitted: adjust width, height, font size or text and validate every row.

## Timing and geometry

Carry begins at `grabAt + 0.15`; drop is that time plus `travelDuration`. Rows below the selected
item move up by `cardHeight + gap` over `reflowDuration`, starting at drop. Confirmation fades in
over 0.15s after drop. Departure begins after `dropHold` and lasts `departDuration`.
Stage duration preserves both the full reflow and the departure/tail hold.
The first row center is `108 + cardHeight/2`; left/right centers are `cardWidth/2 + 48`
and `cardWidth*1.5 + 144`. Use those formulas when constructing checks for edited parameters.

## Required validation

1. Strictly validate and query actual nested ids/root windows. Defaults include `dragged__label_1`, `row_2__label` and `row_2__surface`; host instances add scopes or prefixes.
2. Compare intended card/pointer offset during carry, arrival, selected-label presence, landing, gap closure, confirmation opacity and label containment using supported `picsart_scene_lint_layout` relationships and explicit queries. Constant relative translation can preserve a wrong initial offset.
3. Compare rest after drop and motion through carry/drop/departure against independent expectations. Run relationship records with `picsart_scene_check_contracts` and motion records with `picsart_scene_check_motion` at the export FPS; state the windows checked.
4. Lint event intervals and allow only named intentional overlaps with panels, slot and rows. Do not hide heading collisions with blanket allowances.
5. Inspect full-resolution stills and continuous video for legibility, grip, clipping, ordering and confirmation. Pixel stability is not checked automatically.

Retiming or nesting requires shifted windows; changing the count/index requires new row IDs.
Negative controls: detach the pointer, move the landing point, reveal confirmation early,
overflow a label, request a nonexistent index. Each corresponding check must become a non-pass.
Report analysis, pixel evidence and visual inspection separately; no pass guarantees arbitrary edits.
