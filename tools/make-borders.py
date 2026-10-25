#!/usr/bin/env python3
"""Code geschrieben von Claude (KI-Modell von Anthropic), siehe README.md.

Erzeugt PWA/borders.json: vereinfachte Landesgrenzen für die Offline-Landeserkennung.

Quelle: Natural Earth, „Admin 0 – Countries“ im Maßstab 1:50 Mio. (gemeinfrei), z. B.
https://raw.githubusercontent.com/nvkelso/natural-earth-vector/v5.1.2/geojson/ne_50m_admin_0_countries.geojson

Aufruf:  python3 PWA/tools/make-borders.py <pfad/zu/ne_50m_admin_0_countries.geojson>

Format von borders.json: {"CZ": [[x0, y0, dx1, dy1, …], …], …}
Je Land eine Liste von Ringen (Außen- und Innenringe gemischt; die App wertet sie mit der
Gerade-ungerade-Regel aus). Koordinaten in Hundertstel Grad, ab dem zweiten Punkt als Differenz.
"""
import json
import pathlib
import sys

PRECISION = 100       # Hundertstel Grad ≈ 1 km
TOLERANCE = 0.02      # Vereinfachung: Abweichung bis ≈ 2 km

# Gebiete ohne eigenen ISO-Code dem Land zuordnen, zu dem sie praktisch gehören.
FALLBACK_CODES = {"Somaliland": "SO", "Northern Cyprus": "CY"}


def simplify(points, tolerance):
    """Douglas-Peucker-Vereinfachung einer Punktliste."""
    if len(points) < 3:
        return points
    keep = [False] * len(points)
    keep[0] = keep[-1] = True
    stack = [(0, len(points) - 1)]
    while stack:
        start, end = stack.pop()
        (x1, y1), (x2, y2) = points[start], points[end]
        dx, dy = x2 - x1, y2 - y1
        length = (dx * dx + dy * dy) ** 0.5
        farthest, index = 0.0, None
        for i in range(start + 1, end):
            px, py = points[i]
            if length == 0:
                dist = ((px - x1) ** 2 + (py - y1) ** 2) ** 0.5
            else:
                dist = abs(dy * px - dx * py + x2 * y1 - y2 * x1) / length
            if dist > farthest:
                farthest, index = dist, i
        if index is not None and farthest > tolerance:
            keep[index] = True
            stack += [(start, index), (index, end)]
    return [p for p, k in zip(points, keep) if k]


def encode(ring):
    ints = []
    for x, y in ring:
        point = (round(x * PRECISION), round(y * PRECISION))
        if not ints or point != ints[-1]:
            ints.append(point)
    if len(ints) < 4:  # zu klein nach dem Runden (winzige Inseln)
        return None
    flat = [ints[0][0], ints[0][1]]
    for (ax, ay), (bx, by) in zip(ints, ints[1:]):
        flat += [bx - ax, by - ay]
    return flat


def main(source):
    data = json.load(open(source, encoding="utf-8"))
    borders = {}
    for feature in data["features"]:
        props = feature["properties"]
        code = props.get("ISO_A2") if props.get("ISO_A2") not in (None, "-99") else props.get("ISO_A2_EH")
        if code in (None, "-99"):
            code = FALLBACK_CODES.get(props.get("ADMIN"))
        if not code:
            continue
        geometry = feature["geometry"]
        polygons = geometry["coordinates"] if geometry["type"] == "MultiPolygon" else [geometry["coordinates"]]
        for polygon in polygons:
            for ring in polygon:
                encoded = encode(simplify(ring, TOLERANCE))
                if encoded:
                    borders.setdefault(code, []).append(encoded)
    out = pathlib.Path(__file__).resolve().parent.parent / "borders.json"
    out.write_text(json.dumps(borders, separators=(",", ":"), sort_keys=True), encoding="utf-8")
    print(f"{out.name}: {len(borders)} Länder, {out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main(sys.argv[1])
