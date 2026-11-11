---
name: social-posting
description: Post a finished video to the user's own TikTok, Instagram, YouTube or other connected accounts through the Picsart app's post preview - the connected accounts read first, a connect panel only for an account that is missing, then one preview per post whose own buttons post or schedule it. Use in edit-footage's channel-clips job, once it delivered its clips and the user says to post, publish or schedule them; never before delivery. Other jobs and use cases post as they always have, with their own steps or the social tools directly.
user-invocable: false
---

# Posting to social accounts

The app posts, not you. You read which accounts are connected, open the connect panel when one
the user wants is missing, and open a post preview with the video and a caption; the user presses
Post now or Schedule on the preview, and the result comes back to you. Nothing here spends
credits.

## When it runs

These steps are edit-footage's `channel-clips` job's. Every other job and use case keeps
posting as it always has:
 recast's own Post step, or
 the social tools called directly when the
user asks. Only after the use case delivered the video, and only when the user asks to post it or said yes
to the use case's one offer. A post is outward-facing: never open a preview the user did not ask
for, and never press its buttons for them.

## The run

1. **The accounts.** Call `picsart_social_accounts` first, every time: it is read-only and lists
   the connected accounts per platform. Say in one line where the clips can go.
2. **A missing account.** When the user names a platform with no connected account, or one that
   cannot post, call `picsart_social_connect` with those `platforms` once: the app draws a
   Connect panel. End the turn; the user connects there, and their next message says so. Then
   read the accounts again before anything else. Never ask them to describe or paste what the
   panel showed.
3. **The preview, one per post.** Call `picsart_social_post_preview` with the video's URL in
   `media`, exactly as the export returned it, the `platforms`, and a `caption`: the post copy
   the use case wrote, with a campaign's mandatory lines and handles character for character.
   Several videos are several previews, in the order the user chose them. A date or time the user
   named goes in `scheduledFor` with their `timezone`; otherwise leave both out, and the preview
   offers Post now. YouTube takes a `youtubeTitle`: the clip's title. The preview posts nothing by
   itself: it shows the post, and the user presses Post now or Schedule on it.
4. **The result.** The preview's own result says what the user did and what each platform
   answered. Say it back in one line per post: live with its link, scheduled for when, or what
   failed and on which platform. Never claim a post went live until that result says so; a
   preview that was opened and never pressed posted nothing.

Each platform's own rules (a TikTok privacy level, a YouTube title, a length cap) are read from
the preview or the tools' own replies, never assumed. A platform the tools do not list: the file is
in Drive, ready to post by hand; say so in one line.

Run it yourself. Never hand posting to another agent: the handoff loses the video URLs and what
the user said. One preview at a time, the user's pick first.
