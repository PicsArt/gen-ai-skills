#!/usr/bin/env python3
"""
Put the spoken words of a cut reel on screen: running captions on every spoken clip, highlight
phrases on the few words that matter, or both.

    python3 scripts/reel_text.py input.json
    python3 scripts/reel_text.py < input.json

The input is one JSON object:

    {
      "scene": { the reel's scene, as it was approved } or "scene.json",
      "transcripts": {"talk": "transcript-talk.json"},
      "captions": {"style": { a caption style }},
      "highlights": [
        {"clip": 0, "say": "revenue tripled"},
        {"clip": 2, "say": "nobody tells you this", "text": "Nobody tells you this"}
      ],
      "highlightStyle": { a caption style }
    }

- `scene` is the scene the user approved, theirs if they edited it: the words are timed on its
  own clips, so a clip they trimmed in the editor is read as they left it. Its reel is its first
  `track` layer, and it ends at the composition's `duration`, or with none at that layer's: a clip
  that runs over the end is cut there, and one past it gets no words.
- `transcripts` maps a media asset id in the scene to its `picsart_media_transcribe` result (or
  that result's `transcript`), or to the path of a file that holds it. A clip whose asset has no
  transcript (a photo) or that is `muted` gets no words. A clip held past its `trim.out` freezes
  on its last frame, so only the words inside its trim count.
- `captions` asks for running captions: one `captions` layer per spoken clip, open while that
  clip plays its source, carrying its source's transcript as returned and a `timeOffset` that lines the
  source's clock up with the clip's trim. `style` is the caption style, passed through as given.
- `highlights` asks for phrases: each names a clip of the track, by its index, and `say`, the
  words in that clip it calls out, as spoken (case and punctuation do not matter). `text` is what
  shows, `say` by default. All of them go on one `captions` layer, one segment per phrase, with
  `highlightStyle` (passed through as given) or, without one, big white text on a dark pill that
  the renderer fits to the measured words.

- `cards` asks for word cards (PI-11892), one `captions` layer `captions` over the talk:
  `{"words": 3, "seam": 960, "style": { a caption style }}`. A card closes at `words` words (1 to 3)
  or on a word ending in `. , ? !`; the words are kept as spoken, only shifted onto the reel's
  clock. Each card holds toward the next, so they never blink: its end becomes
  `max(end, min(next start, max(end + 0.8, start + 0.5)))`. With `seam`, the style's `offset` puts
  the cards on it. A split reel's words come from its audio-carrying track (the unmuted one).
- `hook` asks for the hook card, as the format sets it: `{"lines": ["HE'S PARALYZED.", ...],
  "box": "#C8161D", "color": "#FFFFFF", "font": "bebas-neue-regular", "size": 96, "lineHeight": 100,
  "seam": 960, "gap": 70, "length": 3.2}`. Two layers from 0, `hook-box` (a colour box that hugs
  the text) and `hook-text`, centred, the box's bottom edge `gap` px above the seam (or, with no
  seam, at a third of the height). The lines are the ones the map approved, never written here;
  a line over 22 characters, or more than three lines, is a note.

A phrase shows from its first word to half a second after its last, at least 1.5 s and at most
3 s, and never past its clip's end or into the next phrase. It prints one JSON line,
`{scene, layers, highlights, notes}`: the scene with the new layers on top, their ids, each
phrase's `start` and `end` on the reel, and `notes` on any phrase it had to shorten. Input it
cannot place exits 1, with one line on stderr that says what is wrong.

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import copy
import json
import math
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

USAGE = 'usage: reel_text.py [input.json]; with no file, the input is read from stdin'

HOLD_AFTER = 0.5
MIN_SHOW = 1.5
MAX_SHOW = 3.0
GAP = 0.1
EDGE = 0.02
# The default highlight: 96 px text at 1080 wide, its centre two thirds of the way down the frame.
BASE_SIZE = 96
BASE_WIDTH = 1080
DEFAULT_Y = 0.66

Json = Dict[str, Any]
Word = Tuple[str, float, float]


class InputError(ValueError):
    """Input the words cannot be placed from; the message says what to change."""


def number(value: Any, what: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise InputError(f'{what} must be a number')
    return float(value)


def bare(word: str) -> str:
    return re.sub(r"[^\w'-]", '', word.lower())


def read_json(value: Any, base: str, what: str) -> Any:
    if not isinstance(value, str):
        return value
    path = os.path.join(base, value)
    try:
        with open(path, encoding='utf-8-sig') as f:
            return json.load(f)
    except (OSError, UnicodeDecodeError) as err:
        raise InputError(f'{what}: cannot read {path}: {err}')
    except json.JSONDecodeError as err:
        raise InputError(f'{what}: {path} is not JSON: {err}')


def read_transcript(asset_id: str, value: Any) -> Json:
    """The transcript block, as the tool returned it."""
    if isinstance(value, dict) and isinstance(value.get('transcript'), dict):
        value = value['transcript']
    if not isinstance(value, dict) or not isinstance(value.get('segments'), list):
        raise InputError(f'transcripts "{asset_id}" must be the picsart_media_transcribe result, or its transcript')
    return value


def timed_words(transcript: Json) -> List[Word]:
    """Every word with its own times, on the source's clock; a segment without them has none."""
    words = []
    for seg in transcript['segments']:
        tokens = (seg.get('text') or '').split()
        timed = seg.get('words') or []
        if len(timed) == len(tokens):
            words += [(t, float(w['start']), float(w['end'])) for t, w in zip(tokens, timed)]
    return sorted(words, key=lambda w: w[1])


def spoken(transcript: Json) -> List[Tuple[str, float, float, bool]]:
    """What a word card can show: every timed word, and each segment without word times as one
    block over its own start and end (text, start, end, is_block), in spoken order."""
    out: List[Tuple[str, float, float, bool]] = []
    for seg in transcript['segments']:
        tokens = (seg.get('text') or '').split()
        timed = seg.get('words') or []
        if tokens and len(timed) == len(tokens):
            out += [(t, float(w['start']), float(w['end']), False) for t, w in zip(tokens, timed)]
        elif tokens and seg.get('start') is not None and seg.get('end') is not None:
            out.append((' '.join(tokens), float(seg['start']), float(seg['end']), True))
    return sorted(out, key=lambda w: w[1])


def heard_runs(clips: List[Json], assets: Any) -> List[Json]:
    """The heard clips, with pieces that play one source straight on (a split cuts its footage at
    every shot and emphasis edge) joined into one run, so a word across an edge stays whole. A piece
    that holds its last frame ends its run: the next one plays after the hold, not straight on."""
    runs: List[Json] = []
    for clip in clips:
        if clip['image'] or clip['muted'] or clip['cut'] or clip['asset'] not in assets:
            continue
        last = runs[-1] if runs else None
        if (last is not None and last['asset'] == clip['asset'] and last['speed'] == clip['speed']
                and abs(last['spoken_end'] - last['end']) < 1e-3
                and abs(last['out'] - clip['in']) < 1e-3 and abs(last['end'] - clip['start']) < 1e-3):
            last['out'], last['end'], last['spoken_end'] = clip['out'], clip['end'], clip['spoken_end']
        else:
            runs.append(dict(clip))
    return runs


def reel_clips(scene: Json) -> List[Json]:
    """Each clip of the reel's track: where it starts on the reel, how long, and what it plays.

    `out` is the last source second the clip plays: a clip longer than its trim holds the last
    frame, so `spoken_end` is where its source stops on the reel, before `end`.
    """
    tracks = [layer for layer in scene.get('layers') or []
              if isinstance(layer, dict) and (layer.get('content') or {}).get('kind') == 'track']
    # A split reel has two tracks and only one is heard: its words are that track's.
    heard = [t for t in tracks if any(isinstance(c, dict) and (c.get('content') or {}).get('kind') == 'media'
                                      and (c.get('content') or {}).get('muted') is not True
                                      for c in t['content'].get('clips') or [])]
    track = (heard or tracks or [None])[0]
    if track is None:
        raise InputError('the scene has no track layer to time the words on')
    at = number(track.get('start', 0), 'the track layer start')
    # Where the reel stops: the composition's duration, or with none, the track layer's own. A
    # clip past it is never seen, and one that runs over it is cut there.
    composed = scene['composition'].get('duration')
    if composed is not None:
        stop = number(composed, 'the composition duration')
    elif track.get('duration') is not None:
        stop = at + number(track['duration'], 'the track layer duration')
    else:
        stop = math.inf
    images = {a.get('id') for a in scene.get('assets') or [] if isinstance(a, dict) and a.get('type') == 'image'}
    out = []
    for i, clip in enumerate(track['content'].get('clips') or []):
        content = clip.get('content') or {}
        trim = content.get('trim') if content.get('kind', 'media') == 'media' else None
        speed = number(content.get('speed', 1), f'clips[{i}] speed')
        if clip.get('duration') is not None:
            length = number(clip['duration'], f'clips[{i}] duration')
        elif trim:
            length = (number(trim['out'], f'clips[{i}] trim out') - number(trim['in'], f'clips[{i}] trim in')) / speed
        else:
            raise InputError(f'clips[{i}] has no duration and no trim, so its length is unknown')
        source_in = float(trim['in']) if trim else 0.0
        source_out = source_in + length * speed
        if trim:
            source_out = min(source_out, number(trim['out'], f'clips[{i}] trim out'))
        start = min(at, stop)
        if at + length > stop:
            source_out = min(source_out, source_in + max(0.0, stop - at) * speed)
        out.append({'start': start, 'end': min(at + length, stop),
                    'asset': content.get('assetId') if content.get('kind', 'media') == 'media' else None,
                    'image': content.get('assetId') in images, 'muted': content.get('muted') is True,
                    'in': source_in, 'out': source_out, 'speed': speed, 'cut': at >= stop,
                    'spoken_end': start + max(0.0, source_out - source_in) / speed})
        at += length
    if not out:
        raise InputError('the track has no clips')
    return out


def find(words: List[Word], say: str, clip: Json) -> Optional[Tuple[float, float]]:
    """The reel times of `say`, spoken inside `clip`."""
    wanted = [bare(w) for w in say.split() if bare(w)]
    inside = [w for w in words if w[1] >= clip['in'] - EDGE and w[2] <= clip['out'] + EDGE]
    keys = [bare(w[0]) for w in inside]
    for k in range(len(inside) - len(wanted) + 1):
        if keys[k:k + len(wanted)] == wanted:
            return (clip['start'] + (inside[k][1] - clip['in']) / clip['speed'],
                    clip['start'] + (inside[k + len(wanted) - 1][2] - clip['in']) / clip['speed'])
    return None


def caption_layers(clips: List[Json], transcripts: Dict[str, Json], style: Any) -> List[Json]:
    layers = []
    for i, clip in enumerate(clips):
        if clip['image'] or clip['muted'] or clip['cut'] or clip['asset'] not in transcripts:
            continue
        if clip['speed'] != 1:
            raise InputError(f'clips[{i}] plays at speed {clip["speed"]}; captions follow a clip at its own speed only')
        content: Json = {'kind': 'captions', 'transcript': transcripts[clip['asset']],
                         'timeOffset': round(-clip['in'], 3) + 0.0}
        if style:
            content['style'] = style
        layers.append({'id': f'captions-{i}', 'start': round(clip['start'], 3),
                       'duration': round(clip['spoken_end'] - clip['start'], 3), 'content': content})
    if not layers:
        raise InputError('no unmuted clip of the track plays a source with a transcript, so there is nothing to caption')
    return layers


CARD_HOLD = 0.8
CARD_MIN = 0.5
BREAKS = '.,?!'


def word_cards(clips: List[Json], words: Dict[str, List[Tuple[str, float, float, bool]]], raw: Any,
               height: float) -> Json:
    """One captions layer of 1-3 word cards over every heard clip, held so they never blink. A
    segment without word times is one card over the part of it the clip plays."""
    opts = raw if isinstance(raw, dict) else {}
    most = opts.get('words', 3)
    if isinstance(most, bool) or not isinstance(most, int) or not 1 <= most <= 3:
        raise InputError('cards words is 1, 2 or 3')
    cards: List[Json] = []
    runs = heard_runs(clips, words)
    for clip in runs:
        def at(t: float) -> float:
            return clip['start'] + (t - clip['in']) / clip['speed']

        def close(chunk: List[Tuple[str, float, float, bool]]) -> None:
            if not chunk:
                return
            timed = [{'text': t.strip(), 'start': round(max(clip['start'], at(a)), 3),
                      'end': round(min(clip['end'], at(b)), 3)} for t, a, b, _ in chunk]
            start, end = min(x['start'] for x in timed), max(x['end'] for x in timed)
            cards.append({'start': start, 'end': max(end, start + 0.1), 'text': ' '.join(x['text'] for x in timed),
                          'words': timed})

        chunk: List[Tuple[str, float, float, bool]] = []
        for w in words[clip['asset']]:
            if w[3]:
                # an untimed segment: one card over the part of it this clip plays
                if w[1] < clip['out'] and w[2] > clip['in']:
                    close(chunk)
                    chunk = []
                    start, end = round(max(clip['start'], at(w[1])), 3), round(min(clip['end'], at(w[2])), 3)
                    cards.append({'start': start, 'end': max(end, start + 0.1), 'text': w[0]})
                continue
            # a word the trim cuts into stays, within 50 ms of its edges; one wholly outside it is not heard
            if not (w[1] >= clip['in'] - 0.05 and w[2] <= clip['out'] + 0.05 and w[2] > clip['in'] and w[1] < clip['out']):
                continue
            chunk.append(w)
            if len(chunk) == most or w[0].strip()[-1:] in BREAKS:
                close(chunk)
                chunk = []
        close(chunk)
    if not cards:
        raise InputError('no heard clip plays a source with word times, so there are no cards to make')
    cards.sort(key=lambda c: c['start'])
    # Cards hold no further than the last heard clip: never onto a muted end card after it.
    stop = max(c['end'] for c in runs)
    for card, nxt in zip(cards, cards[1:] + [{'start': stop}]):
        card['end'] = round(max(card['end'], min(nxt['start'], max(card['end'] + CARD_HOLD, card['start'] + CARD_MIN))), 3)
    style = copy.deepcopy(opts.get('style')) if isinstance(opts.get('style'), dict) else {}
    if opts.get('seam') is not None:
        style['offset'] = [0, round(number(opts['seam'], 'cards seam') - height / 2, 3)]
    content: Json = {'kind': 'captions', 'timeOffset': 0, 'transcript': {'segments': cards}}
    if style:
        content['style'] = style
    return {'id': 'captions', 'start': 0, 'duration': round(stop, 3), 'content': content}


def hook_layers(raw: Any, width: float, height: float, notes: List[str]) -> List[Json]:
    """The hook card: a colour box hugging the lines, and the lines on it, above the seam."""
    if not isinstance(raw, dict):
        raise InputError('hook must be an object with its lines')
    lines = raw.get('lines')
    if not isinstance(lines, list) or not lines or not all(isinstance(x, str) and x.strip() for x in lines):
        raise InputError('hook lines are the approved lines of the hook, as a list')
    if len(lines) > 3:
        notes.append(f'the hook has {len(lines)} lines; the format reads 2 or 3')
    for line in lines:
        if len(line) > 22:
            notes.append(f'the hook line "{line}" runs {len(line)} characters, over 22')
    size = number(raw.get('size', 96), 'hook size')
    line_height = number(raw.get('lineHeight', size * 100 / 96), 'hook lineHeight')
    length = number(raw.get('length', 3.2), 'hook length')
    w = min(width - 80, max(len(x) for x in lines) * size * 0.42 + 70)
    h = line_height * len(lines) + 36
    if raw.get('seam') is not None:
        bottom = number(raw['seam'], 'hook seam') - number(raw.get('gap', 70), 'hook gap')
    else:
        bottom = height / 3 + h / 2
    y = round(bottom - h / 2, 3)
    font: Json = {'size': size}
    if isinstance(raw.get('font'), str):
        font['family'] = raw['font']
    return [
        {'id': 'hook-box', 'start': 0, 'duration': length, 'transform': {'position': [width / 2, y]},
         'content': {'kind': 'color', 'color': raw.get('box', '#C8161D'), 'size': [round(w), round(h)]}},
        {'id': 'hook-text', 'start': 0, 'duration': length, 'transform': {'position': [width / 2, y]},
         'content': {'kind': 'text', 'text': '\n'.join(lines), 'font': font, 'color': raw.get('color', '#FFFFFF'),
                     'alignment': 'center', 'lineHeight': line_height, 'wrapWidth': round(w - 40)}},
    ]


def default_highlight_style(width: float, height: float) -> Json:
    return {
        'font': {'size': round(BASE_SIZE * width / BASE_WIDTH)},
        'color': '#FFFFFFFF',
        'alignment': 'center',
        'offset': [0, round(height * (DEFAULT_Y - 0.5))],
        'decorations': [{'target': 'line', 'place': 'behind', 'preset': 'pill',
                         'params': {'color': '#000000', 'cornerRadius': 0.3}, 'opacity': 0.6}],
    }


def place_highlights(raw: Any, clips: List[Json], words: Dict[str, List[Word]]) -> Tuple[List[Json], List[str]]:
    if not isinstance(raw, list) or not raw:
        raise InputError('highlights must be a list with at least one phrase')
    placed = []
    for i, h in enumerate(raw):
        if not isinstance(h, dict) or not isinstance(h.get('say'), str) or not any(bare(w) for w in h['say'].split()):
            raise InputError(f'highlights[{i}] needs "say", the words it calls out')
        index = h.get('clip')
        if isinstance(index, bool) or not isinstance(index, int) or not 0 <= index < len(clips):
            raise InputError(f'highlights[{i}] clip must be the index of a clip in the track, from 0 to {len(clips) - 1}')
        clip = clips[index]
        if clip['image'] or clip['asset'] not in words:
            raise InputError(f'highlights[{i}]: clip {index} plays "{clip["asset"]}", which has no transcript')
        if clip['muted']:
            raise InputError(f'highlights[{i}]: clip {index} is muted, so its words are not heard')
        if clip['cut']:
            raise InputError(f'highlights[{i}]: clip {index} starts after the reel ends, so it is never seen')
        found = find(words[clip['asset']], h['say'], clip)
        if found is None:
            raise InputError(f'highlights[{i}]: "{h["say"]}" is not spoken, with word times, in clip {index}')
        text = h.get('text', h['say'])
        if not isinstance(text, str) or not text.strip():
            raise InputError(f'highlights[{i}] text must be the words to show')
        placed.append({'i': i, 'clip': index, 'text': text.strip(), 'from': found[0], 'to': found[1],
                       'clip_end': clip['end']})

    placed.sort(key=lambda p: p['from'])
    notes = []
    for k, p in enumerate(placed):
        end = min(max(p['to'] + HOLD_AFTER, p['from'] + MIN_SHOW), p['from'] + MAX_SHOW, p['clip_end'])
        if k + 1 < len(placed):
            end = min(end, placed[k + 1]['from'] - GAP)
        if end <= p['from']:
            raise InputError(f'highlights[{p["i"]}] starts as the next phrase does; keep one of the two')
        if end - p['from'] < MIN_SHOW:
            notes.append(f'highlights[{p["i"]}] shows for {end - p["from"]:.2f}s, under {MIN_SHOW}s: '
                         'its clip ends or the next phrase starts; drop one, or call it out earlier')
        p['start'], p['end'] = round(p['from'], 3), round(end, 3)
    return placed, notes


def place(data: Any, base: str = '.') -> Json:
    if not isinstance(data, dict):
        raise InputError('the input must be a JSON object')
    if not any(k in data for k in ('captions', 'highlights', 'cards', 'hook')):
        raise InputError('ask for "captions", "cards", "highlights", "hook", or several')
    scene = read_json(data.get('scene'), base, 'scene')
    if not isinstance(scene, dict) or not isinstance(scene.get('composition'), dict):
        raise InputError('scene must be the scene document, or the path of a file that holds it')
    scene = copy.deepcopy(scene)
    width = number(scene['composition'].get('width'), 'the composition width')
    height = number(scene['composition'].get('height'), 'the composition height')
    clips = reel_clips(scene)
    raw = data.get('transcripts')
    if (not isinstance(raw, dict) or not raw) and set(data) & {'captions', 'highlights', 'cards'}:
        raise InputError('transcripts must map an asset id to its transcript')
    transcripts = {aid: read_transcript(aid, read_json(t, base, f'transcripts "{aid}"')) for aid, t in (raw or {}).items()}
    taken = {layer.get('id') for layer in scene.get('layers') or [] if isinstance(layer, dict)}

    added: List[Json] = []
    if 'captions' in data:
        captions = data['captions'] if isinstance(data['captions'], dict) else {}
        added += caption_layers(clips, transcripts, captions.get('style'))

    placed: List[Json] = []
    notes: List[str] = []
    if 'cards' in data:
        added.append(word_cards(clips, {a: spoken(t) for a, t in transcripts.items()}, data['cards'], height))
    if 'hook' in data:
        added += hook_layers(data['hook'], width, height, notes)
    if 'highlights' in data:
        placed, notes = place_highlights(data['highlights'], clips, {a: timed_words(t) for a, t in transcripts.items()})
        style = data.get('highlightStyle') or default_highlight_style(width, height)
        added.append({
            'id': 'highlights', 'start': 0, 'duration': round(clips[-1]['end'], 3),
            'content': {'kind': 'captions', 'style': style, 'transcript': {
                'segments': [{'start': p['start'], 'end': p['end'], 'text': p['text']} for p in placed]}},
        })

    clash = [layer['id'] for layer in added if layer['id'] in taken]
    if clash:
        raise InputError(f'the scene already has layers {", ".join(clash)}: start from the scene without them')
    scene.setdefault('layers', []).extend(added)
    return {
        'scene': scene,
        'layers': [layer['id'] for layer in added],
        'highlights': [{'text': p['text'], 'clip': p['clip'], 'start': p['start'], 'end': p['end']} for p in placed],
        'notes': notes,
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
        out = place(json.loads(text), os.path.dirname(os.path.abspath(argv[0])) if argv else os.getcwd())
    except json.JSONDecodeError as err:
        return fail(f'the input is not JSON: {err}')
    except InputError as err:
        return fail(str(err))
    except (KeyError, IndexError, TypeError, AttributeError, ZeroDivisionError) as err:
        return fail(f'cannot place words from this input: {type(err).__name__} {err}')
    sys.stdout.buffer.write((json.dumps(out, separators=(',', ':'), ensure_ascii=False) + '\n').encode('utf-8'))
    return 0


def fail(reason: str, code: int = 1) -> int:
    sys.stderr.write('reel_text.py: ' + ' '.join(reason.split()) + '\n')
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
