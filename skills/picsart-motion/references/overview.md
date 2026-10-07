# Motion — a static design becomes a motion-designed ad

The frames are not the video. They are a **design**, and a design is made of **layers**:
panels, headlines, buttons, images, lists. Motion design animates those *elements* — a
list scrolls, a headline types on, a card slides in with a stagger, a tap-dot pulses,
the shared chrome **smart-animates** from one screen to the next, everything moving with
depth. Bind a frame as one flat PNG and all of that is impossible — you get a slideshow.

So the first principle of this pipeline: **the design comes in as layers, and the video
is a composite of moving elements — never a montage of flat screens.** A real ad is
built the way a layered motion-graphics comp is built: each element on its own layer, each
with its own motion, shared elements carried between frames.

One economic law runs underneath: **the motion loop is free; the one paid capability is video
generation, and it is always credit-gated.** Every tool the compose/motion/preview loop touches —
layer ingest, compose/`patch_scene`, layout queries, `validate`, the panel, and the renders
themselves (`picsart_media_export`, `picsart_media_contact_sheet`) — is zero-credit, so for
all of that: **never tell the designer an
action will cost credits, and never hesitate to render for cost reasons — there is no cost.** The
**sole exception** is **generating video** (`picsart_generate` and the generative tools), which spends
credits — and it **never runs without the designer's explicit, informed consent**: show the balance,
quote the exact cost, get a yes (full gate in *Video generation* below). No other part of this
pipeline charges.

**Ignore the "charged"-looking badge on `export` / `contact_sheet`.** Both dispatch a real GPU
render and leave a Drive-saved file, so they carry a *behavioral* annotation (`readOnlyHint:
false`, artifact-producing) that a host UI or permission prompt may surface as "writes" /
"charged." That flag is about **behavior, not price** — the credit cost is still **zero**.
Do not read that badge as a credit charge or warn the
designer about it. Still author with care: a render costs *time* even when it costs nothing, so
decide on the panel's free previews and render the export when the reel is worth rendering.

## When to read which reference (mandatory, lazy)

References are not loaded with this skill — **read each one at its step, before doing that
step**, not "if you happen to need it":

| Before you… | Read |
|---|---|
| touch any tool, or wonder which tool answers a question | [`tool-routing.md`](tool-routing.md) |
| compose ANY scene — the rules **both** paths share (highest-level-tool, hosting/CSP, Drive, live text/fonts, placement, treatment, the eye) | [`compose-fundamentals.md`](compose-fundamentals.md) — read alongside whichever compose path applies; **the tools are the same, only the ingest differs** |
| import a **Figma** design / compose frames from its layers | [`authoring-flow.md`](authoring-flow.md) — the Figma golden path (coords, layer kinds) on top of the fundamentals |
| compose a scene from **uploaded assets** (photos/logos/screenshots/clips) — grid / stack / collage / montage | [`asset-composition.md`](asset-composition.md) — the non-Figma compose path (upload, probe, layout, fit-to-canvas) |
| decide *what* motion a change deserves (easing, duration, reduced-motion) | [`motion-principles.md`](motion-principles.md) |
| author a named pattern (scroll, type-on, tap-dot, progressive text) | [`motion-patterns.md`](motion-patterns.md) |
| author a seam between two frames | [`transitions.md`](transitions.md) |
| stagger/sequence multiple elements in one beat | [`choreography.md`](choreography.md) |
| choose ANY motion, or author scene JSON — the full menu of **layer kinds, motion presets, text animations, looks, effects, transitions, masks** (Figma AND from-scratch alike) | [`mp-scene-vocabulary.md`](mp-scene-vocabulary.md) — enumerate it via `get_capabilities`; don't hand-roll what a preset/look/effect already does |
| act on any widget/panel response | [`widget-feedback.md`](widget-feedback.md) |
| validate a scene — before showing ANY render, or when "it validates but looks wrong" | [`scene-validation.md`](scene-validation.md) — schema ≠ correct; the eye is the real check, ground truth branches by route |
| a render/preview looks wrong or a tool errors | [`motion-troubleshooting.md`](motion-troubleshooting.md) |
| write the first keyframe / nested comp / zoom math / opacity from Figma | [`engine-gotchas.md`](engine-gotchas.md) — silent-bug rules (local clocks, one track per channel, sRGB→linear opacity, fixed-point zoom) |

## Context discipline — never load the whole design at once

Tool results live in the context window for the rest of the session, so what you fetch is what you
pay for — in tokens, in cost, and in the model's attention. **Assume there is no file-offload: a big
result goes straight into context or the call errors** — a whole-page Figma metadata read on a real
storyboard is ~100KB+ and overflows. So fetch
narrowly, hold little, and persist facts to state:

- **Frame INDEX once, cheaply.** Read the top-level frame list — ids, names, left→right order,
  dimensions — from the page/canvas node **without drilling into each frame's tree**. That's all you
  need to know what exists and the running order.
- **Full layer tree per PAIR, then release it.** Pull a frame's full nested tree only when you reach
  its pair, and keep at most the **current pair (A + B)** in working context — don't accumulate frame
  7's tree while authoring 2→3. **The payoff of that narrow breadth is affordable DEPTH:** because
  you're holding only one or two frames, you can retrieve *everything* about them — every sub-layer,
  exact coords, text ink bounds, styles — which is exactly the completeness correct
  composition needs and which you could never afford across the whole storyboard at once. Narrow
  breadth buys full depth where it matters.
- **Scan the sequence with COMPACT tools, not full metadata.** Scroll-run / matched-element / zoom
  detection rides on `picsart_media_diff_layouts` / `query_layout`, which return small geometry
  deltas — peek ahead only as far as a run actually extends, never full-read the whole storyboard.
- **Persist resolved facts to `motion.json` / the scene doc, not the conversation.** Once a frame's
  coords, matchKeys, or the frame index are resolved, they live in state — so the next pair doesn't
  re-hold them in context, and a compacted or fresh session re-reads the file instead of re-fetching
  Figma. State is the memory; context is scratch.

## Flat vs. layered — the difference that is the whole product

| Flat-frame montage (the anti-goal) | Layered motion design (this skill) |
|---|---|
| each frame is one sealed PNG | each frame is its **layers**, each movable |
| motion = a transition at the seam | motion = every **element** animates (slide, scroll, type-on, parallax, tap) |
| screens **cross-dissolve** | shared elements **smart-animate** A→B (matched motion) |
| reads as a slideshow | reads as an ad |

Flat montage is the **fallback only** — used when a design's layers genuinely cannot be
had (a rasterized image, no Figma access). When you fall back to it, say so plainly:
*"without the design's layers this becomes a slideshow, not motion design."* Never
choose it while layers are available.

## Scope — phased

- **Motion-design static material into an ad/reel.** A Figma design's layers — or
  the user's own uploaded assets — → a composed, animated MP Scene → tuned by eye → rendered. All
  of what follows.
- **Also available: generate footage when the design needs it.** When a beat calls for real
  generated video (a video card/element, or the designer asks to generate a clip with a model of
  their choice), that's supported — but it spends credits, so it runs behind the cost-consent gate
  (see *Video generation*). It's a capability within the flow, not a separate phase.

## 0. Triage — route before anything

This skill animates **static material**, and material arrives several ways. Route first — the route
sets the **ground truth** you'll later validate the rendered result against, by eye:

| User brings | Route | Ground truth |
|---|---|---|
| A **Figma design / flow** with layers | **this skill**, Figma ingest (Stage 1) — run the opening tool sequence in [`tool-routing.md`](tool-routing.md) | **match the design** |
| **Their own assets** (photos, logos, screenshots, clips) **+ a described motion** | **this skill**, asset ingest — `picsart_media_upload` the files, `probe_media` them, then compose and author the motion **to the brief** | **match the brief** |
| **Their own assets, but NO motion described** | **this skill**, **propose mode** — analyze the assets (`probe_media` + **view them**), then **offer 2–3 concrete motion concepts** for the user to pick; author the chosen one | **the concept they picked** |
| An existing **MP Scene** to keep editing | **this skill**, resume — open the editor on it and edit | the current scene |
| **Flat exported images of a design** whose layers can't be had | **this skill**, flat-fallback — warn it will be a slideshow, and offer layered if they can share the Figma file | the flat frames |
| Footage already edited, to stitch | not this — that is a plain montage | — |
| A clip from a **pure text idea** (no assets) | not this — that is text-to-video generation | — |

The dividing line is **static material in, motion authored** — the material may be a Figma design
*or* the user's own assets. Note the difference between a **photo/asset reel** (the images *are* the
content — a first-class raster route, not a degradation) and **flat PNGs of a design** (layers were
lost — the announced slideshow fallback); don't treat uploaded photos as a failed layered import.

**Two postures — do not blur them.** With a Figma design or a stated brief you are in a **fidelity**
posture: build exactly that, and *propose* anything extra separately — **never invent** (the whole
"change only what was asked" discipline). With assets and no brief you are in a **proposal** posture:
inventing a concept is the *job* — but you still **offer 2–3 options and get a pick before authoring**,
never run off and build one unasked. Both postures meet at one rule: **a concrete plan is agreed
before motion is authored** — a matching plan in fidelity mode, a chosen concept in proposal mode.

**If the page holds SEVERAL distinct sequences/storyboards, list them and ask which to animate
first.** A Figma page routinely carries multiple reels side by side; don't silently start on the first
cluster. Group the frames into their sequences (by spacing/section/naming) from the cheap frame index,
name what you found, and let the designer pick the running order before composing anything
(`authoring-flow.md` §1).

**Never start from — or hand back — an animated video pulled from Drive.** `picsart_media_export`
auto-saves its render to Drive, but that video is an **output, not an input**: do not list Drive
for a prior render and reuse it as the result or the source. **Always author the motion from
scratch**, from the design's layers/frames. The only valid inputs are the Figma design (or flat
frames) and an in-progress MP Scene — never a rendered video. A Drive export is read-only
history; open the MP Scene and re-author, don't re-serve the old video.
**The one exception: the designer explicitly asks for it.** If they name a previously created
Drive video and ask to use it ("take the video we rendered yesterday", "use the export from
Drive"), then using it is honoring their instruction, not a shortcut — fetch that video and do
what they asked with it. The rule bans *you* reaching for a prior render on your own initiative;
it never overrides an explicit user request.

## Tool names — read this first

Two families on the `picsart` MCP server, and they are wired differently:

- **Scene tools — `picsart_media_*`.** Import, compose, validate, patch, translate,
  export, contact-sheet: the media/scene tools, surfaced under the `picsart_media_` prefix.
- **Panel tools — `picsart_<widget>`.** Each opens an interactive panel. This skill's is **`picsart_scene_editor`** (the
  scene editor — the pair-review surface: it **plays** the MP Scene document in the browser, free,
  and returns the designer's verdict + edit-request comments; **pass it a `scene` document, never
  video/media**). It is a *review* surface — motion is authored by you through
  `picsart_media_patch_scene`, not picked per-layer inside the panel. (This workflow does not use the
  `picsart_motion_setup` format console — the video format
  (ratio/fps/energy) is decided directly; see `picsart-motion-import` *Set the format*.) `picsart_scene_editor` is the complete panel
  surface. Full contract: `mp-scene-editor-widget.md`.

**Show the motion in the scene editor — don't re-export a video each time.** After authoring
a pair, open `picsart_scene_editor` **on the whole scene built so far** (title it for the current
pair, e.g. "f3→f4", so the designer knows where to look), so they watch the pair play **in context**
and can scrub straight to it — never a 2-frame sub-scene. That panel is the viewing surface, free,
and cheaper/faster than exporting
just to see a result. It **renders no file** — do not look for a `videoUrl` or save anything to
Drive from its reply. Reserve `picsart_media_export` for the final deliverable and for the error
fallback below. Do **not**
batch — never render a contact sheet of every frame as the main flow (that is what produces "all
frames at once").

**If a `picsart_scene_editor` call errors — a 503, a transport failure, or any
exception — do not leave the designer with nothing.** Export the **whole scene** (the full
reel end to end, **not** just the current pair's A→B window) with `picsart_media_export` and
**show the result video** so they can still see the motion play, then continue the
pair-by-pair flow once the panel recovers. Exporting a preview render is free
(`picsart_media_export` is 0-credit), so this costs nothing. The panel itself already falls
back to a video on a render error; this is the same move at the tool level. The
contact-sheet + the host question interface path is the **last resort** — reach for it only if the
export also fails, and never stall because of a panel error.

**What you SHOW is always the whole reel — even while authoring one pair.** Pair scope is an
*authoring* focus (it makes it easy to work one seam at a time), but every time the designer sees
the motion — the editor preview of a pair, an error-fallback video, any "let me see it" export —
show the **whole scene built so far**, positioned at the current pair, **never just that pair's
window** (e.g. not only the 3→4 transition in isolation). The editor plays a timeline, so opening it
on the whole scene lets the designer watch 3→4 *in context* and scrub to it; a 2-frame sub-scene
throws that context away. "Whole scene so far" = every composed frame up to now (later, uncomposed
frames simply aren't there yet). The designer navigates pair by pair; what they watch is the reel.

**Ground your facts in tools; own your judgment; author through tools.** The real work of
this skill lives in the tools — but the *judgment* about what to do is yours. Three different
activities, three different rules:

- **Facts come from tools — never invent them.** The design's layers, geometry, stacking
  order, fonts, layout; what changed between two frames; the valid presets/easings; whether a
  scene validates or rendered — these are *ground truth*. **Do not eyeball, describe, or infer
  the composition from the image and act on that guess** — your visual read is not a substitute
  and will be wrong about coordinates, layer boundaries, and fonts. Read each through the tool
  that owns it: `picsart_media_query_layout`, `picsart_media_diff_layouts` (what changed between
  two frames — opacity-blind, so check fades yourself), `picsart_media_get_capabilities`,
  `picsart_media_probe_media`, `picsart_media_list_fonts`, `picsart_media_validate_scene`.
- **Judgment is yours — apply it on the facts, with the designer.** What moves, which preset,
  what timing, which element is focal, essential vs decorative, when to override a default — this
  is the work you are here to do; no tool decides it for you. Drive it from the tool-resolved
  layers + `get_capabilities` presets and judge it on rendered previews (the scene editor, or
  an exported video). Deciding *what* is your job — **but never
  stop at describing it in prose**: author it and show the render.
- **Author through tools — never hand-write the artifact.** `picsart_media_patch_scene`,
  `picsart_media_apply_motion_preset`, `picsart_media_apply_text_animation`,
  `picsart_media_apply_scene_template`, `picsart_media_apply_effect`. **Never hand-write scene
  JSON, or type a coordinate/value you didn't get from a tool** — mint every edit through the tool.
- **Show / preview**: `picsart_scene_editor` (view the motion moving) or `picsart_media_export` (a rendered video). Never describe motion in prose.
- **Validate / render**: `picsart_media_validate_scene`, `picsart_media_export`. Run `picsart_media_layout_lint` too — a cheap automatic overlap/z-order pass over the whole timeline, done **before** the `contact_sheet` eye check (it's opacity-blind, so the eye check follows it, never replaces it).

The failure to avoid isn't *thinking* — it's **fabricating a fact you could have looked up, or
hand-building an artifact a tool should mint.** Think all you want about *what* the motion should
be; get every *fact* it rests on from a tool, and *author* it through one.

**Without the panel (a host that cannot display the `picsart_scene_editor` widget — a valid,
lower-fidelity setup) you STILL must use the media tools**: read via
`picsart_media_query_layout`, author via `picsart_media_patch_scene` /
`picsart_media_apply_motion_preset`, show via `picsart_media_export` /
`picsart_media_contact_sheet`. The panels' absence is a degraded *surface* — it is **not**
permission to invent facts (coordinates, layers, fonts) or hand-author the motion.

If a tool you genuinely need is unavailable (not connected, or it errors), **say so and stop**
— never silently fall back to doing the work yourself and proceeding as if you had the real data.

**Do the least work yourself — reach for the highest-level tool that does the job.** You are an 
orchestrator; the mp-scene server is the engine. Before assembling anything by hand out of
many low-level ops, check whether the server already does it in one call: a **scene template**
(`apply_scene_template` — montage/collage/title families) before hand-building a composition; a
**motion preset** (`apply_motion_preset`) or **text animation** (`apply_text_animation`) before
hand-keyframing; `quickstart` / the **recipes** before inventing a step sequence; `patch_scene`
for *edits*, not for constructing whole scenes op by op. The chat's judgment goes into WHAT to
do (which layer, which motion, what timing — with the designer); the server does the HOW.

## The edit loop — every designer instruction is a tool round-trip

The designer's job is to **point and say**; yours is to **run the tools**. Every instruction —
*"speed this up", "remove the animation from that", "update the easing", "this button has an
extra outline", "make the CTA pop later"* — is handled the same way, and **never** by describing
the change or acting on what the image looks like:

1. **Locate** — resolve the target through `picsart_media_query_layout`: the
   exact layer id, its box, its active window, its authored content. A pinned comment in the
   panel gives a spot on the picture and a moment, not a layer id — resolve the layer at that
   time through the tool, don't assume it.
2. **Edit** — apply the change with the right tool (full map in
   [`tool-routing.md`](tool-routing.md)): almost always
   `picsart_media_patch_scene` (`set` to change a value, `remove` to drop one), id-anchored;
   `apply_motion_preset` / `apply_text_animation` when **adding** motion. Values (easings, presets)
   come from `get_capabilities`, paths from `get_scene_schema` — **never invented**.
3. **Validate** — `patch_scene` re-validates inside itself; a `severity:error` fails the batch with
   diagnostics. Read them, fix, retry — never proceed on an invalid scene.
4. **Show** — re-open the panel on the pair (or `export` the whole reel) so the designer **sees**
   the result, not a description. The edit minted a **new `sceneRef`** — always work from the latest.
5. **Repeat** — one instruction at a time, pair by pair, advancing only on the designer's approval.

The whole product is this loop: the designer speaks small, specific edits; you turn each into a
tool call and show the result. If you ever catch yourself reasoning about coordinates, easings, or
layers **from the picture** instead of the tools, stop — that is the failure mode.

## Lean on the server's recipes — don't duplicate them

The scene/media tools are the
`picsart_media_*` tools, and their authoritative step sequences are the server's **recipes**. Ask the
server rather than hardcoding:

- `picsart_media_quickstart` — the on-ramp for common jobs; it also surfaces the relevant
  recipe steps.
- `picsart_media_list_recipes` / `picsart_media_get_recipe` — the recipe catalogue and a named
  recipe's steps. **When present, fetch the official recipes before hand-authoring:**
  **`figma-storyboard-to-scene`** (the canonical Figma→scene flow), **`motion-intent`** /
  **`motion-patterns`** / **`motion-mechanics`** (craft), **`transition-authoring`**. If a named recipe isn't in the catalogue, fall
  back to this skill's references + `picsart_media_quickstart` and proceed.

**This skill orchestrates; the recipe supplies the steps.** When a recipe and this skill
disagree on a *step*, the recipe wins; the gates, the motion vocabulary, and the panel
turns this skill adds are its own job.

## The pipeline — 5 stages, gates between them

| Stage | Does | Skill | Gate to pass |
|---|---|---|---|
| 1 · Import | Figma design → each frame's **layer tree** (elements + transforms + assets); matched elements tagged; format set | `picsart-motion-import` | every animatable layer has an asset/content + transform; matched elements tagged; format set |
| 2 · Compose | rebuild each frame as a **layered MP Scene** (elements placed by transform), verified to match the design | this skill | each composed frame `validate`s clean **and** renders identical to its design |
| 3 · Motion (interactive) | author real motion **one pair at a time** — per-element animation + matched-element smart-animate for frames A→B | `picsart-motion-design` | **every pair** approved on a moving preview, not a still |
| 4 · Preview | filmstrip across each pair and the whole cut | this skill | motion reviewed on real frames before the deliverable is rendered |
| 5 · Deliver | from the MP Scene: `export → mp4` for the final video (free); the MP Scene itself stays the editable source | this skill | mp4 exported and verified once |

**Gates are the product.** The expensive mistake is exporting motion the designer never
watched — a still hides everything. A gate passes only on evidence (a tool result, a
recorded waiver, a user's yes) or a conscious override. Before naming the next stage,
print the gate check with ✓/✗ and the evidence.

**Export and Drive-save are user-initiated — never automatic.** Do **not** call
`picsart_media_export` on your own to "show" a result (the editor already plays it on
free frames), and do **not** upload or save the output to Picsart Drive (`picsart_drive`
`action: "upload"`) as an automatic step. Both the final render *and* saving to Drive
happen only when the designer explicitly asks for them (or clicks the panel's own
control) — offer them, don't perform them. Producing a deliverable and stashing it in the
user's Drive without being asked is exactly the silent, unwanted side effect this gate
exists to prevent.

## Traps

- **Binding a frame as a flat PNG when its layers were available.** This is *the*
  slideshow trap. Layers in → elements
  move; flat in → screens dissolve.
- **Not tagging matched elements**, so shared chrome cross-dissolves instead of
  smart-animating — the single biggest tell of "slideshow, not ad".
- **Over-splitting** a design into hundreds of nodes (noise) or **under-splitting** so
  nothing can move independently. A layer is anything that moves on its own or persists
  across frames.
- Firing all entrances together instead of staggering; no depth/parallax, so it reads flat.
- Judging an export from a **still**; editing a **stale `sceneRef`**; losing the scene to
  an **expired CDN link** because nothing was saved to Drive.
