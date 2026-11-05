---
name: make-comics
description: Turn a photo into a short ComicMe comic book - the person in the photo becomes the hero of a few drawn pages in a genre, art style and tone the user picks, with a friend from a second photo and the user's own story if they want them - or into the other things ComicMe makes - an illustrated tale, an animated video, a motion episode, a short reel, a narrated quote video, or an anime series from several photos - with the price said before anything is charged, and every page or clip shown when it is made. Use when the user wants a comic, a tale, a reel, an animated video or a series made from a photo of themselves or someone else, or asks what they would look like as a comic hero.
metadata:
  title: Make comics
  short-description: Turn a photo into a short comic book
  argument-hint: '[the photo and the comic you want]'
  starter-prompt: Turn my photo into a comic book.
argument-hint: '[the photo and the comic you want]'
---

# Make a comic from a photo

Read the `picsart-video-rules` skill first. One job: a photo of a person in; a short comic book
out, drawn page by page, with the person as its hero. ComicMe makes other things from the same
photo, each through
its own tool, and this use case covers those too (see "The other things ComicMe makes" at the end):
the stages below are written for the comic book and apply to each of them the same way, with that
tool's schema in place of `picsart_comic_create`'s. A poster or a single picture is another use
case: when the user wants one of those, start that use case instead.

| Stage | Gate | Skills |
|---|---|---|
| 1. The hero, and the comic they want | ASK | — |
| 2. The photo, as a URL | — | — |
| 3. The quote | SPEND | — |
| 4. Draw it | — | — |
| 5. Show it | SHOW | — |

## 1. The hero, and the comic they want

Read the request before you ask (the `picsart-video-rules` skill's Asking). Most say the hero and
the mood in
one line ("make me a horror comic"). Say back what follows from it, and ASK only what is open and
changes the pages, one question each. The values and their defaults are in `picsart_comic_create`'s
own schema, never written here:

- **The genre** (`genre`): 2–4 of the schema's values, the default first, each with one line on
  the world it draws the hero into.
- **The art style** (`artStyle`): 2–4 of the schema's values, the default first, each with one
  line on the line and colour it gives every page.
- **How many pages** (`pageCount`): the default first, then more, within the schema's limit. More
  pages cost more and take longer.

Derive, then say: the tone (`tone`) follows the genre or the user's words, from the schema's
values, or is left to the tool; the language (`language`) is the language they wrote in. A second
person they named goes in as the friend (`friendImage`).

Ideas get words, not options. When the user tells their own story, keep it as `plot`, with a
`title`, a `heroName` and a `nemesisName` when they gave them: the tool then draws their story
under the premise "Custom". Otherwise leave `premise` to the tool. Never ask for a story the
user did not offer: a comic needs none.

"Just make it" takes the defaults and says them as assumed (Asking, rule 6).

## 2. The photo, as a URL

The hero's photo goes in as `heroImage`, and the friend's as `friendImage`: each an https URL a
Picsart tool returned in this conversation, as the `picsart-video-rules` skill says under Asset
URLs: a file you cannot reach comes in with `picsart_drive_upload_ask`, a link or an attachment
with `picsart_drive_upload`, and a photo in their Picsart Drive is found with `picsart_drive_list`.
A file on disk, where you can run shell commands, comes in with `picsart_upload_local_files`, as
its description says. One upload serves the whole conversation.

## 3. The quote

`picsart_comic_create` charges credits for every page it draws, and gives no quote of its own: say
that each page is charged, that the amount is not known in advance, and the balance from
`picsart_credits`, in one message, then SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says). A page the
tool could not draw is not charged. When the balance looks short, offer fewer pages. When the
result carries a link to top up, give it exactly as returned.

## 4. Draw it

One `picsart_comic_create` call, with every input from stages 1 and 2. It answers with a job
receipt, not the comic: drawing takes a few minutes. Pass the receipt's `job` verbatim to
`picsart_job_status` until it reports the result, as the `picsart-video-rules` skill's Tools says.
While it
runs, say in one line that the pages are being drawn. Never call `picsart_comic_create` again while
its job runs: a second call draws and charges a second comic.

A FAILED job carries a user-facing `error`: give it, and offer another photo or fewer pages, which
is a new SPEND.

## 5. Show it

COMPLETED carries `result.pages`, each with its `page` number and `url`, the same pages in order
as image assets in `result.assets`, and `result.comicId`.
SHOW every page as a link, in order, with one line each on what it is: "the cover", "page 1".
Look at the cover as the host notes say under "Looking at an image", and say in one line what the
hero looks like in it. A number in `result.failedPages` is a page that could not be drawn: say so,
and that it was not charged.

Keep `result.comicId` in the project record: it names this comic in a later turn. Then offer one
next step in a sentence (another genre, more pages, a comic for the friend), and do it only on a
yes: it is a new SPEND.

## The other things ComicMe makes

Read the request for what the user wants to end up with, and pick the one tool that makes it. Each
is a job like the comic's: the same stages, the same quote before anything is charged, the same
`picsart_job_status` polling with the receipt's `job` verbatim, and never a second call while the
job runs. The values and their defaults are in each tool's own schema.

- **A tale**, an illustrated storybook: `picsart_comic_create_tale`, with a `setting`, `artStyle`,
  `tone`, `theme` and `premise` of its own and a `companionImage` for a second person; charged per
  page; its result carries `result.taleId`.
- **An animated video** drawn from the photo and narrated: `picsart_comic_create_video`, in the
  comic or tale `style`; charged per page; its result carries `result.url` and `result.videoId`.
- **A motion episode**, a vertical video of several animated shots with speech and music, as long
  as its `shotCount` and `clipSeconds` make it, within the schema's bounds:
  `picsart_comic_create_episode`; charged once; its result carries `result.url` and
  `result.episodeId`.
- **A reel**, one short vertical clip, as long as its `durationSeconds` within the schema's bounds:
  `picsart_comic_create_reel`, with the user's own `story` when they told one and a
  `secondaryImage` for a second person; charged once; its result carries `result.url` and
  `result.episodeId`.
- **A narrated quote video**, no photo needed: `picsart_comic_create_aphorism`, with the `text`
  and its `author`; charged once; its result carries `result.url`.
- **An anime series** of several episodes from a story idea and the characters' photos, as many
  as the schema's `characterImages` allows: `picsart_comic_create_series`, with `storyIdea`,
  `characterImages` and `totalEpisodes`; charged
  per finished episode, and the job runs a long time; its result carries `result.episodes`,
  `result.fullVideoUrl` when there is one, and `result.seriesId`. Say the length and the per-episode
  charge before the quote.
- **A video of a comic or tale that already exists**: `picsart_comic_export_video` with the
  `comicId` or `taleId` kept in the project record; free; its result carries `result.url`.

A video or a clip is SHOWN as its link, the way a page is; a series is shown episode by episode.

## When a call fails

- **The photo refused** ("URL refused", a local path): get a URL (stage 2), then call again.
- **A setting refused:** read the value from the tool's schema, correct it, and quote again.
- **The job is not found:** the receipt was changed on the way back. Give what you have, and offer
  to draw the comic again, which charges again.
