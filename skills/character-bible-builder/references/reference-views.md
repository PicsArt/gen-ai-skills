# Reference views and clips

Which views to ask for, what each 1 is actually for, and how to write the prompts. A list of
view names is not useful on its own: a user who does not know what a profile is for will drop it
to save credits, and the profile is the view that catches the drift.

Every prompt on this page reuses the **same** description text, byte identical, from
`## Verbatim description` in `<bible>/<character-id>.md`. Only the view clause, the framing and
the background change. If the description varies between views, the views will not agree with
each other and the sheet is worth nothing.

## The 6 required image views

### Front, neutral

Head and shoulders or chest up, camera at eye level, straight on, neutral expression, mouth
closed, eyes to camera, even light, plain background.

**What it is for.** This is the identity anchor. It is the view a person compares every later
render against, and it is the frame most image to video calls will start from, so it has to be
correct rather than flattering. Neutral expression is not a stylistic choice: an expression bakes
muscle deformation into the anchor, and every clip started from it will inherit the expression.

### Three quarter

Head turned about 45 degrees, eye level, same light and background.

**What it is for.** The volume of the head. A front view leaves the cheekbone, the depth of the
brow and the shape of the skull undetermined, so a generator invents them, differently each time.
This is also the angle most generators default to when a prompt does not name an angle, which
means it is the angle most of the user's real shots will be in. A correct 1 in the bible stops
the invention.

### Profile

Full side, eye level, same light and background.

**What it is for.** Nose, chin, brow and ear placement, none of which a front view pins down. It
is also the cheapest way to catch drift: 2 generations of the same character will agree from the
front and disagree in profile long before anybody notices from the front.

### Full body, standing, feet visible

Whole figure in frame with headroom and the feet inside the frame, arms relaxed at the sides,
neutral stance, plain background, no crop.

**What it is for.** Proportion, height, limb length and footwear, and it is the source of the
silhouette used in `references/silhouette-check.md`. Feet inside the frame is not a detail: a
cropped reference leaves the leg line and the footwear undefined, and a generator will put the
character in whatever shoes it likes, which changes the whole lower silhouette.

Ask for this against a plain mid value background so the outline can be read directly.

### Expression range

4 to 6 heads on 1 sheet, same character, same light, same angle, each 1 a different expression.
Neutral, and then the expressions the script actually needs. Pick them from the script rather
than from a standard set: a comedy needs delight and dismay, a thriller needs fear and control.

**What it is for.** So a scene that needs an emotion does not restyle the face to get it. Asked
for an angry version of a character with no angry reference, a generator commonly changes the
brow ridge, the jaw and sometimes the age, and the character stops being the same person at the
exact moment the scene needs them most.

Ask for 1 sheet rather than 6 images. Held on 1 sheet, the expressions are generated against
each other and stay consistent. Generated separately they drift, which defeats the purpose.

### In the story's setting

The character standing in a location from the script, in that location's own light, framed full
body or mid shot.

**What it is for.** Every other view is studio grey, and studio grey lies. This view proves the
wardrobe reads against the world's own palette, that the character does not vanish into their
background, and that the palette survives the lighting the style guide specifies. When a style
guide exists, use the named variant from `<guide>/lighting.md` that fits the character's most
common scene, not the default setup.

It is also the view a director looks at to decide whether the design is right, which makes it
worth generating even when credits are tight.

## Optional views

Ask for these only when the reason applies. Each 1 multiplies across the cast.

| view | when it earns its cost |
|---|---|
| Back | Hair is worn up or long, there is a hood, a pack, a cape, a logo, or the character is seen walking away in the script |
| Hands | Hands do something specific in the script: play, sign, sew, hold a weapon. Hands are where generation fails, so a reference helps |
| Wardrobe variant | The character has a second outfit that appears in more than 1 scene. Generate the front and full body only, reusing the same face description |
| Age variant | The script has a younger or older version. Treat as a separate character id with a shared face rule, not as a view |
| Seated | The character is seated in most of their scenes, which is common for interviews and dialogue driven work |

## Writing the image prompts

Order the clauses the same way in every prompt, so the only difference between 2 prompts is the
part that is meant to differ:

1. The medium and style clause, from `<guide>/fragments.md` verbatim when a guide exists.
2. The description, from `### Long form`, byte identical.
3. The view clause: angle, shot size, what the eyes and mouth do.
4. The background clause: plain, mid value, no props, or the setting for the in-setting view.
5. The lighting clause: even and neutral for the sheets, or from `<guide>/lighting.md` for the
   in-setting view.
6. The exclusion clause.

Check `Applicability` in `<guide>/camera.md` before adding any lens or depth of field language.
A flat illustrated style has no optics, and asking for an 85mm lens on it fights the style.

For the sheet views, ask for no props, no scene, no action and no expression. Anything in the
frame that is not the character is a thing a later generation may inherit.

## Reference clips: 5 seconds, always

**Short form only. 5 seconds.** Do not offer a longer option and do not agree to 1 if asked
without saying what it costs:

1. 5 seconds is the cheap unit, and the duration is the multiplier on a bill that already scales
   with the cast. 9 characters at 3 clips each is 27 generations.
2. A reference clip carries no story. It shows a turn, a walk or a look. None of those needs
   longer, and the extra seconds add nothing that a reference is for.
3. Identity drift appears **inside** a longer clip. A 12 second clip often ends on a different
   face than it started with, which makes it useless as a reference and actively misleading if
   somebody pulls a frame from the end of it. 5 seconds does not have time to drift.

### Turnaround

5 seconds. Locked camera, full body, the character rotates in place at a steady speed, arms
relaxed, neutral expression, plain background, even light.

**What it is for.** Every angle in 1 asset. If you generate only 1 clip per character, generate
this. Frames pulled from it fill in the angles the still sheet does not cover.

Start it from the full body still when the model supports image to video, and then **prompt the
motion only**. Do not redescribe the character to a model that already has the frame.

### Walk

5 seconds. Locked camera, side on, full body, the character walks across frame at their own
speed, plain background.

**What it is for.** Gait, weight and posture in motion, which is the part of a character no still
carries. Worth the credits when the character walks in the script, when gait is part of who they
are, or when 2 characters were close in the distinction check and posture is 1 of the differences
holding them apart.

### Look

5 seconds. Head and shoulders, locked camera, the character holds a neutral expression and moves
to 1 named expression, no dialogue, no speech.

**What it is for.** Dialogue heavy characters, and anything going to lip sync. It records how the
face moves between the states on the expression sheet, which is what a generator gets wrong when
it has to animate an emotion it has never seen on this face.

No dialogue in the prompt. Generated mouth shapes for speech are unreliable and a reference clip
full of bad phonemes is worse than no clip.

### Writing the clip prompts

- Name the camera. `Locked camera, no movement` for all 3 clips unless there is a reason
  otherwise. An unnamed camera drifts, and drift in a reference clip reads as the character
  moving when they are not.
- Name the subject motion and nothing else. 1 action per clip.
- Describe the background even when it is meant to be nothing: `plain mid grey background,
  empty`. An undescribed background is where a model puts whatever it likes.
- Carry the exclusion clause, and include the artefacts that matter for a figure: extra limbs,
  extra fingers, warping, text, watermarks.
- Keep the whole prompt under about 120 words. Past that, generators drop clauses, and the ones
  they drop are at the end, which is where the exclusions are.

If the user wants shot prompts for the actual scenes rather than references, that is
`video-prompt-engineer`. Hand it the slug and the character ids and let it take the descriptions
verbatim out of `<bible>/<character-id>.md`.
