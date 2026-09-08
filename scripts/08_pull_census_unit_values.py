"""US import unit values for the commodities named in China's 2023-25 export controls.

Source: US Census Bureau international trade API, HS10 line items, general imports,
all countries, monthly. Free API key required; this script reads it from the
environment and never stores it:

    export CENSUS_API_KEY=...        never commit this
    python3 pull_census_unit_values.py

Output: data/us_import_unit_values.csv (month, hts10, commodity, value, quantity, unit value).

Coverage note: the twelve rare earths China restricted have NO individual HTS line.
US HTS 2805.30 breaks out only lanthanum, cerium, praseodymium and neodymium - the four
China never restricted - and pools everything else in "Other". USGS states the same in
Mineral Commodity Summaries 2026. This route therefore covers ten commodities, not 22.
"""
import csv
import json
import os
import pathlib
import time
import urllib.request

CODES = {
    "8112921000": "gallium",
    "8112926000": "germanium (unwrought)",
    "8112926500": "germanium (powders)",
    "8112923000": "indium",
    "8110100000": "antimony (unwrought/powder)",
    "8101940000": "tungsten (unwrought)",
    "2841800010": "tungsten APT",
    "2804500020": "tellurium",
    "8106100000": "bismuth (>99.99%)",
    "8102940000": "molybdenum (unwrought)",
    "2504101000": "graphite (crystalline flake)",
    "2504105000": "graphite (other natural)",
    "7104210000": "synthetic diamond (unworked)",
}
START, END = "2023-01", "2026-12"
OUT = pathlib.Path("data/us_import_unit_values.csv")

key = os.environ.get("CENSUS_API_KEY")
if not key:
    raise SystemExit("Set CENSUS_API_KEY first. Free key: https://api.census.gov/data/key_signup.html")

rows = []
for code, name in CODES.items():
    url = (
        "https://api.census.gov/data/timeseries/intltrade/imports/hs?"
        "get=I_COMMODITY,I_COMMODITY_LDESC,GEN_VAL_MO,GEN_QY1_MO,UNIT_QY1"
        f"&COMM_LVL=HS10&I_COMMODITY={code}&CTY_CODE=-"
        f"&time=from+{START}+to+{END}&key={key}"
    )
    with urllib.request.urlopen(url, timeout=120) as resp:
        payload = json.load(resp)
    header = payload[0]
    for raw in payload[1:]:
        rec = dict(zip(header, raw))
        try:
            value = float(rec["GEN_VAL_MO"])
            qty = float(rec["GEN_QY1_MO"])
        except (TypeError, ValueError):
            value = qty = 0.0
        rows.append([
            rec["time"], code, name, rec.get("I_COMMODITY_LDESC", ""),
            int(value), int(qty), rec["UNIT_QY1"],
            round(value / qty, 4) if qty > 0 else "",
        ])
    print(f"{code} {name}: {len(payload) - 1} months")
    time.sleep(1)

rows.sort(key=lambda r: (r[2], r[0]))
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["US general imports, all countries, monthly. Source: US Census Bureau "
                "international trade API, HS10 line items.", "", "", "", "", "", "", ""])
    w.writerow(["month", "hts10", "commodity", "census_description",
                "customs_value_usd", "quantity", "unit", "unit_value_usd_per_unit"])
    w.writerows(rows)
print(f"wrote {len(rows)} rows to {OUT}")
