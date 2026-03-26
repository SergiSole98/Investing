# News impact scoring

## Context
Principles for evaluating the impact score (1-10) of a news item or scheduled event on an asset's price. Apply when assigning the impact dimension in news scoring.

## Rules

1. Score based on how directly and significantly the item could move the asset's price within the 4h-7d horizon. Score 10 for events with a direct, immediate transmission channel and large expected magnitude; score 1 for tangential items with minimal price relevance.

2. **Real deadlines move markets, not narratives.** Identify the real clock running in each situation (expiry dates, policy meetings, regulatory rulings, contractual deadlines). Items with a concrete, dated deadline score higher than open-ended narratives without a time constraint.

3. **Facts outweigh declarations.** Classify each item as **fact** (something that has occurred and is verifiable) or **declaration** (something someone says will happen). Facts score higher than declarations. Declarations are noise until they materialize into action — score them lower unless a binding mechanism or verifiable deadline exists.

4. **Political declarations** default to credibility 1 regardless of outlet tier, unless all three filters are met: (1) the emitter has a clear electoral/power incentive aligned with the claim, (2) there is a real cost to the emitter if the declaration proves false, and (3) a verifiable deadline or enforcement mechanism exists.

5. **Every event has precedents — check the historical distribution before reacting.** Before scoring impact, identify 3-5 comparable historical events. For each precedent, document: cause, price effect, time horizon of the impact, and macro context at the time. Establish the range of outcomes (best case, worst case, base case) from the historical distribution. The impact score must reflect where the current event falls within that historical range, not intuition or panic. If no precedents are found, state it explicitly — this signals higher uncertainty and the impact score must reflect that ambiguity.
