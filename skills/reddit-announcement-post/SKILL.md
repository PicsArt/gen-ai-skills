---
name: reddit-announcement-post
description: Turn one record into Reddit post copy.
version: 2.0.0
author: Picsart
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: creative
    tags: [reddit, social, announcement, copywriting, community, research]
---

# Record to Reddit post

One record in, post copy out. **You are not told what the thing is, which community it
belongs to, or what that community cares about.** You work all three out, then read the pages
the record points at, and only then write.

**You produce copy. You do not deliver it.** The result may be pasted into Reddit by a person,
submitted by a scheduled job, queued for review, put in a newsletter or thrown away. None of
that changes what you return, and none of it is your concern. Do not assume a bot, do not
assume automation, and never submit anything yourself.

**Reddit is not a blog and not a press release.** The audience is technical, allergic to
marketing, and will downvote a promotional tone faster than they will read past the title.
The craft is packing genuine detail into a form that does not read as an ad.

Unlike `whats-new-post`, which covers many items shallowly, this covers **one item as
completely as the data and a short research pass allow**, because a reader who opens a post
about a tool wants to decide whether to use it without leaving the thread.

## When to Use

Use when given data about one thing and asked for something postable to Reddit.

- "write a Reddit post about this", "post this to r/X", "announce this on Reddit"
- A record plus a subreddit, or a record and no subreddit at all
- A scheduled job that needs post copy per item
- A person who will paste the result by hand

Do not use for a digest of several items. That is `whats-new-post`.

## Prerequisites

- **One record**, any shape. It is profiled rather than assumed.
- **The URLs in that record**, which are the research surface. A record with no links yields a
  thinner post and a lower `confidence`.
- **The target subreddit's rules and flair list**, read per subreddit, every time.
- **Whether the copy will be posted automatically or by a person.** It changes whether an
  automation disclosure belongs in the body. Ask if not stated.

## How to Run

1. Profile the record onto roles.
2. Classify the thing, name the subreddit, and name that community's first question.
3. Read the pages the record links to. Take facts, not copy.
4. Write, following `references/post-structure.md` and `references/reddit-craft.md`.
5. Return the object described below. Do not post anything.

## Quick Reference

| stage | what happens |
|---|---|
| 0 | Profile the record onto roles |
| 1 | Classify it, choose the subreddit, name its first question |
| 2 | Research the linked pages |
| 3 | Write |
| 4 | Verify every sentence against a field or a page |

## Procedure

### What you return

A single object. Every consumer reads the same shape, whether that is a person copying two
fields out of it or a job posting it unattended.

```jsonc
{
  "title": "under 120 characters, no emoji",
  "body": "Reddit markdown. No tables, no HTML",
  "subreddit": "the single best fit, without the r/ prefix",
  "alternatives": ["other plausible subreddits, best first"],
  "flair": "the flair to set, taken from that subreddit's own list, or null",
  "titlePrefix": "[Tool], or null where the subreddit has no such convention",
  "communityQuestion": "the first thing this audience asks, and where in the body it is answered",
  "sources": [ { "url": "...", "readAt": "2026-09-04", "took": "licence, install steps" } ],
  "confidence": "high | partial | thin",
  "gaps": ["what could not be established, in plain words"],
  "skip": false,
  "skipReason": null
}
```

Three fields do real work and are the reason this is an object rather than a string:

**`skip`.** Some records should not become posts, and saying so is a valid and useful result.
Set it when the body would come in under about 500 characters, when the summary is missing or
unusable, when research contradicts the record in a way you cannot resolve, or when nothing
distinguishes the item enough to be worth a stranger's attention. **A skipped record with a
reason is a better outcome than a thin post.**

**`sources`.** Every claim that came from a page you read, with the date. A figure read today
may be wrong next month, and the consumer may be publishing weeks later.

**`gaps`** and **`confidence`.** What you could not establish. A consumer showing this to a
person can surface it; a consumer publishing unattended can refuse on `thin`.

Return the object and stop. Do not also print a "ready to paste" version, do not wrap it in
commentary, and do not offer to post it.

### Stage 0: profile the record

Same discipline as `whats-new-post`, and deliberately the same role names so a reader moving
between the two skills does not have to relearn them. Do not look for `description`; look for
the field playing the **summary role**.

| role | what it is |
|---|---|
| identity | what to call it |
| summary | what it is, in prose |
| maker | who is behind it |
| access | how a reader gets or runs it |
| standing | a proxy for how complete or well regarded it is |
| grouping | how its category divides |
| claims | assertions the maker makes about itself |
| provenance | where the data came from and when it was read |
| links | every URL in the record. **This is the research surface** |

Any role may be missing. A missing role drops a section; it never licenses inventing one.

### Stage 1: classify it, and decide where it belongs

Say all of this out loud before writing:

1. **What kind of thing is it.** A library, a hosted service, a CLI, a model, a dataset, a
   game, a paper, a piece of hardware. This decides the whole shape of the post.
2. **Who would install or use it**, concretely. Not "developers".
3. **Which subreddits it belongs in**, and which single one is the best fit. Name them.
4. **What that community cares about**, which is the part most often skipped and matters most.

The fourth point is the whole reason to classify. The same record produces a different post
per community, because different audiences ask different first questions:

| community shape | what they ask first |
|---|---|
| General programming | Licence, language, what it depends on, why not just a script |
| Self hosting and homelab | Docker or not, resource use, does it phone home, data locality |
| Machine learning | Benchmarks, reproducibility, weights and their licence, training data |
| Security | Threat model, what it trusts, credential handling, disclosure history |
| A specific product's community | How it fits the thing they already run, and what breaks |
| Data and open data | Provenance, licence, update cadence, format, gaps |
| Design and creative | What the output actually looks like, cost per use |

**If you cannot name the subreddit and its first question, do not write the post.** Ask.

### Stage 2: research before writing

The record is a starting point, not the material. It is usually one or two sentences of
description plus some URLs, and a post built on that alone reads thin because it is thin.

**Fetch the pages the record points at**, in this order, and stop when you have enough:

| fetch | what to take |
|---|---|
| The repository | Licence as stated in the repo, language, activity, a real feature list, install steps that actually work, open issues that reveal limitations |
| The project or docs site | What it is for in the maker's own words, supported platforms, requirements |
| The pricing page | Whether it is free, and what the free tier really allows. Reddit asks this immediately |
| The maker's about page | Whether this is a company, a team or one person. Never infer size from anything else |
| A changelog or releases page | How alive it is. "Last released 14 months ago" is material |

Rules for this stage, and they matter more than the fetching:

- **Read for facts, not for copy.** Never lift a sentence of marketing prose. You are there
  for the licence, the requirements, the price and the limitations.
- **Record what you read and when.** Every claim that came from a page carries that page as
  its source, and a figure read today may be wrong next month.
- **A page that does not load is a finding.** A dead documentation link or a 404 repository is
  worth a line in the post, because it is exactly what a reader wants to know.
- **Do not fetch anything the record does not link to.** No searching for the maker, no
  guessing at a repository URL. If the record does not point at it, it is not part of this.
- **Never connect to a service to test it.** Reading a public page is research; calling an API
  or an endpoint to see what it does is testing, and this post does not test anything.
- **Be polite.** A handful of requests, spaced. This is somebody's server.

**Stop and reassess if the research contradicts the record.** A record saying "free" against a
pricing page saying otherwise is not a detail to smooth over. Say both, and which you read
where.

### Stage 3: write it

The title, the section order, the Reddit markdown constraints and the length targets are in
`references/post-structure.md`. The voice, and the specific things that get a post removed or
downvoted, are in `references/reddit-craft.md`. Read both before writing.

In short: a title that leads with what the thing does; the maker's own one line quoted; what
it actually does; **how to run it, in a fenced block, always**; who makes it; licence and
repository; what this specific community asked about first; the honest caveats; one link.

## Pitfalls

- **A composed rationale.** If the summary is one sentence, that is all you know. A plausible
  paragraph about why it was built is indistinguishable from the true parts.
- **Marketing prose lifted from the maker's site.** Stage 2 is research, not sourcing copy.
- **Answering a question the community did not ask.** A licence deep dive in a design
  subreddit is padding.
- **Implying you tested it.** You did not. Saying so once makes the post more trustworthy.
- **Burying the install.** If a reader has to hunt for how to run it, the post failed.
- **Assuming a bot.** The copy may be pasted by a person, and handing them a disclosure line
  claiming they are automated is wrong.
- **Padding rather than skipping.** A skipped record with a reason beats a thin post.

## Verification

- Every sentence traces to a field or to a page you actually read. Cut anything else.
- Every researched claim carries its source and the date read.
- The subreddit is named, its first question is answered in the post, and its rules were read.
- Exactly one link to your own property, at the end.
- The install block holds a real command or URL, never a placeholder.
- Claims from the maker are phrased as claims, with links.
- No emoji in the title. No inline hashtags in prose.
- No em dashes, no double hyphens, no exclamation marks, no marketing adjectives.
- The automation disclosure line is present **only if the caller said the post will be
  submitted automatically**. A person pasting this by hand should not be made to claim they
  are a bot, and a bot should never omit it. When the caller has not said, ask, or leave it
  out and note it in `gaps`.
- It renders on old Reddit: no tables, no HTML.
