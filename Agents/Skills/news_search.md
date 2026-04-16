# News Search

## Context
Applies when an agent searches for news on an asset within the last 3 days for a 4h–7d investment horizon.

## Rules
1. Prioritize items published **today or yesterday** — surface them first regardless of topic or relevance.
2. Include items from 2–3 days ago; do not filter by impact, topic type, or perceived relevance — collect all items.
3. Discard only exact duplicates: same fact, same figures, no new data. Keep all other items regardless of topic (product news, software updates, regulatory, analyst calls, executive statements, market data, human-interest if published by a recognized source).
4. Order the final list **most-recent first** (today → yesterday → earlier).
5. Add a `Recency:` field to each item: `today`, `yesterday`, or `N days ago`.
