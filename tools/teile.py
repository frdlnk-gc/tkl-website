"""Gemeinsame Bausteine: Icons, Logo, Kopf, Fuß, Hecke, Karte."""
import random, math

# ---------- Icons (Strich-Icons, 24er Raster) ----------
_I = {
 'blatt': '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10Z"/><path d="M2 21c0-3 1.9-5.4 5.1-6"/>',
 'schnee': '<path d="M12 2v20M4.9 4.9l14.2 14.2M2 12h20M4.9 19.1 19.1 4.9"/><path d="m9 4 3 3 3-3M9 20l3-3 3 3M4 9l3 3-3 3M20 9l-3 3 3 3"/>',
 'spiel': '<path d="M3 21V8l5-4 5 4v13"/><path d="M8 21v-5h0"/><path d="M13 12l7 9"/><path d="M3 12h10"/>',
 'baum': '<path d="M12 22v-7"/><path d="M8 15h8a5 5 0 0 0 1.6-9.7A5 5 0 0 0 7.5 6 4.5 4.5 0 0 0 8 15Z"/>',
 'pflaster': '<rect x="3" y="3" width="8" height="5" rx="1"/><rect x="13" y="3" width="8" height="5" rx="1"/><rect x="3" y="10" width="5" height="5" rx="1"/><rect x="10" y="10" width="11" height="5" rx="1"/><rect x="3" y="17" width="11" height="4" rx="1"/><rect x="16" y="17" width="5" height="4" rx="1"/>',
 'tel': '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2Z"/>',
 'mail': '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
 'pin': '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
 'haken': '<path d="M20 6 9 17l-5-5"/>',
 'pfeil': '<path d="M5 12h14M13 6l6 6-6 6"/>',
 'zurueck': '<path d="M19 12H5M11 18l-6-6 6-6"/>',
 'team': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
 'traktor': '<circle cx="7" cy="16" r="4"/><circle cx="18" cy="17" r="3"/><path d="M3 13V6h7l2 6h6l2 2v3"/><path d="M10 6V3"/><path d="M14 12V8h3"/>',
 'kalender': '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/><path d="m9 16 2 2 4-4"/>',
 'schild': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/>',
 'uhr': '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
 'auto': '<path d="M3 17h2m14 0h2M5 17a2 2 0 1 0 4 0 2 2 0 1 0-4 0m10 0a2 2 0 1 0 4 0 2 2 0 1 0-4 0"/><path d="M9 17h6M3 17V8a1 1 0 0 1 1-1h10v10M14 10h4l3 4v3"/>',
 'sonne': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M6.3 17.7l-1.4 1.4M19.1 4.9l-1.4 1.4"/>',
 'haus': '<path d="M3 21h18M5 21V8l7-5 7 5v13"/><path d="M9 21v-6h6v6"/><path d="M9 10h.01M15 10h.01"/>',
 'fabrik': '<path d="M2 21h20M4 21V10l5 3V10l5 3V6l6 3v12"/><path d="M8 17h1M13 17h1M18 17h1"/>',
 'stadt': '<path d="M3 21h18M5 21V5l6-2v18M11 21V9l8 3v9"/><path d="M8 8h.01M8 12h.01M8 16h.01M15 14h.01M15 18h.01"/>',
 'stern': '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1Z"/>',
 'herz': '<path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7Z"/>',
 'schluessel': '<circle cx="7.5" cy="15.5" r="5.5"/><path d="m21 2-9.6 9.6M15.5 7.5l3 3L22 7l-3-3"/>',
 'shirt': '<path d="M20.4 6.6 16 4l-1.5 1.5a3.5 3.5 0 0 1-5 0L8 4 3.6 6.6a1 1 0 0 0-.5 1.2l1.3 3.5a1 1 0 0 0 1 .7H7v9a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1v-9h1.6a1 1 0 0 0 1-.7l1.3-3.5a1 1 0 0 0-.5-1.2Z"/>',
 'lenkrad': '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="2.5"/><path d="M12 14.5V22M9.6 11.3 2.4 9.8M14.4 11.3l7.2-1.5"/>',
 'wachstum': '<path d="M3 3v18h18"/><path d="m7 15 4-4 3 3 6-7"/><path d="M15 7h5v5"/>',
 'info': '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>',
 'besen': '<path d="m13 11 8-8"/><path d="M9.5 9.5 14.5 14.5"/><path d="M4 21c1.5-3 2-6 5.5-11.5l5 5C9 18 6.5 19 4 21Z"/>',
 'liste': '<path d="M9 6h11M9 12h11M9 18h11"/><path d="m3 6 1 1 2-2M3 12l1 1 2-2M3 18l1 1 2-2"/>',
 'kaffee': '<path d="M17 8h1a4 4 0 1 1 0 8h-1"/><path d="M3 8h14v9a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4Z"/><path d="M6 2v2M10 2v2M14 2v2"/>',
 'flagge': '<path d="M4 22V4a1 1 0 0 1 1-1h12l-2 4 2 4H5"/>',
 'blitz': '<path d="M13 2 3 14h9l-1 8 10-12h-9Z"/>',
 'werkzeug': '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9Z"/>',
 'pause': '<path d="M12 2a10 10 0 1 0 10 10"/><path d="M12 6v6l4 2"/><path d="M17 2l5 0 0 5"/>',
}
def ic(name, cls=''):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}>{_I[name]}</svg>'

# ---------- Logo ----------
def logo_mark(farbe='#15191C', rot='#D8231C', gruen='#1E9E4A', blau='#2E8BD8', titel=True):
    t = '<title>TKL</title>' if titel else ''
    return f'''<svg viewBox="0 0 100 100" role="img" aria-label="TKL Logo">{t}<g transform="rotate(-3 50 50)"><g fill="{farbe}"><path d="M4 15 C30 12 62 10 96 9 L96.4 19.6 C63 20.4 31 22.4 4.8 25.6 Z"/><path d="M10.6 20 L22 19.2 C21.4 42 21.2 63 21.6 84 L9.8 85.6 C9.4 63 9.6 41 10.6 20 Z"/><path d="M79.8 15.6 L91 15 C90.2 38 90 60 90.4 83.6 L79 84.2 C78.6 61 78.8 38 79.8 15.6 Z"/><path d="M3.5 91.5 C34 83.6 66 81.4 98 82 L98 91 C67 90.4 37 93 5.5 100 Z"/><path d="M52.2 47.4 L59.6 49.2 L48.2 83.4 L40.4 83.4 Z"/><path d="M68.4 48.6 L75.6 46.8 L78.6 83.4 L71 83.4 Z"/></g><path d="M25.6 45 L35.2 42.6 L42 83.4 L31.6 83.4 Z" fill="{gruen}"/><circle cx="63.6" cy="35" r="15" fill="{rot}" stroke="{farbe}" stroke-width="4.6"/><path d="M53 83.4 L70.4 83.4 L63.4 62.4 Z" fill="{blau}"/></g></svg>'''

def marke(hell=False, link='/'):
    f = '#FFFFFF' if hell else '#15191C'
    return f'''<a class="marke" href="{link}" aria-label="TKL GmbH – zur Startseite">{logo_mark(f, '#E8352D' if hell else '#D8231C', '#2DB35C' if hell else '#1E9E4A', '#4AA3EA' if hell else '#2E8BD8', False)}<span class="marke-text"><b>TKL</b><small>Grünpflege · Winterdienst · Spielplätze</small></span></a>'''

# ---------- Hecke (Anspielung auf die Fahrzeugbeklebung) ----------
def hecke():
    random.seed(7)
    W, H = 1440, 160
    def kante(basis, rmin, rmax, seed):
        random.seed(seed); x = -20; d = f'M{-20} {H} L{-20} {basis} '
        while x < W + 20:
            r = random.uniform(rmin, rmax); nx = x + r * 1.6
            d += f'Q{x + r * .8:.1f} {basis - r * random.uniform(.9, 1.3):.1f} {nx:.1f} {basis + random.uniform(-4, 4):.1f} '
            x = nx
        return d + f'L{W + 20} {H} Z'
    return f'''<svg class="hecke" viewBox="0 0 {W} {H}" preserveAspectRatio="none" aria-hidden="true"><path d="{kante(70, 18, 34, 3)}" fill="#2f8a4a"/><path d="{kante(92, 16, 30, 9)}" fill="#1e7a3e"/><path d="{kante(118, 14, 26, 11)}" fill="#156433"/><rect x="0" y="146" width="{W}" height="14" fill="#0f4f28"/></svg>'''

# ---------- Karte Einsatzgebiet ----------
ORTE = [  # name, lat, lon, gross, dx, dy
 ('Duisburg', 51.4344, 6.7623, True, 14, -12), ('Essen', 51.4556, 7.0116, True, 14, -12), ('Castrop-Rauxel', 51.5550, 7.3110, True, -60, -22),
 ('Oberhausen', 51.4963, 6.8638, False, 10, -10), ('Mülheim', 51.4180, 6.8845, False, 10, 18), ('Bottrop', 51.5235, 6.9286, False, 10, -10),
 ('Gelsenkirchen', 51.5177, 7.0857, False, 10, -10), ('Bochum', 51.4818, 7.2162, False, 10, 18), ('Herne', 51.5380, 7.2257, False, -46, -8),
 ('Dortmund', 51.5136, 7.4653, False, -30, 22), ('Moers', 51.4516, 6.6408, False, 10, -10), ('Recklinghausen', 51.6141, 7.1979, False, -50, -12),
 ('Remscheid', 51.1787, 7.1897, False, 10, 4), ('Velbert', 51.3400, 7.0435, False, 10, 4), ('Witten', 51.4370, 7.3350, False, 10, 18),
]
STANDORTE = {'Duisburg': ('1', '#D8231C'), 'Essen': ('2', '#1E9E4A'), 'Castrop-Rauxel': ('3', '#2E8BD8')}
def proj(lat, lon):
    return (lon - 6.55) / 1.0 * 1000, (51.66 - lat) / 0.52 * 830

def karte():
    pkt = lambda la, lo: '%.0f %.0f' % proj(la, lo)
    rhein = f'M{pkt(51.15, 6.80)} C{pkt(51.28, 6.74)} {pkt(51.36, 6.76)} {pkt(51.43, 6.73)} S{pkt(51.58, 6.63)} {pkt(51.68, 6.58)}'
    ruhr = f'M{pkt(51.42, 7.62)} C{pkt(51.44, 7.40)} {pkt(51.38, 7.30)} {pkt(51.40, 7.18)} S{pkt(51.37, 7.02)} {pkt(51.40, 6.93)} S{pkt(51.44, 6.80)} {pkt(51.445, 6.735)}'
    emscher = f'M{pkt(51.50, 7.50)} C{pkt(51.53, 7.30)} {pkt(51.51, 7.10)} {pkt(51.52, 6.95)} S{pkt(51.53, 6.80)} {pkt(51.55, 6.70)}'
    pts = [proj(la, lo) for la, lo in [(51.63, 6.60), (51.66, 7.00), (51.64, 7.40), (51.52, 7.56), (51.40, 7.45), (51.33, 7.26), (51.30, 7.05), (51.34, 6.85), (51.38, 6.62)]]
    def glatt(p):  # geschlossene Catmull-Rom-Kurve als Bezier
        n = len(p); d = f'M{p[0][0]:.0f} {p[0][1]:.0f} '
        for i in range(n):
            p0, p1, p2, p3 = p[i - 1], p[i], p[(i + 1) % n], p[(i + 2) % n]
            c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6); c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
            d += f'C{c1[0]:.0f} {c1[1]:.0f} {c2[0]:.0f} {c2[1]:.0f} {p2[0]:.0f} {p2[1]:.0f} '
        return d + 'Z'
    gebiet = glatt(pts)
    out = [f'<svg viewBox="0 0 1000 830" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Karte des Einsatzgebiets im Ruhrgebiet mit den Standorten Duisburg, Essen und Castrop-Rauxel">',
           '<defs><pattern id="raster" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#c9dcef" stroke-width="1"/></pattern></defs>',
           '<rect width="1000" height="830" fill="url(#raster)"/>',
           f'<path d="{gebiet}" fill="#d6ecd9" stroke="#9fd0ac" stroke-width="2" stroke-dasharray="6 6" opacity=".95"/>',
           f'<path d="{rhein}" fill="none" stroke="#7fb6e6" stroke-width="10" stroke-linecap="round"/>',
           f'<path d="{ruhr}" fill="none" stroke="#7fb6e6" stroke-width="6" stroke-linecap="round"/>',
           f'<path d="{emscher}" fill="none" stroke="#a9cdee" stroke-width="3.5" stroke-linecap="round" stroke-dasharray="1 0"/>',
           f'<text x="{proj(51.30, 6.765)[0]+8:.0f}" y="{proj(51.30, 6.765)[1]:.0f}" font-size="13" font-style="italic" fill="#4d87bd" font-family="Inter">Rhein</text>',
           f'<text x="{proj(51.393, 7.10)[0]:.0f}" y="{proj(51.393, 7.10)[1]+22:.0f}" font-size="13" font-style="italic" fill="#4d87bd" font-family="Inter">Ruhr</text>']
    for name, la, lo, gross, dx, dy in ORTE:
        x, y = proj(la, lo)
        if name in STANDORTE:
            nr, f = STANDORTE[name]
            out.append(f'<circle class="standort-ring" cx="{x:.0f}" cy="{y:.0f}" r="22" fill="{f}" opacity=".35"/><circle cx="{x:.0f}" cy="{y:.0f}" r="17" fill="{f}" stroke="#fff" stroke-width="4"/><text x="{x:.0f}" y="{y+5:.0f}" text-anchor="middle" font-family="Bricolage Grotesque" font-weight="800" font-size="15" fill="#fff">{nr}</text>')
            out.append(f'<text class="stadt gross" x="{x+dx+10:.0f}" y="{y+dy:.0f}">{name}</text>')
        else:
            out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5.5" fill="#15191c"/><text class="stadt" x="{x+dx:.0f}" y="{y+dy:.0f}">{name}</text>')
    out.append('</svg>')
    return ''.join(out)
