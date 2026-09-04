# Platform layout

Every feed platform draws its own interface over your video. The file you generate looks fine; the app then puts a caption over the bottom third and a column of buttons down the right side, and whatever you put there is gone. You cannot see this in the render, which is why it has to be decided before the shot rather than after.

**Ask which platform this is for.** It changes the framing, and it is one question.

## The safe area, if you only remember one thing

Recommended universal safe area on a 1080x1920 frame: top 288px (15%), bottom 672px (35%), left 120px (11.1%), right 300px (27.8%). That leaves a usable rectangle of 660 x 960px at x 120-780, y 288-1248 - 61.1% of the width and 50.0% of the height.

In prompt terms: keep the subject and anything that has to be read inside the middle of the frame, well clear of the bottom third and the right quarter. Compose as though the lower and right edges are going to be covered, because they are.

## Per platform

Margins on a 1080x1920 frame. Anything important must sit inside them.

| platform | top | bottom | left | right | usable width |
|---|---|---|---|---|---|
| TikTok feed (In-Feed / For You) | 240 | 660 | 120 | 300 | 660px |
| Instagram Reels | 269 | 672 | 65 | 65 | 950px |
| YouTube Shorts | 288 | 672 | 48 | 192 | 840px |
| Instagram Stories | 269 | 672 | 65 | 65 | 950px |
| Facebook Reels | 269 | 672 | 65 | 65 | 950px |
| Facebook Stories | 250 | 340 | not established | not established | 1080px |
| Snapchat (Spotlight, Stories, Commercials - one shared spec) | 192 | 672 | 65 | 162 | 853px |
| LinkedIn vertical video | not established | | | | |
| X (Twitter) vertical video | not established | | | | |

Two platforms have no published figures, and estimating them would be worse than saying so: use the universal safe area above for those.

## What occupies each edge

**TikTok feed (In-Feed / For You).**
- top: Status bar (clock, battery, signal), the Following / For You tab switcher, and the search icon. Measured unsafe band 160px on TikTok's 720x1280 template = 240px at 1080x1920
- bottom: Account handle, ad caption (white text, uniform font, max 4 lines, per TikTok's own spec), 'Sponsored' label on ads, the music/sound attribution ticker, the CTA or anchor button, and TikTok's own bottom app nav bar (Home / Discover / + / Inbox / Me)
- right: The vertical action rail: profile avatar with follow '+', like, comment, share, and the spinning sound disc
- left: No UI element. TikTok's template still marks an 80px (of 720) blue edge band on BOTH sides, i.e.
- always there: Top status bar and tab switcher, Right-hand action rail (profile, like, comment, share, sound disc), Account handle and sound attribution strip at the bottom, Bottom app navigation bar, The 11.11% left and right edge margins marked on TikTok's own template
- only sometimes: Caption length: TikTok states in writing that 'the safe zone size is determined by the dimension (vertical, horizontal, or square), ad caption length, and any additional formats used'. Measured from TikTok's four official with-anchor templates, the bottom unsafe band grows with caption lines: 1 line 42.4% (814px), 2 lines 45.9% (881px), 3 lines 49.5% (950px), 4 lines 52.9% (1016px) of a 1920px frame, Anchor / CTA button (ads only): present in the with-anchor templates and absent from the standard one. This is the single biggest swing on TikTok, 'Sponsored' label: ads only, Comment overlays and the tap-to-pause progress bar appear on interaction and are not in any published template

**Instagram Reels.**
- top: Status bar, the 'Reels' title and camera icon. Meta names 'devices with taller screens' as a reason for the top reserve, so part of this band is device-variance rather than a fixed overlay
- bottom: Profile handle and follow button, caption, audio attribution strip, and the call-to-action button on ads. Meta's wording names 'the profile icon or call-to-action'
- right: The vertical action rail: like, comment, share, save, more, and the rotating audio thumbnail. NOTE: Meta's single 6% side figure does NOT carve out the action rail, which visibly occupies far more than 6%.
- left: No UI element; 6% is an edge/device-variance margin
- always there: Top status bar, Right-hand action rail, Profile handle, caption and audio attribution at the bottom, 6% side edge margins
- only sometimes: Call-to-action button and 'Sponsored' label: ads only. Meta's 35% bottom figure already assumes a CTA, so organic Reels have headroom Meta does not quantify, Caption length: a long caption pushes the text block higher. Meta publishes no per-caption-line numbers, unlike TikTok., Comment sheet and share sheet appear on interaction and are not covered by any published number

**YouTube Shorts.**
- top: Status bar, YouTube Shorts header and search icon. 288px is the largest top reserve of any platform here
- bottom: Channel name and avatar, video title/description, the 'Sponsored' or ad label, the audio attribution strip, and the CTA overlay card. Google states the mobile CTA overlay card shows a headline (40 characters) and description (90 characters)
- right: The action rail: like, dislike, comment, share, remix and the audio thumbnail. Google explicitly names 'Like, dislike, comment, and share buttons appear alongside the ad'.
- left: Only 48px (4.44%), an edge margin. Google reserves almost nothing on the left
- always there: Top status bar and Shorts header, Right-hand action rail (like, dislike, comment, share), Channel name, title and audio attribution at the bottom, 48px left edge margin
- only sometimes: CTA overlay card on ads: Google states it appears at 3 seconds for Performance Max, App and Demand Gen campaigns, and at 10 seconds for Video View and Video Reach campaigns. So on YouTube the bottom-most overlay is time-gated, not present from frame one - a genuinely different risk profile from TikTok, Description truncation: Google notes descriptions are 'limited to 90 characters' with truncation beyond 1-2 lines 'depending on device', so the bottom block's height is device-dependent, Player compression on interaction: Google states that when a user interacts with the app, 'the video player can compress up to a 1:1 aspect ratio. This will crop the displayed video at the bottom and top.' This is a conditional crop, not an overlay, and it is the harshest conditional risk on YouTube

**Instagram Stories.**
- top: Story progress bar segments, profile avatar and handle, timestamp, and the close/more controls. Stories is the one surface where the top band contains a genuinely variable element
- bottom: Reply/message field, the swipe-up or CTA button on ads, 'Sponsored' label, and share/send controls
- right: More menu and the send/share controls. Stories has no full-height action rail, which is why its right side is genuinely less contested than Reels or TikTok - but Meta publishes the same 6% for both, so the distinction is not reflected in the spec
- left: No UI element; 6% edge margin
- always there: Progress bar, avatar, handle and timestamp at the top, Reply field and send controls at the bottom, 6% side edge margins
- only sometimes: Progress bar segmentation: the bar splits into one segment per story in the sequence, so its visual density - though not its height - varies with how many stories the account has posted. The height itself is inside the 14% either way, CTA / swipe-up and 'Sponsored' label: ads only, Stickers, polls, questions, link stickers and music stickers placed by the poster occupy arbitrary positions and are not covered by any published number, Tap-to-advance zones cover the left and right thirds of the screen; they are invisible but mean interactive elements should not be composed at the edges

**Facebook Reels.**
- top: Status bar, Reels header, and back/search controls
- bottom: Page name and follow button, caption, audio attribution, CTA button on ads, and Facebook's bottom app navigation
- right: Action rail: like, comment, share, more, audio thumbnail. As with Instagram Reels, Meta's 6% does not model the rail
- left: No UI element; 6% edge margin
- always there: Top status bar and Reels header, Right-hand action rail, Page name, caption and audio attribution at the bottom, 6% side edge margins
- only sometimes: CTA button and 'Sponsored' label: ads only, The separate 'Ads on Facebook Reels' overlay format (1:1, 1440x1440) can be placed over an organic reel by an advertiser, adding an overlay the reel's own creator cannot predict or design around. This is a conditional overlay unique to Facebook, Caption length effect: not established

**Facebook Stories.**
- top: Progress bar, profile avatar and Page name, timestamp, close control
- bottom: Call-to-action button, 'Sponsored' label, and reply/share controls. Meta's wording names only 'UI elements such as the call-to-action'
- always there: Progress bar, avatar, Page name and timestamp at the top, Bottom reply/share controls
- only sometimes: Call-to-action button and 'Sponsored' label: ads only, Progress bar segmentation varies with the number of stories in the sequence, Poster-placed stickers and links: arbitrary position, not covered by any published number

**Snapchat (Spotlight, Stories, Commercials - one shared spec).**
- top: Snap's article names 'brand name, headline, call-to-action pill, or progress bar' as the overlay set; in the diagram the top band holds the avatar, the For You / Following tab switcher, and add-friend and add-story icons. 10% is the shallowest top reserve of any platform in this file
- bottom: Brand name, headline, the 'Ad' label, collection-ad product tiles where present, the CTA pill, and Snapchat's own bottom app navigation bar
- right: Action rail: profile with follow '+', heart, share arrow, and the more menu. Reserved 15% across the band it occupies
- left: No UI element; 6% edge margin
- always there: Top bar with avatar and tab switcher, Right-hand action rail across its band, Brand name, headline and 'Ad' label at the bottom, Bottom app navigation bar, 6% side edge margins, Progress bar (named by Snap as a standing overlay element)
- only sometimes: Dynamic CTA: Snap states that 'For eligible Snap Ads, CTA format and placement may also be dynamically selected' and that 'Dynamic CTA variants themselves do not appear in Ads Preview'. This is the most explicit admission of an unpredictable overlay from any platform in this set - Snap is telling you the CTA can move and that you cannot preview where, The 45% versus 35% bottom bracket: the diagram carries both without saying which format each governs. Snap's prose says only that 'each format has defined top, bottom, and side buffers'., Collection-ad product tiles occupy the lower band and are format-conditional

## It will be cropped more than once

The same clip appears at different shapes in different places in the same app, so a composition that only works at 9:16 gets cut.

- **TikTok feed (In-Feed / For You)**: Organic TikTok is composed and consumed at 9:16 full-bleed; there is no second aspect ratio in the feed itself
- **TikTok feed (In-Feed / For You)**: Profile grid and search-result thumbnail crop: not established. TikTok publishes no numeric spec for the video cover crop.
- **TikTok feed (In-Feed / For You)**: Non-vertical uploads: TikTok accepts 1:1 and 16:9, but its own templates show the usable box shrinking hard - the 1:1 template measures top 21.9% / bottom 42.4-52.9% / left 9.3% / right 22.4%, and the 16:9 template top 34.2% / bottom 42.4-52.9% / left 10.4% / right 22.1%, both as a share of the 9:16 screen. Shooting anything but 9:16 for TikTok costs roughly half the frame
- **Instagram Reels**: Reel cover in the profile grid: Instagram's own help center recommends a cover of 420 x 654 px, which is 1:1.55 - i.e. NOT 9:16 (1:1.78) and not 1:1.
- **Instagram Reels**: Instagram profile grid tile ratio: Instagram moved off 1:1 square tiles in early 2025 to a taller tile. Whether the tile is 3:4 or 4:5 is DISPUTED among secondary sources and no official Instagram statement was retrieved.
- **Instagram Reels**: Home feed crop of a Reel to 4:5: commonly asserted by blogs, but Meta's own ads guide for the Instagram Feed video placement specifies 9:16 at 1080x1920 with 1% tolerance, which contradicts a hard 4:5 feed crop for video. Not established.
- **YouTube Shorts**: Google states that when the viewer interacts with the app the player 'can compress up to a 1:1 aspect ratio', cropping the displayed video at top and bottom. A 9:16 frame squeezed to 1:1 loses 43.75% of its height, centred - so the subject must also survive a centred 1:1 crop
- **YouTube Shorts**: Google also documents the initial-impression crop: a portion of a 9:16 vertical video is cropped for the initial ad impression, with fullscreen showing the full frame. The exact crop fraction is not stated numerically.
- **YouTube Shorts**: Horizontal or square uploads to Shorts are not cropped but padded - Google says horizontal assets 'serve with blurred top and bottoms'
- **Instagram Stories**: Stories are full-bleed 9:16 with no second crop in the Stories player itself
- **Instagram Stories**: Stories saved to Highlights get a cover crop; its ratio is not established
- **Instagram Stories**: Stories are ephemeral and do not enter the profile grid, so unlike Reels there is no grid-crop constraint
- **Facebook Reels**: Facebook Reels crop in the main Facebook feed versus the Reels tab: not established. No official Meta statement was retrieved
- **Facebook Reels**: Reel cover crop on a Facebook Page: not established
- **Facebook Stories**: Full-bleed 9:16 in the Stories player. No second crop established
- **Snapchat (Spotlight, Stories, Commercials - one shared spec)**: Spotlight and Stories play full-bleed 9:16; no second crop is documented
- **Snapchat (Spotlight, Stories, Commercials - one shared spec)**: Spotlight cover or thumbnail crop: not established
- **Snapchat (Spotlight, Stories, Commercials - one shared spec)**: A recommendation circulating in secondary sources to keep all branded elements 'in the central 50% of the vertical frame' for Spotlight specifically is not in Snap's documentation and is recorded here only as an unverified blog claim
- **LinkedIn vertical video**: not established
- **X (Twitter) vertical video**: not established

## Composition and pacing

**TikTok feed (In-Feed / For You).**
- TikTok's caption is rendered in white with a fixed, non-customisable font (official). A creative with a white or transparent lower third will make the handle, caption and music ticker illegible - keep tonal contrast in the bottom third
- The safe box is offset left, not centred: on a 1080x1920 frame the usable rectangle is x 120-780, whose centre is x=450, i.e. 90px (8.3% of width) left of frame centre.
- Because the bottom unsafe band can reach 52.9%, treat TikTok as an upper-half-of-frame medium: hero subject and any burned-in text belong between 15% and 47% of frame height
- TikTok's own reservation spec recommends 9-15 seconds for TopView ('Video Duration: 5-60s, recommend 9-15s'), which is the only duration recommendation TikTok states numerically. Source: (no date visible)
- In-Feed auction ads have no duration restriction and accept up to 10 minutes, so the 9-15s figure is a creative recommendation and not a limit

**Instagram Reels.**
- Meta's own guidance is that the value is in the safe zone plus audio plus verticality together: the ads guide notes 'Reels ads with key messages in the safe zone, quality audio and vertical video see better results'
- Meta marks captions and sound as 'optional, but strongly recommended' on the Reels placement - a stronger wording than the plain 'recommended' it uses on Instagram Feed. Burn in or enable captions
- Because the grid and cover crops are all narrower than 9:16, keep the subject horizontally centred on Instagram even though TikTok and YouTube both push you left. Instagram is the platform that argues for centring
- Meta's placement spec allows 0s to 15 minutes, so it imposes no pacing. Meta publishes no numeric hook-timing figure on the placement page
- No official Meta 'first N seconds' statistic was verified. Not established

**YouTube Shorts.**
- Google's stated intent for the safe zone is specifically 'logo, product, supers' - brand and text furniture - rather than the whole subject. Their wording tolerates a subject bleeding into the reserve as long as the message does not
- The 48px-left / 192px-right asymmetry means YouTube wants the subject offset LEFT. The safe box centre is x=468 on a 1080 frame, 72px left of true centre
- The 288px top reserve is the deepest of any platform - do not put text in the top 15% for Shorts
- Official: 'For action-oriented ads, use 10-30 second vertical videos' (Google Ads Help 16041697)
- Official: videos can be up to 3 minutes but 'only the first 60 seconds will play on the Shorts feed', and Google recommends under 60 seconds 'to align with viewer behavior'

**Instagram Stories.**
- Stories is the one surface in this set where the top band is the more dangerous one relative to the others' bottoms, because the progress bar plus handle plus timestamp all stack there and the viewer's eye starts there
- Because the tap-to-advance zones are the left and right thirds, anything that looks tappable should sit in the central third
- Meta's captions/sound wording on the Stories placement is the softer 'optional, but recommended', not the 'strongly recommended' used on Reels
- Meta imposes 1 second to 60 minutes and states no pacing recommendation on the placement page. Not established from official sources

**Facebook Reels.**
- Meta's own performance claim, quoted in its guide, is that 'Reels ads with key messages in the safe zone, quality audio and vertical video see better results'
- A separately reported Meta figure that 9:16 Reels ads with audio and key elements in the safe zone saw '34.5% lower cost per result than image ads on Reels' circulates widely; it was not verified on a Meta-owned page and is recorded here as unverified
- Not established from official sources

**Facebook Stories.**
- Meta's phrasing here reserves the bands against 'text and logos' specifically, not against the subject - a narrower ask than the Reels wording, which also names 'other key creative elements'
- Meta caps Facebook Stories video at 3 minutes, shorter than the 15-minute Reels and 60-minute Instagram Stories allowances, but states no pacing recommendation. Not established

**Snapchat (Spotlight, Stories, Commercials - one shared spec).**
- Snap's guidance is unusually explicit about type: 'Use modern, legible fonts in large enough sizes and with strong color contrast.'
- Snap tells you to place legal text 'well above the bottom buffer' rather than at its edge - i.e. treat the bottom reserve as soft-edged, not a hard line to butt up against
- Because the Dynamic CTA can be repositioned by Snap and does not appear in Ads Preview, Snapchat is the surface where you should over-reserve rather than compose to the published minimum
- Official and unusually aggressive: for Single Image or Video ads, 'if you're using a video, we recommend keeping it at 3-5 seconds' (length limit 3-180s)
- Official: for Sponsored Snaps, 'We recommend keeping < 10 seconds' (180s max)

**LinkedIn vertical video.**
- not established
- not established

**X (Twitter) vertical video.**
- not established
- not established

## What holds across all of them

- Reserve about a third of the bottom of the frame, on every platform. Three of the four platforms with published specs independently converge on exactly 35% (Meta across three placements, Google at 672/1920, Snapchat's diagram) and TikTok's standard template lands at 34.4%.
- Reserve the right side much more heavily than the left. Every platform that models its action rail is strongly asymmetric: TikTok 11% left against 22-28% right, YouTube 4.4% left against 17.8% right, Snapchat 6% left against 15% right.
- Sound is assumed ON, and captions are still mandatory. Google states sound 'has been shown to increase conversions by over 20%' on Shorts; Meta marks sound 'strongly recommended' on Reels; Snap expects audio on video ads; TikTok rejects ads with missing or muffled audio.
- Native-looking beats polished, per the platforms themselves rather than per marketing blogs. Google's official Shorts guidance is to 'Make your ads feel organic and social-first.
- Do not set up a premise. Google's official Shorts guidance: 'there's no need to set up a premise or establish a storyline with lots of extra context.' Snap's official recommendation for a single image or video ad is 3-5 seconds, and TikTok's for TopView is 9-15 seconds.
- Text must survive a white-on-white collision. TikTok states its captions and music attribution render 'in white with a uniform font that can't be customized', so a bright lower third makes platform-drawn text illegible over your footage.
- Compose for more than one crop. Instagram re-crops a Reel to a 1:1.55 cover and a taller-than-square grid tile; Google states the YouTube player 'can compress up to a 1:1 aspect ratio' on interaction, cropping top and bottom.
- Treat conditional overlays as hard constraints when they are unpredictable. Snap explicitly says Dynamic CTA placement 'may also be dynamically selected' and that those variants 'do not appear in Ads Preview'.

## Where the platforms contradict themselves

Worth knowing before you defend a number to a client. These are the platforms' own published figures disagreeing, not uncertainty on our side.

- Meta contradicts itself on the bottom band: 35% on Instagram Reels, Instagram Stories and Facebook Reels versus 20% (340 pixels) on Facebook Stories, all in the same ads guide. Compose to 35%
- Meta's percentage and pixel figures do not reconcile on Facebook Stories: '14% (250 pixels)' and '20% (340 pixels)' imply a reference frame of about 1786px tall, not 1920 or 2560. The percentages are the safer reading
- TikTok contradicts itself on the right margin across two template generations: 27.78% total in the standard 720x1280 template versus 22.22% in the with-anchor 540x960 template
- TikTok's bottom band ranges from 34.4% (standard, no anchor) to 52.9% (anchor plus four caption lines) - an 18.5-point spread within TikTok's own official templates, driven by caption length and the CTA button
- Snapchat's own diagram prints both 35% and 45% bottom brackets without saying which format governs which
- Snapchat official versus the secondary web: Snap's current diagram says 10% top / 35% bottom / 6% sides / 15% right rail, while a large and mutually-copying set of blogs still says 150px top / 330px bottom and mentions no side reserve at all. The blogs appear to be repeating a superseded spec

## Fragments

- `Composed for vertical 9:16, the subject centred and held inside the middle of the frame.`
- `Keep the lower third of the frame clear of the subject and of anything that has to be read.`
- `Keep the right quarter of the frame clear, the subject offset to the left of centre.`
- `The composition also reads when cropped to 1:1 and to 4:5 around the centre.`
- `Generous empty space in the upper middle for a headline added later.`
- `No on-screen text, since captions and interface elements will sit over the lower third.`

## Before you finish

Check the result in the app itself. Every number here is the platform describing its own interface, and interfaces change with app versions.
