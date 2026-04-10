# News Search

## Context
Applies when an agent searches for news on an asset within the last 7 days for a 4h–7d investment horizon.

## Rules
1. Prioritize items published **today or yesterday** — surface them first regardless of relevance score.
2. Include items from 2–7 days ago only if no more recent coverage exists on the same development.
3. Include an item only if it could **shift the general market perspective on the asset or directly cause a price move** within 4h–7d: narrative-changing events, expectation revisions, new risks or catalysts. Exclude human-interest pieces, broad market commentary without direct asset link, and repeat articles that restate the same disclosed fact without new figures.
4. Order the final list **most-recent first** (today → yesterday → earlier).
5. Add a `Recency:` field to each item: `today`, `yesterday`, or `N days ago`.
