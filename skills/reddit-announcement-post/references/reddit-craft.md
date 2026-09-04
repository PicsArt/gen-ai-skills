# Reddit craft

## Hashtags, honestly

**Reddit does not use hashtags and inline tags read as spam.** Do not scatter `#opensource`
through prose. The real equivalents:

- **Post flair.** The actual mechanism, and per subreddit. Read the subreddit's flair list and
  pick from it rather than guessing.
- **A bracketed title prefix** where the subreddit's own convention uses one.
- **At most one short tag line at the very end**, on its own line, two or three tags, and only
  where the subreddit tolerates it. Default to omitting it entirely.
- **Never tag a company or product you are not.**

## If the copy is being posted automatically

These apply to a scheduled job, not to a person pasting once. Where the caller has not said
which it is, assume a person and note the assumption.

- **Disclose it.** One line at the bottom. Required by some subreddits, honest everywhere,
  and this audience punishes discovering it later far more than being told up front.
- **Self promotion ratios accumulate over an account, not over a post.** An account posting
  only links to one domain gets shadowbanned however good each post is. That is a scheduling
  and account-behaviour problem, and no amount of copy quality solves it.
- **Deduplicate before calling.** This skill cannot see what has already been posted.
- **Cap and space the posts.** Flooding is what gets an app banned rather than a post removed.

A person posting by hand needs none of the above, and should not be handed a disclosure line
claiming they are a bot.

## What gets a post removed

- **Self promotion ratios.** Most technical subreddits enforce one. An account posting only
  links to a single domain gets shadowbanned regardless of how good the content is.
- **Rules differ per subreddit and change.** Read them each time. Some ban bots outright,
  some require flair, some require automation disclosure, some ban link posts entirely.
- **Never post the same body to several subreddits.** Identical text across communities is
  detectable and reads as spam. Rewrite the opening and the community question section for
  each one, or post to one.

## Voice

- Plain, specific, unexcited. The facts carry the interest, so the prose does not have to.
- **No em dashes, no double hyphens, no emoji in prose, no exclamation marks.**
- Banned because they describe nothing: unlock, seamless, leverage, dive into, supercharge,
  elevate, game changer, revolutionise, blazing fast, battle tested.
- Numbers as digits. Dates absolute.
- **A claim from the data beats any adjective.** "The only one here with a hosted endpoint and
  no credentials" is more persuasive than "incredibly easy to try".
- Say what is not known plainly. "The licence is not stated anywhere I could find" is a
  sentence, and a useful one.

## What ruins it

**A composed rationale.** If the summary says "MCP server for Acme", that is the whole of what
you know. A plausible paragraph about why Acme built it is indistinguishable to a reader from
the parts that are true, and it contaminates the whole post.

**Marketing prose lifted from the maker's site.** Stage 2 is research, not sourcing copy. The
moment a sentence sounds like a landing page, it is doing damage.

**Answering a question the community did not ask.** A licence deep dive in a design subreddit
is padding. Stage 1 exists so this does not happen.

**Implying you tested it.** You did not. Saying so once makes the whole post more trustworthy,
not less.

**Burying the install.** If someone has to hunt for how to run it, the post failed at its one
job.
