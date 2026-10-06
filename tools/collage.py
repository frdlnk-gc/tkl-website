"""Comic-Collagen: gemalter Hintergrund + echter Freisteller mit weißem Rand (wie die alte TKL-Seite)."""
import os
from PIL import Image, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.path.join(ROOT, '_work'); OUT = os.path.join(ROOT, 'site', 'assets', 'img')

def rand(im, px=14):
    pad = px * 3; base = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0)); base.paste(im, (pad, pad), im)
    a = base.split()[3].point(lambda v: 255 if v > 110 else 0)
    r = a.filter(ImageFilter.MaxFilter(px * 2 + 1)).filter(ImageFilter.GaussianBlur(1.2)).point(lambda v: 255 if v > 100 else 0)
    weiss = Image.new('RGBA', base.size, (255, 255, 255, 255)); weiss.putalpha(r)
    sch = Image.new('RGBA', base.size, (40, 40, 30, 0)); sch.putalpha(r.filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * .3)))
    out = Image.new('RGBA', base.size, (0, 0, 0, 0)); out.alpha_composite(sch, (8, 12)); out.alpha_composite(weiss); out.alpha_composite(base)
    return out.crop(out.getbbox())

# name: hintergrund, [(freisteller, höhe in % der Bildhöhe, x-Mitte %, unterkante %)]
COLLAGEN = {
 'collage-winter': ('bg-winter', [('raw_fm86', .70, .50, .97)]),
 'collage-spielplatz': ('bg-spielplatz', [('raw_03135', .66, .60, .98)]),
 'collage-baum': ('bg-baum', [('raw_03246', .62, .44, .96)]),
 'collage-neubau': ('bg-neubau', [('raw_03218', .66, .62, .98)]),
}
for name, (bg, teile) in COLLAGEN.items():
    hg = Image.open(os.path.join(W, 'illu', bg + '.png')).convert('RGBA'); Wd, H = hg.size
    for datei, hoehe, xm, unten in teile:
        st = rand(Image.open(os.path.join(W, 'sticker', datei + '.png')).convert('RGBA'))
        s = hoehe * H / st.height; st = st.resize((int(st.width * s), int(st.height * s)), Image.LANCZOS)
        hg.alpha_composite(st, (int(xm * Wd - st.width / 2), int(unten * H - st.height)))
    hg = hg.convert('RGB')
    for suf, w in (('m', 1400), ('s', 800)):
        c = hg.copy(); c.thumbnail((w, w)); c.save(os.path.join(OUT, f'{name}-{suf}.webp'), quality=82, method=6)
    print('✓', name)
