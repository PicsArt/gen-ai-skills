"""Captions as an .ass file, for burning in at the conform with ffmpeg's `subtitles` filter.

Usage:
  captions_ass.py <captions.json> <out.ass>

The JSON holds the frame and the style the approved scene used, scaled to the master, and the lines
in master seconds:
  {"width": 2160, "height": 3840, "font": "Work Sans", "size": 80, "color": "#FBFCF7",
   "centerY": 2592, "wrapWidth": 1560, "fade": 0.12,
   "segments": [{"start": 0.89, "end": 4.69, "text": "When people ask ..."}]}

The font is named by its family; pass the brand pack's font folder to ffmpeg as `fontsdir`, so the
burn uses the brand's own file. Each line keeps a soft dark edge so it reads on a bright frame.
"""
from __future__ import annotations

import json
import sys


def ass_colour(hexcode: str, alpha: int = 0) -> str:
    h = hexcode.lstrip('#')
    if len(h) != 6:
        raise ValueError(f'colour must be #RRGGBB, got {hexcode!r}')
    return f'&H{alpha:02X}{h[4:6]}{h[2:4]}{h[0:2]}'.upper()


def stamp(t: float) -> str:
    cs = max(0, int(round(t * 100)))
    return f'{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}'


def escape(text: str) -> str:
    return text.replace('\\', '\\\\').replace('{', '(').replace('}', ')').replace('\n', '\\N')


def build(c: dict) -> str:
    w, h = int(c['width']), int(c['height'])
    margin = max(0, int(round((w - float(c.get('wrapWidth', w))) / 2)))
    fade = int(round(float(c.get('fade', 0.12)) * 1000))
    x, y = w // 2, int(round(float(c.get('centerY', h / 2))))
    head = [
        '[Script Info]', 'ScriptType: v4.00+', f'PlayResX: {w}', f'PlayResY: {h}', 'WrapStyle: 0',
        'ScaledBorderAndShadow: yes', '',
        '[V4+ Styles]',
        'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, '
        'Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, '
        'MarginR, MarginV, Encoding',
        f'Style: Caption,{c["font"]},{c["size"]},{ass_colour(c["color"])},{ass_colour(c["color"])},'
        f'{ass_colour("#000000", 0x90)},{ass_colour("#000000", 0xFF)},0,0,0,0,100,100,0,0,1,'
        f'{max(1, int(c["size"]) // 30)},0,5,{margin},{margin},0,1',
        '', '[Events]', 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text',
    ]
    events = []
    for s in c['segments']:
        if float(s['end']) <= float(s['start']):
            raise ValueError(f'segment ends before it starts: {s}')
        events.append(f'Dialogue: 0,{stamp(float(s["start"]))},{stamp(float(s["end"]))},Caption,,0,0,0,,'
                      f'{{\\pos({x},{y})\\fad({fade},{fade})\\blur3}}{escape(str(s["text"]))}')
    return '\n'.join(head + events) + '\n'


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    with open(argv[0]) as f:
        cfg = json.load(f)
    with open(argv[1], 'w', encoding='utf-8') as f:
        f.write(build(cfg))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
