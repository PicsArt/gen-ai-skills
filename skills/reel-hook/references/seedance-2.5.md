# Seedance 2.5 prompt writing

Source: [BytePlus Dreamina Seedance 2.5 prompt guide](https://docs.byteplus.com/en/docs/modelark/seedance-2-5-prompt-guide), read 26 October 2026 from the rendered page. This is model-specific guidance, not a guarantee of output fidelity or a substitute for the execution provider's schema.

## Source notes

- Structure prompts around asset roles, a story summary, shot/timeline detail, and persistent visual/audio requirements.
- Map numbered references to upload order and purpose. Separate identity, voice, action, camera, environment and style; specify partial reuse. Avoid redundant descriptions of accurate references.
- Use whole-second story timing with continuous coverage and realistic action density; timestamps are unsuitable for high-frequency movement counts.
- Prefer positive descriptions. Subtitle/audio exclusions are supported. Avoid dialogue repetition and subtitle-bearing references when subtitles are unwanted.
- Specify a transition's trigger and method. Describe key actions selectively; explain obscure camera terms visually.
- Distinguish semantic references from locked editing, extension and first/last-frame tasks. Native frame roles differ from approximate prompt-only frame references. Validate corresponding parameters.
- Simple storyboards guide narrative; separately ordered keyframes offer closer visual alignment. Multi-view subject images are supported.
- Scope edits with timestamps and before/after changes. Split unstable complex jobs into simpler passes. MOV can improve edit/extension continuity; inspect duration and audio afterward.
- Correct text images help lettering. Neutral expressions can reduce glowing-eye artifacts. Reorder references by subject appearance when identities are mismatched.

## Operational adaptations for our workflows

These are our implementation choices, informed by the guide and the hook experiments; they are not additional vendor claims.

### Compile the task before the prose

Record the intended operation: new generation, reference adaptation, bounded edit, extension, keyframes, or transition bridge. Keep model settings outside the prompt. Use the current provider's actual enum names, reference syntax, limits and asset slots; do not copy native BytePlus parameters into a Picsart wrapper without schema support. A prompt-only request ends at the prompt.

Prepare an asset map with actual supplied identifiers, upload order, role, and attributes to preserve or change. For example, Image 1 controls the adult performer's identity and wardrobe; Image 2 controls the bottle shape, cap, colors and front label. A motion clip controls choreography only, not its actor or product. Check the submitted attachment order against every reference token. Ask only for missing required assets or identity choices; reuse approved ones.

For image-to-video, focus on change over time, but still supply missing action, camera, audio, identity bindings and desired end state. Do not interpret “motion only” as prohibiting these decisions. Do not force an arbitrary 120-word ceiling or repeat global constraints in every shot of one request. Carry those constraints into each separately generated clip.

### Build an executable story

Use: asset bindings → one-sentence premise → persistent look/continuity/audio → ordered beats → end state. Allocate whole-second story beats that cover the requested runtime. Preserve critical user counts as goals without pretending subsecond timestamps guarantee them. For exact fast chops or rotations, consider a suitable motion reference or an editorial timing pass; verify the returned take.

For a join, specify the outgoing state, visible trigger, incoming state, matching direction/position, and what continues across the boundary. “Smooth transition” alone is insufficient. If the user requests only a join repair, keep the rest of the approved sequence out of the rewrite scope. A generative edit does not guarantee untouched pixels outside the requested interval; a deterministic splice may be needed to preserve approved footage.

Use concise, relevant exclusions when needed, particularly audio/subtitles. A mandatory generic anatomy ban is not a remedy for every failure. Check conflicting instructions, asset ambiguity, action density and model limitations first. Keep exact label artwork supplied and front-facing when required; inspect spelling in output, and use approved compositing if exact typography is essential.

### Original example: dam-to-glass bridge repair

Prompt example only; source video identifiers and edit-window timestamps must be bound to the actual selected take before execution:

```text
Edit only the approved transition window in Video 1. Keep the established
performer and drink identity from Images 1 and 2. Change the separate reservoir
impact and glass ripple into one continuous splash event.

At the performer's water entry, the reservoir spray rises. During that upward
motion, match the central water column's position, direction and shape into an
upward splash originating inside the cafe glass. Reveal the glass rim before
the splash reaches its apex. The same water column peaks above the rim and
falls back into that glass, leaving settling ripples. The visual joke is that
his jump caused the splash inside the glass. The person remains out of view
after the reservoir impact. Preserve the subsequent hand pickup and cafe sip.
Carry one continuous splash sound across the join, followed by cafe ambience.
```

### Review gate

Before handoff, verify task type, asset order, timeline coverage, achievable beat density, transition causality, identity and label constraints, and explicit audio intent. After an authorized render, inspect those properties in the actual output; record failures separately from prompt intentions. Compare frame count, total duration and audio seams after edits. Do not label any draft compliant from its prompt alone.
