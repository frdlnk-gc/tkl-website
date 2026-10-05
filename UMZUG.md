# Umzug tkl.greenfield-digital.de → tkl.gmbh

1. DNS bei TKLs Domain-Anbieter: `tkl.gmbh` A → 185.199.108.153 / 185.199.109.153 / 185.199.110.153 / 185.199.111.153, `www` CNAME → frdlnk-gc.github.io. MX/SPF/DKIM NICHT ändern.
2. `site/CNAME` auf `www.tkl.gmbh` (oder `tkl.gmbh`) ändern, in `tools/build.py` `BASIS_URL` anpassen und `VORSCHAU = False` setzen (noindex raus), `site/robots.txt` auf `Allow: /` + Sitemap.
3. `python3 tools/build.py`, committen, pushen → GitHub Pages veröffentlicht; Custom Domain in den Repo-Einstellungen prüfen, „Enforce HTTPS“ an.
4. CORS ist für tkl.gmbh in der Function `tkl-api` schon freigegeben.
5. Beispieldaten in der Verwaltung löschen, TKL-Logins anlegen (Tabelle `tkl_users`, Passwort-Hash PBKDF2-SHA256, 210 000 Runden).
6. Google-Unternehmensprofil + Search Console aktualisieren.
