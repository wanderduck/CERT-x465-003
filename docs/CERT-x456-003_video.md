#  **CERT x465-003**: Data Interpretation and Application

## Video Presentation Notes

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

---

## Question 1

-   Does physical body shape/size predict Pokémon type or combat role?
-   Pokémon are assigned one of the seven roles as defined and then their BMI is analyzed to see if there is any correlation to their role vs. physical size

  

### Graph Q1.A: BMI Distribution

-   The distribution is heavily right-skewed
-   Most Pokemon cluster in the 10-60 BMI range, with a pronounced peak near 20-30
-   However, the tail extends to extreme values — most notably Cosmoem, whose 0.1 m height and 999.9 kg mass produce a BMI of approximately 99,990

#### Graph Q1.A Conclusion

-   This skew has practical consequences: any analysis using BMI must account for these outliers, either through clipping, log-transformation, or exclusion, to avoid distorted summary statistics

  

### Graph Q1.B: BMI by Combat Role

-   Violin plots display the BMI distribution for each of the seven combat roles, with embedded box plots and mean lines to facilitate comparison
-   Physical Walls and Tanks exhibit moderately higher median BMI values, consistent with the intuition that bulkier, heavier Pokemon gravitate toward defensive roles
-   Sweepers — both Physical and Special — skew lighter
-   **However**: *the overlap between distributions is substantial*
-   Every role contains Pokemon across a wide BMI range, and the interquartile ranges overlap heavily

#### Graph Q1.B Conclusion

-   BMI alone is a weak predictor of combat role

  

### Graph Q1.C: Mean Height x Mean Weight by Combat Role

-   Bubble scatter plot on log-log axes positions each of the 18 primary types by its mean height (x-axis) and mean weight (y-axis)
    -   Bubble size encodes the number of Pokemon belonging to each type, and color follows the standard 18-type palette
-   Steel and Rock types anchor the heavy end of the distribution, reflecting their thematic association with dense, metallic, or geological body plans
-   Bug and Fairy types sit at the opposite extreme — small and light

#### Graph Q1.C Conclusion

-   The log-log relationship between mean height and mean weight is approximately linear, suggesting a power-law scaling relationship: across types, weight scales roughly as a fixed power of height
-   This is consistent with real-world allometric scaling in biology, a notable parallel given that Pokemon dimensions are designer-assigned rather than naturally evolved.

  

### Graph Q1 Overall Conclusion

-   Body composition provides a weak and unreliable signal for combat role classification
    -   Physical Walls tend to be heavier and Sweepers tend to be lighter
    -   However the distributions overlap far too much for BMI, height, or weight to function as meaningful predictors
    -   The extreme right-skew is driven by outliers like Cosmoem and the dense Steel/Rock types dominate the distributional tail
    -   BMI is stable across generations
-   **Physical dimensions reflect thematic design choices more than competitive function**

---

## Question 2