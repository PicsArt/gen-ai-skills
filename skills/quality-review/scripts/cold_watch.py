#!/usr/bin/env python3
"""
The cold watch's arithmetic: the pieces a draft is watched in, every call to the three viewers, and
the gap list the comparer's marks make. The viewers and the comparer are models the caller runs;
this script writes what they are sent and reads what they answer.

    python3 scripts/cold_watch.py input.json
    python3 scripts/cold_watch.py < input.json

The input is one JSON object whose `step` is `plan`, `round` or `gaps`; `track` is the viewer
track's text (references/cold-watch.md has its format). Times are seconds.

`plan`: `{"step": "plan", "track": "...", "duration": 30.5}`. Prints `{ok, track, packets, seal,
errors}`: the track as `{premise, must_know: [{id, by, text}], must_not: [...], questions: [{id,
question, answer}]}`; `packets`, the pieces the draft is watched in, `[{packet, t0, t1}]` (none
without a `duration`); `seal`, a sha256 of the track's text with its line ends and trailing spaces
made alike; and `errors`, a line for each rule the track breaks: 4 to 8 must-knows, 1 to 3
must-not-thinks, 3 to 6 questions, ids in order, a `By` above 0 and within the video, no empty
cell, a premise of at most 120 words.

`round`: the watch, one round of calls at a time. The input:

    {"step": "round", "track": "...",
     "personas": [{"id": "v1", "text": "...", "model": "..."}, ...three],
     "video": {"duration": 30.5, "fps": 4, "frames": ["https://..."], "transcript": {...},
               "voices": [{"start": 0, "end": 4.2, "voice": "Mira"}]},
     "replies": [{"viewer": "v1", "packet": 1, "text": "{...}"}, {"viewer": "v1", "packet": "end", ...}],
     "short": false, "promo": false, "cuts": false}

- `video`: the draft's image-sequence `frames` (frame `i` is at `i / fps` s) and `transcript` as
  `picsart_media_transcribe` returned it (the whole result, its `transcript`, or `{segments}`);
  `voices`, the draft's voice lines, name the voices when diarization merged them. In place of
  `video`, `rows` watches on paper: `[{"t0": 0, "t1": 2, "seen": "...", "heard": "...",
  "on_screen": "..."}]`, each row a piece told in words and carrying no picture.
- `replies`: each model reply as it came, by viewer and `packet` (the piece's number, or `"end"`).
- `short`, `promo` and `cuts` add the questions a short, a promo and an edit of footage ask.

It prints `{ok, done, packets, calls, unreadable, errors}`. `calls` is each viewer's next call,
`{viewer, model, packet, t0, t1, imageUrls, prompt, retry}` (the end has no `t0`, `t1` or
`imageUrls`); send each verbatim and add its reply to `replies`. A reply that is not a JSON object
is asked again once (`retry`), then named in `unreadable`. When `done` it also prints `accounts`,
`asked`, `jumps` and `comparer`, the prompt for whoever marks the accounts against the track.

`gaps`: the same input with `marks`, the comparer's reply (as text, or as the object) `{"marks":
[{"id": "K1", "viewer": "v1", "mark": "carried", "quote": "..."}], "final_misread": {"v1": false},
"unplanned": [{"t": 6.0, "question": "...", "viewers": ["v1"], "quote": "..."}]}`. A mark is
`carried`, `missed`, `misread` or `wondering` for a must-know, `thought` or `clear` for a
must-not-think; every one but `missed` and `clear` needs a quote from that viewer's own words. A
must-know is hit when a viewer's words carry it by the end of the first piece that ends after its
`By`. Prints `{ok, problems, gaps, must_not, asked, jumps, unplanned, fixes, floor, markdown}`; with
a problem, only `{ok, problems, retry_prompt}`: send `retry_prompt` to the same worker once.

Input it cannot read (not JSON, a missing or wrong-typed field, an unknown `step`) exits 1, with
one line on stderr that says what is wrong. Input that is readable but breaks a rule prints
`ok: false` with `errors` or `problems` and exits 0.

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
import re
import sys
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple

SYSTEM = ('You are a member of the public watching a short video on your phone. You know only what you are shown. '
          'Answer only with the JSON object asked for.')

# The pieces: 0, 1.5, 3, 6, then every 3 s; a last piece under TAIL_MIN joins the one before.
HEAD_BOUNDS = (0.0, 1.5, 3.0, 6.0)
EVERY = 3.0
TAIL_MIN = 1.0
SHORTEST = 1.5
# A piece's frames: 4 a second up to FAST_UNTIL, then 2 a second; at most FRAME_MAX.
FAST_STEP, SLOW_STEP, FAST_UNTIL, FRAME_MAX = 0.25, 0.5, 3.0, 8
PAUSE = 0.4
VOICE_REACH = 1.0
PROMPT_MAX = 7000
LIMIT, LIMIT_EXTRA = 40, 60
PREMISE_MAX = 120
NEED = 2
TOLERANCE = 1e-9

NO_ANSWER = '(no answer)'
CUT = '(earlier notes cut)'
NONE_YET = '(none yet)'
NOTE_KEYS = ('happening', 'who', 'expect', 'unclear')
NOTE_KEYS_SHORT = ('happening', 'unclear')
MEANS_NOTHING = {'', 'nothing', 'none', 'no', 'n/a', NO_ANSWER, 'nothing yet', 'nothing much'}
TRAILING = ' \t\r\n.,;:!?…'

K_MARKS = ('carried', 'missed', 'misread', 'wondering')
X_MARKS = ('thought', 'clear')
QUOTED = ('carried', 'misread', 'wondering', 'thought')
ROW_KEYS = ('t0', 't1', 'seen', 'heard', 'on_screen')

HEADERS = {('k', 'by', 'the viewer should know'): 'K', ('x', 'by', 'the viewer must not think'): 'X',
           ('q', 'question', 'answer'): 'Q'}
COUNTS = {'K': (4, 8), 'X': (1, 3), 'Q': (3, 6)}
TABLE_NAMES = {'K': ('must-knows', '| K | By | The viewer should know |'),
               'X': ('must-not-thinks', '| X | By | The viewer must not think |'),
               'Q': ('questions', '| Q | Question | Answer |')}
SEPARATOR = re.compile(r':?-+:?')
BY = re.compile(r'(\d+(?:\.\d*)?|\.\d+)\s*s?', re.IGNORECASE)
PREMISE = re.compile(r'\s*\*{0,2}premise\*{0,2}\s*:\s*\*{0,2}\s*(.*?)\s*', re.IGNORECASE)
CELL_BREAK = re.compile(r'(?<!\\)\|')
PLACEHOLDER = re.compile(r'\{(\w+)\}')
QUOTE_MARKS = str.maketrans({'‘': "'", '’': "'", '‚': "'", '‛': "'", 'ʼ': "'", '′': "'",
                             '“': '"', '”': '"', '„': '"', '‟': '"', '″': '"'})

EXTRA_SHORT = ', "keep_watching": "yes, maybe or no, and why", "ad": "does it feel like an ad: no, a bit or yes"'
EXTRA_CUTS = ', "jump": "a cut in these seconds that felt like a jump or too fast, and why, or nothing"'
EXTRA_END = ', "could_do": "yes, maybe or no", "keep": "save, send, both or neither"'
SHORT_LINES = ('4. Could you do it now? Yes, maybe or no.', '5. Would you save it, send it to someone, both, or neither?')
PROMO_LINES = ('4. Would you try it? Yes, maybe or no.', SHORT_LINES[1])
END_VIDEO = 'You just watched a short video, a few seconds at a time. These are your own notes from each piece, in order:'
END_PAPER = 'Someone just described a short video to you, one moment at a time. These are your own notes from each moment, in order:'

VIDEO_PIECE = '''{system}

{persona}

You're scrolling short videos on your phone, and one starts to play. You see it a few seconds at a time, in order; you can't go back or skip ahead.

Now playing: {t0} to {t1} seconds. The pictures are this piece's frames, in time order: {times} s.
{heard}

Your own notes from the earlier pieces:
{notes}

Say, as yourself and in plain words, what you make of it so far. Use only what you saw and heard. "Don't know" is a good answer. At most {limit} words in all.
Reply with only this JSON object:
{"happening": "what is happening now", "who": "who the people are, as far as you can tell", "expect": "what you expect next", "unclear": "what you don't get, or nothing"{extra}}'''

PAPER_PIECE = '''{system}

{persona}

Someone is describing a short phone video to you, one moment at a time, exactly as it would look and sound. You can't go back or skip ahead.

Moment {packet} ({t0} to {t1} seconds):
{text}

Your own notes from the earlier moments:
{notes}

Say, as yourself and in plain words, what you make of it so far. Use only what you were told. "Don't know" is a good answer. At most {limit} words in all.
Reply with only this JSON object:
{"happening": "what is happening now", "who": "who the people are, as far as you can tell", "expect": "what you expect next", "unclear": "what you don't get, or nothing"{extra}}'''

END_PROMPT = '''{system}

{persona}

{intro}
{notes}

It has ended. Answer as yourself, in plain words. "Don't know" is a good answer.
1. Tell a friend what it was about, in two sentences.
2. Where would you have scrolled away, and why? Give the second, or "never".
3. Answer these questions about it:
{questions}
Reply with only this JSON object:
{"friend": "two sentences", "scroll_away": {"at": "second or never", "why": "why"}, "answers": {answers}{extra}}'''

RETRY = '\n\nYour last reply had these problems. Return the whole object again with them fixed:\n'
USAGE = 'usage: cold_watch.py [input.json]; with no file, the input is read from stdin'


class InputError(Exception):
    """Input that cannot be read at all: the script exits 1 with the reason."""


@dataclass
class Word:
    text: str
    start: float
    end: float
    seg: int
    speaker: Optional[str]
    voice: Any = None

    @property
    def mid(self) -> float:
        return (self.start + self.end) / 2


@dataclass
class Video:
    fps: float
    frames: List[str]
    words: List[Word]
    names: Dict[Any, str]


@dataclass
class Watch:
    track_text: str
    track: Dict[str, Any]
    personas: List[Dict[str, str]]
    replies: List[Dict[str, Any]]
    short: bool
    promo: bool
    cuts: bool
    pieces: List[Tuple[float, float]]
    video: Optional[Video]
    rows: Optional[List[Dict[str, Any]]]

    @property
    def duration(self) -> float:
        return self.pieces[-1][1]


@dataclass
class Walk:
    viewer: str
    done: List[Tuple[Any, Optional[Dict[str, Any]]]]
    due: Any
    retry: bool


# --- Reading the input ------------------------------------------------------------------------


def _num(v: Any) -> bool:
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return False
    try:
        return math.isfinite(v)
    except OverflowError:
        return False


def need(ok: bool, message: str) -> None:
    if not ok:
        raise InputError(message)


def as_dict(v: Any, where: str) -> Dict[str, Any]:
    need(isinstance(v, dict), f'{where} must be an object')
    return v


def as_list(v: Any, where: str) -> List[Any]:
    need(isinstance(v, list), f'{where} must be a list')
    return v


def as_str(v: Any, where: str) -> str:
    need(isinstance(v, str), f'{where} must be text')
    return v


def as_num(v: Any, where: str) -> float:
    need(_num(v), f'{where} must be a number')
    return float(v)


def as_flag(data: Dict[str, Any], key: str) -> bool:
    v = data.get(key, False)
    need(isinstance(v, bool), f'{key} must be true or false')
    return v


def tm(x: float) -> str:
    """A time in a prompt or a note: 0.0, 1.5, 31.25."""
    return str(round(float(x), 2))


def tm2(x: float) -> str:
    return f'{x:.2f}'


def collapse(s: str) -> str:
    return ' '.join(s.split())


def join_and(items: List[str]) -> str:
    if len(items) < 2:
        return ''.join(items)
    return ', '.join(items[:-1]) + ' and ' + items[-1]


def fill(template: str, **values: str) -> str:
    """Each `{name}` in one pass, so a persona's own braces are never filled again."""
    return PLACEHOLDER.sub(lambda m: values.get(m.group(1), m.group(0)), template)


# --- The track ----------------------------------------------------------------------------------


def seal(text: str) -> str:
    lines = text.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    return hashlib.sha256('\n'.join(line.rstrip() for line in lines).encode('utf-8', 'surrogatepass')).hexdigest()


def cells(line: str) -> List[str]:
    s = line.strip()
    s = s[1:] if s.startswith('|') else s
    if s.endswith('|') and not s.endswith('\\|'):
        s = s[:-1]
    return [c.replace('\\|', '|').strip() for c in CELL_BREAK.split(s)]


def table_blocks(lines: List[str]) -> List[List[List[str]]]:
    """Every run of lines that start with a pipe, as its rows of cells."""
    blocks, run = [], []
    for line in lines + ['']:
        if line.strip().startswith('|'):
            run.append(cells(line))
        elif run:
            blocks.append(run)
            run = []
    return blocks


def read_premise(lines: List[str]) -> Optional[str]:
    for i, line in enumerate(lines):
        found = PREMISE.fullmatch(line)
        if not found:
            continue
        parts = [found.group(1)] if found.group(1) else []
        j = i + 1
        while not parts and j < len(lines) and not lines[j].strip():
            j += 1
        while j < len(lines) and lines[j].strip() and not lines[j].lstrip().startswith(('|', '#')):
            parts.append(lines[j].strip())
            j += 1
        return ' '.join(parts)
    return None


def read_by(cell: str, label: str, duration: Optional[float], errors: List[str]) -> Optional[float]:
    if not cell:
        errors.append(f'{label}: By is empty')
        return None
    found = BY.fullmatch(cell)
    by = float(found.group(1)) if found else 0.0
    if by <= 0:
        errors.append(f'{label}: By must be a number of seconds above 0, not "{cell}"')
        return None
    if duration is not None and by > duration:
        errors.append(f'{label}: By {tm(by)} is after the end of the video, {tm(duration)} s')
    return by


def read_row(kind: str, n: int, row: List[str], header: List[str], duration: Optional[float], errors: List[str]) -> Optional[Dict[str, Any]]:
    label = f'{kind}{n}'
    if len(row) != len(header):
        errors.append(f'{label}: the row has {len(row)} cells and its header has {len(header)}')
        return None
    if not row[0]:
        errors.append(f'{label}: the id is empty')
    elif row[0] != label:
        errors.append(f'{label}: the id is "{row[0]}"; the ids run {kind}1, {kind}2 and on, in order')
    for cell, name in zip(row[1:], header[1:]):
        if not cell:
            errors.append(f'{label}: "{name}" is empty')
    if kind == 'Q':
        return {'id': row[0], 'question': row[1], 'answer': row[2]}
    by = read_by(row[1], label, duration, errors) if row[1] else None
    return {'id': row[0], 'by': by, 'text': row[2]}


def read_table(kind: str, block: List[List[str]], duration: Optional[float], errors: List[str]) -> Optional[List[Dict[str, Any]]]:
    """A table's rows, or None when it has no separator row to read them under."""
    header = block[0]
    if len(block) < 2 or len(block[1]) != len(header) or not all(SEPARATOR.fullmatch(c) for c in block[1]):
        errors.append(f'the {TABLE_NAMES[kind][1]} table has no separator row under its header (| --- | --- | --- |)')
        return None
    rows = [read_row(kind, n, row, header, duration, errors) for n, row in enumerate(block[2:], 1)]
    count(kind, len(rows), errors)
    return [r for r in rows if r]


def count(kind: str, n: Optional[int], errors: List[str]) -> None:
    low, high = COUNTS[kind]
    name, header = TABLE_NAMES[kind]
    if n is None:
        errors.append(f'{name}: no table headed {header}, need {low} to {high} rows')
    elif not low <= n <= high:
        errors.append(f'{name}: {n} row{"" if n == 1 else "s"}, need {low} to {high}')


def check_track(text: str, duration: Optional[float]) -> Tuple[Dict[str, Any], List[str]]:
    """The track as read, and a line for each rule it breaks."""
    lines = text.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    errors: List[str] = []
    premise = read_premise(lines)
    if premise is None:
        errors.append('the premise is missing: start the track with "Premise: ..."')
    elif not premise:
        errors.append('the premise is empty')
    elif len(premise.split()) > PREMISE_MAX:
        errors.append(f'the premise is {len(premise.split())} words, at most {PREMISE_MAX}')
    found: Dict[str, Optional[List[Dict[str, Any]]]] = {}
    for block in table_blocks(lines):
        kind = HEADERS.get(tuple(collapse(c).lower() for c in block[0]))
        if kind and kind in found:
            errors.append(f'the {TABLE_NAMES[kind][1]} table is there twice: keep one')
        elif kind:
            found[kind] = read_table(kind, block, duration, errors)
    for kind in 'KXQ':
        if kind not in found:
            count(kind, None, errors)
    track = {'premise': premise or '', 'must_know': found.get('K') or [], 'must_not': found.get('X') or [],
             'questions': found.get('Q') or []}
    return track, errors


# --- The pieces ---------------------------------------------------------------------------------


def piece_bounds(duration: float) -> List[Tuple[float, float]]:
    bounds = [b for b in HEAD_BOUNDS if b < duration]
    edge = HEAD_BOUNDS[-1] + EVERY
    while edge < duration:
        bounds.append(edge)
        edge += EVERY
    bounds.append(duration)
    pieces = list(zip(bounds, bounds[1:]))
    if len(pieces) > 1 and pieces[-1][1] - pieces[-1][0] < TAIL_MIN:
        pieces[-2:] = [(pieces[-2][0], pieces[-1][1])]
    return pieces


def packets_of(pieces: List[Tuple[float, float]]) -> List[Dict[str, Any]]:
    return [{'packet': i, 't0': a, 't1': b} for i, (a, b) in enumerate(pieces, 1)]


def run_plan(data: Dict[str, Any]) -> Dict[str, Any]:
    text = as_str(data.get('track'), 'track')
    duration = None if data.get('duration') is None else as_num(data['duration'], 'duration')
    pieces: List[Tuple[float, float]] = []
    problems: List[str] = []
    if duration is not None and duration < SHORTEST:
        problems.append(f'duration {tm(duration)} s is under {SHORTEST} s: a video that short has no piece to watch')
    elif duration is not None:
        pieces = piece_bounds(duration)
    track, errors = check_track(text, duration if not problems else None)
    errors = problems + errors
    return {'ok': not errors, 'track': track, 'packets': packets_of(pieces), 'seal': seal(text), 'errors': errors}


# --- The video's words and frames ---------------------------------------------------------------


def spread(text: str, start: float, end: float) -> List[Tuple[str, float, float]]:
    """A segment's words with no times of their own, spread evenly over it."""
    tokens = text.split()
    n = len(tokens)
    return [(tok, start + (end - start) * i / n, start + (end - start) * (i + 1) / n) for i, tok in enumerate(tokens)]


def segment_words(k: int, seg: Dict[str, Any]) -> List[Word]:
    where = f'video.transcript segments[{k}]'
    start, end = as_num(seg.get('start'), f'{where}.start'), as_num(seg.get('end'), f'{where}.end')
    text = seg.get('text', '')
    need(isinstance(text, str), f'{where}.text must be text')
    tags = as_list(seg.get('tags') or [], f'{where}.tags')
    speaker = next((t for t in tags if isinstance(t, str) and t.startswith('speaker:')), None)
    entries = as_list(seg.get('words') or [], f'{where}.words')
    tokens = text.split()
    if entries and (len(entries) == len(tokens) or all(isinstance(w, dict) and isinstance(w.get('text', w.get('word')), str) for w in entries)):
        timed = []
        for i, w in enumerate(entries):
            w = as_dict(w, f'{where}.words[{i}]')
            word = w.get('text', w.get('word', tokens[i] if len(entries) == len(tokens) else None))
            need(isinstance(word, str), f'{where}.words[{i}].text must be text')
            timed.append((word.strip(), as_num(w.get('start'), f'{where}.words[{i}].start'), as_num(w.get('end'), f'{where}.words[{i}].end')))
    else:
        timed = spread(text, start, end)
    return [Word(text=w, start=a, end=b, seg=k, speaker=speaker) for w, a, b in timed if w]


def read_words(raw: Any) -> List[Word]:
    transcript = as_dict(raw, 'video.transcript')
    if isinstance(transcript.get('transcript'), dict):
        transcript = transcript['transcript']
    segments = as_list(transcript.get('segments'), 'video.transcript.segments')
    words: List[Word] = []
    for k, seg in enumerate(segments):
        words.extend(segment_words(k, as_dict(seg, f'video.transcript segments[{k}]')))
    return words


def read_voices(raw: Any) -> List[Tuple[float, float, str]]:
    out = []
    for i, line in enumerate([] if raw is None else as_list(raw, 'video.voices')):
        line = as_dict(line, f'video.voices[{i}]')
        label = line.get('voice')
        need(isinstance(label, str) and bool(label) or _num(label), f'video.voices[{i}].voice must be text or a number')
        out.append((as_num(line.get('start'), f'video.voices[{i}].start'), as_num(line.get('end'), f'video.voices[{i}].end'), str(label)))
    return out


def voice_of(mid: float, speaker: Optional[str], lines: List[Tuple[float, float, str]]) -> Any:
    """The voice line that holds a word's midpoint, else the nearest within reach, else its speaker tag."""
    best: Optional[Tuple[Tuple[float, float, int], str]] = None
    for i, (a, b, label) in enumerate(lines):
        gap = 0.0 if a <= mid <= b else min(abs(mid - a), abs(mid - b))
        if gap <= VOICE_REACH and (best is None or (gap, a, i) < best[0]):
            best = ((gap, a, i), label)
    if best:
        return ('line', best[1])
    return ('tag', speaker) if speaker else None


def name_voices(words: List[Word], lines: List[Tuple[float, float, str]], duration: float) -> Dict[Any, str]:
    """Each voice's name, `voice 1`, `voice 2`, in order of first appearance over the video."""
    names: Dict[Any, str] = {}
    for word in sorted(words, key=lambda x: x.mid):
        word.voice = voice_of(word.mid, word.speaker, lines)
        if word.voice is not None and 0 <= word.mid <= duration and word.voice not in names:
            names[word.voice] = f'voice {len(names) + 1}'
    return names


def read_video(raw: Any, errors: List[str]) -> Tuple[float, Video]:
    v = as_dict(raw, 'video')
    duration, fps = as_num(v.get('duration'), 'video.duration'), as_num(v.get('fps'), 'video.fps')
    frames = [as_str(u, f'video.frames[{i}]') for i, u in enumerate(as_list(v.get('frames'), 'video.frames'))]
    words, lines = read_words(v.get('transcript')), read_voices(v.get('voices'))
    if duration < SHORTEST:
        errors.append(f'video.duration {tm(duration)} s is under {SHORTEST} s: a video that short has no piece to watch')
    if fps <= 0:
        errors.append('video.fps must be above 0')
    if not frames:
        errors.append('video.frames is empty: give the image sequence')
    return duration, Video(fps, frames, words, name_voices(words, lines, duration))


def frame_times(a: float, b: float) -> List[float]:
    """4 a second below 3 s, then 2 a second from the first half-second step at or after 3 s."""
    times, i = [], 0
    while a + FAST_STEP * i < min(b, FAST_UNTIL):
        times.append(a + FAST_STEP * i)
        i += 1
    k = 0
    while a + SLOW_STEP * k < FAST_UNTIL:
        k += 1
    while a + SLOW_STEP * k < b:
        times.append(a + SLOW_STEP * k)
        k += 1
    return times


def frames_of(video: Video, a: float, b: float) -> List[Tuple[float, str]]:
    """A piece's frames as (time, url): none twice, at most FRAME_MAX spread evenly, the first and last kept."""
    picks, seen = [], set()
    for x in frame_times(a, b):
        i = min(round(x * video.fps), len(video.frames) - 1)
        # The nearest frame can be the next piece's first: take the one before, so no piece shows what comes after it.
        if i > 0 and i / video.fps >= b:
            i -= 1
        if i not in seen:
            seen.add(i)
            picks.append((i, x))
    if len(picks) > FRAME_MAX:
        picks = [picks[round(i * (len(picks) - 1) / (FRAME_MAX - 1))] for i in range(FRAME_MAX)]
    return [(x, video.frames[i]) for i, x in picks]


def voice_line(group: List[Word], names: Dict[Any, str], a: float, b: float) -> str:
    who = names.get(group[0].voice, 'a voice')
    said = ' '.join(x.text for x in group)
    return f'[{tm2(max(group[0].start, a))}–{tm2(min(group[-1].end, b))}] {who}: "{said}"'


def quiet_lines(words: List[Word], a: float, b: float) -> List[str]:
    """`No words:` for each stretch of PAUSE or more in the piece with no word heard."""
    out, cursor = [], a
    for x in sorted(words, key=lambda w: w.start):
        start = max(x.start, a)
        if start - cursor >= PAUSE - TOLERANCE:
            out.append(f'No words: {tm2(cursor)}–{tm2(start)} s')
        cursor = max(cursor, min(x.end, b))
    if b - cursor >= PAUSE - TOLERANCE:
        out.append(f'No words: {tm2(cursor)}–{tm2(b)} s')
    return out


def heard_lines(video: Video, a: float, b: float, last: bool) -> List[str]:
    """The words heard in a piece with their times and voices, its pauses, and its pace."""
    words = sorted((x for x in video.words if a <= x.mid < b or (last and x.mid == b)), key=lambda x: x.mid)
    pace = f'Pace: {len(words) / (b - a):.1f} words/s'
    if not words:
        return ['Heard: nothing', pace]
    runs = [voice_line(list(g), video.names, a, b) for _, g in itertools.groupby(words, key=lambda x: (x.seg, x.voice))]
    return ['Heard:'] + runs + quiet_lines(words, a, b) + [pace]


def moment_text(row: Dict[str, Any]) -> str:
    parts = []
    if row.get('seen'):
        parts.append(f'Seen: {row["seen"]}')
    if row.get('heard'):
        parts.append(f'Heard: "{row["heard"]}"')
    if row.get('on_screen'):
        parts.append(f'On screen: "{row["on_screen"]}"')
    return '\n'.join(parts)


def view_of(w: Watch, k: int) -> Tuple[List[str], str, str]:
    """What piece `k` shows: its picture urls, the times of its frames, and the lines it tells."""
    a, b = w.pieces[k]
    if w.video is None:
        return [], '', moment_text((w.rows or [])[k])
    shown = frames_of(w.video, a, b)
    body = '\n'.join(heard_lines(w.video, a, b, k == len(w.pieces) - 1))
    return [u for _, u in shown], join_and([tm2(x) for x, _ in shown]), body


# --- The paper rows -----------------------------------------------------------------------------


def row_errors(i: int, row: Dict[str, Any], before: Optional[Dict[str, Any]], errors: List[str]) -> None:
    where = f'rows[{i}]'
    for key in row:
        if key not in ROW_KEYS:
            errors.append(f'{where}: "{key}" is not a part of a moment; a row holds t0, t1 and what is seen, heard or '
                          'on screen in it, never its feeling, its intent or its cause')
    if not any(row[k] for k in ('seen', 'heard', 'on_screen')):
        errors.append(f'{where}: needs seen, heard or on_screen')
    if row['t0'] < 0 or row['t1'] <= row['t0']:
        errors.append(f'{where}: needs 0 <= t0 < t1, not {tm(row["t0"])} to {tm(row["t1"])}')
    elif before and row['t0'] < before['t0']:
        errors.append(f'{where}: starts at {tm(row["t0"])} s, before the row above it: put the rows in time order')
    elif before and row['t0'] < before['t1']:
        errors.append(f'{where}: starts at {tm(row["t0"])} s, before the row above it ends at {tm(before["t1"])} s')


def read_rows(raw: Any, errors: List[str]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for i, item in enumerate(as_list(raw, 'rows')):
        item = as_dict(item, f'rows[{i}]')
        row = {'t0': as_num(item.get('t0'), f'rows[{i}].t0'), 't1': as_num(item.get('t1'), f'rows[{i}].t1')}
        for key in ('seen', 'heard', 'on_screen'):
            part = item.get(key)
            need(part is None or isinstance(part, str), f'rows[{i}].{key} must be text')
            row[key] = collapse(part or '')
        row_errors(i, {**item, **row}, rows[-1] if rows else None, errors)
        rows.append(row)
    if not rows:
        errors.append('rows is empty: give the moments, each with its t0 and t1')
    return rows


# --- Reading the round --------------------------------------------------------------------------


def read_personas(raw: Any, errors: List[str]) -> List[Dict[str, str]]:
    out = []
    for i, p in enumerate(as_list(raw, 'personas')):
        p = as_dict(p, f'personas[{i}]')
        out.append({key: as_str(p.get(key), f'personas[{i}].{key}') for key in ('id', 'text', 'model')})
    for i, p in enumerate(out):
        errors.extend(f'personas[{i}].{key} is empty' for key, value in p.items() if not value.strip())
    if len(out) != 3:
        errors.append(f'personas: need exactly 3 viewers, got {len(out)}')
    ids = [p['id'] for p in out]
    errors.extend(f'personas: the id "{x}" is used twice' for x in sorted({x for x in ids if ids.count(x) > 1}))
    return out


def read_replies(raw: Any) -> List[Dict[str, Any]]:
    out = []
    for i, r in enumerate(as_list(raw, 'replies')):
        r = as_dict(r, f'replies[{i}]')
        packet = r.get('packet')
        if packet != 'end':
            need(_num(packet) and float(packet).is_integer(), f'replies[{i}].packet must be a piece number or "end"')
            packet = int(packet)
        out.append({'viewer': as_str(r.get('viewer'), f'replies[{i}].viewer'), 'packet': packet,
                    'text': as_str(r.get('text'), f'replies[{i}].text')})
    return out


def read_source(data: Dict[str, Any], errors: List[str]) -> Tuple[List[Tuple[float, float]], Optional[Video], Optional[List[Dict[str, Any]]]]:
    video, rows = data.get('video'), data.get('rows')
    need((video is None) != (rows is None), 'give the draft as "video" or the cards as "rows", one of them')
    if rows is not None:
        found = read_rows(rows, errors)
        return [(r['t0'], r['t1']) for r in found], None, found
    duration, watched = read_video(video, errors)
    return (piece_bounds(duration) if duration >= SHORTEST else []), watched, None


def read_round(data: Dict[str, Any]) -> Tuple[Watch, List[str]]:
    """The round's input as a Watch, and a line for each rule it breaks."""
    text = as_str(data.get('track'), 'track')
    source_errors: List[str] = []
    pieces, video, rows = read_source(data, source_errors)
    persona_errors: List[str] = []
    personas = read_personas(data.get('personas'), persona_errors)
    replies = read_replies(data.get('replies'))
    flags = [as_flag(data, key) for key in ('short', 'promo', 'cuts')]
    usable = bool(pieces) and not source_errors
    track, track_errors = check_track(text, pieces[-1][1] if usable else None)
    w = Watch(text, track, personas, replies, flags[0], flags[1], flags[2], pieces, video, rows)
    return w, track_errors + persona_errors + source_errors


# --- Reading a reply, and walking a viewer ------------------------------------------------------


def read_reply(text: str) -> Optional[Dict[str, Any]]:
    """The JSON object in a model's reply: its fence and anything around the braces dropped."""
    body = re.sub(r'\s*```\s*$', '', re.sub(r'^\s*```(?:json)?\s*', '', text, flags=re.IGNORECASE))
    first, last = body.find('{'), body.rfind('}')
    if first < 0 or last < first:
        return None
    try:
        obj = json.loads(body[first:last + 1])
    except ValueError:
        return None
    return obj if isinstance(obj, dict) else None


def keys_of(w: Watch) -> List[Any]:
    return list(range(1, len(w.pieces) + 1)) + ['end']


def label_of(key: Any) -> str:
    return 'the end' if key == 'end' else f'packet {key}'


def walk(w: Watch, viewer: str, by_key: Dict[Tuple[str, Any], List[str]]) -> Walk:
    """Go through a viewer's pieces in order: each with a readable reply is done; the first that is not is its next call."""
    done: List[Tuple[Any, Optional[Dict[str, Any]]]] = []
    for key in keys_of(w):
        texts = by_key.get((viewer, key), [])
        good = [r for r in (read_reply(t) for t in texts) if r is not None]
        if good:
            done.append((key, good[-1]))
        elif len(texts) >= 2:
            done.append((key, None))
        else:
            return Walk(viewer, done, key, len(texts) == 1)
    return Walk(viewer, done, None, False)


def reply_errors(w: Watch, walks: List[Walk], by_key: Dict[Tuple[str, Any], List[str]]) -> List[str]:
    out = []
    ids, keys = [p['id'] for p in w.personas], keys_of(w)
    for r in w.replies:
        if r['viewer'] not in ids:
            out.append(f'a reply names {r["viewer"]}, who is not one of the viewers ({", ".join(ids)})')
        elif r['packet'] not in keys:
            out.append(f'{r["viewer"]}: a reply for packet {r["packet"]}, but the video has packets 1 to {len(w.pieces)} and "end"')
    for x in walks:
        later = keys[keys.index(x.due) + 1:] if x.due is not None else []
        out.extend(f'{x.viewer}: the reply for {label_of(k)} is ahead of {x.viewer}\'s next call, {label_of(x.due)}'
                   for k in later if (x.viewer, k) in by_key)
    return out


# --- The notes and the prompts ------------------------------------------------------------------


def answer(reply: Optional[Dict[str, Any]], key: str) -> str:
    v = reply.get(key) if reply else None
    return v if isinstance(v, str) else NO_ANSWER


def checkpoint(w: Watch) -> int:
    return next((i for i, (_, end) in enumerate(w.pieces) if end >= 3.0), len(w.pieces) - 1)


def piece_keys(w: Watch, packet: int) -> Tuple[str, ...]:
    """The keys beyond the four every piece asks."""
    return (('keep_watching', 'ad') if w.short and (packet <= 2 or packet == checkpoint(w) + 1) else ()) + (('jump',) if w.cuts else ())


def note_line(a: float, b: float, fields: Optional[Dict[str, str]], short: bool = False) -> str:
    head = f'{tm(a)}–{tm(b)} s: '
    if fields is None:
        return head + NO_ANSWER
    return head + '; '.join(f'{k}: {collapse(fields[k])}' for k in (NOTE_KEYS_SHORT if short else NOTE_KEYS))


def fit(build: Callable[[str], str], notes: List[Tuple[float, float, Optional[Dict[str, str]]]]) -> Optional[str]:
    """The prompt, with the oldest notes cut down until it is under the cap; None when it never is."""
    lines = [note_line(*n) for n in notes]
    for step in range(len(notes) + 1):
        prompt = build('\n'.join(lines) or NONE_YET)
        if len(prompt) <= PROMPT_MAX:
            return prompt
        if step < len(notes):
            lines[step] = note_line(*notes[step], short=True)
    for n in range(1, len(notes) + 1):
        prompt = build('\n'.join([CUT] + lines[n:]))
        if len(prompt) <= PROMPT_MAX:
            return prompt
    return None


def piece_prompt(w: Watch, persona: Dict[str, str], packet: int, view: Tuple[List[str], str, str], notes: str) -> str:
    a, b = w.pieces[packet - 1]
    extra = (EXTRA_SHORT if w.short and (packet <= 2 or packet == checkpoint(w) + 1) else '') + (EXTRA_CUTS if w.cuts else '')
    values = {'system': SYSTEM, 'persona': persona['text'], 't0': tm(a), 't1': tm(b), 'notes': notes, 'extra': extra,
              'limit': str(LIMIT_EXTRA if extra else LIMIT)}
    if w.video is None:
        return fill(PAPER_PIECE, packet=str(packet), text=view[2], **values)
    return fill(VIDEO_PIECE, times=view[1], heard=view[2], **values)


def end_prompt(w: Watch, persona: Dict[str, str], notes: str) -> str:
    asked = [f'{i}. {collapse(q["question"])}' for i, q in enumerate(w.track['questions'], 1)]
    answers = '[' + ', '.join(f'"answer to question {i}"' for i in range(1, len(asked) + 1)) + ']'
    if w.short:
        asked += list(PROMO_LINES if w.promo else SHORT_LINES)
    return fill(END_PROMPT, system=SYSTEM, persona=persona['text'], intro=END_VIDEO if w.video else END_PAPER, notes=notes,
                questions='\n'.join(asked), answers=answers, extra=EXTRA_END if w.short else '')


def call_for(w: Watch, persona: Dict[str, str], key: Any, notes: List[Tuple[float, float, Optional[Dict[str, str]]]],
             retry: bool, errors: List[str]) -> Optional[Dict[str, Any]]:
    call: Dict[str, Any] = {'viewer': persona['id'], 'model': persona['model'], 'packet': key}
    if key == 'end':
        prompt = fit(lambda block: end_prompt(w, persona, block), notes)
    else:
        view = view_of(w, key - 1)
        call.update({'t0': w.pieces[key - 1][0], 't1': w.pieces[key - 1][1], 'imageUrls': view[0]})
        prompt = fit(lambda block: piece_prompt(w, persona, key, view, block), notes)
    if prompt is None:
        errors.append(f'{persona["id"]}\'s call for {label_of(key)} is over {PROMPT_MAX} characters even with its notes cut: '
                      'shorten the persona or the questions')
        return None
    call.update({'prompt': prompt, 'retry': retry})
    return call


# --- The accounts -------------------------------------------------------------------------------


def piece_account(w: Watch, k: int, reply: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    out: Dict[str, Any] = {'packet': k + 1, 't0': w.pieces[k][0], 't1': w.pieces[k][1]}
    out.update({key: answer(reply, key) for key in NOTE_KEYS + piece_keys(w, k + 1)})
    return out


def end_account(w: Watch, reply: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    n = len(w.track['questions'])
    away = reply.get('scroll_away') if reply else None
    away = away if isinstance(away, dict) else {}
    given = reply.get('answers') if reply else None
    answers = [x if isinstance(x, str) else NO_ANSWER for x in given] if isinstance(given, list) else []
    at = str(away['at']) if _num(away.get('at')) else answer(away, 'at')
    out: Dict[str, Any] = {'friend': answer(reply, 'friend'), 'scroll_away': {'at': at, 'why': answer(away, 'why')},
                           'answers': (answers + [NO_ANSWER] * n)[:n]}
    if w.short:
        out.update({'could_do': answer(reply, 'could_do'), 'keep': answer(reply, 'keep')})
    return out


def accounts_of(w: Watch, walks: List[Walk]) -> List[Dict[str, Any]]:
    out = []
    for persona, x in zip(w.personas, walks):
        done = dict(x.done)
        out.append({'viewer': persona['id'], 'model': persona['model'],
                    'packets': [piece_account(w, k, done[k + 1]) for k in range(len(w.pieces))],
                    'end': end_account(w, done['end'])})
    return out


def means_nothing(text: str) -> bool:
    return text.strip().lower().rstrip(TRAILING) in MEANS_NOTHING


def folded(text: str) -> str:
    """An answer as its repeat would read: lowercase, no punctuation, no "still", spaces alike."""
    return collapse(re.sub(r'\bstill\b', '', re.sub(r'[^\w\s]', '', text.lower())))


def raised(accounts: List[Dict[str, Any]], key: str) -> List[Dict[str, Any]]:
    """Every answer to `key` by its time, those that mean nothing left out and a viewer's repeats folded."""
    out = []
    for account in accounts:
        last = None
        for p in account['packets']:
            text = p.get(key)
            if not isinstance(text, str) or means_nothing(text) or folded(text) == last:
                continue
            last = folded(text)
            out.append({'t': p['t1'], 'viewer': account['viewer'], 'text': text.strip()})
    return sorted(out, key=lambda x: (x['t'], x['viewer']))


def comparer_prompt(track_text: str, accounts: List[Dict[str, Any]]) -> str:
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'references/cold-watch-comparer.md')
    try:
        with open(path, encoding='utf-8') as f:
            brief = f.read()
    except OSError as err:
        raise InputError(f'cannot read the comparer\'s brief, references/cold-watch-comparer.md: {err}')
    lines = [json.dumps(a, separators=(',', ':'), ensure_ascii=False) for a in accounts]
    return brief + '\n\n# The track\n\n' + track_text + '\n\n# The accounts\n\n' + '\n'.join(lines)


# --- `round` ------------------------------------------------------------------------------------


def evaluate(w: Watch) -> Tuple[List[Walk], List[Dict[str, Any]], List[str]]:
    """Walk every viewer: each one's walk, the calls to send now, and the rules the replies break."""
    by_key: Dict[Tuple[str, Any], List[str]] = {}
    for r in w.replies:
        by_key.setdefault((r['viewer'], r['packet']), []).append(r['text'])
    walks = [walk(w, p['id'], by_key) for p in w.personas]
    errors = reply_errors(w, walks, by_key)
    calls = []
    for persona, x in zip(w.personas, walks):
        if x.due is None:
            continue
        notes = [(w.pieces[k - 1][0], w.pieces[k - 1][1], None if r is None else {key: answer(r, key) for key in NOTE_KEYS}) for k, r in x.done]
        call = call_for(w, persona, x.due, notes, x.retry, errors)
        if call:
            calls.append(call)
    return walks, calls, errors


def unreadable_of(walks: List[Walk]) -> List[Dict[str, Any]]:
    return [{'viewer': x.viewer, 'packet': key} for x in walks for key, reply in x.done if reply is None]


def stopped(w: Watch, errors: List[str]) -> Dict[str, Any]:
    return {'ok': False, 'done': False, 'packets': packets_of(w.pieces), 'calls': [], 'unreadable': [], 'errors': errors}


def run_round(data: Dict[str, Any]) -> Dict[str, Any]:
    w, errors = read_round(data)
    if errors:
        return stopped(w, errors)
    walks, calls, errors = evaluate(w)
    if errors:
        return stopped(w, errors)
    out: Dict[str, Any] = {'ok': True, 'done': not calls, 'packets': packets_of(w.pieces), 'calls': calls,
                           'unreadable': unreadable_of(walks), 'errors': []}
    if not calls:
        accounts = accounts_of(w, walks)
        out.update({'accounts': accounts, 'asked': raised(accounts, 'unclear'),
                    'jumps': raised(accounts, 'jump'),
                    'comparer': {'prompt': comparer_prompt(w.track_text, accounts)}})
    return out


# --- `gaps`: the comparer's marks ---------------------------------------------------------------


def straight(text: str) -> str:
    """Text as a quote is matched: straight quotes, spaces alike, lowercase."""
    return collapse(text.translate(QUOTE_MARKS)).lower()


def words_of(account: Dict[str, Any]) -> Tuple[List[List[str]], List[str]]:
    """A viewer's answer fields, each piece's and then the end's."""
    pieces = [[v for k, v in p.items() if isinstance(v, str) and k not in ('packet', 't0', 't1')] for p in account['packets']]
    end = account['end']
    tail = [end['friend'], end['scroll_away']['at'], end['scroll_away']['why']] + list(end['answers'])
    return pieces, tail + [end[k] for k in ('could_do', 'keep') if k in end]


def locate(words: Tuple[List[List[str]], List[str]], quote: str) -> Optional[int]:
    """The earliest piece whose fields hold the quote; the end counts after every piece."""
    want = straight(quote)
    for i, fields in enumerate(words[0]):
        if want and any(want in straight(f) for f in fields):
            return i
    return len(words[0]) if want and any(want in straight(f) for f in words[1]) else None


def locate_carried(words: Tuple[List[List[str]], List[str]], quote: str) -> Optional[int]:
    """Prefer an occurrence outside a denial or uncertainty, then the latest match."""
    want = straight(quote)
    matches = []
    for i, fields in enumerate(words[0] + [words[1]]):
        for field in fields:
            text = straight(field)
            for match in re.finditer(re.escape(want), text) if want else ():
                # Doubt counts in the quote's own clause only: "I don't know who sent it, but it is her
                # sister's account" says the fact.
                context = re.split(r'[.!?;:]|\b(?:but|though|although|however|yet)\b', text[:match.start()])[-1]
                uncertain = re.search(r"\b(?:not|no|never|whether|if|unknown|unsure|doubt|don't|doesn't|isn't|can't)\b", context)
                matches.append((i, bool(uncertain)))
    return next((i for i, uncertain in matches if not uncertain), matches[-1][0] if matches else None)


def check_mark_rows(raw: Any, w: Watch, words: Dict[str, Any], problems: List[str]) -> Dict[Tuple[str, str], Dict[str, Any]]:
    marks: Dict[Tuple[str, str], Dict[str, Any]] = {}
    if not isinstance(raw, list):
        problems.append('marks: must be a list of {id, viewer, mark, quote}')
        return marks
    known = {k['id']: K_MARKS for k in w.track['must_know']}
    known.update({x['id']: X_MARKS for x in w.track['must_not']})
    for i, m in enumerate(raw):
        if not isinstance(m, dict) or not all(isinstance(m.get(k), str) for k in ('id', 'viewer', 'mark')):
            problems.append(f'marks[{i}]: needs an id, a viewer and a mark, all text')
            continue
        id_, viewer, mark, quote = m['id'].strip(), m['viewer'].strip(), m['mark'].strip().lower(), m.get('quote')
        label = f'{id_} {viewer}'
        if id_ not in known:
            problems.append(f'{label}: {id_} is not a must-know or a must-not-think of the track')
        elif viewer not in words:
            problems.append(f'{label}: {viewer} is not one of the viewers ({", ".join(words)})')
        elif mark not in known[id_]:
            problems.append(f'{label}: the mark "{mark}" must be one of {", ".join(known[id_])}')
        elif (id_, viewer) in marks:
            problems.append(f'{label}: marked more than once; give exactly one mark')
        else:
            marks[(id_, viewer)] = {'mark': mark, 'quote': quote if mark in QUOTED and isinstance(quote, str) else ''}
            quote_problem(label, mark, quote, words[viewer], problems)
    return marks


def quote_problem(label: str, mark: str, quote: Any, words: Tuple[List[List[str]], List[str]], problems: List[str]) -> None:
    if mark not in QUOTED:
        return
    who = label.split()[1]
    if not isinstance(quote, str) or not quote.strip():
        problems.append(f'{label}: "{mark}" needs a quote copied from {who}\'s own words')
    elif locate(words, quote) is None:
        problems.append(f'{label}: the quote “{collapse(quote)}” is not in {who}\'s own words')


def check_unplanned(raw: Any, words: Dict[str, Any], problems: List[str]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    if not isinstance(raw, list):
        problems.append('unplanned: must be a list of {t, question, viewers, quote}')
        return out
    for i, u in enumerate(raw):
        ok = (isinstance(u, dict) and _num(u.get('t')) and isinstance(u.get('question'), str) and isinstance(u.get('quote'), str)
              and isinstance(u.get('viewers'), list) and u['viewers'] and all(isinstance(v, str) for v in u['viewers']))
        if not ok:
            problems.append(f'unplanned[{i}]: needs t, a question, the viewers who raised it and a quote')
            continue
        who = [v for v in u['viewers'] if v in words]
        if len(who) != len(u['viewers']):
            problems.append(f'unplanned[{i}] “{collapse(u["question"])}”: {", ".join(u["viewers"])} are not all viewers')
        elif not any(locate(words[v], u['quote']) is not None for v in who):
            problems.append(f'unplanned[{i}] “{collapse(u["question"])}”: the quote “{collapse(u["quote"])}” is not in '
                            f'the words of {join_and(who)}')
        else:
            out.append({'t': float(u['t']), 'question': u['question'].strip(), 'viewers': list(u['viewers']),
                        'quote': u['quote'].strip(), 'quote_viewer': next(v for v in who if locate(words[v], u['quote']) is not None)})
    return sorted(out, key=lambda x: x['t'])


def check_marks(raw: Any, w: Watch, accounts: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], List[str]]:
    """The comparer's reply, validated against the track and the viewers' own words."""
    problems: List[str] = []
    if isinstance(raw, str):
        raw = read_reply(raw)
        if raw is None:
            return {}, ['the reply is not a JSON object: return the object with marks, final_misread and unplanned']
    words = {a['viewer']: words_of(a) for a in accounts}
    marks = check_mark_rows(raw.get('marks'), w, words, problems)
    for item in w.track['must_know'] + w.track['must_not']:
        problems.extend(f'{item["id"]} {v}: no mark; give exactly one for every viewer' for v in words if (item['id'], v) not in marks)
    final = raw.get('final_misread')
    final = final if isinstance(final, dict) else {}
    problems.extend(f'final_misread {v}: missing; name every viewer, true or false' for v in words if v not in final)
    problems.extend(f'final_misread {v}: must be true or false' for v in words if v in final and not isinstance(final[v], bool))
    problems.extend(f'final_misread {v}: not one of the viewers' for v in final if v not in words)
    unplanned = check_unplanned(raw.get('unplanned', []), words, problems)
    return {'marks': marks, 'final': final, 'unplanned': unplanned}, problems


def deadline_of(by: float, pieces: List[Tuple[float, float]]) -> int:
    """The first piece that ends after `By`; the end, counted as after every piece, when none does."""
    return next((i for i, (_, b) in enumerate(pieces) if b > by), len(pieces))


def time_at(w: Watch, i: int) -> float:
    return w.pieces[i][1] if i < len(w.pieces) else w.duration


def judge(w: Watch, item: Dict[str, Any], marks: Dict[Tuple[str, str], Dict[str, Any]], words: Dict[str, Any]) -> Dict[str, Any]:
    """Each viewer's mark for one must-know or must-not-think, a carried quote told hit or late."""
    out: Dict[str, Any] = {}
    deadline = deadline_of(item['by'], w.pieces)
    for persona in w.personas:
        viewer = persona['id']
        m = marks[(item['id'], viewer)]
        mark, quote, t = m['mark'], m['quote'] or None, None
        if mark in QUOTED:
            at = locate_carried(words[viewer], m['quote']) if mark == 'carried' else locate(words[viewer], m['quote'])
            t = time_at(w, at if at is not None else len(w.pieces))
            if mark == 'carried':
                mark = 'hit' if at is not None and at <= deadline else 'late'
        out[viewer] = {'mark': mark, 'quote': quote, 't': t}
    return out


def starts(text: str, *words: str) -> bool:
    return re.match(r'\W*(?:' + '|'.join(re.escape(x) for x in words) + r')\b', text, re.IGNORECASE) is not None


def short_failures(w: Watch, accounts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """What a short must also clear: staying for the first seconds, no ad, could do it, would keep it."""
    if not w.short:
        return []
    first = checkpoint(w)
    at = min(3.0, w.duration)
    out: List[Dict[str, Any]] = []

    def put(text: str, t: float, bad: List[Tuple[str, str]]) -> None:
        out.append({'text': text, 't': t, 'quotes': [{'viewer': v, 'quote': q} for v, q in bad]})

    pieces = [(a['viewer'], a['packets'][first]) for a in accounts]
    bad = [(v, p['keep_watching']) for v, p in pieces if not starts(p['keep_watching'], 'yes')]
    if len(pieces) - len(bad) < NEED:
        put(f'keep watching at {at:g} s: {len(pieces) - len(bad)} of {len(pieces)}, need {NEED}', at, bad)
    yes = [(v, p['ad']) for v, p in pieces if starts(p['ad'], 'yes')]
    bit = [(v, p['ad']) for v, p in pieces if starts(p['ad'], 'a bit')]
    if yes:
        put(f'ad: {join_and([v for v, _ in yes])} said yes', at, yes)
    if len(bit) > 1:
        put(f'ad: {join_and([v for v, _ in bit])} said a bit, at most 1', at, bit)
    ends = [(a['viewer'], a['end']) for a in accounts]
    do = 'would try it' if w.promo else 'could do it now'
    bad = [(v, e['could_do']) for v, e in ends if not starts(e['could_do'], 'yes')]
    if len(ends) - len(bad) < NEED:
        put(f'{do}: {len(ends) - len(bad)} of {len(ends)}, need {NEED}', w.duration, bad)
    bad = [(v, e['keep']) for v, e in ends if not starts(e['keep'], 'save', 'send', 'both')]
    if len(ends) - len(bad) < NEED:
        put(f'save or send: {len(ends) - len(bad)} of {len(ends)}, need {NEED}', w.duration, bad)
    return out


def fix_of(t: float, kind: str, what: str, quotes: List[Dict[str, str]], id_: Optional[str] = None) -> Dict[str, Any]:
    out: Dict[str, Any] = {'t': t, 'kind': kind}
    if id_:
        out['id'] = id_
    out.update({'what': what, 'quotes': quotes})
    return out


def fixes_of(gaps: List[Dict[str, Any]], must_not: List[Dict[str, Any]], asked: List[Dict[str, Any]],
             unplanned: List[Dict[str, Any]], shorts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Every gap with when it shows, earliest first."""
    out = []
    for g in gaps:
        said = [{'viewer': v, 'quote': m['quote']} for v, m in g['marks'].items() if m['quote'] and m['mark'] != 'hit']
        if g['hits'] < NEED:
            out.append(fix_of(g['by'], 'must-know', g['text'], said, g['id']))
    for row in gaps + must_not:
        out.extend(fix_of(m['t'], m['mark'], row['text'], [{'viewer': v, 'quote': m['quote']}], row['id'])
                   for v, m in row['marks'].items() if m['mark'] in ('misread', 'wondering', 'thought'))
    out.extend(fix_of(u['t'], 'unplanned', u['question'], [{'viewer': u['quote_viewer'], 'quote': u['quote']}]) for u in unplanned)
    out.extend(fix_of(s['t'], 'short', s['text'], s['quotes']) for s in shorts)
    return sorted(out, key=lambda x: x['t'])


def md(text: str) -> str:
    return collapse(text).replace('|', '\\|')


def quote_cell(marks: Dict[str, Dict[str, Any]]) -> str:
    return ' · '.join(f'{v}: “{md(m["quote"])}”' for v, m in marks.items() if m['quote'])


def markdown_of(gaps: List[Dict[str, Any]], must_not: List[Dict[str, Any]], asked: List[Dict[str, Any]],
                unplanned: List[Dict[str, Any]], jumps: List[Dict[str, Any]], line: str) -> str:
    out = ['Cold watch (simulated)', '', '| By | ID | The viewer should know | Marks | Quotes |', '|---|---|---|---|---|']
    for g in gaps:
        marks = ' · '.join(f'{v} {m["mark"]}' for v, m in g['marks'].items())
        out.append(f'| {g["by"]:g} | {g["id"]} | {md(g["text"])} | {marks} | {quote_cell(g["marks"])} |')
    out += ['', '## Misreads to avoid', '']
    for x in must_not:
        who = join_and([f'{v} (“{md(x["marks"][v]["quote"])}”)' for v in x['thought']])
        out.append(f'- {x["id"]}: {md(x["text"])} ' + (f'Thought by {who}.' if who else 'Nobody thought it.'))
    out += ['', '## What the viewers asked', '']
    raised_ = [(a['t'], 0, f'- {a["t"]:g} s, {a["viewer"]}: “{md(a["text"])}”') for a in asked]
    raised_ += [(u['t'], 1, f'- {u["t"]:g} s, {join_and(u["viewers"])}: {md(u["question"])} (“{md(u["quote"])}”)') for u in unplanned]
    out += [r[2] for r in sorted(raised_, key=lambda r: r[:2])] or ['- None.']
    if jumps:
        out += ['', '## Where a cut jumped', ''] + [f'- {j["t"]:g} s, {j["viewer"]}: “{md(j["text"])}”' for j in jumps]
    return '\n'.join(out + ['', line])


def build_gaps(w: Watch, accounts: List[Dict[str, Any]], checked: Dict[str, Any]) -> Dict[str, Any]:
    words = {a['viewer']: words_of(a) for a in accounts}
    marks = checked['marks']
    gaps = []
    for k in w.track['must_know']:
        judged = judge(w, k, marks, words)
        gaps.append({'id': k['id'], 'by': k['by'], 'text': k['text'], 'marks': judged,
                     'hits': sum(m['mark'] == 'hit' for m in judged.values())})
    must_not = []
    for x in w.track['must_not']:
        judged = judge(w, x, marks, words)
        must_not.append({'id': x['id'], 'by': x['by'], 'text': x['text'], 'marks': judged,
                         'thought': [v for v, m in judged.items() if m['mark'] == 'thought']})
    asked = raised(accounts, 'unclear')
    jumps = raised(accounts, 'jump')
    shorts = short_failures(w, accounts)
    reasons = [f'{g["id"]}: {g["hits"]} hit{"" if g["hits"] == 1 else "s"}, need {NEED}' for g in gaps if g['hits'] < NEED]
    reasons += [f'{p["id"]} got the ending wrong' for p in w.personas if checked['final'][p['id']]]
    reasons += [s['text'] for s in shorts]
    line = 'FLOOR NOT MET: ' + '; '.join(reasons) if reasons else 'FLOOR MET'
    return {'ok': True, 'problems': [], 'gaps': gaps, 'must_not': must_not, 'asked': asked, 'jumps': jumps,
            'unplanned': checked['unplanned'], 'fixes': fixes_of(gaps, must_not, asked, checked['unplanned'], shorts),
            'floor': {'met': not reasons, 'line': line},
            'markdown': markdown_of(gaps, must_not, asked, checked['unplanned'], jumps, line)}


def run_gaps(data: Dict[str, Any]) -> Dict[str, Any]:
    raw = data.get('marks')
    need(isinstance(raw, (str, dict)), 'marks must be the comparer\'s reply, as text or as its object')
    w, errors = read_round(data)
    if errors:
        return {'ok': False, 'problems': errors}
    walks, calls, errors = evaluate(w)
    if errors or calls:
        waiting = [f'the watch is not done: {x.viewer} still has {label_of(x.due)} to answer' for x in walks if x.due is not None]
        return {'ok': False, 'problems': errors or waiting}
    accounts = accounts_of(w, walks)
    checked, problems = check_marks(raw, w, accounts)
    if problems:
        retry = comparer_prompt(w.track_text, accounts) + RETRY + '\n'.join(f'- {p}' for p in problems)
        return {'ok': False, 'problems': problems, 'retry_prompt': retry}
    return build_gaps(w, accounts, checked)


STEPS = {'plan': run_plan, 'round': run_round, 'gaps': run_gaps}


def run(data: Any) -> Dict[str, Any]:
    """The script's whole job: the checked input in, the line it prints out."""
    need(isinstance(data, dict), 'the input must be one JSON object')
    step = data.get('step')
    need(isinstance(step, str) and step in STEPS, 'step must be "plan", "round" or "gaps"')
    return STEPS[step](data)


def main(argv: List[str]) -> int:
    if len(argv) > 1 or any(a.startswith('-') for a in argv):
        return fail(USAGE, 2)
    try:
        if argv:
            with open(argv[0], encoding='utf-8-sig') as f:
                text = f.read()
        else:
            text = sys.stdin.buffer.read().decode('utf-8-sig')
    except (OSError, UnicodeDecodeError) as err:
        return fail(f'cannot read the input: {err}')
    try:
        out = run(json.loads(text))
    except json.JSONDecodeError as err:
        return fail(f'the input is not JSON: {err}')
    except InputError as err:
        return fail(str(err))
    sys.stdout.buffer.write((json.dumps(out, separators=(',', ':'), ensure_ascii=False) + '\n').encode('utf-8', 'replace'))
    return 0


def fail(reason: str, code: int = 1) -> int:
    sys.stderr.write('cold_watch.py: ' + ' '.join(reason.split()) + '\n')
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
