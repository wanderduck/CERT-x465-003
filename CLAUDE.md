# CERT x465-003 Data Interpretation Course

## Project Overview

-   Educational repository for UMN CERT x465-003 course assignments
-   Primary work happens in `CERT-x465-003_MAIN.ipynb` - main assignment submission notebook
-   Helper notebooks in `src/` for data scraping (`dataScrapers_notebook.ipynb`) and cleaning (`dataCleanersExpanders_notebook.ipynb`)

## Dataset

-   Master dataset: `data/pokemon_dataset_MASTER.csv` — 1,231 rows × 55 columns
-   Column groups: base stats, types, physical traits, evolution, legendary flag, derived ratios, role classification, stat tiers, z-scores
-   `data/evo2.csv` (cols: ev1, ev2) and `data/evo3.csv` (cols: ev1, ev2, ev3) — explicit evolution chain pair tables; use for role transition analysis, not name-merging across stages
-   `docs/plans/pokemon-eda-design.md` — 8-section EDA design with question-per-section structure

## Development Environment

-   Python 3.12 (strictly <3.13) managed with UV package manager
-   Dependencies: data science stack (pandas 2.3.3, numpy 2.2.6, matplotlib, seaborn, plotly, scikit-learn)
-   Jupyter notebooks are the primary development interface

## Workflow Patterns

-   `uv sync` - Install/update dependencies from pyproject.toml
-   `uv run jupyter lab` - Launch JupyterLab environment
-   Data files stored in `data/` directory (not tracked in git)
-   Visualization assets in `notebook_images/`
-   Extracted matplotlib PNGs saved to `notebook_images/plot_images/` (tracked in git)
-   `docs/plans/` — design docs (`*-design.md`) and implementation plans (`*-implementation.md`)
-   `docs/reports/` — analytical reports (`full_report.md`, `assignment-03-eda-report.md`, `assignment-05a-recommendations-report.md`)

## EDA Notebook (Section 3.3)

-   Notebook has two distinct sections: scraper pipeline (cells 0–42, RAPIDS GPU libs + live web requests — skip in fresh kernel) and EDA (cells 43+, self-contained)
-   Constants/imports cell id `zhargt522xn`: defines `STAT_COLS`, `ROLE_ORDER`, `PCT_COLS`, `ZSCORE_COLS`, `DATA_DIR`, loads `pokes` DataFrame
-   `zhargt522xn` includes `import pandas as pd` — required for self-contained EDA execution; do not remove
-   nbclient execution: find `zhargt522xn` index, run `nb.cells[eda_start:]` as sub-notebook, write outputs back to original
-   TYPE_COLORS cell id `8sfaxj1a05i`: 18-type palette with **title-cased** keys (e.g. `'Fire'`, `'Water'`) — use `color_discrete_map=TYPE_COLORS` in all Plotly type-colored charts
-   `8sfaxj1a05i` also defines: `TYPE_COLORS_LIGHT`, `TYPE_COLORS_DARK`, `ROLE_COLORS`, `ROLE_COLOR_MAP`, `stats_note(fig, text)` helper, and `_hex_scale(hex, factor)` — use from there, never redefine
-   `src/plotly_colours.ipynb` has `pokes_colors` with **lowercase** keys — do NOT use directly with Plotly `color_discrete_map` (keys won't match DataFrame column values)
-   Chart defaults in `zhargt522xn`: `_H=1200`, `_W=1600`, `_T='plotly_dark'` — apply to every figure
-   `stats_note(fig, text)` — appends a centered annotation below the plot area at `y=-0.16`, `bottom_margin=300`; call before `fig.show()`; adjust `y_pos` further negative if it still overlaps x-axis labels
-   `make_subplots` is NOT in the base EDA imports — add `from plotly.subplots import make_subplots` locally when needed
-   Violin width in `violinmode='group'`: add `violingap=0.1, violingroupgap=0.05` to `update_layout` to widen violin bodies
-   Histogram bin width: `bargap=0` makes bins touch; default has visible gaps
-   `px.box()` does NOT accept `color_continuous_scale` — cast numeric columns to string and use `color_discrete_map` instead
-   `Speed Tier` column has 3 values: `Slow`, `Medium`, `Fast` (not a 5-tier scale); `Stat Tier`: `Low`, `Mid`, `High`, `Very High`
-   Plotly outputs in nbclient are `application/vnd.plotly.v1+json`, not PNGs — verify with `c['outputs'][0]['data']['application/vnd.plotly.v1+json']`
-   Polar subplot key naming: first subplot is `'polar'`, subsequent are `'polar2'`, `'polar3'`, etc. (`'polar' if i==0 else f'polar{i+1}'`)
-   CSV column names: `Special Attack`, `Special Defense` (full names); `HP_zscore`, `Attack_zscore`, `Defense_zscore`, `Speed_zscore`, `Special_Attack_zscore`, `Special_Defense_zscore` (underscore-separated z-scores)
-   `STAT_COLS` and `ZSCORE_COLS` in the constants cell use notebook-friendly names — when running standalone Python outside the notebook, use the CSV column names directly
-   `go.Sankey` node list: source-side roles first, then target-side roles; links map from index `0..n-1` to index `n..2n-1`

## Git Practices

-   Currently staged changes include notebooks and project config - verify before committing
-   `.gitignore` excludes sample notebooks (sample.ipynb, pokesproject_main.ipynb)
-   Standard branch: `master`

## Assignments

### Assignment 01 Details

-   Write a short essay that address the following questions:
    -   What problem or question are you trying to address?
    -   Why are you interested in addressing this?
    -   Why is this an important question or problem to address (in general)?
    -   Who might your audience(s) be for this investigation?
    -   How will the results of this investigation help your audience make decisions or draw conclusions?

### Assignment 02A Details

-   Identify at least one data source that can help answer the question you developed in Module 1.

1.  First, do some research on your own to try and find a data source(s).
    -   You might start with a simple Google search, you may ask someone who has knowledge in the area, or you might already know of some candidates.
    -   For example, if your question pertains to K-12 education in Minnesota, you might check out the Department of Education's data sources.
2.  After you have finished your search and identified good data source(s), please write a short essay that addresses to the following questions:
    -   Describe the data source(s) that you found.
    -   How is the data relevant to your question?
    -   Where does the data come from?
    -   How reliable is the source? Are there any signs of bias?

### Assignment 02B Details

-   In a discussion board post, share your data source from Assignment 02A along with your question from Assignment 01.
-   Briefly describe the data source and share where/how you found it.
-   In responses to two peers, reflect on the data source(s) they chose and point out any additional resources or data points that you think would be helpful for them to consider.

### Assignment 03 Details

-   Using the data source(s) that you identified, produce a 5-minute video describing what you are seeing in the data and what conclusions the data is pointing towards.
-   Make sure you tie it back to the original question you set out to address.
-   In the video, please also include a brief discussion of how groups with different perspectives might interpret the data differently.
-   Post this video to share with your peers, and provide feedback on the videos of at least two peers.

### Assignment 04 Details

-   Find two data visualizations online
    
    1.  one that you think is a good, effective visual
    2.  one that you think is less effective.
-   Note that these do not need to be about the same topic your other assignments have focused on.
    
-   Write a reflection paper about the data visualizations that answer the following questions:
    
    -   What are the key points that each visualization is trying to make?
    -   What makes the good visualization good?
    -   What makes the bad visualization bad? How would you improve it to make it easier to interpret?

### Assignment 05A Details

-   In previous assignments, you have developed your question, found your data, and interpreted it. Now, we’re going to put it all together.
-   Write a brief report to a clearly-specified audience that contains at least three recommendations or takeaways that are justified by data.
    -   The exact format of the report is up to you - you can use a tool like Canva to make something more visual, you can create a slide deck, or you can create a written report.
-   Whatever format you choose make sure:
    -   You describe the question(s) you set out to answer.
    -   Your recommendations or takeaways answer the question, are clearly stated, and are derived from the data source(s) you chose.
    -   You specify who your audiences is and what your purposes is (i.e., informing a decision, educating about a topic).

### Assignment 05B Details

-   Using the report that you created in part one, record a 5-min video where you present your recommendations in a mock professional setting.
-   This is your “elevator speech” version of your key takeaways.
-   Provide feedback on two of your peers’ videos.

### Assignment 06

-   Find a dashboard or other interactive data visualization online.
-   Please write a short essay that assess the visualization tool.
-   In your essay, please address the following questions:
    -   What 1-2 takeaways can you glean from this dashboard?
    -   How easy is it to interpret and interact with the data?
    -   What would you change about this dashboard to make it more effective?