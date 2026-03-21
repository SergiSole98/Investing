# Writing agent skill

## Context

Estructura fija para documentos de agente. Un archivo = un agente. Cada sección tiene un propósito; no mezclar contenidos entre secciones.

## Rules

1. **Role:** Identidad y alcance del agente. No meter prohibiciones ni formato de salida.
2. **Task:** Pasos concretos y accionables. Solo lo que se ejecuta siempre. Lo condicional va en Rules.
3. **Context:** Dominio, supuestos, qué queda fuera de su responsabilidad. Genérico salvo que el usuario acote.
4. **Rules:** Límites, bloqueos, políticas, condicionales. Una instrucción por línea. **Numerar** cada regla (`1.`, `2.`, `3.`…).
5. **Reference:** Rutas a documentación o guías que el agente debe leer. Solo las que el usuario pida explícitamente.
6. **Output:** Formato exacto de la entrega. Plantillas, headers obligatorios, restricciones de verbosidad.
7. **Orden de redacción:** Primero objetivo (Role, Task, Context) → luego límites (Rules) → luego dependencias (Reference) → luego formato (Output).
8. **Sin cruces entre agentes:** Un agente no menciona a otro agente (nombres, personalidades ni rutas a otros ficheros en `Agents/`). El alcance se define solo con su propio rol y límites.
