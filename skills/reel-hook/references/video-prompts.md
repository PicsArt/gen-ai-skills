# B — Script and complete video prompts

Write the creative idea first, then compile its production details. Use Seedance 2.5 by default; honor any explicit model choice. Check the actual provider's current catalog and parameter schema before calling a prompt executable. Names, durations, reference syntax, and supported controls differ between providers. If discovery is unavailable, deliver a clearly marked creative prompt with settings awaiting verification; do not silently switch models.

Before rendering, complete [reference-intake.md](reference-intake.md); for visual-first sequences compile [visual-hook-system.md](visual-hook-system.md).

For Seedance 2.5 writing or optimization, read [seedance-2.5.md](seedance-2.5.md). It adds task selection, explicit asset mapping, whole-second timing, transition repair and model-specific review checks.

## Capability snapshot, not a permanent contract

On 25 October 2026, Picsart's live catalog returned `seedance-2.5`; `picsart_model_params` returned 9:16; 480p/720p/1080p; durations 4–30 integer seconds or -1 automatic; `generateAudio`; `draft`; up to 30 image, 10 video and 10 audio references. ByteDance's [official announcement](https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5) independently describes 30s generation and multimodal references. These limits do not prove exact cut timing or product fidelity. Refresh the provider schema when executing. The live catalog's provider-name filter did not match “seedance”; searching returned model names in the unfiltered video catalog did.

## Package contents

1. **Creative brief:** audience, truthful promise, hook mechanism, payoff and objective.
2. **Full timed script:** every beat, exact VO/dialogue, picture, sound and approved text layers. Name the total duration.
3. **Reference manifest:** asset identifier/path or URL, ownership/provenance, visual role, and product/character details it constrains. Use actual assets, not invented URLs. A missing real-product reference makes fidelity unverified. A broad style reference must not silently replace product identity.
4. **Model settings:** provider and exact model, verified settings separately from prose direction. Camera/lens words are creative instructions unless the API exposes corresponding controls. Choose duration for the story, not to fill the maximum.
5. **One complete prompt per generation run:** setup once, then timecoded shot blocks. For a supporting model, pack coherent cuts into a run; split at supported limits or useful production boundaries. For another model, adapt to its actual supported workflow rather than imposing Seedance syntax.
6. **Edit/assembly notes:** clip order, joins, overlays if allowed, exact logos composited from approved assets, music placement, final caption and CTA. Never ask a generator to invent exact logos or legible UI as proof of the product.
7. **Review criteria:** first frame, contact and occlusion, continuity, true scale, readable product, payoff, speech timing, audio seams, final resolution and CTA destination.

## Prompt structure

Write full concrete prose in each block; placeholders below describe fields, not acceptable final output:

```text
VISUAL SETUP: [one consistent look, material treatment, location, light].
SUBJECTS AND REFERENCES: [bind actual supplied reference identifiers to roles,
using the selected provider's documented syntax]. Exactly [count] relevant
people/objects; [which aspects references constrain].
CONTINUITY: [fixed product shape/color/scale; geography; handedness; start state].
AUDIO: [exact voice language, performance, dialogue/VO, ambient sound and Foley;
music included/excluded according to brief; no unrequested speech].
TEXT: [none, or reserve defined areas for editorial overlays; preserve real
product lettering; no invented branding].

00:00–00:02 — [framing, one primary action, camera behavior, object start/end
state, exact speech and sound timing].
00:02–00:05 — [same concrete decisions; meaningful continuation or cut].
... [all remaining shots with continuous time coverage].
END STATE: [payoff and final composition, audio finish, optional loop seam].
```

Avoid contradictory global camera movement and shot-specific locked cameras. Do not bury five unrelated actions in one short shot. In a multi-run sequence, repeat the exact approved identity/look constraints and state the opening situation completely; “continue as before” is not enough. Reserve time for the last phoneme and meaningful action completion. Keep captions and exact typography in the edit, unless a brand's clean-media rule requires them outside the picture entirely.

For the installed film pipeline, use its own compiler/verification tools when available and required by that workflow; discover their current schemas. Do not invent those calls or import film-specific bans as universal model limitations. Story approval, prompt drafting and generation are separate states.

## Impossible-object choreography

Specify the illusion as a sequence: object appears flat from camera viewpoint; person approaches on a clear path; fingers occlude a defined edge; object gains visible depth while maintaining silhouette and orientation; grip supports its weight; use produces the appropriate consequence. Maintain shadows, reflections, hand anatomy, object count and a plausible path. Intentional floating is allowed; accidental geometry changes are failures.

Practical fallback: locked camera + clean plate + real object interaction + tracked/masked graphic. Match framing, lighting, contact point, grip and motion across passes. A natural gesture hides a cut better than a conspicuous corrective movement. Do not prescribe fixed lens-to-object distances without checking lens capability.

## Example: complete creative prompt for a fictional 12s visual-only cup Reel

This demonstrates structure, not an actual catalog product or a generated result. For a real SKU, replace the fictional object with approved references and verify identity. 9:16, 12s, 1080p, audio on, draft false are supported in the dated Picsart snapshot; refresh before execution.

```text
A playful realistic product illusion on a quiet sunlit pedestrian street. Warm
daylight from frame-left, soft shadows, restrained natural color. Exactly one
adult performer and one plain matte cream takeaway cup with an unmarked brown
sleeve and fitted white lid. No logo or writing. Preserve the cup's silhouette,
lid, sleeve, and normal hand-held scale throughout. The performer moves left
to right; the cup stays near frame center. No other people enter.
Natural street ambience and subtle cloth movement. No music, narration,
dialogue, subtitles, captions, or added graphics except the intentional
flat-looking cup illusion described below.

00:00–00:03: Locked medium side view. At the opening, the cup appears as a flat
cutout suspended at chest height. The performer is already approaching and
reaches with the right hand. Keep both the approaching hand and cup visible.

00:03–00:06: Hard cut to a closer view from the same side of the action. The
right fingers curl naturally around the sleeve, briefly obscuring its right
edge. As the wrist turns, the same silhouette reveals a cylindrical cup with
consistent lid and sleeve. It now moves with the supported grip. No duplicate
cup, teleportation, liquid spill, or extra fingers. Soft paper contact sound.

00:06–00:09: Hard cut to a medium close view on the same side. The performer
lifts the cup and takes one small sip through the lid. A quiet sip, not a crunch.
Keep the cup intact; do not remove or change the lid.

00:09–00:12: Hard cut to a medium view. The performer lowers the cup and looks
back at the now-empty spot with a small amused smile. Hold the final readable
cup and reaction. End the action and ambience naturally; no forced loop.
```

Commercial adaptation: establish the actual cafe/cup identity through approved assets, show the real serving product, and put a truthful visit/order CTA in the allowed caption surface. The illusion alone does not prove the drink tastes good. This example has not been rendered or tested for retention.
