"""Generate The Scholar Edu logo SVGs (text converted to outlines using Cinzel, OFL).

Setup (once):  pip install fonttools
Download Cinzel Medium and SemiBold from Google Fonts (https://fonts.google.com/specimen/Cinzel)
and save them next to this script as cinzel500.ttf and cinzel600.ttf.
Run:           python3 tools/logo/gen_logo.py      -> writes SVGs into ../../logo/
(PNG versions are exported separately; see README.md.)
"""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "logo"))
os.makedirs(OUT, exist_ok=True)

NAVY, GOLD, CREAM, BLACK = "#14233a", "#b08d4c", "#f7f4ec", "#16181d"
F500 = TTFont(os.path.join(HERE, "cinzel500.ttf"))
F600 = TTFont(os.path.join(HERE, "cinzel600.ttf"))


def text_width(font, text, size, tracking):
    gs, cmap, upm = font.getGlyphSet(), font.getBestCmap(), font["head"].unitsPerEm
    w = 0
    for ch in text:
        w += gs[cmap[ord(ch)]].width * size / upm + tracking
    return w - tracking


def text_path(font, text, size, tracking, cx, baseline, anchor="middle"):
    """Return SVG path data of `text`, letter-spaced, anchored at cx."""
    gs, cmap, upm = font.getGlyphSet(), font.getBestCmap(), font["head"].unitsPerEm
    w = text_width(font, text, size, tracking)
    x = cx - w / 2 if anchor == "middle" else cx
    s = size / upm
    d = []
    for ch in text:
        g = gs[cmap[ord(ch)]]
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
        g.draw(TransformPen(pen, (s, 0, 0, -s, x, baseline)))
        d.append(pen.getCommands())
        x += g.width * s + tracking
    return " ".join(d), w


# --- Crown, drawn in a 200 x 130 box, centred on x=100 -----------------------
_HALF = (
    "M100 50 "
    "C86 50 76 50 66 44 "          # arch toward second peak
    "C68 38 68 32 64 26 "          # second peak
    "C58 40 50 54 38 58 "          # valley
    "C36 50 30 42 22 36 "          # outer peak
    "C22 52 24 70 30 90 "          # outer wall
    "L100 90 Z"
)
FLEUR = (
    "M100 2 C93 12 92 26 100 40 C108 26 107 12 100 2 Z "        # centre petal
    "M96 42 C88 42 80 38 80 28 C80 21 86 17 91 20 "              # left petal, curling out
    "C86 22 86 28 90 31 C92 33 95 34 97 35 Z "
)
CROWN_HALF = _HALF


def crown(color, x, y, width, bg=None):
    """Crown group; (x, y) is the top-left of its box; width in px."""
    k = width / 200
    bg = bg or "#ffffff"
    return (
        f'<g transform="translate({x:.2f} {y:.2f}) scale({k:.4f})" fill="{color}" stroke="{color}" stroke-width="0.7" stroke-linejoin="round">'
        f'<path d="{CROWN_HALF}"/>'
        f'<path d="{CROWN_HALF}" transform="translate(200 0) scale(-1 1)"/>'
        f'<path d="{FLEUR}"/><path d="{FLEUR}" transform="translate(200 0) scale(-1 1)"/>'
        f'<rect x="93" y="38" width="14" height="7" rx="1.5"/><rect x="98.6" y="48" width="2.8" height="44"/>'
        # band
        f'<rect x="28" y="94" width="144" height="16" rx="2"/>'
        f'<rect x="32" y="114" width="136" height="5" rx="1.5"/>'
        # tip jewels
        f'<circle cx="22" cy="32" r="4.2"/><circle cx="178" cy="32" r="4.2"/>'
        f'<circle cx="64" cy="24" r="3.8"/><circle cx="136" cy="24" r="3.8"/>'
        # negative-space diamonds in band
        f'<g fill="{bg}" stroke="none"><path d="M100 97 L105 102 L100 107 L95 102 Z"/>'
        f'<path d="M64 99 L68 102 L64 105 L60 102 Z"/><path d="M136 99 L140 102 L136 105 L132 102 Z"/>'
        f'<path d="M34 99 L37 102 L34 105 L31 102 Z"/><path d="M166 99 L169 102 L166 105 L163 102 Z"/></g>'
        f"</g>"
    )


def diamond(cx, cy, r, color):
    return f'<path d="M{cx} {cy-r} L{cx+r} {cy} L{cx} {cy+r} L{cx-r} {cy} Z" fill="{color}"/>'


def svg(w, h, body, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{title}"><title>{title}</title>{body}</svg>\n'
    )


TAG = "GLOBAL EDUCATION CONSULTING"
NAME = "THE SCHOLAR EDU"


def stacked(text_color, gold, bg_for_cutout, name):
    W, H = 720, 400
    cx = W / 2
    name_d, name_w = text_path(F600, NAME, 54, 4.5, cx, 282)
    tag_d, tag_w = text_path(F500, TAG, 16, 6, cx, 362)
    rule_y = 318
    half = max(name_w, tag_w) / 2
    body = crown(gold, cx - 135, 22, 270, bg_for_cutout)
    body += f'<path d="{name_d}" fill="{text_color}"/>'
    body += (
        f'<line x1="{cx-half}" y1="{rule_y}" x2="{cx-14}" y2="{rule_y}" stroke="{gold}" stroke-width="1.5"/>'
        f'<line x1="{cx+14}" y1="{rule_y}" x2="{cx+half}" y2="{rule_y}" stroke="{gold}" stroke-width="1.5"/>'
        + diamond(cx, rule_y, 6, gold)
    )
    body += f'<path d="{tag_d}" fill="{text_color}"/>'
    return svg(W, H, body, "The Scholar Edu — Global Education Consulting"), name


def horizontal(text_color, gold, bg_for_cutout, name):
    W, H = 640, 170
    body = crown(gold, 4, 40, 130, bg_for_cutout)
    body += f'<line x1="152" y1="26" x2="152" y2="146" stroke="{gold}" stroke-width="1.5"/>'
    the_d, _ = text_path(F600, "THE", 40, 6, 172, 70, anchor="start")
    sch_d, sch_w = text_path(F600, "SCHOLAR EDU", 40, 4, 172, 116, anchor="start")
    tag_d, _ = text_path(F500, TAG, 11.2, 3.6, 172, 144, anchor="start")
    body += f'<path d="{the_d}" fill="{text_color}"/><path d="{sch_d}" fill="{text_color}"/>'
    body += f'<path d="{tag_d}" fill="{gold}"/>'
    return svg(W, H, body, "The Scholar Edu — Global Education Consulting"), name


def monogram(text_color, gold, bg_for_cutout, name):
    W, H = 300, 340
    cx = W / 2
    # T and S overlapped, like the reference monogram
    t_d, _ = text_path(F600, "T", 150, 0, cx - 30, 268)
    s_d, _ = text_path(F600, "S", 150, 0, cx + 26, 296)
    body = crown(gold, cx - 70, 14, 140, bg_for_cutout)
    body += f'<path d="{t_d}" fill="{gold}"/><path d="{s_d}" fill="{text_color}"/>'
    return svg(W, H, body, "The Scholar Edu monogram"), name


VARIANTS = [
    ("light", NAVY, GOLD, CREAM),   # for cream / white backgrounds
    ("dark", CREAM, GOLD, NAVY),    # for navy backgrounds
]

for tag, tcol, gcol, cut in VARIANTS:
    for fn, base in ((stacked, "scholar-logo"), (horizontal, "scholar-horizontal"), (monogram, "scholar-monogram")):
        s, _ = fn(tcol, gcol, cut, base)
        with open(f"{OUT}/{base}-{tag}.svg", "w", encoding="utf-8") as f:
            f.write(s)
print(sorted(os.listdir(OUT)))
