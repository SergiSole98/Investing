---
name: fuentes-datos-financieros
description: |
  USAR SIEMPRE que necesites buscar datos financieros específicos (put/call ratio, 
  flujos institucionales, niveles técnicos, sentimiento). Contiene el mapa exacto 
  de dónde encontrar cada dato con queries óptimas. Sin esta skill, las búsquedas 
  serán ineficientes y perderás datos críticos.
triggers:
  - put/call
  - flujos institucionales
  - 13F
  - niveles técnicos
  - Fear & Greed
  - VIX
  - soportes
  - resistencias
---

# Fuentes de Datos Financieros

## Cuándo Usar Esta Skill

Cuando Nora, Alex o Laia necesiten buscar datos financieros específicos y no sepan dónde encontrarlos.

## Mapa de Fuentes por Tipo de Dato

### Posicionamiento del Dinero

| Dato | Fuente | Query óptima | Fiabilidad |
|------|--------|--------------|------------|
| **Put/Call Ratio** | CBOE, Barchart | `"{ticker} put call ratio"` | ⭐⭐⭐ |
| **Flujos Institucionales** | WhaleWisdom, 13F filings | `"{ticker} 13F filings 2026"` o `"institutional ownership {ticker}"` | ⭐⭐⭐ |
| **Short Interest** | FINRA, Fintel | `"{ticker} short interest"` | ⭐⭐⭐ |
| **Curva de Futuros** | CME Group, Investing.com | `"{commodity} futures curve contango backwardation"` | ⭐⭐⭐ |
| **Dark Pool Activity** | Fintel, Unusual Whales | `"{ticker} dark pool"` | ⭐⭐ |

### Niveles Técnicos

| Dato | Fuente | Query óptima | Fiabilidad |
|------|--------|--------------|------------|
| **Soportes/Resistencias** | TradingView, Investing.com | `"{ticker} support resistance levels"` | ⭐⭐ |
| **Medias Móviles** | TradingView, Yahoo Finance | `"{ticker} moving average 50 200"` | ⭐⭐⭐ |
| **RSI, MACD** | TradingView, Investing.com | `"{ticker} technical indicators RSI"` | ⭐⭐ |
| **Volumen** | Yahoo Finance, TradingView | `"{ticker} volume analysis"` | ⭐⭐⭐ |

### Sentimiento

| Dato | Fuente | Query óptima | Fiabilidad |
|------|--------|--------------|------------|
| **Fear & Greed Index** | CNN Business | `"fear greed index CNN"` | ⭐⭐ |
| **VIX** | CBOE, Yahoo Finance | `"VIX index"` | ⭐⭐⭐ |
| **Analyst Ratings** | TipRanks, Yahoo Finance | `"{ticker} analyst ratings"` | ⭐⭐ |
| **Social Sentiment** | StockTwits, Reddit (con cautela) | `"{ticker} sentiment"` | ⭐ |

### Fundamentales (contexto)

| Dato | Fuente | Query óptima | Fiabilidad |
|------|--------|--------------|------------|
| **Earnings** | Earnings Whispers, Yahoo Finance | `"{ticker} earnings date"` | ⭐⭐⭐ |
| **Guidance** | SEC filings, Reuters | `"{ticker} guidance 2026"` | ⭐⭐⭐ |
| **Insider Trading** | SEC Form 4, OpenInsider | `"{ticker} insider trading"` | ⭐⭐⭐ |

### España / IBEX

| Dato | Fuente | Query óptima | Fiabilidad |
|------|--------|--------------|------------|
| **Precio IBEX** | Investing.com, Bolsa de Madrid | `"IBEX 35 cotización"` | ⭐⭐⭐ |
| **Noticias banca** | Reuters ES, Expansión | `"{banco} noticias 2026"` | ⭐⭐⭐ / ⭐⭐ |
| **Resultados empresas** | CNMV, web corporativa | `"{empresa} resultados 2026 CNMV"` | ⭐⭐⭐ |
| **Posiciones cortas** | CNMV | `"posiciones cortas CNMV {empresa}"` | ⭐⭐⭐ |

## Estrategia de Búsqueda

1. **Empieza por la fuente primaria** (⭐⭐⭐) antes de usar agregadores
2. **Si no encuentras**, simplifica la query y añade el nombre de la fuente: `"put call ratio CBOE"`
3. **Para datos históricos**, añade el período: `"{ticker} 13F Q4 2025"`
4. **Para comparar**, busca el sector: `"{ticker} vs sector put call ratio"`

## Errores Comunes

1. **Buscar en español datos de USA** → Siempre en inglés para mercados americanos
2. **No especificar período** → Los datos sin fecha pueden ser obsoletos
3. **Confiar en agregadores sin verificar** → Cruza con fuente primaria si es dato crítico

---

**Tokens:** ~750
**Última actualización:** 2026-03-21
**Basada en:** Gaps identificados en auditoría de Iris
