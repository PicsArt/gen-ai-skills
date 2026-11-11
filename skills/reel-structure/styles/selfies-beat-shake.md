### Selfie beat shake

| Field | Value |
|---|---|
| Group | Transitions and speed |
| Looks like | full-screen selfies that jolt with a quick blurred shake on the beat, flipping between two poses, with one calm slow push in the middle |
| Vibe | selfie dump, aesthetic, beat shake, flirty, pose flip, blur hits |
| Fit | slots 3–12; mixed; solo; everyday, any; aesthetic, playful, stylish, moody |
| Music | sultry, bouncy pop-dance with a chanted vocal hook and off-beat stabs, 98 BPM (beat 0.612 s; every bar line and hit is rounded to the nearest 30 fps frame from the start) |
| Skin | only the bed mood; no title, colours or text on screen, the selfies alone |
| Preview | none yet |
| Proven | yes: agent build 2026-11-08, user-approved |
| Seams | `transition:zoom_through(duration=0.2)` on every seam, centred on the bar line (0.1 s before to 0.1 s after), plus `effect:gaussian_blur(blur=32→0)` on the incoming photo over its first 0.1 s, ease-out |
| Motion | every photo full-frame (cover-fit 1080x1920, centred) at base scale 1.08 so a shake never shows an edge. Bar lines (frame-rounded 98 BPM bars): 0.000, 2.433, 4.900, 7.333, 9.800, 12.233, 14.700, 17.133, 19.600 s. Hits are the bar's 2nd to 6th eighth notes, frame-rounded from the start: bar 1 at 0.600, 0.933, 1.233, 1.533, 1.833; bar 2 at 3.067, 3.367, 3.667, 3.967, 4.300; bar 3 at 5.500, 5.800, 6.133, 6.433, 6.733; bar 4 at 7.967, 8.267, 8.567, 8.867, 9.200; bar 5 at 10.400, 10.700, 11.033, 11.333, 11.633; bar 6 at 12.867, 13.167, 13.467, 13.767, 14.067; bar 7 at 15.300, 15.600, 15.933, 16.233, 16.533; bar 8 at 17.767, 18.067, 18.367, 18.667, 18.967. The last bar adds one more hit on its 1st eighth note (bar 2: 2.767, bar 3: 5.200, bar 4: 7.667, bar 5: 10.100, bar 6: 12.567, bar 7: 15.000, bar 8: 17.433). One hit starting at h, on every photo layer of that bar: scale 1.08 → 1.20 at h+0.067 (ease-out) → 1.08 at h+0.167 (ease-in-out); position x 0 → +48 px at h+0.067 (ease-out) → −24 px at h+0.100 (linear) → 0 at h+0.167 (ease-out), the sign flipping on every next hit (+48, −48, +48 ...); `effect:gaussian_blur(blur=0→28→0)` with 28 at h+0.067 (ease-out) and 0 at h+0.167 (ease-in). Pair bars: photo A is shown first and sits below; photo B sits on top with the same hit keys. B's opacity is a hold (step) key: 0 at the bar start, then 1, 0, 1, 0, 1 at the peaks (h+0.067) of the bar's five eighth-note hits 2 to 6. The bar reads A, B, A, B, A, B and ends on B. The extra first hit of a last bar shakes without a flip. Calm bar: scale 1.08 → 1.14 from bar line to bar line, linear, centred, no blur, no shake |
| Text | none: no words on screen in any frame |
| Look | none (each selfie keeps its own colour) |
| Template | none |
| Ending | the final hit ends 0.167 s after it starts; the selfie then holds sharp and still to the last bar line (the length from the count table) and the reel stops on it with the bed's last hit, no fade, no end card |
| Skills | motion-design-craft, scene-building-basics, resting-frame-rules |

- ID: selfies-beat-shake
- Format: selfie dump in one-bar slots, blurred shake hits on the off-beats, two poses flipping inside a bar
- Length: from the count table (one bar per slot group), 4.900 s at the minimum and 19.600 s at the maximum
- Cut rate: ~24 cuts/min (a new bar every 2.433–2.467 s), plus about 2 hits a second inside the hit bars
- Caption style: none, no words on screen
- Bed: sultry bouncy pop-dance with a chanted hook, 98 BPM
- Layout: single
- Source: our style library

**Choosing the photos.** Leave out any photo whose mood contradicts the style rather than using it. The style is flirty and confident, so a crying, sad or eyes-down close-up is dropped. The count below is the number of photos left after that.

**Bars from the count.** Fill bars in this cycle, then start it again:
1. pair-with-hits (2 photos);
2. single-calm (1);
3. pair-with-hits (2);
4. single-with-hits (1).

If only one photo is left for a pair bar, that bar becomes single-with-hits. The last bar always has hits: a single-calm last bar gets the hits instead. No photo is used in two bars. The only return is A coming back inside its own pair flip.

| Photos | Bars | Length |
|---|---|---|
| 3 (minimum) | pair, single-with-hits | 4.900 s |
| 4 | pair, calm, single-with-hits | 7.333 s |
| 5 | pair, calm, pair | 7.333 s |
| 6 | pair, calm, pair, single-with-hits | 9.800 s |
| 12 (maximum) | the cycle twice | 19.600 s |

Below 3 photos, pick another style. A clip in a slot plays its first 2.433 s, muted, with the same hit keys.

**Which photo is A and which is B.** Each pair holds two selfies with the same outfit or setting, so the flip reads as one moment. When no two left share an outfit or setting, pair the two closest in light (both night, or both day).
- A, shown first, is the calmer, more neutral pose.
- B is the livelier pose: a laugh, a bigger gesture or a closer framing. The bar lands on B.
- The calmest remaining photo takes the calm bar. The boldest shot ends the reel.

The beat table below is the 5-photo build (pair, calm, pair); other counts follow the table above with the same keys.

| Time (s) | Beat | What happens (picture) | Voice | On screen | Shot | Move | Caption | Sound |
|---|---|---|---|---|---|---|---|---|
| 0.000–2.433 | Hook | selfie A still and sharp for 0.600 s, then 5 blurred shake hits on the off-beats (0.600, 0.933, 1.233, 1.533, 1.833), flipping to selfie B and back at each hit, ending on B | — | — | pair 1, A then B | scale punch 1.08 → 1.20 → 1.08, x jolt ±48 px, blur 0 → 28 → 0 per hit | — | bed starts on the downbeat, chanted hook |
| 2.433–4.900 | Breath | zoom-through whip into the calm selfie, which sits sharp under a slow push | — | — | calm photo | scale 1.08 → 1.14, linear | — | bed |
| 4.900–7.333 | Finale | zoom-through whip into pair 2's A; 6 blurred shake hits (5.200 without a flip, then 5.500, 5.800, 6.133, 6.433, 6.733 flipping A and B), ending on B, then a sharp still hold from 6.900 s to the end | — | — | pair 2, A then B | same hit keys as the Hook | — | bed, stops on the last bar line at 7.333 s |
