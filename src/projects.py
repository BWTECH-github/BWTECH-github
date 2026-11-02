"""Projektkarten für die öffentlichen Repositorys (owncloud.online, client, Android, IOS-App).

Je Repo eine Karte 600×200 (r=20) in Hell und Dunkel:
eigenes Geräte-Icon in einer Kachel, Anzeigename, Repo-Name mit Repo-Symbol,
Sprach-Punkt, zweizeilige Beschreibung (aus den READMEs), Pfeil als Link-Hinweis.
Bewusst ohne Sterne/Zahlen – die veralten.

Erzeugt assets/project-<repo>-light.svg und -dark.svg.
Aufruf: python src/projects.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import brand  # noqa: E402
from textpath import Font, GlyphDefs  # noqa: E402

W, H = 600, 200
R = 20
EASE = 'cubic-bezier(.2,.8,.2,1)'

# Inhalte aus den READMEs der Repos (Stand gh api …/readme); max. 2 Zeilen
PROJECTS = [
    {
        'repo': 'owncloud.online', 'name': 'owncloud.online', 'lang': 'PHP', 'icon': 'server',
        'lines': ('Dateiablage, Freigaben und Zusammenarbeit', 'auf dem eigenen Server.'),
        'alt': 'Server-Plattform für Dateiablage, Freigaben und Zusammenarbeit',
    },
    {
        'repo': 'client', 'name': 'Desktop-Client', 'lang': 'C++', 'icon': 'desktop',
        'lines': ('Hält Dateien zwischen Server und Rechner', 'abgeglichen – für Windows, macOS und Linux.'),
        'alt': 'Desktop-Client für Windows, macOS und Linux',
    },
    {
        'repo': 'Android', 'name': 'Android-App', 'lang': 'Kotlin', 'icon': 'android',
        'lines': ('Dateien ansehen, teilen und offline halten,', 'Fotos und Videos automatisch hochladen.'),
        'alt': 'Android-App: Dateien ansehen, teilen, offline halten und automatisch hochladen',
    },
    {
        'repo': 'IOS-App', 'name': 'iOS-App', 'lang': 'Swift', 'icon': 'ios',
        'lines': ('Dateien ansehen und teilen – direkt in der', 'Dateien-App von iOS, auch auf dem iPad.'),
        'alt': 'iOS-App: Dateien ansehen und teilen, eingebunden in die Dateien-App',
    },
]

THEMES = {
    'light': {
        'card': '#ffffff', 'card2': brand.LAVENDER_PALE, 'edge_a': '#d6c4f2', 'edge_b': '#ebe2f8',
        'glow': brand.LAVENDER, 'grid': '#d3c1ee',
        'title': brand.PURPLE, 'meta': '#5e4b78', 'text': '#2c1f40', 'accent': brand.VIOLET,
        'tile_a': brand.PURPLE, 'tile_b': brand.VIOLET, 'icon': '#ffffff',
    },
    'dark': {
        'card': '#22002f', 'card2': '#1a0b26', 'edge_a': '#4a2a68', 'edge_b': '#2c1640',
        'glow': '#3a0f5c', 'grid': '#3b2456',
        'title': brand.LAVENDER_LIGHT, 'meta': '#b4a3d0', 'text': '#cdbbe9', 'accent': '#a78bfa',
        'tile_a': '#4a0a6b', 'tile_b': brand.VIOLET, 'icon': '#ffffff',
    },
}

# Layout
PAD = 28
TILE = 64
TILE_R = 16
TEXT_X = PAD + TILE + 20          # 112
TITLE_SIZE, TITLE_BASE = 30, 54
META_SIZE, META_BASE = 22, 86
DESC_SIZE, DESC_BASE, DESC_LH = 22, 140, 30
DESC_MAX_W = W - 2 * PAD          # 544


# ---------------------------------------------------------------- Hilfen
def _lum(hex_color: str) -> float:
    h = hex_color.lstrip('#')
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        out.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = out
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def _f(v: float) -> str:
    s = f'{v:.2f}'.rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


# ---------------------------------------------------------------- Icons (selbst gezeichnet, 40×40)
# Linien-Icons, Strich 2,4, runde Enden – Farbe über stroke/fill des umgebenden <g>
ICONS = {
    # Server-Plattform: drei Einschübe mit Status-LEDs
    'server': (
        '<rect x="6" y="5" width="28" height="9" rx="2.6"/>'
        '<rect x="6" y="15.5" width="28" height="9" rx="2.6"/>'
        '<rect x="6" y="26" width="28" height="9" rx="2.6"/>'
        '<path d="M22 9.5h7M22 20h7M22 30.5h7"/>'
        '<circle class="led" cx="11.5" cy="9.5" r="1.6" stroke="none" fill="currentColor"/>'
        '<circle class="led l2" cx="11.5" cy="20" r="1.6" stroke="none" fill="currentColor"/>'
        '<circle class="led l3" cx="11.5" cy="30.5" r="1.6" stroke="none" fill="currentColor"/>'
    ),
    # Desktop-Client: Bildschirm mit Abgleich-Pfeilen
    'desktop': (
        '<rect x="3.5" y="6" width="33" height="22.5" rx="3"/>'
        '<path d="M20 28.5v5.5M13 34.5h14"/>'
        '<g class="sync">'
        '<path d="M14.6 15.2a6 6 0 0 1 10.3-1.9"/><path d="M25.6 10.6v3.4h-3.4"/>'
        '<path d="M25.4 19.3a6 6 0 0 1-10.3 1.9"/><path d="M14.4 23.9v-3.4h3.4"/>'
        '</g>'
    ),
    # Android-App: Telefon mit Kamera-Loch, Upload-Pfeil (automatischer Upload)
    'android': (
        '<rect x="10" y="3" width="20" height="34" rx="4"/>'
        '<circle cx="20" cy="7.6" r="1.25" stroke="none" fill="currentColor"/>'
        '<g class="up"><path d="M20 26.5v-11"/><path d="M15.8 19.4 20 15.2l4.2 4.2"/></g>'
        '<path d="M15 31h10" opacity=".55"/>'
    ),
    # iOS-App: Telefon mit Kamerainsel und Home-Balken, Ordner (Dateien-App)
    'ios': (
        '<rect x="10" y="3" width="20" height="34" rx="5"/>'
        '<path d="M17.4 7.4h5.2" stroke-width="2.6"/>'
        '<path d="M17 32.6h6" opacity=".55"/>'
        '<path class="fold" d="M13.8 16a1.8 1.8 0 0 1 1.8-1.8h3l1.8 2h4a1.8 1.8 0 0 1 1.8 1.8v6'
        'a1.8 1.8 0 0 1-1.8 1.8h-8.8a1.8 1.8 0 0 1-1.8-1.8z"/>'
    ),
}

# Repo-Symbol (Buch), 16×16
REPO_ICON = (
    '<path d="M3 13.2V3.4A1.6 1.6 0 0 1 4.6 1.8H13v10.4H4.6A1.6 1.6 0 0 0 3 13.8 1.6 1.6 0 0 0 4.6 15.4H13"/>'
    '<path d="M6 5h4"/>'
)

# Pfeil „öffnen“ (nach rechts oben), 20×20
ARROW = '<path d="M5.5 14.5 14.5 5.5M7.5 5.5h7v7"/>'


# ---------------------------------------------------------------- Karte
def build(p: dict, theme_name: str, idx: int) -> str:
    th = THEMES[theme_name]
    defs = GlyphDefs('p')
    f_title = Font('Lexend', 600)
    f_text = Font('Lexend', 400)

    # Kontraste prüfen (Fließtext 22 → ≥ 4,5:1, auch gegen die dunklere Kartenecke)
    for key in ('title', 'meta', 'text'):
        for bg in (th['card'], th['card2']):
            c = contrast(th[key], bg)
            assert c >= 4.5, f'{theme_name}/{key}: Kontrast {c:.2f}'
    for line in p['lines']:
        lw = f_text.measure(line, DESC_SIZE)
        assert lw <= DESC_MAX_W, f'{p["repo"]}: Zeile zu lang ({lw:.0f} > {DESC_MAX_W}): {line}'

    d = idx * 0.12   # gestaffelte Einblendung über die vier Karten im Raster
    css = (
        '.e{transform-box:fill-box;transform-origin:50% 50%;'
        f'animation:fu .7s {EASE} both}}'
        '@keyframes fu{from{opacity:0;transform:translateY(8px)}}'
        f'.bg{{animation-name:fi;animation-duration:.6s;animation-delay:{d:.2f}s}}'
        '@keyframes fi{from{opacity:0}}'
        f'.ti{{animation-name:zi;animation-delay:{d + .1:.2f}s}}'
        '@keyframes zi{from{opacity:0;transform:scale(.86)}}'
        f'.tt{{animation-name:sl;animation-delay:{d + .18:.2f}s}}'
        f'.mt{{animation-name:sl;animation-delay:{d + .26:.2f}s}}'
        '@keyframes sl{from{opacity:0;transform:translateX(-10px)}}'
        f'.d1{{animation-delay:{d + .34:.2f}s}}.d2{{animation-delay:{d + .42:.2f}s}}'
        f'.ar{{animation-name:ar;animation-delay:{d + .5:.2f}s}}'
        '@keyframes ar{from{opacity:0;transform:translate(-5px,5px)}}'
        # ruhiger Glanz über die Kachel: kurzer Durchlauf, dann lange Pause (Periode 9 s)
        '.sh{transform-box:view-box;transform-origin:0 0;'
        f'animation:sh 9s ease-in-out {d + 1.4:.2f}s infinite}}'
        '@keyframes sh{0%{transform:translateX(0)}16%,100%{transform:translateX(170px)}}'
        # je Icon ein ruhiges Detail (Periode 6–8 s, nahtlos)
        '.led{animation:led 6s ease-in-out infinite}.l2{animation-delay:-2s}.l3{animation-delay:-4s}'
        '@keyframes led{0%,100%{opacity:1}50%{opacity:.35}}'
        '.sync{transform-box:fill-box;transform-origin:50% 50%;'
        f'animation:sy 8s cubic-bezier(.6,0,.2,1) {d + 2.4:.2f}s infinite}}'
        # 180° – das Pfeilpaar ist punktsymmetrisch, Ende = Anfang
        '@keyframes sy{0%,70%{transform:rotate(0)}90%,100%{transform:rotate(180deg)}}'
        '.up{transform-box:fill-box;transform-origin:50% 50%;'
        f'animation:up 8s ease-in-out {d + 2.4:.2f}s infinite}}'
        '@keyframes up{0%,66%,100%{transform:translateY(0);opacity:1}'
        '78%{transform:translateY(-5px);opacity:0}79%{transform:translateY(5px);opacity:0}'
        '92%{transform:translateY(0);opacity:1}}'
        '.fold{transform-box:fill-box;transform-origin:50% 100%;'
        f'animation:fo 8s ease-in-out {d + 2.4:.2f}s infinite}}'
        '@keyframes fo{0%,70%,88%,100%{transform:translateY(0)}79%{transform:translateY(-2.5px)}}'
        # weiches Licht oben rechts atmet langsam
        '.gl{animation:gl 10s ease-in-out infinite alternate}'
        '@keyframes gl{from{opacity:1}to{opacity:.55}}'
    )

    gx0, gy0 = PAD, PAD
    defs_extra = (
        f'<linearGradient id="pcg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{th["card"]}"/><stop offset="1" stop-color="{th["card2"]}"/>'
        '</linearGradient>'
        f'<radialGradient id="pgl" cx="1" cy="0" r="1">'
        f'<stop offset="0" stop-color="{th["glow"]}" stop-opacity=".95"/>'
        f'<stop offset=".6" stop-color="{th["glow"]}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="ptg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{th["tile_a"]}"/><stop offset="1" stop-color="{th["tile_b"]}"/>'
        '</linearGradient>'
        f'<linearGradient id="ped" x1="0" y1="0" x2="{W}" y2="{H}" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{th["edge_a"]}"/><stop offset="1" stop-color="{th["edge_b"]}"/>'
        '</linearGradient>'
        '<linearGradient id="psg" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset=".5" stop-color="#fff" stop-opacity=".38"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<clipPath id="pcl"><rect x="{gx0}" y="{gy0}" width="{TILE}" height="{TILE}" rx="{TILE_R}"/></clipPath>'
        f'<clipPath id="pcc"><rect width="{W}" height="{H}" rx="{R}"/></clipPath>'
        f'<pattern id="ppt" width="16" height="16" patternUnits="userSpaceOnUse">'
        f'<circle cx="8" cy="8" r="1.3" fill="{th["grid"]}"/></pattern>'
        '<radialGradient id="pmg" cx="1" cy="0" r="1">'
        '<stop offset="0" stop-color="#fff" stop-opacity="1"/>'
        '<stop offset=".75" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        f'<mask id="pmk" maskUnits="userSpaceOnUse" x="300" y="0" width="300" height="{H}">'
        f'<rect x="300" y="0" width="300" height="{H}" fill="url(#pmg)"/></mask>'
    )

    # Hintergrund: Fläche, weiches Licht, Punktraster oben rechts, feine Kontur
    bg = (
        '<g class="e bg">'
        f'<rect width="{W}" height="{H}" rx="{R}" fill="url(#pcg)"/>'
        '<g clip-path="url(#pcc)">'
        f'<rect class="gl" x="260" y="-120" width="440" height="300" fill="url(#pgl)"/>'
        f'<rect x="300" y="0" width="300" height="{H}" fill="url(#ppt)" mask="url(#pmk)"/>'
        '</g>'
        f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="{R - .75}" fill="none" '
        'stroke="url(#ped)" stroke-width="1.5"/>'
        '</g>'
    )

    # Kachel mit Icon und Glanz
    tile = (
        '<g class="e ti">'
        f'<rect x="{gx0}" y="{gy0}" width="{TILE}" height="{TILE}" rx="{TILE_R}" fill="url(#ptg)"/>'
        f'<g transform="translate({gx0 + 12} {gy0 + 12})" fill="none" stroke="{th["icon"]}" '
        f'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" color="{th["icon"]}">'
        f'{ICONS[p["icon"]]}</g>'
        '<g clip-path="url(#pcl)"><g class="sh">'
        f'<rect x="{gx0 - 70}" y="{gy0 - 20}" width="36" height="{TILE + 40}" fill="url(#psg)" '
        f'transform="rotate(18 {gx0 - 52} {gy0 + TILE / 2})"/>'
        '</g></g>'
        '</g>'
    )

    # Titel
    title = f_title.text(p['name'], TITLE_SIZE, TEXT_X, TITLE_BASE, defs=defs,
                         attrs=f'class="e tt" fill="{th["title"]}"')

    # Meta-Zeile: Repo-Symbol + Repo-Name · Sprach-Punkt + Sprache
    mx = TEXT_X
    repo_w = f_text.measure(p['repo'], META_SIZE)
    icon_s = 1.15
    icon_y = META_BASE - 7.7 - 8.6 * icon_s   # Symbolmitte auf Versalmitte
    meta = (
        f'<g class="e mt">'
        f'<g transform="translate({mx - 1} {_f(icon_y)}) scale({icon_s})" fill="none" stroke="{th["meta"]}" stroke-width="1.5" '
        f'stroke-linecap="round" stroke-linejoin="round">{REPO_ICON}</g>'
        + f_text.text(p['repo'], META_SIZE, mx + 26, META_BASE, defs=defs, attrs=f'fill="{th["meta"]}"')
    )
    lx = mx + 26 + repo_w + 22
    meta += (
        f'<circle cx="{_f(lx + 6)}" cy="{_f(META_BASE - 7.7)}" r="6" fill="{th["accent"]}"/>'
        + f_text.text(p['lang'], META_SIZE, lx + 20, META_BASE, defs=defs, attrs=f'fill="{th["meta"]}"')
        + '</g>'
    )

    # Beschreibung
    desc = ''.join(
        f_text.text(line, DESC_SIZE, PAD, DESC_BASE + i * DESC_LH, defs=defs,
                    attrs=f'class="e d{i + 1}" fill="{th["text"]}"')
        for i, line in enumerate(p['lines'])
    )

    # Pfeil oben rechts (Link-Hinweis)
    arrow = (
        f'<g class="e ar"><g transform="translate({W - PAD - 22} {PAD + 2}) scale(1.1)" fill="none" '
        f'stroke="{th["accent"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        f'{ARROW}</g></g>'
    )

    body = bg + tile + title + meta + desc + arrow
    t = f'{p["name"]} – Repository BWTECH-github/{p["repo"]}'
    dsc = f'{p["alt"]}. Sprache: {p["lang"]}. {" ".join(p["lines"])}'
    return brand.svg_doc(W, H, body, title=t, desc=dsc, css=css, defs=defs.render() + defs_extra)


def main() -> None:
    for idx, p in enumerate(PROJECTS):
        for theme in THEMES:
            name = f'project-{p["repo"]}-{theme}.svg'
            path = brand.write_asset(name, build(p, theme, idx))
            print('geschrieben', os.path.relpath(path, brand.ROOT), os.path.getsize(path), 'B')


if __name__ == '__main__':
    main()
