# Where the reel is going

Written 2026-10-02; lengths rechecked 2026-10-21 (Shorts and most Reels accounts take up to 3 min). The lengths come from the platforms' own notes, with YouTube's
longer Shorts added. The safe band is our working rule for a 1080×1920 frame, not a platform's published spec:
the platforms move their buttons, so when the user says text sits under one, believe them and move
it.

| Platform | Frame | Length to aim for | The hook |
|---|---|---|---|
| TikTok | 9:16, 1080×1920 | 15–60 s; 30 s unless asked | the first 2 s, or they swipe |
| Instagram Reels | 9:16, 1080×1920 | 15–60 s for reach, up to 90 s when it holds (it takes up to 3 min) | the first 2 s |
| YouTube Shorts | 9:16, 1080×1920 | under 60 s; it takes up to 3 min, but say so before going past 60 | the first 2 s |

With no platform named, cut a 9:16 reel of 30 s: it plays on all three. Never ask which. Another
shape only when the user names one:

| They say | Frame | Words keep out of |
|---|---|---|
| "post", "feed" | 4:5, 1080×1350 | `landscape`: 5 % from each edge |
| "square" | 1:1, 1080×1080 | `landscape` |
| "YouTube video", "horizontal" | 16:9, 1920×1080 | `landscape` |

The same cut and style laid out again for that frame: titles, cards and grids placed for it, each
clip reframed as the footage-reframing skill says. Never a crop of the 9:16.

## The safe band

The platform draws its own buttons over the reel: the caption and the account name across the
bottom, the like and share buttons down the right edge, the tabs across the top. Keep every word
inside the band the screen-recording-layouts skill's `scripts/safe_zone.py` checks for the platform. With none named,
check `["reels", "tiktok", "shorts"]` at once: in a 1080×1920 frame that is **y 250–1440, 65 px in from each side**,
clear of the button rail on the right from y 864 down. Key faces stay inside it too.

| Words | Where, in a 1080×1920 frame | As a caption style's `offset` |
|---|---|---|
| Captions | centred on y ≈ 1400 | `[0, 440]` |
| Highlights, alone | centred on y ≈ 1270, below the face of a centred speaker | `[0, 307]`, the spoken-captions skill's default |
| Highlights, with captions on | centred on y ≈ 330, above the head | `[0, -630]` |

A face the footage-reframing skill has framed sits near the middle of the frame, so check each highlight's
frame for the face before REVIEW, and move it to the other band when it covers the face.
