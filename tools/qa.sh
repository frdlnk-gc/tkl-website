#!/bin/bash
# Spiegelt site/ in die Vorschau und macht Ganzseiten-Shots: tools/qa.sh <name> <pfad> <breite> <hoehe>
cd "$(dirname "$0")/.."
SP=/private/tmp/claude-501/-Users-frederiklinke-Desktop-Alle-Ordner-Claude-Coding/f0417822-9295-460e-af8a-edb9857469fa/scratchpad/tkl-preview
rsync -a --delete site/ $SP/site/
sep='?'; [[ "$2" == *\?* ]] && sep='&'
tools/shoot.sh "$2${sep}statisch" $3 $4 _work/shots/$1.png
python3 - "$1" <<'PY'
import sys
from PIL import Image
n=sys.argv[1]; im=Image.open(f'_work/shots/{n}.png'); w,h=im.size
# leeren Rest unten abschneiden
px=im.convert('RGB'); 
step=1700 if w>800 else 2200
for i in range(0,h,step):
    c=im.crop((0,i,w,min(h,i+step))); c.thumbnail((1000 if w>800 else 420,1400)); c.save(f'_work/shots/{n}-{i//step}.jpg',quality=78)
print(n,w,h,(h+step-1)//step,'Teile')
PY
