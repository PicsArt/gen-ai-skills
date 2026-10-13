---
name: motion
description: Turn static material into a real motion-designed video — a Figma design's LAYERS, or the user's own uploaded assets (photos, logos, screenshots, clips), become a composed, animated ad/reel where elements slide, scroll, type on, parallax, and smart-animate, tuned by eye, then rendered — or add designed motion to a video that already exists. The user can describe the motion they want, or let the skill analyze the assets and propose a concept. Use when the user wants to animate a design or assets, "make an ad/reel/video from these images/frames/screens", add motion to a Figma flow, bring static material to life, or add an animated intro, title card, transition, morph, callout or logo reveal to a tutorial, walkthrough, promo or reel. Not for cutting the user's footage into an edit, and not for generating footage from a pure text idea (that's text-to-video); the motion inside such a video still comes here.
metadata:
  owner: motion-designer
  uses: motion-import, motion-design
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
themselves (`picsart_media_export`, `picsart_media_contact_sheet`) — is on the connector's
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

The `references/` and `docs/` files named in this skill are in the motion-design skill; read them
from its folder.

References are not loaded with this skill — **read each one at its step, before doing that
step**, not "if you happen to need it":

| Before you… | Read |
|---|---|
| touch any tool, or wonder which tool answers a question | `references/TOOL-ROUTING.md` |
| compose ANY scene — the rules **both** paths share (highest-level-tool, hosting/CSP, Drive, live text/fonts, placement, treatment, the eye) | `references/COMPOSE-FUNDAMENTALS.md` — read alongside whichever compose path applies; **the tools are the same, only the ingest differs** |
| import a **Figma** design / compose frames from its layers | `references/AUTHORING-FLOW.md` — the Figma golden path (coords, layer kinds) on top of the fundamentals |
| compose a scene from **uploaded assets** (photos/logos/screenshots/clips) — grid / stack / collage / montage | `references/ASSET-COMPOSITION.md` — the non-Figma compose path (upload, probe, layout, fit-to-canvas) |
| decide *what* motion a change deserves (easing, duration, reduced-motion) | `references/MOTION-PRINCIPLES.md` |
| author a named pattern (scroll, type-on, tap-dot, progressive text) | `references/MOTION-PATTERNS.md` |
| author a seam between two frames | `references/TRANSITIONS.md` |
| stagger/sequence multiple elements in one beat | `references/CHOREOGRAPHY.md` |
| choose ANY motion, or author scene JSON — the full menu of **layer kinds, motion presets, text animations, looks, effects, transitions, masks** (Figma AND from-scratch alike) | `references/MP-SCENE-VOCABULARY.md` — enumerate it via `get_capabilities`; don't hand-roll what a preset/look/effect already does |
| act on any widget/panel response | `references/WIDGET-FEEDBACK.md` |
| validate a scene — before showing ANY render, or when "it validates but looks wrong" | `references/SCENE-VALIDATION.md` — schema ≠ correct; the eye is the real check, ground truth branches by route |
| a render/preview looks wrong or a tool errors | `references/MOTION-TROUBLESHOOTING.md` |
| write the first keyframe / nested comp / zoom math / opacity from Figma | `references/ENGINE-GOTCHAS.md` — silent-bug rules (local clocks, one track per channel, sRGB→linear opacity, fixed-point zoom) |

## Context discipline — never load the whole design at once

Tool results live in the context window for the rest of the session, so what you fetch is what you
pay for — in tokens, in cost, and in the model's attention. **On Claude Desktop / the MCP connector
(where this plugin runs) there is no file-offload: a big result goes straight into context or the
call errors** — a whole-page `get_metadata` on a real storyboard is ~100KB+ and overflows. So fetch
narrowly, hold little, and persist facts to state:

- **Frame INDEX once, cheaply.** Read the top-level frame list — ids, names, left→right order,
  dimensions — from the page/canvas node **without drilling into each frame's tree**. That's all you
  need to know what exists and the running order.
- **Full layer tree per PAIR, then release it.** Pull a frame's full nested tree only when you reach
  its pair, and keep at most the **current pair (A + B)** in working context — don't accumulate frame
  7's tree while authoring 2→3. **The payoff of that narrow breadth is affordable DEPTH:** because
  you're holding only one or two frames, you can retrieve *everything* about them — every sub-layer,
  exact coords, ink bounds via `use_figma`, styles — which is exactly the completeness correct
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

- **Phase 1 (now): motion-design static material into an ad/reel.** A Figma design's layers — or
  the user's own uploaded assets — → a composed, animated MP Scene → tuned by eye → rendered. All
  of what follows.
- **Also available: generate footage when the design needs it.** When a beat calls for real
  generated video (a video card/element, or the designer asks to generate a clip with a model of
  their choice), that's supported — but it spends credits, so it runs behind the cost-consent gate
  (see *Video generation*). It's a capability within the flow, not a separate phase.
- **Phase 2 (later): generate a *new* video from a given one.** A video-to-video pass,
  once the server's v2v path is wired. Don't build it yet; keep the hook
  (`motion.json.source` can name a given video, not only a design).

## 0. Triage — route before anything

The plugin animates **static material**, and material arrives several ways. Route first — the route
sets the **ground truth** you'll later validate the rendered result against, by eye:

| User brings | Route | Ground truth |
|---|---|---|
| A **Figma design / flow** with layers | **this skill**, Figma ingest (Stage 1) — run the opening tool sequence in `references/TOOL-ROUTING.md` | **match the design** |
| **Their own assets** (photos, logos, screenshots, clips) **+ a described motion** | **this skill**, asset ingest — `picsart_media_upload` the files, `probe_media` them, then compose and author the motion **to the brief** | **match the brief** |
| **Their own assets, but NO motion described** | **this skill**, **propose mode** — analyze the assets (`probe_media` + **view them**), then **offer 2–3 concrete motion concepts** for the user to pick; author the chosen one | **the concept they picked** |
| An existing **MP Scene** to keep editing | **this skill**, resume — open the editor on it and edit | the current scene |
| **Motion inside another video** — a tutorial, walkthrough, promo or reel that needs an animated intro, title card, transition, morph, callout or logo reveal | **this skill**, scene path — skip ingest and compose (unless a design comes in to animate: motion-import first); author the motion with the motion-design skill (its *Motion in any scene* section) on the scene that still holds the layers, then hand back to the flow that owns the video | the brief, in that video's look |
| **Flat exported images of a design** whose layers can't be had | **this skill**, flat-fallback — warn it will be a slideshow, and offer layered if they can share the Figma file | the flat frames |
| Footage already edited, to stitch | not this — that is a plain montage (the motion added between or over it is the scene path above) | — |
| A clip from a **pure text idea** (no assets) | not this — that is text-to-video generation | — |

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

## Propose mode — assets in, no brief

When the user brings **assets but doesn't say what motion they want**, you propose it. This is the one
place where inventing is the job — but it stays disciplined: analyze, offer a small menu, build the pick.

1. **Analyze the assets — by looking.** `picsart_media_upload` the files, `picsart_media_probe_media`
   for dims / fps / duration, and **view each asset with your own vision** (the same eye that validates
   output — `references/SCENE-VALIDATION.md`). You cannot propose
   sensible motion for material you have not seen.
2. **Classify what you have.** Photos? a logo / brand mark? app screenshots? a product shot? a video
   clip? text? The class drives the concept: photos → a promo/reel (recipe `photo-promo`); screens → a
   UI walkthrough (`ui-motion`); a logo → a brand sting; mixed → a title + montage.
3. **Offer 2–3 concrete concepts — not one, and never a blank "how do you want it?"** Each concept is a
   short, specific pitch the user can choose between, differing in *approach* (e.g. calm/premium vs
   punchy/ad vs playful), and each naming: the **format** (ratio/fps), the **layout** (how the assets
   are arranged — a grid, a stack, a collage, a montage/sequence, or a single focus; assets need not be
   one-per-screen), the **key moves** (its 2–3 signature animations), and the **rough pacing/length**.
   Use `motion-intent` to derive the moves from the intent each concept expresses, and `apply_scene_template`
   (montage/collage/title families) as a starting layout where it fits. Keep the concepts genuinely
   distinct — a real creative-direction menu, not three shades of one idea.
4. **User picks (or steers).** They choose one, or blend ("option 2 but calmer") — fold that into a
   single agreed concept. That concept is now the **ground truth** you validate the render against
   (`SCENE-VALIDATION.md` rung 4, chosen-concept branch).
5. **Author the pick** — compose the assets into a scene (a scene template or `patch_scene`), author
   the concept's moves (`apply_motion_preset` / `apply_text_animation` / keyframes), then validate by
   eye and preview for approval, exactly as the fidelity path does.

**Deciding the layout — like a designer, not a checklist.** Don't tally asset properties to pick
"show all at once vs give each focus." Decide it the way designers actually do:

- **Message and hierarchy first.** Ask what the piece must *say* — "we have range/lots" makes the
  **set** the hero (grid / collage / stack); "this one is the star" makes a **single** asset the hero
  (focus). Then rank primary → secondary → rest; it's rarely all-equal (even a grid usually has one
  bigger or first tile).
- **Motion usually dissolves the choice.** You can show many **and** guide attention one at a time by
  **revealing in sequence** (a staggered grid/collage), or by **establishing then pushing in** (the
  whole set lands, then the camera moves to the hero). So "together vs focus" is most often a *pacing*
  choice on the same layout, not a hard fork.
- **Budget by time.** How many beats fit the length — nine items in 6s → a grid that reveals; five in
  20s → walk through them.
- **Then let the pick decide.** Spread the 2–3 concepts across that real axis (e.g. all-at-once grid
  vs spotlight-each vs establish→detail) and let the user choose — the decision is settled by reacting
  to concrete options, exactly as a designer roughs out directions rather than deciding by rule.

**Read the theme / occasion, and let it drive the concept.** When the assets or brief carry a theme
or occasion — Christmas, Valentine's, back-to-school, a sale, a brand's own palette/vibe — reflect it:
a themed **colour palette**, and where it fits, a few **themed accent elements** (an authored
snowflake/ornament/heart shape, a seasonal texture) and a matching motion register. Read the theme by
**looking** at the assets (the eye) and from what the user said — don't assume one. Put it in the
2–3 concepts and let the user pick, and keep it to a **few coherent accents** (MOTION-PRINCIPLES §7),
never a snow-globe of decorations.

> **This themed-invention licence is PROPOSAL MODE ONLY.** With a Figma design or a stated brief you
> are in fidelity posture: the theme's colours and shapes are **already the designer's** — respect the
> design's palette and **do not invent themed decorations onto it** (that is exactly the trust-breaking
> invention the "animate existing layers only" rule forbids — see `ENGINE-GOTCHAS.md`). Offer a themed
> addition as a separate proposal; never sprinkle it in.

**Do not skip the menu and build one concept unasked** — that is the proposal-mode form of running
ahead. Propose → pick → author, every time. Once a concept is picked you are back in **fidelity
posture to that concept**: build what was chosen, and propose any extras separately.

## Working mode for uploaded assets — part by part, or the whole motion at once

The pair-by-pair rhythm (Stage 3 below) is for **frame sequences** — a Figma storyboard gives natural
A→B pairs to work through. **Uploaded assets have no frames**, so there is nothing to pair. Before
authoring, **offer the user how they want to work**:

- **Part by part** — build and approve the motion in pieces, beat by beat. A "part" is a **beat, not
  one asset**: a single beat can move several assets together — a grid of photos revealing, a stack
  fanning out, a row sliding in, a title typing over a collage. Safer for a longer or multi-beat piece
  — the user steers as it grows, and one wrong call doesn't compound.
- **The whole motion-added version at once** — author the entire motion, render it, and show the full
  result, then refine from there. Faster for a short or simple piece (a single logo sting, a 3-photo
  reel), where seeing the whole thing is the quickest way to react.

Offer both, recommend by size (part-by-part for multi-beat/longer, whole for short/simple), and let
the user pick — don't assume. Either way the **eye-check + preview-approve gate still applies**
(`references/SCENE-VALIDATION.md`): part-by-part approves each piece
as it's added; whole-at-once approves the full render, then iterates.

## Tool names — read this first

Two families on this plugin's `picsart-gen-ai` connector, and they are wired differently:

- **Scene tools — `picsart_media_*`.** Import, compose, validate, patch, translate,
  export, contact-sheet: the media/scene tools, surfaced under the `picsart_media_` prefix.
  Server recipes and older docs name `mp_export`, `mp_patch_scene`, etc.; translate `mp_<x>` →
  `picsart_media_<x>`.
- **Panel tools — `picsart_<widget>`, gen-ai-native and new.** The widget-opening tools
  are **not** media-tools proxies — they are registered directly in the gen-ai server,
  each bound to a `ui://` widget resource. This plugin's review panel is **`picsart_scene_editor`** (the
  scene editor — the pair-review surface: it **plays** the MP Scene document in the browser, free,
  and returns the designer's verdict + edit-request comments; **pass it a `scene` document, never
  video/media**). It is a *review* surface — motion is authored by you through
  `picsart_media_patch_scene`, not picked per-layer inside the panel. `picsart_scene_editor`
  **replaces the old scene inspector** (and its `mp_inspect_scene` / `mp_suggest_motion`
  drafts) — do **not** read those as tool names; they no longer exist. The other panel is
  **`picsart_motion_setup`** — the Motion Setup console, opened once at the start, prefilled
  from the frames, to lock the video format (ratio/fps/energy, hold and seam defaults); it replies
  `motion_setup_feedback` (see `motion-import` *Set the format*). Full contract of the editor:
  `docs/widget-specs/mp-scene-editor.md`.

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
- **Validate / render**: `picsart_media_validate_scene`, `picsart_media_export`. Run `picsart_media_layout_lint` too whenever it's in your tool list — a cheap automatic overlap/z-order pass over the whole timeline, done **before** the `contact_sheet` eye check (it's opacity-blind, so the eye check follows it, never replaces it).

The failure to avoid isn't *thinking* — it's **fabricating a fact you could have looked up, or
hand-building an artifact a tool should mint.** Think all you want about *what* the motion should
be; get every *fact* it rests on from a tool, and *author* it through one.

**Without the panel (the `picsart_scene_editor` widget not connected — a valid,
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

1. **Locate** — resolve the target through `picsart_media_query_layout` (at a `time`): the
   exact layer id, its box, its active window. Its authored content (items, paints, effects) is
   that layer in the scene document itself; `query_layout` returns geometry only. If the designer clicked a
   layer in the panel, the selection already carries the id + time — still confirm the *current*
   state through the tool, don't assume it.
2. **Edit** — apply the change with the right tool (full map in
   `references/TOOL-ROUTING.md`): almost always
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

The scene/media tools reach this plugin **through the MCP connector**: they are the
`picsart_media_*` tools, and their authoritative step sequences are the server's **recipes**. Ask the
server rather than hardcoding:

- `picsart_media_quickstart` — the on-ramp for common jobs; it also surfaces the relevant
  recipe steps.
- `picsart_media_list_recipes` / `picsart_media_get_recipe` — the recipe catalogue and a named
  recipe's steps. **When present, fetch the official recipes before hand-authoring:**
  **`mp-figma-storyboard-to-scene`** (the canonical Figma→scene flow), **`mp-motion-intent`** /
  **`mp-motion-patterns`** / **`mp-motion-mechanics`** (craft), **`mp-transition-authoring`**,
  **`mp-scene-format-architecture`** (the format). **Availability varies by connector** — these
  are commonly **not mirrored today**; if the two tools aren't in your tool list, that's normal,
  not an error: fall back to this plugin's references + `picsart_media_quickstart` and proceed.

**This skill orchestrates; the recipe supplies the steps.** When a recipe and this skill
disagree on a *step*, the recipe wins; the gates, the motion vocabulary, and the panel
turns this skill adds are its own job.

## The pipeline — 5 stages, gates between them

| Stage | Does | Skill | Gate to pass |
|---|---|---|---|
| 1 · Import | Figma design → each frame's **layer tree** (elements + transforms + assets); matched elements tagged; format set | `motion-import` | every animatable layer has an asset/content + transform; matched elements tagged; format set |
| 2 · Compose | rebuild each frame as a **layered MP Scene** (elements placed by transform), verified to match the design | this skill | each composed frame `validate`s clean **and** renders identical to its design |
| 3 · Motion (interactive) | author real motion **one pair at a time** — per-element animation + matched-element smart-animate for frames A→B | `motion-design` | **every pair** approved on a moving preview, not a still |
| 4 · Preview | filmstrip across each pair and the whole cut | this skill | motion reviewed on real frames before the deliverable is rendered |
| 5 · Deliver | from the MP Scene: `export → mp4` for the final video (free); the MP Scene itself stays the editable source | this skill | mp4 exported and verified once |

**Gates are the product.** The expensive mistake is exporting motion the designer never
watched — a still hides everything. A gate passes only on evidence (a tool result, a
recorded waiver, a user's yes) or a conscious override. Before naming the next stage,
print the gate check with ✓/✗ and the evidence.

**Export and Drive-save are user-initiated — never automatic.** Do **not** call
`picsart_media_export` on your own to "show" a result (the editor already plays it on
free frames), and do **not** upload or save the output to Picsart Drive (`picsart_drive`,
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
> included — becomes a shape layer: created with `picsart_media_patch_scene` (its outline, when it
> is not a plain rect or ellipse, appended with `picsart_media_import_svg_path`), then painted by
> `layerId` with `picsart_media_import_figma_paint` (see `motion-import`), not an uploaded SVG and
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
(x, y, w, h, rotation, opacity, z-order). Author this with `picsart_media_patch_scene`
(or a compose recipe if the server exposes one), never the montage template.

**Layered means LIVE, not rasterized — a hard requirement.** Text is always a live `text`
layer (font by file URL), never a baked PNG; solid/gradient rectangles, cards, borders, circles
and masks are `color`/shape layers; icons and logos stay **vectors** where supported; a raster
asset is reserved for **true imagery** (photos, videos, textures, or an effect the engine can't
reproduce — disclosed to the designer when baked in). Never flatten a group whose children carry
text or animate independently into one screenshot: a flattened slab can only fade/scale as a whole,
which forfeits every per-element move Stage 3 exists for. The full kind-triage lives in
`references/AUTHORING-FLOW.md` §5.

- **"Upload every asset" means EXTERNAL MEDIA ONLY — it does NOT mean "turn every visual element
  into an uploaded image."** Drive/`upload` applies only to external media files (photos, videos,
  textures, unavoidable raster). **Native scene shapes, vectors, and live text must remain authored
  elements and must never be converted to raster images merely for upload or CSP compatibility.**
  PNG export is a **fallback** for genuine raster content or a truly unsupported vector — not the
  default, and never a way to make a card/component/screen "uploadable." (This is the exact trap that
  produces a rebuilt-from-screenshots frame that diverges from the design.)
- **A CSP/blob failure is fixed by changing ONLY the affected asset's URL or format — never by
  flattening.** Re-host that one image to a Picsart URL (or convert an unsupported vector to a raster
  *for that element alone*); do **not** rasterize the card, component, or whole screen it sits in to
  make the error go away. Flattening to dodge CSP destroys the layering and is a wrong ad.
- **Audit every node's kind BEFORE composing** — shape / vector / text / photo / video — and author
  each as its native kind (above). This layer-type pass is a required step, not optional; skipping it
  is how shapes and text get wrongly baked.
- **If Figma metadata shows no text but the reference visibly has text, STOP and verify the node/
  frame before authoring — do not proceed on the exported assets.** A `get_metadata` call can land on
  the wrong node (a rectangle, a collapsed instance) or not expand the frame's nested tree, returning
  no text for a frame that clearly contains it. That is a signal to re-inspect the full nested
  structure / correct frame node (`get_metadata` on the right frame, `use_figma` for the tree), never
  to reconstruct from the visible screenshots and omit the text. Missing text in the read = read
  again, don't guess.

- **A composed frame must render identical to the static design — proven by comparison, not
  assumed.** Render one `contact_sheet` frame at the frame's hold start and put it **side by side
  with the source** (`get_screenshot` of the Figma frame). Look specifically for **text that
  clipped, wrapped, or shifted** versus the design (the alignment/box traps above), layers that
  landed off-position, and wrong z-order. Skipping this compare is how a mispositioned or
  wrapped headline ships — it is a wrong ad, cheaply caught now.
- **Compose one frame, PREVIEW it, and wait for the designer before the next — never
  batch-compose the storyboard.** After each frame is composed, actually **render it and show it**
  (the `contact_sheet`/editor still beside the source) and let the designer confirm it before
  you compose the next frame. The preview is a **hard precondition to advancing, not a formality
  you narrate past**: proceeding on your own "it should match" judgment — *without having rendered
  and shown the frame* — is the skipped-preview failure, the same one the pair rhythm below exists
  to prevent. If you catch yourself *describing* a frame instead of *showing* it, stop and render
  it. The designer should never have to ask you to preview — and the reverse holds too:
  **never ask the designer for a go-ahead to render.** A free render (`validate_scene`,
  `contact_sheet`, the editor panel) needs no permission — run it, show the result, and let
  the designer react to what they see. "Approve the render when it pops up" / "say go and I'll
  run it" is a dead turn where the result should already be on screen.
- **You do NOT have to compose the whole storyboard before any motion — compose and motion
  INTERLEAVE per pair.** The stage table lists Compose (2) before Motion (3), but that is the order
  *for a given frame*, not a barrier across the whole reel. The rhythm: **compose frame 1 → animate
  frame 1's opening beat → then, for each pair, compose the next frame only when its pair comes up, and
  motion it.** Composing every frame first and only then starting motion both **delays the motion the
  designer is waiting to see** and contradicts *"open with frame 1's entrance before pair 1→2"* (Stage
  3). Rebuild just-in-time, pair by pair.
- **Matched elements stay one continuous layer across the frames they appear in**, keyed
  by `matchKey` from import — that is what lets Stage 3 smart-animate them rather than
  cross-dissolve. A header present in frames 1–4 is *one* layer with four transform
  states, not four separate headers.
- **Duration is derived by default; an explicit target is opt-in and soft.** By default
  (`duration.mode: "derived"` — the console's checked box) the total is `$sum` of the
  holds, each grown to fit its own motion (a 1.2s type-on needs a hold ≥ 1.2s), so it
  *grows as motion is added*. A designer may instead set `duration.mode: "target"` with a
  length — a **soft budget**: holds scale toward it where there is slack, but never below
  each hold's motion-minimum, so a too-short target **lengthens** the video rather than
  clipping an animation. Never silently clip motion to hit a number; a target the motion
  overflows is shown, not enforced.

- **Every asset URL in the scene must be Picsart-hosted (`pastatic`/`gcdn`) — never a `figma.com`,
  `data:`, or `blob:` URL.** A Figma `get_screenshot` returns a `figma.com/api/mcp/asset/…` URL and
  browsers hand you `blob:` object URLs; **do not author either into the scene.** First lift every
  image to a durable Picsart URL with `picsart_media_upload` (or `picsart_drive`) and author *that*.
  The catch: server-side `export`/`contact_sheet` **can** fetch `figma.com`, so they render fine and
  hide the problem — but the browser preview's Content-Security-Policy blocks these hosts
  (`csp: blocked connect-src … figma.com`, `csp: blocked img-src … blob:`), so the layer goes blank
  or the engine fails. **Validation and a clean contact-sheet are NOT proof it loads in the preview.**
  Fix a blocked scene by re-uploading the offending assets and `patch_scene`-ing their `uri` to the
  Picsart URLs. (Full detail: `references/AUTHORING-FLOW.md` §5.)
- **A text layer's font is always the resolved `.ttf`/`.otf` file URL from `picsart_media_list_fonts`
  (or an `assets[]` `{ type: "font", id, uri }` entry carrying it) — never a family name ("Inter")
  and never a bare catalog key ("gilroy-semibold").** A key *passes* `validate_scene` but the
  editor/exporter engine **fails to boot** on it (no catalog wired → *"cannot read fontLocation…
  font is a NAME"* → the still/video fallback): **validation ≠ boot for fonts.** Match the design's
  typeface to a catalog entry, then author that entry's **URL**, which hands the engine a location.
- **A text layer carries the design's real horizontal alignment and box behaviour — never a
  guessed one.** Author the `alignment` Figma actually set (`textAlignHorizontal`), because the
  anchor follows it: a **left**-aligned layer's `position.x` is the box's **left edge**, a
  **center**-aligned layer's is the box **center**. Defaulting a headline to `center` (and so to a
  center-of-box x) is the classic tell — it drags left-aligned copy off toward the middle/right.
  And if Figma's text sits in a **fixed-width box that overflows the frame**, it **clips** there;
  a scene text layer with only a point anchor + font size will instead **soft-wrap** the overlong
  line at the space. Carry the box width (so it clips like the design) or drop the font size so the
  single line fits — never let it silently wrap to two lines.
- **A missing font is surfaced, never silently swapped.** For every text layer, check its
  typeface against `picsart_media_list_fonts` (the platform's available fonts) — **or
  `picsart_media_discover_fonts`** when `list_fonts` isn't on your connector, or to live-search a
  font not in the bundled snapshot (it returns a `.ttf`/`.otf` URL you author directly). If the
  design's font is **not available from the media tools** — neither tool can find it — do
  **not** quietly substitute a fallback and move on. **Tell the designer plainly**: name
  the missing font, name the fallback you'd otherwise use, and say the text will render in
  that fallback (different metrics → the layout can shift). Let them decide — pick an
  available font, supply/upload the font, or accept the fallback knowingly. A silently
  swapped font is a wrong ad that reads as "close enough" until someone notices.

Then `picsart_media_validate_scene` — free, catches schema errors before any render is
spent on a broken scene.

## Stage 3 — the real motion design (the whole point)

This is where a slideshow becomes an ad. You **author** the motion through
`picsart_media_patch_scene` / the apply tools, then **show** it in `picsart_scene_editor` (the
gen-ai widget tool, **not** a `picsart_media_*` proxy): it plays the pair's MP Scene document in
the browser, free, and the designer approves it or sends it back with edit-request comments (pins
and marked stretches, each with its own instruction). Full contract in
`docs/widget-specs/mp-scene-editor.md` and `references/WIDGET-FEEDBACK.md`; the authoring
craft is in the `motion-design` skill.

**The motion vocabulary** — what "real motion design" is made of, all per-element:

- **Entrances / exits** — fade, slide (from an edge), scale/pop, blur-in, mask-reveal.
- **Continuous** — list **scroll**, **parallax** (layers drift by depth), text **type-on**,
  counters, marquees.
- **Interaction simulation** — the **tap-dot pulse** and cursor moves that make a UI look
  driven (the magenta taps in the reference).
- **Matched-element smart-animate** — a shared layer **morphs its transform/opacity/content
  from frame A to frame B**, so the interface *moves* between screens instead of dissolving.
- **Kinetic type** — headlines animating in word-by-word or with a character stagger; and the
  **assembling sentence**, where shared words *persist and re-position* across frames while new words
  enter (`AI` → `AI Effects` → `AI Effects made easy.`) — not a per-frame re-type, and never a cut
  (recipe: `MOTION-PATTERNS.md` *"Progressive text build"*).
- **Camera** — a gentle push-in/scale on the whole comp for emphasis; or, when a connective
  through-line (a stroke, road, path, ribbon, type baseline — any content, not only a vector) runs
  off one frame's edge and continues into the next, **tile the frames into one world canvas** at the
  offset that makes the line continuous and **travel the viewport along it while the line draws on in
  sync** — one continuous shot, not a cut. (The pan is an **empty-"world"-layer rig**, not a
  `composition.camera` pan, which is a v1 no-op — detection + full recipe in `references/TRANSITIONS.md`.)
- **Brand outro** — the closing logo lockup.

Craft rules: entrances ease **out**, stagger siblings (~0.05–0.12s apart) rather than
firing together, and let the matched elements carry continuity so new elements are the
only things entering at a seam. Depth sells it — background panels drift less than
foreground.

Keep the motion legible: lead with the simplest move that reads (a preset entrance, a matched
smart-animate), tune params only when the designer asks, and drop to raw keyframes only for what a
preset can't express. The designer judges the result on the played scene, not a description.

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
"Present" means you **actually call the preview** (`picsart_scene_editor` / `picsart_media_export`)
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
jumps into the first transition is a slideshow tell (full craft in the `motion-design` skill,
*The opening beat*).

**First, analyze the whole frame sequence — a "pair" isn't always two frames.** Before you start
pairing, read the run with the diff tools (`picsart_media_diff_layouts` / `query_layout`, never by
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

1. **Show the balance FIRST.** Call `picsart_credits` and tell the designer what they have (`balance`,
   plus `nextResetDate` if the pool refills) **before** anything is chosen — this frames every cost
   decision that follows.
2. **Let the designer pick the model.** Narrow with `picsart_model_catalog` (plain
   data, no UI), then open **`picsart_model_choice`** with 2–3 candidates that fit the brief (exactly
   one marked `recommended`, each with a `creditsNote`); the pick returns as widget context. Don't
   pick silently when the trade-offs (duration vs resolution vs cost vs audio) are the designer's.
3. **Assemble params** with `picsart_model_params` (the model's schema) — prompt, duration, aspect,
   resolution.
4. **Get the EXACT cost — `picsart_preflight`** (free): it validates the params *and* returns
   `credits`, the dry-run price with no charge. Fix every `errors` entry before going on.
5. **Ask for consent, showing the number.** State it plainly — *"this will cost ~N credits; you have
   M"* — and wait for an explicit **yes**. **No preflight cost shown + no explicit yes = no
   generation.** This is a hard gate: the only credit-spending action in the plugin, never run
   unasked. If `preflight` returns `credits: null` (pricing unavailable), say so and either get
   consent to proceed at unknown cost or stop — never charge silently.
6. **Generate** with `picsart_generate` (video defaults to `async: true` → a job handle; pass the
   project's `folderUid` so the take is filed under this design).
7. **Monitor** with `picsart_render_monitor` on the job(s) — it polls and posts the finished URL back;
   never ask the designer to wait or check.
8. **Place the result** as a `media` layer in the scene (it's real external footage — a legitimate
   video asset, the one uploaded asset that's generated rather than exported from Figma), positioned
   like any other layer, then previewed in the editor for approval as usual.

## Formats — MP Scene is the source of truth

Everything is authored and edited as an **MP Scene** — the format the SDK natively
supports and the one every `picsart_media_*` edit / validate / query tool speaks, and the
one `sceneRef` points at. The **mp4** is *derived* from it at Stage 5 (`export`). The MP
Scene is the single editable source of truth — keep it and edit it; the mp4 is the final
render, never an editing surface.

## The state — `motion.json`

Keep project state in `motion.json`, updated whole at every milestone. **Never print it
in chat** — a request to *see* something opens the panel, not the data.

```json
{
  "project": "ai-playground-ad", "stage": 3,
  "source": { "kind": "figma", "fileKey": "…", "frames": ["node:1:2", "node:1:8"] },
  "target": { "ratio": "9:16", "width": 1080, "height": 1920, "fps": 30 },
  "sceneRef": ".mp-ai-output/scenes/<hash>.json",
  "frames": [
    { "id": "f1", "name": "model picker", "hold": 3.0,
      "layers": [
        { "id": "f1_tabs", "role": "chrome", "type": "group", "matchKey": "tabs",
          "transform": { "x": 80, "y": 120, "w": 920, "h": 96, "opacity": 1, "z": 10 },
          "asset": { "url": "https://…/tabs.png" },
          "motion": [ { "kind": "slide", "from": "top", "at": 0, "duration": 0.5, "easing": "ease_out" } ] },
        { "id": "f1_list", "role": "content", "type": "raster",
          "transform": { "x": 80, "y": 260, "w": 920, "h": 1300, "opacity": 1, "z": 5 },
          "asset": { "url": "https://…/model-list.png" },
          "motion": [ { "kind": "scroll", "axis": "y", "by": -600, "at": 0.6, "duration": 1.8, "easing": "ease_in_out" } ] },
        { "id": "f1_tap", "role": "fx", "type": "vector",
          "transform": { "x": 610, "y": 940, "w": 64, "h": 64, "opacity": 0, "z": 20 },
          "motion": [ { "kind": "tap_pulse", "at": 2.4, "duration": 0.4 } ] }
      ] }
  ],
  "matched": [ { "key": "tabs", "layers": { "f1": "f1_tabs", "f2": "f2_tabs" } } ],
  "seams": [ { "between": ["f1", "f2"], "kind": "smart-animate", "approved": false } ],
  "gates": { "1": "passed", "2": "passed", "3": null, "4": null, "5": null },
  "blocked_on": null
}
```

Why the shape: a **layer** carries its own `transform`, `asset`/`content`, and a `motion`
list; `matchKey` links a layer to its twin in the next frame so `matched[]` can drive a
smart-animate; a **seam** is a `smart-animate` (matched layers morph) rather than a flat
transition wherever elements are shared. `sceneRef` **moves** with every edit — store
the latest.

A layer's **`type`** records what it *is*, which is what `motion-import` decided the export
format from: **`text`** (live text — the string + font, animatable per-line/char), **`vector`**
(icon/logo/shape kept as SVG or a flat fill — stays crisp at any scale), **`raster`** (a photo
or complex image baked to PNG), or **`group`**. Don't record a vector or text layer as a raster
PNG — that's the defaulting mistake that softens the ad at every scale but the one it was baked
at (see `motion-import`).

**`motion[].kind` labels above are DESCRIPTIVE project state — NOT `apply_motion_preset` ids.**
Each is *realized* through a real mp-scene mechanism, and you must map it, not pass the label to the
engine: `slide` → `apply_motion_preset("slide_in")`; `tap_pulse` → **`apply_motion_preset("tap_pulse")`
— this IS a real preset** (verified on current builds; a one-shot dip to ~0.92 and back, `at` = when it
fires, `appliesTo` includes `shape`; older text here said it didn't exist — that's out of date);
`scroll` / `smart-animate` → `position`/`scale`/`opacity` **keyframes** via `patch_scene` (there is no
`scroll` preset). So the label→mechanism map is: some labels are presets (`slide`, `tap_pulse`), some
are keyframes (`scroll`, `smart-animate`) — **resolve every id from `get_capabilities`** rather than
assuming a label is or isn't a preset, and only if your build lacks `tap_pulse` compose it from
`scale_pop` + `opacity` keyframes. Hand-authoring a whole animation "from scratch" when a real preset
(`scale_pop`, `slide_in`, `fade_in`, `tap_pulse`…) fits is the anti-pattern (see *"reach for the
highest-level tool"*); keyframe only the part no preset covers.

## Cost ledger

| Free (everything in this plugin's loop) | Charged, no rollback |
|---|---|
| layer import, compose, `validate`, layout queries, the panel and its motion previews, filmstrip, **and the renders** — `picsart_media_export`, `picsart_media_contact_sheet` (GPU renders that move no credits) | **generative** tools only — image/video/audio generation, remove-bg and kin |

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
