"""Transkribiert Interview-Clips (deutsch) mit Zeitstempeln: python3 tools/transkribieren.py datei.mp4 ..."""
import sys, json, os
from faster_whisper import WhisperModel
m = WhisperModel(os.environ.get('WHISPER_MODEL', 'medium'), device='cpu', compute_type='int8')
for f in sys.argv[1:]:
    ziel = f.rsplit('.', 1)[0] + '.transkript.json'
    if os.path.exists(ziel): continue
    segs, info = m.transcribe(f, language='de', vad_filter=True, word_timestamps=False)
    out = [{'von': round(s.start, 2), 'bis': round(s.end, 2), 'text': s.text.strip()} for s in segs]
    json.dump(out, open(ziel, 'w'), ensure_ascii=False, indent=1)
    print('✓', os.path.basename(f), len(out), 'Segmente', flush=True)
