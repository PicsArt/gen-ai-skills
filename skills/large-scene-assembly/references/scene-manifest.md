# Editable scene manifest

Keep this beside the sources or in the handoff message. It is documentation, not scene syntax.

```text
Root: <latest returned handle / source path>
Canvas / fps / duration: <width × height> / <fps> / <seconds>
Shared decisions: <type scale, palette, margins, motion character>

Unit          Instance id     Source revision    Root window    Owner
intro         intro-01        <handle>           0–3            <component>
detail        detail-01       <handle>           3–7            <component>
shared card   product-card    <inline root>      0–7            <assembly>

Per component:
  Inputs and defaults: <declared parameters; no implicit inheritance>
  Asset scope: <media/font ids and resolvable URLs owned here>
  Local duration and source window: <seconds>
  Entry / event / exit state: <geometry and time>
  Grouped members: <common transform owner; deliberate internal exceptions>
  Layout contract: <padding, reflow, clipping, resize timing>
  Executable sidecar: <contract file/revision; stable contract ids and root-time windows>
  Validation evidence: <revision, times, lint results, preview/video>

Per seam:
  Intent: <continuation / reveal / replacement / reset>
  Carrier and lifetime: <id or deliberately none>
  Timing: <root event time, clip mapping, overlap, tail>
  Boundary checks: <contract ids; before/at/after spacing; deliberate unchecked phases>
  Evidence: <sample window, step, relationship targets, watched video>

Consolidation:
  Source snapshot: <root + child revisions retained>
  Delivery dependencies: <embedded / external / local-only>
  Changed references: <old → new>
  Remaining references and unresolved assets: <list, not assumed empty>
  Rechecked components and seams: <evidence>
```

Prefer a small manifest you actually update over a second scene model that can drift. When a child
changes, update its source revision, the root reference, and evidence for affected seams together.
