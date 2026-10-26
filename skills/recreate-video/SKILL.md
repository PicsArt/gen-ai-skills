---
name: recreate-video
description: Rebuild a reference video as an editable animated scene that moves and looks like it - the same layout, the same timing, the same motion - measured from the video rather than eyeballed, with the user's own photos and text in place of the original's. Use when the user brings a video and wants one like it ("make a video like this one", "recreate this ad", "copy this animation", "rebuild this promo with my product"). Not for editing or trimming the user's own footage, and not for a new video from a description alone.
metadata:
  uses: reference-fragment-matching, motion-tracking-from-video, scene-building-basics, quality-review
  title: Recreate a video
  short-description: Rebuild a reference video with your own photos and text
  argument-hint: '[reference video, your photos and text]'
  starter-prompt: Recreate this reference video with my own photos and text.
argument-hint: '[reference video, your photos and text]'
---

# Recreate a video

A reference video is flat pixels: nothing in it says how it was made. This use case measures it,
fragment by fragment, and rebuilds it as a scene the user can edit, with their own content. The
result reproduces what the viewer sees, not the original project.

Read picsart-video-rules first. One job: a reference video in, an editable scene that matches it out.

| Stage | Gate | Skills |
|---|---|---|
| 1. Take the reference in | ASK | — |
| 2. Read it and check the scope | SPEND | reference-fragment-matching |
| 3. The fragment plan | SPEND, ASK | reference-fragment-matching |
| 4. Measure each fragment | SPEND | reference-fragment-matching, motion-tracking-from-video |
| 5. Build each fragment | — | reference-fragment-matching, scene-building-basics |
| 6. Check each fragment | SPEND | reference-fragment-matching, motion-tracking-from-video, quality-review |
| 7. Join the fragments | SPEND | reference-fragment-matching |
| 8. The user reviews | REVIEW | — |
| 9. Deliver | DELIVER | — |

## 1. Take the reference in

ASK for what is missing, in one question:

- **the reference video**, brought in as picsart-video-rules says (Asset URLs);
- **which part**, when it is longer than the part they want: a start and end time;
- **their own content** for the places the reference shows photos, logos or text. Without it, the
  scene gets plain stand-ins in each of those places: a colour box of the same size, and the text
  the reference shows. Never the reference's own pixels, as the reference-fragment-matching skill says.

## 2. Read it and check the scope

`picsart_media_probe` on the reference for its size, frame rate and duration, and a sheet of
stills across it with `picsart_media_video_stills` (SPEND, as picsart-video-rules says, when its description
says it charges). From the stills, decide whether it is within what reference-fragment-matching can rebuild.
When it is not, say what of it can and cannot be rebuilt, and stop unless the user still wants it.

## 3. The fragment plan

Split the reference and take the global census as the reference-fragment-matching skill says, then show the
user the plan in plain words: the fragments in order, each with its window and what happens in it,
and the elements that recur. ASK once whether it is right. A fragment the user merges, splits or
drops changes the plan before any measuring starts.

**The plan is the project record.** Where the host gives you files, keep it as `recreation.md` in
the working folder, with the beat tables, the boundary records and every check; otherwise keep it
in the conversation. Update it whole as each fragment lands.

## 4. Measure each fragment

The census and the measured beat table for each fragment, as reference-fragment-matching says, with the
tracking done as motion-tracking-from-video says. Quote the tracking for the whole plan in one SPEND, and
start every job before following any.

## 5. Build each fragment

Build it as reference-fragment-matching and scene-building-basics say, from the beat table only. A beat with no
measured row is not built: measure it first.

## 6. Check each fragment

Check it against the reference as reference-fragment-matching says, and check the scene as quality-review says.
The fix rounds are picsart-video-rules's. A fragment that still misses after them goes on, and its gap goes
into the plan in plain words ("the card docks 0.2 s late").

## 7. Join the fragments

Join them and check the whole clip as reference-fragment-matching says (`references/seams.md` there).

## 8. The user reviews

REVIEW the whole scene, as picsart-video-rules says. With it, in one or two sentences: what matches, and
any gap the checks left, in plain words, never a score. Each change the user asks for goes back to
the fragment it lives in, and through its check again.

## 9. Deliver

DELIVER as picsart-video-rules says.
