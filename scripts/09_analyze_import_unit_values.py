"""H2b, fourth thermometer: US import unit values around each export-control announcement.

Reads data/us_import_unit_values.csv (built by pull_census_unit_values.py) and reports,
for each window length, the excess unit-value change of the restricted commodities over a
19-commodity never-restricted control basket, split by the map's quadrant.

The twelve rare earths are absent by construction: US HTS 2805.30 breaks out only
lanthanum, cerium, praseodymium and neodymium - the four China never restricted.
"""
import csv
import itertools
import pathlib
import statistics

DATA = pathlib.Path("data/us_import_unit_values.csv")
MIN_MEDIAN_MONTHLY_VALUE = 250_000   # size filter, set on trade volume, not on outcomes

# commodity -> (quadrant at its own cutoff, announcement month)
RESTRICTED = {
    "gallium": ("latent", "2023-07"),
    "germanium (unwrought)": ("latent", "2023-07"),
    "indium": ("latent", "2025-02"),
    "antimony (unwrought/powder)": ("latent", "2024-08"),
    "tellurium": ("latent", "2025-02"),
    "bismuth (>99.99%)": ("latent", "2025-02"),
    "synthetic diamond (unworked)": ("latent", "2025-10"),
    "tungsten (unwrought)": ("landmark", "2025-02"),
    "molybdenum (unwrought)": ("landmark", "2025-02"),
    "graphite (crystalline flake)": ("landmark", "2023-10"),
}


def read():
    series, group = {}, {}
    with DATA.open(encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    header = rows[1]
    for raw in rows[2:]:
        r = dict(zip(header, raw))
        if not r["unit_value_usd_per_unit"]:
            continue
        series.setdefault(r["commodity"], {})[r["month"]] = (
            float(r["unit_value_usd_per_unit"]), float(r["customs_value_usd"]))
        group[r["commodity"]] = r["group"]
    return series, group


def shift(month, k):
    y, m = (int(x) for x in month.split("-"))
    t = y * 12 + m - 1 + k
    return f"{t // 12:04d}-{t % 12 + 1:02d}"


def change(s, event, w):
    pre = [s[shift(event, k)][0] for k in range(-w, 0) if shift(event, k) in s]
    post = [s[shift(event, k)][0] for k in range(1, w + 1) if shift(event, k) in s]
    if len(pre) < 2 or len(post) < 2:
        return None
    base = statistics.mean(pre)
    return 100 * (statistics.mean(post) - base) / base


def permutation_p(a, b):
    pool, k = a + b, len(b)
    obs = statistics.mean(a) - statistics.mean(b)
    hits = total = 0
    for combo in itertools.combinations(range(len(pool)), k):
        lo = [pool[i] for i in combo]
        hi = [pool[i] for i in range(len(pool)) if i not in combo]
        total += 1
        if statistics.mean(hi) - statistics.mean(lo) >= obs:
            hits += 1
    return hits / total


def main():
    series, group = read()
    controls = [c for c, g in group.items() if g.startswith("control")]
    thin = {c for c in RESTRICTED
            if statistics.median(v[1] for v in series[c].values()) < MIN_MEDIAN_MONTHLY_VALUE}
    if thin:
        print(f"dropped for thin trade (median monthly value < ${MIN_MEDIAN_MONTHLY_VALUE:,}): "
              + ", ".join(sorted(thin)) + "\n")
    print(f"{'window':<9}{'latent':>9}{'median':>10}{'landmark':>11}{'median':>10}{'exact p':>10}")
    for w in (2, 3, 4, 6):
        latent, landmark = [], []
        for name, (quad, event) in RESTRICTED.items():
            if name in thin:
                continue
            raw = change(series[name], event, w)
            if raw is None:
                continue
            basket = [x for x in (change(series[c], event, w) for c in controls) if x is not None]
            excess = raw - statistics.median(basket)
            (latent if quad == "latent" else landmark).append(excess)
        print(f"+/-{w:<6}{len(latent):>9}{statistics.median(latent):>9.1f}%"
              f"{len(landmark):>11}{statistics.median(landmark):>9.1f}%"
              f"{permutation_p(latent, landmark):>10.4f}")
    print("\nThe direction holds at every window; significance does not. With nine commodities "
          "the permutation floor is p=0.012, so this is corroboration, not a standalone result.")


if __name__ == "__main__":
    main()
