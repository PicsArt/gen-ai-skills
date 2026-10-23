---
name: screen-ui-redesign
description: Recreate the screens of a recording as designed motion UI - the app's own screens, layout, colours and words, redrawn larger and cleaner for 9:16 and built only from what the recording shows. Use when screen footage will not read at the destination, or when the UI is only the means and a designed version tells the step better.
user-invocable: false
---

# Designed UI

A screen recording cropped into a vertical frame is tiny and dense: viewers swipe at the cut to
it. The same moment, redrawn as a few large elements, reads at a glance. The redraw is a claim
about the product, so it is the app's own screen made larger, never a different one.

## What stays true

- **Redraw the real app, never invent one.** Keep its layout, the kinds of its components, its
  colours, its words and the user's own typed text. Make them larger, cleaner and fit for 9:16,
  then add motion. A light chat stays a light chat; a magenta button stays magenta.
  Never draw a different UI or a component the app does not have: dark cards labelled WIDE and
  MEDIUM, where the app shows a light shot-list board with "Shot size Medium" chips, is an
  invented UI.
- **You may crop and add the picture.** Show only the one component that matters, and add the
  shot's picture (a still) as a visual inside it.
- **Every element is something on a still.** Its words, values and states are copied from the
  still sheets, letter for letter: the same labels, the same numbers, the same order of states.
  Never add a state, an option or a result the recording does not show.
- **Fewer, not other.** Leave out what the step does not need (menus, settings rows, other
  cards). Never merge two states into one the app never showed.
- **Each state names its recording second** (`seen`). The script refuses a state without one.
  It covers the look as well as the words: every element maps to something that still shows.
- **Your own words go in labels, not in the UI**: a `tag` on a card ("kept wide") points at a
  fact the states show; a chip or a bubble holds only the app's own text.
- **A thumbnail is a still of the recording**, through the privacy pass like every still.
- Where honesty needs proof (a result the product made, a claim a viewer would doubt), one frame of
  the real recording goes beside the redraw: the hook or the payoff, held.

## Mapping the recording to elements

| On the still | Element | Fields |
|---|---|---|
| A card, a tile, a row with a picture | `card` | `title`, `chip` (its key value), `image` (a still, cropped to the picture), `tag` |
| A message typed into a chat or a search box | `bubble` | `text` |
| A setting, a badge, a value on its own | `chip` | `text` |
| A menu, a list of options | `list` | `items`, at most the ones the step uses |
| The button pressed | `button` | `label` |

The thing that changes is one element across states, never two: the card whose chip goes from
"Shot size Medium" to "Shot size Close-up" is the same card in both states, with `set` on the second.

## Building a beat

From this skill's folder, run `python3 scripts/ui_beat.py <file>`. Never place or keyframe the
elements yourself. Its docstring lists every field. In short:

- `box`, `start` and `duration`: where and when the beat plays, in frame px and scene seconds;
- `style` and `font`: the app's own colours, read from the stills (`canvas`, `surface`, `ink`,
  and its primary button's colour as `accent`), and the scene's font;
- `elements`: each element by name, with its first values;
- `states`: each screen in order, with `at` (its beat second), `seen`, `show` (top to bottom),
  `set` (what changes from here), `tap` (the element pressed to cause it) and `source` (the still
  of the `seen` second). States sit at least 1.5 s apart, so each is read before the next moves.

It prints `{layers, assets, duration, states, diagnostics}`. Add the layers to the scene and the
assets (each thumbnail is a nested scene) to its `assets`. No layer uses a mask. Act on each
`warning`: `typing_cut` (a bubble sent before its text has typed out: move that state later),
`long_text` (shorten to what the still shows first), `never_shown`, `no_source` (a state with no
still to compare: name the still). Input it cannot build exits 1 with the field to fix.

## How it moves

The script fixes the motion so every beat reads alike. The craft behind it is the motion-design-craft
skill's: matched-element smart-animate, entrances by role staggered by hierarchy, a press before
the state it causes.

- **Matched elements are carried.** A card in two states moves to its new place on the house
  curve, `cubic-bezier(0.65, 0, 0.2, 1)`, over 0.5 s, and is never cut or faded.
- **New elements enter after the moves start**, sliding up 60 px and fading in over 0.5 s on
  `cubic-bezier(0.16, 1, 0.3, 1)`, 0.1 s apart, in the order shown. Rows of a list stagger behind
  the first. An element a state drops leaves upward in 0.3 s.
- **A tap comes before the change**: the pressed element dips to 0.92 and back in the 0.35 s
  before its state; for a bubble, its send button.
- **The change pops**, 0.5 s into its state: the old pill fades, the new one scales 0.6, 1.1, 1
  in the accent. A thumbnail with a new `zoom` pushes in over 0.9 s.
- **A bubble types** once it has risen, at about 0.045 s a character.

## Compare it with the recording

Check the beat on a contact sheet at each state's `at` plus 1 s, as the quality-review skill says: every
word large, nothing overlapping, the changed value plain. Then put each state's `source` still
next to its designed frame and compare them: the same layout, component kinds, colours and words.
Fix any element with no match on the still, or one that looks like another app, and build the
beat again. Do this before the video is rendered for review or export, never after.
