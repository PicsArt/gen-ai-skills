# Motion — propose mode

## Propose mode — assets in, no brief

When the user brings **assets but doesn't say what motion they want**, you propose it. This is the one
place where inventing is the job — but it stays disciplined: analyze, offer a small menu, build the pick.

1. **Analyze the assets — by looking.** `picsart_media_upload` the files, `picsart_media_probe_media`
   for dims / fps / duration, and **view each asset with your own vision** (the same eye that validates
   output — [`scene-validation.md`](scene-validation.md)). You cannot propose
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
   (`scene-validation.md` rung 4, chosen-concept branch).
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
2–3 concepts and let the user pick, and keep it to a **few coherent accents** (motion-principles §7),
never a snow-globe of decorations.

> **This themed-invention licence is PROPOSAL MODE ONLY.** With a Figma design or a stated brief you
> are in fidelity posture: the theme's colours and shapes are **already the designer's** — respect the
> design's palette and **do not invent themed decorations onto it** (that is exactly the trust-breaking
> invention the "animate existing layers only" rule forbids — see `engine-gotchas.md`). Offer a themed
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
([`scene-validation.md`](scene-validation.md)): part-by-part approves each piece
as it's added; whole-at-once approves the full render, then iterates.
