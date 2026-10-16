#!/usr/bin/env python3
"""
Read a cut of speech the way the viewer will hear it, and say which clips are chopped, empty or
lost at their seam.

    python3 scripts/review_cuts.py reel.json
    python3 scripts/review_cuts.py < reel.json

The input is the reel's plan, the same file reel_cut.py reads, with each spoken source's
transcript added:

    {
      "sources": [
        {"id": "talk", "transcript": "transcript-talk.json"},
        {"id": "photo", "type": "image"}
      ],
      "clips": [
        {"source": "talk", "in": 12.0, "out": 18.5},
        {"source": "photo", "duration": 2.0},
        {"source": "talk", "in": 40.2, "out": 44.0}
      ]
    }

- `transcript` is the `picsart_media_transcribe` result (or its `transcript`), or the path of a
  file that holds it, relative to the input file (or to the working directory, for stdin).
- A clip of a source with no transcript (a photo, a silent shot) is a beat of silence: it is not
  reviewed, and the clips on either side of it still have to make sense.
- Every other field is ignored, so reel_cut.py's input can be passed as it is.

It prints one JSON line, `{clips, script, clean, duration}`:

- `clips`, one per clip: `heard`, the words kept; `verdict`, `ok` or `fix`; `issues`, each
  `{check, problem}` where check is `integrity`, `substance` or `fluency`; `repairs`, each
  `{edge, to}` with the time to move that edge to, or `{drop: true}`; and `speakers`, the speaker
  tags the clip's words carry.
- `script`: the whole reel's heard words in play order, `[photo]` where a beat has no speech.
  Read it as prose.
- `clean`: how many clips need no fix. It never refuses a cut: it reports.

Input it cannot read exits 1, with one line on stderr that says what is wrong.

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import json
import math
import os
import re
import sys
from typing import Any, Dict, List, Optional

USAGE = 'usage: review_cuts.py [input.json]; with no file, the input is read from stdin'

# A real pause: both edges of a silence this long are clean places to cut.
PAUSE = 0.6
# A clip is filler when this share of its words is filler; the opening clip, at the lower share.
FILLER_SHARE = 0.6
HOOK_FILLER_SHARE = 0.35
# A boundary this close to a word's edge is on it, not inside it.
EDGE = 0.02

DANGLING = {'but', 'so', 'and', 'because', "that's", 'thats', 'which', 'or', 'then', 'also', 'plus',
            'however', 'anyway', 'though', 'although', 'yet'}
ORPHAN = {'he', 'she', 'it', 'they', 'him', 'her', 'them', 'his', 'hers', 'their', 'this', 'that',
          'these', 'those'}
FILLER = {'yeah', 'yep', 'yes', 'no', 'nope', 'right', 'ok', 'okay', 'mm', 'mhm', 'mm-hmm', 'uh', 'um',
          'er', 'ah', 'oh', 'like', 'just', 'really', 'totally', 'exactly', 'sure', 'well', 'anyway',
          'basically', 'literally', 'actually', 'i', 'mean', 'you', 'know'}
TERMINAL = re.compile(r'[.!?]["\')\]]?$')

Json = Dict[str, Any]


class InputError(ValueError):
    """Input that cannot be reviewed; the message says what to change."""


def number(value: Any, what: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise InputError(f'{what} must be a number')
    return float(value)


def bare(word: str) -> str:
    return re.sub(r"[^a-z'-]", '', word.lower())


# --- The transcript -------------------------------------------------------------------------


class Speech:
    """One source's words on its own clock, and the segments they belong to."""

    def __init__(self, source_id: str, transcript: Any):
        where = f'sources "{source_id}" transcript'
        if isinstance(transcript, dict) and isinstance(transcript.get('transcript'), dict):
            transcript = transcript['transcript']
        segments = transcript.get('segments') if isinstance(transcript, dict) else None
        if not isinstance(segments, list):
            raise InputError(f'{where} must be the picsart_media_transcribe result, or its transcript')
        self.segments: List[Json] = []
        self.words: List[Json] = []
        for k, seg in enumerate(sorted(segments, key=lambda s: s.get('start', 0))):
            start = number(seg.get('start'), f'{where} segments[{k}] start')
            end = number(seg.get('end'), f'{where} segments[{k}] end')
            text = seg.get('text') if isinstance(seg.get('text'), str) else ''
            tokens = text.split()
            speaker = next((t for t in seg.get('tags') or [] if isinstance(t, str) and t.startswith('speaker:')), None)
            timed = seg.get('words') or []
            entry = {'start': start, 'end': end, 'speaker': speaker, 'timed': bool(timed) and len(timed) == len(tokens)}
            self.segments.append(entry)
            if entry['timed']:
                for token, w in zip(tokens, timed):
                    self.words.append({'w': token, 's': number(w.get('start'), f'{where} word start'),
                                       'e': number(w.get('end'), f'{where} word end'), 'seg': entry})
            elif tokens:
                # No word times for this segment: it is one block, cut only at its edges.
                self.words.append({'w': ' '.join(tokens), 's': start, 'e': end, 'seg': entry, 'block': True})
        self.words.sort(key=lambda x: x['s'])

    def inside(self, t: float) -> Optional[Json]:
        """The word a cut at `t` would chop."""
        return next((x for x in self.words if x['s'] + EDGE < t < x['e'] - EDGE), None)

    def kept(self, t_in: float, t_out: float) -> List[Json]:
        return [x for x in self.words if x['s'] >= t_in - EDGE and x['e'] <= t_out + EDGE]

    def silence_before(self, t: float) -> float:
        before = [x['e'] for x in self.words if x['e'] <= t + EDGE]
        return t - before[-1] if before else math.inf

    def silence_after(self, t: float) -> float:
        after = [x['s'] for x in self.words if x['s'] >= t - EDGE]
        return after[0] - t if after else math.inf

    def thought_start(self, t: float) -> float:
        """The nearest clean in-point at or before `t`: a sentence's first word, or a word after a pause."""
        best = self.words[0]['s'] if self.words else t
        for prev, word in zip([None] + self.words, self.words):
            if word['s'] > t + EDGE:
                break
            opens = prev is None or word['s'] - prev['e'] >= PAUSE or TERMINAL.search(prev['w'])
            if opens:
                best = word['s']
        return best

    def thought_end(self, t: float) -> float:
        """The nearest clean out-point at or after `t`: a sentence's last word, or a word before a pause."""
        for word, nxt in zip(self.words, self.words[1:] + [None]):
            if word['e'] < t - EDGE:
                continue
            if nxt is None or nxt['s'] - word['e'] >= PAUSE or TERMINAL.search(word['w']):
                return word['e']
        return self.words[-1]['e'] if self.words else t


# --- The review -----------------------------------------------------------------------------


def review_clip(speech: Speech, t_in: float, t_out: float, first: bool,
                before: Optional[List[float]] = None) -> Json:
    """`before` is the range of the clip played just before this one, when it is of the same source."""
    words = speech.kept(t_in, t_out)
    issues: List[Json] = []
    repairs: List[Json] = []

    def problem(check: str, text: str) -> None:
        issues.append({'check': check, 'problem': text})

    # The seam carries on the source's own passage when the clip before kept the word before this one
    # and stopped before this one's first word: an overlapping or backward range replays speech.
    carried = False
    if words and before is not None:
        k = speech.words.index(words[0])
        prev = speech.words[k - 1] if k > 0 else None
        carried = (prev is not None and before[0] - EDGE <= prev['s'] and prev['e'] <= before[1] + EDGE
                   and before[1] <= words[0]['s'] + EDGE)

    def repair(edge: str, to: float) -> None:
        to = round(to, 3)
        if abs(to - (t_in if edge == 'in' else t_out)) > EDGE and {'edge': edge, 'to': to} not in repairs:
            repairs.append({'edge': edge, 'to': to})

    # Integrity: nothing is chopped.
    for edge, t in (('in', t_in), ('out', t_out)):
        word = speech.inside(t)
        if word is not None:
            what = 'a stretch with no word times' if word.get('block') else f'the word "{word["w"]}"'
            problem('integrity', f'the {edge} point cuts through {what}')
            repair(edge, speech.thought_start(t) if edge == 'in' else speech.thought_end(t))
    if not words:
        problem('integrity', 'no whole words are inside this clip')
    else:
        lead = words[0]['w']
        if not (lead[:1].isupper() or carried or speech.silence_before(t_in) >= PAUSE) and speech.inside(t_in) is None:
            problem('integrity', f'it opens mid-sentence, on "{lead}"')
            repair('in', speech.thought_start(words[0]['s']))
        last = words[-1]['w']
        if not (TERMINAL.search(last) or speech.silence_after(t_out) >= PAUSE) and speech.inside(t_out) is None:
            problem('integrity', f'it stops mid-sentence, on "{last}"')
            repair('out', speech.thought_end(words[-1]['e']))
        if any(w.get('block') for w in words):
            problem('integrity', 'part of it has no word times, so its edges are only checked at its sentences')

    # Substance: it is worth hearing.
    tokens = [b for b in (bare(t) for w in words for t in w['w'].split()) if b]
    if tokens:
        share = sum(1 for t in tokens if t in FILLER) / len(tokens)
        if share >= FILLER_SHARE:
            problem('substance', f'{round(share * 100)}% of its words are filler: it carries no claim or beat')
            repairs.append({'drop': True})
        elif first and share >= HOOK_FILLER_SHARE:
            problem('substance', f'the opening clip is {round(share * 100)}% filler, and the first seconds decide '
                                 'whether anyone keeps watching')

    # Fluency: the seam plays.
    if tokens:
        if tokens[0] in DANGLING and not carried:
            problem('fluency', f'it opens on "{words[0]["w"].split()[0]}", with nothing before it to connect to')
            repair('in', speech.thought_start(words[0]['s'] - EDGE * 2))
        elif first and tokens[0] in ORPHAN:
            problem('fluency', f'the reel opens on "{words[0]["w"].split()[0]}", which names no one yet')

    speakers = sorted({w['seg']['speaker'] for w in words if w['seg']['speaker']})
    return {
        'heard': ' '.join(w['w'] for w in words),
        'verdict': 'fix' if issues else 'ok',
        'issues': issues,
        'repairs': repairs,
        'speakers': speakers,
    }


def read_json_file(path: str, what: str) -> Any:
    try:
        with open(path, encoding='utf-8-sig') as f:
            return json.load(f)
    except (OSError, UnicodeDecodeError) as err:
        raise InputError(f'{what}: cannot read {path}: {err}')
    except json.JSONDecodeError as err:
        raise InputError(f'{what}: {path} is not JSON: {err}')


def review(data: Any, base: str = '.') -> Json:
    """The review. A `transcript` given as a file path is read relative to `base`."""
    if not isinstance(data, dict):
        raise InputError('the input must be a JSON object')
    raw_sources = data.get('sources')
    if not isinstance(raw_sources, list) or not raw_sources:
        raise InputError('sources must be a list with at least one source')
    speech: Dict[str, Optional[Speech]] = {}
    kinds: Dict[str, str] = {}
    for i, s in enumerate(raw_sources):
        if not isinstance(s, dict) or not isinstance(s.get('id'), str) or not s['id']:
            raise InputError(f'sources[{i}] needs an id')
        transcript = s.get('transcript')
        if isinstance(transcript, str):
            transcript = read_json_file(os.path.join(base, transcript), f'sources "{s["id"]}" transcript')
        speech[s['id']] = Speech(s['id'], transcript) if transcript is not None else None
        kinds[s['id']] = s.get('type', 'video')
    clips = data.get('clips')
    if not isinstance(clips, list) or not clips:
        raise InputError('clips must be a list with at least one clip')

    out: List[Json] = []
    script: List[str] = []
    duration = 0.0
    spoken = 0
    for i, clip in enumerate(clips):
        if not isinstance(clip, dict) or clip.get('source') not in speech:
            raise InputError(f'clips[{i}] names a source that is not in sources')
        sid = clip['source']
        if clip.get('in') is None:
            length = number(clip.get('duration'), f'clips[{i}] duration')
            item: Json = {'clip': i, 'source': sid, 'verdict': 'silent'}
            script.append(f'[{kinds[sid]}]')
        else:
            t_in, t_out = number(clip.get('in'), f'clips[{i}] in'), number(clip.get('out'), f'clips[{i}] out')
            if t_out <= t_in:
                raise InputError(f'clips[{i}] needs in < out')
            length = t_out - t_in
            if speech[sid] is None:
                item = {'clip': i, 'source': sid, 'range': [t_in, t_out], 'verdict': 'silent'}
                script.append(f'[{kinds[sid]}]')
            else:
                item = dict({'clip': i, 'source': sid, 'range': [t_in, t_out]},
                            **review_clip(speech[sid], t_in, t_out, first=spoken == 0,
                                          before=out[-1].get('range') if out and out[-1]['source'] == sid else None))
                spoken += 1
                script.append(item['heard'])
        duration += length
        out.append(item)
    return {
        'clips': out,
        'script': ' '.join(script),
        'clean': sum(1 for c in out if c['verdict'] != 'fix'),
        'duration': round(duration, 3),
    }


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
        out = review(json.loads(text), os.path.dirname(os.path.abspath(argv[0])) if argv else os.getcwd())
    except json.JSONDecodeError as err:
        return fail(f'the input is not JSON: {err}')
    except InputError as err:
        return fail(str(err))
    except (KeyError, IndexError, TypeError, AttributeError) as err:
        return fail(f'cannot review this input: {type(err).__name__} {err}')
    sys.stdout.buffer.write((json.dumps(out, separators=(',', ':'), ensure_ascii=False) + '\n').encode('utf-8'))
    return 0


def fail(reason: str, code: int = 1) -> int:
    sys.stderr.write('review_cuts.py: ' + ' '.join(reason.split()) + '\n')
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
