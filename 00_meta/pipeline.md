# Pipeline de Análisis

Flujo definido de cómo el equipo analiza un tema de inversión.

---

## Resumen Visual

```
┌─────────────────────────────────────────────────────────────────┐
│                         USUARIO                                 │
│                    "Analiza [TEMA]"                             │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PASO 1: MARCO                              │
│                     (Orquestador)                               │
│  • Recibe el tema                                               │
│  • Crea carpeta si no existe                                    │
│  • Decide qué agentes lanzar                                    │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
┌───────────────────────┐   ┌───────────────────────┐
│      PASO 2A: NORA    │   │      PASO 2B: ALEX    │
│      (Noticias)       │   │      (Análisis)       │
│  • WebSearch          │   │  • Fundamental        │
│  • Últimas noticias   │   │  • Valoración         │
│  • Señales/narrativas │   │  • Riesgos            │
│  • Guarda en          │   │  • Timing             │
│    01_noticias/       │   │  • Guarda en          │
│                       │   │    02_analisis/       │
└───────────┬───────────┘   └───────────┬───────────┘
            │       EN PARALELO         │
            └───────────┬───────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PASO 3: MARCO                              │
│                    (Consolidación)                              │
│  • Recibe output de Nora y Alex                                 │
│  • Integra información                                          │
│  • Resuelve contradicciones                                     │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       PASO 4: LEO                               │
│                      (Redactor)                                 │
│  • Recibe síntesis de Marco                                     │
│  • Simplifica y estructura                                      │
│  • Genera documento ejecutivo                                   │
│  • Guarda en 03_sintesis/                                       │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         USUARIO                                 │
│              Recibe análisis completo + recomendación           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Paso 1: Marco (Orquestador)

### Trigger
Usuario dice: "Analiza X", "Marco, analiza X", o similar.

### Acciones
1. **Verificar si existe** `01_temas/{tema}/`
   - Si NO existe → Crear estructura de carpetas
   - Si existe → Verificar última actualización

2. **Decidir modo de ejecución**:

| Situación | Modo | Agentes |
|-----------|------|---------|
| Tema nuevo | Completo | Nora + Alex → Leo |
| Última actualización > 7 días | Actualización | Nora + Alex → Leo |
| Última actualización < 7 días | Solo noticias | Nora |
| Usuario pide específico | Individual | El que pida |

3. **Lanzar agentes** en paralelo cuando aplique

### Output
- Carpeta creada (si nueva)
- Agentes lanzados

---

## Paso 2A: Nora (Noticias)

### Trigger
Marco la invoca, o usuario dice "Nora, ¿qué hay de nuevo en X?"

### Acciones
1. **Buscar noticias** con WebSearch:
   - "[tema] news last week"
   - "[tema] latest developments 2026"
   - "[tema] stock analysis"

2. **Filtrar** por relevancia para inversión:
   - ¿Afecta valoración?
   - ¿Cambia tesis?
   - ¿Nuevo catalizador/riesgo?

3. **Clasificar** cada noticia:
   - Señal: 🟢 BULLISH / 🔴 BEARISH / ⚪ NEUTRAL
   - Impacto: ALTO / MEDIO / BAJO

4. **Detectar narrativas** emergentes

5. **Guardar** en `01_temas/{tema}/01_noticias/YYYY-MM-DD.md`

### Output
- Archivo de noticias guardado
- Resumen para Marco

---

## Paso 2B: Alex (Análisis)

### Trigger
Marco lo invoca, o usuario dice "Alex, analiza X"

### Acciones
1. **Entender el negocio**:
   - ¿Qué hace? ¿Cómo gana dinero?
   - ¿Tiene moat?

2. **Analizar métricas** (si hay datos disponibles):
   - Crecimiento, márgenes, ROIC
   - Deuda, FCF

3. **Valorar**:
   - Múltiplos actuales vs histórico vs sector
   - Estimar valor justo

4. **Identificar riesgos**:
   - Críticos (pueden romper tesis)
   - A monitorizar

5. **Evaluar timing** (si aplica):
   - Tendencia, niveles clave

6. **Emitir recomendación**:
   - COMPRAR / MANTENER / VENDER / WATCHLIST
   - Convicción: ALTA / MEDIA / BAJA
   - Sizing, entrada, stop-loss, target

7. **Guardar** en `01_temas/{tema}/02_analisis/YYYY-MM-DD.md`

### Output
- Archivo de análisis guardado
- Resumen para Marco

---

## Paso 3: Marco (Consolidación)

### Trigger
Nora y Alex terminan sus análisis.

### Acciones
1. **Recibir outputs** de Nora y Alex

2. **Integrar información**:
   - ¿Las noticias confirman o contradicen el análisis?
   - ¿Hay información nueva que cambie la tesis?

3. **Resolver contradicciones**:
   - Ponderar por recencia (noticias > histórico)
   - Ponderar por severidad (riesgo crítico tiene peso)

4. **Preparar síntesis** para Leo

### Output
- Síntesis consolidada para Leo

---

## Paso 4: Leo (Redactor)

### Trigger
Marco le pasa la síntesis, o usuario dice "Leo, simplifícame esto"

### Acciones
1. **Simplificar** jerga financiera

2. **Estructurar** con pirámide invertida:
   - Decisión + Acción (primero)
   - Razones principales
   - Evidencia de soporte
   - Detalles (último)

3. **Incluir siempre**:
   - Recomendación clara
   - Qué hacer concretamente
   - Sizing y niveles
   - Riesgos principales

4. **Guardar** en `01_temas/{tema}/03_sintesis/YYYY-MM-DD.md`

### Output
- Documento ejecutivo final
- Respuesta al usuario

---

## Modos de Ejecución Alternativos

### Solo Noticias
```
Usuario: "Nora, ¿qué hay de nuevo en X?"
→ Solo Nora trabaja
→ Guarda en 01_noticias/
→ Responde directamente
```

### Solo Análisis
```
Usuario: "Alex, analiza X a fondo"
→ Solo Alex trabaja
→ Guarda en 02_analisis/
→ Responde directamente
```

### Solo Resumen
```
Usuario: "Leo, resúmeme el último análisis de X"
→ Leo lee análisis existente
→ Genera resumen ejecutivo
→ Responde directamente
```

### Análisis Completo
```
Usuario: "Analiza X" o "Marco, analiza X"
→ Pipeline completo (Pasos 1-4)
→ Todos los archivos guardados
→ Documento final entregado
```

---

## Estructura de Carpetas Resultante

```
01_temas/{tema}/
├── 00_overview.md           # Ficha del tema (se actualiza)
├── 01_noticias/
│   ├── 2026-03-20.md        # Nora
│   └── 2026-03-27.md        # Nora (siguiente semana)
├── 02_analisis/
│   ├── 2026-03-20.md        # Alex
│   └── 2026-04-15.md        # Alex (siguiente revisión)
└── 03_sintesis/
    ├── 2026-03-20.md        # Leo
    └── 2026-04-15.md        # Leo (siguiente revisión)
```

---

## Frecuencia Recomendada

| Acción | Frecuencia | Quién |
|--------|------------|-------|
| Check de noticias | Semanal | Nora |
| Actualización de análisis | Mensual o post-evento | Alex |
| Síntesis completa | Trimestral o cuando cambie algo | Todos |
