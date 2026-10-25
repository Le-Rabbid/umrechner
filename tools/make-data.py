#!/usr/bin/env python3
"""Code geschrieben von Claude (KI-Modell von Anthropic), siehe README.md.

Erzeugt PWA/data.js: Zeitzone → Land → Währung (Standort-Knopf) und einen eingebetteten Kursstand.

Aufruf aus dem Projektordner:  python3 PWA/tools/make-data.py
Braucht macOS (Zeitzonen-Datenbank und Swift für die Landeswährungen) und Internet für die Kurse.
"""
import datetime
import json
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
RATES_URL = "https://api.frankfurter.dev/v1/latest?base=EUR"

# Ältere Namen, die Browser teilweise noch melden.
ALIASES = {
    "Europe/Kiev": "UA", "Asia/Calcutta": "IN", "Asia/Saigon": "VN", "Asia/Katmandu": "NP",
    "Asia/Rangoon": "MM", "America/Buenos_Aires": "AR", "Atlantic/Faeroe": "FO", "Pacific/Truk": "FM",
    "Pacific/Ponape": "FM", "Asia/Ulan_Bator": "MN", "America/Indianapolis": "US", "America/Louisville": "US",
}


def timezones():
    zones = {}
    for line in open("/usr/share/zoneinfo/zone.tab", encoding="utf-8"):
        if line.startswith("#"):
            continue
        country, _coords, zone = line.rstrip("\n").split("\t")[:3]
        zones[zone] = country
    zones.update(ALIASES)
    return zones


def main():
    zones = timezones()
    currencies = json.loads(subprocess.run(
        ["swift", str(HERE / "country-currency.swift")], check=True, capture_output=True, text=True,
    ).stdout)
    used = sorted(set(zones.values()))
    tzmap = {"tz": zones, "cur": {c: currencies[c] for c in used if c in currencies}}

    # curl statt urllib: nutzt die Zertifikate des Systems (python.org-Python bringt keine mit).
    rates = json.loads(subprocess.run(
        ["curl", "-sSf", "--max-time", "15", RATES_URL], check=True, capture_output=True, text=True,
    ).stdout)
    fallback = {
        "base": rates["base"],
        "date": rates["date"],
        "rates": rates["rates"],
        "fetchedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    }

    out = HERE.parent / "data.js"
    out.write_text(
        "// Erzeugt von tools/make-data.py – nicht von Hand bearbeiten. Code geschrieben von Claude (KI-Modell von Anthropic), siehe README.md.\n"
        "// Zeitzone → Land und Land → Währung (Standort-Knopf) sowie ein Kursstand für den ersten Start ohne Internet.\n"
        f"const TZMAP = {json.dumps(tzmap, separators=(',', ':'), sort_keys=True)};\n"
        f"const FALLBACK = {json.dumps(fallback, separators=(',', ':'))};\n",
        encoding="utf-8",
    )
    print(f"{out.name}: {len(zones)} Zeitzonen, {len(tzmap['cur'])} Länder, Kurse vom {rates['date']}")


if __name__ == "__main__":
    main()
