#!/usr/bin/env python3
"""
Say whether a source's camera recorded gyro data, from its ffprobe reading.

    ffprobe -v error -show_streams -show_format -of json "<original>" > probe.json
    python3 scripts/gyro.py probe.json [--file "<original>"]
    python3 scripts/gyro.py < probe.json

Prints one JSON object, the fields a source keeps in the record:

    {"gyro": true, "gyroKind": "sony-rtmd", "stream": 2}
    {"gyro": false}

The kinds, by the stream that carries them:

- `sony-rtmd`: a data stream tagged `rtmd`, or a data stream whose handler is
  "Timed Metadata Media Handler" (Sony FX3, FX6, A7S III and their kin). Sony writes this
  stream also in modes that record no motion samples (an a7S III at 4K 120 fps), and its samples
  cannot be read here, so it prints `"maybe": true`: the source may have gyro data;
- `gopro-gpmf`: a stream tagged `gpmd`, or a handler naming "GoPro MET";
- `dji`: a data stream tagged `djmd`, or a handler naming "DJI meta";
- `insta360`: no stream: Insta360 keeps its motion data in a trailer at the end of the file, so
  this kind needs `--file`, which reads the file's last 32 bytes and nothing else.

A data stream this list does not know is not counted as gyro data: say it is there, and leave
the source `gyro: false` unless the user says the camera records it.
"""
from __future__ import annotations

import json
import os
import sys

INSTA360_MAGIC = b'8db42d694ccc418790edff439fe026bf'

# (kind, codec tags, handler substrings, data streams only)
KINDS = [
    ('sony-rtmd', ('rtmd',), ('timed metadata media handler',), True),
    ('gopro-gpmf', ('gpmd',), ('gopro met',), False),
    ('dji', ('djmd',), ('dji meta',), True),
]


def classify(probe: dict) -> dict:
    for stream in probe.get('streams', []) or []:
        tag = str(stream.get('codec_tag_string', '')).lower()
        handler = str((stream.get('tags') or {}).get('handler_name', '')).lower()
        is_data = stream.get('codec_type') == 'data'
        for kind, tags, handlers, data_only in KINDS:
            if data_only and not is_data:
                continue
            if tag in tags or any(h in handler for h in handlers):
                found = {'gyro': True, 'gyroKind': kind, 'stream': stream.get('index')}
                if kind == 'sony-rtmd':
                    found['maybe'] = True
                return found
    return {'gyro': False}


def has_insta360_trailer(path: str) -> bool:
    try:
        size = os.path.getsize(path)
        if size < len(INSTA360_MAGIC):
            return False
        with open(path, 'rb') as f:
            f.seek(size - len(INSTA360_MAGIC))
            return f.read() == INSTA360_MAGIC
    except OSError:
        return False


def main(argv: list) -> int:
    args = list(argv)
    file = None
    if '--file' in args:
        i = args.index('--file')
        file = args[i + 1] if i + 1 < len(args) else None
        del args[i:i + 2]
    if args:
        with open(args[0], encoding='utf-8') as f:
            probe = json.load(f)
    else:
        probe = json.load(sys.stdin)
    result = classify(probe)
    if not result['gyro'] and file and has_insta360_trailer(file):
        result = {'gyro': True, 'gyroKind': 'insta360', 'stream': None}
    print(json.dumps(result))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
