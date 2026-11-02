"""Grafik „Über BW.Tech“: Zählwerk „seit 2008“, drei Werte, Faktenleiste.

Erzeugt assets/about-light.svg (GitHub hell) und assets/about-dark.svg (GitHub dunkel).
Aufruf (im Repo-Wurzelverzeichnis): python src/about.py

Animationen (nur CSS, bei prefers-reduced-motion aus – Grundzustand = Endzustand):
  - Rollziffern 2-0-0-8, gestaffelt, einmalig (bis ~2 s)
  - Werte-Spalten blenden gestaffelt ein, Häkchen und Verbindungslinien zeichnen sich
  - Faktenleiste blendet nacheinander ein (alles fertig nach ~2,2 s)
  - Dauer (gemeinsamer 9-s-Takt): Glanz über die Zählwerk-Kachel, danach ein Lichtpuls
    nacheinander über die drei Verbindungslinien; Licht in der Kachel atmet sanft
"""
from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from brand import (  # noqa: E402
    INK, LAVENDER, LAVENDER_LIGHT, LAVENDER_PALE, PURPLE, PURPLE_DEEP, VIOLET, WHITE,
    svg_doc, write_asset,
)
from textpath import Font, Glyph, GlyphDefs, _fmt  # noqa: E402

W, H = 1200, 412
R = 24
PAD = 44

# Zählwerk-Kachel
TILE_X, TILE_Y, TILE_W, TILE_H = PAD, PAD, 300, 236
TILE_PAD = 30

# Werte-Spalten
COL_X = (384, 646, 908)
COL_W = 244

# Faktenleiste
BAND_Y = TILE_Y + TILE_H + PAD   # gleicher Abstand wie oben

EASE = 'cubic-bezier(.2,.8,.2,1)'

# Dauerbewegung: ein gemeinsamer 9-s-Takt – Glanz über die Kachel, danach läuft ein
# Lichtpuls nacheinander über die drei Verbindungslinien (eine Bewegung von links nach rechts)
PERIOD = 9.0
SHEEN_START = 2.6
FLOW_START = SHEEN_START + PERIOD * 0.22
FLOW_STEP = 0.75
FLOW_FRAC = 0.16
FLOW_DASH = 44
FLOW_KF = ['']

F400 = Font('Lexend', 400)
F500 = Font('Lexend', 500)
F600 = Font('Lexend', 600)
F700 = Font('Lexend', 700)

VALUES = (
    ('ehrlich.', ('Auf unsere Beratung', 'ist Verlass.')),
    ('offen.', ('Stetige Verbesserung', 'und neue Ideen.')),
    ('kundenorientiert.', ('Die beste Lösung', 'passt genau zu Ihrem', 'Anwendungsfall.')),
)

FACTS = (
    ('pin', ('Serverstandort', 'Deutschland')),
    ('server', ('Hochverfügbarkeits-', 'Rechenzentrum')),
    ('shield', ('DSGVO-konform',)),
    ('people', ('Beratung auf', 'Augenhöhe')),
)

# Linien-Icons der Faktenleiste im 24er-Raster (Strich, runde Enden)
FACT_ICONS = {
    'pin': (
        '<path d="M12 21.2s-6.6-6-6.6-11.1a6.6 6.6 0 0 1 13.2 0c0 5.1-6.6 11.1-6.6 11.1z"/>'
        '<circle cx="12" cy="10" r="2.5"/>'
    ),
    'server': (
        '<rect x="3.8" y="3.8" width="16.4" height="6.6" rx="2"/>'
        '<rect x="3.8" y="13.6" width="16.4" height="6.6" rx="2"/>'
        '<path d="M7.6 7.1h.01M7.6 16.9h.01M11.4 7.1h5M11.4 16.9h5"/>'
    ),
    'shield': (
        '<path d="M12 2.9l7.2 2.9v5.6c0 4.6-3 8.3-7.2 9.7-4.2-1.4-7.2-5.1-7.2-9.7V5.8z"/>'
        '<path d="M8.7 12.1l2.3 2.3 4.4-4.5"/>'
    ),
    'people': (
        '<circle cx="7.6" cy="8.4" r="2.7"/><circle cx="16.4" cy="8.4" r="2.7"/>'
        '<path d="M2.9 19.3c0-2.9 2.1-4.8 4.7-4.8s4.7 1.9 4.7 4.8"/>'
        '<path d="M11.7 19.3c0-2.9 2.1-4.8 4.7-4.8s4.7 1.9 4.7 4.8"/>'
    ),
}

THEMES = {
    'light': dict(
        panel_top=WHITE, panel_bottom=LAVENDER_PALE, panel_stroke=LAVENDER,
        band='#F0E9FA', band_line=LAVENDER,
        tile_a='#4a0a6b', tile_b=PURPLE_DEEP, tile_stroke='none',
        tile_glow='#9b5cf6', tile_glow_op=0.45, sheen_op=0.2, flow='#9b5cf6',
        digit=WHITE, tile_label=LAVENDER, tile_accent='#b48cff', tile_dots=WHITE,
        kicker='#6a5884', heading=PURPLE, body='#43365a',
        check_fill=LAVENDER_LIGHT, check_ring=LAVENDER, check=VIOLET,
        line_a=VIOLET, line_b=LAVENDER,
        fact_text=INK, fact_tile=WHITE, fact_tile_stroke=LAVENDER, fact_icon=VIOLET,
        divider=LAVENDER, glow=VIOLET, glow_op=0.07, dots=VIOLET, dots_op=0.16,
        bg=WHITE,
    ),
    'dark': dict(
        panel_top='#1f0b2e', panel_bottom='#170922', panel_stroke='#3a1f55',
        band='#130719', band_line='#33194b',
        tile_a='#46116a', tile_b='#2a0743', tile_stroke='#5a2d86',
        tile_glow='#a78bfa', tile_glow_op=0.35, sheen_op=0.15, flow='#d4c4ff',
        digit=LAVENDER_LIGHT, tile_label='#d9c8f5', tile_accent='#a78bfa', tile_dots=WHITE,
        kicker='#b3a0d3', heading=LAVENDER_LIGHT, body='#cdbbe9',
        check_fill='#2c1342', check_ring='#4a2a6b', check='#c4b5fd',
        line_a='#a78bfa', line_b='#3a1f55',
        fact_text='#e6dcf5', fact_tile='#1f0b2e', fact_tile_stroke='#3a1f55', fact_icon='#a78bfa',
        divider='#3a1f55', glow='#a78bfa', glow_op=0.08, dots='#a78bfa', dots_op=0.14,
        bg='#0d1117',
    ),
}


# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------

def _lum(hexcol: str) -> float:
    h = hexcol.lstrip('#')
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a: str, b: str) -> float:
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def use_glyph(g: Glyph, x: float, y: float, extra: str = '') -> str:
    tr = f'translate({_fmt(x)} {_fmt(y)}) scale({g.scale:.5f} {-g.scale:.5f})'
    return f'<use href="#{g.gid}" transform="{tr}"{extra}/>'


def polyline_len(pts: list[tuple[float, float]]) -> float:
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))


# Gezeichnete Linien: je Länge ein eigenes @keyframes (kein var() in Keyframes – Safari-sicher)
_DRAW_KF: dict[str, str] = {}


def draw_attrs(length: float, delay: float, dur: float = 0.6) -> str:
    """class/style/dasharray für eine Linie, die sich einmalig zeichnet (Grundzustand: fertig gezeichnet)."""
    L = math.ceil(length) + 1
    name = f'ab-dl{L}'
    _DRAW_KF[name] = f'@keyframes {name}{{from{{stroke-dashoffset:{L}px}}to{{stroke-dashoffset:0}}}}'
    return (f'class="ab-draw" stroke-dasharray="{L} {L}" '
            f'style="animation-name:{name};animation-delay:{delay:.2f}s;animation-duration:{dur:.2f}s"')


# ---------------------------------------------------------------------------
# Bausteine
# ---------------------------------------------------------------------------

def counter_tile(t: dict, defs: GlyphDefs) -> tuple[str, str, str]:
    """Zählwerk-Kachel. Liefert (svg, css, defs)."""
    x0, y0, w, h = TILE_X, TILE_Y, TILE_W, TILE_H
    tx = x0 + TILE_PAD
    css: list[str] = []
    d: list[str] = []
    out: list[str] = []

    d.append(
        f'<linearGradient id="ab-tile" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{t["tile_a"]}"/><stop offset="1" stop-color="{t["tile_b"]}"/>'
        f'</linearGradient>'
        f'<radialGradient id="ab-tglow" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" '
        f'gradientTransform="translate({x0 + w - 30} {y0 + 20}) scale(230 190)">'
        f'<stop offset="0" stop-color="{t["tile_glow"]}" stop-opacity="{t["tile_glow_op"]}"/>'
        f'<stop offset="1" stop-color="{t["tile_glow"]}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="ab-sheen" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="#fff" stop-opacity="{t["sheen_op"]}"/>'
        f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<clipPath id="ab-tclip"><rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="20"/></clipPath>'
    )

    # Kachel mit Licht, Punktraster und Glanz
    stroke = '' if t['tile_stroke'] == 'none' else f' stroke="{t["tile_stroke"]}" stroke-width="1.5"'
    out.append(f'<g class="ab-tile">')
    out.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="20" fill="url(#ab-tile)"{stroke}/>')
    out.append('<g clip-path="url(#ab-tclip)">')
    out.append(f'<rect class="ab-breathe" x="{x0}" y="{y0}" width="{w}" height="{h}" fill="url(#ab-tglow)"/>')
    # Punktraster oben rechts, nach links unten auslaufend
    dots = []
    for row in range(4):
        for col in range(6):
            cx = x0 + w - 26 - col * 15
            cy = y0 + 26 + row * 15
            op = max(0.0, 0.34 - 0.055 * (col + row * 1.3))
            if op > 0.02:
                dots.append(f'<circle cx="{cx}" cy="{cy}" r="1.6" fill-opacity="{op:.2f}"/>')
    out.append(f'<g fill="{t["tile_dots"]}">{"".join(dots)}</g>')
    # Glanz: Grundzustand links außerhalb der Kachel (unsichtbar)
    out.append(
        f'<g class="ab-sheen"><rect x="{x0 - 200}" y="{y0 - 20}" width="170" height="{h + 40}" '
        f'fill="url(#ab-sheen)" transform="skewX(-14)"/></g>'
    )
    out.append('</g>')

    # „seit“
    seit_y = y0 + TILE_PAD + 20
    out.append(F500.text('seit', 26, tx, seit_y, defs=defs, letter_spacing=0.5,
                         attrs=f'class="ab-fade" style="--d:.05s" fill="{t["tile_label"]}"'))

    # Rollziffern „2008“
    size = 96
    base = seit_y + 28 + round(F700.cap_height / F700.upem * size)
    final = F700.glyphs('2008', size, tx - 3, base, defs=defs)
    cap = F700.cap_height / F700.upem * size
    pad = 15      # davon 12 px weiche Blende, 3 px Luft für Überhänge der Rundungen
    win_top, win_bot = base - cap - pad, base + pad
    step = math.ceil(win_bot - win_top) + 24
    x_end = final[-1].x + final[-1].advance + 6
    d.append(
        f'<linearGradient id="ab-winfade" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        f'<stop offset="{12 / (win_bot - win_top):.3f}" stop-color="#fff"/>'
        f'<stop offset="{1 - 12 / (win_bot - win_top):.3f}" stop-color="#fff"/>'
        f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<mask id="ab-win" maskUnits="userSpaceOnUse" x="{tx - 10}" y="{_fmt(win_top)}" '
        f'width="{_fmt(x_end - tx + 20)}" height="{_fmt(win_bot - win_top)}">'
        f'<rect x="{tx - 10}" y="{_fmt(win_top)}" width="{_fmt(x_end - tx + 20)}" '
        f'height="{_fmt(win_bot - win_top)}" fill="url(#ab-winfade)"/></mask>'
    )
    strips = []
    steps = (6, 8, 9, 11)
    for i, g in enumerate(final):
        target = int(g.char)
        n = steps[i]
        cx = g.x + g.advance / 2
        uses = [use_glyph(g, g.x, base)]
        for k in range(1, n + 1):
            v = (target - k) % 10
            gv = F700.glyphs(str(v), size, 0, 0, defs=defs)[0]
            uses.append(use_glyph(gv, cx - gv.advance / 2, base - k * step))
        strips.append(f'<g class="ab-roll ab-r{i}">{"".join(uses)}</g>')
        delay = 0.1 + i * 0.09
        dur = 1.25 + i * 0.12
        css.append(f'@keyframes ab-r{i}{{from{{transform:translateY({n * step}px)}}to{{transform:none}}}}')
        css.append(f'.ab-r{i}{{animation:ab-r{i} {dur:.2f}s {EASE} {delay:.2f}s both}}')
    out.append(f'<g mask="url(#ab-win)" fill="{t["digit"]}">{"".join(strips)}</g>')

    # Akzentlinie + „an Ihrer Seite“
    ly = base + 22
    out.append(f'<path {draw_attrs(44, 1.05)} d="M{tx} {ly}h44" '
               f'stroke="{t["tile_accent"]}" stroke-width="3" stroke-linecap="round" fill="none"/>')
    out.append(F500.text('an Ihrer Seite', 26, tx, ly + 40, defs=defs,
                         attrs=f'class="ab-fade" style="--d:1.0s" fill="{t["tile_label"]}"'))
    out.append('</g>')
    return ''.join(out), ''.join(css), ''.join(d)


def value_column(t: dict, defs: GlyphDefs, idx: int, keyword: str, lines: tuple[str, ...]) -> tuple[str, str]:
    x = COL_X[idx]
    cy = TILE_Y + 20
    cx = x + 20
    delay = 0.35 + idx * 0.2
    out = [f'<g class="ab-col" style="--d:{delay:.2f}s">']
    # Häkchen
    out.append(f'<circle cx="{cx}" cy="{cy}" r="20" fill="{t["check_fill"]}" stroke="{t["check_ring"]}" stroke-width="1.5"/>')
    pts = [(cx - 7.5, cy + 0.5), (cx - 2.5, cy + 5.5), (cx + 8, cy - 5.5)]
    ln = polyline_len(pts) + 2
    out.append(
        f'<path {draw_attrs(ln, delay + .3, .5)} '
        f'd="M{_fmt(pts[0][0])} {_fmt(pts[0][1])}L{_fmt(pts[1][0])} {_fmt(pts[1][1])}L{_fmt(pts[2][0])} {_fmt(pts[2][1])}" '
        f'fill="none" stroke="{t["check"]}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>'
    )
    # Verbindungslinie rechts vom Häkchen
    lx0, lx1 = cx + 34, x + COL_W - 4
    llen = lx1 - lx0 + 2
    gid = f'ab-ln{idx}'
    out.append(
        f'<path {draw_attrs(llen, delay + .45, .9)} d="M{lx0} {cy}H{lx1}" '
        f'stroke="url(#{gid})" stroke-width="1.5" stroke-linecap="round" fill="none"/>'
    )
    # Dauer: ein kurzer Lichtpuls läuft die Linie entlang (Grundzustand: versteckt vor dem Linienanfang)
    dash = FLOW_DASH
    out.append(
        f'<path class="ab-flow" style="animation-delay:{FLOW_START + idx * FLOW_STEP:.2f}s" d="M{lx0} {cy}H{lx1}" '
        f'stroke="{t["flow"]}" stroke-width="1.75" stroke-linecap="round" fill="none" '
        f'stroke-dasharray="{dash} {llen + dash * 2:.0f}" stroke-dashoffset="{dash + 2}"/>'
    )
    # Puls blendet am Anfang auf und läuft zum (auslaufenden) Linienende hin aus
    flow_kf = (f'@keyframes ab-flow{{0%{{stroke-dashoffset:{dash + 2}px;opacity:0}}'
               f'{FLOW_FRAC * 25:.1f}%{{opacity:1}}'
               f'{FLOW_FRAC * 100:.0f}%,100%{{stroke-dashoffset:-{llen + 2:.0f}px;opacity:0}}}}')
    FLOW_KF[0] = flow_kf
    defs_out = (
        f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{lx0}" y1="0" x2="{lx1}" y2="0">'
        f'<stop offset="0" stop-color="{t["line_a"]}"/><stop offset=".45" stop-color="{t["line_b"]}"/>'
        f'<stop offset="1" stop-color="{t["line_b"]}" stop-opacity="0"/></linearGradient>'
    )
    # Überschrift zweizeilig: „Wir sind“ + Wert
    out.append(F500.text('Wir sind', 24, x, 128, defs=defs, attrs=f'fill="{t["kicker"]}"'))
    out.append(F600.text(keyword, 28, x - 1, 162, defs=defs, attrs=f'fill="{t["heading"]}"'))
    for j, line in enumerate(lines):
        out.append(F400.text(line, 22, x, 204 + j * 30, defs=defs, attrs=f'fill="{t["body"]}"'))
    out.append('</g>')
    return ''.join(out), defs_out


def fact_band(t: dict, defs: GlyphDefs) -> str:
    out = []
    out.append(f'<g clip-path="url(#ab-pclip)"><rect x="0" y="{BAND_Y}" width="{W}" height="{H - BAND_Y}" fill="{t["band"]}"/></g>')
    out.append(f'<path d="M1 {BAND_Y}H{W - 1}" stroke="{t["band_line"]}" stroke-width="1.5"/>')
    tile, gap = 44, 14
    cy = BAND_Y + (H - BAND_Y) / 2
    widths = []
    for _, lines in FACTS:
        widths.append(tile + gap + max(F500.measure(s, 22) for s in lines))
    free = (W - 2 * PAD) - sum(widths)
    spacing = free / (len(FACTS) - 1)
    x = PAD
    for i, ((ic, lines), cw) in enumerate(zip(FACTS, widths)):
        delay = 1.1 + i * 0.13
        g = [f'<g class="ab-fact" style="--d:{delay:.2f}s">']
        g.append(f'<rect x="{x}" y="{cy - tile / 2}" width="{tile}" height="{tile}" rx="12" '
                 f'fill="{t["fact_tile"]}" stroke="{t["fact_tile_stroke"]}" stroke-width="1.5"/>')
        isz = 28
        g.append(f'<g transform="translate({x + (tile - isz) / 2:.1f} {cy - isz / 2:.1f}) scale({isz / 24:.4f})" '
                 f'fill="none" stroke="{t["fact_icon"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{FACT_ICONS[ic]}</g>')
        tx = x + tile + gap
        if len(lines) == 1:
            g.append(F500.text(lines[0], 22, tx, cy + 8, defs=defs, attrs=f'fill="{t["fact_text"]}"'))
        else:
            g.append(F500.text(lines[0], 22, tx, cy - 6, defs=defs, attrs=f'fill="{t["fact_text"]}"'))
            g.append(F500.text(lines[1], 22, tx, cy + 22, defs=defs, attrs=f'fill="{t["fact_text"]}"'))
        g.append('</g>')
        out.append(''.join(g))
        if i < len(FACTS) - 1:
            dx = x + cw + spacing / 2
            out.append(f'<path d="M{dx:.1f} {cy - 18}V{cy + 18}" stroke="{t["divider"]}" stroke-width="1.5"/>')
        x += cw + spacing
    return ''.join(out)


BASE_CSS = (
    # Einblendungen
    '.ab-fade,.ab-col,.ab-fact,.ab-tile{transform-box:fill-box;transform-origin:center}'
    '@keyframes ab-in{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}'
    '@keyframes ab-op{from{opacity:0}to{opacity:1}}'
    f'.ab-tile{{animation:ab-in .8s {EASE} 0s both}}'
    f'.ab-fade{{animation:ab-op .7s {EASE} var(--d,0s) both}}'
    f'.ab-col{{animation:ab-in .8s {EASE} var(--d,0s) both}}'
    f'.ab-fact{{animation:ab-in .7s {EASE} var(--d,0s) both}}'
    # Linien zeichnen: Easing und Füllmodus hier, Name/Dauer/Verzögerung je Linie im style-Attribut
    f'.ab-draw{{animation-timing-function:{EASE};animation-fill-mode:both}}'
    # Rollziffern
    '.ab-roll{transform-box:view-box;transform-origin:0 0}'
    # Dauer im 9-s-Takt: Glanz über die Kachel, Lichtpuls über die Linien (Sprung jeweils
    # unsichtbar außerhalb), atmendes Licht (hin und zurück = nahtlos)
    '.ab-sheen{transform-box:view-box;transform-origin:0 0;'
    f'animation:ab-sheen {PERIOD:.0f}s cubic-bezier(.45,0,.25,1) {SHEEN_START}s infinite}}'
    '@keyframes ab-sheen{0%{transform:translateX(0)}30%,100%{transform:translateX(620px)}}'
    '.ab-breathe{transform-box:fill-box;transform-origin:center;'
    f'animation:ab-breathe {PERIOD:.0f}s ease-in-out 2s infinite alternate}}'
    '@keyframes ab-breathe{from{opacity:1}to{opacity:.45}}'
    f'.ab-flow{{animation:ab-flow {PERIOD:.0f}s cubic-bezier(.45,0,.35,1) 0s infinite}}'
)


def build(theme: str) -> str:
    t = THEMES[theme]
    _DRAW_KF.clear()
    defs = GlyphDefs('ab')
    body: list[str] = []
    extra_defs: list[str] = []

    extra_defs.append(
        f'<linearGradient id="ab-panel" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{t["panel_top"]}"/><stop offset="1" stop-color="{t["panel_bottom"]}"/>'
        f'</linearGradient>'
        f'<radialGradient id="ab-glow" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" '
        f'gradientTransform="translate(1080 40) scale(520 300)">'
        f'<stop offset="0" stop-color="{t["glow"]}" stop-opacity="{t["glow_op"]}"/>'
        f'<stop offset="1" stop-color="{t["glow"]}" stop-opacity="0"/></radialGradient>'
        f'<clipPath id="ab-pclip"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="{R}"/></clipPath>'
    )
    body.append(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="{R}" fill="url(#ab-panel)"/>')
    body.append(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="{R}" fill="url(#ab-glow)"/>')

    tile_svg, tile_css, tile_defs = counter_tile(t, defs)
    extra_defs.append(tile_defs)
    body.append(tile_svg)

    for i, (kw, lines) in enumerate(VALUES):
        col_svg, col_defs = value_column(t, defs, i, kw, lines)
        body.append(col_svg)
        extra_defs.append(col_defs)

    body.append(fact_band(t, defs))
    # Rahmen zuletzt, damit die Leiste ihn nicht überdeckt
    body.append(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="{R}" fill="none" '
                f'stroke="{t["panel_stroke"]}" stroke-width="1.5"/>')

    title = 'Über BW.Tech – seit 2008 an Ihrer Seite'
    desc = ('Seit 2008 an Ihrer Seite. Unsere Werte: Wir sind ehrlich – auf unsere Beratung ist Verlass. '
            'Wir sind offen – stetige Verbesserung und neue Ideen. Wir sind kundenorientiert – die beste '
            'Lösung passt genau zu Ihrem Anwendungsfall. Serverstandort Deutschland, '
            'Hochverfügbarkeits-Rechenzentrum, DSGVO-konform, Beratung auf Augenhöhe.')
    return svg_doc(W, H, ''.join(body), title=title, desc=desc,
                   css=BASE_CSS + tile_css + ''.join(_DRAW_KF.values()) + FLOW_KF[0], defs=defs.render() + ''.join(extra_defs))


def report_contrast() -> None:
    for name, t in THEMES.items():
        pairs = [
            ('kicker', t['kicker'], t['panel_top']), ('kicker', t['kicker'], t['panel_bottom']),
            ('heading', t['heading'], t['panel_bottom']), ('body', t['body'], t['panel_top']),
            ('body', t['body'], t['panel_bottom']), ('fact', t['fact_text'], t['band']),
            ('digit', t['digit'], t['tile_a']), ('tile_label', t['tile_label'], t['tile_a']),
            ('tile_label', t['tile_label'], t['tile_b']),
        ]
        print(name, '  '.join(f'{n}={contrast(a, b):.1f}' for n, a, b in pairs))


def main() -> None:
    for theme in ('light', 'dark'):
        path = write_asset(f'about-{theme}.svg', build(theme))
        print(f'{os.path.relpath(path)}  {os.path.getsize(path)} B')
    report_contrast()


if __name__ == '__main__':
    main()
