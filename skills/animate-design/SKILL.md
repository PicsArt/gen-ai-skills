---
name: animate-design
description: Turn static material into a real motion-designed video — a Figma design's LAYERS, or the user's own uploaded assets (photos, logos, screenshots, clips), become a composed, animated ad/reel where elements slide, scroll, type on, parallax, and smart-animate, tuned by eye, then rendered — or add designed motion to a video that already exists. The user can describe the motion they want, or let the skill analyze the assets and propose a concept. Use when the user wants to animate a design or assets, "make an ad/reel/video from these images/frames/screens", add motion to a Figma flow, bring static material to life, or add an animated intro, title card, transition, morph, callout or logo reveal to a tutorial, walkthrough, promo or reel. Not for cutting the user's footage into an edit, and not for generating footage from a pure text idea (that's generate-media); the motion inside such a video still comes here.
metadata:
  owner: motion-designer
  uses: design-layer-import, motion-design-craft, resting-frame-rules
---

# Motion — a static design becomes a motion-designed ad

The frames are not the video. They are a **design**, and a design is made of **layers**:
panels, headlines, buttons, images, lists. Motion design animates those *elements* — a
list scrolls, a headline types on, a card slides in with a stagger, a tap-dot pulses,
the shared chrome **smart-animates** from one screen to the next, everything moving with
depth. Bind a frame as one flat PNG and all of that is impossible — you get a slideshow.

So the first principle of this pipeline: **the design comes in as layers, and the video
is a composite of moving elements — never a montage of flat screens.** A real ad is
built the way the After-Effects reference is built: each element on its own layer, each
with its own motion, shared elements carried between frames.

One economic law runs underneath: **the motion loop is free; the one paid capability is video
generation, and it is always credit-gated.** Every tool the compose/motion/preview loop touches —
layer ingest, compose/`patch_scene`, layout queries, `validate`, the panel, and the renders
themselves (`picsart_scene_export`, `picsart_scene_contact_sheet`) — is on the connector's
zero-credit list (verified against live billing), so for all of that: **never tell the designer an
action will cost credits, and never hesitate to render for cost reasons — there is no cost.** The
**sole exception** is **generating video** (`picsart_generate` and the generative tools), which spends
credits — and it **never runs without the designer's explicit, informed consent**: show the balance,
quote the exact cost, get a yes (full gate in *Video generation* below). No other part of this
pipeline charges.

**Ignore the "charged"-looking badge on `export` / `contact_sheet`.** Both dispatch a real GPU
render and leave a Drive-saved file, so they carry a *behavioral* annotation (`readOnlyHint:
false`, artifact-producing) that a connector UI or permission prompt may surface as "writes" /
"charged." That flag is about **behavior, not price** — the credit cost is still **zero**
(they're in the server's `FREE_TOOLS`). Do not read that badge as a credit charge or warn the
designer about it. Still author with care: a render costs *time* even when it costs nothing, so
decide on the panel's free previews and render the export when the reel is worth rendering.

## When to read which reference (mandatory, lazy)

The UPPERCASE `references/` files and the `docs/` files named in this skill are in the motion-design-craft
skill; read them from its folder. The lowercase `references/` files are this skill's own.

References are not loaded with this skill — **read each one at its step, before doing that
step**, not "if you happen to need it":

| Before you… | Read |
|---|---|
| touch any tool, or wonder which tool answers a question | `references/TOOL-ROUTING.md` |
| compose ANY scene — the rules **both** paths share (highest-level-tool, hosting/CSP, Drive, live text/fonts, placement, treatment, the eye) | `references/COMPOSE-FUNDAMENTALS.md` — read alongside whichever compose path applies; **the tools are the same, only the ingest differs** |
| import a **Figma** design / compose frames from its layers | `references/AUTHORING-FLOW.md` — the Figma golden path (coords, layer kinds) on top of the fundamentals |
| compose a scene from **uploaded assets** (photos/logos/screenshots/clips) — grid / stack / collage / montage | `references/ASSET-COMPOSITION.md` — the non-Figma compose path (upload, probe, layout, fit-to-canvas) |
| decide *what* motion a change deserves (easing, duration, reduced-motion) | `references/MOTION-PRINCIPLES.md` |
| author any pair — the craft rules (easing budget, duration, stagger, holds) | `references/CRAFT-RULES.md` |
| author a named pattern (scroll, type-on, tap-dot, progressive text) | `references/MOTION-PATTERNS.md` |
| author a seam between two frames | `references/TRANSITIONS.md` |
| stagger/sequence multiple elements in one beat | `references/CHOREOGRAPHY.md` |
| choose ANY motion, or author scene JSON — the full menu of **layer kinds, motion presets, text animations, looks, effects, transitions, masks** (Figma AND from-scratch alike) | `references/SCENE-VOCABULARY.md` — enumerate it via `get_capabilities`; don't hand-roll what a preset/look/effect already does |
| act on any widget/panel response | `references/WIDGET-FEEDBACK.md` |
| validate a scene — before showing ANY render, or when "it validates but looks wrong" | `references/SCENE-VALIDATION.md` — schema ≠ correct; the eye is the real check, ground truth branches by route |
| a render/preview looks wrong or a tool errors | `references/MOTION-TROUBLESHOOTING.md` |
| write the first keyframe / nested comp / zoom math / opacity from Figma | `references/ENGINE-GOTCHAS.md` — silent-bug rules (local clocks, one track per channel, sRGB→linear opacity, fixed-point zoom) |
| fetch anything from a Figma file | `references/figma-context.md` — this skill's; frame index once, full tree per pair, state not context |
| work from uploaded assets with no motion described, or choose part-by-part vs whole | `references/asset-routes.md` — this skill's; propose mode and the working-mode offer |
| compose any frame (Stage 2) | `references/stage-2-compose.md` — this skill's; live layers, hosting/CSP, fonts, alignment, duration, preview per frame |
| author Stage 3 motion | `references/motion-vocabulary.md` — this skill's; the per-element vocabulary and craft rules |
| generate footage (the one paid capability) | `references/video-generation.md` — this skill's; the eight-step credit gate, in order |
| write or read `motion.json` | `references/motion-state.md` — this skill's; its shape and the `motion[].kind` → preset/keyframe map |

## Context discipline — never load the whole design at once

On the MCP connector a big tool result goes straight into context or the call errors. Fetch
narrowly and persist facts to `motion.json`: read `references/figma-context.md` before the first
Figma call.

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

## Scope and formats

Static material into an ad is the scope now; generated footage is a credit-gated capability within
it. The scene is the one editable source and the mp4 is only its render. Both in full:
`references/scope-and-formats.md`.

## 0. Triage — route before anything

The plugin animates **static material**, and material arrives several ways. Route first — the route
sets the **ground truth** you'll later validate the rendered result against, by eye:

| User brings | Route | Ground truth |
|---|---|---|
| A **Figma design / flow** with layers | **this skill**, Figma ingest (Stage 1) — run the opening tool sequence in `references/TOOL-ROUTING.md` | **match the design** |
| **Their own assets** (photos, logos, screenshots, clips) **+ a described motion** | **this skill**, asset ingest — `picsart_drive_upload_ask` the files, `probe_media` them, then compose and author the motion **to the brief** | **match the brief** |
| **Their own assets, but NO motion described** | **this skill**, **propose mode** — analyze the assets (`probe_media` + **view them**), then **offer 2–3 concrete motion concepts** for the user to pick; author the chosen one | **the concept they picked** |
| An existing **scene** to keep editing | **this skill**, resume — open the editor on it and edit | the current scene |
| **Motion inside another video** — a tutorial, walkthrough, promo or reel that needs an animated intro, title card, transition, morph, callout or logo reveal | **this skill**, scene path — skip ingest and compose (unless a design comes in to animate: design-layer-import first); author the motion with the motion-design-craft skill (its *Motion in any scene* section) on the scene that still holds the layers, then hand back to the flow that owns the video | the brief, in that video's look |
| **Flat exported images of a design** whose layers can't be had | **this skill**, flat-fallback — warn it will be a slideshow, and offer layered if they can share the Figma file | the flat frames |
| Footage already edited, to stitch | not this — that is a plain montage (the motion added between or over it is the scene path above) | — |
| A clip from a **pure text idea** (no assets) | not this — that is generation: **generate-media** | — |

The dividing line is **static material in, motion authored** — the material may be a Figma design
*or* the user's own assets. Motion added to a video that already exists is in scope too: the material
is that video's layers. Note the difference between a **photo/asset reel** (the images *are* the
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
(`references/AUTHORING-FLOW.md` §1).

**Never start from — or hand back — an animated video pulled from Drive.** `picsart_scene_export`
auto-saves its render to Drive, but that video is an **output, not an input**: do not list Drive
for a prior render and reuse it as the result or the source. **Always author the motion from
scratch**, from the design's layers/frames. The only valid inputs are the Figma design (or flat
frames) and an in-progress scene — never a rendered video. A Drive export is read-only
history; open the scene and re-author, don't re-serve the old video.
**The one exception: the designer explicitly asks for it.** If they name a previously created
Drive video and ask to use it ("take the video we rendered yesterday", "use the export from
Drive"), then using it is honoring their instruction, not a shortcut — fetch that video and do
what they asked with it. The rule bans *you* reaching for a prior render on your own initiative;
it never overrides an explicit user request.

## Assets in — propose mode and working mode

With assets and no brief, analyze by looking, then offer 2–3 concepts and get a pick before
authoring. Before authoring uploaded assets, offer part-by-part or whole-at-once. The steps are in
`references/asset-routes.md`; read it before either.

Before either is shown, check it with the `resting-frame-rules` skill: once the motion stops, every photo,
card and title is whole or gone, never cut by the edge of the frame.

## Tool names — read this first

Two families on this plugin's `picsart` connector, and they are wired differently:

- **Scene tools — `picsart_scene_*` / `picsart_media_*`.** Import, compose, validate, patch, translate,
  export, contact-sheet: the scene tools are surfaced under the `picsart_scene_` prefix, and the
  media-analysis tools under `picsart_media_`. To turn a short name in these docs into a tool
  name, use the table in `skills/motion-design-craft/references/TOOL-ROUTING.md`, never a prefix rule.
- **Panel tools — gen-ai-native and new, each named in full below.** The widget-opening tools
  are **not** media-tools proxies — they are registered directly in the gen-ai server,
  each bound to a `ui://` widget resource. This plugin's review panel is **`picsart_scene_editor`** (the
  scene editor — the pair-review surface: it **plays** the scene document in the browser, free,
  and returns the designer's verdict + edit-request comments; **pass it the document as `sceneUrl`
  whenever you have one, otherwise as `scene`, never video/media**). It is a *review* surface — motion is authored by you through
  `picsart_scene_patch`, not picked per-layer inside the panel. `picsart_scene_editor`
  **replaces the old scene inspector** and its motion-suggestion drafts, which no longer exist. The other panel is
  **`picsart_scene_setup`** — the Motion Setup console, opened once at the start, prefilled
  from the frames, to lock the video format (ratio/fps/energy, hold and seam defaults); it replies
  `motion_setup_feedback` (see `design-layer-import` *Set the format*). Full contract of the editor:
  `docs/widget-specs/scene-editor.md`.

**Show the motion in the scene editor — don't re-export a video each time.** After authoring
a pair, open `picsart_scene_editor` **on the whole scene built so far** (title it for the current
pair, e.g. "f3→f4", so the designer knows where to look), so they watch the pair play **in context**
and can scrub straight to it — never a 2-frame sub-scene. That panel is the viewing surface, free,
and cheaper/faster than exporting
just to see a result. It **renders no file** — do not look for a `videoUrl` or save anything to
Drive from its reply. Reserve `picsart_scene_export` for the final deliverable and for the error
fallback below. Do **not**
batch — never render a contact sheet of every frame as the main flow (that is what produces "all
frames at once").

**If a `picsart_scene_editor` call errors — a 503, a transport failure, or any
exception — do not leave the designer with nothing.** Export the **whole scene** (the full
reel end to end, **not** just the current pair's A→B window) with `picsart_scene_export` and
**show the result video** so they can still see the motion play, then continue the
pair-by-pair flow once the panel recovers. Exporting a preview render is free
(`picsart_scene_export` is 0-credit), so this costs nothing. The panel itself already falls
back to a video on a render error; this is the same move at the tool level. The
contact-sheet + ASK path is the **last resort** — reach for it only if the
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
this plugin lives in the tools — but the *judgment* about what to do is yours. Three different
activities, three different rules:

- **Facts come from tools — never invent them.** The design's layers, geometry, stacking
  order, fonts, layout; what changed between two frames; the valid presets/easings; whether a
  scene validates or rendered — these are *ground truth*. **Do not eyeball, describe, or infer
  the composition from the image and act on that guess** — your visual read is not a substitute
  and will be wrong about coordinates, layer boundaries, and fonts. Read each through the tool
  that owns it: `picsart_scene_query_layout`, `picsart_scene_diff_layouts` (what changed between
  two frames — opacity-blind, so check fades yourself), `picsart_scene_capabilities`,
  `picsart_media_probe`, `picsart_scene_fonts`, `picsart_scene_validate`.
- **Judgment is yours — apply it on the facts, with the designer.** What moves, which preset,
  what timing, which element is focal, essential vs decorative, when to override a default — this
  is the work you are here to do; no tool decides it for you. Drive it from the tool-resolved
  layers + `get_capabilities` presets and judge it on rendered previews (the scene editor, or
  an exported video). Deciding *what* is your job — **but never
  stop at describing it in prose**: author it and show the render.
- **Author through tools — never hand-write the artifact.** `picsart_scene_patch`,
  `picsart_scene_apply_preset`, `picsart_scene_apply_template`. **Never hand-write scene
  JSON, or type a coordinate/value you didn't get from a tool** — mint every edit through the tool.
- **Show / preview**: `picsart_scene_editor` (view the motion moving) or `picsart_scene_export` (a rendered video). Never describe motion in prose.
- **Validate / render**: `picsart_scene_validate`, `picsart_scene_export`. Run `picsart_scene_lint_layout` too whenever it's in your tool list — a cheap automatic overlap/z-order pass over the whole timeline, done **before** the `contact_sheet` eye check (it's opacity-blind, so the eye check follows it, never replaces it).

The failure to avoid isn't *thinking* — it's **fabricating a fact you could have looked up, or
hand-building an artifact a tool should mint.** Think all you want about *what* the motion should
be; get every *fact* it rests on from a tool, and *author* it through one.

**Without the panel (the `picsart_scene_editor` widget not connected — a valid,
lower-fidelity setup) you STILL must use the media tools**: read via
`picsart_scene_query_layout`, author via `picsart_scene_patch` /
`picsart_scene_apply_preset`, show via `picsart_scene_export` /
`picsart_scene_contact_sheet`. The panels' absence is a degraded *surface* — it is **not**
permission to invent facts (coordinates, layers, fonts) or hand-author the motion.

If a tool you genuinely need is unavailable (not connected, or it errors), **say so and stop**
— never silently fall back to doing the work yourself and proceeding as if you had the real data.

**Do the least work yourself — reach for the highest-level tool that does the job.** You are an 
orchestrator; the Picsart media server is the engine. Before assembling anything by hand out of
many low-level ops, check whether the server already does it in one call: a **scene template**
(`apply_scene_template` — montage/collage/title families) before hand-building a composition; a
**motion preset** or **text animation** (`apply_preset`) before
hand-keyframing; the **recipes** (`get_recipe`, `quick-merge-and-export` first) before inventing a step sequence; `patch_scene`
for *edits*, not for constructing whole scenes op by op. The chat's judgment goes into WHAT to
do (which layer, which motion, what timing — with the designer); the server does the HOW.

## The edit loop — every designer instruction is a tool round-trip

The designer's job is to **point and say**; yours is to **run the tools**. Every instruction —
*"speed this up", "remove the animation from that", "update the easing", "this button has an
extra outline", "make the CTA pop later"* — is handled the same way, and **never** by describing
the change or acting on what the image looks like:

1. **Locate** — resolve the target through `picsart_scene_query_layout` (at a `time`): the
   exact layer id, its box, its active window. Its authored content (items, paints, effects) is
   that layer in the scene document itself; `query_layout` returns geometry only. If the designer clicked a
   layer in the panel, the selection already carries the id + time — still confirm the *current*
   state through the tool, don't assume it.
2. **Edit** — apply the change with the right tool (full map in
   `references/TOOL-ROUTING.md`): almost always
   `picsart_scene_patch` (`set` to change a value, `remove` to drop one), id-anchored;
   `apply_preset` (`motionPreset:` / `textAnimation:`) when **adding** motion. Values (easings, presets)
   come from `get_capabilities`, paths from its `schema:<Name>` sections — **never invented**.
3. **Validate** — `patch_scene` re-validates inside itself; a `severity:error` fails the batch with
   diagnostics. Read them, fix, retry — never proceed on an invalid scene.
4. **Show** — re-open the panel on the pair (or `export` the whole reel) so the designer **sees**
   the result, not a description. The edit minted a **new `sceneRef`** — always work from the latest.
5. **Repeat** — one instruction at a time, pair by pair, advancing only on the designer's approval.

The whole product is this loop: the designer speaks small, specific edits; you turn each into a
tool call and show the result. If you ever catch yourself reasoning about coordinates, easings, or
layers **from the picture** instead of the tools, stop — that is the failure mode.

## Lean on the authoring skills — don't duplicate them

The scene/media tools reach this plugin **through the MCP connector**: they are the
`picsart_scene_*` / `picsart_media_*` tools. Their authoritative step sequences ship as skills of this plugin, so read
them rather than hardcoding:

- `picsart_scene_recipe` with `name: "quick-merge-and-export"` — the on-ramp for common jobs.
- The authoring skills, **read before hand-authoring:** **`figma-storyboard-animation`** (the
  canonical Figma→scene flow), **`motion-intent`** / **`motion-pattern-library`** /
  **`scene-animation-reference`** (craft) and **`custom-transitions`**.

**This skill orchestrates; the authoring skill supplies the steps.** When one of them and this
skill disagree on a *step*, the authoring skill wins; the gates, the motion vocabulary, and the panel
turns this skill adds are its own job.

## Progress messages — tell the designer what you're doing

The designer sees nothing while you read Figma, patch the scene or study frames, so silence looks
like a hang. **Before each stage, and before each long step inside one** (a Figma read, a round of
patches, a look at the frames by eye, a render), post ONE short line on its own. One line per step,
not per tool call. Pick a different option each time, and match the tone to the project (playful
for social ads, plain for corporate).

- **Reading Figma:** "Reading your layers…" / "Unpacking your design…" / "Gathering your assets…"
- **Composing:** "Rebuilding your frames…" / "Putting each layer in place…" / "Lining everything up…"
- **Planning:** "Choreographing the motion…" / "Deciding what moves first…" / "Sketching the timing…"
- **Animating / patching:** "Adding the motion…" / "Smoothing the transitions…" / "Tuning the easing…"
- **Checking by eye:** "Watching the frames back…" / "Checking every frame…" / "Looking for anything off…"
- **Rendering:** "Rendering your video…" / "Putting it all together…" / "Almost there, finishing frames…"

You may write your own message in the same style if it fits better, e.g. naming the pair:
"Moving the headline into frame 3…". **Never mention tool names, layer ids or internal steps**
(no "calling patch_scene", no "validating the sceneRef").

## The pipeline — 5 stages, gates between them

| Stage | Does | Skill | Gate to pass |
|---|---|---|---|
| 1 · Import | Figma design → each frame's **layer tree** (elements + transforms + assets); matched elements tagged; format set | `design-layer-import` | every animatable layer has an asset/content + transform; matched elements tagged; format set |
| 2 · Compose | rebuild each frame as a **layered scene** (elements placed by transform), verified to match the design | this skill | each composed frame `validate`s clean **and** renders identical to its design |
| 3 · Motion (interactive) | author real motion **one pair at a time** — per-element animation + matched-element smart-animate for frames A→B | `motion-design-craft`, `resting-frame-rules` | **every pair** approved on a moving preview, not a still |
| 4 · Preview | filmstrip across each pair and the whole cut | this skill | motion reviewed on real frames before the deliverable is rendered |
| 5 · Deliver | from the scene: `export → mp4` for the final video (free); the scene itself stays the editable source | this skill | mp4 exported and verified once |

**Gates are the product.** The expensive mistake is exporting motion the designer never
watched — a still hides everything. A gate passes only on evidence (a tool result, a
recorded waiver, a user's yes) or a conscious override. Before naming the next stage,
print the gate check with ✓/✗ and the evidence.

**Export and Drive-save are user-initiated — never automatic.** Do **not** call
`picsart_scene_export` on your own to "show" a result (the editor already plays it on
free frames), and do **not** upload or save the output to Picsart Drive (`picsart_drive_upload`,
`driveSave`) as an automatic step. Both the final render *and* saving to Drive
happen only when the designer explicitly asks for them (or clicks the panel's own
control) — offer them, don't perform them. Producing a deliverable and stashing it in the
user's Drive without being asked is exactly the silent, unwanted side effect this gate
exists to prevent.

## Stage 2 — compose the layers into live frames

> **HARD GATE — READ BEFORE COMPOSING. A frame is rebuilt from its LAYERS, never from a screenshot
> of the frame.** The single most common failure is taking one `get_screenshot` of the whole frame
> (or of a group) and dropping it in as one image. **That is wrong, always.** A `get_screenshot` of a
> frame or a multi-element group is **never** a scene layer. Each design node becomes its **own**
> scene layer, authored as its native kind (text→`text`, rects/cards/borders/circles/masks→`shape`,
> icons/logos→vector, only true photos/video→a raster asset). Every Figma shape — icons and logos
> included — becomes a shape layer: created with `picsart_scene_patch` (its outline, when it
> is not a plain rect or ellipse, appended with `picsart_scene_import_svg_path`), then painted by
> `layerId` with `picsart_scene_import_figma_paint` (see `design-layer-import`), not an uploaded SVG and
> not a baked node. Only what the paint tool reports in `skipped` may stay baked, and you disclose
> it.
>
> **Definition of done (check it):** a composed frame's layer count roughly matches the design
> frame's node count. A frame that has one `media` layer covering the whole thing, or a handful of
> big raster slabs, is a **failed** composition — throw it out and rebuild from the per-node tree.
> If you don't have the per-node kinds/coords yet, that's the signal to **fetch this frame's full
> layer tree** (you're only holding one or two frames, so you can afford all of it — see *Context
> discipline*), **not** to fall back to a screenshot.
>
> If you catch yourself reaching for a whole-frame or whole-group screenshot "to save time" or "to
> fix CSP," stop — that is the exact shortcut that produces a slideshow instead of motion design.

Do **not** bind frames to `mpscene://montage` — that treats a frame as one flat clip and
throws away every element. Instead **rebuild each frame as a composition of scene
layers**: one scene layer per imported design layer, positioned by its `transform`
(x, y, w, h, rotation, opacity, z-order). Author this with `picsart_scene_patch`
(or a compose recipe if the server exposes one), never the montage template.

Read `references/stage-2-compose.md` before composing the first frame: it holds the live-layer,
hosting, font, alignment, duration and preview-per-frame rules that `validate_scene` does not
catch.

## Stage 3 — the real motion design (the whole point)

This is where a slideshow becomes an ad. You **author** the motion through
`picsart_scene_patch` / the apply tools, then **show** it in `picsart_scene_editor` (a
gen-ai widget tool, despite the `picsart_scene_` prefix, not an engine proxy): it plays the pair's scene document in
the browser, free, and the designer approves it or sends it back with edit-request comments (pins
and marked stretches, each with its own instruction). Full contract in
`docs/widget-specs/scene-editor.md` and `references/WIDGET-FEEDBACK.md`; the authoring
craft is in the `motion-design-craft` skill.

The motion vocabulary (entrances, continuous, interaction, smart-animate, kinetic type, camera,
outro) and the craft rules are in `references/motion-vocabulary.md`.

### Work pair by pair — the default rhythm

**HARD RULE — one pair at a time, and STOP for approval before the next.** Never
author, compose, or review more than **one pair (two adjacent frames, A→B)** in a single
turn. Do **not** run ahead across the whole storyboard, do **not** batch multiple pairs or
all frames at once, and do **not** author the next pair until the designer has **explicitly
approved** the current one. Present one pair → wait → only after the approval comes back do
you advance to the next. Jumping ahead — composing or motioning several pairs before the
first is approved — is the single most common failure this rhythm exists to prevent.

**This pair rhythm is for FRAME SEQUENCES (a Figma storyboard).** Uploaded assets have no frames —
they're arranged into one composition (a **grid, stack, collage, montage, or single focus** — not
one-asset-per-screen by default) and worked by the **working mode the user picked** (part by part, or
the whole motion at once — see *Working mode for uploaded assets*), never by A→B pairs.

**The preview is mandatory and self-standing — never skip it and never wait to be asked.**
"Present" means you **actually call the preview** (`picsart_scene_editor` / `picsart_scene_export`)
and show the result; it does **not** mean describing the motion in prose, citing a `validate_scene`
pass, or saying it "should" look right. Advancing without a shown preview — or only previewing
because the designer *reminded* you to — is itself the violation, even if the motion turns out fine.
Every pair ends the same way: **shown preview → explicit designer yes → next.** No shown preview,
no advance; no explicit yes, no advance.

**And the preview that proves MOTION is the editor, not stills.** Contact-sheet / still exports are
fine for the Stage-2 *position* render-match, but the still renderer and the browser editor **draw some
moving things differently** (a photo scaling from its edge looked right in stills yet overlapped a
sibling in the editor). So judge motion on `picsart_scene_editor` (or a played export), never a
still — `references/MOTION-TROUBLESHOOTING.md` §"It looked right in the stills but wrong when it played".

**Approval gates what the designer SEES, never your intention to render it.** Free calls —
`validate_scene`, `contact_sheet`, opening the editor, an export used as a preview — run
without asking: render first, show, *then* wait for the reaction. Never ask "shall I render?",
never report that a preview "needs your go-ahead", and **never tell the designer to type "go"
(or any keyword) to continue** — the designer speaks in design terms ("snappier", "approved",
"change the easing"), not in control tokens. The compose/motion/preview loop is free, so it never
gates on cost. The actions that **do** require an explicit ask are **saving to Drive** and
**generating video** — the latter behind the full cost-consent gate (show credits → preflight cost →
explicit yes; see *Video generation*). Those two aside, act on free calls without asking.

**Open with frame 1's entrance, before pair 1→2.** The reel starts with motion, not a frozen
frame — author frame 1's own elements animating **in** at `t=0` (entrances by role, staggered by
hierarchy), get that opening beat approved, and only then start pair 1→2. A static first frame that
jumps into the first transition is a slideshow tell (full craft in the `motion-design-craft` skill,
*The opening beat*).

**First, analyze the whole frame sequence — a "pair" isn't always two frames.** Before you start
pairing, read the run with the diff tools (`picsart_scene_diff_layouts` / `query_layout`, never by
eye) and find the stretches that are really **one motion across several frames**: a **scroll** (frame
k, k+1, k+2… are the same page translated along one axis), a **zoom/pan** (B is A scaled/cropped), or
a **highlight-in-place** (B is A with emphasis). Those runs collapse into a **single continuous beat
over one unit of content** — you animate the whole scroll as one gesture, not frame-by-frame with a
stop on each waypoint (full detection + authoring in `references/TRANSITIONS.md`).
**This is a judgment that highly depends on the case** — how many frames belong to the run, whether
it's truly one scroll or genuinely separate screens, where it should pause — so decide it per design
from the tool-read facts, not from a fixed rule, and confirm on the played result. Everything below
about "pairs" applies to these grouped beats too: one is authored, shown, and approved at a time.

**Then work in the imported Figma order, from the top** — the first beat (frame 1's opening, then
1→2 or the first grouped run), then the next, and so on. "The next" always means the next in
sequence. **Never open with a middle or last beat (e.g. 8→9), and never hop between non-adjacent
ones** — not even when a later frame looks more interesting. Picking out of order is the same failure
as running ahead, pointed sideways: the storyboard is animated from the top, so the designer reviews
it the way it plays.

Author motion **one pair at a time** (the reference was built the same way — screen to
screen):

1. Focus **exactly one pair** — the **earliest pair not yet approved** (start at 1→2): frame A,
   the motion, frame B. Nothing beyond this pair is touched yet. (Open `picsart_scene_editor`
   on this pair to view the motion.)
2. **Propose the motion — author it, don't ask first.** Lead with the best role×energy /
   principle-based suggestion for the pair: each element's entrance/continuous motion **and** the
   matched-element smart-animate carrying shared layers A→B. A rendered proposal on screen is a far
   better prompt than a blank *"how do you want this to move?"* — so author, then show. (If the
   designer *has* stated an idea, author that instead — never impose your proposal over a stated one.)
3. **Show it moving, framed as a proposal** — open `picsart_scene_editor` **on the whole scene
   built so far** (titled for this pair) to play the motion in context (or export the whole reel):
   *"Here's f2→f3 — tell me what to change."* The designer approves or sends it back with comments.
4. **Take direction and revise.** The designer reacts to what they see — "snappier", "drop that
   element", "slower on the CTA". Fold each request into the pair and re-show. Expect a few passes;
   each maps to timing / staggering / element inventory, not a fresh design.
5. **Wait for the designer's explicit approval.** Only after it arrives do you flip that
   pair `approved: true` in `motion.json.seams` and move to the **next** pair. No approval →
   no advance, full stop.

**One decision per turn**, the running cut stays playable, and the **gate is met only
when every pair is approved**. Never self-approve by describing motion — the yes comes
from the designer, on a moving preview. Touch a shared frame and you may change both its
pairs, so re-preview the neighbour.

The panel does not latch: every edit writes a new scene document and `sceneRef` moves —
always edit the latest. And when the editor returns an **`edited` document**, that becomes the
latest — patch further changes onto it, not onto the copy you opened with.

## Video generation — opt-in, and CREDIT-GATED (the one paid capability)

Sometimes the design needs **generated footage** — a video card/element that should be real motion,
or the designer asks to generate a clip with the model they want. This is the plugin's only
credit-spending path, so it is **always gated on the designer's explicit, informed consent.** Use it
only when the design genuinely needs it or the designer asks — never on your own initiative to "fill"
something. Run this flow **in order, and never skip the gate**:
the eight steps in `references/video-generation.md`, in order — balance, model pick, params,
`picsart_preflight` cost, explicit yes, generate, monitor, place. **No preflight cost shown and no
explicit yes means no generation.**

## The state — `motion.json`

Keep project state in `motion.json`, updated whole at every milestone. **Never print it
in chat** — a request to *see* something opens the panel, not the data.

Its shape, and how each `motion[].kind` label maps to a preset or keyframes, are in
`references/motion-state.md`.

## Cost ledger

| Free (everything in this plugin's loop) | Charged, no rollback |
|---|---|
| layer import, compose, `validate`, layout queries, the panel and its motion previews, filmstrip, **and the renders** — `picsart_scene_export`, `picsart_scene_contact_sheet` (GPU renders that move no credits) | **generative** tools only — image/video/audio generation, remove-bg and kin |

**A dropped call is never a failed render.** An export usually completed even when the
connection dropped — check first (`picsart_job_status`, recent Drive files), never
blind-retry (each retry re-renders, and an `async: false` one re-saves to Drive), never present a completed
render as an error.

## Traps

- **Binding a frame as a flat PNG when its layers were available.** This is *the*
  slideshow trap, and the reason for the whole layered rewrite. Layers in → elements
  move; flat in → screens dissolve.
- **Not tagging matched elements**, so shared chrome cross-dissolves instead of
  smart-animating — the single biggest tell of "slideshow, not ad".
- **Over-splitting** a design into hundreds of nodes (noise) or **under-splitting** so
  nothing can move independently. A layer is anything that moves on its own or persists
  across frames.
- Firing all entrances together instead of staggering; no depth/parallax, so it reads flat.
- Judging an export from a **still**; editing a **stale `sceneRef`**; losing the scene to
  an **expired CDN link** because nothing was saved to Drive.
