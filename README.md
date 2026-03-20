# Sistema de Análisis de Inversión

Sistema de chat con subagentes reales para análisis de inversión de corto plazo (max 7 días).

## Cómo Funciona

Habla con el equipo. Cursor lanza subagentes reales que trabajan en paralelo.

```
Tú: "Analiza NVIDIA"

Marco (orquestador) lanza:
  ├── Nora (subagente) → busca noticias      ─┐ EN PARALELO
  └── Alex (subagente) → playbook 11 pasos   ─┘
                                │
                    Leo (subagente) → simplifica
                                │
                    Documento final con GO / NO GO / WAIT
```

## El Equipo

| Nombre | Puesto | Tipo | Cómo hablarle |
|--------|--------|------|---------------|
| **Marco** | Orquestador | Agente principal | "Marco, analiza X" / "Analiza X" |
| **Nora** | Analista de Noticias | Subagente | "Nora, ¿qué hay de nuevo en X?" |
| **Alex** | Director de Análisis | Subagente | "Alex, analiza X" / "Alex, ¿entro en X?" |
| **Leo** | Redactor Ejecutivo | Subagente | "Leo, resúmeme X" / "Leo, simplifícame esto" |

## Diferencia vs Antes

| Antes | Ahora |
|-------|-------|
| Yo hacía todo secuencialmente | Nora y Alex trabajan en paralelo (subagentes reales) |
| Un solo contexto para todo | Cada subagente tiene su propio contexto limpio |
| Leo era una "personalidad" | Leo es un subagente real que recibe inputs consolidados |

## Modos de Uso

| Dices | Qué pasa |
|-------|----------|
| "Analiza X" | Marco lanza Nora + Alex en paralelo, luego Leo |
| "Nora, busca noticias de X" | Solo Nora trabaja |
| "Alex, ¿entro en X?" | Solo Alex ejecuta playbook |
| "Leo, resúmeme el último análisis" | Solo Leo simplifica |

## Estructura de Carpetas

```
Investing/
├── .cursor/rules/
│   └── investing-system.mdc    # Regla que define a Marco como orquestador
├── 00_meta/
│   ├── agente_noticias.md      # Prompt de Nora (se pasa al subagente)
│   ├── agente_analisis.md      # Prompt de Alex (incluye playbook + principios)
│   ├── agente_redactor.md      # Prompt de Leo
│   ├── agente_general.md       # Definición de Marco
│   ├── principios_inversion.md # Los 15 principios
│   ├── playbook_analisis.md    # Los 11 pasos detallados
│   └── pipeline.md             # Flujo de trabajo
├── 01_temas/
│   └── {activo}/
│       ├── 01_noticias/        # Output de Nora
│       ├── 02_analisis/        # Output de Alex
│       └── 03_sintesis/        # Output de Leo
└── 99_templates/
    ├── plantilla_noticias.md
    ├── plantilla_onepager.md
    ├── plantilla_sintesis.md
    ├── plantilla_final.md
    └── plantilla_overview.md
```

## Output Obligatorio

Todo análisis termina en: **GO / NO GO / WAIT**

No "depende". No ambigüedades.
