---
name: whats-new-post
description: Turn a list of new items into a what's new blog post.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: creative
    tags: [content, blog, changelog, roundup, seo, copywriting]
---

# The what's new post

You are given an array of records that were recently added to something, and you return one
article about them. The records could be software packages, AI models, vendors, job listings,
products, papers or venues. **You do not need to be told which.** You read the data, work out
what it is, and write accordingly.

**The output is a post, not a table.** A table is what the reader could already see. The
article exists to say which of these matter, who is behind them, and what changed about the
whole set. If the honest answer is that nothing in the batch is interesting, say so in one
paragraph and write a short post; padding a thin window is how a periodical loses readers.

## When to Use

Use when someone hands over a list of new items and wants an article rather than a table.

- **Roundups**: "write up what we added this month", "new additions post", "what's new post"
- **Changelogs as prose**: "turn this changelog into a blog post", "release notes article"
- **Launch and batch announcements**: "we just indexed 400 new X, write something"
- **Periodicals**: "the monthly roundup is due", "this window's post"

Also use when handed a JSON array, a JSONL file or a directory of records with no further
explanation, and asked for something publishable.

## Prerequisites

- **An array of records**, as a JSON array, a JSONL file, a directory or glob of per record
  JSON files, or a path plus the name of the field marking when each record arrived.
- **Optionally the previous post**, so the window can start exactly where that one ended.
- Nothing else. The skill profiles whatever it is given and infers the subject.

## How to Run

1. Profile the data before writing a word. Stage 0 below.
2. Say what the items are, in one sentence, and ask if two readings would produce different
   articles.
3. Map the fields onto roles. Stage 2. This is what makes the skill portable.
4. Settle the window, then let the record count decide the article's shape.
5. Write, following `references/post-structure.md` and `references/writing.md`.
6. Verify against the checklist in Verification.

## Quick Reference

| stage | what happens |
|---|---|
| 0 | Profile: counts, keys, types, how universal each field is |
| 1 | Infer what the items are, and say it out loud |
| 2 | Map fields onto roles, not names |
| 3 | Choose the window so it tiles with the previous post |
| 4 | Let the count decide the shape |
| 5 | Write |
| 6 | Verify every claim against a field |

| window size | shape |
|---|---|
| 1 to 3 | One post per item, or a single short piece. No table of contents |
| 4 to 15 | Every item gets a full entry |
| 16 to 60 | 8 to 12 full entries, the rest in a closing table |
| over 60 | 8 to 12 entries, themes carrying most of the value, and a capped table |

## Procedure

### Stage 0: profile before you write a word

Never start from the first record. Start from the shape of all of them.

Report, and keep for later:

- how many records
- every key that appears, and in what share of records
- for each key: the type, and for strings whether it is short like a label, long like prose,
  a URL, a date, or an enum with few distinct values
- which keys are nested, and what the nested shapes hold
- which keys are near-universal and which are rare. **A field present in 4 percent of records
  cannot be a section of every entry**, and finding that out after writing eight entries
  wastes the work

### Stage 1: work out what these things are

State it explicitly before writing. Draw on the key names, the value shapes, the URLs, and 3
or 4 full records read end to end.

Then say it back in one sentence: *"These are 47 Model Context Protocol servers, each a
package or hosted endpoint an AI agent can call, added to a catalogue."* Or *"These are 12
text to video models with duration and resolution specifications."*

**If two readings are plausible and they would produce different articles, ask.** One
question, with your best guess offered as the default. Getting this wrong produces an article
that is fluent and about the wrong subject, which is worse than an awkward one.

### Stage 2: find the roles, not the field names

This is the whole trick of making the skill portable. Do not look for `description`; look for
**the field playing the summary role**. Map what you profiled onto these roles. Any role may
be missing, and a missing role means a section is dropped, never invented.

| role | what it is | commonly called |
|---|---|---|
| identity | what to call the item | `name`, `title`, `label`, `id`, `slug` |
| summary | what it is, in prose | `description`, `summary`, `oneLine`, `whatItDoes`, `abstract` |
| arrival | when we first saw it | `syncedAt`, `addedAt`, `createdAt`, `firstSeen`, `indexedAt` |
| origin | when the thing itself was made or released | `publishedAt`, `releasedOrUpdated`, `version` |
| maker | who is behind it | `author`, `vendor`, `publisher`, `owner`, `company`, `maintainer` |
| access | how a reader gets or tries it | `packages`, `install`, `endpoint`, `url`, `apiDocsUrl`, `pricing` |
| standing | a proxy for how good or complete it is | `score`, `rating`, `stars`, `rank`, `confidence` |
| grouping | how the set divides | `category`, `type`, `kind`, `facet`, `tags` |
| claims | assertions the maker makes about itself | `certifications`, `compliance`, `badges`, `awards` |
| provenance | where the data came from and when it was read | `sourceUrls`, `verifiedAt`, `checkedAt` |

Two roles decide the article's spine:

**arrival is not origin.** New means new to the reader, which is when it entered this dataset,
not when its author first released it. A model published in March that arrived in the data
yesterday belongs in this post. Where only origin exists, say so in the post: the window is
then "released between" rather than "added between", and that is a different and weaker claim.

**standing decides the running order.** Where no standing role exists, rank on completeness:
count the populated fields per record. A record its publisher filled in properly is a better
lead than one with three fields, and that is true in every dataset.

### Stage 3: choose the window and the cut

The window runs from the previous post's end to now, so windows tile with no gap. If there is
a previous post, take its end. If not, ask for a start date or take the earliest arrival.

**Never choose the window by eye.** A gap silently drops records, and the dropped ones are the
obscure ones, which are the ones nobody will notice are missing.

### Stage 4: decide the shape from the count

The number of records decides the article, and getting this wrong is the most common failure.

| window size | shape |
|---|---|
| 1 to 3 | One post per item, or a single short piece. No table of contents |
| 4 to 15 | The standard form: every item gets a full entry |
| 16 to 60 | 8 to 12 full entries, the rest in a closing table |
| over 60 | 8 to 12 full entries, a themes section carrying most of the value, and a table. The article is now about the pattern, and the entries are illustrations of it |

Selecting the full entries: rank by standing, then adjust for **spread across the grouping
role**, for a recognisable maker, and for one or two that are simply odd. A run of eight
entries from one category reads as a mailing list. One genuinely strange item is worth three
competent ones.

### Stage 5: write it

The structure, the required headings and the front matter live in
`references/post-structure.md`. Read it before writing. The house voice and the specific
copywriting moves that make a roundup readable to the end are in `references/writing.md`.

In short: an `h1` that is not the meta title, a lede that says what the period was like, a
counted stats row, 2 or 3 themes, the entries as `h2` with a fixed set of `h3` under each, a
table for the remainder, an FAQ, and a provenance note.

### Stage 6: the rules that will get you into trouble

These hold whatever the data is about.

**Never assert a claim the maker made about itself.** A `claims` role field is a list of
things the vendor's own page says. Write "their security page claims SOC 2" and link it, never
"SOC 2 certified". This is the rule most at risk in marketing copy, because the honest phrasing
is the less punchy one.

**Never imply the data was tested.** Unless a field records a test you ran, the article
describes what publishers published. Say that once, plainly.

**Never invent a reason something exists.** If the summary field says "MCP server for Acme",
that is the whole of what you know. Write that, and say the publisher has not explained the use
case. A composed rationale is the single most damaging thing you can put in this article,
because it is indistinguishable from the true parts.

**Every sentence in an entry traces to a field.** If you cannot point at the field, cut the
sentence. Say what is not known plainly rather than skipping it: "the publisher has not put a
company site behind this" is information.

**A standing score is not quality.** Where you rank on one, say once what it measures and link
its definition if the dataset has one. Ranking by score while implying merit is a
misrepresentation the reader cannot detect.

**Absence is not a finding.** A field nobody filled in means unmeasured, not zero.

## Pitfalls

The failures that ruin this article, whatever the data is about.

- **A composed rationale.** The single most damaging thing you can write. If the summary field
  says "MCP server for Acme", that is all you know. A plausible paragraph about why Acme built
  it is indistinguishable, to a reader, from the parts that are true.
- **Asserting a maker's self description.** Anything from the claims role is what the maker says
  about itself. Write "their security page claims SOC 2" and link it. Never "SOC 2 certified".
- **Implying you tested anything.** Unless a field records a test that ran, the piece describes
  what publishers published. Say so once.
- **Treating a standing score as merit.** Say once what it measures. A documentation score is
  not a quality ranking.
- **Padding a thin window.** A short honest post beats a long inflated one.
- **Absence read as a finding.** An empty field means unmeasured, not zero.

## Verification

Before reporting done:
- Every item referenced resolves to a record in the input.
- Every claim traces to a field. Spot check 5 sentences against the data.
- The counted stats recount from the records, not from an earlier draft.
- The window start equals the previous post's end exactly.
- Every maker claim is attributed and linked.
- Copy rules: no em dashes, no double hyphens, no emoji, no exclamation marks, no "unlock",
  "seamless", "leverage", "dive into", "supercharge", "elevate", "game changer".
- One `h1`. Headings nest without skipping. Every table of contents anchor resolves.
- If the host project has a build and a link checker, run both.
