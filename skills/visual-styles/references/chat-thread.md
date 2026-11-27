# Chat thread

A phone chat screen at night: a dark violet gradient ground, a header with a round avatar and a name, speech bubbles that
pop in one by one on the left (the other person, slate) and the right (the viewer, bright violet), small timestamps under
some of them and a three-dot typing bubble that shows before each incoming message. A message bar sits at the foot. It is
a calm story told as a conversation, not a screen recording of a real app and not a comic (that is
[comic-panels](comic-panels.md)). For screen-motion craft see the `app-ui-animation` skill (a pointer, not a requirement).

## Palette and colour roles

| Role | Colour | Its one job |
|---|---|---|
| ground | a diagonal gradient `#15122e`, `#241b52`, `#3a2573` | the deep night screen |
| header and bar | `#1b1838` | a slightly lighter panel for the header and the message bar |
| incoming bubble | slate `#2f2a55` | the other person's messages |
| outgoing bubble | violet `#7a5cff` | the viewer's messages, the one saturated colour |
| text | off-white `#f4f2ff` | every message and the name |
| timestamp, hint | `#9d98c9` | small and quiet |
| avatar | amber `#ffb86b` disc with a brown `#7a3b00` head-and-shoulders figure | the one warm colour, with a green dot `#37d67a` for online |

Hero colour: violet `#7a5cff`. The amber avatar is the only warm spot, the green dot the only green.

## The medium

- **Bubbles are pills fitted to their text**, left-aligned for incoming and right-aligned for outgoing, wrapping inside a column about 760 px wide. The incoming column starts at x 100 and the outgoing one ends at x 980.
- **Typing is a pill with three dots** that bounce on a 1.4-per-second sine, each dot 0.18 of a cycle after the last.
- **The header** is a panel with a chevron, an avatar made of three shapes, a bold name and a green status line.
- **The thread does not scroll in the proof:** it is laid out down the whole screen, six rows 180 to 220 px apart.

## Rates

| Held rate | Root rate |
|---|---|
| none | everything: pops, the dots, timestamps |

## Boil

None: the screen is crisp and flat.

## Line width under a zoom

The one stroke is the back chevron, 8 px with round caps; the rest are fills, so a camera push keeps clean edges.

## Motion habits, and the transitions

- **A bubble pops in** about 0.35 s with a small overshoot (a back ease, up to about 1.07 of its size) and scales from
  its own side's edge, so an incoming bubble grows from the left and an outgoing one from the right.
- **A typing bubble shows first** for about a second before each incoming message, then is gone as the message arrives.
- **Timestamps** appear 0.2 s after their bubble, the same pop.
- **Rhythm:** a new message every 1.2 to 1.6 s; the pace is the chat's, so a reply can come quicker than a question.
- Transitions: the screen slides off up, or the last bubble grows to fill the frame and becomes the next scene.

## Type

A plain humanist sans at 42 px for messages, 26 px for timestamps, 44 px bold for the name, off-white on the bubbles. No
emoji in the recipe; messages are mostly short (five words or fewer), with one longer line allowed for the story.

## Scene features used

Hints, not rules: a box that fits its text is the look, so check the box-fitting caption decorations in `picsart_scene_capabilities` and
the "A box that fits its text" note in app-ui-animation; any other way of making fitted pills works. The proof used caption
boxes, text and shape layers and scale expressions for the pops.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. The header, the bubbles and the bar stay inside the safe area, with 40 px or more of margin at each side.
2. Incoming bubbles are slate on the left; outgoing are violet on the right; no other bubble colour.
3. Every text reads at phone size: messages 42 px, nothing under 26 px.
4. A typing bubble is visible only just before an incoming message.
5. Timestamps sit under their bubble and never touch the next one.
6. The last message is fully visible at the end and the message bar is never covered.

QC: lean on a contact sheet across the thread and the viewer's pass at normal speed for the rhythm.

## Build with the tools (a hint, optional)

Any construction that keeps the look is fine, including a template driven by a list of messages. Check that a long
message wraps inside the column and that a bubble keeps its box fitted.

## Do / don't

- **Do** keep the two sides one colour each so the thread reads at a glance.
- **Do** let a typing pill lead each incoming message.
- **Do** keep messages short.
- **Don't** copy a real messenger's interface, logo or colours; this is a generic chat.
- **Don't** fade the bubbles; they pop by scale.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Rate split: everything runs at the root rate; nothing is held.
  - Nothing fades: a bubble pops by scale, the typing pill scales to nothing.
  - Height is shadow: none; the screen is flat.
  - Boil: none.

## Originality guard

Design your own names, messages, avatar and palette. It must not copy a messenger's interface, brand colours or icons, or
a known person's chat. A dark gradient screen, side-by-side pill bubbles, a typing indicator and timestamps are the style.

## Proven on

A 10 s portrait clip (1080 by 1920, 24 fps): six messages between two people, three typing
bubbles and four timestamps; exported locally, not on the hosted renderer. The clip builds up and does not loop.

**Not proven:** the stage editor (not tried), the transitions (the screen sliding off up, the last bubble growing to fill the frame), a slight banding in the dark gradient, a scrolling thread (more messages than fit), images or emoji in a bubble,
a read receipt, a group chat with several senders, a landscape frame and a seamless loop.
