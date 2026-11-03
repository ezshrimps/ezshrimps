"""Generate the animated SVGs in assets/ (header, project cards, dividers, footer).

Text is converted to outlines so the cards look the same on every machine
(GitHub renders README SVGs as <img>, which can't load web fonts).
Needs fontTools and two OFL fonts; defaults are the Windows copies:
  NOTO=<NotoSansSC-VF.ttf> MONO=<CascadiaMono.ttf> python scripts/build_assets.py
"""
import os
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

FONTS = "C:/Windows/Fonts"
NOTO = os.environ.get("NOTO", f"{FONTS}/NotoSansSC-VF.ttf")
MONO = os.environ.get("MONO", f"{FONTS}/CascadiaMono.ttf")
OUT = os.path.join(os.path.dirname(__file__), "..", "assets")

W = 1300
BG, CARD, PANEL = "#0d1117", "#11161d", "#0a0d12"
INK, MUTED, DIM, LINE = "#e6edf3", "#8b949e", "#484f58", "rgba(140,148,158,.28)"


class Face:
    def __init__(self, path, wght):
        font = instancer.instantiateVariableFont(TTFont(path), {"wght": wght})
        self.glyphs = font.getGlyphSet()
        self.cmap = font.getBestCmap()
        self.upm = font["head"].unitsPerEm


print("loading fonts…")
FACES = {
    "sans": Face(NOTO, 400), "sansm": Face(NOTO, 500), "sansb": Face(NOTO, 700),
    "mono": Face(MONO, 400), "monob": Face(MONO, 700),
}


def ntos(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def layout(s, size, face):
    """Yield (face, glyph, x-offset) and return total advance, with CJK fallback to Noto."""
    primary, fallback = FACES[face], FACES["sansb" if face.endswith("b") else "sans"]
    x, out = 0.0, []
    for ch in s:
        f = primary if ord(ch) in primary.cmap else fallback
        name = f.cmap.get(ord(ch))
        if name is None:
            continue
        out.append((f, name, x))
        x += f.glyphs[name].width * size / f.upm
    return out, x


def width(s, size, face="sans"):
    return layout(s, size, face)[1]


def T(s, x, y, size, face="sans", fill=INK, anchor="start", attrs=""):
    glyphs, w = layout(s, size, face)
    x0 = x - (w if anchor == "end" else w / 2 if anchor == "middle" else 0)
    cmds = []
    for f, name, dx in glyphs:
        k = size / f.upm
        pen = SVGPathPen(f.glyphs, ntos=ntos)
        f.glyphs[name].draw(TransformPen(pen, (k, 0, 0, -k, x0 + dx, y)))
        cmds.append(pen.getCommands())
    return f'<path fill="{fill}" {attrs} d="{"".join(cmds)}"/>'


ANIM = (
    "@keyframes cur{0%,49.9%{opacity:1}50%,100%{opacity:0}}.cur{animation:cur 1.1s steps(1) infinite}"
    "@keyframes fade{0%,6%{opacity:0;transform:translateY(6px)}14%,86%{opacity:1;transform:none}96%,100%{opacity:0}}"
    ".fade{opacity:0;animation:fade 8s ease-out infinite;transform-box:fill-box}"
    "@keyframes grow{0%,4%{transform:scaleY(0)}18%,86%{transform:scaleY(1)}96%,100%{transform:scaleY(0)}}"
    ".grow{transform-box:fill-box;transform-origin:center bottom;animation:grow 8s cubic-bezier(.3,0,.2,1) infinite}"
    "@keyframes wide{0%,6%{transform:scaleX(0)}24%,86%{transform:scaleX(1)}96%,100%{transform:scaleX(0)}}"
    ".wide{transform-box:fill-box;transform-origin:left center;animation:wide 8s cubic-bezier(.6,0,.2,1) infinite}"
    "@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}.bob{animation:bob 5s ease-in-out infinite}"
    "@keyframes tw{0%,100%{opacity:.15}50%{opacity:.9}}.tw{animation:tw 3s ease-in-out infinite}"
    "@keyframes scan{0%{transform:translateY(0)}50%{transform:translateY(176px)}100%{transform:translateY(0)}}.scan{animation:scan 3.2s ease-in-out infinite}"
    "@keyframes drift{from{transform:translateX(-40px)}to{transform:translateX(40px)}}.drift{animation:drift 9s ease-in-out infinite alternate}"
    "@keyframes lit{0%,100%{opacity:.08}12%,40%{opacity:1}}.lit{animation:lit 6s ease-in-out infinite}"
    "@keyframes out{0%{transform:scale(.15);opacity:0}15%{opacity:1}100%{transform:scale(1);opacity:0}}"
    ".out{transform-box:view-box;animation:out 2.4s linear infinite}"
    "@keyframes pulse{0%{transform:scale(.6);opacity:.9}100%{transform:scale(1.9);opacity:0}}"
    ".pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2.4s ease-out infinite}"
    "@keyframes sw{0%{transform:translateX(0)}70%,100%{transform:translateX(1620px)}}.sw{animation:sw 4.5s cubic-bezier(.45,0,.25,1) infinite}"
    "@keyframes eq{0%,100%{transform:scaleY(.25)}50%{transform:scaleY(1)}}.eq{transform-box:fill-box;transform-origin:center bottom;animation:eq 1.2s ease-in-out infinite}"
    "@keyframes dot{0%,100%{opacity:.12}50%{opacity:.8}}.dot{animation:dot 3.6s ease-in-out infinite}"
    "@media (prefers-reduced-motion: reduce){*{animation:none!important;opacity:1!important}}"
)


def svg(h, title, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" '
            f'role="img" aria-labelledby="t"><title id="t">{title}</title><style>{ANIM}</style>{body}</svg>')


def d(sec):
    return f'style="animation-delay:{sec}s"'


def chip(x, y, text, color, filled=False):
    w = width(text, 13, "monob") + 24
    bg = f'fill="{color}"' if filled else 'fill="none"'
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="26" rx="13" {bg} stroke="{color}" stroke-opacity=".55"/>'
            + T(text, x + 12, y + 17.5, 13, "monob", BG if filled else color)), w


# ---------------------------------------------------------------- header / footer / dividers

def header():
    b = [f'<rect x="1" y="1" width="{W-2}" height="228" rx="14" fill="{CARD}" stroke="{LINE}"/>']
    b += [f'<circle cx="{x}" cy="{y}" r="1" fill="{DIM}"/>' for x in range(620, 1280, 26) for y in range(20, 220, 26)]
    b.append(f'<rect x="600" y="2" width="680" height="226" fill="{CARD}" opacity=".55"/>')
    b.append(T("Izzy Xia", 56, 112, 66, "sansb"))
    bars = "".join(f'<rect class="eq" {d(-i*0.17)} x="{338+i*9}" y="62" width="5" height="48" rx="2" fill="#FFA657" opacity=".85"/>' for i in range(5))
    b.append(bars)
    b.append(T("夏梓浩 · @ezshrimps", 58, 150, 19, "mono", MUTED))
    b.append(T("AI BUILDER @ SVTR  ·  LOS ANGELES  ·  RHYTHM GAMER", 58, 196, 13, "mono", DIM))
    tag = "好奇心驱动，做真正用得上的小工具。"
    b.append(f'<rect class="wide" x="640" y="92" width="{width(tag, 30, "sansb"):.0f}" height="12" fill="#FFA657" opacity=".22"/>')
    b.append(T(tag, 640, 100, 30, "sansb"))
    cx = 640 + width(tag, 30, "sansb") + 6
    b.append(f'<rect class="cur" x="{cx:.0f}" y="72" width="12" height="32" fill="#FFA657"/>')
    b.append(T("Curiosity-driven. Shipping small AI tools people actually use.", 640, 134, 16, "sans", MUTED))
    x = 640
    for i, (label, color) in enumerate([("#1 AI 工具", "#FFA657"), ("#2 学日语", "#39D3BB"),
                                         ("#3 生活", "#7EE787"), ("#4 音游", "#FF6BC1")]):
        b.append(f'<circle cx="{x+4}" cy="191" r="3.5" fill="{color}"/>')
        b.append(T(label, x + 14, 196, 13, "mono", MUTED))
        b.append(f'<rect class="tw" {d(i*0.75)} x="{x}" y="206" width="{width(label, 13, "mono")+14:.0f}" height="2" fill="{color}"/>')
        x += width(label, 13, "mono") + 46
    return svg(230, "Izzy Xia · 好奇心驱动，做真正用得上的小工具。Curiosity-driven. Shipping small AI tools people actually use.", "".join(b))


def divider(color):
    return svg(44, "", (
        f'<defs><linearGradient id="g"><stop offset="0" stop-color="{color}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{color}"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></linearGradient>'
        '<clipPath id="ln"><rect x="0" y="19" width="616" height="6"/><rect x="684" y="19" width="616" height="6"/></clipPath></defs>'
        f'<path d="M0 22H616M684 22H1300" stroke="{LINE}" stroke-width="1.5"/>'
        '<g clip-path="url(#ln)"><rect class="sw" x="-320" y="20.5" width="320" height="3" rx="1.5" fill="url(#g)"/></g>'
        f'<circle cx="650" cy="22" r="10" fill="none" stroke="{color}" stroke-width="2"/>'
        f'<circle cx="650" cy="22" r="3.5" fill="{color}"/>'
        f'<circle class="pulse" cx="650" cy="22" r="10" fill="none" stroke="{color}" stroke-width="1.5"/>'))


def footer():
    b = [f'<rect x="1" y="1" width="{W-2}" height="168" rx="14" fill="{CARD}" stroke="{LINE}"/>']
    b.append(T("觉得有意思的话，点一颗 star 就是对我最大的鼓励。", 650, 72, 26, "sansb", INK, "middle"))
    b.append(T("If something here makes you smile, a star means a lot. Thanks for stopping by.", 650, 106, 16, "sans", MUTED, "middle"))
    b.append(T("ezshrimps.com  ·  svtr.ai", 650, 142, 14, "mono", "#FFA657", "middle"))
    for i, x in enumerate(range(470, 840, 30)):
        if 540 < x < 760:
            continue
        b.append(f'<circle class="dot" {d(i*0.3)} cx="{x}" cy="137" r="2.5" fill="#FFA657"/>')
    return svg(170, "觉得有意思的话，点一颗 star 就是对我最大的鼓励。ezshrimps.com · svtr.ai", "".join(b))


# ---------------------------------------------------------------- mockups (panel origin 650,36; size 602x288)
PX, PY, PW, PH = 650, 36, 602, 288


def m_bp(c):
    b = [f'<rect x="{PX+44}" y="{PY+56}" width="150" height="196" rx="8" fill="#161b22" stroke="{LINE}"/>',
         f'<path d="M{PX+164} {PY+56}v30h30" fill="none" stroke="{LINE}"/>',
         T("BP.pdf", PX+62, PY+86, 15, "monob", c)]
    b += [f'<rect x="{PX+62}" y="{PY+106+i*20}" width="{[110,90,114,70,100,84,108][i]}" height="6" rx="3" fill="{DIM}"/>' for i in range(7)]
    b.append(f'<g class="scan"><rect x="{PX+40}" y="{PY+56}" width="158" height="3" fill="{c}" opacity=".9"/>'
             f'<rect x="{PX+40}" y="{PY+59}" width="158" height="18" fill="{c}" opacity=".08"/></g>')
    b.append(f'<path d="M{PX+214} {PY+154}h40m-10-8 10 8-10 8" fill="none" stroke="{c}" stroke-width="2"/>')
    rows = [("公司", "Shrimp Labs"), ("赛道", "AI Agents"), ("轮次", "Seed"), ("金额", "$3M"), ("创始人", "A. Chen · ex-Google")]
    for i, (k, v) in enumerate(rows):
        y = PY + 44 + i * 42
        b.append(T(k, PX+276, y+22, 14, "sans", MUTED))
        b.append(f'<rect x="{PX+340}" y="{y}" width="220" height="32" rx="6" fill="#161b22" stroke="{LINE}"/>')
        b.append(f'<g class="fade" {d(i*0.5)}>' + T(v, PX+352, y+21, 15, "mono", INK) + "</g>")
    b.append(f'<g class="fade" {d(2.8)}>' + chip(PX+340, PY+258, "→ 飞书 Bitable ✓", c)[0] + "</g>")
    return "".join(b)


def m_lyrics(c):
    segs = [("夜空", "よぞら"), ("に", ""), ("浮", "う"), ("かぶ", ""), ("星", "ほし")]
    x, y, b = PX + 56, PY + 110, []
    total = sum(width(s, 50, "sansb") for s, _ in segs)
    b.append(f'<rect class="wide" x="{x}" y="{y+10}" width="{total:.0f}" height="4" rx="2" fill="{c}"/>')
    for i, (s, r) in enumerate(segs):
        w = width(s, 50, "sansb")
        b.append(T(s, x, y, 50, "sansb"))
        if r:
            b.append(f'<g class="fade" {d(i*0.3)}>' + T(r, x + w/2, y - 56, 17, "sansm", c, "middle") + "</g>")
        x += w
    b.append(T("yozora ni ukabu hoshi", PX+58, PY+150, 17, "mono", MUTED))
    tr = "浮在夜空中的星星"
    b.append(f'<rect x="{PX+56}" y="{PY+166}" width="{width(tr,16)+28:.0f}" height="32" rx="16" fill="{c}" fill-opacity=".14"/>')
    b.append(T(tr, PX+70, PY+188, 16, "sans", c))
    x = PX + 56
    for i, (w_, pos) in enumerate([("夜空", "名詞"), ("に", "助詞"), ("浮かぶ", "動詞"), ("星", "名詞")]):
        label = f"{w_} · {pos}"
        cw = width(label, 14, "sans") + 24
        b.append(f'<g class="fade" {d(1.2+i*0.35)}><rect x="{x:.0f}" y="{PY+222}" width="{cw:.0f}" height="30" rx="6" fill="#161b22" stroke="{LINE}"/>'
                 + T(label, x+12, PY+242, 14, "sans", INK) + "</g>")
        x += cw + 10
    b.append(T("Web  +  微信小程序", PX+PW-30, PY+40, 13, "mono", DIM, "end"))
    return "".join(b)


def house(x, y, w, h, roof, win=True):
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#e8dcc8"/>'
         f'<path d="M{x-5} {y}L{x+w/2} {y-h*0.7}L{x+w+5} {y}Z" fill="{roof}"/>')
    if win:
        s += f'<rect class="tw" x="{x+w/2-4}" y="{y+h*0.3}" width="8" height="8" fill="#FFD866"/>'
    return s


def m_planet(c):
    cx, cy = PX + PW/2, PY + 150
    b = [f'<circle class="tw" {d(i*0.4)} cx="{PX+30+(i*97)%540}" cy="{PY+20+(i*53)%110}" r="1.6" fill="#fff"/>' for i in range(14)]
    g = [f'<path d="M{cx-190} {cy}Q{cx} {cy+190} {cx+190} {cy}Z" fill="#3b3350"/>',
         f'<path d="M{cx-120} {cy+30}Q{cx} {cy+120} {cx+110} {cy+30}" fill="none" stroke="#2a2440" stroke-width="10"/>',
         f'<ellipse cx="{cx}" cy="{cy}" rx="190" ry="34" fill="#5fbf7a"/>',
         f'<ellipse cx="{cx}" cy="{cy-4}" rx="176" ry="26" fill="#7ed492"/>',
         f'<path d="M{cx-150} {cy+2}Q{cx-40} {cy-16} {cx+40} {cy+4}T{cx+160} {cy-2}" fill="none" stroke="#d9c79f" stroke-width="5"/>']
    g.append(house(cx-120, cy-40, 34, 28, "#ff7b72"))
    g.append(house(cx-60, cy-52, 40, 34, c))
    g.append(house(cx+10, cy-44, 30, 26, "#FFA657"))
    g.append(house(cx+70, cy-56, 44, 38, "#39D3BB"))
    for tx, ty in [(cx-158, cy-14), (cx+136, cy-16), (cx-14, cy-8)]:
        g.append(f'<rect x="{tx-2}" y="{ty}" width="4" height="12" fill="#6b4f3a"/><circle cx="{tx}" cy="{ty-6}" r="11" fill="#3f9c5a"/>')
    b.append('<g class="bob">' + "".join(g) + "</g>")
    b.append(f'<g class="drift"><ellipse cx="{PX+120}" cy="{PY+60}" rx="36" ry="10" fill="#fff" opacity=".18"/>'
             f'<ellipse cx="{PX+470}" cy="{PY+84}" rx="44" ry="11" fill="#fff" opacity=".14"/></g>')
    b.append(T("9 个室内场景 · 旅行地图 · 摄影作品集", PX+PW/2, PY+272, 14, "sans", MUTED, "middle"))
    return "".join(b)


def m_tx(c):
    base, b = PY + 236, []
    cols = ["#7EE787", "#d6c65b", "#FFA657", "#ff7b72"]
    data = [[40, 30, 20], [52, 24, 34], [36, 40, 18], [60, 28, 40], [44, 22, 26], [70, 36, 48], [38, 30, 22], [56, 34, 30]]
    for i, segs in enumerate(data):
        x, y = PX + 70 + i * 62, base
        parts = []
        for j, h in enumerate(segs):
            y -= h
            parts.append(f'<rect x="{x}" y="{y}" width="38" height="{h-2}" rx="3" fill="{cols[min(3, (h//18))]}" opacity=".9"/>')
        b.append(f'<g class="grow" {d(i*0.12)}>' + "".join(parts) + "</g>")
        b.append(T(f"{i+3}月", x+19, base+22, 12, "sans", DIM, "middle"))
    b.append(f'<path d="M{PX+56} {PY+118}H{PX+PW-40}" stroke="{c}" stroke-dasharray="6 6" stroke-width="1.5"/>')
    b.append(T("budget", PX+PW-40, PY+110, 12, "mono", c, "end"))
    b.append(f'<path d="M{PX+56} {base}H{PX+PW-40}" stroke="{LINE}"/>')
    hx, hy = PX + 70 + 5*62 + 19, base - 154
    b.append(f'<g class="bob"><rect x="{hx-14}" y="{hy-6}" width="28" height="8" rx="4" fill="#fff"/>'
             f'<path d="M{hx+6} {hy+6}l0 22 6-6 8 12 5-3-8-11 9-1z" fill="#fff" stroke="{BG}" stroke-width="1.5"/></g>')
    b.append(T("拖一拖，改一笔 · Ctrl+Z 撤销", PX+56, PY+40, 13, "sans", MUTED))
    return "".join(b)


def m_diet(c):
    b = [f'<rect x="{PX+36}" y="{PY+40}" width="250" height="208" rx="10" fill="#161b22" stroke="{LINE}"/>',
         f'<circle cx="{PX+161}" cy="{PY+144}" r="80" fill="#e9e4da"/><circle cx="{PX+161}" cy="{PY+144}" r="62" fill="#f6f2ea"/>',
         f'<path d="M{PX+110} {PY+150}q20-40 60-28 10 22-14 40-46-12z" fill="#e3a86b"/>',
         f'<ellipse cx="{PX+196}" cy="{PY+130}" rx="34" ry="24" fill="#fff" stroke="#e0d9cc"/>',
         f'<circle cx="{PX+150}" cy="{PY+184}" r="10" fill="#6fbf5f"/><circle cx="{PX+170}" cy="{PY+190}" r="8" fill="#5aa84f"/>']
    for i, (x, y, w, h, label) in enumerate([(96, 110, 92, 72, "鸡胸肉 165 kcal"), (156, 98, 84, 58, "米饭 230 kcal")]):
        b.append(f'<g class="fade" {d(i*0.6)}><rect x="{PX+x}" y="{PY+y}" width="{w}" height="{h}" fill="none" stroke="{c}" stroke-width="2"/>'
                 f'<rect x="{PX+x}" y="{PY+y-24}" width="{width(label,12)+14:.0f}" height="22" fill="{c}"/>'
                 + T(label, PX+x+7, PY+y-8, 12, "sansm", BG) + "</g>")
    rx, ry, r = PX + 430, PY + 118, 70
    circ = 2 * 3.14159 * r
    b.append(f'<circle cx="{rx}" cy="{ry}" r="{r}" fill="none" stroke="#21262d" stroke-width="14"/>')
    b.append(f'<circle cx="{rx}" cy="{ry}" r="{r}" fill="none" stroke="{c}" stroke-width="14" stroke-linecap="round" '
             f'stroke-dasharray="{circ*0.66:.0f} {circ:.0f}" transform="rotate(-90 {rx} {ry})"/>')
    b.append(T("1,840", rx, ry+6, 30, "monob", INK, "middle"))
    b.append(T("/ 2,800 kcal", rx, ry+30, 13, "mono", MUTED, "middle"))
    b.append(T("蛋白质  128 / 160 g", PX+346, PY+232, 14, "sans", MUTED))
    b.append(f'<rect x="{PX+346}" y="{PY+244}" width="180" height="8" rx="4" fill="#21262d"/>'
             f'<rect class="wide" x="{PX+346}" y="{PY+244}" width="144" height="8" rx="4" fill="{c}"/>')
    return "".join(b)


def m_arena(c):
    b = [f'<rect x="{PX+40}" y="{PY+26}" width="{PW-80}" height="36" rx="8" fill="#161b22" stroke="{LINE}"/>',
         T("› a shrimp astronaut, watercolor", PX+56, PY+50, 15, "mono", MUTED),
         f'<rect class="cur" x="{PX+56+width("› a shrimp astronaut, watercolor",15,"mono")+4:.0f}" y="{PY+36}" width="8" height="17" fill="{c}"/>',
         '<defs><linearGradient id="ga" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2b5876"/><stop offset="1" stop-color="#4e4376"/></linearGradient>'
         '<linearGradient id="gb" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#ee9ca7"/><stop offset="1" stop-color="#ffdde1"/></linearGradient></defs>']
    for k, (x, grad, pct) in enumerate([(40, "ga", 62), (342, "gb", 38)]):
        X = PX + x
        b.append(f'<rect x="{X}" y="{PY+78}" width="220" height="150" rx="8" fill="url(#{grad})"/>')
        b.append(f'<circle cx="{X+110}" cy="{PY+146}" r="36" fill="#fff" opacity=".85"/><circle cx="{X+110}" cy="{PY+146}" r="24" fill="#9fd3ff" opacity=".8"/>'
                 f'<path d="M{X+80} {PY+186}q30-24 60 0" fill="none" stroke="#ff8a65" stroke-width="10" stroke-linecap="round"/>')
        b.append(T("模型 A ?" if k == 0 else "模型 B ?", X+12, PY+100, 13, "monob", "#fff"))
        b.append(f'<rect x="{X}" y="{PY+244}" width="220" height="10" rx="5" fill="#21262d"/>'
                 f'<rect class="wide" {d(k*0.3)} x="{X}" y="{PY+244}" width="{220*pct/100:.0f}" height="10" rx="5" fill="{c if k == 0 else DIM}"/>')
        b.append(T(f"{pct}%", X+220, PY+276, 14, "monob", c if k == 0 else MUTED, "end"))
    b.append(T("VS", PX+PW/2, PY+164, 30, "monob", c, "middle"))
    return "".join(b)


def m_triz(c):
    b, hot = [], {1: 0, 35: 1.2, 40: 2.4, 13: 3.6}
    b.append(chip(PX+40, PY+24, "矛盾：更轻  ↔  更坚固", c)[0])
    for n in range(40):
        col, row = n % 10, n // 10
        x, y = PX + 40 + col * 53, PY + 68 + row * 44
        b.append(f'<rect x="{x}" y="{y}" width="45" height="36" rx="6" fill="#161b22" stroke="{LINE}"/>')
        b.append(T(f"{n+1:02d}", x+22.5, y+23, 14, "mono", DIM, "middle"))
        if n + 1 in hot:
            b.append(f'<rect class="lit" {d(hot[n+1])} x="{x}" y="{y}" width="45" height="36" rx="6" fill="{c}"/>')
    b.append(T("→  01 分割 · 35 参数变化 · 40 复合材料", PX+40, PY+270, 15, "sans", INK))
    return "".join(b)


def m_maimai(c):
    cx, cy, R = PX + 150, PY + 144, 104
    b = [f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#161b22" stroke="{c}" stroke-width="3"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{R-16}" fill="none" stroke="{LINE}"/>']
    import math
    for i in range(8):
        a = math.radians(22.5 + i * 45)
        x, y = cx + R * math.sin(a), cy - R * math.cos(a)
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="{c}" opacity=".85"/>')
        b.append(f'<g class="out" style="transform-origin:{cx}px {cy}px;animation-delay:{-i*0.3:.1f}s">'
                 f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="none" stroke="#fff" stroke-width="3"/></g>')
    b.append(T("maimai", cx, cy+7, 20, "monob", c, "middle"))
    heads = ["版本", "等级", "谱师", "BPM", "流派"]
    colors = [["#3fb950", "#d29922", DIM, "#d29922", DIM], ["#3fb950", "#3fb950", "#d29922", DIM, "#3fb950"],
              ["#3fb950"] * 5]
    for j, h in enumerate(heads):
        b.append(T(h, PX + 328 + j * 52 + 22, PY + 58, 12, "sans", MUTED, "middle"))
    for i, row in enumerate(colors):
        for j, col in enumerate(row):
            x, y = PX + 328 + j * 52, PY + 72 + i * 52
            b.append(f'<rect class="fade" {d(i*0.9+j*0.12)} x="{x}" y="{y}" width="44" height="44" rx="6" fill="{col}"/>')
    b.append(T("猜歌 · 算分 · 上分", PX + 328 + 128, PY + 260, 14, "sans", INK, "middle"))
    return "".join(b)


PROJECTS = [
    # key, accent, index, name, kicker, zh, en, tags, status, mockup
    ("bp", "#FFA657", "01", "BP-Parser", "AI 创投工具", "一份 BP 丢进来，一条投资记录走出去。",
     "Drop in a pitch deck, get a structured deal record out.", ["Chrome 扩展", "Claude", "飞书"], ["PUBLIC"], m_bp),
    ("lyrics", "#39D3BB", "02", "Lyrics Parser", "学日语", "每一句歌词，都是一堂日语课。",
     "Every lyric is a Japanese lesson: furigana, romaji, grammar.", ["Next.js", "Claude", "小程序"], ["LIVE", "PUBLIC"], m_lyrics),
    ("planet", "#A493FF", "03", "Little Planet", "个人说明书", "一座可以走进去的漂浮小镇。",
     "A personal manual you can walk into: a floating 3D town.", ["Three.js", "R2", "摄影"], ["PRIVATE", "WIP"], m_planet),
    ("tx", "#7EE787", "04", "ShrimpTransactions", "生活 · 记账", "把每一笔钱，堆成看得见的柱子。",
     "Every expense stacked into bars you can drag around.", ["D3.js", "Supabase", "Next.js"], ["LIVE", "PUBLIC"], m_tx),
    ("diet", "#FF7B72", "05", "ShrimpDiet", "生活 · 增肌", "拍一张饭，算出离增肌还差多少。",
     "Snap your meal; a VLM counts what's left to bulk.", ["VLM", "每日提醒", "卡路里"], ["PRIVATE"], m_diet),
    ("arena", "#D2A8FF", "06", "Image Gen Arena", "AI 实验", "同一句提示词，让模型们盲选对决。",
     "One prompt, blind side-by-side battles between image models.", ["Replicate", "盲测", "投票"], ["PUBLIC"], m_arena),
    ("triz", "#F2CF1D", "07", "ShrimpTRIZ", "AI 思考工具", "卡住的问题，交给 40 条发明原理。",
     "Stuck on a problem? Let 40 inventive principles have a go.", ["AutoTRIZ", "Claude", "Next.js"], ["LIVE"], m_triz),
    ("maimai", "#FF6BC1", "08", "maimai toolkit", "音游", "音游玩家的工具箱：猜歌、算分、上分。",
     "A rhythm gamer's toolkit: guess songs, calc scores, climb.", ["Wordle-like", "马赛克猜歌", "算分器"], ["LIVE", "PUBLIC"], m_maimai),
]


def card(p):
    key, c, idx, name, kicker, zh, en, tags, status, mock = p
    b = [f'<rect x="1" y="1" width="{W-2}" height="358" rx="14" fill="{CARD}" stroke="{LINE}"/>',
         f'<rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="10" fill="{PANEL}" stroke="{LINE}"/>',
         f'<rect x="1" y="40" width="4" height="64" rx="2" fill="{c}"/>']
    b.append(T(f"#{idx}  ·  {kicker}", 52, 72, 14, "mono", c))
    size = min(48, 540 / width(name, 1, "monob"))
    b.append(T(name, 50, 136, size, "monob"))
    b.append(T(zh, 52, 190, 24, "sansb"))
    b.append(T(en, 52, 222, 15, "sans", MUTED))
    x = 52
    for t in tags:
        s, w = chip(x, 256, t, MUTED)
        b.append(s)
        x += w + 8
    x = 52
    for s_ in status:
        col = {"LIVE": c, "PUBLIC": MUTED, "PRIVATE": "#ff7b72", "WIP": "#d29922"}[s_]
        s, w = chip(x, 296, ("● " if s_ == "LIVE" else "") + s_, col, s_ == "LIVE")
        b.append(s)
        x += w + 8
    b.append(mock(c))
    return svg(360, f"{name}：{zh} {en}", "".join(b))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    files = {"header.svg": header(), "footer.svg": footer(), "divider-end.svg": divider("#FFA657")}
    for p in PROJECTS:
        files[f"card-{p[0]}.svg"] = card(p)
        files[f"divider-{p[0]}.svg"] = divider(p[1])
    for n, s in files.items():
        with open(os.path.join(OUT, n), "w", encoding="utf-8") as f:
            f.write(s)
        print(f"{n:24s} {len(s)//1024:>4d} KB")
