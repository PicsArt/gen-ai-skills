# Host notes: Claude

How this host performs the five interactions in `video-core`.

| Interaction | How |
|---|---|
| **ASK** | The host's own question tool, so the options show as buttons the user taps: `AskUserQuestion` in Claude Code, and in the Claude apps (claude.ai, the desktop and mobile apps, Cowork) the tool they offer for tappable options. Up to 4 questions per call, 2–4 options each; the tool adds an "Other" answer itself. Only when the host offers no such tool: one message with numbered options |
| **REVIEW** | The scene editor board the use case names. Where the app draws it, the user reviews there. The decision and the fallback are below |
| **SHOW** | The URL as a Markdown link, with one line on what it is |
| **SPEND** | The quote in text, then ASK with "Yes, go ahead" and "No" |
| **DELIVER** | `picsart_media_export`, then the link |

## What a board sends back

The scene editor and the other Picsart boards (the ones with a Lock, Approve or Send button) send
the user's decision as widget context, not inside the chat message. When the user's message
announces a decision ("sent it back", "locked", "approved"), read it before you reply: if a
`read_widget_context` tool is available, call it; otherwise it is in the message. Never ask the
user to repeat, re-click, describe or paste it. Only if neither carries it, say so in one line and
ASK the one thing you need, with the options the board offered. A board's first tool result is a
preview, never an approval.

The editor's approval comes as its `approved` verdict (the Accept button) or as a chat message.

## When a board is not drawn

If a board other than the editor errors twice, or the user says they cannot see it, carry its
decision in text: show what the board would have shown (the pictures as links, the shot list as a
table, the candidates with their trade-offs), then ASK with the board's own choices.
The gate still holds; only the surface changes.

## When the editor is not drawn

The Claude Code terminal may not draw the editor. If the call errors twice, or the user says they
cannot see it:

1. export a preview of the scene with `picsart_media_export` and give its link;
2. show the frames from `picsart_media_contact_sheet` at the moments the use case checks;
3. ASK: "Approve" or "Change something".

A preview exported here is a draft. Export the approved version again to DELIVER.

## Looking at an image

Save the image to a file in the session's scratch directory with the `Bash` tool
(`curl -sL -o <file> "<url>"`), then open the file with the `Read` tool, which shows it to you.
One file per image. Open only images this way, never a video or audio file.

## Running a skill's script

A skill's text says to run `python3 scripts/<name>.py`. Run it with the `Bash` tool, from the
skill's own folder: the base directory Claude Code names when it loads the skill. Pass the input as
a file in the session's scratch or working directory, not inline.

If `python3` is missing, say so in one line and stop. On a Mac without Apple's command line tools,
`python3` offers to install them. Tell the user what it is, and wait for them.

## When the upload is not drawn

If the user says they cannot see the upload, ask for a link to the file or the name of a file in
their Picsart Drive, and bring it in as video-core's Asset URLs say. A file that is only on their
computer can come in only through the upload; say so plainly.
