# Pipeline de Análisis

Flujo de cómo el equipo analiza un tema de inversión. El detalle de cada agente está en su propio archivo.

---

## Flujo Visual

```
┌─────────────────────────────────────────────────────────────────┐
│                         USUARIO                                 │
│                    "Analiza [TEMA]"                             │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PASO 1: MARCO                              │
│                     (Orquestador)                               │
│  • Crea carpeta si no existe                                    │
│  • Lee los prompts de los agentes                               │
│  • Decide qué agentes lanzar                                    │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PASO 2: PAULA                              │
│              (Planificadora de Investigación)                    │
│   agente_planificadora.md                                       │
│   Lee los 15 principios + sus inputs requeridos                 │
│   Genera briefing con preguntas específicas para Nora y Alex    │
│   → 00_briefing/YYYY-MM-DD.md                                   │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                        ┌─────────┴─────────┐
                        │                   │
                        ▼                   ▼
┌───────────────────────────┐   ┌───────────────────────────┐
│      PASO 3A: NORA        │   │      PASO 3B: ALEX        │
│   (Busca noticias)        │   │   (Análisis técnico)      │
│   Recibe briefing Paula   │   │   Recibe briefing Paula   │
│   agente_noticias.md      │   │   agente_analisis.md      │
│   → 01_noticias/bruto_    │   │   → 02_analisis/          │
└─────────────┬─────────────┘   └─────────────┬─────────────┘
              │       EN PARALELO              │
              └───────────┬────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PASO 4: LAIA                               │
│           (Filtra y analiza noticias de Nora)                   │
│   agente_filtro_noticias.md                                     │
│   Recibe: output de Nora                                        │
│   → 01_noticias/YYYY-MM-DD.md                                   │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PASO 5: VERA                               │
│              (Validadora de Inputs)                              │
│   agente_validadora.md                                          │
│   Recibe: briefing Paula + outputs Laia + Alex                  │
│   Compara inputs requeridos vs datos obtenidos                  │
│   → PASS: continúa a Sergi                                      │
│   → REJECT: devuelve a Nora/Alex con instrucciones específicas  │
│   (máximo 2 rondas de re-trabajo)                               │
└──────────┬──────────────────────────────────┬───────────────────┘
           │ PASS                             │ REJECT
           ▼                                  ▼
┌──────────────────────────┐   ┌──────────────────────────────────┐
│      PASO 6: SERGI       │   │   VUELTA A PASO 3A/3B/4         │
│   (Estratega — DECIDE)   │   │   Nora/Alex re-trabajan con     │
│   agente_estratega.md    │   │   instrucciones específicas      │
│   Recibe: Laia + Alex    │   │   de Vera                        │
│   + notas de Vera        │   │   → Vuelve a PASO 5 (Vera)      │
│   → 02_analisis/         │   └──────────────────────────────────┘
│     estrategia_          │
└──────────┬───────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                       PASO 7: LEO                               │
│                      (Redactor)                                 │
│   agente_redactor.md                                            │
│   Recibe: SOLO output de Sergi                                  │
│   → 03_sintesis/YYYY-MM-DD.md                                   │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                         USUARIO                                 │
│              GO / NO GO / WAIT con plan concreto                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Flujo Resumido

```
Marco → Paula (planifica) → Nora + Alex (EN PARALELO) → Laia (filtra Nora) → Vera (valida) → Sergi (decide) → Leo (traduce)
                                    ↑                                              │
                                    └──────── REJECT (re-trabajo) ─────────────────┘
```

---

## Modos de Ejecución

| Modo | Trigger | Agentes | Flujo |
|------|---------|---------|-------|
| **Completo** | "Analiza X" | Todos | Paula → Nora + Alex → Laia → Vera → Sergi → Leo |
| **Solo buscar noticias** | "Nora, busca noticias de X" | Nora | Nora → guarda bruto |
| **Solo analizar noticias** | "Laia, analiza las noticias de X" | Laia | Lee último bruto de Nora → guarda |
| **Solo análisis técnico** | "Alex, analiza X" | Alex | Alex → guarda |
| **Solo estrategia** | "Sergi, cruza X" | Sergi | Lee últimos Laia+Alex → guarda |
| **Solo resumen** | "Leo, resúmeme X" | Leo | Lee último Sergi → guarda |
| **Auditoría de agente** | "Óscar, audita a X" | Óscar | Lee prompt del agente → genera informe de mejora |
| **Auditoría completa** | "Óscar, audita el sistema" | Óscar | Lee todos los prompts → prioriza mejoras |
| **Crear skill** | "Iris, crea skill para X" | Iris | Identifica gap → diseña skill → documenta |
| **Auditar skill** | "Iris, audita skill X" | Iris | Evalúa 9 principios → propone mejoras |
| **Proponer skills** | "Iris, observa y propón" | Iris | Observa agentes → documenta gaps → prioriza |

---

## Estructura de Carpetas

```
01_temas/{tema}/
├── 00_briefing/
│   └── YYYY-MM-DD.md                # Paula (briefing de investigación)
├── 01_noticias/
│   ├── bruto_YYYY-MM-DD.md          # Nora (noticias en bruto)
│   └── YYYY-MM-DD.md                # Laia (noticias filtradas y analizadas)
├── 02_analisis/
│   ├── YYYY-MM-DD.md                # Alex
│   └── estrategia_YYYY-MM-DD.md     # Sergi
└── 03_sintesis/
    └── YYYY-MM-DD.md                # Leo
```

---

## Responsabilidad de Cada Archivo

| Archivo | Responsabilidad ÚNICA |
|---------|----------------------|
| `investing-system.mdc` | Quién es Marco, qué agentes tiene, cómo los lanza |
| `tesis_inversion.md` | Horizonte, qué opero, cómo |
| `principios/principios_inversion.md` | Los 15 principios + inputs requeridos por principio |
| `principios/fiabilidad_indicadores.md` | Sistema de fiabilidad de indicadores |
| `principios/resumen_principios.md` | Tabla resumen rápido de los 15 principios |
| `agente_planificadora.md` | Cómo planifica Paula + formato briefing |
| `agente_noticias.md` | Cómo busca Nora + fuentes de noticias |
| `agente_filtro_noticias.md` | Cómo filtra y analiza Laia + test del detalle |
| `agente_analisis.md` | Playbook de 11 pasos de Alex + formato output |
| `agente_validadora.md` | Cómo valida Vera + protocolo de re-trabajo |
| `agente_estratega.md` | Cómo cruza Sergi + formato output + decide |
| `agente_redactor.md` | Cómo escribe Leo + formato output |
| `agente_auditor.md` | Cómo audita Óscar + 7 principios Anthropic |
| `agente_skills.md` | Cómo diseña Iris + 9 principios de skills |
| `pipeline.md` | Este archivo: flujo visual + modos de ejecución |

> **Regla:** cada pieza de información vive en UN solo sitio. Los demás referencian.
