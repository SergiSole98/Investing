# Writing agent skill

## Context

Estructura fija para documentos de agente. Un archivo = un agente. Cada sección tiene un propósito; no mezclar contenidos entre secciones.

## Rules

### Role — qué es y qué no

1. **Definición:** Quién es el agente, qué produce y qué queda **fuera** de su mandato (en una frase o párrafo corto).
2. **Incluye:** Nombre del agente, verbo de responsabilidad (**redactas**, **analizas**, **filtras**…), alcance de archivos/carpetas si aplica.
3. **Prohibido en Role:** listas de pasos (eso es Task), políticas largas (Rules), plantillas de salida (Output), rutas a skills salvo que definan identidad en una línea.
4. **Test:** Si suena a “cómo hacerlo paso a paso” o “nunca hagas X”, no es Role.

### Task — qué es y qué no

5. **Definición:** Secuencia **1 → 2 → 3** de lo que el agente hace en un encargo típico. Solo **verbos** y orden claro.
6. **Incluye:** Máximo **3–7** pasos. Cada paso = una acción ejecutable.
7. **Prohibido en Task:** condicionales largos (“si… entonces…” extensos), “no hagas / siempre” repetidos, reglas de estilo — eso va en **Rules**.
8. **Test:** “¿Es un paso que siempre ocurre en el flujo?” Sí → Task. “¿Es una excepción o límite?” → Rules.

### Context — qué es y qué no

9. **Definición:** **Dónde** opera el agente (meta vs dominio), **qué** asume el usuario ya sabe, **qué** no va a hacer aunque se pida en la misma conversación si es otro entregable.
10. **Incluye:** Bullets o párrafos cortos: meta-agente vs agente de dominio, “un archivo = un X”, cómo tratar requests mixtas.
11. **Prohibido en Context:** órdenes imperativas que deban cumplirse siempre como política (muévelas a **Rules**). Si el texto dice “haz / no hagas” como norma, no es Context.
12. **Test:** “¿Esto describe el terreno de juego?” Sí → Context. “¿Esto castiga o exige conducta?” → Rules.

### Rules — qué es y qué no

13. **Definición:** Límites, bloqueos, políticas, condicionales, citas a otras guías (“aplica X”).
14. **Formato:** **Numerar** cada regla (`1.`, `2.`, `3.`…). **Una instrucción por línea** (o una idea por ítem); no párrafos con varias órdenes mezcladas.
15. **Incluye:** “sin datos no entregas Output”, alcance estricto, fuente de verdad, cuándo preguntar vs actuar.
16. **Prohibido en Rules:** repetir palabra por palabra lo ya dicho en Reference; basta “aplica [ruta o nombre]”.
17. **Test:** Cada regla debe evitar **un** fallo concreto; si no, elimínala.
18. **Supuestos:** solo válidos para detalles menores de formato/estilo que no alteran comportamiento. Si afecta lógica o alcance → preguntar, no asumir. No incluir sección "Supuestos" en Output.
19. **Fuente de verdad:** solo la request original y las aclaraciones del usuario en la conversación.

### Resto de secciones

20. **Reference:** Rutas a documentación o guías que el agente debe leer. Solo las que el usuario pida explícitamente o que sean imprescindibles para el rol.
21. **Output:** Formato exacto de la entrega. Plantillas, headers obligatorios, restricciones de verbosidad.
22. **Orden de redacción:** Primero objetivo (Role, Task, Context) → luego límites (Rules) → luego dependencias (Reference) → luego formato (Output).
23. **Sin cruces entre agentes:** Un agente no menciona a otro agente (nombres, personalidades ni rutas a otros ficheros en `Agents/`). El alcance se define solo con su propio rol y límites.
