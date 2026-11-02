"""Kopfgrafik des GitHub-Profils: assets/hero.svg (1200×400, eine Variante).

Aufbau
  - Fläche: abgerundetes Rechteck mit lila Verlauf, dezentes Punktraster,
    drei weiche Lichtflächen, die langsam driften
  - links: Logo „BW.Tech“ mit Slogan „Cloud by Design“ (exakt aus dem Profilbild),
    Unterzeile und drei Pillen
  - rechts: abstrakte Cloud-Infrastruktur – Wolken-Kontur, Knoten mit den
    Website-Icons, Verbindungen mit wandernden Datenpunkten, Orbit um den Hauptknoten,
    darunter ein Server-Einschub als Bezug zum Rechenzentrum

Aufruf: cd C:/git/BWTECH-github && python src/hero.py
"""
from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from brand import (  # noqa: E402
    LAVENDER, LAVENDER_LIGHT, PURPLE, PURPLE_DEEP, VIOLET, VIOLET_SOFT, WHITE,
    icon, logo_part, logo_part_box, svg_doc, tagline_word, write_asset,
)
from textpath import Font, GlyphDefs  # noqa: E402

W, H = 1200, 400
EASE = 'cubic-bezier(.2,.8,.2,1)'
EASE_IO = 'cubic-bezier(.45,0,.55,1)'

defs = GlyphDefs('h')
F400 = Font('Lexend', 400)
F500 = Font('Lexend', 500)


def f(v: float) -> str:
    """Zahl kompakt formatieren (spart Bytes, vermeidet -0)."""
    s = f'{v:.2f}'.rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


# ---------------------------------------------------------------------------
# Raster und Maße
# ---------------------------------------------------------------------------
PAD_X = 72                 # linke Kante aller Inhalte (Stamm des „B“)
LOGO_S = 1.45              # Logo-Skalierung
LOGO_TOP = 40              # Oberkante „B“

SUB_SIZE = 26              # Unterzeile
SUB_LEAD = 34
SUB_Y1 = 258               # Grundlinie Zeile 1
SUB_LINES = ('Maßgeschneiderte Cloud-Lösungen,', 'die Sie voranbringen.')

PILL_SIZE = 22
PILL_H = 40
PILL_R = 20
PILL_PAD = 18
PILL_GAP = 12
PILL_Y = 316
PILLS = ('Persönliche Beratung', 'Rechenzentrum in Deutschland', 'DSGVO-konform')


# ---------------------------------------------------------------------------
# Hintergrund
# ---------------------------------------------------------------------------
def background() -> tuple[str, str, str]:
    d = (
        f'<clipPath id="hcard"><rect width="{W}" height="{H}" rx="24"/></clipPath>'
        f'<linearGradient id="hbg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{PURPLE}"/><stop offset="1" stop-color="{PURPLE_DEEP}"/>'
        f'</linearGradient>'
        # weiche Lichtfläche (statisch, kein Filter)
        f'<radialGradient id="hglow">'
        f'<stop offset="0" stop-color="{VIOLET}" stop-opacity=".55"/>'
        f'<stop offset=".45" stop-color="{VIOLET}" stop-opacity=".18"/>'
        f'<stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>'
        f'</radialGradient>'
        # Punktraster
        f'<pattern id="hdots" width="24" height="24" patternUnits="userSpaceOnUse">'
        f'<circle cx="12" cy="12" r="1.15" fill="{LAVENDER}"/></pattern>'
        # Raster nur rechts sichtbar, weich auslaufend – Textbereich bleibt ruhig
        f'<radialGradient id="hdm" cx="930" cy="170" r="560" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="#fff"/><stop offset=".55" stop-color="#fff" stop-opacity=".5"/>'
        f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        f'<mask id="hdmask"><rect width="{W}" height="{H}" fill="url(#hdm)"/></mask>'
    )
    body = (
        f'<rect width="{W}" height="{H}" rx="24" fill="url(#hbg)"/>'
        f'<g clip-path="url(#hcard)">'
        f'<circle class="gl gl1" cx="980" cy="120" r="380" fill="url(#hglow)" opacity=".55"/>'
        f'<circle class="gl gl2" cx="140" cy="430" r="420" fill="url(#hglow)" opacity=".35"/>'
        f'<circle class="gl gl3" cx="600" cy="-60" r="300" fill="url(#hglow)" opacity=".25"/>'
        f'<rect width="{W}" height="{H}" fill="url(#hdots)" opacity=".16" mask="url(#hdmask)"/>'
        f'</g>'
        # feine Innenkontur – auf GitHub-Dunkel sauber abgesetzt
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="23.5" fill="none" '
        f'stroke="#fff" stroke-opacity=".08"/>'
    )
    css = (
        '.gl{transform-box:view-box;transform-origin:0 0}'
        '.gl1{animation:hdr1 22s ease-in-out infinite alternate}'
        '.gl2{animation:hdr2 18s ease-in-out infinite alternate}'
        '.gl3{animation:hdr3 24s ease-in-out infinite alternate}'
        '@keyframes hdr1{to{transform:translate(-90px,40px)}}'
        '@keyframes hdr2{to{transform:translate(120px,-30px)}}'
        '@keyframes hdr3{to{transform:translate(80px,50px)}}'
    )
    return d, body, css


# ---------------------------------------------------------------------------
# Logo-Lockup
# ---------------------------------------------------------------------------
def lockup() -> tuple[str, str, str]:
    bx0, by0 = logo_part_box('B')[:2]
    ox = PAD_X - bx0 * LOGO_S
    oy = LOGO_TOP - by0 * LOGO_S

    # Wortmarke: Buchstaben steigen aus der Grundlinie auf (Clip = Rechteck bis knapp unter die Grundlinie)
    letters = []
    for i, name in enumerate(('B', 'W', 'dot', 'T', 'e', 'c', 'h')):
        delay = 0.05 + i * 0.065
        letters.append(f'<g class="lt" style="animation-delay:{delay:.3f}s">{logo_part(name)}</g>')
    words = []
    for i, w in enumerate(('Cloud', 'by', 'Design')):
        delay = 0.95 + i * 0.15
        words.append(f'<g class="wd" style="animation-delay:{delay:.2f}s">{tagline_word(w)}</g>')

    clip_slogan = ''.join(tagline_word(w) for w in ('Cloud', 'by', 'Design'))
    d = (
        f'<clipPath id="hwm"><rect x="0" y="-20" width="379" height="98.4"/></clipPath>'
        f'<clipPath id="hsl">{clip_slogan}</clipPath>'
        f'<linearGradient id="hshg" x1="0" x2="1" y1="0" y2="0">'
        f'<stop offset="0" stop-color="{VIOLET_SOFT}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{VIOLET_SOFT}" stop-opacity=".6"/>'
        f'<stop offset="1" stop-color="{VIOLET_SOFT}" stop-opacity="0"/>'
        f'</linearGradient>'
    )
    body = (
        f'<g transform="translate({f(ox)} {f(oy)}) scale({LOGO_S})" fill="{WHITE}">'
        f'<g clip-path="url(#hwm)">{"".join(letters)}</g>'
        f'{"".join(words)}'
        # Lichtschimmer über dem Slogan (nur innerhalb der Buchstaben sichtbar)
        f'<g clip-path="url(#hsl)"><g class="sh">'
        f'<rect x="-84" y="86" width="72" height="44" fill="url(#hshg)" transform="skewX(-18)"/>'
        f'</g></g>'
        f'</g>'
    )
    css = (
        f'.lt{{transform-box:fill-box;transform-origin:50% 100%;'
        f'animation:hrise .7s {EASE} both}}'
        f'@keyframes hrise{{from{{opacity:0;transform:translateY(110%)}}60%{{opacity:1}}'
        f'to{{opacity:1;transform:none}}}}'
        f'.wd{{transform-box:fill-box;transform-origin:50% 100%;animation:hup .6s {EASE} both}}'
        f'@keyframes hup{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}'
        f'.sh{{transform-box:view-box;transform-origin:0 0;opacity:0;'
        f'animation:hsh 8s {EASE_IO} 2.4s infinite}}'
        f'@keyframes hsh{{0%{{opacity:0;transform:translateX(0)}}3%,21%{{opacity:1}}'
        f'24%,100%{{opacity:0;transform:translateX(450px)}}}}'
    )
    return d, body, css


# ---------------------------------------------------------------------------
# Unterzeile und Pillen
# ---------------------------------------------------------------------------
def copy_block() -> tuple[str, str]:
    parts = []
    for i, line in enumerate(SUB_LINES):
        x0 = F400.bounds(line, SUB_SIZE)[0]
        g = F400.text(line, SUB_SIZE, PAD_X - x0, SUB_Y1 + i * SUB_LEAD, defs=defs,
                      attrs=f'fill="{LAVENDER}" class="fx" style="animation-delay:{1.3 + i * 0.1:.2f}s"')
        parts.append(g)

    x = PAD_X
    for i, label in enumerate(PILLS):
        tw = F500.measure(label, PILL_SIZE)
        w = tw + 2 * PILL_PAD
        cy = PILL_Y + PILL_H / 2
        base = cy + F500.cap_height / F500.upem * PILL_SIZE / 2
        txt = F500.text(label, PILL_SIZE, x + PILL_PAD, base, defs=defs, attrs=f'fill="{LAVENDER}"')
        parts.append(
            f'<g class="fx" style="animation-delay:{1.5 + i * 0.1:.2f}s">'
            f'<rect x="{f(x + .75)}" y="{f(PILL_Y + .75)}" width="{f(w - 1.5)}" height="{PILL_H - 1.5}" '
            f'rx="{PILL_R - .75}" fill="#fff" fill-opacity=".05" stroke="{LAVENDER}" stroke-opacity=".42" '
            f'stroke-width="1.5"/>{txt}</g>'
        )
        x += w + PILL_GAP
    css = f'.fx{{transform-box:fill-box;transform-origin:50% 50%;animation:hup .7s {EASE} both}}'
    return ''.join(parts), css


def pills_right() -> float:
    """Rechte Kante der Pillenreihe."""
    w = sum(F500.measure(t, PILL_SIZE) + 2 * PILL_PAD for t in PILLS)
    return PAD_X + w + PILL_GAP * (len(PILLS) - 1)


# ---------------------------------------------------------------------------
# Illustration: Cloud-Infrastruktur
# ---------------------------------------------------------------------------
# Wolke als Vereinigung dreier Kreise mit flacher Unterkante (Unterkanten von L und R gleich)
LOBE_L = (786.0, 214.0, 60.0)
LOBE_C = (920.0, 148.0, 108.0)
LOBE_R = (1054.0, 192.0, 82.0)
RACK = True                # Server-Einschub unter der Wolke (Bezug „Rechenzentrum“)


def _inter(c1, c2, upper=True):
    """Schnittpunkt zweier Kreise (der obere bzw. untere)."""
    x1, y1, r1 = c1
    x2, y2, r2 = c2
    dx, dy = x2 - x1, y2 - y1
    d = math.hypot(dx, dy)
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(max(r1 * r1 - a * a, 0))
    mx, my = x1 + a * dx / d, y1 + a * dy / d
    p1 = (mx + h * dy / d, my - h * dx / d)
    p2 = (mx - h * dy / d, my + h * dx / d)
    return min(p1, p2, key=lambda p: p[1]) if upper else max(p1, p2, key=lambda p: p[1])


def _ang(c, p):
    return math.atan2(p[1] - c[1], p[0] - c[0])


def _arc(c, p_from, p_to, sweep):
    """SVG-Bogen auf Kreis c von p_from nach p_to; liefert (Befehl, Länge)."""
    a0, a1 = _ang(c, p_from), _ang(c, p_to)
    delta = (a1 - a0) % (2 * math.pi) if sweep else (a0 - a1) % (2 * math.pi)
    large = 1 if delta > math.pi else 0
    r = c[2]
    return f'A{f(r)} {f(r)} 0 {large} {sweep} {f(p_to[0])} {f(p_to[1])}', r * delta


def cloud_halves(inset: float = 0.0):
    """Wolken-Kontur als zwei Hälften: von unten Mitte nach links bzw. rechts bis zum Scheitel."""
    L = (LOBE_L[0], LOBE_L[1], LOBE_L[2] - inset)
    C = (LOBE_C[0], LOBE_C[1], LOBE_C[2] - inset)
    R = (LOBE_R[0], LOBE_R[1], LOBE_R[2] - inset)
    bottom = L[1] + L[2]
    start = (C[0], bottom)
    top = (C[0], C[1] - C[2])
    p_lc = _inter(L, C)
    p_cr = _inter(C, R)
    l_bot = (L[0], bottom)
    r_bot = (R[0], bottom)

    a1, n1 = _arc(L, l_bot, p_lc, 1)
    a2, n2 = _arc(C, p_lc, top, 1)
    left = (f'M{f(start[0])} {f(start[1])}H{f(l_bot[0])}{a1}{a2}', (start[0] - l_bot[0]) + n1 + n2)
    b1, m1 = _arc(R, r_bot, p_cr, 0)
    b2, m2 = _arc(C, p_cr, top, 0)
    right = (f'M{f(start[0])} {f(start[1])}H{f(r_bot[0])}{b1}{b2}', (r_bot[0] - start[0]) + m1 + m2)
    return left, right


def cloud_bottom_y(x: float) -> float:
    """Unterkante der Wolke an Stelle x (für Anschlüsse nach unten)."""
    cx, cy, r = LOBE_R
    if x <= cx:
        return LOBE_L[1] + LOBE_L[2]
    return cy + math.sqrt(max(r * r - (x - cx) ** 2, 0))


# Knoten: Name -> (Icon, x, y, Radius, Icon-Größe)
NODES = {
    'hub': ('cloud', 920, 168, 44, 52),
    'backup': ('backup', 790, 220, 30, 32),
    'software': ('software', 1054, 204, 30, 32),
    'managed': ('managed', 700, 98, 28, 29),
    'ai': ('it', 1120, 76, 28, 29),
}
LINKS = [('hub', 'backup'), ('hub', 'software'), ('hub', 'managed'), ('hub', 'ai'),
         ('managed', 'backup'), ('ai', 'software')]
# Datenpunkte: (von, nach, Dauer, Verzögerung)
FLOWS = [
    ('managed', 'hub', 9.0, 2.3),
    ('hub', 'backup', 8.0, 3.5),
    ('software', 'hub', 10.0, 2.9),
    ('hub', 'ai', 11.0, 4.7),
    ('backup', 'managed', 12.0, 6.1),
    ('ai', 'software', 9.5, 5.3),
]

RACK_W, RACK_UNIT, RACK_GAP = 112, 11, 3.5


def _flow_dot(i: int, sx, sy, ex, ey, dur, delay) -> tuple[str, str]:
    """Datenpunkt auf gerader Strecke; Grundzustand (ohne Bewegung) = Mitte der Strecke."""
    mx, my = (sx + ex) / 2, (sy + ey) / 2
    el = (f'<circle class="dp" cx="{f(mx)}" cy="{f(my)}" r="3" '
          f'style="animation:hdp{i} {dur}s {delay}s infinite both"/>')
    css = (
        f'@keyframes hdp{i}{{'
        f'0%{{opacity:0;transform:translate({f(sx - mx)}px,{f(sy - my)}px);'
        f'animation-timing-function:{EASE_IO}}}'
        f'8%,38%{{opacity:1}}'
        f'46%,100%{{opacity:0;transform:translate({f(ex - mx)}px,{f(ey - my)}px)}}}}'
    )
    return el, css


def illustration() -> tuple[str, str, str]:
    d = (
        f'<radialGradient id="hhub">'
        f'<stop offset="0" stop-color="{VIOLET}" stop-opacity=".6"/>'
        f'<stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>'
    )
    css = []
    out = []

    # Wolken-Kontur (zeichnet sich von unten Mitte nach oben ein) und feine Innenlinie
    (lp, ll), (rp, rl) = cloud_halves()
    for cls, p, ln in (('cl1', lp, ll), ('cl2', rp, rl)):
        L = math.ceil(ln) + 2
        out.append(f'<path class="cl {cls}" d="{p}" style="stroke-dasharray:{L} {L}"/>')
        css.append(f'.{cls}{{animation:hd{cls} 1.7s {EASE} .2s both}}'
                   f'@keyframes hd{cls}{{from{{stroke-dashoffset:{L}}}to{{stroke-dashoffset:0}}}}')
    (lp2, _), (rp2, _) = cloud_halves(inset=13)
    out.append(f'<g class="ci"><path d="{lp2}"/><path d="{rp2}"/></g>')
    css.append(
        f'.cl{{fill:none;stroke:{LAVENDER};stroke-opacity:.9;stroke-width:2;stroke-linecap:round}}'
        f'.ci{{fill:none;stroke:{LAVENDER};stroke-opacity:.3;stroke-width:1.25;stroke-dasharray:2 7;'
        f'stroke-linecap:round;animation:hfade 1s ease-out 1.2s both}}'
        f'@keyframes hfade{{from{{opacity:0}}to{{opacity:1}}}}'
    )

    flows_el, flows_css = [], []

    # Server-Einschub unter der Wolke, mit Anschlussleitung
    if RACK:
        _, aix, _, air, _ = NODES['ai']
        rx1 = aix + air                       # rechte Kante bündig mit Knoten „ai“
        rx0 = rx1 - RACK_W
        ry0 = PILL_Y
        cx = (rx0 + rx1) / 2
        top_y = cloud_bottom_y(cx)
        units, leds = [], []
        for u in range(3):
            uy = ry0 + u * (RACK_UNIT + RACK_GAP)
            my = uy + RACK_UNIT / 2
            units.append(
                f'<rect x="{f(rx0 + .75)}" y="{f(uy + .75)}" width="{f(RACK_W - 1.5)}" '
                f'height="{f(RACK_UNIT - 1.5)}" rx="3"/>'
                f'<line x1="{f(rx0 + 32)}" y1="{f(my)}" x2="{f(rx1 - 12)}" y2="{f(my)}" class="rs"/>'
            )
            leds.append(
                f'<circle class="led" cx="{f(rx0 + 12)}" cy="{f(my)}" r="2" '
                f'style="animation-delay:{2.4 + u * 1.7:.1f}s"/>'
                f'<circle cx="{f(rx0 + 20)}" cy="{f(my)}" r="1.6" fill="{LAVENDER}" fill-opacity=".45"/>'
            )
        out.append(
            f'<g class="rk">'
            f'<line x1="{f(cx)}" y1="{f(top_y)}" x2="{f(cx)}" y2="{f(ry0)}" class="rc"/>'
            f'<g class="ru">{"".join(units)}</g>{"".join(leds)}</g>'
        )
        css.append(
            f'.rk{{animation:hfade .8s ease-out 1.5s both}}'
            f'.rc{{stroke:{LAVENDER};stroke-opacity:.38;stroke-width:1.25}}'
            f'.ru{{fill:#fff;fill-opacity:.04;stroke:{LAVENDER};stroke-opacity:.42;stroke-width:1.5}}'
            f'.rs{{stroke-dasharray:6 4;stroke-opacity:.3}}'
            f'.led{{fill:{VIOLET_SOFT};animation:hled 6s ease-in-out infinite alternate}}'
            f'@keyframes hled{{to{{opacity:.35}}}}'
        )
        e, c = _flow_dot(len(FLOWS), cx, ry0 - 2, cx, top_y + 2, 7.0, 3.1)
        flows_el.append(e)
        flows_css.append(c)

    # Verbindungen
    lines = []
    for a, b in LINKS:
        _, ax, ay, _, _ = NODES[a]
        _, bx, by, _, _ = NODES[b]
        lines.append(f'<line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}"/>')
    out.append(f'<g class="ln">{"".join(lines)}</g>')
    css.append(f'.ln{{stroke:{LAVENDER};stroke-opacity:.38;stroke-width:1.25;'
               f'animation:hfade .8s ease-out 1s both}}')

    # Glanz hinter dem Hauptknoten
    _, hx, hy, hr, _ = NODES['hub']
    out.append(f'<circle cx="{hx}" cy="{hy}" r="{hr * 2.5:.0f}" fill="url(#hhub)" class="gw"/>')
    css.append('.gw{animation:hfade 1s ease-out .6s both}')

    # Orbit (gestrichelt, rotiert langsam) mit zwei Trabanten
    orb_r = 70
    out.append(
        f'<g class="ob"><g class="obr">'
        f'<circle cx="{hx}" cy="{hy}" r="{orb_r}" fill="none" stroke="{LAVENDER}" stroke-opacity=".5" '
        f'stroke-width="1.25" stroke-dasharray="1.5 8" stroke-linecap="round"/>'
        f'<circle cx="{hx + orb_r}" cy="{hy}" r="3.5" fill="{LAVENDER_LIGHT}"/>'
        f'<circle cx="{hx - orb_r}" cy="{hy}" r="2.5" fill="{VIOLET_SOFT}"/>'
        f'</g></g>'
    )
    css.append(
        f'.ob{{animation:hfade 1s ease-out 1.4s both}}'
        f'.obr{{transform-box:view-box;transform-origin:{hx}px {hy}px;animation:hspin 64s linear infinite}}'
        f'@keyframes hspin{{to{{transform:rotate(360deg)}}}}'
    )

    # Datenpunkte (Start/Ende am Rand der Knoten)
    for i, (a, b, dur, delay) in enumerate(FLOWS):
        _, ax, ay, ar, _ = NODES[a]
        _, bx, by, br, _ = NODES[b]
        ln = math.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / ln, (by - ay) / ln
        e, c = _flow_dot(i, ax + ux * ar, ay + uy * ar, bx - ux * br, by - uy * br, dur, delay)
        flows_el.append(e)
        flows_css.append(c)
    out.extend(flows_el)
    css.extend(flows_css)
    css.append(f'.dp{{fill:{LAVENDER_LIGHT};transform-box:view-box;transform-origin:0 0}}')

    # Puls um den Hauptknoten
    out.append(f'<circle class="pu" cx="{hx}" cy="{hy}" r="{hr}" fill="none" stroke="{VIOLET_SOFT}" '
               f'stroke-width="1.5"/>')
    css.append(
        f'.pu{{transform-box:fill-box;transform-origin:50% 50%;opacity:0;'
        f'animation:hpu 7s ease-out 2.4s infinite}}'
        f'@keyframes hpu{{0%{{opacity:0;transform:scale(1)}}8%{{opacity:.5}}'
        f'60%,100%{{opacity:0;transform:scale(1.6)}}}}'
    )

    # Knoten
    for i, (key, (ic, x, y, r, isz)) in enumerate(NODES.items()):
        delay = 0.6 + i * 0.12
        if key == 'hub':
            disc = f'<circle cx="{x}" cy="{y}" r="{r}" fill="{VIOLET}"/>'
            col = WHITE
        else:
            disc = (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#2a003d" stroke="{LAVENDER}" '
                    f'stroke-opacity=".6" stroke-width="1.5"/>')
            col = LAVENDER_LIGHT
        fill_attr = f'fill="{col}"'
        out.append(
            f'<g class="nd" style="animation-delay:{delay:.2f}s">{disc}'
            f'{icon(ic, isz, x - isz / 2, y - isz / 2, fill_attr)}</g>'
        )
    css.append(
        f'.nd{{transform-box:fill-box;transform-origin:50% 50%;animation:hpop .6s {EASE} both}}'
        f'@keyframes hpop{{from{{opacity:0;transform:scale(.6)}}to{{opacity:1;transform:none}}}}'
    )
    return d, ''.join(out), ''.join(css)


def build() -> str:
    bg_d, bg_b, bg_c = background()
    lo_d, lo_b, lo_c = lockup()
    cp_b, cp_c = copy_block()
    il_d, il_b, il_c = illustration()
    body = bg_b + il_b + lo_b + cp_b
    css = bg_c + lo_c + cp_c + il_c
    return svg_doc(
        W, H, body,
        title='BW.Tech – Cloud by Design',
        desc=('Logo BW.Tech mit dem Slogan „Cloud by Design“. Maßgeschneiderte Cloud-Lösungen, '
              'die Sie voranbringen. Persönliche Beratung · Rechenzentrum in Deutschland · '
              'DSGVO-konform. Daneben eine stilisierte Cloud-Infrastruktur mit vernetzten Knoten.'),
        css=css,
        defs=bg_d + lo_d + il_d + defs.render(),
    )


if __name__ == '__main__':
    path = write_asset('hero.svg', build())
    print(path, os.path.getsize(path), 'B', '| Pillen rechts:', round(pills_right()))
