"""Baut alle Seiten der TKL-Website nach site/. Aufruf: python3 tools/build.py
Eine Seite = eine statische HTML-Datei (saubere URLs über Ordner/index.html)."""
import os, json, html
from PIL import Image
from teile import ic, logo_mark, marke, hecke, karte

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
BASIS_URL = 'https://tkl.greenfield-digital.de'
VORSCHAU = True  # solange die Seite auf der Vorschau-Domain liegt: noindex
V = '20261005f'  # Cache-Version für CSS/JS

TEL, TEL_LINK = '02065 90 36-0', 'tel:+492065903600'
MAIL = 'info@tkl.gmbh'

LEISTUNGEN = [
 # slug, titel, kurz, icon, farbe, bild, illu?
 ('gruenpflege', 'Grünpflege', 'Rasen, Hecken, Gehölze und Wege – regelmäßig, nach festem Plan und immer mit derselben Kolonne.', 'blatt', 'gruen', 'maeher-block', False),
 ('winterdienst', 'Winterdienst', 'Räumen und Streuen, bevor Ihre Mieter und Mitarbeiter aus dem Haus gehen – zuverlässig den ganzen Winter.', 'schnee', 'blau', 'illu-winterdienst', True),
 ('spielplaetze', 'Spielplätze', 'Regelmäßige Kontrolle, Pflege und Reparatur – damit Ihre Spielplätze sicher bleiben.', 'spiel', 'rot', 'illu-spielplaetze', True),
 ('baumpflege', 'Baumpflege', 'Gesunde, verkehrssichere Bäume auf Ihren Grünflächen – als Teil der laufenden Pflege.', 'baum', 'gruen', 'illu-baumpflege', True),
 ('aussenanlagen', 'Neubau & Sanierung', 'Neue Außenanlagen nach Sanierung oder Neubau: Rasen, Pflanzungen, Wege und Pflaster aus einer Hand.', 'pflaster', 'sand', 'illu-neubau', True),
]

def esc(s): return html.escape(s, quote=True)

_groessen = {}
def groesse(datei):
    if datei not in _groessen:
        p = os.path.join(SITE, 'assets', 'img', datei)
        _groessen[datei] = Image.open(p).size
    return _groessen[datei]

_GES = json.load(open(os.path.join(ROOT, 'tools', 'gesichter.json'))) if os.path.exists(os.path.join(ROOT, 'tools', 'gesichter.json')) else {}
def fokus(name):
    """object-position so wählen, dass alle Gesichter/Köpfe bei jedem Seitenverhältnis sichtbar bleiben:
    p = Abstand_vorn / (Abstand_vorn + Abstand_hinten) – dann liegt der Kopfbereich nie außerhalb des Ausschnitts."""
    boxen = _GES.get(f'{name}-m.webp') or []
    if not boxen: return ''
    m = .04
    l = max(0, min(b[0] for b in boxen) - m); r = min(1, max(b[0] + b[2] for b in boxen) + m)
    t = max(0, min(b[1] for b in boxen) - m * 1.5); u = min(1, max(b[1] + b[3] for b in boxen) + m)
    px = l / (l + 1 - r) if (l + 1 - r) > 0 else .5
    py = t / (t + 1 - u) if (t + 1 - u) > 0 else .5
    return f'{px * 100:.0f}% {py * 100:.0f}%'

def bild(name, alt, sizes='(max-width: 980px) 100vw, 50vw', eager=False, cls='', pos=''):
    pos = pos or fokus(name)
    """Responsive Bild. name ohne Endung; nutzt -s/-m(/-l).webp."""
    vorhanden = [s for s in ('s', 'm', 'l') if os.path.exists(os.path.join(SITE, 'assets', 'img', f'{name}-{s}.webp'))]
    w, h = groesse(f'{name}-{vorhanden[-1]}.webp')
    srcset = ', '.join(f'/assets/img/{name}-{s}.webp {groesse(f"{name}-{s}.webp")[0]}w' for s in vorhanden)
    src = f'/assets/img/{name}-{"m" if "m" in vorhanden else vorhanden[0]}.webp'
    lade = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    st = f' style="object-position:{pos}"' if pos else ''
    return f'<img src="{src}" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" alt="{esc(alt)}" {lade}{" class=" + chr(34) + cls + chr(34) if cls else ""}{st}>'

def sticker(name, alt, cls='sticker', eager=False):
    w, h = groesse(f'sticker-{name}.webp')
    return f'<img class="{cls}" src="/assets/img/sticker-{name}.webp" width="{w}" height="{h}" alt="{esc(alt)}" {"" if eager else "loading=" + chr(34) + "lazy" + chr(34)}>'

# ---------- Kopf / Fuß ----------
def kopf(aktiv):
    drop = ''.join(f'<a href="/leistungen/{s}/"><span class="ic {f}">{ic(i)}</span><span><b>{t}</b><span>{k.split(" – ")[0].split(".")[0]}</span></span></a>' for s, t, k, i, f, *_ in LEISTUNGEN)
    def a(href, txt, key): return f'<a href="{href}"{" aria-current=" + chr(34) + "page" + chr(34) if aktiv == key else ""}>{txt}</a>'
    unter = ''.join(f'<a href="/leistungen/{s}/">{t}</a>' for s, t, *_ in LEISTUNGEN)
    return f'''<a class="skip" href="#inhalt">Zum Inhalt springen</a>
<header class="kopf"><div class="wrap kopf-innen">
{marke()}
<nav class="nav" aria-label="Hauptnavigation">
<div class="nav-drop{' aktiv' if aktiv == 'leistungen' else ''}"><button type="button" aria-expanded="false" aria-haspopup="true">Leistungen <svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2"><path d="m2 4 4 4 4-4"/></svg></button>
<div class="drop">{drop}<a class="alle" href="/leistungen/">Alle Leistungen im Überblick <span>{ic('pfeil')}</span></a></div></div>
{a('/ueber-uns/', 'Über uns', 'ueber')}{a('/karriere/', 'Karriere', 'karriere')}{a('/kontakt/', 'Kontakt', 'kontakt')}
</nav>
<div class="kopf-aktion"><a class="tel" href="{TEL_LINK}">{ic('tel')}<span>{TEL}</span></a><a class="btn klein" href="/kontakt/#anfrage">Anfrage stellen</a></div>
<button class="burger" type="button" aria-label="Menü öffnen" aria-expanded="false" aria-controls="mobil-nav"><span></span><span></span><span></span></button>
</div></header>
<nav class="mobil-nav" id="mobil-nav" aria-label="Mobile Navigation">
<a class="haupt" href="/leistungen/">Leistungen {ic('pfeil')}</a><div class="unter">{unter}</div>
<a class="haupt" href="/ueber-uns/">Über uns</a><a class="haupt" href="/karriere/">Karriere</a><a class="haupt" href="/kontakt/">Kontakt</a>
<div class="fuss-aktionen"><a class="btn" href="/kontakt/#anfrage">Anfrage stellen {ic('pfeil', 'pfeil')}</a><a class="btn rand" href="{TEL_LINK}">{ic('tel')} {TEL}</a></div>
</nav>'''

def fuss(aktiv=''):
    leist = ''.join(f'<li><a href="/leistungen/{s}/">{t}</a></li>' for s, t, *_ in LEISTUNGEN)
    return f'''<footer class="fuss on-dark"><div class="wrap">
<div class="fuss-grid">
<div>{marke(hell=True)}<p class="claim">Grünpflege, Winterdienst und Spielplatzpflege für Wohnungsunternehmen, Genossenschaften und Firmen im Ruhrgebiet.</p>
<p><a href="{TEL_LINK}"><b style="color:#fff">{TEL}</b></a><br><a href="mailto:{MAIL}">{MAIL}</a></p></div>
<div><h4>Leistungen</h4><ul>{leist}</ul></div>
<div><h4>Unternehmen</h4><ul><li><a href="/ueber-uns/">Über uns</a></li><li><a href="/karriere/">Karriere &amp; Jobs</a></li><li><a href="/kontakt/">Kontakt &amp; Anfrage</a></li><li><a href="/kontakt/#standorte">Standorte</a></li></ul></div>
<div><h4>Standorte</h4>
<address><b>Zentrale Duisburg</b>Hochstraße 184, 47228 Duisburg</address>
<address><b>Ruhrgebiet-West</b>Bunsenstraße 30, 45145 Essen</address>
<address><b>Ruhrgebiet-Ost</b>Oststraße 25, 44575 Castrop-Rauxel</address></div>
</div>
<div class="fuss-unten"><span>© <span data-jahr>2026</span> TKL GmbH · Duisburg</span><nav aria-label="Rechtliches"><a href="/impressum/">Impressum</a><a href="/datenschutz/">Datenschutz</a><a href="/verwaltung/" rel="nofollow">Kunden-Login</a></nav></div>
</div></footer>
<div class="mobil-cta" aria-label="Schnellkontakt"><a href="{TEL_LINK}">{ic('tel')} Anrufen</a><a class="primaer" href="{'#bewerben' if aktiv == 'karriere' else '/kontakt/#anfrage'}">{'Jetzt bewerben' if aktiv == 'karriere' else 'Anfrage stellen'}</a></div>'''

def seite(pfad, titel, beschreibung, inhalt, aktiv='', funnel=False, extra_head='', body_attr=''):
    url = BASIS_URL + pfad
    robots = '<meta name="robots" content="noindex, nofollow">' if VORSCHAU else '<meta name="robots" content="index, follow">'
    ld = {
      "@context": "https://schema.org", "@type": "LocalBusiness", "name": "TKL GmbH", "url": BASIS_URL + '/',
      "telephone": "+49 2065 90360", "email": MAIL, "image": BASIS_URL + '/assets/img/og-tkl.jpg',
      "address": {"@type": "PostalAddress", "streetAddress": "Hochstraße 184", "postalCode": "47228", "addressLocality": "Duisburg", "addressCountry": "DE"},
      "areaServed": ["Duisburg", "Essen", "Oberhausen", "Mülheim an der Ruhr", "Bottrop", "Gelsenkirchen", "Bochum", "Herne", "Castrop-Rauxel", "Dortmund", "Ruhrgebiet"],
      "department": [
        {"@type": "LocalBusiness", "name": "TKL GmbH – Niederlassung Ruhrgebiet-West", "address": {"@type": "PostalAddress", "streetAddress": "Bunsenstraße 30", "postalCode": "45145", "addressLocality": "Essen", "addressCountry": "DE"}},
        {"@type": "LocalBusiness", "name": "TKL GmbH – Niederlassung Ruhrgebiet-Ost", "address": {"@type": "PostalAddress", "streetAddress": "Oststraße 25", "postalCode": "44575", "addressLocality": "Castrop-Rauxel", "addressCountry": "DE"}}]}
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(titel)}</title>
<meta name="description" content="{esc(beschreibung)}">
{robots}
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#f7f4ee">
<meta property="og:type" content="website"><meta property="og:locale" content="de_DE"><meta property="og:site_name" content="TKL GmbH">
<meta property="og:title" content="{esc(titel)}"><meta property="og:description" content="{esc(beschreibung)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASIS_URL}/assets/img/og-tkl.jpg">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/bricolage-grotesque.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/tkl.css?v={V}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{extra_head}
</head>
<body{body_attr}>
{kopf(aktiv)}
<main id="inhalt">
{inhalt}
</main>
{fuss(aktiv)}
<script src="/assets/js/main.js?v={V}" defer></script>
{f'<script src="/assets/js/funnel.js?v={V}" defer></script>' if funnel else ''}
</body>
</html>'''

def schreibe(pfad, inhalt):
    ziel = os.path.join(SITE, pfad.strip('/'), 'index.html') if pfad != '/' else os.path.join(SITE, 'index.html')
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    open(ziel, 'w', encoding='utf-8').write(inhalt)
    print('✓', pfad)

def brot(*teile):
    li = '<li><a href="/">Start</a></li>' + ''.join(f'<li><a href="{h}">{t}</a></li>' if h else f'<li aria-current="page">{t}</li>' for t, h in teile)
    return f'<ol class="brot">{li}</ol>'

def cta_hecke(titel='Legen Sie’s in unsere Hände. <span class="pinsel gruen">Wir haben viele davon.</span>', text='Sagen Sie uns kurz, worum es geht – wir melden uns, schauen uns Ihre Flächen vor Ort an und machen Ihnen ein klares Angebot.', knopf='Jetzt Anfrage stellen', link='/kontakt/#anfrage'):
    return f'''<section class="cta-hecke" aria-labelledby="cta-titel">
<span class="wolke" style="top:18%;width:160px;height:38px;animation-delay:-12s"></span><span class="wolke" style="top:34%;width:110px;height:28px;animation-delay:-38s;animation-duration:80s"></span>
<div class="wrap rv"><span class="eyebrow">Jetzt anfragen</span><h2 id="cta-titel">{titel}</h2><p class="lead">{text}</p>
<div class="btn-reihe"><a class="btn" href="{link}">{knopf} {ic('pfeil', 'pfeil')}</a><a class="btn rand" href="{TEL_LINK}">{ic('tel')} {TEL}</a></div></div>
{hecke()}
</section>'''

def faq(fragen, titel='Häufige Fragen', eyebrow='FAQ'):
    items = ''.join(f'<details><summary>{esc(f)}</summary><div class="antwort"><p>{a}</p></div></details>' for f, a in fragen)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": f, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a.replace('<br>', ' '))}} for f, a in fragen]}
    return f'''<section class="sec" aria-labelledby="faq-titel"><div class="wrap schmal">
<div class="sec-kopf mitte rv"><span class="eyebrow">{eyebrow}</span><h2 id="faq-titel">{titel}</h2></div>
<div class="faq rv">{items}</div></div>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></section>'''

import seiten  # noqa: E402  (Seiteninhalte)

if __name__ == '__main__':
    seiten.alle(globals())
