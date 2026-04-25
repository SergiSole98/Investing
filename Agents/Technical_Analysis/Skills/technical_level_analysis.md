# Technical level analysis

## Context
Applies after the current price and POC supports/resistances are loaded for a technical analysis report.
Use it to select nearby levels and classify congestion zones.

## Rules
1. Split supports below the current price and resistances above the current price using `price_center`.
2. Calculate each level's distance from the current price as a percentage of the current price.
3. Flag every level within 3% of the current price as **proximate**.
4. Report a maximum of 3 proximate supports and 3 proximate resistances, ordered by closest distance.
5. If no level is within 3% of the current price, report the single nearest support below and the single nearest resistance above with their distances.
6. State clearly when no support below or no resistance above exists in the POC data.
7. Apply `Agents/Skills/poc_analysis.md` when any proximate support and proximate resistance are within 1% of each other.
8. Do NOT invent levels that are not present in the POC data.

## Reference
- `Agents/Skills/poc_analysis.md` — Congestion zone classification for nearby POC support/resistance levels.
