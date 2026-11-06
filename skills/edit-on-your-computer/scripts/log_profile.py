"""Whether a camera original was shot in a log profile, read from its own metadata.

Usage:
  log_profile.py --file <original> [--probe <ffprobe json>]

ffprobe rarely names a log curve: a Sony XAVC file reports its transfer as unknown and its range
as full. The camera writes the curve in its own XML, inside the file or in a sidecar beside it
(<name>M01.XML), so this reads both. Prints JSON: `log`, `gamma`, `gamut` (and `gamutAssumed`
when the file names none), `builtInLut` (true when log_lut.py can convert it), `rangeFlag`.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

HEAD = 8 * 1024 * 1024
TAIL = 2 * 1024 * 1024
# the first match wins, so longer names come before the names they contain
GAMMAS = [('s-log3', 's-log3'), ('slog3', 's-log3'), ('s-log2', 's-log2'), ('v-log', 'v-log'),
          ('vlog', 'v-log'), ('c-log3', 'c-log3'), ('c-log2', 'c-log2'), ('canon log 3', 'c-log3'),
          ('canon log 2', 'c-log2'), ('d-log', 'd-log'), ('n-log', 'n-log'), ('f-log2', 'f-log2'),
          ('f-log', 'f-log'), ('log3g10', 'log3g10'), ('logc4', 'logc4'), ('logc3', 'logc3'),
          ('s-cinetone', None)]
GAMUTS = [('s-gamut3-cine', 's-gamut3.cine'), ('s-gamut3.cine', 's-gamut3.cine'), ('sgamut3cine', 's-gamut3.cine'),
          ('s-gamut3', 's-gamut3')]
BUILT_IN = {'s-log3': ('s-gamut3.cine', 's-gamut3')}
# Sony writes CaptureGammaEquation="s-log3-cine" for S-Log3 with S-Gamut3.Cine
SONY = re.compile(rb'CaptureGammaEquation[^>]{0,40}?(?:value=)?"([^"]{1,40})"', re.I)


def chunks(path: str) -> list[bytes]:
    out = []
    size = os.path.getsize(path)
    with open(path, 'rb') as f:
        out.append(f.read(HEAD))
        if size > HEAD + TAIL:
            f.seek(size - TAIL)
            out.append(f.read(TAIL))
    return out


def sidecars(path: str) -> list[str]:
    stem, _ = os.path.splitext(path)
    found = []
    for cand in (stem + 'M01.XML', stem + 'M01.xml', stem + '.XML', stem + '.xml'):
        # a case-insensitive disk answers for both spellings of one file
        if os.path.isfile(cand) and not any(os.path.samefile(cand, f) for f in found):
            found.append(cand)
    return found


def read(blobs: list[bytes], probe: dict | None) -> dict:
    gamma = gamut = None
    for blob in blobs:
        m = SONY.search(blob)
        if m:
            tag = m.group(1).decode('ascii', 'ignore').lower()
            if tag.startswith('s-log3'):
                gamma = 's-log3'
                if tag.endswith('cine'):
                    gamut = 's-gamut3.cine'
            break
    text = b'\n'.join(blobs).lower()
    if gamma is None:
        for needle, name in GAMMAS:
            if needle.encode() in text:
                gamma = name
                break
    if gamut is None:
        for needle, name in GAMUTS:
            if needle.encode() in text:
                gamut = name
                break
    stream = {}
    for s in (probe or {}).get('streams', []):
        if s.get('codec_type') == 'video':
            stream = s
            break
    transfer = stream.get('color_transfer')
    if gamma is None and transfer == 'arib-std-b67':
        gamma = 'hlg'
    if gamma is None and transfer == 'smpte2084':
        gamma = 'pq'
    result = {'log': gamma not in (None, 'hlg', 'pq'), 'gamma': gamma, 'gamut': gamut,
              'rangeFlag': stream.get('color_range')}
    if gamma in BUILT_IN:
        if gamut is None:
            result['gamut'] = BUILT_IN[gamma][0]
            result['gamutAssumed'] = True
        result['builtInLut'] = result['gamut'] in BUILT_IN[gamma]
    else:
        result['builtInLut'] = False
    return result


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser()
    p.add_argument('--file', required=True)
    p.add_argument('--probe')
    a = p.parse_args(argv)
    probe = json.load(open(a.probe)) if a.probe else None
    blobs = chunks(a.file)
    for side in sidecars(a.file):
        blobs.append(open(side, 'rb').read(HEAD))
    print(json.dumps(read(blobs, probe)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
