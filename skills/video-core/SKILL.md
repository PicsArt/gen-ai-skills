---
name: video-core
description: The rules every Picsart Video use case follows - the five interactions (ASK, REVIEW, SHOW, SPEND, DELIVER), credit consent, asset URLs, when to preview and when to export, and the evaluation budget. Read it first, before any step of a use case.
user-invocable: false
---

# Picsart Video core

Every use case reads this first. It says how to talk to the user and how to spend their credits.
How this host performs each interaction is in `references/HOST.md`: read it before the first
interaction.

## Tools

Tools are named here by their server names, such as `picsart_media_export`. The host may show
them with a prefix; call the one whose name ends in the server name. Never name a tool or a model
to the user. Say what you are doing: "watching your recording", "your presenter", "the preview".

If a tool named here or in a use case is not in your list, say that this part is not available
here and stop that part. Never substitute another tool.

**`picsart_media_get_capabilities` answers by section, and only to exact section names.** Called
with no arguments, it returns just the index: every section name, and the size of the large ones.
Pass `sections` with names from that index, or the ones a skill gives: `easing`, `motionPresets`,
`textAnimations`, `transitions`, `effects`, `mask`, `limits`, and `looksCompact` to choose a look,
then `look:<id>` for that one look in full. Never make a name from a word in the text: `easings`
and `presets` are refused, and one wrong name fails the whole call. Never pass `["all"]`, because
the whole document overflows the context; ask for a large section (`effects`, `looks`, `supports`)
in a call of its own. When a call is refused, its error lists the valid names: take the name from
there.

**A tool that replies with a job receipt** has not finished. Pass the receipt's `job` verbatim to
the tool its `tools.jobStatus` names (`picsart_job_status`) until it reports the result; that
result is what the tool returns with `async: false`. A `picsart_generate` job is checked the same
way, and its check also needs the `model` the job was submitted with. Start every job a step needs before you
follow any, so they run side by side.

**A scene can travel by URL.** `picsart_media_patch_scene`, `picsart_media_expand_scene_ref` and
the six `apply_*` tools take `returnSceneUrl: true`: the result then names the edited scene by its
`sceneUrl` instead of carrying it. Pass that URL on as the next call's `scene` where its schema
takes a URL, and as `sceneUrl` to `picsart_scene_editor`. Leave it off when you need to read the
scene yourself, or when the next tool takes only the document.

## The five interactions

| Interaction | When | What happens |
|---|---|---|
| **ASK** | The user must choose | Closed questions with 2–4 options each. Ask everything a step needs in one turn, and never make the user type an answer you have already listed |
| **REVIEW** | The user must see the work before it is final | Open the scene in `picsart_scene_editor` and wait |
| **SHOW** | An image, a video or audio is ready | Show it, with one line on what it is |
| **SPEND** | A call charges credits | Quote it, then get an explicit yes |
| **DELIVER** | The work is approved | Export once and give the file |

### REVIEW

Call `picsart_scene_editor` with `sceneUrl` when you hold the scene as a URL, otherwise with
`scene` set to the scene document itself, as a parsed object, never a string. Before you open it:

- expand every `scene_ref` layer with `picsart_media_expand_scene_ref`;
- make sure every media URL in the scene is Picsart-hosted (see Asset URLs);
- run the use case's check (see Evaluation).

Then end the turn. The editor is free and renders nothing. The user answers in one of three ways:

- **Accept** in the editor, with nothing edited or commented: the reply's `verdict` is `approved`.
  That is the approval.
- **In chat**, saying it is ready: that message is the approval. Where the editor has no Accept
  button, this is the only way to approve.
- **Submit** in the editor, after editing or commenting: the reply's `verdict` is `needs_changes`,
  with `edited`, `documentUrl`, `comments`, `timelineComments` and `duration`.

The reply names their scene by `documentUrl`, a hosted copy of it as they left it. Pass that URL
on, never the document: as `scene` to `picsart_media_patch_scene` and `picsart_media_export`, and
as `sceneUrl` to the editor. Only when that copy could not be stored does the reply carry the scene
itself, as `document`; pass that as `scene` instead.

On `needs_changes`:

- `edited: true` means their scene replaces yours. Make further changes to theirs.
- Each of `comments` is a pin on the picture, with its `instruction` and the moment it is about.
  Each of `timelineComments` is a marked stretch, with its `text` and its `start` and `end`. Apply
  each one there, check again, and open the editor again.
- If both are absent, their edits are the whole answer: never ask what they meant. Check their
  scene and open the editor again on it.
- The reply carries no video. Never say anything was rendered or saved because of it.

On approval, DELIVER the latest document: theirs if they edited it, otherwise yours. If the editor
cannot be shown, follow the fallback in `references/HOST.md`.

### SPEND

A call costs credits when it is `picsart_generate`, or when the tool's description says it charges
credits. Before one:

1. Quote it. For a model, validate the parameters and get the estimate with `picsart_preflight`,
   and read the balance with `picsart_credits`. Never quote a number from memory. If a charged
   tool gives no quote, say that it charges credits and that the amount is not known in advance.
2. Put everything the step needs in one quote, and ask once.
3. Call only after an explicit yes. A yes covers what was quoted, once. Running it again, or
   anything new, needs a new yes.
4. **A batch is one quote and one yes.** Several generations on one model (the sheets of a cast,
   a set of shots, the voice lines of a script) are one `picsart_generate` call each, with the
   same `model`, `resolution` and `folderUid`, all sent in the same turn before you follow any.
   The yes for the batch covers every call in it. Several candidates of ONE prompt are `count` on
   one call, never a call per candidate. Put every job the calls return on one
   `picsart_render_monitor`, each with the `model` it was submitted with and a `label` that names
   its entry (a shot id, an asset tag). The monitor follows them and posts
   `render_monitor_feedback` when all have finished; never ask anyone to wait or check back.

If the user declines, say plainly what the work cannot do without it, and stop that part.
`picsart_media_export`, `picsart_media_contact_sheet`, `picsart_media_validate_scene` and the
scene editor are free.

### DELIVER

Export the approved scene once with `picsart_media_export`, and give the link with one line on
what it is. Only an `async: false` export saves the file to the user's Picsart Drive by itself;
the default receipt's finished result offers the Drive save instead. Either way, say it was saved
only when a result returns a `driveUid`. Then offer one next step in a sentence, and do it only if
the user says yes.

## Asset URLs

- Asset URLs are opaque handles. Show them to the user as links and pass them back into tools
  exactly as returned. Never read a hostname, a path or a query string as meaning anything.
- Never open, download or fetch a video or audio URL yourself: the tools read it. An image is the
  one exception. To look at one yourself (a still sheet, a contact-sheet frame, a generated
  picture, a reference the user brought), open its URL as the host notes say under "Looking at an
  image". Never describe an image you have not looked at. Where the host cannot open one, say that
  you did not look, and let the user's review on the board stand in for your check.
- **Where a URL came from decides what it is, never how it looks.** A URL a Picsart tool returned
  in this conversation (the upload, `picsart_drive`, `picsart_generate`, an export, a still sheet,
  the editor's document) is Picsart-hosted. Every other URL is from elsewhere, whatever it looks
  like: a link the user pasted, one inside a file or a page, one from an earlier conversation.
- A scene opened in REVIEW plays only Picsart-hosted media. The user's own file comes in with
  `picsart_media_upload`. A link from elsewhere is saved first with `picsart_drive`
  (`action: "upload"`, with the link as `url` and a `name`), and the `url` it returns goes into the
  scene. A file the user names in their Picsart Drive is found with `picsart_drive`
  (`action: "list"`); use its `url`, never its `downloadUrl`.

## Preview and export

The live scene is the preview. Export only:

- to DELIVER;
- when the host cannot show the scene, as `references/HOST.md` says;
- when neither a still from `picsart_media_contact_sheet` nor the scene data can answer a question
  you have.

## Evaluation

Check your own work before the user sees it, as the `evaluate` skill says. At most two fix rounds.
After that, go on anyway and tell the user plainly what is still weak. A turn never ends with
nothing to show.

## Voice

Brief and concrete, like a producer. Post one short line before any step that takes more than a
few seconds. Never end a turn without a message the user can read.
