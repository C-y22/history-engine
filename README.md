# The History Engine

Latent supply-chain chokepoints: a sedimentation mechanism builds them (H1), public data maps them years ahead (H2a), and the intensity of an awakening follows criticality × unpreparedness (H2b).

**Chunyang Zhang** · The University of Texas at Austin · first published 2026-08-16

> **Work in progress — the paper is being written; this repository is the data and method record behind it.**
> Data are complete and final as of 2026-08-15 (completed pool, corrected diamond term). Documents here are working documents, not a manuscript. Findings may be refined; every revision is in the commit history.
>
> **Citation.** Zhang, Chunyang (2026). *The History Engine: latent supply-chain chokepoints.* https://github.com/C-y22/history-engine
>
> **Standing predictions are on the record as of this repository's publication date** — fluorspar as the #1 forward prediction, wollastonite as the on-record false light, and the MOFCOM 2025 No. 70/72 suspensions expiring November 2026. They were written before the outcomes were known, and the commit history is the timestamp.
>
> Licensing: code MIT, data and documents CC BY 4.0 — see `LICENSE`. Correspondence: dorazhang0322@gmail.com

## Where things are

| Path | What it is |
|---|---|
| `docs/01_advisor_briefing.md` | The argument in full, cited. Start here. |
| `docs/02_results_final_numbers.md` | **Single source of truth for every number.** |
| `docs/03_data_readme.md` | Sources, computation methods, and the five data-quality tiers. Read before citing any figure. |
| `docs/04_research_design_v2.4.2.md` | Design ledger, all eight revisions. |
| `docs/05_term_map_lock_v1.1.md` | Visibility-query rules, rule (d), adversarial audit, revision log. |
| `docs/06_pool_completion_and_diamond_repull.md` | What was completed, what was re-pulled, what changed downstream. |
| `docs/11_paper_skeleton.md` | Section-by-section writing plan. |
| `data/history_engine_master_2026-08.xlsx` | The 13-sheet consolidated workbook. |
| `data/sheets_csv/` | Each workbook sheet as a flat CSV — generated from the workbook by `scripts/07_export_sheets.py`, so git can diff the data line by line. **The workbook is the source: edit it, re-run the script, commit both.** |
| `data/H1_mechanism_data_2026-08.xlsx` | H1 data pack — the USGS series, the 44-refinery census, the discharge-permit panel and the two USGS facility lists, each sheet carrying its own source column. |
| `data/` | Everything that is not a workbook sheet: the 100-row term map, the term-map lock, the discharge-permit panel, the two USGS facility lists, the evidence manifest. |
| `figures/` | Five self-contained HTML figures; open in a browser. |
| `scripts/` | Collection and verification scripts (`02f` is the diamond re-pull). |
| `deck/` | 16-slide English advisor deck. |
| `records_zh/` | The author's original Chinese working records, kept verbatim. |

**Where numbers conflict, `docs/02` and the workbook govern.** Any 57-row-era number is retired — do not cite.

## Headline results

- **H2a, element level:** A 9/10 (p=7.4e-06), B 9/10 (3.2e-06), C 9/10 (2.0e-06), D 10/10 (1.6e-08), E1 10/10 (2.0e-10); at E2 the six positives sweep ranks 1–6 (1.3e-06). Wollastonite is the single false light on the record.
- **H2a, cluster level:** A 6/10, B 4/10 (p=0.019), C 5/10, D 5/10 significant; E1/E2 degrade, reported as-is.
- **H2b:** price product spec ρ=0.89 at one month (p=0.0008), 0.80 at the longest window; attention is unpreparedness alone (ρ=0.66, p=0.0005, n=22; the product is 0.36, marginal at p=0.051); stocks in between (0.54, p=0.004). Quadrant contrast: the more latent half of the restricted commodities jumped ×24.7 against ×9.6 for the rest (median split, n=11/11, p=0.0105).

## Figures

| File | Figure |
|---|---|
| `figures/h1_sedimentation.html` | Figure 1 — sedimentation evidence (the ratchet) |
| `figures/h1_vintage_en.html` | Figure 2 — the two waves, 44 plants |
| `figures/engine_interactive_en.html` | **Interactive evidence** — H1 the ratchet and the plant timeline, H2a the map at six cutoffs, H2b the three thermometers; click any point for its formula and a link to the data row |
| `figures/h2b_activation_en.html` | Figure 4 — latent power vs one-month offshore price change, ρ=0.89 |
| `figures/h2b_division_en.html` | Figure 5 — division of labour across the three thermometers (n=22 basis) |

## Reproducing the data collection

The visibility and attention scripts need a Media Cloud API token in the environment; nothing is stored in this repository.

```bash
export MC_API_TOKEN=...          # never commit this
python scripts/02c_visibility_mediacloud.py     # 600-cell visibility panel
python scripts/02d_attention_activation.py      # H2b attention jumps
python scripts/02f_diamond_repull.py            # rule-(d) diamond correction
python scripts/02e_resample_verify.py           # stability check, seed 20260814
python3 scripts/07_export_sheets.py              # re-export the workbook to data/sheets_csv/
```

## Standing bets on the record

Fluorspar is the #1 forward prediction; wollastonite is the on-record false light of the betting pair; the MOFCOM 2025 No. 70/72 suspensions expire November 2026.

## Open items (none block writing)

02e resampling check; term-lock sign-off; spot-verify the 12 flagged share rows; exact kyanite figure.

## Data use

USGS, DOE, SCRREEN and MOFCOM material is public and cited per row. Benchmark Mineral Intelligence data are licensed: only percentage changes are reported here, never raw price points. Media Cloud counts are derived measurements, not article text.
