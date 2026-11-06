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

It prints one JSON line, `{clips, script, clean, duration, context}`:

- `clips`, one per clip: `heard`, the words kept; `verdict`, `ok` or `fix`; `issues`, each
  `{check, problem}` where check is `integrity`, `substance`, `fluency` or `context`; `repairs`, each
  `{edge, to}` with the time to move that edge to, or `{drop: true}`; and `speakers`, the speaker
  tags the clip's words carry.
- `script`: the whole reel's heard words in play order, `[photo]` where a beat has no speech.
  Read it as prose.
- `clean`: how many clips need no fix. It never refuses a cut: it reports.
- `context`: what a listener who knows only the reel may not be able to place, in play order, each
  `{at, clip, kind, heard, ask}`, with `dropped`, the source's own words the cut leaves out, when they
  are the likely answer. `at` is the second of the reel it is heard at. Kinds: `name`, a name heard
  for the first time; `pointer`, a word like "she" or "that" in the first words after a seam;
  `callback`, a phrase like "as I said"; `seam`, two clips of one source far apart or out of order.
  These are candidates, not faults: a cold reader's account says whether each one landed.

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
# A clip that opens on one of these answers something; the question must be heard first.
ANSWERS = {'yes', 'yeah', 'yep', 'no', 'nope', 'exactly', 'right', 'absolutely', 'definitely', 'sure',
           'totally', 'correct', 'true', 'agreed'}
# Openings that start on an answer word and answer nothing ("Right now our factory employs fifty people").
NOT_ANSWERS = {('right', 'now'), ('right', 'after'), ('no', 'one'), ('sure', 'enough'), ('true', 'story')}
# Words that point back, looked for in the first words after a seam.
POINTERS = ORPHAN | {'they', 'there', 'here', 'theirs'}
POINTER_REACH = 4
# Phrases that call back to something said earlier; the last three only right after a seam.
CALLBACKS = [('like', 'i', 'said'), ('as', 'i', 'said'), ('as', 'i', 'mentioned'), ('i', 'mentioned'),
             ('i', 'told', 'you'), ('like', 'we', 'said'), ('as', 'we', 'said'), ('you', 'remember'),
             ('going', 'back', 'to'), ('the', 'same', 'thing')]
SEAM_CALLBACKS = [("that's", 'why'), ('which', 'is', 'why'), ('this', 'is', 'why')]
# Two clips of one source further apart than this, or out of order, may not read as one thought.
SEAM_JUMP = 20.0
NOT_NAMES = {'I', "I'm", "I've", "I'll", "I'd", 'OK', 'Okay', 'January', 'February', 'March', 'April', 'May', 'June',
             'July', 'August', 'September', 'October', 'November', 'December', 'Monday', 'Tuesday', 'Wednesday',
             'Thursday', 'Friday', 'Saturday', 'Sunday'}

Json = Dict[str, Any]


class InputError(ValueError):
    """Input that cannot be reviewed; the message says what to change."""


def number(value: Any, what: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise InputError(f'{what} must be a number')
    return float(value)


def bare(word: str) -> str:
    return re.sub(r"[^a-z'-]", '', word.lower())


def name_key(token: str) -> str:
    """A token as a name: 'Leo's' and 'Leo.' are 'Leo'."""
    return re.sub(r"['’]s$", '', re.sub(r"[^\w'’-]", '', token))


def tokens_of(words: List[Json]) -> List[tuple]:
    """Each token with the word it is in, and whether it opens a sentence."""
    out: List[tuple] = []
    prev: Optional[tuple] = None
    for w in words:
        for i, token in enumerate(w['w'].split()):
            opens = (prev is None or bool(TERMINAL.search(prev[0]))
                     or (i == 0 and w['s'] - prev[1]['e'] >= PAUSE))
            out.append((token, w, opens))
            prev = (token, w)
    return out


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

    def sentence(self, word: Json) -> str:
        """The words of the sentence `word` is in."""
        start, end = self.thought_start(word['s']), self.thought_end(word['e'])
        return ' '.join(x['w'] for x in self.words if start - EDGE <= x['s'] and x['e'] <= end + EDGE)

    def names(self) -> set:
        """Words the transcript capitalises mid-sentence: its names, as far as words can tell."""
        return {name_key(t) for t, _, opens in tokens_of(self.words)
                if not opens and name_key(t)[:1].isupper() and name_key(t) not in NOT_NAMES}


def carries(speech: Speech, words: List[Json], before: Optional[List[float]]) -> bool:
    """The seam carries on the source's own passage when the clip before, of the same source, kept the
    word before this one's first and stopped before it: an overlapping or backward range replays speech."""
    if not words or before is None:
        return False
    k = speech.words.index(words[0])
    prev = speech.words[k - 1] if k > 0 else None
    return (prev is not None and before[0] - EDGE <= prev['s'] and prev['e'] <= before[1] + EDGE
            and before[1] <= words[0]['s'] + EDGE)


# --- The review -----------------------------------------------------------------------------


def review_clip(speech: Speech, t_in: float, t_out: float, first: bool,
                before: Optional[List[float]] = None, played: Optional[List[List[float]]] = None,
                other_speech: Optional[List[List[str]]] = None) -> Json:
    """`before` is the range of the clip played just before this one, when it is of the same source;
    `played` holds earlier ranges of the same source; `other_speech` holds words heard from other sources."""
    words = speech.kept(t_in, t_out)
    issues: List[Json] = []
    repairs: List[Json] = []

    def problem(check: str, text: str) -> None:
        issues.append({'check': check, 'problem': text})

    carried = carries(speech, words, before)

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

    # Context: an answer is heard with its question. A clip to drop needs no other repair.
    # The question is heard already when an earlier clip of this source played it, a photo or another
    # clip between them or not: reaching back would replay it. A clip of another source heard it too
    # when its words hold the question (a second camera on the same interview). A speaker change alone
    # makes an answer only of an answer word that stands alone ("Yes." or "Yes" and a pause), never of
    # a sentence that opens on one ("No one expected it"), and no opening in NOT_ANSWERS answers.
    if tokens and tokens[0] in ANSWERS and not carried and {'drop': True} not in repairs:
        k = speech.words.index(words[0])
        prev = speech.words[k - 1] if k > 0 else None
        heard = prev is not None and any(r[0] - EDGE <= prev['s'] and prev['e'] <= r[1] + EDGE
                                         for r in (played or []))
        lead = words[0]['w'].split()
        alone = (bool(re.search(r'[.,!?;:…—-]["\')\]]?$', lead[0]))
                 or (len(lead) == 1 and (len(words) == 1 or words[1]['s'] - words[0]['e'] >= PAUSE)))
        non_answer = not alone and tuple(tokens[:2]) in NOT_ANSWERS
        if prev is not None and re.search(r'\?["\')\]]?$', prev['w']):
            question = [bare(t) for t in speech.sentence(prev).split()]
            heard = heard or any(any(row[i:i + len(question)] == question
                                     for i in range(len(row) - len(question) + 1))
                                 for row in (other_speech or []))
        if prev is not None and not heard and not non_answer and (re.search(r'\?["\')\]]?$', prev['w'])
                                               or (alone and prev['seg']['speaker'] != words[0]['seg']['speaker'])):
            problem('context', f'it opens on "{words[0]["w"].split()[0]}", an answer to '
                               f'"{speech.sentence(prev)}", which the cut drops')
            repair('in', speech.thought_start(prev['s']))

    speakers = sorted({w['seg']['speaker'] for w in words if w['seg']['speaker']})
    return {
        'heard': ' '.join(w['w'] for w in words),
        'verdict': 'fix' if issues else 'ok',
        'issues': issues,
        'repairs': repairs,
        'speakers': speakers,
    }


def context(spoken: List[Json], speech: Dict[str, Optional[Speech]]) -> List[Json]:
    """What a listener who knows only the reel may not be able to place, in play order. Each spoken
    clip is `{clip, source, in, out, at, words, carried}`, `at` being where it starts in the reel."""
    found: List[Json] = []
    heard: set = set()
    names = {sid: s.names() for sid, s in speech.items() if s is not None}
    for n, clip in enumerate(spoken):
        s, words = speech[clip['source']], clip['words']
        if s is None or not words:
            continue
        toks = tokens_of(words)
        seam = not clip['carried']
        k = s.words.index(words[0])
        prev = s.words[k - 1] if k > 0 else None

        def add(kind: str, word: Json, said: str, ask: str, dropped: Optional[str] = None, **extra: Any) -> None:
            item = dict({'at': round(clip['at'] + max(0.0, word['s'] - clip['in']), 2), 'clip': clip['clip'],
                         'kind': kind, 'heard': said, 'ask': ask}, **extra)
            if dropped:
                item['dropped'] = dropped
            found.append(item)

        # A name, the first time the reel says it; and where the source said it first, when the cut drops that.
        for token, word, _ in toks:
            key = name_key(token)
            if key in names[clip['source']] and key not in heard:
                heard.add(key)
                first = next(x for x in s.words if key in {name_key(t) for t in x['w'].split()})
                add('name', word, key, f'Who or what is {key}?',
                    f'{round(first["s"], 2)} s in the source: "{s.sentence(first)}"' if first['s'] < word['s'] - EDGE
                    else None)
        # A word that points back, in the first words after a seam, before any name.
        if seam:
            for i, (token, word, _) in enumerate(toks[:POINTER_REACH]):
                if any(name_key(t) in names[clip['source']] for t, _, _ in toks[:i]):
                    break
                if bare(token) in POINTERS:
                    # The reel's opening pronoun is already a fluency issue.
                    if not (n == 0 and i == 0 and bare(token) in ORPHAN):
                        add('pointer', word, bare(token), f'What does "{bare(token)}" point to?',
                            f'just before, in the source: "{s.sentence(prev)}"' if prev is not None else None)
                    break
        # A phrase that calls back to something said before.
        bares = [bare(t) for t, _, _ in toks]
        for phrase in CALLBACKS + (SEAM_CALLBACKS if seam else []):
            limit = len(bares) if phrase in CALLBACKS else POINTER_REACH
            for i in range(min(limit, len(bares) - len(phrase) + 1)):
                if tuple(bares[i:i + len(phrase)]) == phrase:
                    add('callback', toks[i][1], ' '.join(phrase), f'What does "{" ".join(phrase)}" refer back to?')
        # Two clips of one source, far apart or out of order, heard as one passage, even with nothing
        # said between them.
        before = spoken[n - 1] if n > 0 else None
        if before is not None and before['source'] == clip['source']:
            jump = clip['in'] - before['out']
            if jump > SEAM_JUMP or clip['in'] < before['in']:
                add('seam', words[0], ' '.join(t for t, _, _ in toks[:6]),
                    'Do the clips on either side of this seam read as one thought?', jump=round(jump, 1))
    return sorted(found, key=lambda item: (item['at'], item['clip']))


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
    spoken: List[Json] = []
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
                before = out[-1].get('range') if out and out[-1]['source'] == sid else None
                played = [[c['in'], c['out']] for c in spoken if c['source'] == sid]
                other_speech = [[bare(t) for w in c['words'] for t in w['w'].split()]
                                for c in spoken if c['source'] != sid]
                item = dict({'clip': i, 'source': sid, 'range': [t_in, t_out]},
                            **review_clip(speech[sid], t_in, t_out, first=not spoken, before=before,
                                          played=played, other_speech=other_speech))
                words = speech[sid].kept(t_in, t_out)
                spoken.append({'clip': i, 'source': sid, 'in': t_in, 'out': t_out, 'at': duration, 'words': words,
                               'carried': carries(speech[sid], words, before)})
                script.append(item['heard'])
        duration += length
        out.append(item)
    return {
        'clips': out,
        'script': ' '.join(script),
        'clean': sum(1 for c in out if c['verdict'] != 'fix'),
        'duration': round(duration, 3),
        'context': context(spoken, speech),
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
