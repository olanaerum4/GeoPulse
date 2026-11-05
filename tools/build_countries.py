"""Builds data/world.json: the built-in country dataset GeoWawe uses when the
REST Countries API is unreachable (and as the instant first load otherwise).

Sources (npm packages, unpacked locally and passed as arguments):
  world-countries (mledoze/countries): names, capitals, regions, area, borders, independence
  country-json: population (2018), scaled to ~2024 with rough regional growth factors
Populations for the game's 50 core countries are overridden in index.html with 2024 figures.

Usage: python3 -I tools/build_countries.py <world-countries/countries.json> <country-json/src/country-by-population.json> data/world.json
"""
import json, sys, unicodedata

wc_path, pop_path, out = sys.argv[1:4]
wc = [c for c in json.load(open(wc_path, encoding="utf-8")) if c.get("independent")]
pop = json.load(open(pop_path, encoding="utf-8"))

def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return "".join(ch for ch in s if ch.isalnum())

names = {}
for c in wc:
    for s in [c["name"]["common"], c["name"]["official"], *c.get("altSpellings", [])]:
        names.setdefault(norm(s), c["cca2"])
ALIAS = {"cape verde": "CV", "czech republic": "CZ", "east timor": "TL", "ivory coast": "CI", "swaziland": "SZ",
         "macedonia": "MK", "the gambia": "GM", "gambia": "GM", "congo": "CG", "the democratic republic of congo": "CD",
         "democratic republic of the congo": "CD", "libyan arab jamahiriya": "LY", "micronesia, federated states of": "FM",
         "fiji islands": "FJ", "holy see (vatican city state)": "VA", "vatican city": "VA", "palestine": "PS",
         "russian federation": "RU", "syria": "SY", "turkey": "TR", "south korea": "KR", "north korea": "KP",
         "laos": "LA", "brunei": "BN", "bahamas": "BS", "moldova": "MD", "tanzania": "TZ", "vietnam": "VN",
         "iran": "IR", "bolivia": "BO", "venezuela": "VE", "kyrgyzstan": "KG", "slovakia": "SK", "myanmar": "MM",
         "saint kitts and nevis": "KN", "saint lucia": "LC", "saint vincent and the grenadines": "VC", "sao tome and principe": "ST"}
GROWTH = {"Africa": 1.16, "Asia": 1.06, "Europe": 1.00, "Americas": 1.05, "Oceania": 1.08, "Antarctic": 1.0}
region = {c["cca2"]: c["region"] for c in wc}
p = {}
unmatched = []
for row in pop:
    nm, v = row["country"], row.get("population")
    if not v:
        continue
    cc = ALIAS.get(nm.lower()) or names.get(norm(nm))
    if cc and cc in region:
        p[cc] = v * GROWTH.get(region[cc], 1.0)
    else:
        unmatched.append(nm)

rows = []
for c in sorted(wc, key=lambda c: c["name"]["common"]):
    cc = c["cca2"]
    if cc not in p or not c.get("area"):
        print("skip (no population/area):", cc, c["name"]["common"], file=sys.stderr)
        continue
    rows.append([cc, c["name"]["common"], (c.get("capital") or [""])[0], c["region"],
                 round(p[cc] / 1e6, 3), round(c["area"] / 1000, 5), len(c.get("borders", []))])
json.dump(rows, open(out, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(f"{len(rows)} countries -> {out}; unmatched population rows (territories etc.): {len(unmatched)}", file=sys.stderr)
