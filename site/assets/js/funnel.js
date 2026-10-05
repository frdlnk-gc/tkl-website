/* TKL – mehrstufige Formulare (Kundenanfrage + Bewerbung) */
(function () {
  document.querySelectorAll('.funnel').forEach(function (box) {
    var form = box.querySelector('form');
    var schritte = [].slice.call(form.querySelectorAll('.schritt-f'));
    var balken = box.querySelector('.fortschritt i');
    var zaehler = box.querySelector('[data-zaehler]');
    var zurueck = form.querySelector('.zurueck');
    var weiter = form.querySelector('[data-weiter]');
    var absenden = form.querySelector('[data-absenden]');
    var fehler = form.querySelector('.f-fehler');
    var danke = box.querySelector('.danke');
    var i = 0, start = 0, gestartet = false;
    var du = form.dataset.anrede === 'du';
    var T = du ? { wahl: 'Bitte wähle eine Option.', felder: 'Bitte prüf die markierten Felder.', kontakt: 'Bitte gib Telefon oder E-Mail an, damit wir uns melden können.', ds: 'Bitte stimm der Datenschutzerklärung zu.', alt: ' Du erreichst uns auch unter 02065 90 36-0.' }
                : { wahl: 'Bitte wählen Sie eine Option.', felder: 'Bitte die markierten Felder prüfen.', kontakt: 'Bitte Telefon oder E-Mail angeben, damit wir uns melden können.', ds: 'Bitte der Datenschutzerklärung zustimmen.', alt: ' Alternativ erreichen Sie uns unter 02065 90 36-0.' };

    function zeige(n) {
      i = Math.max(0, Math.min(n, schritte.length - 1));
      schritte.forEach(function (s, k) { s.classList.toggle('aktiv', k === i); });
      if (balken) balken.style.width = Math.round((i + 1) / schritte.length * 100) + '%';
      if (zaehler) zaehler.textContent = 'Schritt ' + (i + 1) + ' von ' + schritte.length;
      zurueck.hidden = i === 0;
      var letzter = i === schritte.length - 1;
      weiter.hidden = letzter; absenden.hidden = !letzter;
      var auto = schritte[i].dataset.auto === 'ja';
      weiter.style.display = (auto && !letzter) ? 'none' : '';
      fehler.textContent = '';
    }
    function fokusOben() {
      var top = box.getBoundingClientRect().top;
      if (top < 0 || top > window.innerHeight * .5) window.scrollTo({ top: window.scrollY + top - 90, behavior: 'smooth' });
      var erstes = schritte[i].querySelector('input:not([type=hidden]), textarea');
      if (erstes && erstes.type !== 'radio' && erstes.type !== 'checkbox' && window.matchMedia('(min-width: 981px)').matches) setTimeout(function () { erstes.focus({ preventScroll: true }); }, 350);
    }
    function pruefe() {
      var s = schritte[i];
      var gruppen = {};
      s.querySelectorAll('input[type=radio][required], input[type=checkbox][data-min]').forEach(function (el) { gruppen[el.name] = el; });
      for (var n in gruppen) {
        if (!s.querySelector('input[name="' + n + '"]:checked')) { fehler.textContent = s.dataset.hinweis || T.wahl; return false; }
      }
      var ok = true;
      s.querySelectorAll('.feld input, .feld textarea').forEach(function (el) {
        var f = el.closest('.feld'); f.classList.remove('fehler');
        if ((el.required && !el.value.trim()) || (el.type === 'email' && el.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(el.value))) { f.classList.add('fehler'); ok = false; }
      });
      if (!ok) { fehler.textContent = T.felder; return false; }
      var tel = s.querySelector('[name=telefon]'), mail = s.querySelector('[name=email]');
      if (tel && mail && !tel.value.trim() && !mail.value.trim()) { fehler.textContent = T.kontakt; return false; }
      var ds = s.querySelector('[name=datenschutz]');
      if (ds && !ds.checked) { fehler.textContent = T.ds; return false; }
      return true;
    }
    function starte() {
      if (gestartet) return; gestartet = true; start = Date.now();
      if (window.tklTrack) window.tklTrack('funnel_start');
    }
    form.addEventListener('change', function (e) {
      starte();
      if (e.target.type === 'radio' && schritte[i].dataset.auto === 'ja') {
        setTimeout(function () { if (pruefe()) { zeige(i + 1); fokusOben(); } }, 260);
      }
    });
    form.addEventListener('input', starte);
    weiter.addEventListener('click', function () { if (pruefe()) { zeige(i + 1); fokusOben(); } });
    zurueck.addEventListener('click', function () { zeige(i - 1); fokusOben(); });
    form.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && e.target.tagName === 'INPUT' && e.target.type !== 'checkbox') { e.preventDefault(); if (i < schritte.length - 1) weiter.click(); else absenden.click(); }
    });

    // Vorauswahl über URL (?leistung=winterdienst, ?stelle=gruenpflege) oder Buttons mit data-vorauswahl
    function vorauswahl(name, wert, springen) {
      var el = form.querySelector('input[name="' + name + '"][value="' + wert + '"]');
      if (!el) return;
      el.checked = true;
      if (springen) { var k = schritte.indexOf(el.closest('.schritt-f')); if (k === i) zeige(k + 1); }
    }
    var p = new URLSearchParams(location.search);
    form.querySelectorAll('input[data-param]').forEach(function (el) {
      var v = p.get(el.dataset.param); if (v && el.value === v) { el.checked = true; }
    });
    document.querySelectorAll('[data-vorauswahl]').forEach(function (b) {
      b.addEventListener('click', function (e) {
        var teile = b.dataset.vorauswahl.split('=');
        if (!form.querySelector('input[name="' + teile[0] + '"][value="' + teile[1] + '"]')) return;
        e.preventDefault();
        zeige(0); vorauswahl(teile[0], teile[1], true); starte();
        window.scrollTo({ top: box.getBoundingClientRect().top + window.scrollY - 90, behavior: 'smooth' });
      });
    });

    absenden.addEventListener('click', function () {
      if (!pruefe()) return;
      var fd = new FormData(form), daten = {}, felder = ['name', 'firma', 'email', 'telefon', 'ort', 'nachricht', 'website'];
      var payload = { typ: form.dataset.typ, quelle: location.pathname.replace(/^\/tkl-website(?=\/)/, ''), dauer: start ? Date.now() - start : 0, datenschutz: !!form.querySelector('[name=datenschutz]:checked') };
      form.querySelectorAll('.schritt-f').forEach(function (s) {
        s.querySelectorAll('input[type=radio]:checked, input[type=checkbox]:checked').forEach(function (el) {
          if (el.name === 'datenschutz') return;
          var lbl = el.dataset.label || el.value;
          if (el.type === 'checkbox') (daten[el.name] = daten[el.name] || []).push(lbl); else daten[el.name] = lbl;
        });
      });
      felder.forEach(function (f) { if (fd.get(f)) payload[f] = String(fd.get(f)); });
      if (fd.get('plz')) payload.ort = (fd.get('plz') + ' ' + (payload.ort || '')).trim();
      payload.daten = daten;
      var utm = {}; ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'gclid', 'fbclid'].forEach(function (k) { if (p.get(k)) utm[k] = p.get(k).slice(0, 120); });
      if (Object.keys(utm).length) payload.utm = utm;
      absenden.disabled = true; var alt = absenden.innerHTML; absenden.innerHTML = 'Wird gesendet …';
      fetch(window.TKL_API + '/lead', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(payload) })
        .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (res) {
          if (!res.ok) throw new Error(res.j && res.j.fehler || 'Fehler');
          form.style.display = 'none'; var fk = box.querySelector('.fortschritt'); if (fk) fk.style.display = 'none';
          if (zaehler) zaehler.textContent = 'Gesendet';
          var vname = danke.querySelector('[data-vorname]'); if (vname) vname.textContent = String(payload.name).split(' ')[0];
          danke.classList.add('aktiv');
          window.scrollTo({ top: box.getBoundingClientRect().top + window.scrollY - 100, behavior: 'smooth' });
        })
        .catch(function (err) {
          fehler.textContent = (err && err.message && err.message !== 'Failed to fetch' ? err.message : 'Senden hat nicht geklappt.') + T.alt;
          absenden.disabled = false; absenden.innerHTML = alt;
        });
    });
    zeige(0);
  });
})();
