# Pokémon EDA Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement the eight-section EDA (+ ML clustering capstone) into `CERT-x465-003_MAIN.ipynb`, producing the full set of visualizations and analyses designed in `docs/plans/2026-03-01-pokemon-eda-design.md`.

**Architecture:** Each section is a self-contained block of Jupyter cells (one markdown header + 2–4 code cells) appended after the existing scraping/cleaning content in `CERT-x465-003_MAIN.ipynb`. The dataset is fully pre-built at `data/pokemon_dataset_MASTER.csv` (1,231 rows × 55 columns) — no data engineering required here.

**Tech Stack:** pandas, numpy, seaborn, matplotlib, plotly (express + graph_objects), scikit-learn (KMeans, PCA, silhouette_score)

---

## Notes for the Implementer

- All cells go into **`CERT-x465-003_MAIN.ipynb`**, appended after the last existing content cell.
- The notebook uses `NotebookEdit` with `edit_mode=insert` to add cells after a target `cell_id`.
- The last existing cell ID is `28d671325d378c6c` (empty markdown `###`). The first new cell goes after this.
- "Verification" in this plan = `assert` statements confirming data shape/columns before plotting — analogous to failing tests. If an assert fails, diagnose the data issue before proceeding.
- `uv run jupyter lab` launches the environment.
- GPU acceleration cells (`%load_ext cudf.pandas`) already exist at the top of the notebook — do NOT add them again.

---

## Task 1: EDA Setup — Imports and Dataset Load

**Files:**
- Modify: `CERT-x465-003_MAIN.ipynb` (append cells after `28d671325d378c6c`)

### Step 1: Add the EDA section markdown header cell

Insert after cell `28d671325d378c6c`:

```markdown
### **3.3.iii)** Exploratory Data Analysis (EDA)

---

#### EDA Overview
- This section contains the full Exploratory Data Analysis for Assignment 03.
- The dataset used is `pokemon_dataset_MASTER.csv` (1,231 rows × 55 columns), custom-built from scraped Bulbapedia and Pokémon Fandom Wiki data.
- Eight thematic questions are explored, followed by an unsupervised machine learning clustering capstone.
```

### Step 2: Add the EDA imports and data load code cell

```python
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')

# Consistent style across all seaborn/matplotlib plots
sns.set_theme(style='darkgrid', palette='viridis')
plt.rcParams['figure.dpi'] = 120
plt.rcParams['figure.figsize'] = (12, 6)

STAT_COLS = ['HP', 'Attack', 'Defense', 'Speed', 'Special Attack', 'Special Defense']
ROLE_ORDER = ['Physical Sweeper', 'Special Sweeper', 'Mixed Attacker',
              'Balanced', 'Tank', 'Physical Wall', 'Special Wall']
PCT_COLS   = ['HP_pct', 'Attack_pct', 'Defense_pct',
              'Speed_pct', 'Special_Attack_pct', 'Special_Defense_pct']
ZSCORE_COLS = ['HP_zscore', 'Attack_zscore', 'Defense_zscore',
               'Speed_zscore', 'Special_Attack_zscore', 'Special_Defense_zscore']

DATA_DIR = os.path.expanduser(
    '~/000_Duckspace/WanderduckDevelopment/Ducks/UMN/CERT-x465-003/data/'
)
pokes = pd.read_csv(DATA_DIR + 'pokemon_dataset_MASTER.csv')
```

### Step 3: Add the data verification cell

```python
# --- Dataset Verification ---
assert pokes.shape == (1231, 55), f"Expected (1231, 55), got {pokes.shape}"
assert 'BMI' in pokes.columns,          "Missing column: BMI"
assert 'Role' in pokes.columns,         "Missing column: Role"
assert 'Stat Std Dev' in pokes.columns, "Missing column: Stat Std Dev"
assert 'Legendary' in pokes.columns,    "Missing column: Legendary"
assert 'Evolution Stage' in pokes.columns, "Missing column: Evolution Stage"
for col in ZSCORE_COLS:
    assert col in pokes.columns, f"Missing z-score column: {col}"

print(f"Dataset loaded: {pokes.shape[0]} rows × {pokes.shape[1]} columns")
print(f"\nRole distribution:\n{pokes['Role'].value_counts().to_string()}")
print(f"\nMissing values in key columns:\n"
      f"{pokes[['BMI','Role','Stat Std Dev','Legendary','Evolution Stage']].isna().sum().to_string()}")
```

**Expected output:** No AssertionError. Shape `(1231, 55)`. Role counts matching the Phase 2 output from `dataScrapersCleanersExpanders_notebook.ipynb`.

### Step 4: Commit

```bash
git add CERT-x465-003_MAIN.ipynb
git commit -m "feat: add EDA section header, imports, and data verification"
```

---

## Task 2: Section 1 — Body Composition and Combat Role (Q4)

**Files:**
- Modify: `CERT-x465-003_MAIN.ipynb`

### Step 1: Add section markdown header cell

```markdown
### **3.3.iii.1)** Section 1: Body Composition and Combat Role

---
**Question:** Does a Pokémon's physical body shape (BMI, height, weight) predict how it fights?
```

### Step 2: Add BMI distribution cell and verify

```python
# --- 1a: BMI Distribution ---
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.histplot(pokes['BMI'].clip(upper=200), bins=60, kde=True,
             ax=axes[0], color='steelblue')
axes[0].set_title('BMI Distribution (clipped at 200)')
axes[0].set_xlabel('BMI')

bmi_filtered = pokes[pokes['BMI'] < 200]
sns.histplot(bmi_filtered['BMI'], bins=60, kde=True,
             ax=axes[1], color='coral')
axes[1].set_title('BMI Distribution (BMI < 200)')
axes[1].set_xlabel('BMI')

plt.suptitle("Pokémon BMI Distribution", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

print("\nTop 10 highest-BMI Pokémon:")
print(pokes.nlargest(10, 'BMI')[
    ['Pokemon', 'Type 1', 'Height (m)', 'Weight (kg)', 'BMI', 'Role']
].to_string(index=False))
```

**Verify:** Right-skewed histogram with a long tail. Cosmoem should appear at the top of the outlier list (extremely small, extremely heavy).

### Step 3: Add BMI by Role violin plot cell

```python
# --- 1b: BMI by Combat Role ---
fig, ax = plt.subplots(figsize=(12, 6))
bmi_data = pokes[pokes['BMI'] < 200].copy()

sns.violinplot(
    data=bmi_data,
    x='Role', y='BMI',
    order=ROLE_ORDER,
    palette='Set2',
    inner='box',
    ax=ax
)
ax.set_title('BMI Distribution by Combat Role', fontsize=14, fontweight='bold')
ax.set_xlabel('Combat Role')
ax.set_ylabel('BMI')
ax.tick_params(axis='x', rotation=30)
plt.tight_layout()
plt.show()
```

### Step 4: Add Height vs. Weight interactive scatter cell

```python
# --- 1c: Height vs Weight scatter (log scale, interactive) ---
fig = px.scatter(
    pokes[pokes['BMI'] < 500],
    x='Height (m)', y='Weight (kg)',
    color='Type 1',
    hover_name='Pokemon',
    hover_data=['BMI', 'Role', 'Generation'],
    log_x=True, log_y=True,
    title='Height vs. Weight by Primary Type (log-log scale)',
    template='plotly_dark',
    opacity=0.7
)
fig.show()
```

### Step 5: Add BMI by Generation bar chart cell

```python
# --- 1d: Median BMI by Generation ---
gen_bmi = pokes.groupby('Generation')['BMI'].median().reset_index()

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=gen_bmi, x='Generation', y='BMI', palette='viridis', ax=ax)
ax.set_title('Median Pokémon BMI by Generation', fontsize=14, fontweight='bold')
ax.set_xlabel('Generation')
ax.set_ylabel('Median BMI')
plt.tight_layout()
plt.show()

print("\nMedian BMI per Generation:")
print(gen_bmi.to_string(index=False))
```

**Verify:** An upward trend in median BMI across generations (consistent with published research).

### Step 6: Commit

```bash
git add CERT-x465-003_MAIN.ipynb
git commit -m "feat: EDA Section 1 — body composition and combat role (BMI analysis)"
```

---

## Task 3: Section 2 — Type Shapes Stat Identity (Q5)

**Files:**
- Modify: `CERT-x465-003_MAIN.ipynb`

### Step 1: Add section markdown header cell

```markdown
### **3.3.iii.2)** Section 2: Type Shapes Stat Identity, Not Just Stat Total

---
**Question:** Does a Pokémon's primary type determine its fighting personality more than its raw power level?
```

### Step 2: Add Physical/Special and Offensive/Defensive ratio bar charts cell

```python
# --- 2a: Combat ratio profiles by Type 1 ---
type_ps  = pokes.groupby('Type 1')['Physical/Special'].median().sort_values()
type_od  = pokes.groupby('Type 1')['Offensive/Defensive'].median().sort_values()

fig, axes = plt.subplots(1, 2, figsize=(16, 8))

type_ps.plot(kind='barh', ax=axes[0], color='steelblue')
axes[0].axvline(1.0, color='red', linestyle='--', linewidth=1.5, label='Balanced (1.0)')
axes[0].set_title('Median Physical/Special Ratio by Type', fontweight='bold')
axes[0].set_xlabel('Physical / Special')
axes[0].legend()

type_od.plot(kind='barh', ax=axes[1], color='coral')
axes[1].axvline(1.0, color='red', linestyle='--', linewidth=1.5, label='Balanced (1.0)')
axes[1].set_title('Median Offensive/Defensive Ratio by Type', fontweight='bold')
axes[1].set_xlabel('Offensive / Defensive')
axes[1].legend()

plt.suptitle('Combat Personality by Primary Type', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.show()
```

**Verify:** Fighting/Rock types at the Physical/Special high end; Ghost/Psychic at the low end. Steel/Water near the bottom of Offensive/Defensive.

### Step 3: Add radar "fingerprint" chart cell

```python
# --- 2b: Stat fingerprint radar charts (6 focal types) ---
FOCUS_TYPES = ['Ghost', 'Psychic', 'Fighting', 'Rock', 'Steel', 'Dragon']
labels = ['HP', 'Attack', 'Defense', 'Speed', 'Sp. Atk', 'Sp. Def']
N = len(labels)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

fig, axes = plt.subplots(2, 3, figsize=(15, 10), subplot_kw=dict(polar=True))
axes = axes.flatten()

for i, ptype in enumerate(FOCUS_TYPES):
    means = pokes[pokes['Type 1'] == ptype][PCT_COLS].mean().values.tolist()
    means += means[:1]
    axes[i].plot(angles, means, 'o-', linewidth=2)
    axes[i].fill(angles, means, alpha=0.25)
    axes[i].set_xticks(angles[:-1])
    axes[i].set_xticklabels(labels)
    axes[i].set_title(f'{ptype} Type', fontweight='bold', pad=15)
    axes[i].set_ylim(0, 0.25)

plt.suptitle('Stat Profile "Fingerprint" by Type (% of Stat Total)',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

### Step 4: Add mono vs. dual type comparison cell

```python
# --- 2c: Does dual typing affect stat profile shape? ---
pokes['Type Label'] = pokes['Dual Type'].map({True: 'Dual Type', False: 'Mono Type'})

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

sns.violinplot(data=pokes, x='Type Label', y='Physical/Special',
               palette='Set1', inner='box', ax=axes[0])
axes[0].axhline(1.0, color='black', linestyle='--', linewidth=1.2)
axes[0].set_title('Physical/Special by Type Count', fontweight='bold')

sns.violinplot(data=pokes, x='Type Label', y='Offensive/Defensive',
               palette='Set1', inner='box', ax=axes[1])
axes[1].axhline(1.0, color='black', linestyle='--', linewidth=1.2)
axes[1].set_title('Offensive/Defensive by Type Count', fontweight='bold')

plt.suptitle('Does Dual Typing Affect Stat Identity?', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

print("\nMedian ratios — Mono vs. Dual Type:")
print(pokes.groupby('Type Label')[['Physical/Special', 'Offensive/Defensive']].median().round(3).to_string())
```

### Step 5: Commit

```bash
git add CERT-x465-003_MAIN.ipynb
git commit -m "feat: EDA Section 2 — type shapes stat identity (radar + ratio charts)"
```

---

## Task 4: Section 3 — The Specialization Premium (Q2)

**Files:**
- Modify: `CERT-x465-003_MAIN.ipynb`

### Step 1: Add section markdown header cell

```markdown
### **3.3.iii.3)** Section 3: The Specialization Premium

---
**Question:** Do more powerful Pokémon pay for their power by becoming one-dimensional?
```

### Step 2: Add Stat Std Dev vs. Stat Total scatter cell

```python
# --- 3a: Stat Std Dev vs. Stat Total ---
tier_map = {'Low': 0, 'Mid': 1, 'High': 2, 'Very High': 3}
colors_num = pokes['Stat Tier'].map(tier_map).fillna(0)

fig, ax = plt.subplots(figsize=(12, 7))
scatter = ax.scatter(
    pokes['Stat Total'], pokes['Stat Std Dev'],
    c=colors_num, cmap='RdYlGn', alpha=0.5, s=20
)
m, b = np.polyfit(
    pokes['Stat Total'].fillna(0),
    pokes['Stat Std Dev'].fillna(0), 1
)
x_line = np.linspace(pokes['Stat Total'].min(), pokes['Stat Total'].max(), 200)
ax.plot(x_line, m * x_line + b, 'r--', linewidth=2,
        label=f'Regression (slope = {m:.4f})')
plt.colorbar(scatter, ax=ax, label='Stat Tier (0=Low → 3=Very High)')
ax.set_xlabel('Stat Total')
ax.set_ylabel('Stat Std Dev  (higher = more specialized)')
ax.set_title('Does Higher Power = Greater Specialization?',
             fontsize=14, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.show()

r = np.corrcoef(
    pokes['Stat Total'].fillna(0),
    pokes['Stat Std Dev'].fillna(0)
)[0, 1]
print(f"Pearson r (Stat Total vs. Stat Std Dev): {r:.4f}")
```

**Verify:** Positive slope and r > 0.4 expected.

### Step 3: Add Stat Std Dev by Tier and Role cell

```python
# --- 3b: Stat Std Dev by Stat Tier and by Role ---
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

sns.boxplot(
    data=pokes, x='Stat Tier', y='Stat Std Dev',
    order=['Low', 'Mid', 'High', 'Very High'],
    palette='RdYlGn', ax=axes[0]
)
axes[0].set_title('Stat Std Dev by Stat Tier', fontweight='bold')
axes[0].set_xlabel('Stat Tier')
axes[0].set_ylabel('Stat Std Dev')

sns.violinplot(
    data=pokes, x='Role', y='Stat Std Dev',
    order=ROLE_ORDER, palette='Set2', inner='box', ax=axes[1]
)
axes[1].tick_params(axis='x', rotation=30)
axes[1].set_title('Stat Std Dev by Combat Role', fontweight='bold')
axes[1].set_xlabel('Role')
axes[1].set_ylabel('Stat Std Dev')

plt.suptitle('The Specialization Premium', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

print("\nMean Stat Std Dev by Stat Tier:")
print(pokes.groupby('Stat Tier')['Stat Std Dev'].mean().reindex(
    ['Low', 'Mid', 'High', 'Very High']
).round(2).to_string())
```

### Step 4: Commit

```bash
git add CERT-x465-003_MAIN.ipynb
git commit -m "feat: EDA Section 3 — specialization premium (Stat Std Dev analysis)"
```

---

## Task 5: Section 4 — The Speed-Bulk Tradeoff (Q7)

**Files:**
- Modify: `CERT-x465-003_MAIN.ipynb`

### Step 1: Add section markdown header cell

```markdown
### **3.3.iii.4)** Section 4: The Speed-Bulk Tradeoff Across Generations

---
**Question:** Is "fast = fragile" a real design rule in the data, and has it intensified over time?
```

### Step 2: Add bulk column and interactive scatter cell

```python
# --- 4a: Speed vs. Bulk interactive scatter ---
pokes['Bulk'] = pokes['HP'] + pokes['Defense'] + pokes['Special Defense']

assert pokes['Bulk'].isna().sum() == 0, "Bulk has unexpected NaNs"

fig = px.scatter(
    pokes,
    x='Speed', y='Bulk',
    color='Generation',
    color_continuous_scale='Viridis',
    hover_name='Pokemon',
    hover_data=['Role', 'Stat Total', 'Type 1'],
    trendline='ols',
    title='Speed vs. Bulk (HP + Defense + Sp. Def) — colored by Generation',
    template='plotly_dark',
    opacity=0.6
)
fig.show()

r_speed_bulk = pokes[['Speed', 'Bulk']].corr().iloc[0, 1]
print(f"Overall Pearson r (Speed vs. Bulk): {r_speed_bulk:.4f}")
```

**Verify:** Negative correlation (r < 0).

### Step 3: Add correlation-per-generation line chart cell

```python
# --- 4b: Speed-Bulk Pearson r by Generation ---
gen_corrs = (
    pokes.groupby('Generation')
    .apply(lambda df: df['Speed'].corr(df['Bulk']))
    .reset_index(name='Pearson_r')
)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(gen_corrs['Generation'], gen_corrs['Pearson_r'],
        'o-', color='steelblue', linewidth=2, markersize=8)
ax.axhline(0, color='black', linestyle='--', linewidth=1)
ax.set_title('Speed–Bulk Correlation by Generation\n(More Negative = Stronger Tradeoff)',
             fontweight='bold')
ax.set_xlabel('Generation')
ax.set_ylabel("Pearson r")
ax.set_xticks(range(1, 10))
plt.tight_layout()
plt.show()

print("\nPearson r per Generation:")
print(gen_corrs.to_string(index=False))
```

### Step 4: Add Speed/Defense ratio box plots cell

```python
# --- 4c: Speed/Defense ratio distribution by Generation ---
fig, ax = plt.subplots(figsize=(14, 6))
sns.boxplot(
    data=pokes, x='Generation', y='Speed/Defense',
    palette='viridis', showfliers=False, ax=ax
)
ax.set_title('Speed/Defense Ratio Distribution by Generation',
             fontsize=14, fontweight='bold')
ax.set_xlabel('Generation')
ax.set_ylabel('Speed / Defense')
plt.tight_layout()
plt.show()
```

### Step 5: Commit

```bash
git add CERT-x465-003_MAIN.ipynb
git commit -m "feat: EDA Section 4 — speed-bulk tradeoff across generations"
```

---

## Task 6: Section 5 — Is Power Creep Asymmetric? (Q1)

**Files:**
- Modify: `CERT-x465-003_MAIN.ipynb`

### Step 1: Add section markdown header cell

```markdown
### **3.3.iii.5)** Section 5: Is Power Creep Asymmetric?

---
**Question:** Has offensive power inflated faster than defensive bulk across nine generations?
```

### Step 2: Add generational aggregation and dual line chart cell

```python
# --- 5a: Offensive vs. Defensive totals by generation ---
gen_stats = pokes.groupby('Generation').agg(
    Offensive_Mean=('Offensive Total', 'mean'),
    Defensive_Mean=('Defensive Total', 'mean'),
    StatTotal_Mean=('Stat Total', 'mean'),
    OffDef_Ratio=('Offensive/Defensive', 'mean'),
    **{f'{s}_Mean': (s, 'mean') for s in STAT_COLS}
).reset_index()

assert len(gen_stats) == 9, f"Expected 9 generations, got {len(gen_stats)}"

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

axes[0].plot(gen_stats['Generation'], gen_stats['Offensive_Mean'],
             'o-', color='tomato', label='Offensive Total', linewidth=2)
axes[0].plot(gen_stats['Generation'], gen_stats['Defensive_Mean'],
             'o-', color='steelblue', label='Defensive Total', linewidth=2)
axes[0].set_title('Mean Offensive vs. Defensive Total by Generation', fontweight='bold')
axes[0].set_xlabel('Generation')
axes[0].set_ylabel('Mean Partial Stat Total')
axes[0].legend()
axes[0].set_xticks(range(1, 10))

axes[1].plot(gen_stats['Generation'], gen_stats['OffDef_Ratio'],
             'o-', color='goldenrod', linewidth=2)
axes[1].axhline(1.0, color='black', linestyle='--', linewidth=1.2)
axes[1].set_title('Mean Offensive/Defensive Ratio by Generation', fontweight='bold')
axes[1].set_xlabel('Generation')
axes[1].set_ylabel('Ratio  (>1 = more offensive)')
axes[1].set_xticks(range(1, 10))

plt.suptitle('Is Power Creep Asymmetric?', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

### Step 3: Add per-stat inflation faceted chart cell

```python
# --- 5b: Which individual stats inflated most? ---
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes = axes.flatten()
colors = sns.color_palette('tab10', 6)

for i, stat in enumerate(STAT_COLS):
    col = f'{stat}_Mean'
    axes[i].plot(gen_stats['Generation'], gen_stats[col],
                 'o-', color=colors[i], linewidth=2)
    axes[i].set_title(f'Mean {stat} by Generation', fontweight='bold')
    axes[i].set_xlabel('Generation')
    axes[i].set_ylabel(f'Mean {stat}')
    axes[i].set_xticks(range(1, 10))

plt.suptitle('Which Stats Inflated Most? (Power Creep by Stat)',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

### Step 4: Add Stat Total distribution box plots cell

```python
# --- 5c: Stat Total distribution per generation (box plots) ---
fig, ax = plt.subplots(figsize=(14, 6))
sns.boxplot(
    data=pokes, x='Generation', y='Stat Total',
    palette='viridis', showfliers=False, ax=ax
)
ax.set_title('Stat Total Distribution by Generation',
             fontsize=14, fontweight='bold')
ax.set_xlabel('Generation')
ax.set_ylabel('Stat Total')
plt.tight_layout()
plt.show()

print("\nMean Stat Total per Generation:")
print(gen_stats[['Generation', 'StatTotal_Mean']].round(1).to_string(index=False))
```

### Step 5: Commit

```bash
git add CERT-x465-003_MAIN.ipynb
git commit -m "feat: EDA Section 5 — asymmetric power creep across generations"
```

---

## Task 7: Section 6 — Is the Legendary Gap Closing? (Q3)

**Files:**
- Modify: `CERT-x465-003_MAIN.ipynb`

### Step 1: Add section markdown header cell

```markdown
### **3.3.iii.6)** Section 6: Is the Legendary Gap Closing?

---
**Question:** Have ordinary Pokémon powered up enough that Legendary status no longer signals exceptional strength?
```

### Step 2: Add overall Legendary vs. Non-Legendary violin cell

```python
# --- 6a: Stat Total — Legendary vs Non-Legendary ---
leg_counts = pokes['Legendary'].value_counts()
assert True in leg_counts.index, "No Legendary=True rows found"

fig, ax = plt.subplots(figsize=(10, 6))
sns.violinplot(
    data=pokes, x='Legendary', y='Stat Total',
    palette={True: 'gold', False: 'steelblue'},
    inner='box', ax=ax
)
ax.set_xticklabels(['Non-Legendary', 'Legendary'])
ax.set_title('Stat Total: Legendary vs. Non-Legendary',
             fontsize=14, fontweight='bold')
ax.set_xlabel('')
ax.set_ylabel('Stat Total')
plt.tight_layout()
plt.show()

print("\nStat Total summary by Legendary status:")
print(pokes.groupby('Legendary')['Stat Total']
      .agg(['mean', 'median', 'std', 'min', 'max'])
      .round(1).to_string())
```

### Step 3: Add gap-over-generations dual line + bar chart cell

```python
# --- 6b: Legendary gap by generation ---
gen_leg = (
    pokes.groupby(['Generation', 'Legendary'])['Stat Total']
    .mean()
    .unstack('Legendary')
    .rename(columns={False: 'Non-Legendary', True: 'Legendary'})
)
gen_leg['Gap'] = gen_leg['Legendary'] - gen_leg['Non-Legendary']

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

gen_leg[['Non-Legendary', 'Legendary']].plot(
    ax=axes[0], marker='o', linewidth=2,
    color={'Non-Legendary': 'steelblue', 'Legendary': 'gold'}
)
axes[0].set_title('Mean Stat Total by Generation', fontweight='bold')
axes[0].set_xlabel('Generation')
axes[0].set_ylabel('Mean Stat Total')
axes[0].set_xticks(range(1, 10))

gen_leg['Gap'].plot(ax=axes[1], kind='bar', color='darkorange', edgecolor='black')
axes[1].axhline(0, color='black', linestyle='--')
axes[1].set_title('Legendary Stat Gap by Generation\n(Legendary − Non-Legendary mean)',
                  fontweight='bold')
axes[1].set_xlabel('Generation')
axes[1].set_ylabel('Stat Total Gap')
axes[1].tick_params(axis='x', rotation=0)

plt.suptitle('Is the Legendary Gap Closing?', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

print("\nLegendary gap per generation:")
print(gen_leg['Gap'].round(1).to_string())
```

### Step 4: Add top-50 non-legendary interactive chart cell

```python
# --- 6c: Where do the top-50 non-legendary Pokémon come from? ---
top50_nonleg = pokes[~pokes['Legendary']].nlargest(50, 'Stat Total')

fig = px.strip(
    top50_nonleg,
    x='Generation', y='Stat Total',
    color='Type 1',
    hover_name='Pokemon',
    hover_data=['Role', 'Is Variation', 'Stat Tier'],
    title='Top 50 Non-Legendary Pokémon by Stat Total',
    template='plotly_dark'
)
fig.show()

print("\nTop 50 non-legendaries — generation breakdown:")
print(top50_nonleg['Generation'].value_counts().sort_index().to_string())
```

### Step 5: Commit

```bash
git add CERT-x465-003_MAIN.ipynb
git commit -m "feat: EDA Section 6 — legendary gap closing over generations"
```

---

## Task 8: Section 7 — Evolution Role Stability (Q6)

**Files:**
- Modify: `CERT-x465-003_MAIN.ipynb`

### Step 1: Add section markdown header cell

```markdown
### **3.3.iii.7)** Section 7: Does Evolution Preserve or Flip Combat Role?

---
**Question:** Is a Stage 1 Pokémon a miniature version of its final form, or does evolution sometimes change the whole game plan?
```

### Step 2: Add role distribution by evolution stage bar chart cell

```python
# --- 7a: Role distribution at each Evolution Stage ---
evo_pokes = pokes[pokes['Evolution Stage'] > 0].copy()
assert len(evo_pokes) > 0, "No evolving Pokémon found"

role_by_stage = (
    evo_pokes.groupby(['Evolution Stage', 'Role'])
    .size()
    .unstack('Role')
    .fillna(0)
)

fig, ax = plt.subplots(figsize=(14, 6))
role_by_stage[ROLE_ORDER].plot(kind='bar', stacked=True,
                                colormap='Set2', ax=ax)
ax.set_title('Role Distribution by Evolution Stage',
             fontsize=14, fontweight='bold')
ax.set_xlabel('Evolution Stage')
ax.set_ylabel('Count')
ax.legend(title='Role', bbox_to_anchor=(1.05, 1))
ax.tick_params(axis='x', rotation=0)
plt.tight_layout()
plt.show()
```

### Step 3: Add role-transition heatmaps cell

```python
# --- 7b: Role transition heatmaps ---
def build_transition_matrix(df, from_stage, to_stage):
    """Build a Role→Role transition count matrix across an evolution step."""
    stage_from = (df[df['Evolution Stage'] == from_stage]
                  [['Pokemon', 'Role']].rename(columns={'Role': 'From Role'}))
    stage_to   = (df[df['Evolution Stage'] == to_stage]
                  [['Pokemon', 'Role']].rename(columns={'Role': 'To Role'}))
    merged = stage_from.merge(stage_to, on='Pokemon')
    matrix = (merged.groupby(['From Role', 'To Role'])
              .size()
              .unstack('To Role')
              .fillna(0))
    return matrix.reindex(index=ROLE_ORDER, columns=ROLE_ORDER, fill_value=0)

trans_1_2 = build_transition_matrix(evo_pokes, 1, 2)
trans_2_3 = build_transition_matrix(evo_pokes, 2, 3)

fig, axes = plt.subplots(1, 2, figsize=(18, 7))

sns.heatmap(trans_1_2, annot=True, fmt='.0f', cmap='Blues', ax=axes[0])
axes[0].set_title('Role Transitions: Stage 1 → Stage 2', fontweight='bold')
axes[0].set_xlabel('Stage 2 Role')
axes[0].set_ylabel('Stage 1 Role')

sns.heatmap(trans_2_3, annot=True, fmt='.0f', cmap='Greens', ax=axes[1])
axes[1].set_title('Role Transitions: Stage 2 → Stage 3', fontweight='bold')
axes[1].set_xlabel('Stage 3 Role')
axes[1].set_ylabel('Stage 2 Role')

plt.suptitle('Does Evolution Flip Combat Role?', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

# Role-preservation rate
total_1_2  = trans_1_2.values.sum()
preserved  = sum(trans_1_2.iloc[i, i] for i in range(len(ROLE_ORDER)))
print(f"\nStage 1→2 role preservation rate: {preserved/total_1_2:.1%}")
```

**Verify:** Diagonal values dominate (most roles preserved). Non-zero off-diagonal cells show flips.

### Step 4: Add stat growth per stage cell

```python
# --- 7c: Mean stat growth per evolution step ---
stat_by_stage = evo_pokes.groupby('Evolution Stage')[STAT_COLS].mean()
stat_delta    = stat_by_stage.diff().dropna()
stat_delta.index = ['Stage 1→2', 'Stage 2→3']

fig, ax = plt.subplots(figsize=(12, 6))
stat_delta.T.plot(kind='bar', ax=ax, colormap='Set1', width=0.8)
ax.set_title('Mean Stat Growth Per Evolution Step',
             fontsize=14, fontweight='bold')
ax.set_xlabel('Stat')
ax.set_ylabel('Mean Increase')
ax.legend(title='Transition')
ax.tick_params(axis='x', rotation=30)
plt.tight_layout()
plt.show()

print("\nMean stat gain per evolution step:")
print(stat_delta.round(1).to_string())
```

### Step 5: Commit

```bash
git add CERT-x465-003_MAIN.ipynb
git commit -m "feat: EDA Section 7 — evolution role stability and stat growth"
```

---

## Task 9: ML Capstone — Unsupervised Clustering

**Files:**
- Modify: `CERT-x465-003_MAIN.ipynb`

### Step 1: Add section markdown header cell

```markdown
### **3.3.iii.8)** Section 8: ML Capstone — Unsupervised Clustering

---
**Question:** Without using any labels, can the data's own patterns rediscover the role archetypes we defined — and reveal unexpected groupings?

**Method:** K-Means clustering on the six z-score stat columns, visualized via PCA dimensionality reduction.
```

### Step 2: Add elbow method and silhouette scoring cell

```python
# --- 8a: Choosing K — Elbow + Silhouette ---
cluster_df = pokes.dropna(subset=ZSCORE_COLS).copy()
X = cluster_df[ZSCORE_COLS].values

assert X.shape[0] > 100, "Too few rows after dropping NaN — check ZSCORE_COLS"

inertias    = []
silhouettes = []
K_range     = range(2, 13)

for k in K_range:
    km  = KMeans(n_clusters=k, random_state=42, n_init=10)
    lbl = km.fit_predict(X)
    inertias.append(km.inertia_)
    silhouettes.append(silhouette_score(X, lbl))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].plot(list(K_range), inertias, 'o-', color='steelblue', linewidth=2)
axes[0].set_title('Elbow Method (Inertia vs. K)', fontweight='bold')
axes[0].set_xlabel('Number of Clusters (K)')
axes[0].set_ylabel('Inertia')

axes[1].plot(list(K_range), silhouettes, 'o-', color='coral', linewidth=2)
axes[1].set_title('Silhouette Score vs. K', fontweight='bold')
axes[1].set_xlabel('Number of Clusters (K)')
axes[1].set_ylabel('Silhouette Score')

plt.suptitle('Choosing the Optimal K', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

best_k = list(K_range)[silhouettes.index(max(silhouettes))]
print(f"Best K by silhouette: {best_k}  (score: {max(silhouettes):.4f})")
```

### Step 3: Add K-Means fit and PCA projection cell

```python
# --- 8b: Fit K-Means and project via PCA ---
CHOSEN_K = best_k  # override manually if desired after reviewing elbow plot

km_final = KMeans(n_clusters=CHOSEN_K, random_state=42, n_init=10)
cluster_df['Cluster'] = km_final.fit_predict(X)

pca = PCA(n_components=2, random_state=42)
components = pca.fit_transform(X)
cluster_df['PC1'] = components[:, 0]
cluster_df['PC2'] = components[:, 1]

print(f"Cluster sizes (K={CHOSEN_K}):")
print(cluster_df['Cluster'].value_counts().sort_index().to_string())
print(f"\nPCA explained variance: "
      f"PC1={pca.explained_variance_ratio_[0]:.1%}, "
      f"PC2={pca.explained_variance_ratio_[1]:.1%}")

fig = px.scatter(
    cluster_df,
    x='PC1', y='PC2',
    color=cluster_df['Cluster'].astype(str),
    hover_name='Pokemon',
    hover_data=['Role', 'Type 1', 'Legendary', 'Stat Total', 'Generation'],
    title=f'K-Means Clusters (K={CHOSEN_K}) — PCA Projection',
    template='plotly_dark',
    opacity=0.7
)
fig.show()
```

**Verify:** Clusters are visually separable in 2D PCA space. PC1+PC2 explain at least 60% of variance.

### Step 4: Add cluster vs. role heatmap cell

```python
# --- 8c: How well do data-driven clusters match rule-based roles? ---
cross = pd.crosstab(cluster_df['Cluster'], cluster_df['Role'])[ROLE_ORDER]

fig, ax = plt.subplots(figsize=(14, 6))
sns.heatmap(cross, annot=True, fmt='d', cmap='Blues', ax=ax)
ax.set_title(f'K-Means Cluster vs. Role Label (K={CHOSEN_K})',
             fontsize=14, fontweight='bold')
ax.set_xlabel('Role (rule-based label)')
ax.set_ylabel('Cluster (data-driven)')
plt.tight_layout()
plt.show()
```

### Step 5: Add cluster stat profile bar chart cell

```python
# --- 8d: What does each cluster "look like" statistically? ---
cluster_profiles = cluster_df.groupby('Cluster')[STAT_COLS].mean()

fig, ax = plt.subplots(figsize=(14, 6))
cluster_profiles.T.plot(kind='bar', ax=ax, colormap='tab10', width=0.8)
ax.set_title('Mean Base Stats per Cluster',
             fontsize=14, fontweight='bold')
ax.set_xlabel('Stat')
ax.set_ylabel('Mean Value')
ax.legend(title='Cluster')
ax.tick_params(axis='x', rotation=30)
plt.tight_layout()
plt.show()

print("\nCluster mean stat profiles:")
print(cluster_profiles.round(1).to_string())
```

### Step 6: Add notable Pokémon callout cell

```python
# --- 8e: Notable Pokémon in each cluster ---
for c in sorted(cluster_df['Cluster'].unique()):
    subset = cluster_df[cluster_df['Cluster'] == c]
    print(f"\n--- Cluster {c} ({len(subset)} Pokémon) ---")
    top5 = subset.nlargest(5, 'Stat Total')[
        ['Pokemon', 'Type 1', 'Role', 'Stat Total', 'Legendary']
    ]
    print(top5.to_string(index=False))
```

### Step 7: Final commit

```bash
git add CERT-x465-003_MAIN.ipynb
git commit -m "feat: EDA Section 8 — ML capstone K-Means clustering with PCA projection"
```

---

## Quick-Reference: Column Inventory

| Column | Type | Used in |
|---|---|---|
| `BMI` | float | Tasks 2 |
| `Role` | str category | Tasks 2, 4, 9 |
| `Stat Std Dev` | float | Task 4 |
| `Offensive Total` / `Defensive Total` | int | Task 6 |
| `Offensive/Defensive` | float | Tasks 3, 5, 6 |
| `Physical/Special` | float | Tasks 3, 8 |
| `Bulk` (derived in Task 5) | int | Task 5 |
| `Legendary` | bool | Task 7 |
| `Evolution Stage` | int (0-3) | Task 8 |
| `Generation` | int (1-9) | Tasks 2, 5, 6, 7 |
| `*_zscore` (6 cols) | float | Task 9 |
| `*_pct` (6 cols) | float | Task 3 |
| `Speed/Defense` | float | Task 5 |
| `Dual Type` / `Type Label` | bool/str | Task 3 |
