# News credibility scoring

## Context
Credibility tier system for evaluating news and event sources. Apply when scoring the reliability of a news item based on its original publishing outlet.

## Rules

1. Assign credibility based on the **original publishing outlet**, not the aggregator that republished it.

2. **Tier definitions:**
   - **3:** Strong indicator — high reliability, solid basis for decision-making.
   - **2:** Medium indicator — useful as confirmation, not as sole basis.
   - **1:** Weak indicator — informational but unreliable, can mislead.

3. **International sources:**

   | Source | Credibility |
   |--------|-------------|
   | Reuters | 3 |
   | Bloomberg | 3 |
   | Wall Street Journal | 3 |
   | CNBC | 2 |
   | Twitter/X | 1 |

4. **Spanish sources (IBEX 35):**

   | Source | Credibility |
   |--------|-------------|
   | Reuters / Bloomberg | 3 |
   | Expansión | 2 |
   | Cinco Días | 2 |
   | El Economista | 1 |
   | Bolsamanía / Investing.com España | 1 |

5. All sources not listed above default to credibility 1.
6. Credibility 3 sources are the basis for analysis. Credibility 1 sources may only confirm a dominant narrative already established by higher-tier sources; never use them as the sole basis for a high impact score.
