# What Nine Generations of Pokémon Data Actually Show

**Course:** CERT x465-003 — Data Interpretation and Application **Assignment:** 03 — EDA Video Presentation **Question:** Can we reverse-engineer the design logic behind Pokémon's stat system by analyzing patterns across nine generations?

---

## Introduction

This presentation walks through an Exploratory Data Analysis of 1,231 Pokémon across all nine generations (Gen 1 through Gen 9), using a custom-built dataset of 55 columns covering base stats, types, physical traits, evolution chains, legendary status, and derived metrics.

The question guiding this investigation: **does the data reveal a coherent design logic — or does it expose patterns that accumulated accidentally over 25+ years?**

Eight analytical sections follow, each posing a specific sub-question. Findings are reported as-seen, without prescription.

---

## Section 1: Does Physical Body Shape Predict How a Pokémon Fights?

The EDA classifies each Pokémon into one of seven combat roles based on its stat distribution:

Role

Definition

**Physical Sweeper**

High Attack and Speed; built to hit first and hit hard with physical moves

**Special Sweeper**

High Special Attack and Speed; same offensive intent but through the special damage channel

**Mixed Attacker**

High in both Attack and Special Attack; threats that can't be walled by a single defensive stat

**Balanced**

No dominant stat; generalist profile without a clear offensive or defensive identity

**Tank**

High HP and both defensive stats; absorbs hits from any angle while retaining offensive presence

**Physical Wall**

Specialized in Defense and HP; shuts down physical attackers at the cost of special vulnerability

**Special Wall**

Specialized in Special Defense and HP; the mirror of Physical Wall

BMI in the dataset follows a heavy right skew — most Pokémon cluster in a low-to-moderate range, with a long outlier tail pulled by extreme cases like Cosmoem (a near-zero-height, 999.9 kg Pokémon with a BMI of approximately 100,000) and Celesteela. Once outliers are filtered, the distribution settles around a median of roughly 28.

**What the data shows:** Physical Wall and Tank roles do cluster toward higher BMIs. Ghost and Fairy types anchor the low-BMI extreme. Median BMI has trended upward across generations — Pokémon designs have gotten physically denser on average since Gen 1.

**Conclusion:** Body shape is a weak-to-moderate predictor of combat role. The relationship exists but is noisy. Physical heft correlates with defensive roles, but there are enough counter-examples (very light physical attackers, very heavy special sweepers) that BMI alone is not diagnostic.

---

## Section 2: Does Primary Type Determine a Pokémon's Fighting Personality?

Each of the 18 types has a measurable stat "fingerprint" — a characteristic ratio of physical-to-special offense and offense-to-defense that holds across individual power levels.

**What the data shows:**

-   Ground types are the most physically oriented (Physical/Special ratio ≈ 1.53)
-   Psychic types are the most specially oriented (≈ 0.76)
-   Electric types are the most offensively skewed (Offensive/Defensive ≈ 1.31)
-   Rock types are the most defensively skewed (≈ 0.87)

Dual-typed Pokémon show nearly identical ratio distributions to mono-typed Pokémon — adding a second type does not measurably blur the primary type's stat identity.

**Conclusion:** Type is one of the strongest predictors of combat personality in the dataset — stronger than generation, stronger than power level. The fingerprints are stable and consistent. Dragon is the notable exception: it shows the flattest radar profile of all 18 types, suggesting it functions as a "generalist" archetype rather than a specialized one.

---

## Section 3: Do More Powerful Pokémon Become More One-Dimensional?

The Specialization Premium question: does raw power require giving up versatility?

**What the data shows:** Stat Standard Deviation (a measure of how unevenly a Pokémon's stats are distributed) correlates with Stat Total at r = +0.45. "Very High" tier Pokémon have measurably higher Stat Std Dev than "Low" tier Pokémon — they are not just stronger, they are more extreme in one dimension. Tanks and Walls are the exception: they reach high totals while maintaining relatively balanced distributions.

**Conclusion:** The data supports a specialization premium. Power tends to come with asymmetry. The game rewards going all-in. The exceptions — Tanks and Walls — are designed to be high-total and well-rounded simultaneously, which is a coherent design choice for the "unmovable fortress" archetype.

---

## Section 4: Is "Fast = Fragile" a Real Design Rule?

One of the most intuitive assumptions in Pokémon is that fast Pokémon trade bulk for speed. The data tests this directly.

**What the data shows:** The overall Pearson r between Speed and Bulk (HP + Defense + Special Defense) is slightly negative, but the signal is weak. When broken down by generation, the correlation fluctuates between -0.1 and +0.1 for most generations — never strongly negative. Speed Tier and Stat Tier correlate at r = +0.47: fast Pokémon tend to be *stronger overall*, not more fragile.

When testing Offense (Attack + Special Attack) vs. Bulk directly, the correlation is r = +0.61 — strongly *positive*. High-offense Pokémon are, on average, more durable, not less.

**Conclusion:** The "fast = fragile" rule does not hold in the base stats. The glass cannon archetype exists in the metagame through movepools, abilities, and type matchups — but the stat architecture does not enforce it. This is one of the larger surprises in the data.

---

## Section 5: Has Offensive Power Inflated Faster Than Defense?

Power creep — the gradual escalation of stat totals over time — is well-known in the Pokémon community. The question is whether it is symmetric.

**What the data shows:** Both Offensive Total and Defensive Total have risen across generations, but not at the same rate. Offensive Total shows a steeper slope, particularly after Gen 5. The Offensive/Defensive ratio trends upward in later generations. Among individual stats, HP has inflated the most of any single stat (+12.8 points from Gen 1 median to Gen 9 median), followed by Special Attack.

Speed shows increased bimodality in later generations — the distribution spreads out, with more very-fast and very-slow Pokémon and fewer in the middle.

**Conclusion:** Power creep is real and slightly offense-biased. The game is getting more offensive on average, though the effect is modest relative to the overall variance. The HP inflation is notable because it is the least visible stat — players track Attack and Speed more closely, but HP has quietly been rising.

---

## Section 6: Is the Legendary Gap Closing?

**What the data shows:** In Generation 3, the mean Stat Total gap between Legendary and non-Legendary Pokémon was 237.8 points. By Generation 7, it had dropped to 129.2. Generation 9 is similarly compressed at 134.3.

The top 50 non-Legendary Pokémon by Stat Total are dominated by Gen 1 designs — largely because Mega Evolutions pushed classic Pokémon into Legendary stat territory.

**Conclusion:** The Legendary gap has narrowed significantly. Legendary status is a weaker signal of raw power than it was in the franchise's early generations. This may be an intentional design shift (Legendaries now win through abilities and lore rather than raw stats) or an unintended drift — the data cannot distinguish between those two interpretations.

---

## Section 7: What Does Unsupervised Clustering Reveal?

Using K-Means clustering on the six z-score stat columns (no labels provided), with K=7 chosen to match the seven rule-based roles:

**What the data shows:** The algorithm partially recovers the designed role taxonomy but makes two notable deviations:

1.  It merges Physical Sweeper and Special Sweeper into a single "high-offense" cluster more often than separating them, suggesting the data views them as more similar than the rule-based system does.
2.  It carves out a cluster the role system does not name: "HP Titans" — 22 Pokémon whose defining characteristic is extreme HP (avg 170.8, more than triple the dataset average), including Zygarde Complete Forme, Regidrago, Guzzlord, and Iron Hands. The rule system distributes these across four different role labels.

PCA explains approximately 60–65% of variance in two components, with PC1 broadly tracking overall power and PC2 tracking physical-vs-special orientation.

**Conclusion:** The designed role taxonomy is mostly supported by the data, but the HP Titan cluster is a genuine gap — the rule system doesn't have a label for Pokémon whose primary identity is extreme HP rather than extreme offense or defense. K-Means found this archetype without being told to look for it.

---

## Overall Conclusions

Across eight analytical sections, four consistent signals emerge:

1.  **Type identity is the strongest and most stable design axis.** Type predicts combat personality reliably, across power levels and generations.
    
2.  **The specialization premium is real.** Power comes with asymmetry. The game rewards one-dimensional excellence more than well-rounded competence (with the intentional exception of walls and tanks).
    
3.  **Several assumed tradeoffs do not appear in the stats.** The glass cannon rule and the fast-equals-fragile rule are metagame conventions, not stat architecture. The data contradicts both.
    
4.  **The game has drifted in ways the data can detect but cannot explain.** The narrowing Legendary gap and the offense-biased power creep are measurable trends — whether they are intentional design decisions or emergent drift from 25 years of game design is a question the data cannot answer alone.
    

---

## How Different Audiences Might Interpret This Differently

**Competitive players** would likely focus on the offense-bulk positive correlation (r = +0.61) as evidence that the competitive metagame has good reason to run bulky offensive Pokémon — the data supports that strategy as rational, not just a metagame quirk.

**Casual fans** might read the narrowing Legendary gap as a good thing — it means their favorite non-Legendary Pokémon can now compete with Legendaries they previously couldn't — rather than as a weakening of Legendary identity.

**Game designers at Game Freak** would probably be most interested in the HP Titan gap: a cluster the data found that their own role taxonomy missed. That's a concrete signal that the design space has an unnamed archetype.

**Skeptics of the Pokemon franchise** might interpret the offense-biased power creep and narrowing Legendary gap as evidence of design fatigue — that Game Freak is running out of new design space and papering over it with stat inflation. The same data that competitive players read as "strategically rich" could be read as "unintentionally escalating."

**Data science practitioners** would note the tension between the rule-based role classification and the K-Means results: the fact that an unsupervised algorithm at K=7 doesn't fully recover the 7 designed roles is a signal that the rule system is slightly misspecified — either too many categories in some areas (Sweeper split) or too few in others (the HP Titan gap).

---

## Dataset and Methods

-   **Dataset:** 1,231 Pokémon, 55 columns, scraped from Bulbapedia and Pokémon Fandom Wiki
-   **Analysis methods:** Descriptive statistics, distribution analysis, correlation analysis, grouped comparisons, K-Means clustering (K=7), PCA dimensionality reduction
-   **Tools:** Python (pandas, numpy, seaborn, matplotlib, plotly, scikit-learn)
-   **Reliability note:** All variant forms (Mega, Regional, etc.) are included and flagged via an `Is Variation` column. Key findings were validated with and without variants. Scraped data was cross-checked against known stat databases.