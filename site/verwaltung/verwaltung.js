/* TKL Verwaltung – Anmeldung, Kennzahlen, Anfragen und Bewerbungen */
(function () {
  var API = 'https://ildagygshaiaiqghjouj.supabase.co/functions/v1/tkl-api';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var token = null, name = '';
  try { token = sessionStorage.getItem('tkl_token'); name = sessionStorage.getItem('tkl_name') || ''; } catch (e) {}
  var cache = { anfrage: null, bewerbung: null }, ansicht = 'uebersicht', tage = 30, aktuell = null;

  var STATUS = {
    anfrage: [['neu', 'Neu'], ['kontaktiert', 'Kontaktiert'], ['termin', 'Termin vor Ort'], ['angebot', 'Angebot raus'], ['gewonnen', 'Auftrag'], ['abgesagt', 'Kein Auftrag'], ['archiviert', 'Archiviert']],
    bewerbung: [['neu', 'Neu'], ['kontaktiert', 'Kontaktiert'], ['termin', 'Gespräch vereinbart'], ['eingestellt', 'Eingestellt'], ['abgesagt', 'Abgesagt'], ['archiviert', 'Archiviert']]
  };
  var FELD = { leistungen: 'Leistungen', objekt: 'Objekt', umfang: 'Anzahl Objekte', start: 'Start', rueckruf: 'Rückruf gewünscht', zeit: 'Wunschzeit', stelle: 'Stelle', erfahrung: 'Erfahrung', fuehrerschein: 'Führerschein', arbeitszeit: 'Arbeitszeit' };
  var SEITE = { '/': 'Startseite', '/leistungen/': 'Leistungen', '/leistungen/gruenpflege/': 'Grünpflege', '/leistungen/winterdienst/': 'Winterdienst', '/leistungen/spielplaetze/': 'Spielplätze', '/leistungen/baumpflege/': 'Baumpflege', '/leistungen/aussenanlagen/': 'Neubau & Sanierung', '/karriere/': 'Karriere', '/kontakt/': 'Kontakt', '/ueber-uns/': 'Über uns', '/impressum/': 'Impressum', '/datenschutz/': 'Datenschutz' };

  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function datum(iso, mitZeit) {
    var d = new Date(iso), h = new Date(), gestern = new Date(h - 864e5);
    var z = d.toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' });
    if (d.toDateString() === h.toDateString()) return 'Heute, ' + z;
    if (d.toDateString() === gestern.toDateString()) return 'Gestern, ' + z;
    return d.toLocaleDateString('de-DE', { day: '2-digit', month: '2-digit', year: 'numeric' }) + (mitZeit ? ', ' + z : '');
  }
  function toast(t) { var el = $('.vw-toast') || document.body.appendChild(Object.assign(document.createElement('div'), { className: 'vw-toast' })); el.textContent = t; el.classList.add('zeigen'); clearTimeout(el._t); el._t = setTimeout(function () { el.classList.remove('zeigen'); }, 2400); }

  function api(pfad, opt) {
    opt = opt || {}; opt.headers = Object.assign({ 'content-type': 'application/json' }, opt.headers || {});
    if (token) opt.headers.authorization = 'Bearer ' + token;
    return fetch(API + pfad, opt).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) {
        if (r.status === 401 && pfad !== '/login') { abmelden(); throw new Error('Sitzung abgelaufen – bitte neu anmelden.'); }
        if (!r.ok) throw new Error(j.fehler || 'Fehler ' + r.status);
        return j;
      });
    });
  }

  // ---------- Anmeldung ----------
  function zeigeLogin() { $('#app').hidden = true; $('#login').hidden = false; setTimeout(function () { $('#l-mail').focus(); }, 50); }
  function zeigeApp() { $('#login').hidden = true; $('#app').hidden = false; $('#nutzer-name').textContent = name; wechsle(location.hash.replace('#', '') || 'uebersicht'); }
  function abmelden() { token = null; try { sessionStorage.removeItem('tkl_token'); } catch (e) {} zeigeLogin(); }
  $('#login-form').addEventListener('submit', function (e) {
    e.preventDefault(); var f = e.target, fehl = $('#login-fehler'); fehl.textContent = '';
    var b = f.querySelector('button'); b.disabled = true; b.textContent = 'Wird geprüft …';
    api('/login', { method: 'POST', body: JSON.stringify({ email: f.email.value.trim(), passwort: f.passwort.value }) })
      .then(function (j) { token = j.token; name = j.name; try { sessionStorage.setItem('tkl_token', token); sessionStorage.setItem('tkl_name', name); } catch (e) {} f.passwort.value = ''; zeigeApp(); })
      .catch(function (err) { fehl.textContent = err.message; })
      .finally(function () { b.disabled = false; b.textContent = 'Anmelden'; });
  });
  $('#abmelden').addEventListener('click', abmelden);

  // ---------- Navigation ----------
  function wechsle(z) {
    if (['uebersicht', 'anfrage', 'bewerbung'].indexOf(z) < 0) z = 'uebersicht';
    ansicht = z; history.replaceState(null, '', '#' + z);
    $$('.vw-nav button').forEach(function (b) { b.classList.toggle('aktiv', b.dataset.ansicht === z); });
    $('[data-bereich="uebersicht"]').hidden = z !== 'uebersicht';
    $('[data-bereich="liste"]').hidden = z === 'uebersicht';
    if (z === 'uebersicht') ladeUebersicht(); else ladeListe(z);
    window.scrollTo(0, 0);
  }
  $$('.vw-nav button').forEach(function (b) { b.addEventListener('click', function () { wechsle(b.dataset.ansicht); }); });
  $$('.vw-segment button').forEach(function (b) {
    b.addEventListener('click', function () { tage = +b.dataset.tage; $$('.vw-segment button').forEach(function (x) { x.classList.toggle('aktiv', x === b); }); ladeUebersicht(); });
  });

  function ladeBeide() {
    return Promise.all([api('/leads?typ=anfrage'), api('/leads?typ=bewerbung')]).then(function (r) {
      cache.anfrage = r[0]; cache.bewerbung = r[1]; badges(); return r;
    });
  }
  function badges() {
    ['anfrage', 'bewerbung'].forEach(function (t) { var n = (cache[t] || []).filter(function (l) { return l.status === 'neu'; }).length; $('#badge-' + t).textContent = n || ''; });
    var demo = (cache.anfrage || []).concat(cache.bewerbung || []).some(function (l) { return l.demo; });
    $('#demo-hinweis').hidden = !demo && !(window._stats && window._stats.demo);
  }

  // ---------- Übersicht ----------
  function ladeUebersicht() {
    $('#zeitraum-text').textContent = 'Letzte ' + tage + ' Tage';
    Promise.all([api('/stats?tage=' + tage), ladeBeide()]).then(function (r) {
      var s = r[0]; window._stats = s; badges();
      $('#k-besucher').textContent = s.besucher.toLocaleString('de-DE');
      $('#k-aufrufe').textContent = s.aufrufe.toLocaleString('de-DE') + ' Seitenaufrufe';
      $('#k-anfragen').textContent = s.anfragen; $('#k-bewerbungen').textContent = s.bewerbungen; $('#k-offen').textContent = s.offen;
      var q = function (n) { return s.besucher ? (n / s.besucher * 100).toLocaleString('de-DE', { maximumFractionDigits: 1 }) + ' % der Besucher' : ''; };
      $('#k-quote-a').textContent = q(s.anfragen); $('#k-quote-b').textContent = q(s.bewerbungen);
      diagramm(s.verlauf);
      balken('#seiten', s.seiten.map(function (x) { return [SEITE[x.pfad] || x.pfad, x.aufrufe]; }));
      balken('#quellen', s.quellen.map(function (x) { return [x.quelle.charAt(0).toUpperCase() + x.quelle.slice(1), x.besucher]; }));
      var g = s.geraete || {}, sum = Object.values(g).reduce(function (a, b) { return a + b; }, 0) || 1;
      $('#geraete').innerHTML = ['mobil', 'desktop'].map(function (k) { return '<div><b>' + Math.round((g[k] || 0) / sum * 100) + ' %</b>' + (k === 'mobil' ? 'Smartphone' : 'Computer') + '</div>'; }).join('');
      var neu = (cache.anfrage || []).concat(cache.bewerbung || []).sort(function (a, b) { return b.created_at < a.created_at ? -1 : 1; }).slice(0, 5);
      $('#neueste').innerHTML = neu.length ? neu.map(zeile).join('') : '<div class="vw-leer">Noch keine Eingänge.</div>';
      bindeZeilen($('#neueste'));
    }).catch(function (e) { toast(e.message); });
  }
  function balken(sel, daten) {
    var max = Math.max.apply(null, daten.map(function (d) { return d[1]; }).concat([1]));
    $(sel).innerHTML = daten.length ? daten.map(function (d) { return '<li><i style="width:' + (d[1] / max * 100) + '%"></i><span>' + esc(d[0]) + '</span><b>' + d[1] + '</b></li>'; }).join('') : '<li><span class="muted">Noch keine Daten</span></li>';
  }
  function diagramm(v) {
    var el = $('#diagramm'), W = el.clientWidth || 800, H = 240, p = { l: 34, r: 8, t: 10, b: 26 };
    var n = v.length, bw = (W - p.l - p.r) / n;
    var maxB = Math.max.apply(null, v.map(function (d) { return d.besucher; }).concat([5]));
    var maxL = Math.max.apply(null, v.map(function (d) { return d.anfragen + d.bewerbungen; }).concat([3]));
    var y = function (val, m) { return H - p.b - (val / m) * (H - p.t - p.b); };
    var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" preserveAspectRatio="none">';
    for (var k = 0; k <= 4; k++) { var gy = p.t + k * (H - p.t - p.b) / 4; s += '<line x1="' + p.l + '" x2="' + (W - p.r) + '" y1="' + gy + '" y2="' + gy + '" stroke="#ece8df" stroke-width="1"/><text x="0" y="' + (gy + 4) + '">' + Math.round(maxB * (1 - k / 4)) + '</text>'; }
    v.forEach(function (d, i) {
      var x = p.l + i * bw, h = (H - p.b) - y(d.besucher, maxB);
      s += '<rect x="' + (x + bw * .14) + '" y="' + y(d.besucher, maxB) + '" width="' + Math.max(1, bw * .72) + '" height="' + Math.max(0, h) + '" rx="3" fill="#b9d4ee" stroke="none"><title>' + new Date(d.tag).toLocaleDateString('de-DE') + ': ' + d.besucher + ' Besucher, ' + d.anfragen + ' Anfragen, ' + d.bewerbungen + ' Bewerbungen</title></rect>';
      var cy = H - p.b - 8;
      for (var a = 0; a < d.anfragen; a++) s += '<circle cx="' + (x + bw / 2) + '" cy="' + (cy - a * 9) + '" r="3.6" fill="#1e9e4a" stroke="#fff" stroke-width="1.5"/>';
      for (var b = 0; b < d.bewerbungen; b++) s += '<circle cx="' + (x + bw / 2) + '" cy="' + (cy - (d.anfragen + b) * 9) + '" r="3.6" fill="#d8231c" stroke="#fff" stroke-width="1.5"/>';
      var schritt = Math.ceil(n / 8);
      if (i % schritt === 0) s += '<text x="' + (x + bw / 2) + '" y="' + (H - 6) + '" text-anchor="middle">' + new Date(d.tag).toLocaleDateString('de-DE', { day: '2-digit', month: '2-digit' }) + '</text>';
    });
    el.innerHTML = s + '</svg>';
  }
  window.addEventListener('resize', function () { if (window._stats && ansicht === 'uebersicht') diagramm(window._stats.verlauf); });

  // ---------- Listen ----------
  function statusLabel(typ, st) { var f = (STATUS[typ] || []).filter(function (x) { return x[0] === st; })[0]; return f ? f[1] : st; }
  function zeile(l) {
    var d = l.daten || {}, chips = [];
    if (l.typ === 'anfrage') { (Array.isArray(d.leistungen) ? d.leistungen : []).forEach(function (x) { chips.push(x); }); if (d.objekt) chips.push(d.objekt); }
    else { if (d.stelle) chips.push(d.stelle); if (d.fuehrerschein) chips.push('FS ' + d.fuehrerschein.replace('Klasse ', '')); if (d.erfahrung) chips.push(d.erfahrung); }
    if (d.rueckruf) chips.unshift('Rückruf');
    var initialen = l.name.split(/\s+/).map(function (w) { return w[0]; }).slice(0, 2).join('').toUpperCase();
    var sub = l.typ === 'anfrage' ? [l.firma, l.ort].filter(Boolean).join(' · ') : [l.ort, l.telefon].filter(Boolean).join(' · ');
    return '<button type="button" class="vw-eintrag' + (l.status === 'neu' ? ' neu' : '') + '" data-id="' + l.id + '" data-typ="' + l.typ + '"><span class="vw-ava">' + esc(initialen) + '</span>' +
      '<span><b>' + esc(l.name) + (l.demo ? '<span class="vw-demo-tag">Beispiel</span>' : '') + '</b><span class="sub">' + esc(sub || (l.email || '')) + ' · ' + datum(l.created_at) + '</span></span>' +
      '<span class="vw-chips">' + chips.slice(0, 3).map(function (c) { return '<span class="vw-chip">' + esc(c) + '</span>'; }).join('') + '</span>' +
      '<span class="vw-status s-' + l.status + '">' + esc(statusLabel(l.typ, l.status)) + '</span></button>';
  }
  function bindeZeilen(root) { $$('.vw-eintrag', root).forEach(function (b) { b.addEventListener('click', function () { oeffne(b.dataset.typ, b.dataset.id); }); }); }
  function ladeListe(typ) {
    $('#liste-titel').textContent = typ === 'anfrage' ? 'Kundenanfragen' : 'Bewerbungen';
    var sel = $('#filter-status'); sel.innerHTML = '<option value="">Alle Status</option>' + STATUS[typ].map(function (s) { return '<option value="' + s[0] + '">' + s[1] + '</option>'; }).join('');
    $('#suche').value = '';
    var zeichne = function () { zeigeListe(typ); };
    if (cache[typ]) zeichne();
    ladeBeide().then(zeichne).catch(function (e) { toast(e.message); });
  }
  function gefiltert(typ) {
    var q = $('#suche').value.toLowerCase().trim(), st = $('#filter-status').value;
    return (cache[typ] || []).filter(function (l) {
      if (st && l.status !== st) return false;
      if (st !== 'archiviert' && !st && l.status === 'archiviert') return false;
      if (!q) return true;
      return JSON.stringify([l.name, l.firma, l.email, l.telefon, l.ort, l.nachricht, l.daten]).toLowerCase().indexOf(q) >= 0;
    });
  }
  function zeigeListe(typ) {
    if (ansicht !== typ) return;
    var l = gefiltert(typ), alle = cache[typ] || [];
    $('#liste-info').textContent = alle.length + ' insgesamt · ' + alle.filter(function (x) { return x.status === 'neu'; }).length + ' neu';
    $('#liste').innerHTML = l.length ? l.map(zeile).join('') : '<div class="vw-leer">' + (alle.length ? 'Keine Treffer für diesen Filter.' : (typ === 'anfrage' ? 'Noch keine Kundenanfragen – sie erscheinen hier, sobald jemand das Formular abschickt.' : 'Noch keine Bewerbungen.')) + '</div>';
    bindeZeilen($('#liste'));
  }
  $('#suche').addEventListener('input', function () { zeigeListe(ansicht); });
  $('#filter-status').addEventListener('change', function () { zeigeListe(ansicht); });

  // CSV
  $('#export').addEventListener('click', function () {
    var typ = ansicht, l = gefiltert(typ); if (!l.length) return toast('Keine Einträge zum Exportieren.');
    var keys = typ === 'anfrage' ? ['leistungen', 'objekt', 'umfang', 'start'] : ['stelle', 'erfahrung', 'fuehrerschein', 'start'];
    var kopf = ['Datum', 'Status', 'Name', 'Firma', 'Telefon', 'E-Mail', 'Ort'].concat(keys.map(function (k) { return FELD[k] || k; })).concat(['Nachricht', 'Quelle']);
    var zeilen = l.map(function (x) { var d = x.daten || {}; return [new Date(x.created_at).toLocaleString('de-DE'), statusLabel(typ, x.status), x.name, x.firma, x.telefon, x.email, x.ort].concat(keys.map(function (k) { return Array.isArray(d[k]) ? d[k].join(', ') : d[k]; })).concat([x.nachricht, x.quelle]); });
    var csv = '﻿' + [kopf].concat(zeilen).map(function (r) { return r.map(function (c) { return '"' + String(c == null ? '' : c).replace(/"/g, '""') + '"'; }).join(';'); }).join('\r\n');
    var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }));
    a.download = 'tkl-' + (typ === 'anfrage' ? 'anfragen' : 'bewerbungen') + '-' + new Date().toISOString().slice(0, 10) + '.csv'; a.click();
  });

  // ---------- Detail ----------
  function telNorm(t) { var d = String(t || '').replace(/[^\d+]/g, ''); if (d.indexOf('00') === 0) d = '+' + d.slice(2); else if (d.indexOf('0') === 0) d = '+49' + d.slice(1); return d; }
  function oeffne(typ, id) {
    var l = (cache[typ] || []).filter(function (x) { return x.id === id; })[0]; if (!l) return; aktuell = l;
    var d = l.daten || {}, tel = telNorm(l.telefon), mobil = /^\+491[5-7]/.test(tel);
    var vor = l.name.split(' ')[0];
    var betreff = typ === 'anfrage' ? 'Ihre Anfrage bei TKL' : 'Deine Bewerbung bei TKL';
    var text = typ === 'anfrage' ? 'Guten Tag ' + l.name + ',\n\nvielen Dank für Ihre Anfrage. ' : 'Hallo ' + vor + ',\n\nvielen Dank für deine Bewerbung bei TKL. ';
    var wa = typ === 'anfrage' ? 'Guten Tag ' + l.name + ', hier ist die TKL GmbH. Vielen Dank für Ihre Anfrage!' : 'Hallo ' + vor + ', hier ist TKL. Danke für deine Bewerbung! Wann passt dir ein kurzes Telefonat?';
    var felder = [['Eingang', datum(l.created_at, true)], ['Firma', l.firma], ['Telefon', l.telefon], ['E-Mail', l.email], ['Ort', l.ort]];
    Object.keys(d).forEach(function (k) { felder.push([FELD[k] || k, Array.isArray(d[k]) ? d[k].join(', ') : d[k]]); });
    felder.push(['Gesendet von', SEITE[l.quelle] || l.quelle]);
    if (l.utm && l.utm.utm_source) felder.push(['Kampagne', [l.utm.utm_source, l.utm.utm_campaign].filter(Boolean).join(' / ')]);
    var verlauf = (l.notizen || []).slice().reverse().map(function (n) { return '<li class="' + (n.system ? 'sys' : '') + '"><small>' + esc(n.von || '') + ' · ' + datum(n.t, true) + '</small>' + esc(n.text) + '</li>'; }).join('');
    $('#detail-inhalt').innerHTML =
      '<span class="vw-status s-' + l.status + '">' + esc(statusLabel(typ, l.status)) + '</span>' + (l.demo ? '<span class="vw-demo-tag">Beispiel</span>' : '') +
      '<h2 id="d-name">' + esc(l.name) + '</h2><p class="muted" style="margin:0">' + (typ === 'anfrage' ? 'Kundenanfrage' : 'Bewerbung') + (d.stelle ? ' · ' + esc(d.stelle) : '') + '</p>' +
      '<div class="vw-aktionen">' +
      '<a href="' + (tel ? 'tel:' + tel : '#') + '" class="' + (tel ? '' : 'aus') + '"><svg viewBox="0 0 24 24"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2Z"/></svg>Anrufen</a>' +
      '<a href="' + (l.email ? 'mailto:' + esc(l.email) + '?subject=' + encodeURIComponent(betreff) + '&body=' + encodeURIComponent(text) : '#') + '" class="' + (l.email ? '' : 'aus') + '"><svg viewBox="0 0 24 24"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>E-Mail</a>' +
      '<a href="' + (mobil ? 'https://wa.me/' + tel.replace('+', '') + '?text=' + encodeURIComponent(wa) : '#') + '" target="_blank" rel="noopener" class="' + (mobil ? '' : 'aus') + '"><svg viewBox="0 0 24 24"><path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 21l2.1-5.4A8.5 8.5 0 1 1 21 11.5Z"/></svg>WhatsApp</a></div>' +
      '<dl class="vw-felder">' + felder.filter(function (f) { return f[1]; }).map(function (f) { return '<dt>' + esc(f[0]) + '</dt><dd>' + (f[0] === 'Telefon' && tel ? '<a href="tel:' + tel + '">' + esc(f[1]) + '</a>' : f[0] === 'E-Mail' ? '<a href="mailto:' + esc(f[1]) + '">' + esc(f[1]) + '</a>' : esc(f[1])) + '</dd>'; }).join('') + '</dl>' +
      (l.nachricht ? '<div class="vw-block"><h3>Nachricht</h3><div class="vw-nachricht">' + esc(l.nachricht) + '</div></div>' : '') +
      '<div class="vw-block"><h3>Status</h3><div class="vw-statuswahl">' + STATUS[typ].map(function (s) { return '<button type="button" data-status="' + s[0] + '" class="' + (s[0] === l.status ? 'aktiv' : '') + '">' + s[1] + '</button>'; }).join('') + '</div></div>' +
      '<div class="vw-block vw-notiz"><h3>Notizen</h3><textarea id="notiz" placeholder="z. B. Termin vor Ort am Dienstag, 10 Uhr …"></textarea><button type="button" class="btn klein dunkel" id="notiz-speichern">Notiz speichern</button><ul class="vw-verlauf">' + verlauf + '</ul></div>';
    $$('.vw-statuswahl button').forEach(function (b) { b.addEventListener('click', function () { speichere({ status: b.dataset.status }, 'Status geändert'); }); });
    $('#notiz-speichern').addEventListener('click', function () { var t = $('#notiz').value.trim(); if (!t) return; speichere({ notiz: t }, 'Notiz gespeichert'); });
    var hg = $('#detail-hg'), dt = $('#detail'); hg.hidden = false; requestAnimationFrame(function () { hg.classList.add('offen'); dt.classList.add('offen'); }); dt.setAttribute('aria-hidden', 'false');
    setTimeout(function () { $('#detail-zu').focus(); }, 300);
  }
  function schliesse() { var hg = $('#detail-hg'), dt = $('#detail'); hg.classList.remove('offen'); dt.classList.remove('offen'); dt.setAttribute('aria-hidden', 'true'); setTimeout(function () { hg.hidden = true; }, 300); aktuell = null; }
  $('#detail-zu').addEventListener('click', schliesse); $('#detail-hg').addEventListener('click', schliesse);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && aktuell) schliesse(); });
  function speichere(body, msg) {
    var l = aktuell; if (!l) return;
    api('/leads/' + l.id, { method: 'PATCH', body: JSON.stringify(body) }).then(function (neu) {
      var arr = cache[l.typ]; for (var i = 0; i < arr.length; i++) if (arr[i].id === neu.id) arr[i] = neu;
      toast(msg); badges(); oeffne(l.typ, l.id);
      if (ansicht === 'uebersicht') ladeUebersicht(); else zeigeListe(ansicht);
    }).catch(function (e) { toast(e.message); });
  }

  $('#demo-loeschen').addEventListener('click', function () {
    if (!confirm('Alle Beispieldaten (Einträge und Besucherzahlen) endgültig löschen? Echte Anfragen bleiben erhalten.')) return;
    api('/demo-loeschen', { method: 'POST' }).then(function () { toast('Beispieldaten gelöscht'); window._stats = null; wechsle(ansicht); }).catch(function (e) { toast(e.message); });
  });

  // Start
  if (token) api('/me').then(function (u) { name = u.name; zeigeApp(); }).catch(function () { zeigeLogin(); }); else zeigeLogin();
})();
