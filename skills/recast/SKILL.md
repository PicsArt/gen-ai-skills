---
name: recast
description: Put the user's own characters, people or things into a video of theirs with Recast - each picture replaces one person or thing in the video, and the motion, the place and the sound stay as filmed - on a board that checks the video, offers each video model with its price and makes the video itself. A character swap for an AI influencer, a mascot or a product placed into real footage. Use when the user has a video and wants someone or something in it replaced by their character, a photo or a product ("put my character in this clip", "replace the cup with my product", "swap me into this video"). Not for a new video from a prompt or a picture (generate-media), cutting their footage (edit-footage), or an animated ad rebuilt with new photos and text (recreate-video).
metadata:
  title: Recast
  short-description: Put your character or product into your own video
  argument-hint: '[your video, and who or what goes in]'
  starter-prompt: Put my character into my video.
argument-hint: '[your video, and who or what goes in]'
---

# Recast

When you read `picsart_scene_capabilities` or the recipe index (`picsart_scene_recipe` without `name`), pass `useCase: "recast"`: the answer leads with what this job reads and names the rest in one line.

Read picsart-video-rules first. One job: one of the user's own videos, with people or things in it
replaced by the user's pictures. The Recast board checks the video, offers the video models with
the price, and makes the video itself. You bring it the video, the pictures and who is in the video,
then read what it made.

| Stage | Gate | Skills |
|---|---|---|
| 1. The video and the pictures | ASK | — |
| 2. Who is in the video | — | — |
| 3. The board | ASK, SPEND | — |
| 4. What it made | DELIVER | — |

## 1. The video and the pictures

Every file goes in as a Picsart-hosted URL, as picsart-video-rules's Asset URLs says. A video or a
picture a Picsart tool returned in this conversation is used as it is. Files on the user's disk go
up with `picsart_upload_local_files` when you have a shell. Otherwise
ASK with `picsart_drive_upload_ask` for all of them in one panel, in the first turn.

What goes in, at most 8 pictures, in the order the user named them:

- **A character they name:** find it with `picsart_asset_list`, with no `projectFolderUid` for
  a character made outside a film and with the film's for its cast. Pass its `portraitUrl` as `url`,
  its `name`, and `character: true`: the sheet's views are one character.
- **A photo or a product shot:** its URL, with a `name` when the user gave one.
- **A new place they asked for** in a picture: that picture with `role: "place"`.

The board's own What goes in step adds pictures from the user's images, characters and props, or
from their device, and its Place step adds a place from their images, so never hold the board for a
picture: open it with what you have. A picture
that does not exist yet (a new character, a product shot) is a job of its own: offer make-character
or generate-media in one sentence, and do it only on a yes.

The board checks the video's length, size and frame rate against each model and says which ones
take it, so read no limits here.

## 2. Who is in the video

Read the video's length with `picsart_media_probe`, then look at 4 to 6 moments spread over it with
`picsart_media_video_stills` (`times`, `labels: true`). Both are free. Look at the sheet as
picsart-video-rules's Asset URLs says.

Write `found` from what you saw: every person, the main one first, then the things that matter to
the action, at most 8. Each is a short lowercase label by how it looks, never by where it stands or
by a name: "the woman in the long dark coat", "the cup in her hand". The board offers these labels
as what each picture replaces. When the user said who or what a picture replaces, set its
`replaces` to the label that matches.

## 3. The board

ASK with `picsart_recast_setup`: `videoUrl`, `pictures`, `found`, and only what the user said:

- `sound`: `generated` when they want new sound, `none` for silence; leave it out to keep the
  video's own sound.
- `notes`: their own words for the run that the board has no control for ("keep her hat on, make
  the cup red"), and with them `notesSay`: whether those words say what the place should be, and
  whether they say anything about the sound.

Opening the board is free. It is the whole turn: add one line at most, and end the turn. On the
board the user picks what each picture replaces, the place, the model, the resolution, the versions
and the sound, and sees the price above Generate. Their Generate at that price is this spend's
go-ahead: never quote it again in the chat, and never call `picsart_generate` for this video
yourself. The board runs every job, and a second run charges twice.

## 4. What it made

The board's answer is `recast_feedback`; read it before the sentence around it.

- **`status: "done"`:** the board already shows the video before and after, with Download. Say in
  one line that it is ready. Give each link in `results` only when the user asks for the file. When
  `shortfall` is there, say plainly how many versions could not be made (`versions`), or how many
  kept the model's own sound because the original could not be put back (`sound`).
- **`status: "failed"`:** say in one line where it stopped, from `failedStep`: `words` is the check
  of what they wrote, `copy` is preparing their video, `make` is making the new video, and `sound` is
  putting the sound back. The board offers the other models.
- **`recast_post`:** they pressed Post. Open `picsart_social_post_preview` with that `video` in
  `media` (`[{ "type": "video", "url": <video> }]`), a caption you wrote for it, and as `platforms`
  the ones the user named, else `["instagram", "tiktok"]`: the preview lets them tick others.

Run nothing again unless the user asks: Change and run again and Try another model are on the
board. Then offer one next step in a sentence (another version, another model, posting it), and do
it only on a yes.
