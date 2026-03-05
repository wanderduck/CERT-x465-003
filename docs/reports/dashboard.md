---

# Dashboard Assessment

## Key Takeaways From This Dashboard

**Takeaway 1 — Type is destiny, power level is secondary.** The *Type Identity* tab reveals that each of the 18 primary types has a distinct, consistent stat fingerprint — Ground types are physically oriented (Physical/Special ratio = 1.53), Psychic types are specially oriented (0.76), regardless of whether the individual Pokemon is weak or strong. This is immediately visible by comparing the radar charts across types: each polygon has a characteristic shape that holds when you filter to different generations or power tiers. The tab now shows fingerprints for both Type 1 and Type 2, using the same visual language as the EDA notebook's Section 2c: dark-shaded fills with white borders for Type 2 averages, light-shaded fills with black borders for Type 1. For a game designer, this means type assignment is the single strongest predictor of how a Pokemon will play.

**Takeaway 2 — The "glass cannon" trope is not in the data.** The *Power & Specialization* tab's Speed vs. Bulk scatter shows a *positive* trendline — fast Pokemon are, on average, slightly *more* durable, not less. This is counterintuitive and becomes even more striking when you filter to Legendary-only: the fastest legendaries (Deoxys, Mewtwo) also have substantial bulk. The conventional RPG assumption that speed must trade against durability is a design choice that Game Freak has not enforced at the stat level.

**Takeaway 3 — Rule-based roles and data-driven clusters tell different stories.** The *Evolution & Roles* tab now shows both the 7 hand-crafted combat roles and the 14 GMM-discovered cluster roles side by side, stacked by evolution stage. The rule-based roles (Physical Sweeper, Tank, etc.) shift predictably as Pokemon evolve — more Sweepers at Stage 3, more Balanced at Stage 1. The cluster roles reveal a different pattern: type-driven groupings like "Armored Heavyweights" (Rock/Ground/Steel/Ice) and "Blue-Collar Brawlers" (Water/Fighting) persist across all evolution stages, showing that type identity overrides evolution stage as an organizing principle. Filtering by both role types simultaneously using the Role dropdown confirms that these two classification systems capture complementary dimensions of the data.

## Ease of Interpretation and Interaction

**What works well:**
- **Six global filters propagate everywhere.** Generation, Type 1, Type 2, Role (rule-based and cluster), and Legendary status filters instantly update the KPI cards and every chart on every tab. This lets you ask compound questions ("How do Gen 7 Fire types in the Dragon Powerhouses cluster compare to Gen 1 Fire types?") without writing any code.
- **Role filter combines two classification systems.** The dropdown presents 7 rule-based roles prefixed with `[Rule]` and 14 GMM cluster roles prefixed with `[Cluster]`. Selecting from either group uses OR logic — a Pokemon matches if it belongs to any selected rule role or any selected cluster role. This enables cross-system comparisons that would require custom code in the notebook.
- **KPI cards provide at-a-glance context.** Before diving into any chart, you can see the count, average power, speed, BMI, dominant role, legendary percentage, and specialization for your current filter — seven metrics updated in real time.
- **Hover tooltips on every data point.** Every scatter plot shows the Pokemon's name, type, role, and stat total on hover, turning aggregate visualizations into individual-level lookups.
- **Tab organization reduces cognitive load.** Six tabs (Overview, Type Identity, Power & Specialization, Generational Trends, Evolution & Roles, Pokemon Creator) group related charts so you're never looking at more than 4 visualizations at once.
- **The Pokemon Creator enables "what-if" analysis.** Users can design a custom Pokemon with 6 stat sliders, height/weight inputs, Type 1/Type 2 selectors, and a Legendary toggle, then immediately see how it compares to the real dataset through 4 live-updating charts: a radar overlay against type averages, a BST histogram with position marker, a BMI comparison, and a Speed vs. Bulk scatter with the custom Pokemon highlighted as a red star.

**What could be improved:**
- **No cross-tab linking.** Clicking a Pokemon in one chart doesn't highlight it in other charts. Linked brushing (e.g., selecting a cluster in the PCA scatter and seeing those Pokemon highlighted in the Speed vs. Bulk chart) would make the dashboard significantly more powerful for exploratory analysis.
- **No export or annotation features.** A business user would want to save a filtered view, add notes, or export a chart as an image — none of which the current Dash implementation supports without additional libraries.
- **Filter state isn't saved.** Refreshing the page resets all filters to defaults. For repeated use, URL-encoded filter state or a "save view" feature would prevent lost context.
- **The radar chart only shows the top 6 types** in the current filter. A dropdown to select specific types for comparison — rather than defaulting to the most common — would give users more control over the comparison.
- **Mobile responsiveness is limited.** The side-by-side chart layout works on desktop but stacks awkwardly on smaller screens. Media queries or a responsive grid framework would improve the experience on tablets.
- **GMM runs at startup.** The 14-cluster GMM model is refit each time the dashboard launches (~1-2 seconds). Pre-computing and caching the cluster assignments in the CSV would eliminate this startup cost.

## Dashboard Feature Highlights

| Feature | Description |
|---------|-------------|
| **6 global filters** | Generation, Type 1, Type 2, Role (rule + cluster), and Legendary status — all multi-select with OR logic for roles |
| **Role filter (21 options)** | 7 rule-based roles (`[Rule]` prefix) + 14 GMM cluster roles (`[Cluster]` prefix) in a single dropdown |
| **7 live KPI cards** | Count, Stat Total, Speed, BMI, Role, Legendary %, and Specialization update reactively |
| **6 themed tabs** | Overview, Type Identity, Power & Specialization, Generational Trends, Evolution & Roles, Pokemon Creator |
| **18+ interactive charts** | Bar, histogram, scatter (with OLS trendlines), radar (2c-style layered), stacked bar, and BMI comparison visualizations |
| **Hover tooltips** | Every data point shows individual Pokemon details on mouseover |
| **Dark theme** | Blue-tinted dark palette (`#1a1a2e` base) with gradient title, accented KPI cards, and glowing tab indicators |
| **Color coding** | Type-specific colors from the EDA's `TYPE_COLORS` palette, plus `TYPE_COLORS_LIGHT` and `TYPE_COLORS_DARK` for radar layering |
| **Pokemon Creator** | Full stat builder with 6 sliders (1-255), height/weight inputs, dual-type selectors, Legendary toggle, and reset button |
| **4 Creator comparison charts** | Radar overlay (2c-style Type 1/Type 2 layering), BST histogram with marker, BMI comparison, Speed-Bulk scatter with star marker |
| **GMM clustering** | 14-cluster Gaussian Mixture Model (27 features: 6 z-scores + 3 scaled ratios + 18 one-hot Type 1) computed at startup |
| **Dual role systems** | Both rule-based (7 roles) and cluster-based (14 roles) classifications available in filters and Evolution & Roles tab |

## Tab-by-Tab Chart Inventory

### Overview (3 charts)
1. **BST Distribution** — Histogram of Stat Total, colored by Stat Tier, `bargap=0`
2. **Role Distribution** — Horizontal bar of the 7 rule-based roles
3. **Type 1 Distribution** — Horizontal bar of Type 1 counts
4. **Type 2 Distribution** — Horizontal bar of Type 2 counts (non-null only)

### Type Identity (4 charts)
1. **Stat Fingerprints — Top 6 Type 1s** — 2x3 radar grid with light fills, 0.45 opacity, black borders
2. **Stat Fingerprints — Top 6 Type 2s** — 2x3 radar grid with dark fills, 0.72 opacity, white borders
3. **Physical / Special Ratio by Type** — Horizontal bar with red reference line at 1.0
4. **Offensive / Defensive Ratio by Type** — Horizontal bar with red reference line at 1.0

### Power & Specialization (3 charts)
1. **Speed vs. Bulk** — Scatter with OLS trendline, Pearson r in title, colored by Generation
2. **Offense vs. Bulk** — Same format, Offensive Total vs. Defensive Total
3. **Specialization vs. Power** — Stat Std Dev vs. Stat Total, colored by Stat Tier

### Generational Trends (3 charts)
1. **Offensive vs. Defensive Balance** — 2-panel: line trends + Off/Def ratio with reference line
2. **Individual Stat Trends** — 2x3 grid of per-stat mean trends across generations
3. **Stat Total Distribution** — Box plots per generation with overall mean line

### Evolution & Roles (4 charts)
1. **Created Role Distribution by Evolution Stage** — Stacked bar of 7 rule-based roles by stage
2. **Cluster Role Distribution by Evolution Stage** — Stacked bar of 14 GMM cluster roles by stage
3. **Mean Stats by Evolution Stage** — Grouped bar of 6 stats across stages 1-3
4. **Legendary Percentage by Generation** — Bar chart with percentage labels

### Pokemon Creator (4 charts + form)
- **Form inputs:** Name, Type 1, Type 2 (with "None"), 6 stat sliders (1-255), Height (m), Weight (kg), Legendary toggle, Reset All button
- **Computed summary:** Stat Total, Std Dev, BMI, Role, Legendary status
1. **Radar overlay** — Custom Pokemon vs. Type 1 average (light fill, black border) and Type 2 average (dark fill, white border, if selected)
2. **BST Histogram** — Where the custom Pokemon falls in the overall distribution (red marker line)
3. **BMI Comparison** — Custom Pokemon's BMI vs. dataset distribution (clipped at 200 for readability)
4. **Speed-Bulk Scatter** — Custom Pokemon as a red star marker on top of the full dataset colored by type
