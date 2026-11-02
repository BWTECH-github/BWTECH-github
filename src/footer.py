"""Fußzeile: ruhige Wellen, Slogan „Cloud by Design“, „bw.tech · Seit 2008 an Ihrer Seite“.

Erzeugt assets/footer.svg (viewBox 1200×200, eine Variante mit eigener lila Fläche, r=24).

  - Drei übereinanderliegende Wellen laufen nahtlos nach links: Jede Wellenform ist
    periodisch und wird um genau eine Wellenlänge verschoben – der Übergang am
    Schleifenende ist dadurch unsichtbar. Unterschiedliche Wellenlängen und Tempi
    ergeben eine ruhige Tiefenwirkung.
  - Slogan aus dem Profilbild (brand.tagline_word), darunter Lexend 400.
  - Weiche Lichtfläche über radialGradient (kein Filter), feines Punktraster.
"""
from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import brand  # noqa: E402
from intro_util import EASE, f, require_contrast  # noqa: E402
from textpath import Font, GlyphDefs  # noqa: E402

W, H, R = 1200, 200, 24
SUBLINE = 'bw.tech · Seit 2008 an Ihrer Seite'
SUB_SIZE = 26
SUB_COLOR = '#dccdf3'

# Wellen von hinten nach vorn:
# (Wellenlänge, Amplitude, Ruhelinie y, Periode s, Füllung, Deckkraft, Linienfarbe, Liniendeckkraft)
WAVES = [
    (820, 12, 150, 46, brand.VIOLET, 0.24, '#b48cf8', 0.38),
    (600, 10, 163, 30, '#5a1784', 0.78, brand.VIOLET_SOFT, 0.30),
    (460, 7, 179, 21, brand.PURPLE_DEEP, 0.88, brand.VIOLET_SOFT, 0.22),
]

sub_font = Font('Lexend', 400)


def wave_curve(lam: float, amp: float, y0: float, width: float, phase: float = 0.0) -> str:
    """Periodische Sinuswelle als Bézier-Kurven (8 Stützstellen je Wellenlänge), offen."""
    seg = lam / 8
    n = int(math.ceil(width / seg)) + 1
    pts = []
    for i in range(n + 1):
        x = i * seg
        a = 2 * math.pi * (x / lam) + phase
        pts.append((x, y0 + amp * math.sin(a), amp * math.cos(a) * 2 * math.pi / lam))
    d = [f'M{f(pts[0][0])} {f(pts[0][1])}']
    for (xa, ya, sa), (xb, yb, sb) in zip(pts, pts[1:]):
        h = (xb - xa) / 3
        d.append(f'C{f(xa + h)} {f(ya + sa * h)} {f(xb - h)} {f(yb - sb * h)} {f(xb)} {f(yb)}')
    return ''.join(d)


def build() -> str:
    require_contrast(SUB_COLOR, brand.PURPLE, 4.5, 'Fußzeile: Unterzeile')
    require_contrast(SUB_COLOR, '#4a0a6b', 4.5, 'Fußzeile: Unterzeile auf hellster Stelle')

    defs = GlyphDefs('ft')
    css = []
    waves_svg = []
    for i, (lam, amp, y0, period, color, op, line, line_op) in enumerate(WAVES):
        curve = wave_curve(lam, amp, y0, W + lam, phase=i * 1.3)
        # Fläche und feine Kammlinie bewegen sich gemeinsam
        waves_svg.append(
            f'<g class="fw{i}"><path d="{curve}V{H + 2}H0Z" fill="{color}" fill-opacity="{op}"/>'
            f'<path d="{curve}" fill="none" stroke="{line}" stroke-opacity="{line_op}" stroke-width="1.5"/></g>'
        )
        css.append(f'@keyframes fw{i}{{to{{transform:translateX(-{lam}px)}}}}')
        css.append(f'.fw{i}{{transform-box:view-box;transform-origin:0 0;'
                   f'animation:fw{i} {period}s linear infinite}}')

    # Slogan exakt aus dem Profilbild, zentriert
    c0 = brand.tagline_box('Cloud')
    d1 = brand.tagline_box('Design')
    tx0, tx1 = c0[0], d1[2]
    cap_top, base = c0[1], c0[3]            # „Cloud“: Oberkante C/l bis Grundlinie
    scale = 38 / (base - cap_top)           # Versalhöhe ~38 px
    tw = (tx1 - tx0) * scale
    slogan_top = 30
    ox = (W - tw) / 2 - tx0 * scale
    oy = slogan_top - cap_top * scale
    slogan = (
        # äußere Gruppe trägt die Lage, innere die Einblendung (CSS-transform würde sonst das Attribut ersetzen)
        f'<g class="fs"><g transform="translate({f(ox)} {f(oy)}) scale({f(scale, 4)})" fill="#ffffff">'
        + ''.join(brand.tagline_word(w) for w in ('Cloud', 'by', 'Design')) + '</g></g>'
    )
    sub_base = slogan_top + 38 + 49
    sub = sub_font.text(SUBLINE, SUB_SIZE, W / 2, sub_base, anchor='middle', defs=defs,
                        attrs=f'class="fsub" fill="{SUB_COLOR}"')

    css.append(f'@keyframes fin{{from{{opacity:0;transform:translateY(8px)}}}}')
    css.append(f'.fs,.fsub{{transform-box:fill-box;transform-origin:50% 50%;animation:fin .9s {EASE} both}}')
    css.append('.fsub{animation-delay:.15s}')

    grads = (
        f'<linearGradient id="fbg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="#42005f"/><stop offset=".55" stop-color="{brand.PURPLE}"/>'
        f'<stop offset="1" stop-color="#2c0042"/></linearGradient>'
        f'<radialGradient id="fgl" cx="600" cy="70" r="420" gradientUnits="userSpaceOnUse" '
        f'gradientTransform="translate(600 70) scale(1 .38) translate(-600 -70)">'
        f'<stop offset="0" stop-color="{brand.VIOLET}" stop-opacity=".34"/>'
        f'<stop offset="1" stop-color="{brand.VIOLET}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="fdm" cx="600" cy="80" r="560" gradientUnits="userSpaceOnUse" '
        f'gradientTransform="translate(600 80) scale(1 .3) translate(-600 -80)">'
        f'<stop offset="0" stop-color="#fff" stop-opacity="1"/>'
        f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        f'<mask id="fmk" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
        f'<rect width="{W}" height="{H}" fill="url(#fdm)"/></mask>'
        f'<pattern id="fdt" width="24" height="24" patternUnits="userSpaceOnUse">'
        f'<circle cx="12" cy="12" r="1.1" fill="#ffffff"/></pattern>'
        f'<clipPath id="fcl"><rect width="{W}" height="{H}" rx="{R}"/></clipPath>'
    )
    body = (
        f'<g clip-path="url(#fcl)">'
        f'<rect width="{W}" height="{H}" fill="url(#fbg)"/>'
        f'<rect width="{W}" height="{H}" fill="url(#fdt)" opacity=".07" mask="url(#fmk)"/>'
        f'<rect width="{W}" height="{H}" fill="url(#fgl)"/>'
        + ''.join(waves_svg)
        + '</g>'
        + slogan + sub
    )
    return brand.svg_doc(
        W, H, body,
        title='BW.Tech – Cloud by Design',
        desc='Fußzeile mit ruhig laufenden Wellen: Cloud by Design – bw.tech, seit 2008 an Ihrer Seite.',
        css=''.join(css),
        defs=grads + defs.render(),
    )


def main() -> None:
    sys.stdout.reconfigure(errors='replace')   # Konsolen ohne UTF-8 nicht abbrechen lassen
    svg = build()
    p = brand.write_asset('footer.svg', svg)
    print(f'{os.path.relpath(p)}  {len(svg.encode())} B')


if __name__ == '__main__':
    main()
