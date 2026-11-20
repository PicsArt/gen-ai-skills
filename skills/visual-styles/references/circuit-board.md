# Circuit board

A chip on a printed board: copper traces draw outward from the chip to pads, pulses of light run along the traces
at steady speed, pads light up as they are reached and the chip's core glows brighter with each pulse.

## Palette

Board green `#0b3d2e`, deeper `#082a20`, copper trace `#c98a3b`, pad `#e0b060`, chip body `#1b1f24`, chip pins
`#9aa4ad`. **The hero colour is the pulse mint `#9dffcf`, reserved for the travelling light and the lit pads.**

## The medium

- **Traces** are polylines with 45- and 90-degree corners only, 6 px copper strokes with round joins and a 1 px
  darker edge line.
- **Pads** are small rings with a hole; **vias** are tiny dots where traces change layer.
- **The chip** is a rounded dark square with pins along its sides and a small notch at one corner; its core is a
  square with a gradient fill.
- A faint **silkscreen** of labels and outlines in pale green at 25 % opacity.

## Motion habits

- **Draw the traces** outward with `trim` end 0 to 1 over 1.2 s, nearest first, 0.1 s apart.
- **Pulses:** a short bright segment (a mint stroke with `trim` start and end keyed together) travels each trace at
  one speed (320 px/s); the time on a trace is its length over speed. Loop with `ctx:loopOut("cycle")` at
  the whole-board period.
- **Pads light** with a mint fill that fades over 0.5 s after the pulse arrives.
- **Core glow:** a `glow` on the chip core whose intensity keys up as each pulse leaves.
- Cued layers use `timeMode: "layer"`.

## Type

A few tiny labels in the mono face on the silkscreen; no headline.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Traces use only 45- and 90-degree angles.
2. Every pulse travels at the same speed.
3. A pad lights when, and only when, a pulse arrives.
4. Mint appears only on pulses and lit pads.
5. Traces never cross without a via.

## Build with the tools

Compute trace lengths and pulse timings in a script from the polylines; one layer per trace and per pulse; the
pad fill keyed from the arrival times. Verify timing on a contact sheet.

## Do / don't

- **Do** keep trace widths the same.
- **Don't** render a real chip's markings or a real board's layout.

## Originality guard

Design your own chip and routing. It must not copy a real processor's package art or logo, or a famous board's
layout. The copper traces, travelling light and glowing core are generic conventions.

## Proven on

The chip-circuit film (traces drawing out from a chip, pulses running at steady speed, pads lighting as reached,
a glowing core).
