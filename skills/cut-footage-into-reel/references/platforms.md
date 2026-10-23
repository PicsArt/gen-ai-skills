# Where the reel is going

Written 2026-10-02; lengths rechecked 2026-10-21 (Shorts and most Reels accounts take up to 3 min). The lengths come from the platform notes Short Reel Maker used, with YouTube's
longer Shorts added. The safe band is our working rule for a 1080×1920 frame, not a platform's published spec:
the platforms move their buttons, so when the user says text sits under one, believe them and move
it.

| Platform | Frame | Length to aim for | The hook |
|---|---|---|---|
| TikTok | 9:16, 1080×1920 | 15–60 s; 30 s unless asked | the first 2 s, or they swipe |
| Instagram Reels | 9:16, 1080×1920 | 15–60 s for reach, up to 90 s when it holds (it takes up to 3 min) | the first 2 s |
| YouTube Shorts | 9:16, 1080×1920 | under 60 s; it takes up to 3 min, but say so before going past 60 | the first 2 s |

With no platform named, cut a 9:16 reel of 30 s: it plays on all three.

## The safe band

The platform draws its own buttons over the reel: the caption and the account name across the
bottom, the like and share buttons down the right edge, the tabs across the top. Keep every word
inside the band the screen-recording-layouts skill's `scripts/safe_zone.py` checks for the platform; for `reels` in a
1080×1920 frame that is **y 250–1440, 65 px in from each side**, clear of the like rail on the right.

| Words | Where, in a 1080×1920 frame | As a caption style's `offset` |
|---|---|---|
| Captions | centred on y ≈ 1400 | `[0, 440]` |
| Highlights, alone | centred on y ≈ 1270, below the face of a centred speaker | `[0, 307]`, the spoken-captions skill's default |
| Highlights, with captions on | centred on y ≈ 330, above the head | `[0, -630]` |

A face the footage-reframing skill has framed sits near the middle of the frame, so check each highlight's
frame for the face before REVIEW, and move it to the other band when it covers the face.
