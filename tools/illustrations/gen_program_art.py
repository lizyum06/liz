#!/usr/bin/env python3
"""Draw the three programme illustrations as SVG (original artwork, no third-party assets).

    python3 tools/illustrations/gen_program_art.py   -> images/program-*.svg

Palette follows style.css: ink #1e1e1a, yellow #ffda00, purple #ca92fc, teal #2aceaa, white.
Edit the shapes below and re-run. PNG exports are made separately (see README.md).
"""
import math, os

INK, YEL, PUR, TEAL, WHITE = "#1e1e1a", "#ffda00", "#ca92fc", "#2aceaa", "#ffffff"
OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "images"))
os.makedirs(OUT, exist_ok=True)


def svg(bg, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 320" width="480" height="320" role="img" aria-label="{title}">'
            f'<title>{title}</title><rect width="480" height="320" fill="{bg}"/>{body}</svg>\n')


def stroke(w=3):
    return f'stroke="{INK}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'


def dots(items):
    return "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" {stroke(2.5)}/>' for x, y, r, c in items)


# ---------------------------------------------------------------- 1. Biotechnology & Bioengineering
def biotech():
    b = [f'<circle cx="240" cy="165" r="122" fill="{WHITE}" {stroke()}/>']
    # DNA helix: two strands + rungs
    top, height, amp, cx = 60, 210, 48, 240
    def pt(t, s=1):
        return cx + s * amp * math.sin(t), top + height * t / (4 * math.pi)
    for k in range(13):
        y = top + 14 + k * 15.4
        t = (y - top) * 4 * math.pi / height
        x1, _ = pt(t); x2, _ = pt(t, -1)
        col = YEL if k % 2 == 0 else PUR
        b.append(f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="7" stroke-linecap="round"/>')
        b.append(f'<circle cx="{x1:.1f}" cy="{y:.1f}" r="6" fill="{col}" {stroke(2.5)}/><circle cx="{x2:.1f}" cy="{y:.1f}" r="6" fill="{col}" {stroke(2.5)}/>')
    for s in (1, -1):
        pts = " ".join(f"{pt(i * 4 * math.pi / 160, s)[0]:.1f},{pt(i * 4 * math.pi / 160, s)[1]:.1f}" for i in range(161))
        b.append(f'<polyline points="{pts}" fill="none" {stroke(5)}/>')
    # flask (left)
    b.append(f'<path d="M82 168 H112 V198 L140 252 Q144 262 134 262 H60 Q50 262 54 252 L82 198 Z" fill="{WHITE}" {stroke()}/>')
    b.append(f'<path d="M66 232 H128 L140 252 Q144 262 134 262 H60 Q50 262 54 252 Z" fill="{YEL}" {stroke()}/>')
    b.append(f'<line x1="76" y1="168" x2="118" y2="168" {stroke(4)}/>')
    b.append(dots([(88, 215, 5, WHITE), (104, 200, 4, WHITE), (100, 245, 4, WHITE)]))
    # molecule (right)
    cxm, cym, r = 392, 118, 34
    hexp = [(cxm + r * math.cos(math.radians(60 * i - 30)), cym + r * math.sin(math.radians(60 * i - 30))) for i in range(6)]
    b.append(f'<line x1="{hexp[0][0]:.0f}" y1="{hexp[0][1]:.0f}" x2="440" y2="84" {stroke(4)}/><line x1="{hexp[2][0]:.0f}" y1="{hexp[2][1]:.0f}" x2="432" y2="176" {stroke(4)}/><line x1="{hexp[4][0]:.0f}" y1="{hexp[4][1]:.0f}" x2="340" y2="140" {stroke(4)}/>')
    b.append('<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in hexp) + f'" fill="{PUR}" {stroke()}/>')
    b.append(dots([(440, 84, 11, YEL), (432, 176, 11, WHITE), (340, 140, 11, YEL)]))
    # AI chip (bottom right)
    for i in range(3):
        b.append(f'<line x1="{372 + i * 18}" y1="238" x2="{372 + i * 18}" y2="226" {stroke(3)}/><line x1="{372 + i * 18}" y1="292" x2="{372 + i * 18}" y2="280" {stroke(3)}/>')
    b.append(f'<rect x="360" y="238" width="68" height="42" rx="8" fill="{YEL}" {stroke()}/>')
    b.append(f'<text x="394" y="268" text-anchor="middle" font-family="Arial, sans-serif" font-weight="800" font-size="22" fill="{INK}">AI</text>')
    b.append(dots([(48, 70, 7, YEL), (440, 36, 6, PUR), (30, 150, 5, WHITE)]))
    return svg(TEAL, "".join(b), "생명과학과 공학, 기술, AI를 결합한 바이오공학 일러스트")


# ---------------------------------------------------------------- 2. Medicine, Nursing & Health Sciences
def health():
    b = [f'<rect x="150" y="56" width="270" height="208" rx="26" fill="{WHITE}" {stroke()}/>']
    # heart
    b.append(f'<path d="M285 196 C240 162 218 138 236 116 C252 98 278 106 285 124 C292 106 318 98 334 116 C352 138 330 162 285 196 Z" fill="{YEL}" {stroke(4)}/>')
    # ECG line
    b.append(f'<polyline points="170,228 226,228 240,206 256,250 274,186 290,228 400,228" fill="none" {stroke(5)}/>')
    # small chart ticks
    b.append(f'<line x1="176" y1="84" x2="244" y2="84" {stroke(4)}/><line x1="176" y1="98" x2="214" y2="98" {stroke(4)}/>')
    # stethoscope
    b.append(f'<path d="M52 78 V150 C52 204 124 204 124 150 V78" fill="none" {stroke(5)}/>')
    b.append(f'<circle cx="52" cy="72" r="8" fill="{INK}"/><circle cx="124" cy="72" r="8" fill="{INK}"/>')
    b.append(f'<path d="M88 196 V232" fill="none" {stroke(5)}/>')
    b.append(f'<circle cx="88" cy="254" r="24" fill="{TEAL}" {stroke(4)}/><circle cx="88" cy="254" r="9" fill="{WHITE}" {stroke(3)}/>')
    # medical cross badge (overlaps the card corner)
    b.append(f'<circle cx="414" cy="76" r="36" fill="{YEL}" {stroke(4)}/>')
    b.append(f'<path d="M406 56 H422 V68 H434 V84 H422 V96 H406 V84 H394 V68 H406 Z" fill="{WHITE}" {stroke(3)}/>')
    # pill badge
    b.append(f'<g transform="rotate(-30 392 262)"><rect x="362" y="248" width="60" height="28" rx="14" fill="{TEAL}" {stroke(4)}/><path d="M392 248 V276" {stroke(4)}/><path d="M392 248 H408 a14 14 0 0 1 0 28 H392 Z" fill="{WHITE}" {stroke(4)}/></g>')
    b.append(dots([(30, 40, 6, WHITE), (454, 190, 6, WHITE), (140, 296, 5, YEL), (36, 188, 5, YEL)]))
    return svg(PUR, "".join(b), "의학, 간호, 보건을 표현한 하트와 청진기 일러스트")


# ---------------------------------------------------------------- 3. Career Change & Study
def career():
    b = []
    # two big circles: briefcase -> cap
    b.append(f'<circle cx="122" cy="120" r="62" fill="{TEAL}" {stroke(4)}/><circle cx="358" cy="120" r="62" fill="{PUR}" {stroke(4)}/>')
    # briefcase
    b.append(f'<path d="M110 96 V88 a6 6 0 0 1 6 -6 H128 a6 6 0 0 1 6 6 V96" fill="none" {stroke(4)}/>')
    b.append(f'<rect x="88" y="96" width="68" height="46" rx="8" fill="{WHITE}" {stroke(4)}/><line x1="88" y1="116" x2="156" y2="116" {stroke(4)}/><rect x="116" y="110" width="12" height="12" rx="2" fill="{YEL}" {stroke(3)}/>')
    # graduation cap
    b.append(f'<path d="M330 122 V146 C344 158 372 158 386 146 V122" fill="{WHITE}" {stroke(4)}/>')
    b.append(f'<polygon points="358,84 412,106 358,128 304,106" fill="{WHITE}" {stroke(4)}/>')
    b.append(f'<line x1="412" y1="106" x2="412" y2="144" {stroke(4)}/><circle cx="412" cy="148" r="6" fill="{YEL}" {stroke(3)}/>')
    # swap arrows
    b.append(f'<line x1="196" y1="98" x2="270" y2="98" {stroke(6)}/><polygon points="286,98 266,86 266,110" fill="{INK}" {stroke(2)}/>')
    b.append(f'<line x1="284" y1="144" x2="210" y2="144" {stroke(6)}/><polygon points="194,144 214,132 214,156" fill="{INK}" {stroke(2)}/>')
    # laptop
    b.append(f'<rect x="188" y="212" width="104" height="66" rx="8" fill="{WHITE}" {stroke(4)}/>')
    b.append(f'<path d="M168 278 H312 L318 296 H162 Z" fill="{WHITE}" {stroke(4)}/>')
    b.append(f'<polyline points="204,262 224,242 242,254 276,226" fill="none" stroke="{TEAL}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
    b.append(f'<line x1="204" y1="230" x2="232" y2="230" {stroke(3)}/>')
    # open book
    b.append('<g transform="translate(-30 0)">')
    b.append(f'<path d="M64 236 C88 226 112 228 128 240 V292 C112 282 88 280 64 290 Z" fill="{WHITE}" {stroke(4)}/><path d="M128 240 C144 228 168 226 192 236 V290 C168 280 144 282 128 292 Z" fill="{WHITE}" {stroke(4)}/>')
    b.append(f'<line x1="78" y1="250" x2="114" y2="252" {stroke(3)}/><line x1="78" y1="264" x2="114" y2="266" {stroke(3)}/><line x1="142" y1="252" x2="178" y2="250" {stroke(3)}/>')
    b.append('</g>')
    # pencil
    b.append(f'<g transform="rotate(35 380 262)"><rect x="344" y="250" width="84" height="24" rx="4" fill="{TEAL}" {stroke(4)}/><polygon points="344,250 322,262 344,274" fill="{WHITE}" {stroke(4)}/><rect x="410" y="250" width="18" height="24" rx="4" fill="{PUR}" {stroke(4)}/></g>')
    b.append(dots([(36, 40, 6, WHITE), (448, 40, 7, WHITE), (454, 220, 5, WHITE), (30, 200, 5, PUR)]))
    return svg(YEL, "".join(b), "직업에서 학업으로 전환하는 커리어 전환과 학업 병행 일러스트")


for name, fn in (("program-biotech", biotech), ("program-health", health), ("program-career", career)):
    path = os.path.join(OUT, name + ".svg")
    open(path, "w", encoding="utf-8").write(fn())
    print("wrote", path)
