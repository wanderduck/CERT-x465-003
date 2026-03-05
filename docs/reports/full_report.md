## **Section 2: Type Shapes Stat Identity, Not Just Stat Total\# Pokemon Base Stats Exploratory Data Analysis — Full Report**

**Dataset:** 1,231 Pokemon across 9 generations | 55 columns | Base stats, types, physical traits, evolution data, derived ratios, z-scores, and rule-based combat role classifications

**Analysis Notebook:** `CERT-x465-003_MAIN.ipynb`

---

This report presents a systematic exploratory data analysis of 1,231 Pokemon spanning nine generations of the franchise. The dataset comprises 55 columns covering base stats, typing, physical traits, evolution data, and a suite of derived metrics including combat ratios, z-scores, stat tiers, and rule-based combat role classifications. The analysis is organized around a series of focused questions, each investigated through purpose-built visualizations. Sections 1 through 4 address body composition, type-driven stat identity, the relationship between power and specialization, and the persistence (or absence) of classic stat tradeoffs across generations. Sections 5 through 7 examine power creep, the Legendary gap, and unsupervised clustering as an ML capstone.

---

## **Section 1: Body Composition and Combat Role**

**Guiding Question:** Does a Pokemon's physical body shape — captured through BMI, height, and weight — predict how it fights?

Pokemon are assigned one of seven rule-based combat roles: Physical Sweeper, Special Sweeper, Mixed Attacker, Balanced, Tank, Physical Wall, and Special Wall. This section asks whether a Pokemon's physical dimensions carry meaningful signal about which role it occupies.

### **1a: BMI Distribution**

The analysis opens with a pair of side-by-side histograms overlaid with kernel density estimates. The left panel displays the full BMI distribution clipped at 200 for readability; the right panel restricts the view to BMI values below 200, where the vast majority of observations fall.

The distribution is heavily right-skewed. Most Pokemon cluster in the 10-60 BMI range, with a pronounced peak near 20-30. However, the tail extends to extreme values — most notably Cosmoem, whose 0.1 m height and 999.9 kg mass produce a BMI of approximately 99,990. An annotation lists the ten highest-BMI Pokemon, confirming that the tail is populated by a small number of ultra-dense or unusually proportioned species rather than by any systematic trend. This skew has practical consequences: any analysis using BMI must account for these outliers, either through clipping, log-transformation, or exclusion, to avoid distorted summary statistics.

### **1b: BMI by Combat Role**

Violin plots display the BMI distribution for each of the seven combat roles, with embedded box plots and mean lines to facilitate comparison. The horizontal layout allows direct visual comparison of distributional shape across roles.

Physical Walls and Tanks exhibit moderately higher median BMI values, consistent with the intuition that bulkier, heavier Pokemon gravitate toward defensive roles. Sweepers — both Physical and Special — skew lighter. However, the overlap between distributions is substantial. Every role contains Pokemon across a wide BMI range, and the interquartile ranges overlap heavily. Median BMI values by role, reported in the chart annotation, confirm that the differences, while directionally sensible, are modest in magnitude. BMI alone is a weak predictor of combat role.

### **1c: Mean Height vs. Mean Weight by Primary Type**

A bubble scatter plot on log-log axes positions each of the 18 primary types by its mean height (x-axis) and mean weight (y-axis). Bubble size encodes the number of Pokemon belonging to each type, and color follows the standard 18-type palette.

Steel and Rock types anchor the heavy end of the distribution, reflecting their thematic association with dense, metallic, or geological body plans. Bug and Fairy types sit at the opposite extreme — small and light. The log-log relationship between mean height and mean weight is approximately linear, suggesting a power-law scaling relationship: across types, weight scales roughly as a fixed power of height. This is consistent with real-world allometric scaling in biology, a notable parallel given that Pokemon dimensions are designer-assigned rather than naturally evolved.

### **1d: Median and Mean BMI by Generation**

A grouped bar chart compares median and mean BMI across all nine generations. Cosmoem is excluded from this visualization because its BMI of 99,990 inflates the Generation 7 mean from approximately 40.8 to over 1,030, rendering cross-generational comparison meaningless.

With Cosmoem removed, median BMI is remarkably stable across generations, fluctuating in a narrow band of roughly 30-37. No clear temporal trend emerges — later generations do not produce systematically heavier or lighter Pokemon. The mean consistently exceeds the median in every generation, confirming that right-skew from heavy outliers is a persistent feature of every generational cohort, not an artifact of any single generation.

### **Section 1 Summary**

Body composition provides a weak and unreliable signal for combat role classification. Physical Walls tend to be heavier and Sweepers tend to be lighter, but the distributions overlap far too much for BMI, height, or weight to function as meaningful predictors. The extreme right-skew driven by outliers like Cosmoem and the dense Steel/Rock types dominates the distributional tail, and BMI is stable across generations. Physical dimensions reflect thematic design choices more than competitive function.

---

**Guiding Question:** Does a Pokemon's primary type determine its fighting personality — the *shape* of its stat distribution — more than its raw power level?

Stat Total (the sum of all six base stats) measures overall power, but two Pokemon with identical stat totals can fight very differently if their stats are allocated differently. This section investigates whether type systematically determines *how* stats are distributed, not just *how much* total stat budget a Pokemon receives.

### **2a: Combat Ratio Profiles by Type 1**

Two horizontal bar charts present the median Physical/Special ratio (left panel) and median Offensive/Defensive ratio (right panel) for each primary type. A red dashed reference line at 1.0 marks perfect balance: values above 1.0 indicate physical or offensive orientation, values below indicate special or defensive orientation.

The results reveal strong and consistent type-level combat personalities. Fighting and Rock types are the most physically oriented, with Physical/Special ratios well above 1.0 — their Attack stats substantially exceed their Special Attack stats. Psychic and Ghost types fall on the opposite side, with ratios well below 1.0, reflecting their reliance on Special Attack. On the offensive-defensive axis, Dragon emerges as the most offensively oriented type, while Fairy skews most defensive. These are not random fluctuations; the separations between types are large relative to within-type variance, indicating that type assignment carries genuine information about combat orientation.

### **2a-ii: Combat Ratio Profiles by Type 2**

The same paired bar chart format is repeated using secondary type instead of primary type. The patterns are strikingly similar. Fighting remains physically oriented and Psychic remains specially oriented regardless of whether the type appears in the primary or secondary slot. This consistency reinforces the interpretation that type-stat associations are intrinsic to the type itself, not an artifact of which Pokemon happen to have it as their primary designation.

### **2b: Stat Fingerprint Radar Charts (All 18 Types)**

A grid of 18 radar (polar) charts — arranged in a 3x6 layout — plots the mean value of each of the six base stats (HP, Attack, Defense, Speed, Special Attack, Special Defense) for every primary type. Each chart produces a distinctive hexagonal "fingerprint" shape.

The fingerprints are remarkably informative. Dragon types produce a large, relatively uniform hexagon — high in every stat, reflecting their status as generalist powerhouses. Bug types produce a small hexagon — low across the board. More diagnostic are the asymmetric shapes: Fighting types spike sharply on Attack while remaining modest elsewhere; Psychic types peak on Special Attack and Speed; Steel types bulge on Defense. These shapes are more revealing than stat totals alone, because they capture the *allocation strategy* that defines each type's competitive identity. Two types with similar stat totals (e.g., Fire and Water) can have visibly different fingerprint shapes, reflecting their distinct combat roles.

### **2c: Primary vs. Secondary Type Stat Fingerprints**

The same 3x6 radar grid is repeated, but each chart now overlays two fingerprints: a light fill for Pokemon with that type as their primary type, and a dark fill for Pokemon carrying it as their secondary type. This allows direct comparison of how a type's stat signature shifts depending on its slot.

When a type appears as Type 2, its stat fingerprint consistently shifts toward moderation. The peaks are slightly lower and the valleys slightly higher compared to the primary-type fingerprint. This makes intuitive sense: a Pokemon whose primary type is Fighting will be designed around that type's Attack-heavy identity, but a Pokemon that merely *also* has Fighting as a secondary type will temper that identity with the stat tendencies of its primary type.

### **2d: Does Dual Typing Affect Stat Profile Shape?**

Side-by-side violin plots compare the Physical/Special ratio and Offensive/Defensive ratio distributions of mono-typed versus dual-typed Pokemon.

Dual-typed Pokemon display slightly more moderate ratios, with distributions pulled closer to 1.0 on both axes. The effect is modest but consistent: dual typing acts as a statistical averaging mechanism, blending two type identities and dampening the extremes associated with either type individually. A pure Fighting-type is more likely to have an extreme Physical/Special ratio than a Fighting/Flying-type, because the Flying component introduces some countervailing stat tendencies.

### **Section 2 Summary**

Type is the single strongest predictor of stat shape in the dataset. Each of the 18 types exhibits a recognizable stat fingerprint — a characteristic allocation pattern that persists regardless of stat total, generation, or legendary status. These fingerprints remain consistent whether a type appears in the primary or secondary slot, though secondary typing moderates the signal. Dual typing blends two fingerprints, producing more balanced profiles. For analytic purposes, type should be understood not as a label but as a proxy for combat identity: it encodes *how* a Pokemon's stat budget is spent, which is often more competitively meaningful than *how much* budget it received.

---

## **Section 3: The Specialization Premium**

**Guiding Question:** Do more powerful Pokemon pay for their power by becoming one-dimensional — concentrating their stats into fewer categories?

If a Pokemon has a high stat total, that budget could be distributed evenly across all six stats (a generalist) or concentrated into one or two stats (a specialist). This section investigates whether stronger Pokemon systematically favor specialization over balance.

### **3a: Stat Standard Deviation vs. Stat Total**

A scatter plot positions each Pokemon by its Stat Total (x-axis) and the standard deviation of its six base stats (y-axis). Points are colored by Stat Tier (Low, Mid, High, Very High), and an OLS trendline is overlaid. The Pearson correlation coefficient is reported in the chart annotation.

The correlation is strongly positive. As Stat Total increases, stat standard deviation increases in tandem — meaning higher-powered Pokemon distribute their stats less evenly. The "Very High" tier (the most powerful Pokemon) clusters visibly higher on the y-axis than lower tiers, confirming that elite Pokemon achieve their totals not by being uniformly good at everything but by excelling dramatically in selected stats while accepting relative weakness elsewhere. The trendline's slope quantifies this relationship: for every additional point of Stat Total, stat standard deviation increases by a measurable and consistent amount.

### **3b: Stat Standard Deviation by Stat Tier and by Role**

A two-panel visualization presents the same metric — stat standard deviation — segmented two ways. The left panel shows box plots by Stat Tier; the right panel shows violin plots by combat role.

By tier, the relationship is monotonic: Low-tier Pokemon have the lowest stat standard deviation, and each successive tier is more specialized. Mean stat standard deviation values by tier, reported in the annotation, confirm a clear staircase pattern. By role, the results align with mechanical expectations. Physical Walls and Special Walls exhibit the highest specialization — they funnel stat budget into one defensive dimension at the expense of others. Balanced Pokemon, by definition, have the most even stat distributions and therefore the lowest standard deviation. Sweepers fall in between, specialized but less extremely so than Walls.

### **Section 3 Summary**

The data reveal a consistent specialization premium. Stronger Pokemon are more specialized, not more balanced. The design logic is clear: to achieve an exceptional stat total, a Pokemon must concentrate resources rather than spread them evenly. This has practical implications for analysis and prediction — stat total alone understates the competitive differences between Pokemon, because a 600-BST specialist and a 600-BST generalist play completely different roles despite identical power budgets. The combination of stat total and stat standard deviation provides a more complete picture of a Pokemon's competitive profile than either metric alone.

---

## **Section 4: The Speed-Bulk Tradeoff Across Generations**

**Guiding Question:** Is "fast equals fragile" a real design rule embedded in the data, and has it intensified or relaxed over the franchise's nine generations?

A common assumption in competitive Pokemon analysis is that Speed comes at the cost of defensive bulk — that fast Pokemon must sacrifice HP, Defense, and Special Defense to fund their Speed stat. This section tests that assumption empirically.

### **4a: Speed vs. Bulk (HP \+ Defense \+ Special Defense)**

A scatter plot positions each Pokemon by Speed (x-axis) and Bulk, defined as the sum of HP, Defense, and Special Defense (y-axis). Points are colored on a continuous scale by Generation, and an OLS trendline is overlaid. The Pearson correlation coefficient is reported.

The result contradicts the conventional assumption. The Speed-Bulk correlation is weakly *positive*, not negative. Fast Pokemon are not systematically fragile; if anything, they are marginally bulkier on average. The explanation lies in the confounding effect of stat total: high-BST Pokemon tend to be high in *all* stats, including both Speed and Bulk. A legendary with a 680 stat total will likely have high Speed *and* high Bulk simply because it has more stat budget to allocate everywhere. The "fast \= fragile" narrative holds for specific designed archetypes (glass cannons like Alakazam or Weavile) but does not describe the population-level pattern.

### **4b: Speed-Bulk and Offense-Bulk Pearson r by Generation**

A two-line time-series chart tracks the per-generation Pearson correlation between Speed and Bulk (blue line) and between Offense (Attack \+ Special Attack) and Bulk (orange line). A dashed reference line at r \= 0 marks the point of no correlation.

The Speed-Bulk correlation fluctuates by generation but never becomes strongly negative. It hovers near zero or slightly positive across all nine generations, confirming that no single generation introduced a systematic "fast \= fragile" design philosophy. The Offense-Bulk correlation follows a similar pattern — weakly positive on average, with more generation-to-generation variability. Individual generation correlations, reported in the annotation, reveal occasional dips below zero, but these are small and inconsistent. There is no evidence that Game Freak systematically increased or decreased the Speed-Bulk tradeoff over the franchise's 25-year history.

### **4c: Speed Tier x Stat Tier Cross-Tabulation Heatmap**

A heatmap cross-tabulates Speed Tier (Slow, Medium, Fast) against Stat Tier (Low, Mid, High, Very High). Cell color intensity encodes count, and exact counts are annotated in each cell. The Pearson correlation between the two tier variables is reported.

The heatmap reveals a positive diagonal trend: fast Pokemon are more likely to appear in higher overall stat tiers, and slow Pokemon concentrate in lower tiers. This reinforces the finding from 4a — Speed does not trade against overall power. Instead, Speed is a *component* of total power, so high-BST Pokemon tend to be fast simply because they have more stat budget to allocate everywhere. The correlation is moderate and positive, confirming that Speed Tier and Stat Tier move together rather than in opposition.

### **4d: Offense Tier x Stat Tier Cross-Tabulation Heatmap**

A heatmap cross-tabulates Offense Tier (Low, Mid, High) against Stat Tier (Low, Mid, High, Very High). Cell color intensity encodes count, and exact counts are annotated in each cell. The Pearson correlation between the two tier variables is reported.

The heatmap reveals a strong diagonal concentration: high-offense Pokemon are overwhelmingly found in higher overall stat tiers, and low-offense Pokemon cluster in lower tiers. This confirms that offense is not traded against overall power — it is a *component* of it. A Pokemon with high Attack and Special Attack is likely to have a high stat total, not because it sacrificed Bulk to fund Offense, but because high offensive stats contribute directly to the total. The Pearson r between the two tier variables is strongly positive, quantifying the degree of alignment between offensive power and overall power.

### **Section 4 Summary**

The "fast \= fragile" tradeoff is a myth at the population level. Speed, Offense, and Bulk are all positively correlated with stat total, and therefore positively correlated with each other once the stat-total confound is accounted for. Individual Pokemon certainly make Speed-for-Bulk tradeoffs — glass cannons and slow tanks exist by deliberate design — but these are specific archetypes, not a systematic rule. Across all nine generations, the data show no evidence that Game Freak enforces or has intensified a Speed-Bulk tradeoff as a population-wide design constraint. Analysts should be cautious about assuming tradeoffs exist without first controlling for overall power level.

---

## **Section 5: Is Power Creep Asymmetric?**

**Guiding Question:** Has offensive power inflated faster than defensive bulk across nine generations of Pokemon design?

The notion of "power creep" — the gradual inflation of stats in newer game entries to keep content appealing — is a persistent concern in any long-running franchise. Across 26 years and nine generations, Game Freak has introduced increasingly diverse Pokemon. But does the data support the claim that offense has outpaced defense, tilting the metagame toward glass-cannon designs? Or has the inflation been more disciplined than popular discourse suggests?

### **5a: Offensive vs. Defensive Totals by Generation**

This two-panel line chart tracks the balance between offense and defense over time. The left panel plots mean Offensive Total (Attack \+ Sp. Atk) and mean Defensive Total (HP \+ Defense \+ Sp. Def) per generation on separate trend lines. The right panel distills this into a single metric: the mean Offensive/Defensive ratio per generation, with a dashed reference line at 1.0.

The result is striking in its stability. Both offensive and defensive means creep upward across generations, but the ratio between them holds remarkably steady near 1.0. There is no generation in which offensive inflation meaningfully outstrips defensive inflation or vice versa. Peak offensive and defensive generations are noted in the chart's annotation, but the key takeaway is not which generation peaks — it is that the peaks co-occur. When offense rises, defense rises with it, generation after generation.

This finding directly contradicts the common narrative that newer Pokemon are designed to hit harder at the expense of durability. The data shows that Game Freak has maintained an implicit balance constraint: for every point added to the offensive side of the stat budget, a roughly equivalent point appears on the defensive side.

### **5b: Which Individual Stats Inflated Most?**

A 2x3 grid of line charts breaks the aggregate trend into its component parts, plotting the mean value of each base stat (HP, Attack, Defense, Speed, Sp. Atk, Sp. Def) per generation. This decomposition reveals which stats are driving the overall upward trend and whether inflation is uniform across the stat hexagon.

The fastest-growing stat is identified in the chart annotation, showing its cumulative increase from Generation 1 to Generation 9\. Most stats exhibit modest upward trends punctuated by generation-to-generation fluctuations. Attack and Sp. Atk show the clearest upward trajectories, consistent with the franchise's increasing emphasis on distinct physical and special attackers. Defense and Sp. Def track these increases closely, reinforcing the symmetry observed in chart 5a.

Speed stands apart as the most stable stat. Its mean has remained relatively flat across all nine generations, showing neither the upward creep of offensive stats nor the compensatory rise of defensive stats. This flatness suggests that Speed occupies a different design role — it functions more as a strategic differentiator (fast vs. slow archetypes) than as a power metric subject to inflation.

### **5c: Stat Total Distribution per Generation**

Box plots for each generation, colored along a sequential palette, display the full distribution of Base Stat Totals (BST). A horizontal dashed line marks the all-generation average for reference. Mean BST per generation is listed in the chart annotation.

The generation medians fluctuate but do not follow a clear monotonic increase. Some later generations sit above the all-generation average, while others sit near or below it. More revealing than the central tendency is the spread: later generations show wider interquartile ranges and longer whiskers than earlier ones. This widening reflects a deliberate design strategy — newer generations include both very high-BST designs (Mega Evolutions, Ultra Beasts, Paradox forms) and very low-BST designs (early-route Pokemon, pre-evolutions), producing greater diversity rather than a uniform upward shift.

The distinction is important. Pure power creep would manifest as rising medians with stable spread. What the data shows instead is stable medians with rising variance — a pattern better described as "design diversification" than "inflation."

### **Section 5 Summary**

Power creep exists in the Pokemon franchise but is modest and symmetric. Offensive and defensive inflation track each other closely across nine generations, preserving the fundamental balance ratio near 1.0. Speed has remained essentially flat, serving as a role-defining stat rather than a power-scaling one. Later generations exhibit more stat diversity — both stronger and weaker designs — rather than uniformly higher baselines. The game's balance has been more carefully maintained than popular perception suggests.

---

## **Section 6: Is the Legendary Gap Closing?**

**Guiding Question:** Have ordinary Pokemon powered up enough that Legendary status no longer signals exceptional strength?

Legendary Pokemon are the franchise's marquee designs — rare, narratively significant, and traditionally far more powerful than their common counterparts. But as overall stat budgets have crept upward and Game Freak has introduced pseudo-legendaries, Mega Evolutions, and other high-BST non-legendaries, has the statistical gap between legendary and ordinary Pokemon narrowed?

### **6a: Stat Total — Legendary vs. Non-Legendary**

Overlaid violin plots compare the full BST distributions of Legendary and Non-Legendary Pokemon. Gold marks the Legendary distribution; blue marks the Non-Legendary. Interior box plots and mean lines provide additional distributional detail.

The gap is immediately visible. The Legendary distribution is centered dramatically higher, with a mean BST around 580 compared to approximately 430 for Non-Legendaries — a difference of roughly 150 stat points. The Legendary distribution is also more compact, reflecting the narrower design space these Pokemon occupy (most are fully evolved, high-powered, singular designs). The Non-Legendary distribution is far wider, encompassing everything from unevolved first-route encounters to pseudo-legendaries.

There is meaningful overlap in the tails: the strongest non-legendaries (Mega Evolutions, pseudo-legendaries like Dragonite and Tyranitar) reach into the lower range of the Legendary distribution. But this overlap is limited. For the vast majority of Pokemon, Legendary status remains a reliable indicator of statistical superiority.

### **6b: Legendary Gap by Generation**

A two-panel chart examines whether the gap identified in 6a has evolved over time. The left panel plots mean BST for Legendary and Non-Legendary Pokemon per generation as separate trend lines. The right panel shows the absolute gap (Legendary mean minus Non-Legendary mean) as a bar chart, one bar per generation.

The gap fluctuates substantially by generation but shows no systematic convergence. Some generations feature unusually large gaps (where the Legendary roster includes cover legendaries and mythicals with BSTs of 600 or 680), while others feature narrower gaps (where the non-Legendary roster includes pseudo-legendaries or Mega Evolutions that pull the non-Legendary mean upward). Per-generation gap values appear in the annotation.

Crucially, there is no downward trend in the gap over time. Generation 9 does not have a meaningfully smaller Legendary/Non-Legendary gap than Generation 1\. The fluctuations are driven by roster composition within each generation rather than by any systematic closing of the divide.

### **6c: Top 25 Legendary vs. Top 25 Non-Legendary by Stat Total**

A strip plot isolates the elite tier: the 25 highest-BST Legendary Pokemon and the 25 highest-BST Non-Legendary Pokemon, plotted as individual points with generation on the x-axis and BST on the y-axis. Purple marks Legendaries; yellow marks Non-Legendaries.

At this elite level, the picture changes. The strongest non-legendaries — Mega Evolutions and pseudo-legendaries — compete with or exceed many legendaries in raw BST. The distributions of the two groups overlap far more than in the population-level violin plot. The annotation details the generational distribution of these top-50 Pokemon, revealing that they are concentrated in the generations that introduced Mega Evolution and certain stat-heavy pseudo-legendaries.

This finding illustrates an important nuance: Legendary status is a strong signal at the population level but a weak differentiator at the elite tier. The very best non-legendaries have been deliberately designed to rival legendaries, blurring the distinction for competitive players who operate exclusively in the upper tail of the distribution.

### **Section 6 Summary**

Legendary status remains a powerful signal of statistical strength. The average Legendary carries roughly 150 more base stat points than the average Non-Legendary — a gap that has not systematically closed across nine generations. However, at the elite tier, the boundary blurs considerably. Mega Evolutions, pseudo-legendaries, and other high-BST non-legendary designs compete with and occasionally surpass typical legendaries. The Legendary gap is real and persistent in aggregate, but increasingly porous at the top.

---

## **Section 7: ML Capstone — Unsupervised Clustering**

**Guiding Question:** Without using any predefined labels, can the data's own structure rediscover the combat role archetypes defined earlier in this analysis — and reveal groupings that rule-based classification missed?

The preceding six sections relied on hand-crafted categories: combat roles derived from stat ratio thresholds, stat tiers based on quintile cuts, and the binary Legendary/Non-Legendary flag provided by the game itself. These categories were useful for structured analysis, but they impose the analyst's assumptions on the data. Unsupervised clustering inverts this approach: it asks the data to organize itself, revealing whatever structure is most statistically prominent — whether or not it aligns with human-defined categories.

**Method.** A Gaussian Mixture Model (GMM) was fitted using Bayesian Information Criterion (BIC) for model selection. The feature set comprised 27 dimensions: six base stat z-scores (HP, Attack, Defense, Speed, Sp. Atk, Sp. Def), three scaled derived ratios (BMI, Physical/Special ratio, Offensive/Defensive ratio), and 18 one-hot encoded columns for Type 1\. The inclusion of type encoding was a deliberate analytical choice — it tests whether type identity or stat patterns dominate the data's clustering structure.

### **7a: Feature Engineering and BIC Curve**

A line chart plots BIC score against the number of mixture components K, ranging from 2 to 15\. A vertical dashed line marks the BIC-optimal K, and the annotation details the feature set and the winning BIC score.

BIC selects K=14 as optimal. This high cluster count is itself a finding: it exceeds the 7 rule-based combat roles defined earlier and approaches the 18 possible Type 1 values. The implication — confirmed in subsequent charts — is that the model is finding type-aligned clusters rather than role-aligned ones. The 18 one-hot type dimensions exert strong influence on the GMM's covariance structure, pulling the clustering solution toward type separation.

### **7b: GMM Clusters — PCA Projection**

A two-dimensional scatter plot projects all 1,231 Pokemon onto the first two principal components of the feature space. Points are colored by their GMM cluster assignment, and 2-sigma confidence ellipses outline each cluster's spread. A random sample of 13 Pokemon per cluster is displayed for interpretability. Hover data includes each Pokemon's name, combat role, Type 1, Legendary status, BST, generation, BMI, and assignment confidence.

Clusters separate clearly in PCA space, though boundary overlap is evident — expected behavior for a mixture model, where probabilistic assignments replace hard boundaries. Mean assignment confidence across all Pokemon is high, indicating that most individuals are firmly assigned to a single cluster rather than split between two. Cluster sizes range from a single observation (the extreme outlier Cosmoem) to over 200 Pokemon.

### **7c: Cluster vs. Role Heatmap**

A heatmap cross-tabulates the 14 GMM clusters (y-axis) against the 7 rule-based combat roles (x-axis), with color intensity proportional to count and exact values annotated in each cell.

The heatmap reveals that the GMM clusters do not cleanly rediscover the seven combat roles. Most clusters have "Tank" or "Balanced" as their plurality role — a consequence of these being the two most common roles in the dataset overall, not a sign of clustering success. Some clusters show modest role concentration (e.g., the Electric Speedsters cluster over-represents the "Sweeper" role relative to the population base rate), but no cluster maps one-to-one onto a single role. The clustering has organized the data along a different axis entirely — one dominated by type identity rather than combat function.

### **7d: Mean Feature Values per Cluster**

A grouped bar chart displays the mean value of each input feature (six base stats, BMI, Physical/Special ratio, Offensive/Defensive ratio) for each of the 14 clusters. A log-scaled y-axis accommodates the wide range between stat values (typically 60-100) and BMI (which ranges from roughly 20 to 700+). The annotation lists the dominant Type 1 for each cluster.

Clusters differ most visibly by overall stat level — high-BST clusters (Dragon Powerhouses at 545 mean BST) tower over low-BST clusters (Fragile Normals at 412 mean BST). Within stat-level tiers, type-specific patterns emerge: the Electric Speedsters cluster shows elevated Speed and Sp. Atk bars, the Armored Heavyweights show elevated Defense, and the Psychic Cannons show the highest Sp. Atk of any cluster.

Of the 14 clusters, 10 are type-pure — every member shares the same Type 1\. The remaining four multi-type clusters are the most analytically interesting:

| Cluster | Name | Size | Mean BST | Composition | Defining Trait |
| :---- | :---- | ----- | ----- | :---- | :---- |
| C0 | Fairy Fortress Elite | 5 | 506 | Fairy | Extreme Sp. Def |
| C1 | Dragon Powerhouses | 52 | 545 | Dragon | Highest BST; 31% Legendary |
| C2 | Extreme Wall Outlier | 1 | 400 | Psychic (Cosmoem) | Def \= Sp. Def \= 131; zero offense |
| C3 | Ghost Generalists | 47 | 441 | Ghost | No standout stat; versatile roles |
| C4 | Electric Speedsters | 73 | 453 | Electric | Speed \+ Sp. Atk emphasis |
| C5 | Blue-Collar Brawlers | 205 | 446 | Water \+ Fighting | Physical lean; largest cluster |
| C6 | Armored Heavyweights | 208 | 460 | Rock / Ground / Steel / Ice | Highest Defense; slowest; heaviest BMI |
| C7 | Low-Stat Midtiers | 170 | 425 | Bug \+ Fire | Lowest overall stats |
| C8 | Pixie Wardens | 30 | 462 | Fairy | Sp. Def focused; light build |
| C9 | Rooted Slowpokes | 113 | 428 | Grass | Lowest Speed of any cluster |
| C10 | Toxic Heavies | 60 | 446 | Poison \+ Normal | No standout stat; heavy |
| C11 | Shadow Strikers | 59 | 456 | Dark | Above-average Attack \+ Speed |
| C12 | Psychic Cannons | 79 | 486 | Psychic | Highest Sp. Atk; 35% Legendary |
| C13 | Fragile Normals | 129 | 412 | Normal \+ Flying Lowest BST; | below-average defenses |

The four multi-type clusters — Blue-Collar Brawlers (Water \+ Fighting), Armored Heavyweights (Rock   
/ Ground / Steel / Ice), Low-Stat Midtiers (Bug \+ Fire), and Fragile Normals (Normal \+ Flying) — are united not by shared type identity but by shared stat shape. Water-types and Fighting-types land in the same cluster because both lean physical. Rock, Ground, Steel, and Ice types cluster together because all four emphasize Defense and carry high BMI. These cross-type groupings represent the genuinely novel insight of the ML analysis: they reveal latent statistical alliances between types that share mechanical roles despite occupying different positions in the type effectiveness chart.

### **Section 7 Summary**

The GMM clustering was dominated by the one-hot Type 1 encoding, producing 10 type-pure clusters out of 14 — effectively performing type classification rather than discovering novel stat archetypes. The clusters do not cleanly map to the seven rule-based combat roles, demonstrating that type identity is the strongest organizing principle in the dataset, more powerful than stat distributions or combat role classifications. The four multi-type clusters provide the most valuable finding: they identify unexpected type alliances united by shared stat profiles rather than shared type labels. These groupings would not emerge from any rule-based analysis and validate the use of unsupervised methods as a complement to — not a replacement for — domain-driven classification.

---

## **Conclusion**

Across seven sections and more than two dozen visualizations, this analysis examined the Pokemon franchise's base stat system from multiple angles: physical composition, type identity, stat specialization, cross-stat tradeoffs, generational trends, legendary exceptionalism, and unsupervised structure discovery. Several findings challenge conventional wisdom. Body composition metrics like BMI bear almost no relationship to combat role — a Pokemon's physical dimensions are cosmetic rather than functional. The Speed-Bulk tradeoff, often assumed to be a fundamental design constraint, does not hold at the population level; fast Pokemon are not systematically fragile, and slow Pokemon are not systematically durable. Power creep, while present, is both modest and symmetric: offensive and defensive stats have inflated in lockstep, preserving the balance ratio near 1.0 across all nine generations.

The single most consistent finding is the dominance of type identity as an organizing principle. Type determines stat shape more reliably than it determines power level. Each type carries a characteristic statistical fingerprint — Electric types emphasize Speed and Sp. Atk, Steel types emphasize Defense, Dragon types run high across the board — and these fingerprints are so distinctive that an unsupervised GMM, given no type labels, independently rediscovered type groupings as its primary clustering axis. The seven rule-based combat roles, by contrast, cut across types rather than aligning with them, which is precisely why the ML model did not recover them. Role classification captures a real but secondary dimension of variation, one that operates within type rather than between types.

The analysis also reveals that power in the Pokemon stat system comes through specialization rather than uniform strength. High-BST Pokemon do not simply have more of everything; they tend to concentrate their stat budget into one or two standout dimensions, producing higher standard deviations and more extreme stat profiles. This specialization principle extends to the Legendary gap: Legendary Pokemon carry roughly 150 more base stat points than ordinary Pokemon on average, a gap that has persisted without systematic convergence across nine generations. Yet at the elite tier — the top 25 of each category — Mega Evolutions and pseudo-legendaries compete with and occasionally surpass typical legendaries, demonstrating that the franchise has created deliberate pathways for non-legendary designs to reach legendary-tier power.

Finally, the ML capstone demonstrated both the power and the limitations of unsupervised methods in a domain-rich dataset. The GMM's type-dominated clusters were not a failure of the method but a genuine finding: type is simply the strongest signal in the data, stronger than stat patterns, combat roles, or generational effects. The four multi-type clusters — groupings like Water with Fighting, or Rock with Ground/Steel/Ice — represent the analysis's most novel contribution, revealing latent statistical alliances between types that share mechanical profiles despite having no relationship on the type effectiveness chart. These alliances would not emerge from any rule-based or domain-driven analysis, validating unsupervised clustering as a complementary lens for understanding a system that, after 26 years and 1,231 designs, remains more balanced and more internally coherent than its complexity might suggest.

# **Data-Driven Design Recommendations for Future Pokemon Generations**

**Course:** CERT x465-003 — Data Interpretation and Application **Assignment:** 05A — Recommendations Report **Audience:** Game Freak's Pokemon stat design team **Purpose:** Inform design decisions for Generation 10+ by identifying what nine generations of stat data reveal about emerging patterns, unintentional trends, and underutilized design space.

---

## **Background**

This report draws on an Exploratory Data Analysis of 1,231 Pokemon across all nine generations, using a custom-built dataset of 55 columns covering base stats, types, physical traits, evolution chains, role classifications, and derived metrics (z-scores, ratios, stat tiers). The analysis was organized around focused questions in seven sections: body composition and combat role, type-driven stat identity, the specialization premium, speed-bulk and offense-bulk tradeoffs, power creep symmetry, the Legendary gap, and an unsupervised ML capstone using Gaussian Mixture Models.

The question driving this work: **Can the accumulated data across nine generations reveal where the stat system is working as intended, where it's drifting, and where there's room for deliberate innovation?**

---

## **Recommendation 1: Restore Meaningful Legendary Differentiation**

### **The finding**

Legendary Pokemon carry an average base stat total (BST) of approximately 580 compared to roughly 430 for non-Legendaries — a gap of around 150 points that has persisted across all nine generations. Contrary to popular belief that power creep is closing this gap, the data shows no systematic convergence trend. The gap fluctuates generation to generation, driven primarily by roster composition rather than any directional narrowing. Gen 9 does not have a meaningfully smaller gap than Gen 1\.

However, at the elite tier the picture changes. When comparing the top 25 Legendaries against the top 25 non-Legendaries, boundaries blur considerably. Mega Evolutions and pseudo-legendaries (Dragonite, Tyranitar, Garchomp, and their peers) routinely match or surpass typical Legendaries in raw stat totals. The Legendary gap is real and persistent in aggregate, but increasingly porous at the top.

### **The problem**

The Legendary designation is meant to signal narrative and mechanical distinctiveness — these are Pokemon that reshape ecosystems, anchor mythologies, and anchor box art. When pseudo-legendaries and Mega Evolutions occupy the same stat space, the mechanical identity of Legendaries erodes. A player encountering a Legendary for the first time should feel it in the numbers, not just the lore. The compact distribution of Legendary stats (narrow design space, fully evolved, high-powered, singular) means there is limited room to differentiate within the category itself, while the wide non-Legendary distribution (spanning unevolved basics to pseudo-legendaries) keeps pushing its upper boundary upward.

### **The recommendation**

Rather than inflating Legendary BSTs further — which risks runaway escalation — Generation 10 should differentiate Legendaries through **stat-shape distinctiveness**, not raw totals. Reserve specific stat profiles for Legendaries that non-Legendaries cannot access: extreme specialization ratios (e.g., offensive-to-defensive splits above 2.0 or below 0.5), or stat configurations that occupy empty regions of the current design space. Simultaneously, consider capping pseudo-legendary BSTs at 580 rather than 600, restoring a clean 20-point buffer. This preserves the aggregate gap's integrity while making the top-tier boundary less porous. The data confirms the gap does not need to be widened — it needs to be made qualitatively sharper.

---

## **Recommendation 2: Embrace Design Diversification Over Uniform Power Creep**

### **The finding**

Nine generations of stat data reveal that power creep in Pokemon is modest, symmetric, and frequently mischaracterized. Offensive and defensive inflation track each other closely — the offensive-to-defensive ratio holds remarkably steady near 1.0 across all generations. When Attack and Special Attack rise, Defense and Special Defense rise with them, maintaining an implicit balance constraint. Speed is the most stable stat across all nine generations, remaining essentially flat and functioning as a role-defining attribute rather than a power-scaling one.

More revealing than median trends is what happens to spread. Later generations show wider interquartile ranges and longer whiskers in their stat distributions. Pure power creep would manifest as rising medians with stable spread. What the data actually shows is stable medians with rising variance. This is design diversification, not inflation. HP has inflated the most of any individual stat, gaining approximately 12.8 points from Gen 1 to Gen 9\. Attack and Special Attack show the clearest upward trajectories, but Defense and Special Defense track them in lockstep.

### **The problem**

The community perception of runaway power creep creates pressure to respond to a problem that largely does not exist in the form assumed. If the design team reacts to perceived inflation by artificially constraining new Pokemon stats, it would suppress the actual trend — increasing design diversity — which is arguably the franchise's greatest mechanical strength entering its fourth decade. Each new generation needs Pokemon that feel distinct from 1,000+ predecessors, and wider stat variance is the primary tool for achieving that.

### **The recommendation**

Lean into diversification deliberately rather than allowing it to emerge as a byproduct. Generation 10 should target specific underrepresented stat profiles — the empty zones in the stat-shape landscape — rather than anchoring designs to generation-average BSTs. The symmetry between offensive and defensive inflation is a feature worth preserving: for every new glass cannon, introduce a corresponding wall. Maintain Speed's role as the great differentiator by keeping it decoupled from overall BST scaling. The data supports a design philosophy of **wider palette, not higher ceiling**. Set explicit diversity targets per generation (e.g., minimum variance in BST, required representation across stat tiers) to ensure this pattern continues by design rather than by accident.

---

## **Recommendation 3: Preserve Type Fingerprints as a Design Anchor**

### **The finding**

Every one of the 18 Pokemon types carries a distinct stat "fingerprint" — a characteristic radar-profile shape that has remained consistent across nine generations. Ground types are the most physically oriented (Physical/Special ratio of 1.53), Psychic types the most specially oriented (0.76), Electric types the most offensive (Offensive/Defensive ratio of 1.31), and Rock types the most defensive (0.87). Dragon, notably, has the weakest fingerprint — a nearly round radar chart — which aligns with its narrative identity as a generalist archetype. When a type appears as Type 2 rather than Type 1, the fingerprint shifts toward moderation: peaks lower, valleys rise, and ratios pull closer to 1.0. Dual typing functions as statistical averaging.

### **The problem**

Nine generations of consistency have trained players to form reliable intuitions about what a type "feels like" in combat. A Fighting-type should hit hard physically. A Psychic-type should lean into Special Attack. These expectations are not arbitrary — they emerge from hundreds of design decisions that, in aggregate, have been remarkably coherent. If Generation 10 introduces a cluster of physically oriented Psychic-types or specially oriented Fighting-types without clear narrative justification, it does not read as creative variety. It reads as noise. The fingerprints are also load-bearing for dual-type design: the predictable blending effect lets players reason about type combinations without consulting a spreadsheet.

### **The recommendation**

Treat each type's stat fingerprint as a soft constraint, not a rigid rule. When designing a new Pokemon, start from the established profile for its primary type and deviate only with intentional narrative justification — a physically bulky Psychic-type should have a lore reason for breaking the mold. For dual-typed Pokemon, use the averaging effect deliberately: pair types whose fingerprints complement each other to create mid-range generalists, or pair types with similar orientations to reinforce a sharp identity. Dragon's round fingerprint is an asset, not a flaw — preserve it as the designated generalist slot. Finally, use the specialization premium (Stat Std Dev correlates with Stat Total at r \= 0.45) as a budget guide: when allocating a high base stat total, lean into the type's existing peaks rather than spreading points evenly. Stronger Pokemon should feel more like their type, not less.

---

## **Recommendation 4: Make the Glass Cannon Tradeoff Intentional**

### **The finding**

The data contradicts one of the most persistent assumptions in Pokemon design discourse: that fast Pokemon are systematically fragile. Speed-Bulk correlation across the full dataset is weakly *positive* (r \= \+0.18), not negative. Offense-Bulk correlation is strongly positive (r \= \+0.61). The Speed-Bulk relationship holds across every combat role without exception — Mixed Attackers (r \= 0.95), Balanced (r \= 0.89), Tanks (r \= 0.83), Physical Walls (r \= 0.77), Physical Sweepers (r \= 0.77), Special Sweepers (r \= 0.70), and even Special Walls (r \= 0.37). No generation introduced a systematic "fast equals fragile" design pattern; the correlation hovers near zero or slightly positive across all nine generations, with only Gen 7 briefly dipping to \-0.035. The explanation is straightforward: high-BST Pokemon have more budget for *all* stats, including both Speed and Bulk.

### **The problem**

Glass cannons are some of the most memorable Pokemon in competitive play — Alakazam, Gengar, Pheromosa — but they exist because individual designers chose to make them fragile, not because the system enforces fragility on fast Pokemon. The current design process produces glass cannons as happy accidents of individual stat allocation rather than as outputs of a deliberate design philosophy. This means the frequency and distribution of glass cannons across types, generations, and power tiers is essentially unmanaged. Meanwhile, the specialization premium (Stat Std Dev correlates with Stat Total at r \= 0.45, with a monotonic staircase from Low tier to Very High tier) confirms that stronger Pokemon *are* more specialized — but the axis of specialization is not predictably Speed-versus-Bulk.

### **The recommendation**

Formalize the glass cannon as a design role with explicit parameters rather than leaving it to emerge from ad hoc stat allocation. Define a Speed-to-Bulk ratio threshold (the data suggests a ratio above 1.5 reliably produces the "fast and fragile" gameplay feel) and tag designs that cross it during the prototyping phase. Set generation-level targets: for example, ensure that at least 8–12% of new Pokemon per generation fall into the glass cannon profile, distributed across physical and special orientations. Use the specialization premium intentionally — when a Pokemon's BST is high, spend the budget to sharpen its defining axis rather than rounding off weaknesses. The tradeoff between Speed and durability should be a conscious design lever, pulled on purpose, not a pattern that players imagine exists but the data says does not.

---

## **Recommendation 5: Design Around the HP Axis**

### **The finding**

A Gaussian Mixture Model (GMM) with BIC-based model selection identifies 14 natural clusters in the Pokemon stat space — and 10 of those 14 are type-pure. Type identity dominates clustering to such a degree that it absorbs most stat-shape variation. The four multi-type clusters represent the most analytically interesting finding: Blue-Collar Brawlers (Water \+ Fighting, 205 members) share a physical lean; Armored Heavyweights (Rock/Ground/Steel/Ice, 208 members) converge on highest Defense, slowest Speed, and heaviest BMI; Low-Stat Midtiers (Bug \+ Fire, 170 members) cluster at the bottom of overall stats; and Fragile Normals (Normal \+ Flying, 129 members) share the lowest BSTs with below-average defenses.

Notably absent from the 14-cluster solution is any HP-specialist archetype. Despite HP being the most inflated stat across generations (+12.8 points from Gen 1 to Gen 9), Pokemon with high HP are distributed across type-pure clusters rather than forming their own stat-shape alliance. The GMM also does not cleanly rediscover the seven rule-based combat roles, confirming that type membership exerts stronger gravitational pull on stat design than role archetype does.

### **The problem**

HP is the stat most subject to inflation, yet it has no dedicated design identity. Every other stat axis has recognizable archetypes: glass cannons (high Attack, low Defense), walls (high Defense, low offense), and speed demons are all familiar. But "HP tank" is not a consistently designed category — high-HP Pokemon are scattered across types and clusters without a unifying stat shape. This represents an untapped design axis. The multi-type clusters prove that cross-type stat alliances are possible and meaningful (208 Rock/Ground/Steel/Ice Pokemon converge on a shared defensive identity despite type differences), yet no equivalent alliance has formed around HP.

### **The recommendation**

Generation 10 should introduce a deliberate **HP-anchored design archetype** that spans multiple types — modeled on the cross-type alliances the GMM already detects. Concretely, this means designing 15–20 new Pokemon across at least four types that share a common stat shape: HP as the primary stat (130+), moderate mixed defenses, and low-to-moderate Speed. This would create a mechanically coherent cluster analogous to the Armored Heavyweights but organized around bulk through HP rather than through Defense. The data shows that type dominates stat clustering, but the multi-type clusters prove it does not have to. Where stat-shape similarity is strong enough, it overrides type boundaries. Intentionally designing around HP — the most inflated yet least architected stat — would channel existing inflationary pressure into a purposeful design identity rather than letting it diffuse invisibly across the roster.

---

## **Summary of Recommendations**

| \# | Recommendation | Key Data Point | Effort |
| ----- | :---- | :---- | :---- |
| 1 | Restore Legendary differentiation through stat-shape distinctiveness | \~150-pt gap persistent but porous at elite tier (top 25 overlap) | Medium — stat profile guidelines \+ pseudo-legendary BST cap |
| 2 | Embrace design diversification over uniform power creep | Stable medians \+ rising variance \= diversification, not inflation; Off/Def ratio steady at \~1.0 | Low — formalize existing trend with explicit diversity targets |
| 3 | Preserve type fingerprints as a design anchor | 18 distinct profiles stable across 9 gens; specialization premium r \= 0.45 | Low — documentation and awareness |
| 4 | Make the glass cannon tradeoff intentional | Speed-Bulk r \= \+0.18; Offense-Bulk r \= \+0.61 — both contradict "glass cannon" assumption | High — requires design philosophy decision \+ generation-level targets |
| 5 | Design around the HP axis | HP most inflated stat (+12.8 pts); no HP-specialist cluster in 14-cluster GMM; multi-type alliances prove cross-type archetypes are viable | Medium — new designs across 4+ types with shared HP-anchored stat shape |

---

## 

## 

## 

## 

## 

## 

## 

## 

## 

## 

## 

## 

## 

## **Data Sources and Methods**

- **Dataset:** 1,231 Pokemon, 55 columns, scraped from Bulbapedia and Pokemon Fandom Wiki  
- **Analysis methods:** Descriptive statistics, correlation analysis, grouped comparisons, distribution analysis, Gaussian Mixture Model clustering (BIC-optimal K=14), PCA dimensionality reduction  
- **Tools:** Python (pandas, numpy, seaborn, matplotlib, plotly, scikit-learn)  
- **Visualizations:** 25+ charts across 7 analytical sections covering body composition, type identity, specialization, speed-bulk dynamics, power creep, legendary status, and unsupervised clustering  
- **Key methodological note:** The ML capstone used a 27-feature GMM (6 base stat z-scores, 3 scaled derived ratios, 18 one-hot Type 1 columns). The inclusion of type encoding was a deliberate analytical choice that revealed type identity as the dominant organizing principle in the dataset — 10 of 14 clusters are type-pure, with 4 multi-type clusters providing the most novel cross-type insights.  
- **Reliability note:** The dataset includes all variant forms (Mega, Regional, etc.) flagged via an `Is Variation` column. Core findings were validated with and without variants included. Scraped data was cross-validated against known stat databases for accuracy.

---

# **Dashboard Assessment**

command: \`\`\`uv run python src/dashboard.py | firefox 127.0.0.1:8050\`\`\`

## **Key Takeaways From This Dashboard**

**Takeaway 1 — Type is destiny, power level is secondary.** The *Type Identity* tab reveals that each of the 18 primary types has a distinct, consistent stat fingerprint — Ground types are physically oriented (Physical/Special ratio \= 1.53), Psychic types are specially oriented (0.76), regardless of whether the individual Pokemon is weak or strong. This is immediately visible by comparing the radar charts across types: each polygon has a characteristic shape that holds when you filter to different generations or power tiers. The tab now shows fingerprints for both Type 1 and Type 2, using the same visual language as the EDA notebook's Section 2c: dark-shaded fills with white borders for Type 2 averages, light-shaded fills with black borders for Type 1\. For a game designer, this means type assignment is the single strongest predictor of how a Pokemon will play.

**Takeaway 2 — The "glass cannon" trope is not in the data.** The *Power & Specialization* tab's Speed vs. Bulk scatter shows a *positive* trendline — fast Pokemon are, on average, slightly *more* durable, not less. This is counterintuitive and becomes even more striking when you filter to Legendary-only: the fastest legendaries (Deoxys, Mewtwo) also have substantial bulk. The conventional RPG assumption that speed must trade against durability is a design choice that Game Freak has not enforced at the stat level.

**Takeaway 3 — Rule-based roles and data-driven clusters tell different stories.** The *Evolution & Roles* tab now shows both the 7 hand-crafted combat roles and the 14 GMM-discovered cluster roles side by side, stacked by evolution stage. The rule-based roles (Physical Sweeper, Tank, etc.) shift predictably as Pokemon evolve — more Sweepers at Stage 3, more Balanced at Stage 1\. The cluster roles reveal a different pattern: type-driven groupings like "Armored Heavyweights" (Rock/Ground/Steel/Ice) and "Blue-Collar Brawlers" (Water/Fighting) persist across all evolution stages, showing that type identity overrides evolution stage as an organizing principle. Filtering by both role types simultaneously using the Role dropdown confirms that these two classification systems capture complementary dimensions of the data.

## **Ease of Interpretation and Interaction**

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
- **GMM runs at startup.** The 14-cluster GMM model is refit each time the dashboard launches (\~1-2 seconds). Pre-computing and caching the cluster assignments in the CSV would eliminate this startup cost.

## **Dashboard Feature Highlights**

| Feature | Description |
| :---- | :---- |
| **6 global filters** | Generation, Type 1, Type 2, Role (rule \+ cluster), and Legendary status — all multi-select with OR logic for roles |
| **Role filter (21 options)** | 7 rule-based roles (`[Rule]` prefix) \+ 14 GMM cluster roles (`[Cluster]` prefix) in a single dropdown |
| **7 live KPI cards** | Count, Stat Total, Speed, BMI, Role, Legendary %, and Specialization update reactively |
| **6 themed tabs** | Overview, Type Identity, Power & Specialization, Generational Trends, Evolution & Roles, Pokemon Creator |
| **18+ interactive charts** | Bar, histogram, scatter (with OLS trendlines), radar (2c-style layered), stacked bar, and BMI comparison visualizations |
| **Hover tooltips** | Every data point shows individual Pokemon details on mouseover |
| **Dark theme** | Blue-tinted dark palette (`#1a1a2e` base) with gradient title, accented KPI cards, and glowing tab indicators |
| **Color coding** | Type-specific colors from the EDA's `TYPE_COLORS` palette, plus `TYPE_COLORS_LIGHT` and `TYPE_COLORS_DARK` for radar layering |
| **Pokemon Creator** | Full stat builder with 6 sliders (1-255), height/weight inputs, dual-type selectors, Legendary toggle, and reset button |
| **4 Creator comparison charts** | Radar overlay (2c-style Type 1/Type 2 layering), BST histogram with marker, BMI comparison, Speed-Bulk scatter with star marker |
| **GMM clustering** | 14-cluster Gaussian Mixture Model (27 features: 6 z-scores \+ 3 scaled ratios \+ 18 one-hot Type 1\) computed at startup |
| **Dual role systems** | Both rule-based (7 roles) and cluster-based (14 roles) classifications available in filters and Evolution & Roles tab |

## **Tab-by-Tab Chart Inventory**

### **Overview (3 charts)**

1. **BST Distribution** — Histogram of Stat Total, colored by Stat Tier, `bargap=0`  
2. **Role Distribution** — Horizontal bar of the 7 rule-based roles  
3. **Type 1 Distribution** — Horizontal bar of Type 1 counts  
4. **Type 2 Distribution** — Horizontal bar of Type 2 counts (non-null only)

### **Type Identity (4 charts)**

1. **Stat Fingerprints — Top 6 Type 1s** — 2x3 radar grid with light fills, 0.45 opacity, black borders  
2. **Stat Fingerprints — Top 6 Type 2s** — 2x3 radar grid with dark fills, 0.72 opacity, white borders  
3. **Physical / Special Ratio by Type** — Horizontal bar with red reference line at 1.0  
4. **Offensive / Defensive Ratio by Type** — Horizontal bar with red reference line at 1.0

### **Power & Specialization (3 charts)**

1. **Speed vs. Bulk** — Scatter with OLS trendline, Pearson r in title, colored by Generation  
2. **Offense vs. Bulk** — Same format, Offensive Total vs. Defensive Total  
3. **Specialization vs. Power** — Stat Std Dev vs. Stat Total, colored by Stat Tier

### **Generational Trends (3 charts)**

1. **Offensive vs. Defensive Balance** — 2-panel: line trends \+ Off/Def ratio with reference line  
2. **Individual Stat Trends** — 2x3 grid of per-stat mean trends across generations  
3. **Stat Total Distribution** — Box plots per generation with overall mean line

### **Evolution & Roles (4 charts)**

1. **Created Role Distribution by Evolution Stage** — Stacked bar of 7 rule-based roles by stage  
2. **Cluster Role Distribution by Evolution Stage** — Stacked bar of 14 GMM cluster roles by stage  
3. **Mean Stats by Evolution Stage** — Grouped bar of 6 stats across stages 1-3  
4. **Legendary Percentage by Generation** — Bar chart with percentage labels

### **Pokemon Creator (4 charts \+ form)**

- **Form inputs:** Name, Type 1, Type 2 (with "None"), 6 stat sliders (1-255), Height (m), Weight (kg), Legendary toggle, Reset All button  
- **Computed summary:** Stat Total, Std Dev, BMI, Role, Legendary status  
1. **Radar overlay** — Custom Pokemon vs. Type 1 average (light fill, black border) and Type 2 average (dark fill, white border, if selected)  
2. **BST Histogram** — Where the custom Pokemon falls in the overall distribution (red marker line)  
3. **BMI Comparison** — Custom Pokemon's BMI vs. dataset distribution (clipped at 200 for readability)  
4. **Speed-Bulk Scatter** — Custom Pokemon as a red star marker on top of the full dataset colored by type

