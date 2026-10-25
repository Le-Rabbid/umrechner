# Umrechner

Währungsrechner als Web-App (PWA) mit den Referenzkursen der Europäischen Zentralbank. Lässt sich auf dem iPhone über Safari → Teilen → „Zum Home-Bildschirm“ wie eine App installieren und funktioniert auch offline.

- Kurstabelle mit runden Beträgen; wischen oder ← → für ×10 / ÷10, Zeile antippen für Zwischenwerte
- ↻ lädt neue Kurse; ohne Verbindung gelten die zuletzt gespeicherten (mit Hinweis)
- Standort-Knopf erkennt das Land über die Zeitzone des Geräts (keine Standortfreigabe nötig)

Kurse: [frankfurter.dev](https://frankfurter.dev) (EZB-Daten, kostenlos, ohne Schlüssel).

## Herkunft des Codes

Der gesamte Code dieses Projekts – App, Service Worker, Hilfsskripte und Icon – wurde von **Claude**, einem KI-Modell von [Anthropic](https://www.anthropic.com), geschrieben. Der Inhaber dieses Repositorys hat die Anforderungen und das Design vorgegeben, die Ergebnisse geprüft und die Entscheidungen getroffen. Commits, die mit Claude entstanden sind, tragen den Vermerk `Co-Authored-By: Claude`.

Die Bedienidee (eine Tabelle runder Beträge, die sich in Zehnerschritten skalieren lässt) ist ein verbreitetes Konzept für Reise-Währungsrechner. Code, Gestaltung, Farben, Icon und Texte sind eigenständig erstellt; es wurden keine Inhalte anderer Apps übernommen.

## Datenquelle

Wechselkurse: Referenzkurse der Europäischen Zentralbank, abgerufen über [frankfurter.dev](https://frankfurter.dev). Die Kurse dienen nur zur Information und gelten nicht für tatsächliche Umtauschgeschäfte.

## Entwicklung

- `index.html` – die App, `sw.js` – Offline-Speicher, `manifest.webmanifest` – App-Name und Icons
- `data.js` neu erzeugen (Zeitzonen, Währungen, Rückfall-Kurse): `python3 tools/make-data.py`
- Nach Änderungen an App-Dateien in `sw.js` die `VERSION` erhöhen, damit installierte Apps das Update laden
