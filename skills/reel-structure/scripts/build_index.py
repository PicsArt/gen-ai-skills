"""Write the style index from the style files: one short line per style.

    python3 scripts/build_index.py            # rewrite references/style-index.md
    python3 scripts/build_index.py --check    # exit 1 when the index is out of date

Every `styles/<id>.md` gets one line: its id, group, media and item range, subjects,
occasions, moods and the first vibe words, kept under LINE_MAX characters so the whole index stays
small enough to read every time. The agent reads the index; it opens only the picked style's file.
"""
from __future__ import annotations

import glob
import os
import re
import sys
from typing import Dict, List

HERE = os.path.dirname(os.path.abspath(__file__))
REFS = os.path.join(os.path.dirname(HERE), "references")
INDEX = os.path.join(REFS, "style-index.md")
LINE_MAX = 110
INDEX_MAX = 25_000
HEAD = """# Style index

One line per style, written by `scripts/build_index.py` from the skill's `styles/<id>.md`; don't edit by hand.
Each line: id · group · media items · subjects · occasions · moods · vibe. `+2` counts the words left
out (the style's file has them); `+any` means it also takes any subject or occasion. All styles are
available to `scripts/pick_style.py` as style-library.md says. The sections record whether an agent
build has proven the style; this does not restrict selection. Open only `styles/<id>.md`.

"""


def fields(path: str) -> Dict[str, str]:
    text = open(path, encoding="utf-8").read()
    found = dict(re.findall(r"^\| ([A-Z][a-z ]+?) \| (.+?) \|$", text, re.M))
    ident = re.search(r"^- ID: (\S+)", text, re.M)
    found["id"] = ident.group(1) if ident else ""
    found["generative"] = "yes" if re.match(r"\s*<!-- generative:file -->", text) else ""
    return found


def words(part: str, most: int) -> str:
    """The first few words of a Fit list; the rest counted (+2), and +any when it takes any."""
    items = [w.strip() for w in part.split(",")]
    named = [w for w in items if w != "any"]
    if not named:
        return "any"
    more = f" +{len(named) - most}" if len(named) > most else ""
    return ", ".join(named[:most]) + more + (" +any" if "any" in items else "")


def line(f: Dict[str, str]) -> str:
    slots, media, subjects, occasions, moods = [p.strip() for p in f["Fit"].split(";")]
    for most in ((3, 2, 2), (2, 1, 1), (1, 1, 1)):  # fewer Fit words until the line fits
        head = (f"- {f['id']} · {f['Group']} · {media} {slots[6:]} · {words(subjects, most[0])} · "
                f"{words(occasions, most[1])} · {words(moods, most[2])} · ")
        if len(head) + 8 <= LINE_MAX:
            break
    vibe = ""
    for w in [w.strip() for w in f.get("Vibe", "").split(",")]:
        if len(head) + len(vibe) + len(w) + 2 > LINE_MAX:
            break
        vibe += (", " if vibe else "") + w
    return head + vibe if vibe else head[:-3]


def fenced(f: Dict[str, str], text: str) -> str:
    """A style whose file is generative-only gets its index line fenced the same way (generative:start/end)."""
    if not f.get("generative"):
        return text
    return "<!-- generative:start -->\n" + text + "\n<!-- generative:end -->"


def proven(f: Dict[str, str]) -> bool:
    return f.get("Proven", "").startswith("yes")


def render() -> str:
    styles = [fields(p) for p in sorted(glob.glob(os.path.join(os.path.dirname(REFS), "styles", "*.md")))]
    sections = []
    for title, status in (("Proven", True), ("Not yet proven", False)):
        lines = [fenced(f, line(f)) for f in styles if proven(f) == status]
        sections.append(f"## {title} ({len(lines)})\n\n" + "\n".join(lines) + "\n")
    return HEAD + "\n".join(sections)


if __name__ == "__main__":
    new = render()
    if "--check" in sys.argv:
        current = open(INDEX, encoding="utf-8").read() if os.path.isfile(INDEX) else ""
        sys.exit(0 if current == new else 1)
    open(INDEX, "w", encoding="utf-8").write(new)
    print(new.count("\n- "), "styles indexed,", len(new.encode()), "bytes")
