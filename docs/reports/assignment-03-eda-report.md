**CERT x465-003**: Data Interpretation and Application  
Video Presentation Notes

---

## **1.** Dataset

### Where

-   The dataset was scraped from two sources:
    1.  [https://bulbapedia.bulbagarden.net](https://bulbapedia.bulbagarden.net)
    2.  [https://pokemon.fandom.com](https://pokemon.fandom.com)

### How

-   This was done with **python** and the **playwright** library
-   Other libraries used:
    -   **pandas**: data manipulation
    -   **plotly**: visualization and dashboard creation
    -   **scikit-learn**: machine learning clustering algorithms
    -   **RAPIDS**: GPU acceleration

### What

-   This report presents a systematic exploratory data analysis of 1,231 Pokemon spanning nine generations of the franchise.
-   The dataset comprises 55 columns covering base stats, typing, physical traits, evolution data, and a suite of derived metrics including:
    -   combat ratios
    -   z-scores
    -   stat tiers
    -   rule-based combat role classifications
-   The analysis is organized around a series of focused questions, each investigated through purpose-built visualizations

### Questioning the Dataset

1.  Does physical body shape/size predict Pokémon type or combat role?
2.  Does type determine fighting personality?
3.  Do more powerful Pokémon become one-dimensional in stats?
4.  Do the tropes of “fast equals fragile” or “glass cannon” exist in the world of Pokémon?
5.  Have stats inflated with newer generations of Pokémon?
6.  Has the gap between Legendary and ordinary Pokemon closed?

### Machine Learning Capstone

-   *Question*: Without using any predefined labels, can the data's own structure rediscover the combat role archetypes defined earlier in this analysis — and reveal groupings that rule-based classification missed?
-   *Method*: **Algorithmic Clustering**: A Gaussian Mixture Model (GMM) was fitted using Bayesian Information Criterion (BIC) for model selection, using a feature set of twenty-seven dimensions.

### Combat Roles Explained

Role

Definition

**Physical Sweeper**

High Attack and Speed; built to hit first and hit hard with physical moves.

**Special Sweeper**

High Special Attack and Speed; same offensive intent but through the special damage channel.

**Mixed Attacker**

High in both Attack and Special Attack; threats that can't be walled by a single defensive stat.

**Balanced**

No dominant stat; generalist profile without a clear offensive or defensive identity.

**Tank**

High HP and both defensive stats; absorbs hits from any angle while retaining offensive presence.

**Physical Wall**

Specialized in Defense and HP; shuts down physical attackers at the cost of special vulnerability.

**Special Wall**

Specialized in Special Defense and HP; the mirror of the Physical Wall.