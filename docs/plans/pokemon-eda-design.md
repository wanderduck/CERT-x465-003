# EDA Design: Deep Poking into Pokémon Data
**Date:** 2026-03-01
**Course:** CERT x465-003 — Data Interpretation and Application
**Assignment:** 03 (and supporting material for 05)
**Notebook target:** `CERT-x465-003_MAIN.ipynb` → Section 3.3

---

## Overview

An Exploratory Data Analysis (EDA) of the custom-built Pokémon dataset
(`data/pokemon_dataset_MASTER.csv`, 1,231 rows × 55 columns). The analysis
is organized into seven thematic questions plus an unsupervised machine
learning capstone. Sequencing follows analytical complexity — starting with
intuitive physical data, moving through stat architecture, then zooming out
to generational history, and landing on K-Means clustering as a synthesis.

**Format:** Long-form video presentation
**Narrative approach:** Follow the data's lead — no prescribed story arc;
each section reaches its own conclusions, with the clustering capstone as
a unifying synthesis.

---

## Dataset Snapshot

| Property | Value |
|---|---|
| Rows | 1,231 |
| Columns | 55 |
| Key column groups | Base stats, types, physical traits, evolution, legendary flag, derived ratios, role classification, stat tiers, z-scores |
| Source | Bulbapedia (base stats + individual pages), Pokémon Fandom Wiki (evolution chains), custom-scraped legendary list |

---

## Analysis Sections

---

### Section 1 — Q4: Body Composition and Combat Role
**Question:** Does physical body shape predict how a Pokémon fights?

**Columns used:** `BMI`, `Height (m)`, `Weight (kg)`, `Role`, `Type 1`, `Generation`

**Techniques:** Descriptive statistics, distribution analysis, grouped comparisons

| Visualization | Library |
|---|---|
| BMI distribution (histogram + KDE) | seaborn |
| BMI by Role (violin or box plot) | seaborn |
| Height vs. Weight scatter, colored by Type 1 (log scale) | plotly |
| BMI trend by Generation (bar or line) | seaborn |
| Outlier annotations (Cosmoem, Eternatus, etc.) | matplotlib |

**Expected finding:** High-BMI Pokémon cluster toward Physical Wall and Tank
roles. Ghost/Fairy types occupy the low-BMI extreme. BMI trends upward over
generations.

---

### Section 2 — Q5: Type Shapes Stat Identity, Not Just Stat Total
**Question:** Does a Pokémon's primary type determine its fighting personality
more than its raw power level?

**Columns used:** `Type 1`, `Type 2`, `Physical/Special`, `Offensive/Defensive`,
`Dual Type`, all six base stats

**Techniques:** Grouped comparison, radar profiles per type, mono vs. dual-type split

| Visualization | Library |
|---|---|
| Physical/Special ratio by Type 1 (horizontal bar, sorted) | seaborn |
| Offensive/Defensive ratio by Type 1 | seaborn |
| Stat "fingerprint" radar chart per type | matplotlib |
| Mono vs. dual-type stat profile comparison (violin) | seaborn |

**Expected finding:** Ghost/Psychic lean Special Offensive; Fighting/Rock lean
Physical; Steel/Water lean Defensive. Dual-typed Pokémon are statistically
more "average" in profile shape than mono-types.

---

### Section 3 — Q2: The Specialization Premium
**Question:** Do more powerful Pokémon pay for their power by becoming
one-dimensional?

**Columns used:** `Stat Std Dev`, `Stat Total`, `Stat Tier`, `Role`

**Techniques:** Scatter with regression overlay, correlation analysis

| Visualization | Library |
|---|---|
| Stat Std Dev vs. Stat Total (scatter + regression) | seaborn |
| Stat Std Dev by Stat Tier (box plot) | seaborn |
| Stat Std Dev by Role (violin plot) | seaborn |
| Correlation of Std Dev vs. each individual stat (heatmap) | seaborn |

**Expected finding:** "Very High" tier Pokémon have significantly higher Stat
Std Dev — the game rewards going all-in on one dimension. Tanks and Walls are
the exception: high total, lower Std Dev.

---

### Section 4 — Q7: The Speed-Bulk Tradeoff Across Generations
**Question:** Is the "fast = fragile" rule real in the data, and has it
intensified over time?

**Columns used:** `Speed`, `Defense`, `HP`, `Speed/Defense`, `Generation`,
`Speed Tier`, `Stat Tier`

**Techniques:** Correlation, generational faceting, regression per generation

| Visualization | Library |
|---|---|
| Speed vs. (Defense + HP) scatter, colored by Generation | plotly |
| Pearson r per generation (line chart) | matplotlib |
| Speed Tier × Stat Tier cross-tab heatmap | seaborn |
| Speed/Defense ratio by Generation (box plot, faceted) | seaborn |

**Expected finding:** Negative correlation exists and strengthens in Gen VI+.
Variance around the tradeoff also increases — newer Pokémon are designed more
extreme in both directions.

---

### Section 5 — Q1: Is Power Creep Asymmetric?
**Question:** Has offensive power inflated faster than defensive bulk
across nine generations?

**Columns used:** `Offensive Total`, `Defensive Total`, `Offensive/Defensive`,
`Stat Total`, `Generation`, all six base stats

**Techniques:** Time series comparison, distribution shift analysis

| Visualization | Library |
|---|---|
| Mean Offensive Total vs. Defensive Total by Generation (dual line) | matplotlib |
| Offensive/Defensive ratio trend by Generation | matplotlib |
| Stat Total distribution by Generation (ridge/joy plot or stacked box) | seaborn |
| Mean of each individual stat by Generation (faceted line chart) | seaborn |

**Expected finding:** Offensive Total has inflated more than Defensive Total
since Gen VI. The Gen III→IV spike is visible. Speed has become more bimodal
in later generations.

---

### Section 6 — Q3: Is the Legendary Gap Closing?
**Question:** Have ordinary Pokémon powered up enough that being Legendary
no longer signals exceptional strength?

**Columns used:** `Legendary`, `Stat Total`, `Generation`

**Techniques:** Group comparison over time, gap magnitude calculation

| Visualization | Library |
|---|---|
| Stat Total distributions: Legendary vs. Non-Legendary (violin) | seaborn |
| Mean Stat Total by Generation × Legendary (dual line) | matplotlib |
| Gap (mean_legendary − mean_non_legendary) per generation (bar chart) | seaborn |
| Top-50 non-legendary Stat Totals by generation (dot plot or stacked bar) | plotly |

**Expected finding:** The gap has measurably shrunk since Gen V.
Pseudo-legendaries and late-game ordinaries have crept into legendary
territory — the Legendary label has inflated alongside everything else.

---

### Section 7 — Q6: Does Evolution Preserve or Flip Combat Role?
**Question:** Is a Stage 1 Pokémon a miniature version of its final form,
or does evolution sometimes change the whole game plan?

**Columns used:** `Evolution Stage`, `Role`, `Physical/Special`,
`Offensive/Defensive`, all six base stats, `Pokemon` (for chain matching)

**Techniques:** Transition mapping, role distribution per stage, stat
growth rate analysis

| Visualization | Library |
|---|---|
| Role distribution at each Evolution Stage (grouped bar) | seaborn |
| Role transitions Stage 1→2 and 2→3 (Sankey/alluvial diagram) | plotly |
| Physical/Special ratio shift per Evolution Stage (box plot) | seaborn |
| Mean stat gain per stage, by stat type (faceted bar chart) | seaborn |

**Expected finding:** Most Pokémon preserve role through evolution. A
meaningful minority (~15–20%) flip — typically Balanced Stage 1s evolving
into Sweepers. Speed and the dominant offensive stat grow fastest.

---

### Section 8 — ML Capstone: Unsupervised Clustering
**Question:** Without using labels, can the data's own patterns rediscover
the role archetypes we defined — and reveal unexpected groupings?

**Columns used:** `HP_zscore`, `Attack_zscore`, `Defense_zscore`,
`Speed_zscore`, `Special_Attack_zscore`, `Special_Defense_zscore`
(plus `Role`, `Legendary`, `Generation` for post-hoc labeling)

**Techniques:** K-Means clustering, PCA dimensionality reduction,
silhouette scoring

| Analysis | Visualization | Library |
|---|---|
| Elbow method (inertia vs. K) | Line chart | matplotlib |
| Silhouette scores for candidate K values | Bar chart | sklearn / matplotlib |
| K-Means fit on 6 z-score columns | — | sklearn |
| PCA 2-component projection, colored by cluster | 2D scatter | plotly |
| Cluster vs. Role label comparison | Confusion-style heatmap | seaborn |
| Notable Pokémon callouts in each cluster | Annotated scatter | plotly |

**Expected finding:** 5–7 clusters emerge, roughly corresponding to the
`Role` column with some informative splits — Legendaries may form a
cluster independent of role; HP-heavy tanks may separate from
Defense-heavy tanks.

---

## Visualization Library Summary

| Library | Primary Use |
|---|---|
| seaborn | Static distributions, box/violin plots, heatmaps, grouped comparisons |
| matplotlib | Line charts, time series, subplot grids, annotations |
| plotly | Interactive scatter plots, Sankey diagrams, generational drill-downs |
| sklearn | K-Means, PCA, silhouette scoring |

---

## Constraints and Decisions

- **No prescribed narrative arc** — sections are self-contained; conclusions
  emerge from the data rather than being forced into a story.
- **Long-form video format** — no compression needed; each section gets full
  treatment.
- **Variations included** — the dataset includes Mega, Regional, and other
  variant forms (flagged via `Is Variation`). Analyses should note where
  variants skew results and optionally filter to base forms for clean
  comparisons.
- **Cluster labeling is post-hoc** — `Role` was derived from rule-based
  logic; the clustering section intentionally ignores it during fitting and
  compares afterward to validate (or challenge) the manual classification.
