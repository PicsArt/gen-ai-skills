---
name: picsart-onboarding
description: Get started with Picsart Video - check that your Picsart account is connected and how many credits you have, open Picsart beside the conversation where the host can, and see what you can make and edit. Use when the user has just installed Picsart, Picsart Video or Picsart GenAI & Video, asks to set it up, asks what it can do, or asks how to get started.
metadata:
  uses: open-picsart
  optional: open-picsart
---

# Getting started with Picsart Video

Read video-core first. One job: in a turn or two, the user knows their account works, has their
Picsart open if they want it, and knows what to ask for next. Nothing here charges credits.

If the user installed Picsart Video in the middle of a task, do stage 1, then go back to that task
in the same conversation. Offer the rest in one line at the end instead.

| Stage | Gate | Skills |
|---|---|---|
| 1. The account and the credits | — | — |
| 2. Open Picsart, when the host has it | ASK | open-picsart |
| 3. What Picsart Video does | — | — |
| 4. Where to start | ASK | — |

## 1. The account and the credits

Call `picsart_credits` with `{}`.

- **It answers:** say in one line that the account is connected and give the balance as the tool
  returns it. Never round it, add it up or guess it.
- **It says the user is not signed in:** say that making and editing need a signed-in Picsart
  account, and that the host will ask them to sign in the first time a step needs it. Go on with
  stage 3, and skip stage 2 until they are signed in.
- **It fails otherwise:** say that the balance could not be read right now, and go on.

## 2. Open Picsart, when the host has it

Only when the open-picsart skill is among your skills: offer it as that skill says. Without it,
skip this stage and say nothing about it: not every host can open Picsart beside the conversation.

## 3. What Picsart Video does

Say it in three short parts, in the user's words. The tools in brackets are for you, never for the
user (video-core's Tools).

- **Drive.** Their files, stored with their Picsart account: browse them, search them in
  Picsart, make folders, move and delete (a deleted file goes to the trash first).
  `picsart_drive` does this. When they bring a file of their own, it comes in with
  `picsart_media_upload`.
- **Create.** Images, videos and audio from a prompt, with a choice of models. They can pick a
  model themselves (`picsart_list_models`), and every creation is quoted before anything is
  charged (`picsart_preflight`, then video-core's SPEND).
- **Edit.** For an image: remove the background (`picsart_remove_bg`), replace it
  (`picsart_change_bg`), enhance it (`picsart_enhance`) or turn it into a vector
  (`picsart_vectorize`). For a video: a scene editor where they watch it, trim, split and comment,
  and approve it before it is exported (`picsart_scene_editor`, video-core's REVIEW).

Edits charge credits too; each is quoted first. Say that once, not per item.

## 4. Where to start

Offer the use cases in this package that fit the user, in their words. Name only use cases that
are here: look at the skills you have, not at this list. Today they can include:

- `screen-video`: a screen recording of an app or website becomes how-to shorts, a promo or a
  tutorial;
- `motion`: a design or the user's own images and clips become an animated ad or reel;
- `short-film`: a story becomes a short film with recurring characters, one look and several
  scenes.

ASK with 2–4 of them, plus "Just explore". On a use case, start it by its name, from its first
stage. On "Just explore", invite them to ask for anything from stage 3, and end the turn.
