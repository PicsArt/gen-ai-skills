---
name: picsart-presenter
description: Create a Picsart presenter clip from a supported avatar, portrait, script, or speech recording. Use for talking-head delivery.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, presenter, talking-head, avatar]
---

# Presenter

Produce a talking-head clip from an avatar with a script, or a portrait driven by recorded speech.

## When to Use

- The user wants a presenter or talking-head clip from an avatar, portrait, script, or speech recording.
- For still headshot images from a selfie, use [prosumer-headshot-studio](../prosumer-headshot-studio/SKILL.md).

## Prerequisites

- The `picsart` MCP server is connected.
- Read the [interface map](../picsart-workflows/references/interface-map.md). Set the script, presenter source, voice, and output format from the brief.

## How to Run

Use [asset reuse](../picsart-asset-reuse/SKILL.md) for an existing cast member and available voice references.

## Quick Reference

- Input routes (step 1): a stock avatar with text, or a portrait driven by recorded speech.

## Procedure

1. Choose the input route before choosing a model. Distinguish a stock avatar with text from a portrait driven by recorded speech.
2. Discover models with `picsart_model_catalog`. Read `picsart_model_params` for the chosen model. Check required visual, audio, voice, and avatar fields.
3. Select returned voice or avatar IDs. Do not invent IDs. For missing catalog options, use a verified interface that exposes them.
4. For a speech-driven route, require a schema that accepts an audio input and produces video. Generic image-to-video support does not establish speech synchronization.
5. Use the final approved recording for audio input. Use its actual duration. Do not replace recorded dialogue with a prompt paraphrase.
6. Preflight the complete request. Stop when a required input is unavailable or unknown pricing prevents compliance with a strict credit cap.
7. Generate the authorized take with `async: true`. Preserve the handle. Poll it after a timeout instead of submitting again.
8. Review the whole clip with sound. Check facial stability, speech timing, mouth motion, and the final frame. Request corrections within the authorized budget.

## Pitfalls

- Do not guarantee lip-sync from an audio-input field alone. Do not claim that identity references train a model.

## Verification

Use [captions](../picsart-captions/SKILL.md) and [delivery check](../picsart-delivery-check/SKILL.md) as the brief requires.
