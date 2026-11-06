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
# The camera's own word on its curve and gamut, as Sony writes them:
# <Item name="CaptureGammaEquation" value="s-log3-cine"/> is S-Log3 with S-Gamut3.Cine.
# Also read: <CaptureGammaEquation value="..."/> and CaptureGammaEquation="...".
CAPTURE = re.compile(rb'Capture(GammaEquation|ColorPrimaries)"?(?:\s+value\s*=\s*|\s*=\s*)"([^"]{1,40})"', re.I)
# What a person typed (a title, a comment) can name a curve, "Daily vlog", without being one:
# XML title and comment elements, and QuickTime's title, comment and description atoms.
TYPED = re.compile(rb'<(Title|Description|Comment|UserComment)\b[^>]*>.*?</\1\s*>', re.I | re.S)
TYPED_ATOMS = (b'\xa9nam', b'\xa9cmt', b'\xa9des')


def chunks(path: str) -> list[bytes]:
    out = []
    size = os.path.getsize(path)
    with open(path, 'rb') as f:
        out.append(f.read(HEAD))
        if size > HEAD:
            # the rest of a file under HEAD + TAIL, the last TAIL bytes of a longer one
            f.seek(max(HEAD, size - TAIL))
            out.append(f.read(TAIL))
    return out


def untyped(blob: bytes) -> bytes:
    """The blob without the text a person typed into it."""
    blob = TYPED.sub(b'', blob)
    for atom in TYPED_ATOMS:
        at = blob.find(atom)
        while at != -1:
            size = int.from_bytes(blob[max(at - 4, 0):at], 'big') if at >= 4 else 0
            # an atom is its 4-byte size, its name and its data; a size that cannot be one drops the name alone
            start, end = (at - 4, at - 4 + size) if 8 <= size <= 64 * 1024 else (at, at + 4)
            blob = blob[:start] + blob[end:]
            at = blob.find(atom, start)
    return blob


def name_of(text: str, names: list) -> str | None:
    return next((name for needle, name in names if needle in text), None)


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
    declared = {}
    for blob in blobs:
        for m in CAPTURE.finditer(blob):
            declared.setdefault(m.group(1).lower(), m.group(2).decode('ascii', 'ignore').lower())
    text = b'\n'.join(untyped(blob) for blob in blobs).decode('latin-1').lower()
    curve = declared.get(b'gammaequation')
    if curve is not None:
        # The camera named its curve, so that decides: a Rec.709 clip stays Rec.709 whatever else it says.
        gamma = name_of(curve, GAMMAS)
        if gamma == 's-log3' and curve.endswith('cine'):
            gamut = 's-gamut3.cine'
    else:
        gamma = name_of(text, GAMMAS)
    if gamut is None:
        gamut = name_of(declared.get(b'colorprimaries', text), GAMUTS)
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
