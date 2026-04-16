# Skill writing skill

## Context
Fixed structure for agent skill files. One file = one skill. Format CRR: Context, Rules, Reference. No Role, no Task, no Output — those belong to the agent that consumes the skill.

## Rules
1. **Context:** When and where the skill applies. 1-2 lines max.
2. **Rules:** Concrete instructions, one per line. No explanations of why.
3. **Reference:** Input/output examples only if format matters. Omit if rules are self-explanatory.
4. All three blocks are optional — include only those that add value. Do not fill for completeness.
5. Maximum conciseness: every token loads into the context of every agent that consumes the skill.
6. Do not repeat — verbatim or paraphrased — what is already covered by a referenced skill. When in doubt, delete the rule.
7. Skill files live in `Agents/Skills/`. Do not place them in `Agents/` or other folders.