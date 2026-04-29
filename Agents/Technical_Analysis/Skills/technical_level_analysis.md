# Technical level analysis

## Context
Applies after the current price and POC supports/resistances are loaded for a technical analysis report.

## Rules
1. Identify the nearest support levels below the current price and the nearest resistance levels above it.
2. Flag any level within 3% of the current price as **proximate**.
3. Apply `Agents/Skills/poc_analysis.md` to detect congestion zones among proximate levels.

## Reference
- `Agents/Skills/poc_analysis.md` — Congestion zone classification for nearby POC support/resistance levels.
