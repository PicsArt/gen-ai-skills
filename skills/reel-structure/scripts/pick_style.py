"""Rank the style library's styles for one request, free and local.

    python3 scripts/pick_style.py read.json [--library FILE ...]

read.json is the agent's free read of the request, as the style library's "Picking the style" says:

    {"words": ["cute"], "photos": 1, "clips": 3, "subject": "pet", "occasion": "everyday",
     "moods": ["cute", "playful", "warm"], "place": ""}

`words` are the look, mood, subject and occasion words the user said, in their spelling; `subject`,
`occasion` and `moods` come from the footage. Prints the ranking as JSON, best first, with why each
style fits; an empty ranking means no style takes this many items, or none that does keeps the user's
mood word: say so and ask, as the library says. `--exclude` leaves out the styles already tried,
oldest first, and moves to a group not tried yet (or the one tried longest ago), so "try another
style" looks different.

All styles are eligible. Each ranking row retains its `proven` status: an agent build's validation
history, not a selection restriction.

The Vibe set (`set` in the output) is the ranking's first four: the pick, then the next three "try another style" builds.
The set is kept varied: at most one Text-led style, and at least two styles from other groups, one of
them motion-led (MOTION_GROUPS). The pick is always the best fit; the rest of the set follows the
ranking where the rules allow, and fills from the other fitting styles when the user's words leave too few;
when no fitting style may fill a place, the set is shorter.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from typing import Dict, List

HERE = os.path.dirname(os.path.abspath(__file__))
REFS = os.path.join(os.path.dirname(HERE), "references")

SPELLINGS = {"cozy": "cosy", "color": "colour", "selfies": "selfie", "pets": "pet", "dog": "pet", "dogs": "pet",
             "puppy": "pet", "cat": "pet", "cats": "pet", "travel": "trip", "vacation": "trip", "holidays": "holiday",
             "journey": "trip", "nightout": "night out", "party": "party", "parties": "party", "concerts": "concert",
             "everyday life": "everyday", "daily": "everyday", "day in my life": "everyday", "film": "film",
             "movie": "cinematic", "funny": "funny", "romance": "romantic", "aesthetics": "aesthetic"}
# A mood the user asked for that no fitting style names is met by its neighbours.
NEIGHBOURS = {"cute": ["playful", "fun", "warm", "friendly"], "playful": ["fun", "cute", "funny"],
              "fun": ["playful", "upbeat", "energetic"], "funny": ["playful", "fun"],
              "cosy": ["warm", "calm"], "warm": ["cosy", "nostalgic"], "calm": ["cosy", "dreamy", "minimal"],
              "cinematic": ["moody", "epic", "emotional"], "moody": ["cinematic"], "dreamy": ["calm", "romantic"],
              "energetic": ["upbeat", "bold", "fun"], "upbeat": ["energetic", "fun"], "romantic": ["warm", "dreamy"],
              "epic": ["wow", "cinematic"], "wow": ["epic", "bold"], "stylish": ["aesthetic", "minimal"],
              "aesthetic": ["stylish", "dreamy"], "nostalgic": ["warm", "emotional"],
              "festive": ["upbeat", "fun", "warm"]}
# Everyday footage reads bright and calm: never a moody style unless the user's words name it.
EVERYDAY_OUT = {"moody"}
DEFAULT_MOODS = ["calm", "warm"]
# The Vibe set: the ranking's first SET_SIZE styles.
SET_SIZE = 4
TEXT_GROUP = "Text-led"
MOTION_GROUPS = {"Cards and frames", "Grids and collages", "Fast cuts", "Transitions and speed", "Strips and swipes"}
# A style with any of these moods is never picked for the user's mood word.
OPPOSITES = {w: ["moody", "cinematic", "epic", "emotional"] for w in ("cute", "playful", "fun", "funny", "friendly")}
OPPOSITES.update({w: ["energetic", "bold", "epic"] for w in ("calm", "cosy", "dreamy", "minimal")})
OPPOSITES.update({w: ["calm", "cosy", "minimal"] for w in ("energetic", "upbeat", "bold")})
OPPOSITES.update({"moody": ["cute", "playful", "funny", "festive"], "cinematic": ["cute", "funny"], "festive": ["moody"]})


# Words that end in -s without being a plural: never cut to a different word ("news" is not "new").
NOT_PLURAL = {"news", "series", "species", "lens", "canvas", "chaos", "atlas", "cosmos", "always", "perhaps",
              "yes", "this", "his", "its", "was", "has", "does", "goes", "plus", "alias", "christmas", "thanks"}


def singulars(w: str) -> List[str]:
    """The singulars a plural-looking word may have, none for a word that only ends in -s (glass, bus, news)."""
    if w in NOT_PLURAL or len(w) < 4 or w.endswith(("ss", "us", "is", "ous")):
        return []
    return ([w[:-3] + "y"] if w.endswith("ies") else []) + ([w[:-2]] if w.endswith("es") else []) + ([w[:-1]] if w.endswith("s") else [])


def norm(word: str) -> str:
    """The word in the library's spelling, one form for a singular and its plural: an exact Fit-list word
    stays; else its singular or plural that a Fit list uses ("places" is the subject place; "friend" is the
    occasion friends); else the singular the styles' words have ("grids" is grid), so both forms match the
    same styles. A word is only ever cut to its own singular, and only to a word the library knows."""
    w = word.strip().lower()
    w = SPELLINGS.get(w, w)
    if w in FIT_WORDS:
        return w
    plurals = [] if w.endswith("s") and singulars(w) else [w + "s", w + "es"]
    for form in singulars(w) + [p for p in plurals if w in singulars(p)]:
        if form in FIT_WORDS:
            return form
    for form in singulars(w):
        if form in ALL_WORDS:
            return form
    return w


# The words of the styles' Fit lists (subjects, occasions, moods), and those plus the words of
# their name, Looks like and Vibe.
FIT_WORDS: set = set()
ALL_WORDS: set = set()


def entries(path: str) -> List[Dict]:
    text = open(path, encoding="utf-8").read()
    out = []
    for block in re.split(r"\n### ", "\n" + text)[1:]:
        name, body = block.split("\n", 1)
        fields = dict(re.findall(r"^\| ([A-Z][a-z ]+?) \| (.+?) \|$", body, re.M))
        ident = re.search(r"^- ID: (\S+)", body, re.M)
        if not ident or "Fit" not in fields:
            continue
        slots, media, subjects, occasions, moods = [p.strip() for p in fields["Fit"].split(";")]
        lo, _, hi = slots[6:].partition("–")
        out.append(dict(id=ident.group(1), name=name.strip(), group=fields.get("Group", ""), lo=int(lo),
                        proven=fields.get("Proven", "").startswith("yes"),
                        hi=int(hi or lo), media=media, subjects=[s.strip().lower() for s in subjects.split(",")],
                        occasions=[s.strip().lower() for s in occasions.split(",")],
                        moods=[s.strip().lower() for s in moods.split(",")],
                        text=" ".join([name, fields.get("Looks like", ""), fields.get("Vibe", "")]).lower()))
    return out


def library(extra: List[str]) -> List[Dict]:
    files = [os.path.join(REFS, "style-library.md")] + sorted(glob.glob(os.path.join(os.path.dirname(REFS), "styles", "*.md"))) + extra
    styles = [s for f in files if os.path.isfile(f) for s in entries(f)]
    for s in styles:
        FIT_WORDS.update(s["moods"] + s["occasions"] + s["subjects"])
        ALL_WORDS.update(s["moods"] + s["occasions"] + s["subjects"] + re.findall(r"[a-z]+", s["text"]))
    return styles


def named(style: Dict, word: str) -> bool:
    """The style's name, Looks like or Vibe says the word: what the style is about."""
    forms = [word] + [p for p in (word + "s", word + "es", word[:-1] + "ies") if word in singulars(p)]
    return re.search(r"\b(?:" + "|".join(map(re.escape, forms)) + r")\b", style["text"]) is not None


def says(style: Dict, word: str) -> bool:
    """The style's name, Looks like, Vibe or Fit names the word."""
    return word in style["moods"] + style["occasions"] + style["subjects"] or named(style, word)


def tidy(read: Dict) -> Dict:
    """The read's subject and occasion in the Fit lists' spelling: "Thanksgiving" and "thanksgiving" are one occasion."""
    return dict(read, subject=norm(read.get("subject") or ""), occasion=norm(read.get("occasion") or ""))


def fits(style: Dict, read: Dict) -> List[str]:
    """Why the style can't take this footage; empty when it fits."""
    read = tidy(read)
    n, photos, clips = read["photos"] + read["clips"], read["photos"], read["clips"]
    why = []
    if n < style["lo"]:
        why.append(f"needs at least {style['lo']} items, has {n}")
    if n > style["hi"] + style["hi"] // 3:
        why.append(f"takes at most {style['hi'] + style['hi'] // 3} items, has {n}")
    if style["media"] == "photos" and clips or style["media"] == "clips" and photos:
        why.append(f"takes {style['media']} only")
    if read.get("subject") and read["subject"] not in style["subjects"] and "any" not in style["subjects"]:
        why.append(f"subject {read['subject']} not in {style['subjects']}")
    if read.get("occasion") and read["occasion"] not in style["occasions"] and "any" not in style["occasions"]:
        why.append(f"occasion {read['occasion']} not in {style['occasions']}")
    return why


def read_words(read: Dict) -> List[str]:
    words = [norm(w) for w in read.get("words", [])]
    return words + ["trip"] if read.get("place") else words


def read_moods(read: Dict) -> List[str]:
    """The footage's moods; with none read, everyday's bright and calm."""
    return [norm(m) for m in read.get("moods", [])] or DEFAULT_MOODS


def clash(style: Dict, read: Dict) -> str:
    """Why the style's mood rules it out: the user's mood word, or a moody style for everyday footage the user didn't name it for.

    The footage's own moods only score; they never rule a style out, so one mood word can't flip the pick."""
    words, moods = read_words(read), read_moods(read)
    for w in words:
        if set(OPPOSITES.get(w, [])) & set(style["moods"]):
            return f"its mood clashes with the user's word '{w}'"
    if not any(named(style, w) for w in words):
        if "everyday" in words + [read.get("occasion")] and EVERYDAY_OUT & set(style["moods"]):
            return "everyday footage is never given a moody style"
    return ""


def rank(styles: List[Dict], read: Dict) -> List[Dict]:
    read = tidy(read)
    words = read_words(read)
    moods = read_moods(read)
    fitting = [s for s in styles if not fits(s, read) and not clash(s, read)]
    if not fitting:  # never a plain slideshow: the styles that take this count and media, whatever their subjects and occasions
        fitting = [s for s in styles if not fits(s, dict(read, subject="", occasion="")) and not clash(s, read)]
    scored = []
    for order, s in enumerate(fitting):
        hits = [w for w in words if says(s, w)]
        near = [w for w in words if w not in hits and any(says(s, x) for x in NEIGHBOURS.get(w, []))]
        strong = [w for w in hits if named(s, w)]
        occ = read.get("occasion") in s["occasions"] and read.get("occasion") != "any"
        made_for = occ and "any" not in s["occasions"]
        sub = read.get("subject") in s["subjects"]
        mood_hits = [m for m in moods if m in s["moods"]]
        # A mood counts by the share of the style's own moods it takes, so a style that lists many moods
        # (a broad Fit) never outranks one made for the footage's mood just by listing more.
        share = len(mood_hits) / max(1, len(s["moods"]))
        mood_fit = len([m for m in moods if {m, *NEIGHBOURS.get(m, [])} & set(s["moods"])]) / max(1, len(s["moods"]))
        score = 3 * len(strong) + len(hits) + 2 * len(near) + 2 * occ + made_for + sub + round(len(mood_hits) * share, 2)
        scored.append(dict(id=s["id"], name=s["name"], group=s["group"], proven=s.get("proven", False), score=score, order=order, words=hits, named=strong, made_for=made_for,
                           near=near, occasion=occ, subject=sub, moods=mood_hits, mood_fit=round(mood_fit, 2)))
    # a tie goes to the style whose moods sit closest to the media's (its own or a neighbour), never to the item count
    scored.sort(key=lambda x: (-x["score"], -x["mood_fit"], x["order"]))
    if any(x["words"] for x in scored):  # the user's own words are a filter, not a bonus
        best = max(len(x["words"]) for x in scored)
        kept = [x for x in scored if len(x["words"]) == best]
    elif any(x["near"] for x in scored):
        best = max(len(x["near"]) for x in scored)
        kept = [x for x in scored if len(x["near"]) == best]
    else:
        kept = scored
    # the rest only fill the Vibe set when the kept styles can't keep it varied
    return kept + [dict(x, filler=True) for x in scored if x not in kept]


def varied(ranking: List[Dict]) -> List[Dict]:
    """The ranking with its first SET_SIZE kept varied: the pick first, then each next style the rules
    allow (at most one Text-led; at least two from other groups, one of them motion-led). A filler (a
    style the user's words left out) joins the set only when none of the user's styles may; when no
    fitting style may, the set stays shorter and the rest follow it. Each of the set's styles carries
    `set: true`."""
    if not ranking:
        return ranking
    chosen, rest = [ranking[0]], ranking[1:]

    def need(group_list: List[str]) -> int:
        other = [g for g in group_list if g != TEXT_GROUP]
        return max(0 if any(g in MOTION_GROUPS for g in group_list) else 1, 2 - len(other))

    def allowed(x: Dict) -> bool:
        groups = [c["group"] for c in chosen] + [x["group"]]
        if x["group"] == TEXT_GROUP and groups.count(TEXT_GROUP) > 1:
            return False
        return need(groups) <= SET_SIZE - len(groups)

    while len(chosen) < SET_SIZE and rest:
        own = [x for x in rest if not x.get("filler")]
        pick = next((x for x in own if allowed(x)), None) or next((x for x in rest if allowed(x)), None)
        if pick is None:  # no fitting style meets the rules: the set stays shorter
            break
        chosen.append(pick)
        rest.remove(pick)
    return [dict(x, set=True) for x in chosen] + [x for x in rest if not x.get("filler")]


def another(ranking: List[Dict], tried_groups: List[str]) -> List[Dict]:
    """After styles were tried, a group not tried yet comes first, then the one tried longest ago.

    tried_groups is the tried styles' groups, oldest first. A filler stays behind the user's own styles."""
    last = {g: i for i, g in enumerate(tried_groups)}
    return sorted(ranking, key=lambda x: (bool(x.get("filler")), last.get(x["group"], -1)))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("read")
    ap.add_argument("--library", nargs="*", default=[])
    ap.add_argument("--exclude", nargs="*", default=[], help="style ids already tried (the record's stylesTried)")
    a = ap.parse_args()
    read = json.load(open(a.read, encoding="utf-8"))
    every = library(a.library)
    groups = {s["id"]: s["group"] for s in every}
    styles = [s for s in every if s["id"] not in a.exclude]
    # rank() already drops the subject and occasion when nothing fits; the user's mood words always hold
    ranking = varied(another(rank(styles, read), [groups[i] for i in a.exclude if i in groups]))
    read = tidy(read)
    json.dump({"pick": ranking[0]["id"] if ranking else None, "set": [x["id"] for x in ranking if x.get("set")],
               "ranking": ranking[:8],
               "unfit": {s["id"]: fits(s, read) or [clash(s, read)] for s in styles if fits(s, read) or clash(s, read)}},
              sys.stdout, indent=1)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
