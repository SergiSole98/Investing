# Skill writing skill

## Context
Estructura fija para Agent Skills de Cursor. Un archivo = una skill. Formato CRR: Context, Rules, Reference. Sin Role, sin Task, sin Output — esos son del agente que la consume.

## Rules
1. **Context:** Cuándo y dónde aplica la skill. 1-2 líneas.
2. **Rules:** Instrucciones concretas, una por línea. Sin explicaciones de por qué.
3. **Reference:** Ejemplos de input/output solo si el formato importa. Si las reglas son autoexplicativas, omitir.
4. Los tres bloques son opcionales — solo incluir los que aporten. No rellenar por completar.
5. Máxima concisión. Cada token se carga en contexto de cada agente que consume la skill.