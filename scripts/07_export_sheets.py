"""Export every sheet of the three hypothesis data packs to data/sheets_csv/ as flat CSVs.

The workbooks are the source of truth. Edit a workbook, re-run this script, commit both.
The 0_README sheet of each pack is documentation, not data, and is not exported.
"""
import csv
import pathlib

import openpyxl

WORKBOOKS = [
    pathlib.Path("data/H1_mechanism_data_2026-08.xlsx"),
    pathlib.Path("data/H2a_map_data_2026-08.xlsx"),
    pathlib.Path("data/H2b_awakening_data_2026-08.xlsx"),
]
OUTDIR = pathlib.Path("data/sheets_csv")
OUTDIR.mkdir(parents=True, exist_ok=True)

written = []
for path in WORKBOOKS:
    wb = openpyxl.load_workbook(path, data_only=True)
    for ws in wb.worksheets:
        if ws.title.startswith("0_"):
            continue
        target = OUTDIR / f"{ws.title}.csv"
        with target.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            for row in ws.iter_rows(values_only=True):
                writer.writerow(["" if cell is None else cell for cell in row])
        written.append(target.name)

print(f"{len(written)} sheets exported to {OUTDIR}/")
for name in sorted(written):
    print(" ", name)
