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
    "@keyframes wide{0%,6%{transform:scaleX(0)}24%,86%{transform:scaleX(1)}96%,100%{transform:scaleX(0)}}"
    ".wide{transform-box:fill-box;transform-origin:left center;animation:wide 8s cubic-bezier(.6,0,.2,1) infinite}"
    "@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}.bob{animation:bob 5s ease-in-out infinite}"
    "@keyframes tw{0%,100%{opacity:.15}50%{opacity:.9}}.tw{animation:tw 3s ease-in-out infinite}"
    "@keyframes drift{from{transform:translateX(-40px)}to{transform:translateX(40px)}}.drift{animation:drift 9s ease-in-out infinite alternate}"
    "@keyframes lit{0%,100%{opacity:.08}12%,40%{opacity:1}}.lit{animation:lit 6s ease-in-out infinite}"
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
    for i, (label, color) in enumerate([("#1 FUNDING", "#FFA657"), ("#2 DAILY", "#58A6FF"),
                                         ("#3 GOLF", "#7EE787"), ("#4 学日语", "#39D3BB")]):
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



def m_funding(c):
    b = [f'<rect x="{PX}" y="{PY}" width="{PW}" height="34" rx="10" fill="#161b22"/>',
         f'<path d="M{PX} {PY+34}H{PX+PW}" stroke="{LINE}"/>']
    b += [f'<circle cx="{PX+20+i*16}" cy="{PY+17}" r="5" fill="{col}"/>' for i, col in enumerate(["#ff7b72", "#d29922", "#3fb950"])]
    b.append(T("$ tail -f svtr/funding.log", PX+78, PY+22, 13, "mono", MUTED))
    b.append(T("TOP 5 · 7 DAYS", PX+PW-20, PY+22, 12, "monob", c, "end"))
    sectors = ["算力", "大模型", "机器人", "生命科学", "智能体"]
    for i, (sector, amt) in enumerate(zip(sectors, [1.0, .62, .44, .33, .25])):
        y = PY + 62 + i * 38
        row = [T(f"{i+1:02d}", PX+24, y+16, 13, "monob", c),
               f'<rect x="{PX+56}" y="{y+5}" width="{[132, 108, 150, 96, 120][i]}" height="12" rx="6" fill="{INK}" opacity=".85"/>',
               f'<rect x="{PX+222}" y="{y}" width="{width(sector,12)+18:.0f}" height="22" rx="11" fill="none" stroke="{LINE}"/>',
               T(sector, PX+231, y+15, 12, "sans", MUTED),
               f'<rect x="{PX+322}" y="{y+5}" width="200" height="12" rx="6" fill="#21262d"/>',
               f'<rect class="wide" {d(0.3+i*0.25)} x="{PX+322}" y="{y+5}" width="{200*amt:.0f}" height="12" rx="6" fill="{c}" opacity="{1-i*.13:.2f}"/>',
               T("$", PX+PW-24, y+16, 13, "monob", c, "end")]
        b.append(f'<g class="fade" {d(i*0.35)}>' + "".join(row) + "</g>")
    b.append(f'<circle class="pulse" cx="{PX+30}" cy="{PY+260}" r="5" fill="{c}"/><circle cx="{PX+30}" cy="{PY+260}" r="4" fill="{c}"/>')
    b.append(T("每天 09:00 PT 自动刷新 · via svtr.ai MCP", PX+46, PY+265, 13, "sans", MUTED))
    return "".join(b)

def m_bpskill(c):
    b = [f'<rect x="{PX+32}" y="{PY+44}" width="118" height="164" rx="8" fill="#161b22" stroke="{LINE}"/>',
         f'<path d="M{PX+124} {PY+44}v26h26" fill="none" stroke="{LINE}"/>',
         T("deck.pdf", PX+46, PY+72, 13, "monob", c)]
    b += [f'<rect x="{PX+46}" y="{PY+90+i*18}" width="{[86,70,90,58,80,66][i]}" height="5" rx="2.5" fill="{DIM}"/>' for i in range(6)]
    b.append(f'<path d="M{PX+160} {PY+126}h22m-8-7 8 7-8 7" fill="none" stroke="{c}" stroke-width="2"/>')
    claims = [("C1", "ARR $1.2M", "已核实", "#3fb950"), ("C2", "500 强试点", "查不到", "#8b949e"),
              ("C3", "CEO 前大厂", "已核实", "#3fb950"), ("C4", "月增 20%", "对不上", "#ff7b72")]
    for i, (k, text, status, col) in enumerate(claims):
        y = PY + 44 + i * 42
        b.append(f'<g class="fade" {d(i*0.45)}><rect x="{PX+192}" y="{y}" width="208" height="34" rx="7" fill="#161b22" stroke="{LINE}"/>'
                 + T(k, PX+204, y+22, 12, "monob", DIM) + T(text, PX+232, y+22, 13, "sans", INK)
                 + f'<circle cx="{PX+342}" cy="{y+17}" r="4" fill="{col}"/>' + T(status, PX+390, y+22, 12, "sansm", col, "end") + "</g>")
    for i, (k, v) in enumerate([("团队", 7), ("市场", 6), ("产品", 7), ("牵引", 4), ("壁垒", 5)]):
        y = PY + 52 + i * 30
        b.append(T(k, PX+424, y+10, 12, "sans", MUTED))
        b.append(f'<rect x="{PX+458}" y="{y+1}" width="100" height="10" rx="5" fill="#21262d"/>'
                 f'<rect class="wide" {d(1.8+i*0.2)} x="{PX+458}" y="{y+1}" width="{v*10}" height="10" rx="5" fill="{c}"/>')
        b.append(T(str(v), PX+574, y+10, 12, "monob", INK, "end"))
    b.append(f'<g class="fade" {d(3)}>' + chip(PX+424, PY+212, "继续观察 · 6.1", c, True)[0] + "</g>")
    b.append(T("8 条主张 · 23 个来源 · 6 个尽调问题", PX+32, PY+262, 13, "sans", MUTED))
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




def m_daily(c):
    b = [f'<rect x="{PX+36}" y="{PY+34}" width="{PW-72}" height="58" rx="12" fill="#161b22" stroke="{c}" stroke-opacity=".6"/>']
    txt = "午饭牛肉面 18，4 点到 6 点健身，周五前交水电费"
    b.append(f'<g class="fade">' + T(txt, PX+56, PY+70, 17, "sans", INK) + "</g>")
    b.append(f'<rect class="cur" x="{PX+56+width(txt,17,"sans")+4:.0f}" y="{PY+52}" width="9" height="24" fill="{c}"/>')
    hub_y = PY + 138
    b.append(f'<path d="M{PX+PW/2} {PY+92}V{hub_y-18}" stroke="{c}" stroke-width="2"/>')
    b.append(f'<rect x="{PX+PW/2-62}" y="{hub_y-18}" width="124" height="36" rx="18" fill="{c}"/>')
    b.append(T("Claude 中枢", PX+PW/2, hub_y+6, 15, "sansb", BG, "middle"))
    dests = [("饮食", "牛肉面 32g 蛋白"), ("花费", "$18 · 餐饮"), ("时间线", "16:00–18:00 健身"), ("待办", "交水电费 周五")]
    cw = (PW - 72 - 3 * 12) / 4
    for i, (k, v) in enumerate(dests):
        x = PX + 36 + i * (cw + 12)
        b.append(f'<path d="M{PX+PW/2} {hub_y+18}C{PX+PW/2} {hub_y+50} {x+cw/2:.0f} {hub_y+40} {x+cw/2:.0f} {hub_y+74}" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
        b.append(f'<g class="fade" {d(0.6+i*0.45)}><rect x="{x:.0f}" y="{hub_y+74}" width="{cw:.0f}" height="66" rx="10" fill="#161b22" stroke="{LINE}"/>'
                 + T(k, x+14, hub_y+100, 14, "sansb", c) + T(v, x+14, hub_y+124, 12.5, "sans", MUTED) + "</g>")
    return "".join(b)


def m_golf(c):
    b = [f'<rect x="{PX+1}" y="{PY+150}" width="{PW-2}" height="{PH-151}" rx="0" fill="{c}" opacity=".07"/>',
         f'<path d="M{PX} {PY+150}H{PX+PW}" stroke="{LINE}"/>']
    b.append(chip(PX+28, PY+24, "HOLE 4 · PAR 4 · 288 YDS", c, True)[0])
    for i in range(15):
        b.append(f'<rect x="{PX+30+i*14+(8 if i >= 9 else 0)}" y="{PY+62}" width="10" height="4" rx="2" '
                 f'fill="{c if i == 3 else INK}" opacity="{1 if i == 3 else .7 if i < 3 else .2}"/>')
    bx, by = PX + 170, PY + 238
    b.append(f'<path d="M{bx-4} {by-6}A50 70 0 1 1 {bx+44} {by-98}" fill="none" stroke="{c}" stroke-width="4" opacity=".9"/>')
    b.append(f'<g class="fade" {d(0.8)}><path d="M{bx} {by}C{bx+40} {by-220} {bx+170} {by-200} {bx+200} {by-90}" fill="none" stroke="#ff7b72" stroke-width="3.5"/>'
             f'<circle cx="{bx+200}" cy="{by-90}" r="4" fill="#ff7b72"/>'
             + T("BALL TRACKED", bx+110, by-58, 12, "monob", "#ff7b72") + "</g>")
    b.append(f'<circle cx="{bx}" cy="{by}" r="5" fill="{INK}"/>')
    cx0, cy0 = PX + 400, PY + 96
    b.append(f'<rect x="{cx0}" y="{cy0}" width="174" height="170" rx="10" fill="#161b22" stroke="{LINE}"/>')
    b.append(T("TEE SHOT", cx0+14, cy0+24, 12, "monob", c) + T("EST.", cx0+160, cy0+24, 11, "mono", DIM, "end"))
    b.append(T("DRIVER", cx0+14, cy0+54, 22, "monob"))
    for i, (k, v) in enumerate([("BALL", "132 mph"), ("CARRY", "214 yds"), ("TEMPO", "3.1 : 1")]):
        y = cy0 + 86 + i * 30
        b.append(f'<path d="M{cx0+14} {y-14}H{cx0+160}" stroke="{LINE}"/>')
        b.append(T(k, cx0+14, y+4, 12, "mono", MUTED))
        b.append(f'<g class="fade" {d(1.4+i*0.4)}>' + T(v, cx0+160, y+4, 15, "monob", INK, "end") + "</g>")
    b.append(T("70 段原片 → 20 分钟整场 vlog", PX+PW-28, PY+40, 13, "mono", DIM, "end"))
    return "".join(b)


PROJECTS = [
    # key, accent, index, name, kicker, zh, en, tags, status, mockup
    ("funding", "#FFA657", "00", "funding.log", "SVTR 创投数据", "每天早上，最大的 AI 融资自动送到这里。",
     "The week's biggest AI rounds, refreshed here every morning.", ["SVTR MCP", "GitHub Action", "每日刷新"], ["LIVE"], m_funding),
    ("daily", "#58A6FF", "01", "izzy · daily", "个人每日面板", "一句话进来，全部归位。",
     "One sentence in: meals, spending, to-dos and schedule all filed.", ["Claude Artifact", "MCP", "单文件 HTML"], ["PUBLIC"], m_daily),
    ("golf", "#7EE787", "02", "golf-course-vlog-skill", "Claude Skill", "一场球的原片丢进来，一条整场 vlog 走出去。",
     "Raw round footage in, a full-course vlog with broadcast UI out.", ["Claude Code", "YOLO Pose", "ffmpeg"], ["PUBLIC"], m_golf),
    ("bpskill", "#F78166", "03", "bp-parser-skill", "Claude Skill", "一份 BP 丢进来，一份有出处的研究报告走出去。",
     "Pitch deck in, an evidence-backed research report out.", ["WebSearch", "主张核实", "五维打分"], ["PUBLIC"], m_bpskill),
    ("lyrics", "#39D3BB", "04", "Lyrics Parser", "学日语", "每一句歌词，都是一堂日语课。",
     "Every lyric is a Japanese lesson: furigana, romaji, grammar.", ["Next.js", "Claude", "小程序"], ["LIVE", "PUBLIC"], m_lyrics),
    ("triz", "#F2CF1D", "05", "ShrimpTRIZ", "AI 思考工具", "卡住的问题，交给 40 条发明原理。",
     "Stuck on a problem? Let 40 inventive principles have a go.", ["AutoTRIZ", "Claude", "Next.js"], ["LIVE"], m_triz),
    ("planet", "#A493FF", "06", "Little Planet", "个人说明书", "一座可以走进去的漂浮小镇。",
     "A personal manual you can walk into: a floating 3D town.", ["Three.js", "R2", "摄影"], ["PRIVATE", "WIP"], m_planet),
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
