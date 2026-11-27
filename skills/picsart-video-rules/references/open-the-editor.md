# Open the editor

Read before every `picsart_scene_editor` call.

What the scene is decides the tools the user gets in the editor. Pass them every time, and never
leave the editor to guess from the scene:

| The scene | Call with | The user gets |
|---|---|---|
| A cut of footage (an edit, a reel, clips, a screen video) | `purpose: "video"` | every video tool: trim, split, speed, volume, text, captions and the rest |
| A motion design (an animated design, a logo reveal) | `purpose: "motion"` | move and resize any element, add an image |
| A character check (a new character in action) | `tools: []` | comments only: pins on the picture and marked stretches, no editing |
| An animated film's review rounds (a cartoon, an explainer) | `tools: ["comments", "trim", "delete", "add_shot"]` | comments, trim and delete a shot, and Add shot for a shot that is missing |

`tools` keeps only the tools it lists. `tools: []` is the only way to open a review the user
cannot edit: tell the user in one line that this view is for comments.

`comments` never takes a tool away. `comments: "all"` is the default, pins on the picture and
marked stretches; `comments: "timeline"` keeps the marked stretches only.

Add shot answers with `plannedShots` in the reply: each is an empty slot in the user's scene, with
a `description` of what should happen in it and its length. Make that shot the way the use case
makes its other shots (a built scene in an animated film, a generated video in a cut of footage),
put it in its slot, and open the editor again.
