# Film — outages

## When a tool or endpoint is down

Outages happen (a connector drops i2i while t2i works, a widget tool is
missing from the session). They are **status, not decisions**: report the
outage in one line, keep the conveyor moving on everything free and working
(reviews, descriptors, checklists, planning), park the blocked items in
`openDecisions` with a retry note, and retry quietly next turn. Do **not**
turn an outage into a user choice when the pipeline's own rules already answer
it — "redraw the lead's variant from scratch, or wait for i2i?" is not a
question, because taking consistency debt on a face to dodge a temporary
outage is exactly what the rules forbid. Offer a genuine workaround decision
only when both paths are actually defensible.

The rules that stop thrash loops (repeated retries, silent waits, an invented
diagnosis):

- **Running out of credits gets ZERO retries.** An
  explicit insufficient-credits or insufficient-balance response from any
  Picsart tool is not a transient failure. Do not resubmit it, switch models, or
  substitute another charged operation. Preserve `film.json`, its job handles,
  and the current scene or asset state, and set `blocked_on` to
  `Picsart credits for <the paused operation>`.

  When the error returns a plan or credit link, share it exactly as given so
  they can subscribe or buy more credits; never open a browser for them. Say
  which operation is paused and continue only after the user says their credits
  are available; never poll their balance or retry automatically.
- **Every failure has either a NAMED substitute or none.** Named substitutes
  are sanctioned in the skills (t2i when i2i is down is NOT one for a lead's
  variant; the markdown fallback when a board tool is absent IS one; the
  by-ear path when transcription is absent IS one). If no substitute is
  named, there isn't one — do not invent a workaround chain to keep moving.
- **Other critical-component failures retry ONCE, then stop and hand it back.** The tools
  the pipeline cannot run without (`picsart_generate`, the job status poll,
  the export) get one identical retry; a second failure is the user's news,
  in one plain line: what you tried to do, what blocked it, what you need.
  Never reword-and-refire, never sleep-and-loop, never diagnose beyond what
  the error actually says.
- **An authentication error gets ZERO retries.** The call was refused before
  any work started: nothing was charged and no job exists to recover, and an
  identical payload can only be refused again. Tell the user in one line that
  the Picsart connection did not carry their sign-in on that call, which
  operation is paused, and that it continues once the connection is working.
  Do not claim their session expired, and do not treat visible credits as proof
  that generation works (`picsart_credits` can keep answering while every
  generation fails).

  The one useful probe is `picsart_job_status` on a known job handle: if it is
  refused too, the connection is the problem, not that one call.
- **Track it in `film.json`**: `blocked_on` names the ONE missing thing
  (or `none`), and `attempts` counts per tool+failure so the once-only retry
  is enforced by bookkeeping, not memory.
