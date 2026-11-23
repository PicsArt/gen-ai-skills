# Spatial and action continuity for product Reels

Use for multi-shot scenes involving people, carried products or attached accessories. Camera variety must not silently rearrange the scene. Apply these checks to drafts too, not only HD finals.

## Plan the physical state before prompting

- Assign stable IDs to people, products and support surfaces. Distinguish CONSOLE_A from WINDOWSILL_B even if both sit beside the window. Describe one room coordinate system and a few fixed anchors, with a simple top-down diagram when useful. World-left/right is not screen-left/right.
- For each shot record: camera position and viewing direction; each person's start/end position, facing and occupied hands; each product's start/end support, orientation and carrier; the one action that changes that state. Include foliage shape, saucer, ribbon and attachment where relevant.
- A shot's opening inherits the previous shot's ending. Changing the angle changes projection, not world position. Write explicit world anchors in each shot instead of ambiguous phrases such as 'beside the window'.
- Every move requires a visible, motivated action or an explicitly planned, understandable time jump. Track pickup -> supported carry -> placement -> release. The carrier cannot hold two products while another hand magically places one. A product cannot appear on another surface merely because the next composition looks prettier.
- Establish any payoff object before revealing it, or show its arrival. Do not hide a second pot offscreen and rely on words alone to prevent duplication or spontaneous appearance.
- Keep the camera on a coherent side of the action axis; if crossing it, use a readable wider or continuous bridging shot. Use a wider shot to re-establish geography when necessary, not extra cuts to conceal unclear blocking.

## Compile and simplify

Write the room map, product IDs and immutable support rules once, then explicit state transitions into timecoded shots. Use approved location/character references when the production workflow requires them. Prompt text is not a replacement for missing reference views.

Limit simultaneous interactions. For a product transfer, let one person finish before another starts. If a short cut cannot show pickup and placement legibly, give the action another shot or simplify it; do not solve crowding with teleportation.

For stationary product stories, state the invariant: 'After placement, POT_A remains on CONSOLE_A until the end; WINDOWSILL_B is empty in every shot.' Prefer camera changes around a fixed arrangement over unnecessary relocation. For mobile products, record each actual change instead of an impossible global 'never moves' instruction.

For accessories, record connection topology: ribbon passes through HOLE_A at its actual location, with the same anchor after each cut. Show threading/contact clearly; never replace it with attachment to a solid edge or newly invented hole.

## Review the delivered sequence, not the intended script

Inspect the last usable frame before and first usable frame after EVERY cut, plus full playback of every pickup, carry, placement and attachment. Compare actual positions against the planned state table. Inspect room anchors, people, occupied hands, product identity, support surface, orientation, foliage and contact points. A close-up alone cannot prove where an object is; inspect adjoining wider frames.

Record pass/fail per transition with timestamps and evidence. If playback or frames are inaccessible, mark continuity unverified; do not claim a pass or promote to final/Ready to post. User approval is separate from this technical check.

An unexplained move, duplicate, plant swap or impossible attachment fails the take. Preserve it as needs-changes and repair only the necessary span while checking both joins; reshoot a coherent sequence when local repair would preserve incompatible geography. Do not spend on HD before the discontinuity is resolved. Retry within authorized scope, keep failed versions, and stop rather than running an unlimited render loop.

## Recorded failures — 25 October 2026

- 'That one's mine / now he wants one': owner reported people and pots changing places across camera cuts. The prompt specified room directions but lacked shot-by-shot ownership and support states; the ending also asked both people to transfer pots simultaneously. Repair with explicit sequential transfers and a fixed room map, not stronger adjectives about consistency.
- Corduroy corner: owner reported console -> windowsill -> console without a move. Repair by binding the single pot to the same named console after placement and explicitly leaving the separate windowsill empty.
- Name tags: visible pre-made hole but attachment elsewhere. Hole visibility is insufficient; verify the ribbon actually passes through it before and after the cut.

These are owner-reported defects, not an independent frame audit. The rules reduce risk and make rejection actionable; no prompt guarantees model compliance.
