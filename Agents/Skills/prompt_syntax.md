# Prompt syntax

## Context
Formatting conventions for writing LLM instructions.

## Rules
1. Use markdown headers (`##`) to separate sections. Never mix content between sections.
2. One instruction per line. Number steps. Never two instructions on the same line.
3. **Bold** only for 2-3 critical rules. Avoid CAPS.
4. Instructions first, then constraints. Objective before limits.
5. Use `Do NOT` / `NEVER` / `Respond ONLY with` for explicit exclusions.
6. Maximum conciseness: if it fits in 5 words, do not use 15.
7. Use clear prose instead of symbolic notation: symbols are ambiguous and the model interprets them rather than executing them.
8. Use words with unambiguous meaning; discard those that admit more than one interpretation.
9. Los documentos generados deben estar en español, salvo que un agente requiera explícitamente otro idioma por razones de formato o integración.
