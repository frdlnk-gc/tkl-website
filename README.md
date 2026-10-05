# TKL GmbH – Website (Vorschau Greenfield Digital)

Vorschau: https://frdlnk-gc.github.io/tkl-website/ · Verwaltung: …/verwaltung/ (Umzug auf eigene Domain: BASE in tools/build.py auf "" setzen, CNAME anlegen)

## Aufbau
- `site/` – fertige statische Website (wird per GitHub Actions auf GitHub Pages veröffentlicht)
- `tools/build.py` + `tools/seiten.py` + `tools/teile.py` – erzeugen alle Seiten (`python3 tools/build.py`)
- `tools/bilder_export.py` – Fotos/Freisteller aus dem Drive-Material → `site/assets/img`
- `tools/gesichter.swift` – erkennt Gesichter/Köpfe, daraus berechnet `build.py` den Bildausschnitt (Gesichter nie angeschnitten)
- `tools/gen_illustrationen.py` – Illustrationen (Winterdienst, Spielplätze, Baumpflege, Neubau) per OpenAI-Bildmodell
- `supabase/functions/tkl-api` – Backend (Supabase-Projekt `ildagygshaiaiqghjouj`): Formulare, anonyme Besucherzählung, Login, Leads, Kennzahlen
  - Tabellen `tkl_leads`, `tkl_events`, `tkl_users` – RLS an, keine Policies, Zugriff nur über die Function (Service-Role)

## Umzug auf tkl.gmbh
Siehe `UMZUG.md`.
