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

  // Jahr im Footer
  document.querySelectorAll('[data-jahr]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
