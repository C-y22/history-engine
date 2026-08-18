# The History Engine

*Research briefing for advisor meeting — Chunyang Zhang, August 2026*

## 1. The question

China's 98% share of low-purity gallium sat in USGS yearbooks for a decade — public, free. In the twenty-four months before the July 2023 export controls, an English-language news corpus carried 10,878 supply-chain articles on lithium and 3,675 on cobalt; gallium drew 394, germanium 75. Then Beijing put both under export licence, and in thirty days germanium drew 149 articles — a decade's worth of inattention undone in a month — while the Rotterdam price of gallium rose 43%. Neon in 2022 was the same story: half of semiconductor-grade supply ran through two purification firms in Mariupol and Odesa — a fact in the trade press and nowhere else until the missiles landed.

The question is how to find the parts of a supply chain that matter before someone uses them. Comparative advantage asks who produces most cheaply; criticality ratings ask which materials matter today. Neither asks how a node came to be where it is — and the ones that turn out to matter were usually built sideways, decades ago, inside somebody else's industry. China's gallium capacity was never a gallium investment: it is a circuit bolted onto alumina refineries, most of it installed before 2014, kept running through a 67% price collapse because nobody dismantles a line that costs nothing to keep. Nothing newsworthy ever happened, so nothing was ever written. History buries these nodes in the act of building them, and what is buried is not watched — which is also what makes it measurable, and what makes the map hold still long enough to be drawn.

This paper builds a framework from three axes and, more importantly, from the interaction between them. Criticality asks whether it hurts when cut. Visibility asks whether anyone is watching. Reflexivity asks whether the thing moves when you talk about it — a price hears a prediction, a refinery line does not — and so decides what can be predicted at all. None of the three is worth much alone: criticality by itself reproduces the watch-lists everyone already has, obscurity by itself returns dust. Crossed, they define a state space, and its most interesting region is the latent zone — important, unwatched, fixed in place — where supply-chain power sits until someone uses it. Scored this way, the full pool is graded against six rounds of Chinese export controls: on the eve of the first, nine of the top ten picks were commodities restricted twenty-one to twenty-seven months later. The claim is about where latent chokepoints sit, not about what Beijing restricts next.

## 2. Framework


Three axes, and the eight regions they define. 

| Axis | What it asks | How it is operationalized | Source / dialogue |
|---|---|---|---|
| **Criticality** | Does it hurt when cut? | Two rulers, both other people's numbers, both published before any of these controls existed: the USGS 2021 supply-risk score (available for 49 of the pool's rows), and China's production share taken at the stage where the restricted product is actually made — refining for gallium, separation for rare earths, mining for molybdenum. That choice of stage is mine, by a rule stated in advance and disclosed; the shares themselves come from USGS, DOE and SCRREEN. | Graedel et al. 2015; Nassar & Fortier 2021; DOE 2022; USGS MCS 2023; SCRREEN 2023 |
| **Visibility** | Is anyone watching? | Context-filtered article counts on Media Cloud's US national collection: 100 commodities × 6 cutoff dates = 600 cells, each a 24-month window ending the day before an announcement. Every query is `term AND (mining OR supply OR production OR export OR smelter OR refinery)`; 77 terms are the USGS commodity name verbatim, 23 depart from it under three mechanical rules — parenthetical or compound row names, multi-word phrases needing quotes, non-mineral ambiguity — none of which refers to any commodity's expected result. V = log1p(count) ÷ the largest log1p in the pool still uncontrolled at that cutoff; invisibility = 1 − V. | Farrell & Newman 2019 (from anecdote to a node-level variable); Roberts et al. 2021 (the instrument) |
| **Reflexivity** | Does the thing move when you talk about it? | Not scored, and not in any formula. It decides what kind of fact can be predicted at all: a price hears a forecast and adjusts, an installed refinery line does not. Mineral supply belongs to the second kind — output responds weakly to price, mines take five to fifteen years, and capacity outlives the conditions that justified it. The axis is therefore held fixed by the composition of the pool rather than measured within it, and it appears in the argument as a scope condition: predictions are made about structure — installed capacity, existing circuits, production shares — never about prices or the timing of policy. | Soros 2013; Merton 1948; Grunberg & Modigliani 1954; Lucas 1976; Hughes 1969; Berger & Luckmann 1966; Callon 1991 |

### 2.2 The state space: eight regions

Three binary axes give eight regions. Reflexivity splits them into the half this framework can work in and the half it cannot.

**Non-reflexive — structure that stays put. This is where the whole pool sits, and where the empirical test runs.**

| | invisible | visible |
|---|---|---|
| **high criticality** | **1 · Latent zone** — matters, unwatched, and cannot rearrange itself once found. The hunting ground: neon before 2022; the heavy rare earths before 2025, thulium among them at seventeen articles in two years. | **2 · Landmark zone** — matters, and everyone already knows. No information advantage: the risk is priced into everyone's planning. TSMC, Hormuz, ASML. |
| **low criticality** | **3 · Dust corner** — nobody watches because nobody needs it. The false-positive trap for any method that hunts obscurity alone: thallium, whose production nobody even publishes, and kyanite. | **4 · Bulk celebrities** — loud but not lethal. Widely sourced, substitutable, endlessly covered: gold, copper. |

**Reflexive — behaviour that answers back. Shown for completeness; the framework makes no claims here.**

| | invisible | visible |
|---|---|---|
| **high criticality** | **5 · Dark currents** — matters, unwatched, and moves the moment it is observed. Secret stockpiles, undisclosed contracts. public data cannot see it. | **6 · The arena** — matters, watched, and answers back. Prices, tariffs, exchange rates: the Lucas critique's home ground, and the reason economics is cautious about prediction. |
| **low criticality** | **7 · The whispers** — hidden, responsive, inconsequential. Small markets that move when noticed and matter to no one outside them. | **8 · The froth** — visible, responsive, and not load-bearing. Logically this cell exists; in commodities it is close to empty, and for an instructive reason. Capital mobilizes around believed importance, and in minerals belief stays anchored to real use, so hype cycles attach to materials that genuinely matter and the froth forms one layer up, in the equities and ventures built on top of them. The cell is named for completeness and carries no weight in the argument. |

### 2.3 Why the empirical work runs on two axes

The pool sits entirely in the first table. Reflexivity varies across domains, not inside this pool. Every row here is a physical mineral commodity: supply responds slowly to price, capacity is sunk, and what exists today was largely decided years ago. Gold is the clean illustration — the price quadrupled between 2005 and 2011 and mine output barely moved. A published map does not cause a refinery line to be built or torn out inside the horizon over which the map is being tested.

That has two consequences. It is a limitation: the framework has nothing to say about the reflexive half of the state space, where most of economics lives. And it is the enabling condition: because the objects hold still, a map drawn from public data in July 2023 can still be graded in October 2025. The empirical test therefore runs in the **visibility × criticality** plane, with reflexivity fixed; the theory uses the reflexivity × visibility plane, where hardening carries a node from the arena toward the landmark or latent zones as decisions turn into concrete (§2.4), and §8 returns to the axis to ask what happens as attention erodes the latent zone from the outside.

### 2.4 The score

**Latent power = criticality × invisibility × (1 − reflexivity)** — a ranking device, not a cardinal quantity.

The third factor is carried because the framework is meant to travel beyond minerals. In this pool it equals one for every row — mineral structure responds too slowly for a published map to move it — so it drops out of every number reported here and is never estimated.

The same score does two jobs: across the pool it ranks who holds power nobody has noticed (§5); among the commodities actually restricted, it predicts how hard the shock lands (§6).


### 2.5 What the framework adds

The three axes are borrowed; the arrangement is not. Each reads the same supply chain in a different tense. **Reflexivity is its past**: the structure it inherited and cannot quickly undo. **Visibility reads its present** — not a property of the material but a state of knowledge about it, and the only coordinate that can change in a week. **Criticality reads its trajectory** — which dependencies the economy has accumulated, a list that looks different every decade as technologies arrive and substitutes appear.

Existing instruments hold one axis and treat the others as fixed. Criticality assessment scores what a loss would cost, but treats that cost as a property of the material rather than of what is known about it. Weaponized interdependence establishes that network position is power, but its variables are topological: it does not ask whether anyone has noticed the position. The reflexivity literature, from Merton through Grunberg–Modigliani to Lucas, gives rules for when a forecast defeats itself, but none for which objects are slow enough to forecast safely. What this paper adopts is a restriction rather than a criterion: it predicts structural facts — installed capacity, existing circuits, production shares — and never prices or the timing of policy. In this domain the restriction costs little, because mineral structure moves slowly (§2.3).

Crossed, the three axes give eight regions, and the one this paper is about is the latent zone: critical without being watched. The claim is that the two measured coordinates have to be read together — a rating that ignores attention cannot tell a chokepoint from a landmark already priced in, and an attention measure that ignores consequence cannot tell one from dust.

## 3. Design and results

Three tests. H1 asks how a latent chokepoint gets built, and answers it with one commodity examined closely. H2a puts the classification against an answer key that reality supplies. H2b asks whether the same score explains how hard the shock lands, among the commodities that were used. The two large tests share their failures: graphite and molybdenum are the commodities the map did not place in the latent zone, and they are also the ones whose restriction produced almost no shock — being unremarkable beforehand explains both.

### H1 — why the structure holds still, and why nobody writes about it

Gallium is the case because its mechanism is observable, not because it scores highest. On the eve of the first announcement it ranked twentieth of eighty-eight: 394 supply-chain articles put it in the more-covered half of the pool, and the ten places above it went to darker things. What gallium has instead is a legible history — a single host process, twenty-one years of USGS capacity records, forty-four refineries whose retrofit dates can be checked one by one, and discharge permits that reveal a circuit whether or not its owner discusses it. Two questions follow: does this capacity respond to price at all, and if it does not, how did two decades of its accumulation stay out of the news?

**1. The time series: the structure does not respond.** Chinese gallium capacity, output and the low-grade price, together with host alumina output, reconstructed year by year for 2003–2023 on a single basis from the USGS Minerals Yearbook gallium chapters and the annual Mineral Commodity Summaries. Prices are the low-grade series throughout: crude gallium is what the by-product circuit produces and what the controls cover, while the high-purity series prices a separate downstream step.

Reported capacity never falls in any year of the series, from 40 t in 2003 to 1,000 t in 2023; output does. The hard case is 2011–16, when the price fell 67% (US$374 → 125/kg) and output fell 61% in a single year (444 t in 2015 to 171 t in 2016) while capacity sat at 600 t and later resumed climbing. Individual plants do exit — one refinery halted in 2019 and its host went into restructuring — but the lines stay installed and the national total does not move. The market adjusts the flow, not the stock. This is the scope condition of the whole framework, shown rather than assumed: an object that ignores a two-thirds price collapse will not rearrange itself because someone published a map of it.

**2. The plant census: how it accumulates.** Every Chinese alumina refinery at or above 0.8 Mt/yr — 44 of them — with the frame taken from three independent industry lists. Each row records the host's commissioning year, whether a gallium circuit exists, who operates it, its capacity, the installation year, how confident that date is, and the Chinese source text verbatim.

Twenty-three refineries run a circuit, three are verified to have none, and the rest cannot be settled from public sources. Twenty circuits carry a date: ten installed by 2015, eight from 2020 onward, two bracketed only as earlier than 2021, and none dated to the years between. The hand China played in 2023 was built in the first wave, when gallium was worthless. The lag can be extreme — Luoyang Xiangjiang Wanji commissioned its refinery in 2005 and its gallium circuit in 2025, and the filing states that it adds 60 t of gallium with alumina output unchanged. Nine circuits are run not by the refinery but by a third party inside it, six of those by a single specialist operator: the fixed cost never touches the host's books, installation is nearly free, and keeping the line costs almost nothing.

Sources are Chinese and first-hand — plant-anniversary features in the non-ferrous trade press, environmental filings and discharge permits, listed-company reports and exchange inquiry letters — cross-checked against USGS where an English record exists; anything unsettled stays blank rather than estimated.

**Why none of it became news.** A retrofit inside an existing refinery is not an investment story, an outsourced circuit does not appear in the host's capital spending, and a by-product has no market of its own to report. The measure makes this concrete: capacity rose from 650 t to 1,000 t in 2022 — the largest expansion in the entire series, more than half again — and the twenty-four months ending on the eve of the controls carried 394 supply-chain articles on gallium, fewer than antimony and a fraction of cobalt's. Leverage accumulated for two decades, and most visibly in the two years just before it was used, in the one place a news-based instrument cannot see it.

### H2a — the map test

H2a puts the classification against an answer key that reality supplies. A commodity placed under export control is one whose leverage has been confirmed by the party best placed to know; if the map measures leverage at all, such commodities should already be sitting in its latent zone before the announcement. What is tested is the classification, not any ability to anticipate policy.

**The pool.** All commodities in the 2023 Mineral Commodity Summaries chapter list, mapped to 86 commodity rows by a documented consolidation rule (Appendix A), plus 14 lanthanide rows — defined externally and used whole. Visibility is measured for all 100. Ninety-nine are scored and ranked; the "rare earths" chapter row is dropped at element level, since its members are already in the pool individually. Of those, 88 carry a China production share from a pre-cutoff source and 11 are documented-NA, cases where USGS states no data is published. All 22 commodities later restricted are scorable.

**The exams.** Every Chinese export-control announcement covering physical minerals between 2023 and 2025, verified one by one against the MOFCOM originals as a complete set.

| Exam | Announced | Official number | Restricted | Cutoff | Element level | Cluster level |
|---|---|---|---|---|---|---|
| A | 2023-07-03 | 2023 No. 23 | gallium, germanium | 2023-07-02 | **9/10** | 6/10 |
| B | 2023-10-20 | 2023 No. 39 | graphite (a tightening of 2006 controls) | 2023-10-19 | 9/10 | 4/10 |
| C | 2024-08-15 | 2024 No. 33 | antimony | 2024-08-14 | 9/10 | 5/10 |
| D | 2025-02-04 | 2025 No. 10 | tungsten, tellurium, bismuth, molybdenum, indium | 2025-01-31 | **10/10** | 5/10 |
| E1 | 2025-04-04 | 2025 No. 18 | samarium, gadolinium, terbium, dysprosium, lutetium, scandium, yttrium | 2025-04-01 | **10/10** | 2/10 |
| E2 | 2025-10-09 | 2025 Nos. 55–58, 61–62 | holmium, erbium, thulium, europium, ytterbium, synthetic diamond | 2025-10-08 | **all six positives took ranks 1–6** | 1/10 |

E1 and E2 are the two rare-earth rounds, graded separately; E2 bundles several announcement numbers issued the same day. D and E1 use cutoffs pulled back beyond the usual day-before, since both were embedded in retaliation packages foreseeable from US actions on 1 February and 2 April.

**Grading.** At each cutoff the pool is scored, the top ten taken, and a pick counts as a hit if that commodity is restricted then or later. Commodities already under control leave the pool.

**Two units of analysis.** At element level each of the sixteen rare-earth family members competes as its own candidate. At cluster level the family counts as one candidate, scored by its strongest member and removed once played at E1 — the reading for a critic who says the engine placed a single bet on rare earths and collected it many times. That corrects the counting, not the measurement; family-level measurement is tested by the coarse-share ablation below. Maximum, mean and median folds give identical results in all six exams.

**The headline.** On 2 July 2023, the day before the first announcement, the top ten read: thulium, holmium, ytterbium, erbium, europium, samarium, synthetic diamond, gadolinium, wollastonite, yttrium. Nine of those ten were restricted in 2025, twenty-one to twenty-seven months later. Rank nine is wollastonite — a 75%-share filler mineral on no critical list, never restricted, and the one false light on the record. It is the cost of running without a criticality gate, and it is where the dust corner reaches into the results.

**What each factor contributes** (exam A, matched pool of 88 scorable rows):

| Ruler | Rows ranked | Top ten later restricted |
|---|---|---|
| The engine — share × invisibility | 88 | **9/10**; ranks diamond 7th |
| Share alone, precise element-level data | 88 | **10/10** — one better, but ranks diamond 13th |
| Coarse group-level shares: product vs share alone | 88 | **7/10 vs 5/10** |
| Invisibility alone | 88 | 4/10 — the dust-corner trap |
| USGS supply-risk score alone (a different ruler, not an ablation) | 49 | 2/10 |

Precise share alone edges the engine by one, and that is reported as it stands. The product's contribution is ranking quality and robustness rather than the hit count: it places diamond seventh where share alone leaves it thirteenth, and when the shares coarsen to what is actually published at family level it holds 7/10 while share alone falls to 5/10. Separating the two factors is H2b's job.

**Is this just obvious?** Inside the rare-earth family share is nearly flat — every member sits between 88% and 99% — so share cannot order the family at all. What ordered it was coverage: thulium (17 articles) first, holmium (19) second, samarium (35) sixth, yttrium (73) tenth, while neodymium (255) and praseodymium (134) fell to twenty-first and seventeenth. Neodymium and praseodymium are the two most-covered rare earths, and the two that have never been restricted. Outside the family, dropping every rare earth still leaves 5/10 (p=3.3×10⁻³: diamond, bismuth, gallium, tungsten, germanium). And the obvious ruler — Washington's own supply-risk score — puts two of ten.

**Where the map missed.** Graphite was not latent: 1,601 articles before its exam, and a tightening rather than a new control. Molybdenum carries only a 40% share. Both are recovered in H2b as the quiet end of the gradient.

**One correction, under a result-blind rule.** Every query must cover the subcategory names in its own USGS chapter, with synonyms drawn only from USGS and HS descriptions. Across 100 rows the rule produces exactly one correction: synthetic diamond, whose frozen term missed the synthetic branch that the chapter treats alongside the natural one. Re-pulled, its pre-cutoff windows read 32–48 articles against 3–4 before; diamond moves to seventh in exam A, stays in every exam's top ten, and no hit count changes.

**Robustness.** Three normalizations on the completed pool (log 9/10, linear 10/10, percentile 9/10); a Wikipedia-pageview substitute performs worse, which is evidence about the construct; capping every inferred rare-earth share at 85% leaves nine of ten exam-A picks standing.

### H2b — the awakening test

The sample is the 22 commodities actually restricted, which conditions away the question of why Beijing chose them; what remains is whether the ones more latent beforehand were hit harder afterwards. Three instruments read each shock, and points with no reaction are pursued as hard as the dramatic ones — coverage of a commodity that did not move is scarce, so a sample built from what is easy to find would manufacture the correlation it reports.

| Instrument | Measure | Result |
|---|---|---|
| News | 30-day post-announcement count ÷ pre-event monthly mean | targets ×12.9 (n=22) vs 58 placebos ×1.26 (p<0.00001); latent half ×24.7 vs landmark half ×9.6 (median split, n=11/11, p=0.0105) |
| Stocks | five-day abnormal return vs CSI 300, pure-exposure A-shares, 24 ticker-events | ρ=0.54 with pre-event invisibility (p=0.004); Yunnan Germanium +37.8% |
| Prices | offshore price change; the domestic price falls when exports are blocked, so the offshore move is the power reading | product specification: one month ρ=0.89 (p=0.0008), longest window ρ=0.80 (p=0.002) |

**Which factor each instrument listens to** (Spearman ρ within the restricted; attention on the n=22 sample):

| Ruler | News (n=22) | Stocks (n=24/22) | Price, longest (n=12) | Price, 1 month (n=10) |
|---|---|---|---|---|
| Invisibility alone | **0.66** (p=0.0005) | **0.54** | 0.55 | 0.30 n.s. |
| Share alone | 0.09 n.s. | 0.28 n.s. | 0.61 | 0.82 |
| Product | 0.36 (p=0.051, marginal) | 0.51 | **0.80** | **0.89** |

News tracks invisibility alone — an information phenomenon, where the size of the reversal depends on how dark it was before. Prices track the full product — a physical phenomenon, where the supply must really be chokeable and nobody can have stockpiled. Stocks sit between. Tellurium and dysprosium were equally dark; tellurium at 53% share rose 7% in a month, dysprosium at 99% tripled.

**Inside a single announcement.** Gallium and germanium were restricted on the same day. Germanium had drawn 75 supply-chain articles in the preceding two years and gallium 394; afterwards germanium's coverage rose ×47.7 and gallium's ×9.3. One day, one announcement, and the darker of the two took the larger jolt — the gradient without any cross-event comparison.

**The counterexample.** Synthetic diamond drew zero articles in the thirty days after its restriction even under the corrected term. That is a real reading, not a missing one: some commodities never cross the newsroom threshold at all, and only the stock market priced it, the two listed producers returning +25% over five days. It is the clearest case for reading three instruments rather than one.

**Calibrations** (methods notes): a fixed-seed placebo draw shows announcement months do not lift news generally (×1.26); dark-against-dark shows the jump is not a small-baseline artifact (restricted dark commodities ×23.2 against equally dark unrestricted ones ×1.03).

## 4. H1 — sedimentation (gallium riding alumina)

| Fact | Number | Reading |
|---|---|---|
| Declines of Chinese gallium capacity, 21 yrs of USGS records | **0** | Capacity is a ratchet: the market adjusts flow, never stock. Sources: USGS Minerals Yearbook & MCS; Asian Metal/CNIA basis. |
| 2011→16: price / output / capacity | **−67% / −61% / 0** | |
| Host (alumina) growth over the period | **×19** | |

**44-plant census timeline** (frame: every refinery ≥0.8 Mt/yr, three independent lists):

**Wave 1 ≤2014** (fixed China's 2023 hand) → **2015–19: empty band** (price trough — not one new line) → **Wave 2 ≥2020** (prices recover and the controls light the map).

Key exhibits: Xiangjiang Wanji — refinery 2005, gallium line 2025, filing reads "adds 60 t gallium, alumina unchanged" (the circuit is a decision, not a chemical freebie). Fangyuan ran outsourced circuits at six sites: installing nearly free, keeping free, nothing gets torn out. Bridge to H2: stacking share inside a host generates no news — high criticality with low visibility is a manufactured equilibrium.

## 5. H2a — map test

**Procedure:** freeze data at announcement's eve → score the pool → take top ten → reality grades (precision@10 + specificity).

**Locks:** per-exam cutoffs (D/E1 pull back before the triggering US actions) · pool defined externally from the USGS list, nothing added or dropped · criticality imported from 2021 · queries generated by outcome-blind rules and audited.

**Pool, fully accounted for (completed Aug 15).** 100 externally defined rows. Visibility measured for all 100. Production share: 88 rows carry a value from a pre-cutoff source; 11 are documented-NA where USGS states no data exists (thallium — "most producers withhold production data"; cultured quartz crystal; iron oxide pigments; cesium; rubidium; thorium; gemstones; steel scrap; clays; sand and gravel; stone). All 22 restricted commodities are scorable. Remaining estimates are inventoried with sensitivity statements: twelve routine entries sit 2× or more below any entry threshold; the synthetic-diamond share (industry-sourced; USGS gives only "leading producer") leaves every conclusion unchanged anywhere from 68% to 99%; seven inferred rare-earth shares capped at 85% leave nine of ten exam-A picks standing.

| Exam | Date | Restricted | Element-level top-10 hits | Cluster-level (REE family = 1 unit) |
|---|---|---|---|---|
| A | 2023-07 | Ga, Ge | **9/10** (p=7.4×10⁻⁶) | **6/10** (p=4.4×10⁻⁴) |
| B | 2023-10 | graphite (tightened) | 9/10 (p=3.2×10⁻⁶) | 4/10 (p=0.019) |
| C | 2024-08 | antimony | 9/10 (p=2.0×10⁻⁶) | 5/10 (p=9.5×10⁻⁴) |
| D | 2025-02 | W, Te, Bi, Mo, In | **10/10** (p=1.6×10⁻⁸) | 5/10 (p=4.1×10⁻⁴) |
| E1 | 2025-04 | 7 rare earths (incl. Sc, Y) | **10/10** (p=2.0×10⁻¹⁰) | 2/10 (p=0.022) |
| E2 | 2025-10 | 5 rare earths + diamond | **all 6 restricted swept ranks 1–6** (p=1.3×10⁻⁶) | 1/10 (n.s.; one positive left) |

**Headline:** on July 2, 2023 — the day before the first announcement — the completed pool's top ten reads: thulium, holmium, ytterbium, erbium, europium, samarium, synthetic diamond (#7), gadolinium, wollastonite, yttrium. Nine of those ten were restricted in 2025, twenty-one to twenty-seven months later. Diamond appears in every exam's top ten and stands 5th at E2, where the engine's top six were exactly the six commodities announced. Rank 9 is wollastonite, the one false light — a 75%-share filler mineral on no critical list, the on-record cost of running without a criticality gate and a live demonstration of why the dust corner needs one. Nd/Pr never ranked and remain unrestricted.

**What each factor contributes (exam A, matched pool of 88 scorable rows):**

| Specification | Rows ranked | Top-10 later restricted |
|---|---|---|
| Full engine — share × invisibility | 88 | **9/10**; ranks diamond 7th |
| Share only, precise element-level data | 88 | **10/10** — one better on precision, but ranks diamond 13th |
| Coarse group-level shares: product vs share-only | 88 | **7/10 vs 5/10** — the product holds when the data coarsen |
| Invisibility only | 88 | 4/10 — the dust-corner trap |
| USGS supply-risk score only (a different ruler, not an ablation) | 49 | 2/10 |

**Reading, stated plainly.** On raw precision, precise share alone edges the product by one — reported as is. The product's value in H2a is ranking quality and robustness, not the hit count: the product ranks diamond 7th where share alone leaves it 13th, and on coarse share data the product holds 7/10 while share alone falls to 5/10. The separation of the two factors is H2b's job, and its ablation grid does it cleanly. Earlier versions (the 10/10 headline on the 57-row pool; diamond at #1 under the pre-correction term) are superseded and archived.

**Robustness:** three normalizations on the completed pool (log 9/10, linear 10/10, percentile 9/10); a Wikipedia-pageview substitute performs worse (construct validity); dropping the entire rare-earth family still yields 5/10 (p=3.3×10⁻³: diamond, bismuth, gallium, tungsten, germanium). Misses diagnosable: graphite not latent; molybdenum 40% share. **Fluorspar** — repeatedly top-five, untouched — remains the standing prediction, joined by wollastonite as its falsifying twin: if wollastonite is ever restricted the false light becomes a hit, and if fluorspar never is, the engine loses its bet. Both outcomes are written down.

## 6. H2b — awakening test

| Thermometer | Measure | Result |
|---|---|---|
| Attention jump | 30-day post-announcement context news ÷ pre-event monthly average (Media Cloud) | targets **×12.9** (n=22, diamond restored) vs 58 placebos ×1.26 (p<0.00001); latent ×24.7 vs landmark ×9.6 (median split of pre-event invisibility, n=11/11, p=0.0105; the earlier 0.564 threshold gives ×23.2 vs ×4.8, n=17/5, p=0.0065) |
| Stock CAR | 5-day abnormal return vs CSI 300, pure-exposure A-shares, 24 ticker-events | ρ=**0.54** with pre-event latency (p=0.004); Yunnan Germanium +37.8% |
| Commodity price | offshore price change (onshore–offshore gap = the power reading); Benchmark + archived quotes | product spec: 1-month ρ=**0.89** (p=0.0008); longest window ρ=0.80 (p=0.002) |

**Ablation grid** (Spearman ρ within restricted commodities; attention column shows the n=22 sample with the pre-correction n=21 value in parentheses):

| Ruler | Attention n=22 (n=21) | Stock CAR (n=24/22) | Price, longest (n=12) | Price, 1-month (n=10) |
|---|---|---|---|---|
| Unpreparedness only (1−V) | **0.66**, p=0.0005 (0.82) | **0.54** | 0.55 | 0.30 (n.s.) |
| Share only | 0.09, n.s. (0.12) | 0.28 (n.s.) | 0.61 | 0.82 |
| **Product: criticality × unpreparedness** | 0.36, p=0.051 (0.53) | 0.51 | **0.80** | **0.89** |

**Reading:** news listens to unpreparedness alone (information phenomenon); prices listen to the full product (physical phenomenon — chokeable supply and empty warehouses); stocks sit between. Tellurium and dysprosium were equally dark before their controls: tellurium at 53% share rose 7% in a month, dysprosium at 99% tripled. Diamond marks the attention thermometer's floor: even with the corrected term, US media wrote zero articles in the 30 days after its restriction — some commodities never cross the newsroom threshold, and only stocks priced it (+25%). The division of labor holds; its attention leg is softer with diamond in, and both samples are reported.

Calibrations (methods notes): fixed-seed placebo draw (announcement months do not lift news generally); dark-against-dark (dark restricted commodities ×23.2 vs equally dark unrestricted ones ×1.03 — no small-baseline artifact). The product specification was written in the design document before the test was run; a single-factor run of the same window (ρ=0.30, n.s.) is reported alongside it.

## 7. Instrument discipline

Queries are generated from the USGS row names by mechanical rules that never reference outcomes. Twenty-three of the 100 depart from the raw row name under three such rules — compound row names, multi-word phrasing, non-mineral ambiguity — and all 23 were audited afterwards for directional bias. None affects the headline result. Two are disclosed: the graphite override runs against the hypothesis; the magnesium override could favor it, but magnesium never enters any top ten.

One query failed and was corrected under a result-blind rule: every query must cover the subcategory names in its USGS chapter, with synonyms drawn only from USGS and HS descriptions. Synthetic diamond is the only correction the rule produces across all 100 rows. The corrected re-pull (Aug 15) read 32–48 articles per 24-month window against 3–4 under the old term: diamond drops from #1 to #7 in exam A but stays in every exam's top ten, and no hit count changes. Its post-announcement window read zero under the corrected term too — a real zero, not a vocabulary artifact — so diamond re-enters the attention sample as a genuine observation rather than a measurement failure. Per the author's ruling the corrected data are the main specification; the pre-correction version is reported as the disclosed alternative.

Seven exams verified against every MOFCOM announcement of 2023–25 as the complete set of physical mineral controls. Standing bets carry pass/fail conditions written in advance: fluorspar as the #1 prediction; wollastonite as the on-record false light; the suspension orders (2025 No. 70/72) expiring November 2026 as a dated second bet.

## 8. Status and three questions

Data are complete and final: the pool was closed out and the diamond term correction re-pulled on August 15; all six exams, the H2b attention sample, and every downstream statistic (quadrant contrasts, calibrations, robustness variants) are rerun on the corrected data. Writing starts now (9 sections, 5 figures, 3 tables).

1. Venue: IPE/political science, or does theory-plus-prediction fit a general-interest journal better?
2. Collaboration: inviting a computational co-author for replication/benchmark packaging, with theory and data complete — how should contributions be structured?
3. Standing predictions: main text or appendix — how to weigh a public bet's payoff against its risk?

## References

Berger, P. L., & Luckmann, T. (1966). *The Social Construction of Reality*. Anchor Books.

Callon, M. (1991). Techno-economic networks and irreversibility. In J. Law (Ed.), *A Sociology of Monsters*. Routledge.

Farrell, H., & Newman, A. L. (2019). Weaponized interdependence. *International Security*, 44(1), 42–79.

Graedel, T. E., et al. (2015). Criticality of metals and metalloids. *PNAS*, 112(14), 4257–4262.

Grunberg, E., & Modigliani, F. (1954). The predictability of social events. *Journal of Political Economy*, 62(6), 465–478.

Hughes, T. P. (1969). Technological momentum in history: Hydrogenation in Germany 1898–1933. *Past & Present*, 44, 106–132.

Lucas, R. E., Jr. (1976). Econometric policy evaluation: A critique. *Carnegie-Rochester Conference Series on Public Policy*, 1, 19–46.

Merton, R. K. (1948). The self-fulfilling prophecy. *Antioch Review*, 8(2), 193–210.

Nassar, N. T., & Fortier, S. M. (2021). *Methodology and technical input for the 2021 review and revision of the U.S. Critical Minerals List* (OFR 2021-1045). USGS. https://doi.org/10.3133/ofr20211045

Roberts, H., et al. (2021). Media Cloud: Massive open source collection of global news on the open web. *Proc. ICWSM*, 15.

Soros, G. (2013). Fallibility, reflexivity, and the human uncertainty principle. *Journal of Economic Methodology*, 20(4), 309–329.

## Data sources

**Public, downloadable:**

- USGS Mineral Commodity Summaries (2016–2024): https://www.usgs.gov/centers/national-minerals-information-center/mineral-commodity-summaries
- USGS Minerals Yearbook, gallium chapters 2002–2022: https://www.usgs.gov/centers/national-minerals-information-center/gallium-statistics-and-information
- USGS supply-risk scores: Nassar & Fortier (2021), https://doi.org/10.3133/ofr20211045
- U.S. DOE (Feb 2022), *Rare Earth Permanent Magnets: Supply Chain Deep Dive Assessment*: energy.gov
- SCRREEN factsheets: https://scrreen.eu/factsheets/
- Media Cloud: https://www.mediacloud.org
- Global Trade Alert control inventory (cross-check): https://globaltradealert.org/blog/chinese-export-controls-on-critical-raw-materials-inventory

**Press (verified copies of the two wire stories cited in §1):**

- Reuters (2022-03-11), "Ukraine halts half of world's neon output for chips, clouding outlook" — carried by CNN: https://edition.cnn.com/2022/03/11/tech/ukraine-neon-chips and CNBC: https://www.cnbc.com/2022/03/12/russias-attack-on-ukraine-halts-half-of-worlds-neon-output-for-chips.html
- Reuters (2023-07-04), "US firm AXT applying for permits after China restricts chipmaking exports" — carried by Malay Mail: https://www.malaymail.com/news/money/2023/07/04/us-firm-axt-applying-for-permits-after-china-restricts-chipmaking-exports/77754

**MOFCOM announcement originals (exam-defining; full 14-link archive in `data/evidence_manifest.csv`):**

- 2023 No. 23 (Ga/Ge): https://aqygzj.mofcom.gov.cn/qdml/art/2023/art_c2ae3d2061e14e97ba608de1ed565f78.html
- 2023 No. 39 (graphite): https://www.mofcom.gov.cn/zcfb/blgg/art/2023/art_f6b1bc49e2c8482f8eb749012bc66dec.html
- 2024 No. 33 (antimony): https://aqygzj.mofcom.gov.cn/qdml/art/2024/art_b907a108e35945db9f8b04e1ed77b659.html
- 2025 No. 10 (W/Te/Bi/Mo/In): https://www.mofcom.gov.cn/zwgk/zcfb/art/2025/art_e623090907fc4e1092f0a4db72f57b95.html
- 2025 No. 18 (7 heavy rare earths): https://www.mofcom.gov.cn/zwgk/zcfb/art/2025/art_9c2108ccaf754f22a34abab2fedaa944.html
- 2025 No. 55 (synthetic diamond): https://www.mofcom.gov.cn/zwgk/zcfb/art/2025/art_949f47563b834dad95b0010f375a892c.html
- 2025 No. 57 (5 rare earths): https://www.mofcom.gov.cn/zwgk/zcfb/art/2025/art_59ec4f6bec0b459aa4a30c4bbd0a41c1.html

**Licensed / market:** Benchmark Mineral Intelligence quarterly price assessments (licensed files on hand — percentage changes only are cited, raw points are not redistributed); SSE/SZSE daily quotes and CSI 300 (via Yahoo Finance API).

**Author datasets (this repository):** `data/history_engine_master_2026-08.xlsx` (13-sheet consolidated workbook; sheet `1_Results` holds all final numbers) with `docs/03_data_readme.md`; underlying CSVs in `data/`.
