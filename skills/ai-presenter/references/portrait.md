# The presenter's portrait

A take is only as good as the face it starts from. The avatar model moves the mouth, the jaw and
the head of the portrait it is given, so anything in their way shows in every frame of every take.

## What a take needs

- **One person, facing the lens.** Shoulders square to the camera, head level, eyes open and on
  the lens. A three-quarter view, a profile or a tilted head drifts out of sync.
- **Lips together.** Relaxed, a slight smile at most, the jaw closed. An open mouth or visible
  teeth is a failed portrait: generate it again, and never start a take from it.
- **Nothing over the mouth, the jaw or the chin.** Hair behind the shoulders or behind the ears,
  hands out of frame, and no glasses, microphone, hat brim, large earrings or beard over the lips.
- **Head and shoulders, with room to move.** The top of the head a little below the top edge, the
  chin well inside the frame, the upper chest visible. The take moves the head, and the head bubble
  and the head-and-screen split crop around the face.
- **One soft light with a direction.** A window or a softbox to one side, and a gentle fill from
  the other. Hard side light flickers once the face moves; flat light with no source reads as a
  stock photo.
- **A plain, still background**, softly out of focus: a wall or a tidy room. Nothing that could
  move, such as a screen, leaves or other people.
- **The take's shape.** `kling-avatar` has no aspect-ratio input, so its take has the portrait's
  shape: make the portrait 9:16 for a vertical promo. On Dev on 2026-10-01, a 9:16 portrait gave a
  720×1280 take.

## Writing the prompt

- **Choose the person for the product.** Who would present it to its audience: their age, their
  role, what they wear. Never a real person, and never someone's look-alike.
- **Sentences, subject first.** Describe what is in the picture. Write the needs above as what is
  there ("lips gently closed", "arms relaxed out of frame"), not as a list of "no"s: the image
  models that make presenters read no negative prompt.
- **Realism comes from what a camera would see:** a named lens and aperture, a light with a
  source, and the texture of skin, hair and fabric. Give the face one or two things a real face
  has, such as freckles or one eyebrow a little higher than the other. A face that is too perfect
  reads as generated.
- **Leave out the vocabulary of synthetic images:** "beautiful", "flawless", "perfect skin", "8K",
  "hyperrealistic", "masterpiece", "photorealistic". They bring the plastic, retouched look.
- **Show who they are with clothes and a setting, not adjectives:** "a small-brand marketer in an
  olive knit", not "a friendly, professional woman".

Fill in the braces and keep the rest:

> A vertical head-and-shoulders photograph of {age, heritage and role}, looking straight into the
> lens. {One or two specifics of the face}. {Hair: length, texture and colour}, {tucked behind the
> ears or falling behind the shoulders}, a few fine flyaways at the crown. Natural skin with
> visible pores and gentle tone variation, {makeup}. Shoulders square to the camera, head level,
> eyes open and relaxed, lips gently closed in a slight smile. {The garment and its fabric}.
> Behind {them}, {a plain, still background}, softly out of focus. {A soft light and its
> direction}, with a gentle fill from the other side and natural catchlights in both eyes. Shot on
> a full-frame camera with an 85mm lens at f/4, focus on the eyes, faint grain. The top of the head
> a little below the top edge, the eyes about a third of the way down the frame, the upper chest in
> frame, arms relaxed out of frame.

For example:

> A vertical head-and-shoulders photograph of a woman in her early thirties who runs marketing for
> a small brand, looking straight into the lens. A faint scatter of freckles across the nose, one
> eyebrow a little higher than the other. Shoulder-length dark brown hair with soft natural waves,
> tucked behind both ears and falling behind her shoulders, a few fine flyaways at the crown.
> Natural skin with visible pores and gentle tone variation, minimal makeup. Shoulders square to the
> camera, head level, eyes open and relaxed, lips gently closed in a slight smile. An olive cotton
> crew-neck with a fine visible knit. Behind her, a plain warm sand-coloured plaster wall, softly
> out of focus. Large window light from camera-left, with a gentle fill from the other side and
> natural catchlights in both eyes. Shot on a full-frame camera with an 85mm lens at f/4, focus on
> the eyes, faint grain. The top of the head a little below the top edge, the eyes about a third of
> the way down the frame, the upper chest in frame, arms relaxed out of frame.

## Generating it

Pick an image model with `picsart_model_catalog` (`purpose: "generate"`, `mode: "image"`), and
read its inputs with `picsart_model_params`. On Dev on 2026-10-01, `gemini-3.1-flash-image` made a
usable presenter. Ask for four candidates in one `picsart_generate` call (`count: 4`) where the
model takes a count, at the take's shape (`aspectRatio`) and at the model's 2K or higher.

## Checking it

Look at every candidate (picsart-video-rules, Asset URLs) before any take is paid for, and keep one that
passes all of these:

- one face, frontal, eyes open and on the lens;
- lips together, no teeth showing;
- nothing over the mouth, the jaw or the chin;
- the top of the head and the chin well inside the frame;
- a large face: in a head bubble a small one loses its lips, and the take moves what it cannot see;
- no second face, extra fingers or a warped ear anywhere in the frame;
- skin with texture, not wax or plastic.

When none passes, rewrite the prompt where they failed, and generate again. Check a photo the user
uploads in the same way, but never regenerate or restyle a real person's face.
