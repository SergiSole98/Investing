## Context

Fixed structure for agent documents. One file = one agent. Each section has a specific purpose; do not mix content across sections.

## Rules

### Role — what it is and what it is not

1. **Definition:** Who the agent is, what it produces, and what is **outside** its mandate (in one sentence or a short paragraph).
2. **Include:** Agent name, responsibility verb (**you draft**, **you analyze**, **you filter**...), and file/folder scope if needed.
3. **Forbidden in Role:** step lists (that is Task), long policies (Rules), output templates (Output), and skill paths unless they define identity in one line.
4. **Test:** If it sounds like "how to do it step by step" or "never do X," it is not Role.

### Task — what it is and what it is not

5. **Definition:** Sequence **1 -> 2 -> 3** of what the agent does in a typical request. Only **verbs** and clear order.
6. **Include:** Maximum **3-7** steps. Each step = one executable action.
7. **Forbidden in Task:** long conditionals ("if... then..." in extended form), repeated "do not / always," style rules - those belong in **Rules**.
8. **Test:** "Is this a step that always happens in the flow?" Yes -> Task. "Is it an exception or limit?" -> Rules.

### Context — what it is and what it is not

9. **Definition:** **Where** the agent operates (meta vs domain), **what** the user is assumed to already know, and **what** it will not do even if requested in the same conversation when it is a different deliverable.
10. **Include:** Bullets or short paragraphs: meta-agent vs domain agent, "one file = one X," and how to handle mixed requests.
11. **Forbidden in Context:** imperative commands that must always be followed as policy (move those to **Rules**). If the text says "do / do not do" as a norm, it is not Context.
12. **Test:** "Does this describe the playing field?" Yes -> Context. "Does this enforce or punish behavior?" -> Rules.

### Rules — what it is and what it is not

13. **Definition:** Limits, blocking conditions, policies, conditionals, and references to other guides ("apply X").
14. **Format:** **Number** each rule (`1.`, `2.`, `3.`...). **One instruction per line** (or one idea per item); no paragraphs with mixed commands.
15. **Include:** "without data, do not deliver Output," strict scope, source of truth, and when to ask vs act.
16. **Forbidden in Rules:** repeating word-for-word what is already in Reference; "apply [path or name]" is enough.
17. **Test:** Each rule must prevent **one** concrete failure; otherwise delete it.
18. **Assumptions:** valid only for minor format/style details that do not alter behavior. If it affects logic or scope -> ask, do not assume.
19. **Source of truth:** only the original request and the user's clarifications in the conversation.
20. Do not repeat in Rules — verbatim or paraphrased — what is already covered 
    by a referenced skill. If the skill covers it, "apply [path]" is enough. 
    When in doubt, delete the rule.


### Remaining sections

21. **Reference:** Paths to documentation or guides the agent must read. Include only what the user explicitly requests or what is essential for the role.
22. **Output:** Exact delivery format. Templates, required headers, verbosity constraints. Do not include an "Assumptions" section in Output.
23. **Drafting order:** First objective (Role, Task, Context) -> then limits (Rules) -> then dependencies (Reference) -> then format (Output).
24. Do not reference other agents inside Role, Task, Context, or Rules. 
    Cross-agent references belong only in **Reference**.
25. **Skill routing:** Cursor skills live in `.cursor/skills/`; agent skills live in `Skills/`. Confirm type before delegating to `Agents/sofia.md`.