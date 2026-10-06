/* TKL – Navigation, Animationen, Besucherstatistik (ohne Cookies) */
(function () {
  var API = 'https://ildagygshaiaiqghjouj.supabase.co/functions/v1/tkl-api';
  window.TKL_API = API;
  var body = document.body;
  if (/[?&]statisch/.test(location.search)) document.documentElement.classList.add('statisch');

  // Kopfzeile beim Scrollen
  var kopf = document.querySelector('.kopf');
  var mcta = document.querySelector('.mobil-cta');
  var funnelSichtbar = false;
  if ('IntersectionObserver' in window) document.querySelectorAll('.funnel, .cta-hecke, .fuss').forEach(function (f) {
    new IntersectionObserver(function (es) { es.forEach(function (e) { f._sicht = e.isIntersecting; }); funnelSichtbar = [].some.call(document.querySelectorAll('.funnel, .cta-hecke, .fuss'), function (x) { return x._sicht; }); onScroll(); }, { threshold: 0 }).observe(f);
  });
  function onScroll() {
    var y = window.scrollY;
    if (kopf) kopf.classList.toggle('gescrollt', y > 8);
    if (mcta) mcta.classList.toggle('sichtbar', y > 520 && !funnelSichtbar);
  }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // Mobiles Menü
  var burger = document.querySelector('.burger');
  if (burger) burger.addEventListener('click', function () {
    var offen = body.classList.toggle('nav-offen');
    burger.setAttribute('aria-expanded', offen ? 'true' : 'false');
  });
  document.querySelectorAll('.mobil-nav a').forEach(function (a) {
    a.addEventListener('click', function () { body.classList.remove('nav-offen'); if (burger) burger.setAttribute('aria-expanded', 'false'); });
  });
  window.matchMedia('(min-width: 981px)').addEventListener('change', function (e) { if (e.matches) body.classList.remove('nav-offen'); });

  // Dropdown Leistungen
  document.querySelectorAll('.nav-drop').forEach(function (d) {
    var b = d.querySelector('button'); var t;
    function auf() { clearTimeout(t); d.classList.add('offen'); b.setAttribute('aria-expanded', 'true'); }
    function zu() { t = setTimeout(function () { d.classList.remove('offen'); b.setAttribute('aria-expanded', 'false'); }, 160); }
    d.addEventListener('mouseenter', auf); d.addEventListener('mouseleave', zu);
    b.addEventListener('click', function () { d.classList.contains('offen') ? zu() : auf(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { d.classList.remove('offen'); } });
  });

  // Einblenden beim Scrollen
  var rv = document.querySelectorAll('.rv, .pinsel');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: .08 });
    rv.forEach(function (el) { io.observe(el); });
  } else rv.forEach(function (el) { el.classList.add('in'); });

  // Zahlen hochzählen
  var zahlen = document.querySelectorAll('[data-zahl]');
  if ('IntersectionObserver' in window && zahlen.length && !document.documentElement.classList.contains('statisch') && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var zio = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return; zio.unobserve(e.target);
        var el = e.target, ziel = parseInt(el.dataset.zahl, 10), t0 = performance.now(), d = 1300;
        (function tick(t) { var p = Math.min(1, (t - t0) / d); el.textContent = Math.round(ziel * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(tick); })(t0);
      });
    }, { threshold: .6 });
    zahlen.forEach(function (z) { zio.observe(z); });
  }

  // Tabs (Zielgruppen)
  document.querySelectorAll('[role="tablist"]').forEach(function (liste) {
    var tabs = liste.querySelectorAll('[role="tab"]');
    tabs.forEach(function (tab, i) {
      tab.addEventListener('click', function () { waehle(i); });
      tab.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); var n = (i + (e.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length; waehle(n); tabs[n].focus(); }
      });
    });
    function waehle(i) {
      tabs.forEach(function (t, k) {
        t.setAttribute('aria-selected', k === i ? 'true' : 'false'); t.tabIndex = k === i ? 0 : -1;
        var p = document.getElementById(t.getAttribute('aria-controls')); if (p) p.hidden = k !== i;
      });
    }
  });

  // Videos nur abspielen, wenn sichtbar
  document.querySelectorAll('video[data-auto]').forEach(function (v) {
    if (!('IntersectionObserver' in window)) return;
    new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { if (v.preload === 'none') { v.preload = 'auto'; } v.play().catch(function () {}); } else v.pause();
      });
    }, { threshold: .25 }).observe(v);
  });

  // Besucherstatistik: kein Cookie, kein Speicher – Zählung serverseitig anonym
  var params = new URLSearchParams(location.search);
  function quelle() {
    if (params.get('utm_source')) return params.get('utm_source').toLowerCase().slice(0, 40);
    if (params.get('gclid')) return 'google-ads';
    if (params.get('fbclid')) return 'facebook';
    var r = document.referrer;
    if (!r) return 'direkt';
    try { var h = new URL(r).hostname.replace(/^www\./, ''); if (h === location.hostname) return null;
      if (/google\./.test(h)) return 'google'; if (/bing\./.test(h)) return 'bing'; if (/instagram/.test(h)) return 'instagram';
      if (/facebook|fb\./.test(h)) return 'facebook'; if (/linkedin/.test(h)) return 'linkedin'; return h.slice(0, 40); } catch (e) { return null; }
  }
  window.tklTrack = function (typ) {
    if (/^(localhost|127\.)/.test(location.hostname) && !params.has('track')) return;
    var d = JSON.stringify({ typ: typ || 'view', pfad: location.pathname.replace(/^\/tkl-website(?=\/)/, ''), ref: document.referrer ? document.referrer.slice(0, 200) : null, quelle: quelle() });
    try { fetch(API + '/track', { method: 'POST', body: d, headers: { 'content-type': 'application/json' }, keepalive: true, mode: 'cors' }).catch(function () {}); } catch (e) {}
  };
  if (!body.hasAttribute('data-kein-tracking')) window.tklTrack('view');
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href^="tel:"], a[href^="mailto:"]');
    if (a) window.tklTrack('cta');
  });


  // Sticker schweben beim Scrollen leicht mit
  var par = [].slice.call(document.querySelectorAll('[data-parallax]'));
  if (par.length && !matchMedia('(prefers-reduced-motion: reduce)').matches && !document.documentElement.classList.contains('statisch')) {
    var tick = false;
    var bewege = function () { tick = false; par.forEach(function (el) { var r = el.getBoundingClientRect(); var mitte = r.top + r.height / 2 - innerHeight / 2; el.style.translate = '0 ' + (mitte * parseFloat(el.dataset.parallax)).toFixed(1) + 'px'; }); };
    window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(bewege); } }, { passive: true }); bewege();
  }

  // Jahreskalender: aktuellen Monat hervorheben und Text setzen
  var kal = document.querySelector('[data-kalender]');
  if (kal) {
    var m = new Date().getMonth();
    kal.querySelectorAll('[data-m="' + m + '"]').forEach(function (z) { z.classList.add('jetzt'); });
    var texte = JSON.parse(kal.dataset.kalender);
    var ziel = kal.querySelector('[data-jetzt-text]'); if (ziel) ziel.textContent = texte[m];
    var mn = kal.querySelector('[data-jetzt-monat]'); if (mn) mn.textContent = ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'][m];
  }

  // Rückruf-Box
  var rr = document.querySelector('.rueckruf');
  if (rr) {
    var auf = function (o) { rr.classList.toggle('offen', o); rr.querySelector('.rueckruf-knopf').setAttribute('aria-expanded', o ? 'true' : 'false'); if (o) { setTimeout(function () { var i = rr.querySelector('input[name=name]'); if (i) i.focus(); }, 250); if (window.tklTrack) window.tklTrack('cta'); } };
    rr.querySelector('.rueckruf-knopf').addEventListener('click', function () { auf(!rr.classList.contains('offen')); });
    rr.querySelector('.rueckruf-zu').addEventListener('click', function () { auf(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') auf(false); });
    var f = rr.querySelector('form'), t0 = Date.now();
    f.addEventListener('submit', function (e) {
      e.preventDefault(); var msg = f.querySelector('.f-fehler'); msg.textContent = '';
      var du = f.dataset.anrede === 'du';
      if (!f.name.value.trim()) { msg.textContent = du ? 'Bitte gib deinen Namen an.' : 'Bitte geben Sie Ihren Namen an.'; return; }
      if (f.telefon.value.replace(/\D/g, '').length < 6) { msg.textContent = du ? 'Bitte gib eine Telefonnummer an, damit wir zurückrufen können.' : 'Bitte geben Sie eine Telefonnummer an, damit wir zurückrufen können.'; return; }
      if (f.email.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.email.value)) { msg.textContent = 'Bitte E-Mail-Adresse prüfen.'; return; }
      if (!f.datenschutz.checked) { msg.textContent = du ? 'Bitte stimm der Datenschutzerklärung zu.' : 'Bitte der Datenschutzerklärung zustimmen.'; return; }
      var b = f.querySelector('button'); b.disabled = true; b.textContent = 'Wird gesendet …';
      var text = f.nachricht.value.trim();
      fetch(API + '/lead', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ typ: f.dataset.typ, name: f.name.value, firma: f.firma ? f.firma.value : '', telefon: f.telefon.value, email: f.email.value, datenschutz: true, dauer: Date.now() - t0, website: f.website.value, quelle: location.pathname.replace(/^\/tkl-website(?=\/)/, ''), nachricht: 'Rückruf gewünscht' + (text ? ': ' + text : ''), daten: { rueckruf: 'Ja' } }) })
        .then(function (r) { return r.json().then(function (j) { if (!r.ok) throw new Error(j.fehler); }); })
        .then(function () { f.outerHTML = '<div class="rueckruf-danke"><b>Danke' + (du ? '!' : ' für Ihre Anfrage!') + '</b><br>' + (du ? 'Wir rufen dich innerhalb von 24 bis 48 Stunden zurück.' : 'Wir rufen Sie innerhalb von 24 bis 48 Stunden zurück.') + '</div>'; })
        .catch(function (err) { msg.textContent = err.message || 'Hat nicht geklappt – bitte rufen Sie uns an.'; b.disabled = false; b.textContent = 'Rückruf anfordern'; });
    });
  }


  // Stimmen: Vorschau beim Überfahren, Klick öffnet Player mit Ton + Untertiteln
  var basis = (location.pathname.match(/^\/tkl-website(?=\/)/) || [''])[0];
  document.querySelectorAll('.stimme[data-video]').forEach(function (k) {
    var src = basis + '/assets/video/' + k.dataset.video;
    if (matchMedia('(hover: hover)').matches) {
      var v;
      k.addEventListener('mouseenter', function () {
        if (!v) { v = document.createElement('video'); v.muted = true; v.loop = true; v.playsInline = true; v.preload = 'auto'; v.src = src + '.mp4'; v.setAttribute('aria-hidden', 'true'); k.insertBefore(v, k.querySelector('.stimme-text')); }
        v.currentTime = 0; v.play().catch(function () {});
      });
      k.addEventListener('mouseleave', function () { if (v) v.pause(); });
    }
    k.addEventListener('click', function () {
      var d = document.querySelector('.vid-dialog');
      if (!d) { d = document.createElement('dialog'); d.className = 'vid-dialog'; d.innerHTML = '<button class="vid-zu" type="button" aria-label="Video schließen">×</button><video controls playsinline preload="auto" crossorigin="anonymous"></video><p class="vid-titel"></p>'; document.body.appendChild(d);
        d.querySelector('.vid-zu').addEventListener('click', function () { d.close(); });
        d.addEventListener('click', function (e) { if (e.target === d) d.close(); });
        d.addEventListener('close', function () { d.querySelector('video').pause(); }); }
      var vid = d.querySelector('video');
      vid.innerHTML = '<source src="' + src + '.mp4" type="video/mp4"><track kind="subtitles" srclang="de" label="Deutsch" src="' + src + '.vtt" default>';
      vid.poster = src + '-poster.webp'; vid.load();
      d.querySelector('.vid-titel').innerHTML = '<b>' + (k.dataset.titel || '') + '</b>' + (k.dataset.untertitel || '');
      d.showModal(); vid.play().catch(function () {});
      if (vid.textTracks[0]) vid.textTracks[0].mode = 'showing';
      if (window.tklTrack) window.tklTrack('cta');
    });
  });

  // Jahr im Footer
  document.querySelectorAll('[data-jahr]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
