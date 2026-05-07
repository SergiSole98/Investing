## Context

Applies after news.md, events.md, and analysis_*.md have been loaded for an asset.
Extracts technical key levels from the analysis, scores combined sentiment from news
and events on a 1–5 scale, and produces an investment thesis.

## Rules

1. Read `analysis_*.md` and extract: current price, all proximate support levels
   (at or within 3% below current price), and the percentage distance to each.
2. Read `news.md` and `events.md`; assign an individual sentiment score to each item:
   1 = very negative, 2 = negative, 3 = neutral, 4 = positive, 5 = very positive.
3. Calculate the global sentiment score as the weighted average of all items, giving
   higher weight to items published or scheduled within the next 24 hours.
4. **Principle 1 — Support + Sentiment ≤ 2 → Long:**
   a. Confirm that the current price is at or within 3% above a proximate support level.
   b. Confirm that the global sentiment score is ≤ 2.
   c. If both conditions are met → produce a LARGO thesis with narrative justification.
5. If no principle is triggered → output SIN SEÑAL with a one-sentence summary of
   the current technical and sentiment state.
6. Do NOT confirm a principle without explicitly verifying both of its conditions.
7. Do NOT state price targets, stop-loss levels, or position sizing.
8. Write all output in Spanish.

## Reference

- `Agents/Technical_Analysis/Skills/technical_level_analysis.md` — proximate support
  definition (within 3% of current price).
- `Agents/Skills/poc_analysis.md` — congestion zone logic for support/resistance.

## Output

    ## Datos técnicos
    Precio actual: <precio>
    Soportes próximos (≤3%):
      - <nivel> — distancia: <X.X%>
      - ...

    ## Sentimiento
    Puntuación global: <1–5>
    Ítems evaluados:
      - [FECHA] <titular> — Puntuación: <1–5>
      - ...

    ## Evaluación de principios
    Principio activado: <nombre o "Ninguno">
    Condiciones verificadas:
      - Soporte próximo: <sí/no — nivel, distancia%>
      - Sentimiento ≤ 2: <sí/no — puntuación global>

    ## Tesis
    <Párrafo en español: situación técnica + sentimiento + conclusión. Sin recomendación
    de precio, stop ni sizing. Si SIN SEÑAL, describir estado actual en una frase.>
