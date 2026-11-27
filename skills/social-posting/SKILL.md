---
name: social-posting
description: Offer once to post a final video the user approved to their own TikTok, Instagram, YouTube or other connected accounts, and on a yes post it through the app's post preview - the connected accounts read first, a connect panel only for an account that is missing, then one preview per post whose own buttons post or schedule it. Use after any use case delivered a final video the user approved, when the app you are in draws the post preview, and whenever the user says to post, publish or schedule a delivered video; never before delivery.
user-invocable: false
---

# Posting to social accounts

The app posts, not you. You read which accounts are connected, open the connect panel when one
the user wants is missing, and open a post preview with the video and a caption; the user presses
Post now or Schedule on the preview, and the result comes back to you. Nothing here spends
credits.

## When it runs

After the use case delivered a final video and the user approved it, offer posting once, in one
line beside the delivery: where it could go and that nothing goes out until they press the
preview's button. A no, or no answer, ends it; never offer again for that video. When the user
asks to post, publish or schedule a delivered video on their own, run the steps without the offer.
A use case that sets its own posting keeps it, as its own skill says: make-clips offers posting in
its `channel-clips` job
, and recast posts from its board's Post button
.

Offer it only where the app draws the post preview and the connect panel: both
`picsart_social_post_preview` and `picsart_social_connect` are among your tools and nothing in
the app's own notes says otherwise. An app that cannot draw them gets no offer; the file is ready
to post by hand, and one line says so when the user asks to post.

A post is outward-facing: never open a preview the user did not say yes to, and never press its
buttons for them. Never before delivery: a draft or a preview export is not a final.

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
