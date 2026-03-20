# Sistema de Análisis de Inversión

Sistema jerárquico de agentes para investigación y análisis de temas de inversión.

## Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENTE GENERAL                           │
│              (Orquestador / Coordinador)                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┬─────────────┐
        │             │             │             │
        ▼             ▼             ▼             ▼
   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
   │NOTICIAS │  │FUNDAMENT│  │ RIESGO  │  │ TÉCNICO │
   │         │  │   AL    │  │         │  │(opcional)│
   └─────────┘  └─────────┘  └─────────┘  └─────────┘
        │             │             │             │
        └─────────────┴─────────────┴─────────────┘
                      │
                      ▼
              ┌───────────────┐
              │   ORQUESTADOR │
              │  (consolida)  │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │   REDACTOR    │
              │ (doc. final)  │
              └───────────────┘
```

## Flujo de Ejecución

1. **Entrada**: Usuario proporciona un tema (ej: "semiconductores", "energía solar")
2. **Orquestador** crea carpeta del tema si no existe
3. **Ejecución paralela** de agentes especializados:
   - Noticias: busca información reciente
   - Fundamental: analiza negocio y valoración
   - Riesgo: evalúa amenazas y escenarios adversos
   - Técnico: (opcional) señales de precio/volumen
4. **Consolidación**: Orquestador integra resultados de todos los agentes
5. **Redacción**: Agente Redactor transforma la síntesis en documento ejecutivo
6. **Persistencia**: Guarda resultados en estructura `.md`

### Diferencia Orquestador vs Redactor

| Orquestador | Redactor |
|-------------|----------|
| Coordina agentes | Recibe output consolidado |
| Resuelve conflictos entre datos | Simplifica y clarifica |
| Genera síntesis técnica | Genera documento accionable |
| Foco: completitud | Foco: claridad y decisión |

## Estructura de Carpetas

```
Investing/
├── README.md                    # Este archivo
├── 00_meta/
│   ├── agente_general.md        # Protocolo del orquestador
│   ├── agente_noticias.md       # Definición agente noticias
│   ├── agente_fundamental.md    # Definición agente fundamental
│   ├── agente_riesgo.md         # Definición agente riesgo
│   ├── agente_tecnico.md        # Definición agente técnico
│   ├── agente_redactor.md       # Definición agente redactor
│   └── criterios_analisis.md    # Criterios de evaluación
├── 01_temas/
│   └── {nombre_tema}/
│       ├── 00_overview.md       # Resumen del tema
│       ├── 01_noticias/         # Reportes de noticias
│       ├── 02_fundamental/      # Análisis fundamental
│       ├── 03_riesgo/           # Análisis de riesgos
│       ├── 04_tecnico/          # Análisis técnico
│       ├── 05_sintesis/         # Síntesis consolidada
│       └── 06_fuentes/          # Referencias y fuentes
└── 99_templates/
    ├── plantilla_noticias.md
    ├── plantilla_fundamental.md
    ├── plantilla_riesgo.md
    ├── plantilla_tecnico.md
    ├── plantilla_sintesis.md
    └── plantilla_final.md       # Output del Redactor
```

## Uso

Para analizar un nuevo tema:

```
Analiza el tema: [NOMBRE_TEMA]
```

El sistema automáticamente:
1. Creará la estructura de carpetas
2. Ejecutará los agentes en paralelo
3. Consolidará los resultados
4. Generará la síntesis final

## Reglas de Ejecución

| Situación | Agentes a ejecutar | Modo |
|-----------|-------------------|------|
| Tema nuevo | Todos | Paralelo |
| Actualización rutinaria | Noticias + Riesgo | Paralelo |
| Evento específico | Noticias → Fundamental | Secuencial |
| Revisión completa | Todos → Síntesis | Paralelo + Secuencial |
