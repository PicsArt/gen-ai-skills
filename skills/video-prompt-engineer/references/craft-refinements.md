# Craft refinements for existing prompts

## Contents

- [camera](#camera)
- [motion-timing](#motion-timing)
- [lighting](#lighting)
- [film-look](#film-look)
- [skin-detail](#skin-detail)
- [performance](#performance)
- [continuity](#continuity)
- [product-detail](#product-detail)

Apply only the dimensions in the request. Preserve settled decisions. These are observable creative directions, not guaranteed model controls. Each specialist can be used independently; none requires a sibling skill installation.

## camera

Separate five decisions: framing, camera height and aim, physical path, focus, and support. Use a professional name followed by a visible instruction. Expand MCU (medium close-up), CU (close-up), ECU (extreme close-up), OTS (over the shoulder) and POV (point of view); framing boundaries vary by crew.

- Pan/tilt rotate from a fixed position; truck translates sideways; push in/dolly in and pull back/dolly out travel toward/away from the subject. Translation can reveal occluded surfaces and change parallax. Zoom changes focal length from a fixed viewpoint; it is not a push-in. Real lenses may breathe or change distortion.
- Boom up/down describes vertical travel; crane describes equipment. Pedestal up/down describes a vertical lift without necessarily changing aim. State both height and aim: a camera near the floor need not look up.
- A fixed Dutch angle is not a rolling camera. A rack focus changes the sharp plane between named targets; focus breathing may change framing. Do not promise a perfectly unchanged frame.
- Locked off means a stationary camera. Handheld, stabilized tracking, aerial and performer-mounted describe support or operation, not a complete path. Steadicam and Snorricam are equipment names, not generic synonyms for all stabilization or body mounting. FPV names a control/viewing method; specify banking or a level horizon explicitly.
- Arc and rise, push past and reveal, and other combinations are descriptive directions. Keep a feasible user-requested combination; do not invent an industry nickname or prohibit all combined moves.
- Tracking is broader than following behind. An insert is not every cutaway; a two-shot is not a three-shot. A dirty single includes another person at the edge, but is not always the same composition as OTS. A oner describes a continuous-take treatment; do not claim hidden joins are a true unbroken capture.
- Choose field of view, camera distance and focus target before arbitrary lens numbers. Viewpoint determines perspective; sensor/film format affects the field of view for a given focal length. A lens number in a generative prompt is a request, not calibrated optics.

Review: Check the intended path, start/end framing, occlusions and focus. Preserve existing movement timing unless that is also in scope.

## motion-timing

Keep the chosen route and subject action. Specify timing separately for camera, subject, focus change and edit; they are different clocks.

| Profile | Visible instruction |
|---|---|
| Constant speed | Move at an even rate through the stated travel interval. |
| Accelerate | Start slowly and build speed toward the named endpoint. |
| Decelerate | Begin at the selected pace and progressively slow to a stop. |
| Ease in and out | Build speed gently, maintain the middle pace, then ease to rest. |
| Pause and resume | Arrive at the named view, hold, then resume the route. |

Smooth means stable or continuous; it does not necessarily mean slow or constant-speed. Constant speed through the entire clip conflicts with a gradual stop unless separate intervals are named. Constant speed around a curve is not a fixed velocity vector: use speed or angular rate rather than promising fixed velocity on an arc.

If an actual duration is known, make phases fit that duration; otherwise use start/middle/end and identify timing as an assumption. Do not invent a supported duration or frame rate. Use supported generation settings for export duration/rate. A prompt mentioning a shutter angle does not configure capture physics.

Slow camera travel, slowed subject playback, long exposure blur and fast-forward are different. Describe the moving part, blur direction and desired readability. Keep still areas stable; do not use smear to conceal morphing. A speed-versus-time sketch has time horizontally and speed/rate vertically: a plateau is constant, a rising line acceleration, a falling line deceleration, and zero a hold. It is a conceptual plan, not measured model output.

Review: Check the whole move at playback speed, then inspect the transitions and final hold. No promise of exact physical timing without tool controls.

## lighting

Separate direction, quality, intensity, fill and colour. Identify a motivated key relative to the subject/camera: front, side, back, top or another specified position. Then describe a crisp or gradual shadow edge. Apparent source size at the subject affects softness; soft does not mean dim or low contrast.

Specify shadow-side readability separately with fill or negative fill where useful. A backlight can separate an edge while leaving the front dark; add readable front detail only when the brief needs it. Keep rims local to source-facing edges, not a glow around every object.

Describe what the light reveals: face shape, cloth weave, glaze, machining or glass contours. Soft light must not erase skin or material texture. On reflective objects, source shape and surroundings matter; keep highlights attached to geometry as the object turns.

For a single view, camera-left/right is useful. Across reverse angles, preserve the source in world space (for example, the window beside the door); its screen-side description can change with the camera. Do not force camera-left in every reverse shot and accidentally move the window. Treat setup names as optional shorthand, not universal mood guarantees. Do not invent key-to-fill ratios or lamp settings.

Review: Check cast-shadow direction, shadow edges, face readability, source position and reflections throughout the action.

## film-look

Separate palette and saturation, tonal contrast, highlight roll-off, texture, and optical/finishing effects. Preserve approved brand colours and skin tone. Describe what remains legible in highlights and shadows rather than adding cinematic adjectives.

Grain, bloom and halation are different controls. Grain is texture; bloom spreads bright light; halation is a highlight-edge effect whose appearance depends on the process. Request restraint and local placement when appropriate. Do not use grain or haze to hide unstable geometry or hands.

A film-stock name is an optional reference, not proof of accurate emulation. No movement, genre or era has one universal lens, palette or exposure ratio. Translate the desired look into visible properties; do not invent stock history, processing or technical settings. Monochrome needs tonal separation between objects, not just absent colour.

When repeatability matters, propose a clean generation plus a shared post-production grade/grain treatment outside the generation prompt. Do not silently perform that edit or add paid rendering. Softness, diffusion and grain must preserve required product and facial detail. Do not add scratches, gate weave or flicker unless requested.

Review: Compare start/end colour and the full take at delivery scale. Check texture crawl, clipping, halos and matching across adjacent shots.

## skin-detail

Preserve identity, age, skin tone, makeup and distinctive marks from the brief/reference. Add only plausible visible detail at the shot scale. Do not manufacture wrinkles, freckles or pores as a universal realism recipe, and do not change demographic features to improve realism.

Distinguish surface texture, local colour variation and light response. Request subtle pores where visible, restrained specular highlights and natural transitions through shadow. Skin is not uniformly rough plastic; excessive sharpness or pore contrast can look etched. Soft illumination is not skin blur.

A reference frame may already settle the face and light. For image-to-video, concentrate on preserving those features through the requested motion rather than rewriting the appearance. Do not promise that terms such as subsurface scattering configure a physical renderer.

Review temporal attachment: marks should move with the face, not swim across it; cheeks, eyelids, teeth and ears should preserve form through a turn. Photoreal appearance is not evidence that footage records a real event. These are creative hypotheses to test, not proven cures for model defects.

Review: Compare identity before/during/after movement. Check texture at final crop size, not only an enlarged still.

## performance

Keep the intended action and emotion. Give gaze a target and a reason: notice an object, then react; direct lens contact remains valid for a presenter. Avoid stacking conflicting emotions or mandatory blinking/twitching into every shot.

For movement, describe approach, contact, weight transfer, release and settling only where visible. A supporting foot stays planted during weight transfer; hands maintain plausible grips; clothing responds and settles. Contact shadows alone do not prove weight. Keep geometry and product mechanisms stable.

Match action complexity to available duration and references. Simplify a difficult action as an explicitly labelled alternative rather than silently removing the requested demonstration. Preserve hands/feet in frame when the brief needs to verify them; cropping away defects is not a successful demonstration.

Separate camera movement from performer movement. A deliberate still pose is valid. For dialogue, preserve exact words and distinguish native speech/lip-sync from a separate voiceover workflow; prompt repair alone does not produce audio. Model failure, reference ambiguity and insufficient coverage remain possible even with a clear prompt.

Review: Watch gaze targets, planted contacts, hand grips, proportions and the end state through the whole action.

## continuity

Map people, props and light sources in world space first, using an existing master/shared view or a simple seating plan. Track speaker/listener, gaze target, screen position, body orientation, prop state and action phase for each shot.

Keep camera positions on the intended side of the action axis for conventional coverage. Deliberate axis crossings can work when geography is re-established; do not forbid them universally. A listener looks toward the other person, not automatically past the lens in every kind of film. Direct-address presenters may look into the lens.

Use OTS (over the shoulder), clean single, dirty single, two-shot, master, insert and reaction for their actual functions. A dirty single has some of another person in frame; OTS specifies shoulder-based framing. An insert isolates scene detail; a reaction is not necessarily an insert. A continuous-looking oner may contain joins.

Carry approved identity, wardrobe, product geometry and material references into each independent generation. Shared wording helps consistency but cannot guarantee it. Preserve the world-space key source across reverse angles, not an invariant camera-left label. Match focus, exposure, palette, action phase and background geography at the cut.

For one multi-shot prompt, state shared context once; for independent calls, include the needed context in every prompt. Keep dialogue/audio continuity as a separate edit decision. Do not claim repeatedly generating the same music description yields one continuous score.

Review: Compare shots side by side and at the intended cut; verify references, eyelines, action phase and world-space light rather than matching isolated adjectives.

## product-detail

Keep the approved product’s silhouette, dimensions, finish, colour, markings, wear and working state. Distinguish presentation from condition: a used component can be photographed carefully without becoming new or hiding a defect. Do not invent performance, testimonials or a functioning mechanism from visual polish.

Choose a useful detail and describe how composition/light reveal it: machining, seams, glaze, fabric or glass. Specify a clear contact/support surface, coherent reflections and a restrained background. Premium presentation is a creative treatment, not proof of quality or value. Translate luxury into observable material, light, framing and pacing rather than a living creator or fashion-house imitation.

If a presenter is requested, preserve the chosen adult identity, wardrobe, task and expertise; do not assign expertise or product category by gender or attractiveness. For demonstrations, maintain grip, contact and the real mechanism. Keep exact logos/labels from approved assets or place them in post; do not promise generated typography accuracy.

Keep brand palette and approved references. Do not turn a camera-only request into a new luxury concept, swap a model, or polish a matte/aged surface without permission. Where no reference supports fine detail, call it unknown rather than inventing it.

Review: Check silhouette, wear, finish, labels, reflections, contact and any claimed function throughout the take.

