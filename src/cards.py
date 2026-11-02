"""Lösungskarten für das Profil-README (sechs Karten, je hell und dunkel).

Aufruf (im Repo-Wurzelverzeichnis): python src/cards.py
Erzeugt assets/card-<icon>-light.svg und assets/card-<icon>-dark.svg (viewBox 600×300).

Aufbau je Karte:
  - Fläche mit feiner Kontur, zarter Verlauf, weiche Lichtfläche und Punktraster oben rechts
  - Icon der Website in einer weichen Kachel oben links, Titel daneben
  - Beschreibung (ausgeglichener Zeilenumbruch, max. 3 Zeilen), unten rechts „Mehr erfahren“ mit Pfeil
Bewegung (nur CSS, bei prefers-reduced-motion aus – der Grundzustand ist das fertige Bild):
  - Einblendung: Karte hebt sich ein, Inhalte folgen gestaffelt (Verzögerung index × 0,12 s)
  - Lichtschimmer schräg über die Karte, Periode 9 s, im 2er-Raster diagonal versetzt (Welle)
  - Pfeil stupst nach rechts, kurz nachdem der Schimmer ihn erreicht
  - je Icon eine ruhige Zusatzbewegung als Überlagerung (Icon-Pfad bleibt unangetastet)
"""
from __future__ import annotations

import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import brand  # noqa: E402
from brand import (LAVENDER, LAVENDER_LIGHT, LAVENDER_PALE, PURPLE, PURPLE_DEEP,  # noqa: E402
                   VIOLET, icon, svg_doc, write_asset)
from textpath import Font, GlyphDefs  # noqa: E402

W, H = 600, 300
R = 20                       # Eckenradius Karten
PAD = 32                     # Innenabstand
TILE = 76                    # Kachelgröße
TILE_R = 18
TILE_X = TILE_Y = PAD
TCX = TILE_X + TILE / 2      # Kachelmitte
TCY = TILE_Y + TILE / 2
TITLE_X = TILE_X + TILE + 22
TITLE_SIZE = 36
BODY_SIZE = 24
BODY_LH = 35                 # Zeilenabstand ≈ 1,46
BODY_Y = 150                 # Grundlinie der ersten Textzeile
BODY_W = W - 2 * PAD
LINK_SIZE = 24
LINK_Y = 268                 # Grundlinie „Mehr erfahren“
ARROW_W = 18
ARROW_GAP = 10

EASE = 'cubic-bezier(.2,.8,.2,1)'
SHEEN_PERIOD = 9.0
SHEEN_START = 2.2            # erster Schimmer nach der Einblendung

CARDS = [
    dict(icon='cloud', title='Cloud by Design',
         text='Maßgeschneiderte Cloud-Lösungen, die sich flexibel Ihrem Bedarf anpassen.',
         url='https://bw.tech/loesungen/cloud-by-design/'),
    dict(icon='backup', title='Backup',
         text='Backup-, Restore- und Desaster-Recovery-Lösungen für jede IT-Umgebung.',
         url='https://bw.tech/loesungen/backup/'),
    dict(icon='software', title='Softwareentwicklung',
         text='Individuelle Software – maßgeschneidert oder auf Basis von Standardprodukten.',
         url='https://bw.tech/loesungen/softwareentwicklung/'),
    dict(icon='it', title='IT-Komplettlösungen',
         text='Unkompliziertes Management von Kundendaten – auf Wunsch auch als Cloud-Lösung.',
         url='https://bw.tech/loesungen/it-komplettloesungen/'),
    dict(icon='managed', title='Managed Services',
         text='Ihre sichere Cloud im Hochverfügbarkeits-Rechenzentrum in Deutschland.',
         url='https://bw.tech/loesungen/ihre-sichere-cloud-managed-services-im-rechenzentrum/'),
    dict(icon='ai', title='KI-Hosting',
         text='Leistungsstarke KI-Server für Ihr Unternehmen – DSGVO-konform, Serverstandort Deutschland.',
         url='https://bw.tech/loesungen/ki-hosting/'),
]

THEMES = {
    'light': dict(
        bg0='#ffffff', bg1=LAVENDER_PALE,
        glow=LAVENDER, glow_op=0.75,
        stroke0='#d6c4f2', stroke1='#ebe2f8',
        dots=VIOLET, dots_op=0.30,
        tile0=LAVENDER_LIGHT, tile1='#e6daf8', tile_stroke='#ffffff', tile_stroke_op=0.9,
        icon=PURPLE,
        title=PURPLE, body='#463a59', link=VIOLET,
        accent=VIOLET, rule='#e3d6f7',
        sheen='#c9b2f2', sheen_op=0.34,
    ),
    'dark': dict(
        bg0=PURPLE_DEEP, bg1='#1a0b26',
        glow=VIOLET, glow_op=0.30,
        stroke0='#4a2a68', stroke1='#2c1640',
        dots=LAVENDER, dots_op=0.20,
        tile0='#3a1659', tile1='#2a0d42', tile_stroke=LAVENDER, tile_stroke_op=0.12,
        icon=LAVENDER,
        title=LAVENDER_LIGHT, body='#cdbbe9', link='#a78bfa',
        accent='#a78bfa', rule='#341b4b',
        sheen='#b99cff', sheen_op=0.11,
    ),
}

FONT_TITLE = Font('Lexend', 600)
FONT_BODY = Font('Lexend', 400)
FONT_LINK = Font('Lexend', 500)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'brand', 'brand.json'),
          encoding='utf-8') as _fh:
    _ICONS = json.load(_fh)['icons']


def f(v: float) -> str:
    s = f'{v:.2f}'.rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


# ---------------------------------------------------------------- Zeilenumbruch

def _tokens(text: str) -> list[tuple[str, str]]:
    """Trennstellen als (Stück, Trenner danach).

    - an Leerzeichen (Trenner ' ')
    - nach einem vorhandenen Bindestrich in Komposita mit mindestens 4 Buchstaben davor
      („Desaster-|Recovery“, nicht „IT-|Umgebung“ oder „Backup-,“) – Trenner ''
    - Gedankenstrich bleibt am vorigen Wort (Umbruch erst danach)
    """
    words: list[str] = []
    for w in text.split(' '):
        if w in ('–', '—') and words:
            words[-1] += ' ' + w
        else:
            words.append(w)
    out: list[tuple[str, str]] = []
    for w in words:
        parts, cur = [], ''
        for k, ch in enumerate(w):
            cur += ch
            nxt = w[k + 1] if k + 1 < len(w) else ''
            if ch == '-' and nxt.isalpha() and sum(c.isalpha() for c in cur.split('-')[-2]) >= 4:
                parts.append(cur)
                cur = ''
        parts.append(cur)
        out += [(p, '') for p in parts[:-1]] + [(parts[-1], ' ')]
    return out


HYPHEN_PENALTY = 4000.0      # Umbruch am Bindestrich nur, wenn er spürbar ausgeglichener ist


def wrap_balanced(font: Font, text: str, size: float, max_w: float, max_lines: int = 3) -> list[str]:
    """Kleinste Zeilenzahl, die passt; darin die Aufteilung mit dem gleichmäßigsten Flattersatz."""
    toks = _tokens(text)
    n = len(toks)
    cache: dict[tuple[int, int], tuple[str, float]] = {}

    def line(i: int, j: int) -> tuple[str, float]:
        if (i, j) not in cache:
            t = ''.join(p + sep for p, sep in toks[i:j - 1]) + toks[j - 1][0]
            cache[(i, j)] = (t, font.measure(t.replace(' ', ' '), size))
        return cache[(i, j)]

    for lines in range(1, max_lines + 1):
        best = None

        def rec(start: int, left: int, acc: list[tuple[int, int]]):
            nonlocal best
            if left == 1:
                if line(start, n)[1] <= max_w:
                    cand = acc + [(start, n)]
                    widths = [line(a, b)[1] for a, b in cand]
                    hyph = sum(1 for a, b in cand[:-1] if toks[b - 1][1] == '')
                    # gleichmäßige Zeilen; letzte Zeile darf kürzer sein, aber kein einzelnes Wort
                    cost = sum((max_w - x) ** 2 for x in widths[:-1]) +                         max(0.0, (max(widths) * 0.6 - widths[-1])) ** 2 * 4 +                         (max(widths) - min(widths)) ** 2 + hyph * HYPHEN_PENALTY
                    if best is None or cost < best[0]:
                        best = (cost, cand)
                return
            for end in range(start + 1, n - left + 2):
                if line(start, end)[1] > max_w:
                    break
                rec(end, left - 1, acc + [(start, end)])

        rec(0, lines, [])
        if best:
            return [line(a, b)[0].replace(' ', ' ') for a, b in best[1]]
    raise ValueError(f'Text passt nicht in {max_lines} Zeilen: {text}')


# ---------------------------------------------------------------- Icon optisch ausgleichen

def icon_bbox(name: str) -> tuple[float, float, float, float]:
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.svgLib.path import parse_path
    x0 = y0 = float('inf')
    x1 = y1 = float('-inf')
    for d in _ICONS[name]['paths']:
        bp = BoundsPen(None)
        parse_path(d, bp)
        a, b, c, e = bp.bounds
        x0, y0, x1, y1 = min(x0, a), min(y0, b), max(x1, c), max(y1, e)
    return x0, y0, x1, y1


# Zielgröße je Icon (geometrisches Mittel der Tintenbox) – flächige Icons etwas kleiner
ICON_OPTICAL = {'cloud': 49, 'backup': 45, 'software': 48, 'it': 40, 'managed': 41, 'ai': 41}
ICON_SHIFT = {'cloud': (0, 3)}   # Wolke etwas tiefer: oben Platz für die aufsteigenden Bits


def placed_icon(name: str, cx: float, cy: float, attrs: str) -> tuple[str, float, float, float]:
    """Icon so platzieren, dass seine Tintenbox mittig auf (cx, cy) sitzt.

    Liefert (svg, s, ox, oy) – Icon-Koordinate p wird zu (ox + p.x·s, oy + p.y·s).
    """
    vx, vy, vw, vh = (float(v) for v in _ICONS[name]['viewBox'].split())
    bx0, by0, bx1, by1 = icon_bbox(name)
    dx, dy = ICON_SHIFT.get(name, (0, 0))
    s = ICON_OPTICAL[name] / math.sqrt((bx1 - bx0) * (by1 - by0))
    ox = cx + dx - (bx0 + bx1) / 2 * s
    oy = cy + dy - (by0 + by1) / 2 * s
    # brand.icon erwartet Größe + linke obere Ecke der viewBox-Fläche
    size = max(vw, vh) * s
    x = ox - (size - vw * s) / 2 + vx * s
    y = oy - (size - vh * s) / 2 + vy * s
    return icon(name, size, x, y, attrs), s, ox, oy


# ---------------------------------------------------------------- Zusatzbewegungen je Icon

def overlay(name: str, th: dict, start: float, s: float, ox: float, oy: float) -> tuple[str, str, str, str]:
    """(hinter_der_kachel, zwischen_kachel_und_icon, über_dem_icon, css) für die Icon-Zusatzbewegung."""
    acc = th['accent']
    below = mid = above = css = ''
    if name == 'cloud':
        # kleine Bits steigen hinter der Wolke auf und verblassen
        bx0, by0, bx1, by1 = icon_bbox('cloud')
        top = oy + by0 * s
        bits = [(TCX - 9, 5.5), (TCX + 4, 4.5), (TCX + 14, 5.0)]
        for k, (x, sz) in enumerate(bits):
            mid += (f'<rect class="bit" x="{f(x - sz / 2)}" y="{f(top + 3)}" width="{f(sz)}" '
                      f'height="{f(sz)}" rx="1.2" fill="{acc}" '
                      f'style="animation-delay:{f(start + k * 2.0 + (0.7 if k == 1 else 0))}s"/>')
        css += ('.bit{opacity:0;transform-box:fill-box;transform-origin:50% 50%;'
                'animation:bit 6s cubic-bezier(.33,.6,.4,1) infinite both}'
                '@keyframes bit{0%{opacity:0;transform:translateY(0)}'
                '14%{opacity:.85}'
                '52%,100%{opacity:0;transform:translateY(-22px)}}')
    elif name == 'backup':
        # Bogen mit weichem Schweif kreist entgegen dem Uhrzeigersinn (wie der Icon-Pfeil)
        r = 32.5
        c = 2 * math.pi * r
        head, tail = c * 0.16, c * 0.34
        above += (f'<g class="orbit">'
                  f'<circle cx="{f(TCX)}" cy="{f(TCY)}" r="{r}" fill="none" stroke="{acc}" '
                  f'stroke-width="2.2" stroke-linecap="round" opacity=".22" '
                  f'stroke-dasharray="{f(tail)} {f(c - tail)}"/>'
                  f'<circle cx="{f(TCX)}" cy="{f(TCY)}" r="{r}" fill="none" stroke="{acc}" '
                  f'stroke-width="2.2" stroke-linecap="round" opacity=".7" '
                  f'stroke-dasharray="{f(head)} {f(c - head)}"/></g>')
        css += (f'.orbit{{transform-box:view-box;transform-origin:{f(TCX)}px {f(TCY)}px;'
                f'animation:orbit 8s linear {f(start)}s infinite}}'
                '@keyframes orbit{to{transform:rotate(-360deg)}}')
    elif name == 'software':
        # Cursor-Balken zwischen den Code-Klammern, in Kachelfarbe (wirkt wie Teil des Icons)
        cx = ox + 64.66 * s
        cy = oy + 54.58 * s
        cw, ch = 4.4 * s, 19 * s
        above += (f'<rect class="cur" x="{f(cx - cw / 2)}" y="{f(cy - ch / 2)}" width="{f(cw)}" '
                  f'height="{f(ch)}" rx="{f(cw / 2)}" fill="url(#tile)"/>')
        css += (f'.cur{{animation:cur 6s ease-in-out {f(start)}s infinite}}'
                '@keyframes cur{0%,22%,33.3%,55%,66.6%,88%,100%{opacity:1}'
                '27%,29%,60%,62%,93%,95%{opacity:0}}')
    elif name == 'it':
        # gestrichelter Ring dreht sich langsam (Abstand zum Zahnrad unten rechts beachten)
        r = 33.5
        c = 2 * math.pi * r
        seg = c / 20
        above += (f'<circle class="ring" cx="{f(TCX)}" cy="{f(TCY)}" r="{r}" fill="none" '
                  f'stroke="{acc}" stroke-width="1.8" stroke-linecap="round" opacity=".55" '
                  f'stroke-dasharray="{f(seg * 0.42)} {f(seg * 0.58)}"/>')
        css += ('.ring{transform-box:fill-box;transform-origin:50% 50%;'
                f'animation:ring 28s linear {f(start)}s infinite}}'
                '@keyframes ring{to{transform:rotate(360deg)}}')
    elif name == 'managed':
        # Puls-Ringe: die Kachelkontur hallt zweimal nach außen
        for k in range(2):
            below += (f'<rect class="pulse" x="{TILE_X}" y="{TILE_Y}" width="{TILE}" height="{TILE}" '
                      f'rx="{TILE_R}" fill="none" stroke="{acc}" stroke-width="1.6" '
                      f'style="animation-delay:{f(start + k * 0.7)}s"/>')
        css += ('.pulse{opacity:0;transform-box:fill-box;transform-origin:50% 50%;'
                'animation:pulse 6s cubic-bezier(.25,.6,.35,1) infinite both}'
                '@keyframes pulse{0%{opacity:0;transform:scale(1)}'
                '6%{opacity:.55}'
                '40%,100%{opacity:0;transform:scale(1.24)}}')
    elif name == 'ai':
        # zarte Funkel-Sterne an der Kachel
        # zwei Sterne als Gruppe an der oberen rechten Ecke, einer unten links – Abstand zum Titel
        stars = [(TILE_X + TILE - 4, TILE_Y + 4, 9.0), (TILE_X + TILE + 11, TILE_Y - 6, 5.5),
                 (TILE_X + 6, TILE_Y + TILE - 2, 6.5)]
        for k, (x, y, rr) in enumerate(stars):
            q = rr * 0.18
            d = (f'M{f(x)} {f(y - rr)}Q{f(x + q)} {f(y - q)} {f(x + rr)} {f(y)}'
                 f'Q{f(x + q)} {f(y + q)} {f(x)} {f(y + rr)}Q{f(x - q)} {f(y + q)} {f(x - rr)} {f(y)}'
                 f'Q{f(x - q)} {f(y - q)} {f(x)} {f(y - rr)}Z')
            above += (f'<path class="star" d="{d}" fill="{acc}" '
                      f'style="animation-delay:{f(start + k * 2.0)}s"/>')
        css += ('.star{transform-box:fill-box;transform-origin:50% 50%;'
                'animation:star 6s ease-in-out infinite both}'
                '@keyframes star{0%{opacity:0;transform:scale(0) rotate(0)}'
                '12%{opacity:1;transform:scale(1) rotate(45deg)}'
                '26%,100%{opacity:0;transform:scale(0) rotate(90deg)}}')
    return below, mid, above, css


# ---------------------------------------------------------------- Karte

def build(i: int, spec: dict, mode: str) -> str:
    th = THEMES[mode]
    defs = GlyphDefs(f'c{i}{mode[0]}')
    row, col = divmod(i, 2)
    d_in = i * 0.12                                   # Einblendung gestaffelt nach Index
    d_sheen = SHEEN_START + 1.0 * col + 0.5 * row     # Welle diagonal durch das 2er-Raster
    d_arrow = d_sheen + 0.95                          # Pfeil stupst, wenn der Schimmer ihn erreicht
    d_icon = 1.6 + d_in

    # ---- Texte
    title = FONT_TITLE.text(spec['title'], TITLE_SIZE, TITLE_X,
                            TCY + FONT_TITLE.cap_height / 1000 * TITLE_SIZE / 2,
                            defs=defs, attrs=f'fill="{th["title"]}"')
    lines = wrap_balanced(FONT_BODY, spec['text'], BODY_SIZE, BODY_W)
    body = ''.join(FONT_BODY.text(t, BODY_SIZE, PAD, BODY_Y + k * BODY_LH, defs=defs)
                   for k, t in enumerate(lines))
    link_end = W - PAD - ARROW_W - ARROW_GAP
    link_w = FONT_LINK.measure('Mehr erfahren', LINK_SIZE)
    link = FONT_LINK.text('Mehr erfahren', LINK_SIZE, link_end, LINK_Y, anchor='end', defs=defs)
    ay = LINK_Y - FONT_LINK.x_height / 1000 * LINK_SIZE / 2 - 1
    ax0, ax1 = W - PAD - ARROW_W, W - PAD
    arrow = (f'<path class="arrow" d="M{f(ax0)} {f(ay)}H{f(ax1)}M{f(ax1 - 6.5)} {f(ay - 6.5)}'
             f'L{f(ax1)} {f(ay)}L{f(ax1 - 6.5)} {f(ay + 6.5)}" fill="none" stroke="{th["link"]}" '
             f'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')
    rule_x1 = link_end - link_w - 24
    rule = (f'<path d="M{PAD} {f(ay)}H{f(rule_x1)}" stroke="{th["rule"]}" stroke-width="1.5" '
            f'stroke-linecap="round"/>')

    # ---- Icon + Zusatzbewegung
    ic, s, ox, oy = placed_icon(spec['icon'], TCX, TCY, f'fill="{th["icon"]}"')
    below, mid, above, css_icon = overlay(spec['icon'], th, d_icon, s, ox, oy)

    # ---- Defs
    sheen_c = th['sheen']
    defs_svg = (
        f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{th["bg0"]}"/><stop offset="1" stop-color="{th["bg1"]}"/></linearGradient>'
        f'<radialGradient id="glow" cx="{W}" cy="0" r="340" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{th["glow"]}" stop-opacity="{th["glow_op"]}"/>'
        f'<stop offset="1" stop-color="{th["glow"]}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="edge" x1="0" y1="0" x2="{W}" y2="{H}" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{th["stroke0"]}"/><stop offset="1" stop-color="{th["stroke1"]}"/></linearGradient>'
        f'<linearGradient id="tile" x1="{TILE_X}" y1="{TILE_Y}" x2="{TILE_X + TILE}" y2="{TILE_Y + TILE}" '
        f'gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{th["tile0"]}"/>'
        f'<stop offset="1" stop-color="{th["tile1"]}"/></linearGradient>'
        f'<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{sheen_c}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{sheen_c}" stop-opacity="{th["sheen_op"]}"/>'
        f'<stop offset="1" stop-color="{sheen_c}" stop-opacity="0"/></linearGradient>'
        f'<pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse" x="{W - 8}" y="8">'
        f'<circle cx="0" cy="0" r="1.3" fill="{th["dots"]}"/></pattern>'
        f'<radialGradient id="fade" cx="{W}" cy="0" r="200" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="#fff"/><stop offset=".55" stop-color="#fff" stop-opacity=".45"/>'
        f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        f'<mask id="dm"><rect x="300" width="300" height="200" fill="url(#fade)"/></mask>'
        f'<clipPath id="clip"><rect x="0" y="0" width="{W}" height="{H}" rx="{R}"/></clipPath>'
        + defs.render()
    )
    # defs.render() muss nach allen Texten aufgerufen werden – Texte sind oben bereits gesetzt

    body_svg = (
        f'<g class="card">'
        f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="{R - .75}" fill="url(#bg)"/>'
        f'<g clip-path="url(#clip)">'
        f'<rect x="200" y="0" width="400" height="300" fill="url(#glow)"/>'
        f'<rect x="300" y="0" width="300" height="200" fill="url(#dots)" opacity="{th["dots_op"]}" mask="url(#dm)"/>'
        f'<g class="sheen"><rect x="-240" y="-60" width="170" height="420" fill="url(#sh)" '
        f'transform="skewX(-18)"/></g>'
        f'</g>'
        f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="{R - .75}" fill="none" '
        f'stroke="url(#edge)" stroke-width="1.5"/>'
        # Kachel mit Icon
        f'<g class="in i1">{below}'
        f'<rect x="{TILE_X}" y="{TILE_Y}" width="{TILE}" height="{TILE}" rx="{TILE_R}" fill="url(#tile)"/>'
        f'<rect x="{TILE_X + .75}" y="{TILE_Y + .75}" width="{TILE - 1.5}" height="{TILE - 1.5}" '
        f'rx="{TILE_R - .75}" fill="none" stroke="{th["tile_stroke"]}" stroke-opacity="{th["tile_stroke_op"]}" '
        f'stroke-width="1.5"/>'
        f'{mid}{ic}{above}</g>'
        f'<g class="in i2">{title}</g>'
        f'<g class="in i3" fill="{th["body"]}">{body}</g>'
        f'<g class="in i4">{rule}<g fill="{th["link"]}">{link}</g>{arrow}</g>'
        f'</g>'
    )

    css = (
        f'.card{{transform-box:view-box;transform-origin:300px 0;'
        f'animation:cardIn .9s {EASE} {f(d_in)}s both}}'
        '@keyframes cardIn{from{opacity:0;transform:translateY(8px) scale(.97)}}'
        f'.in{{transform-box:view-box;transform-origin:0 0;animation:rise .8s {EASE} both}}'
        '@keyframes rise{from{opacity:0;transform:translateY(10px)}}'
        + ''.join(f'.i{k}{{animation-delay:{f(d_in + 0.1 + k * 0.08)}s}}' for k in range(1, 5))
        + f'.sheen{{transform-box:view-box;transform-origin:0 0;'
        f'animation:sheen {f(SHEEN_PERIOD)}s cubic-bezier(.45,.05,.3,1) {f(d_sheen)}s infinite both}}'
        '@keyframes sheen{0%{transform:translateX(0)}17%,100%{transform:translateX(1000px)}}'
        f'.arrow{{transform-box:view-box;transform-origin:0 0;'
        f'animation:nudge {f(SHEEN_PERIOD)}s cubic-bezier(.45,0,.3,1) {f(d_arrow)}s infinite both}}'
        '@keyframes nudge{0%,12%,100%{transform:translateX(0)}5%{transform:translateX(5px)}}'
        + css_icon
    )
    return svg_doc(W, H, body_svg, title=f'BW.Tech – {spec["title"]}', desc=spec['text'],
                   css=css, defs=defs_svg)


# README-Raster: zwei Karten je Reihe, Fuge als unsichtbares Bild mit Prozentbreite.
# Ein Leerzeichen als Fuge wäre nur ~4 px breit; feste px-Abstände (&nbsp;, hspace) würden auf
# schmalen Bildschirmen umbrechen. Mit 48,25 % + 2,5 % + 48,25 % (ohne Leerraum dazwischen) bleibt
# die Fuge ≈ 22 px – so hoch wie der Absatzabstand zwischen den Reihen – und es bricht nie um.
CARD_WIDTH = '48.25%'
GAP_WIDTH = '2.5%'
GAP_FILE = 'card-gap.svg'


def readme_html() -> str:
    """HTML-Ausschnitt fürs README: 3 Reihen à 2 Karten, je verlinkt, hell/dunkel per <picture>."""
    rows = []
    for r in range(0, len(CARDS), 2):
        cells = []
        for k, spec in enumerate(CARDS[r:r + 2]):
            n = spec['icon']
            alt = f'{spec["title"]}: {spec["text"]}'
            # Fuge im Link der linken Karte – sonst verlinkt GitHub das Fugenbild auf sich selbst
            gap = f'<img src="assets/{GAP_FILE}" width="{GAP_WIDTH}" alt="">' if k == 0 else ''
            cells.append(
                f'<a href="{spec["url"]}"><picture>'
                f'<source media="(prefers-color-scheme: dark)" srcset="assets/card-{n}-dark.svg">'
                f'<img src="assets/card-{n}-light.svg" width="{CARD_WIDTH}" alt="{alt}">'
                f'</picture>{gap}</a>')
        rows.append('<p align="center">\n' + ''.join(cells) + '\n</p>')
    return '\n'.join(rows) + '\n'


def gap_svg() -> str:
    """Unsichtbares Fugenbild (1×1, transparent) – GitHub hinterlegt Bilder mit der Seitenfarbe."""
    return svg_doc(1, 1, '', title='Abstand zwischen den Lösungskarten')


def main() -> None:
    if '--readme' in sys.argv:
        sys.stdout.reconfigure(encoding='utf-8')
        print(readme_html(), end='')
        return
    p = write_asset(GAP_FILE, gap_svg())
    print('geschrieben', os.path.relpath(p, brand.ROOT), os.path.getsize(p), 'B')
    for i, spec in enumerate(CARDS):
        for mode in THEMES:
            p = write_asset(f'card-{spec["icon"]}-{mode}.svg', build(i, spec, mode))
            print('geschrieben', os.path.relpath(p, brand.ROOT), os.path.getsize(p), 'B')


if __name__ == '__main__':
    main()
