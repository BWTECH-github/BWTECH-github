"""Link-Buttons für das Profil: bw.tech, Kontakt, Lösungen, Karriere.

Erzeugt assets/btn-<id>-light.svg und assets/btn-<id>-dark.svg.

  - viewBox 256×76: Button 240×64 (r=20) mit 8/6 px transparentem Rand. Der Rand
    ergibt im README gleichmäßige Abstände – auch beim Umbruch auf schmalen
    Bildschirmen, wo zwischen Bildzeilen sonst kaum Luft bleibt.
  - „bw.tech“ ist der Primär-Button (gefüllt), die anderen sind Kontur-Buttons.
  - Eigene, schlichte Linien-Icons im 24er-Raster (Globus, Brief, Stapel, Koffer).
  - Animation: gelegentlicher weicher Glanz-Sweep, Periode 7 s, je Button versetzt.
    Ohne Animation liegt der Glanz außerhalb des Buttons – der Button ist dann einfach ruhig.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import brand  # noqa: E402
from intro_util import contrast, f, require_contrast  # noqa: E402
from textpath import Font, GlyphDefs  # noqa: E402

VW, VH = 256, 76
BX, BY, BW, BH, R = 8, 6, 240, 64, 20
LABEL_SIZE = 24
ICON = 28                 # Kantenlänge des Icons in px
ICON_GAP = 10
PERIOD = 7.0              # Glanz alle 7 s
SWEEP_SHARE = 0.17        # Anteil der Periode, in dem der Glanz wandert (~1,2 s)
SWEEP_W = 84

BUTTONS = [
    # id, Beschriftung, Ziel, Icon, primär, Titel (Screenreader)
    ('website', 'bw.tech', 'https://bw.tech', 'globe', True, 'Website bw.tech'),
    ('kontakt', 'Kontakt', 'https://bw.tech/kontakt/', 'mail', False, 'Kontakt aufnehmen'),
    ('loesungen', 'Lösungen', 'https://bw.tech/loesungen/cloud-by-design/', 'stack', False, 'Unsere Lösungen'),
    ('karriere', 'Karriere', 'https://bw.tech/ueber-uns/#stellenAnzeigen', 'case', False, 'Karriere bei BW.Tech'),
]

# Linien-Icons im 24×24-Raster (Strichstärke wird mitskaliert)
ICONS = {
    'globe': (
        '<circle cx="12" cy="12" r="9.25"/>'
        '<ellipse cx="12" cy="12" rx="4.1" ry="9.25"/>'
        '<path d="M2.9 12h18.2"/>'
    ),
    'mail': (
        '<rect x="2.75" y="5" width="18.5" height="14" rx="2.6"/>'
        '<path d="M3.6 6.6 12 12.9l8.4-6.3"/>'
    ),
    'stack': (
        '<path d="M12 3.2 20.8 7.8 12 12.4 3.2 7.8Z"/>'
        '<path d="M3.2 12.1 12 16.7l8.8-4.6"/>'
        '<path d="M3.2 16.3 12 20.9l8.8-4.6"/>'
    ),
    'case': (
        '<rect x="2.75" y="7" width="18.5" height="13" rx="2.6"/>'
        '<path d="M8.6 7V5.3c0-.95.75-1.7 1.7-1.7h3.4c.95 0 1.7.75 1.7 1.7V7"/>'
        '<path d="M2.75 12.6h18.5"/>'
        '<path d="M10.4 12.6v1.3h3.2v-1.3"/>'
    ),
}

THEMES = {
    'light': {
        'page': brand.GITHUB_LIGHT_BG,
        'primary': {'top': '#460a66', 'bottom': brand.PURPLE, 'text': '#ffffff', 'icon': brand.LAVENDER,
                    'stroke': None, 'sweep': '#ffffff', 'sweep_op': 0.16},
        'outline': {'top': '#ffffff', 'bottom': '#fbf9fe', 'text': brand.PURPLE, 'icon': brand.VIOLET,
                    'stroke': '#bea4ea', 'sweep': brand.LAVENDER, 'sweep_op': 0.85},
    },
    'dark': {
        'page': brand.GITHUB_DARK_BG,
        'primary': {'top': '#7b27f3', 'bottom': '#6a14e3', 'text': '#ffffff', 'icon': '#ffffff',
                    'stroke': None, 'sweep': '#ffffff', 'sweep_op': 0.16},
        'outline': {'top': '#1d0d2b', 'bottom': '#170923', 'text': brand.LAVENDER_LIGHT, 'icon': '#a78bfa',
                    'stroke': '#5c3f8f', 'sweep': '#a78bfa', 'sweep_op': 0.16},
    },
}

label_font = Font('Lexend', 600)


def build(idx: int, bid: str, label: str, icon: str, primary: bool, title: str, theme: str) -> str:
    th = THEMES[theme]['primary' if primary else 'outline']
    page = THEMES[theme]['page']
    for surface in (th['top'], th['bottom']):
        require_contrast(th['text'], surface, 4.5, f'{bid}-{theme}: Beschriftung')
    if th['stroke'] is None:
        # Fläche gegen Seite nur zur Info: der Button wird über seine Beschriftung erkannt
        # (WCAG 1.4.11 verlangt für Buttons mit Text keinen Flächenkontrast)
        print(f'  {bid}-{theme}: Fläche/Seite {contrast(th["bottom"], page):.2f}:1')

    defs = GlyphDefs('bt')
    lw = label_font.measure(label, LABEL_SIZE)
    x0, _, x1, _ = label_font.bounds(label, LABEL_SIZE)
    ink_w = x1 - x0
    group_w = ICON + ICON_GAP + ink_w
    gx = BX + (BW - group_w) / 2
    cy = BY + BH / 2
    cap = label_font.cap_height / label_font.upem * LABEL_SIZE
    baseline = cy + cap / 2
    lx = gx + ICON + ICON_GAP - x0
    s = ICON / 24
    icon_svg = (
        f'<g transform="translate({f(gx)} {f(cy - ICON / 2)}) scale({f(s, 4)})" fill="none" '
        f'stroke="{th["icon"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        f'{ICONS[icon]}</g>'
    )
    label_svg = label_font.text(label, LABEL_SIZE, lx, baseline, defs=defs, attrs=f'fill="{th["text"]}"')

    start, end = -SWEEP_W - 40, VW + 40
    delay = 1.4 + idx * 0.35
    css = (
        f'@keyframes sw{{0%{{transform:translateX({start}px)}}'
        f'{f(SWEEP_SHARE * 100)}%{{transform:translateX({end}px)}}100%{{transform:translateX({end}px)}}}}'
        f'.sw{{transform-box:view-box;transform-origin:0 0;transform:translateX({start}px);'
        f'animation:sw {f(PERIOD)}s cubic-bezier(.45,0,.25,1) {f(delay)}s infinite both}}'
    )
    grad = (
        f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{th["top"]}"/><stop offset="1" stop-color="{th["bottom"]}"/></linearGradient>'
        f'<linearGradient id="sg" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{th["sweep"]}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{th["sweep"]}" stop-opacity="{th["sweep_op"]}"/>'
        f'<stop offset="1" stop-color="{th["sweep"]}" stop-opacity="0"/></linearGradient>'
        f'<clipPath id="cl"><rect x="{BX}" y="{BY}" width="{BW}" height="{BH}" rx="{R}"/></clipPath>'
    )
    if th['stroke']:
        # Kontur innen liegend, damit sie nicht über den Button hinausragt
        frame = (f'<rect x="{BX + 1}" y="{BY + 1}" width="{BW - 2}" height="{BH - 2}" rx="{R - 1}" '
                 f'fill="none" stroke="{th["stroke"]}" stroke-width="2"/>')
    else:
        # feine helle Innenkante oben für etwas Tiefe
        frame = (f'<rect x="{BX + .5}" y="{BY + .5}" width="{BW - 1}" height="{BH - 1}" rx="{R - .5}" '
                 f'fill="none" stroke="#ffffff" stroke-opacity=".12"/>')
    body = (
        f'<rect x="{BX}" y="{BY}" width="{BW}" height="{BH}" rx="{R}" fill="url(#bg)"/>'
        f'<g clip-path="url(#cl)"><g transform="skewX(-20)">'
        f'<rect class="sw" x="0" y="{BY - 4}" width="{SWEEP_W}" height="{BH + 8}" fill="url(#sg)"/></g></g>'
        f'{frame}{icon_svg}{label_svg}'
    )
    return brand.svg_doc(VW, VH, body, title=title, css=css, defs=grad + defs.render())


def main() -> None:
    for idx, (bid, label, _href, icon, primary, title) in enumerate(BUTTONS):
        for theme in THEMES:
            svg = build(idx, bid, label, icon, primary, title, theme)
            p = brand.write_asset(f'btn-{bid}-{theme}.svg', svg)
            print(f'{os.path.relpath(p)}  {len(svg.encode())} B')


if __name__ == '__main__':
    main()
