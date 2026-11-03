# Closed carousel: reusable media, shared motion

Use `scene://closed-media-carousel` for any number of media cards circulating on a
circle, ellipse or tilted ellipse. This independently authored adaptation draws on
Hyperframes carousel-circle 1–5, not their HTML, assets or exact AE timing. The
128-chord path approximates arc-length travel; shared speed pulses keep all cards
in phase. Depth is 2D scale, not a 3D camera or depth sorting. Open paths, spherical
orbits and text-circle transitions are different capabilities.

Describe the template before binding parameters. Reference is reusable; bootstrap
and inline produce editable copies. Each `cards` record requires `content`, `width`
and `height`. Supply complete layer content (image, video, color or composition); these
are not clip records. For a video URL specify `assetType:"video"` and sufficient
source duration/trim. The card box controls fitting; inspect the crop. Source media
plays from scene start independently of spatial phase and staggered opacity entry.
Clip-level audio, transforms and looks are not forwarded. Wrap looked content in a
composition or edit the expanded surface. Empty produces only the background;
one card still travels. The count is not fixed to the source's twelve cards.

All cards use the same phase owner; depth scale and optional heading derive from
actual position. Preserve that ownership when editing. Do not duplicate position,
scale and heading tracks independently. `rotationFollow:0` avoids tangent queries;
`1` follows travel. `period` controls mean travel, `pulsePeriod`/`pulseStrength`
control speed variation, and `phase`/`spacing` control initial slots. Center/radii
do not auto-fit a new canvas. Entry completes at the larger of `duration*entryFraction`
and `1/(120*(1-staggerShare))` seconds, retaining at least one 1/120-second keyframe tick
per fade. Very short entries may occupy only a few output frames. Motion
continues until the hard cut. Changing period alone does not change media speed.

Later cards paint over earlier cards throughout the loop, even when visually
smaller. This differs from the source's first-card-on-top ordering; neither sorts
by depth. Change list order deliberately and inspect overlaps. Use another design
if the brief requires physically correct occlusion.

Apply this controlled request with `picsart_scene_apply_template`. Its colors make the
checks reproducible without external media:

```json
{"uri":"scene://closed-media-carousel","mode":"bootstrap","parameters":{"width":800,"height":600,"duration":6,"centerX":400,"centerY":300,"radiusX":200,"radiusY":200,"tiltDeg":0,"period":4,"pulseStrength":0,"nearScale":1,"farScale":1,"entryFraction":0.01,"staggerShare":0,"cards":[{"width":100,"height":60,"content":{"kind":"color","color":"#ee6644ff"}},{"width":100,"height":60,"content":{"kind":"color","color":"#4488eeff"}}]}}
```

Retain the returned scene. Run strict `picsart_scene_validate`, then `picsart_scene_query_layout`
at 0, 0.06, 1, 2 and 4 seconds. The carriers are `card_0`/`card_1`; entry opacity is
on their children `card_0__surface_0`/`card_1__surface_0`, not the carrier itself.
After nesting/inline edits get actual IDs and root-time windows from queries.
Inline insertion and detaching retain an editable composition when expressions
depend on `ctx`: this preserves sibling lookups and the shared clock. Do not
flatten that scope or rename its children without repairing their relationships.

At one second the first card should reach the rightmost point. The following contract records that independent expectation. Run it with `picsart_scene_check_contracts` and record the actual verdict:

```json
{"version":1,"timeSpace":"root","contracts":[{"id":"rightmost-arrival","window":{"start":1,"end":1.001,"step":0.01},"assert":{"kind":"motion_range","target":{"id":"card_0"},"channel":"centerX","min":599.9,"max":600.1}}]}
```

This motion record specifies direction in a short window, not the whole orbit; run it with `picsart_scene_check_motion`. For a continuity claim, check X/Y positions and rates across every output frame of the full revolution and seam, splitting windows over 1000 frames with the overlap the tool requires. Derive limits from radii, period and pulse; never widen them to hide a discontinuity. Report the windows checked, not continuous-time or pixel proof.

```json
{"version":1,"timeSpace":"root","fps":30,"window":{"start":1.1,"end":1.4},"checks":[{"id":"travels-left","kind":"velocity_range","target":{"id":"card_0"},"channel":"centerX","min":-200,"max":-40}]}
```

This illustrative pixel record expects red paint at one second, with background margins around the complete card. Pixel records have no automated checker; inspect a full-resolution frame and retain numerical thresholds as unverified. Unknown colors or clipped measurement boundaries must not be assumed to pass.

```json
{"version":1,"times":[1],"checks":[{"id":"right-card-red","kind":"ink_presence","region":[540,260,120,80],"foreground":[238,102,68],"background":[237,237,239],"colorTolerance":16,"minPixels":5800,"maxFillFraction":0.7}]}
```

Prove the checks catch mistakes: shift `centerX` by 40 (geometry must fail), set
`reverse:true` (direction must fail), then change the first card to the background
color `#ededef` (missing red ink must fail). Restore the original and rerun unchanged assertions. For paint order,
set `spacing:0`: the last blue card should cover red. This overlap is intentional,
not a blanket exemption for other lint findings.

Rebase IDs, times, bounds, regions and colors after customization. Use
`picsart_scene_lint_layout` across entry, orbit extremes and seams; evaluate off-canvas reports
against the requested framing. Render those times with `picsart_scene_contact_sheet` with explicit `times` and `resolution` equal to the composition dimensions, inspect
continuous video for pulses/entry, and test changed counts and a delayed/scaled host.
For video, compare frames at the same spatial phase on later cycles to ensure footage
continues instead of restarting. Report what was actually checked and leave unsupported
occlusion, audio, source exhaustion or unsampled behavior explicitly unverified.
