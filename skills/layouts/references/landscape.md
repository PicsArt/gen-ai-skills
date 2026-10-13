# A landscape frame

A 16:9 video, 1920×1080 at 30 fps, made from a desktop recording: a tutorial, an explainer, a
walkthrough. A desktop recording already has the frame's shape, so it needs no panel: it fills the
frame, and the push does the framing a panel does in the vertical frame.

## The recording fills the frame

- **At rest, the whole recording**, `fit: "contain"`, framed with the formula in SKILL.md as a
  panel the size of the frame: rest `S = max(1920 / srcW, 1080 / srcH)`. Run `scripts/framing.py`
  with `frame: { w: 1920, h: 1080 }` and a panel `{ x: 0, y: 0, w: 1920, h: 1080 }`; it uses that
  `S` when you leave `S` out.
- **A 16:10 desktop** (1440×900, 2560×1600) loses a thin band at the top and the bottom. Frame on
  the content, as a portrait recording does in the vertical frame, so the band lost is the empty
  one: a browser's empty tab strip, never the app's toolbar.
- **The push** leans in on where the screen responded, as the screen-zoom skill says, on the
  full-frame layer, with the focus clamped so the frame never shows past the recording's edge.
  A screen that stays on for minutes also zooms back out between pushes (screen-zoom's zoom out).
- **No panel card, no backdrop, no rim.** Two beats are the exception, and both put a card over the
  recording's own footage, cover-fit, blurred and darkened behind it:
  - **the result**: the finished result on a card the shape of its box, at most 1280×720 at
    x 320, y 240, under its title;
  - **a chapter card**: the chapter's first screen behind its title, the title centred on it.

## Where text goes

The frame has no dark band of its own, so every word sits on a dark bubble, inside the title-safe
area: the inner 90% of the frame, x 96–1824 and y 54–1026.

| Text | Where | Size |
|---|---|---|
| **The step line** | a lower third: a bubble 1536×110 at x 192, y 820, the line centred on it; 160 tall for two lines, its bottom kept at y 930 | 40 px, a line of about 60 characters |
| **Captions** | the bottom band, under the lower third: caption style `offset: [0, 450]` (y ≈ 990) | as the captions skill says |
| **A title** | the result's: centred above its card, at y ≈ 130; a chapter's: centred on its card | 72 px; a chapter's at most five words |

**Never over the zoomed box.** When a push lands on a box in the lower third, the step line moves
to the top band, a bubble at x 192, y 150, for that step, and the captions move with it. Keep the
text off bright content, as SKILL.md says.

## Callouts and private data

A ring, a highlight or an inset of a small control on the response box are the motion-design
skill's patterns; name that skill for them rather than drawing them here. The push alone is the
first version. Anything private on screen (an email, a key, a customer's name) is framed out or
covered, as the motion-design skill says, before the user sees a draft.
