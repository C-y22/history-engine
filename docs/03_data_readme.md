# The History Engine — Master Data Workbook README (final basis, 2026-08-15)

**One file**: `history_engine_master_2026-08.xlsx`, 12 sheets. This README documents each sheet's source, basis, and every computation. The loose CSVs in `data/` remain as replication-package originals; the workbook is their consolidated view. **Where numbers conflict, the workbook (= final basis) governs.** `ranking_unified_v1.csv` and `archive_v0/` are historical archives — do not cite.

## Sheet map

| Sheet | Contents | Source |
|---|---|---|
| **1_Results** | All final result numbers (corrected-diamond basis) (H2a element/cluster/ablation; H2b thermometers/ablation grid) | Computed from sheets 2–12; methods below |
| 2_Shares | China production share, non-REE commodities (85: 80 valued + 11 documented-NA) | USGS MCS 2023 primarily (MCS 2022/2020 fallbacks noted per row); numerator/denominator kept in notes |
| 3_REE_Shares | Rare-earth element shares, dual basis (mine / separation) | DOE Feb-2022 REPM Deep Dive; USGS MCS 2023; SCRREEN 2023; 7 rows flagged INFERRED |
| 4_Visibility | Context-filtered news counts, 600 cells (100 commodities × 6 cutoffs, 24-month windows) | Media Cloud API; queries per term_map_lock.md v1.1 |
| 5_Rankings | H2a final rankings, completed pool (6 exams × 99 rows, per-row source flags) | Computed from sheets 2, 3, 4 |
| 6_AnswerKey | Seven exams: announcement/effective dates, official numbers, positives, cutoffs | MOFCOM originals, checked number by number (complete-set audit 2026-08-12); Chinese official designations kept verbatim |
| 7_H2b_Attention | Attention jump: 30-day post-announcement counts ÷ pre-event monthly baseline (21 targets + 58 placebos + dark-vs-dark) | Media Cloud; placebo seed 20260813 |
| 8_H2b_Stocks | Stock BHAR[0,+5] vs CSI 300, 24 ticker-events | SSE/SZSE daily quotes via Yahoo Finance API |
| 9_H2b_Prices | Offshore price changes (1-month n=10, longest n=12), point-level sourcing | Benchmark Mineral Intelligence (licensed) + archived quotes (Wayback) |
| 10_H1_Plants | 44 alumina refineries: host start-up year × gallium-line year, cell-level sources | EIA filings, listed-company disclosures, China Nonferrous Metals News, SHFE brand list, Mysteel capacity tables; Chinese source text kept verbatim |
| 11_H1_Series | Figure 1 series: alumina output / Ga capacity & output / Ga price, single basis | USGS Minerals Yearbook Ga chapters 2002–2022, MCS 2016–2024; production basis Asian Metal/CNIA |
| 12_Pool_USGS | Pool definition (100 rows) + USGS 2021 supply-risk scores + 2022 critical-list flags | USGS MCS commodity list (86 + 14 lanthanides); scores from Nassar & Fortier 2021, Fig. 3 |

## Methods (everything behind 1_Results and 5_Rankings)

**Visibility.** V = log1p(context count) ÷ max log1p within the pool still uncontrolled at that cutoff. Log because counts span five orders of magnitude; per-exam max-normalization makes the six exams comparable and immune to secular growth in news volume. Invisibility = 1 − V.

**Latent score (main spec)** = (China share / 100) × (1 − V). Both factors on 0–1; the score ranks only — its magnitude has no cardinal meaning. Rare earths use the separation basis.

**Grading.** Each exam: top ten by latent score, graded against the answer key ("later restricted" = hit). Already-controlled commodities are removed from pool and ranking at each cutoff; ties broken alphabetically.

**Significance.** Hypergeometric exact test: population = scorable live pool (N), successes = later-restricted within it (K), draw 10, upper-tail probability of the observed hits.

**Cluster level.** The 16-member REE family (14 lanthanides + scandium + yttrium; the separate 'rare earths' chapter row is not scored) folds into one candidate scored by its best member; the unit is removed after it is played at E1. The fold was validated by reproducing the Aug-12 original record exam by exam (A–E1 exact).

**Ablation.** Each single-factor ruler ranks the same matched pool of 88 scorable rows. Coarse variant = all 15 REE element shares set to the group proxy of 70.

**H2b.** Attention = 30-day post-announcement context count ÷ pre-event 24-month monthly mean; group contrasts by medians + permutation tests. Stocks = 5-day buy-and-hold abnormal return vs CSI 300 from the market-aligned event day. Prices = offshore price change (the domestic price falls when exports are blocked, so the onshore–offshore gap is the power reading). Associations with pre-event latency: Spearman rank correlation + one-sided permutation tests (small-sample robust; no regression).

## Data-quality tiers (read before citing)

1. **Measured / official** (the large majority): USGS, DOE, SCRREEN, MOFCOM originals, exchange quotes — sourced row by row.
2. **Documented-NA** (11 rows): thallium (USGS: "most producers withhold production data"), cultured quartz, iron oxide pigments, cesium, rubidium, thorium, gemstones, steel scrap, clays, sand & gravel, stone — no data exists officially; these are not gaps in collection.
3. **Inferred** (7 REE rows + scandium): deduced from the processing chain (same ionic-clay route; DOE records separation ≈100% in China). Sensitivity: capping all inferred shares at 85% leaves 9 of 10 exam-A picks unchanged.
4. **Industry-sourced** (synthetic diamond, 95%): USGS gives only "leading producer; 3–5 countries = 99%"; the figure comes from pre-2023 China Superhard Materials Association / industry filings. Sensitivity: every conclusion unchanged for any value from 68% to 99%.
5. **Routine, spot-verify** (12 rows, flagged in sheet 2 notes): shares sit ≥2× below any entry threshold; even if wrong they change no number. Verify during the writing phase.

## Version history (against mis-citation)

- **2026-08-15 (evening)**: diamond term-correction re-pull completed (7 queries, corrected term). Pre-cutoff counts 32–48 vs 3–4 under the old term: diamond drops #1 → #7 in exam A but stays in every exam's top ten; no hit count changes; E2's six positives still sweep ranks 1–6. The post-announcement window read zero under the corrected term too — a real zero, so diamond re-enters the attention sample (n=22; median ×12.9; unpreparedness ρ 0.82→0.66, p=0.0005; quadrant contrast ×23.2 vs ×4.8, p=0.0065; both samples reported). Corrected data are the main specification per author's ruling.
- **2026-08-15**: pool completed; main spec switched to the completed pool (author's ruling). Exam A 9/10 with wollastonite the single false light; E2 swept ranks 1–6. Cluster fold codified and validated.
- 2026-08-13: 57-row-era final (10/10 ×5) — superseded; archived in ranking_unified_v1.csv and the H2-audit doc.
- 2026-08-12: complete-set audit + significance tests + locked normalization (archive_v0/ holds the three older rankings).
- Term-map lock v1.1 (2026-08-15): rule (d) vocabulary-validity check added; synthetic diamond the only correction; per author's ruling the corrected data are the main specification, with the frozen version reported as the disclosed alternative.

## Open items (none block writing)

02e resampling check (author runs); term-lock sign-off; spot-verify the 12 flagged rows; exact kyanite figure; design-doc revision 8.
