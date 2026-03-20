# Sistema de Análisis de Inversión

Sistema de chat con agentes especializados para análisis de inversión. No es código, es conversación.

## Cómo Funciona

Simplemente **habla con el equipo**. Cursor ya sabe quién es cada uno gracias a las reglas en `.cursor/rules/`.

```
Tú: "Analiza NVIDIA"
Marco: Coordino el análisis, lanzo a Nora y Alex...

Tú: "Nora, ¿qué hay de nuevo en semiconductores?"
Nora: Busco las últimas noticias...

Tú: "Alex, ¿está cara Apple?"
Alex: Analizo la valoración...
```

## El Equipo

| Nombre | Puesto | Especialidad | Cómo hablarle |
|--------|--------|--------------|---------------|
| **Marco** | Orquestador | Coordina todo el flujo | "Marco, analiza X" |
| **Nora** | Analista de Noticias | Información reciente, señales | "Nora, ¿qué hay de nuevo en X?" |
| **Alex** | Director de Análisis | Análisis completo (fundamental + riesgo + técnico) | "Alex, analiza X a fondo" |
| **Leo** | Redactor Ejecutivo | Simplificar, comunicar | "Leo, hazme un resumen ejecutivo" |

> **Tip**: Puedes hablar directamente con cualquier empleado por su nombre, o pedirle a Marco que coordine un análisis completo.

## Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                       MARCO                                 │
│                   (Orquestador)                             │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
   ┌─────────┐                ┌─────────┐
   │  NORA   │                │  ALEX   │
   │(Noticias)│                │(Análisis)│
   └─────────┘                └─────────┘
        │                           │
        └─────────────┬─────────────┘
                      │
                      ▼
              ┌───────────────┐
              │     LEO       │
              │  (Redactor)   │
              └───────────────┘
```

## Flujo de Ejecución

1. **Entrada**: Usuario proporciona un tema (ej: "semiconductores", "energía solar")
2. **Marco** crea carpeta del tema si no existe
3. **Ejecución paralela**:
   - **Nora**: busca noticias e información reciente
   - **Alex**: hace análisis completo (fundamental + riesgo + técnico)
4. **Consolidación**: Marco integra resultados
5. **Redacción**: Leo transforma todo en documento ejecutivo
6. **Persistencia**: Guarda resultados en estructura `.md`

## Estructura de Carpetas

```
Investing/
├── README.md                    # Este archivo
├── 00_meta/
│   ├── agente_general.md        # Marco (orquestador)
│   ├── agente_noticias.md       # Nora (noticias)
│   ├── agente_analisis.md       # Alex (análisis completo)
│   ├── agente_redactor.md       # Leo (redactor)
│   └── criterios_analisis.md    # Criterios de evaluación
├── 01_temas/
│   └── {nombre_tema}/
│       ├── 00_overview.md       # Resumen del tema
│       ├── 01_noticias/         # Reportes de noticias (Nora)
│       ├── 02_analisis/         # Análisis completo (Alex)
│       ├── 03_sintesis/         # Síntesis consolidada
│       └── 04_fuentes/          # Referencias y fuentes
└── 99_templates/
    ├── plantilla_noticias.md    # Template de Nora
    ├── plantilla_analisis.md    # Template de Alex
    ├── plantilla_sintesis.md    # Template de síntesis
    └── plantilla_final.md       # Template de Leo
```

## Uso

Para analizar un nuevo tema:

```
Analiza el tema: [NOMBRE_TEMA]
```

El sistema automáticamente:
1. Creará la estructura de carpetas
2. Nora buscará noticias, Alex hará el análisis (en paralelo)
3. Marco consolidará los resultados
4. Leo generará el documento final

## Reglas de Ejecución

| Situación | Quién trabaja | Modo |
|-----------|---------------|------|
| Tema nuevo | Nora + Alex | Paralelo |
| Solo noticias | Nora | Individual |
| Análisis profundo | Alex | Individual |
| Resumen ejecutivo | Leo | Individual |
| Análisis completo | Todos | Marco coordina |
