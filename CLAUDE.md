# CERT x465-003 Data Interpretation Course

## Project Overview
- Educational repository for UMN CERT x465-003 course assignments
- Primary work happens in `CERT-x465-003_MAIN.ipynb` - main assignment submission notebook
- Helper notebooks in `src/` for data scraping (`dataScrapers_notebook.ipynb`) and cleaning (`dataCleanersExpanders_notebook.ipynb`)

## Dataset
- Master dataset: `data/pokemon_dataset_MASTER.csv` — 1,231 rows × 55 columns
- Column groups: base stats, types, physical traits, evolution, legendary flag, derived ratios, role classification, stat tiers, z-scores
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
- `docs/plans/` — design docs (`*-design.md`) and implementation plans (`*-implementation.md`)

## EDA Notebook (Section 3.3)
- Constants/imports cell id `zhargt522xn`: defines `STAT_COLS`, `ROLE_ORDER`, `PCT_COLS`, `ZSCORE_COLS`, `DATA_DIR`, loads `pokes` DataFrame
- TYPE_COLORS cell id `8sfaxj1a05i`: 18-type palette with **title-cased** keys (e.g. `'Fire'`, `'Water'`) — use `color_discrete_map=TYPE_COLORS` in all Plotly type-colored charts
- `src/plotly_colours.ipynb` has `pokes_colors` with **lowercase** keys — do NOT use directly with Plotly `color_discrete_map` (keys won't match DataFrame column values)
- `make_subplots` is NOT in the base EDA imports — add `from plotly.subplots import make_subplots` locally when needed

## Git Practices
- Currently staged changes include notebooks and project config - verify before committing
- `.gitignore` excludes sample notebooks (sample.ipynb, pokesproject_main.ipynb)
- Standard branch: `master`
