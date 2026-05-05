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
│   └── investing-system.mdc    # Reglas del proyecto (objetivo, docs)
├── Agents/
│   ├── Invest_Analysis/
│   │   ├── agent_investm_analysis.md  # Delega: Setup -> (News + Events en paralelo)
│   │   ├── Setup/
│   │   │   └── generate_analisis.md   # Crea Analisis/<nombre>/
│   │   ├── News/
│   │   │   └── news_researcher.md     # Escribe Analisis/<nombre>/News/news.md
│   │   └── Events/
│   │       └── event_scanner.md       # Escribe Analisis/<nombre>/Events/events.md
│   ├── Invest_Research/
│   ├── Technical_Analysis/
│   ├── Skills/
│   └── Improvement_agents/            # Solo referencias a /Users/ssole/Documents/Agents
├── Analisis/
│   └── {nombre}/
│       ├── News/news.md
│       ├── Events/events.md
│       └── Technical_analysis/
└── basic/
    ├── tesis_inversion.md
    └── principios/
```

## Meta-agentes

Los agentes que crean, auditan o modifican otros agentes viven fuera de este proyecto.

| Necesidad | Agente canónico |
|---|---|
| Crear specs de agentes | `/Users/ssole/Documents/Agents/agent_spec_generator/agent_spec_generator.md` |
| Crear specs de skills | `/Users/ssole/Documents/Agents/skill_spec_generator/skill_spec_generator.md` |
| Auditar specs | `/Users/ssole/Documents/Agents/spec_compliance_auditor/spec_compliance_auditor.md` |
| Planificar cambios de workflow | `/Users/ssole/Documents/Agents/Agent_ai_planner/Agent_ai_planner.md` |
| Implementar un plan aprobado | `/Users/ssole/Documents/Agents/agent_ai_implementer/agent_ai_implementer.md` |

## Output Obligatorio

Todo análisis termina en: **GO / NO GO / WAIT**

No "depende". No ambigüedades.
