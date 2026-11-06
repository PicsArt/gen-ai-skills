---
name: make-comics
description: Turn a photo into a ComicMe creation - a comic book of drawn pages, an illustrated tale, an animated video, a motion episode, a short reel, a narrated quote video or an anime series from several photos - with the person in the photo as its hero, a second person from a second photo if they want one, in a genre, art style and tone they pick, with the price said before anything is charged and every page or clip shown when it is made. Use when the user wants a comic, a tale, a reel, an animated video or a series made from a photo of themselves or someone else, or asks what they would look like as a comic hero.
metadata:
  title: Make comics
  short-description: Turn a photo into a comic book, video, reel or anime series
  argument-hint: '[the photo and the comic you want]'
  starter-prompt: Turn my photo into a ComicMe creation.
argument-hint: '[the photo and the comic you want]'
---

# Make a comic from a photo

Read the `picsart-video-rules` skill first. One job: a photo of a person in; a ComicMe creation
out, with the person as its hero. ComicMe makes six things from a photo, each through its own
tool, and this use case covers them all: the user picks one first (stage 1), then the photos,
then the settings, and every one is quoted before anything is charged. The stages below are
written for the comic book and apply to each of the others the same way, with that tool's schema
in place of `picsart_comic_create`'s (see "Each thing ComicMe makes" at the end). A poster or a
single picture is another use case: when the user wants one of those, start that use case instead.

| Stage | Gate | Skills |
|---|---|---|
| 1. What to make | ASK | — |
| 2. The genre | ASK | — |
| 3. The art style | ASK | — |
| 4. The length | ASK | — |
| 5. The photos, as URLs | ASK | — |
| 6. The quote | SPEND | — |
| 7. Draw it | — | — |
| 8. Show it | SHOW | — |

## 1. What to make

The choice comes before anything else, the photo included. When the request already names it
("make me a reel", "an anime series of us"), take it and go on. Otherwise ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says), the comic book
first, one line each on what comes out. Stages 1 to 4 are boards of buttons, never lists the
user answers by typing, one per turn, as the `picsart-video-rules` skill says under How you talk
to the user. Where the host has no question tool of its own, the board is `picsart_ask`, one
question per call, its answer read from the user's next turn, with `recommended` left unset: the
option to take first is simply first, and no badge says so. The quote's yes in stage 6 is never
put on that board.

- **A comic book**: drawn pages with them as the hero, `picsart_comic_create`.
- **A tale**: an illustrated storybook, `picsart_comic_create_tale`.
- **An animated video**: pages drawn and animated into one narrated video,
  `picsart_comic_create_video`.
- **A motion episode**: a vertical video of several animated shots with speech and music,
  `picsart_comic_create_episode`.
- **A reel**: one short vertical clip, `picsart_comic_create_reel`.
- **An anime series**: several episodes from a story idea and the characters' photos,
  `picsart_comic_create_series`.

A narrated quote video, `picsart_comic_create_aphorism`, needs no photo: offer it only when the user
asks for words on screen rather than themselves. Keep the choice in the project record; the stages
below name that tool wherever they say `picsart_comic_create`.

## 2. The genre

Read the request before you ask (the `picsart-video-rules` skill's Asking): a value the request
already named ("make me a horror comic") is taken and said back, and its board is skipped. That
holds for stages 2 to 4. The values and their defaults are in `picsart_comic_create`'s own
schema, never written here.

The genre (`genre`): one board, 2–4 of the schema's values, the default first, each with one line
on the world it draws the hero into.

## 3. The art style

The art style (`artStyle`): one board, 2–4 of the schema's values, the default first, each with
one line on the line and colour it gives every page.

## 4. The length

How many pages (`pageCount`): one board, the default first, then more, within the schema's limit;
more pages cost more and take longer. The other creations ask their own length from their schema
the same way, one board: a reel's `durationSeconds`, an episode's `shotCount`, a series'
`totalEpisodes`.

Derive, then say: the tone (`tone`) follows the genre or the user's words, from the schema's
values, or is left to the tool; the language (`language`) is the language they wrote in.

Ideas get words, not options. When the user tells their own story, keep it as `plot`, with a
`title`, a `heroName` and a `nemesisName` when they gave them: the tool then draws their story
under the premise "Custom". Otherwise leave `premise` to the tool. Never ask for a story the
user did not offer: a comic needs none.

"Just make it" takes the defaults and says them as assumed (Asking, rule 6).

## 5. The photos, as URLs

After the last setting's answer, open `picsart_drive_upload_ask` for the hero's photo, and say in
its prompt that a second person can join from a second photo: the friend of a comic book
(`friendImage`), the companion of a tale (`companionImage`), either of those for a video or an
episode by its style, the `secondaryImage` of a reel. An anime series takes every character's
photo in that one panel, the first the protagonist (`characterImages`). Ask for all of them in
that first panel, as the `picsart-video-rules` skill says under Asset URLs; the panel is the ASK,
and the URLs arrive with the user's next message.

Each goes in as an https URL a Picsart tool returned in this conversation, as those same rules
say (a link or an attachment with `picsart_drive_upload`, a photo in their Picsart Drive with
`picsart_drive_list`); a file on disk, where you can run shell commands, comes in with
`picsart_upload_local_files`, as its description says. The hero's URL is `heroImage`. One upload
serves the whole conversation.

## 6. The quote

`picsart_comic_create` charges credits for every page it draws, and gives no quote of its own: say
that each page is charged, that the amount is not known in advance, and the balance from
`picsart_credits`, in one message, then SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says). A page the
tool could not draw is not charged. When the balance looks short, offer fewer pages. When the
result carries a link to top up, give it exactly as returned.

## 7. Draw it

One `picsart_comic_create` call, with every input from stages 1 to 5. It answers with a job
receipt, not the comic: drawing takes a few minutes. Pass the receipt's `job` verbatim to
`picsart_job_status` until it reports the result, as the `picsart-video-rules` skill's Tools says.
While it
runs, say in one line that the pages are being drawn. Never call `picsart_comic_create` again while
its job runs: a second call draws and charges a second comic.

A FAILED job carries a user-facing `error`: give it, and offer another photo or fewer pages, which
is a new SPEND.

## 8. Show it

COMPLETED carries `result.pages`, each with its `page` number and `url`, the same pages in order
as image assets in `result.assets`, and `result.comicId`.
SHOW every page as a link, in order, with one line each on what it is: "the cover", "page 1".
Look at the cover as the host notes say under "Looking at an image", and say in one line what the
hero looks like in it. A number in `result.failedPages` is a page that could not be drawn: say so,
and that it was not charged.

Keep `result.comicId` in the project record: it names this comic in a later turn. Then offer one
next step in a sentence (another genre, more pages, a comic for the friend), and do it only on a
yes: it is a new SPEND.

## Each thing ComicMe makes

Stage 1's choice names the tool. Each is a job like the comic's: the same stages, the same quote
before anything is charged, the same `picsart_job_status` polling with the receipt's `job`
verbatim, and never a second call while the job runs. The values and their defaults are in each
tool's own schema.

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
