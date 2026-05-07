## Context

Applies after news.md, events.md, and analysis_*.md have been loaded for an asset.
Evaluates the data against the active investment principles and produces a single
recommendation.

## Rules

1. Read and parse the three input files before evaluating any principle.
2. Apply principles in order; stop at the first triggered principle.
3. **Principle 1 — Support + Negative News → Long:**
   a. From the technical analysis, check if the current price is at or within 3%
      above a proximate support level (per technical_level_analysis.md definition).
   b. From the news file, check whether any item published in the last 3 days
      contains negative sentiment for the asset.
   c. If both conditions are met → recommendation: ENTRAR EN LARGO.
4. If no principle is triggered → output: SIN SEÑAL.
5. Do NOT confirm a principle without verifying both of its conditions explicitly.
6. Do NOT state price targets, stop-loss levels, or position sizing.
7. Write all output in Spanish.

## Reference

- `Agents/Technical_Analysis/Skills/technical_level_analysis.md` — proximate support
  definition (within 3% of current price).
- `Agents/Skills/poc_analysis.md` — congestion zone logic for support/resistance.

## Output

    Principio activado: <nombre del principio o "Ninguno">
    Condiciones verificadas:
      - Soporte próximo: <sí/no — nivel, distancia%>
      - Noticia negativa: <sí/no — titular>
    Recomendación: <ENTRAR EN LARGO / SIN SEÑAL>
