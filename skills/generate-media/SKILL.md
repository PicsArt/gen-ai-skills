---
name: generate-media
description: Make an image, a video, a voice line, a sound or a song from a prompt, or edit a picture - remove or replace its background, enhance or upscale it, or turn it into a vector - with a model that fits, its settings checked and its price quoted before anything is charged. Also answers questions about models, prices, credits and Drive. Use when the user asks to generate, make or create an image, a video or audio, to edit a picture, to browse the models, or about a price, their credits or their Drive files.
metadata:
  uses: film-shot-generation
---

# Make or edit an image, a video or audio

Read picsart-video-rules first. One job: the user asks for one piece of media, or one edit of a picture,
and gets it with no failed call and no surprise charge. A whole video project is another use case:
when the user wants their footage cut, a screen recording turned into a video, a film or an
animated design, start that use case instead.

| Stage | Gate | Skills |
|---|---|---|
| 1. What to make, and from what | ASK | — |
| 2. The user's files, as URLs | — | — |
| 3. The model and its settings | ASK | film-shot-generation |
| 4. The quote | SPEND | — |
| 5. Run it | — | film-shot-generation |
| 6. Show it | SHOW | — |

A question that makes nothing (which models there are, a model's settings, a price, the balance, a
Drive folder) skips the stages: answer it as **Questions that make nothing** says, and charge
nothing.

## 1. What to make, and from what

Read the request before you ask (picsart-video-rules's Asking). Most say all of it: the medium, the
subject, and any picture or clip to start from. Say back what follows from it in one line ("a 9:16
image for a story"). ASK only for what is open and changes the result: the medium when it is not
said, the frame when the destination does not set it, a voice or a song when "audio" is not said.

An edit names its tool by what it does to the picture:

| The user wants | Tool | Its input |
|---|---|---|
| The background removed, the subject cut out | `picsart_image_remove_bg` | `image` |
| The background replaced ("put it on a beach") | `picsart_image_change_bg` | `image`, and `prompt` for the new background |
| Sharper, cleaner or bigger ("make it 4k") | `picsart_image_enhance` | `image`, and `scaleFactor` when they gave one |
| A vector, an SVG | `picsart_image_vectorize` | `image` |

Each picks its own model. Before a vector of a photo, say once that photos vectorize poorly and
logos, icons and simple graphics well. Anything else is made with `picsart_generate`.

## 2. The user's files, as URLs

Every input is a URL: `image` on the edit tools, `imageUrls` and `videoUrl` on `picsart_generate`.
A URL a Picsart tool returned in this conversation is passed as it is (picsart-video-rules's Asset URLs).
Otherwise:

- **A file on disk, and you can run shell commands:** call `picsart_upload_local_files` with each
  file's `name` and `bytes`, run each command it returns with the path in place of `{path}`, and
  read the URL from what the command prints, where the tool's description says it is. The copy is
  temporary: to keep the file, save it with `picsart_drive_upload` (`url`, `name`).
- **A file you cannot reach:** call `picsart_drive_upload_ask` and end the turn. The URL arrives with
  the user's next message.
- **An attachment the host hands you as a file object** (`download_url`, `file_id`): pass it as
  `file` to `picsart_drive_upload`, and use the `url` in its result.
- **A file in their Picsart Drive:** find it as **Their Drive** says, and use its `url`, never its
  `downloadUrl`.

Upload a file once, and reuse its URL for the rest of the conversation. Never pass a local path to
a tool: when one is refused (`local_source_not_supported`, "Only https:// URLs or data: URIs"),
get a URL as above and call again.

## 3. The model and its settings

An edit skips this stage. For `picsart_generate`:

1. **The model.** When the user named one, use it. When they want to pick, ASK with
   `picsart_model_choose`: three candidates from `picsart_model_catalog` (`concise: false`), each with what it is best
   for here, one marked recommended. When they want to look through all of them, open
   `picsart_model_show` with the `mode` and `purpose: "generate"`. Otherwise choose it yourself:
   - an image: `flux-2-pro`;
   - anything else: `picsart_model_catalog` with the `mode`, `purpose: "generate"`, the
     `inputType` (`t2v` or `i2v` for a video, `tts` for a voice line, `sfx` for a sound, `music`
     for a song) and `acceptsImage` or `acceptsVideo` when the user brought one. Take the first
     row that holds the frame, the length and the inputs the request needs.

   Never name the model to the user unless they asked about models (picsart-video-rules's Tools).
2. **Its settings.** For anything beyond `prompt`, read `picsart_model_params` for that model,
   and set only the settings it lists, with values it allows. A model's own settings, such as a
   start frame or a voice, go in `extra`. Correct a value whose meaning is clear without asking
   (`"1920x1080"` is `aspectRatio: "16:9"`); ASK when two readings give different results.
   Never take a setting from a model with a similar name. A start or end frame goes first in
   `imageUrls`, and the prompt names it: "IMAGE 1 - START FRAME".
3. **A video** is drafted and prompted as picsart-video-rules's SPEND says (rules 5, 8 and 9): its key
   frames first, as stills, and every prompt compiled and verified, as the film-shot-generation skill says
   under Key frames and Compile and verify.

## 4. The quote

Every generation and every edit charges credits. Quote it and get a yes, as picsart-video-rules's SPEND
says. `picsart_preflight` takes the model and the planned `picsart_generate` inputs as `params`,
`prompt` included: it checks them against the model and estimates the price. Fix everything it
reports before you quote. `credits: null` means the price is not known, never that it is free. The
edit tools give no quote of their own: to price one, preflight the model id you will pass as its
`model` (the default may pick a different model). If that gives no number, say it charges credits
and the amount is not known in advance.

When the balance from `picsart_credits` is short of the quote, say by how much, and offer what
costs less: fewer outputs (`count`), a lower resolution or a shorter length, or a cheaper model.
When the result carries a link to top up, give it exactly as returned.

## 5. Run it

- Several outputs of one prompt are `count` on one call; several different prompts on one model
  are `items` on one call (picsart-video-rules's SPEND, rule 4). Never loop calls: each call draws its own
  progress card.
- A generation answers with a job. Follow it with `picsart_job_status`, passing the job and the
  `model` (picsart-video-rules's Tools). With `count` or `items` the top-level `job` is only the first: pass
  each handle in `jobs` (an `items` entry's are in its own `jobs`) as `job`, one call each. Where
  the host draws widgets, the generation's card follows its jobs and posts the results back, so
  never ask the user to wait. Never send a generation again because it seems slow or the host
  timed out: it has usually finished and charged. Check the job, and for an `async: false` call
  look in their Drive first.
- A result belongs to their Drive only when it says so (`drive`). With `folderUid`, a sync result
  is filed there before it returns (`drive.uid`); save an async one there with
  `picsart_drive_upload` once it completes.

## 6. Show it

SHOW each result, with one line on what it is: what was made, not how. Then offer one next step in
a sentence (another take, a different frame, an edit), and do it only on a yes.

## Questions that make nothing

All of these are free. Answer in a few lines; never paste a whole list or table.

- **Which models there are:** open `picsart_model_show` with the `mode` they asked about, so they
  can look through them. When you only need the list yourself, read `picsart_model_catalog`
  instead.
- **What a model can do:** read `picsart_model_params` and say the gist: what it takes and its
  limits.
- **What something would cost:** `picsart_preflight` for the price, `picsart_credits` for the
  balance. Give both, and make nothing until they say yes (stage 4).
- **Their balance:** `picsart_credits`. Give it exactly as returned.
- **Their Drive:** `picsart_drive_list` with no `folderUid` lists the top level. To open a folder,
  read its `uid` from `folders` in that result and pass it as `folderUid`, with `type` to keep one
  kind of file: `folderUid` takes a uid, never a folder name.

## When a call fails

- **Not enough credits:** read `picsart_credits`, give the balance and what the call needed, and
  offer what costs less (stage 4). Never call it again until the user says they are ready.
- **Not signed in:** making and editing need a signed-in Picsart account. Say so in one line and
  stop; the host asks them to sign in. Never retry.
- **A setting refused** ("Invalid parameter", "Unsupported value", a length past the model's
  limit): read `picsart_model_params`, correct the value, and quote again if the price changed.
  Never send the same settings again.
- **The model is not found:** find its id with `picsart_model_catalog` (`provider` with the part of
  the name you have), then call again with the id it lists.
- **A local path or a file refused:** get a URL (stage 2), then call again.
- **The model is busy or the service errors:** say it is busy right now, and offer to try again
  in a moment or with another model. Never loop the retry yourself.
- **A link from earlier stopped working:** find the file in their Drive (`picsart_drive_list`),
  or offer to make it again.
