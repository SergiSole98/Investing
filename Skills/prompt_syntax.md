# Sintaxis de prompts

## Context
Convenciones de formato para instrucciones dentro de documentos de agente o prompts sueltos.

## Rules
1. Separar bloques con XML tags: `<role>`, `<context>`, `<rules>`, `<output>`. Nunca mezclar identidad con restricciones.
2. Una instrucción por línea. Numerar pasos. Nunca dos instrucciones en un párrafo.
3. **Negrita** y MAYÚSCULAS solo para 2-3 reglas críticas que el modelo tiende a violar.
4. Incluir un `<example>` con input/output cuando el formato importa. Un ejemplo, no dos.
5. Primero instrucciones, luego restricciones. El objetivo antes que los límites.
6. Silencio explícito: `Do NOT...` / `NEVER...` / `Respond ONLY with...` para lo que no quieres en el output.
7. Máxima concisión. Si cabe en 5 palabras, no usar 15.