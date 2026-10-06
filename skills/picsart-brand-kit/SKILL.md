---
name: picsart-brand-kit
description: Define or apply a visual brand kit for Picsart creative assets. Use for colors, type, logo use, and consistent layouts.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, brand-kit, design-system, layout]
---

# Brand kit

Build a compact brand specification and prove it on a representative application.

## When to Use

- The user needs a brand kit for colors, type, logo use, and consistent layouts.
- An existing brand must be applied to new Picsart creative assets.

## Prerequisites

- The `picsart` MCP server is connected.
- Read [the interface map](../picsart-workflows/references/interface-map.md) before tool use.

## How to Run

Start with the requested applications.
List the decisions each application needs.
For an existing brand, inspect its supplied guide and official assets.
Keep the exact logo, approved copy, colors, and type choices.
For a new brand, distinguish proposed design choices from supplied brand facts.

## Quick Reference

### Specification fields

Create a compact specification with these fields:

- Color values and their roles.
- Type choices for headings, body text, and small labels.
- Logo placement, clear space, and permitted backgrounds.
- Image treatment and layout spacing.
- Motion rules, when an application requires motion.

Mark each field as supplied, proposed, or unresolved.

## Procedure

### Build an application

Resolve contradictions that affect the requested output.
Build a representative application with [scene design](../picsart-scene-design/SKILL.md).
Use [generation](../picsart-generate/SKILL.md) only for required new imagery.
Keep exact logos and text as separate composition elements.
Check the application at its intended size.

### Revise

If a design choice changes, revise only the affected applications.

## Pitfalls

- Do not redesign an official logo unless requested.

## Verification

Inspect contrast, type hierarchy, logo legibility, and consistency with the specification.
Deliver the specification and requested assets.
State which choices remain proposed.
Use [delivery check](../picsart-delivery-check/SKILL.md) for rendered files.
