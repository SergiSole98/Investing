---
name: estrategia-busqueda-noticias
description: |
  USAR SIEMPRE antes de hacer búsquedas de noticias o datos financieros. Contiene 
  el protocolo amplio→estrecho que evita queries largas que devuelven 0 resultados. 
  Incluye ejemplos de queries que fallan y cómo arreglarlas. Sin esta skill, 
  perderás tiempo en búsquedas ineficientes.
triggers:
  - WebSearch
  - buscar noticias
  - no encuentro
  - 0 resultados
  - query
---

# Estrategia de Búsqueda: Amplio → Estrecho

## Cuándo Usar Esta Skill

Antes de cualquier búsqueda de noticias o datos. Especialmente útil cuando:
- No sabes qué cobertura hay sobre un tema
- Tus búsquedas anteriores dieron pocos resultados
- El activo es poco conocido o de nicho

## El Protocolo Amplio → Estrecho

### Fase 1: Exploración (2-3 queries cortas)

**Objetivo:** Descubrir qué hay disponible, no encontrar todo.

```
"{activo} news 2026"
"{activo} stock"
"{activo} {sector}"
```

**Evalúa:**
- ¿Qué medios cubren este activo?
- ¿Qué ángulos tienen cobertura (earnings, regulatorio, M&A)?
- ¿Qué ángulos están vacíos?

### Fase 2: Profundización (3-5 queries específicas)

**Objetivo:** Ir a fondo SOLO donde hay señal.

```
"{activo} earnings site:reuters.com"
"{activo} {ángulo específico} 2026"
"{persona clave} {activo}"
```

**Solo profundiza si:**
- La Fase 1 mostró resultados prometedores en ese ángulo
- Es una pregunta CRÍTICA del briefing de Paula

### Fase 3: Verificación (1-2 queries de cruce)

**Objetivo:** Confirmar datos importantes con segunda fuente.

```
"{dato específico} site:{otra fuente}"
"{evento} {fecha exacta}"
```

## Queries que FALLAN (evitar)

### ❌ Demasiado específica desde el inicio

```
"TSLA Q4 2025 earnings revenue guidance analyst estimates March 2026"
```
→ 0 resultados (demasiados términos)

### ✅ Mejor

```
Fase 1: "TSLA earnings 2025"
Fase 2: "TSLA Q4 results" → "TSLA guidance 2026 site:reuters.com"
```

### ❌ Demasiados filtros de fuente

```
"{activo} news marzo 2026 Reuters Bloomberg WSJ CNBC"
```
→ Pocos resultados (los motores no manejan bien múltiples sites)

### ✅ Mejor

```
Fase 1: "{activo} news 2026"
Fase 2: "{activo} site:reuters.com" (si Reuters apareció en Fase 1)
```

### ❌ Mezclar idiomas

```
"Santander resultados Q4 2025 earnings"
```
→ Confunde al motor de búsqueda

### ✅ Mejor

```
Para fuentes españolas: "Santander resultados 2025"
Para fuentes USA/UK: "Santander earnings 2025"
```

## Criterio de Parada

| Situación | Acción |
|-----------|--------|
| Últimas 2-3 búsquedas no añaden info nueva | PARAR |
| Cubriste todas las preguntas CRÍTICAS | PARAR |
| Hay preguntas CRÍTICAS sin respuesta | SEGUIR (hasta máx 12) |
| Ángulo prometedor merece más profundidad | SEGUIR |

## Qué Hacer Si No Encuentras Nada

1. **Simplifica** — Reduce a 2-3 palabras clave
2. **Cambia el ángulo** — Si "regulatorio" no da resultados, prueba "SEC" o "investigation"
3. **Amplía el período** — De "marzo 2026" a "2026"
4. **Prueba sinónimos** — "layoffs" vs "job cuts" vs "workforce reduction"
5. **Marca como gap** — Si después de 3 intentos no hay nada, es un gap real

## Heurística Final

> **Regla de los 3 términos:** Una query con más de 3-4 términos sustantivos probablemente devolverá pocos resultados. Empieza con menos, añade solo si necesitas filtrar.

---

**Tokens:** ~650
**Última actualización:** 2026-03-21
**Basada en:** Principio #3 de Anthropic (Amplio→Estrecho) + gaps en Nora/Alex
