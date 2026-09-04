# Post structure

## The title

The single highest leverage decision. To most readers the title is the whole post.

```
<Name>: <what it does, plainly> (<the one fact that decides interest>)
```

- Under 120 characters. Reddit allows 300, mobile shows far less.
- **Lead with what it does, not with the fact that it exists.** "New tool released" is
  scrolled past. "Live European power prices across 47 bidding zones, no API key" is opened.
- **Put the deciding fact in the brackets.** It differs by community: `hosted`, `MIT`,
  `self hosted, Docker`, `open weights`, `free tier`, `no telemetry`. Stage 1 tells you which
  one this audience asks first, and that is the one that goes there.
- Follow the subreddit's own convention for a bracketed prefix, such as `[Tool]` or
  `[Project]`, where it has one. Never impose one where it does not.
- No emoji, no clickbait, no exclamation marks. Several programming and AI subreddits
  auto-remove titles containing emoji.
- No score, rank or rating in the title. It reads as self promotion.

## Body sections, in order

Reddit markdown only. Two newlines between blocks, `**bold**`, `>` for quotes, `-` for
bullets, backticks and fences for code. **No tables and no HTML**: old Reddit does not render
tables and a large share of this audience is on old Reddit or a third party client.

Drop any section whose data is missing. Never pad one.

### 1. The maker's own line

The summary role, quoted with `>`, marked as theirs. Never paraphrase it: the paraphrase is
what makes a post read like an ad.

### 2. What it actually does

2 to 4 sentences, in your own plain words, drawing on the record and on what you read in
stage 2. Concrete over abstract. Where there is a feature list, name 3 or 4 real items rather
than characterising them.

### 3. How to run it

The part people scroll to. **Always a fenced block.**

Hosted: the endpoint and the auth type. A package: the real install command with the real
identifier. Both: show both and say which you would try first. Then credentials, and where
nothing is needed, **"no credentials required" belongs on its own line**, because it is the
most persuasive thing available.

### 4. Who makes it

Company, team or one person, from the maker role and the about page if you read one. Where
nothing is published, say so: "no company site, the namespace is a personal account" is
information this audience specifically values. Never infer size, funding or location.

### 5. Licence and repository

Licence, language, activity, open issue count. **Reddit cares about licence more than any
other audience**, so it is never omitted when known, and its absence is stated. A repository
that does not exist, or whose last release is old, is a finding and goes here.

### 6. What this community asked first

The section that makes the post land rather than merely be accurate. Stage 1 named the
community's first question; answer it here, explicitly, under a heading in their vocabulary.
Docker and resource use for self hosters. Benchmarks and weight licensing for ML. Threat
model and credential handling for security.

If you cannot answer it from the record or the research, **say that it is not documented**.
That is a useful answer and an honest one.

### 7. The honest caveats

Non negotiable, and what earns the post its credibility:

- You have not run it. No testing, no audit, no calling the service.
- Anything the maker says about itself is a claim, with a link.
- Any inferred label is inferred, and says so.
- Any score measures what it measures, in one clause, once.
- Figures were read on a date, and that date is stated.

### 8. One link

One, at the end, plainly labelled. **One.** Repeated links to your own property is the
fastest route to a spam filter and a moderator ban.

## Length

800 to 1,600 characters of body for a typical item. Up to 2,500 where there is genuinely a
repository, a licence, a maker and a real feature list. Below about 500 there is not enough
here to justify a post: skip it and let a roundup cover it instead.
