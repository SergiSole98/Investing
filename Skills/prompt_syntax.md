# Sintaxis de prompts

## Context
Convenciones de formato para instrucciones a los LLMs.

## Rules
1. Separar bloques con XML tags: `<role>`, `<context>`, `<rules>`, `<output>`. Nunca mezclar identidad con restricciones.
2. Una instrucción por línea. Numerar pasos. Nunca dos instrucciones en un párrafo.
3. **Negrita** y MAYÚSCULAS solo para 2-3 reglas críticas.
4. Primero instrucciones, luego restricciones. El objetivo antes que los límites.
5. Silencio explícito: `Do NOT...` / `NEVER...` / `Respond ONLY with...` para lo que no quieres en el output.
6. Máxima concisión. Si cabe en 5 palabras, no usar 15.
7. Usa prosa clara en lugar de notación simbólica: los símbolos son ambiguos y el modelo los interpreta en lugar de ejecutarlos.
8. Usa palabras de significado inequívoco; descarta las que admitan más de una interpretación.