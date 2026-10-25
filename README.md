# Umrechner

Währungsrechner als Web-App (PWA) mit den Referenzkursen der Europäischen Zentralbank. Lässt sich auf dem iPhone über Safari → Teilen → „Zum Home-Bildschirm“ wie eine App installieren und funktioniert auch offline.

- Kurstabelle mit runden Beträgen; wischen oder ← → für ×10 / ÷10, Zeile antippen für Zwischenwerte
- ↻ lädt neue Kurse; ohne Verbindung gelten die zuletzt gespeicherten (mit Hinweis)
- Standort-Knopf stellt die Landeswährung ein (siehe „Landeserkennung“)

Kurse: [frankfurter.dev](https://frankfurter.dev) (EZB-Daten, kostenlos, ohne Schlüssel).

## Herkunft des Codes

Der gesamte Code dieses Projekts – App, Service Worker, Hilfsskripte und Icon – wurde von **Claude**, einem KI-Modell von [Anthropic](https://www.anthropic.com), geschrieben. Der Inhaber dieses Repositorys hat die Anforderungen und das Design vorgegeben, die Ergebnisse geprüft und die Entscheidungen getroffen. Commits, die mit Claude entstanden sind, tragen den Vermerk `Co-Authored-By: Claude`.

Die Bedienidee (eine Tabelle runder Beträge, die sich in Zehnerschritten skalieren lässt) ist ein verbreitetes Konzept für Reise-Währungsrechner. Code, Gestaltung, Farben, Icon und Texte sind eigenständig erstellt; es wurden keine Inhalte anderer Apps übernommen.

## Landeserkennung und Datenschutz

Der Standort-Knopf fragt beim ersten Mal nach der Standortfreigabe; der ungefähre Standort genügt.

1. **Online:** Die Koordinaten werden auf ≈ 1 km gerundet und an [BigDataCloud](https://www.bigdatacloud.com) geschickt, das daraus das Land bestimmt. Sonst verlässt nichts das Gerät.
2. **Offline oder Dienst nicht erreichbar:** Abgleich mit eingebauten, vereinfachten Landesgrenzen (`borders.json`, Genauigkeit ≈ 2 km; sehr kleine Staaten wie Monaco werden dem Nachbarland zugeordnet).
3. **Ohne Standortfreigabe:** Schätzung über die Zeitzone des Geräts – ungenau, weil z. B. Deutschland und Tschechien dieselbe Zeitzone haben. Die App sagt dann dazu, dass geschätzt wurde.

Einstellungen und gespeicherte Kurse bleiben auf dem Gerät (localStorage), es gibt kein Konto und keine Analyse.

## Datenquellen

- Wechselkurse: Referenzkurse der Europäischen Zentralbank, abgerufen über [frankfurter.dev](https://frankfurter.dev). Die Kurse dienen nur zur Information und gelten nicht für tatsächliche Umtauschgeschäfte.
- Landesgrenzen: [Natural Earth](https://www.naturalearthdata.com) (gemeinfrei), Admin 0 – Countries, 1:50 Mio., vereinfacht.
- Land aus Koordinaten (online): [BigDataCloud](https://www.bigdatacloud.com/free-api/free-reverse-geocode-to-city-api), kostenlose Client-Schnittstelle.

## Lizenz

Gemeinfrei nach [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/deed.de), siehe [LICENSE](LICENSE). Jeder darf den Code ohne Bedingungen nutzen, verändern und weitergeben, auch ohne Namensnennung – ohne jede Gewähr und Haftung.

Die Lizenz gilt für den Code, das Icon und die Texte dieses Repositorys. Die abgerufenen Wechselkurse und die Landesgrenzen (Natural Earth, selbst gemeinfrei) unterliegen den Bedingungen ihrer Quellen; „Claude“ und „Anthropic“ sind Namen von Anthropic.

## Entwicklung

- `index.html` – die App, `sw.js` – Offline-Speicher, `manifest.webmanifest` – App-Name und Icons
- `data.js` neu erzeugen (Zeitzonen, Währungen, Rückfall-Kurse): `python3 tools/make-data.py`
- `borders.json` neu erzeugen: Natural-Earth-Datei laden und `python3 tools/make-borders.py <datei.geojson>`
- Nach Änderungen an App-Dateien in `sw.js` die `VERSION` erhöhen. Installierte Apps suchen beim Öffnen und beim Zurückholen aus dem Hintergrund nach Updates und starten sich bei einer neuen Version selbst neu.
