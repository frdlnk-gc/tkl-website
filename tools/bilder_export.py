"""Exportiert ausgewählte Drive-Fotos + Freisteller als Web-Bilder nach site/assets/img.
Fotos: WebP in 3 Breiten (-s 800, -m 1400, -l 2200). Sticker: WebP mit weißem Rand + Schatten."""
import os, sys
from PIL import Image, ImageOps, ImageFilter, ImageChops
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_rohmaterial", "bilder"); OUT = os.path.join(ROOT, "site", "assets", "img")
# name: (datei, crop als (x0,y0,x1,y1) in Anteilen oder None)
FOTOS = {
 "siedlung-hecke": ("DSC03100.JPG", None),
 "maeher-block": ("DSC03178.JPG", None),
 "kolonne-aktion": ("DSC03240.JPG", None),
 "kollegen-duo": ("DSC03130.JPG", None),
 "maeher-weg": ("DSC03224.JPG", None),
 "maeher-front": ("DSC03083.JPG", (0, .12, 1, .92)),
 "blasgeraet": ("DSC03219.JPG", None),
 "trimmer-weg": ("DSC03222.JPG", None),
 "trimmer-baum": ("DSC03241.JPG", None),
 "hecke-weg": ("DSC03245.JPG", None),
 "portrait-jung": ("DSC03158.JPG", None),
 "portrait-jung-ernst": ("DSC03159.JPG", None),
 "portrait-erfahren": ("DSC03110.JPG", None),
 "team-absprache": ("DSC03127.JPG", (0, 0, 1, .8)),
 "team-drei": ("DSC03210.JPG", None),
 "geschaeftsfuehrung": ("DSC03251.JPG", None),
 "staub-trimmer": ("DSC03088.JPG", None),
 "maeher-himmel": ("IMG_3955.jpg", None),
 "trimmer-pfosten": ("DSC03229.JPG", None),
 "rasen-baum": ("DSC03141.JPG", None),
 "trimmer-hecke": ("DSC03246.JPG", None),
}
STICKER = {"duo": "03135", "laecheln": "03158", "blasen": "03218", "trimmer": "03205", "maeher": "03083", "trimmer2": "03234"}

def foto(name, fn, crop):
    im = Image.open(os.path.join(SRC, fn)); im = ImageOps.exif_transpose(im).convert("RGB")
    if crop: w, h = im.size; im = im.crop((int(crop[0]*w), int(crop[1]*h), int(crop[2]*w), int(crop[3]*h)))
    for suf, wmax in (("s", 800), ("m", 1400), ("l", 2200)):
        c = im.copy(); c.thumbnail((wmax, wmax * 2)) if c.width >= c.height else c.thumbnail((wmax, wmax))
        if c.width < c.height:  # Hochformat: Breite begrenzen
            c = im.copy(); r = (wmax * 0.75) / im.width; c = c.resize((int(im.width*r), int(im.height*r)), Image.LANCZOS)
        c.save(os.path.join(OUT, f"{name}-{suf}.webp"), quality=80, method=6)
    print(name, im.size)

def sticker(name, nr):
    raw = os.path.join(ROOT, "_work", "sticker", f"raw_{nr}.png")
    im = Image.open(raw).convert("RGBA"); im.thumbnail((900, 1100))
    pad = 40; base = Image.new("RGBA", (im.width + 2*pad, im.height + 2*pad), (0, 0, 0, 0)); base.paste(im, (pad, pad), im)
    a = base.split()[3].point(lambda v: 255 if v > 110 else 0)
    rand = a.filter(ImageFilter.MaxFilter(17)).filter(ImageFilter.GaussianBlur(1.2)).point(lambda v: 255 if v > 100 else 0)
    weiss = Image.new("RGBA", base.size, (255, 255, 255, 255)); weiss.putalpha(rand)
    schatten = Image.new("RGBA", base.size, (20, 25, 28, 0)); schatten.putalpha(rand.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v*.28)))
    out = Image.new("RGBA", base.size, (0, 0, 0, 0)); out.alpha_composite(schatten, (6, 10)); out.alpha_composite(weiss); out.alpha_composite(base)
    out = out.crop(out.getbbox()); out.save(os.path.join(OUT, f"sticker-{name}.webp"), quality=86, method=6)
    print("sticker", name, out.size)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:]
    for n, (fn, cr) in FOTOS.items():
        if not only or n in only: foto(n, fn, cr)
    for n, nr in STICKER.items():
        if not only or n in only: sticker(n, nr)
