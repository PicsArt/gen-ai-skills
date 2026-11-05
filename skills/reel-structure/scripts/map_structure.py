#!/usr/bin/env python3
"""Fit the user's script rows to a reference's beats.

    python3 scripts/map_structure.py sheet.json script.md [--spans allowed-spans.json]
                                     [--length 45] [--out mapping.json]

`sheet` is the structure sheet (JSON, or a Markdown breakdown sheet.py parses). `script` is the
user's script: a Markdown table with a Time column (and a Beat column when the writer named the
beats), or JSON rows [{"id", "start", "end", "beat", "voice", "on_screen", "fixed"}].

Which beat a row takes:
1. The first row opens on the reference's first beat when that beat is a hook.
2. A row whose Beat names a beat of the sheet (hook, stake, joke run, a name of the sheet's own)
   takes the next beat of that name, never one before the previous row's.
3. A time range on the reference's clock in the row's Beat ("F1 36–54 s", with the sheet's id)
   carries the row forward over each later beat that range mostly covers.
4. An unnamed row (empty Beat) between two rows of the same beat joins it; any other unnamed row is added:
   it is ours, and kept. When no row is named at all, each row after the hook takes the beat its
   middle falls in, on the reference's clock scaled to the script's.

Consecutive sheet rows with the same beat name are one beat here: its time runs from the first
row's start to the last row's end, and `sheet_rows` lists the rows it joins.

Lengths: each beat (beats one row spans count as one) gets the reference's share of the mapped
script, scaled to the rows that copy beats (or to `--length`, less the added rows). Rows inside
an allowed span, or marked `fixed`, keep their length and are placed first; the others scale by
at most 15 %. A beat whose rows then land within 15 % of its share matches; otherwise it is
changed, with the reason. A beat no row takes is dropped. No row is ever dropped.

Prints the mapping as JSON. Exits 0 when every row and beat fits, 1 when any beat is changed,
dropped or any row added, 2 for bad input. Standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any, Dict, List, Optional, Set

import sheet as sheets

Json = Dict[str, Any]
# Each beat's length may differ from its share of the reference by this fraction.
TOLERANCE = 0.15
# A reference time range carries a row over a beat when it covers at least this much of it.
COVER = 0.5


def read_script(value: Any) -> List[Json]:
    """Script rows with id, start, end, beat, voice, on_screen and fixed."""
    markdown = isinstance(value, str)
    if markdown:
        rows, _, _ = sheets.read_rows(value)
    elif isinstance(value, dict) and isinstance(value.get("rows"), list):
        rows = value["rows"]
    elif isinstance(value, list):
        rows = value
    else:
        raise sheets.InputError("the script must be a Markdown table with a Time column or a list of rows")
    out = []
    for n, row in enumerate(rows, 1):
        if (not isinstance(row, dict) or not sheets.finite(row.get("start"))
                or not sheets.finite(row.get("end")) or not 0 <= row["start"] < row["end"]):
            raise sheets.InputError(f"script row {n} needs numeric 0 <= start < end")
        if markdown and row.get("picture"):
            picture = sheets.plain(row["picture"])
            voice, screen = ("?", "?") if sheets.unknown(picture) else sheets.split_quotes(picture)
            if "voice" not in row:
                row["voice"] = voice
            if not row.get("on_screen"):
                row["on_screen"] = screen
        if markdown and row.get("voice"):
            row["voice"] = re.sub(r"<br\s*/?>", " ", row["voice"], flags=re.I)
        if markdown and row.get("on_screen"):
            row["on_screen"] = re.sub(r"<br\s*/?>", "\n", row["on_screen"], flags=re.I)
        out.append({"id": str(row.get("id") or n), "start": float(row["start"]), "end": float(row["end"]),
                    "beat": sheets.plain(str(row.get("beat") or "")),
                    "voice": str(row.get("voice") or ""), "on_screen": str(row.get("on_screen") or ""),
                    "fixed": bool(row.get("fixed"))})
    if not out:
        raise sheets.InputError("the script has no rows")
    return out


def mark_fixed(rows: List[Json], spans: Any) -> None:
    """Rows that overlap an allowed span keep their length."""
    if spans is None:
        return
    if not isinstance(spans, list):
        raise sheets.InputError("allowed spans must be a list of {start, end, file, reason}")
    for n, span in enumerate(spans, 1):
        if not isinstance(span, dict) or not sheets.finite(span.get("start")) or not sheets.finite(span.get("end")):
            raise sheets.InputError(f"allowed span {n} needs numeric start and end")
        for row in rows:
            if row["start"] < span["end"] and row["end"] > span["start"]:
                row["fixed"] = True


def reference_range(label: str, ident: Optional[str]):
    if not ident:
        return None
    match = re.search(r"\b" + re.escape(ident) + r"\b[^()\d]*?(" + sheets.NUMBER + r")\s*[–—-]\s*("
                      + sheets.NUMBER + r")\s*s\b", label)
    return (float(match.group(1)), float(match.group(2))) if match else None


def covered(beat: Json, span) -> bool:
    inside = min(beat["end"], span[1]) - max(beat["start"], span[0])
    return inside >= COVER * (beat["end"] - beat["start"]) - 1e-9


def assign(rows: List[Json], beats: List[Json], ident: Optional[str]) -> None:
    own = tuple(sorted({r for b in beats for r in b["roles"] if r not in sheets.ROLES}))
    pointer, claimed = 0, -1
    for n, row in enumerate(rows):
        row["beats"] = []
        if n == 0 and "hook" in beats[0]["roles"]:
            row["beats"] = [0]
        names = [] if sheets.unknown(row["beat"]) else sheets.beat_roles(row["beat"], own)
        span = reference_range(row["beat"], ident)
        named = [j for j in range(pointer, len(beats)) if set(beats[j]["roles"]) & set(names)]
        # A time range tells repeated names apart: the first beat of the name that it covers.
        complete = next((j for j in named if set(names) <= set(beats[j]["roles"])), None)
        fresh = [j for j in named if j > claimed]
        # A row that continues the beat it is on stays there, e.g. a split reveal, rather
        # than jumping over an unclaimed beat to a later one with the same name.
        continues = (claimed in named and set(names) <= set(beats[claimed]["roles"])
                     and bool(fresh) and fresh[0] > claimed + 1)
        if fresh and not continues:
            # An earlier contiguous run of unclaimed beats that holds every name comes
            # before a later superset.
            run = set(beats[fresh[0]]["roles"])
            for j in range(fresh[0] + 1, len(beats)):
                if not set(beats[j]["roles"]) & (set(names) - set(beats[fresh[0]]["roles"])):
                    break
                run |= set(beats[j]["roles"])
            if set(names) <= run:
                complete = fresh[0]
        first = next((j for j in named if span and covered(beats[j], span)),
                     complete if complete is not None else (named[0] if named else None))
        if first is None and span:
            first = next((j for j in range(pointer, len(beats)) if covered(beats[j], span)), None)
        if row["beats"]:
            first = row["beats"][0]
            # An opener labelled for another reference still anchors only the hook.
            if "hook" not in names and not span:
                names = []
        if first is None:
            continue
        chosen = [first]
        for j in range(first + 1, len(beats)):
            if (span and covered(beats[j], span)) or set(beats[j]["roles"]) & set(names) - set(beats[first]["roles"]):
                chosen.append(j)
            else:
                break
        row["beats"] = chosen
        pointer = claimed = chosen[-1]
    if not any(r["beats"] for r in rows[1:]) and not any(r["beat"] and not sheets.unknown(r["beat"]) for r in rows):
        # Nothing is named: each row takes the beat its middle falls in, on a scaled clock.
        scale = (rows[-1]["end"] - rows[0]["start"]) / (beats[-1]["end"] - beats[0]["start"])
        for row in rows[1:] if rows[0]["beats"] else rows:
            middle = beats[0]["start"] + ((row["start"] + row["end"]) / 2 - rows[0]["start"]) / scale
            # Containment wins over merely touching a beat at its end boundary.
            row["beats"] = [min(range(len(beats)), key=lambda j: (
                (0, 0.0) if beats[j]["start"] <= middle < beats[j]["end"]
                else (1, min(abs(middle - beats[j]["start"]), abs(middle - beats[j]["end"])))))]
        return
    for n, row in enumerate(rows):
        if row["beats"] or (row["beat"] and not sheets.unknown(row["beat"])):
            continue  # a row that names its beat and found none is added, never absorbed
        before = next((r["beats"] for r in reversed(rows[:n]) if r["beats"]), None)
        after = next((r["beats"] for r in rows[n + 1:] if r["beats"]), None)
        if before and after and before[-1] == after[0]:
            row["beats"] = [before[-1]]


def groups_of(rows: List[Json], count: int) -> List[List[int]]:
    """Beats joined by a row that spans them, as runs of beat indexes."""
    parent = list(range(count))

    def root(i: int) -> int:
        while parent[i] != i:
            i = parent[i]
        return i
    for row in rows:
        for a, b in zip(row["beats"], row["beats"][1:]):
            parent[root(b)] = root(a)
    found: Dict[int, List[int]] = {}
    for i in range(count):
        found.setdefault(root(i), []).append(i)
    return sorted(found.values())


def length(row: Json) -> float:
    return row["end"] - row["start"]


def fit(sheet: Json, rows: List[Json], target: Optional[float] = None, tol: float = TOLERANCE) -> Json:
    # Consecutive rows of one name are one beat here (sheet.merge_beats).
    beats = sheets.merge_beats(sheets.timed(sheet)["beats"])
    assign(rows, beats, sheet.get("id"))
    groups = groups_of(rows, len(beats))
    members = {tuple(g): [r for r in rows if r["beats"] and r["beats"][0] in g] for g in groups}
    span = {tuple(g): beats[g[-1]]["end"] - beats[g[0]]["start"] for g in groups}
    used = [tuple(g) for g in groups if members[tuple(g)]]
    added = [r for r in rows if not r["beats"]]
    mapped_total = sum(length(r) for g in used for r in members[g])
    if target is not None:
        mapped_total = target - sum(length(r) for r in added)
        if mapped_total <= 0:
            raise sheets.InputError("--length leaves no time for the rows that copy beats")
    reference_total = sum(span[g] for g in used)
    scale = mapped_total / reference_total if reference_total else 0.0
    factors: Dict[int, float] = {}
    out_beats = []
    for g in groups:
        key = tuple(g)
        mine = members[key]
        share = span[key] * scale
        natural = sum(length(r) for r in mine)
        fixed = sum(length(r) for r in mine if r["fixed"])
        stretch = natural - fixed
        factor = 1.0
        if stretch > 0:
            factor = min(1 + tol, max(1 - tol, (share - fixed) / stretch))
        for r in mine:
            factors[id(r)] = 1.0 if r["fixed"] else factor
        planned = fixed + stretch * factor
        deviation = planned / share - 1 if share > 0 else 0.0
        if not mine:
            status, reason = "dropped", "no row of the script takes this beat"
        elif abs(deviation) <= tol + 1e-9:
            status, reason = "matched", ""
        else:
            status = "changed"
            reason = (f"length {planned:.1f} s against its share {share:.1f} s "
                      f"({deviation:+.1%}), outside ±{tol:.0%}")
            if fixed > share * (1 + tol):
                reason += f"; the allowed span alone is {fixed:.1f} s and is never stretched"
        for i in g:
            out_beats.append({"index": i + 1, "beat": beats[i]["beat"] or " + ".join(beats[i]["roles"]),
                              "sheet_rows": beats[i]["rows"], "soft": beats[i]["soft"],
                              "roles": beats[i]["roles"], "start": beats[i]["start"], "end": beats[i]["end"],
                              "rows": [r["id"] for r in mine], "status": status, "reason": reason,
                              "share": round(share, 2), "natural": round(natural, 2),
                              "planned": round(planned, 2), "deviation": round(deviation, 3),
                              "joined": [j + 1 for j in g] if len(g) > 1 else []})
    clock, out_rows = rows[0]["start"], []
    for r in rows:
        planned = length(r) * factors.get(id(r), 1.0)
        out_rows.append({"id": r["id"], "start": r["start"], "end": r["end"],
                         "planned_start": round(clock, 2), "planned_end": round(clock + planned, 2),
                         "beats": [j + 1 for j in r["beats"]], "fixed": r["fixed"],
                         "status": "mapped" if r["beats"] else "added",
                         "reason": "" if r["beats"] else "names no beat of the reference: it is ours, and kept",
                         "beat": r["beat"], "voice": r["voice"], "on_screen": r["on_screen"]})
        clock += planned
    return {"reference": sheet.get("id") or sheet.get("title") or "", "scale": round(scale, 4),
            "tolerance": tol, "beats": out_beats, "rows": out_rows,
            "added": [r["id"] for r in out_rows if r["status"] == "added"],
            "dropped": [b["index"] for b in out_beats if b["status"] == "dropped"],
            "length": round(clock - rows[0]["start"], 2)}


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("sheet")
    parser.add_argument("script")
    parser.add_argument("--spans", help="allowed-spans.json: a list of {start, end, file, reason}")
    parser.add_argument("--length", type=float, help="the target length in seconds")
    parser.add_argument("--out")
    args = parser.parse_args(argv)
    try:
        sheet = sheets.load_sheet(args.sheet)
        if args.script.lower().endswith(".json"):
            script = sheets.load_json(args.script)
        else:
            with open(args.script, encoding="utf-8-sig") as handle:
                script = handle.read()
        rows = read_script(script)
        mark_fixed(rows, sheets.load_json(args.spans) if args.spans else None)
        mapping = fit(sheet, rows, args.length)
    except (OSError, sheets.InputError) as exc:
        print("error: " + " ".join(str(exc).splitlines()), file=sys.stderr)
        return 2
    sheets.emit(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n", args.out)
    unsettled = mapping["added"] or mapping["dropped"] or any(b["status"] != "matched" for b in mapping["beats"])
    return 1 if unsettled else 0


if __name__ == "__main__":
    sys.exit(main())
