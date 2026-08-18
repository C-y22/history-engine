# The History Engine · Pool Completion & Diamond Re-pull Record (2026-08-15)

**Origin.** An audit of the H2a ablation found the main spec could score only 57/100 rows (43 lacked a China share), and that "invisibility-only 4/10" had been computed on a mismatched pool. This record closes out all 43 rows, then documents the diamond term-correction re-pull. Final numbers live in `docs/02_results_final_numbers.md`.

## Method: thresholds first

For every unscored row, compute the share it would need to enter any exam's top ten (threshold = that exam's 10th-place latent score ÷ the row's invisibility). Twelve rows (lime, cement, silicon, salt, mercury, PGM, …) cannot enter even at 100% — routine MCS values suffice. Only threshold-reachable rows required individual verification.

## Verification results (all pre-cutoff sources)

| Row | China share | Basis / source | Outcome |
|---|---|---|---|
| Wollastonite | **75.0%** | mine, 900/1,200 kt; MCS 2023 | enters exams A, B, C, E2 — never restricted = **the single false light** |
| Synthetic diamond | **~95%** | industry-sourced (USGS qualitative only); conclusions unchanged over 68–99% | enters every exam's top ten — restricted Oct 2025 = a hit |
| Magnesium compounds | 63.8% | mine (magnesite), 17,000/26,660 kt; MCS 2023 | enters E2 only |
| Abrasives / zeolites / kyanite / scandium | 54.3 / 5.2 / ~15 / ~68 | MCS 2022–23; scandium inferred | none enters |
| Thallium, cultured quartz, iron oxide pigments | **documented-NA** | USGS states data withheld / inadequate | dust-corner residents whose production nobody even publishes — itself evidence |

Remaining routine rows entered with MCS 2023 values (each noted with its threshold and "entry-insensitive"; spot-verify during writing). Final state: **88 valued + 11 documented-NA + 15 REE rows; all 22 restricted commodities scorable.**

## Author's ruling

"Use only the completed pool — the incomplete one was simply wrong." Main spec = completed pool, sole specification, no criticality eligibility gate (the 2022 critical-list gate survives as one robustness line).

## Diamond re-pull endgame (same evening; script 02f, 7 queries)

Corrected term ("industrial diamond" OR "synthetic diamond"): six pre-cutoff windows read **32/37/48/43/42/34 articles** (old term: 3–4); the **post-announcement 30-day window = 0**.

1. **Ranks settle.** Diamond falls #1 → **#7** in exam A but keeps a top-ten place in all six exams (E2 #5; the six-for-six sweep of ranks 1–6 holds); no hit count changes; wollastonite remains the only false light; invisibility-only ablation 5 → 4/10.
2. **The "vocabulary mismatch" story is half-refuted.** The pre-windows were a vocabulary problem (4 → 32); the post-window zero is a **real zero** — even under the corrected term, US media wrote nothing in the 30 days after the restriction, while the two listed producers returned +25% in five days. Diamond is reclassified from "measurement failure, excluded" to a genuine observation: the attention thermometer's ceiling counterexample, and the strongest exhibit for three-instrument complementarity.
3. **H2b attention recomputed (n=22 main; n=21 in parentheses).** Target median ×12.9 (placebos ×1.26; group contrast p<0.00001); unpreparedness-only ρ=0.66 (p=0.0005); share-only 0.09 n.s.; product 0.36 (p=0.051, marginal); quadrant contrast ×23.2 vs ×4.8 (p=0.0065); dark-vs-dark ×23.2 vs ×1.03.
4. **Downstream checks.** Coarse-data product 7/10 and no-REE 5/10 (p=3.3e-03) unchanged; normalizations hold (log 9 / linear 10 / percentile 9); the cap-85 sensitivity statement remains true.

## Cluster level (fold confirmed)

The fold (16 rows → one unit: 14 lanthanides + scandium + yttrium, max member score, unit removed after E1) was validated by exam-by-exam reproduction on the old pool. Final: A 6/10 (4.4e-04), B 4/10 (0.019), C 5/10 (9.5e-04), D 5/10 (4.1e-04), E1 2/10 (0.022), E2 1/10 n.s. (one positive left).

## File state

Final state lives in `data/history_engine_master_2026-08.xlsx` (13 sheets) and its flat export `data/sheets_csv/`: shares in `2_Shares`, rankings in `5_Rankings` with `diamond_term_corrected` source flags, the re-pull in `4b_Diamond_Repull`. Open items (none block writing): 12 spot-verify rows; exact kyanite figure; 02e resampling; term-lock sign-off.
