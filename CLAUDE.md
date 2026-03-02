# CERT x465-003 Data Interpretation Course

## Project Overview
- Educational repository for UMN CERT x465-003 course assignments
- Primary work happens in `CERT-x465-003_MAIN.ipynb` - main assignment submission notebook
- Helper notebooks in `src/` for data scraping (`dataScrapers_notebook.ipynb`) and cleaning (`dataCleanersExpanders_notebook.ipynb`)

## Dataset
- Master dataset: `data/pokemon_dataset_MASTER.csv` — 1,231 rows × 55 columns
- Column groups: base stats, types, physical traits, evolution, legendary flag, derived ratios, role classification, stat tiers, z-scores
- `data/evo2.csv` (cols: ev1, ev2) and `data/evo3.csv` (cols: ev1, ev2, ev3) — explicit evolution chain pair tables; use for role transition analysis, not name-merging across stages
- `docs/plans/2026-03-01-pokemon-eda-design.md` — 8-section EDA design with question-per-section structure

## Development Environment
- Python 3.12 (strictly <3.13) managed with UV package manager
- Dependencies: data science stack (pandas 2.3.3, numpy 2.2.6, matplotlib, seaborn, plotly, scikit-learn)
- Jupyter notebooks are the primary development interface

## Workflow Patterns
- `uv sync` - Install/update dependencies from pyproject.toml
- `uv run jupyter lab` - Launch JupyterLab environment
- Data files stored in `data/` directory (not tracked in git)
- Visualization assets in `notebook_images/`
- Extracted matplotlib PNGs saved to `notebook_images/plot_images/` (tracked in git)
- `docs/plans/` — design docs (`*-design.md`) and implementation plans (`*-implementation.md`)

## EDA Notebook (Section 3.3)
- Notebook has two distinct sections: scraper pipeline (cells 0–42, RAPIDS GPU libs + live web requests — skip in fresh kernel) and EDA (cells 43+, self-contained)
- Constants/imports cell id `zhargt522xn`: defines `STAT_COLS`, `ROLE_ORDER`, `PCT_COLS`, `ZSCORE_COLS`, `DATA_DIR`, loads `pokes` DataFrame
- `zhargt522xn` includes `import pandas as pd` — required for self-contained EDA execution; do not remove
- nbclient execution: find `zhargt522xn` index, run `nb.cells[eda_start:]` as sub-notebook, write outputs back to original
- TYPE_COLORS cell id `8sfaxj1a05i`: 18-type palette with **title-cased** keys (e.g. `'Fire'`, `'Water'`) — use `color_discrete_map=TYPE_COLORS` in all Plotly type-colored charts
- `8sfaxj1a05i` also defines: `TYPE_COLORS_LIGHT`, `TYPE_COLORS_DARK`, `ROLE_COLORS`, `ROLE_COLOR_MAP`, `stats_note(fig, text)` helper, and `_hex_scale(hex, factor)` — use from there, never redefine
- `src/plotly_colours.ipynb` has `pokes_colors` with **lowercase** keys — do NOT use directly with Plotly `color_discrete_map` (keys won't match DataFrame column values)
- Chart defaults in `zhargt522xn`: `_H=1200`, `_W=1600`, `_T='plotly_dark'` — apply to every figure
- `stats_note(fig, text)` — appends a centered annotation below the plot area at `y=-0.10`; call before `fig.show()`
- `make_subplots` is NOT in the base EDA imports — add `from plotly.subplots import make_subplots` locally when needed
- `px.box()` does NOT accept `color_continuous_scale` — cast numeric columns to string and use `color_discrete_map` instead
- `Speed Tier` column has 3 values: `Slow`, `Medium`, `Fast` (not a 5-tier scale); `Stat Tier`: `Low`, `Mid`, `High`, `Very High`
- Plotly outputs in nbclient are `application/vnd.plotly.v1+json`, not PNGs — verify with `c['outputs'][0]['data']['application/vnd.plotly.v1+json']`
- Polar subplot key naming: first subplot is `'polar'`, subsequent are `'polar2'`, `'polar3'`, etc. (`'polar' if i==0 else f'polar{i+1}'`)
- `go.Sankey` node list: source-side roles first, then target-side roles; links map from index `0..n-1` to index `n..2n-1`

## Git Practices
- Currently staged changes include notebooks and project config - verify before committing
- `.gitignore` excludes sample notebooks (sample.ipynb, pokesproject_main.ipynb)
- Standard branch: `master`
