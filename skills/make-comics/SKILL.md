---
name: make-comics
description: Turn a photo into a ComicMe creation - a comic of drawn pages, an illustrated tale, a video comic or video tale, a short reel, a narrated quote video or an anime series from several photos - with the person in the photo as its hero, a second person from a second photo if they want one, in a genre, art style and tone they pick, with the price said before anything is charged and every page or clip shown when it is made. Use when the user wants a comic, a tale, a reel, an animated video or a series made from a photo of themselves or someone else, or asks what they would look like as a comic hero.
metadata:
  title: Make comics
  short-description: Turn a photo into a comic, tale, video, reel or anime series
  argument-hint: '[the photo and the comic you want]'
  starter-prompt: Turn my photo into a ComicMe creation.
argument-hint: '[the photo and the comic you want]'
---

# Make a comic from a photo

Read the `picsart-video-rules` skill first. One job: a photo of a person in; a ComicMe creation
out, with the person as its hero. ComicMe makes six things from a photo, each through its own
tool, and this use case covers them all: the user picks one and its settings on the setup console
(stage 1), then the photos, and every one is quoted before anything is charged. The stages below
are written for the comic book and apply to each of the others the same way, with that tool's
schema in place of `picsart_comic_create`'s (see "Each thing ComicMe makes" at the end). A poster
or a single picture is another use case: when the user wants one of those, start that use case
instead.

| Stage | Gate | Skills |
|---|---|---|
| 1. The setup, on the console | ASK | — |
| 2. The photos, as URLs | ASK | — |
| 3. The quote | SPEND | — |
| 4. Draw it | — | — |
| 5. Show it | SHOW | — |

## 1. The setup, on the console

A message asking to open Comic Setup again (the result panel's Open Comic Setup button sends one
after a creation) is this stage once more: open the console, with `heroImage` when the hero's photo
is already known, and treat its next lock as a new setup.

**`picsart_comic_setup` comes first**, before the photos and before a word of story. The console is
the ASK for everything at once: what to make, a comic (`picsart_comic_create`), a tale
(`picsart_comic_create_tale`), a video comic or a video tale (`picsart_comic_create_video`, by its
`style`), a reel (`picsart_comic_create_reel`) or an anime series (`picsart_comic_create_series`),
and that creation's settings: for the comic the genre (`genre`), the art style (`artStyle`), the
tone (`tone`), the premise (`premise`) and how many pages (`pageCount`); for the others their own
look and length, and for a series its story idea (`storyIdea`). It offers the values the Picsart app
offers, every one a value the tool's schema accepts, with the defaults chosen, so no value is
written here. One panel, one lock: never a question in the chat for what the console asks. Read the
request before you open it (the `picsart-video-rules` skill's Asking): most say the hero and the
mood in one line ("make me a horror comic").

- Pass `creation` when the words name what to make ("make me a reel"), and what they decide as
  `suggested.selections` under the tool's own input names, one `suggested.why` line each: the
  genre the words name, the pages when they said a number, a series' story idea when they told
  one, and the language (`language`) they wrote in when it is not English. Pass only what the
  words decide; the console's defaults stand otherwise.
- Pass the hero's photo as `heroImage` when its URL is already known (stage 2), so the console
  shows it. Open the console in full screen where the host supports it.
- The console is the ASK. On `comic_setup_feedback` (`verdict: "locked"`), its `tool` is the one
  to call and its `selections` go to that tool unchanged, with `language` when present; its
  `estimatedCredits` is the cost the console showed next to the lock, for stage 3. That
  lock is the setup's lock; to change it later, open the console again with `current`.
- A "Custom" kind of story (`premise`, or a tale look's `talePremise`) means the user tells
  their own story: ask for it only then, in one question, and pass it under the inputs the
  lock's reply names, which differ by tool and look: the comic's and video comic's `plot`, with
  a `title`, a `heroName` and a `nemesisName` when they gave them; a tale's `plot` with its
  `companionName`; a video tale's `talePlot`, `taleTitle` and `taleHeroName`; a reel's `story`
  with its `secondaryName`. Any other kind of story needs none. Never ask for a story the user
  did not offer: a comic needs none, and only the series requires one, which the console
  collects.
- A narrated quote video, `picsart_comic_create_aphorism`, needs no photo and no console: offer
  it only when the user asks for words on screen rather than themselves, and take its `text` and
  `author` in the chat.

"Just make it" still opens the console: locking it is one tap, and it is where the defaults are
said (Asking, rule 6).

Where the host notes say the console is not served, ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) what to make, then its settings, in
the chat instead, one question each, on `picsart_ask` where the host has no question tool of its
own: 2–4 of the schema's values with the default first, and one line on what each does. Derive
the tone from the genre or the user's words.

## 2. The photos, as URLs

After the lock, open `picsart_drive_upload_ask` for the hero's photo, and say in its prompt that
a second person can join from a second photo: the friend of a comic or a video comic
(`friendImage`), the companion of a tale or a video tale (`companionImage`), the
`secondaryImage` of a reel. An anime series takes its cast in that one panel
(`characterImages`): the main role's photo first, then the secondary role's, then any other
character's, up to the schema's limit; the first is the protagonist. Ask for all of them in that
first panel, as the `picsart-video-rules` skill says under Asset URLs; the panel is the ASK, and
the URLs arrive with the user's next message.

Each goes in as an https URL a Picsart tool returned in this conversation, as those same rules
say (a link or an attachment with `picsart_drive_upload`, a photo in their Picsart Drive with
`picsart_drive_list`); a file on disk, where you can run shell commands, comes in with
`picsart_upload_local_files`, as its description says. The hero's URL is `heroImage`. One upload
serves the whole conversation.

## 3. The quote

The lock's `estimatedCredits` is the cost of this setup as the console showed it: the Picsart
price of one page, clip or episode times the count, the same price the tool charges when the job
starts. Say that cost in one message, as "This comic costs 21 credits", then SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says): no call of
your own for a price or a balance before it. A page or episode the tool could not make is not
charged. When the lock carries no `estimatedCredits`, say that each page, clip or episode is
charged. When the result carries a link to top up, give it exactly as returned.

## 4. Draw it

One `picsart_comic_create` call (the lock's `tool`, for another creation), with every input from
stages 1 and 2. It answers with a job
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

## Each thing ComicMe makes

The console's lock names the tool. Each is a job like the comic's: the same stages, the same quote
before anything is charged, the same `picsart_job_status` polling with the receipt's `job`
verbatim, and never a second call while the job runs. The values and their defaults are in each
tool's own schema.

- **A tale**, an illustrated storybook: `picsart_comic_create_tale`, with a `setting`, `artStyle`,
  `tone`, `theme` and `premise` of its own and a `companionImage` for a second person; charged per
  page; its result carries `result.taleId`.
- **A video comic or a video tale**, drawn from the photo and narrated:
  `picsart_comic_create_video`, in the comic or tale `style`; charged per page; its result
  carries `result.url` and `result.videoId`.
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
  Episode by episode instead, when the user wants to see one before the next: the same call with
  `firstEpisodeOnly: true` plans the arc and makes episode 1 alone, charged as one episode; then each
  **next episode** is `picsart_comic_continue_series` with `seriesId` and, when they said what happens,
  `episodeIdea`, charged as one episode: say that charge, then SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says), every time; its result carries
  `result.url`, `result.episode` and `result.episodeId`. A refusal naming an unfinished episode means
  `picsart_comic_retry_episode` with that `episodeId` first, charged as one episode, so SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) again. A
  series made with every episode at once has no next one. `picsart_comic_export_series` cuts the finished
  episodes into one video, free; `picsart_comic_replan_series` rewrites the episodes not yet made for
  the user's `reason`, free, and the finished ones stay.
- **A video of a comic or tale that already exists**: `picsart_comic_export_video` with the
  `comicId` or `taleId` kept in the project record; free; its result carries `result.url`.
- **A video comic or tale made again** from the same pages: `picsart_comic_regenerate_video` with
  the `videoId` kept in the project record; free, and the earlier video is replaced, so say so first.

A video or a clip is SHOWN as its link, the way a page is; a series is shown episode by episode.

## Changing a book that exists

A comic or tale the user already has, named by the `comicId` or `taleId` in the project record, is
changed without drawing it again. Each change is a job like the comic's, polled the same way with
the receipt's `job`, and its result carries the whole book's `result.pages` again.

- **More pages**: `picsart_comic_add_page` with `pageCount`; each added page is charged at the
  comic's per-page price, so say the count and that charge, then SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says). `result.addedPages`
  names the new pages: SHOW those.
- **A page drawn again**: `picsart_comic_rewrite_page` with the `page` number (0 is the cover);
  charged as one page, and the old page is gone, so say both, then SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says).
- **A page removed**: `picsart_comic_delete_page` with the `page` number; free, and it cannot be
  undone, so ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) first, "Delete page 2? It can't be brought back." / "Keep it", and call it only on
  the first.

## When a call fails

- **The photo refused** ("URL refused", a local path): get a URL (stage 2), then call again.
- **A setting refused:** read the value from the tool's schema, correct it, and quote again.
- **The job is not found:** the receipt was changed on the way back. Give what you have, and offer
  to draw the comic again, which charges again.
