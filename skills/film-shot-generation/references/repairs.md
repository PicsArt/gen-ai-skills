# Repairs: edit, extend, or re-roll

Route a note by what it means, not by its words.

| The user wants | Route |
|---|---|
| Something already in the clip to play differently: a performance, an object, the light, a marked stretch | **Edit** |
| The same seconds to hold a different event | **Edit** |
| Something new after the clip's last frame, or more seconds | **Extend** |
| The whole run changed: its cut count, its cast or its light throughout; or "regenerate", "a new take" | **Re-roll the run** |

A marked stretch is usually an edit; a clip picked for a new event is usually an extend. When the
note truly supports both, flag it as ambiguous and name the two routes.

## Diagnose before you route

Most defects in a take are one missing clause. Find it before choosing the route, and fix only it:

| Defect in the take | Almost always |
|---|---|
| The camera drifts, or nothing happens | No camera move named, so the model invented one |
| It plays like a slideshow | Only the camera moves; the subject's motion was never named |
| Extra limbs or fingers | More people than the shot's seconds can hold, or no stated action for the hands |
| Melted hands | The hands do something unnamed: name the action, or frame them out |
| A distorted face | The face is too small in frame to resolve: go closer |
| Morphs mid-clip | The action does not fit the seconds: one action, or a longer shot (the user's) |
| Uninvited people or objects | The background was never described: describe it, even as an empty room |
| Changes between shots | A voice line, a geography line or the style line was retyped: restore it verbatim |
| The last word is cut off | The line runs too close to the cut: shorten it or move it earlier, then re-roll; no edit puts a word back |

**A shot that keeps misfiring is stripped back**: freeze the camera, simplify the action, get it
right, then add one element back at a time. Keep every line that worked verbatim.

**A shot you know is hard** (a transformation, a mechanism, a crowd, a colour that drifts) names its
likely failure and a fallback before it is generated, so the first take already carries the guard: a
drifting colour is restated at each moment it appears.

## Edit

The film's edit model (the chosen model's edit sibling). Send the clip, **only the change**, with the
shot id and its seconds, the run's same numbered references and the same audio flag. Never
re-describe the whole shot. Compile with `kind: "edit"` and verify as for any prompt.

## Extend

The film's extend model. Send the clip and only what happens next, as a new block, with the
references by number if the model's schema takes them. Read the schema with `picsart_model_params`
first; never assume a field exists.

**Before the quote**, probe every input clip with `picsart_media_probe` and check the extend
model's input limits (a shortest input, a longest sum). The duration asked for is the new part, not
the whole. For a seam repair that must show the next run, attach a short excerpt of its opening,
exported and probed, never the whole run.

## Re-roll

A fresh take of the whole run. Change one header line or one block, keep the rest, and quote the
whole run. A camera-only correction changes exactly that shot's camera value and carries a
full-size frame of the old take as that cut's `FRAME REFERENCE`; a note that changes the camera and
something else is an ordinary re-roll.

## For all three

- **Each is its own quote and its own yes.**
- Each is compiled and verified on its own literal arguments.
- An edit that fails twice is not tried a third time the same way: re-roll, or simplify the shot.
- The result is split at its real cuts and put back into the review timeline. An edit replaces its
  piece of the run; an extend appends one. Keep every superseded file in the record with its call,
  its prompt version, the change and the verdict.
