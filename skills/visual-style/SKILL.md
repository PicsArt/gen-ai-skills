---
name: visual-style
description: A video's style, chosen by eye and kept - eight named styles as colour roles and text entrances, a brand's colours mapped onto one, the defaults that make a video look machine-made, and a check that a built scene keeps to its style. Use when choosing or applying the look of a built video (screen videos, promos, tutorials), or checking that one does not look generic.
user-invocable: false
---

# Art direction

A video looks made by hand when its colours, type and motion were chosen for it, and generic when
they were left at a default. This skill holds the choice: a **style** is a palette by role and a
text entrance per role, which a builder takes instead of colours of its own.

## The styles

`scripts/style.py` holds them; run it with no arguments for each one's tokens. To the user they
are "styles", never tokens.

| Style | Feel | Suits |
|---|---|---|
| `studio-dark` | premium, cinematic: deep plum, warm off-white words, coral payoff | a launch, a dark UI, creative tools |
| `paper-ink` | calm, editorial: warm paper, near-black ink, a red pencil mark | how-tos for beginners, writing and planning apps |
| `pop-block` | loud, social: flat sunflower, black words, hot pink | Reels and TikTok for a young audience |
| `keynote` | clean product: light grey stage, one electric blue | a feature explainer, a B2B tool |
| `sticky-note` | friendly how-to: notepad yellow, an orange marker, typed titles | tips, "save this for later" shorts |
| `terminal` | technical: green-tinted black, mint text, typed lines | developer tools, AI chats |
| `bloom` | warm, creative: berry stage, blush words, peach payoff | photo, video and design apps |
| `native` | creator-made, not an ad: minimal chrome around the recording | content that should not read as an ad |

Roles: `canvas` is the frame behind everything, `surface` the cards, bubbles and rims, `ink` every
word (it reads on both), `accent` the payoff and the call to action, and `entrance` the text
entrance for titles, lines and the call to action.

## Choosing one

1. **Recommend from the material**, never by habit: the recording's own brightness and colours,
   the product's category, the destination and the audience. Say the reason in one line: "a bright
   UI and beginners: paper-ink keeps it friendly and lets the app's colours lead".
2. **Show three that differ**, on the user's own recording, before anything is rendered: the same
   hook frame and one step frame built in each, sampled on a contact sheet (free). Never ask for a
   style by its name alone.
3. **A brand** (colours the recording shows, or the user gives) goes onto the chosen style's roles:
   `python3 scripts/style.py <style> brand.json`. The style keeps its bones; the brand gives its
   colours. A brand colour that would make the words unreadable is refused with the role it
   breaks: keep that role from the style.
4. Pass the style's id, and the brand when there is one, in the builder's spec as `style` and
   `brand`. The builder resolves them; never copy colours into the spec by hand.

## Defaults that look machine-made

Check a build against this list before the user sees it. Each hit is fixed, or kept with a one-line
reason ("the app itself is navy, so the canvas follows it"):

- the same dark navy or black stage whatever the subject;
- every text entering the same way;
- everything centred, with nothing breaking the grid;
- a push-in as the only move;
- pure `#000000` or `#ffffff` as the canvas or the words;
- purple-to-blue gradients, gradient text, and full-frame gradients on a dark canvas (they band
  when the video is compressed);
- a hook that opens on a login screen or an empty app instead of the result;
- a hook that is a product or a posed character with a slogan over it: the retention-hooks skill's ad
  tells;
- a logo sting, a greeting or a title card before the first real frame, or a lower third in it;
- the same layout or the same move on two beats in a row;
- glow halos around words or panels, and emoji standing in for icons;
- a centred headline over a gradient as the hero, with nothing of the product in it;
- "amazing", "seamless", "powerful" on screen where the result should do the talking, and
  "Introducing…", "check this out" or "like and subscribe" anywhere.

## Checking a build

`python3 scripts/adherence.py <file>` with `{ scene, style, brand? }` prints `{ ok, findings }`:

- `off_palette`: a layer draws a colour the style does not have, including colour keyframe
  values. Rebuild with the style; never patch one layer's colour.
- `one_entrance`: every text enters the same way. Use the style's entrances.
- `linear_move`: a position or scale that moves on a linear curve. Every move eases; the house
  curve is screen-recording-zoom's.
- `overshoot`: a bounce on a panel, a position or an opacity. A bounce belongs only to a payoff
  pop, the scale of a word or a shape.

Motion checks include masks in `mask.clip` or legacy `mask.layer`, with `clip` taking precedence.
A mask's fill and a scrim's black are not drawn
colours, so they never count.
