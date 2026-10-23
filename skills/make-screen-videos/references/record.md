# The project record

The set's state, kept as picsart-video-rules's project record says, as `screen-video.json` where the host
gives files. Update it at every gate. On resume, read it before saying where things stand.

```json
{
  "recordings": [{ "uri": "<as a Picsart tool returned it>", "name": "chat-filmmaking.mov", "moments": "<kept as returned, or a note that they were read>" }],
  "brief": {
    "said": { "destination": "Instagram Reels", "kind": "how-to", "audience": "people new to Picsart", "data": "demo" },
    "read": { "topics": 5, "brand": { "accent": "#7b2ff7" }, "speech": false },
    "assumed": { "length": 20, "language": "en", "ending": "Try it in Picsart" },
    "message": "Making a film with AI is easy"
  },
  "plan": { "firstLook": "stills", "line": "stills of short 1 in three styles → short 1 → the other four → music", "pass": 2, "of": 4 },
  "style": { "id": "paper-ink", "brand": { "accent": "#7b2ff7" } },
  "screens": { "choice": "recreate", "failing": ["shot-cards"], "steps": ["s2", "s3"] },
  "videos": [
    { "id": "storyboard", "title": "Storyboard a film in one chat", "learns": "turn one idea into six scenes", "from": 12.4, "to": 61.0, "status": "approved", "draft": 2, "scene": "<documentUrl>" }
  ],
  "openDecisions": []
}
```

- `brief` keeps what the user said, what you read and what you assumed apart, as picsart-video-rules's
  Asking says. An assumption moves to `said` when the user confirms it.
- `screens` is "The screens": `recreate`, `keep` or `mix`, the moments `readability.py`
  failed, and the steps drawn as designed UI.
- `plan` is stage 5's agreement: what the user sees first, the passes in one line, and where you
  are.
- `videos[].status` is `planned`, `built`, `in review`, `approved` or `delivered`; `scene` is the
  latest document's URL, the user's if they edited it.
