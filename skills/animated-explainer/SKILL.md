---
name: animated-explainer
description: 'Make an animated explainer you can edit afterwards: one idea made clear by narration and drawn or built 2D or 3D animation (a diagram, objects, numbers, a host character) that grows as each part is named, not generated video. Use for explain how or why X works, an educational or how-it-works video. Not for a screen recording (make-screen-videos) or generated footage. Triggers include "explain how X works", "explain why X", "how does X work", "teach me / show me how X works", when X is a real-world topic. "Explain how X works" comes here, not to a text answer, when the user is in a video or Picsart context, and applies inside a code repository too when X is not part of the user''s code or files. A question about the user''s own code ("explain how this function works") stays a normal answer.'
metadata:
  uses: scene-building-basics, visual-styles, voice-over-generation, spoken-captions, scene-animation-reference, motion-pattern-library, linked-element-motion, character-rigging, lip-sync-lines, background-music, motion-review
  optional: visual-styles, voice-over-generation, character-rigging, lip-sync-lines, background-music
  title: Make an explainer
  short-description: Explain one idea with a narrator and a diagram that grows
  argument-hint: '[the idea to explain, and who it is for]'
  starter-prompt: Make me an animated explainer about an idea.
argument-hint: '[the idea to explain, and who it is for]'
---

# Make an explainer

When you read `picsart_scene_capabilities` or the recipe index (`picsart_scene_recipe` without `name`), pass `useCase: "animated-explainer"`: the answer leads with what this job reads and names the rest in one line.

Read picsart-video-rules first. A narrator explains one idea and the picture grows with the voice. A request that asks to explain something comes here, with a host character only when the user wants one. A request that names a story, or a character's journey, goes to animated-story, which this use case never loads: the stages below reach the shared skills directly.

Before acting on a stage, load the available skills in its row that apply to this job, also when the work resumes there.

| Stage | Gate | Skills |
|---|---|---|
| 1. The question | ASK | scene-building-basics |
| 1b. The style | ASK | scene-building-basics, visual-styles |
| 2. The script | ASK | scene-building-basics |
| 2b. The scene table | ASK | — |
| 3. The scenes | SPEND | scene-building-basics, scene-animation-reference, motion-pattern-library |
| 4. Join and host | SPEND, REVIEW | character-rigging, lip-sync-lines, scene-building-basics, spoken-captions, background-music, motion-review |
| 5. The voice and the timing table | SPEND, REVIEW | voice-over-generation, spoken-captions, motion-review |
| 6. Review | REVIEW | motion-review, linked-element-motion |
| 7. Export | DELIVER | scene-building-basics |

**Review goes by round, on the whole film, never a card per scene.** Every scene animation the user reviews opens in `picsart_scene_editor` (picsart-video-rules, "Every scene animation is reviewed in the editor"): one card on the joined root per round: round 1 is no editor card but a plain-text scene table (stage 2b, before any spend), round 2 every scene built, silent, with the captions timed (stage 4), round 3 the same film with the voice (stage 5). The user pins or comments anywhere on it; map each pin's time to the scene that holds it (the table's starts and lengths) and fix those scenes. After each card ask with the question tool and two buttons, **OK** and **I pinned changes**, never end the turn silent. A single scene over about 15 s that is the riskiest shot may get its own early card.

## 1. The question

Turn the request into one paragraph and ASK (with `picsart_ask`, found as picsart-video-rules says, for any closed choice, a multi-select included, so the options are buttons the user taps, the recommended one first; then your host's own question tool, such as AskUserQuestion; only where all fail, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) the user to approve or edit it in one turn:
- **The idea**: one thing the viewer could repeat afterwards.
- **The question** it answers, a person's question the video opens on, and the person it returns to with the answer.
- **One metaphor** from the viewer's world, used from start to end.
- **The arc**: the question or problem, what is at stake, the idea, how it works one part per beat, and the answer.
  As a guide and never a rule, about 20% problem, 15% solution, 45% how it works, 20% payoff. Make the cost of the
  problem felt before the how. The problem and the stakes are brisk, the solution is one plain sentence with one clear
  hold, how it works is the slowest (one scene per step, each held), and the payoff holds on one end card.
- **The size** the request names: ratio and length decide, and nothing here caps either.
- **A host**, yes or no. A host is a character the viewer meets: one from the saved library or the ready-made cast.
- **The sound**, suggested here in plain text with a yes or no for each: a narrator's voice (the explainer is built around it) and a quiet music bed under it. Each says what it costs; the user is free to say no to either, and no audio is made or paid for without that yes and the credit quote. Captions are on by default, in one line the user can say no to. None of these is a separate question.

Facts come from the user's source text when they send one. A number that is not in the source is marked illustrative.

**No source text, factual topic: research first.** When the user gives no source and the topic is factual or technical
("how a boxer engine works"), search the web before writing the plan, if the host has a search tool. Check each key
fact and every number against 2 or 3 reliable sources, preferring official, academic or maker sources over blogs. List
the sources (title and link) in the plan paragraph the user approves. Every number shown on screen traces to one of
them and lives in the scene's one data block. Anything still unsourced is marked illustrative, as above. With no
search tool, say in the plan that the facts come from general knowledge. Restate facts in your own words and never
copy a source's sentences. A request that comes with source text does not search.

## 1b. The style

Once the idea and the question are approved and before the script or any storyboard, the look is fixed in one ask. A
style named in the request (by its label or id) is taken as asked, with no picker. Otherwise read the style index with
`picsart_scene_recipe` `name: "visual-styles"` (`references/style-index.md`) and open `picsart_scene_picker`, one tile
each with its label, notes and `previewUrl`, and a `category`: the chip the index's "Category chips each use case shows" NAMES for the row in the animated-explainer column, else `Other styles` (every card gets one). Mark 4 to 6 cards `recommended`, `flat-explainer` among them (a style the request names goes first, 4 to 6 in all). Order the cards by that table's chip order, `Other styles` cards last (the board orders its chips by first appearance); within a chip, in this order:
- `flat-explainer` first: the one-click default when the user skips;
- then every row whose `use` is `graphic`, in the index's order;
- then the film rows that explain well: `stick-explainer` (whiteboard), `line-boil-sketch` and `one-line`.

No other film row is offered here: a story's look is animated-story's. In the same single ASK (with `picsart_ask`, found as picsart-video-rules says, for any closed choice, a multi-select included, so the options are buttons the user taps, the recommended one first; then your host's own question tool, such as AskUserQuestion; only where all fail, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says), and not in a second
turn, ask for the **palette** (the brand's or the user's colours, or "the style's own"), the **length** (a number of
seconds, or "short") and the **facts**: the source text, figures or links the explainer must stay true to, or "none". A
number that is not in what they send is marked illustrative. When a host was asked for, it is drawn in the picked style
(a flat figure in a flat style, a stick figure on the whiteboard), never a different kind of character beside it.
Keep the picked style's row for the rest of the video; stage 3 locks its type scale and colours from it.

## 2. The script

Write the narration first, as short phrases, one idea each. Every phrase is a cue point: a part of the picture
appears when its phrase names it. Then ASK (with `picsart_ask`, found as picsart-video-rules says, for any closed choice, a multi-select included, so the options are buttons the user taps, the recommended one first; then your host's own question tool, such as AskUserQuestion; only where all fail, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) for approval of the script, with the cue marked in each phrase.

Write it as people speak: contractions and short sentences. Pace it with arithmetic and no tool: spoken narration runs
about 2.2 to 2.3 words a second, about 2.0 for technical or number-heavy lines. As a budget, 30 s is about 69 words,
60 s about 138, 90 s about 207. A scene lasts its words
divided by that, plus about 0.4 s; a silent beat holds at least 1 s. About 19 words fill a 9 s scene, and few scenes
should pass 26. If a scene's words do not fit the picture it needs, trim the script and never stretch the motion.

One idea to a scene: a scene that carries two is split. Write a worked example into the script, not an abstraction: the
explanation shows one case and then names the rule.

## 2b. The scene table (round 1)

Before any spend, show the scenes as a plain-text table inside the stage-2 script ask: one row per scene, in order, with its name, its length (its words ÷ 2.2 plus about 0.4 s; a silent beat at least 1 s) and its phrases. Ask OK or what to edit, in plain text; no editor opening here. It costs nothing, and the order, the lengths and the words are the user's to change here.

## 3. The scenes

Build each scene silent, as its own scene, as character-rigging's "Films are scenes of scenes" says, with `returnSceneUrl: true`,
so a scene can be changed without touching the others. There is no voice yet: a cue's second is its word's offset in the
scene's phrases ÷ 2.2, and the scene's length is its words ÷ 2.2 plus about 0.4 s.

**Draw the real thing once, before any scene.** From the research and the script, list the real parts that get named
(for a boxer engine: two opposed cylinder banks, the pistons, the crankshaft, the spark plugs). Draw the object once as
an SVG cutaway, one SVG per part, in real proportions and with silhouettes a viewer recognises. Import each part with its own
`picsart_scene_import_svg_path` call (`svg` for a part drawn with several paths) into its own shape layer named for the part:
a whole-SVG import makes one group per `<path>` and bakes the parent group's transforms into the vertices, so the SVG's own
group names are lost, and a part kept in its own layer is the one thing an animation or a reveal can target. Save it with `picsart_scene_library_save` and place it by `library:` reference
in every scene, never inlined, the way animated-story places props. Never stand a box in for a named part. A moving part
animates on its own layer: pistons slide in their bores, the crank turns. A label sits on the part it names. The
style changes the line and never the vocabulary: a chalkboard draws the same cutaway in chalk (visual-styles).

**No dead title time.** A scene never shows only a title or text for more than 1 s: its drawing starts within 0.5 s
of the scene's start, with the title alongside it or after it.

**Fill the frame for its ratio.** Lay each scene out for its ratio. In 9:16 the diagram spans the middle band and the
caption band at the bottom is reserved; in 16:9 the diagram and its labels go side by side. The content box covers
most of the safe area, and no band larger than about a quarter of the frame stays empty except the reserved caption
band. A label never enters the caption band.

**Lock the style before the second scene** and keep it: one type scale, one colour grammar where each colour has one
meaning (the idea at full opacity, its context at about 0.4, its structure at about 0.15), one easing family chosen by
role (a long ease-out for arrivals, an ease-in for exits, exits 40 to 50% shorter than entrances), and one spring
character, a standard entrance of about 0.4 s and a transition of 0.25 to 0.4 s. A spring moves position and size, and
opacity and colour never bounce. For a hand-drawn look use the
`line_boil` preset on the shapes (scene-animation-reference).

**Reveal on the word.** Each part appears when the voice names it. Set each element's `start` to its cue word's estimated time, about 0.1 s ahead, as scene parameters (one number per cue,
its default that estimate, so the scene previews on its own); stage 5 re-keys them to the measured word times. The `reveal-on-word` pattern is a reference of the motion-pattern-library recipe; read it
with `picsart_scene_recipe` using `name: "motion-pattern-library"` and `reference: "references/reveal-on-word.md"`. Never put everything on screen in a scene's first quarter and
then hold it still.

**A diagram grows in order**: faint regions first, then nodes, then edges, then labels on the settled nodes. A node
arrives from about 85% scale with a settle, an edge draws on over 0.4 to 0.7 s, and a label fades in about 0.3 s, its
neighbours 0.1 s behind it. Hold each step 0.5 to 1.5 s, and let the voice's cue and not a timer start it. The part
being explained is full and the rest dims to about 0.35 over 0.3 s. A label sits on the part it names, with a leader
line, and no legend stands apart from the drawing. A drawn edge draws on with a near-linear easing; in a sequence of
messages, hold about 0.6 s after each.

**A whiteboard look draws one thing at a time**, in narration order, with a hold of 0.4 to 1 s after each lands.
Import each visible line as its own open path with no fill (`picsart_scene_import_svg_path`); a traced picture
gives filled shapes, which draw on wrongly, so redraw the centre lines. Order the paths top to bottom and left to right,
structure before detail, and split a line only where a pen would lift. Draw the outlines first and fade the fills in
after. A label finishes drawing as the voice says it: draw time is about its words divided by 2.3, an emphasis stroke
slower and a connecting one quicker. Clear the board between sections with one wipe in one direction, the
`shape_reveal` transition with `wipe_straight` and the same `angle` every time. A marker hand riding the tip of a drawn
line is not available yet: draw on without a hand.

**Charts**: bars grow from the baseline about 0.06 to 0.08 s apart, a line draws on over 0.8 to 1.2 s with its points
popping in after it, and a bar moves on the same clock as the number it counts. A list enters in rank order, the first
rank first, every row with the same motion and one stagger step.

**A counter and a ring are recipes, not hand-written.** Read `picsart_scene_recipe` `name: "motion-pattern-library"`
before building one: a counting number or a word swap is ONE text layer (`references/counting-text.md`), and a ring, pie,
loader or drum is an `ellipse` with a `trim` item (section "Drawing a line on"), never 100 hand-placed layers. A counter:
`"text": { "expression": "local p = math.min(time / 1.6, 1)\nreturn picsart.formatNumber(72 * (1 - (1 - p)^3), {suffix = '%'})" }`
on a layer with `"timeMode": "layer"`. A ring that fills to 72%, starting at the top:
`{ "transform": { "rotation": -90 }, "content": { "kind": "shape", "items": [{ "type": "ellipse", "size": [400, 400] }, { "type": "trim", "start": 0, "end": { "keyframes": [{ "time": 0.4, "value": 0, "easing": "ease_out" }, { "time": 2, "value": 0.72 }] } }, { "type": "stroke", "color": "#5b6cff", "width": 28, "lineCap": "round" }] } }`.
Every position and size key carries an ease (a key with none draws `linear_easing_by_omission`): `ease_out` for an
arrival, `ease_in` for an exit, linear only for a progress bar.

**Numbers** come from one data block, so every figure agrees. When several figures build up to one, show the small
context first and the biggest last, never open on the hero number, and hold the climax longest and largest. A figure that counts up is one text layer per shown
value, as the `countdown` template does it, switched on in turn from that block, and the per-value layers carry no
entrance: with one, every value pops in. Its scale-in does not overshoot. Pick a font whose digits have equal width and check it by measuring 0 to 9,
or a centred number shakes.

**Text**: a keyword that enters word by word enters about 0.05 to 0.1 s per word apart. A title that has landed stays still. Hold 0.3 to 0.75 s before a payoff. Never read the screen text word for
word in the narration: the voice says the idea and the screen shows its parts.

**Refuse the tells**: a bullet slide, icons in circles, three cards in a row, the whole diagram at once, one easing on
everything, every seam a hard cut or a crossfade.

**Seams.** Use 3 to 5 kinds of transition in the film, each caused by something on screen, a hard cut on at most a
third of the seams, and a morph rather than a cut inside one diagram. Land a cut on the stressed word, and use a match cut between related scenes. Worlds never crossfade into each other.

## 4. Join and host

Join the scenes as character-rigging's "Films are scenes of scenes" says: a root scene with one `scene` asset per
scene (`uri` its `sceneUrl`) and a `track` of clips in table order, each clip as long as its scene.
The voice goes on the root, over the whole track. End on a card that holds completely still for at least 2 s with one
call to action, never three, and design it first. In a 9:16 video keep type and key numbers clear of the top 12%, the
bottom 18% and the outer 5% at each side, with the most important element near the vertical centre; address the viewer
as "you", in lines of about 7 words or fewer.

**Captions are on by default**, off only when the user says so. They come from the same transcript, as spoken-captions says for a voice-over. Group the words by the energy of
the delivery: 2 to 3 words when it is fast and punchy, 3 to 5 conversational, 4 to 6 calm; break at a sentence end, at
a pause of 150 ms or more, or at the word limit. One group shows at a time, in at most 2 lines, for at least about 0.8 s, and gone before the next begins. Size the
text to fit the width and keep it in the safe area, clear of the picture's key parts. A caption never repeats an action the host does.

**A host**, only when the plan has a character (the user asked for a presenter; otherwise no cast board, no library widget, no lookup): pick the character as character-rigging's Cast says, on the cast board
(`picsart_asset_choose_characters`, never `picsart_scene_picker`; it holds the saved characters and the ready-made cast, and a lookup draws nothing first), and place it by `library:` uri. The host
asks the question in stage 1's opening and reacts to the answer at the end, and acts only the beats character-rigging's
actions give. Each action reads once. The host's own lines are voiced as the script says, and its mouth moves on them as
lip-sync-lines says; a host without the viseme mouth set speaks as narration, and the user is told.

Lay a music bed under the voice only when the user said yes to it in stage 1, ducked as background-music says; none when they said no, and their own music, if they send it, takes its place.
Validate the root with `picsart_scene_validate`.

**Round 2.** The captions here are timed at the estimate and the film is silent. Open the root in `picsart_scene_editor`
(one card, the whole film) and ask OK / I pinned changes; fix the scenes the pins point at before stage 5. Before that card opens, run one `picsart-staging:critic-art` pass on the contact sheet (that critic only, not the full panel) that answers one question, "what object is this?"; a wrong answer is fixed before the user sees it.

## 5. The voice and the timing table

**Build with the tools, never with scripts.** Scenes are made and changed with `picsart_scene_apply_template`,
`picsart_scene_apply_preset` and `picsart_scene_patch`, from the recipes in `picsart_scene_recipe` (counting-text for
numbers, drawn strokes / draw-on for diagrams, the motion-pattern-library). It is saved to Drive (`picsart_drive_upload`, `scene`) only when the user asks to keep it. A script may compute values (positions, timings). It never writes the scene document, and nothing is
uploaded with curl.

**No narrator's voice.** If the user said no to the narrator's voice in the plan, this stage makes no voice: no generation, no `picsart_media_transcribe`, no re-keying to measured words and no round 3. The estimated scene and caption timings stay as they are, the timing table is written at the estimate, and the captions carry the words. A recording the user brings is a voice and takes the road below.

The voice is made only after every scene is accepted in round 2, and its measured timings are the timing table.
Generate the narration as voice-over-generation says: quote it with `picsart_preflight`, then SPEND (quote it in one line, then get the yes with `picsart_ask`, found as picsart-video-rules says, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", else your host's own question tool, such as AskUserQuestion; never as a typed question unless both fail; only then those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says).
The user's own recording, received with `picsart_drive_upload_ask` (`accept: 'audio'`), takes the same road.

Get the word timings with `picsart_media_transcribe`, passing `text` the script you voiced: recognition mishears short
lines and invents words over silence, and with `text` the result is the known script on the timing of the speech
heard. A cue the transcript cannot place is named to the user and never guessed.

Write the table, which is also the storyboard: one row per scene with its phrases, each cue's second, the scene's start
and length, the words per second, the visual that grows on each cue, its key motion, the transition into it with what
on screen causes it and the word it lands on, its caption and its assets. A scene over about 2.3 words a second is trimmed in the script and the voice made again.

**Voice lines are placed by their own length.** Each voice line's audio layer starts at its cue and lasts its own probed length (from the voice result or `picsart_media_probe`), never the film's length, so `picsart_scene_validate` shows no `media_window_exceeds_source`.

**Re-key to the voice.** Set every reveal's cue parameter to its word's measured time (about 0.1 s ahead, always within
0.3 s of the word), and make each scene and its clip as long as its measured phrases need: the slot grows and you say so,
and a line is never cut. Reopen and re-save only the scenes whose length or timing changed, and leave the others as they
were. Retime the captions to the words. **Round 3:** open the root with the voice in `picsart_scene_editor` (one card)
and ask OK / I pinned changes.

## 6. Review

Review each scene first, then the root, as motion-review says. Render a contact sheet with `picsart_scene_contact_sheet`
at frame 0, at each cue second, inside each scene and at the end, and look at it. Each failure goes back through its
own path before any export:
- a part appears within about 0.3 s of the voice naming it, never before it, and no scene has all of it on screen in
  the first quarter;
- nodes, then edges, then labels, with the active part full and the rest dim, and each label on its part;
- no visual is still building after its phrase ends: the voice never outruns the picture;
- each scene's last frame reads on its own, as a still, and the end card is still;
- the captions match the voice word for word, one group at a time, inside the safe area, and off the host's mouth;
- one type scale, colours that keep their meaning, easing that varies by role;
- every seam has a visible cause, and not every seam is a hard cut or a crossfade;
- **layout, on each scene**, by `picsart_scene_lint_layout` over the scene's whole length, with a `relationships` entry for
  each label and its anchor (linked-element-motion): fail on a label that is not under or over its anchor, on a label
  that wraps to a second line (measure it with `picsart_scene_query_layout`), and on a caption that repeats text already
  on screen. Read the report and look at the contact sheet: a scene that shows one of these is not reviewed, whatever
  the sheet looked like at a glance.

**The self-check comes before anything is shown.** `picsart_scene_check_motion` shows nothing static for over 1 s except the end hold. Before every `picsart_scene_editor` opening (each review round) and
before export, run `picsart_scene_lint_layout` and render a `picsart_scene_contact_sheet` at each title's and label's
on-screen times. Fix any text that overlaps the diagram or a figure, or leaves the safe area, before opening the
editor: the user never sees a defect the lint or the sheet shows.

This is your own check, run before the last card and again before export; the user's reviews are rounds 1 to 3. After a pin is fixed, reopen the editor on the new version and say which pins you addressed. They tweak timing and colours there or in `picsart_scene_tune`, or ask in words.

## 7. Export

`picsart_scene_export` at the size the request named (default 1080 by 1920, 30 fps) for the root scene. DELIVER the
`downloadUrl`, naming each check that failed its bar before any praise. Offer to save the scenes to the library as
kind `story` with `picsart_scene_library_save`, and do it only on a yes.

Ideas for the diagram, whiteboard, counter and recap rules from iart-ai/explainer-video-skills, MIT.
