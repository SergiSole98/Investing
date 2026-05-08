## Context

Applies after news.md, events.md, and analysis_*.md have been loaded for an asset.
Extracts technical key levels and the daily opening gap from the analysis, scores
combined sentiment from news and events on a 1–5 scale, and produces an
investment thesis.

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
5. **Principle 2 — Gap alcista diario → Sesgo alcista:**
   a. Confirm that the latest candle opens above the immediately previous candle's close.
   b. Confirm that this comparison is strictly between one trading day/session and the next.
   c. If both conditions are met → include a SESGO ALCISTA thesis with narrative justification.
6. **Principle 3 — Short-term volume trend is not a signal:**
   a. Do not treat short-term volume increases or decreases as bullish or bearish evidence.
   b. Mention volume only as descriptive context when needed, never as a trigger.
7. If no principle is triggered → output SIN SEÑAL with a one-sentence summary of
   the current technical and sentiment state.
8. Do NOT confirm a principle without explicitly verifying its conditions.
9. Do NOT state price targets, stop-loss levels, or position sizing.
10. Write all output in Spanish.

## Reference

- `Agents/Technical_Analysis/Skills/technical_level_analysis.md` — proximate support
  definition (within 3% of current price).
- `Agents/Skills/poc_analysis.md` — congestion zone logic for support/resistance.

## Output

    ## Datos técnicos
    Precio actual: <precio>
    Hueco diario:
      - Apertura última sesión: <precio>
      - Cierre sesión anterior: <precio>
      - Tipo: <alcista/bajista/sin hueco>
    Soportes próximos (≤3%):
      - <nivel> — distancia: <X.X%>
      - ...

    ## Sentimiento
    Puntuación global: <1–5>
    Ítems evaluados:
      - [FECHA] <titular> — Puntuación: <1–5>
      - ...

    ## Evaluación de principios
    Principio activado: <nombre(s) o "Ninguno">
    Condiciones verificadas:
      - Soporte próximo: <sí/no — nivel, distancia%>
      - Sentimiento ≤ 2: <sí/no — puntuación global>
      - Gap alcista diario: <sí/no — apertura última sesión vs cierre anterior>
      - Tendencia de volumen a corto plazo: ignorada como señal según Principio 3

    ## Tesis
    <Párrafo en español: situación técnica + sentimiento + gap diario + conclusión. Sin recomendación
    de precio, stop ni sizing. Si SIN SEÑAL, describir estado actual en una frase.>

    ## Resumen
    <1–2 frases con la lectura final y los principios activados o descartados.>
