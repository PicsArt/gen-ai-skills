# Device mockup

A product-promo frame: a dark phone with a white habit-list screen stands on the right over a warm peach gradient, and a
split headline sits on the left, two lines in ink and two in coral. The list ticks itself off one row at a time while a
teal progress bar fills. It is a clean, bright demo of an app idea, not a screen recording of a real app and not a dark
tech board (that is [dark-tech-explainer](dark-tech-explainer.md)). For screen-motion craft see
the `app-ui-animation` skill (a pointer, not a requirement).

## Palette and colour roles

| Role | Colour | Its one job |
|---|---|---|
| ground | a diagonal gradient `#fff3e6` to `#ffd9c7`, with two soft discs `#ffe0d0` and `#ffcdb8` behind the phone | a warm studio backdrop |
| phone body | ink `#1c1b22`, shadow `#000000` at 18 % | the one dark object |
| screen | `#fbfbfd`, rows `#f1f1f7`, checkbox rim `#c9c9d6` | a light app screen |
| headline | ink `#1c1b22` for the first half, coral `#ff5a4a` for the second | the split: set-up, then pay-off |
| tick, progress | teal `#16b58f` | the one cool colour, the "done" state |
| small text | `#8a8a99` on the screen, `#7a6a62` on the ground | a quiet caption |

Hero colour: coral `#ff5a4a`. Teal appears only on done states.

## The medium

- **The phone is three shapes:** a dark rounded body, a slightly smaller white screen, a small round dot for the camera. The
  corner radius of the body is about 76 px on a 470 by 920 shape. A flat soft shadow sits 14 px below it.
- **Rows** are rounded `#f1f1f7` cards with a hollow circle; a tick is a teal disc, a little bigger than the circle, with a white check that covers the circle's rim, so the empty
  circle shows until its row is done.
- **The headline is split** by colour, one word to a line, left aligned, a heavy grotesque at about 112 px.
- **The screen text is a plain sans**, 34 px for rows, 48 px bold for the title.

## Rates

| Held rate | Root rate |
|---|---|
| none | everything: the headline slides, the ticks, the progress bar |

## Boil

None: the frame is crisp and flat.

## Line width under a zoom

The only strokes are the check path (7 px, round caps) and the checkbox rim (5 px). A camera push keeps them readable.

## Motion habits, and the transitions

- **The headline lands first:** each word slides in from the left about 260 px with a cubic ease-out over 0.5 s, 0.3 s
  after the one before.
- **Ticks pop** over 0.4 s with a small overshoot (a back ease), one row about every 1.1 s, and the progress bar
  steps to a quarter, a half, three quarters and full on each tick.
- **The phone stays still** while the content moves: a mockup that floats needs every row to float with it.
- Transitions: the phone slides off up and the next screen slides in; a wipe in the coral of the headline.

## Type

The headline: a heavy grotesque, two ink words then two coral words, with a small lowercase tagline under it. Screen
text: a plain sans. No second typeface.

## Scene features used

Hints, not rules: nothing here depends on one effect, so use whatever draws the shapes, text and pops (`picsart_scene_capabilities`
lists what is available). The proof used shape and text layers with expression-driven slide and pop.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. The headline is fully readable by the end and never touches the phone.
2. The phone sits inside the frame with 40 px or more of margin, and nothing is cropped.
3. Coral is used for the headline's second half only; teal is used for done states only.
4. Every row's text fits its card; a tick sits exactly on its circle.
5. The progress bar's fill matches the number of ticks at every moment.
6. Screen text reads at phone size: nothing under 28 px.

QC: lean on a contact sheet across the five ticks and the viewer's pass at normal speed for the pace.

## Build with the tools (a hint, optional)

Any construction that keeps the look is fine, including a template with a list of habits. Check that a long habit name
fits its card and that the bar steps as each tick lands, not as it starts.

## Do / don't

- **Do** let one thing move at a time: the headline, then the ticks.
- **Do** keep the phone a plain generic shape.
- **Do** keep the screen to one task with four rows or fewer.
- **Don't** copy a real phone's notch, a real app's icon or its brand colours.
- **Don't** fade the ticks; they pop by scale.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Rate split: everything runs at the root rate; nothing is held.
  - Nothing fades: a tick pops by scale; the headline slides.
  - Height is shadow: the phone has one flat soft shadow, nothing else casts one.
  - Boil: none.

## Originality guard

Design your own headline, habits, phone shape and palette. It must not copy a real device, app, brand or a published
mockup. A bright ground, a dark phone with a light list screen, a split headline and ticks that pop in order are the style.

## Proven on

A 7 s portrait clip (1080 by 1350, 24 fps): a four-line split headline, a phone with four rows,
four ticks and a progress bar; exported locally, not on the hosted renderer. The clip builds up and does not loop.

**Not proven:** the stage editor (not tried), the transitions (the phone sliding off up, a coral wipe), a floating or tilted phone with moving content, a screen that scrolls, a
second device, a landscape frame and a longer list than four rows.
