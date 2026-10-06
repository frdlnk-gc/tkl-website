// Prüft, ob Overlays (Blasen, Karten, Sticker, Labels, Text) über erkannten Gesichtern liegen.
window.FACES = {"betriebshof-poster":[[0.244,0.363,0.18,0.127]],"blasgeraet":[[0.457,0.217,0.244,0.09]],"collage-baum":[[0.435,0.408,0.038,0.057],[0.409,0.354,0.094,0.114]],"collage-neubau":[[0.526,0.329,0.112,0.125]],"collage-spielplatz":[[0.528,0.36,0.039,0.059],[0.58,0.364,0.044,0.066],[0.502,0.326,0.071,0.127],[0.605,0.337,0.081,0.125]],"geschaeftsfuehrung":[[0.429,0.309,0.202,0.134],[0.338,0.245,0.393,0.145]],"grischa-km-poster":[[0.515,0.31,0.07,0.039],[0.435,0.266,0.222,0.116],[0.033,0.34,0.05,0.029],[0.182,0.34,0.058,0.029]],"gruenpflege-20000-poster":[[0.367,0.221,0.281,0.158],[0.23,0.166,0.572,0.165]],"gruenpflege-loop-poster":[[0.408,0.305,0.163,0.069]],"hecke-weg":[[0.153,0.372,0.064,0.069]],"illu-baumpflege":[[0.547,0.625,0.045,0.039]],"illu-neubau":[[0.344,0.604,0.083,0.049],[0.063,0.532,0.048,0.047]],"illu-spielplaetze":[[0.74,0.461,0.041,0.052],[0.216,0.541,0.044,0.037]],"illu-winterdienst":[[0.728,0.478,0.051,0.065]],"kollegen-duo":[[0.556,0.356,0.084,0.125],[0.447,0.346,0.078,0.117],[0.426,0.306,0.289,0.137],[0.378,0.294,0.139,0.141],[0.616,0.318,0.15,0.136]],"kolonne-aktion":[[0.413,0.198,0.101,0.126]],"maeher-block":[[0.58,0.321,0.028,0.042],[0.552,0.273,0.086,0.062]],"maeher-front":[[0.582,0.246,0.069,0.058],[0.511,0.213,0.167,0.075]],"portrait-erfahren":[[0.461,0.23,0.145,0.097],[0.306,0.172,0.382,0.165]],"portrait-jung-ernst":[[0.394,0.259,0.28,0.187],[0.227,0.169,0.499,0.166]],"portrait-jung":[[0.476,0.182,0.195,0.13],[0.411,0.114,0.41,0.176]],"ralf-angebot-poster":[[0.313,0.3,0.299,0.168],[0.186,0.209,0.557,0.158]],"ralf-vorstellung-poster":[[0.433,0.293,0.272,0.153],[0.245,0.213,0.545,0.157]],"staub-trimmer":[[0.445,0.316,0.134,0.07]],"sticker-blasen":[[0.481,0.074,0.094,0.065]],"sticker-duo":[[0.42,0.066,0.173,0.098],[0.219,0.063,0.15,0.085],[0.539,0.02,0.304,0.188],[0.111,0.009,0.285,0.191]],"sticker-laecheln":[[0.298,0.079,0.267,0.142],[0.222,0.012,0.55,0.19]],"sticker-maeher":[[0.512,0.165,0.075,0.078],[0.439,0.104,0.167,0.101]],"sticker-trimmer":[[0.375,0.059,0.115,0.087],[0.294,0.009,0.321,0.186]],"sticker-trimmer2":[[0.423,0.07,0.206,0.094],[0.218,0.018,0.553,0.192]],"stimme-20-jahre-poster":[[0.411,0.232,0.204,0.115],[0.247,0.157,0.501,0.168]],"stimme-duo-poster":[[0.563,0.204,0.155,0.087],[0.226,0.183,0.196,0.11],[0.117,0.14,0.32,0.171],[0.549,0.154,0.328,0.169]],"stimme-grischa-poster":[[0.42,0.204,0.184,0.104],[0.212,0.151,0.436,0.169]],"stimme-kai-poster":[[0.381,0.212,0.161,0.091],[0.346,0.18,0.36,0.122]],"stimme-nail-poster":[[0.377,0.146,0.27,0.152],[0.224,0.072,0.543,0.185]],"team-absprache":[[0.158,0.21,0.109,0.091],[0.524,0.199,0.088,0.074],[0.555,0.138,0.166,0.172],[0.111,0.157,0.332,0.166]],"team-drei":[[0.327,0.335,0.053,0.035],[0.79,0.338,0.056,0.037],[0.745,0.315,0.132,0.082],[0.483,0.327,0.134,0.093],[0.231,0.294,0.153,0.106]],"trimmer-baum":[[0.545,0.267,0.043,0.064],[0.49,0.226,0.104,0.12]],"trimmer-hecke":[[0.148,0.352,0.077,0.084]],"trimmer-pfosten":[[0.497,0.12,0.117,0.078],[0.353,0.063,0.312,0.148]],"trimmer-weg":[[0.443,0.234,0.049,0.033],[0.451,0.197,0.22,0.102]]};
window.qaGesichter = async function (seiten, breiten) {
  const OVER = '.stimme-text, .stimme-play, .stimme-dauer, .live-clip, .laufband, .blase, .hero-karte, .zitatkarte, .tag, figcaption, .badge, .sticker, .hero-sticker, .vw-demo-tag, .eyebrow, h1, h2, .lead, .btn, .karte-label, .reel-name, .stimme-text';
  const erg = [];
  for (const W of breiten) for (const s of seiten) {
    const f = document.createElement('iframe'); f.style.cssText = 'position:absolute;left:0;top:0;width:' + W + 'px;height:900px;border:0;visibility:hidden'; f.src = s + (s.includes('?') ? '&' : '?') + 'statisch'; document.body.appendChild(f);
    await new Promise(r => f.onload = r); await new Promise(r => setTimeout(r, 600));
    const d = f.contentDocument, w = f.contentWindow;
    d.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager'); await new Promise(r => setTimeout(r, 900));
    const flaechen = [];
    d.querySelectorAll('img').forEach(img => {
      const m = (img.getAttribute('src') || '').match(/(?:img|video)\/([a-z0-9-]+?)(?:-[sml])?\.webp/); if (!m) return;
      const boxen = window.FACES[m[1]]; if (!boxen) return;
      const r = img.getBoundingClientRect(); if (!r.width) return;
      const cs = w.getComputedStyle(img); const nw = img.naturalWidth || +img.getAttribute('width'), nh = img.naturalHeight || +img.getAttribute('height');
      let sw = r.width, sh = r.height, ox = 0, oy = 0;
      if (cs.objectFit === 'cover') { const sc = Math.max(r.width / nw, r.height / nh); sw = nw * sc; sh = nh * sc; const [px, py] = cs.objectPosition.split(' ').map(v => parseFloat(v) / 100); ox = (r.width - sw) * px; oy = (r.height - sh) * py; }
      boxen.forEach(b => {
        const fx = r.left + ox + b[0] * sw, fy = r.top + oy + b[1] * sh, fw = b[2] * sw, fh = b[3] * sh;
        const clip = img.closest('.hero-foto, .lk-bild, .seitenkopf-bild, .haupt, .bild, .portraet, figure, .foto-rund') || img;
        const c = clip.getBoundingClientRect();
        const sichtbar = { l: Math.max(fx, c.left), t: Math.max(fy, c.top), r: Math.min(fx + fw, c.right), b: Math.min(fy + fh, c.bottom) };
        const anteil = Math.max(0, sichtbar.r - sichtbar.l) * Math.max(0, sichtbar.b - sichtbar.t) / (fw * fh);
        if (anteil < 0.85 && fw * fh > 150) erg.push([W, s, 'Gesicht angeschnitten', m[1], Math.round(anteil * 100) + '%']);
        flaechen.push({ img, name: m[1], l: fx, t: fy, r: fx + fw, b: fy + fh });
      });
    });
    d.querySelectorAll(OVER).forEach(o => {
      const cs = w.getComputedStyle(o); if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) return;
      const r = o.getBoundingClientRect(); if (!r.width) return;
      flaechen.forEach(F => {
        if (o === F.img || o.contains(F.img) || F.img.contains(o)) return;
        const ix = Math.min(r.right, F.r) - Math.max(r.left, F.l), iy = Math.min(r.bottom, F.b) - Math.max(r.top, F.t);
        if (ix > 4 && iy > 4 && ix * iy > 0.06 * (F.r - F.l) * (F.b - F.t)) erg.push([W, s, 'Overlay über Gesicht', (o.className || o.tagName).toString().slice(0, 30), F.name]);
      });
    });
    f.remove();
  }
  return erg;
};
// Layout-Prüfung: Raster-Zeilen, die viel Fläche frei lassen
window.qaLayout = async function (seiten, breiten) {
  const erg = [];
  for (const W of breiten) for (const s of seiten) {
    const f = document.createElement('iframe'); f.style.cssText = 'position:absolute;left:0;top:0;width:' + W + 'px;height:900px;border:0;visibility:hidden'; f.src = s + (s.includes('?') ? '&' : '?') + 'statisch'; document.body.appendChild(f);
    await new Promise(r => f.onload = r); await new Promise(r => setTimeout(r, 500));
    const d = f.contentDocument, w = f.contentWindow;
    d.querySelectorAll('main *').forEach(g => {
      const cs = w.getComputedStyle(g); if (cs.display !== 'grid') return;
      const spalten = cs.gridTemplateColumns.split(' ').length; if (spalten < 2) return;
      const gr = g.getBoundingClientRect(); if (gr.width < 300) return;
      const kinder = [...g.children].filter(k => w.getComputedStyle(k).display !== 'none' && k.getBoundingClientRect().height > 0);
      const zeilen = {}; kinder.forEach(k => { const r = k.getBoundingClientRect(); const key = Math.round(r.top / 8); (zeilen[key] = zeilen[key] || []).push(r); });
      const keys = Object.keys(zeilen);
      keys.forEach((key, idx) => {
        const rs = zeilen[key]; const breite = Math.max(...rs.map(r => r.right)) - Math.min(...rs.map(r => r.left));
        if (breite < gr.width * 0.62) erg.push([W, s, (g.className || g.tagName).toString().slice(0, 30), 'Zeile ' + (idx + 1) + '/' + keys.length, Math.round(breite / gr.width * 100) + '% gefüllt', rs.length + ' Elemente']);
      });
    });
    f.remove();
  }
  return erg;
};
