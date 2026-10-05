"""Illustrationen für Leistungen ohne Fotomaterial (Winterdienst, Spielplätze, Baumpflege, Neubau).
Modell: $GC_IMAGE_MODEL (Standard gpt-image-2.5-sunburst). Key: greencareers-kundenfunnel/config.json.
Aufruf: python3 tools/gen_illustrationen.py [name ...]"""
import json, os, sys, base64, urllib.request, io
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
KEY = os.environ.get("OPENAI_API_KEY") or json.load(open(os.path.join(ROOT, "..", "greencareers-kundenfunnel", "config.json")))["openai_api_key"]
MODEL = os.environ.get("GC_IMAGE_MODEL", "gpt-image-2.5-sunburst")
STYLE = ("Hand-painted editorial illustration in gouache and acrylic with visible brush strokes and subtle paper grain. "
 "Soft pastel palette (pale sky blue, mint green, warm cream, soft coral) with confident accents of signal red (#D8231C) and fresh leaf green. "
 "Modern, calm and professional, like a high-end picture book for adults, slightly naive shapes, no outlines overload. "
 "Workers wear black long-sleeve work shirts and bright red work trousers, ear protection where it fits, friendly faces seen from a distance. "
 "Setting: typical Ruhr area residential estate of a housing cooperative: three-storey white plastered apartment blocks with balconies, mature trees, lawns, grey paved paths. "
 "Absolutely no text, no letters, no numbers, no logos, no brand names, no signs. Calm negative space in the upper third. Scene: ")
SCENES = {
 "winterdienst": "Early winter morning at blue hour, light fresh snow. A compact red municipal utility tractor with a front rotating brush clears a paved footpath between apartment blocks, a worker in red trousers and a black winter jacket spreads grit with a small push spreader. Warm glowing street lamps, a few lit windows, quiet and safe atmosphere.",
 "spielplaetze": "A tidy playground in the green courtyard of an apartment estate on a sunny late-summer morning: wooden climbing tower with a stainless slide, swings, sandbox. One worker in red trousers kneels and checks a swing chain with a clipboard, a second worker rakes the sand. No children present. Fresh, safe, well maintained.",
 "baumpflege": "Autumn afternoon in an apartment estate. A worker in red trousers and a helmet stands in the basket of a compact aerial work platform and prunes a branch of a large old lime tree next to a white apartment block. A colleague below in red trousers collects cut branches inside an area secured with red and white cones. Golden leaves.",
 "neubau": "A freshly renovated white apartment block with new balconies. In front, three workers in red trousers lay fresh rolled turf and build a new path with grey concrete pavers, young newly planted trees with wooden stakes, a small orange mini excavator in the background. Bright spring day, sense of a fresh start.",
}
def gen(name):
    out = os.path.join(ROOT, "_work", "illu", name + ".png")
    if os.path.exists(out): return name + " existiert"
    body = json.dumps({"model": MODEL, "prompt": STYLE + SCENES[name], "size": "1536x1024", "quality": "high", "n": 1}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=body, headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=400) as r: d = json.load(r)
    Image.open(io.BytesIO(base64.b64decode(d["data"][0]["b64_json"]))).save(out)
    return name + " ok"
if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "_work", "illu"), exist_ok=True)
    names = sys.argv[1:] or list(SCENES)
    with ThreadPoolExecutor(4) as ex:
        for res in ex.map(lambda n: (lambda: gen(n))() if True else None, names):
            print(res, flush=True)
