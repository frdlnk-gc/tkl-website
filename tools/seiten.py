"""Inhalte aller Seiten. Wird von build.py aufgerufen (bekommt dessen Helfer über alle(g))."""

def alle(g):
    globals().update(g)
    startseite(); leistungen_uebersicht()
    for l in LEISTUNGEN: leistung(l)
    ueber_uns(); karriere(); kontakt(); impressum(); datenschutz(); fehlerseite(); intern(); weiterleitungen()


# ---------- Video-Karten ----------
STIMMEN = {
 'ralf-vorstellung': ('„Wir sind 50 Leute in 10 bis 12 Kolonnen.“', 'Ralf Jung · Geschäftsführer', '1:25'),
 'ralf-angebot': ('„Sprecht uns an – wir machen euch gern ein Angebot.“', 'Ralf Jung · Geschäftsführer', '0:12'),
 'stimme-duo': ('„Wir sind ein eingespieltes Team.“', 'Vorarbeiter-Duo · seit 2007 zusammen', '0:41'),
 'stimme-20-jahre': ('„Die Chefs lassen uns nicht im Stich.“', 'Grischa · bald 20 Jahre bei TKL', '0:33'),
 'stimme-grischa': ('„Wir haben eine tolle Truppe.“', 'Grischa · Kolonne Grünpflege', '1:00'),
 'stimme-kai': ('„Die Pause ist immer das Beste.“', 'Kai · über 30 Jahre bei TKL', '0:43'),
 'stimme-nail': ('„Ich mag alles an meinem Job.“', 'Nail · Grünpflege, seit 3,5 Jahren', '1:02'),
 'gruenpflege-20000': ('„20.000 Quadratmeter an einem Tag.“', 'Kolonne in Duisburg-Walsum', '0:26'),
 'grischa-km': ('„15, 16 Kilometer am Tag.“', 'Grischa · zu Fuß mit dem Freischneider', '0:20'),
}
def stimme(name, extra=''):
    z, u, d = STIMMEN[name]
    return (f'<button type="button" class="stimme{extra}" data-video="{name}" data-titel="{esc(z)}" data-untertitel="{esc(u)}" aria-label="Video ansehen: {esc(u)}">'
            f'<img src="/assets/video/{name}-poster.webp" alt="" loading="lazy" width="720" height="1280">'
            f'<span class="stimme-text"><span class="stimme-meta"><span class="stimme-play"><svg viewBox="0 0 24 24"><path d="M7 4.5v15l13-7.5z"/></svg></span><span class="stimme-dauer">{d}</span></span>'
            f'<b>{z}</b><span class="stimme-wer">{u}</span></span></button>')


# =====================================================================
# STARTSEITE
# =====================================================================
def startseite():
    karten = []
    for n, (s, t, k, i, f, b, illu) in enumerate(LEISTUNGEN):
        farbe = {'gruen': 'var(--green)', 'blau': 'var(--blue)', 'rot': 'var(--red)', 'sand': '#c9922a'}[f]
        karten.append(f'''<a class="lk{' gross' if n < 2 else ''} rv d{n % 3 + 1}" href="/leistungen/{s}/" style="--c:{farbe}">
<span class="tag">{['Kernleistung', 'November bis März', 'Sicherheit zuerst', 'Teil der Grünpflege', 'Für Bestandskunden'][n]}</span>
<div class="lk-bild{' illu' if illu else ''}">{bild(b, '' if illu else 'Mitarbeiter der TKL mäht mit dem Aufsitzmäher eine Rasenfläche vor einem Wohnblock', '(max-width: 640px) 100vw, (max-width: 980px) 50vw, 40vw')}</div>
<div class="lk-text"><h3>{t}</h3><p>{k}</p><span class="mehr">Mehr erfahren <i>{ic('pfeil')}</i></span></div></a>''')
    inhalt = f'''
<section class="hero" aria-labelledby="hero-titel">
<div class="wrap hero-grid">
<div>
<span class="eyebrow">Duisburg · Castrop-Rauxel · Ruhrgebiet</span>
<h1 id="hero-titel">Gepflegtes Grün. Sichere Wege. <span class="pinsel">Das ganze Jahr.</span></h1>
<p class="lead">TKL pflegt die Außenanlagen von Wohnungsgenossenschaften, Immobilienunternehmen und Firmen im Ruhrgebiet – mit festen Kolonnen, eigenem Maschinenpark und kurzen Wegen von zwei Standorten aus.</p>
<div class="btn-reihe"><a class="btn" href="/kontakt/#anfrage">Anfrage stellen {ic('pfeil', 'pfeil')}</a><a class="btn rand" href="/leistungen/">Leistungen ansehen</a></div>
<ul class="hero-chips">
<li><span class="ic gruen" style="border-radius:50%;width:30px;height:30px;display:grid;place-items:center">{ic('team')}</span>Feste Kolonne je Objekt</li>
<li><span class="ic rot" style="border-radius:50%;width:30px;height:30px;display:grid;place-items:center">{ic('traktor')}</span>Profi-Maschinenpark</li>
<li><span class="ic blau" style="border-radius:50%;width:30px;height:30px;display:grid;place-items:center">{ic('schnee')}</span>Sommer wie Winter</li>
</ul>
</div>
<div class="hero-bild">
<div class="hero-foto">{bild('siedlung-hecke', 'TKL-Mitarbeiter mäht mit einem roten Aufsitzmäher die Rasenfläche einer Wohnsiedlung, daneben eine gepflegte Hecke', '(max-width: 980px) 100vw, 52vw', eager=True)}</div>
<div class="sticker-gruppe" data-parallax="-0.06">{sticker('duo', 'Zwei TKL-Kollegen in roter Arbeitskleidung, Arm in Arm', 'hero-sticker', eager=True)}<span class="blase" aria-hidden="true">Wir kümmern uns!</span></div>
<div class="live-clip" data-parallax="0.05"><span class="badge"><span class="lang">Unterwegs mit der Kolonne</span><span class="kurz">Unterwegs</span></span><video autoplay muted loop playsinline preload="metadata" poster="/assets/video/kolonne-live-poster.webp" aria-label="Kurzer Clip: TKL-Kolonne beim Mähen und Freischneiden"><source src="/assets/video/kolonne-live.mp4" type="video/mp4"></video></div>
</div>
</div>
</section>

<div class="laufband" aria-hidden="true"><div class="band-spur">{"".join(f"<span>{t}<i></i></span>" for t in (["Rasen mähen", "Hecken schneiden", "Laub blasen", "Wege kehren", "Spielplätze prüfen", "Bäume pflegen", "Schnee räumen", "Streuen", "Rasen anlegen", "Pflaster legen"] * 2))}</div></div>

<section class="sec eng" aria-label="TKL in Zahlen" style="padding-top:clamp(40px,5vw,64px)">
<div class="wrap"><div class="zahlen rv">
<div class="zahl"><b><span data-zahl="50">50</span></b><span>Mitarbeiter – im Winterdienst ist die ganze Mannschaft draußen</span></div>
<div class="zahl"><b>10–12</b><span>feste Kolonnen, jede mit ihren eigenen Objekten</span></div>
<div class="zahl"><b><span data-zahl="25">25</span></b><span>eigene Fahrzeuge plus moderner Maschinenpark</span></div>
<div class="zahl"><b><span data-zahl="30">30</span><em>+</em></b><span>Jahre – so lange ist Kai schon bei TKL</span></div>
</div></div>
</section>

<section class="sec" aria-labelledby="leist-titel" style="padding-top:clamp(40px,5vw,70px)">
<div class="wrap">
<div class="sec-kopf split rv"><div><span class="eyebrow">Leistungen</span><h2 id="leist-titel">Alles rund um Ihre <span class="pinsel gruen">Außenanlagen</span>.</h2></div>
<p class="lead">Von der wöchentlichen Rasenpflege bis zum Streudienst am frühen Morgen: Sie haben einen Partner für das ganze Jahr – und einen Ansprechpartner, der Ihre Objekte kennt.</p></div>
<div class="leist-grid">{''.join(karten)}
<a class="lk band rv" href="/kontakt/#anfrage"><div class="lk-text"><span class="ic rot">{ic('liste')}</span><h3>Mehrere Leistungen,<br>ein Vertrag</h3><p>Grünpflege im Sommer, Winterdienst im Winter, Spielplatzkontrolle dazu – alles aus einer Hand und abgestimmt auf Ihr Objekt.</p><span class="mehr">Angebot anfragen <i style="background:var(--red);color:#fff">{ic('pfeil')}</i></span></div></a>
</div>
</div>
</section>


<section class="sec" aria-labelledby="kal-titel" style="padding-top:0">
<div class="wrap">
<div class="sec-kopf split rv"><div><span class="eyebrow">Das ganze Jahr im Einsatz</span><h2 id="kal-titel">Was gerade bei uns <span class="pinsel gruen">passiert</span>.</h2></div>
<p class="lead">Grünpflege hat Saison, Winterdienst auch. Unser Jahr im Überblick – der aktuelle Monat ist markiert.</p></div>
<div class="kalender rv" data-kalender='["Im Januar sind unsere Teams im Winterdienst unterwegs und schneiden Gehölze – das geht nur in der kalten Jahreszeit.", "Im Februar räumen und streuen wir bei Glätte und nutzen die letzten Wochen für den großen Gehölzschnitt.", "Im März startet die Saison: erste Rasenpflege, Pflanzungen und die Vorbereitung der Flächen fürs Frühjahr.", "Im April wächst alles – unsere Kolonnen sind im festen Rhythmus mit Mähern und Freischneidern draußen.", "Im Mai ist Hochsaison für die Rasenpflege. Jede Anlage bekommt ihre Kolonne nach Plan.", "Im Juni mähen wir in kurzen Abständen und bringen Hecken mit dem Formschnitt in Form.", "Im Juli ist Sommer in den Siedlungen: Rasenpflege, Bewässerung neuer Flächen und Formschnitt.", "Im August geht die Rasenpflege weiter – und wir planen schon die Winterdienst-Touren.", "Im September beginnt die Pflanzzeit. Ein guter Moment, um Neuanlagen und den Winterdienst zu beauftragen.", "Im Oktober sind unsere Kolonnen vor allem mit Laub und Gehölzschnitt beschäftigt – und machen die Fahrzeuge winterfest.", "Im November ist Laubzeit und der Winterdienst steht bereit, sobald der erste Frost kommt.", "Im Dezember räumen und streuen wir früh am Morgen – damit Ihre Wege sicher sind."]'>
<div class="kal-raster" role="table" aria-label="Leistungen nach Monaten">
<span></span><span class="kal-monat" data-m="0">Jan</span><span class="kal-monat" data-m="1">Feb</span><span class="kal-monat" data-m="2">Mär</span><span class="kal-monat" data-m="3">Apr</span><span class="kal-monat" data-m="4">Mai</span><span class="kal-monat" data-m="5">Jun</span><span class="kal-monat" data-m="6">Jul</span><span class="kal-monat" data-m="7">Aug</span><span class="kal-monat" data-m="8">Sep</span><span class="kal-monat" data-m="9">Okt</span><span class="kal-monat" data-m="10">Nov</span><span class="kal-monat" data-m="11">Dez</span>
<span class="kal-name">{ic('blatt')} Rasenpflege</span><span class="kal-zelle" data-m="0" style="--c:var(--green)"></span><span class="kal-zelle" data-m="1" style="--c:var(--green)"></span><span class="kal-zelle an halb" data-m="2" style="--c:var(--green)"></span><span class="kal-zelle an" data-m="3" style="--c:var(--green)"></span><span class="kal-zelle an" data-m="4" style="--c:var(--green)"></span><span class="kal-zelle an" data-m="5" style="--c:var(--green)"></span><span class="kal-zelle an" data-m="6" style="--c:var(--green)"></span><span class="kal-zelle an" data-m="7" style="--c:var(--green)"></span><span class="kal-zelle an" data-m="8" style="--c:var(--green)"></span><span class="kal-zelle an" data-m="9" style="--c:var(--green)"></span><span class="kal-zelle an halb" data-m="10" style="--c:var(--green)"></span><span class="kal-zelle" data-m="11" style="--c:var(--green)"></span>
<span class="kal-name">{ic('baum')} Hecken- & Gehölzschnitt</span><span class="kal-zelle an" data-m="0" style="--c:#2f8a4a"></span><span class="kal-zelle an" data-m="1" style="--c:#2f8a4a"></span><span class="kal-zelle" data-m="2" style="--c:#2f8a4a"></span><span class="kal-zelle" data-m="3" style="--c:#2f8a4a"></span><span class="kal-zelle" data-m="4" style="--c:#2f8a4a"></span><span class="kal-zelle an halb" data-m="5" style="--c:#2f8a4a"></span><span class="kal-zelle an halb" data-m="6" style="--c:#2f8a4a"></span><span class="kal-zelle an halb" data-m="7" style="--c:#2f8a4a"></span><span class="kal-zelle" data-m="8" style="--c:#2f8a4a"></span><span class="kal-zelle an" data-m="9" style="--c:#2f8a4a"></span><span class="kal-zelle an" data-m="10" style="--c:#2f8a4a"></span><span class="kal-zelle an" data-m="11" style="--c:#2f8a4a"></span>
<span class="kal-name">{ic('besen')} Laub entfernen</span><span class="kal-zelle" data-m="0" style="--c:#c9922a"></span><span class="kal-zelle" data-m="1" style="--c:#c9922a"></span><span class="kal-zelle" data-m="2" style="--c:#c9922a"></span><span class="kal-zelle" data-m="3" style="--c:#c9922a"></span><span class="kal-zelle" data-m="4" style="--c:#c9922a"></span><span class="kal-zelle" data-m="5" style="--c:#c9922a"></span><span class="kal-zelle" data-m="6" style="--c:#c9922a"></span><span class="kal-zelle" data-m="7" style="--c:#c9922a"></span><span class="kal-zelle an halb" data-m="8" style="--c:#c9922a"></span><span class="kal-zelle an" data-m="9" style="--c:#c9922a"></span><span class="kal-zelle an" data-m="10" style="--c:#c9922a"></span><span class="kal-zelle an halb" data-m="11" style="--c:#c9922a"></span>
<span class="kal-name">{ic('schnee')} Winterdienst</span><span class="kal-zelle an" data-m="0" style="--c:var(--blue)"></span><span class="kal-zelle an" data-m="1" style="--c:var(--blue)"></span><span class="kal-zelle an halb" data-m="2" style="--c:var(--blue)"></span><span class="kal-zelle" data-m="3" style="--c:var(--blue)"></span><span class="kal-zelle" data-m="4" style="--c:var(--blue)"></span><span class="kal-zelle" data-m="5" style="--c:var(--blue)"></span><span class="kal-zelle" data-m="6" style="--c:var(--blue)"></span><span class="kal-zelle" data-m="7" style="--c:var(--blue)"></span><span class="kal-zelle" data-m="8" style="--c:var(--blue)"></span><span class="kal-zelle" data-m="9" style="--c:var(--blue)"></span><span class="kal-zelle an" data-m="10" style="--c:var(--blue)"></span><span class="kal-zelle an" data-m="11" style="--c:var(--blue)"></span>
<span class="kal-name">{ic('spiel')} Spielplatzkontrolle</span><span class="kal-zelle an" data-m="0" style="--c:var(--red)"></span><span class="kal-zelle an" data-m="1" style="--c:var(--red)"></span><span class="kal-zelle an" data-m="2" style="--c:var(--red)"></span><span class="kal-zelle an" data-m="3" style="--c:var(--red)"></span><span class="kal-zelle an" data-m="4" style="--c:var(--red)"></span><span class="kal-zelle an" data-m="5" style="--c:var(--red)"></span><span class="kal-zelle an" data-m="6" style="--c:var(--red)"></span><span class="kal-zelle an" data-m="7" style="--c:var(--red)"></span><span class="kal-zelle an" data-m="8" style="--c:var(--red)"></span><span class="kal-zelle an" data-m="9" style="--c:var(--red)"></span><span class="kal-zelle an" data-m="10" style="--c:var(--red)"></span><span class="kal-zelle an" data-m="11" style="--c:var(--red)"></span>
<span class="kal-name">{ic('pflaster')} Pflanzen & Neuanlagen</span><span class="kal-zelle" data-m="0" style="--c:#8a6a3a"></span><span class="kal-zelle" data-m="1" style="--c:#8a6a3a"></span><span class="kal-zelle an" data-m="2" style="--c:#8a6a3a"></span><span class="kal-zelle an" data-m="3" style="--c:#8a6a3a"></span><span class="kal-zelle an halb" data-m="4" style="--c:#8a6a3a"></span><span class="kal-zelle" data-m="5" style="--c:#8a6a3a"></span><span class="kal-zelle" data-m="6" style="--c:#8a6a3a"></span><span class="kal-zelle" data-m="7" style="--c:#8a6a3a"></span><span class="kal-zelle an" data-m="8" style="--c:#8a6a3a"></span><span class="kal-zelle an" data-m="9" style="--c:#8a6a3a"></span><span class="kal-zelle an halb" data-m="10" style="--c:#8a6a3a"></span><span class="kal-zelle" data-m="11" style="--c:#8a6a3a"></span>
</div>
<div class="kal-legende"><span>Hauptsaison</span><span class="halb">je nach Wetter</span></div>
<div class="kal-jetzt"><span class="punkt" data-jetzt-monat>Okt</span><p><b>Jetzt bei TKL:</b> <span data-jetzt-text>Im Oktober sind unsere Kolonnen vor allem mit Laub und Gehölzschnitt beschäftigt – und machen die Fahrzeuge winterfest.</span></p></div>
</div>
</div>
</section>

<section class="sec bg-weiss" aria-labelledby="usp-titel">
<div class="wrap grid-2">
<div class="bild-stapel rv">
<div class="haupt">{bild('kolonne-aktion', 'Eine TKL-Kolonne bei der Arbeit: ein Mitarbeiter mit Freischneider am Baum, im Hintergrund ein Kollege auf dem Aufsitzmäher', '(max-width: 980px) 100vw, 50vw')}</div>
<div class="zitatkarte unten"><b>Gleiche Kolonne.</b>Seit Jahren dieselben Leute bei denselben Kunden – sie kennen jede Ecke und jeden Ablauf.</div>
{sticker('blasen', 'TKL-Mitarbeiter mit Laubbläser')}
</div>
<div>
<span class="eyebrow">Warum TKL</span>
<h2 id="usp-titel">Ihre Flächen in <span class="pinsel">festen Händen</span>.</h2>
<p class="lead">Bei TKL fährt nicht jede Woche ein anderes Team raus. Jede Anlage hat ihre Kolonne – das spart Absprachen, Zeit und Nerven.</p>
<div class="usp-liste">
<div class="usp rv"><span class="ic gruen">{ic('team')}</span><div><h3>Immer dieselbe Kolonne</h3><p>Ihre Mitarbeiter kennen das Objekt, die Mieter und die Besonderheiten. Eingespielte Abläufe – und schnell wieder vom Hof.</p></div></div>
<div class="usp rv d1"><span class="ic rot">{ic('traktor')}</span><div><h3>Profi-Maschinen statt Kleingerät</h3><p>Aufsitzmäher, Kehrmaschinen, Freischneider und Laubbläser in Profi-Qualität: große Flächen sind schneller und sauberer fertig.</p></div></div>
<div class="usp rv d2"><span class="ic blau">{ic('pin')}</span><div><h3>Kurze Wege im Ruhrgebiet</h3><p>Von Duisburg und Castrop-Rauxel aus sind wir schnell vor Ort – auch, wenn im Winter nachts Glätte kommt.</p></div></div>
<div class="usp rv d3"><span class="ic sand">{ic('schild')}</span><div><h3>Erfahrene Leute, die bleiben</h3><p>Viele Kollegen sind seit über 20 Jahren dabei. Diese Erfahrung merken Sie an der Qualität – und an der Ruhe auf der Baustelle.</p></div></div>
</div>
</div>
</div>
</section>

<section class="sec" id="fuer-wen" aria-labelledby="ziel-titel">
<div class="wrap">
<div class="sec-kopf rv"><span class="eyebrow">Für wen wir arbeiten</span><h2 id="ziel-titel">Partner für Wohnungswirtschaft und Gewerbe.</h2>
<p class="lead">Wir pflegen keine Privatgärten, sondern große Flächen – dort, wo viele Menschen wohnen, arbeiten und unterwegs sind.</p></div>
<div class="ziel-tabs rv" role="tablist" aria-label="Zielgruppen">
<button class="ziel-tab" role="tab" id="tab-1" aria-selected="true" aria-controls="ziel-1">{ic('haus')} Genossenschaften &amp; Wohnungsunternehmen</button>
<button class="ziel-tab" role="tab" id="tab-2" aria-selected="false" aria-controls="ziel-2" tabindex="-1">{ic('stadt')} Immobilienverwaltungen</button>
<button class="ziel-tab" role="tab" id="tab-3" aria-selected="false" aria-controls="ziel-3" tabindex="-1">{ic('fabrik')} Firmen &amp; Gewerbe</button>
</div>
<div class="ziel-panel rv" role="tabpanel" id="ziel-1" aria-labelledby="tab-1">
<div class="text"><h3>Ganze Siedlungen an einem Tag gepflegt</h3><p>Mehrere Wohnblöcke, große Rasenflächen, Spielplätze und Wege: Wir rücken mit mehreren Kolonnen gleichzeitig an und sind meist am selben Tag durch. Ihre Mieter erleben gepflegte Anlagen statt wochenlanger Baustelle.</p>
<ul class="haken"><li>Grünpflege, Winterdienst und Spielplatzkontrolle aus einer Hand</li><li>Feste Pflegeintervalle über die ganze Saison</li><li>Ein Ansprechpartner für alle Ihre Objekte</li></ul>
<a class="textlink" href="/leistungen/gruenpflege/">Grünpflege für Wohnanlagen {ic('pfeil')}</a></div>
<div class="bild">{bild('maeher-weg', 'Aufsitzmäher von TKL auf einer Rasenfläche zwischen Wohnblöcken', '(max-width: 980px) 100vw, 50vw')}</div></div>
<div class="ziel-panel" role="tabpanel" id="ziel-2" aria-labelledby="tab-2" hidden>
<div class="text"><h3>Weniger Aufwand für Ihre Verwaltung</h3><p>Sie betreuen viele Objekte und brauchen einen Dienstleister, der einfach läuft. Wir arbeiten nach Leistungsverzeichnis, halten Termine ein und melden uns, wenn uns vor Ort etwas auffällt – etwa ein beschädigter Zaun oder ein kranker Baum.</p>
<ul class="haken"><li>Klare Leistungen, klare Preise</li><li>Rückmeldung, wenn vor Ort etwas nicht stimmt</li><li>Winterdienst mit Räum- und Streueinsätzen nach Wetterlage</li></ul>
<a class="textlink" href="/leistungen/winterdienst/">Winterdienst für Verwaltungen {ic('pfeil')}</a></div>
<div class="bild">{bild('hecke-weg', 'TKL-Mitarbeiter mit Freischneider an einem Gehweg vor einem Mehrfamilienhaus', '(max-width: 980px) 100vw, 50vw')}</div></div>
<div class="ziel-panel" role="tabpanel" id="ziel-3" aria-labelledby="tab-3" hidden>
<div class="text"><h3>Ein gepflegter erster Eindruck</h3><p>Das Firmengelände ist Ihre Visitenkarte – für Kunden, Bewerber und Mitarbeiter. Wir halten Grünflächen, Hecken und Wege rund um Bürogebäude, Hallen und Parkplätze in Schuss und sorgen im Winter für sichere Zufahrten.</p>
<ul class="haken"><li>Pflege auch außerhalb Ihrer Betriebszeiten möglich</li><li>Sichere Zufahrten, Parkplätze und Eingänge im Winter</li><li>Alles sauber hinterlassen – kein Schnittgut auf den Wegen</li></ul>
<a class="textlink" href="/kontakt/#anfrage">Angebot für Ihr Gelände {ic('pfeil')}</a></div>
<div class="bild">{bild('blasgeraet', 'TKL-Mitarbeiter reinigt mit dem Laubbläser einen gepflasterten Weg', '(max-width: 980px) 100vw, 50vw')}</div></div>
</div>
</section>

<section class="sec bg-weiss" aria-labelledby="gebiet-titel">
<div class="wrap gebiet">
<div>
<span class="eyebrow">Einsatzgebiet</span>
<h2 id="gebiet-titel">Zu Hause im <span class="pinsel gruen">Ruhrgebiet</span>.</h2>
<p class="lead">Von Duisburg aus betreuen wir das westliche, von Castrop-Rauxel aus das östliche Ruhrgebiet. Im Winterdienst sind wir zusätzlich bis nach Remscheid unterwegs.</p>
<div class="standorte">
<div class="standort rv"><span class="nr" style="background:var(--red)">1</span><div><b>Zentrale Duisburg · westliches Ruhrgebiet</b><span>Hochstraße 184, 47228 Duisburg</span></div></div>
<div class="standort rv d2"><span class="nr" style="background:var(--green)">2</span><div><b>Niederlassung Castrop-Rauxel · östliches Ruhrgebiet</b><span>Oststraße 25, 44575 Castrop-Rauxel</span></div></div>
</div>
<ul class="staedte" aria-label="Städte im Einsatzgebiet"><li>Duisburg</li><li>Essen</li><li>Oberhausen</li><li>Mülheim</li><li>Bottrop</li><li>Gelsenkirchen</li><li>Bochum</li><li>Herne</li><li>Castrop-Rauxel</li><li>Dortmund</li><li>Moers</li><li>Remscheid (Winterdienst)</li></ul>
</div>
<div class="karte rv">{karte()}</div>
</div>
</section>

<section class="sec bg-dunkel on-dark" aria-labelledby="masch-titel">
<div class="wrap maschinen">
<div>
<span class="eyebrow">Betriebshof &amp; Maschinenpark</span>
<h2 id="masch-titel">Gutes Werkzeug für gute Arbeit.</h2>
<p class="lead">Wer große Flächen pflegt, braucht Maschinen, die das schaffen. Darum investieren wir laufend in Profi-Technik – und pflegen sie in der eigenen Halle.</p>
<div class="geraete">
<div class="geraet">{ic('traktor')} Aufsitzmäher für große Flächen</div>
<div class="geraet">{ic('besen')} Kehrmaschinen &amp; Streutechnik</div>
<div class="geraet">{ic('blatt')} Freischneider &amp; Heckenscheren</div>
<div class="geraet">{ic('auto')} 25 Fahrzeuge für feste Kolonnen</div>
</div>
<a class="btn hell" href="/ueber-uns/">Mehr über TKL {ic('pfeil', 'pfeil')}</a>
</div>
<div class="video-paar">
<div class="foto-rund rv" style="aspect-ratio:3/4">{bild('halle-maeher', 'Maschinenhalle der TKL mit mehreren Aufsitzmähern und Geräten in Regalen', '(max-width: 980px) 50vw, 22vw')}</div>
<div class="video-rahmen rv d1"><span class="badge">Unser Betriebshof</span>
<video data-auto muted loop playsinline preload="none" poster="/assets/video/betriebshof-poster.webp" aria-label="Rundgang durch die Maschinenhalle der TKL"><source src="/assets/video/betriebshof.mp4" type="video/mp4"></video></div>
</div>
</div>
</section>

<section class="sec" aria-labelledby="ablauf-titel">
<div class="wrap">
<div class="sec-kopf mitte rv"><span class="eyebrow">So starten wir</span><h2 id="ablauf-titel">In vier Schritten zur festen Pflege.</h2></div>
<div class="ablauf">
<div class="schritt rv"><h3>Anfrage</h3><p>Sie schildern kurz Objekt und Leistungen – online in zwei Minuten oder telefonisch.</p></div>
<div class="schritt rv d1"><h3>Besichtigung</h3><p>Wir schauen uns Ihre Flächen vor Ort an und klären Intervalle, Zugänge und Wünsche.</p></div>
<div class="schritt rv d2"><h3>Angebot</h3><p>Sie bekommen ein klares Angebot mit allen Leistungen – ohne versteckte Positionen.</p></div>
<div class="schritt rv d3"><h3>Feste Kolonne</h3><p>Ihre Kolonne übernimmt – und kommt ab dann regelmäßig nach Plan.</p></div>
</div>
</div>
</section>

<section class="sec" aria-labelledby="kennen-titel">
<div class="wrap">
<div class="sec-kopf split rv"><div><span class="eyebrow">Lernen Sie uns kennen</span><h2 id="kennen-titel">Die Leute hinter Ihrer <span class="pinsel">Grünpflege</span>.</h2></div>
<p class="lead">Keine Werbesprüche: Hier erzählen unser Geschäftsführer und die Kolonnen selbst, wie sie arbeiten. Mit Ton und Untertiteln.</p></div>
<div class="stimmen vier rv">{stimme('ralf-vorstellung')}{stimme('stimme-duo')}{stimme('gruenpflege-20000')}{stimme('stimme-kai')}</div>
</div>
</section>

<section class="sec eng" aria-labelledby="karr-titel" style="padding-top:0">
<div class="wrap"><div class="karriere-band rv">
<div class="text on-dark"><span class="eyebrow">Karriere bei TKL</span><h2 id="karr-titel">Draußen arbeiten. Mit Leuten, die zusammenhalten.</h2>
<p class="lead">Wir suchen Verstärkung für unsere Kolonnen – gern auch Quereinsteiger. Bewerben geht in einer Minute, ganz ohne Lebenslauf.</p>
<ul class="vorteil-chips"><li>Feste Kolonne</li><li>Profi-Maschinen</li><li>Arbeit das ganze Jahr</li><li>Kurze Wege im Revier</li></ul>
<div class="btn-reihe"><a class="btn" href="/karriere/">Jobs ansehen {ic('pfeil', 'pfeil')}</a><a class="btn rand" href="/karriere/#bewerben">Direkt bewerben</a></div></div>
<div class="bild">{sticker('laecheln', 'Junger TKL-Mitarbeiter in schwarzem Shirt und roter Arbeitshose lächelt', '')}<span class="blase" aria-hidden="true">Komm in unser Team!</span></div>
</div></div>
</section>

{cta_hecke()}
'''
    schreibe('/', seite('/', 'TKL GmbH – Grünpflege, Winterdienst & Spielplätze im Ruhrgebiet', 'TKL aus Duisburg pflegt Außenanlagen für Wohnungsgenossenschaften, Immobilienunternehmen und Firmen im Ruhrgebiet: Grünpflege, Winterdienst, Spielplatzpflege und Baumpflege – mit festen Kolonnen.', inhalt))


# =====================================================================
# LEISTUNGEN ÜBERSICHT
# =====================================================================
def leistungen_uebersicht():
    karten = ''.join(f'''<a class="lk rv d{n % 3 + 1}" href="/leistungen/{s}/"><div class="lk-bild{' illu' if illu else ''}">{bild(b, '', '(max-width: 640px) 100vw, (max-width: 980px) 50vw, 33vw')}</div>
<div class="lk-text"><h3 style="display:flex;gap:10px;align-items:center"><span class="ic {f}" style="width:38px;height:38px;border-radius:11px;display:grid;place-items:center">{ic(i)}</span>{t}</h3><p>{k}</p><span class="mehr">Zur Leistung <i>{ic('pfeil')}</i></span></div></a>''' for n, (s, t, k, i, f, b, illu) in enumerate(LEISTUNGEN))
    inhalt = f'''
<section class="seitenkopf"><div class="wrap">
{brot(('Leistungen', None))}
<div class="sec-kopf split" style="margin:0"><div><span class="eyebrow">Unsere Leistungen</span><h1>Ein Partner für Ihre Außenanlagen – <span class="pinsel gruen">das ganze Jahr</span>.</h1></div>
<p class="lead">Grünpflege ist unser Kerngeschäft. Dazu kommen Winterdienst, Spielplatzpflege, Baumpflege und – für unsere Bestandskunden – Neubau und Sanierung von Außenanlagen. Alles aus einer Hand, alles im Ruhrgebiet.</p></div>
</div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="grid-3">{karten}
<div class="lk rv" style="background:var(--green-soft);box-shadow:none"><div class="lk-text" style="justify-content:center"><h3>Nicht dabei, was Sie suchen?</h3><p>Rufen Sie uns an – wenn es zu Ihren Außenanlagen gehört, finden wir meist eine Lösung oder sagen Ihnen ehrlich, wer besser passt.</p><a class="btn dunkel klein" href="{TEL_LINK}" style="align-self:flex-start">{ic('tel')} {TEL}</a></div></div>
</div></div></section>
<section class="sec bg-weiss"><div class="wrap grid-2">
<div><span class="eyebrow">Was wir nicht machen</span><h2>Klarer Fokus statt Bauchladen.</h2><p class="lead">Wir sind spezialisiert auf große Flächen von Wohnungswirtschaft, Gewerbe und öffentlichen Auftraggebern. Privatgärten, Pools oder Terrassen für Einfamilienhäuser übernehmen wir nicht – dafür sind wir in unserem Bereich richtig gut.</p></div>
<div class="kacheln">
<div class="kachel rv"><h3>{ic('haus')} Wohnanlagen</h3><p>Siedlungen, Wohnblöcke und Innenhöfe von Genossenschaften und Wohnungsunternehmen.</p></div>
<div class="kachel rv d1"><h3>{ic('fabrik')} Firmengelände</h3><p>Außenanlagen rund um Bürogebäude, Hallen, Werksgelände und Parkplätze.</p></div>
<div class="kachel rv d2"><h3>{ic('spiel')} Spielplätze</h3><p>Spielplätze in Wohnanlagen und auf Firmen- oder Vereinsgelände.</p></div>
<div class="kachel rv d3"><h3>{ic('stadt')} Öffentliche Flächen</h3><p>Grün- und Verkehrsflächen für Kommunen und öffentliche Einrichtungen.</p></div>
</div></div></section>
{cta_hecke()}'''
    schreibe('/leistungen/', seite('/leistungen/', 'Leistungen: Grünpflege, Winterdienst, Spielplätze | TKL GmbH Ruhrgebiet', 'Grünpflege, Winterdienst, Spielplatzpflege, Baumpflege sowie Neubau und Sanierung von Außenanlagen für Wohnungsunternehmen und Firmen in Duisburg, Castrop-Rauxel und dem ganzen Ruhrgebiet.', inhalt, 'leistungen'))


# =====================================================================
# LEISTUNGS-DETAILSEITEN
# =====================================================================
DETAILS = {
 'gruenpflege': dict(
   h1='Grünpflege für Wohnanlagen und Firmengelände.', pinsel='Grünpflege',
   eyebrow='Kernleistung', seo_titel='Grünpflege im Ruhrgebiet für Wohnanlagen & Gewerbe | TKL GmbH',
   seo='Grünpflege in Duisburg, Essen und dem Ruhrgebiet: Rasenpflege, Hecken- und Gehölzschnitt, Laub und Wegepflege für Wohnungsgenossenschaften, Immobilienunternehmen und Firmen – mit fester Kolonne.',
   lead='Rasen mähen, Hecken schneiden, Laub entfernen, Wege sauber halten: Wir kümmern uns um das ganze „Drumherum“ Ihrer Immobilien – regelmäßig, nach festem Plan und mit einer Kolonne, die Ihre Anlage kennt.',
   bild='maeher-block', alt='TKL-Mitarbeiter auf dem Aufsitzmäher vor einem Wohnblock, zwischen zwei Bäumen',
   leistungen=['Rasenpflege mit Aufsitzmähern und Freischneidern', 'Hecken-, Strauch- und Gehölzschnitt', 'Pflege von Beeten und Pflanzflächen', 'Laubbeseitigung im Herbst', 'Wege, Plätze und Zufahrten sauber halten', 'Kontrolle auf Gefahrenstellen bei jedem Einsatz', 'Schnittgut-Entsorgung inklusive', 'Pflege nach Ihrem Leistungsverzeichnis'],
   kacheln=[('team', 'Feste Kolonne', 'Dieselben Leute kommen jede Woche – eingespielt, schnell, ohne lange Einweisung.'), ('kalender', 'Feste Intervalle', 'Pflegegänge nach Plan über die ganze Saison – Sie müssen nichts hinterhertelefonieren.'), ('traktor', 'Profi-Technik', 'Große Aufsitzmäher schaffen weite Rasenflächen in einem Bruchteil der Zeit.'), ('besen', 'Sauber hinterlassen', 'Nach dem Mähen wird geblasen und gekehrt – Wege und Eingänge bleiben sauber.')],
   galerie=[('trimmer-baum', 'TKL-Mitarbeiter mäht mit dem Freischneider um einen Baum herum', True), ('trimmer-weg', 'Mitarbeiter mit Freischneider an einem Gehweg', False), ('staub-trimmer', 'Freischneider-Einsatz an einer Böschung', False), ('maeher-front', 'Aufsitzmäher von vorn', False), ('blasgeraet', 'Laubbläser auf einem gepflasterten Weg', False)],
   faq=[('Wie oft kommen Sie zur Pflege?', 'Das legen wir gemeinsam fest – je nach Fläche, Nutzung und Budget. Üblich sind feste Pflegegänge über die Saison, zum Beispiel wöchentlich oder alle zwei Wochen beim Rasen, dazu Hecken- und Gehölzschnitt zu den passenden Zeiten.'),
        ('Kommt wirklich immer dieselbe Kolonne?', 'Ja, das ist bei uns die Regel. Jede Anlage hat ihre feste Kolonne. Die Mitarbeiter kennen das Objekt, die Abläufe und Ihre Ansprechpartner – das spart Zeit und Abstimmung.'),
        ('Wer entsorgt das Schnittgut?', 'Das übernehmen wir. Rasenschnitt, Laub und Gehölzschnitt nehmen wir mit oder entsorgen sie nach Absprache.'),
        ('Übernehmen Sie auch Privatgärten?', 'Nein. Wir sind auf größere Flächen von Wohnungsunternehmen, Genossenschaften, Verwaltungen und Firmen spezialisiert.')]),
 'winterdienst': dict(
   h1='Winterdienst, auf den Sie sich verlassen können.', pinsel='verlassen',
   eyebrow='Räum- und Streudienst', seo_titel='Winterdienst Duisburg, Essen & Ruhrgebiet | TKL GmbH',
   seo='Winterdienst für Wohnanlagen und Firmengelände im Ruhrgebiet: Räumen und Streuen von Gehwegen, Zufahrten und Parkplätzen – früh am Morgen, mit Kehrmaschinen und Streutechnik.',
   lead='Schnee und Glätte warten nicht auf Bürozeiten. Wir räumen und streuen Gehwege, Hauszugänge, Zufahrten und Parkplätze, bevor Ihre Mieter und Mitarbeiter unterwegs sind – den ganzen Winter, nach Wetterlage.',
   bild='illu-winterdienst', alt='', illu=True,
   leistungen=['Räumen von Schnee auf Gehwegen und Zugängen', 'Streuen bei Glätte und Eis', 'Zufahrten, Parkplätze und Höfe', 'Einsätze früh morgens und nach Wetterlage', 'Kehrmaschinen und Streufahrzeuge', 'Wohnanlagen ebenso wie Firmen- und Industriegelände'],
   kacheln=[('uhr', 'Früh vor Ort', 'Wir sind unterwegs, bevor der Berufsverkehr beginnt – damit niemand auf dem Weg zur Arbeit ausrutscht.'), ('besen', 'Eigene Technik', 'Kehrmaschinen und Streugeräte aus dem eigenen Fuhrpark – kein Warten auf Subunternehmer.'), ('team', 'Mehr Leute im Winter', 'Für die Wintersaison verstärken wir unsere Teams gezielt, damit jede Tour sicher abgedeckt ist.'), ('pin', 'Kurze Wege', 'Drei Standorte im Revier – unsere Fahrzeuge stehen nah an Ihren Objekten.')],
   bildzeile=('kehrmaschine', 'Grüne Kehrmaschine von TKL mit Kehrbesen in der Maschinenhalle'),
   faq=[('Übernehmen Sie die Räum- und Streupflicht?', 'Wir übernehmen den Winterdienst im vereinbarten Umfang und zu den vereinbarten Zeiten. Wie die Verkehrssicherungspflicht vertraglich geregelt wird, besprechen wir gemeinsam im Angebot.'),
        ('Ab wann sollte ich den Winterdienst beauftragen?', 'Am besten im Spätsommer oder Herbst. Dann planen wir Ihre Objekte fest in die Touren ein, bevor der erste Frost kommt.'),
        ('Räumen Sie auch Parkplätze und Firmenzufahrten?', 'Ja. Neben Gehwegen und Hauszugängen räumen und streuen wir auch Zufahrten, Höfe und Parkplätze – mit Fahrzeugen, die für größere Flächen ausgelegt sind.')]),
 'spielplaetze': dict(
   h1='Sichere Spielplätze in Ihren Anlagen.', pinsel='Sichere',
   eyebrow='Kontrolle · Pflege · Reparatur', seo_titel='Spielplatzkontrolle & Spielplatzpflege im Ruhrgebiet | TKL GmbH',
   seo='Spielplatzkontrolle, Spielplatzpflege und Reparaturen für Wohnungsunternehmen und Genossenschaften in Duisburg, Essen und dem Ruhrgebiet. Sichere Spielgeräte, sauberer Sand, gepflegte Flächen.',
   lead='Spielplätze müssen nicht nur schön aussehen, sondern vor allem sicher sein. Unsere geschulten Mitarbeiter kontrollieren Spielgeräte regelmäßig, pflegen die Flächen und kümmern sich um Reparaturen – damit Kinder unbeschwert spielen können.',
   bild='illu-spielplaetze', alt='', illu=True,
   leistungen=['Regelmäßige Sichtkontrollen der Spielgeräte', 'Prüfung auf Verschleiß und Unfallgefahren', 'Sand reinigen, auflockern oder austauschen', 'Pflege von Fallschutz und Umgebung', 'Reparatur und Austausch einzelner Bauteile', 'Neubau von Spielplätzen auf Anfrage'],
   kacheln=[('schild', 'Sicherheit zuerst', 'Abnutzung und Gefahrenstellen erkennen wir früh – bevor etwas passiert.'), ('liste', 'Nachvollziehbar', 'Sie erfahren, was wir geprüft und erledigt haben, und bekommen Bescheid, wenn etwas zu tun ist.'), ('werkzeug', 'Direkt repariert', 'Kleinere Schäden beheben wir meist gleich mit – größere stimmen wir mit Ihnen ab.'), ('blatt', 'Alles in einem Gang', 'Spielplatzkontrolle und Grünpflege lassen sich wunderbar kombinieren.')],
   faq=[('Wie oft sollte ein Spielplatz kontrolliert werden?', 'Spielplätze werden in festen Intervallen kontrolliert – von der regelmäßigen Sichtkontrolle bis zur jährlichen Hauptuntersuchung. Wie oft genau, hängt von Nutzung und Geräten ab. Wir beraten Sie gern dazu.'),
        ('Können Sie Spielgeräte auch reparieren?', 'Ja. Kleinere Reparaturen und den Austausch von Verschleißteilen übernehmen wir selbst. Bei größeren Arbeiten stimmen wir das Vorgehen mit Ihnen ab.'),
        ('Lässt sich die Spielplatzpflege mit der Grünpflege verbinden?', 'Sehr gut sogar. Die Kolonne, die Ihre Anlage pflegt, hat den Spielplatz ohnehin im Blick.')]),
 'baumpflege': dict(
   h1='Baumpflege für gesunde, sichere Bäume.', pinsel='sichere',
   eyebrow='Im Rahmen der Grünpflege', seo_titel='Baumpflege für Wohnanlagen & Gewerbe im Ruhrgebiet | TKL GmbH',
   seo='Baumpflege auf Wohnanlagen und Firmengeländen im Ruhrgebiet: Kronenpflege, Totholz entfernen, Lichtraumprofil und Verkehrssicherheit – als Teil der laufenden Grünpflege.',
   lead='Bäume machen Wohnanlagen lebenswert – solange sie gesund und sicher sind. Wir pflegen den Baumbestand auf den Flächen, die wir betreuen: mit Blick für das Ganze und für die Sicherheit Ihrer Mieter, Kunden und Besucher.',
   bild='illu-baumpflege', alt='', illu=True,
   leistungen=['Kronenpflege und Rückschnitt', 'Totholz entfernen', 'Lichtraumprofil über Wegen und Zufahrten', 'Kontrolle der Verkehrssicherheit', 'Arbeiten mit Hubarbeitsbühne', 'Abtransport und Entsorgung des Schnittguts'],
   kacheln=[('schild', 'Verkehrssicherheit', 'Wir sehen bei jedem Pflegegang hin und melden uns, wenn ein Baum Aufmerksamkeit braucht.'), ('baum', 'Fachgerechter Schnitt', 'Geschulte Mitarbeiter schneiden so, dass der Baum gesund bleibt.'), ('team', 'Starke Partner', 'Für besondere Fälle wie Seilklettertechnik arbeiten wir mit erfahrenen Fachpartnern zusammen.'), ('liste', 'Teil der Pflege', 'Baumpflege läuft bei uns zusammen mit der Grünpflege – ein Ansprechpartner, ein Termin.')],
   hinweis='Baumpflege bieten wir für Flächen an, die wir ohnehin pflegen. Für reine Einzelbaum-Aufträge ohne laufende Pflege sind wir nicht der richtige Partner.',
   faq=[('Fällen Sie auch Bäume?', 'Wenn es auf einer von uns gepflegten Fläche nötig ist, ja – nach Absprache und mit den nötigen Genehmigungen. Aufwendige Fällungen übernehmen wir gemeinsam mit Fachpartnern.'),
        ('Machen Sie auch einzelne Baumschnitte ohne Pflegevertrag?', 'In der Regel nicht. Baumpflege ist bei uns Teil der laufenden Grünpflege Ihrer Anlage.')]),
 'aussenanlagen': dict(
   h1='Neubau und Sanierung von Außenanlagen.', pinsel='Außenanlagen',
   eyebrow='Für unsere Bestandskunden', seo_titel='Neubau & Sanierung von Außenanlagen im Ruhrgebiet | TKL GmbH',
   seo='Neue Außenanlagen nach Sanierung oder Neubau: Rasen anlegen, Pflanzungen, Wege und Pflasterarbeiten für Wohnungsunternehmen und Firmen im Ruhrgebiet – aus einer Hand.',
   lead='Nach der Fassadensanierung oder beim Neubau sollen auch die Außenanlagen wieder stimmen. Für Kunden, deren Flächen wir pflegen, legen wir Rasen neu an, pflanzen Bäume und Sträucher und bauen Wege und Pflasterflächen.',
   bild='illu-neubau', alt='', illu=True,
   leistungen=['Rasenflächen neu anlegen (Saat oder Rollrasen)', 'Bäume, Hecken und Sträucher pflanzen', 'Wege, Zufahrten und Pflasterflächen', 'Wiederherstellung nach Sanierungen', 'Reparaturen an bestehenden Anlagen', 'Übergang direkt in die laufende Pflege'],
   kacheln=[('pflaster', 'Pflaster vom Fach', 'Mit der Eintragung in die Straßenbauer-Handwerksrolle bauen wir Pflasterflächen fachgerecht.'), ('haus', 'Nach der Sanierung', 'Wenn die Fassade fertig ist, bringen wir das Grün drumherum wieder in Form.'), ('blatt', 'Bau und Pflege', 'Was wir bauen, pflegen wir anschließend – aus einer Hand, ohne Übergabeprobleme.'), ('kalender', 'Planbar', 'Wir stimmen uns mit Ihrer Bauleitung ab und halten den Zeitplan.')],
   hinweis='Neubau und Sanierung übernehmen wir vor allem für Kunden, deren Anlagen wir bereits pflegen. Sprechen Sie uns gern an – wir sagen Ihnen ehrlich, ob Ihr Projekt zu uns passt.',
   faq=[('Bauen Sie auch Gärten für Privatkunden?', 'Nein. Wir arbeiten für Wohnungsunternehmen, Genossenschaften, Verwaltungen und Firmen.'),
        ('Übernehmen Sie danach auch die Pflege?', 'Ja, und genau das ist der Vorteil: Die neue Anlage geht direkt in die laufende Pflege über – durch dieselbe Firma.')]),
}

def leistung(l):
    s, t, k, i, f, b, illu = l
    d = DETAILS[s]
    h1 = d['h1'].replace(d['pinsel'], f'<span class="pinsel{" gruen" if f == "gruen" else ""}">{d["pinsel"]}</span>', 1)
    liste = ''.join(f'<li>{x}</li>' for x in d['leistungen'])
    kacheln = ''.join(f'<div class="kachel rv d{n % 2 + 1}"><h3>{ic(a)} {b_}</h3><p>{c}</p></div>' for n, (a, b_, c) in enumerate(d['kacheln']))
    gal = ''
    if d.get('galerie'):
        gal = '<div class="galerie" style="margin-top:20px">' + ''.join(f'<figure class="rv{" breit" if br else ""}">{bild(n, a, "(max-width: 640px) 50vw, 25vw")}</figure>' for n, a, br in d['galerie']) + '</div>'
    if d.get('bildzeile'):
        n, a = d['bildzeile']
        gal = f'<div class="grid-2" style="margin-top:20px;gap:20px;align-items:stretch"><figure class="foto-rund rv" style="margin:0;aspect-ratio:4/5">{bild(n, a, "(max-width: 980px) 100vw, 30vw")}</figure><div class="box rv d1" style="margin:0;display:flex;flex-direction:column;justify-content:center"><span class="eyebrow">Aus unserem Fuhrpark</span><h3>Eigene Kehrmaschinen und Streutechnik</h3><p class="muted" style="margin:0">Im Winter rücken unsere Kehrmaschinen und Streufahrzeuge vom eigenen Betriebshof aus. Gepflegt und gewartet in der eigenen Halle – damit sie laufen, wenn es drauf ankommt.</p></div></div>'
    hinweis = f'<div class="hinweis rv" style="margin-top:20px">{ic("info")}<p>{d["hinweis"]}</p></div>' if d.get('hinweis') else ''
    if s == 'gruenpflege':
        hinweis += f'<div class="box rv" style="margin-top:20px"><span class="eyebrow">Aus der Kolonne</span><h3>20.000 Quadratmeter an einem Tag</h3><p class="muted">In einer Siedlung in Duisburg-Walsum erzählt die Kolonne, wie sie eine ganze Anlage an einem Tag mäht, freischneidet und sauber hinterlässt – und wer dabei die meisten Schritte macht.</p><div class="stimmen zwei">{stimme("gruenpflege-20000")}{stimme("grischa-km")}</div></div>'
    andere = ''.join(f'<a href="/leistungen/{s2}/"{" aria-current=" + chr(34) + "page" + chr(34) if s2 == s else ""}>{t2} {ic("pfeil")}</a>' for s2, t2, *_ in LEISTUNGEN)
    inhalt = f'''
<section class="seitenkopf"><div class="wrap">
{brot(('Leistungen', '/leistungen/'), (t, None))}
<div class="grid-2">
<div><span class="eyebrow">{d['eyebrow']}</span><h1>{h1}</h1><p class="lead">{d['lead']}</p>
<div class="btn-reihe"><a class="btn" href="/kontakt/?leistung={s}#anfrage">Angebot anfragen {ic('pfeil', 'pfeil')}</a><a class="btn rand" href="{TEL_LINK}">{ic('tel')} {TEL}</a></div></div>
<div class="seitenkopf-bild{' illu' if illu else ''}">{bild(d['bild'], d['alt'], '(max-width: 980px) 100vw, 50vw', eager=True)}</div>
</div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap detail-grid">
<div>
<div class="box rv"><h2 style="font-size:clamp(1.6rem,2.6vw,2.2rem)">Das übernehmen wir für Sie</h2><ul class="haken zwei">{liste}</ul></div>
<div class="box rv"><h2 style="font-size:clamp(1.6rem,2.6vw,2.2rem)">Ihr Vorteil mit TKL</h2><div class="kacheln">{kacheln}</div></div>
{hinweis}{gal}
</div>
<aside class="seitenleiste">
<div class="kontaktkarte"><span class="eyebrow" style="color:rgba(255,255,255,.75)">Angebot</span><h3>{t} für Ihr Objekt</h3><p>Schildern Sie kurz Ihr Objekt – wir melden uns und schauen uns die Flächen vor Ort an.</p><a class="btn" href="/kontakt/?leistung={s}#anfrage">Anfrage starten {ic('pfeil', 'pfeil')}</a><a class="tel-gross" href="{TEL_LINK}">{ic('tel')} {TEL}</a></div>
<nav class="mini-links" aria-label="Weitere Leistungen">{andere}</nav>
</aside>
</div></section>
{faq(d['faq'])}
{cta_hecke(f'{t} im Ruhrgebiet? <span class="pinsel gruen">Sprechen wir.</span>', knopf='Angebot anfragen', link=f'/kontakt/?leistung={s}#anfrage')}'''
    schreibe(f'/leistungen/{s}/', seite(f'/leistungen/{s}/', d['seo_titel'], d['seo'], inhalt, 'leistungen'))


# =====================================================================
# ÜBER UNS
# =====================================================================
def ueber_uns():
    inhalt = f'''
<section class="seitenkopf"><div class="wrap">
{brot(('Über uns', None))}
<div class="grid-2">
<div><span class="eyebrow">Über TKL</span><h1>Ein Team aus dem Revier – für die <span class="pinsel gruen">Grünflächen</span> im Revier.</h1>
<p class="lead">Die TKL GmbH pflegt seit vielen Jahren Außenanlagen im Ruhrgebiet. Von unserer Zentrale in Duisburg und der Niederlassung in Castrop-Rauxel aus sind täglich rund 50 Mitarbeiter in 10 bis 12 Kolonnen unterwegs – für Genossenschaften, Wohnungsunternehmen und Firmen.</p></div>
<div class="seitenkopf-bild">{bild('kollegen-duo', 'Zwei langjährige TKL-Kollegen in Arbeitskleidung stehen Arm in Arm auf einer Rasenfläche', '(max-width: 980px) 100vw, 50vw', eager=True)}</div>
</div></div></section>

<section class="sec" style="padding-top:0"><div class="wrap">
<div class="sec-kopf rv"><span class="eyebrow">Wofür wir stehen</span><h2>Was unsere Kunden an uns schätzen.</h2></div>
<div class="werte">
<div class="wert rv"><b>01</b><h3>Feste Teams</h3><p>Jede Anlage hat ihre Kolonne. Wir stellen die Teams so zusammen, dass die Leute zueinander passen – das merkt man an Tempo und Qualität.</p></div>
<div class="wert rv d1"><b>02</b><h3>Gutes Gerät</h3><p>Wir investieren in Profi-Maschinen und pflegen sie selbst. Wer gutes Werkzeug hat, macht gute Arbeit.</p></div>
<div class="wert rv d2"><b>03</b><h3>Leute, die bleiben</h3><p>Einige Kollegen sind seit über 20 Jahren dabei. Diese Erfahrung ist unser größter Wert.</p></div>
<div class="wert rv d3"><b>04</b><h3>Sauber übergeben</h3><p>Wir fahren erst, wenn alles ordentlich ist – Wege gekehrt, Schnittgut weg, Flächen gepflegt.</p></div>
</div></div></section>

<section class="sec bg-weiss"><div class="wrap grid-2">
<div class="rv" style="max-width:360px;justify-self:center;width:100%">{stimme('ralf-vorstellung')}</div>
<div><span class="eyebrow">Unsere Haltung</span><h2>Wir machen, was wir können. Und das richtig.</h2>
<p class="lead">TKL ist kein Bauchladen. Wir konzentrieren uns auf das, worin wir stark sind: große Grünflächen pflegen, Winterdienst fahren, Spielplätze sicher halten. Dafür haben wir eingespielte Teams, gute Maschinen und kurze Wege.</p>
<p>Unsere Kunden sind vor allem Wohnungsgenossenschaften, Immobilienunternehmen und Firmen im Ruhrgebiet. Viele davon begleiten wir seit Jahren – mit denselben Kolonnen, die ihre Anlagen in- und auswendig kennen.</p>
<p>Seit 2003 gehört TKL zur niederländischen Krinkels-Gruppe, einem der großen Spezialisten für Garten- und Landschaftspflege in Europa. Für unsere Kunden heißt das: regionale Nähe mit einem starken Verbund im Rücken.</p>
<a class="textlink" href="/kontakt/">Lernen Sie uns kennen {ic('pfeil')}</a></div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-kopf split rv"><div><span class="eyebrow">Unsere Leute</span><h2>Die Menschen hinter TKL.</h2></div><p class="lead">Rund um Rasen, Hecke und Weg: Unsere Kolonnen sind jeden Tag draußen – bei Sonne, Regen und im Winter auch mal vor Sonnenaufgang.</p></div>
<div class="foto-band">
<figure class="rv">{bild('team-drei', 'Drei TKL-Mitarbeiter machen sich mit Gehörschutz und Geräten für den Einsatz bereit', '(max-width: 640px) 50vw, 30vw')}</figure>
<figure class="rv d1">{bild('portrait-erfahren', 'Erfahrener TKL-Mitarbeiter mit Tragegurt lächelt in die Kamera', '(max-width: 640px) 50vw, 22vw')}</figure>
<figure class="rv d2">{bild('portrait-jung', 'Junger TKL-Mitarbeiter mit Gehörschutz und Sonnenbrille lacht', '(max-width: 640px) 50vw, 22vw')}</figure>
<figure class="rv d3">{bild('trimmer-pfosten', 'TKL-Mitarbeiter mit Freischneider an einem Weg mit Laternen', '(max-width: 640px) 50vw, 30vw')}</figure>
</div>
<div class="stimmen vier rv" style="margin-top:28px">{stimme('stimme-duo')}{stimme('stimme-grischa')}{stimme('stimme-kai')}{stimme('stimme-nail')}</div>
</div></section>

<section class="sec bg-dunkel on-dark"><div class="wrap maschinen">
<div><span class="eyebrow">Betriebshof Duisburg</span><h2>Unsere Halle, unsere Maschinen.</h2>
<p class="lead">Aufsitzmäher, Kehrmaschinen, Streufahrzeuge und Transporter: Unser Fuhrpark steht in Duisburg und wird dort gewartet. Unsere Transporter erkennen Sie übrigens sofort – an der grünen Hecke und den Männern in Rot.</p>
<div class="geraete"><div class="geraet">{ic('auto')} 25 Fahrzeuge</div><div class="geraet">{ic('team')} 10–12 Kolonnen</div><div class="geraet">{ic('werkzeug')} Eigene Wartung</div><div class="geraet">{ic('pin')} 3 Standorte</div></div></div>
<div class="video-paar">
<div class="foto-rund rv" style="aspect-ratio:3/4">{bild('fuhrpark-transporter', 'TKL-Transporter mit Heckenmotiv-Beklebung neben einem Aufsitzmäher in der Fahrzeughalle', '(max-width: 980px) 50vw, 22vw', pos='35% center')}</div>
<div class="video-rahmen rv d1"><span class="badge">Rundgang Halle</span><video data-auto muted loop playsinline preload="none" poster="/assets/video/betriebshof-poster.webp" aria-label="Rundgang durch die Maschinenhalle der TKL"><source src="/assets/video/betriebshof.mp4" type="video/mp4"></video></div>
</div></div></section>

<section class="sec"><div class="wrap gebiet">
<div><span class="eyebrow">Standorte</span><h2>Zweimal im Ruhrgebiet.</h2><p class="lead">Kurze Anfahrt, schnelle Reaktion: Unsere Teams starten dort, wo Ihre Objekte sind.</p>
<div class="standorte">
<div class="standort"><span class="nr" style="background:var(--red)">1</span><div><b>Zentrale Duisburg · westliches Ruhrgebiet</b><span>Hochstraße 184, 47228 Duisburg</span></div></div>
<div class="standort"><span class="nr" style="background:var(--green)">2</span><div><b>Niederlassung Castrop-Rauxel · östliches Ruhrgebiet</b><span>Oststraße 25, 44575 Castrop-Rauxel</span></div></div>
</div></div>
<div class="karte rv">{karte()}</div>
</div></section>
{cta_hecke('Lernen Sie uns kennen – <span class="pinsel gruen">vor Ort</span>.', 'Wir kommen vorbei, schauen uns Ihre Flächen an und sagen Ihnen ehrlich, was wir für Sie tun können.', 'Termin anfragen')}'''
    schreibe('/ueber-uns/', seite('/ueber-uns/', 'Über uns – TKL GmbH aus Duisburg | Grünpflege im Ruhrgebiet', 'Die TKL GmbH aus Duisburg: feste Kolonnen, eigener Maschinenpark und zwei Standorte im Ruhrgebiet. Lernen Sie das Team hinter der Grünpflege kennen.', inhalt, 'ueber'))


# =====================================================================
# FUNNEL-BAUSTEINE
# =====================================================================
def opt(name, wert, label, sub='', icon='', typ='radio', req=True, param=''):
    i = f'<span class="oi">{ic(icon)}</span>' if icon else ''
    s = f'<small>{sub}</small>' if sub else ''
    pid = f'{name}-{wert}'
    r = ' required' if (req and typ == 'radio') else ''
    dm = ' data-min="1"' if (typ == 'checkbox' and req) else ''
    dp = f' data-param="{param}"' if param else ''
    return f'<div class="option"><input type="{typ}" name="{name}" id="{pid}" value="{wert}" data-label="{esc(label)}"{r}{dm}{dp}><label for="{pid}">{i}<span>{label}{s}</span></label></div>'

def funnel_rahmen(titel, typ, anrede, schritte, danke_html, vertrauen):
    return f'''<div class="funnel" id="{'bewerben' if typ == 'bewerbung' else 'anfrage-form'}">
<div class="funnel-kopf"><b>{titel}</b><span data-zaehler>Schritt 1</span></div>
<div class="fortschritt"><i></i></div>
<form data-typ="{typ}" data-anrede="{anrede}" novalidate>
<div class="honig" aria-hidden="true"><label>Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
{schritte}
<p class="f-fehler" role="alert" aria-live="polite"></p>
<div class="funnel-nav"><button type="button" class="zurueck">{ic('zurueck')} Zurück</button><button type="button" class="btn" data-weiter>Weiter {ic('pfeil', 'pfeil')}</button><button type="button" class="btn" data-absenden hidden>{'Bewerbung absenden' if typ == 'bewerbung' else 'Anfrage absenden'} {ic('pfeil', 'pfeil')}</button></div>
</form>
<div class="danke" aria-live="polite">{danke_html}</div>
<div class="vertrauen">{vertrauen}</div>
</div>'''


# =====================================================================
# KARRIERE
# =====================================================================
def karriere():
    stellen = [
      ('gruenpflege', 'Mitarbeiter Grünpflege (m/w/d)', ['Vollzeit', 'Quereinsteiger willkommen', 'Führerschein B']),
      ('kolonnenfuehrer', 'Kolonnenführer / Vorarbeiter Grünpflege (m/w/d)', ['Vollzeit', 'Erfahrung in der Grünpflege', 'Führerschein BE']),
      ('winterdienst', 'Winterdienst-Fahrer (m/w/d)', ['Saison Nov.–März', 'Aushilfe oder Minijob', 'Führerschein B']),
      ('initiativ', 'Initiativbewerbung', ['Du passt zu uns?', 'Sag uns, was du kannst']),
    ]
    stellen_html = ''.join(f'<button type="button" class="stelle rv d{n % 3 + 1}" data-vorauswahl="stelle={s}"><span><h3>{t}</h3><span class="meta">{"".join(f"<span>{m}</span>" for m in ms)}</span></span><span class="los">{ic("pfeil")}</span></button>' for n, (s, t, ms) in enumerate(stellen))
    schritte = f'''
<div class="schritt-f" data-auto="ja" data-hinweis="Bitte wähle eine Stelle aus."><h3>Für welche Stelle interessierst du dich?</h3><p>Keine Sorge – du kannst das im Gespräch noch ändern.</p>
<div class="optionen">{opt('stelle', 'gruenpflege', 'Mitarbeiter Grünpflege', 'Rasen, Hecken, Wege', 'blatt', param='stelle')}{opt('stelle', 'kolonnenfuehrer', 'Kolonnenführer / Vorarbeiter', 'Team führen, Objekte betreuen', 'team', param='stelle')}{opt('stelle', 'winterdienst', 'Winterdienst-Fahrer', 'Saison November bis März', 'schnee', param='stelle')}{opt('stelle', 'initiativ', 'Initiativbewerbung', 'Ich bin offen für mehr', 'stern', param='stelle')}</div></div>
<div class="schritt-f" data-auto="ja" data-hinweis="Bitte wähle eine Antwort."><h3>Wie viel Erfahrung bringst du mit?</h3><p>Quereinsteiger sind bei uns ausdrücklich willkommen.</p>
<div class="optionen">{opt('erfahrung', 'quereinsteiger', 'Quereinsteiger', 'Ich will draußen anpacken', 'blitz')}{opt('erfahrung', 'etwas', 'Etwas Erfahrung', 'Bis zu 2 Jahre in Grünpflege oder Bau', 'blatt')}{opt('erfahrung', 'viel', 'Viel Erfahrung', 'Mehr als 2 Jahre', 'stern')}{opt('erfahrung', 'ausbildung', 'Ausbildung im GaLaBau', 'Landschaftsgärtner o.&nbsp;Ä.', 'schild')}</div></div>
<div class="schritt-f" data-auto="ja" data-hinweis="Bitte wähle deinen Führerschein."><h3>Welchen Führerschein hast du?</h3><p>Für den Start reicht oft Klasse B.</p>
<div class="optionen">{opt('fuehrerschein', 'b', 'Klasse B', 'Pkw', 'auto')}{opt('fuehrerschein', 'be', 'Klasse BE', 'Pkw mit Anhänger', 'auto')}{opt('fuehrerschein', 'c', 'Klasse C / CE', 'Lkw', 'auto')}{opt('fuehrerschein', 'keiner', 'Noch keinen', 'Ist kein Ausschlusskriterium', 'info')}</div></div>
<div class="schritt-f" data-auto="ja" data-hinweis="Bitte wähle, ab wann du starten kannst."><h3>Ab wann könntest du starten?</h3><p>Damit wir besser planen können.</p>
<div class="optionen">{opt('start', 'sofort', 'Sofort', '', 'blitz')}{opt('start', '1monat', 'In etwa einem Monat', '', 'kalender')}{opt('start', 'spaeter', 'Später', '', 'uhr')}{opt('start', 'offen', 'Weiß ich noch nicht', '', 'info')}</div></div>
<div class="schritt-f"><h3>Wie erreichen wir dich?</h3><p>Wir melden uns – meistens kurz telefonisch. Einen Lebenslauf brauchst du dafür nicht.</p>
<div class="felder">
<div class="feld"><label for="b-name">Vor- und Nachname</label><input id="b-name" name="name" autocomplete="name" required></div>
<div class="feld"><label for="b-tel">Telefon / Handy</label><input id="b-tel" name="telefon" type="tel" autocomplete="tel" inputmode="tel" required></div>
<div class="feld"><label for="b-mail">E-Mail <em>(optional)</em></label><input id="b-mail" name="email" type="email" autocomplete="email"></div>
<div class="feld"><label for="b-ort">Wohnort <em>(optional)</em></label><input id="b-ort" name="ort" autocomplete="address-level2"></div>
<div class="feld voll"><label for="b-msg">Möchtest du uns noch etwas sagen? <em>(optional)</em></label><textarea id="b-msg" name="nachricht" rows="3"></textarea></div>
</div>
<label class="check"><input type="checkbox" name="datenschutz" value="ja"><span>Ich bin einverstanden, dass TKL meine Angaben zur Bearbeitung meiner Bewerbung speichert. Mehr dazu in der <a href="/datenschutz/" target="_blank">Datenschutzerklärung</a>.</span></label>
</div>'''
    danke = f'<span class="haken-gross">{ic("haken")}</span><h3>Danke, <span data-vorname>du</span>!</h3><p class="lead" style="max-width:520px;margin:0 auto 22px">Deine Bewerbung ist bei uns angekommen. Wir melden uns so schnell wie möglich – meistens telefonisch.</p><a class="btn rand" href="/">Zur Startseite</a>'
    vertrauen = f'<span>{ic("uhr")} Dauert ca. 1 Minute</span><span>{ic("haken")} Ohne Lebenslauf</span><span>{ic("schild")} Daten sicher</span>'
    fun = funnel_rahmen('Jetzt bei TKL bewerben', 'bewerbung', 'du', schritte, danke, vertrauen)

    inhalt = f'''
<section class="hero hero-karriere" aria-labelledby="k-titel"><div class="wrap hero-grid">
<div>{brot(('Karriere', None))}<span class="eyebrow">Jobs bei TKL · Ruhrgebiet</span>
<h1 id="k-titel">Draußen arbeiten. In einem Team, das <span class="pinsel">zusammenhält</span>.</h1>
<p class="lead">Bei TKL pflegst du Grünanlagen im ganzen Ruhrgebiet – mit Profi-Maschinen, deiner festen Kolonne und Chefs, die hinter dir stehen. Quereinsteiger sind herzlich willkommen.</p>
<div class="btn-reihe"><a class="btn" href="#bewerben">In 1 Minute bewerben {ic('pfeil', 'pfeil')}</a><a class="btn rand" href="#stellen">Offene Stellen</a></div>
<ul class="hero-chips"><li><span class="ic gruen" style="border-radius:50%;width:30px;height:30px;display:grid;place-items:center">{ic('haken')}</span>Ohne Lebenslauf</li><li><span class="ic gruen" style="border-radius:50%;width:30px;height:30px;display:grid;place-items:center">{ic('haken')}</span>Führerschein B reicht oft</li><li><span class="ic gruen" style="border-radius:50%;width:30px;height:30px;display:grid;place-items:center">{ic('haken')}</span>Start in Duisburg oder Castrop-Rauxel</li></ul>
</div>
<div class="hero-bild"><div class="hero-foto">{bild('portrait-jung', 'Nail, Mitarbeiter in der Grünpflege bei TKL, mit Gehörschutz und Sonnenbrille', '(max-width: 980px) 100vw, 52vw', eager=True)}</div>
<div class="sticker-gruppe" data-parallax="-0.06">{sticker('trimmer', 'TKL-Mitarbeiter mit Freischneider', 'hero-sticker', eager=True)}<span class="blase" aria-hidden="true">Komm in unser Team!</span></div>
<div class="hero-karte unten"><span class="punkt" style="color:var(--red)">{ic('herz')}</span><span><b>„Ich mag alles an meinem Job.“</b><span>Nail · seit 3,5 Jahren in der Grünpflege</span></span></div></div>
</div></section>

<section class="sec" style="padding-top:clamp(30px,4vw,60px)"><div class="wrap">
<div class="sec-kopf mitte rv"><span class="eyebrow">Das bekommst du bei uns</span><h2>Gute Gründe für TKL.</h2><p class="lead">Kein Versprechen aus dem Prospekt, sondern das, was unsere Leute jeden Tag erleben.</p></div>
<div class="benefits">
<div class="benefit rv"><span class="ic gruen">{ic('team')}</span><h3>Deine feste Kolonne</h3><p>Du arbeitest jeden Tag mit denselben Kollegen. Wir stellen die Teams so zusammen, dass es passt.</p></div>
<div class="benefit rv d1"><span class="ic rot">{ic('traktor')}</span><h3>Die besten Maschinen</h3><p>Aufsitzmäher, Profi-Freischneider, moderne Kehrmaschinen: Bei uns arbeitest du mit Gerät, das Spaß macht.</p></div>
<div class="benefit rv d2"><span class="ic blau">{ic('sonne')}</span><h3>Arbeit das ganze Jahr</h3><p>Im Sommer Grünpflege, im Winter Winterdienst – bei uns gibt es keine Zwangspause, wenn das Gras nicht wächst.</p></div>
<div class="benefit rv"><span class="ic sand">{ic('pin')}</span><h3>Kurze Wege</h3><p>Zwei Standorte im Revier: Duisburg und Castrop-Rauxel. Du startest dort, wo es für dich passt.</p></div>
<div class="benefit rv d1"><span class="ic gruen">{ic('shirt')}</span><h3>Ausrüstung gestellt</h3><p>Arbeitskleidung, Gehörschutz und alles, was du draußen brauchst, bekommst du von uns.</p></div>
<div class="benefit rv d2"><span class="ic rot">{ic('herz')}</span><h3>Chefs mit offenem Ohr</h3><p>Bei uns redet man miteinander. Viele Kollegen sind seit über 20 Jahren dabei – das sagt mehr als jeder Slogan.</p></div>
</div></div></section>

<section class="sec" style="padding-top:0"><div class="wrap">
<div class="sec-kopf split rv"><div><span class="eyebrow">Das sagen unsere Leute</span><h2>Frag nicht uns. <span class="pinsel">Frag die Kolonne.</span></h2></div><p class="lead">Grischa, Kai, Nail und die anderen erzählen, warum sie bei TKL arbeiten – manche seit über 30 Jahren.</p></div>
<div class="stimmen vier rv">{stimme('stimme-nail')}{stimme('stimme-grischa')}{stimme('stimme-kai')}{stimme('stimme-duo')}</div>
</div></section>

<section class="sec bg-dunkel on-dark"><div class="wrap">
<div class="sec-kopf split rv"><div><span class="eyebrow">Dein Arbeitstag</span><h2>So sieht ein Tag bei uns aus.</h2></div><p class="lead">Kein Büro, kein Fließband – sondern jeden Tag draußen und am Ende sehen, was man geschafft hat.</p></div>
<div class="tag-ablauf">
<div class="tag-schritt rv">{ic('kaffee')}<b>Start am Betriebshof</b><p>Kurze Absprache mit deiner Kolonne, Maschinen aufladen, los geht's.</p></div>
<div class="tag-schritt rv d1">{ic('auto')}<b>Raus zum Objekt</b><p>Ihr fahrt zu „euren“ Siedlungen und Firmengeländen – ihr kennt sie wie eure Westentasche.</p></div>
<div class="tag-schritt rv d2">{ic('blatt')}<b>Anpacken</b><p>Mähen, schneiden, blasen, kehren. Mit mehreren Kolonnen ist eine ganze Siedlung an einem Tag fertig.</p></div>
<div class="tag-schritt rv d3">{ic('flagge')}<b>Feierabend</b><p>Alles sauber hinterlassen, zurück zum Hof – und sehen, was ihr heute geschafft habt.</p></div>
</div></div></section>

<section class="sec" id="stellen"><div class="wrap grid-2" style="align-items:start">
<div><span class="eyebrow">Offene Stellen</span><h2>Wir suchen <span class="pinsel gruen">Verstärkung</span>.</h2><p class="lead">Such dir aus, was zu dir passt – oder bewirb dich einfach initiativ. Ein Klick auf eine Stelle startet deine Bewerbung.</p>
<div class="stellen" style="margin-top:26px">{stellen_html}</div>
<figure class="foto-rund rv" style="margin:22px 0 0;aspect-ratio:16/10">{bild('team-absprache', 'Zwei langjährige TKL-Kollegen im Gespräch auf einer Grünfläche, einer zeigt den Daumen hoch', '(max-width: 980px) 100vw, 45vw')}</figure>
</div>
<div style="position:sticky;top:100px">{fun}</div>
</div></section>

{faq([('Brauche ich eine Ausbildung?', 'Nein. Für die Grünpflege lernen wir dich an. Wichtig sind uns Zuverlässigkeit, Lust auf Arbeit draußen und Teamgeist. Eine Ausbildung im Garten- und Landschaftsbau ist natürlich ein Plus.'),
      ('Brauche ich einen Lebenslauf?', 'Für den ersten Schritt nicht. Füll einfach das kurze Formular aus – wir rufen dich an und lernen dich kennen. Unterlagen klären wir später.'),
      ('Welchen Führerschein brauche ich?', 'Für viele Stellen reicht Klasse B. Für Kolonnenführer ist BE gut, weil oft mit Anhänger gefahren wird. Und wenn du noch keinen hast, bewirb dich trotzdem.'),
      ('Gibt es auch im Winter Arbeit?', 'Ja. Im Winter fahren wir Winterdienst für unsere Kunden. Für die Saison suchen wir zusätzlich Aushilfen.'),
      ('Wo fange ich morgens an?', 'An einem unserer Standorte: Duisburg oder Castrop-Rauxel. Wo genau, besprechen wir mit dir – am liebsten möglichst nah an deinem Wohnort.')],
     'Fragen zur Bewerbung', 'Gut zu wissen')}
{cta_hecke('Lust auf Arbeit an der <span class="pinsel gruen">frischen Luft</span>?', 'Bewirb dich in einer Minute – ohne Lebenslauf. Oder ruf uns einfach an, wir freuen uns auf dich.', 'Jetzt bewerben', '#bewerben')}'''
    schreibe('/karriere/', seite('/karriere/', 'Jobs Grünpflege & Winterdienst Ruhrgebiet | Karriere bei TKL', 'Jobs bei TKL in Duisburg und Castrop-Rauxel: Mitarbeiter Grünpflege, Kolonnenführer und Winterdienst. Quereinsteiger willkommen – in 1 Minute bewerben, ohne Lebenslauf.', inhalt, 'karriere', funnel=True))


# =====================================================================
# KONTAKT / ANFRAGE
# =====================================================================
def kontakt():
    schritte = f'''
<div class="schritt-f" data-hinweis="Bitte wählen Sie mindestens eine Leistung."><h3>Welche Leistungen benötigen Sie?</h3><p>Mehrfachauswahl möglich.</p>
<div class="optionen">{opt('leistungen', 'gruenpflege', 'Grünpflege', 'Rasen, Hecken, Wege', 'blatt', 'checkbox', param='leistung')}{opt('leistungen', 'winterdienst', 'Winterdienst', 'Räumen und Streuen', 'schnee', 'checkbox', param='leistung')}{opt('leistungen', 'spielplaetze', 'Spielplätze', 'Kontrolle und Pflege', 'spiel', 'checkbox', param='leistung')}{opt('leistungen', 'baumpflege', 'Baumpflege', 'Im Rahmen der Pflege', 'baum', 'checkbox', param='leistung')}{opt('leistungen', 'aussenanlagen', 'Neubau / Sanierung', 'Außenanlagen, Wege, Pflaster', 'pflaster', 'checkbox', param='leistung')}{opt('leistungen', 'sonstiges', 'Etwas anderes', 'Erklären Sie es uns gleich', 'info', 'checkbox')}</div></div>
<div class="schritt-f" data-auto="ja"><h3>Um welche Art von Objekt geht es?</h3><p>So können wir Ihre Anfrage gleich richtig einordnen.</p>
<div class="optionen">{opt('objekt', 'wohnanlage', 'Wohnanlage / Siedlung', 'Genossenschaft, Wohnungsunternehmen', 'haus')}{opt('objekt', 'verwaltung', 'Mehrere verwaltete Objekte', 'Immobilien- oder Hausverwaltung', 'stadt')}{opt('objekt', 'firma', 'Firmengelände', 'Büro, Halle, Werk, Parkplatz', 'fabrik')}{opt('objekt', 'oeffentlich', 'Öffentliche Fläche', 'Kommune, Einrichtung', 'flagge')}</div></div>
<div class="schritt-f" data-auto="ja"><h3>Wie viele Objekte sind es ungefähr?</h3><p>Eine grobe Schätzung reicht.</p>
<div class="optionen">{opt('umfang', '1', 'Ein Objekt', '', 'pin')}{opt('umfang', '2-10', '2 bis 10 Objekte', '', 'liste')}{opt('umfang', '10+', 'Mehr als 10 Objekte', '', 'stadt')}{opt('umfang', 'unklar', 'Weiß ich noch nicht', '', 'info')}</div></div>
<div class="schritt-f" data-auto="ja"><h3>Wann soll es losgehen?</h3><p>Damit wir die Kapazitäten Ihrer Kolonne planen können.</p>
<div class="optionen">{opt('start', 'sofort', 'So schnell wie möglich', '', 'blitz')}{opt('start', 'saison', 'Zur nächsten Saison', '', 'kalender')}{opt('start', 'winter', 'Zum kommenden Winter', '', 'schnee')}{opt('start', 'vergleich', 'Erst mal ein Angebot zum Vergleich', '', 'liste')}</div></div>
<div class="schritt-f"><h3>Wie erreichen wir Sie?</h3><p>Wir melden uns zeitnah und vereinbaren bei Bedarf einen Termin vor Ort.</p>
<div class="felder">
<div class="feld"><label for="a-name">Ihr Name</label><input id="a-name" name="name" autocomplete="name" required></div>
<div class="feld"><label for="a-firma">Unternehmen <em>(optional)</em></label><input id="a-firma" name="firma" autocomplete="organization"></div>
<div class="feld"><label for="a-tel">Telefon</label><input id="a-tel" name="telefon" type="tel" autocomplete="tel" inputmode="tel"></div>
<div class="feld"><label for="a-mail">E-Mail</label><input id="a-mail" name="email" type="email" autocomplete="email"></div>
<div class="feld voll"><label for="a-ort">Ort / Lage der Objekte</label><input id="a-ort" name="ort" placeholder="z. B. Duisburg-Rheinhausen" required></div>
<div class="feld voll"><label for="a-msg">Ihre Nachricht <em>(optional)</em></label><textarea id="a-msg" name="nachricht" rows="3" placeholder="Größe der Flächen, besondere Wünsche, Fragen …"></textarea></div>
</div>
<label class="check"><input type="checkbox" name="datenschutz" value="ja"><span>Ich bin einverstanden, dass TKL meine Angaben zur Bearbeitung meiner Anfrage speichert. Mehr dazu in der <a href="/datenschutz/" target="_blank">Datenschutzerklärung</a>.</span></label>
</div>'''
    danke = f'<span class="haken-gross">{ic("haken")}</span><h3>Vielen Dank, Ihre Anfrage ist da!</h3><p class="lead" style="max-width:520px;margin:0 auto 22px">Wir prüfen Ihre Angaben und melden uns zeitnah bei Ihnen – in der Regel telefonisch, um einen Termin vor Ort abzustimmen.</p><a class="btn rand" href="/leistungen/">Leistungen ansehen</a>'
    vertrauen = f'<span>{ic("uhr")} Dauert ca. 2 Minuten</span><span>{ic("haken")} Unverbindlich</span><span>{ic("schild")} Daten sicher</span>'
    fun = funnel_rahmen('Angebot anfragen', 'anfrage', 'sie', schritte, danke, vertrauen)
    st = [('1', 'var(--red)', 'Zentrale Duisburg', 'Hochstraße 184, 47228 Duisburg', MAIL), ('2', 'var(--green)', 'Niederlassung Castrop-Rauxel', 'Oststraße 25, 44575 Castrop-Rauxel', 'ruhrgebietost@tkl.gmbh')]
    st_html = ''.join(f'<div class="standort"><span class="nr" style="background:{c}">{n}</span><div><b>{t}</b><span>{a}<br><a href="mailto:{m}">{m}</a></span></div></div>' for n, c, t, a, m in st)
    inhalt = f'''
<section class="seitenkopf" id="anfrage"><div class="wrap">
{brot(('Kontakt', None))}
<div class="grid-2" style="align-items:start">
<div><span class="eyebrow">Kontakt &amp; Anfrage</span><h1>Sprechen wir über Ihre <span class="pinsel gruen">Flächen</span>.</h1>
<p class="lead">Beantworten Sie ein paar kurze Fragen – wir melden uns zeitnah und schauen uns Ihr Objekt vor Ort an. Lieber direkt sprechen? Rufen Sie uns an.</p>
<div class="box" style="margin-top:26px;display:grid;gap:14px">
<a class="standort" href="{TEL_LINK}" style="text-decoration:none;box-shadow:none;background:var(--paper)"><span class="nr" style="background:var(--ink)">{ic('tel')}</span><div><b>{TEL}</b><span>Zentrale – Mo. bis Fr.</span></div></a>
<a class="standort" href="mailto:{MAIL}" style="text-decoration:none;box-shadow:none;background:var(--paper)"><span class="nr" style="background:var(--ink)">{ic('mail')}</span><div><b>{MAIL}</b><span>Wir antworten zeitnah</span></div></a>
</div>
<div class="video-seite box" style="margin-top:16px;grid-template-columns:minmax(0,1fr) 140px;padding:18px"><p class="muted" style="margin:0"><b style="color:var(--ink)">Ralf Jung, Geschäftsführer:</b> „Wenn ihr im Ruhrgebiet einen Partner für Grünpflege und Winterdienst sucht – sprecht uns an.“</p>{stimme('ralf-angebot', ' mini')}</div>
<div class="hinweis" style="margin-top:16px">{ic('info')}<p><b>Nur im Ruhrgebiet:</b> Wir sind von Duisburg und Castrop-Rauxel aus tätig. Frühere Niederlassungen in Berlin und im Münsterland gibt es nicht mehr.</p></div>
</div>
<div>{fun}</div>
</div></div></section>

<section class="sec bg-weiss" id="standorte"><div class="wrap gebiet">
<div><span class="eyebrow">Standorte</span><h2>So finden Sie uns.</h2><p class="lead">Unsere Zentrale ist in Duisburg, die Niederlassung in Castrop-Rauxel. Telefonisch erreichen Sie alle Standorte über die Zentrale.</p>
<div class="standorte">{st_html}</div></div>
<div class="karte rv">{karte()}</div>
</div></section>
{faq([('In welchen Städten sind Sie tätig?', 'Im gesamten Ruhrgebiet und den angrenzenden Städten – unter anderem in Duisburg, Essen, Oberhausen, Mülheim, Bottrop, Gelsenkirchen, Bochum, Herne, Castrop-Rauxel, Dortmund und Moers. Fragen Sie gern nach, wenn Ihr Ort nicht dabei ist.'),
      ('Haben Sie noch Niederlassungen in Berlin oder im Münsterland?', 'Nein. Wir sind ausschließlich im Ruhrgebiet tätig – mit unserer Zentrale in Duisburg und der Niederlassung in Castrop-Rauxel.'),
      ('Ist das Angebot kostenlos?', 'Ja. Besichtigung und Angebot sind für Sie unverbindlich und kostenfrei.'),
      ('Übernehmen Sie auch Privatgärten?', 'Nein. Wir arbeiten für Wohnungsunternehmen, Genossenschaften, Verwaltungen, Firmen und öffentliche Auftraggeber.')])}'''
    schreibe('/kontakt/', seite('/kontakt/', 'Kontakt & Angebot anfragen | TKL GmbH Duisburg & Castrop-Rauxel', 'Angebot für Grünpflege, Winterdienst oder Spielplatzpflege anfragen: TKL GmbH, Hochstraße 184, 47228 Duisburg, Telefon 02065 90 36-0. Niederlassung in Castrop-Rauxel.', inhalt, 'kontakt', funnel=True))


# =====================================================================
# RECHTLICHES
# =====================================================================
def impressum():
    inhalt = f'''<section class="seitenkopf"><div class="wrap schmal">{brot(('Impressum', None))}<h1>Impressum</h1></div></section>
<section class="sec" style="padding-top:0"><div class="wrap schmal"><div class="rechtstext">
<div class="entwurf-hinweis"><b>Vorschau-Hinweis:</b> Angaben aus dem bisherigen Impressum übernommen. Vor dem Go-live mit TKL prüfen (Geschäftsführung, Registerdaten, verantwortliche Person).</div>
<h2>Angaben gemäß § 5 DDG</h2>
<p>TKL GmbH<br>Hochstraße 184<br>47228 Duisburg</p>
<p>Telefon: 02065 90 36-0<br>Telefax: 02065 90 36-20<br>E-Mail: <a href="mailto:{MAIL}">{MAIL}</a></p>
<h3>Vertreten durch</h3><p>Ruud Krinkels, Peter van Boesschouten</p>
<h3>Registereintrag</h3><p>Eingetragen im Handelsregister<br>Registergericht: Amtsgericht Duisburg<br>Registernummer: HRB 24364</p>
<h3>Umsatzsteuer-ID</h3><p>Umsatzsteuer-Identifikationsnummer gemäß § 27a Umsatzsteuergesetz: DE120496681</p>
<h3>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h3><p>Ralf Jung, Anschrift wie oben</p>
<h3>Niederlassung</h3><p>Oststraße 25, 44575 Castrop-Rauxel</p>
<h3>Verbraucherstreitbeilegung</h3><p>Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
<h3>Haftung für Inhalte und Links</h3><p>Die Inhalte dieser Website werden mit größtmöglicher Sorgfalt erstellt. Für die Richtigkeit, Vollständigkeit und Aktualität übernehmen wir jedoch keine Gewähr. Für Inhalte externer Websites, auf die wir verlinken, sind ausschließlich deren Betreiber verantwortlich.</p>
<h3>Urheberrecht</h3><p>Texte, Fotos, Illustrationen und Grafiken dieser Website unterliegen dem deutschen Urheberrecht. Eine Verwendung außerhalb dieser Website bedarf der vorherigen schriftlichen Zustimmung der TKL GmbH.</p>
<h3>Gestaltung und Umsetzung</h3><p>Greenfield Digital</p>
</div></div></section>'''
    schreibe('/impressum/', seite('/impressum/', 'Impressum | TKL GmbH', 'Impressum der TKL GmbH, Hochstraße 184, 47228 Duisburg.', inhalt))

def datenschutz():
    inhalt = f'''<section class="seitenkopf"><div class="wrap schmal">{brot(('Datenschutz', None))}<h1>Datenschutz&shy;erklärung</h1></div></section>
<section class="sec" style="padding-top:0"><div class="wrap schmal"><div class="rechtstext">
<div class="entwurf-hinweis"><b>Entwurf:</b> Auf die Technik dieser Website zugeschnitten. Vor dem Go-live rechtlich prüfen lassen und Kontaktdaten des Verantwortlichen bzw. Datenschutzbeauftragten mit TKL abstimmen.</div>
<h2>1. Verantwortlicher</h2><p>TKL GmbH, Hochstraße 184, 47228 Duisburg, Telefon 02065 90 36-0, E-Mail <a href="mailto:{MAIL}">{MAIL}</a>.</p>
<h2>2. Grundsätze</h2><p>Wir verarbeiten personenbezogene Daten nur, soweit das für den Betrieb dieser Website, die Bearbeitung Ihrer Anfragen und Bewerbungen oder aufgrund gesetzlicher Pflichten erforderlich ist. Diese Website setzt <b>keine Cookies</b> und speichert keine Daten auf Ihrem Endgerät.</p>
<h2>3. Hosting und Server-Protokolle</h2><p>Die Website wird über GitHub Pages (GitHub Inc., USA) bereitgestellt. Beim Aufruf werden technisch notwendige Daten wie IP-Adresse, Zeitpunkt, aufgerufene Seite und Browserinformationen verarbeitet, um die Seite auszuliefern und die Sicherheit zu gewährleisten (Art. 6 Abs. 1 lit. f DSGVO). Die Übermittlung in die USA erfolgt auf Grundlage des EU-US Data Privacy Framework bzw. von Standardvertragsklauseln.</p>
<h2>4. Anfrage- und Bewerbungsformulare</h2><p>Wenn Sie uns über ein Formular eine Anfrage oder Bewerbung senden, verarbeiten wir Ihre Angaben (z. B. Name, Firma, Telefon, E-Mail, Ort, Nachricht und Ihre Antworten im Formular), um Ihre Anfrage zu bearbeiten bzw. das Bewerbungsverfahren durchzuführen (Art. 6 Abs. 1 lit. b DSGVO, für Bewerbungen zusätzlich § 26 BDSG). Die Daten werden in einer Datenbank bei Supabase (Supabase Inc.; Serverstandort EU) gespeichert, die ausschließlich für TKL und deren beauftragten Dienstleister zugänglich ist. Anfragen löschen wir, sobald sie erledigt sind und keine Aufbewahrungspflichten bestehen; Bewerbungen spätestens sechs Monate nach Abschluss des Verfahrens, sofern Sie nicht in eine längere Speicherung eingewilligt haben.</p>
<h2>5. Reichweitenmessung ohne Cookies</h2><p>Um zu verstehen, welche Seiten genutzt werden, zählen wir Seitenaufrufe anonym: Gespeichert werden die aufgerufene Seite, die Herkunft (z. B. Suchmaschine) und der Gerätetyp. Zur Unterscheidung von Besuchern bilden wir serverseitig einen täglich wechselnden, nicht umkehrbaren Prüfwert aus IP-Adresse und Browserkennung; die IP-Adresse selbst wird nicht gespeichert. Es werden keine Cookies gesetzt und keine Profile gebildet (Art. 6 Abs. 1 lit. f DSGVO).</p>
<h2>6. Schriftarten</h2><p>Alle Schriftarten werden direkt von unserem Server geladen. Es findet keine Verbindung zu Google Fonts oder anderen Drittanbietern statt.</p>
<h2>7. Ihre Rechte</h2><p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit sowie Widerspruch gegen Verarbeitungen auf Grundlage berechtigter Interessen. Außerdem können Sie sich bei einer Datenschutzaufsichtsbehörde beschweren, etwa bei der Landesbeauftragten für Datenschutz und Informationsfreiheit Nordrhein-Westfalen.</p>
<h2>8. Kontakt zum Datenschutz</h2><p>Bei Fragen zum Datenschutz erreichen Sie uns unter <a href="mailto:{MAIL}">{MAIL}</a>.</p>
<p class="muted">Stand: Oktober 2026</p>
</div></div></section>'''
    schreibe('/datenschutz/', seite('/datenschutz/', 'Datenschutz | TKL GmbH', 'Datenschutzerklärung der TKL GmbH: Formulare, Hosting, Reichweitenmessung ohne Cookies.', inhalt))

def fehlerseite():
    inhalt = f'''<section class="sec"><div class="wrap schmal" style="text-align:center"><span class="eyebrow">Fehler 404</span><h1>Hier wächst leider nichts.</h1><p class="lead">Die Seite gibt es nicht (mehr). Vielleicht hilft Ihnen einer dieser Links weiter:</p>
<div class="btn-reihe" style="justify-content:center"><a class="btn" href="/">Zur Startseite</a><a class="btn rand" href="/leistungen/">Leistungen</a><a class="btn rand" href="/kontakt/">Kontakt</a></div></div></section>'''
    s = seite('/404.html', 'Seite nicht gefunden | TKL GmbH', 'Diese Seite wurde nicht gefunden.', inhalt, body_attr=' data-kein-tracking')
    open(os.path.join(SITE, '404.html'), 'w', encoding='utf-8').write(mit_basis(s)); print('✓ /404.html')

def weiterleitungen():
    """Alte WordPress-Adressen von tkl.gmbh -> neue Seiten (wichtig nach dem Domain-Umzug)."""
    ziele = {'gruenpflege': '/leistungen/gruenpflege/', 'winterdienst': '/leistungen/winterdienst/', 'neubau': '/leistungen/aussenanlagen/',
             'baumpflege': '/leistungen/baumpflege/', 'spielplaetze': '/leistungen/spielplaetze/', 'stellenanzeigen': '/karriere/', 'referenzen': '/ueber-uns/'}
    for alt, neu in ziele.items():
        d = os.path.join(SITE, alt); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(mit_basis(f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Weiterleitung</title><meta name="robots" content="noindex"><link rel="canonical" href="{BASIS_URL}{neu}"><meta http-equiv="refresh" content="0; url={neu}"><script>location.replace("{neu}")</script></head><body><a href="{neu}">Weiter zur neuen Seite</a></body></html>'))
    print('✓ Weiterleitungen', len(ziele))

def intern():
    """Interne Abstimmungsseite für Janni/Steffi – nicht verlinkt, noindex."""
    b = '''<svg viewBox="0 0 100 100" role="img" aria-label="Logo-Entwurf B"><rect x="4" y="4" width="92" height="92" rx="26" fill="#15191C"/><rect x="24" y="30" width="11" height="42" rx="5.5" fill="#2DB35C"/><circle cx="64" cy="35" r="14" fill="#E8352D"/><path d="M46 72h34L63 44Z" fill="#4AA3EA" stroke="#4AA3EA" stroke-width="4" stroke-linejoin="round"/></svg>'''
    klaeren = [
     ('Standort Essen', 'Ralf Jung nennt im Video zwei Niederlassungen: Duisburg (Westen) und Castrop-Rauxel (Osten). Die Essener Adresse (Bunsenstraße 30) habe ich deshalb herausgenommen. Gibt es den Standort noch?', 'Startseite, Kontakt, Footer'),
     ('Zahlen aus dem Video', 'Jetzt verwendet: 50 Mitarbeiter, 10–12 Kolonnen (aus Ralfs Video), 25 Fahrzeuge (Janni), Kai über 30 Jahre dabei. Bitte kurz bestätigen.', 'Startseite, Über uns'),
     ('Videos freigeben', 'Ralf, Grischa, Kai, Nail und das Duo sind mit O-Tönen und Untertiteln eingebunden. Bitte von TKL und den Mitarbeitern das OK holen (Recht am eigenen Bild).', 'Startseite, Karriere, Über uns'),
     ('Krinkels-Gruppe', '„Seit 2003 Teil der Krinkels-Gruppe“ stammt von der alten Seite. Noch aktuell und soll das genannt werden?', 'Über uns'),
     ('Impressum', 'Vertreter (Ruud Krinkels, Peter van Boesschouten), HRB 24364, USt-ID und Fax aus dem alten Impressum übernommen – aktuell?', 'Impressum'),
     ('Karriere-Vorteile', 'Bitte bestätigen: Arbeitskleidung gestellt, Arbeit das ganze Jahr (Winterdienst), Führerschein B reicht für den Start, BE für Kolonnenführer.', 'Karriere'),
     ('Offene Stellen', 'Angelegt: Mitarbeiter Grünpflege, Kolonnenführer/Vorarbeiter, Winterdienst-Fahrer (Saison), Initiativ. Passt das? Gibt es Gehaltsspannen oder Zusatzleistungen, die wir nennen dürfen?', 'Karriere'),
     ('Ansprechpartner', 'Die alte Seite nennt Thomas Schröder und Wolfram Rybacki mit Durchwahlen. Noch aktuell? Dann bekommen die Leistungsseiten wieder Namen und Fotos.', 'Leistungsseiten'),
     ('Referenzen', 'Dürfen Kunden genannt werden (z. B. LEG, GEBAG, SWS Mülheim, Covivio)? Mit Logos wäre ein Referenzband auf der Startseite stark.', 'Startseite'),
     ('Qualifikationen', 'Spielplatzkontrollen (Norm DIN EN 1176, Schulungen), Baumpflege (AS Baum I/II), Straßenbauer-Handwerksrolle für Pflaster – noch aktuell?', 'Leistungsseiten'),
     ('Benachrichtigung', 'Neue Anfragen und Bewerbungen landen im Backend. An welche E-Mail-Adresse(n) soll zusätzlich eine Info gehen?', 'Backend'),
     ('Erreichbarkeit', 'Telefonzeiten der Zentrale (aktuell „Mo. bis Fr.“) und ob die Niederlassungen eigene Durchwahlen haben.', 'Kontakt'),
     ('Instagram & Co.', 'Link zum neuen Instagram-Kanal; Facebook/YouTube der alten Seite noch aktiv?', 'Footer'),
    ]
    umzug = [
     ('Domain-Verwaltung', 'Bei welchem Anbieter liegt tkl.gmbh (z. B. IONOS, Strato)? Wir brauchen entweder einen Zugang oder eine Person (IT/Agentur), die zwei DNS-Einträge setzt.'),
     ('DNS-Einträge', 'tkl.gmbh: A-Einträge auf 185.199.108.153, .109.153, .110.153, .111.153 · www.tkl.gmbh: CNAME auf frdlnk-gc.github.io. Danach stellen wir die Domain in GitHub um, das Zertifikat kommt automatisch.'),
     ('E-Mail nicht anfassen', 'MX-, SPF- und DKIM-Einträge bleiben unverändert – info@tkl.gmbh und alle Postfächer laufen weiter. Vorher Screenshot der aktuellen DNS-Liste sichern.'),
     ('Alte Website', 'WordPress-Hosting erst nach dem Umzug kündigen. Alte Adressen (/gruenpflege/, /stellenanzeigen/ …) leiten wir bereits auf die neuen Seiten um.'),
     ('Google-Unternehmensprofil', 'Zugang oder Freigabe, damit Standorte (Berlin, Münsterland raus), Telefonnummer und Website stimmen – das ist die Hauptquelle der Fehlanrufe.'),
     ('Google Search Console', 'Zugang oder Einladung an uns, damit wir die neue Seite anmelden und die Sitemap einreichen.'),
     ('Rechtstexte', 'Impressum und Datenschutz final von TKL (bzw. Datenschutzbeauftragtem) freigeben lassen.'),
     ('Zugänge Verwaltung', 'Wer bei TKL soll ins Backend (Name + E-Mail)? Jede Person bekommt einen eigenen Login.'),
     ('Alte Domain tk-landschaftsbau.de', 'Wird sie noch genutzt (alte E-Mail-Adressen)? Falls ja: Weiterleitung auf tkl.gmbh einrichten.'),
    ]
    li = lambda arr, nr=True: ''.join(f'<li><b>{t}</b><span>{x}</span>{f"<em>{w}</em>" if len(e) and (w := e[0]) else ""}</li>' for t, x, *e in arr)
    inhalt = f'''<section class="seitenkopf"><div class="wrap"><span class="eyebrow">Intern · Greenfield Digital · Stand 05.10.2026</span><h1>TKL-Website: Abstimmung</h1><p class="lead">Arbeitsstand für Janni und Steffi. Diese Seite ist nicht verlinkt und nicht in Suchmaschinen.</p>
<div class="btn-reihe"><a class="btn dunkel klein" href="/">Website ansehen</a><a class="btn rand klein" href="/verwaltung/">Verwaltung (Login)</a></div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><h2 style="font-size:1.8rem">1. Logo – Neuinterpretation</h2><div class="grid-3" style="margin-top:20px">
<div class="box"><span class="eyebrow">Bisher</span><div style="height:180px;display:grid;place-items:center"><img src="/assets/img/logo-alt.png" alt="Bisheriges TKL-Logo" width="140" height="140"></div><h3>Original</h3><p class="muted">Gemalter Pinselrahmen, roter Kreis, grüner Balken, blaues Dreieck. Steht auf rund 25 Fahrzeugen, Kleidung und Wänden.</p></div>
<div class="box"><span class="eyebrow">Entwurf A · auf der Website</span><div style="height:180px;display:grid;place-items:center"><div style="width:140px">{logo_mark()}</div></div><h3>Nah am Original</h3><p class="muted">Gleiche Bausteine, gleiche Anordnung – als saubere Vektorgrafik, kräftiger und auch klein gut lesbar. Passt neben die bestehende Beklebung, Umstellung nach und nach möglich.</p></div>
<div class="box"><span class="eyebrow">Entwurf B · weiter weg</span><div style="height:180px;display:grid;place-items:center"><div style="width:140px">{b}</div></div><h3>Modernes Zeichen</h3><p class="muted">Nur die drei Farbformen als Zeichen. Sehr modern, aber ein deutlicher Bruch – eher für einen späteren kompletten Marken-Relaunch.</p></div>
</div><div class="grid-2" style="margin-top:18px"><div class="box">{marke()}</div><div class="box" style="background:var(--ink)">{marke(hell=True)}</div></div></div></section>
<section class="sec bg-weiss"><div class="wrap schmal"><h2 style="font-size:1.8rem">2. Bitte mit TKL klären</h2><p class="muted">Diese Angaben stehen so auf der Seite oder fehlen bewusst, bis TKL sie bestätigt.</p><ol class="intern-liste">{li(klaeren)}</ol></div></section>
<section class="sec"><div class="wrap schmal"><h2 style="font-size:1.8rem">3. Umzug auf tkl.gmbh – was wir von TKL brauchen</h2><ol class="intern-liste">{li(umzug)}</ol>
<h2 style="font-size:1.8rem;margin-top:50px">4. Technik in Kürze</h2><ul class="haken"><li>Website: statisch, gehostet auf GitHub Pages (Repo frdlnk-gc/tkl-website), schnell und wartungsarm</li><li>Formulare + Verwaltung: Supabase (EU), eigener Login, Daten getrennt von GreenCareers</li><li>Besucherzahlen ohne Cookies – kein Cookie-Banner nötig</li><li>Schriften lokal eingebunden (kein Google-Fonts-Abruf)</li><li>Bilder: Drive-Material vom Dreh 30.09.; Winterdienst, Spielplätze, Baumpflege und Neubau als gekennzeichnete Illustrationen, bis eigene Fotos da sind</li></ul></div></section>'''
    extra = '<style>.intern-liste{{display:grid;gap:12px;padding:0;margin:24px 0 0;list-style:none;counter-reset:n}}.intern-liste li{{counter-increment:n;background:#fff;border-radius:16px;box-shadow:var(--shadow);padding:18px 20px 18px 66px;position:relative}}.intern-liste li::before{{content:counter(n);position:absolute;left:18px;top:16px;width:32px;height:32px;border-radius:50%;background:var(--ink);color:#fff;display:grid;place-items:center;font:800 .95rem var(--font-d)}}.intern-liste b{{display:block;margin-bottom:4px}}.intern-liste span{{color:var(--ink-2);font-size:.96rem}}.intern-liste em{{display:inline-block;margin-top:8px;font-style:normal;font-size:.78rem;font-weight:650;background:var(--paper);border-radius:999px;padding:3px 10px}}</style>'.replace('{{', '{').replace('}}', '}')
    schreibe('/intern/', seite('/intern/', 'Abstimmung (intern) | TKL', 'Interner Arbeitsstand.', inhalt, extra_head=extra, body_attr=' data-kein-tracking'))
