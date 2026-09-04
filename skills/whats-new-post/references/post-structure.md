# Post structure

The shape of the article, and the front matter it needs. Written in terms of the field
**roles** from stage 2 of the skill, never in terms of a particular dataset's key names, so
this holds whether the items are software packages, models, vendors or venues.

## Front matter

| field | rule |
|---|---|
| `slug` | `whats-new-YYYY-MM`, or `-b` suffixed for a second post in one month |
| `kind` | `additions`. Reserved so other post kinds can reuse the same renderer |
| `coversFrom` | Exactly the previous post's `coversUntil`. Windows tile with no gap |
| `coversUntil` | The arrival cut, usually the moment the data was last synced |
| `publishedAt` | Date only, absolute |
| `seo.title` | Under 60 characters. Count first, then what the items are, then the period |
| `seo.description` | 140 to 160 characters, naming 2 or 3 of the most recognisable items |
| `seo.h1` | **Different from the title.** The title competes in a result list, the h1 speaks to someone who already arrived |
| `stats` | Counted from the records. Never carried over from a draft |
| `sources` | Where the data came from and the date each was read |

## The order, and why

1. **`h1`**, then a **lede** of one paragraph.
2. **A counted stats row.** The numbers are what make the rest credible.
3. **`themes`**, 2 or 3.
4. **The entries**, each an `h2`.
5. **The remainder as a table.**
6. **FAQ.**
7. **Provenance note.**

A table of contents goes after the lede whenever there are more than 4 entries. It is what
makes a roundup skimmable, and it is what earns sitelinks in a result page.

## The lede

One paragraph, and it must say **what the period was like**, not what the article contains.

> Eleven arrived, and nine of them are hosted, which is the first window where that has been
> true.

not

> This month we added the following items to the catalogue.

The first gives a reason to keep reading. The second is a heading with a full stop.

## `stats`

A short row of counted figures under the lede. Which figures depends on what roles exist, but
the pattern is: how many, how they divide, and how many clear some bar that matters in this
domain.

Always include the count. Then pick 3 or 4 from: distinct values of the grouping role, how
many have a maker identified, how many are directly usable versus needing installation, how
many carry the standing role above some threshold, how many publish some optional thing.

**Recount these from the records at the end.** A stat carried over from an earlier draft after
the window shifted is the most common factual error in a periodical.

## `themes`

2 or 3 entries of `{heading, body}`, one paragraph each. The only editorialising in the piece,
and the part that carries most of the value when the window is large.

**A theme must be countable against the window.** "Payments is heating up" is a vibe. "Four of
the eleven are payment rails, against none in the previous two windows" is a theme. If you
cannot count it, cut it.

Good themes come from: a grouping value that suddenly moved, a maker appearing for the first
time, several items wrapping the same underlying thing, a shift in how items are distributed,
or a field that used to be empty and now is not.

## The entries

Each is an `h2` carrying the item's own name from the identity role, not a rewrite of it, with
a one line hook underneath saying why this one is in the post. Then a fixed set of `h3`, in
this order, each dropped entirely when its role is missing from the data:

| heading | from role | content |
|---|---|---|
| What it does | summary | 2 to 4 sentences, plain |
| Who makes it | maker | The organisation, what else they do, how to reach them |
| Getting it running | access | The command, endpoint or link, and what it requires |
| Worth knowing | standing, claims, provenance | Bullets, each traceable to a field |

**Keep the `h3` set identical across entries.** A reader scanning ten of them needs the same
shape each time, and a missing section is more informative than a reordered one.

**"Who makes it" is what makes this readable rather than a changelog.** A reader will skim a
list of packages and stop on "made by a four person team who also run the largest Slovenian
legal database". Where the maker role is empty, say so plainly. "The publisher has not put an
organisation behind this, and the namespace is a personal account" is information a reader can
act on. Restating the summary to fill the space is not.

Never infer headcount, funding, location or revenue. If a maker's own page states it, quote and
link it. Otherwise leave it out.

## The remainder table

Everything in the window without a full entry. Name, grouping value, one clause.

**Sort by the standing role, not alphabetically.** The table then degrades gracefully: a reader
who stops a third of the way down has still seen the better documented ones.

**Cap it.** Past roughly 50 rows a table stops being readable and starts being a data dump the
site probably already publishes better elsewhere. Show the top 40 or so and link to the filtered
listing for the rest, saying how many are not shown.

## FAQ

4 to 8 pairs, answering what a reader of a roundup actually asks:

- How often is this published
- What counts as new
- How do I get my thing listed
- Why is X not here
- Does appearing here mean you tested it

The last one matters most, and the answer is almost always no. It belongs in every post.

## Provenance

Where the data came from, and when each source was read. A periodical is exactly where this
gets skipped, and it is exactly where a reader most needs it, because the article is a claim
about a period rather than about a thing.
