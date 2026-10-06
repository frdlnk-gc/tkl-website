"""Illustrationen für Leistungen ohne Fotomaterial (Winterdienst, Spielplätze, Baumpflege, Neubau).
Modell: $GC_IMAGE_MODEL (Standard gpt-image-2.5-sunburst). Key: greencareers-kundenfunnel/config.json.
Aufruf: python3 tools/gen_illustrationen.py [name ...]"""
import json, os, sys, base64, urllib.request, io
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
KEY = os.environ.get("OPENAI_API_KEY") or json.load(open(os.path.join(ROOT, "..", "greencareers-kundenfunnel", "config.json")))["openai_api_key"]
MODEL = os.environ.get("GC_IMAGE_MODEL", "gpt-image-2.5-sunburst")
STYLE_ALT = ("Hand-painted editorial illustration in gouache and acrylic with visible brush strokes and subtle paper grain. "
 "Soft pastel palette (pale sky blue, mint green, warm cream, soft coral) with confident accents of signal red (#D8231C) and fresh leaf green. "
 "Modern, calm and professional, like a high-end picture book for adults, slightly naive shapes, no outlines overload. "
 "Workers wear black long-sleeve work shirts and bright red work trousers, ear protection where it fits, friendly faces seen from a distance. "
 "Setting: typical Ruhr area residential estate of a housing cooperative: three-storey white plastered apartment blocks with balconies, mature trees, lawns, grey paved paths. "
 "Absolutely no text, no letters, no numbers, no logos, no brand names, no signs. Calm negative space in the upper third. Scene: ")
STYLE2 = None
STYLE = ("Loose hand-drawn editorial sketch: confident thin black ink outlines with soft transparent watercolor washes on warm off-white paper, "
 "lots of white paper showing, slightly naive and friendly like an architect's concept sketch, muted pastel palette (sage green, pale sky blue, warm sand, soft brick). "
 "{personen}The lower middle of the image is an open, calm empty area of ground where a cut-out photo will be placed later. "
 "Absolutely no text, letters, numbers or signs. Scene: ")
SCENES_COLLAGE2 = {
 "bg-baum2": "A large old deciduous tree next to a simple white apartment block. A red aerial work platform (cherry picker) stands beside the tree, in its basket a small sketched worker in red trousers and helmet prunes a branch with a pole saw; below, red-white traffic cones and a small pile of cut branches. The right third of the foreground is an open empty lawn.",
 "bg-neubau2": "A renovated apartment block with balconies; in front an outdoor area under construction: a half-laid grey concrete paver path, a pallet stack of paving stones, a small orange mini excavator, rolls of fresh turf, sand heap, young trees with wooden stakes. Two small sketched workers in red trousers kneel laying pavers in the middle distance on the left. The right third of the foreground is open empty ground.",
 "bg-gruen": "The wide green lawn of an apartment estate with three-storey white apartment blocks, mature trees and neat hedges, freshly mown stripes in the grass, a paved footpath at the edge. The middle foreground is open empty lawn.",
}
SCENES_COLLAGE = {
 "bg-winter": "A curved footpath between two simple three-storey apartment blocks in winter, snow on roofs and lawns, bare trees, a few street lamps, the path itself freshly cleared.",
 "bg-spielplatz": "The green courtyard of an apartment estate with a small wooden playground: climbing tower with slide on the left side, sandbox, two swings, a bench, trees. Open lawn in the middle foreground.",
 "bg-baum": "One large old deciduous tree with a wide crown standing on a lawn in front of a simple white apartment block, a paved path curving past, autumn colours in the leaves.",
 "bg-neubau": "A freshly renovated modern apartment block with balconies, in front newly laid lawn, young trees with wooden stakes, a new paved path and a parking bay in the foreground.",
}
SCENES = {
 "winterdienst": "Early winter morning at blue hour, light fresh snow. A compact red municipal utility tractor with a front rotating brush clears a paved footpath between apartment blocks, a worker in red trousers and a black winter jacket spreads grit with a small push spreader. Warm glowing street lamps, a few lit windows, quiet and safe atmosphere.",
 "spielplaetze": "A tidy playground in the green courtyard of an apartment estate on a sunny late-summer morning: wooden climbing tower with a stainless slide, swings, sandbox. One worker in red trousers kneels and checks a swing chain with a clipboard, a second worker rakes the sand. No children present. Fresh, safe, well maintained.",
 "baumpflege": "Autumn afternoon in an apartment estate. A worker in red trousers and a helmet stands in the basket of a compact aerial work platform and prunes a branch of a large old lime tree next to a white apartment block. A colleague below in red trousers collects cut branches inside an area secured with red and white cones. Golden leaves.",
 "neubau": "A freshly renovated white apartment block with new balconies. In front, three workers in red trousers lay fresh rolled turf and build a new path with grey concrete pavers, young newly planted trees with wooden stakes, a small orange mini excavator in the background. Bright spring day, sense of a fresh start.",
}
def gen(name):
    out = os.path.join(ROOT, "_work", "illu", name + ".png")
    if os.path.exists(out): return name + " existiert"
    body = json.dumps({"model": MODEL, "prompt": STYLE.replace("{personen}", "Only the small sketched people and machines explicitly described, drawn in the same loose ink-and-watercolor style, no other people. " if name in SCENES_COLLAGE2 else "NO people, NO vehicles, NO machines, NO animals in the image. ") + SCENES[name], "size": "1536x1024", "quality": "high", "n": 1}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=body, headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=400) as r: d = json.load(r)
    Image.open(io.BytesIO(base64.b64decode(d["data"][0]["b64_json"]))).save(out)
    return name + " ok"
if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "_work", "illu"), exist_ok=True)
    if sys.argv[1:2] == ["collage2"]:
        SCENES.update(SCENES_COLLAGE2); names = list(SCENES_COLLAGE2)
    elif sys.argv[1:2] == ["collage"]:
        SCENES.update(SCENES_COLLAGE); names = list(SCENES_COLLAGE)
    else:
        names = sys.argv[1:] or list(SCENES)
    with ThreadPoolExecutor(4) as ex:
        for res in ex.map(lambda n: (lambda: gen(n))() if True else None, names):
            print(res, flush=True)
