"""Schneidet Interview-Clips fürs Web (mit Ton) und erzeugt Untertitel (WebVTT) aus den Transkripten.
Aufruf: python3 tools/clips.py [name ...]
Ausgabe: site/assets/video/<name>.mp4, <name>-poster.webp, <name>.vtt"""
import json, os, subprocess, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '_rohmaterial', 'videos2')
OUT = os.path.join(ROOT, 'site', 'assets', 'video')

# Korrekturen typischer Hörfehler der Spracherkennung
KORREKTUR = {'Grischer': 'Grischa', 'allen Rade': 'Aldenrade', 'zu behen': 'zu mähen', 'Galerbauunternehmen': 'GaLaBau-Unternehmen', 'Kastrop': 'Castrop', 'rennt euch gerne an uns': 'wendet euch gerne an uns', 'Mehlmaschine': 'Mähmaschine', 'Aufsitz mehr': 'Aufsitzmäher', 'sämtliche Wohngesellschaften': 'sämtlichen Wohnungsgesellschaften', 'viel Umwechsel': 'viel Abwechslung', 'mit dem Mähmaschine': 'mit der Mähmaschine', 'Natur arbeiten': 'In der Natur arbeiten', 'Ich muss sagen, draußen': 'Ich muss sagen: Draußen'}

# name: (quelle, [(von, bis), ...], posterzeit_im_ergebnis)
CLIPS = json.load(open(os.path.join(ROOT, 'tools', 'clips.json'), encoding='utf-8'))

def ts(t):
    h, r = divmod(max(0, t), 3600); m, s = divmod(r, 60)
    return f'{int(h):02d}:{int(m):02d}:{s:06.3f}'

def vtt(name, quelle, segs, ausnahmen):
    p = os.path.join(SRC, quelle + '.transkript.json')
    if not os.path.exists(p): return False
    tr = json.load(open(p, encoding='utf-8'))
    zeilen, offset = ['WEBVTT', ''], 0.0
    for von, bis in segs:
        for s in tr:
            if s['bis'] <= von or s['von'] >= bis: continue
            if any(a in s['text'] for a in ausnahmen): continue
            t = s['text']
            for a, b in KORREKTUR.items(): t = t.replace(a, b)
            a_ = max(s['von'], von) - von + offset; b_ = min(s['bis'], bis) - von + offset
            if b_ - a_ < 0.4: continue
            zeilen += [f'{ts(a_)} --> {ts(b_)}', t, '']
        offset += bis - von
    open(os.path.join(OUT, name + '.vtt'), 'w', encoding='utf-8').write('\n'.join(zeilen))
    return True

def schneide(name, c):
    quelle, segs, poster = c['quelle'], c['segmente'], c.get('poster', 1.0)
    inp, fc = [], []
    for i, (von, bis) in enumerate(segs):
        inp += ['-ss', str(von), '-t', str(bis - von), '-i', os.path.join(SRC, quelle + '.mp4')]
        fc.append(f'[{i}:v]scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1[v{i}];[{i}:a]aresample=48000,loudnorm=I=-16:TP=-1.5[a{i}]')
    fc.append(''.join(f'[v{i}][a{i}]' for i in range(len(segs))) + f'concat=n={len(segs)}:v=1:a=1[v][a]')
    ziel = os.path.join(OUT, name + '.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(fc), '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '27', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart', ziel], check=True)
    tmp = f'/tmp/{name}-p.jpg'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(poster), '-i', ziel, '-frames:v', '1', '-q:v', '3', tmp], check=True)
    Image.open(tmp).save(os.path.join(OUT, name + '-poster.webp'), quality=76)
    ok = vtt(name, quelle, segs, c.get('ohne', []))
    groesse = os.path.getsize(ziel) / 1e6
    print(f'✓ {name}: {sum(b - a for a, b in segs):.0f}s, {groesse:.1f} MB, Untertitel {"ja" if ok else "FEHLT"}')

if __name__ == '__main__':
    nur = sys.argv[1:]
    for n, c in CLIPS.items():
        if not nur or n in nur: schneide(n, c)
